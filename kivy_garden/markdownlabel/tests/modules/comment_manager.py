"""Unified comment management module for property-based test documentation.

This module consolidates comment format validation, analysis, and standardization
functionality. It now serves as a compatibility layer that re-exports from the
split modules for backward compatibility.

The functionality has been split into three focused modules:
- comment_validation.py: Format validation and comment generation
- comment_analysis.py: Test file analysis and compliance checking
- comment_standardization.py: Automated comment standardization

This module maintains backward compatibility by re-exporting all public APIs.
"""

# Re-export everything from the split modules for backward compatibility
from .comment_validation import (
    StrategyType,
    CommentPattern,
    ValidationResult,
    CommentFormatValidator,
    CommentFormatRegistry,
)

from .comment_analysis import (
    FormatViolation,
    Inconsistency,
    StrategyMismatch,
    FileAnalysis,
    DirectoryAnalysis,
    CommentStrategyClassification,
    CommentAnalyzer,
)

from .comment_standardization import (
    StandardizationResult,
    BatchResult,
    CommentStandardizer,
)


__all__ = [
    # Enums
    'StrategyType',

    # Data models from validation
    'CommentPattern',
    'ValidationResult',

    # Data models from analysis
    'FormatViolation',
    'Inconsistency',
    'StrategyMismatch',
    'FileAnalysis',
    'DirectoryAnalysis',
    'CommentStrategyClassification',

    # Data models from standardization
    'StandardizationResult',
    'BatchResult',

    # Main classes
    'CommentFormatValidator',
    'CommentFormatRegistry',
    'CommentAnalyzer',
    'CommentStandardizer',
]
