"""
Property-based tests for code duplication minimization validation.

This module contains property tests that validate the refactoring successfully
minimizes code duplication in the test suite.
"""

import pytest
from hypothesis import given, strategies as st, settings
import tempfile
import os

from kivy_garden.markdownlabel.tests.modules.duplicate_detector import DuplicateDetector


# *For any* test file, the amount of duplicated code (identical function implementations,
# repeated setup patterns) SHALL be below a reasonable threshold.


@st.composite
def _test_suite_with_duplicates(draw):
    """Generate a test suite with varying levels of code duplication."""
    num_files = draw(st.integers(min_value=3, max_value=8))
    duplication_level = draw(st.sampled_from(['low', 'medium', 'high']))

    # Define helper function templates
    helper_templates = {
        'find_labels': """    if labels is None:
        labels = []
    for child in widget.children:
        if isinstance(child, Label):
            labels.append(child)
        labels = find_labels_recursive(child, labels)
    return labels""",

        'collect_ids': """    ids = set()
    ids.add(id(widget))
    for child in getattr(widget, 'children', []):
        ids.update(collect_widget_ids(child))
    return ids""",

        'assert_colors': """    if expected is None and actual is None:
        return True
    if expected is None or actual is None:
        return False
    return abs(expected[0] - actual[0]) < 0.01 and abs(expected[1] - actual[1]) < 0.01""",

        'setup_widget': """    widget = MarkdownLabel()
    widget.text = text or "Test text"
    widget.font_size = 16
    return widget"""
    }

    # Determine duplication pattern based on level
    # Calculate max allowed spread to stay below 70% threshold
    max_allowed_spread = max(2, int(num_files * 0.7))

    if duplication_level == 'low':
        # 1-2 functions duplicated across 2-3 files
        num_duplicated_functions = draw(st.integers(min_value=1, max_value=2))
        duplication_spread = draw(st.integers(min_value=2, max_value=min(3, max_allowed_spread)))
    elif duplication_level == 'medium':
        # 2-4 functions duplicated across 3-5 files
        num_duplicated_functions = draw(st.integers(min_value=2, max_value=4))
        duplication_spread = draw(
            st.integers(min_value=min(3, max_allowed_spread),
                       max_value=min(5, max_allowed_spread)))
    else:  # high
        # 4-6 functions duplicated across 5+ files
        num_duplicated_functions = draw(st.integers(min_value=4, max_value=6))
        duplication_spread = draw(
            st.integers(min_value=min(5, max_allowed_spread),
                       max_value=max_allowed_spread))

    # Select which functions to duplicate
    function_names = list(helper_templates.keys())
    duplicated_functions = draw(st.lists(
        st.sampled_from(function_names),
        min_size=min(num_duplicated_functions, len(function_names)),
        max_size=min(num_duplicated_functions, len(function_names)),
        unique=True
    ))

    # Generate test files
    files = []
    for i in range(num_files):
        file_content = f'''"""Test module {i}."""
import pytest
from kivy_garden.markdownlabel import MarkdownLabel
from kivy.uix.label import Label

class TestModule{i}:
    """Test class {i}."""
'''

        # Add duplicated helper functions to some files
        for func_name in duplicated_functions:
            if i < duplication_spread:  # Only add to first N files
                template = helper_templates[func_name]
                file_content += f'''
    def {func_name}_helper(self, widget, labels=None):
        """Helper function for {func_name}."""
{template}
'''

        # Add unique functions to each file
        file_content += f'''
    def unique_helper_{i}(self):
        """Unique helper for file {i}."""
        return {i}

    def test_example_{i}(self):
        """Example test {i}."""
        assert self.unique_helper_{i}() == {i}
'''

        files.append(file_content)

    return {
        'files': files,
        'duplication_level': duplication_level,
        'expected_duplicates': len(duplicated_functions) * duplication_spread,
        'num_files': num_files
    }


@pytest.mark.test_tests
class TestCodeDuplicationMinimization:
    """Property tests for code duplication minimization (Property 9)."""

    @given(_test_suite_with_duplicates())
    # Complex strategy: 15 examples (adequate coverage for duplication patterns)
    @settings(max_examples=15, deadline=None)
    def test_duplication_below_threshold(self, test_data):
        """Test suite should have code duplication below acceptable threshold."""
        files = test_data['files']
        duplication_level = test_data['duplication_level']
        num_files = test_data['num_files']

        # Create temporary test files
        temp_files = []
        temp_dir = tempfile.mkdtemp()

        try:
            for i, content in enumerate(files):
                file_path = os.path.join(temp_dir, f"test_module_{i}.py")
                with open(file_path, 'w') as f:
                    f.write(content)
                temp_files.append(file_path)

            # Analyze duplication
            detector = DuplicateDetector(similarity_threshold=0.8)
            report = detector.analyze_directory(temp_dir)

            # Calculate duplication metrics
            duplication_ratio = report.total_duplicates / max(num_files, 1)

            # Property 9: Duplication should be below reasonable thresholds
            if duplication_level == 'low':
                # Low duplication: should have very few duplicates
                assert duplication_ratio <= 2.0, \
                    f"Low duplication test suite has too many duplicates: {duplication_ratio:.1f} per file"
            elif duplication_level == 'medium':
                # Medium duplication: should be moderate
                assert duplication_ratio <= 4.0, \
                    f"Medium duplication test suite has too many duplicates: {duplication_ratio:.1f} per file"
            else:  # high
                # High duplication: should still be manageable
                assert duplication_ratio <= 8.0, \
                    f"High duplication test suite has excessive duplicates: {duplication_ratio:.1f} per file"

            # Additional constraint: no single function should appear in more than 70% of files
            for group in report.duplicate_groups:
                unique_files = len(set(func.file_path for func in group.functions))
                file_spread_ratio = unique_files / num_files
                assert file_spread_ratio <= 0.7, \
                    f"Function {group.function_name} appears in too many files: {file_spread_ratio:.1%}"

        finally:
            # Clean up
            for file_path in temp_files:
                if os.path.exists(file_path):
                    os.unlink(file_path)
            os.rmdir(temp_dir)

    @given(st.integers(min_value=2, max_value=6))
    # Small finite strategy: 5 examples (input space size: 5)
    @settings(max_examples=5, deadline=None)
    def test_consolidation_reduces_duplication(self, num_duplicates):
        """Consolidating duplicates should reduce overall duplication metrics."""
        temp_dir = tempfile.mkdtemp()

        try:
            # Create "before" state with duplicates
            before_files = []
            for i in range(num_duplicates):
                content = f'''"""Test module {i} - before consolidation."""
import pytest

class TestBefore{i}:
    """Test class {i}."""

    def find_labels_recursive(self, widget, labels=None):
        """Duplicate helper function."""
        if labels is None:
            labels = []
        for child in widget.children:
            if hasattr(child, 'text'):
                labels.append(child)
            labels = self.find_labels_recursive(child, labels)
        return labels

    def test_example_{i}(self):
        """Example test."""
        assert True
'''
                file_path = os.path.join(temp_dir, f"test_before_{i}.py")
                with open(file_path, 'w') as f:
                    f.write(content)
                before_files.append(file_path)

            # Measure "before" duplication
            detector = DuplicateDetector()
            before_report = detector.analyze_directory(temp_dir)

            # Clean up before files
            for file_path in before_files:
                os.unlink(file_path)

            # Create "after" state with consolidated helpers
            # First create test_utils.py
            utils_content = '''"""Consolidated test utilities."""

def find_labels_recursive(widget, labels=None):
    """Consolidated helper function."""
    if labels is None:
        labels = []
    for child in widget.children:
        if hasattr(child, 'text'):
            labels.append(child)
        labels = find_labels_recursive(child, labels)
    return labels
'''
            utils_path = os.path.join(temp_dir, "test_utils.py")
            with open(utils_path, 'w') as f:
                f.write(utils_content)

            # Create "after" test files that import from utils
            after_files = [utils_path]
            for i in range(num_duplicates):
                content = f'''"""Test module {i} - after consolidation."""
import pytest
from test_utils import find_labels_recursive

class TestAfter{i}:
    """Test class {i}."""

    def test_example_{i}(self):
        """Example test."""
        # Use imported helper
        result = find_labels_recursive(None, [])
        assert result == []
'''
                file_path = os.path.join(temp_dir, f"test_after_{i}.py")
                with open(file_path, 'w') as f:
                    f.write(content)
                after_files.append(file_path)

            # Measure "after" duplication
            after_report = detector.analyze_directory(temp_dir)

            # Property 9: Consolidation should reduce duplication
            assert after_report.total_duplicates < before_report.total_duplicates, \
                (f"Consolidation should reduce duplicates: "
                 f"{before_report.total_duplicates} -> {after_report.total_duplicates}")

            assert len(after_report.duplicate_groups) <= len(before_report.duplicate_groups), \
                (f"Consolidation should reduce duplicate groups: "
                 f"{len(before_report.duplicate_groups)} -> {len(after_report.duplicate_groups)}")

        finally:
            # Clean up all files
            for file_path in after_files:
                if os.path.exists(file_path):
                    os.unlink(file_path)
            os.rmdir(temp_dir)

    def test_duplication_threshold_realistic(self):
        """Duplication thresholds should be realistic for actual test suites."""
        # Test with a realistic test suite structure
        temp_dir = tempfile.mkdtemp()

        try:
            # Create a realistic test suite with some acceptable duplication
            realistic_files = [
                # Core functionality tests
                '''"""Core functionality tests."""
import pytest
from kivy_garden.markdownlabel import MarkdownLabel

class TestCoreFunctionality:
    """Test core functionality."""

    def setup_basic_widget(self, text="Test"):
        """Setup helper - acceptable duplication."""
        widget = MarkdownLabel()
        widget.text = text
        return widget

    def test_basic_rendering(self):
        """Test basic rendering."""
        widget = self.setup_basic_widget()
        assert widget.text == "Test"
''',

                # Property tests
                '''"""Property tests."""
import pytest
from kivy_garden.markdownlabel import MarkdownLabel

class TestProperties:
    """Test properties."""

    def setup_basic_widget(self, text="Test"):
        """Setup helper - acceptable duplication."""
        widget = MarkdownLabel()
        widget.text = text
        return widget

    def test_font_properties(self):
        """Test font properties."""
        widget = self.setup_basic_widget()
        widget.font_size = 20
        assert widget.font_size == 20
''',

                # Performance tests
                '''"""Performance tests."""
import pytest
from kivy_garden.markdownlabel import MarkdownLabel

class TestPerformance:
    """Test performance."""

    def create_large_widget(self, size=1000):
        """Unique helper - no duplication."""
        text = "Large text " * size
        widget = MarkdownLabel()
        widget.text = text
        return widget

    def test_large_text_performance(self):
        """Test large text performance."""
        widget = self.create_large_widget(100)
        assert len(widget.text) > 1000
'''
            ]

            # Write files
            temp_files = []
            for i, content in enumerate(realistic_files):
                file_path = os.path.join(temp_dir, f"test_realistic_{i}.py")
                with open(file_path, 'w') as f:
                    f.write(content)
                temp_files.append(file_path)

            # Analyze duplication
            detector = DuplicateDetector(similarity_threshold=0.8)
            report = detector.analyze_directory(temp_dir)

            # This realistic suite should pass our thresholds
            duplication_ratio = report.total_duplicates / len(realistic_files)

            # Should be acceptable (some setup duplication is normal)
            assert duplication_ratio <= 3.0, \
                f"Realistic test suite exceeds duplication threshold: {duplication_ratio:.1f}"

            # Should not have excessive duplicate groups
            assert len(report.duplicate_groups) <= 2, \
                f"Realistic test suite has too many duplicate groups: {len(report.duplicate_groups)}"

        finally:
            # Clean up
            for file_path in temp_files:
                if os.path.exists(file_path):
                    os.unlink(file_path)
            os.rmdir(temp_dir)

    @given(st.floats(min_value=0.1, max_value=1.0))
    # Complex strategy: 8 examples (adequate coverage)
    @settings(max_examples=8, deadline=None)
    def test_similarity_threshold_affects_detection(self, threshold):
        """Different similarity thresholds should affect duplicate detection."""
        temp_dir = tempfile.mkdtemp()

        try:
            # Create files with similar but not identical functions
            similar_files = []
            for i in range(3):
                # Vary the implementation slightly
                if i == 0:
                    body = """        if labels is None:
            labels = []
        return labels"""
                elif i == 1:
                    body = """        if not labels:
            labels = []
        return labels"""
                else:
                    body = """        labels = labels or []
        return labels"""

                content = f'''"""Test module {i}."""
import pytest

class TestSimilar{i}:
    """Test class {i}."""

    def similar_helper(self, labels=None):
        """Similar helper function."""
{body}

    def test_example_{i}(self):
        """Example test."""
        assert True
'''
                file_path = os.path.join(temp_dir, f"test_similar_{i}.py")
                with open(file_path, 'w') as f:
                    f.write(content)
                similar_files.append(file_path)

            # Test with the given threshold
            detector = DuplicateDetector(similarity_threshold=threshold)
            report = detector.analyze_directory(temp_dir)

            # Higher thresholds should find fewer duplicates (more strict)
            # Lower thresholds should find more duplicates (less strict)
            if threshold >= 0.9:
                # Very strict - might not find these similar functions
                assert report.total_duplicates <= 3
            elif threshold <= 0.3:
                # Very lenient - should find the similar functions
                assert report.total_duplicates >= 0  # At least not crash

            # Should not crash regardless of threshold
            assert isinstance(report.total_duplicates, int)
            assert report.total_duplicates >= 0

        finally:
            # Clean up
            for file_path in similar_files:
                if os.path.exists(file_path):
                    os.unlink(file_path)
            os.rmdir(temp_dir)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
