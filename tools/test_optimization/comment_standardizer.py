"""Comment standardization tool for property-based test documentation.

This module provides automated comment generation and standardization based on
strategy analysis, with file modification capabilities and backup functionality.
"""

import os
import re
import shutil
from datetime import datetime
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Dict, Tuple

from .comment_analyzer import CommentAnalyzer, FileAnalysis
from .comment_format import CommentFormatValidator, CommentPattern, StrategyType
from .strategy_type_mapper import StrategyTypeMapper, TestCodeAnalyzer, CommentStrategyClassification
from .performance_rationale_handler import PerformanceAwareCommentStandardizer
from .ci_optimization_handler import CIOptimizationIntegrator


@dataclass
class StandardizationResult:
    """Result of standardizing a single file."""
    file_path: str
    success: bool
    changes_made: int
    backup_path: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    generated_comments: List[CommentPattern] = field(default_factory=list)


@dataclass
class BatchResult:
    """Result of batch standardization operation."""
    total_files: int
    successful_files: int
    failed_files: int
    total_changes: int
    file_results: List[StandardizationResult] = field(default_factory=list)
    global_errors: List[str] = field(default_factory=list)


class CommentStandardizer:
    """Automated comment generation and standardization tool."""
    
    def __init__(self, backup_dir: Optional[str] = None):
        """Initialize standardizer with analysis and validation tools.
        
        Args:
            backup_dir: Directory for backup files. If None, uses default backup location.
        """
        self.analyzer = CommentAnalyzer()
        self.validator = CommentFormatValidator()
        self.mapper = StrategyTypeMapper()
        self.code_analyzer = TestCodeAnalyzer()
        self.performance_standardizer = PerformanceAwareCommentStandardizer()
        self.ci_integrator = CIOptimizationIntegrator()
        
        # Set up backup directory
        if backup_dir is None:
            backup_dir = os.path.join(os.getcwd(), "optimization_backups", 
                                    f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        self.backup_dir = backup_dir
        
        # Standard max_examples values that typically don't need documentation
        self.standard_values = {2, 5, 10, 20, 50, 100}
        
        # Pattern to match @settings decorator with max_examples
        self.settings_pattern = re.compile(r'(@settings\([^)]*max_examples\s*=\s*\d+[^)]*\))', re.DOTALL)
        
        # Pattern to match @given decorator
        self.given_pattern = re.compile(r'(@given\([^)]*\))', re.DOTALL)
        
        # Pattern to match function definition
        self.function_pattern = re.compile(r'(def\s+test_\w+\s*\([^)]*\):)')
    
    def standardize_file(self, file_path: str, dry_run: bool = False) -> StandardizationResult:
        """Standardize comments in a single test file.
        
        Args:
            file_path: Path to the test file to standardize
            dry_run: If True, analyze but don't modify the file
            
        Returns:
            StandardizationResult with details of the standardization process
        """
        if not os.path.exists(file_path):
            return StandardizationResult(
                file_path=file_path,
                success=False,
                changes_made=0,
                errors=[f"File not found: {file_path}"]
            )
        
        try:
            # Read the file content
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
        except (IOError, UnicodeDecodeError) as e:
            return StandardizationResult(
                file_path=file_path,
                success=False,
                changes_made=0,
                errors=[f"Could not read file: {e}"]
            )
        
        # Analyze the file to identify what needs standardization
        analysis = self.analyzer.analyze_file(file_path)
        
        # Generate standardized content
        try:
            new_content, generated_comments, warnings = self._generate_standardized_content(
                original_content, analysis
            )
        except Exception as e:
            return StandardizationResult(
                file_path=file_path,
                success=False,
                changes_made=0,
                errors=[f"Error generating standardized content: {e}"]
            )
        
        changes_made = len(generated_comments)
        
        # If dry run, don't modify the file
        if dry_run:
            return StandardizationResult(
                file_path=file_path,
                success=True,
                changes_made=changes_made,
                warnings=warnings,
                generated_comments=generated_comments
            )
        
        # Create backup if changes will be made
        backup_path = None
        if changes_made > 0:
            try:
                backup_path = self._create_backup(file_path, original_content)
            except Exception as e:
                return StandardizationResult(
                    file_path=file_path,
                    success=False,
                    changes_made=0,
                    errors=[f"Could not create backup: {e}"]
                )
        
        # Write the standardized content
        if changes_made > 0:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
            except IOError as e:
                # Try to restore from backup if write failed
                if backup_path and os.path.exists(backup_path):
                    try:
                        shutil.copy2(backup_path, file_path)
                    except Exception:
                        pass  # Backup restoration failed, but original error is more important
                
                return StandardizationResult(
                    file_path=file_path,
                    success=False,
                    changes_made=0,
                    backup_path=backup_path,
                    errors=[f"Could not write standardized content: {e}"]
                )
        
        return StandardizationResult(
            file_path=file_path,
            success=True,
            changes_made=changes_made,
            backup_path=backup_path,
            warnings=warnings,
            generated_comments=generated_comments
        )
    
    def generate_comment(self, strategy_type: str, max_examples: int, 
                        input_space_size: Optional[int] = None) -> str:
        """Generate a standardized comment for given parameters.
        
        Args:
            strategy_type: Type of strategy (Boolean, Small finite, etc.)
            max_examples: Number of examples to use
            input_space_size: Size of input space (for finite strategies)
            
        Returns:
            Standardized comment string
        """
        try:
            # Convert string to StrategyType enum
            strategy_enum = None
            for enum_val in StrategyType:
                if enum_val.value.lower() == strategy_type.lower():
                    strategy_enum = enum_val
                    break
            
            if strategy_enum is None:
                # Default to Complex if unknown type
                strategy_enum = StrategyType.COMPLEX
            
            return self.validator.generate_standard_comment(
                strategy_enum, max_examples, input_space_size
            )
        except Exception as e:
            # Fallback to basic format
            return f"# {strategy_type} strategy: {max_examples} examples (adequate coverage)"
    
    def apply_standardization(self, files: List[str], dry_run: bool = False) -> BatchResult:
        """Apply standardization to multiple files.
        
        Args:
            files: List of file paths to standardize
            dry_run: If True, analyze but don't modify files
            
        Returns:
            BatchResult with summary of batch operation
        """
        file_results = []
        successful_files = 0
        failed_files = 0
        total_changes = 0
        global_errors = []
        
        # Ensure backup directory exists if not dry run
        if not dry_run:
            try:
                os.makedirs(self.backup_dir, exist_ok=True)
            except Exception as e:
                global_errors.append(f"Could not create backup directory: {e}")
                return BatchResult(
                    total_files=len(files),
                    successful_files=0,
                    failed_files=len(files),
                    total_changes=0,
                    file_results=[],
                    global_errors=global_errors
                )
        
        # Process each file
        for file_path in files:
            try:
                result = self.standardize_file(file_path, dry_run)
                file_results.append(result)
                
                if result.success:
                    successful_files += 1
                    total_changes += result.changes_made
                else:
                    failed_files += 1
                    
            except Exception as e:
                failed_files += 1
                file_results.append(StandardizationResult(
                    file_path=file_path,
                    success=False,
                    changes_made=0,
                    errors=[f"Unexpected error: {e}"]
                ))
        
        return BatchResult(
            total_files=len(files),
            successful_files=successful_files,
            failed_files=failed_files,
            total_changes=total_changes,
            file_results=file_results,
            global_errors=global_errors
        )
    
    def _generate_standardized_content(self, content: str, analysis: FileAnalysis) -> Tuple[str, List[CommentPattern], List[str]]:
        """Generate standardized content with proper comments.
        
        Args:
            content: Original file content
            analysis: File analysis result
            
        Returns:
            Tuple of (new_content, generated_comments, warnings)
        """
        lines = content.split('\n')
        generated_comments = []
        warnings = []
        
        # Process missing documentation
        for func_name, line_num, max_examples in analysis.missing_documentation:
            # Find the function in the content
            func_start_line = line_num - 1  # Convert to 0-based indexing
            
            # Extract the test function code for analysis
            func_code = self._extract_function_code(lines, func_start_line)
            if not func_code:
                warnings.append(f"Could not extract function code for {func_name} at line {line_num}")
                continue
            
            # Analyze the strategy type
            strategy_classification = self.code_analyzer.analyze_test_function(func_code)
            if not strategy_classification:
                warnings.append(f"Could not classify strategy for {func_name}, using default")
                strategy_classification = CommentStrategyClassification(
                    strategy_type=StrategyType.COMPLEX,
                    rationale="adequate coverage"
                )
            
            # Generate the comment with CI optimization and performance awareness
            comment_text = self.ci_integrator.generate_integrated_comment(func_code, max_examples)
            
            # Fall back to performance-aware comment if no CI optimization
            if not comment_text:
                comment_text = self.performance_standardizer.generate_comment_with_performance_awareness(
                    func_code, max_examples
                )
            
            # Find the best place to insert the comment (before @settings or @given)
            insert_line = self._find_comment_insertion_point(lines, func_start_line)
            
            # Insert the comment
            lines.insert(insert_line, comment_text)
            
            # Parse the generated comment to extract the actual rationale
            validation_result = self.validator.validate_comment_format(comment_text)
            if validation_result.is_valid and validation_result.parsed_pattern:
                # Use the parsed rationale from the actual generated comment
                actual_rationale = validation_result.parsed_pattern.rationale
                actual_strategy_type = validation_result.parsed_pattern.strategy_type
            else:
                # Fall back to strategy classification
                actual_rationale = strategy_classification.rationale
                actual_strategy_type = strategy_classification.strategy_type.value
            
            # Track the generated comment with the actual rationale
            generated_comments.append(CommentPattern(
                strategy_type=actual_strategy_type,
                max_examples=max_examples,
                rationale=actual_rationale,
                line_number=insert_line + 1,
                original_comment=None
            ))
        
        # Process format violations (replace malformed comments)
        for violation in analysis.format_violations:
            if violation.suggested_fix:
                # Find and replace the malformed comment
                violation_line = violation.line_number - 1  # Convert to 0-based
                if 0 <= violation_line < len(lines):
                    lines[violation_line] = violation.suggested_fix
                    
                    # Parse the suggested fix to track it
                    validation_result = self.validator.validate_comment_format(violation.suggested_fix)
                    if validation_result.is_valid and validation_result.parsed_pattern:
                        generated_comments.append(validation_result.parsed_pattern)
        
        new_content = '\n'.join(lines)
        return new_content, generated_comments, warnings
    
    def _extract_function_code(self, lines: List[str], func_start_line: int) -> str:
        """Extract the complete function code starting from the given line.
        
        Args:
            lines: List of file lines
            func_start_line: 0-based line number where function starts
            
        Returns:
            Complete function code as string
        """
        if func_start_line < 0 or func_start_line >= len(lines):
            return ""
        
        # Look backwards to find decorators
        start_line = func_start_line
        while start_line > 0:
            prev_line = lines[start_line - 1].strip()
            if prev_line.startswith('@') or prev_line == "":
                start_line -= 1
            else:
                break
        
        # Look forwards to find end of function
        end_line = func_start_line + 1
        while end_line < len(lines):
            line = lines[end_line]
            # Function ends when we hit another function/class or unindented code
            if (line.strip().startswith('def ') or 
                line.strip().startswith('class ') or
                (line.strip() and not line.startswith(' ') and not line.startswith('\t'))):
                break
            end_line += 1
        
        return '\n'.join(lines[start_line:end_line])
    
    def _find_comment_insertion_point(self, lines: List[str], func_start_line: int) -> int:
        """Find the best line to insert a comment before the function.
        
        Args:
            lines: List of file lines
            func_start_line: 0-based line number where function definition starts
            
        Returns:
            0-based line number where comment should be inserted
        """
        # Look backwards from function definition to find decorators
        insert_line = func_start_line
        
        # Check if there are decorators before the function
        check_line = func_start_line - 1
        while check_line >= 0:
            line = lines[check_line].strip()
            if line.startswith('@'):
                insert_line = check_line
                check_line -= 1
            elif line == "":
                # Skip empty lines
                check_line -= 1
            else:
                # Hit non-decorator, non-empty line
                break
        
        return insert_line
    
    def _create_backup(self, file_path: str, content: str) -> str:
        """Create a backup of the file before modification.
        
        Args:
            file_path: Path to the original file
            content: Content to backup
            
        Returns:
            Path to the backup file
        """
        # Ensure backup directory exists
        os.makedirs(self.backup_dir, exist_ok=True)
        
        # Generate backup filename
        original_name = os.path.basename(file_path)
        backup_name = f"{original_name}.backup"
        backup_path = os.path.join(self.backup_dir, backup_name)
        
        # Handle duplicate backup names
        counter = 1
        while os.path.exists(backup_path):
            backup_name = f"{original_name}.backup.{counter}"
            backup_path = os.path.join(self.backup_dir, backup_name)
            counter += 1
        
        # Write backup
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return backup_path
    
    def rollback_file(self, file_path: str, backup_path: str) -> bool:
        """Rollback a file to its backup version.
        
        Args:
            file_path: Path to the file to rollback
            backup_path: Path to the backup file
            
        Returns:
            True if rollback successful, False otherwise
        """
        try:
            if not os.path.exists(backup_path):
                return False
            
            shutil.copy2(backup_path, file_path)
            return True
        except Exception:
            return False
    
    def validate_standardization(self, file_path: str) -> bool:
        """Validate that a file has been properly standardized.
        
        Args:
            file_path: Path to the file to validate
            
        Returns:
            True if file is properly standardized, False otherwise
        """
        try:
            analysis = self.analyzer.analyze_file(file_path)
            
            # Check if there are any missing documentation or format violations
            has_missing_docs = len(analysis.missing_documentation) > 0
            has_violations = len(analysis.format_violations) > 0
            
            return not (has_missing_docs or has_violations)
        except Exception:
            return False
    
    def create_backup_directory(self) -> bool:
        """Create the backup directory if it doesn't exist.
        
        Returns:
            True if directory exists or was created successfully, False otherwise
        """
        try:
            os.makedirs(self.backup_dir, exist_ok=True)
            return True
        except Exception:
            return False
    
    def list_backups(self) -> List[str]:
        """List all backup files in the backup directory.
        
        Returns:
            List of backup file paths
        """
        try:
            if not os.path.exists(self.backup_dir):
                return []
            
            backup_files = []
            for file in os.listdir(self.backup_dir):
                if file.endswith('.backup') or '.backup.' in file:
                    backup_files.append(os.path.join(self.backup_dir, file))
            
            return sorted(backup_files)
        except Exception:
            return []
    
    def cleanup_old_backups(self, keep_count: int = 10) -> int:
        """Clean up old backup files, keeping only the most recent ones.
        
        Args:
            keep_count: Number of backup files to keep
            
        Returns:
            Number of backup files removed
        """
        try:
            backups = self.list_backups()
            if len(backups) <= keep_count:
                return 0
            
            # Sort by modification time (oldest first)
            backups.sort(key=lambda x: os.path.getmtime(x))
            
            # Remove oldest backups
            to_remove = backups[:-keep_count]
            removed_count = 0
            
            for backup_file in to_remove:
                try:
                    os.unlink(backup_file)
                    removed_count += 1
                except Exception:
                    pass  # Continue with other files
            
            return removed_count
        except Exception:
            return 0
    
    def verify_backup_integrity(self, backup_path: str) -> bool:
        """Verify that a backup file is readable and contains valid content.
        
        Args:
            backup_path: Path to the backup file
            
        Returns:
            True if backup is valid, False otherwise
        """
        try:
            if not os.path.exists(backup_path):
                return False
            
            # Try to read the backup file
            with open(backup_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Basic validation - should contain some Python-like content
            if not content.strip():
                return False
            
            # Check for basic Python test structure
            has_test_function = 'def test_' in content
            has_given_decorator = '@given' in content
            
            return has_test_function or has_given_decorator
        except Exception:
            return False
    
    def rollback_batch(self, file_results: List[StandardizationResult]) -> int:
        """Rollback multiple files from their backup versions.
        
        Args:
            file_results: List of standardization results with backup paths
            
        Returns:
            Number of files successfully rolled back
        """
        rollback_count = 0
        
        for result in file_results:
            if result.backup_path and result.success:
                if self.rollback_file(result.file_path, result.backup_path):
                    rollback_count += 1
        
        return rollback_count
    
    def get_backup_info(self, backup_path: str) -> Optional[Dict[str, str]]:
        """Get information about a backup file.
        
        Args:
            backup_path: Path to the backup file
            
        Returns:
            Dictionary with backup information or None if invalid
        """
        try:
            if not os.path.exists(backup_path):
                return None
            
            stat = os.stat(backup_path)
            
            return {
                'path': backup_path,
                'size': str(stat.st_size),
                'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'valid': str(self.verify_backup_integrity(backup_path))
            }
        except Exception:
            return None