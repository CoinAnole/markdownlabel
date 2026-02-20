"""Strategy analysis system for Hypothesis test optimization.

This module provides tools to analyze Hypothesis strategies and classify them
by input space size and complexity for optimal max_examples calculation.
It consolidates strategy classification and comment format mapping functionality.
"""

import ast
import re
from dataclasses import dataclass
from typing import Optional, List

from .comment_manager import StrategyType


@dataclass
class StrategyAnalysis:
    """Analysis result for a Hypothesis strategy."""
    strategy_type: StrategyType
    input_space_size: Optional[int] = None
    complexity_level: int = 1
    components: List[str] = None

    def __post_init__(self):
        if self.components is None:
            self.components = []


class StrategyClassifier:
    """Classifies Hypothesis strategies by input space size and complexity.

    This class provides both basic strategy classification and comment-format
    classification for standardized test documentation.
    """

    def __init__(self):
        """Initialize classifier with regex patterns for strategy detection."""
        # Regex patterns for strategy detection
        self.boolean_pattern = re.compile(r'st\.booleans\(\)')
        self.integer_pattern = re.compile(
            r'st\.integers\(\s*min_value\s*=\s*(-?\d+)\s*,\s*max_value\s*=\s*(-?\d+)\s*\)'
        )
        self.sampled_from_pattern = re.compile(r'st\.sampled_from\(\s*\[([^\]]*)\]\s*\)')
        self.text_pattern = re.compile(r'st\.text\(')
        self.floats_pattern = re.compile(r'st\.floats\(')
        self.tuples_pattern = re.compile(r'st\.tuples\(')

    def classify_strategy(self, strategy_code: str) -> StrategyAnalysis:
        """Analyze strategy code and return classification.

        Args:
            strategy_code: String containing Hypothesis strategy definition

        Returns:
            StrategyAnalysis with type, size, and complexity information
        """
        strategy_code = strategy_code.strip()

        # First, detect tuple-based combinations so we correctly expand st.tuples(...)
        if self.tuples_pattern.search(strategy_code):
            components = self._extract_tuple_components(strategy_code)
            if len(components) > 1:  # Only treat as combination if multiple components
                total_size = self._calculate_combination_size(components)

                return StrategyAnalysis(
                    strategy_type=StrategyType.COMBINATION,
                    input_space_size=total_size,
                    components=components
                )

        # Check for multi-argument @given usage (variables or inline strategies)
        # Use AST so we can recognize variable-based strategies, not just inline st.* calls.
        if self._is_combination_strategy(strategy_code):
            components = self._extract_strategy_components(strategy_code)
            total_size = self._calculate_combination_size(components)

            return StrategyAnalysis(
                strategy_type=StrategyType.COMBINATION,
                input_space_size=total_size,
                components=components
            )

        # Check for boolean strategies
        if self.boolean_pattern.search(strategy_code):
            return StrategyAnalysis(
                strategy_type=StrategyType.BOOLEAN,
                input_space_size=2,
                components=['st.booleans()']
            )

        # Check for integer range strategies
        integer_match = self.integer_pattern.search(strategy_code)
        if integer_match:
            min_val = int(integer_match.group(1))
            max_val = int(integer_match.group(2))
            size = max_val - min_val + 1

            # Treat 51-value ranges as finite (medium) instead of complex.
            if size <= 10:
                strategy_type = StrategyType.SMALL_FINITE
            elif size <= 51:
                strategy_type = StrategyType.MEDIUM_FINITE
            else:
                strategy_type = StrategyType.COMPLEX
                size = None  # Large ranges are effectively infinite

            return StrategyAnalysis(
                strategy_type=strategy_type,
                input_space_size=size,
                components=[f'st.integers(min_value={min_val}, max_value={max_val})']
            )

        # Check for sampled_from strategies
        sampled_match = self.sampled_from_pattern.search(strategy_code)
        if sampled_match:
            items_str = sampled_match.group(1)
            # Count items by splitting on commas (simple heuristic)
            items = [item.strip() for item in items_str.split(',') if item.strip()]
            size = len(items)

            if size <= 10:
                strategy_type = StrategyType.SMALL_FINITE
            elif size <= 50:
                strategy_type = StrategyType.MEDIUM_FINITE
            else:
                strategy_type = StrategyType.COMPLEX
                size = None

            return StrategyAnalysis(
                strategy_type=strategy_type,
                input_space_size=size,
                components=[f'st.sampled_from([{items_str}])']
            )

        # Default to complex for text, floats, and other infinite strategies
        complexity = self._assess_complexity(strategy_code)
        return StrategyAnalysis(
            strategy_type=StrategyType.COMPLEX,
            input_space_size=None,
            complexity_level=complexity,
            components=[strategy_code]
        )

    def classify_strategy_for_comments(self, strategy_code: str) -> 'CommentStrategyClassification':
        """Classify strategy and return comment-format classification.

        This method provides the same functionality as the original StrategyTypeMapper,
        returning a classification with comment-format terminology and rationale.

        Args:
            strategy_code: String containing Hypothesis strategy definition

        Returns:
            CommentStrategyClassification with type and rationale information
        """
        # Use existing classifier to get base analysis
        existing_analysis = self.classify_strategy(strategy_code)

        # Generate appropriate rationale based on strategy type
        if existing_analysis.strategy_type == StrategyType.BOOLEAN:
            rationale = "True/False coverage"
        elif existing_analysis.strategy_type == StrategyType.SMALL_FINITE:
            if existing_analysis.input_space_size is not None:
                rationale = f"input space size: {existing_analysis.input_space_size}"
            else:
                rationale = "finite coverage"
        elif existing_analysis.strategy_type == StrategyType.MEDIUM_FINITE:
            rationale = "adequate finite coverage"
        elif existing_analysis.strategy_type == StrategyType.COMBINATION:
            rationale = "combination coverage"
        elif existing_analysis.strategy_type == StrategyType.COMPLEX:
            # Check if this is a performance-optimized case
            if self._is_performance_optimized(strategy_code):
                rationale = "performance optimized"
            else:
                rationale = "adequate coverage"
        else:
            rationale = "adequate coverage"

        return CommentStrategyClassification(
            strategy_type=existing_analysis.strategy_type,
            rationale=rationale,
            input_space_size=existing_analysis.input_space_size,
            complexity_level=existing_analysis.complexity_level,
            components=existing_analysis.components or []
        )

    def detect_strategy_from_test_code(self, test_code: str) -> Optional['CommentStrategyClassification']:
        """Detect strategy type from complete test function code.

        Args:
            test_code: Complete test function source code

        Returns:
            CommentStrategyClassification if strategy detected, None otherwise
        """
        # Extract @given decorator and its strategy
        strategy_code = self._extract_given_strategy(test_code)
        if not strategy_code:
            return None

        return self.classify_strategy_for_comments(strategy_code)

    def handle_edge_cases(self, strategy_code: str) -> Optional['CommentStrategyClassification']:
        """Handle edge cases and complex strategy combinations.

        Args:
            strategy_code: Strategy code that may contain edge cases

        Returns:
            CommentStrategyClassification for edge cases, None if standard classification applies
        """
        # Check for CI-specific optimizations
        if self._is_ci_optimized(strategy_code):
            base_classification = self.classify_strategy_for_comments(strategy_code)
            base_classification.rationale = f"CI optimized: {base_classification.rationale}"
            return base_classification

        # Check for custom domain strategies
        if self._is_custom_domain_strategy(strategy_code):
            return CommentStrategyClassification(
                strategy_type=StrategyType.COMPLEX,
                rationale="custom domain strategy",
                input_space_size=None,
                complexity_level=2,
                components=[strategy_code]
            )

        # Check for nested tuple combinations
        if self._is_nested_combination(strategy_code):
            return CommentStrategyClassification(
                strategy_type=StrategyType.COMBINATION,
                rationale="nested combination coverage",
                input_space_size=None,
                complexity_level=3,
                components=self._extract_nested_components(strategy_code)
            )

        return None  # Use standard classification

    def calculate_input_space_size(self, strategy_code: str) -> Optional[int]:
        """Calculate the total number of possible values for a strategy.

        Args:
            strategy_code: String containing Hypothesis strategy definition

        Returns:
            Integer size for finite strategies, None for infinite strategies
        """
        analysis = self.classify_strategy(strategy_code)
        return analysis.input_space_size

    def _is_combination_strategy(self, strategy_code: str) -> bool:
        """Check if strategy code represents multiple combined strategies.

        Prefer an AST-based check so we correctly handle @given(a, b) even when
        a/b are variables defined elsewhere, not just inline st.* calls.
        """
        call = self._parse_as_call(strategy_code)
        if call:
            total_args = len(call.args) + len(call.keywords)
            if total_args > 1:
                return True

        # Fallback: look for multiple inline st.* calls as before
        strategy_calls = len(re.findall(r'st\.\w+\(', strategy_code))
        return strategy_calls > 1

    def _extract_strategy_components(self, strategy_code: str) -> List[str]:
        """Extract individual strategy components from combination."""
        call = self._parse_as_call(strategy_code)
        if call:
            components: List[str] = []
            for arg in call.args:
                components.append(self._stringify_expr(arg))
            for kw in call.keywords:
                kw_value = self._stringify_expr(kw.value)
                components.append(f"{kw.arg}={kw_value}")
            return components

        # Fallback: find all st.* calls (legacy heuristic)
        components = re.findall(r'st\.\w+\([^)]*\)', strategy_code)
        return components

    def _calculate_combination_size(self, components: List[str]) -> Optional[int]:
        """Calculate product of component strategy sizes."""
        total_size = 1

        for component in components:
            # Use direct analysis to avoid recursion
            component_size = self._get_component_size(component)
            if component_size is None:
                return None  # If any component is infinite, combination is infinite
            total_size *= component_size

            # Cap at reasonable limit to prevent overflow
            if total_size > 1000:
                return None

        return total_size

    def _get_component_size(self, component: str) -> Optional[int]:
        """Get size of a single component without full classification."""
        component = component.strip()

        # Check for boolean
        if self.boolean_pattern.search(component):
            return 2

        # Check for integer range
        integer_match = self.integer_pattern.search(component)
        if integer_match:
            min_val = int(integer_match.group(1))
            max_val = int(integer_match.group(2))
            size = max_val - min_val + 1
            return size if size <= 50 else None

        # Check for sampled_from
        sampled_match = self.sampled_from_pattern.search(component)
        if sampled_match:
            items_str = sampled_match.group(1)
            items = [item.strip() for item in items_str.split(',') if item.strip()]
            size = len(items)
            return size if size <= 50 else None

        # For other strategies, assume infinite
        return None

    def _assess_complexity(self, strategy_code: str) -> int:
        """Assess complexity level for infinite/complex strategies."""
        complexity = 1

        # Text strategies are more complex
        if self.text_pattern.search(strategy_code):
            complexity += 1

        # Float strategies with constraints are moderately complex
        if self.floats_pattern.search(strategy_code):
            complexity += 1

        # Additional complexity indicators
        if 'allow_nan=False' in strategy_code:
            complexity += 1
        if 'allow_infinity=False' in strategy_code:
            complexity += 1

        return min(complexity, 4)  # Cap at level 4

    def _parse_as_call(self, strategy_code: str) -> Optional[ast.Call]:
        """Parse strategy code fragment as a call expression for inspection."""
        try:
            expr = ast.parse(f"f({strategy_code})", mode="eval").body
        except SyntaxError:
            return None

        if isinstance(expr, ast.Call):
            return expr
        return None

    def _stringify_expr(self, node: ast.AST) -> str:
        """Render an AST node back to a readable string."""
        try:
            # ast.unparse is available on Python 3.9+
            return ast.unparse(node)  # type: ignore[attr-defined]
        except Exception:
            # Fallback to a coarse dump; better than losing the component entirely
            return ast.dump(node)

    def _extract_tuple_components(self, strategy_code: str) -> List[str]:
        """Extract components from st.tuples() strategy."""
        # Find the content inside st.tuples(...) with proper parentheses matching
        start_idx = strategy_code.find('st.tuples(')
        if start_idx == -1:
            return []

        # Find the matching closing parenthesis
        start_paren = start_idx + len('st.tuples(')
        paren_count = 1
        end_idx = start_paren

        while end_idx < len(strategy_code) and paren_count > 0:
            if strategy_code[end_idx] == '(':
                paren_count += 1
            elif strategy_code[end_idx] == ')':
                paren_count -= 1
            end_idx += 1

        if paren_count != 0:
            return []  # Unmatched parentheses

        content = strategy_code[start_paren:end_idx-1]

        # Split by commas, but be careful about nested parentheses
        components = []
        paren_depth = 0
        current_component = ""

        for char in content:
            if char == '(':
                paren_depth += 1
            elif char == ')':
                paren_depth -= 1
            elif char == ',' and paren_depth == 0:
                if current_component.strip():
                    components.append(current_component.strip())
                current_component = ""
                continue

            current_component += char

        # Add the last component
        if current_component.strip():
            components.append(current_component.strip())

        return components

    def _extract_given_strategy(self, test_code: str) -> Optional[str]:
        """Extract strategy code from @given decorator in test function."""
        # Look for @given decorator with proper parentheses matching
        start_idx = test_code.find('@given(')
        if start_idx == -1:
            return None

        # Find the matching closing parenthesis
        start_paren = start_idx + len('@given(')
        paren_count = 1
        end_idx = start_paren

        while end_idx < len(test_code) and paren_count > 0:
            if test_code[end_idx] == '(':
                paren_count += 1
            elif test_code[end_idx] == ')':
                paren_count -= 1
            end_idx += 1

        if paren_count != 0:
            return None  # Unmatched parentheses

        strategy_code = test_code[start_paren:end_idx-1]
        return strategy_code.strip()

    def _is_performance_optimized(self, strategy_code: str) -> bool:
        """Check if strategy appears to be performance-optimized."""
        # Look for indicators of performance optimization
        performance_indicators = [
            'deadline=None',
            'max_examples=2',
            'max_examples=5',
            'max_examples=10'
        ]

        return any(indicator in strategy_code for indicator in performance_indicators)

    def _is_ci_optimized(self, strategy_code: str) -> bool:
        """Check if strategy uses CI-specific optimizations."""
        # Look for CI environment checks
        ci_patterns = [
            r"os\.getenv\(['\"]CI['\"]\)",
            r"if.*CI.*else",
            r"CI.*\?.*:"
        ]

        return any(re.search(pattern, strategy_code) for pattern in ci_patterns)

    def _is_custom_domain_strategy(self, strategy_code: str) -> bool:
        """Check if strategy uses custom domain-specific generators."""
        custom_indicators = [
            'markdown_',
            'html_',
            'css_',
            'custom_',
            'domain_'
        ]

        return any(indicator in strategy_code.lower() for indicator in custom_indicators)

    def _is_nested_combination(self, strategy_code: str) -> bool:
        """Check if strategy contains nested tuple or composite combinations."""
        # Look for nested st.tuples or multiple levels of composition
        nested_patterns = [
            r'st\.tuples\([^)]*st\.tuples',
            r'st\.composite\([^)]*st\.composite',
            r'st\.one_of\([^)]*st\.one_of'
        ]

        return any(re.search(pattern, strategy_code) for pattern in nested_patterns)

    def _extract_nested_components(self, strategy_code: str) -> List[str]:
        """Extract components from nested strategy combinations."""
        # Simple extraction of top-level strategy calls
        components = re.findall(r'st\.\w+\([^)]*\)', strategy_code)
        return components[:5]  # Limit to avoid excessive detail


class CodeAnalyzer:
    """Analyzes test code to extract strategy information for comment generation."""

    def __init__(self):
        """Initialize analyzer with strategy classifier."""
        self.classifier = StrategyClassifier()

    def analyze_test_function(self, test_code: str) -> Optional['CommentStrategyClassification']:
        """Analyze complete test function and return strategy classification.

        Args:
            test_code: Complete test function source code

        Returns:
            CommentStrategyClassification if analysis successful, None otherwise
        """
        # First check for edge cases
        edge_case_result = self.classifier.handle_edge_cases(test_code)
        if edge_case_result:
            return edge_case_result

        # Use standard classification
        return self.classifier.detect_strategy_from_test_code(test_code)

    def extract_max_examples_from_settings(self, test_code: str) -> Optional[int]:
        """Extract max_examples value from @settings decorator.

        Args:
            test_code: Test function source code

        Returns:
            max_examples value if found, None otherwise
        """
        settings_pattern = re.compile(r'@settings\([^)]*max_examples\s*=\s*(\d+)', re.DOTALL)
        match = settings_pattern.search(test_code)

        if match:
            return int(match.group(1))

        return None

    def extract_function_name(self, test_code: str) -> Optional[str]:
        """Extract test function name from code.

        Args:
            test_code: Test function source code

        Returns:
            Function name if found, None otherwise
        """
        func_pattern = re.compile(r'def\s+(test_\w+)\s*\(')
        match = func_pattern.search(test_code)

        if match:
            return match.group(1)

        return None


# Import CommentStrategyClassification from comment_manager for consistency
from .comment_manager import CommentStrategyClassification


__all__ = [
    # Data classes
    'StrategyAnalysis',
    'CommentStrategyClassification',

    # Main classes
    'StrategyClassifier',
    'CodeAnalyzer',
]

# Backward compatibility alias for StrategyTypeMapper
# This allows code that imported StrategyTypeMapper to continue working
StrategyTypeMapper = StrategyClassifier
