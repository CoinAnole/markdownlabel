"""Test optimization tools for Hypothesis property-based tests.

This package provides tools to analyze and optimize max_examples values
in property-based tests for better performance while maintaining coverage.
"""

from .strategy_classifier import StrategyClassifier, StrategyType, StrategyAnalysis
from .max_examples_calculator import MaxExamplesCalculator
from .file_analyzer import FileAnalyzer, OptimizationRecommendation, FileAnalysis, ValidationReport
from .over_testing_validator import OverTestingValidator, ValidationThresholds, ValidationResult
from .comment_analyzer import CommentAnalyzer, FileAnalysis as CommentFileAnalysis, DirectoryAnalysis, FormatViolation, Inconsistency

__all__ = [
    'StrategyClassifier',
    'StrategyType', 
    'StrategyAnalysis',
    'MaxExamplesCalculator',
    'FileAnalyzer',
    'OptimizationRecommendation',
    'FileAnalysis',
    'ValidationReport',
    'OverTestingValidator',
    'ValidationThresholds',
    'ValidationResult',
    'CommentAnalyzer',
    'CommentFileAnalysis',
    'DirectoryAnalysis',
    'FormatViolation',
    'Inconsistency'
]