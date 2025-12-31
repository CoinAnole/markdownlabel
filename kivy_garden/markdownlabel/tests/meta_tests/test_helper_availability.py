"""
Property tests for helper function availability in test_utils.

This module contains property-based tests that verify all required helper
functions are available in test_utils.py and work correctly.
"""

import pytest
from hypothesis import given, settings, strategies as st
from kivy.uix.label import Label

from kivy_garden.markdownlabel import MarkdownLabel
from kivy_garden.markdownlabel.tests.test_utils import (
    find_labels_recursive,
    colors_equal,
    padding_equal,
    floats_equal,
    collect_widget_ids,
    assert_rebuild_occurred,
    assert_no_rebuild,
    FakeTouch,
    color_strategy,
    text_padding_strategy,
    simple_markdown_document
)


@pytest.mark.test_tests
class TestHelperFunctionAvailability:
    """Property tests for helper function availability (Property 7)."""

    # Complex strategy: 10 examples (adequate coverage)
    @given(st.text(min_size=1, max_size=50))
    @settings(max_examples=10, deadline=None)
    def test_widget_traversal_helpers_available(self, markdown_text):
        """For any markdown content, widget traversal helpers should be available and functional.

        **Feature: test-suite-refactoring, Property 7: Helper Function Availability**
        **Validates: Requirements 2.4, 4.3**
        """
        # Create a MarkdownLabel with content
        label = MarkdownLabel(text=markdown_text)

        # Test find_labels_recursive is available and works
        labels = find_labels_recursive(label)
        assert isinstance(labels, list)
        assert all(isinstance(l, Label) for l in labels)

        # Test collect_widget_ids is available and works
        widget_ids = collect_widget_ids(label)
        assert isinstance(widget_ids, dict)
        assert len(widget_ids) >= 1  # At least the root widget

        # Test collect_widget_ids with exclude_root
        widget_ids_no_root = collect_widget_ids(label, exclude_root=True)
        assert isinstance(widget_ids_no_root, dict)

    # Complex strategy: 10 examples (adequate coverage)
    @given(color_strategy, color_strategy)
    @settings(max_examples=10, deadline=None)
    def test_comparison_helpers_available(self, color1, color2):
        """For any color values, comparison helpers should be available and functional.

        **Feature: test-suite-refactoring, Property 7: Helper Function Availability**
        **Validates: Requirements 2.4, 4.3**
        """
        # Test colors_equal is available and works
        result = colors_equal(color1, color2)
        assert isinstance(result, bool)

        # Test colors_equal with identical colors
        assert colors_equal(color1, color1) is True

    # Complex strategy: 10 examples (adequate coverage)
    @given(text_padding_strategy, text_padding_strategy)
    @settings(max_examples=10, deadline=None)
    def test_padding_comparison_helpers_available(self, padding1, padding2):
        """For any padding values, padding comparison helpers should be available and functional.

        **Feature: test-suite-refactoring, Property 7: Helper Function Availability**
        **Validates: Requirements 2.4, 4.3**
        """
        # Test padding_equal is available and works
        result = padding_equal(padding1, padding2)
        assert isinstance(result, bool)

        # Test padding_equal with identical padding
        assert padding_equal(padding1, padding1) is True

    # Complex strategy: 10 examples (adequate coverage)
    @given(st.floats(min_value=-1000, max_value=1000, allow_nan=False, allow_infinity=False),
           st.floats(min_value=-1000, max_value=1000, allow_nan=False, allow_infinity=False))
    @settings(max_examples=10, deadline=None)
    def test_float_comparison_helpers_available(self, float1, float2):
        """For any float values, float comparison helpers should be available and functional.

        **Feature: test-suite-refactoring, Property 7: Helper Function Availability**
        **Validates: Requirements 2.4, 4.3**
        """
        # Test floats_equal is available and works
        result = floats_equal(float1, float2)
        assert isinstance(result, bool)

        # Test floats_equal with identical floats
        assert floats_equal(float1, float1) is True

    # Complex strategy: 5 examples (adequate coverage)
    @given(simple_markdown_document())
    @settings(max_examples=5, deadline=None)
    def test_rebuild_detection_helpers_available(self, markdown_text):
        """For any markdown content, rebuild detection helpers should be available and functional.

        **Feature: test-suite-refactoring, Property 7: Helper Function Availability**
        **Validates: Requirements 2.4, 4.3**
        """
        # Create a MarkdownLabel with content
        label = MarkdownLabel(text=markdown_text)

        # Test collect_widget_ids works
        ids_before = collect_widget_ids(label, exclude_root=True)

        # Test assert_no_rebuild works (should not raise)
        ids_same = collect_widget_ids(label, exclude_root=True)
        assert_no_rebuild(label, ids_before, exclude_root=True)

        # Change text to trigger rebuild
        label.text = "# Different content"
        label.force_rebuild()

        # Test assert_rebuild_occurred works (should not raise)
        assert_rebuild_occurred(label, ids_before, exclude_root=True)

    def test_touch_simulation_helpers_available(self):
        """Touch simulation helpers should be available and functional.

        **Feature: test-suite-refactoring, Property 7: Helper Function Availability**
        **Validates: Requirements 2.4, 4.3**
        """
        # Test FakeTouch is available and works
        touch = FakeTouch(100, 200)
        assert touch.x == 100
        assert touch.y == 200
        assert touch.pos == (100, 200)

    # Complex strategy: 1 example (strategy availability verification only)
    @given(color_strategy)
    @settings(max_examples=1, deadline=None)
    def test_color_strategy_available(self, color):
        """color_strategy is available and generates valid colors.

        **Feature: test-suite-refactoring, Property 7: Helper Function Availability**
        **Validates: Requirements 2.4, 4.3**
        """
        assert isinstance(color, list)
        assert len(color) == 4
        assert all(isinstance(c, float) for c in color)

    # Complex strategy: 1 example (strategy availability verification only)
    @given(text_padding_strategy)
    @settings(max_examples=1, deadline=None)
    def test_text_padding_strategy_available(self, padding):
        """text_padding_strategy is available and generates valid padding.

        **Feature: test-suite-refactoring, Property 7: Helper Function Availability**
        **Validates: Requirements 2.4, 4.3**
        """
        assert isinstance(padding, list)
        assert len(padding) == 4
        assert all(isinstance(p, float) for p in padding)

    # Complex strategy: 1 example (strategy availability verification only)
    @given(simple_markdown_document())
    @settings(max_examples=1, deadline=None)
    def test_simple_markdown_document_strategy_available(self, doc):
        """simple_markdown_document strategy is available and generates valid documents.

        **Feature: test-suite-refactoring, Property 7: Helper Function Availability**
        **Validates: Requirements 2.4, 4.3**
        """
        assert isinstance(doc, str)
        assert len(doc) > 0


@pytest.mark.test_tests
class TestHelperFunctionConsolidation:
    """Property tests for helper function consolidation (Property 3)."""

    def test_no_duplicate_find_labels_recursive_implementations(self):
        """For any test file, there should be no duplicate _find_labels_recursive implementations.

        **Feature: test-suite-refactoring, Property 3: Helper Function Consolidation**
        **Validates: Requirements 2.1, 2.2, 2.3**
        """
        import ast
        from pathlib import Path

        test_dir = Path(__file__).parent.parent  # Go up from meta_tests to tests
        duplicate_implementations = []

        for test_file in test_dir.glob('test_*.py'):
            if test_file.name == 'test_helper_availability.py':
                continue  # Skip this file

            try:
                with open(test_file, 'r') as f:
                    content = f.read()

                # Parse the AST to find function definitions
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef) and node.name == '_find_labels_recursive':
                        duplicate_implementations.append(str(test_file.name))
                        break
            except Exception:
                # Skip files that can't be parsed
                continue

        assert len(duplicate_implementations) == 0, \
            f"Found duplicate _find_labels_recursive implementations in: {duplicate_implementations}"

    def test_no_duplicate_collect_widget_ids_implementations(self):
        """For any test file, there should be no duplicate collect_widget_ids implementations.

        **Feature: test-suite-refactoring, Property 3: Helper Function Consolidation**
        **Validates: Requirements 2.1, 2.2, 2.3**
        """
        import ast
        from pathlib import Path

        test_dir = Path(__file__).parent.parent  # Go up from meta_tests to tests
        duplicate_implementations = []

        for test_file in test_dir.glob('test_*.py'):
            if test_file.name in ['test_helper_availability.py', 'test_utils.py']:
                continue  # Skip this file and test_utils.py

            try:
                with open(test_file, 'r') as f:
                    content = f.read()

                # Parse the AST to find function definitions
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef) and node.name == 'collect_widget_ids':
                        duplicate_implementations.append(str(test_file.name))
                        break
            except Exception:
                # Skip files that can't be parsed
                continue

        assert len(duplicate_implementations) == 0, \
            f"Found duplicate collect_widget_ids implementations in: {duplicate_implementations}"

    def test_all_test_files_import_from_test_utils(self):
        """For any test file using helper functions, it should import them from test_utils.

        **Feature: test-suite-refactoring, Property 3: Helper Function Consolidation**
        **Validates: Requirements 2.1, 2.2, 2.3**
        """
        from pathlib import Path

        test_dir = Path(__file__).parent.parent  # Go up from meta_tests to tests
        files_without_imports = []

        for test_file in test_dir.glob('test_*.py'):
            if test_file.name in ['test_helper_availability.py', 'test_utils.py']:
                continue  # Skip this file and test_utils.py

            try:
                with open(test_file, 'r') as f:
                    content = f.read()

                # Check if file uses find_labels_recursive but doesn't import from test_utils
                if 'find_labels_recursive' in content:
                    has_absolute_import = 'from kivy_garden.markdownlabel.tests.test_utils import' in content
                    has_relative_import = 'from .test_utils import' in content
                    if not (has_absolute_import or has_relative_import):
                        files_without_imports.append(str(test_file.name))

            except Exception:
                # Skip files that can't be parsed
                continue

        assert len(files_without_imports) == 0, \
            f"Files using helper functions but not importing from test_utils: {files_without_imports}"
