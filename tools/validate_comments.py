#!/usr/bin/env python3
"""
Command-line tool for comment validation and standardization.

This tool provides CLI interface for validating and standardizing comments
in property-based test files, with integration to existing optimization scripts.
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

# Add the tools directory to the path for imports
sys.path.insert(0, os.path.dirname(__file__))

from test_optimization.comment_analyzer import CommentAnalyzer, DirectoryAnalysis
from test_optimization.comment_standardizer import CommentStandardizer, BatchResult
from test_optimization.file_analyzer import FileAnalyzer


class CommentValidationCLI:
    """Command-line interface for comment validation and standardization."""
    
    def __init__(self):
        """Initialize CLI with analysis and standardization tools."""
        self.comment_analyzer = CommentAnalyzer()
        self.comment_standardizer = CommentStandardizer()
        self.file_analyzer = FileAnalyzer()
    
    def create_parser(self) -> argparse.ArgumentParser:
        """Create command-line argument parser.
        
        Returns:
            Configured ArgumentParser instance
        """
        parser = argparse.ArgumentParser(
            description="Validate and standardize comments in property-based test files",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  # Validate comments in test directory
  python validate_comments.py validate kivy_garden/markdownlabel/tests/
  
  # Standardize comments (dry run)
  python validate_comments.py standardize kivy_garden/markdownlabel/tests/ --dry-run
  
  # Apply standardization with backup
  python validate_comments.py standardize kivy_garden/markdownlabel/tests/ --backup-dir ./backups
  
  # Generate detailed report
  python validate_comments.py report kivy_garden/markdownlabel/tests/ --output report.json
  
  # Integration with optimization tools
  python validate_comments.py optimize kivy_garden/markdownlabel/tests/ --include-comments
            """
        )
        
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # Validate command
        validate_parser = subparsers.add_parser(
            'validate', 
            help='Validate comment format compliance'
        )
        validate_parser.add_argument(
            'directory',
            help='Directory containing test files to validate'
        )
        validate_parser.add_argument(
            '--output', '-o',
            help='Output file for validation report (JSON format)'
        )
        validate_parser.add_argument(
            '--verbose', '-v',
            action='store_true',
            help='Show detailed validation results'
        )
        
        # Standardize command
        standardize_parser = subparsers.add_parser(
            'standardize',
            help='Standardize comment formats'
        )
        standardize_parser.add_argument(
            'directory',
            help='Directory containing test files to standardize'
        )
        standardize_parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be changed without modifying files'
        )
        standardize_parser.add_argument(
            '--backup-dir',
            help='Directory for backup files (default: auto-generated)'
        )
        standardize_parser.add_argument(
            '--output', '-o',
            help='Output file for standardization report (JSON format)'
        )
        
        # Report command
        report_parser = subparsers.add_parser(
            'report',
            help='Generate comprehensive analysis report'
        )
        report_parser.add_argument(
            'directory',
            help='Directory containing test files to analyze'
        )
        report_parser.add_argument(
            '--output', '-o',
            required=True,
            help='Output file for report (JSON format)'
        )
        report_parser.add_argument(
            '--include-optimization',
            action='store_true',
            help='Include optimization recommendations in report'
        )
        
        # Optimize command (integration with existing tools)
        optimize_parser = subparsers.add_parser(
            'optimize',
            help='Run optimization analysis with comment integration'
        )
        optimize_parser.add_argument(
            'directory',
            help='Directory containing test files to optimize'
        )
        optimize_parser.add_argument(
            '--include-comments',
            action='store_true',
            help='Include comment compliance in optimization report'
        )
        optimize_parser.add_argument(
            '--output', '-o',
            help='Output file for optimization report (JSON format)'
        )
        
        return parser
    
    def validate_comments(self, directory: str, output: Optional[str] = None, 
                         verbose: bool = False) -> int:
        """Validate comment format compliance in directory.
        
        Args:
            directory: Directory to validate
            output: Optional output file for report
            verbose: Show detailed results
            
        Returns:
            Exit code (0 for success, 1 for validation failures)
        """
        if not os.path.exists(directory):
            print(f"Error: Directory '{directory}' does not exist", file=sys.stderr)
            return 1
        
        print(f"Validating comments in: {directory}")
        
        try:
            analysis = self.comment_analyzer.analyze_directory(directory)
        except Exception as e:
            print(f"Error during analysis: {e}", file=sys.stderr)
            return 1
        
        # Display summary
        stats = analysis.summary_stats
        print(f"\nValidation Summary:")
        print(f"  Files analyzed: {analysis.analyzed_files}")
        print(f"  Total property tests: {stats.get('total_property_tests', 0)}")
        print(f"  Documented tests: {stats.get('total_documented_tests', 0)}")
        print(f"  Undocumented tests: {stats.get('total_undocumented_tests', 0)}")
        print(f"  Format violations: {stats.get('total_format_violations', 0)}")
        print(f"  Strategy mismatches: {stats.get('total_strategy_mismatches', 0)}")
        print(f"  Compliance: {stats.get('compliance_percentage', 0):.1f}%")
        
        # Show detailed results if requested
        if verbose:
            self._show_detailed_validation_results(analysis)
        
        # Save report if requested
        if output:
            self._save_validation_report(analysis, output)
            print(f"\nDetailed report saved to: {output}")
        
        # Determine exit code based on compliance
        has_issues = (
            stats.get('total_undocumented_tests', 0) > 0 or
            stats.get('total_format_violations', 0) > 0 or
            stats.get('total_strategy_mismatches', 0) > 0 or
            len(analysis.global_inconsistencies) > 0
        )
        
        if has_issues:
            print(f"\n⚠️  Validation found issues. Run with --verbose for details.")
            return 1
        else:
            print(f"\n✅ All comments are properly formatted and documented.")
            return 0
    
    def standardize_comments(self, directory: str, dry_run: bool = False,
                           backup_dir: Optional[str] = None,
                           output: Optional[str] = None) -> int:
        """Standardize comment formats in directory.
        
        Args:
            directory: Directory to standardize
            dry_run: Show changes without applying them
            backup_dir: Directory for backup files
            output: Optional output file for report
            
        Returns:
            Exit code (0 for success, 1 for errors)
        """
        if not os.path.exists(directory):
            print(f"Error: Directory '{directory}' does not exist", file=sys.stderr)
            return 1
        
        # Set up standardizer with custom backup directory if provided
        if backup_dir:
            standardizer = CommentStandardizer(backup_dir)
        else:
            standardizer = self.comment_standardizer
        
        print(f"{'Analyzing' if dry_run else 'Standardizing'} comments in: {directory}")
        
        # Find all test files
        test_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.startswith('test_') and file.endswith('.py'):
                    test_files.append(os.path.join(root, file))
        
        if not test_files:
            print("No test files found in directory")
            return 0
        
        try:
            result = standardizer.apply_standardization(test_files, dry_run=dry_run)
        except Exception as e:
            print(f"Error during standardization: {e}", file=sys.stderr)
            return 1
        
        # Display results
        print(f"\nStandardization {'Analysis' if dry_run else 'Results'}:")
        print(f"  Files processed: {result.total_files}")
        print(f"  Successful: {result.successful_files}")
        print(f"  Failed: {result.failed_files}")
        print(f"  Total changes: {result.total_changes}")
        
        if dry_run and result.total_changes > 0:
            print(f"\n📝 {result.total_changes} changes would be made. Run without --dry-run to apply.")
        elif not dry_run and result.total_changes > 0:
            print(f"\n✅ Applied {result.total_changes} standardization changes.")
            if backup_dir or standardizer.backup_dir:
                print(f"   Backups saved to: {backup_dir or standardizer.backup_dir}")
        elif result.total_changes == 0:
            print(f"\n✅ All comments are already properly standardized.")
        
        # Show errors if any
        if result.failed_files > 0:
            print(f"\n⚠️  {result.failed_files} files had errors:")
            for file_result in result.file_results:
                if not file_result.success:
                    print(f"  {file_result.file_path}: {', '.join(file_result.errors)}")
        
        # Save report if requested
        if output:
            self._save_standardization_report(result, output)
            print(f"\nDetailed report saved to: {output}")
        
        return 1 if result.failed_files > 0 else 0
    
    def generate_report(self, directory: str, output: str,
                       include_optimization: bool = False) -> int:
        """Generate comprehensive analysis report.
        
        Args:
            directory: Directory to analyze
            output: Output file for report
            include_optimization: Include optimization recommendations
            
        Returns:
            Exit code (0 for success, 1 for errors)
        """
        if not os.path.exists(directory):
            print(f"Error: Directory '{directory}' does not exist", file=sys.stderr)
            return 1
        
        print(f"Generating comprehensive report for: {directory}")
        
        try:
            # Comment analysis
            comment_analysis = self.comment_analyzer.analyze_directory(directory)
            
            report_data = {
                'directory': directory,
                'comment_analysis': self._serialize_comment_analysis(comment_analysis),
                'generated_at': self._get_timestamp()
            }
            
            # Add optimization analysis if requested
            if include_optimization:
                optimization_report = self.file_analyzer.validate_test_suite(directory)
                report_data['optimization_analysis'] = self._serialize_optimization_report(optimization_report)
            
            # Save report
            with open(output, 'w') as f:
                json.dump(report_data, f, indent=2)
            
            print(f"✅ Report generated: {output}")
            return 0
            
        except Exception as e:
            print(f"Error generating report: {e}", file=sys.stderr)
            return 1
    
    def run_optimization_with_comments(self, directory: str, include_comments: bool = False,
                                     output: Optional[str] = None) -> int:
        """Run optimization analysis with comment integration.
        
        Args:
            directory: Directory to analyze
            include_comments: Include comment compliance in report
            output: Optional output file for report
            
        Returns:
            Exit code (0 for success, 1 for errors)
        """
        if not os.path.exists(directory):
            print(f"Error: Directory '{directory}' does not exist", file=sys.stderr)
            return 1
        
        print(f"Running optimization analysis for: {directory}")
        
        try:
            report = self.file_analyzer.validate_test_suite(directory)
            
            # Display optimization summary
            print(f"\nOptimization Analysis:")
            print(f"  Total tests: {report.total_tests}")
            print(f"  Over-tested: {report.total_over_tested}")
            print(f"  Potential time savings: {report.potential_time_savings_percent:.1f}%")
            print(f"  Estimated time reduction: {report.estimated_time_reduction_seconds:.1f}s")
            
            # Display comment compliance if included
            if include_comments and report.overall_comment_compliance:
                compliance = report.overall_comment_compliance
                print(f"\nComment Compliance:")
                print(f"  Documented tests: {compliance.documented_tests}/{compliance.total_property_tests}")
                print(f"  Compliance rate: {compliance.compliance_percentage:.1f}%")
                print(f"  Format violations: {compliance.format_violations}")
            
            # Save report if requested
            if output:
                report_data = {
                    'directory': directory,
                    'optimization_report': self._serialize_optimization_report(report),
                    'generated_at': self._get_timestamp()
                }
                
                with open(output, 'w') as f:
                    json.dump(report_data, f, indent=2)
                
                print(f"\nDetailed report saved to: {output}")
            
            return 0
            
        except Exception as e:
            print(f"Error during optimization analysis: {e}", file=sys.stderr)
            return 1
    
    def _show_detailed_validation_results(self, analysis: DirectoryAnalysis):
        """Show detailed validation results."""
        print(f"\nDetailed Results:")
        
        for file_analysis in analysis.file_analyses:
            if (file_analysis.format_violations or 
                file_analysis.missing_documentation or
                file_analysis.strategy_mismatches):
                print(f"\n📁 {file_analysis.file_path}:")
                
                if file_analysis.missing_documentation:
                    print(f"  Missing documentation:")
                    for func_name, line_num, max_examples in file_analysis.missing_documentation:
                        print(f"    - {func_name} (line {line_num}): max_examples={max_examples}")
                
                if file_analysis.format_violations:
                    print(f"  Format violations:")
                    for violation in file_analysis.format_violations:
                        print(f"    - Line {violation.line_number}: {violation.message}")

                if file_analysis.strategy_mismatches:
                    print(f"  Strategy mismatches:")
                    for mismatch in file_analysis.strategy_mismatches:
                        print(f"    - {mismatch.function_name} (line {mismatch.line_number}): Documented='{mismatch.documented_type}', Implemented='{mismatch.implemented_type}'")
                        print(f"      Use: {mismatch.rationale}")


        
        if analysis.global_inconsistencies:
            print(f"\nGlobal Inconsistencies:")
            for inconsistency in analysis.global_inconsistencies:
                print(f"  - {inconsistency.inconsistency_type}: {inconsistency.description}")
    
    def _save_validation_report(self, analysis: DirectoryAnalysis, output: str):
        """Save validation report to JSON file."""
        report_data = {
            'directory': analysis.directory_path,
            'summary': analysis.summary_stats,
            'files': self._serialize_comment_analysis(analysis),
            'generated_at': self._get_timestamp()
        }
        
        with open(output, 'w') as f:
            json.dump(report_data, f, indent=2)
    
    def _save_standardization_report(self, result: BatchResult, output: str):
        """Save standardization report to JSON file."""
        report_data = {
            'summary': {
                'total_files': result.total_files,
                'successful_files': result.successful_files,
                'failed_files': result.failed_files,
                'total_changes': result.total_changes
            },
            'file_results': [
                {
                    'file_path': fr.file_path,
                    'success': fr.success,
                    'changes_made': fr.changes_made,
                    'errors': fr.errors,
                    'warnings': fr.warnings
                }
                for fr in result.file_results
            ],
            'global_errors': result.global_errors,
            'generated_at': self._get_timestamp()
        }
        
        with open(output, 'w') as f:
            json.dump(report_data, f, indent=2)
    
    def _serialize_comment_analysis(self, analysis: DirectoryAnalysis) -> Dict[str, Any]:
        """Serialize comment analysis to JSON-compatible format."""
        return {
            'directory_path': analysis.directory_path,
            'total_files': analysis.total_files,
            'analyzed_files': analysis.analyzed_files,
            'summary_stats': analysis.summary_stats,
            'file_analyses': [
                {
                    'file_path': fa.file_path,
                    'total_property_tests': fa.total_property_tests,
                    'documented_tests': fa.documented_tests,
                    'undocumented_tests': fa.undocumented_tests,
                    'format_violations': [
                        {
                            'line_number': fv.line_number,
                            'error_type': fv.error_type,
                            'message': fv.message,
                            'original_comment': fv.original_comment
                        }
                        for fv in fa.format_violations
                    ],
                    'missing_documentation': [
                        {
                            'function_name': md[0],
                            'line_number': md[1],
                            'max_examples': md[2]
                        }
                        for md in fa.missing_documentation
                    ]
                }
                for fa in analysis.file_analyses
            ],
            'global_inconsistencies': [
                {
                    'type': gi.inconsistency_type,
                    'description': gi.description,
                    'affected_files': gi.affected_files
                }
                for gi in analysis.global_inconsistencies
            ]
        }
    
    def _serialize_optimization_report(self, report) -> Dict[str, Any]:
        """Serialize optimization report to JSON-compatible format."""
        return {
            'total_tests': report.total_tests,
            'total_over_tested': report.total_over_tested,
            'potential_time_savings_percent': report.potential_time_savings_percent,
            'estimated_time_reduction_seconds': report.estimated_time_reduction_seconds,
            'overall_comment_compliance': (
                {
                    'total_property_tests': report.overall_comment_compliance.total_property_tests,
                    'documented_tests': report.overall_comment_compliance.documented_tests,
                    'undocumented_tests': report.overall_comment_compliance.undocumented_tests,
                    'format_violations': report.overall_comment_compliance.format_violations,
                    'compliance_percentage': report.overall_comment_compliance.compliance_percentage
                }
                if report.overall_comment_compliance else None
            ),
            'file_analyses': [
                {
                    'file_path': fa.file_path,
                    'total_tests': fa.total_tests,
                    'over_tested_count': fa.over_tested_count,
                    'potential_time_savings_percent': fa.potential_time_savings_percent,
                    'comment_compliance_stats': (
                        {
                            'total_property_tests': fa.comment_compliance_stats.total_property_tests,
                            'documented_tests': fa.comment_compliance_stats.documented_tests,
                            'undocumented_tests': fa.comment_compliance_stats.undocumented_tests,
                            'format_violations': fa.comment_compliance_stats.format_violations,
                            'compliance_percentage': fa.comment_compliance_stats.compliance_percentage
                        }
                        if fa.comment_compliance_stats else None
                    ),
                    'recommendations': [
                        {
                            'test_name': rec.test_name,
                            'line_number': rec.line_number,
                            'current_examples': rec.current_examples,
                            'recommended_examples': rec.recommended_examples,
                            'time_savings_percent': rec.time_savings_percent,
                            'strategy_type': rec.strategy_type,
                            'rationale': rec.rationale,
                            'needs_comment_update': rec.needs_comment_update
                        }
                        for rec in fa.recommendations
                    ]
                }
                for fa in report.file_analyses
            ]
        }
    
    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def run(self, args: List[str]) -> int:
        """Run the CLI with given arguments.
        
        Args:
            args: Command-line arguments
            
        Returns:
            Exit code
        """
        parser = self.create_parser()
        parsed_args = parser.parse_args(args)
        
        if not parsed_args.command:
            parser.print_help()
            return 1
        
        try:
            if parsed_args.command == 'validate':
                return self.validate_comments(
                    parsed_args.directory,
                    parsed_args.output,
                    parsed_args.verbose
                )
            elif parsed_args.command == 'standardize':
                return self.standardize_comments(
                    parsed_args.directory,
                    parsed_args.dry_run,
                    parsed_args.backup_dir,
                    parsed_args.output
                )
            elif parsed_args.command == 'report':
                return self.generate_report(
                    parsed_args.directory,
                    parsed_args.output,
                    parsed_args.include_optimization
                )
            elif parsed_args.command == 'optimize':
                return self.run_optimization_with_comments(
                    parsed_args.directory,
                    parsed_args.include_comments,
                    parsed_args.output
                )
            else:
                print(f"Unknown command: {parsed_args.command}", file=sys.stderr)
                return 1
                
        except KeyboardInterrupt:
            print("\nOperation cancelled by user", file=sys.stderr)
            return 1
        except Exception as e:
            print(f"Unexpected error: {e}", file=sys.stderr)
            return 1


def main():
    """Main entry point for the CLI tool."""
    cli = CommentValidationCLI()
    exit_code = cli.run(sys.argv[1:])
    sys.exit(exit_code)


if __name__ == '__main__':
    main()