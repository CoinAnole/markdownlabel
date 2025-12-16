#!/usr/bin/env python3
"""
Automated optimization script for applying max_examples recommendations.

This script applies the recommended max_examples optimizations with backup,
rollback capabilities, and syntax validation.
"""

import os
import sys
import re
import shutil
import json
import ast
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Optional

# Disable Kivy argument parsing
os.environ['KIVY_NO_ARGS'] = '1'

# Add the package to Python path
sys.path.insert(0, str(Path(__file__).parent))

from tools.test_optimization.test_file_analyzer import FileAnalyzer


class OptimizationApplier:
    """Applies max_examples optimizations with safety checks."""
    
    def __init__(self, backup_dir: str = "optimization_backups"):
        """Initialize with backup directory."""
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(exist_ok=True)
        self.applied_changes = []
        
    def apply_optimizations(self, 
                          recommendations: List,
                          strategy_filter: Optional[List[str]] = None,
                          dry_run: bool = False) -> Dict:
        """Apply optimization recommendations with safety checks.
        
        Args:
            recommendations: List of optimization recommendations
            strategy_filter: Only apply optimizations for these strategy types
            dry_run: If True, show what would be changed without applying
            
        Returns:
            Dictionary with results of the operation
        """
        results = {
            'total_recommendations': len(recommendations),
            'applied_count': 0,
            'skipped_count': 0,
            'failed_count': 0,
            'backup_created': False,
            'changes': [],
            'errors': []
        }
        
        # Filter recommendations if strategy filter is provided
        if strategy_filter:
            filtered_recs = [
                r for r in recommendations 
                if r['strategy_type'] in strategy_filter
            ]
            print(f"Filtered to {len(filtered_recs)} recommendations for strategies: {strategy_filter}")
        else:
            filtered_recs = recommendations
        
        if not filtered_recs:
            print("No recommendations to apply after filtering.")
            return results
        
        # Create backup if not dry run
        if not dry_run:
            backup_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = self.backup_dir / f"backup_{backup_timestamp}"
            self._create_backup(filtered_recs, backup_path)
            results['backup_created'] = True
            results['backup_path'] = str(backup_path)
            print(f"Created backup at: {backup_path}")
        
        # Group recommendations by file for efficient processing
        file_groups = {}
        for rec in filtered_recs:
            file_path = rec['file_path']
            if file_path not in file_groups:
                file_groups[file_path] = []
            file_groups[file_path].append(rec)
        
        # Process each file
        for file_path, file_recs in file_groups.items():
            try:
                file_results = self._process_file(file_path, file_recs, dry_run)
                results['applied_count'] += file_results['applied_count']
                results['skipped_count'] += file_results['skipped_count']
                results['failed_count'] += file_results['failed_count']
                results['changes'].extend(file_results['changes'])
                results['errors'].extend(file_results['errors'])
                
            except Exception as e:
                error_msg = f"Failed to process file {file_path}: {str(e)}"
                results['errors'].append(error_msg)
                results['failed_count'] += len(file_recs)
                print(f"ERROR: {error_msg}")
        
        return results
    
    def _create_backup(self, recommendations: List, backup_path: Path):
        """Create backup of files that will be modified."""
        backup_path.mkdir(exist_ok=True)
        
        # Get unique file paths
        file_paths = set(rec['file_path'] for rec in recommendations)
        
        for file_path in file_paths:
            source_path = Path(file_path)
            if source_path.exists():
                # Preserve directory structure in backup
                if source_path.is_absolute():
                    relative_path = source_path.relative_to(source_path.anchor)
                else:
                    relative_path = source_path
                backup_file_path = backup_path / relative_path
                backup_file_path.parent.mkdir(parents=True, exist_ok=True)
                
                shutil.copy2(source_path, backup_file_path)
                print(f"Backed up: {file_path}")
    
    def _process_file(self, file_path: str, recommendations: List, dry_run: bool) -> Dict:
        """Process a single file with its recommendations."""
        results = {
            'applied_count': 0,
            'skipped_count': 0,
            'failed_count': 0,
            'changes': [],
            'errors': []
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
                
        except (IOError, UnicodeDecodeError) as e:
            error_msg = f"Could not read file {file_path}: {str(e)}"
            results['errors'].append(error_msg)
            results['failed_count'] = len(recommendations)
            return results
        
        # Sort recommendations by line number (descending) to avoid line number shifts
        sorted_recs = sorted(recommendations, key=lambda r: r['line_number'], reverse=True)
        
        modified_content = original_content
        lines = original_content.split('\n')
        
        for rec in sorted_recs:
            try:
                change_result = self._apply_single_change(
                    lines, rec, dry_run
                )
                
                if change_result['success']:
                    results['applied_count'] += 1
                    results['changes'].append(change_result['change_info'])
                    
                    if dry_run:
                        print(f"[DRY RUN] Would change {rec['test_name']}: "
                              f"{rec['current_examples']} → {rec['recommended_examples']}")
                    else:
                        print(f"Applied: {rec['test_name']}: "
                              f"{rec['current_examples']} → {rec['recommended_examples']}")
                else:
                    results['skipped_count'] += 1
                    results['errors'].append(change_result['error'])
                    print(f"Skipped {rec['test_name']}: {change_result['error']}")
                    
            except Exception as e:
                results['failed_count'] += 1
                error_msg = f"Failed to apply change to {rec['test_name']}: {str(e)}"
                results['errors'].append(error_msg)
                print(f"ERROR: {error_msg}")
        
        # Write modified content if not dry run and changes were made
        if not dry_run and results['applied_count'] > 0:
            modified_content = '\n'.join(lines)
            
            # Validate syntax before writing
            if self._validate_python_syntax(modified_content):
                try:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(modified_content)
                    print(f"Updated file: {file_path}")
                except IOError as e:
                    error_msg = f"Could not write file {file_path}: {str(e)}"
                    results['errors'].append(error_msg)
                    print(f"ERROR: {error_msg}")
            else:
                error_msg = f"Syntax validation failed for {file_path}, changes not applied"
                results['errors'].append(error_msg)
                results['failed_count'] += results['applied_count']
                results['applied_count'] = 0
                print(f"ERROR: {error_msg}")
        
        return results
    
    def _apply_single_change(self, lines: List[str], rec: Dict, dry_run: bool) -> Dict:
        """Apply a single max_examples change to the lines."""
        line_idx = rec['line_number'] - 1  # Convert to 0-based index
        
        if line_idx >= len(lines):
            return {
                'success': False,
                'error': f"Line number {rec['line_number']} out of range"
            }
        
        # Look for @settings decorator in the next few lines after @given
        settings_line_idx = None
        settings_pattern = r'@settings\(.*?max_examples\s*=\s*\d+.*?\)'
        
        # Search in a window around the reported line
        search_start = max(0, line_idx - 2)
        search_end = min(len(lines), line_idx + 5)
        
        for i in range(search_start, search_end):
            if re.search(settings_pattern, lines[i], re.DOTALL):
                settings_line_idx = i
                break
        
        if settings_line_idx is None:
            return {
                'success': False,
                'error': f"Could not find @settings with max_examples near line {rec['line_number']}"
            }
        
        original_line = lines[settings_line_idx]
        
        # Replace the max_examples value
        new_line = re.sub(
            r'max_examples\s*=\s*\d+',
            f'max_examples={rec["recommended_examples"]}',
            original_line
        )
        
        if not dry_run:
            lines[settings_line_idx] = new_line
        
        return {
            'success': True,
            'change_info': {
                'file_path': rec['file_path'],
                'line_number': settings_line_idx + 1,  # Convert back to 1-based
                'test_name': rec['test_name'],
                'original_line': original_line.strip(),
                'new_line': new_line.strip(),
                'old_examples': rec['current_examples'],
                'new_examples': rec['recommended_examples']
            }
        }
    
    def _validate_python_syntax(self, content: str) -> bool:
        """Validate that the modified content has valid Python syntax."""
        try:
            ast.parse(content)
            return True
        except SyntaxError:
            return False
    
    def rollback_changes(self, backup_path: str) -> bool:
        """Rollback changes from a backup directory."""
        backup_dir = Path(backup_path)
        
        if not backup_dir.exists():
            print(f"Backup directory {backup_path} does not exist")
            return False
        
        try:
            # Find all files in backup and restore them
            for backup_file in backup_dir.rglob('*.py'):
                # Calculate original file path
                relative_path = backup_file.relative_to(backup_dir)
                original_path = Path.cwd() / relative_path
                
                # Restore the file
                original_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(backup_file, original_path)
                print(f"Restored: {original_path}")
            
            print(f"Rollback completed from {backup_path}")
            return True
            
        except Exception as e:
            print(f"Rollback failed: {str(e)}")
            return False


def load_recommendations_from_analyzer() -> List[Dict]:
    """Load recommendations directly from analyzer (more complete than JSON)."""
    try:
        analyzer = FileAnalyzer()
        test_directory = "kivy_garden/markdownlabel/tests"
        
        # Generate fresh validation report
        report = analyzer.validate_test_suite(test_directory)
        
        # Extract all recommendations
        all_recommendations = []
        for file_analysis in report.file_analyses:
            for rec in file_analysis.recommendations:
                all_recommendations.append({
                    'test_name': rec.test_name,
                    'file_path': rec.file_path,
                    'line_number': rec.line_number,
                    'strategy_type': rec.strategy_type,
                    'current_examples': rec.current_examples,
                    'recommended_examples': rec.recommended_examples,
                    'time_savings_percent': rec.time_savings_percent,
                    'rationale': rec.rationale
                })
        
        return all_recommendations
        
    except Exception as e:
        print(f"Could not load recommendations from analyzer: {str(e)}")
        return []


def main():
    """Main script execution."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Apply max_examples optimizations')
    parser.add_argument('--dry-run', action='store_true', 
                       help='Show what would be changed without applying')
    parser.add_argument('--strategy-types', nargs='+', 
                       choices=['boolean', 'small_finite', 'medium_finite', 'combination', 'complex'],
                       help='Only apply optimizations for these strategy types')
    parser.add_argument('--report-file', default='optimization_report.json',
                       help='JSON report file to load recommendations from')
    parser.add_argument('--rollback', type=str,
                       help='Rollback changes from specified backup directory')
    
    args = parser.parse_args()
    
    applier = OptimizationApplier()
    
    # Handle rollback
    if args.rollback:
        success = applier.rollback_changes(args.rollback)
        sys.exit(0 if success else 1)
    
    # Load recommendations
    recommendations = load_recommendations_from_analyzer()
    
    if not recommendations:
        print("No recommendations found to apply.")
        sys.exit(1)
    
    print(f"Loaded {len(recommendations)} recommendations from {args.report_file}")
    
    # Apply optimizations
    results = applier.apply_optimizations(
        recommendations=recommendations,
        strategy_filter=args.strategy_types,
        dry_run=args.dry_run
    )
    
    # Print results summary
    print(f"\n" + "=" * 60)
    print("OPTIMIZATION RESULTS")
    print("=" * 60)
    print(f"Total recommendations: {results['total_recommendations']}")
    print(f"Applied successfully: {results['applied_count']}")
    print(f"Skipped: {results['skipped_count']}")
    print(f"Failed: {results['failed_count']}")
    
    if results['backup_created']:
        print(f"Backup created at: {results['backup_path']}")
    
    if results['errors']:
        print(f"\nErrors encountered:")
        for error in results['errors']:
            print(f"  - {error}")
    
    if not args.dry_run and results['applied_count'] > 0:
        print(f"\nTo rollback changes, run:")
        print(f"  python apply_optimizations.py --rollback {results.get('backup_path', 'optimization_backups/latest')}")
    
    # Exit with error code if there were failures
    sys.exit(1 if results['failed_count'] > 0 else 0)


if __name__ == "__main__":
    main()