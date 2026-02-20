"""
Test analysis infrastructure for MarkdownLabel test suite refactoring.

This package provides tools for analyzing test files to identify:
- Naming/assertion mismatches
- Duplicate helper functions
- Test organization issues
- Meta-test categorization opportunities
- Hypothesis test optimization patterns
- Comment format validation and standardization
- Over-testing detection and prevention
- Strategy classification and analysis
"""

# =============================================================================
# Imports from assertion_analyzer module
# =============================================================================
from .assertion_analyzer import (
    AssertionType,
    AssertionPattern,
    AssertionAnalysis,
    AssertionAnalyzer
)

# =============================================================================
# Imports from comment_manager module
# =============================================================================
from .comment_manager import (
    StrategyType,
    CommentPattern,
    ValidationResult,
    FormatViolation,
    Inconsistency,
    StrategyMismatch,
    FileAnalysis as CommentFileAnalysis,
    DirectoryAnalysis,
    StandardizationResult,
    BatchResult,
    CommentStrategyClassification,
    CommentFormatValidator,
    CommentFormatRegistry,
    CommentAnalyzer,
    CommentStandardizer
)

# =============================================================================
# Imports from duplicate_detector module
# =============================================================================
from .duplicate_detector import (
    DuplicateGroup,
    ConsolidationReport,
    DuplicateDetector
)

# =============================================================================
# Imports from file_analyzer module
# =============================================================================
from .file_analyzer import (
    PropertyTest as FileAnalyzerPropertyTest,
    CommentInfo,
    OptimizationRecommendation,
    FileAnalysis,
    CommentComplianceStats,
    ValidationReport as FileAnalyzerValidationReport,
    FileAnalyzer
)

# =============================================================================
# Imports from file_parser module
# =============================================================================
from .file_parser import (
    ParsedMethod,
    ParsedClass,
    HelperFunction,
    FileMetadata,
    FileParser
)

# =============================================================================
# Imports from max_examples_calculator module
# =============================================================================
from .max_examples_calculator import MaxExamplesCalculator

# =============================================================================
# Imports from naming_convention_validator module
# =============================================================================
from .naming_convention_validator import (
    NamingViolationType,
    NamingViolation,
    NamingConventionReport,
    NamingConventionValidator
)

# =============================================================================
# Imports from optimization_detector module
# =============================================================================
from .optimization_detector import (
    OptimizationType,
    CIOptimizationPattern,
    OptimizationInfo,
    OptimizationDetector,
    OptimizationCommentGenerator,
    OptimizationAwareCommentStandardizer
)

# =============================================================================
# Imports from over_testing_validator module
# =============================================================================
from .over_testing_validator import (
    ValidationThresholds,
    ValidationResult as OverTestingValidationResult,
    OverTestingValidator
)

# =============================================================================
# Imports from strategy_analyzer module
# =============================================================================
from .strategy_analyzer import (
    StrategyAnalysis,
    StrategyClassifier,
    CodeAnalyzer,
    StrategyTypeMapper
)

# =============================================================================
# Imports from test_discovery module
# =============================================================================
from .test_discovery import (
    PropertyTest,
    find_property_tests,
    _extract_max_examples_from_settings_line,
    _extract_max_examples_from_conditional,
    has_ci_optimization_pattern,
    extract_test_code
)

# =============================================================================
# Public API exports
# =============================================================================
__all__ = [
    # From assertion_analyzer
    'AssertionType',
    'AssertionPattern',
    'AssertionAnalysis',
    'AssertionAnalyzer',

    # From comment_manager
    'StrategyType',
    'CommentPattern',
    'ValidationResult',
    'FormatViolation',
    'Inconsistency',
    'StrategyMismatch',
    'CommentFileAnalysis',
    'DirectoryAnalysis',
    'StandardizationResult',
    'BatchResult',
    'CommentStrategyClassification',
    'CommentFormatValidator',
    'CommentFormatRegistry',
    'CommentAnalyzer',
    'CommentStandardizer',

    # From duplicate_detector
    'DuplicateGroup',
    'ConsolidationReport',
    'DuplicateDetector',

    # From file_analyzer
    'FileAnalyzerPropertyTest',
    'CommentInfo',
    'OptimizationRecommendation',
    'FileAnalysis',
    'CommentComplianceStats',
    'FileAnalyzerValidationReport',
    'FileAnalyzer',

    # From file_parser
    'ParsedMethod',
    'ParsedClass',
    'HelperFunction',
    'FileMetadata',
    'FileParser',

    # From max_examples_calculator
    'MaxExamplesCalculator',

    # From naming_convention_validator
    'NamingViolationType',
    'NamingViolation',
    'NamingConventionReport',
    'NamingConventionValidator',

    # From optimization_detector
    'OptimizationType',
    'CIOptimizationPattern',
    'OptimizationInfo',
    'OptimizationDetector',
    'OptimizationCommentGenerator',
    'OptimizationAwareCommentStandardizer',

    # From over_testing_validator
    'ValidationThresholds',
    'OverTestingValidationResult',
    'OverTestingValidator',

    # From strategy_analyzer
    'StrategyAnalysis',
    'StrategyClassifier',
    'CodeAnalyzer',
    'StrategyTypeMapper',

    # From test_discovery
    'PropertyTest',
    'find_property_tests',
    '_extract_max_examples_from_settings_line',
    '_extract_max_examples_from_conditional',
    'has_ci_optimization_pattern',
    'extract_test_code',
]
