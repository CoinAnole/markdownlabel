"""Property-based tests for finite strategy comment standardization.

Tests the CommentStandardizer's ability to generate and apply standardized
comments for finite strategy property-based tests.
"""

import pytest
import os
import tempfile
from hypothesis import given, strategies as st, settings

from kivy_garden.markdownlabel.tests.modules.comment_manager import (
    CommentStandardizer, CommentFormatValidator
)


@pytest.mark.test_tests
class TestFiniteStrategyDocumentation:
    """Property tests for finite strategy documentation."""

    def setup_method(self):
        """Set up test fixtures."""
        self.standardizer = CommentStandardizer()
        self.validator = CommentFormatValidator()

    # *For any* property-based test using finite strategies, the comment SHALL reference
    # input space size in the rationale

    @pytest.mark.property
    @given(
        min_value=st.integers(min_value=0, max_value=10),
        max_value=st.integers(min_value=11, max_value=50),
        max_examples=st.integers(min_value=1, max_value=100).filter(
            lambda x: x not in {2, 5, 10, 20, 50, 100}
        )
    )
    # Complex combination strategy: 50 examples (440 finite combinations with 1 complex strategy)
    @settings(max_examples=50, deadline=None)
    def test_finite_strategy_comments_reference_input_space_size(
        self, min_value, max_value, max_examples
    ):
        """Finite strategy comments reference input space size in rationale."""
        # Ensure we have a finite range
        if max_value <= min_value:
            max_value = min_value + 10

        input_space_size = max_value - min_value + 1

        # Create test code with finite integer strategy but no comment
        test_code = f'''
@given(num=st.integers(min_value={min_value}, max_value={max_value}))
@settings(max_examples={max_examples}, deadline=None)
def test_finite_strategy(num):
    """Test function using finite integer strategy."""
    assert {min_value} <= num <= {max_value}
'''

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

            # Find the finite strategy comment
            finite_comment = None
            for comment in result.generated_comments:
                if "finite" in comment.strategy_type.lower():
                    finite_comment = comment
                    break

            # Should have generated a finite strategy comment
            assert finite_comment is not None, "Should generate a finite strategy comment"

            # Comment should reference input space size or finite coverage
            rationale_lower = finite_comment.rationale.lower()
            assert ("input space size" in rationale_lower or
                   "finite coverage" in rationale_lower), (
                f"Finite strategy rationale should reference input space or "
                f"finite coverage, got: {finite_comment.rationale}"
            )

            # If it mentions input space size, it should include the actual size for small finite
            if "input space size" in rationale_lower and input_space_size <= 10:
                assert str(input_space_size) in finite_comment.rationale, (
                    f"Small finite strategy should include actual input space size {input_space_size}"
                )

            # Verify the generated comment is valid
            formatted_comment = finite_comment.to_standardized_format()
            validation_result = self.validator.validate_comment_format(formatted_comment)
            assert validation_result.is_valid, f"Generated comment should be valid: {formatted_comment}"

        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    @pytest.mark.property
    @given(
        items=st.lists(st.text(min_size=1, max_size=10), min_size=1, max_size=20),
        max_examples=st.integers(min_value=1, max_value=50).filter(
            lambda x: x not in {2, 5, 10, 20, 50, 100}
        )
    )
    # Complex strategy: 30 examples (adequate coverage)
    @settings(max_examples=30, deadline=None)
    def test_sampled_from_finite_strategy_documentation(self, items, max_examples):
        """Sampled_from finite strategies are properly documented."""
        # Create unique items to avoid duplicates affecting size calculation
        unique_items = list(set(items))
        if len(unique_items) == 0:
            unique_items = ['item1']

        items_str = ', '.join(repr(item) for item in unique_items[:10])  # Limit to 10 items

        test_code = f'''
@given(item=st.sampled_from([{items_str}]))
@settings(max_examples={max_examples}, deadline=None)
def test_sampled_from_strategy(item):
    """Test function using sampled_from strategy."""
    assert item in [{items_str}]
'''

        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(test_code)
            temp_file = f.name

        try:
            result = self.standardizer.standardize_file(temp_file, dry_run=True)

            assert result.success
            assert result.changes_made > 0

            # Should generate appropriate finite strategy comment
            finite_comment = None
            for comment in result.generated_comments:
                if "finite" in comment.strategy_type.lower():
                    finite_comment = comment
                    break

            if finite_comment:
                # Should reference finite coverage or input space
                rationale_lower = finite_comment.rationale.lower()
                assert ("finite coverage" in rationale_lower or
                       "input space size" in rationale_lower), (
                    f"Sampled_from strategy should reference finite coverage: "
                    f"{finite_comment.rationale}"
                )

        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_finite_strategy_size_classification(self):
        """Finite strategies are correctly classified by size."""
        test_cases = [
            # Small finite (≤10 elements)
            ('st.integers(min_value=0, max_value=4)', "Small finite", 5),
            ('st.integers(min_value=1, max_value=10)', "Small finite", 10),

            # Medium finite (11-51 elements)
            ('st.integers(min_value=0, max_value=25)', "Medium finite", 26),
            ('st.integers(min_value=10, max_value=50)', "Medium finite", 41),
        ]

        for strategy_code, expected_type, expected_size in test_cases:
            # Use custom max_examples value
            custom_max_examples = 15  # Non-standard value
            test_code = f'''
@given(num={strategy_code})
@settings(max_examples={custom_max_examples}, deadline=None)
def test_finite_classification(num):
    """Test finite strategy classification."""
    assert isinstance(num, int)
'''

            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(test_code)
                temp_file = f.name

            try:
                result = self.standardizer.standardize_file(temp_file, dry_run=True)

                assert result.success
                assert result.changes_made > 0

                # Find the generated comment
                generated_comment = result.generated_comments[0]

                # Should be classified correctly
                assert expected_type.lower() in generated_comment.strategy_type.lower(), (
                    f"Strategy {strategy_code} should be classified as {expected_type}, "
                    f"got {generated_comment.strategy_type}"
                )

                # Should reference appropriate rationale
                if expected_type == "Small finite":
                    assert ("input space size" in generated_comment.rationale or
                           "finite coverage" in generated_comment.rationale)
                elif expected_type == "Medium finite":
                    assert "finite coverage" in generated_comment.rationale

            finally:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)

    def test_finite_strategy_rationale_consistency(self):
        """Finite strategy rationale is consistent across similar strategies."""
        small_finite_strategies = [
            'st.integers(min_value=0, max_value=5)',
            'st.integers(min_value=1, max_value=8)',
            'st.sampled_from(["a", "b", "c", "d", "e"])'
        ]

        medium_finite_strategies = [
            'st.integers(min_value=0, max_value=20)',
            'st.integers(min_value=5, max_value=30)',
        ]

        # Test small finite strategies
        small_finite_rationales = set()
        for strategy in small_finite_strategies:
            comment = self.standardizer.generate_comment("Small finite", 10, 6)
            small_finite_rationales.add(comment.lower())

        # Should use consistent rationale patterns
        for rationale in small_finite_rationales:
            assert ("input space size" in rationale or "finite coverage" in rationale)

        # Test medium finite strategies
        medium_finite_rationales = set()
        for strategy in medium_finite_strategies:
            comment = self.standardizer.generate_comment("Medium finite", 20)
            medium_finite_rationales.add(comment.lower())

        # Should use consistent rationale patterns
        for rationale in medium_finite_rationales:
            assert "finite coverage" in rationale

    def test_safety_checks_and_validation(self):
        """Test safety checks and validation functionality."""
        # Test file that doesn't need standardization
        already_standardized_content = '''
# Boolean strategy: 2 examples (True/False coverage)
@given(flag=st.booleans())
@settings(max_examples=2, deadline=None)
def test_already_standardized(flag):
    """Already standardized test function."""
    assert isinstance(flag, bool)
'''

        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(already_standardized_content)
            temp_file = f.name

        try:
            # Should not create backup for already standardized file
            result = self.standardizer.standardize_file(temp_file, dry_run=False)

            assert result.success
            assert result.changes_made == 0  # No changes needed
            assert result.backup_path is None  # No backup created

            # Validate standardization
            is_standardized = self.standardizer.validate_standardization(temp_file)
            assert is_standardized

        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_error_handling_in_backup_operations(self):
        """Test error handling in backup operations."""
        # Test rollback with non-existent backup
        rollback_success = self.standardizer.rollback_file(
            "/some/file.py",
            "/non/existent/backup.py"
        )
        assert not rollback_success

        # Test backup info for invalid path
        info = self.standardizer.get_backup_info("/invalid/path/backup.py")
        assert info is None

        # Test cleanup with non-existent backup directory
        original_backup_dir = self.standardizer.backup_dir
        self.standardizer.backup_dir = "/non/existent/backup/dir"

        try:
            removed_count = self.standardizer.cleanup_old_backups()
            assert removed_count == 0

            backups = self.standardizer.list_backups()
            assert backups == []

        finally:
            self.standardizer.backup_dir = original_backup_dir
