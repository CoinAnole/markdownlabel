"""Test optimization tools for Hypothesis property-based tests.

This package provides tools to analyze and optimize max_examples values
in property-based tests for better performance while maintaining coverage.
"""

from .strategy_classifier import StrategyClassifier, StrategyType, StrategyAnalysis
from .max_examples_calculator import MaxExamplesCalculator
from .test_file_analyzer import TestFileAnalyzer, OptimizationRecommendation, FileAnalysis, ValidationReport
from .over_testing_validator import OverTestingValidator, ValidationThresholds, ValidationResult

__all__ = [
    'StrategyClassifier',
    'StrategyType', 
    'StrategyAnalysis',
    'MaxExamplesCalculator',
    'TestFileAnalyzer',
    'OptimizationRecommendation',
    'FileAnalysis',
    'ValidationReport',
    'OverTestingValidator',
    'ValidationThresholds',
    'ValidationResult'
]