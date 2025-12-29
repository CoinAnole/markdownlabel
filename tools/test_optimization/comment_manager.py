"""Unified comment management module for property-based test documentation.

This module consolidates comment format validation, analysis, and standardization
functionality into a single self-contained module. It provides tools for:

1. Validating comment formats against standardized patterns
2. Analyzing test files for comment compliance and consistency
3. Generating and standardizing comments based on strategy analysis

This module eliminates circular dependencies and duplicate code from the original
three separate modules (comment_format.py, comment_analyzer.py, comment_standardizer.py).
"""

import ast
import os
import re
import shutil
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import List, Optional, Dict, Tuple, Set


# =============================================================================
# ENUMS AND DATA MODELS
# =============================================================================

class StrategyType(Enum):
    """Strategy types for comment format classification.

    This unified enum replaces duplicate StrategyType definitions from
    comment_format.py and strategy_classifier.py.
    """
    BOOLEAN = "Boolean"
    SMALL_FINITE = "Small finite"
    MEDIUM_FINITE = "Medium finite"
    COMPLEX = "Complex"
    COMBINATION = "Combination"


@dataclass
class CommentPattern:
    """Data model for standardized comment patterns."""
    strategy_type: str
    max_examples: int
    rationale: str
    line_number: Optional[int] = None
    original_comment: Optional[str] = None
    
    def to_standardized_format(self) -> str:
        """Convert to standardized comment format.
        
        Returns:
            Formatted comment string following the standard pattern
        """
        return f"# {self.strategy_type} strategy: {self.max_examples} examples ({self.rationale})"


@dataclass
class ValidationResult:
    """Result of comment format validation."""
    is_valid: bool
    error_type: Optional[str]
    message: str
    original_comment: str
    parsed_pattern: Optional[CommentPattern] = None


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
    missing_documentation: List[Tuple[str, int, int]] = field(default_factory=list)  # (function_name, line_number, max_examples)
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
# COMMENT FORMAT VALIDATION
# =============================================================================

class CommentFormatValidator:
    """Validates comment formats against standardized patterns."""
    
    def __init__(self):
        """Initialize validator with format patterns and templates."""
        # Standard format pattern: # [Strategy Type] strategy: [N] examples ([Rationale])
        self.standard_pattern = re.compile(
            r'^#\s*(\w+(?:\s+\w+)*)\s+strategy:\s*(\d+)\s+examples\s*\(([^)]+)\)\s*$',
            re.IGNORECASE
        )
        
        # Define rationale templates for each strategy type
        self.rationale_templates = {
            StrategyType.BOOLEAN: [
                "True/False coverage",
                "boolean coverage"
            ],
            StrategyType.SMALL_FINITE: [
                r"input space size: \d+",
                r"input space size",
                r"finite coverage"
            ],
            StrategyType.MEDIUM_FINITE: [
                "adequate finite coverage",
                "finite coverage"
            ],
            StrategyType.COMPLEX: [
                "adequate coverage",
                "performance optimized",
                "complexity coverage",
                "CI optimized"
            ],
            StrategyType.COMBINATION: [
                "combination coverage",
                "product coverage",
                "performance optimized",
                "CI optimized"
            ]
        }
        
        # Valid strategy type names (case-insensitive)
        self.valid_strategy_types = {
            strategy_type.value.lower(): strategy_type 
            for strategy_type in StrategyType
        }
    
    def validate_comment_format(self, comment: str) -> ValidationResult:
        """Validate a comment against the standardized format.
        
        Args:
            comment: Comment string to validate
            
        Returns:
            ValidationResult with validation status and details
        """
        comment = comment.strip()
        
        # Check if comment matches standard pattern
        match = self.standard_pattern.match(comment)
        if not match:
            return ValidationResult(
                is_valid=False,
                error_type="FORMAT_VIOLATION",
                message="Comment does not match standard format: '# [Strategy Type] strategy: [N] examples ([Rationale])'",
                original_comment=comment
            )
        
        strategy_type_str, max_examples_str, rationale = match.groups()
        
        # Validate strategy type
        strategy_type_lower = strategy_type_str.lower()
        if strategy_type_lower not in self.valid_strategy_types:
            return ValidationResult(
                is_valid=False,
                error_type="INVALID_STRATEGY_TYPE",
                message=f"Invalid strategy type: '{strategy_type_str}'. Valid types: {list(self.valid_strategy_types.keys())}",
                original_comment=comment
            )
        
        # Validate max_examples is positive integer
        try:
            max_examples = int(max_examples_str)
            if max_examples <= 0:
                return ValidationResult(
                    is_valid=False,
                    error_type="INVALID_MAX_EXAMPLES",
                    message=f"max_examples must be positive integer, got: {max_examples}",
                    original_comment=comment
                )
        except ValueError:
            return ValidationResult(
                is_valid=False,
                error_type="INVALID_MAX_EXAMPLES",
                message=f"max_examples must be integer, got: '{max_examples_str}'",
                original_comment=comment
            )
        
        # Validate rationale format
        strategy_type = self.valid_strategy_types[strategy_type_lower]
        if not self._validate_rationale(rationale, strategy_type):
            expected_templates = self.rationale_templates[strategy_type]
            return ValidationResult(
                is_valid=False,
                error_type="INVALID_RATIONALE",
                message=f"Rationale '{rationale}' doesn't match expected patterns for {strategy_type.value}: {expected_templates}",
                original_comment=comment
            )
        
        # All validations passed
        return ValidationResult(
            is_valid=True,
            error_type=None,
            message="Comment format is valid",
            original_comment=comment,
            parsed_pattern=CommentPattern(
                strategy_type=strategy_type.value,
                max_examples=max_examples,
                rationale=rationale
            )
        )
    
    def _validate_rationale(self, rationale: str, strategy_type: StrategyType) -> bool:
        """Validate rationale against expected templates for strategy type.
        
        Args:
            rationale: Rationale text to validate
            strategy_type: Strategy type to check against
            
        Returns:
            True if rationale matches expected patterns
        """
        templates = self.rationale_templates[strategy_type]
        rationale_lower = rationale.lower().strip()
        
        for template in templates:
            # Check if template is a regex pattern
            if template.startswith(r"input space size"):
                if re.match(r"input space size:?\s*\d*", rationale_lower):
                    return True
            else:
                # Simple string matching
                if template.lower() in rationale_lower:
                    return True
        
        return False
    
    def generate_standard_comment(self, strategy_type: StrategyType, max_examples: int, 
                                 input_space_size: Optional[int] = None) -> str:
        """Generate a standardized comment for given parameters.
        
        Args:
            strategy_type: Type of strategy being documented
            max_examples: Number of examples to use
            input_space_size: Size of input space (for finite strategies)
            
        Returns:
            Standardized comment string
        """
        # Select appropriate rationale template
        if strategy_type == StrategyType.BOOLEAN:
            rationale = "True/False coverage"
        elif strategy_type == StrategyType.SMALL_FINITE:
            if input_space_size is not None:
                rationale = f"input space size: {input_space_size}"
            else:
                rationale = "finite coverage"
        elif strategy_type == StrategyType.MEDIUM_FINITE:
            rationale = "adequate finite coverage"
        elif strategy_type == StrategyType.COMPLEX:
            rationale = "adequate coverage"
        elif strategy_type == StrategyType.COMBINATION:
            rationale = "combination coverage"
        else:
            rationale = "adequate coverage"
        
        pattern = CommentPattern(
            strategy_type=strategy_type.value,
            max_examples=max_examples,
            rationale=rationale
        )
        
        return pattern.to_standardized_format()


class CommentFormatRegistry:
    """Registry of format templates and validation rules."""
    
    def __init__(self):
        """Initialize registry with standard format templates."""
        self.validator = CommentFormatValidator()
        
        # Standard format templates by strategy type
        self.format_templates = {
            StrategyType.BOOLEAN: "# Boolean strategy: {max_examples} examples (True/False coverage)",
            StrategyType.SMALL_FINITE: "# Small finite strategy: {max_examples} examples (input space size: {input_space_size})",
            StrategyType.MEDIUM_FINITE: "# Medium finite strategy: {max_examples} examples (adequate finite coverage)",
            StrategyType.COMPLEX: "# Complex strategy: {max_examples} examples (adequate coverage)",
            StrategyType.COMBINATION: "# Combination strategy: {max_examples} examples (combination coverage)"
        }
    
    def get_template(self, strategy_type: StrategyType) -> str:
        """Get format template for strategy type.
        
        Args:
            strategy_type: Strategy type to get template for
            
        Returns:
            Format template string with placeholders
        """
        return self.format_templates.get(strategy_type, self.format_templates[StrategyType.COMPLEX])
    
    def get_all_templates(self) -> Dict[StrategyType, str]:
        """Get all format templates.
        
        Returns:
            Dictionary mapping strategy types to format templates
        """
        return self.format_templates.copy()


# =============================================================================
# COMMENT ANALYSIS
# =============================================================================

class CommentAnalyzer:
    """Analyzes test files for comment format compliance and consistency."""
    
    def __init__(self):
        """Initialize analyzer with validation and mapping tools."""
        self.validator = CommentFormatValidator()
        
        # Default: document every custom max_examples (strict per guide).
        # Optional escape hatch: set SKIP_STANDARD_MAX_EXAMPLES=true to allow
        # historical exemptions for {2, 5, 10, 20, 50, 100}.
        default_standard_values = {2, 5, 10, 20, 50, 100}
        skip_standard = os.getenv("SKIP_STANDARD_MAX_EXAMPLES", "").lower() in {"1", "true", "yes", "on"}
        self.standard_values = default_standard_values if skip_standard else set()
        
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
        excluded_patterns = {
            'test_comment_format.py', 
            'test_comment_standardizer.py', 
            'file_analyzer.py',
            'tools/test_optimization',
            'tools/validate_comments.py'
        }
        
        for root, dirs, files in os.walk(directory_path):
            # Skip excluded directories
            if any(ex in root for ex in excluded_patterns):
                continue
                
            for file in files:
                if file.startswith('test_') and file.endswith('.py'):
                    # Check for excluded files
                    if file in excluded_patterns:
                        continue
                        
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

        # Detect strategy mismatches
        inconsistencies.extend(self._detect_strategy_mismatch_patterns(file_analyses))
        
        return inconsistencies
    
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
                description=f"Found {total_mismatches} strategy mismatches (documented vs implemented) across {len(files_with_mismatches)} files",
                affected_files=[analysis.file_path for analysis in files_with_mismatches],
                affected_lines=affected_lines,
                suggested_resolution="Update comments to match actual implementation strategy"
            ))
        
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
                rationale = comment.rationale.lower().strip()
                # Normalize expected variations that should not be treated as inconsistencies.
                #
                # - Small finite: rationale is expected to vary by input space size (N).
                #   Treat all "input space size: <number>" as one canonical pattern.
                # - Complex: multiple rationales are explicitly allowed by the docs
                #   (e.g. "adequate coverage" vs "performance optimized"), so don't
                #   treat that as an inconsistency.
                if strategy_type == 'Small finite' and rationale.startswith('input space size'):
                    rationale = 'input space size: <n>'
                rationales.add(rationale)
                affected_files.add(file_path)
                if comment.line_number:
                    affected_lines.append((file_path, comment.line_number))
            
            # If more than one unique rationale for same strategy type, it's inconsistent
            if strategy_type == 'Complex':
                continue
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
        strategy_mismatches = []
        
        for test_info in property_tests:
            func_name, start_line, end_line, max_examples, decorator_start = test_info
            
            # Look for documentation comments immediately preceding the decorator
            comments_in_function = self._extract_documentation_comments(lines, decorator_start)
            
            # Check if any comment is a valid standardized comment
            has_valid_comment = False
            for line_num, comment_text in comments_in_function:
                validation_result = self.validator.validate_comment_format(comment_text)
                
                if validation_result.is_valid:
                    has_valid_comment = True
                    pattern = validation_result.parsed_pattern
                    pattern.line_number = line_num
                    valid_comments.append(pattern)
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
            if has_valid_comment and valid_comments:
                documented_tests += 1
                
                # Get the most recent valid comment for this function
                current_comment = valid_comments[-1]
                
                # Extract full function code including decorators
                func_code = '\n'.join(lines[decorator_start:end_line])
                
                # Analyze actual strategy from code
                strategy_classification = self._analyze_strategy_from_code(func_code)
                
                if strategy_classification:
                    actual_type = strategy_classification.strategy_type.value.lower()
                    doc_type = current_comment.strategy_type.lower()
                    
                    # Check for mismatch
                    # Allow slight variations or specific upgrades (e.g. finite -> small finite)
                    # But flag gross mismatches like Boolean vs Complex
                    mismatch = False
                    if actual_type == 'boolean' and doc_type != 'boolean':
                        mismatch = True
                    elif 'finite' in actual_type and 'finite' not in doc_type and doc_type != 'boolean':
                        # Small/Medium finite should be documented as finite
                        # Allow "Complex" for finite? No, guidelines say be specific.
                        mismatch = True
                    
                    if mismatch:
                        strategy_mismatches.append(StrategyMismatch(
                            line_number=current_comment.line_number,
                            function_name=func_name,
                            documented_type=current_comment.strategy_type,
                            implemented_type=strategy_classification.strategy_type.value,
                            rationale=f"Code implements '{strategy_classification.strategy_type.value}' but is documented as '{current_comment.strategy_type}'"
                        ))
            
            # Check if this test needs documentation
            # Extract the function code to check for CI optimization patterns
            func_code = '\n'.join(lines[decorator_start:end_line])
            has_ci_optimization = self._has_ci_optimization_pattern(func_code)
            
            # Tests need documentation if:
            # 1. They have non-standard max_examples values, OR
            # 2. They have CI optimization patterns (even with standard values)
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
        """Find all property-based test functions in the content.
        
        Returns:
            List of tuples: (function_name, start_line, end_line, max_examples, decorator_start_line)
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
                        # Get indentation level from the raw line
                        raw_line = lines[j]
                        indentation = len(raw_line) - len(raw_line.lstrip())
                        
                        # Allow broader function names, including unicode and dashes generated
                        # by Hypothesis, by accepting any non-whitespace characters up to '('.
                        func_match = re.match(r'def\s+(test_[^\s(]+)\s*\(', next_line)
                        if func_match:
                            func_name = func_match.group(1)
                            
                            # Find the end of the function
                            # Stop at next line with same or lower indentation (that isn't a comment/empty)
                            end_line = j + 1
                            while end_line < len(lines):
                                line_content = lines[end_line]
                                stripped = line_content.strip()
                                
                                # Skip empty lines and comments
                                if not stripped or stripped.startswith('#'):
                                    end_line += 1
                                    continue
                                
                                # Check indentation
                                current_indent = len(line_content) - len(line_content.lstrip())
                                if current_indent <= indentation:
                                    # Found start of next block (could be decorator or def)
                                    # But wait, decorators for next function might be at same indentation
                                    # If it's a decorator, it belongs to the NEXT function, so we stop here.
                                    break
                                
                                end_line += 1
                            
                            
                            property_tests.append((
                                func_name,
                                j + 1,  # Line numbers are 1-based (function definition line)
                                end_line,
                                max_examples,
                                i  # Decorator start line (0-based index)
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
    
    def _extract_documentation_comments(self, lines: List[str], decorator_start: int) -> List[Tuple[int, str]]:
        """Extract documentation comments near a test decorator block.
        
        Picks up comments directly above @given as well as comments placed
        between decorators (e.g., between @given and @settings).
        """
        comments = []

        # Look upward from the first decorator.
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

        # Also collect comments after the @given decorator.
        #
        # IMPORTANT:
        # @given decorators frequently span multiple lines, e.g.
        #
        #   @given(
        #       st.integers(...),
        #       st.floats(...),
        #   )
        #   # Small finite strategy: 6 examples (input space size: 6)
        #   @settings(max_examples=6, deadline=None)
        #
        # We must scan forward until we reach the next decorator that ends the
        # "decorator block" for this test (typically @settings or def).
        forward_idx = decorator_start + 1
        while forward_idx < len(lines):
            stripped = lines[forward_idx].strip()
            # Stop at the next decorator that begins settings, or the function
            # definition itself. This makes the scan robust to multi-line
            # @given(...) arguments.
            if stripped.startswith('@settings') or stripped.startswith('def ') or stripped.startswith('class '):
                break
            if stripped.startswith('#'):
                comments.append((forward_idx + 1, f"# {stripped.lstrip('#').strip()}"))
            forward_idx += 1

        return sorted(comments, key=lambda c: c[0])
    
    def _looks_like_max_examples_comment(self, comment: str) -> bool:
        """Check if a comment looks like it's trying to document max_examples.
        
        This function is intentionally strict to avoid false positives from
        regular code comments that happen to contain words like 'strategy' or
        'property'. A max_examples documentation comment should follow a
        specific pattern.
        """
        comment_lower = comment.lower()
        
        # Skip property test documentation comments (e.g., "# **Feature: ...")
        # These are test property documentation, not max_examples documentation
        if '**feature:' in comment_lower or '**property' in comment_lower:
            return False
        
        # Skip comments that are clearly not max_examples documentation
        if comment_lower.startswith('# *for any*'):
            return False
        
        # Pattern 1: Contains "N examples" where N is a number
        # This is the most reliable indicator
        has_examples_pattern = re.search(r'\d+\s+examples', comment_lower)
        if has_examples_pattern:
            return True
        
        # Pattern 2: Contains "strategy:" followed by something
        # e.g., "# Boolean strategy: ..." or "# Complex strategy: ..."
        has_strategy_colon = re.search(r'\b(boolean|complex|combination|finite|small finite|medium finite)\s+strategy\s*:', comment_lower)
        if has_strategy_colon:
            return True
        
        # Pattern 3: Starts with a strategy type name followed by "strategy"
        # e.g., "# Boolean strategy" at the start (but not "# Boolean strategy documentation")
        if re.match(r'^#\s*(boolean|complex|combination|small finite|medium finite)\s+strategy\s*:', comment_lower):
            return True
        
        # Don't flag other comments - they're likely regular code comments
        return False
    
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
    
    def _has_ci_optimization_pattern(self, func_code: str) -> bool:
        """Check if function code contains CI optimization patterns.
        
        Args:
            func_code: The function source code
            
        Returns:
            True if CI optimization pattern is detected
        """
        # Patterns that indicate CI optimization
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
    
    def _analyze_strategy_from_code(self, func_code: str) -> Optional[CommentStrategyClassification]:
        """Analyze strategy from function code using StrategyClassifier.
        
        This method uses the proper StrategyClassifier from strategy_analyzer
        to ensure consistent strategy classification across all modules.
        
        Args:
            func_code: Function source code
            
        Returns:
            CommentStrategyClassification if analysis successful, None otherwise
        """
        # Import StrategyClassifier lazily to avoid circular imports
        from .strategy_analyzer import StrategyClassifier
        
        # Extract @given decorator
        given_match = re.search(r'@given\([^)]+\)', func_code, re.DOTALL)
        if not given_match:
            return None
        
        strategy_code = given_match.group(0)
        
        # Use classify_strategy_for_comments to get CommentStrategyClassification with rationale
        classifier = StrategyClassifier()
        classification = classifier.classify_strategy_for_comments(strategy_code)
        
        return classification


# =============================================================================
# COMMENT STANDARDIZATION
# =============================================================================

class CommentStandardizer:
    """Automated comment generation and standardization tool."""
    
    def __init__(self, backup_dir: Optional[str] = None, enable_backups: bool = False):
        """Initialize standardizer with analysis and validation tools.
        
        Args:
            backup_dir: Directory for backup files. If None, uses default backup location.
            enable_backups: Whether to write backup files before modifying tests.
        """
        self.analyzer = CommentAnalyzer()
        self.validator = CommentFormatValidator()
        
        # Backward compatibility: performance_standardizer attribute
        # This is used by tests that expect the old API
        # Initialized lazily to avoid circular imports
        self._performance_standardizer = None
        
        # Set up backup directory
        env_enable = os.getenv("COMMENT_STANDARDIZER_ENABLE_BACKUPS", "").lower() in {"1", "true", "yes", "on"}
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
        
        # Pattern to match @settings decorator with max_examples
        self.settings_pattern = re.compile(r'(@settings\([^)]*max_examples\s*=\s*\d+[^)]*\))', re.DOTALL)
        
        # Pattern to match @given decorator
        self.given_pattern = re.compile(r'(@given\([^)]*\))', re.DOTALL)
        
        # Pattern to match function definition
        self.function_pattern = re.compile(r'(def\s+test_[^\s(]+\s*\([^)]*\):)')
    
    @property
    def performance_standardizer(self):
        """Backward compatibility property for performance_standardizer.
        
        This property lazily initializes OptimizationAwareCommentStandardizer
        to avoid circular imports with optimization_detector module.
        """
        if self._performance_standardizer is None:
            from .optimization_detector import OptimizationAwareCommentStandardizer
            self._performance_standardizer = OptimizationAwareCommentStandardizer()
        return self._performance_standardizer
    
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
            strategy_classification = self.analyzer._analyze_strategy_from_code(func_code)
            if not strategy_classification:
                warnings.append(f"Could not classify strategy for {func_name}, using default")
                strategy_classification = CommentStrategyClassification(
                    strategy_type=StrategyType.COMPLEX,
                    rationale="adequate coverage"
                )
            
            # Generate the comment
            comment_text = self._generate_comment_for_strategy(
                strategy_classification, max_examples, func_code
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
    
    def _generate_comment_for_strategy(self, strategy_classification: CommentStrategyClassification,
                                      max_examples: int, func_code: str) -> str:
        """Generate a comment for a given strategy classification.
        
        Args:
            strategy_classification: Strategy classification result
            max_examples: Number of examples
            func_code: Function source code (for CI/performance optimization detection)
            
        Returns:
            Generated comment string
        """
        # Check for CI optimization
        if self.analyzer._has_ci_optimization_pattern(func_code):
            rationale = "CI optimized"
        # Check for performance optimization (complex strategy with low max_examples)
        elif (strategy_classification.strategy_type == StrategyType.COMPLEX and
              max_examples <= 5):
            rationale = "performance optimized"
        else:
            rationale = strategy_classification.rationale
        
        # Generate comment
        pattern = CommentPattern(
            strategy_type=strategy_classification.strategy_type.value,
            max_examples=max_examples,
            rationale=rationale
        )
        
        return pattern.to_standardized_format()
    
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
        if not self.backups_enabled or not self.backup_dir:
            raise ValueError("Backups are disabled for this standardizer instance")
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
        if not self.backups_enabled or not self.backup_dir:
            return False
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
        """Clean up old backup files, keeping only the most recent ones.
        
        Args:
            keep_count: Number of backup files to keep
            
        Returns:
            Number of backup files removed
        """
        if not self.backups_enabled or not self.backup_dir:
            return 0
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
        if not self.backups_enabled:
            return False
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
        if not self.backups_enabled:
            return 0
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


# =============================================================================
# PUBLIC API EXPORTS
# =============================================================================

__all__ = [
    # Enums
    'StrategyType',
    
    # Data models
    'CommentPattern',
    'ValidationResult',
    'FormatViolation',
    'Inconsistency',
    'StrategyMismatch',
    'FileAnalysis',
    'DirectoryAnalysis',
    'StandardizationResult',
    'BatchResult',
    'CommentStrategyClassification',
    
    # Main classes
    'CommentFormatValidator',
    'CommentFormatRegistry',
    'CommentAnalyzer',
    'CommentStandardizer',
]

