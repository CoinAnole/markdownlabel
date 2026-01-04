"""
Property-based tests for text-related property forwarding in MarkdownLabel.

Tests verify that text-related properties like text_size, unicode_errors,
and strip are correctly forwarded to child Label widgets.
"""

import pytest
from hypothesis import given, strategies as st, settings, assume

from kivy_garden.markdownlabel import MarkdownLabel
from .test_utils import (
    find_labels_recursive,
    simple_markdown_document,
    unicode_errors_strategy,
    collect_widget_ids
)


class TestTextSizeForwarding:
    """Property tests for text_size forwarding."""

    @pytest.mark.property
    @given(st.floats(min_value=50, max_value=1000, allow_nan=False, allow_infinity=False))
    # Complex strategy: 50 examples (adequate coverage)
    @settings(max_examples=50, deadline=None)
    def test_text_size_width_stored_correctly(self, width):
        """text_size width is stored correctly on MarkdownLabel."""
        label = MarkdownLabel(text='Hello World', text_size=[width, None])

        assert label.text_size[0] == width, \
            f"Expected text_size[0]={width}, got {label.text_size[0]}"

    @pytest.mark.property
    @given(st.floats(min_value=50, max_value=1000, allow_nan=False, allow_infinity=False))
    # Complex strategy: 50 examples (adequate coverage)
    @settings(max_examples=50, deadline=None)
    def test_text_size_property_stored_correctly(self, width):
        """text_size property value is stored correctly on MarkdownLabel."""
        label = MarkdownLabel(text='Hello', text_size=[width, None])

        assert len(label.text_size) == 2, \
            f"Expected 2-element text_size, got {len(label.text_size)}"
        assert label.text_size[0] == width, \
            f"Expected text_size[0]={width}, got {label.text_size[0]}"

    @pytest.mark.property
    @given(st.floats(min_value=50, max_value=1000, allow_nan=False, allow_infinity=False),
           st.floats(min_value=50, max_value=1000, allow_nan=False, allow_infinity=False))
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_text_size_change_updates_value(self, width1, width2):
        """Changing text_size updates the stored value on MarkdownLabel."""
        assume(abs(width1 - width2) > 1)  # Ensure they're different

        label = MarkdownLabel(text='Hello World', text_size=[width1, None])

        # Verify initial text_size
        assert label.text_size[0] == width1

        # Change text_size
        label.text_size = [width2, None]

        # Verify new text_size
        assert label.text_size[0] == width2, \
            f"After change, expected text_size[0]={width2}, got {label.text_size[0]}"

    @pytest.mark.unit
    def test_default_text_size_is_none_none(self):
        """Default text_size is [None, None]."""
        label = MarkdownLabel(text='Hello World')

        assert len(label.text_size) == 2, \
            f"Expected 2-element text_size, got {len(label.text_size)}"
        assert label.text_size[0] is None, \
            f"Default text_size[0] should be None, got {label.text_size[0]}"
        assert label.text_size[1] is None, \
            f"Default text_size[1] should be None, got {label.text_size[1]}"

    @pytest.mark.property
    @given(st.floats(min_value=50, max_value=1000, allow_nan=False, allow_infinity=False))
    # Complex strategy: 50 examples (adequate coverage)
    @settings(max_examples=50, deadline=None)
    def test_text_size_with_width_passed_to_renderer(self, width):
        """text_size with width is passed to renderer and affects internal Labels."""
        label = MarkdownLabel(text='Hello World', text_size=[width, None])

        # The text_size should be stored on the MarkdownLabel
        assert label.text_size[0] == width, \
            f"Expected text_size[0]={width}, got {label.text_size[0]}"

        # Verify the label has children (widgets were created)
        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"


# *For any* MarkdownLabel with `text_size[1]` set to a non-None numeric value H,
# all child Labels SHALL have their `text_size[1]` equal to H, and their `valign`
# property SHALL match the MarkdownLabel's `valign` value.

class TestTextSizeHeightForwarding:
    """Property tests for text_size height forwarding."""

    @pytest.mark.property
    @given(st.floats(min_value=50, max_value=500, allow_nan=False, allow_infinity=False))
    # Complex strategy: 50 examples (adequate coverage)
    @settings(max_examples=50, deadline=None)
    def test_text_size_height_forwarded_to_paragraph(self, height):
        """text_size height is forwarded to paragraph Labels."""
        label = MarkdownLabel(text='Hello World', text_size=[None, height])

        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"

        # All labels should have the specified height in text_size
        for lbl in labels:
            assert lbl.text_size[1] == height, \
                f"Expected text_size[1]={height}, got {lbl.text_size[1]}"

    @pytest.mark.property
    @given(st.floats(min_value=50, max_value=500, allow_nan=False, allow_infinity=False))
    # Complex strategy: 50 examples (adequate coverage)
    @settings(max_examples=50, deadline=None)
    def test_text_size_height_forwarded_to_heading(self, height):
        """text_size height is forwarded to heading Labels."""
        label = MarkdownLabel(text='# Heading', text_size=[None, height])

        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"

        # All labels should have the specified height in text_size
        for lbl in labels:
            assert lbl.text_size[1] == height, \
                f"Expected text_size[1]={height}, got {lbl.text_size[1]}"

    @pytest.mark.property
    @given(st.floats(min_value=100, max_value=500, allow_nan=False, allow_infinity=False),
           st.floats(min_value=50, max_value=300, allow_nan=False, allow_infinity=False))
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_text_size_both_width_and_height_forwarded(self, width, height):
        """Both width and height in text_size are forwarded to Labels."""
        label = MarkdownLabel(text='Hello World', text_size=[width, height])

        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"

        # All labels should have both width and height in text_size
        for lbl in labels:
            assert lbl.text_size[0] == width, \
                f"Expected text_size[0]={width}, got {lbl.text_size[0]}"
            assert lbl.text_size[1] == height, \
                f"Expected text_size[1]={height}, got {lbl.text_size[1]}"

    @pytest.mark.property
    @given(st.floats(min_value=50, max_value=500, allow_nan=False, allow_infinity=False),
           st.sampled_from(['top', 'middle', 'bottom']))
    # Continuous height × 3 valigns
    # Use 20 examples to sample adequately
    @settings(max_examples=20, deadline=None)
    def test_valign_forwarded_with_height(self, height, valign):
        """valign is forwarded to Labels when text_size height is set."""
        label = MarkdownLabel(text='Hello World', text_size=[None, height], valign=valign)

        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"

        # All labels should have the specified valign
        for lbl in labels:
            assert lbl.valign == valign, \
                f"Expected valign={valign}, got {lbl.valign}"

    @pytest.mark.property
    @given(st.floats(min_value=50, max_value=500, allow_nan=False, allow_infinity=False))
    # Complex strategy: 50 examples (adequate coverage)
    @settings(max_examples=50, deadline=None)
    def test_text_size_height_forwarded_to_table_cells(self, height):
        """text_size height is forwarded to table cell Labels."""
        markdown = '| A | B |\n| --- | --- |\n| 1 | 2 |'
        label = MarkdownLabel(text=markdown, text_size=[None, height])

        labels = find_labels_recursive(label)
        assert len(labels) >= 4, "Expected at least 4 Labels for table cells"

        # All labels should have the specified height in text_size
        for lbl in labels:
            assert lbl.text_size[1] == height, \
                f"Expected text_size[1]={height}, got {lbl.text_size[1]}"


# *For any* MarkdownLabel with `text_size[1]` set to None, all child Labels SHALL
# have their `text_size[1]` equal to None, maintaining the existing auto-sizing behavior.

class TestTextSizeHeightNoneBackwardCompatibility:
    """Property tests for text_size height None backward compatibility."""

    @pytest.mark.property
    @given(simple_markdown_document())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_text_size_height_none_preserves_auto_sizing(self, markdown_text):
        """text_size[1]=None preserves auto-sizing behavior."""
        assume(markdown_text.strip())

        label = MarkdownLabel(text=markdown_text, text_size=[None, None])

        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"

        # All labels should have text_size[1]=None for auto-sizing
        for lbl in labels:
            assert lbl.text_size[1] is None, \
                f"Expected text_size[1]=None for auto-sizing, got {lbl.text_size[1]}"

    @pytest.mark.property
    @given(st.floats(min_value=50, max_value=1000, allow_nan=False, allow_infinity=False))
    # Complex strategy: 50 examples (adequate coverage)
    @settings(max_examples=50, deadline=None)
    def test_text_size_width_only_preserves_height_none(self, width):
        """Setting only text_size width preserves height=None."""
        label = MarkdownLabel(text='Hello World', text_size=[width, None])

        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"

        # Labels should have width constraint but height=None
        for lbl in labels:
            # Width should be bound dynamically, but we can check the initial text_size
            # The exact behavior depends on binding, but height should be None
            if hasattr(lbl, 'text_size') and lbl.text_size:
                assert lbl.text_size[1] is None, \
                    f"Expected text_size[1]=None, got {lbl.text_size[1]}"

    def test_default_text_size_maintains_none_height(self):
        """Default text_size=[None, None] maintains None height in child Labels."""
        label = MarkdownLabel(text='Hello World')

        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"

        # All labels should have text_size[1]=None by default
        for lbl in labels:
            if hasattr(lbl, 'text_size') and lbl.text_size:
                assert lbl.text_size[1] is None, \
                    f"Expected default text_size[1]=None, got {lbl.text_size[1]}"


# *For any* MarkdownLabel, when `text_size` is changed from value A to value B,
# all child Labels SHALL be updated to reflect the new `text_size` value B.

class TestTextSizeDynamicUpdates:
    """Property tests for text_size dynamic updates."""

    @pytest.mark.property
    @given(st.floats(min_value=50, max_value=300, allow_nan=False, allow_infinity=False),
           st.floats(min_value=350, max_value=600, allow_nan=False, allow_infinity=False))
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_text_size_height_change_updates_labels(self, height1, height2):
        """Changing text_size height updates all child Labels."""
        label = MarkdownLabel(text='Hello World', text_size=[None, height1])

        # Verify initial height
        labels = find_labels_recursive(label)
        for lbl in labels:
            assert lbl.text_size[1] == height1, \
                f"Initial: Expected text_size[1]={height1}, got {lbl.text_size[1]}"

        # Change text_size height
        label.text_size = [None, height2]
        label.force_rebuild()  # Force immediate rebuild for test

        # Verify new height
        labels = find_labels_recursive(label)
        for lbl in labels:
            assert lbl.text_size[1] == height2, \
                f"After change: Expected text_size[1]={height2}, got {lbl.text_size[1]}"

    @pytest.mark.property
    @given(st.floats(min_value=50, max_value=300, allow_nan=False, allow_infinity=False))
    # Complex strategy: 50 examples (adequate coverage)
    @settings(max_examples=50, deadline=None)
    def test_text_size_height_to_none_updates_labels(self, height):
        """Changing text_size height to None updates all child Labels."""
        label = MarkdownLabel(text='Hello World', text_size=[None, height])

        # Verify initial height
        labels = find_labels_recursive(label)
        for lbl in labels:
            assert lbl.text_size[1] == height, \
                f"Initial: Expected text_size[1]={height}, got {lbl.text_size[1]}"

        # Change text_size height to None
        label.text_size = [None, None]
        label.force_rebuild()  # Force immediate rebuild for test

        # Verify height is now None
        labels = find_labels_recursive(label)
        for lbl in labels:
            if hasattr(lbl, 'text_size') and lbl.text_size:
                assert lbl.text_size[1] is None, \
                    f"After change to None: Expected text_size[1]=None, got {lbl.text_size[1]}"

    @pytest.mark.property
    @given(st.floats(min_value=50, max_value=300, allow_nan=False, allow_infinity=False))
    # Complex strategy: 50 examples (adequate coverage)
    @settings(max_examples=50, deadline=None)
    def test_text_size_none_to_height_updates_labels(self, height):
        """Changing text_size height from None to value updates all child Labels."""
        label = MarkdownLabel(text='Hello World', text_size=[None, None])

        # Verify initial height is None
        labels = find_labels_recursive(label)
        for lbl in labels:
            if hasattr(lbl, 'text_size') and lbl.text_size:
                assert lbl.text_size[1] is None, \
                    f"Initial: Expected text_size[1]=None, got {lbl.text_size[1]}"

        # Change text_size height to specific value
        label.text_size = [None, height]
        label.force_rebuild()  # Force immediate rebuild for test

        # Verify new height
        labels = find_labels_recursive(label)
        for lbl in labels:
            assert lbl.text_size[1] == height, \
                f"After change from None: Expected text_size[1]={height}, got {lbl.text_size[1]}"


# *For any* unicode_errors value in ['strict', 'replace', 'ignore'], all internal
# Labels SHALL have `unicode_errors` set to that value.

class TestUnicodeErrorsForwarding:
    """Property tests for unicode_errors forwarding."""

    @pytest.mark.property
    @given(unicode_errors_strategy)
    # Small finite strategy: 3 examples (input space size: 3)
    @settings(max_examples=3, deadline=None)
    def test_unicode_errors_stored_correctly(self, unicode_errors):
        """unicode_errors value is stored correctly on MarkdownLabel."""
        label = MarkdownLabel(text='Hello World', unicode_errors=unicode_errors)

        assert label.unicode_errors == unicode_errors, \
            f"Expected unicode_errors={unicode_errors}, got {label.unicode_errors}"

    @pytest.mark.property
    @given(unicode_errors_strategy)
    # Small finite strategy: 3 examples (input space size: 3)
    @settings(max_examples=3, deadline=None)
    def test_unicode_errors_applied_to_paragraph(self, unicode_errors):
        """unicode_errors is applied to paragraph Labels."""
        label = MarkdownLabel(text='Hello World', unicode_errors=unicode_errors)

        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"

        # All labels should have the specified unicode_errors
        for lbl in labels:
            assert lbl.unicode_errors == unicode_errors, \
                f"Expected unicode_errors={unicode_errors}, got {lbl.unicode_errors}"

    @pytest.mark.property
    @given(unicode_errors_strategy)
    # Small finite strategy: 3 examples (input space size: 3)
    @settings(max_examples=3, deadline=None)
    def test_unicode_errors_applied_to_heading(self, unicode_errors):
        """unicode_errors is applied to heading Labels."""
        label = MarkdownLabel(text='# Heading', unicode_errors=unicode_errors)

        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"

        # All labels should have the specified unicode_errors
        for lbl in labels:
            assert lbl.unicode_errors == unicode_errors, \
                f"Expected unicode_errors={unicode_errors}, got {lbl.unicode_errors}"

    @pytest.mark.property
    @given(unicode_errors_strategy)
    # Small finite strategy: 3 examples (input space size: 3)
    @settings(max_examples=3, deadline=None)
    def test_unicode_errors_applied_to_code_block(self, unicode_errors):
        """unicode_errors is applied to code block Labels."""
        markdown = '```python\nprint("hello")\n```'
        label = MarkdownLabel(text=markdown, unicode_errors=unicode_errors)

        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label for code block"

        # All labels should have the specified unicode_errors
        for lbl in labels:
            assert lbl.unicode_errors == unicode_errors, \
                f"Expected unicode_errors={unicode_errors}, got {lbl.unicode_errors}"

    @pytest.mark.property
    @given(unicode_errors_strategy)
    # Small finite strategy: 3 examples (input space size: 3)
    @settings(max_examples=3, deadline=None)
    def test_unicode_errors_applied_to_list_items(self, unicode_errors):
        """unicode_errors is applied to list item Labels."""
        markdown = '- Item 1\n- Item 2'
        label = MarkdownLabel(text=markdown, unicode_errors=unicode_errors)

        labels = find_labels_recursive(label)
        assert len(labels) >= 2, "Expected at least 2 Labels for list items"

        # All labels should have the specified unicode_errors
        for lbl in labels:
            assert lbl.unicode_errors == unicode_errors, \
                f"Expected unicode_errors={unicode_errors}, got {lbl.unicode_errors}"

    @pytest.mark.property
    @given(unicode_errors_strategy)
    # Small finite strategy: 3 examples (input space size: 3)
    @settings(max_examples=3, deadline=None)
    def test_unicode_errors_applied_to_table_cells(self, unicode_errors):
        """unicode_errors is applied to table cell Labels."""
        markdown = '| A | B |\n| --- | --- |\n| 1 | 2 |'
        label = MarkdownLabel(text=markdown, unicode_errors=unicode_errors)

        labels = find_labels_recursive(label)
        assert len(labels) >= 4, "Expected at least 4 Labels for table cells"

        # All labels should have the specified unicode_errors
        for lbl in labels:
            assert lbl.unicode_errors == unicode_errors, \
                f"Expected unicode_errors={unicode_errors}, got {lbl.unicode_errors}"

    @pytest.mark.property
    @given(unicode_errors_strategy, unicode_errors_strategy)
    # 3 errors × 3 errors = 9 combinations
    # Use 9 examples for full coverage
    @settings(max_examples=9, deadline=None)
    def test_unicode_errors_change_triggers_rebuild(self, errors1, errors2):
        """Changing unicode_errors triggers widget rebuild with new value.

        """
        assume(errors1 != errors2)

        label = MarkdownLabel(text='Hello World', unicode_errors=errors1)

        # Collect widget IDs before change
        ids_before = collect_widget_ids(label)

        # Verify initial unicode_errors
        labels = find_labels_recursive(label)
        for lbl in labels:
            assert lbl.unicode_errors == errors1

        # Change unicode_errors
        label.unicode_errors = errors2
        label.force_rebuild()  # Force immediate rebuild for test

        # Verify rebuild occurred
        ids_after = collect_widget_ids(label)
        assert ids_before != ids_after, "Widget tree should rebuild for unicode_errors changes"

        # Verify new unicode_errors
        labels = find_labels_recursive(label)
        for lbl in labels:
            assert lbl.unicode_errors == errors2, \
                f"After change, expected unicode_errors={errors2}, got {lbl.unicode_errors}"

    @pytest.mark.unit
    def test_default_unicode_errors_is_replace(self):
        """Default unicode_errors is 'replace'."""
        label = MarkdownLabel(text='Hello World')

        assert label.unicode_errors == 'replace', \
            f"Default unicode_errors should be 'replace', got {label.unicode_errors}"


# *For any* Markdown text and any strip boolean value, all internal Labels
# SHALL have `strip` set to that value.

class TestStripForwarding:
    """Property tests for strip forwarding."""

    @pytest.mark.property
    @given(st.booleans())
    # Boolean strategy: 2 examples (True/False coverage)
    @settings(max_examples=2, deadline=None)
    def test_strip_stored_correctly(self, strip_value):
        """strip value is stored correctly on MarkdownLabel."""
        label = MarkdownLabel(text='Hello World', strip=strip_value)

        assert label.strip == strip_value, \
            f"Expected strip={strip_value}, got {label.strip}"

    @pytest.mark.property
    @given(st.booleans())
    # Boolean strategy: 2 examples (True/False coverage)
    @settings(max_examples=2, deadline=None)
    def test_strip_applied_to_paragraph(self, strip_value):
        """strip is applied to paragraph Labels."""
        label = MarkdownLabel(text='Hello World', strip=strip_value)

        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"

        # All labels should have the specified strip value
        for lbl in labels:
            assert lbl.strip == strip_value, \
                f"Expected strip={strip_value}, got {lbl.strip}"

    @pytest.mark.property
    @given(st.booleans())
    # Boolean strategy: 2 examples (True/False coverage)
    @settings(max_examples=2, deadline=None)
    def test_strip_applied_to_heading(self, strip_value):
        """strip is applied to heading Labels."""
        label = MarkdownLabel(text='# Heading', strip=strip_value)

        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"

        # All labels should have the specified strip value
        for lbl in labels:
            assert lbl.strip == strip_value, \
                f"Expected strip={strip_value}, got {lbl.strip}"

    @pytest.mark.property
    @given(st.booleans())
    # Boolean strategy: 2 examples (True/False coverage)
    @settings(max_examples=2, deadline=None)
    def test_strip_applied_to_code_block(self, strip_value):
        """strip is applied to code block Labels."""
        markdown = '```python\nprint("hello")\n```'
        label = MarkdownLabel(text=markdown, strip=strip_value)

        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label for code block"

        # All labels should have the specified strip value
        for lbl in labels:
            assert lbl.strip == strip_value, \
                f"Expected strip={strip_value}, got {lbl.strip}"

    @pytest.mark.property
    @given(st.booleans())
    # Boolean strategy: 2 examples (True/False coverage)
    @settings(max_examples=2, deadline=None)
    def test_strip_applied_to_list_items(self, strip_value):
        """strip is applied to list item Labels."""
        markdown = '- Item 1\n- Item 2'
        label = MarkdownLabel(text=markdown, strip=strip_value)

        labels = find_labels_recursive(label)
        assert len(labels) >= 2, "Expected at least 2 Labels for list items"

        # All labels should have the specified strip value
        for lbl in labels:
            assert lbl.strip == strip_value, \
                f"Expected strip={strip_value}, got {lbl.strip}"

    @pytest.mark.property
    @given(st.booleans())
    # Boolean strategy: 2 examples (True/False coverage)
    @settings(max_examples=2, deadline=None)
    def test_strip_applied_to_table_cells(self, strip_value):
        """strip is applied to table cell Labels."""
        markdown = '| A | B |\n| --- | --- |\n| 1 | 2 |'
        label = MarkdownLabel(text=markdown, strip=strip_value)

        labels = find_labels_recursive(label)
        assert len(labels) >= 4, "Expected at least 4 Labels for table cells"

        # All labels should have the specified strip value
        for lbl in labels:
            assert lbl.strip == strip_value, \
                f"Expected strip={strip_value}, got {lbl.strip}"

    @pytest.mark.property
    @given(st.booleans(), st.booleans())
    # 2 × 2 = 4 combinations
    # Use 4 examples for full coverage
    @settings(max_examples=4, deadline=None)
    def test_strip_change_triggers_rebuild(self, strip1, strip2):
        """Changing strip triggers widget rebuild with new value.

        """
        assume(strip1 != strip2)

        label = MarkdownLabel(text='Hello World', strip=strip1)

        # Collect widget IDs before change
        ids_before = collect_widget_ids(label)

        # Verify initial strip
        labels = find_labels_recursive(label)
        for lbl in labels:
            assert lbl.strip == strip1

        # Change strip
        label.strip = strip2
        label.force_rebuild()  # Force immediate rebuild for test

        # Verify rebuild occurred
        ids_after = collect_widget_ids(label)
        assert ids_before != ids_after, "Widget tree should rebuild for strip changes"

        # Verify new strip
        labels = find_labels_recursive(label)
        for lbl in labels:
            assert lbl.strip == strip2, \
                f"After change, expected strip={strip2}, got {lbl.strip}"

    @pytest.mark.unit
    def test_default_strip_is_false(self):
        """Default strip is False."""
        label = MarkdownLabel(text='Hello World')

        assert label.strip is False, \
            f"Default strip should be False, got {label.strip}"
