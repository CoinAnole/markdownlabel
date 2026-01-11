"""
Property-based tests for text shortening property forwarding.

This module contains tests for label compatibility features including text shortening
property forwarding (shorten, shorten_from, split_str, max_lines, ellipsis_options)
to all child Labels across different markdown structures (paragraphs, headings, lists, tables).

These tests verify that MarkdownLabel correctly implements text shortening properties
while maintaining proper Markdown rendering.
"""

import pytest
from hypothesis import given, strategies as st, settings

from kivy_garden.markdownlabel import MarkdownLabel
from .test_utils import (
    collect_widget_ids,
    find_labels_recursive,
    st_rgba_color
)


# *For any* MarkdownLabel with shortening properties (shorten, shorten_from, split_str,
# max_lines, ellipsis_options), all child Labels SHALL have the same property values.

class TestShorteningPropertyForwarding:
    """Property tests for shortening property forwarding."""

    @pytest.mark.property
    @given(st.booleans())
    # Boolean strategy: 2 examples (True/False coverage)
    @settings(max_examples=2, deadline=None)
    def test_shorten_forwarded_to_paragraph(self, shorten_value):
        """shorten property is forwarded to paragraph Labels."""
        label = MarkdownLabel(text='Hello World', shorten=shorten_value)

        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"

        for lbl in labels:
            assert lbl.shorten == shorten_value, \
                f"Expected shorten={shorten_value}, got {lbl.shorten}"

    @pytest.mark.property
    @given(st.booleans())
    # Boolean strategy: 2 examples (True/False coverage)
    @settings(max_examples=2, deadline=None)
    def test_shorten_forwarded_to_heading(self, shorten_value):
        """shorten property is forwarded to heading Labels."""
        label = MarkdownLabel(text='# Heading', shorten=shorten_value)

        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"

        for lbl in labels:
            assert lbl.shorten == shorten_value, \
                f"Expected shorten={shorten_value}, got {lbl.shorten}"

    @pytest.mark.property
    @given(st.booleans())
    # Boolean strategy: 2 examples (True/False coverage)
    @settings(max_examples=2, deadline=None)
    def test_shorten_forwarded_to_list_items(self, shorten_value):
        """shorten property is forwarded to list item Labels."""
        markdown = '- Item 1\n- Item 2'
        label = MarkdownLabel(text=markdown, shorten=shorten_value)

        labels = find_labels_recursive(label)
        assert len(labels) >= 2, "Expected at least 2 Labels for list items"

        for lbl in labels:
            assert lbl.shorten == shorten_value, \
                f"Expected shorten={shorten_value}, got {lbl.shorten}"

    @pytest.mark.property
    @given(st.booleans())
    # Boolean strategy: 2 examples (True/False coverage)
    @settings(max_examples=2, deadline=None)
    def test_shorten_forwarded_to_table_cells(self, shorten_value):
        """shorten property is forwarded to table cell Labels."""
        markdown = '| A | B |\n| --- | --- |\n| 1 | 2 |'
        label = MarkdownLabel(text=markdown, shorten=shorten_value)

        labels = find_labels_recursive(label)
        assert len(labels) >= 4, "Expected at least 4 Labels for table cells"

        for lbl in labels:
            assert lbl.shorten == shorten_value, \
                f"Expected shorten={shorten_value}, got {lbl.shorten}"

    @pytest.mark.parametrize('shorten_from_value', ['left', 'center', 'right'])
    def test_shorten_from_forwarded_to_paragraph(self, shorten_from_value):
        """shorten_from property is forwarded to paragraph Labels."""
        label = MarkdownLabel(text='Hello World', shorten_from=shorten_from_value)

        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"

        for lbl in labels:
            assert lbl.shorten_from == shorten_from_value, \
                f"Expected shorten_from={shorten_from_value}, got {lbl.shorten_from}"

    @pytest.mark.parametrize('shorten_from_value', ['left', 'center', 'right'])
    def test_shorten_from_forwarded_to_heading(self, shorten_from_value):
        """shorten_from property is forwarded to heading Labels."""
        label = MarkdownLabel(text='# Heading', shorten_from=shorten_from_value)

        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"

        for lbl in labels:
            assert lbl.shorten_from == shorten_from_value, \
                f"Expected shorten_from={shorten_from_value}, got {lbl.shorten_from}"

    @pytest.mark.parametrize('shorten_from_value', ['left', 'center', 'right'])
    def test_shorten_from_forwarded_to_list_items(self, shorten_from_value):
        """shorten_from property is forwarded to list item Labels."""
        markdown = '- Item 1\n- Item 2'
        label = MarkdownLabel(text=markdown, shorten_from=shorten_from_value)

        labels = find_labels_recursive(label)
        assert len(labels) >= 2, "Expected at least 2 Labels for list items"

        for lbl in labels:
            assert lbl.shorten_from == shorten_from_value, \
                f"Expected shorten_from={shorten_from_value}, got {lbl.shorten_from}"

    @pytest.mark.property
    @given(st.text(min_size=0, max_size=5, alphabet='abc '))
    # Complex strategy: 30 examples (adequate coverage)
    @settings(max_examples=30, deadline=None)
    def test_split_str_forwarded_to_paragraph(self, split_str_value):
        """split_str property is forwarded to paragraph Labels."""
        label = MarkdownLabel(text='Hello World', split_str=split_str_value)

        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"

        for lbl in labels:
            assert lbl.split_str == split_str_value, \
                f"Expected split_str={split_str_value!r}, got {lbl.split_str!r}"

    @pytest.mark.property
    @given(st.text(min_size=0, max_size=5, alphabet='abc '))
    # Complex strategy: 30 examples (adequate coverage)
    @settings(max_examples=30, deadline=None)
    def test_split_str_forwarded_to_heading(self, split_str_value):
        """split_str property is forwarded to heading Labels."""
        label = MarkdownLabel(text='# Heading', split_str=split_str_value)

        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"

        for lbl in labels:
            assert lbl.split_str == split_str_value, \
                f"Expected split_str={split_str_value!r}, got {lbl.split_str!r}"

    @pytest.mark.property
    @given(st.integers(min_value=0, max_value=10))
    # Medium finite strategy: 11 examples (adequate finite coverage)
    @settings(max_examples=11, deadline=None)
    def test_max_lines_forwarded_to_paragraph(self, max_lines_value):
        """max_lines property is forwarded to paragraph Labels when non-zero."""
        label = MarkdownLabel(text='Hello World', max_lines=max_lines_value)

        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"

        for lbl in labels:
            if max_lines_value > 0:
                assert lbl.max_lines == max_lines_value, \
                    f"Expected max_lines={max_lines_value}, got {lbl.max_lines}"
            # When max_lines=0, it may not be set on child Labels (default behavior)

    @pytest.mark.property
    @given(st.integers(min_value=1, max_value=10))
    # Small finite strategy: 10 examples (input space size: 10)
    @settings(max_examples=10, deadline=None)
    def test_max_lines_forwarded_to_heading(self, max_lines_value):
        """max_lines property is forwarded to heading Labels when non-zero."""
        label = MarkdownLabel(text='# Heading', max_lines=max_lines_value)

        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"

        for lbl in labels:
            assert lbl.max_lines == max_lines_value, \
                f"Expected max_lines={max_lines_value}, got {lbl.max_lines}"

    @pytest.mark.property
    @given(st.integers(min_value=1, max_value=10))
    # Small finite strategy: 10 examples (input space size: 10)
    @settings(max_examples=10, deadline=None)
    def test_max_lines_forwarded_to_list_items(self, max_lines_value):
        """max_lines property is forwarded to list item Labels when non-zero."""
        markdown = '- Item 1\n- Item 2'
        label = MarkdownLabel(text=markdown, max_lines=max_lines_value)

        labels = find_labels_recursive(label)
        assert len(labels) >= 2, "Expected at least 2 Labels for list items"

        for lbl in labels:
            assert lbl.max_lines == max_lines_value, \
                f"Expected max_lines={max_lines_value}, got {lbl.max_lines}"

    @pytest.mark.property
    @given(st.fixed_dictionaries({
        'markup_color': st_rgba_color()
    }))
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_ellipsis_options_forwarded_to_paragraph(self, ellipsis_opts):
        """ellipsis_options property is forwarded to paragraph Labels."""
        label = MarkdownLabel(text='Hello World', ellipsis_options=ellipsis_opts)

        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"

        for lbl in labels:
            assert lbl.ellipsis_options == ellipsis_opts, \
                f"Expected ellipsis_options={ellipsis_opts}, got {lbl.ellipsis_options}"

    @pytest.mark.property
    @given(st.fixed_dictionaries({
        'markup_color': st_rgba_color()
    }))
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_ellipsis_options_forwarded_to_heading(self, ellipsis_opts):
        """ellipsis_options property is forwarded to heading Labels."""
        label = MarkdownLabel(text='# Heading', ellipsis_options=ellipsis_opts)

        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"

        for lbl in labels:
            assert lbl.ellipsis_options == ellipsis_opts, \
                f"Expected ellipsis_options={ellipsis_opts}, got {lbl.ellipsis_options}"

    @pytest.mark.property
    @given(st.fixed_dictionaries({
        'markup_color': st_rgba_color()
    }))
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_ellipsis_options_forwarded_to_list_items(self, ellipsis_opts):
        """ellipsis_options property is forwarded to list item Labels."""
        markdown = '- Item 1\n- Item 2'
        label = MarkdownLabel(text=markdown, ellipsis_options=ellipsis_opts)

        labels = find_labels_recursive(label)
        assert len(labels) >= 2, "Expected at least 2 Labels for list items"

        for lbl in labels:
            assert lbl.ellipsis_options == ellipsis_opts, \
                f"Expected ellipsis_options={ellipsis_opts}, got {lbl.ellipsis_options}"

    @pytest.mark.property
    @given(st.fixed_dictionaries({
        'markup_color': st_rgba_color()
    }))
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_ellipsis_options_forwarded_to_table_cells(self, ellipsis_opts):
        """ellipsis_options property is forwarded to table cell Labels."""
        markdown = '| A | B |\n| --- | --- |\n| 1 | 2 |'
        label = MarkdownLabel(text=markdown, ellipsis_options=ellipsis_opts)

        labels = find_labels_recursive(label)
        assert len(labels) >= 4, "Expected at least 4 Labels for table cells"

        for lbl in labels:
            assert lbl.ellipsis_options == ellipsis_opts, \
                f"Expected ellipsis_options={ellipsis_opts}, got {lbl.ellipsis_options}"

    def test_empty_ellipsis_options_forwards_default_value(self):
        """Empty ellipsis_options dict results in default behavior."""
        label = MarkdownLabel(text='Hello World', ellipsis_options={})

        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"

        # Empty dict should result in default empty dict on child Labels
        for lbl in labels:
            assert lbl.ellipsis_options == {}, \
                f"Expected empty ellipsis_options, got {lbl.ellipsis_options}"

    @pytest.mark.property
    @given(st.booleans(), st.sampled_from(['left', 'center', 'right']),
           st.text(min_size=0, max_size=3, alphabet='ab '),
           st.integers(min_value=1, max_value=5))
    # Mixed finite/complex strategy: 30 examples (30 finite combinations × 1 complex sample)
    @settings(max_examples=30, deadline=None)
    def test_all_shortening_properties_forwarded_together(
            self, shorten_val, shorten_from_val, split_str_val, max_lines_val):
        """All shortening properties are forwarded together to child Labels."""
        markdown = '''# Heading

Paragraph text

- List item 1
- List item 2

| A | B |
| --- | --- |
| 1 | 2 |
'''
        label = MarkdownLabel(
            text=markdown,
            shorten=shorten_val,
            shorten_from=shorten_from_val,
            split_str=split_str_val,
            max_lines=max_lines_val
        )

        labels = find_labels_recursive(label)
        assert len(labels) >= 5, "Expected at least 5 Labels for various structures"

        for lbl in labels:
            assert lbl.shorten == shorten_val, \
                f"Expected shorten={shorten_val}, got {lbl.shorten}"
            assert lbl.shorten_from == shorten_from_val, \
                f"Expected shorten_from={shorten_from_val}, got {lbl.shorten_from}"
            assert lbl.split_str == split_str_val, \
                f"Expected split_str={split_str_val!r}, got {lbl.split_str!r}"
            assert lbl.max_lines == max_lines_val, \
                f"Expected max_lines={max_lines_val}, got {lbl.max_lines}"

    @pytest.mark.property
    @given(st.booleans(), st.booleans())
    # Combination strategy: 2 examples (combination coverage)
    @settings(max_examples=2, deadline=None)
    def test_shorten_change_preserves_widget_tree(self, shorten1, shorten2):
        """Changing shorten updates widgets in-place (no rebuild)."""
        from hypothesis import assume
        assume(shorten1 != shorten2)

        label = MarkdownLabel(text='Hello World', shorten=shorten1)

        # Verify initial value
        labels = find_labels_recursive(label)
        for lbl in labels:
            assert lbl.shorten == shorten1

        # Collect widget IDs before change
        ids_before = collect_widget_ids(label)

        # Change shorten
        label.shorten = shorten2

        # Verify no rebuild occurred (style-only change)
        ids_after = collect_widget_ids(label)
        assert ids_before == ids_after, \
            "Expected existing widgets to be preserved (no rebuild) when shorten property changed"

        # Verify new value
        labels = find_labels_recursive(label)
        for lbl in labels:
            assert lbl.shorten == shorten2, \
                f"After change, expected shorten={shorten2}, got {lbl.shorten}"
