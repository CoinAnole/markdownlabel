"""Property-based tests for comment standardization functionality.

Tests the CommentStandardizer's ability to generate and apply standardized
comments for property-based tests with proper strategy documentation.
"""

import pytest
import os
import tempfile
from hypothesis import given, strategies as st, settings

from kivy_garden.markdownlabel.tests.modules.comment_manager import (
    CommentStandardizer, StrategyType, CommentFormatValidator, CommentAnalyzer
)
from kivy_garden.markdownlabel.tests.modules.optimization_detector import (
    OptimizationDetector as PerformanceRationaleDetector,
    OptimizationCommentGenerator as PerformanceCommentGenerator,
    OptimizationType as PerformanceReason
)


@pytest.mark.test_tests
class TestBooleanStrategyDocumentation:
    """Property tests for boolean strategy documentation."""

    def setup_method(self):
        """Set up test fixtures."""
        self.standardizer = CommentStandardizer()
        self.validator = CommentFormatValidator()

    # *For any* property-based test using boolean strategies, the comment SHALL reference
    # True/False coverage in the rationale

    @pytest.mark.property
    @given(
        max_examples=st.integers(min_value=1, max_value=100).filter(
            lambda x: x not in {2, 5, 10, 20, 50, 100}
        ),
        function_name=st.text(min_size=5, max_size=30, alphabet=st.characters(
            whitelist_categories=('Lu', 'Ll', 'Nd', 'Pc')
        )).map(lambda x: f"test_{x}")
    )
    # Complex strategy: 2 examples (low max=2 acceptable for meta-test)
    @settings(max_examples=2, deadline=None)
    def test_boolean_strategy_comments_reference_true_false_coverage(
        self, max_examples, function_name
    ):
        """Boolean strategy comments always reference True/False coverage."""
        # Create test code with boolean strategy but no comment
        test_code = f'''
@given(flag=st.booleans())
@settings(max_examples={max_examples}, deadline=None)
def {function_name}(flag):
    """Test function using boolean strategy."""
    assert isinstance(flag, bool)
'''

        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(test_code)
            temp_file = f.name

        try:
            # Standardize the file
            result = self.standardizer.standardize_file(temp_file, dry_run=True)

            # Should succeed and generate a comment
            assert result.success
            assert result.changes_made > 0
            assert len(result.generated_comments) > 0

            # Find the boolean strategy comment
            boolean_comment = None
            for comment in result.generated_comments:
                if comment.strategy_type == "Boolean":
                    boolean_comment = comment
                    break

            # Should have generated a boolean strategy comment
            assert boolean_comment is not None, "Should generate a Boolean strategy comment"

            # Comment should reference True/False coverage
            assert "True/False" in boolean_comment.rationale, (
                f"Boolean strategy rationale should reference True/False coverage, "
                f"got: {boolean_comment.rationale}"
            )

            # Verify the generated comment is valid
            formatted_comment = boolean_comment.to_standardized_format()
            validation_result = self.validator.validate_comment_format(formatted_comment)
            assert validation_result.is_valid, f"Generated comment should be valid: {formatted_comment}"

        finally:
            # Clean up
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_boolean_strategy_comment_generation_consistency(self):
        """Boolean strategy comment generation is consistent."""
        # Test multiple max_examples values
        test_values = [1, 2, 5, 10, 25]

        for max_examples in test_values:
            comment = self.standardizer.generate_comment("Boolean", max_examples)

            # Should always contain True/False reference
            assert "True/False" in comment, f"Boolean comment should reference True/False: {comment}"

            # Should be valid format
            validation_result = self.validator.validate_comment_format(comment)
            assert validation_result.is_valid, f"Generated comment should be valid: {comment}"

            # Should have correct max_examples
            assert str(max_examples) in comment, (
                f"Comment should contain max_examples {max_examples}: {comment}"
            )

    def test_boolean_strategy_detection_accuracy(self):
        """Boolean strategy detection correctly identifies st.booleans() usage."""
        boolean_test_codes = [
            '''
@given(flag=st.booleans())
@settings(max_examples=3, deadline=None)
def test_simple_boolean(flag):
    assert isinstance(flag, bool)
''',
            '''
@given(enabled=st.booleans(), disabled=st.booleans())
@settings(max_examples=4, deadline=None)
def test_multiple_booleans(enabled, disabled):
    assert isinstance(enabled, bool)
    assert isinstance(disabled, bool)
''',
            '''
@given(data=st.tuples(st.booleans(), st.integers(min_value=0, max_value=2)))
@settings(max_examples=6, deadline=None)
def test_boolean_in_tuple(data):
    flag, num = data
    assert isinstance(flag, bool)
'''
        ]

        for i, test_code in enumerate(boolean_test_codes):
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(test_code)
                temp_file = f.name

            try:
                result = self.standardizer.standardize_file(temp_file, dry_run=True)

                # Should detect and generate appropriate comments
                assert result.success, f"Standardization should succeed for test {i}"
                assert result.changes_made > 0, f"Should generate comments for test {i}"

                # Should generate comments that reference boolean strategies appropriately
                has_boolean_reference = False
                for comment in result.generated_comments:
                    if "Boolean" in comment.strategy_type or "True/False" in comment.rationale:
                        has_boolean_reference = True
                        break

                # For tests with boolean strategies, should have boolean or
                # combination references
                # (tuples with booleans might be classified as combinations)
                if 'st.booleans()' in test_code:
                    # Allow either Boolean strategy or combination strategy
                    # for tuple cases
                    has_strategy_reference = any(
                        "Boolean" in comment.strategy_type or
                        "Combination" in comment.strategy_type or
                        "True/False" in comment.rationale or
                        "combination" in comment.rationale.lower()
                        for comment in result.generated_comments
                    )
                    assert has_strategy_reference, (
                        f"Should detect boolean or combination strategy in test {i}"
                    )

            finally:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)

    def test_boolean_strategy_rationale_templates(self):
        """Boolean strategy rationale templates are consistent and correct."""
        # Test different ways to generate boolean strategy comments
        strategy_enum = StrategyType.BOOLEAN

        # Test with validator's generate_standard_comment
        validator_comment = self.validator.generate_standard_comment(strategy_enum, 2)
        assert "True/False" in validator_comment
        assert "Boolean strategy" in validator_comment

        # Test with standardizer's generate_comment
        standardizer_comment = self.standardizer.generate_comment("Boolean", 2)
        assert "True/False" in standardizer_comment
        assert "Boolean strategy" in standardizer_comment

        # Both should produce valid comments
        validator_result = self.validator.validate_comment_format(validator_comment)
        standardizer_result = self.validator.validate_comment_format(standardizer_comment)

        assert validator_result.is_valid
        assert standardizer_result.is_valid

        # Both should have the same essential content
        assert validator_result.parsed_pattern.strategy_type == "Boolean"
        assert standardizer_result.parsed_pattern.strategy_type == "Boolean"
        assert "True/False" in validator_result.parsed_pattern.rationale
        assert "True/False" in standardizer_result.parsed_pattern.rationale

    def test_boolean_strategy_edge_cases(self):
        """Boolean strategy documentation handles edge cases correctly."""
        edge_case_codes = [
            # Boolean with custom settings
            '''
@given(flag=st.booleans())
@settings(max_examples=1, deadline=None, suppress_health_check=[HealthCheck.too_slow])
def test_boolean_edge_case_1(flag):
    assert flag in [True, False]
''',
            # Boolean in complex combination
            '''
@given(data=st.one_of(st.booleans(), st.just(None)))
@settings(max_examples=7, deadline=None)
def test_boolean_edge_case_2(data):
    assert data is None or isinstance(data, bool)
''',
        ]

        for i, test_code in enumerate(edge_case_codes):
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(test_code)
                temp_file = f.name

            try:
                result = self.standardizer.standardize_file(temp_file, dry_run=True)

                # Should handle edge cases gracefully
                assert result.success, f"Should handle edge case {i} gracefully"

                # If comments are generated, they should be valid
                for comment in result.generated_comments:
                    formatted = comment.to_standardized_format()
                    validation_result = self.validator.validate_comment_format(formatted)
                    assert validation_result.is_valid, f"Edge case comment should be valid: {formatted}"

            finally:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)

    def test_boolean_strategy_integration_with_analysis(self):
        """Boolean strategy documentation integrates properly with analysis tools."""
        test_code = '''
@given(flag=st.booleans())
@settings(max_examples=3, deadline=None)
def test_boolean_integration(flag):
    """Test boolean integration."""
    assert isinstance(flag, bool)
'''

        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(test_code)
            temp_file = f.name

        try:
            # First analyze without standardization
            from kivy_garden.markdownlabel.tests.modules.comment_manager import CommentAnalyzer
            analyzer = CommentAnalyzer()

            initial_analysis = analyzer.analyze_file(temp_file)
            assert initial_analysis.undocumented_tests > 0  # Should have undocumented test

            # Apply standardization
            result = self.standardizer.standardize_file(temp_file, dry_run=False)
            assert result.success
            assert result.changes_made > 0

            # Analyze after standardization
            final_analysis = analyzer.analyze_file(temp_file)

            # Should now be documented
            assert final_analysis.documented_tests > initial_analysis.documented_tests
            assert final_analysis.undocumented_tests < initial_analysis.undocumented_tests

            # Should have valid boolean strategy comment
            boolean_comments = [c for c in final_analysis.valid_comments if c.strategy_type == "Boolean"]
            assert len(boolean_comments) > 0

            for comment in boolean_comments:
                assert "True/False" in comment.rationale

        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)


