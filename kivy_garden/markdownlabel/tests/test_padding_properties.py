"""
Property-based tests for MarkdownLabel padding properties.

Tests verify that padding-related properties (padding, text_padding, label_padding)
work correctly and are properly forwarded to child widgets.
"""

import pytest
from hypothesis import given, settings, assume

from kivy_garden.markdownlabel import MarkdownLabel
from .test_utils import (
    text_padding_strategy,
    find_labels_recursive,
    padding_equal,
    padding_single,
    padding_two,
    padding_four,
    collect_widget_ids
)


# *For any* MarkdownLabel with padding set to value P, the padding SHALL be
# normalized and stored correctly according to Kivy's VariableListProperty rules.

class TestPaddingApplication:
    """Property tests for padding application."""

    @pytest.mark.property
    @given(padding_single)
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_single_padding_applied_uniformly(self, padding_value):
        """Single padding value is applied uniformly to all sides."""
        label = MarkdownLabel(text='Hello World', padding=padding_value)

        # VariableListProperty normalizes single value to [v, v, v, v]
        expected = [padding_value, padding_value, padding_value, padding_value]

        assert len(label.padding) == 4, \
            f"Expected 4-element padding, got {len(label.padding)}"

        for i, (actual, exp) in enumerate(zip(label.padding, expected)):
            assert abs(actual - exp) < 0.001, \
                f"Padding[{i}]: expected {exp}, got {actual}"

    @pytest.mark.property
    @given(padding_two)
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_two_element_padding_applied_to_axes(self, padding_values):
        """Two-element padding [horizontal, vertical] is applied to appropriate axes."""
        label = MarkdownLabel(text='Hello World', padding=padding_values)

        # VariableListProperty normalizes [h, v] to [h, v, h, v]
        h, v = padding_values
        expected = [h, v, h, v]

        assert len(label.padding) == 4, \
            f"Expected 4-element padding, got {len(label.padding)}"

        for i, (actual, exp) in enumerate(zip(label.padding, expected)):
            assert abs(actual - exp) < 0.001, \
                f"Padding[{i}]: expected {exp}, got {actual}"

    @pytest.mark.property
    @given(padding_four)
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_four_element_padding_applied_directly(self, padding_values):
        """Four-element padding [left, top, right, bottom] is applied directly."""
        label = MarkdownLabel(text='Hello World', padding=padding_values)

        assert len(label.padding) == 4, \
            f"Expected 4-element padding, got {len(label.padding)}"

        for i, (actual, exp) in enumerate(zip(label.padding, padding_values)):
            assert abs(actual - exp) < 0.001, \
                f"Padding[{i}]: expected {exp}, got {actual}"

    @pytest.mark.property
    @given(padding_four)
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_padding_property_stored_correctly(self, padding_values):
        """padding property value is stored correctly on MarkdownLabel."""
        label = MarkdownLabel(text='Hello', padding=padding_values)

        assert len(label.padding) == 4, \
            f"Expected 4-element padding, got {len(label.padding)}"

        for i, (actual, exp) in enumerate(zip(label.padding, padding_values)):
            assert abs(actual - exp) < 0.001, \
                f"Padding[{i}]: expected {exp}, got {actual}"

    @pytest.mark.property
    @given(padding_four, padding_four)
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_padding_change_triggers_rebuild(self, padding1, padding2):
        """Changing padding triggers rebuild and updates the container padding."""
        assume(padding1 != padding2)

        label = MarkdownLabel(text='Hello World', padding=padding1)

        # Collect widget IDs before change
        ids_before = collect_widget_ids(label)

        # Verify initial padding
        for i, (actual, exp) in enumerate(zip(label.padding, padding1)):
            assert abs(actual - exp) < 0.001

        # Change padding (structure property - triggers rebuild)
        label.padding = padding2
        label.force_rebuild()  # Force immediate rebuild for test

        # Verify rebuild occurred (structure property)
        ids_after = collect_widget_ids(label)
        assert ids_before != ids_after, "Widget tree should rebuild for padding changes"

        # Verify new padding
        for i, (actual, exp) in enumerate(zip(label.padding, padding2)):
            assert abs(actual - exp) < 0.001, \
                f"After change, padding[{i}]: expected {exp}, got {actual}"

    @pytest.mark.unit
    def test_default_padding_is_zero(self):
        """Default padding is [0, 0, 0, 0]."""
        label = MarkdownLabel(text='Hello World')

        expected = [0, 0, 0, 0]
        assert len(label.padding) == 4, \
            f"Expected 4-element padding, got {len(label.padding)}"

        for i, (actual, exp) in enumerate(zip(label.padding, expected)):
            assert abs(actual - exp) < 0.001, \
                f"Default padding[{i}]: expected {exp}, got {actual}"


# *For any* MarkdownLabel with `text_padding` set to value P, all child Labels that display
# text content SHALL have their `padding` property equal to P.

class TestTextPaddingForwarding:
    """Property tests for text_padding forwarding to child Labels."""

    @pytest.mark.property
    @given(text_padding_strategy)
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_text_padding_applied_to_paragraph(self, padding):
        """text_padding is applied to paragraph Labels."""
        label = MarkdownLabel(text='Hello World', text_padding=padding)

        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"

        # All labels should have the specified padding
        for lbl in labels:
            assert padding_equal(list(lbl.padding), padding), \
                f"Expected padding={padding}, got {list(lbl.padding)}"

    @pytest.mark.property
    @given(text_padding_strategy)
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_text_padding_applied_to_heading(self, padding):
        """text_padding is applied to heading Labels."""
        label = MarkdownLabel(text='# Heading', text_padding=padding)

        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"

        # All labels should have the specified padding
        for lbl in labels:
            assert padding_equal(list(lbl.padding), padding), \
                f"Expected padding={padding}, got {list(lbl.padding)}"

    @pytest.mark.property
    @given(text_padding_strategy)
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_text_padding_applied_to_list_items(self, padding):
        """text_padding is applied to list item Labels."""
        markdown = '- Item 1\n- Item 2'
        label = MarkdownLabel(text=markdown, text_padding=padding)

        labels = find_labels_recursive(label)
        assert len(labels) >= 2, "Expected at least 2 Labels for list items"

        # All labels should have the specified padding
        for lbl in labels:
            assert padding_equal(list(lbl.padding), padding), \
                f"Expected padding={padding}, got {list(lbl.padding)}"

    @pytest.mark.property
    @given(text_padding_strategy)
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_text_padding_applied_to_table_cells(self, padding):
        """text_padding is applied to table cell Labels."""
        markdown = '| A | B |\n| --- | --- |\n| 1 | 2 |'
        label = MarkdownLabel(text=markdown, text_padding=padding)

        labels = find_labels_recursive(label)
        assert len(labels) >= 4, "Expected at least 4 Labels for table cells"

        # All labels should have the specified padding
        for lbl in labels:
            assert padding_equal(list(lbl.padding), padding), \
                f"Expected padding={padding}, got {list(lbl.padding)}"

    @pytest.mark.property
    @given(text_padding_strategy)
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_text_padding_applied_to_nested_structures(self, padding):
        """text_padding is applied to Labels in nested structures (lists, tables, block quotes)."""
        markdown = '''
# Heading

Regular paragraph

- List item 1
  - Nested item
- List item 2

> Block quote text

| Header 1 | Header 2 |
| --- | --- |
| Cell 1 | Cell 2 |
'''
        label = MarkdownLabel(text=markdown, text_padding=padding)

        labels = find_labels_recursive(label)
        assert len(labels) >= 5, "Expected at least 5 Labels for various structures"

        # All labels should have the specified padding
        for lbl in labels:
            assert padding_equal(list(lbl.padding), padding), \
                f"Expected padding={padding}, got {list(lbl.padding)}"

    @pytest.mark.property
    @given(text_padding_strategy, text_padding_strategy)
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_text_padding_change_updates_in_place(self, padding1, padding2):
        """Changing text_padding updates child Labels in place without rebuild."""
        assume(not padding_equal(padding1, padding2))

        label = MarkdownLabel(text='Hello World', text_padding=padding1)

        # Collect widget IDs before change
        ids_before = collect_widget_ids(label, exclude_root=True)

        # Verify initial padding
        labels = find_labels_recursive(label)
        for lbl in labels:
            assert padding_equal(list(lbl.padding), padding1)

        # Change text_padding
        label.text_padding = padding2

        # Verify NO rebuild occurred (style-only property)
        ids_after = collect_widget_ids(label, exclude_root=True)
        assert ids_before == ids_after, "Widget tree should NOT rebuild for text_padding changes"

        # Verify new padding applied in place
        labels = find_labels_recursive(label)
        for lbl in labels:
            assert padding_equal(list(lbl.padding), padding2), \
                f"After change, expected padding={padding2}, got {list(lbl.padding)}"

    @pytest.mark.unit
    def test_default_padding_is_zero_for_all_labels(self):
        """Default padding is [0, 0, 0, 0] for all labels."""
        label = MarkdownLabel(text='Hello World')

        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"

        # All labels should have default padding of [0, 0, 0, 0]
        for lbl in labels:
            assert padding_equal(list(lbl.padding), [0, 0, 0, 0]), \
                f"Expected default padding=[0, 0, 0, 0], got {list(lbl.padding)}"


# *For any* MarkdownLabel, when `text_padding` is changed from value A to value B, all child Labels
# SHALL be updated to reflect the new padding value B.

class TestTextPaddingDynamicUpdates:
    """Property tests for text_padding dynamic updates."""

    @pytest.mark.property
    @given(text_padding_strategy, text_padding_strategy)
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_text_padding_update_updates_in_place(self, initial_padding, new_padding):
        """Updating text_padding on paragraph updates child Labels in place without rebuild."""
        assume(not padding_equal(initial_padding, new_padding))

        label = MarkdownLabel(text='Hello World', text_padding=initial_padding)

        # Collect widget IDs before change
        ids_before = collect_widget_ids(label, exclude_root=True)

        # Verify initial padding
        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        for lbl in labels:
            assert padding_equal(list(lbl.padding), initial_padding)

        # Update padding
        label.text_padding = new_padding

        # Verify NO rebuild occurred (style-only property)
        ids_after = collect_widget_ids(label, exclude_root=True)
        assert ids_before == ids_after, "Widget tree should NOT rebuild for text_padding changes"

        # Verify all labels have new padding
        labels = find_labels_recursive(label)
        for lbl in labels:
            assert padding_equal(list(lbl.padding), new_padding), \
                f"After update, expected padding={new_padding}, got {list(lbl.padding)}"

    @pytest.mark.property
    @given(text_padding_strategy, text_padding_strategy)
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_text_padding_update_updates_in_place_complex_content(self, initial_padding, new_padding):
        """Updating text_padding on complex content updates child Labels in place without rebuild."""
        assume(not padding_equal(initial_padding, new_padding))

        markdown = '''
# Title

Paragraph with text.

- List item 1
- List item 2

| A | B |
| --- | --- |
| 1 | 2 |
'''

        label = MarkdownLabel(text=markdown, text_padding=initial_padding)

        # Collect widget IDs before change
        ids_before = collect_widget_ids(label, exclude_root=True)

        # Verify initial padding
        labels = find_labels_recursive(label)
        assert len(labels) >= 5, "Expected at least 5 Labels"
        for lbl in labels:
            assert padding_equal(list(lbl.padding), initial_padding)

        # Update padding
        label.text_padding = new_padding

        # Verify NO rebuild occurred (style-only property)
        ids_after = collect_widget_ids(label, exclude_root=True)
        assert ids_before == ids_after, "Widget tree should NOT rebuild for text_padding changes"

        # Verify all labels have new padding
        labels = find_labels_recursive(label)
        for lbl in labels:
            assert padding_equal(list(lbl.padding), new_padding), \
                f"After update, expected padding={new_padding}, got {list(lbl.padding)}"

    @pytest.mark.parametrize("num_updates", [1, 2, 3, 4, 5])
    def test_multiple_text_padding_updates(self, num_updates):
        """Multiple text_padding updates all work correctly."""
        label = MarkdownLabel(text='Hello World')

        for i in range(num_updates):
            new_padding = [i * 5.0, i * 5.0, i * 5.0, i * 5.0]
            label.text_padding = new_padding

            # Verify all labels have the current padding
            labels = find_labels_recursive(label)
            for lbl in labels:
                assert padding_equal(list(lbl.padding), new_padding), \
                    f"Update {i}: expected padding={new_padding}, got {list(lbl.padding)}"


# *For any* MarkdownLabel containing nested structures (lists, tables, block quotes), all text-containing
# Labels within those structures SHALL have the `padding` property applied without
# breaking the layout structure.

class TestPaddingWithNestedStructures:
    """Property tests for padding with nested structures."""

    @pytest.mark.property
    @given(text_padding_strategy)
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_padding_in_nested_lists(self, padding):
        """padding is applied to Labels in nested lists without breaking structure."""
        markdown = '''
- Top level item 1
  - Nested item 1.1
  - Nested item 1.2
    - Deep nested item 1.2.1
- Top level item 2
  - Nested item 2.1
'''

        label = MarkdownLabel(text=markdown, text_padding=padding)

        # Should have multiple children for the nested list structure
        assert len(label.children) >= 1, "Expected at least one child for list structure"

        # All Labels should have the specified padding
        labels = find_labels_recursive(label)
        assert len(labels) >= 5, "Expected at least 5 Labels for nested list items"

        for lbl in labels:
            assert padding_equal(list(lbl.padding), padding), \
                f"Expected padding={padding}, got {list(lbl.padding)}"

    @pytest.mark.property
    @given(text_padding_strategy)
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_padding_in_nested_quotes(self, padding):
        """padding is applied to Labels in nested block quotes without breaking structure."""
        markdown = '''
> This is a quote
>
> > This is a nested quote
> > with multiple lines
>
> Back to first level quote
'''

        label = MarkdownLabel(text=markdown, text_padding=padding)

        # Should have children for the quote structure
        assert len(label.children) >= 1, "Expected at least one child for quote structure"

        # All Labels should have the specified padding
        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least 1 Label for quote content"

        for lbl in labels:
            assert padding_equal(list(lbl.padding), padding), \
                f"Expected padding={padding}, got {list(lbl.padding)}"

    @pytest.mark.property
    @given(text_padding_strategy)
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_padding_in_complex_table(self, padding):
        """padding is applied to Labels in complex tables without breaking structure."""
        markdown = '''
| Header 1 | Header 2 | Header 3 |
| :--- | :---: | ---: |
| Left aligned | Center aligned | Right aligned |
| Cell with **bold** | Cell with *italic* | Cell with `code` |
| Multi word cell | Another cell | Final cell |
'''

        label = MarkdownLabel(text=markdown, text_padding=padding)

        # Should have children for the table structure
        assert len(label.children) >= 1, "Expected at least one child for table structure"

        # All Labels should have the specified padding
        labels = find_labels_recursive(label)
        assert len(labels) >= 9, "Expected at least 9 Labels for table cells"

        for lbl in labels:
            assert padding_equal(list(lbl.padding), padding), \
                f"Expected padding={padding}, got {list(lbl.padding)}"

    @pytest.mark.property
    @given(text_padding_strategy)
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_padding_in_mixed_nested_structures(self, padding):
        """padding is applied to Labels in mixed nested structures without breaking layout."""
        markdown = '''
# Main Heading

Regular paragraph text.

- List item with text
  - Nested list item

  > Quote inside list

  | Table | In List |
  | --- | --- |
  | Cell 1 | Cell 2 |

> Block quote with content
>
> - List inside quote
> - Another item
>
> > Nested quote

Final paragraph.
'''

        label = MarkdownLabel(text=markdown, text_padding=padding)

        # Should have multiple children for the complex structure
        assert len(label.children) >= 3, "Expected at least 3 children for complex structure"

        # All Labels should have the specified padding
        labels = find_labels_recursive(label)
        assert len(labels) >= 8, "Expected at least 8 Labels for mixed content"

        for lbl in labels:
            assert padding_equal(list(lbl.padding), padding), \
                f"Expected padding={padding}, got {list(lbl.padding)}"

    @pytest.mark.property
    @given(text_padding_strategy)
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_padding_preserves_widget_hierarchy(self, padding):
        """padding application preserves the widget hierarchy structure."""
        markdown = '''
- Item 1
  - Nested item
- Item 2
'''

        label = MarkdownLabel(text=markdown, text_padding=padding)

        # Verify the basic structure is preserved
        assert len(label.children) >= 1, "Expected at least one child for list"

        # Verify padding is applied but structure is intact
        labels = find_labels_recursive(label)
        assert len(labels) >= 3, "Expected at least 3 Labels (2 items + 1 nested)"

        for lbl in labels:
            assert padding_equal(list(lbl.padding), padding), \
                f"Expected padding={padding}, got {list(lbl.padding)}"
            # Verify the label is still properly embedded in the widget tree
            assert lbl.parent is not None, "Label should have a parent widget"


# *For any* MarkdownLabel with padding set to value P, the BoxLayout container (self)
# SHALL have padding P, and child Label widgets SHALL NOT have their padding affected by this property.

class TestPaddingAppliesToContainer:
    """Property tests for padding applies to container."""

    @pytest.mark.property
    @given(text_padding_strategy)
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_padding_applied_to_container_only(self, padding):
        """padding is applied to the MarkdownLabel container, not child Labels."""
        label = MarkdownLabel(text='Hello World', padding=padding)

        # Container should have the specified padding
        assert padding_equal(list(label.padding), padding), \
            f"Expected container padding={padding}, got {list(label.padding)}"

        # Child Labels should have default padding (not affected by container padding)
        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"

        for lbl in labels:
            # Child Labels should have default padding [0, 0, 0, 0], not container padding
            assert padding_equal(list(lbl.padding), [0, 0, 0, 0]), \
                f"Expected child Label padding=[0, 0, 0, 0], got {list(lbl.padding)}"

    @pytest.mark.property
    @given(text_padding_strategy, text_padding_strategy)
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_padding_and_text_padding_independent(self, container_padding, text_padding):
        """padding and text_padding work independently."""
        assume(not padding_equal(container_padding, text_padding))

        label = MarkdownLabel(
            text='Hello World',
            padding=container_padding,
            text_padding=text_padding
        )

        # Container should have container_padding
        assert padding_equal(list(label.padding), container_padding), \
            f"Expected container padding={container_padding}, got {list(label.padding)}"

        # Child Labels should have text_padding
        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"

        for lbl in labels:
            assert padding_equal(list(lbl.padding), text_padding), \
                f"Expected child Label padding={text_padding}, got {list(lbl.padding)}"

    @pytest.mark.property
    @given(text_padding_strategy)
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_padding_change_affects_container_only(self, new_padding):
        """Changing padding triggers rebuild but affects only the container, not child Labels."""
        label = MarkdownLabel(text='Hello World', padding=[0, 0, 0, 0])

        # Collect widget IDs before change
        ids_before = collect_widget_ids(label)

        # Get initial child Label padding (should be [0, 0, 0, 0] by default)
        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        initial_child_padding = list(labels[0].padding)

        # Change container padding (structure property - triggers rebuild)
        label.padding = new_padding
        label.force_rebuild()  # Force immediate rebuild for test

        # Verify rebuild occurred (structure property)
        ids_after = collect_widget_ids(label)
        assert ids_before != ids_after, "Widget tree should rebuild for padding changes"

        # Container should have new padding
        assert padding_equal(list(label.padding), new_padding), \
            f"Expected container padding={new_padding}, got {list(label.padding)}"

        # Child Labels should have default padding (not affected by container padding)
        labels = find_labels_recursive(label)
        for lbl in labels:
            assert padding_equal(list(lbl.padding), [0, 0, 0, 0]), \
                f"Expected child Label padding=[0, 0, 0, 0], got {list(lbl.padding)}"


# *For any* value V assigned to label_padding, text_padding SHALL equal V, and vice versa.

class TestLabelPaddingAliasSynchronization:
    """Property tests for label_padding alias synchronization."""

    @pytest.mark.property
    @given(text_padding_strategy)
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_label_padding_setter_updates_text_padding(self, padding):
        """Setting label_padding updates text_padding."""
        label = MarkdownLabel(text='Hello World')

        # Set label_padding
        label.label_padding = padding

        # text_padding should be updated
        assert padding_equal(list(label.text_padding), padding), \
            f"Expected text_padding={padding}, got {list(label.text_padding)}"

    @pytest.mark.property
    @given(text_padding_strategy)
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_label_padding_getter_returns_text_padding(self, padding):
        """Getting label_padding returns text_padding value."""
        label = MarkdownLabel(text='Hello World', text_padding=padding)

        # label_padding should return text_padding value
        assert padding_equal(list(label.label_padding), padding), \
            f"Expected label_padding={padding}, got {list(label.label_padding)}"

    @pytest.mark.property
    @given(text_padding_strategy)
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_text_padding_setter_updates_label_padding(self, padding):
        """Setting text_padding updates label_padding."""
        label = MarkdownLabel(text='Hello World')

        # Set text_padding
        label.text_padding = padding

        # label_padding should be updated
        assert padding_equal(list(label.label_padding), padding), \
            f"Expected label_padding={padding}, got {list(label.label_padding)}"

    @pytest.mark.property
    @given(text_padding_strategy, text_padding_strategy)
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_bidirectional_synchronization(self, padding1, padding2):
        """label_padding and text_padding stay synchronized in both directions."""
        assume(not padding_equal(padding1, padding2))

        label = MarkdownLabel(text='Hello World')

        # Set via label_padding
        label.label_padding = padding1
        assert padding_equal(list(label.text_padding), padding1), \
            f"Expected text_padding={padding1} after setting label_padding"
        assert padding_equal(list(label.label_padding), padding1), \
            f"Expected label_padding={padding1} after setting label_padding"

        # Set via text_padding
        label.text_padding = padding2
        assert padding_equal(list(label.label_padding), padding2), \
            f"Expected label_padding={padding2} after setting text_padding"
        assert padding_equal(list(label.text_padding), padding2), \
            f"Expected text_padding={padding2} after setting text_padding"

    @pytest.mark.unit
    def test_default_values_synchronized(self):
        """Default values of label_padding and text_padding are synchronized."""
        label = MarkdownLabel(text='Hello World')

        # Both should have the same default value
        assert padding_equal(list(label.label_padding), list(label.text_padding)), \
            f"Expected label_padding={list(label.text_padding)}, got {list(label.label_padding)}"

        # Both should be [0, 0, 0, 0] by default
        assert padding_equal(list(label.label_padding), [0, 0, 0, 0]), \
            f"Expected default label_padding=[0, 0, 0, 0], got {list(label.label_padding)}"
        assert padding_equal(list(label.text_padding), [0, 0, 0, 0]), \
            f"Expected default text_padding=[0, 0, 0, 0], got {list(label.text_padding)}"
