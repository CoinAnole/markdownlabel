"""Property-based tests for strategy classification system.

Tests the StrategyClassifier's ability to correctly identify and categorize
Hypothesis strategies for max_examples optimization.
"""

import pytest
import os
from hypothesis import given, strategies as st, settings

from kivy_garden.markdownlabel.strategy_classifier import (
    StrategyClassifier, StrategyType, StrategyAnalysis
)


class TestStrategyClassification:
    """Property tests for strategy classification (Property 1)."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.classifier = StrategyClassifier()
    
    # **Feature: test-performance-optimization, Property 1: Boolean tests use exactly 2 examples**
    @given(st.just('st.booleans()'))
    @settings(max_examples=2, deadline=None)
    def test_boolean_strategy_classification(self, strategy_code):
        """Boolean strategies are correctly classified with input space size 2.
        
        **Validates: Requirements 1.1, 2.1**
        """
        analysis = self.classifier.classify_strategy(strategy_code)
        
        assert analysis.strategy_type == StrategyType.BOOLEAN
        assert analysis.input_space_size == 2
        assert 'st.booleans()' in analysis.components
    
    @given(st.integers(min_value=1, max_value=10), st.integers(min_value=0, max_value=5))
    @settings(max_examples=10, deadline=None)
    def test_small_integer_range_classification(self, range_size, min_offset):
        """Small integer ranges are classified as SMALL_FINITE with correct size."""
        min_val = min_offset
        max_val = min_offset + range_size - 1
        strategy_code = f'st.integers(min_value={min_val}, max_value={max_val})'
        
        analysis = self.classifier.classify_strategy(strategy_code)
        
        assert analysis.strategy_type == StrategyType.SMALL_FINITE
        assert analysis.input_space_size == range_size
        assert len(analysis.components) == 1
    
    @given(st.lists(st.text(min_size=1, max_size=3, alphabet='abc'), min_size=1, max_size=10))
    @settings(max_examples=10, deadline=None)
    def test_small_sampled_from_classification(self, items):
        """Small sampled_from lists are classified as SMALL_FINITE with correct size."""
        items_str = ', '.join(f'"{item}"' for item in items)
        strategy_code = f'st.sampled_from([{items_str}])'
        
        analysis = self.classifier.classify_strategy(strategy_code)
        
        assert analysis.strategy_type == StrategyType.SMALL_FINITE
        assert analysis.input_space_size == len(items)
        assert len(analysis.components) == 1
    
    @given(st.integers(min_value=11, max_value=50))
    @settings(max_examples=10, deadline=None)
    def test_medium_finite_classification(self, range_size):
        """Medium-sized finite strategies are classified as MEDIUM_FINITE."""
        strategy_code = f'st.integers(min_value=0, max_value={range_size-1})'
        
        analysis = self.classifier.classify_strategy(strategy_code)
        
        assert analysis.strategy_type == StrategyType.MEDIUM_FINITE
        assert analysis.input_space_size == range_size
    
    @given(st.sampled_from(['st.text()', 'st.floats()', 'st.integers()']))
    @settings(max_examples=3, deadline=None)
    def test_complex_strategy_classification(self, strategy_code):
        """Complex/infinite strategies are classified as COMPLEX."""
        analysis = self.classifier.classify_strategy(strategy_code)
        
        assert analysis.strategy_type == StrategyType.COMPLEX
        assert analysis.input_space_size is None
        assert analysis.complexity_level >= 1
    
    def test_boolean_strategy_exact_classification(self):
        """Boolean strategy classification returns exactly the expected values."""
        strategy_code = 'st.booleans()'
        analysis = self.classifier.classify_strategy(strategy_code)
        
        # This is the core property: boolean tests should use exactly 2 examples
        assert analysis.strategy_type == StrategyType.BOOLEAN
        assert analysis.input_space_size == 2
        assert analysis.components == ['st.booleans()']
        assert analysis.complexity_level == 1


class TestMaxExamplesCalculation:
    """Property tests for max_examples calculation (Property 2)."""
    
    def setup_method(self):
        """Set up test fixtures."""
        from kivy_garden.markdownlabel.max_examples_calculator import MaxExamplesCalculator
        self.calculator = MaxExamplesCalculator()
    
    # **Feature: test-performance-optimization, Property 2: Small finite strategies use input space size**
    @given(st.integers(min_value=1, max_value=10))
    @settings(max_examples=10, deadline=None)
    def test_small_finite_uses_input_space_size(self, range_size):
        """Small finite strategies should use max_examples equal to input space size.
        
        **Validates: Requirements 1.2, 1.3, 2.2**
        """
        # Test integer ranges
        strategy_code = f'st.integers(min_value=0, max_value={range_size-1})'
        optimal = self.calculator.calculate_optimal_examples(strategy_code)
        
        assert optimal == range_size, f"Expected {range_size} examples for range of size {range_size}, got {optimal}"
    
    @given(st.lists(st.text(min_size=1, max_size=2, alphabet='ab'), min_size=1, max_size=10))
    @settings(max_examples=10, deadline=None)
    def test_sampled_from_uses_list_length(self, items):
        """sampled_from strategies should use max_examples equal to list length."""
        items_str = ', '.join(f'"{item}"' for item in items)
        strategy_code = f'st.sampled_from([{items_str}])'
        
        optimal = self.calculator.calculate_optimal_examples(strategy_code)
        expected_size = len(items)
        
        assert optimal == expected_size, f"Expected {expected_size} examples for {len(items)} items, got {optimal}"
    
    def test_boolean_strategy_uses_exactly_two_examples(self):
        """Boolean strategies should always use exactly 2 examples."""
        strategy_code = 'st.booleans()'
        optimal = self.calculator.calculate_optimal_examples(strategy_code)
        
        assert optimal == 2, f"Boolean strategy should use exactly 2 examples, got {optimal}"
    
    @given(st.integers(min_value=11, max_value=50))
    @settings(max_examples=10, deadline=None)
    def test_medium_finite_capped_appropriately(self, range_size):
        """Medium finite strategies should be capped at reasonable limits."""
        strategy_code = f'st.integers(min_value=0, max_value={range_size-1})'
        optimal = self.calculator.calculate_optimal_examples(strategy_code)
        
        # Should use the range size but capped at 20
        expected = min(range_size, 20)
        assert optimal == expected, f"Expected {expected} examples for medium range, got {optimal}"
    
    # **Feature: test-performance-optimization, Property 4: Complex strategies use appropriate ranges**
    @given(st.integers(min_value=1, max_value=4))
    @settings(max_examples=4, deadline=None)
    def test_complex_strategy_uses_complexity_based_examples(self, complexity_level):
        """Complex strategies should use examples based on complexity level.
        
        **Validates: Requirements 1.5, 2.3**
        """
        # Simulate a complex strategy analysis
        from kivy_garden.markdownlabel.strategy_classifier import StrategyAnalysis, StrategyType
        
        analysis = StrategyAnalysis(
            strategy_type=StrategyType.COMPLEX,
            input_space_size=None,
            complexity_level=complexity_level
        )
        
        optimal = self.calculator.calculate_from_analysis(analysis)
        expected = min(10 + (complexity_level * 10), 50)
        
        assert optimal == expected, f"Expected {expected} examples for complexity {complexity_level}, got {optimal}"
    
    # **Feature: test-performance-optimization, Property 5: CI environment reduces examples appropriately**
    @given(st.sampled_from([StrategyType.COMPLEX, StrategyType.COMBINATION]))
    @settings(max_examples=5, deadline=None)
    def test_ci_environment_reduces_examples_appropriately(self, strategy_type):
        """CI environment should reduce examples for complex and large combination strategies.
        
        **Validates: Requirements 2.5, 3.5**
        """
        import os
        from kivy_garden.markdownlabel.strategy_classifier import StrategyAnalysis
        
        # Create a strategy analysis that benefits from CI optimization
        if strategy_type == StrategyType.COMPLEX:
            analysis = StrategyAnalysis(
                strategy_type=StrategyType.COMPLEX,
                input_space_size=None,
                complexity_level=2
            )
        else:  # COMBINATION
            analysis = StrategyAnalysis(
                strategy_type=StrategyType.COMBINATION,
                input_space_size=30,  # Large enough to benefit from CI optimization
                complexity_level=1
            )
        
        # Calculate examples without CI
        base_examples = self.calculator.calculate_from_analysis(analysis)
        
        # Simulate CI environment
        original_ci = os.environ.get('CI')
        try:
            os.environ['CI'] = '1'
            ci_examples = self.calculator.calculate_from_analysis(analysis)
        finally:
            if original_ci is None:
                os.environ.pop('CI', None)
            else:
                os.environ['CI'] = original_ci
        
        # CI should reduce examples for these strategy types
        assert ci_examples < base_examples, f"CI should reduce examples: base={base_examples}, ci={ci_examples}"
        assert ci_examples >= 5, f"CI examples should not go below minimum: {ci_examples}"

class TestCombinationStrategies:
    """Property tests for combination strategy handling (Property 3)."""
    
    def setup_method(self):
        """Set up test fixtures."""
        from kivy_garden.markdownlabel.max_examples_calculator import MaxExamplesCalculator
        self.calculator = MaxExamplesCalculator()
    
    # **Feature: test-performance-optimization, Property 3: Combination strategies use product formula**
    @given(st.integers(min_value=2, max_value=5), st.integers(min_value=2, max_value=5))
    @settings(max_examples=10, deadline=None)
    def test_combination_uses_product_formula(self, size1, size2):
        """Combination strategies should use product of individual strategy sizes.
        
        **Validates: Requirements 1.4, 2.4**
        """
        # Create a combination strategy with two small finite strategies
        strategy_code = f'st.tuples(st.integers(min_value=0, max_value={size1-1}), st.integers(min_value=0, max_value={size2-1}))'
        
        optimal = self.calculator.calculate_optimal_examples(strategy_code)
        expected_product = size1 * size2
        expected_capped = min(expected_product, 50)  # Capped at 50
        
        assert optimal == expected_capped, f"Expected {expected_capped} examples for combination {size1}×{size2}, got {optimal}"
    
    def test_two_booleans_combination(self):
        """Two boolean strategies should use 4 examples (2×2)."""
        # This is a common pattern in the test suite
        strategy_code = 'st.tuples(st.booleans(), st.booleans())'
        
        optimal = self.calculator.calculate_optimal_examples(strategy_code)
        
        assert optimal == 4, f"Two booleans should use 4 examples (2×2), got {optimal}"
    
    def test_boolean_and_small_enum_combination(self):
        """Boolean + small enum should use product formula."""
        strategy_code = 'st.tuples(st.booleans(), st.sampled_from(["a", "b", "c"]))'
        
        optimal = self.calculator.calculate_optimal_examples(strategy_code)
        expected = 2 * 3  # boolean (2) × enum (3)
        
        assert optimal == expected, f"Boolean + 3-item enum should use 6 examples, got {optimal}"
    
    @given(st.integers(min_value=6, max_value=10))
    @settings(max_examples=5, deadline=None)
    def test_large_combination_capped_at_fifty(self, large_size):
        """Large combinations should be capped at 50 examples."""
        # Create a combination that would exceed 50
        strategy_code = f'st.tuples(st.integers(min_value=0, max_value={large_size-1}), st.integers(min_value=0, max_value={large_size-1}))'
        
        optimal = self.calculator.calculate_optimal_examples(strategy_code)
        
        # Product would be large_size², but should be capped at 50
        if large_size * large_size > 50:
            assert optimal == 50, f"Large combination should be capped at 50, got {optimal}"
        else:
            assert optimal == large_size * large_size, f"Small combination should use exact product, got {optimal}"
    
    def test_combination_with_infinite_strategy(self):
        """Combinations with infinite strategies should be treated as complex."""
        # This simulates a combination where one component is infinite
        strategy_code = 'st.tuples(st.booleans(), st.text())'
        
        optimal = self.calculator.calculate_optimal_examples(strategy_code)
        
        # Should be treated as complex since text() is infinite
        assert 10 <= optimal <= 50, f"Combination with infinite component should use 10-50 examples, got {optimal}"

class TestOverTestingDetection:
    """Property tests for over-testing detection (Property 7)."""
    
    def setup_method(self):
        """Set up test fixtures."""
        from kivy_garden.markdownlabel.test_file_analyzer import TestFileAnalyzer
        self.analyzer = TestFileAnalyzer()
    
    # **Feature: test-performance-optimization, Property 7: Over-testing detection works correctly**
    @given(st.integers(min_value=101, max_value=200))
    # Combination strategy: 20 examples (capped for performance)
    @settings(max_examples=20 if not os.getenv('CI') else 10, deadline=None)
    def test_boolean_over_testing_detected(self, excessive_examples):
        """Over-testing of boolean strategies should be correctly detected.
        
        **Validates: Requirements 4.1, 4.2, 4.3**
        """
        strategy_code = 'st.booleans()'
        
        is_over_testing = self.analyzer.calculator.is_over_testing(strategy_code, excessive_examples)
        
        assert is_over_testing, f"Should detect over-testing for boolean with {excessive_examples} examples"
        
        # Verify the optimal is indeed 2
        optimal = self.analyzer.calculator.calculate_optimal_examples(strategy_code)
        assert optimal == 2, f"Boolean optimal should be 2, got {optimal}"
    
    @given(st.integers(min_value=1, max_value=10), st.integers(min_value=50, max_value=150))
    @settings(max_examples=10, deadline=None)
    def test_small_finite_over_testing_detected(self, range_size, excessive_examples):
        """Over-testing of small finite strategies should be detected."""
        strategy_code = f'st.integers(min_value=0, max_value={range_size-1})'
        
        # Only test cases where we actually have over-testing
        optimal = self.analyzer.calculator.calculate_optimal_examples(strategy_code)
        if excessive_examples > optimal:
            is_over_testing = self.analyzer.calculator.is_over_testing(strategy_code, excessive_examples)
            assert is_over_testing, f"Should detect over-testing for range size {range_size} with {excessive_examples} examples"
    
    def test_appropriate_examples_not_flagged(self):
        """Appropriate max_examples should not be flagged as over-testing."""
        test_cases = [
            ('st.booleans()', 2),
            ('st.integers(min_value=0, max_value=4)', 5),
            ('st.sampled_from(["a", "b", "c"])', 3),
            ('st.tuples(st.booleans(), st.booleans())', 4),
        ]
        
        for strategy_code, appropriate_examples in test_cases:
            is_over_testing = self.analyzer.calculator.is_over_testing(strategy_code, appropriate_examples)
            assert not is_over_testing, f"Should not flag {strategy_code} with {appropriate_examples} examples as over-testing"
    
    def test_file_analysis_detects_over_testing(self):
        """File analysis should correctly identify over-testing patterns."""
        # Create a mock test file content with over-testing
        test_content = '''
import pytest
from hypothesis import given, strategies as st, settings

class TestExample:
    @given(st.booleans())
    @settings(max_examples=100, deadline=None)
    def test_boolean_property(self, value):
        """Test with over-testing."""
        assert isinstance(value, bool)
    
    @given(st.integers(min_value=0, max_value=2))
    @settings(max_examples=100, deadline=None)
    def test_small_range_property(self, value):
        """Test with over-testing."""
        assert 0 <= value <= 2
'''
        
        # Write to a temporary file and analyze
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(test_content)
            temp_file = f.name
        
        try:
            analysis = self.analyzer.analyze_file(temp_file)
            
            # Should detect 2 over-testing cases
            assert analysis.total_tests == 2, f"Should find 2 tests, found {analysis.total_tests}"
            assert analysis.over_tested_count == 2, f"Should find 2 over-tested, found {analysis.over_tested_count}"
            
            # Check specific recommendations
            boolean_rec = next((r for r in analysis.recommendations if 'boolean' in r.test_name), None)
            assert boolean_rec is not None, "Should have recommendation for boolean test"
            assert boolean_rec.recommended_examples == 2, f"Boolean should recommend 2 examples, got {boolean_rec.recommended_examples}"
            
            range_rec = next((r for r in analysis.recommendations if 'range' in r.test_name), None)
            assert range_rec is not None, "Should have recommendation for range test"
            assert range_rec.recommended_examples == 3, f"Range should recommend 3 examples, got {range_rec.recommended_examples}"
            
        finally:
            os.unlink(temp_file)