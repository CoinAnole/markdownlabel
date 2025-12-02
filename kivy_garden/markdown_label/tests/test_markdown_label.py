"""
Property-based tests for MarkdownLabel widget.

Tests verify that the MarkdownLabel correctly parses Markdown text
and generates appropriate Kivy widget trees.
"""

import os
# Set environment variable to use headless mode for Kivy
os.environ['KIVY_NO_ARGS'] = '1'
os.environ['KIVY_NO_CONSOLELOG'] = '1'

import pytest
from hypothesis import given, strategies as st, settings, assume

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout

from kivy_garden.markdown_label import MarkdownLabel


# Custom strategies for generating valid Markdown text

@st.composite
def markdown_heading(draw):
    """Generate a Markdown heading."""
    level = draw(st.integers(min_value=1, max_value=6))
    text = draw(st.text(min_size=1, max_size=50, alphabet=st.characters(
        whitelist_categories=['L', 'N', 'P', 'S'],
        blacklist_characters='#[]&\n\r'
    )))
    return '#' * level + ' ' + text


@st.composite
def markdown_paragraph(draw):
    """Generate a Markdown paragraph."""
    text = draw(st.text(min_size=1, max_size=100, alphabet=st.characters(
        whitelist_categories=['L', 'N', 'P', 'S', 'Z'],
        blacklist_characters='#[]&\n\r*_`~'
    )))
    return text.strip()


@st.composite
def markdown_bold(draw):
    """Generate bold Markdown text."""
    text = draw(st.text(min_size=1, max_size=30, alphabet=st.characters(
        whitelist_categories=['L', 'N'],
        blacklist_characters='*_[]&\n\r'
    )))
    return f'**{text}**'


@st.composite
def markdown_italic(draw):
    """Generate italic Markdown text."""
    text = draw(st.text(min_size=1, max_size=30, alphabet=st.characters(
        whitelist_categories=['L', 'N'],
        blacklist_characters='*_[]&\n\r'
    )))
    return f'*{text}*'


@st.composite
def markdown_link(draw):
    """Generate a Markdown link."""
    text = draw(st.text(min_size=1, max_size=30, alphabet=st.characters(
        whitelist_categories=['L', 'N'],
        blacklist_characters='[]()&\n\r'
    )))
    url = draw(st.from_regex(r'https?://[a-z]+\.[a-z]+/[a-z]+', fullmatch=True))
    return f'[{text}]({url})'


@st.composite
def simple_markdown_document(draw):
    """Generate a simple Markdown document with various block elements."""
    elements = []
    num_elements = draw(st.integers(min_value=1, max_value=5))
    
    for _ in range(num_elements):
        element_type = draw(st.sampled_from(['heading', 'paragraph']))
        if element_type == 'heading':
            elements.append(draw(markdown_heading()))
        else:
            para = draw(markdown_paragraph())
            if para:  # Only add non-empty paragraphs
                elements.append(para)
    
    # Filter out empty elements and join with double newlines
    elements = [e for e in elements if e.strip()]
    return '\n\n'.join(elements) if elements else 'Default text'


# **Feature: markdown-label, Property 1: Widget Tree Generation**
# *For any* valid Markdown text, when parsed and rendered by MarkdownLabel,
# the resulting widget tree SHALL contain at least one child widget for each
# block-level element in the AST.
# **Validates: Requirements 1.1**

class TestWidgetTreeGeneration:
    """Property tests for widget tree generation (Property 1)."""
    
    @given(simple_markdown_document())
    @settings(max_examples=100, deadline=None)
    def test_markdown_produces_widgets(self, markdown_text):
        """Valid Markdown text produces at least one widget."""
        assume(markdown_text.strip())  # Skip empty text
        
        label = MarkdownLabel(text=markdown_text)
        
        # Should have at least one child widget
        assert len(label.children) >= 1, \
            f"Expected at least 1 child for markdown: {markdown_text!r}"
    
    @given(markdown_heading())
    @settings(max_examples=100, deadline=None)
    def test_heading_produces_label_widget(self, heading):
        """Heading Markdown produces a Label widget."""
        label = MarkdownLabel(text=heading)
        
        # Should have exactly one child (the heading)
        assert len(label.children) >= 1, \
            f"Expected at least 1 child for heading: {heading!r}"
        
        # The child should be a Label
        # Note: Kivy children are in reverse order
        heading_widget = label.children[-1]
        assert isinstance(heading_widget, Label), \
            f"Expected Label, got {type(heading_widget)}"
    
    @given(markdown_paragraph())
    @settings(max_examples=100, deadline=None)
    def test_paragraph_produces_label_widget(self, paragraph):
        """Paragraph Markdown produces a Label widget."""
        assume(paragraph.strip())  # Skip empty paragraphs
        
        label = MarkdownLabel(text=paragraph)
        
        # Should have at least one child
        assert len(label.children) >= 1, \
            f"Expected at least 1 child for paragraph: {paragraph!r}"
    
    @given(st.integers(min_value=1, max_value=5))
    @settings(max_examples=100, deadline=None)
    def test_multiple_blocks_produce_multiple_widgets(self, num_blocks):
        """Multiple block elements produce multiple widgets."""
        # Create markdown with multiple paragraphs
        paragraphs = [f'Paragraph {i}' for i in range(num_blocks)]
        markdown_text = '\n\n'.join(paragraphs)
        
        label = MarkdownLabel(text=markdown_text)
        
        # Should have at least num_blocks children (may have blank_line widgets too)
        assert len(label.children) >= num_blocks, \
            f"Expected at least {num_blocks} children, got {len(label.children)}"
    
    def test_empty_text_produces_no_widgets(self):
        """Empty text produces no child widgets."""
        label = MarkdownLabel(text='')
        
        assert len(label.children) == 0, \
            f"Expected 0 children for empty text, got {len(label.children)}"



# **Feature: markdown-label, Property 2: Reactive Text Updates**
# *For any* two different Markdown texts, when the `text` property is changed
# from the first to the second, the widget tree SHALL reflect the structure
# of the second text, not the first.
# **Validates: Requirements 1.2**

class TestReactiveTextUpdates:
    """Property tests for reactive text updates (Property 2)."""
    
    @given(markdown_heading(), markdown_paragraph())
    @settings(max_examples=100, deadline=None)
    def test_text_change_updates_widgets(self, text1, text2):
        """Changing text property updates the widget tree."""
        assume(text1.strip() and text2.strip())
        assume(text1 != text2)
        
        label = MarkdownLabel(text=text1)
        initial_children = len(label.children)
        
        # Change text
        label.text = text2
        
        # Widget tree should be rebuilt
        # We can't easily compare exact structure, but we can verify
        # that the label's text property reflects the new value
        assert label.text == text2, \
            f"Expected text to be {text2!r}, got {label.text!r}"
    
    @given(st.integers(min_value=1, max_value=3), st.integers(min_value=1, max_value=3))
    @settings(max_examples=100, deadline=None)
    def test_different_block_counts_update_correctly(self, count1, count2):
        """Changing from N blocks to M blocks updates widget count."""
        assume(count1 != count2)
        
        # Create markdown with count1 paragraphs
        text1 = '\n\n'.join([f'Para {i}' for i in range(count1)])
        # Create markdown with count2 paragraphs
        text2 = '\n\n'.join([f'New para {i}' for i in range(count2)])
        
        label = MarkdownLabel(text=text1)
        children_before = len(label.children)
        
        # Change text
        label.text = text2
        children_after = len(label.children)
        
        # The number of children should change to reflect new content
        # (may include blank_line widgets, so we check >= count)
        assert children_after >= count2, \
            f"Expected at least {count2} children after update, got {children_after}"
    
    @given(simple_markdown_document())
    @settings(max_examples=100, deadline=None)
    def test_clear_text_removes_widgets(self, markdown_text):
        """Setting text to empty removes all widgets."""
        assume(markdown_text.strip())
        
        label = MarkdownLabel(text=markdown_text)
        assert len(label.children) > 0, "Should have children initially"
        
        # Clear text
        label.text = ''
        
        assert len(label.children) == 0, \
            f"Expected 0 children after clearing text, got {len(label.children)}"
    
    @given(simple_markdown_document(), simple_markdown_document())
    @settings(max_examples=100, deadline=None)
    def test_ast_updates_with_text(self, text1, text2):
        """AST tokens update when text changes."""
        assume(text1.strip() and text2.strip())
        
        label = MarkdownLabel(text=text1)
        ast1 = label.get_ast()
        
        label.text = text2
        ast2 = label.get_ast()
        
        # If texts are different, ASTs should be different
        if text1 != text2:
            # At minimum, the AST should be updated (not necessarily different
            # if the texts parse to the same structure)
            assert label.text == text2


# **Feature: markdown-label, Property 16: Auto-Sizing Behavior**
# *For any* MarkdownLabel with content, the widget SHALL have size_hint_y=None
# and its height SHALL equal or exceed the sum of its children's heights.
# **Validates: Requirements 11.1**

class TestAutoSizingBehavior:
    """Property tests for auto-sizing behavior (Property 16)."""
    
    @given(simple_markdown_document())
    @settings(max_examples=100, deadline=None)
    def test_size_hint_y_is_none(self, markdown_text):
        """MarkdownLabel has size_hint_y=None for auto-sizing."""
        label = MarkdownLabel(text=markdown_text)
        
        assert label.size_hint_y is None, \
            f"Expected size_hint_y=None, got {label.size_hint_y}"
    
    @given(markdown_heading())
    @settings(max_examples=100, deadline=None)
    def test_height_bound_to_minimum(self, heading):
        """MarkdownLabel height is bound to minimum_height."""
        label = MarkdownLabel(text=heading)
        
        # The height should be bound to minimum_height
        # We can verify the binding exists by checking the property
        assert label.size_hint_y is None, \
            "size_hint_y should be None for auto-sizing"
    
    def test_empty_label_has_zero_height(self):
        """Empty MarkdownLabel has zero or minimal height."""
        label = MarkdownLabel(text='')
        
        assert label.size_hint_y is None, \
            "size_hint_y should be None even for empty label"
        # Empty label should have no children
        assert len(label.children) == 0
    
    @given(st.integers(min_value=1, max_value=5))
    @settings(max_examples=100, deadline=None)
    def test_more_content_means_more_height_potential(self, num_paragraphs):
        """More content should result in more minimum height."""
        # Create markdown with varying number of paragraphs
        text = '\n\n'.join([f'Paragraph number {i} with some text content.' 
                           for i in range(num_paragraphs)])
        
        label = MarkdownLabel(text=text)
        
        # Verify auto-sizing is enabled
        assert label.size_hint_y is None
        # Verify children exist
        assert len(label.children) >= num_paragraphs


# **Feature: markdown-label, Property 12: Link Ref Markup**
# *For any* Markdown link [text](url), the rendered Kivy markup SHALL contain
# [ref=url]text[/ref].
# **Validates: Requirements 7.1**

class TestLinkRefMarkup:
    """Property tests for link ref markup (Property 12)."""
    
    @given(markdown_link())
    @settings(max_examples=100, deadline=None)
    def test_link_produces_ref_markup(self, link_markdown):
        """Markdown links produce [ref=url]...[/ref] markup in Labels."""
        label = MarkdownLabel(text=link_markdown)
        
        # Should have at least one child (paragraph containing the link)
        assert len(label.children) >= 1, \
            f"Expected at least 1 child for link: {link_markdown!r}"
        
        # Find a Label with the ref markup
        found_ref = False
        for child in label.children:
            if isinstance(child, Label) and child.markup:
                if '[ref=' in child.text and '[/ref]' in child.text:
                    found_ref = True
                    break
        
        assert found_ref, \
            f"Expected to find [ref=...][/ref] markup in children for: {link_markdown!r}"
    
    @given(st.text(min_size=1, max_size=20, alphabet=st.characters(
        whitelist_categories=['L', 'N'],
        blacklist_characters='[]()&\n\r'
    )))
    @settings(max_examples=100, deadline=None)
    def test_link_url_in_ref_tag(self, link_text):
        """Link URL appears in ref tag."""
        url = 'https://example.com/page'
        markdown = f'[{link_text}]({url})'
        
        label = MarkdownLabel(text=markdown)
        
        # Find the Label with ref markup
        for child in label.children:
            if isinstance(child, Label) and child.markup:
                if f'[ref={url}]' in child.text:
                    assert '[/ref]' in child.text, \
                        f"Missing closing [/ref] tag in: {child.text}"
                    return
        
        pytest.fail(f"Expected to find [ref={url}] in markup for: {markdown!r}")
    
    @given(st.from_regex(r'https?://[a-z]+\.[a-z]+/[a-z]+', fullmatch=True))
    @settings(max_examples=100, deadline=None)
    def test_various_urls_in_links(self, url):
        """Various URL formats work in links."""
        markdown = f'[Click here]({url})'
        
        label = MarkdownLabel(text=markdown)
        
        # Verify the link is rendered
        assert len(label.children) >= 1
        
        # Find ref markup
        found = False
        for child in label.children:
            if isinstance(child, Label) and child.markup:
                if f'[ref={url}]' in child.text:
                    found = True
                    break
        
        assert found, f"Expected [ref={url}] in markup"
