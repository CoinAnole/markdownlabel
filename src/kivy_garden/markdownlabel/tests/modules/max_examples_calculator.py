"""Max examples calculator for Hypothesis test optimization.

This module calculates optimal max_examples values based on strategy analysis
and environment conditions (CI vs local development).
"""

import os
from typing import Optional

from .strategy_analyzer import StrategyType, StrategyAnalysis, StrategyClassifier


class MaxExamplesCalculator:
    """Calculates optimal max_examples based on input space analysis."""

    # Base limits for different strategy types
    COMPLEXITY_LIMITS = {
        StrategyType.BOOLEAN: 2,
        StrategyType.SMALL_FINITE: lambda size: size,
        StrategyType.MEDIUM_FINITE: lambda size: min(size, 20),
        StrategyType.COMBINATION: lambda size: min(size, 50),
        StrategyType.COMPLEX: lambda complexity: min(10 + (complexity * 10), 50)
    }

    def __init__(self, classifier: Optional[StrategyClassifier] = None):
        """Initialize calculator with optional classifier.

        Args:
            classifier: StrategyClassifier instance, creates new one if None
        """
        self.classifier = classifier or StrategyClassifier()

    def calculate_optimal_examples(self,
                                  strategy_code: str,
                                  current_examples: Optional[int] = None) -> int:
        """Calculate optimal max_examples for given strategy code.

        Args:
            strategy_code: String containing Hypothesis strategy definition
            current_examples: Current max_examples value (for comparison)

        Returns:
            Optimal max_examples value
        """
        analysis = self.classifier.classify_strategy(strategy_code)
        return self._calculate_from_analysis(analysis)

    def calculate_from_analysis(self, analysis: StrategyAnalysis) -> int:
        """Calculate optimal max_examples from strategy analysis.

        Args:
            analysis: StrategyAnalysis object

        Returns:
            Optimal max_examples value
        """
        return self._calculate_from_analysis(analysis)

    def _calculate_from_analysis(self, analysis: StrategyAnalysis) -> int:
        """Internal calculation method."""
        base_examples = self._get_base_examples(analysis)

        # Apply CI optimization if in CI environment
        if self._is_ci_environment():
            return self._apply_ci_optimization(base_examples, analysis.strategy_type)

        return base_examples

    def _get_base_examples(self, analysis: StrategyAnalysis) -> int:
        """Get base max_examples before CI optimization."""
        strategy_type = analysis.strategy_type

        if strategy_type == StrategyType.BOOLEAN:
            return self.COMPLEXITY_LIMITS[StrategyType.BOOLEAN]

        elif strategy_type in [StrategyType.SMALL_FINITE, StrategyType.MEDIUM_FINITE]:
            if analysis.input_space_size is None:
                # Fallback for parsing errors
                return 20 if strategy_type == StrategyType.MEDIUM_FINITE else 10

            limit_func = self.COMPLEXITY_LIMITS[strategy_type]
            return limit_func(analysis.input_space_size)

        elif strategy_type == StrategyType.COMBINATION:
            if analysis.input_space_size is None:
                # If any component is infinite, treat as complex
                return self._get_complex_examples(analysis.complexity_level)

            limit_func = self.COMPLEXITY_LIMITS[StrategyType.COMBINATION]
            return limit_func(analysis.input_space_size)

        else:  # StrategyType.COMPLEX
            return self._get_complex_examples(analysis.complexity_level)

    def _get_complex_examples(self, complexity_level: int) -> int:
        """Calculate examples for complex strategies based on complexity."""
        limit_func = self.COMPLEXITY_LIMITS[StrategyType.COMPLEX]
        return limit_func(complexity_level)

    def _is_ci_environment(self) -> bool:
        """Check if running in CI environment."""
        ci_indicators = [
            'CI', 'CONTINUOUS_INTEGRATION', 'GITHUB_ACTIONS',
            'TRAVIS', 'CIRCLECI', 'JENKINS_URL', 'BUILDKITE'
        ]
        return any(os.getenv(indicator) for indicator in ci_indicators)

    def _apply_ci_optimization(self, base_examples: int, strategy_type: StrategyType) -> int:
        """Apply CI-specific optimizations while maintaining coverage.

        Args:
            base_examples: Base max_examples value
            strategy_type: Type of strategy being optimized

        Returns:
            CI-optimized max_examples value
        """
        # Never reduce finite strategies in CI - they need full coverage
        if strategy_type in [StrategyType.BOOLEAN, StrategyType.SMALL_FINITE, StrategyType.MEDIUM_FINITE]:
            return base_examples

        # For combination strategies, only reduce if they're large
        if strategy_type == StrategyType.COMBINATION:
            if base_examples > 20:
                return max(base_examples // 2, 10)
            return base_examples

        # Complex strategies can be reduced more aggressively in CI
        if strategy_type == StrategyType.COMPLEX:
            return max(base_examples // 2, 5)

        return base_examples

    def get_optimization_ratio(self, current_examples: int, optimal_examples: int) -> float:
        """Calculate the optimization ratio (time savings percentage).

        Args:
            current_examples: Current max_examples value
            optimal_examples: Optimal max_examples value

        Returns:
            Percentage of time that could be saved (0.0 to 1.0)
        """
        if current_examples <= optimal_examples:
            return 0.0

        return (current_examples - optimal_examples) / current_examples

    def is_over_testing(self, strategy_code: str, current_examples: int) -> bool:
        """Check if current max_examples represents over-testing.

        Args:
            strategy_code: String containing Hypothesis strategy definition
            current_examples: Current max_examples value

        Returns:
            True if current_examples is excessive for the strategy
        """
        optimal = self.calculate_optimal_examples(strategy_code)
        return current_examples > optimal
