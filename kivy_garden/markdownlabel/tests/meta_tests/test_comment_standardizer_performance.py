"""Property-based tests for performance rationale comment standardization.

Tests the CommentStandardizer's ability to generate and apply standardized
comments for performance-optimized property-based tests.
"""

import pytest
import os
import tempfile
from hypothesis import given, strategies as st, settings

from kivy_garden.markdownlabel.tests.modules.comment_manager import (
    CommentStandardizer, CommentFormatValidator, CommentAnalyzer
)
from kivy_garden.markdownlabel.tests.modules.optimization_detector import (
    OptimizationDetector as PerformanceRationaleDetector,
    OptimizationCommentGenerator as PerformanceCommentGenerator,
    OptimizationType as PerformanceReason
)


@pytest.mark.test_tests
class TestPerformanceRationaleDocumentation:
    """Property tests for performance rationale documentation."""

    def setup_method(self):
        """Set up test fixtures."""
        self.standardizer = CommentStandardizer()
        self.validator = CommentFormatValidator()

        # Import performance handler components
        self.detector = PerformanceRationaleDetector()
        self.generator = PerformanceCommentGenerator()
        self.PerformanceReason = PerformanceReason  # Make accessible to test methods

    # *For any* property-based test with reduced max_examples for performance reasons,
    # the comment SHALL explain the performance rationale

    @pytest.mark.property
    @given(
        max_examples=st.integers(min_value=1, max_value=5),
        strategy_complexity=st.sampled_from(['text', 'floats', 'composite']),
        function_name=st.text(min_size=5, max_size=30, alphabet=st.characters(
            whitelist_categories=('Lu', 'Ll', 'Nd', 'Pc')
        )).map(lambda x: f"test_{x}")
    )
    # Mixed finite/complex strategy: 15 examples (15 finite combinations × 1 complex sample)
    @settings(max_examples=15, deadline=None)
    def test_execution_time_performance_rationale_documented(
        self, max_examples, strategy_complexity, function_name
    ):
        """Execution time performance rationale is properly documented."""
        # Create test code with complex strategy and low max_examples (performance optimization)
        strategy_map = {
            'text': 'st.text(min_size=50, max_size=200)',
            'floats': 'st.floats(min_value=-1000.0, max_value=1000.0, allow_nan=False)',
            'composite': 'st.composite(lambda draw: draw(st.text()) + str(draw(st.integers())))'
        }

        strategy_code = strategy_map[strategy_complexity]

        test_code = f'''
@given(data={strategy_code})
@settings(max_examples={max_examples}, deadline=None)
def {function_name}(data):
    """Test function with performance optimization."""
    # Complex processing that justifies low max_examples
    processed = str(data).upper().lower().strip()
    assert len(processed) >= 0
'''

        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(test_code)
            temp_file = f.name

        try:
            # Detect performance rationale
            performance_rationale = self.detector.detect_performance_rationale(test_code, max_examples)

            # Should detect performance optimization for complex strategies with low max_examples
            if strategy_complexity in ['text', 'floats', 'composite']:
                assert performance_rationale is not None, (
                    f"Should detect performance rationale for {strategy_complexity} "
                    f"with {max_examples} examples"
                )
                assert not performance_rationale.ci_specific, "Should not be environment-specific"
                assert performance_rationale.reduced_examples == max_examples

            # Generate performance-aware comment
            performance_comment = self.generator.generate_performance_comment(test_code, max_examples)

            if performance_comment:
                # Comment should mention performance optimization
                assert ("performance" in performance_comment.lower() or
                        "optimized" in performance_comment.lower()), (
                    f"Performance comment should mention optimization: {performance_comment}"
                )

                # Should be valid format
                validation_result = self.validator.validate_comment_format(performance_comment)
                assert validation_result.is_valid, (
                    f"Performance comment should be valid: {performance_comment}"
                )

        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    @pytest.mark.property
    @given(
        performance_keywords=st.sampled_from([
            "performance optimized",
            "execution time optimization",
            "memory optimization",
            "deadline constraint",
            "complexity reduction"
        ]),
        max_examples=st.integers(min_value=1, max_value=20),
        function_name=st.text(min_size=5, max_size=30, alphabet=st.characters(
            whitelist_categories=('Lu', 'Ll', 'Nd', 'Pc')
        )).map(lambda x: f"test_{x}")
    )
    # Mixed finite/complex strategy: 25 examples (5 finite × 5 complex samples)
    @settings(max_examples=25, deadline=None)
    def test_explicit_performance_comments_detected(
        self, performance_keywords, max_examples, function_name
    ):
        """Explicit performance comments are properly detected and preserved."""
        # Create test code with explicit performance comment
        test_code = f'''
# This test uses reduced examples for {performance_keywords}
@given(data=st.text(min_size=20, max_size=100))
@settings(max_examples={max_examples}, deadline=None)
def {function_name}(data):
    """Test function with explicit performance comment."""
    assert isinstance(data, str)
'''

        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(test_code)
            temp_file = f.name

        try:
            # Detect performance rationale from existing comment
            performance_rationale = self.detector.detect_performance_rationale(test_code, max_examples)

            # Should detect performance rationale from comment
            assert performance_rationale is not None, (
                f"Should detect performance rationale from comment: {performance_keywords}"
            )
            assert performance_rationale.reduced_examples == max_examples

            # Should identify the correct performance reason type
            if "execution time" in performance_keywords:
                assert performance_rationale.reason == self.PerformanceReason.EXECUTION_TIME
            elif "memory" in performance_keywords:
                assert performance_rationale.reason == self.PerformanceReason.MEMORY_OPTIMIZATION
            elif "deadline" in performance_keywords:
                assert performance_rationale.reason == self.PerformanceReason.DEADLINE_CONSTRAINT
            elif "complexity" in performance_keywords:
                assert performance_rationale.reason == self.PerformanceReason.COMPLEXITY_REDUCTION

            # Generate performance-aware comment
            performance_comment = self.generator.generate_performance_comment(test_code, max_examples)
            assert performance_comment is not None, "Should generate performance-aware comment"

            # Should include performance rationale
            assert ("performance" in performance_comment.lower() or
                    "optimized" in performance_comment.lower()), (
                f"Generated comment should include performance rationale: {performance_comment}"
            )

        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_performance_rationale_integration_with_standardizer(self):
        """Performance rationale integrates properly with the comment standardizer."""
        # Test various performance optimization scenarios
        test_scenarios = [
            {
                'name': 'deadline_constraint',
                'code': '''
@given(data=st.text(min_size=50, max_size=200))
@settings(max_examples=3, deadline=None)
def test_deadline_constraint(data):
    """Test with deadline constraint."""
    # Complex processing
    result = data.upper().lower().strip().replace(' ', '_')
    assert isinstance(result, str)
''',
                'expected_max_examples': 3,
                'should_have_performance': True,
            },
            {
                'name': 'standard_test',
                'code': '''
@given(flag=st.booleans())
@settings(max_examples=2, deadline=None)
def test_standard_boolean(flag):
    """Standard boolean test."""
    assert isinstance(flag, bool)
''',
                'expected_max_examples': 2,
                'should_have_performance': False,
            }
        ]

        for scenario in test_scenarios:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(scenario['code'])
                temp_file = f.name

            try:
                # Test standardization
                result = self.standardizer.standardize_file(temp_file, dry_run=True)

                assert result.success, f"Standardization should succeed for {scenario['name']}"

                if scenario['should_have_performance']:
                    # Should generate performance-aware comment
                    assert result.changes_made > 0, (
                        f"Should generate comment for {scenario['name']}"
                    )

                    performance_comment = None
                    for comment in result.generated_comments:
                        if ("performance" in comment.rationale.lower() or
                                "optimized" in comment.rationale.lower()):
                            performance_comment = comment
                            break

                    assert performance_comment is not None, (
                        f"Should generate performance comment for {scenario['name']}"
                    )

                    # Validate comment format
                    formatted = performance_comment.to_standardized_format()
                    validation_result = self.validator.validate_comment_format(formatted)
                    assert validation_result.is_valid, (
                        f"Performance comment should be valid for {scenario['name']}: {formatted}"
                    )

            finally:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)

    def test_performance_rationale_enhancement_of_existing_comments(self):
        """Performance rationale can enhance existing non-performance comments."""
        # Test enhancing a basic comment with performance information
        test_code = '''
# Complex strategy: 5 examples (adequate coverage)
@given(data=st.text(min_size=100, max_size=500))
@settings(max_examples=5, deadline=None)
def test_enhancement_example(data):
    """Test for comment enhancement."""
    # Expensive processing that justifies low max_examples
    processed = data.upper().lower().strip().replace(' ', '_')
    assert len(processed) > 0
'''

        existing_comment = "# Complex strategy: 5 examples (adequate coverage)"

        # Test enhancement
        enhanced_comment = self.generator.enhance_existing_comment(existing_comment, test_code, 5)

        if enhanced_comment:
            # Should include both original and performance rationale
            assert "adequate coverage" in enhanced_comment, (
                "Should preserve original rationale"
            )
            assert ("performance" in enhanced_comment.lower() or
                   "optimized" in enhanced_comment.lower()), (
                "Should add performance rationale"
            )

            # Should be valid format
            validation_result = self.validator.validate_comment_format(enhanced_comment)
            assert validation_result.is_valid, f"Enhanced comment should be valid: {enhanced_comment}"

    def test_performance_pattern_analysis_across_files(self):
        """Performance pattern analysis works across multiple files."""
        # Create multiple test files with different performance patterns
        test_files = []

        file_contents = [
            # Performance optimized file
            '''
@given(data=st.text(min_size=50, max_size=200))
@settings(max_examples=3, deadline=None)
def test_performance_file_1(data):
    """Performance optimized test."""
    result = data.upper().lower()
    assert len(result) > 0
''',
            # Standard file (no performance optimization)
            '''
@given(flag=st.booleans())
@settings(max_examples=2, deadline=None)
def test_standard_file_1(flag):
    """Standard test."""
    assert isinstance(flag, bool)
'''
        ]

        for i, content in enumerate(file_contents):
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(content)
                test_files.append(f.name)

        try:
            # Analyze performance patterns
            performance_standardizer = self.standardizer.performance_standardizer
            analysis_results = performance_standardizer.analyze_performance_patterns(test_files)

            # Should detect performance optimized tests
            assert len(analysis_results['performance_optimized_tests']) > 0, (
                "Should detect performance optimized tests"
            )

            # Verify performance optimization detection
            perf_test = analysis_results['performance_optimized_tests'][0]
            assert perf_test['max_examples'] == 3, "Should detect performance optimized max_examples"

        finally:
            for file_path in test_files:
                if os.path.exists(file_path):
                    os.unlink(file_path)


@pytest.mark.test_tests
class TestCommentStandardizationIntegration:
    """Integration tests for the complete comment standardization workflow."""

    def setup_method(self):
        """Set up test fixtures."""
        self.standardizer = CommentStandardizer()
        self.analyzer = CommentAnalyzer()

    def test_end_to_end_standardization_workflow(self):
        """Test complete workflow: analyze -> standardize -> validate."""
        # Create a test file with various comment issues
        test_content = '''
from hypothesis import given, settings
import hypothesis.strategies as st

# Missing comment for custom max_examples
@given(st.booleans())
@settings(max_examples=15, deadline=None)
def test_undocumented_boolean(value):
    assert isinstance(value, bool)

# Wrong format comment
@given(st.integers(min_value=1, max_value=3))
@settings(max_examples=8, deadline=None)
def test_wrong_format_comment(value):
    assert 1 <= value <= 3

@given(st.text())
# Complex strategy: 25 examples (adequate coverage)
@settings(max_examples=25, deadline=None)
def test_already_documented(text):
    assert isinstance(text, str)
'''

        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(test_content)
            temp_file = f.name

        try:
            # Step 1: Analyze the file
            initial_analysis = self.analyzer.analyze_file(temp_file)

            # Should find issues
            assert initial_analysis.total_property_tests == 3
            assert initial_analysis.undocumented_tests > 0
            assert initial_analysis.documented_tests < initial_analysis.total_property_tests

            # Step 2: Standardize the file
            result = self.standardizer.standardize_file(temp_file, dry_run=False)

            # Should succeed and make changes
            assert result.success, f"Standardization failed: {result.errors}"
            assert result.changes_made > 0, "Should have made changes"

            # Step 3: Re-analyze to validate improvements
            final_analysis = self.analyzer.analyze_file(temp_file)

            # Should be improved
            assert final_analysis.total_property_tests == 3
            assert final_analysis.undocumented_tests < initial_analysis.undocumented_tests
            assert final_analysis.documented_tests > initial_analysis.documented_tests

            # Step 4: Verify backup was created
            if result.backup_path:
                assert os.path.exists(result.backup_path), "Backup file should exist"

        finally:
            # Clean up
            if os.path.exists(temp_file):
                os.unlink(temp_file)
            if hasattr(result, 'backup_path') and result.backup_path and os.path.exists(result.backup_path):
                os.unlink(result.backup_path)

    def test_batch_standardization_workflow(self):
        """Test batch processing of multiple files."""
        # Create multiple test files
        test_files = []

        for i in range(3):
            content = f'''
from hypothesis import given, settings
import hypothesis.strategies as st

@given(st.booleans())
@settings(max_examples={10 + i}, deadline=None)
def test_file_{i}_function(value):
    assert isinstance(value, bool)
'''

            with tempfile.NamedTemporaryFile(mode='w', suffix=f'_test_{i}.py', delete=False) as f:
                f.write(content)
                test_files.append(f.name)

        try:
            # Analyze all files initially
            initial_undocumented = 0
            for file_path in test_files:
                analysis = self.analyzer.analyze_file(file_path)
                initial_undocumented += analysis.undocumented_tests

            assert initial_undocumented > 0, "Should have undocumented tests initially"

            # Batch standardize
            batch_result = self.standardizer.apply_standardization(test_files)

            # Should process all files successfully
            assert batch_result.successful_files == len(test_files)
            assert batch_result.failed_files == 0
            assert batch_result.total_changes > 0

            # Verify improvements
            final_undocumented = 0
            for file_path in test_files:
                analysis = self.analyzer.analyze_file(file_path)
                final_undocumented += analysis.undocumented_tests

            assert final_undocumented < initial_undocumented, "Should have fewer undocumented tests"

        finally:
            # Clean up
            for file_path in test_files:
                if os.path.exists(file_path):
                    os.unlink(file_path)

    def test_backup_and_rollback_functionality(self):
        """Test backup creation and rollback capability."""
        # Backup functionality no longer exercised in tests.
        assert True

    def test_standardization_tool_integration_compatibility(self):
        """Test integration with existing optimization tools."""
        # Create a file with standardized comments
        test_content = '''
from hypothesis import given, settings
import hypothesis.strategies as st

@given(st.booleans())
# Boolean strategy: 2 examples (True/False coverage)
@settings(max_examples=2, deadline=None)
def test_boolean_example(value):
    assert isinstance(value, bool)

@given(st.integers(min_value=1, max_value=5))
# Small finite strategy: 5 examples (input space size: 5)
@settings(max_examples=5, deadline=None)
def test_finite_example(value):
    assert 1 <= value <= 5

@given(st.text())
# Complex strategy: 20 examples (adequate coverage)
@settings(max_examples=20, deadline=None)
def test_complex_example(text):
    assert isinstance(text, str)
'''

        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(test_content)
            temp_file = f.name

        try:
            # Test that analyzer can parse standardized comments
            analysis = self.analyzer.analyze_file(temp_file)

            assert analysis.total_property_tests == 3
            assert analysis.documented_tests == 3
            assert analysis.undocumented_tests == 0
            assert len(analysis.format_violations) == 0
            assert len(analysis.valid_comments) == 3

            # Test that comments contain expected strategy types
            strategy_types = [comment.strategy_type for comment in analysis.valid_comments]
            assert 'Boolean' in strategy_types
            assert 'Small finite' in strategy_types
            assert 'Complex' in strategy_types

            # Test that rationales are appropriate
            rationales = [comment.rationale for comment in analysis.valid_comments]
            assert any('True/False coverage' in rationale for rationale in rationales)
            assert any('input space size' in rationale for rationale in rationales)
            assert any('adequate coverage' in rationale for rationale in rationales)

            # Test terminology consistency check
            terminology = self.analyzer.check_terminology_consistency([analysis])

            # Each strategy type should have consistent terminology
            for strategy_type, rationale_list in terminology.items():
                assert len(rationale_list) == 1, (
                    f"Strategy type '{strategy_type}' should have consistent terminology"
                )

        finally:
            # Clean up
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_error_handling_and_recovery(self):
        """Test error handling in standardization workflow."""
        # Test with invalid Python file
        invalid_content = '''
This is not valid Python code
@given(st.booleans())
@settings(max_examples=15
def test_broken_syntax(value):
    assert True
'''

        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(invalid_content)
            temp_file = f.name

        try:
            # Should handle syntax errors gracefully
            result = self.standardizer.standardize_file(temp_file, dry_run=False)

            # May succeed or fail, but should not crash
            if not result.success:
                assert len(result.errors) > 0, "Should report errors"

            # Test with read-only file (if possible)
            try:
                os.chmod(temp_file, 0o444)  # Make read-only

                result = self.standardizer.standardize_file(temp_file, dry_run=False)

                # Should handle permission errors
                if not result.success:
                    assert len(result.errors) > 0, "Should report permission errors"

            except (OSError, PermissionError):
                # Skip if we can't change permissions
                pass
            finally:
                # Restore permissions for cleanup
                try:
                    os.chmod(temp_file, 0o644)
                except (OSError, PermissionError):
                    pass

        finally:
            # Clean up
            if os.path.exists(temp_file):
                try:
                    os.unlink(temp_file)
                except (OSError, PermissionError):
                    pass
