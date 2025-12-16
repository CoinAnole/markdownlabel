"""Comment analysis tool for property-based test documentation.

This module provides automated analysis of existing comments in test files,
detection of inconsistencies, and generation of analysis reports for missing
and malformed comment documentation.
"""

import ast
import os
import re
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Set, Tuple
from pathlib import Path

from .comment_format import CommentFormatValidator, ValidationResult, CommentPattern
from .strategy_type_mapper import StrategyTypeMapper, TestCodeAnalyzer


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
class FileAnalysis:
    """Analysis result for a single test file."""
    file_path: str
    total_property_tests: int
    documented_tests: int
    undocumented_tests: int
    format_violations: List[FormatViolation] = field(default_factory=list)
    inconsistencies: List[Inconsistency] = field(default_factory=list)
    missing_documentation: List[Tuple[str, int, int]] = field(default_factory=list)  # (function_name, line_number, max_examples)
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


class CommentAnalyzer:
    """Analyzes test files for comment format compliance and consistency."""
    
    def __init__(self):
        """Initialize analyzer with validation and mapping tools."""
        self.validator = CommentFormatValidator()
        self.mapper = StrategyTypeMapper()
        self.code_analyzer = TestCodeAnalyzer()
        
        # Standard max_examples values that typically don't need documentation
        self.standard_values = {2, 5, 10, 20, 50, 100}
        
        # Pattern to match property-based test functions
        self.property_test_pattern = re.compile(r'def\s+(test_\w+).*@given', re.DOTALL)
        
        # Pattern to match @settings decorator with max_examples
        self.settings_pattern = re.compile(r'@settings\([^)]*max_examples\s*=\s*(\d+)', re.DOTALL)
        
        # Pattern to match conditional max_examples (CI optimization)
        # This pattern captures the entire conditional expression including nested parentheses
        self.conditional_settings_pattern = re.compile(
            r'@settings\([^)]*max_examples\s*=\s*([^,]+(?:,\s*deadline\s*=\s*None)?)', re.DOTALL
        )
        
        # Pattern to match comment lines
        self.comment_pattern = re.compile(r'^\s*#\s*(.+)$')
    
    def analyze_file(self, file_path: str) -> FileAnalysis:
        """Analyze a single test file for comment compliance.
        
        Args:
            file_path: Path to the test file to analyze
            
        Returns:
            FileAnalysis with detailed analysis results
        """
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
        """Analyze all test files in a directory for comment compliance.
        
        Args:
            directory_path: Path to directory containing test files
            
        Returns:
            DirectoryAnalysis with comprehensive analysis results
        """
        if not os.path.exists(directory_path):
            return DirectoryAnalysis(
                directory_path=directory_path,
                total_files=0,
                analyzed_files=0
            )
        
        # Find all Python test files
        test_files = []
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if file.startswith('test_') and file.endswith('.py'):
                    test_files.append(os.path.join(root, file))
        
        # Analyze each file
        file_analyses = []
        for file_path in test_files:
            analysis = self.analyze_file(file_path)
            file_analyses.append(analysis)
        
        # Detect global inconsistencies across files
        global_inconsistencies = self.detect_inconsistencies(file_analyses)
        
        # Calculate summary statistics
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
        """Validate a comment against the standardized format.
        
        Args:
            comment: Comment string to validate
            
        Returns:
            ValidationResult with validation status and details
        """
        return self.validator.validate_comment_format(comment)
    
    def detect_inconsistencies(self, file_analyses: List[FileAnalysis]) -> List[Inconsistency]:
        """Detect inconsistencies across multiple file analyses.
        
        Args:
            file_analyses: List of file analysis results
            
        Returns:
            List of detected inconsistencies
        """
        inconsistencies = []
        
        # Detect terminology inconsistencies
        inconsistencies.extend(self._detect_terminology_inconsistencies(file_analyses))
        
        # Detect missing documentation patterns
        inconsistencies.extend(self._detect_missing_documentation_patterns(file_analyses))
        
        # Detect format violation patterns
        inconsistencies.extend(self._detect_format_violation_patterns(file_analyses))
        
        # Detect max_examples value inconsistencies
        inconsistencies.extend(self._detect_max_examples_inconsistencies(file_analyses))
        
        return inconsistencies
    
    def _detect_terminology_inconsistencies(self, file_analyses: List[FileAnalysis]) -> List[Inconsistency]:
        """Detect terminology inconsistencies within strategy types."""
        inconsistencies = []
        
        # Collect all valid comments by strategy type
        comments_by_strategy = {}
        for analysis in file_analyses:
            for comment in analysis.valid_comments:
                strategy_type = comment.strategy_type
                if strategy_type not in comments_by_strategy:
                    comments_by_strategy[strategy_type] = []
                comments_by_strategy[strategy_type].append((analysis.file_path, comment))
        
        # Check for terminology inconsistencies within each strategy type
        for strategy_type, comments in comments_by_strategy.items():
            rationales = set()
            affected_files = set()
            affected_lines = []
            
            for file_path, comment in comments:
                rationales.add(comment.rationale.lower().strip())
                affected_files.add(file_path)
                if comment.line_number:
                    affected_lines.append((file_path, comment.line_number))
            
            # If more than one unique rationale for same strategy type, it's inconsistent
            if len(rationales) > 1:
                inconsistencies.append(Inconsistency(
                    inconsistency_type="TERMINOLOGY_INCONSISTENCY",
                    description=f"Strategy type '{strategy_type}' uses inconsistent rationale patterns: {list(rationales)}",
                    affected_files=list(affected_files),
                    affected_lines=affected_lines,
                    suggested_resolution=f"Standardize all '{strategy_type}' strategy comments to use consistent rationale"
                ))
        
        return inconsistencies
    
    def _detect_missing_documentation_patterns(self, file_analyses: List[FileAnalysis]) -> List[Inconsistency]:
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
                description=f"Found {total_missing} undocumented custom max_examples values across {len(files_with_missing_docs)} files",
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
    
    def _detect_max_examples_inconsistencies(self, file_analyses: List[FileAnalysis]) -> List[Inconsistency]:
        """Detect inconsistencies in max_examples usage patterns."""
        inconsistencies = []
        
        # Collect max_examples values by strategy type
        max_examples_by_strategy = {}
        for analysis in file_analyses:
            for comment in analysis.valid_comments:
                strategy_type = comment.strategy_type
                if strategy_type not in max_examples_by_strategy:
                    max_examples_by_strategy[strategy_type] = set()
                max_examples_by_strategy[strategy_type].add(comment.max_examples)
        
        # Check for unusual patterns
        for strategy_type, values in max_examples_by_strategy.items():
            if len(values) > 3:  # More than 3 different values for same strategy type
                inconsistencies.append(Inconsistency(
                    inconsistency_type="MAX_EXAMPLES_INCONSISTENCY",
                    description=f"Strategy type '{strategy_type}' uses many different max_examples values: {sorted(values)}",
                    affected_files=[],  # Would need more detailed tracking to populate this
                    suggested_resolution=f"Review and standardize max_examples values for '{strategy_type}' strategy"
                ))
        
        return inconsistencies
    
    def _analyze_file_content(self, file_path: str, content: str) -> FileAnalysis:
        """Analyze the content of a single file."""
        lines = content.split('\n')
        
        # Find all property-based test functions
        property_tests = self._find_property_tests(content)
        
        # Analyze each test function
        documented_tests = 0
        undocumented_tests = 0
        format_violations = []
        valid_comments = []
        missing_documentation = []
        
        for test_info in property_tests:
            func_name, start_line, end_line, max_examples = test_info
            
            # Look for comments in the function and a few lines before (for documentation comments)
            search_start = max(1, start_line - 5)  # Look up to 5 lines before the function
            comments_in_function = self._extract_comments_in_range(lines, search_start, end_line)
            
            # Check if any comment is a valid standardized comment
            has_valid_comment = False
            for line_num, comment_text in comments_in_function:
                validation_result = self.validator.validate_comment_format(comment_text)
                
                if validation_result.is_valid:
                    has_valid_comment = True
                    valid_comments.append(validation_result.parsed_pattern)
                elif self._looks_like_max_examples_comment(comment_text):
                    # This looks like it's trying to document max_examples but has format issues
                    format_violations.append(FormatViolation(
                        line_number=line_num,
                        original_comment=comment_text,
                        error_type=validation_result.error_type or "FORMAT_VIOLATION",
                        message=validation_result.message,
                        suggested_fix=self._suggest_comment_fix(comment_text, max_examples)
                    ))
            
            # Count this test as documented if it has a valid comment
            if has_valid_comment:
                documented_tests += 1
            
            # Check if this test needs documentation
            if not has_valid_comment and max_examples and max_examples not in self.standard_values:
                undocumented_tests += 1
                missing_documentation.append((func_name, start_line, max_examples))
        
        return FileAnalysis(
            file_path=file_path,
            total_property_tests=len(property_tests),
            documented_tests=documented_tests,
            undocumented_tests=undocumented_tests,
            format_violations=format_violations,
            missing_documentation=missing_documentation,
            valid_comments=valid_comments
        )
    
    def _find_property_tests(self, content: str) -> List[Tuple[str, int, int, Optional[int]]]:
        """Find all property-based test functions in the content.
        
        Returns:
            List of tuples: (function_name, start_line, end_line, max_examples)
        """
        property_tests = []
        
        # Use regex-based approach for more reliable detection
        lines = content.split('\n')
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Look for @given decorator
            if line.startswith('@given'):
                # Find the function definition that follows
                j = i + 1
                max_examples = None
                
                # Look for @settings decorator between @given and function def
                while j < len(lines):
                    next_line = lines[j].strip()
                    
                    if next_line.startswith('@settings'):
                        # Try to extract max_examples from more complex expressions first
                        max_examples = self._extract_max_examples_from_settings_line(next_line)
                        
                        # If that didn't work, try the simple pattern
                        if max_examples is None:
                            settings_match = self.settings_pattern.search(next_line)
                            if settings_match:
                                max_examples = int(settings_match.group(1))
                    
                    elif next_line.startswith('def test_'):
                        # Found the function definition
                        func_match = re.match(r'def\s+(test_\w+)\s*\(', next_line)
                        if func_match:
                            func_name = func_match.group(1)
                            
                            # Find the end of the function (next function or class)
                            end_line = j + 1
                            while end_line < len(lines):
                                end_line_content = lines[end_line]
                                if (end_line_content.strip().startswith('def ') or 
                                    end_line_content.strip().startswith('class ') or
                                    (end_line_content and not end_line_content.startswith(' ') and not end_line_content.startswith('\t'))):
                                    break
                                end_line += 1
                            
                            property_tests.append((
                                func_name,
                                j + 1,  # Line numbers are 1-based
                                end_line,
                                max_examples
                            ))
                        break
                    
                    elif next_line.startswith('def ') or next_line.startswith('class '):
                        # Hit another definition without finding test function
                        break
                    
                    j += 1
            
            i += 1
        
        return property_tests
    
    def _extract_max_examples_from_decorators(self, decorators: List[ast.expr]) -> Optional[int]:
        """Extract max_examples value from @settings decorator."""
        for decorator in decorators:
            if isinstance(decorator, ast.Call):
                # Check if this is @settings(...)
                if (isinstance(decorator.func, ast.Name) and decorator.func.id == 'settings') or \
                   (isinstance(decorator.func, ast.Attribute) and decorator.func.attr == 'settings'):
                    
                    # Look for max_examples keyword argument
                    for keyword in decorator.keywords:
                        if keyword.arg == 'max_examples':
                            if isinstance(keyword.value, ast.Constant):
                                return keyword.value.value
                            elif isinstance(keyword.value, ast.Num):  # Python < 3.8 compatibility
                                return keyword.value.n
        
        return None
    
    def _extract_comments_in_range(self, lines: List[str], start_line: int, end_line: int) -> List[Tuple[int, str]]:
        """Extract all comments within a line range."""
        comments = []
        
        for i in range(max(0, start_line - 1), min(len(lines), end_line)):
            line = lines[i].strip()
            if line.startswith('#'):
                # Clean up the comment text
                comment_text = line[1:].strip()
                if comment_text:  # Skip empty comments
                    comments.append((i + 1, f"# {comment_text}"))
        
        return comments
    
    def _looks_like_max_examples_comment(self, comment: str) -> bool:
        """Check if a comment looks like it's trying to document max_examples."""
        comment_lower = comment.lower()
        indicators = [
            'strategy',
            'examples',
            'coverage',
            'boolean',
            'finite',
            'complex',
            'combination',
            'performance',
            'optimized',
            'format',  # "Wrong format: 25 examples"
            'proper',
            'comment'
        ]
        
        # Also check for patterns like "N examples" where N is a number
        has_examples_pattern = re.search(r'\d+\s+examples', comment_lower)
        
        return any(indicator in comment_lower for indicator in indicators) or bool(has_examples_pattern)
    
    def _suggest_comment_fix(self, original_comment: str, max_examples: Optional[int]) -> Optional[str]:
        """Suggest a fix for a malformed comment."""
        if not max_examples:
            return None
        
        # Try to detect strategy type from comment content
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
        """Extract max_examples value from @settings line with complex expressions.
        
        Args:
            settings_line: The @settings decorator line
            
        Returns:
            Integer value to use for documentation purposes, or None if can't parse
        """
        # Find max_examples= and extract the balanced expression
        start_match = re.search(r'max_examples\s*=\s*', settings_line)
        if not start_match:
            return None
        
        start_pos = start_match.end()
        
        # Extract the expression by finding the next comma at the same nesting level
        # or the closing parenthesis of the @settings decorator
        paren_count = 0
        quote_char = None
        i = start_pos
        
        while i < len(settings_line):
            char = settings_line[i]
            
            # Handle quotes
            if char in ('"', "'") and (i == 0 or settings_line[i-1] != '\\'):
                if quote_char is None:
                    quote_char = char
                elif quote_char == char:
                    quote_char = None
            elif quote_char is None:  # Only process structure when not in quotes
                if char == '(':
                    paren_count += 1
                elif char == ')':
                    if paren_count == 0:
                        # This is the closing paren of @settings
                        break
                    paren_count -= 1
                elif char == ',' and paren_count == 0:
                    # This is a comma at the top level
                    break
            
            i += 1
        
        max_examples_expr = settings_line[start_pos:i].strip()
        return self._extract_max_examples_from_conditional(max_examples_expr)
    
    def _extract_max_examples_from_conditional(self, max_examples_expr: str) -> Optional[int]:
        """Extract max_examples value from conditional expression.
        
        Args:
            max_examples_expr: Expression like "20 if not os.getenv('CI') else 5"
            
        Returns:
            Integer value to use for documentation purposes, or None if can't parse
        """
        # For CI optimizations, we want to document the CI (reduced) value
        # since that's what needs performance rationale
        
        # Pattern: "base_value if not CI_condition else ci_value"
        ci_pattern = re.search(r'(\d+)\s+if\s+not.*CI.*else\s+(\d+)', max_examples_expr, re.IGNORECASE)
        if ci_pattern:
            base_value = int(ci_pattern.group(1))
            ci_value = int(ci_pattern.group(2))
            return ci_value  # Return CI value for documentation
        
        # Pattern: "ci_value if CI_condition else base_value"
        ci_reverse_pattern = re.search(r'(\d+)\s+if.*CI.*else\s+(\d+)', max_examples_expr, re.IGNORECASE)
        if ci_reverse_pattern:
            ci_value = int(ci_reverse_pattern.group(1))
            base_value = int(ci_reverse_pattern.group(2))
            return ci_value  # Return CI value for documentation
        
        # Try to extract any integer from the expression
        numbers = re.findall(r'\d+', max_examples_expr)
        if numbers:
            # Return the smallest value (likely the performance-optimized one)
            return min(int(n) for n in numbers)
        
        return None
    
    def _calculate_summary_stats(self, file_analyses: List[FileAnalysis]) -> Dict[str, int]:
        """Calculate summary statistics across all file analyses."""
        stats = {
            'total_property_tests': sum(analysis.total_property_tests for analysis in file_analyses),
            'total_documented_tests': sum(analysis.documented_tests for analysis in file_analyses),
            'total_undocumented_tests': sum(analysis.undocumented_tests for analysis in file_analyses),
            'total_format_violations': sum(len(analysis.format_violations) for analysis in file_analyses),
            'files_with_violations': len([a for a in file_analyses if a.format_violations]),
            'files_with_missing_docs': len([a for a in file_analyses if a.missing_documentation]),
            'total_valid_comments': sum(len(analysis.valid_comments) for analysis in file_analyses)
        }
        
        # Calculate compliance percentage
        if stats['total_property_tests'] > 0:
            stats['compliance_percentage'] = int(
                (stats['total_documented_tests'] / stats['total_property_tests']) * 100
            )
        else:
            stats['compliance_percentage'] = 100
        
        return stats
    
    def find_format_violations(self, file_analyses: List[FileAnalysis]) -> List[FormatViolation]:
        """Find all format violations across multiple file analyses.
        
        Args:
            file_analyses: List of file analysis results
            
        Returns:
            List of all format violations found
        """
        all_violations = []
        for analysis in file_analyses:
            all_violations.extend(analysis.format_violations)
        return all_violations
    
    def identify_missing_comments(self, file_analyses: List[FileAnalysis]) -> List[Tuple[str, str, int, int]]:
        """Identify all missing comments across file analyses.
        
        Args:
            file_analyses: List of file analysis results
            
        Returns:
            List of tuples: (file_path, function_name, line_number, max_examples)
        """
        missing_comments = []
        for analysis in file_analyses:
            for func_name, line_num, max_examples in analysis.missing_documentation:
                missing_comments.append((analysis.file_path, func_name, line_num, max_examples))
        return missing_comments
    
    def check_terminology_consistency(self, file_analyses: List[FileAnalysis]) -> Dict[str, List[str]]:
        """Check terminology consistency across strategy types.
        
        Args:
            file_analyses: List of file analysis results
            
        Returns:
            Dictionary mapping strategy types to lists of unique rationales used
        """
        terminology_by_strategy = {}
        
        for analysis in file_analyses:
            for comment in analysis.valid_comments:
                strategy_type = comment.strategy_type
                if strategy_type not in terminology_by_strategy:
                    terminology_by_strategy[strategy_type] = set()
                terminology_by_strategy[strategy_type].add(comment.rationale.lower().strip())
        
        # Convert sets to lists for JSON serialization
        return {
            strategy_type: list(rationales) 
            for strategy_type, rationales in terminology_by_strategy.items()
        }