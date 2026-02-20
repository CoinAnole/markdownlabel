"""Comment analysis for property-based test documentation.

This module provides tools for analyzing test files for comment format
compliance and consistency.
"""

import os
import re
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple

from .comment_validation import (
    StrategyType,
    CommentPattern,
    ValidationResult,
    CommentFormatValidator
)


# =============================================================================
# DATA MODELS
# =============================================================================

@dataclass
class FormatViolation:
    """Represents a comment format violation."""
    line_number: int
    original_comment: str
    error_type: str
    message: str
    suggested_fix: Optional[str] = None


@dataclass
class Inconsistency:
    """Represents an inconsistency in comment patterns."""
    inconsistency_type: str
    description: str
    affected_files: List[str] = field(default_factory=list)
    affected_lines: List[Tuple[str, int]] = field(default_factory=list)
    suggested_resolution: Optional[str] = None


@dataclass
class StrategyMismatch:
    """Represents a mismatch between documented and implemented strategy."""
    line_number: int
    function_name: str
    documented_type: str
    implemented_type: str
    rationale: str


@dataclass
class FileAnalysis:
    """Analysis result for a single test file."""
    file_path: str
    total_property_tests: int
    documented_tests: int
    undocumented_tests: int
    format_violations: List[FormatViolation] = field(default_factory=list)
    inconsistencies: List[Inconsistency] = field(default_factory=list)
    missing_documentation: List[Tuple[str, int, int]] = field(default_factory=list)
    strategy_mismatches: List[StrategyMismatch] = field(default_factory=list)
    valid_comments: List[CommentPattern] = field(default_factory=list)


@dataclass
class DirectoryAnalysis:
    """Analysis result for a directory of test files."""
    directory_path: str
    total_files: int
    analyzed_files: int
    file_analyses: List[FileAnalysis] = field(default_factory=list)
    global_inconsistencies: List[Inconsistency] = field(default_factory=list)
    summary_stats: Dict[str, int] = field(default_factory=dict)


@dataclass
class CommentStrategyClassification:
    """Classification result for comment format generation."""
    strategy_type: StrategyType
    rationale: str
    input_space_size: Optional[int] = None
    complexity_level: int = 1
    components: List[str] = None

    def __post_init__(self):
        if self.components is None:
            self.components = []


# =============================================================================
# COMMENT ANALYSIS
# =============================================================================

class CommentAnalyzer:
    """Analyzes test files for comment format compliance and consistency."""

    def __init__(self):
        """Initialize analyzer with validation and mapping tools."""
        self.validator = CommentFormatValidator()

        default_standard_values = {2, 5, 10, 20, 50, 100}
        skip_standard = os.getenv("SKIP_STANDARD_MAX_EXAMPLES", "").lower() in {"1", "true", "yes", "on"}
        self.standard_values = default_standard_values if skip_standard else set()

        self.property_test_pattern = re.compile(r'def\s+(test_\w+).*@given', re.DOTALL)
        self.settings_pattern = re.compile(r'@settings\([^)]*max_examples\s*=\s*(\d+)', re.DOTALL)
        self.conditional_settings_pattern = re.compile(
            r'@settings\([^)]*max_examples\s*=\s*([^,]+(?:,\s*deadline\s*=\s*None)?)', re.DOTALL
        )
        self.comment_pattern = re.compile(r'^\s*#\s*(.+)$')

    def analyze_file(self, file_path: str) -> FileAnalysis:
        """Analyze a single test file for comment compliance."""
        if not os.path.exists(file_path):
            return FileAnalysis(
                file_path=file_path,
                total_property_tests=0,
                documented_tests=0,
                undocumented_tests=0
            )

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except (IOError, UnicodeDecodeError) as e:
            return FileAnalysis(
                file_path=file_path,
                total_property_tests=0,
                documented_tests=0,
                undocumented_tests=0,
                format_violations=[FormatViolation(
                    line_number=0,
                    original_comment="",
                    error_type="FILE_READ_ERROR",
                    message=f"Could not read file: {e}"
                )]
            )

        return self._analyze_file_content(file_path, content)

    def analyze_directory(self, directory_path: str) -> DirectoryAnalysis:
        """Analyze all test files in a directory for comment compliance."""
        if not os.path.exists(directory_path):
            return DirectoryAnalysis(
                directory_path=directory_path,
                total_files=0,
                analyzed_files=0
            )

        test_files = []
        excluded_patterns = {
            'test_comment_format.py',
            'test_comment_standardizer.py',
            'test_assertion_analyzer.py',
            'test_code_duplication_minimization.py',
            'test_coverage_preservation.py',
            'test_documentation_compliance.py',
            'test_duplicate_detector.py',
            'test_file_analyzer.py',
            'test_helper_availability.py',
            'test_naming_convention_validator.py',
            'test_strategy_classification.py',
            'test_test_file_parser.py',
            'tools/validate_comments.py',
        }

        for root, dirs, files in os.walk(directory_path):
            if any(ex in root for ex in excluded_patterns):
                continue

            for file in files:
                if file.startswith('test_') and file.endswith('.py'):
                    if file in excluded_patterns:
                        continue
                    test_files.append(os.path.join(root, file))

        file_analyses = []
        for file_path in test_files:
            analysis = self.analyze_file(file_path)
            file_analyses.append(analysis)

        global_inconsistencies = self.detect_inconsistencies(file_analyses)
        summary_stats = self._calculate_summary_stats(file_analyses)

        return DirectoryAnalysis(
            directory_path=directory_path,
            total_files=len(test_files),
            analyzed_files=len(file_analyses),
            file_analyses=file_analyses,
            global_inconsistencies=global_inconsistencies,
            summary_stats=summary_stats
        )

    def validate_comment_format(self, comment: str) -> ValidationResult:
        """Validate a comment against the standardized format."""
        return self.validator.validate_comment_format(comment)

    def detect_inconsistencies(self, file_analyses: List[FileAnalysis]) -> List[Inconsistency]:
        """Detect inconsistencies across multiple file analyses."""
        inconsistencies = []

        inconsistencies.extend(self._detect_terminology_inconsistencies(file_analyses))
        inconsistencies.extend(self._detect_missing_documentation_patterns(file_analyses))
        inconsistencies.extend(self._detect_format_violation_patterns(file_analyses))
        inconsistencies.extend(self._detect_strategy_mismatch_patterns(file_analyses))

        return inconsistencies

    def _analyze_file_content(self, file_path: str, content: str) -> FileAnalysis:
        """Analyze the content of a single file."""
        lines = content.split('\n')
        property_tests = self._find_property_tests(content)

        documented_tests = 0
        undocumented_tests = 0
        format_violations = []
        valid_comments = []
        missing_documentation = []
        strategy_mismatches = []

        for test_info in property_tests:
            func_name, start_line, end_line, max_examples, decorator_start = test_info

            comments_in_function = self._extract_documentation_comments(lines, decorator_start)

            has_valid_comment = False
            for line_num, comment_text in comments_in_function:
                validation_result = self.validator.validate_comment_format(comment_text)

                if validation_result.is_valid:
                    has_valid_comment = True
                    pattern = validation_result.parsed_pattern
                    pattern.line_number = line_num
                    valid_comments.append(pattern)
                elif self._looks_like_max_examples_comment(comment_text):
                    format_violations.append(FormatViolation(
                        line_number=line_num,
                        original_comment=comment_text,
                        error_type=validation_result.error_type or "FORMAT_VIOLATION",
                        message=validation_result.message,
                        suggested_fix=self._suggest_comment_fix(comment_text, max_examples)
                    ))

            if has_valid_comment and valid_comments:
                documented_tests += 1

                current_comment = valid_comments[-1]
                func_code = '\n'.join(lines[decorator_start:end_line])
                strategy_classification = self._analyze_strategy_from_code(func_code)

                if strategy_classification:
                    actual_type = strategy_classification.strategy_type.value.lower()
                    doc_type = current_comment.strategy_type.lower()

                    mismatch = False
                    if actual_type == 'boolean' and doc_type != 'boolean':
                        mismatch = True
                    elif 'finite' in actual_type and 'finite' not in doc_type and doc_type != 'boolean':
                        mismatch = True

                    if mismatch:
                        strategy_mismatches.append(StrategyMismatch(
                            line_number=current_comment.line_number,
                            function_name=func_name,
                            documented_type=current_comment.strategy_type,
                            implemented_type=strategy_classification.strategy_type.value,
                            rationale=f"Code implements "
                            f"'{strategy_classification.strategy_type.value}' but is "
                            f"documented as '{current_comment.strategy_type}'"
                        ))

            func_code = '\n'.join(lines[decorator_start:end_line])
            has_ci_optimization = self._has_ci_optimization_pattern(func_code)

            needs_documentation = (
                not has_valid_comment and
                max_examples and
                (max_examples not in self.standard_values or has_ci_optimization)
            )

            if needs_documentation:
                undocumented_tests += 1
                missing_documentation.append((func_name, start_line, max_examples))

        return FileAnalysis(
            file_path=file_path,
            total_property_tests=len(property_tests),
            documented_tests=documented_tests,
            undocumented_tests=undocumented_tests,
            format_violations=format_violations,
            missing_documentation=missing_documentation,
            strategy_mismatches=strategy_mismatches,
            valid_comments=valid_comments
        )

    def _find_property_tests(self, content: str) -> List[Tuple[str, int, int, Optional[int], int]]:
        """Find all property-based test functions in the content."""
        property_tests = []
        lines = content.split('\n')

        i = 0
        while i < len(lines):
            line = lines[i].strip()

            if line.startswith('@given'):
                j = i + 1
                max_examples = None

                while j < len(lines):
                    next_line = lines[j].strip()

                    if next_line.startswith('@settings'):
                        max_examples = self._extract_max_examples_from_settings_line(next_line)

                        if max_examples is None:
                            settings_match = self.settings_pattern.search(next_line)
                            if settings_match:
                                max_examples = int(settings_match.group(1))

                    elif next_line.startswith('def test_'):
                        raw_line = lines[j]
                        indentation = len(raw_line) - len(raw_line.lstrip())

                        func_match = re.match(r'def\s+(test_[^\s(]+)\s*\(', next_line)
                        if func_match:
                            func_name = func_match.group(1)

                            end_line = j + 1
                            while end_line < len(lines):
                                line_content = lines[end_line]
                                stripped = line_content.strip()

                                if not stripped or stripped.startswith('#'):
                                    end_line += 1
                                    continue

                                current_indent = len(line_content) - len(line_content.lstrip())
                                if current_indent <= indentation:
                                    break

                                end_line += 1

                            property_tests.append((
                                func_name,
                                j + 1,
                                end_line,
                                max_examples,
                                i
                            ))
                        break

                    elif next_line.startswith('def ') or next_line.startswith('class '):
                        break

                    j += 1

            i += 1

        return property_tests

    def _extract_documentation_comments(
        self,
        lines: List[str],
        decorator_start: int
    ) -> List[Tuple[int, str]]:
        """Extract documentation comments near a test decorator block."""
        comments = []

        idx = decorator_start - 1
        while idx >= 0 and lines[idx].strip() == '':
            idx -= 1
        while idx >= 0:
            stripped = lines[idx].strip()
            if stripped.startswith('#'):
                comments.append((idx + 1, f"# {stripped.lstrip('#').strip()}"))
                idx -= 1
                continue
            if stripped == '':
                idx -= 1
                continue
            break

        comments.reverse()

        forward_idx = decorator_start + 1
        while forward_idx < len(lines):
            stripped = lines[forward_idx].strip()
            if stripped.startswith('@settings') or stripped.startswith('def ') or \
               stripped.startswith('class '):
                break
            if stripped.startswith('#'):
                comments.append((forward_idx + 1, f"# {stripped.lstrip('#').strip()}"))
            forward_idx += 1

        return sorted(comments, key=lambda c: c[0])

    def _looks_like_max_examples_comment(self, comment: str) -> bool:
        """Check if a comment looks like it's trying to document max_examples."""
        comment_lower = comment.lower()

        if '**feature:' in comment_lower or '**property' in comment_lower:
            return False

        if comment_lower.startswith('# *for any*'):
            return False

        has_examples_pattern = re.search(r'\d+\s+examples', comment_lower)
        if has_examples_pattern:
            return True

        has_strategy_colon = re.search(
            r'\b(boolean|complex|combination|finite|small finite|medium finite)'
            r'\s+strategy\s*:',
            comment_lower
        )
        if has_strategy_colon:
            return True

        if re.match(
            r'^#\s*(boolean|complex|combination|small finite|medium finite)'
            r'\s+strategy\s*:',
            comment_lower
        ):
            return True

        return False

    def _suggest_comment_fix(self, original_comment: str, max_examples: Optional[int]) -> Optional[str]:
        """Suggest a fix for a malformed comment."""
        if not max_examples:
            return None

        comment_lower = original_comment.lower()

        if 'boolean' in comment_lower or 'true/false' in comment_lower:
            return f"# Boolean strategy: {max_examples} examples (True/False coverage)"
        elif 'finite' in comment_lower and 'small' in comment_lower:
            return f"# Small finite strategy: {max_examples} examples (input space size: {max_examples})"
        elif 'finite' in comment_lower:
            return f"# Medium finite strategy: {max_examples} examples (adequate finite coverage)"
        elif 'combination' in comment_lower:
            return f"# Combination strategy: {max_examples} examples (combination coverage)"
        else:
            return f"# Complex strategy: {max_examples} examples (adequate coverage)"

    def _extract_max_examples_from_settings_line(self, settings_line: str) -> Optional[int]:
        """Extract max_examples value from @settings line with complex expressions."""
        start_match = re.search(r'max_examples\s*=\s*', settings_line)
        if not start_match:
            return None

        start_pos = start_match.end()

        paren_count = 0
        quote_char = None
        i = start_pos

        while i < len(settings_line):
            char = settings_line[i]

            if char in ('"', "'") and (i == 0 or settings_line[i-1] != '\\'):
                if quote_char is None:
                    quote_char = char
                elif quote_char == char:
                    quote_char = None
            elif quote_char is None:
                if char == '(':
                    paren_count += 1
                elif char == ')':
                    if paren_count == 0:
                        break
                    paren_count -= 1
                elif char == ',' and paren_count == 0:
                    break

            i += 1

        max_examples_expr = settings_line[start_pos:i].strip()
        return self._extract_max_examples_from_conditional(max_examples_expr)

    def _extract_max_examples_from_conditional(self, max_examples_expr: str) -> Optional[int]:
        """Extract max_examples value from conditional expression."""
        ci_pattern = re.search(r'(\d+)\s+if\s+not.*CI.*else\s+(\d+)', max_examples_expr, re.IGNORECASE)
        if ci_pattern:
            ci_value = int(ci_pattern.group(2))
            return ci_value

        ci_reverse_pattern = re.search(r'(\d+)\s+if.*CI.*else\s+(\d+)', max_examples_expr, re.IGNORECASE)
        if ci_reverse_pattern:
            ci_value = int(ci_reverse_pattern.group(1))
            return ci_value

        numbers = re.findall(r'\d+', max_examples_expr)
        if numbers:
            return min(int(n) for n in numbers)

        return None

    def _has_ci_optimization_pattern(self, func_code: str) -> bool:
        """Check if function code contains CI optimization patterns."""
        ci_patterns = [
            r"os\.getenv\s*\(\s*['\"]CI['\"]\s*\)",
            r"os\.environ\.get\s*\(\s*['\"]CI['\"]\s*\)",
            r"if\s+not.*CI.*else",
            r"if.*CI.*else",
            r"max_examples\s*=\s*\d+\s+if.*CI",
        ]

        for pattern in ci_patterns:
            if re.search(pattern, func_code, re.IGNORECASE):
                return True

        return False

    def _calculate_summary_stats(self, file_analyses: List[FileAnalysis]) -> Dict[str, int]:
        """Calculate summary statistics across all file analyses."""
        stats = {
            'total_property_tests': sum(analysis.total_property_tests for analysis in file_analyses),
            'total_documented_tests': sum(analysis.documented_tests for analysis in file_analyses),
            'total_undocumented_tests': sum(analysis.undocumented_tests for analysis in file_analyses),
            'total_format_violations': sum(len(analysis.format_violations) for analysis in file_analyses),
            'total_strategy_mismatches': sum(len(analysis.strategy_mismatches) for analysis in file_analyses),
            'files_with_violations': len([a for a in file_analyses if a.format_violations]),
            'files_with_missing_docs': len([a for a in file_analyses if a.missing_documentation]),
            'total_valid_comments': sum(len(analysis.valid_comments) for analysis in file_analyses)
        }

        if stats['total_property_tests'] > 0:
            stats['compliance_percentage'] = int(
                (stats['total_documented_tests'] / stats['total_property_tests']) * 100
            )
        else:
            stats['compliance_percentage'] = 100

        return stats

    def _analyze_strategy_from_code(self, func_code: str) -> Optional[CommentStrategyClassification]:
        """Analyze strategy from function code using StrategyClassifier."""
        from .strategy_analyzer import StrategyClassifier

        given_match = re.search(r'@given\([^)]+\)', func_code, re.DOTALL)
        if not given_match:
            return None

        strategy_code = given_match.group(0)

        classifier = StrategyClassifier()
        classification = classifier.classify_strategy_for_comments(strategy_code)

        return classification

    def _detect_strategy_mismatch_patterns(self, file_analyses: List[FileAnalysis]) -> List[Inconsistency]:
        """Detect strategy mismatch patterns."""
        inconsistencies = []

        files_with_mismatches = [
            analysis for analysis in file_analyses
            if analysis.strategy_mismatches
        ]

        if files_with_mismatches:
            total_mismatches = sum(len(analysis.strategy_mismatches) for analysis in files_with_mismatches)
            affected_lines = []

            for analysis in files_with_mismatches:
                for mismatch in analysis.strategy_mismatches:
                    affected_lines.append((analysis.file_path, mismatch.line_number))

            inconsistencies.append(Inconsistency(
                inconsistency_type="STRATEGY_MISMATCH",
                description=f"Found {total_mismatches} strategy mismatches "
                f"(documented vs implemented) across {len(files_with_mismatches)} files",
                affected_files=[analysis.file_path for analysis in files_with_mismatches],
                affected_lines=affected_lines,
                suggested_resolution="Update comments to match actual implementation strategy"
            ))

        return inconsistencies

    def _detect_terminology_inconsistencies(self, file_analyses: List[FileAnalysis]) -> List[Inconsistency]:
        """Detect terminology inconsistencies within strategy types."""
        inconsistencies = []

        comments_by_strategy = {}
        for analysis in file_analyses:
            for comment in analysis.valid_comments:
                strategy_type = comment.strategy_type
                if strategy_type not in comments_by_strategy:
                    comments_by_strategy[strategy_type] = []
                comments_by_strategy[strategy_type].append((analysis.file_path, comment))

        for strategy_type, comments in comments_by_strategy.items():
            rationales = set()
            affected_files = set()
            affected_lines = []

            for file_path, comment in comments:
                rationale = comment.rationale.lower().strip()
                if strategy_type == 'Small finite' and rationale.startswith('input space size'):
                    rationale = 'input space size: <n>'
                rationales.add(rationale)
                affected_files.add(file_path)
                if comment.line_number:
                    affected_lines.append((file_path, comment.line_number))

            if strategy_type == 'Complex':
                continue
            if len(rationales) > 1:
                inconsistencies.append(Inconsistency(
                    inconsistency_type="TERMINOLOGY_INCONSISTENCY",
                    description=f"Strategy type '{strategy_type}' uses inconsistent "
                    f"rationale patterns: {list(rationales)}",
                    affected_files=list(affected_files),
                    affected_lines=affected_lines,
                    suggested_resolution=f"Standardize all '{strategy_type}' "
                    "strategy comments to use consistent rationale"
                ))

        return inconsistencies

    def _detect_missing_documentation_patterns(
        self,
        file_analyses: List[FileAnalysis]
    ) -> List[Inconsistency]:
        """Detect patterns of missing documentation."""
        inconsistencies = []

        files_with_missing_docs = [
            analysis for analysis in file_analyses
            if analysis.missing_documentation
        ]

        if files_with_missing_docs:
            total_missing = sum(len(analysis.missing_documentation) for analysis in files_with_missing_docs)
            affected_lines = []

            for analysis in files_with_missing_docs:
                for func_name, line_num, max_examples in analysis.missing_documentation:
                    affected_lines.append((analysis.file_path, line_num))

            inconsistencies.append(Inconsistency(
                inconsistency_type="MISSING_DOCUMENTATION",
                description=f"Found {total_missing} undocumented custom "
                f"max_examples values across {len(files_with_missing_docs)} files",
                affected_files=[analysis.file_path for analysis in files_with_missing_docs],
                affected_lines=affected_lines,
                suggested_resolution="Add standardized comments for all custom max_examples values"
            ))

        return inconsistencies

    def _detect_format_violation_patterns(self, file_analyses: List[FileAnalysis]) -> List[Inconsistency]:
        """Detect patterns of format violations."""
        inconsistencies = []

        files_with_violations = [
            analysis for analysis in file_analyses
            if analysis.format_violations
        ]

        if files_with_violations:
            violation_types = set()
            affected_lines = []

            for analysis in files_with_violations:
                for violation in analysis.format_violations:
                    violation_types.add(violation.error_type)
                    affected_lines.append((analysis.file_path, violation.line_number))

            total_violations = sum(len(analysis.format_violations) for analysis in files_with_violations)

            inconsistencies.append(Inconsistency(
                inconsistency_type="FORMAT_VIOLATIONS",
                description=f"Found {total_violations} format violations of types: {list(violation_types)}",
                affected_files=[analysis.file_path for analysis in files_with_violations],
                affected_lines=affected_lines,
                suggested_resolution="Fix all format violations to match standardized pattern"
            ))

        return inconsistencies

    def find_format_violations(self, file_analyses: List[FileAnalysis]) -> List[FormatViolation]:
        """Find all format violations across multiple file analyses."""
        all_violations = []
        for analysis in file_analyses:
            all_violations.extend(analysis.format_violations)
        return all_violations

    def identify_missing_comments(self, file_analyses: List[FileAnalysis]) -> List[Tuple[str, str, int, int]]:
        """Identify all missing comments across file analyses."""
        missing_comments = []
        for analysis in file_analyses:
            for func_name, line_num, max_examples in analysis.missing_documentation:
                missing_comments.append((analysis.file_path, func_name, line_num, max_examples))
        return missing_comments

    def check_terminology_consistency(self, file_analyses: List[FileAnalysis]) -> Dict[str, List[str]]:
        """Check terminology consistency across strategy types."""
        terminology_by_strategy = {}

        for analysis in file_analyses:
            for comment in analysis.valid_comments:
                strategy_type = comment.strategy_type
                if strategy_type not in terminology_by_strategy:
                    terminology_by_strategy[strategy_type] = set()
                terminology_by_strategy[strategy_type].add(comment.rationale.lower().strip())

        return {
            strategy_type: list(rationales)
            for strategy_type, rationales in terminology_by_strategy.items()
        }


__all__ = [
    'FormatViolation',
    'Inconsistency',
    'StrategyMismatch',
    'FileAnalysis',
    'DirectoryAnalysis',
    'CommentStrategyClassification',
    'CommentAnalyzer',
]
