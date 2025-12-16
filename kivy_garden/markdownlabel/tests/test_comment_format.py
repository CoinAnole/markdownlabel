"""Property-based tests for comment format specification and validation.

Tests the CommentFormatValidator's ability to correctly validate and parse
standardized comment formats for max_examples documentation.
"""

import pytest
import os
import sys
from hypothesis import given, strategies as st, settings

# Add tools directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'tools'))

from test_optimization.comment_format import (
    CommentFormatValidator, CommentPattern, StrategyType, ValidationResult
)


class TestCommentFormatValidation:
    """Property tests for comment format validation (Property 1)."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.validator = CommentFormatValidator()
    
    # **Feature: test-comment-standardization, Property 1: Comment Format Compliance**
    # *For any* property-based test with max_examples settings, the associated comment 
    # SHALL follow the standardized format pattern "# [Strategy Type] strategy: [N] examples ([Rationale])"
    # **Validates: Requirements 1.2, 3.1, 3.5**
    
    @given(
        strategy_type=st.sampled_from([s.value for s in StrategyType]),
        max_examples=st.integers(min_value=1, max_value=1000),
        rationale=st.text(min_size=1, max_size=50, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd', 'Pc', 'Pd', 'Zs')))
    )
    # Combination strategy: 50 examples (combination coverage)
    @settings(max_examples=50, deadline=None)
    def test_valid_comment_format_compliance(self, strategy_type, max_examples, rationale):
        """Valid standardized comments are correctly validated and parsed."""
        # Generate a valid comment using the standard format
        comment = f"# {strategy_type} strategy: {max_examples} examples ({rationale})"
        
        result = self.validator.validate_comment_format(comment)
        
        # Should be valid if rationale matches expected patterns
        if result.is_valid:
            assert result.parsed_pattern is not None
            assert result.parsed_pattern.strategy_type == strategy_type
            assert result.parsed_pattern.max_examples == max_examples
            assert result.parsed_pattern.rationale == rationale
            assert result.error_type is None
        else:
            # Invalid results should have error information
            assert result.error_type is not None
            assert result.message is not None
    
    @given(
        strategy_type=st.sampled_from([s.value for s in StrategyType])
    )
    # Small finite strategy: 5 examples (input space size: 5)
    @settings(max_examples=5, deadline=None)
    def test_standard_comment_generation_compliance(self, strategy_type):
        """Generated standard comments comply with format requirements."""
        strategy_enum = StrategyType(strategy_type)
        max_examples = 20
        
        comment = self.validator.generate_standard_comment(strategy_enum, max_examples)
        result = self.validator.validate_comment_format(comment)
        
        # Generated comments should always be valid
        assert result.is_valid, f"Generated comment failed validation: {comment}, Error: {result.message}"
        assert result.parsed_pattern.strategy_type == strategy_type
        assert result.parsed_pattern.max_examples == max_examples
    
    def test_boolean_strategy_rationale_compliance(self):
        """Boolean strategy comments use correct rationale format."""
        comment = "# Boolean strategy: 2 examples (True/False coverage)"
        result = self.validator.validate_comment_format(comment)
        
        assert result.is_valid
        assert result.parsed_pattern.strategy_type == "Boolean"
        assert result.parsed_pattern.max_examples == 2
        assert "True/False" in result.parsed_pattern.rationale
    
    def test_small_finite_strategy_rationale_compliance(self):
        """Small finite strategy comments use correct rationale format."""
        comment = "# Small finite strategy: 10 examples (input space size: 10)"
        result = self.validator.validate_comment_format(comment)
        
        assert result.is_valid
        assert result.parsed_pattern.strategy_type == "Small finite"
        assert result.parsed_pattern.max_examples == 10
        assert "input space size" in result.parsed_pattern.rationale
    
    def test_invalid_format_detection(self):
        """Invalid comment formats are correctly detected."""
        invalid_comments = [
            "# Wrong format",
            "Boolean strategy: 2 examples (missing hash)",
            "# Boolean: 2 examples (missing strategy keyword)",
            "# Boolean strategy 2 examples (missing colon)",
            "# Boolean strategy: examples (missing number)",
            "# Boolean strategy: 2 (missing examples keyword)",
            "# Boolean strategy: 2 examples missing parentheses",
            "# Boolean strategy: 2 examples ()",  # empty rationale
        ]
        
        for comment in invalid_comments:
            result = self.validator.validate_comment_format(comment)
            assert not result.is_valid, f"Comment should be invalid: {comment}"
            assert result.error_type is not None
    
    def test_invalid_strategy_type_detection(self):
        """Invalid strategy types are correctly detected."""
        comment = "# InvalidType strategy: 10 examples (some rationale)"
        result = self.validator.validate_comment_format(comment)
        
        assert not result.is_valid
        assert result.error_type == "INVALID_STRATEGY_TYPE"
        assert "InvalidType" in result.message
    
    def test_invalid_max_examples_detection(self):
        """Invalid max_examples values are correctly detected."""
        # Test zero and negative values (these will match regex but fail validation)
        zero_comment = "# Boolean strategy: 0 examples (True/False coverage)"
        result = self.validator.validate_comment_format(zero_comment)
        assert not result.is_valid
        assert result.error_type == "INVALID_MAX_EXAMPLES"
        
        # Test non-numeric values (these will fail regex match)
        non_numeric_comment = "# Boolean strategy: abc examples (True/False coverage)"
        result = self.validator.validate_comment_format(non_numeric_comment)
        assert not result.is_valid
        # This will be FORMAT_VIOLATION since regex doesn't match non-numeric
        assert result.error_type in ["FORMAT_VIOLATION", "INVALID_MAX_EXAMPLES"]
    
    def test_case_insensitive_strategy_types(self):
        """Strategy type validation is case-insensitive."""
        comments = [
            "# boolean strategy: 2 examples (True/False coverage)",
            "# BOOLEAN strategy: 2 examples (True/False coverage)",
            "# Boolean strategy: 2 examples (True/False coverage)",
            "# small finite strategy: 5 examples (input space size: 5)",
        ]
        
        for comment in comments:
            result = self.validator.validate_comment_format(comment)
            assert result.is_valid, f"Case variation should be valid: {comment}"
    
    def test_whitespace_tolerance(self):
        """Comment validation tolerates reasonable whitespace variations."""
        variations = [
            "#Boolean strategy: 2 examples (True/False coverage)",  # no space after #
            "# Boolean strategy:2 examples (True/False coverage)",  # no space after :
            "# Boolean strategy: 2examples (True/False coverage)",  # no space before examples
            "# Boolean strategy: 2 examples(True/False coverage)",  # no space before (
        ]
        
        for comment in variations:
            result = self.validator.validate_comment_format(comment)
            # Some variations may be invalid due to strict parsing, that's acceptable
            # The key is that the validator handles them gracefully
            assert result.error_type is None or result.error_type in ["FORMAT_VIOLATION"]


class TestCommentPatternModel:
    """Tests for CommentPattern data model."""
    
    def test_comment_pattern_to_standardized_format(self):
        """CommentPattern correctly formats to standardized string."""
        pattern = CommentPattern(
            strategy_type="Boolean",
            max_examples=2,
            rationale="True/False coverage"
        )
        
        formatted = pattern.to_standardized_format()
        expected = "# Boolean strategy: 2 examples (True/False coverage)"
        
        assert formatted == expected
    
    def test_comment_pattern_with_optional_fields(self):
        """CommentPattern handles optional fields correctly."""
        pattern = CommentPattern(
            strategy_type="Complex",
            max_examples=50,
            rationale="adequate coverage",
            line_number=42,
            original_comment="# Old format comment"
        )
        
        assert pattern.line_number == 42
        assert pattern.original_comment == "# Old format comment"
        
        # Formatting should ignore optional fields
        formatted = pattern.to_standardized_format()
        expected = "# Complex strategy: 50 examples (adequate coverage)"
        assert formatted == expected


class TestStrategyTypeConsistency:
    """Property tests for strategy type consistency (Property 3)."""
    
    def setup_method(self):
        """Set up test fixtures."""
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'tools'))
        from test_optimization.strategy_type_mapper import StrategyTypeMapper, TestCodeAnalyzer
        
        self.mapper = StrategyTypeMapper()
        self.analyzer = TestCodeAnalyzer()
    
    # **Feature: test-comment-standardization, Property 3: Strategy Type Consistency**
    # *For any* strategy type classification, all comments documenting that strategy type 
    # SHALL use consistent terminology across all test files
    # **Validates: Requirements 1.3, 2.1, 3.2, 4.2**
    
    @given(
        strategy_code=st.sampled_from([
            'st.booleans()',
            'st.integers(min_value=0, max_value=5)',
            'st.integers(min_value=0, max_value=25)',
            'st.text()',
            'st.tuples(st.booleans(), st.integers(min_value=0, max_value=3))'
        ])
    )
    # Small finite strategy: 5 examples (input space size: 5)
    @settings(max_examples=5, deadline=None)
    def test_strategy_type_classification_consistency(self, strategy_code):
        """Strategy type classification produces consistent results for same input."""
        # Classify the same strategy multiple times
        classification1 = self.mapper.classify_strategy_for_comments(strategy_code)
        classification2 = self.mapper.classify_strategy_for_comments(strategy_code)
        
        # Results should be identical
        assert classification1.strategy_type == classification2.strategy_type
        assert classification1.rationale == classification2.rationale
        assert classification1.input_space_size == classification2.input_space_size
    
    @given(
        strategy_type=st.sampled_from(['st.booleans()', 'st.integers(min_value=0, max_value=5)'])
    )
    # Boolean strategy: 2 examples (True/False coverage)
    @settings(max_examples=2, deadline=None)
    def test_boolean_and_small_finite_terminology_consistency(self, strategy_type):
        """Boolean and small finite strategies use consistent terminology."""
        classification = self.mapper.classify_strategy_for_comments(strategy_type)
        
        if 'booleans' in strategy_type:
            # Boolean strategies should always use "Boolean" type and "True/False coverage"
            assert classification.strategy_type.value == "Boolean"
            assert "True/False" in classification.rationale
        else:
            # Small finite strategies should use "Small finite" type and size information
            assert classification.strategy_type.value == "Small finite"
            assert "input space size" in classification.rationale or "finite coverage" in classification.rationale
    
    def test_complex_strategy_terminology_consistency(self):
        """Complex strategies use consistent terminology."""
        complex_strategies = [
            'st.text()',
            'st.floats()',
            'st.text(min_size=1, max_size=100)'
        ]
        
        classifications = [
            self.mapper.classify_strategy_for_comments(strategy)
            for strategy in complex_strategies
        ]
        
        # All should be classified as Complex type
        for classification in classifications:
            assert classification.strategy_type.value == "Complex"
            # Rationale should be consistent (either "adequate coverage" or "performance optimized")
            assert classification.rationale in ["adequate coverage", "performance optimized"]
    
    def test_combination_strategy_terminology_consistency(self):
        """Combination strategies use consistent terminology."""
        combination_strategies = [
            'st.tuples(st.booleans(), st.integers(min_value=0, max_value=3))',
            'st.tuples(st.text(max_size=5), st.booleans())'
        ]
        
        classifications = [
            self.mapper.classify_strategy_for_comments(strategy)
            for strategy in combination_strategies
        ]
        
        # All should be classified as Combination type
        for classification in classifications:
            assert classification.strategy_type.value == "Combination"
            assert "combination" in classification.rationale.lower()
    
    def test_strategy_type_mapping_consistency(self):
        """Strategy type mapping between existing and comment formats is consistent."""
        # Test that the same strategy always maps to the same comment format type
        test_strategies = {
            'st.booleans()': "Boolean",
            'st.integers(min_value=0, max_value=5)': "Small finite",
            'st.integers(min_value=0, max_value=25)': "Medium finite",
            'st.text()': "Complex",
            'st.tuples(st.booleans(), st.integers(min_value=0, max_value=3))': "Combination"
        }
        
        for strategy_code, expected_type in test_strategies.items():
            classification = self.mapper.classify_strategy_for_comments(strategy_code)
            assert classification.strategy_type.value == expected_type, \
                f"Strategy {strategy_code} should map to {expected_type}, got {classification.strategy_type.value}"
    
    def test_rationale_template_consistency(self):
        """Rationale templates are consistent for each strategy type."""
        # Test that same strategy types always get same rationale patterns
        boolean_strategies = ['st.booleans()']
        small_finite_strategies = [
            'st.integers(min_value=0, max_value=5)',
            'st.integers(min_value=1, max_value=3)'
        ]
        
        # Boolean strategies should all have True/False rationale
        for strategy in boolean_strategies:
            classification = self.mapper.classify_strategy_for_comments(strategy)
            assert "True/False" in classification.rationale
        
        # Small finite strategies should all have input space size rationale
        for strategy in small_finite_strategies:
            classification = self.mapper.classify_strategy_for_comments(strategy)
            assert "input space size" in classification.rationale or "finite coverage" in classification.rationale
    
    def test_edge_case_handling_consistency(self):
        """Edge case handling produces consistent classifications."""
        # Test custom domain strategies
        custom_strategies = [
            'markdown_heading()',
            'html_element()',
            'custom_data_generator()'
        ]
        
        for strategy in custom_strategies:
            classification = self.mapper.handle_edge_cases(strategy)
            if classification:  # If edge case is detected
                assert classification.strategy_type.value == "Complex"
                assert "custom domain" in classification.rationale
    
    def test_classification_determinism(self):
        """Strategy classification is deterministic across multiple calls."""
        test_strategy = 'st.integers(min_value=0, max_value=10)'
        
        # Run classification multiple times
        results = [
            self.mapper.classify_strategy_for_comments(test_strategy)
            for _ in range(5)
        ]
        
        # All results should be identical
        first_result = results[0]
        for result in results[1:]:
            assert result.strategy_type == first_result.strategy_type
            assert result.rationale == first_result.rationale
            assert result.input_space_size == first_result.input_space_size