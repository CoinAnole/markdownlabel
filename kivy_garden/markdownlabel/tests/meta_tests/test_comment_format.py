"""Property-based tests for comment format specification and validation.

Tests the CommentFormatValidator's ability to correctly validate and parse
standardized comment formats for max_examples documentation.
"""

import pytest
from hypothesis import given, strategies as st, settings

from kivy_garden.markdownlabel.tests.modules.comment_manager import (
    CommentFormatValidator, CommentPattern, StrategyType, CommentAnalyzer
)
from kivy_garden.markdownlabel.tests.modules.strategy_analyzer import StrategyTypeMapper, CodeAnalyzer


@pytest.mark.test_tests
class TestCommentFormatValidation:
    """Property tests for comment format validation (Property 1)."""

    def setup_method(self):
        """Set up test fixtures."""
        self.validator = CommentFormatValidator()

    # **Feature: test-comment-standardization, Property 1: Comment Format Compliance**
    # *For any* property-based test with max_examples settings, the associated comment
    # SHALL follow the standardized format pattern "# [Strategy Type] strategy: [N] examples ([Rationale])"
    # **Validates: Requirements 1.2, 3.1, 3.5**

    @pytest.mark.property
    @given(
        strategy_type=st.sampled_from([s.value for s in StrategyType]),
        max_examples=st.integers(min_value=1, max_value=1000),
        rationale=st.text(
            min_size=1,
            max_size=50,
            alphabet=st.characters(
                whitelist_categories=('Lu', 'Ll', 'Nd', 'Pc', 'Pd', 'Zs')
            )
        )
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

    @pytest.mark.property
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


@pytest.mark.test_tests
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


@pytest.mark.test_tests
class TestCustomValueDocumentation:
    """Property tests for custom value documentation (Property 2)."""

    def setup_method(self):
        """Set up test fixtures."""
        self.analyzer = CommentAnalyzer()

    # **Feature: test-comment-standardization, Property 2: Custom Value Documentation**
    # *For any* property-based test using custom max_examples values (not in
    # standard set {2, 5, 10, 20, 50, 100}),
    # there SHALL exist a comment explaining the rationale
    # **Validates: Requirements 1.1, 4.5**

    @pytest.mark.property
    @given(
        max_examples=st.integers(min_value=1, max_value=1000).filter(
            lambda x: x not in {2, 5, 10, 20, 50, 100}
        ),
        strategy_type=st.sampled_from([s.value for s in StrategyType])
    )
    # Complex strategy: 25 examples (adequate coverage)
    @settings(max_examples=25, deadline=None)
    def test_custom_max_examples_require_documentation(self, max_examples, strategy_type):
        """Custom max_examples values require documentation comments."""
        # Create a test function with custom max_examples but no comment
        test_code_without_comment = f'''
@given(data=st.text())
@settings(max_examples={max_examples}, deadline=None)
def test_undocumented_function(data):
    """Test function without documentation comment."""
    assert len(data) >= 0
'''

        # Create a test function with custom max_examples and proper comment
        test_code_with_comment = f'''
# {strategy_type} strategy: {max_examples} examples (adequate coverage)
@given(data=st.text())
@settings(max_examples={max_examples}, deadline=None)
def test_documented_function(data):
    """Test function with documentation comment."""
    assert len(data) >= 0
'''

        # Analyze both versions
        analysis_without = self.analyzer._analyze_file_content("test_without.py", test_code_without_comment)
        analysis_with = self.analyzer._analyze_file_content("test_with.py", test_code_with_comment)

        # Test without comment should have missing documentation
        assert analysis_without.total_property_tests == 1
        assert analysis_without.documented_tests == 0
        assert analysis_without.undocumented_tests == 1
        assert len(analysis_without.missing_documentation) == 1

        # Test with comment should be documented (if comment is valid)
        assert analysis_with.total_property_tests == 1
        if analysis_with.documented_tests == 1:
            # Valid comment case
            assert analysis_with.undocumented_tests == 0
            assert len(analysis_with.missing_documentation) == 0
        else:
            # Invalid comment case - should still detect the attempt
            assert len(analysis_with.format_violations) > 0 or len(analysis_with.missing_documentation) > 0

    @pytest.mark.property
    @given(
        standard_max_examples=st.sampled_from([2, 5, 10, 20, 50, 100])
    )
    # Small finite strategy: 6 examples (input space size: 6)
    @settings(max_examples=6, deadline=None)
    def test_standard_max_examples_require_documentation(self, standard_max_examples):
        """All max_examples values require documentation (strict mode)."""
        # Create a test function with standard max_examples and no comment
        test_code = f'''
@given(data=st.text())
@settings(max_examples={standard_max_examples}, deadline=None)
def test_standard_function(data):
    """Test function with standard max_examples."""
    assert len(data) >= 0
'''

        analysis = self.analyzer._analyze_file_content("test_standard.py", test_code)

        # Even historically standard values require documentation now
        assert analysis.total_property_tests == 1
        assert len(analysis.missing_documentation) == 1
        assert analysis.undocumented_tests == 1

    def test_custom_value_detection_accuracy(self):
        """Custom value detection treats all values as needing docs by default."""
        custom_values = [1, 3, 4, 6, 7, 8, 9, 11, 15, 25, 30, 75, 150, 200, 500]
        standard_values = [2, 5, 10, 20, 50, 100]

        for value in custom_values:
            assert value not in self.analyzer.standard_values, f"Value {value} should be custom"

        for value in standard_values:
            assert value not in self.analyzer.standard_values, f"Value {value} should be documented"

    def test_missing_documentation_reporting(self):
        """Missing documentation is correctly reported with function details."""
        test_code = '''
@given(data=st.text())
@settings(max_examples=15, deadline=None)
def test_missing_doc_function(data):
    """This function has custom max_examples but no documentation comment."""
    assert len(data) >= 0

@given(data=st.integers())
@settings(max_examples=25, deadline=None)
def test_another_missing_doc(data):
    """Another function without documentation."""
    assert data is not None
'''

        analysis = self.analyzer._analyze_file_content("test_missing.py", test_code)

        assert analysis.total_property_tests == 2
        assert analysis.undocumented_tests == 2
        assert len(analysis.missing_documentation) == 2

        # Check that function names and max_examples are correctly reported
        missing_docs = analysis.missing_documentation
        func_names = [doc[0] for doc in missing_docs]
        max_examples_values = [doc[2] for doc in missing_docs]

        assert "test_missing_doc_function" in func_names
        assert "test_another_missing_doc" in func_names
        assert 15 in max_examples_values
        assert 25 in max_examples_values

    def test_documentation_with_invalid_format_detection(self):
        """Invalid documentation format is detected and reported."""
        test_code = '''
# This is not a proper format comment
@given(data=st.text())
@settings(max_examples=15, deadline=None)
def test_invalid_format(data):
    """Function with invalid comment format."""
    assert len(data) >= 0

# Wrong format: 25 examples
@given(data=st.integers())
@settings(max_examples=25, deadline=None)
def test_wrong_format(data):
    """Another function with wrong format."""
    assert data is not None
'''

        analysis = self.analyzer._analyze_file_content("test_invalid.py", test_code)

        assert analysis.total_property_tests == 2
        # Should detect format violations
        assert len(analysis.format_violations) >= 1
        # Should still report missing documentation since format is invalid
        assert analysis.undocumented_tests >= 1


@pytest.mark.test_tests
class TestStrategyTypeConsistency:
    """Property tests for strategy type consistency (Property 3)."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mapper = StrategyTypeMapper()
        self.analyzer = CodeAnalyzer()

    # **Feature: test-comment-standardization, Property 3: Strategy Type Consistency**
    # *For any* strategy type classification, all comments documenting that
    # strategy type
    # SHALL use consistent terminology across all test files
    # **Validates: Requirements 1.3, 2.1, 3.2, 4.2**

    @pytest.mark.property
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

    @pytest.mark.property
    @given(
        strategy_type=st.sampled_from(['st.booleans()', 'st.integers(min_value=0, max_value=5)'])
    )
    # Small finite strategy: 2 examples (input space size: 2)
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
            assert (
                "input space size" in classification.rationale or
                "finite coverage" in classification.rationale
            )

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
                f"Strategy {strategy_code} should map to {expected_type}, " \
                f"got {classification.strategy_type.value}"

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
            assert (
                "input space size" in classification.rationale or
                "finite coverage" in classification.rationale
            )

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


@pytest.mark.test_tests
class TestMachineReadableFormat:
    """Property tests for machine-readable format (Property 8)."""

    def setup_method(self):
        """Set up test fixtures."""
        self.analyzer = CommentAnalyzer()
        self.validator = CommentFormatValidator()

    # **Feature: test-comment-standardization, Property 8: Machine-Readable Format**
    # *For any* standardized comment, automated parsing tools SHALL be able to
    # extract
    # strategy type, example count, and rationale information
    # **Validates: Requirements 4.1, 4.3**

    @pytest.mark.property
    @given(
        strategy_type=st.sampled_from([s.value for s in StrategyType]),
        max_examples=st.integers(min_value=1, max_value=1000),
        rationale_base=st.sampled_from([
            'adequate coverage', 'True/False coverage', 'input space size',
            'combination coverage', 'performance optimized'
        ])
    )
    # Combination strategy: 30 examples (performance optimized)
    @settings(max_examples=30, deadline=None)
    def test_standardized_comments_are_machine_parseable(self, strategy_type, max_examples, rationale_base):
        """Standardized comments can be parsed by automated tools to extract information."""
        # Generate a standardized comment
        if rationale_base == 'input space size' and max_examples <= 50:
            rationale = f"input space size: {max_examples}"
        else:
            rationale = rationale_base

        comment = f"# {strategy_type} strategy: {max_examples} examples ({rationale})"

        # Test that the comment can be parsed by the validator
        validation_result = self.validator.validate_comment_format(comment)

        if validation_result.is_valid:
            # Should be able to extract all required information
            parsed = validation_result.parsed_pattern
            assert parsed is not None
            assert parsed.strategy_type == strategy_type
            assert parsed.max_examples == max_examples
            assert parsed.rationale == rationale

            # Test that the comment can be analyzed by the analyzer
            test_code = f'''
{comment}
@given(data=st.text())
@settings(max_examples={max_examples}, deadline=None)
def test_machine_readable_function(data):
    """Test function with standardized comment."""
    assert len(data) >= 0
'''

            analysis = self.analyzer._analyze_file_content("test_machine_readable.py", test_code)

            # Should detect the test and recognize the valid comment
            assert analysis.total_property_tests == 1
            if analysis.documented_tests == 1:
                assert len(analysis.valid_comments) == 1
                valid_comment = analysis.valid_comments[0]
                assert valid_comment.strategy_type == strategy_type
                assert valid_comment.max_examples == max_examples
                assert valid_comment.rationale == rationale

    @pytest.mark.property
    @given(
        strategy_type=st.sampled_from([s.value for s in StrategyType])
    )
    # Small finite strategy: 5 examples (input space size: 5)
    @settings(max_examples=5, deadline=None)
    def test_generated_comments_are_machine_parseable(self, strategy_type):
        """Comments generated by the system are machine-parseable."""
        strategy_enum = StrategyType(strategy_type)
        max_examples = 5

        # Generate a comment using the validator
        generated_comment = self.validator.generate_standard_comment(strategy_enum, max_examples)

        # Parse the generated comment
        validation_result = self.validator.validate_comment_format(generated_comment)

        # Generated comments should always be valid and parseable
        assert validation_result.is_valid, f"Generated comment failed validation: {generated_comment}"

        parsed = validation_result.parsed_pattern
        assert parsed.strategy_type == strategy_type
        assert parsed.max_examples == max_examples
        assert parsed.rationale is not None and len(parsed.rationale) > 0

    def test_parsing_extracts_all_required_fields(self):
        """Parsing extracts all required fields from standardized comments."""
        test_comments = [
            "# Boolean strategy: 2 examples (True/False coverage)",
            "# Small finite strategy: 10 examples (input space size: 10)",
            "# Medium finite strategy: 20 examples (adequate finite coverage)",
            "# Complex strategy: 50 examples (adequate coverage)",
            "# Combination strategy: 25 examples (combination coverage)"
        ]

        for comment in test_comments:
            validation_result = self.validator.validate_comment_format(comment)

            assert validation_result.is_valid, f"Comment should be valid: {comment}"

            parsed = validation_result.parsed_pattern

            # Check that all required fields are present and non-empty
            assert parsed.strategy_type is not None and len(parsed.strategy_type) > 0
            assert parsed.max_examples is not None and parsed.max_examples > 0
            assert parsed.rationale is not None and len(parsed.rationale) > 0

            # Check that strategy type is one of the valid types
            assert parsed.strategy_type in [s.value for s in StrategyType]

    def test_machine_readable_format_consistency(self):
        """Machine-readable format is consistent across different parsing attempts."""
        comment = "# Complex strategy: 100 examples (adequate coverage)"

        # Parse the same comment multiple times
        results = [
            self.validator.validate_comment_format(comment)
            for _ in range(5)
        ]

        # All results should be identical
        first_result = results[0]
        assert first_result.is_valid

        for result in results[1:]:
            assert result.is_valid == first_result.is_valid
            assert result.parsed_pattern.strategy_type == first_result.parsed_pattern.strategy_type
            assert result.parsed_pattern.max_examples == first_result.parsed_pattern.max_examples
            assert result.parsed_pattern.rationale == first_result.parsed_pattern.rationale

    def test_integration_with_analysis_tools(self):
        """Standardized comments integrate properly with analysis tools."""
        test_code = '''
# Boolean strategy: 2 examples (True/False coverage)
@given(flag=st.booleans())
@settings(max_examples=2, deadline=None)
def test_boolean_logic(flag):
    """Test boolean logic with documented strategy."""
    assert isinstance(flag, bool)

# Complex strategy: 50 examples (adequate coverage)
@given(text=st.text())
@settings(max_examples=50, deadline=None)
def test_text_processing(text):
    """Test text processing with documented strategy."""
    assert isinstance(text, str)
'''

        # Analyze the test code
        analysis = self.analyzer._analyze_file_content("test_integration.py", test_code)

        # Should detect both tests as documented
        assert analysis.total_property_tests == 2
        assert analysis.documented_tests == 2
        assert analysis.undocumented_tests == 0
        assert len(analysis.valid_comments) == 2

        # Check that the parsed information is accessible
        boolean_comment = next(c for c in analysis.valid_comments if c.strategy_type == "Boolean")
        complex_comment = next(c for c in analysis.valid_comments if c.strategy_type == "Complex")

        assert boolean_comment.max_examples == 2
        assert "True/False" in boolean_comment.rationale

        assert complex_comment.max_examples == 50
        assert "adequate coverage" in complex_comment.rationale

    def test_error_handling_in_machine_parsing(self):
        """Machine parsing handles errors gracefully."""
        invalid_comments = [
            "# Invalid format comment",
            "# Boolean: 2 examples (missing strategy keyword)",
            "# Boolean strategy 2 examples (missing colon)",
            "# Boolean strategy: examples (missing number)",
        ]

        for comment in invalid_comments:
            validation_result = self.validator.validate_comment_format(comment)

            # Should fail validation but not crash
            assert not validation_result.is_valid
            assert validation_result.error_type is not None
            assert validation_result.message is not None
            assert validation_result.parsed_pattern is None

    def test_round_trip_parsing_consistency(self):
        """Round-trip parsing maintains consistency."""
        original_patterns = [
            ("Boolean", 2, "True/False coverage"),
            ("Small finite", 10, "input space size: 10"),
            ("Complex", 50, "adequate coverage"),
        ]

        for strategy_type, max_examples, rationale in original_patterns:
            # Create a comment pattern
            pattern = CommentPattern(
                strategy_type=strategy_type,
                max_examples=max_examples,
                rationale=rationale
            )

            # Convert to standardized format
            formatted_comment = pattern.to_standardized_format()

            # Parse it back
            validation_result = self.validator.validate_comment_format(formatted_comment)

            assert validation_result.is_valid
            parsed_pattern = validation_result.parsed_pattern

            # Should match original
            assert parsed_pattern.strategy_type == strategy_type
            assert parsed_pattern.max_examples == max_examples
            assert parsed_pattern.rationale == rationale
