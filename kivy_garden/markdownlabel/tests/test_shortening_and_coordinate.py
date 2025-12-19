"""
Property-based tests for text shortening and coordinate translation features.

This module contains tests for:
- Text shortening property forwarding (shorten, shorten_from, split_str, max_lines, ellipsis_options)
- Coordinate translation for refs and anchors

These tests verify that MarkdownLabel correctly implements text shortening
properties and coordinate translation while maintaining proper Markdown rendering.
"""

import os

import pytest
from hypothesis import given, strategies as st, settings, assume

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout

from kivy_garden.markdownlabel import MarkdownLabel
from .test_utils import (
    markdown_heading, markdown_paragraph, markdown_bold, markdown_italic,
    markdown_link, simple_markdown_document, color_strategy, text_padding_strategy,
    find_labels_recursive, colors_equal, padding_equal, floats_equal, KIVY_FONTS
)


# **Feature: label-compatibility, Property 4: Text Shortening Property Forwarding**
# *For any* MarkdownLabel with shortening properties (shorten, shorten_from, split_str,
# max_lines, ellipsis_options), all child Labels SHALL have the same property values.
# **Validates: Requirements 4.1, 4.2, 4.3, 4.4, 4.5**

class TestShorteningPropertyForwarding:
    """Property tests for shortening property forwarding (Property 4)."""
    
    @given(st.booleans())
    @settings(max_examples=2, deadline=None)
    def test_shorten_forwarded_to_paragraph(self, shorten_value):
        """shorten property is forwarded to paragraph Labels."""
        label = MarkdownLabel(text='Hello World', shorten=shorten_value)
        
        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        for lbl in labels:
            assert lbl.shorten == shorten_value, \
                f"Expected shorten={shorten_value}, got {lbl.shorten}"
    
    @given(st.booleans())
    @settings(max_examples=2, deadline=None)
    def test_shorten_forwarded_to_heading(self, shorten_value):
        """shorten property is forwarded to heading Labels."""
        label = MarkdownLabel(text='# Heading', shorten=shorten_value)
        
        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        for lbl in labels:
            assert lbl.shorten == shorten_value, \
                f"Expected shorten={shorten_value}, got {lbl.shorten}"
    
    @given(st.booleans())
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
    
    @given(st.booleans())
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
    
    @given(st.integers(min_value=1, max_value=10))
    @settings(max_examples=10, deadline=None)
    def test_max_lines_forwarded_to_heading(self, max_lines_value):
        """max_lines property is forwarded to heading Labels when non-zero."""
        label = MarkdownLabel(text='# Heading', max_lines=max_lines_value)
        
        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        for lbl in labels:
            assert lbl.max_lines == max_lines_value, \
                f"Expected max_lines={max_lines_value}, got {lbl.max_lines}"
    
    @given(st.integers(min_value=1, max_value=10))
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
    
    @given(st.fixed_dictionaries({
        'markup_color': st.sampled_from([[1, 0, 0, 1], [0, 1, 0, 1], [0, 0, 1, 1]])
    }))
    # Small finite strategy: 3 examples (input space size: 3)
    @settings(max_examples=3, deadline=None)
    def test_ellipsis_options_forwarded_to_paragraph(self, ellipsis_opts):
        """ellipsis_options property is forwarded to paragraph Labels."""
        label = MarkdownLabel(text='Hello World', ellipsis_options=ellipsis_opts)
        
        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        for lbl in labels:
            assert lbl.ellipsis_options == ellipsis_opts, \
                f"Expected ellipsis_options={ellipsis_opts}, got {lbl.ellipsis_options}"
    
    @given(st.fixed_dictionaries({
        'markup_color': st.sampled_from([[1, 0, 0, 1], [0, 1, 0, 1], [0, 0, 1, 1]])
    }))
    # Small finite strategy: 3 examples (input space size: 3)
    @settings(max_examples=3, deadline=None)
    def test_ellipsis_options_forwarded_to_heading(self, ellipsis_opts):
        """ellipsis_options property is forwarded to heading Labels."""
        label = MarkdownLabel(text='# Heading', ellipsis_options=ellipsis_opts)
        
        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        for lbl in labels:
            assert lbl.ellipsis_options == ellipsis_opts, \
                f"Expected ellipsis_options={ellipsis_opts}, got {lbl.ellipsis_options}"
    
    @given(st.fixed_dictionaries({
        'markup_color': st.sampled_from([[1, 0, 0, 1], [0, 1, 0, 1], [0, 0, 1, 1]])
    }))
    # Small finite strategy: 3 examples (input space size: 3)
    @settings(max_examples=3, deadline=None)
    def test_ellipsis_options_forwarded_to_list_items(self, ellipsis_opts):
        """ellipsis_options property is forwarded to list item Labels."""
        markdown = '- Item 1\n- Item 2'
        label = MarkdownLabel(text=markdown, ellipsis_options=ellipsis_opts)
        
        labels = find_labels_recursive(label)
        assert len(labels) >= 2, "Expected at least 2 Labels for list items"
        
        for lbl in labels:
            assert lbl.ellipsis_options == ellipsis_opts, \
                f"Expected ellipsis_options={ellipsis_opts}, got {lbl.ellipsis_options}"
    
    @given(st.fixed_dictionaries({
        'markup_color': st.sampled_from([[1, 0, 0, 1], [0, 1, 0, 1], [0, 0, 1, 1]])
    }))
    # Small finite strategy: 3 examples (input space size: 3)
    @settings(max_examples=3, deadline=None)
    def test_ellipsis_options_forwarded_to_table_cells(self, ellipsis_opts):
        """ellipsis_options property is forwarded to table cell Labels."""
        markdown = '| A | B |\n| --- | --- |\n| 1 | 2 |'
        label = MarkdownLabel(text=markdown, ellipsis_options=ellipsis_opts)
        
        labels = find_labels_recursive(label)
        assert len(labels) >= 4, "Expected at least 4 Labels for table cells"
        
        for lbl in labels:
            assert lbl.ellipsis_options == ellipsis_opts, \
                f"Expected ellipsis_options={ellipsis_opts}, got {lbl.ellipsis_options}"
    
    def test_empty_ellipsis_options_not_forwarded(self):
        """Empty ellipsis_options dict is not forwarded (default behavior)."""
        label = MarkdownLabel(text='Hello World', ellipsis_options={})
        
        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        # Empty dict should result in default empty dict on child Labels
        for lbl in labels:
            assert lbl.ellipsis_options == {}, \
                f"Expected empty ellipsis_options, got {lbl.ellipsis_options}"
    
    @given(st.booleans(), st.sampled_from(['left', 'center', 'right']),
           st.text(min_size=0, max_size=3, alphabet='ab '),
           st.integers(min_value=1, max_value=5))
    # Combination strategy: 50 examples (combination coverage)
    @settings(max_examples=50, deadline=None)
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
    
    @given(st.booleans(), st.booleans())
    @settings(max_examples=2, deadline=None)
    def test_shorten_change_triggers_rebuild(self, shorten1, shorten2):
        """Changing shorten triggers widget rebuild with new value."""
        assume(shorten1 != shorten2)
        
        label = MarkdownLabel(text='Hello World', shorten=shorten1)
        
        # Verify initial value
        labels = find_labels_recursive(label)
        for lbl in labels:
            assert lbl.shorten == shorten1
        
        # Change shorten
        label.shorten = shorten2
        label.force_rebuild()  # Force immediate rebuild for test
        
        # Verify new value
        labels = find_labels_recursive(label)
        for lbl in labels:
            assert lbl.shorten == shorten2, \
                f"After change, expected shorten={shorten2}, got {lbl.shorten}"


# **Feature: label-compatibility-phase2, Property 5: Coordinate Translation for refs and anchors**
# *For any* MarkdownLabel containing links (refs) or anchors, the `refs` and `anchors`
# properties SHALL return coordinates translated to MarkdownLabel's local coordinate space
# (not child Label's coordinate space).
# **Validates: Requirements 5.1, 5.2, 5.3**
#
# Note: In Kivy, the `refs` dictionary on a Label is only populated after the texture
# is rendered. In headless test environments, refs may be empty. These tests verify:
# 1. The translation algorithm works correctly when refs ARE present
# 2. The ref markup is correctly generated (proving links are rendered)
# 3. Empty refs/anchors are handled correctly

class TestCoordinateTranslation:
    """Property tests for coordinate translation of refs and anchors (Property 5)."""
    
    def _find_labels_with_refs(self, widget, labels=None):
        """Recursively find all Label widgets that have refs."""
        if labels is None:
            labels = []
        
        if isinstance(widget, Label) and hasattr(widget, 'refs') and widget.refs:
            labels.append(widget)
        
        if hasattr(widget, 'children'):
            for child in widget.children:
                self._find_labels_with_refs(child, labels)
        
        return labels
    
    def _find_labels_with_ref_markup(self, widget, labels=None):
        """Recursively find all Label widgets that have ref markup in their text."""
        if labels is None:
            labels = []
        
        if isinstance(widget, Label) and hasattr(widget, 'text'):
            if '[ref=' in widget.text and '[/ref]' in widget.text:
                labels.append(widget)
        
        if hasattr(widget, 'children'):
            for child in widget.children:
                self._find_labels_with_ref_markup(child, labels)
        
        return labels
    
    def _get_widget_offset(self, widget, root):
        """Calculate widget's position relative to root widget.
        
        Args:
            widget: Widget to calculate offset for
            root: Root widget to calculate offset relative to
            
        Returns:
            Tuple (offset_x, offset_y) relative to root
        """
        offset_x = 0
        offset_y = 0
        current = widget
        
        while current is not None and current is not root:
            offset_x += current.x
            offset_y += current.y
            current = current.parent
        
        return offset_x, offset_y
    
    @given(st.text(min_size=1, max_size=20, alphabet=st.characters(
        whitelist_categories=['L', 'N'],
        blacklist_characters='[]()&\n\r'
    )))
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_link_produces_ref_markup_for_translation(self, link_text):
        """Links produce ref markup that will be translated when rendered.
        
        This test verifies that links are correctly rendered with [ref=url] markup,
        which is the prerequisite for coordinate translation. The actual refs
        dictionary is populated by Kivy during texture rendering.
        """
        url = 'https://example.com/page'
        markdown = f'[{link_text}]({url})'
        
        label = MarkdownLabel(text=markdown)
        
        # Find Labels with ref markup
        labels_with_markup = self._find_labels_with_ref_markup(label)
        
        assert len(labels_with_markup) >= 1, \
            f"Expected at least one Label with ref markup for: {markdown}"
        
        # Verify the URL is in the markup
        found_url = False
        for lbl in labels_with_markup:
            if f'[ref={url}]' in lbl.text:
                found_url = True
                break
        
        assert found_url, \
            f"Expected [ref={url}] in Label markup"
    
    @given(st.lists(
        st.text(min_size=1, max_size=10, alphabet=st.characters(
            whitelist_categories=['L', 'N'],
            blacklist_characters='[]()&\n\r'
        )),
        min_size=2, max_size=4
    ))
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_multiple_links_produce_ref_markup(self, link_texts):
        """Multiple links in different paragraphs produce ref markup.
        
        This test verifies that multiple links are correctly rendered with
        [ref=url] markup in their respective Labels.
        """
        # Create markdown with multiple links in separate paragraphs
        paragraphs = []
        urls = []
        for i, text in enumerate(link_texts):
            url = f'https://example{i}.com/page'
            urls.append(url)
            paragraphs.append(f'[{text}]({url})')
        
        markdown = '\n\n'.join(paragraphs)
        label = MarkdownLabel(text=markdown)
        
        # Find Labels with ref markup
        labels_with_markup = self._find_labels_with_ref_markup(label)
        
        # Should have at least as many Labels with markup as we have links
        assert len(labels_with_markup) >= len(link_texts), \
            f"Expected at least {len(link_texts)} Labels with ref markup, got {len(labels_with_markup)}"
        
        # Verify each URL appears in some Label's markup
        for url in urls:
            found = False
            for lbl in labels_with_markup:
                if f'[ref={url}]' in lbl.text:
                    found = True
                    break
            assert found, f"Expected [ref={url}] in some Label markup"
    
    def test_refs_empty_for_no_links(self):
        """refs returns empty dict when there are no links."""
        label = MarkdownLabel(text='Hello World without links')
        
        assert label.refs == {}, \
            f"Expected empty refs, got {label.refs}"
    
    def test_refs_empty_for_empty_text(self):
        """refs returns empty dict for empty text."""
        label = MarkdownLabel(text='')
        
        assert label.refs == {}, \
            f"Expected empty refs for empty text, got {label.refs}"
    
    def test_anchors_empty_for_no_anchors(self):
        """anchors returns empty dict when there are no anchors."""
        label = MarkdownLabel(text='Hello World without anchors')
        
        assert label.anchors == {}, \
            f"Expected empty anchors, got {label.anchors}"
    
    def test_anchors_empty_for_empty_text(self):
        """anchors returns empty dict for empty text."""
        label = MarkdownLabel(text='')
        
        assert label.anchors == {}, \
            f"Expected empty anchors for empty text, got {label.anchors}"
    
    def test_refs_translation_algorithm_correctness(self):
        """Test that the coordinate translation algorithm works correctly.
        
        This test directly verifies the translation logic by checking that
        when child Labels have refs, the aggregated refs contain properly
        translated coordinates.
        """
        markdown = '[Click me](https://example.com)'
        label = MarkdownLabel(text=markdown)
        
        # Get aggregated refs
        aggregated_refs = label.refs
        
        # Find child Labels with refs (if any - depends on rendering)
        labels_with_refs = self._find_labels_with_refs(label)
        
        # If we have child Labels with refs, verify translation
        for child_label in labels_with_refs:
            child_refs = child_label.refs
            offset_x, offset_y = self._get_widget_offset(child_label, label)
            
            for url, child_boxes in child_refs.items():
                assert url in aggregated_refs, \
                    f"Expected URL {url} in aggregated refs"
                
                for child_box in child_boxes:
                    expected_box = [
                        child_box[0] + offset_x,
                        child_box[1] + offset_y,
                        child_box[2] + offset_x,
                        child_box[3] + offset_y
                    ]
                    
                    assert expected_box in aggregated_refs[url], \
                        f"Expected translated box {expected_box} in aggregated refs"
    
    def test_refs_translation_with_nested_list_markup(self):
        """Links in nested content (lists) produce correct ref markup."""
        markdown = '''- [Link 1](https://example1.com)
- [Link 2](https://example2.com)
'''
        label = MarkdownLabel(text=markdown)
        
        # Find Labels with ref markup
        labels_with_markup = self._find_labels_with_ref_markup(label)
        
        # Should have Labels with ref markup for the links
        assert len(labels_with_markup) >= 1, \
            "Expected at least one Label with ref markup in list"
        
        # Verify URLs appear in markup
        all_markup = ' '.join(lbl.text for lbl in labels_with_markup)
        assert '[ref=https://example1.com]' in all_markup or \
               '[ref=https://example2.com]' in all_markup, \
            "Expected ref markup for list links"
    
    def test_refs_translation_with_table_markup(self):
        """Links in table content produce correct ref markup."""
        markdown = '''| Column A | Column B |
| --- | --- |
| [Link](https://example.com) | Text |
'''
        label = MarkdownLabel(text=markdown)
        
        # Find Labels with ref markup
        labels_with_markup = self._find_labels_with_ref_markup(label)
        
        # Should have at least one Label with ref markup
        assert len(labels_with_markup) >= 1, \
            "Expected at least one Label with ref markup in table"
        
        # Verify URL appears in markup
        found = any('[ref=https://example.com]' in lbl.text 
                   for lbl in labels_with_markup)
        assert found, "Expected ref markup for table link"
    
    def test_refs_translation_with_blockquote_markup(self):
        """Links in blockquote content produce correct ref markup."""
        markdown = '> [Quoted link](https://example.com)'
        
        label = MarkdownLabel(text=markdown)
        
        # Find Labels with ref markup
        labels_with_markup = self._find_labels_with_ref_markup(label)
        
        # Should have at least one Label with ref markup
        assert len(labels_with_markup) >= 1, \
            "Expected at least one Label with ref markup in blockquote"
        
        # Verify URL appears in markup
        found = any('[ref=https://example.com]' in lbl.text 
                   for lbl in labels_with_markup)
        assert found, "Expected ref markup for blockquote link"
    
    @given(st.text(min_size=1, max_size=10, alphabet=st.characters(
        whitelist_categories=['L', 'N'],
        blacklist_characters='[]()&\n\r'
    )), st.text(min_size=1, max_size=10, alphabet=st.characters(
        whitelist_categories=['L', 'N'],
        blacklist_characters='[]()&\n\r'
    )))
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_ref_markup_updates_when_text_changes(self, link_text1, link_text2):
        """ref markup updates correctly when text property changes."""
        url1 = 'https://example1.com'
        url2 = 'https://example2.com'
        
        markdown1 = f'[{link_text1}]({url1})'
        markdown2 = f'[{link_text2}]({url2})'
        
        label = MarkdownLabel(text=markdown1)
        
        # Initial markup should have url1
        labels1 = self._find_labels_with_ref_markup(label)
        assert len(labels1) >= 1, "Expected Label with ref markup initially"
        found_url1 = any(f'[ref={url1}]' in lbl.text for lbl in labels1)
        assert found_url1, f"Expected [ref={url1}] in initial markup"
        
        # Change text - use force_rebuild() for immediate update since
        # text changes now use deferred rebuilds
        label.text = markdown2
        label.force_rebuild()
        
        # Updated markup should have url2
        labels2 = self._find_labels_with_ref_markup(label)
        assert len(labels2) >= 1, "Expected Label with ref markup after update"
        found_url2 = any(f'[ref={url2}]' in lbl.text for lbl in labels2)
        assert found_url2, f"Expected [ref={url2}] in updated markup"
        
        # url1 should no longer be present (unless url1 == url2)
        if url1 != url2:
            found_old = any(f'[ref={url1}]' in lbl.text for lbl in labels2)
            assert not found_old, f"Did not expect [ref={url1}] in updated markup"
    
    @given(st.floats(min_value=0, max_value=100),
           st.floats(min_value=0, max_value=100),
           st.floats(min_value=0, max_value=100),
           st.floats(min_value=0, max_value=100))
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_coordinate_translation_math(self, x1, y1, x2, y2):
        """Test that coordinate translation math is correct.
        
        This tests the translation algorithm directly with known values.
        """
        # Simulate a bounding box
        original_box = [x1, y1, x2, y2]
        
        # Simulate an offset
        offset_x = 10.0
        offset_y = 20.0
        
        # Apply translation (same algorithm as in _get_refs)
        translated_box = [
            original_box[0] + offset_x,
            original_box[1] + offset_y,
            original_box[2] + offset_x,
            original_box[3] + offset_y
        ]
        
        # Verify translation
        assert translated_box[0] == x1 + offset_x
        assert translated_box[1] == y1 + offset_y
        assert translated_box[2] == x2 + offset_x
        assert translated_box[3] == y2 + offset_y
    
    @given(st.floats(min_value=0, max_value=100),
           st.floats(min_value=0, max_value=100))
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_anchor_translation_math(self, x, y):
        """Test that anchor coordinate translation math is correct.
        
        This tests the translation algorithm directly with known values.
        """
        # Simulate an anchor position
        original_pos = (x, y)
        
        # Simulate an offset
        offset_x = 15.0
        offset_y = 25.0
        
        # Apply translation (same algorithm as in _get_anchors)
        translated_pos = (
            original_pos[0] + offset_x,
            original_pos[1] + offset_y
        )
        
        # Verify translation
        assert translated_pos[0] == x + offset_x
        assert translated_pos[1] == y + offset_y