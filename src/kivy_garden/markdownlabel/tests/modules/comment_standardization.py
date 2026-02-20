"""Comment standardization for property-based test documentation.

This module provides tools for automated comment generation and standardization.
"""

import os
import re
import shutil
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Tuple

from .comment_validation import (
    StrategyType,
    CommentPattern,
    CommentFormatValidator
)
from .comment_analysis import (
    FileAnalysis,
    CommentAnalyzer,
    CommentStrategyClassification
)


# =============================================================================
# DATA MODELS
# =============================================================================

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


# =============================================================================
# COMMENT STANDARDIZATION
# =============================================================================

class CommentStandardizer:
    """Automated comment generation and standardization tool."""

    def __init__(self, backup_dir: Optional[str] = None, enable_backups: bool = False):
        """Initialize standardizer with analysis and validation tools."""
        self.analyzer = CommentAnalyzer()
        self.validator = CommentFormatValidator()

        self._performance_standardizer = None

        env_enable = os.getenv(
            "COMMENT_STANDARDIZER_ENABLE_BACKUPS", ""
        ).lower() in {"1", "true", "yes", "on"}
        self.backups_enabled = enable_backups or env_enable or backup_dir is not None
        if self.backups_enabled:
            if backup_dir is None:
                backup_dir = os.path.join(
                    os.getcwd(),
                    "optimization_backups",
                    f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                )
            self.backup_dir = backup_dir
        else:
            self.backup_dir = None

        default_standard_values = {2, 5, 10, 20, 50, 100}
        skip_standard = os.getenv("SKIP_STANDARD_MAX_EXAMPLES", "").lower() in {"1", "true", "yes", "on"}
        self.standard_values = default_standard_values if skip_standard else set()

        self.settings_pattern = re.compile(r'(@settings\([^)]*max_examples\s*=\s*\d+[^)]*\))', re.DOTALL)
        self.given_pattern = re.compile(r'(@given\([^)]*\))', re.DOTALL)
        self.function_pattern = re.compile(r'(def\s+test_[^\s(]+\s*\([^)]*\):)')

    @property
    def performance_standardizer(self):
        """Backward compatibility property for performance_standardizer."""
        if self._performance_standardizer is None:
            from .optimization_detector import OptimizationAwareCommentStandardizer
            self._performance_standardizer = OptimizationAwareCommentStandardizer()
        return self._performance_standardizer

    def standardize_file(self, file_path: str, dry_run: bool = False) -> StandardizationResult:
        """Standardize comments in a single test file."""
        if not os.path.exists(file_path):
            return StandardizationResult(
                file_path=file_path,
                success=False,
                changes_made=0,
                errors=[f"File not found: {file_path}"]
            )

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
        except (IOError, UnicodeDecodeError) as e:
            return StandardizationResult(
                file_path=file_path,
                success=False,
                changes_made=0,
                errors=[f"Could not read file: {e}"]
            )

        analysis = self.analyzer.analyze_file(file_path)

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

        if dry_run:
            return StandardizationResult(
                file_path=file_path,
                success=True,
                changes_made=changes_made,
                warnings=warnings,
                generated_comments=generated_comments
            )

        backup_path = None
        if changes_made > 0 and self.backups_enabled:
            try:
                backup_path = self._create_backup(file_path, original_content)
            except Exception as e:
                return StandardizationResult(
                    file_path=file_path,
                    success=False,
                    changes_made=0,
                    errors=[f"Could not create backup: {e}"]
                )

        if changes_made > 0:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
            except IOError as e:
                if backup_path and os.path.exists(backup_path):
                    try:
                        shutil.copy2(backup_path, file_path)
                    except Exception:
                        pass

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

    def generate_comment(
        self,
        strategy_type: str,
        max_examples: int,
        input_space_size: Optional[int] = None
    ) -> str:
        """Generate a standardized comment for given parameters."""
        try:
            strategy_enum = None
            for enum_val in StrategyType:
                if enum_val.value.lower() == strategy_type.lower():
                    strategy_enum = enum_val
                    break

            if strategy_enum is None:
                strategy_enum = StrategyType.COMPLEX

            return self.validator.generate_standard_comment(
                strategy_enum, max_examples, input_space_size
            )
        except Exception as e:
            return f"# {strategy_type} strategy: {max_examples} examples (adequate coverage)"

    def apply_standardization(self, files: List[str], dry_run: bool = False) -> BatchResult:
        """Apply standardization to multiple files."""
        file_results = []
        successful_files = 0
        failed_files = 0
        total_changes = 0
        global_errors = []

        if not dry_run and self.backups_enabled:
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

    def _generate_standardized_content(
        self,
        content: str,
        analysis: FileAnalysis
    ) -> Tuple[str, List[CommentPattern], List[str]]:
        """Generate standardized content with proper comments."""
        lines = content.split('\n')
        generated_comments = []
        warnings = []

        for func_name, line_num, max_examples in analysis.missing_documentation:
            func_start_line = line_num - 1

            func_code = self._extract_function_code(lines, func_start_line)
            if not func_code:
                warnings.append(f"Could not extract function code for {func_name} at line {line_num}")
                continue

            strategy_classification = self.analyzer._analyze_strategy_from_code(func_code)
            if not strategy_classification:
                warnings.append(f"Could not classify strategy for {func_name}, using default")
                strategy_classification = CommentStrategyClassification(
                    strategy_type=StrategyType.COMPLEX,
                    rationale="adequate coverage"
                )

            comment_text = self._generate_comment_for_strategy(
                strategy_classification, max_examples, func_code
            )

            insert_line = self._find_comment_insertion_point(lines, func_start_line)

            lines.insert(insert_line, comment_text)

            validation_result = self.validator.validate_comment_format(comment_text)
            if validation_result.is_valid and validation_result.parsed_pattern:
                actual_rationale = validation_result.parsed_pattern.rationale
                actual_strategy_type = validation_result.parsed_pattern.strategy_type
            else:
                actual_rationale = strategy_classification.rationale
                actual_strategy_type = strategy_classification.strategy_type.value

            generated_comments.append(CommentPattern(
                strategy_type=actual_strategy_type,
                max_examples=max_examples,
                rationale=actual_rationale,
                line_number=insert_line + 1,
                original_comment=None
            ))

        for violation in analysis.format_violations:
            if violation.suggested_fix:
                violation_line = violation.line_number - 1
                if 0 <= violation_line < len(lines):
                    lines[violation_line] = violation.suggested_fix

                    validation_result = self.validator.validate_comment_format(violation.suggested_fix)
                    if validation_result.is_valid and validation_result.parsed_pattern:
                        generated_comments.append(validation_result.parsed_pattern)

        new_content = '\n'.join(lines)
        return new_content, generated_comments, warnings

    def _generate_comment_for_strategy(self, strategy_classification: CommentStrategyClassification,
                                      max_examples: int, func_code: str) -> str:
        """Generate a comment for a given strategy classification."""
        if self.analyzer._has_ci_optimization_pattern(func_code):
            rationale = "CI optimized"
        elif (strategy_classification.strategy_type == StrategyType.COMPLEX and
              max_examples <= 5):
            rationale = "performance optimized"
        else:
            rationale = strategy_classification.rationale

        pattern = CommentPattern(
            strategy_type=strategy_classification.strategy_type.value,
            max_examples=max_examples,
            rationale=rationale
        )

        return pattern.to_standardized_format()

    def _extract_function_code(self, lines: List[str], func_start_line: int) -> str:
        """Extract the complete function code starting from the given line."""
        if func_start_line < 0 or func_start_line >= len(lines):
            return ""

        start_line = func_start_line
        while start_line > 0:
            prev_line = lines[start_line - 1].strip()
            if prev_line.startswith('@') or prev_line == "":
                start_line -= 1
            else:
                break

        end_line = func_start_line + 1
        while end_line < len(lines):
            line = lines[end_line]
            if (line.strip().startswith('def ') or
                    line.strip().startswith('class ') or
                    (line.strip() and not line.startswith(' ') and not
                     line.startswith('\t'))):
                break
            end_line += 1

        return '\n'.join(lines[start_line:end_line])

    def _find_comment_insertion_point(self, lines: List[str], func_start_line: int) -> int:
        """Find the best line to insert a comment before the function."""
        insert_line = func_start_line

        check_line = func_start_line - 1
        while check_line >= 0:
            line = lines[check_line].strip()
            if line.startswith('@'):
                insert_line = check_line
                check_line -= 1
            elif line == "":
                check_line -= 1
            else:
                break

        return insert_line

    def _create_backup(self, file_path: str, content: str) -> str:
        """Create a backup of the file before modification."""
        if not self.backups_enabled or not self.backup_dir:
            raise ValueError("Backups are disabled for this standardizer instance")
        os.makedirs(self.backup_dir, exist_ok=True)

        original_name = os.path.basename(file_path)
        backup_name = f"{original_name}.backup"
        backup_path = os.path.join(self.backup_dir, backup_name)

        counter = 1
        while os.path.exists(backup_path):
            backup_name = f"{original_name}.backup.{counter}"
            backup_path = os.path.join(self.backup_dir, backup_name)
            counter += 1

        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return backup_path

    def rollback_file(self, file_path: str, backup_path: str) -> bool:
        """Rollback a file to its backup version."""
        try:
            if not os.path.exists(backup_path):
                return False

            shutil.copy2(backup_path, file_path)
            return True
        except Exception:
            return False

    def validate_standardization(self, file_path: str) -> bool:
        """Validate that a file has been properly standardized."""
        try:
            analysis = self.analyzer.analyze_file(file_path)

            has_missing_docs = len(analysis.missing_documentation) > 0
            has_violations = len(analysis.format_violations) > 0

            return not (has_missing_docs or has_violations)
        except Exception:
            return False

    def create_backup_directory(self) -> bool:
        """Create the backup directory if it doesn't exist."""
        if not self.backups_enabled or not self.backup_dir:
            return False
        try:
            os.makedirs(self.backup_dir, exist_ok=True)
            return True
        except Exception:
            return False

    def list_backups(self) -> List[str]:
        """List all backup files in the backup directory."""
        if not self.backups_enabled or not self.backup_dir:
            return []
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
        """Clean up old backup files, keeping only the most recent ones."""
        if not self.backups_enabled or not self.backup_dir:
            return 0
        try:
            backups = self.list_backups()
            if len(backups) <= keep_count:
                return 0

            backups.sort(key=lambda x: os.path.getmtime(x))

            to_remove = backups[:-keep_count]
            removed_count = 0

            for backup_file in to_remove:
                try:
                    os.unlink(backup_file)
                    removed_count += 1
                except Exception:
                    pass

            return removed_count
        except Exception:
            return 0

    def verify_backup_integrity(self, backup_path: str) -> bool:
        """Verify that a backup file is readable and contains valid content."""
        if not self.backups_enabled:
            return False
        try:
            if not os.path.exists(backup_path):
                return False

            with open(backup_path, 'r', encoding='utf-8') as f:
                content = f.read()

            if not content.strip():
                return False

            has_test_function = 'def test_' in content
            has_given_decorator = '@given' in content

            return has_test_function or has_given_decorator
        except Exception:
            return False

    def rollback_batch(self, file_results: List[StandardizationResult]) -> int:
        """Rollback multiple files from their backup versions."""
        if not self.backups_enabled:
            return 0
        rollback_count = 0

        for result in file_results:
            if result.backup_path and result.success:
                if self.rollback_file(result.file_path, result.backup_path):
                    rollback_count += 1

        return rollback_count

    def get_backup_info(self, backup_path: str) -> Optional[dict]:
        """Get information about a backup file."""
        if not self.backups_enabled:
            return None
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


__all__ = [
    'StandardizationResult',
    'BatchResult',
    'CommentStandardizer',
]
