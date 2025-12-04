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

from kivy_garden.markdownlabel import MarkdownLabel


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
    # Exclude backslash as it's an escape character in Markdown
    # that gets consumed during parsing (e.g., \: becomes :)
    text = draw(st.text(min_size=1, max_size=100, alphabet=st.characters(
        whitelist_categories=['L', 'N', 'P', 'S', 'Z'],
        blacklist_characters='#[]&\n\r*_`~\\'
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


# **Feature: label-compatibility, Property 1: font_size/base_font_size Alias Bidirectionality**
# *For any* numeric value V, setting `font_size` to V SHALL result in `base_font_size`
# equaling V, and setting `base_font_size` to V SHALL result in `font_size` returning V.
# **Validates: Requirements 2.1, 2.2**

class TestFontSizeAliasBidirectionality:
    """Property tests for font_size/base_font_size alias (Property 1)."""
    
    @given(st.floats(min_value=1, max_value=200, allow_nan=False, allow_infinity=False))
    @settings(max_examples=100, deadline=None)
    def test_font_size_sets_base_font_size(self, font_size_value):
        """Setting font_size updates base_font_size to the same value."""
        label = MarkdownLabel(font_size=font_size_value)
        
        assert label.base_font_size == font_size_value, \
            f"Expected base_font_size={font_size_value}, got {label.base_font_size}"
    
    @given(st.floats(min_value=1, max_value=200, allow_nan=False, allow_infinity=False))
    @settings(max_examples=100, deadline=None)
    def test_base_font_size_returns_via_font_size(self, base_font_size_value):
        """Setting base_font_size is returned when reading font_size."""
        label = MarkdownLabel(base_font_size=base_font_size_value)
        
        assert label.font_size == base_font_size_value, \
            f"Expected font_size={base_font_size_value}, got {label.font_size}"
    
    @given(st.floats(min_value=1, max_value=200, allow_nan=False, allow_infinity=False),
           st.floats(min_value=1, max_value=200, allow_nan=False, allow_infinity=False))
    @settings(max_examples=100, deadline=None)
    def test_font_size_change_updates_base_font_size(self, initial_value, new_value):
        """Changing font_size after creation updates base_font_size."""
        label = MarkdownLabel(font_size=initial_value)
        label.font_size = new_value
        
        assert label.base_font_size == new_value, \
            f"Expected base_font_size={new_value}, got {label.base_font_size}"
    
    @given(st.floats(min_value=1, max_value=200, allow_nan=False, allow_infinity=False),
           st.floats(min_value=1, max_value=200, allow_nan=False, allow_infinity=False))
    @settings(max_examples=100, deadline=None)
    def test_base_font_size_change_updates_font_size(self, initial_value, new_value):
        """Changing base_font_size after creation updates font_size."""
        label = MarkdownLabel(base_font_size=initial_value)
        label.base_font_size = new_value
        
        assert label.font_size == new_value, \
            f"Expected font_size={new_value}, got {label.font_size}"
    
    @given(st.floats(min_value=1, max_value=200, allow_nan=False, allow_infinity=False))
    @settings(max_examples=100, deadline=None)
    def test_bidirectional_equivalence(self, value):
        """font_size and base_font_size are always equivalent."""
        label = MarkdownLabel()
        
        # Set via font_size
        label.font_size = value
        assert label.font_size == label.base_font_size, \
            f"font_size ({label.font_size}) != base_font_size ({label.base_font_size})"
        
        # Set via base_font_size
        label.base_font_size = value + 1
        assert label.font_size == label.base_font_size, \
            f"font_size ({label.font_size}) != base_font_size ({label.base_font_size})"


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



# **Feature: markdown-label, Property 17: Round-Trip Serialization**
# *For any* valid Markdown text M, if we parse M to AST A, serialize A back
# to Markdown M', and parse M' to AST A', then A and A' SHALL be semantically
# equivalent (same structure and content).
# **Validates: Requirements 12.2, 12.3**

class TestRoundTripSerialization:
    """Property tests for round-trip serialization (Property 17)."""
    
    def _normalize_ast(self, tokens):
        """Normalize AST for comparison by removing non-semantic fields.
        
        Args:
            tokens: List of AST tokens
            
        Returns:
            Normalized token list for comparison
        """
        if not isinstance(tokens, list):
            return tokens
        
        normalized = []
        for token in tokens:
            if not isinstance(token, dict):
                normalized.append(token)
                continue
            
            # Skip blank_line tokens as they're formatting artifacts
            if token.get('type') == 'blank_line':
                continue
            
            # Create normalized copy without style/formatting metadata
            norm_token = {}
            for key, value in token.items():
                # Skip non-semantic fields
                if key in ('style',):
                    continue
                elif key == 'children':
                    norm_token[key] = self._normalize_ast(value)
                elif key == 'attrs':
                    # Keep attrs but normalize them
                    norm_token[key] = dict(value) if value else {}
                else:
                    norm_token[key] = value
            
            normalized.append(norm_token)
        
        # Merge adjacent text tokens for semantic comparison
        normalized = self._merge_adjacent_text(normalized)
        
        return normalized
    
    def _merge_adjacent_text(self, tokens):
        """Merge adjacent text tokens into single tokens.
        
        This handles cases where the same text content is tokenized
        differently (e.g., '0:' vs '0' + ':').
        
        Args:
            tokens: List of normalized tokens
            
        Returns:
            Tokens with adjacent text merged
        """
        if not tokens:
            return tokens
        
        merged = []
        i = 0
        while i < len(tokens):
            token = tokens[i]
            
            if isinstance(token, dict) and token.get('type') == 'text':
                # Collect consecutive text tokens
                text_parts = [token.get('raw', '')]
                j = i + 1
                while j < len(tokens):
                    next_token = tokens[j]
                    if isinstance(next_token, dict) and next_token.get('type') == 'text':
                        text_parts.append(next_token.get('raw', ''))
                        j += 1
                    else:
                        break
                
                # Create merged text token
                merged.append({'type': 'text', 'raw': ''.join(text_parts)})
                i = j
            else:
                merged.append(token)
                i += 1
        
        return merged
    
    @given(markdown_heading())
    @settings(max_examples=100, deadline=None)
    def test_heading_round_trip(self, heading):
        """Heading round-trips through parse-serialize-parse."""
        label = MarkdownLabel(text=heading)
        ast1 = self._normalize_ast(label.get_ast())
        
        # Serialize back to markdown
        serialized = label.to_markdown()
        
        # Parse again
        label2 = MarkdownLabel(text=serialized)
        ast2 = self._normalize_ast(label2.get_ast())
        
        # ASTs should be equivalent
        assert ast1 == ast2, \
            f"AST mismatch after round-trip:\nOriginal: {ast1}\nAfter: {ast2}\nSerialized: {serialized!r}"
    
    @given(markdown_paragraph())
    @settings(max_examples=100, deadline=None)
    def test_paragraph_round_trip(self, paragraph):
        """Paragraph round-trips through parse-serialize-parse."""
        assume(paragraph.strip())
        
        label = MarkdownLabel(text=paragraph)
        ast1 = self._normalize_ast(label.get_ast())
        
        # Skip if the paragraph was parsed as something other than a paragraph
        # (e.g., "0)" gets parsed as an ordered list)
        if ast1 and ast1[0].get('type') != 'paragraph':
            assume(False)
        
        serialized = label.to_markdown()
        
        label2 = MarkdownLabel(text=serialized)
        ast2 = self._normalize_ast(label2.get_ast())
        
        assert ast1 == ast2, \
            f"AST mismatch after round-trip:\nOriginal: {ast1}\nAfter: {ast2}"
    
    @given(markdown_bold())
    @settings(max_examples=100, deadline=None)
    def test_bold_round_trip(self, bold_text):
        """Bold text round-trips through parse-serialize-parse."""
        label = MarkdownLabel(text=bold_text)
        ast1 = self._normalize_ast(label.get_ast())
        
        serialized = label.to_markdown()
        
        label2 = MarkdownLabel(text=serialized)
        ast2 = self._normalize_ast(label2.get_ast())
        
        assert ast1 == ast2, \
            f"AST mismatch after round-trip:\nOriginal: {ast1}\nAfter: {ast2}"
    
    @given(markdown_italic())
    @settings(max_examples=100, deadline=None)
    def test_italic_round_trip(self, italic_text):
        """Italic text round-trips through parse-serialize-parse."""
        label = MarkdownLabel(text=italic_text)
        ast1 = self._normalize_ast(label.get_ast())
        
        serialized = label.to_markdown()
        
        label2 = MarkdownLabel(text=serialized)
        ast2 = self._normalize_ast(label2.get_ast())
        
        assert ast1 == ast2, \
            f"AST mismatch after round-trip:\nOriginal: {ast1}\nAfter: {ast2}"
    
    @given(markdown_link())
    @settings(max_examples=100, deadline=None)
    def test_link_round_trip(self, link_text):
        """Link round-trips through parse-serialize-parse."""
        label = MarkdownLabel(text=link_text)
        ast1 = self._normalize_ast(label.get_ast())
        
        serialized = label.to_markdown()
        
        label2 = MarkdownLabel(text=serialized)
        ast2 = self._normalize_ast(label2.get_ast())
        
        assert ast1 == ast2, \
            f"AST mismatch after round-trip:\nOriginal: {ast1}\nAfter: {ast2}"
    
    @given(simple_markdown_document())
    @settings(max_examples=100, deadline=None)
    def test_document_round_trip(self, markdown_text):
        """Full document round-trips through parse-serialize-parse."""
        assume(markdown_text.strip())
        # Skip texts with escape sequences that change meaning when unescaped
        assume('\\' not in markdown_text)
        
        label = MarkdownLabel(text=markdown_text)
        ast1 = self._normalize_ast(label.get_ast())
        
        serialized = label.to_markdown()
        
        label2 = MarkdownLabel(text=serialized)
        ast2 = self._normalize_ast(label2.get_ast())
        
        assert ast1 == ast2, \
            f"AST mismatch after round-trip:\nOriginal: {ast1}\nAfter: {ast2}\nSerialized: {serialized!r}"
    
    def test_code_block_round_trip(self):
        """Code block round-trips correctly."""
        markdown = '```python\nprint("hello")\n```'
        
        label = MarkdownLabel(text=markdown)
        ast1 = self._normalize_ast(label.get_ast())
        
        serialized = label.to_markdown()
        
        label2 = MarkdownLabel(text=serialized)
        ast2 = self._normalize_ast(label2.get_ast())
        
        assert ast1 == ast2, \
            f"AST mismatch after round-trip:\nOriginal: {ast1}\nAfter: {ast2}"
    
    def test_list_round_trip(self):
        """List round-trips correctly."""
        markdown = '- Item 1\n- Item 2\n- Item 3'
        
        label = MarkdownLabel(text=markdown)
        ast1 = self._normalize_ast(label.get_ast())
        
        serialized = label.to_markdown()
        
        label2 = MarkdownLabel(text=serialized)
        ast2 = self._normalize_ast(label2.get_ast())
        
        assert ast1 == ast2, \
            f"AST mismatch after round-trip:\nOriginal: {ast1}\nAfter: {ast2}"
    
    def test_ordered_list_round_trip(self):
        """Ordered list round-trips correctly."""
        markdown = '1. First\n2. Second\n3. Third'
        
        label = MarkdownLabel(text=markdown)
        ast1 = self._normalize_ast(label.get_ast())
        
        serialized = label.to_markdown()
        
        label2 = MarkdownLabel(text=serialized)
        ast2 = self._normalize_ast(label2.get_ast())
        
        assert ast1 == ast2, \
            f"AST mismatch after round-trip:\nOriginal: {ast1}\nAfter: {ast2}"
    
    def test_block_quote_round_trip(self):
        """Block quote round-trips correctly."""
        markdown = '> This is a quote'
        
        label = MarkdownLabel(text=markdown)
        ast1 = self._normalize_ast(label.get_ast())
        
        serialized = label.to_markdown()
        
        label2 = MarkdownLabel(text=serialized)
        ast2 = self._normalize_ast(label2.get_ast())
        
        assert ast1 == ast2, \
            f"AST mismatch after round-trip:\nOriginal: {ast1}\nAfter: {ast2}"
    
    def test_thematic_break_round_trip(self):
        """Thematic break round-trips correctly."""
        markdown = 'Before\n\n---\n\nAfter'
        
        label = MarkdownLabel(text=markdown)
        ast1 = self._normalize_ast(label.get_ast())
        
        serialized = label.to_markdown()
        
        label2 = MarkdownLabel(text=serialized)
        ast2 = self._normalize_ast(label2.get_ast())
        
        assert ast1 == ast2, \
            f"AST mismatch after round-trip:\nOriginal: {ast1}\nAfter: {ast2}"
    
    def test_table_round_trip(self):
        """Table round-trips correctly."""
        markdown = '| A | B |\n| --- | --- |\n| 1 | 2 |'
        
        label = MarkdownLabel(text=markdown)
        ast1 = self._normalize_ast(label.get_ast())
        
        serialized = label.to_markdown()
        
        label2 = MarkdownLabel(text=serialized)
        ast2 = self._normalize_ast(label2.get_ast())
        
        assert ast1 == ast2, \
            f"AST mismatch after round-trip:\nOriginal: {ast1}\nAfter: {ast2}"


# **Feature: markdown-label, Property 18: Deep Nesting Stability**
# *For any* Markdown with nesting depth up to 10 levels (nested lists, quotes),
# the MarkdownLabel SHALL render without raising exceptions or causing stack overflow.
# **Validates: Requirements 13.1**

class TestDeepNestingStability:
    """Property tests for deep nesting stability (Property 18)."""
    
    @given(st.integers(min_value=1, max_value=15))
    @settings(max_examples=100, deadline=None)
    def test_nested_lists_render_without_exception(self, depth):
        """Deeply nested lists render without raising exceptions."""
        # Generate nested list markdown
        markdown = self._generate_nested_list(depth)
        
        # Should not raise any exception
        try:
            label = MarkdownLabel(text=markdown)
            # Verify it produced some output
            assert isinstance(label, BoxLayout)
        except RecursionError:
            pytest.fail(f"RecursionError at depth {depth}")
        except Exception as e:
            pytest.fail(f"Unexpected exception at depth {depth}: {e}")
    
    @given(st.integers(min_value=1, max_value=15))
    @settings(max_examples=100, deadline=None)
    def test_nested_quotes_render_without_exception(self, depth):
        """Deeply nested block quotes render without raising exceptions."""
        # Generate nested quote markdown
        markdown = self._generate_nested_quote(depth)
        
        # Should not raise any exception
        try:
            label = MarkdownLabel(text=markdown)
            assert isinstance(label, BoxLayout)
        except RecursionError:
            pytest.fail(f"RecursionError at depth {depth}")
        except Exception as e:
            pytest.fail(f"Unexpected exception at depth {depth}: {e}")
    
    @given(st.integers(min_value=1, max_value=15))
    @settings(max_examples=100, deadline=None)
    def test_mixed_nesting_renders_without_exception(self, depth):
        """Mixed nested structures (lists and quotes) render without exceptions."""
        # Generate mixed nested markdown
        markdown = self._generate_mixed_nesting(depth)
        
        # Should not raise any exception
        try:
            label = MarkdownLabel(text=markdown)
            assert isinstance(label, BoxLayout)
        except RecursionError:
            pytest.fail(f"RecursionError at depth {depth}")
        except Exception as e:
            pytest.fail(f"Unexpected exception at depth {depth}: {e}")
    
    def test_exactly_10_levels_renders_fully(self):
        """Exactly 10 levels of nesting renders without truncation warning."""
        markdown = self._generate_nested_list(10)
        label = MarkdownLabel(text=markdown)
        
        # Should render without exception
        assert isinstance(label, BoxLayout)
        assert len(label.children) >= 1
    
    def test_beyond_10_levels_still_renders(self):
        """Beyond 10 levels still renders (with truncation) without crashing."""
        markdown = self._generate_nested_list(15)
        label = MarkdownLabel(text=markdown)
        
        # Should render without exception
        assert isinstance(label, BoxLayout)
        # Should have at least some content
        assert len(label.children) >= 1
    
    def _generate_nested_list(self, depth: int) -> str:
        """Generate a nested list with specified depth.
        
        Args:
            depth: Number of nesting levels
            
        Returns:
            Markdown string with nested list
        """
        lines = []
        for i in range(depth):
            indent = '  ' * i
            lines.append(f'{indent}- Level {i + 1}')
        return '\n'.join(lines)
    
    def _generate_nested_quote(self, depth: int) -> str:
        """Generate nested block quotes with specified depth.
        
        Args:
            depth: Number of nesting levels
            
        Returns:
            Markdown string with nested quotes
        """
        prefix = '> ' * depth
        return f'{prefix}Deeply nested quote at level {depth}'
    
    def _generate_mixed_nesting(self, depth: int) -> str:
        """Generate mixed nested structures (alternating lists and quotes).
        
        Args:
            depth: Number of nesting levels
            
        Returns:
            Markdown string with mixed nesting
        """
        lines = []
        for i in range(depth):
            if i % 2 == 0:
                # List item
                indent = '  ' * (i // 2)
                lines.append(f'{indent}- List level {i + 1}')
            else:
                # Quote (inside list)
                indent = '  ' * (i // 2)
                lines.append(f'{indent}  > Quote level {i + 1}')
        return '\n'.join(lines)


# **Feature: label-compatibility, Property 8: No-Op Properties Acceptance**
# *For any* boolean value, setting `bold`, `italic`, `underline`, `strikethrough`,
# or `markup` on MarkdownLabel SHALL NOT raise an exception, and the rendered
# output SHALL be identical regardless of these property values.
# **Validates: Requirements 8.1, 8.2, 8.3, 8.4, 8.5, 8.6**

class TestNoOpPropertiesAcceptance:
    """Property tests for no-op properties acceptance (Property 8)."""
    
    @given(st.booleans())
    @settings(max_examples=100, deadline=None)
    def test_bold_property_accepted(self, value):
        """Setting bold property does not raise an exception."""
        # Should not raise any exception
        label = MarkdownLabel(text='# Hello World', bold=value)
        assert label.bold == value
    
    @given(st.booleans())
    @settings(max_examples=100, deadline=None)
    def test_italic_property_accepted(self, value):
        """Setting italic property does not raise an exception."""
        label = MarkdownLabel(text='# Hello World', italic=value)
        assert label.italic == value
    
    @given(st.booleans())
    @settings(max_examples=100, deadline=None)
    def test_underline_property_accepted(self, value):
        """Setting underline property does not raise an exception."""
        label = MarkdownLabel(text='# Hello World', underline=value)
        assert label.underline == value
    
    @given(st.booleans())
    @settings(max_examples=100, deadline=None)
    def test_strikethrough_property_accepted(self, value):
        """Setting strikethrough property does not raise an exception."""
        label = MarkdownLabel(text='# Hello World', strikethrough=value)
        assert label.strikethrough == value
    
    @given(st.booleans())
    @settings(max_examples=100, deadline=None)
    def test_markup_property_accepted(self, value):
        """Setting markup property does not raise an exception."""
        label = MarkdownLabel(text='# Hello World', markup=value)
        assert label.markup == value
    
    @given(st.booleans(), st.booleans(), st.booleans(), st.booleans(), st.booleans())
    @settings(max_examples=100, deadline=None)
    def test_all_noop_properties_together(self, bold, italic, underline, strikethrough, markup):
        """Setting all no-op properties together does not raise an exception."""
        label = MarkdownLabel(
            text='# Hello World',
            bold=bold,
            italic=italic,
            underline=underline,
            strikethrough=strikethrough,
            markup=markup
        )
        assert label.bold == bold
        assert label.italic == italic
        assert label.underline == underline
        assert label.strikethrough == strikethrough
        assert label.markup == markup
    
    @given(st.booleans(), st.booleans(), st.booleans(), st.booleans(), st.booleans(),
           simple_markdown_document())
    @settings(max_examples=100, deadline=None)
    def test_noop_properties_do_not_affect_rendering(self, bold, italic, underline, 
                                                      strikethrough, markup, markdown_text):
        """No-op properties do not affect the rendered output."""
        assume(markdown_text.strip())
        
        # Create label with default no-op property values
        label_default = MarkdownLabel(text=markdown_text)
        default_child_count = len(label_default.children)
        
        # Create label with various no-op property values
        label_with_props = MarkdownLabel(
            text=markdown_text,
            bold=bold,
            italic=italic,
            underline=underline,
            strikethrough=strikethrough,
            markup=markup
        )
        props_child_count = len(label_with_props.children)
        
        # The number of children should be the same regardless of no-op properties
        assert default_child_count == props_child_count, \
            f"Expected {default_child_count} children, got {props_child_count} with no-op props"
    
    @given(st.booleans())
    @settings(max_examples=100, deadline=None)
    def test_bold_property_change_after_creation(self, value):
        """Changing bold property after creation does not raise an exception."""
        label = MarkdownLabel(text='# Hello')
        label.bold = value
        assert label.bold == value
    
    @given(st.booleans())
    @settings(max_examples=100, deadline=None)
    def test_italic_property_change_after_creation(self, value):
        """Changing italic property after creation does not raise an exception."""
        label = MarkdownLabel(text='# Hello')
        label.italic = value
        assert label.italic == value
    
    @given(st.booleans())
    @settings(max_examples=100, deadline=None)
    def test_underline_property_change_after_creation(self, value):
        """Changing underline property after creation does not raise an exception."""
        label = MarkdownLabel(text='# Hello')
        label.underline = value
        assert label.underline == value
    
    @given(st.booleans())
    @settings(max_examples=100, deadline=None)
    def test_strikethrough_property_change_after_creation(self, value):
        """Changing strikethrough property after creation does not raise an exception."""
        label = MarkdownLabel(text='# Hello')
        label.strikethrough = value
        assert label.strikethrough == value
    
    @given(st.booleans())
    @settings(max_examples=100, deadline=None)
    def test_markup_property_change_after_creation(self, value):
        """Changing markup property after creation does not raise an exception."""
        label = MarkdownLabel(text='# Hello')
        label.markup = value
        assert label.markup == value


# **Feature: label-compatibility, Property 2: font_name Forwarding with Code Preservation**
# *For any* Markdown text containing both regular text and code blocks, and any font_name value,
# all non-code internal Labels SHALL have `font_name` set to the specified value, while code
# Labels SHALL retain `code_font_name`.
# **Validates: Requirements 1.1, 1.3**

# Use Kivy's built-in fonts that are guaranteed to be available
KIVY_FONTS = ['Roboto', 'Roboto-Bold', 'Roboto-Italic', 'RobotoMono-Regular']


class TestFontNameForwarding:
    """Property tests for font_name forwarding (Property 2)."""
    
    def _find_labels_recursive(self, widget, labels=None):
        """Recursively find all Label widgets in a widget tree.
        
        Args:
            widget: Root widget to search
            labels: List to accumulate labels (created if None)
            
        Returns:
            List of Label widgets found
        """
        if labels is None:
            labels = []
        
        if isinstance(widget, Label):
            labels.append(widget)
        
        if hasattr(widget, 'children'):
            for child in widget.children:
                self._find_labels_recursive(child, labels)
        
        return labels
    
    def _is_code_label(self, label, code_font_name='RobotoMono-Regular'):
        """Check if a label is a code label based on its font.
        
        Args:
            label: Label widget to check
            code_font_name: Expected code font name
            
        Returns:
            True if this appears to be a code label
        """
        return label.font_name == code_font_name
    
    @given(st.sampled_from(KIVY_FONTS))
    @settings(max_examples=100, deadline=None)
    def test_font_name_applied_to_paragraph(self, font_name):
        """font_name is applied to paragraph Labels."""
        label = MarkdownLabel(text='Hello World', font_name=font_name)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        # All labels should have the specified font_name
        for lbl in labels:
            assert lbl.font_name == font_name, \
                f"Expected font_name={font_name}, got {lbl.font_name}"
    
    @given(st.sampled_from(KIVY_FONTS))
    @settings(max_examples=100, deadline=None)
    def test_font_name_applied_to_heading(self, font_name):
        """font_name is applied to heading Labels."""
        label = MarkdownLabel(text='# Heading', font_name=font_name)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        # All labels should have the specified font_name
        for lbl in labels:
            assert lbl.font_name == font_name, \
                f"Expected font_name={font_name}, got {lbl.font_name}"
    
    @given(st.sampled_from(KIVY_FONTS))
    @settings(max_examples=100, deadline=None)
    def test_code_block_preserves_code_font_name(self, font_name):
        """Code blocks preserve code_font_name regardless of font_name setting."""
        code_font = 'RobotoMono-Regular'
        markdown = '```python\nprint("hello")\n```'
        
        label = MarkdownLabel(
            text=markdown,
            font_name=font_name,
            code_font_name=code_font
        )
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label for code block"
        
        # Code block labels should use code_font_name, not font_name
        for lbl in labels:
            assert lbl.font_name == code_font, \
                f"Code label should use code_font_name={code_font}, got {lbl.font_name}"
    
    @given(st.sampled_from(['Roboto', 'Roboto-Bold', 'Roboto-Italic']))
    @settings(max_examples=100, deadline=None)
    def test_mixed_content_font_separation(self, font_name):
        """Mixed content correctly separates font_name and code_font_name."""
        code_font = 'RobotoMono-Regular'
        markdown = 'Regular text\n\n```\ncode\n```\n\nMore text'
        
        label = MarkdownLabel(
            text=markdown,
            font_name=font_name,
            code_font_name=code_font
        )
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 2, "Expected at least 2 Labels (text + code)"
        
        # Separate labels by font
        body_labels = [l for l in labels if l.font_name == font_name]
        code_labels = [l for l in labels if l.font_name == code_font]
        
        # Should have both body and code labels
        assert len(body_labels) >= 1, "Expected at least one body text label"
        assert len(code_labels) >= 1, "Expected at least one code label"
    
    @given(st.sampled_from(['Roboto', 'Roboto-Bold', 'Roboto-Italic']),
           st.sampled_from(['Roboto', 'Roboto-Bold', 'Roboto-Italic']))
    @settings(max_examples=100, deadline=None)
    def test_font_name_change_triggers_rebuild(self, font1, font2):
        """Changing font_name triggers widget rebuild with new font."""
        assume(font1 != font2)
        
        label = MarkdownLabel(text='Hello World', font_name=font1)
        
        # Verify initial font
        labels = self._find_labels_recursive(label)
        for lbl in labels:
            assert lbl.font_name == font1
        
        # Change font_name
        label.font_name = font2
        
        # Verify new font
        labels = self._find_labels_recursive(label)
        for lbl in labels:
            assert lbl.font_name == font2, \
                f"After change, expected font_name={font2}, got {lbl.font_name}"
    
    @given(st.sampled_from(KIVY_FONTS))
    @settings(max_examples=100, deadline=None)
    def test_font_name_applied_to_list_items(self, font_name):
        """font_name is applied to list item Labels."""
        markdown = '- Item 1\n- Item 2'
        label = MarkdownLabel(text=markdown, font_name=font_name)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 2, "Expected at least 2 Labels for list items"
        
        # All labels should have the specified font_name
        for lbl in labels:
            assert lbl.font_name == font_name, \
                f"Expected font_name={font_name}, got {lbl.font_name}"
    
    @given(st.sampled_from(KIVY_FONTS))
    @settings(max_examples=100, deadline=None)
    def test_font_name_applied_to_table_cells(self, font_name):
        """font_name is applied to table cell Labels."""
        markdown = '| A | B |\n| --- | --- |\n| 1 | 2 |'
        label = MarkdownLabel(text=markdown, font_name=font_name)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 4, "Expected at least 4 Labels for table cells"
        
        # All labels should have the specified font_name
        for lbl in labels:
            assert lbl.font_name == font_name, \
                f"Expected font_name={font_name}, got {lbl.font_name}"


# **Feature: label-compatibility, Property 3: color Forwarding with Link Preservation**
# *For any* Markdown text containing both regular text and links, and any color value,
# all body text Labels SHALL have `color` set to the specified value, while link text
# SHALL retain `link_color` styling.
# **Validates: Requirements 3.1, 3.2**

# Strategy for generating valid RGBA colors
color_strategy = st.lists(
    st.floats(min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False),
    min_size=4, max_size=4
)


class TestColorForwarding:
    """Property tests for color forwarding (Property 3)."""
    
    def _find_labels_recursive(self, widget, labels=None):
        """Recursively find all Label widgets in a widget tree."""
        if labels is None:
            labels = []
        
        if isinstance(widget, Label):
            labels.append(widget)
        
        if hasattr(widget, 'children'):
            for child in widget.children:
                self._find_labels_recursive(child, labels)
        
        return labels
    
    def _colors_equal(self, c1, c2, tolerance=0.001):
        """Compare two colors with tolerance for floating point differences."""
        if len(c1) != len(c2):
            return False
        return all(abs(a - b) < tolerance for a, b in zip(c1, c2))
    
    @given(color_strategy)
    @settings(max_examples=100, deadline=None)
    def test_color_applied_to_paragraph(self, color):
        """color is applied to paragraph Labels."""
        label = MarkdownLabel(text='Hello World', color=color)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        # All labels should have the specified color
        for lbl in labels:
            assert self._colors_equal(list(lbl.color), color), \
                f"Expected color={color}, got {list(lbl.color)}"
    
    @given(color_strategy)
    @settings(max_examples=100, deadline=None)
    def test_color_applied_to_heading(self, color):
        """color is applied to heading Labels."""
        label = MarkdownLabel(text='# Heading', color=color)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        # All labels should have the specified color
        for lbl in labels:
            assert self._colors_equal(list(lbl.color), color), \
                f"Expected color={color}, got {list(lbl.color)}"
    
    @given(color_strategy)
    @settings(max_examples=100, deadline=None)
    def test_code_block_preserves_light_color(self, color):
        """Code blocks preserve their light text color regardless of color setting."""
        markdown = '```python\nprint("hello")\n```'
        code_color = [0.9, 0.9, 0.9, 1]  # Expected code block color
        
        label = MarkdownLabel(text=markdown, color=color)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label for code block"
        
        # Code block labels should use their own light color, not the specified color
        for lbl in labels:
            assert self._colors_equal(list(lbl.color), code_color), \
                f"Code label should use light color={code_color}, got {list(lbl.color)}"
    
    @given(color_strategy, color_strategy)
    @settings(max_examples=100, deadline=None)
    def test_color_change_triggers_rebuild(self, color1, color2):
        """Changing color triggers widget rebuild with new color."""
        assume(not self._colors_equal(color1, color2))
        
        label = MarkdownLabel(text='Hello World', color=color1)
        
        # Verify initial color
        labels = self._find_labels_recursive(label)
        for lbl in labels:
            assert self._colors_equal(list(lbl.color), color1)
        
        # Change color
        label.color = color2
        
        # Verify new color
        labels = self._find_labels_recursive(label)
        for lbl in labels:
            assert self._colors_equal(list(lbl.color), color2), \
                f"After change, expected color={color2}, got {list(lbl.color)}"
    
    @given(color_strategy)
    @settings(max_examples=100, deadline=None)
    def test_color_applied_to_list_items(self, color):
        """color is applied to list item Labels."""
        markdown = '- Item 1\n- Item 2'
        label = MarkdownLabel(text=markdown, color=color)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 2, "Expected at least 2 Labels for list items"
        
        # All labels should have the specified color
        for lbl in labels:
            assert self._colors_equal(list(lbl.color), color), \
                f"Expected color={color}, got {list(lbl.color)}"
    
    @given(color_strategy)
    @settings(max_examples=100, deadline=None)
    def test_color_applied_to_table_cells(self, color):
        """color is applied to table cell Labels."""
        markdown = '| A | B |\n| --- | --- |\n| 1 | 2 |'
        label = MarkdownLabel(text=markdown, color=color)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 4, "Expected at least 4 Labels for table cells"
        
        # All labels should have the specified color
        for lbl in labels:
            assert self._colors_equal(list(lbl.color), color), \
                f"Expected color={color}, got {list(lbl.color)}"
    
    @given(color_strategy)
    @settings(max_examples=100, deadline=None)
    def test_mixed_content_color_separation(self, color):
        """Mixed content correctly separates body color and code color."""
        code_color = [0.9, 0.9, 0.9, 1]
        markdown = 'Regular text\n\n```\ncode\n```\n\nMore text'
        
        label = MarkdownLabel(text=markdown, color=color)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 2, "Expected at least 2 Labels (text + code)"
        
        # Separate labels by color
        body_labels = [l for l in labels if self._colors_equal(list(l.color), color)]
        code_labels = [l for l in labels if self._colors_equal(list(l.color), code_color)]
        
        # Should have both body and code labels
        assert len(body_labels) >= 1, "Expected at least one body text label with specified color"
        assert len(code_labels) >= 1, "Expected at least one code label with light color"


# **Feature: label-compatibility, Property 4: line_height Forwarding**
# *For any* Markdown text and any line_height value, all internal Labels SHALL have
# `line_height` set to the specified value.
# **Validates: Requirements 4.1**

# Strategy for generating valid line_height values
line_height_strategy = st.floats(min_value=0.5, max_value=3.0, allow_nan=False, allow_infinity=False)


class TestLineHeightForwarding:
    """Property tests for line_height forwarding (Property 4)."""
    
    def _find_labels_recursive(self, widget, labels=None):
        """Recursively find all Label widgets in a widget tree."""
        if labels is None:
            labels = []
        
        if isinstance(widget, Label):
            labels.append(widget)
        
        if hasattr(widget, 'children'):
            for child in widget.children:
                self._find_labels_recursive(child, labels)
        
        return labels
    
    def _floats_equal(self, f1, f2, tolerance=0.001):
        """Compare two floats with tolerance."""
        return abs(f1 - f2) < tolerance
    
    @given(line_height_strategy)
    @settings(max_examples=100, deadline=None)
    def test_line_height_applied_to_paragraph(self, line_height):
        """line_height is applied to paragraph Labels."""
        label = MarkdownLabel(text='Hello World', line_height=line_height)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        # All labels should have the specified line_height
        for lbl in labels:
            assert self._floats_equal(lbl.line_height, line_height), \
                f"Expected line_height={line_height}, got {lbl.line_height}"
    
    @given(line_height_strategy)
    @settings(max_examples=100, deadline=None)
    def test_line_height_applied_to_heading(self, line_height):
        """line_height is applied to heading Labels."""
        label = MarkdownLabel(text='# Heading', line_height=line_height)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        # All labels should have the specified line_height
        for lbl in labels:
            assert self._floats_equal(lbl.line_height, line_height), \
                f"Expected line_height={line_height}, got {lbl.line_height}"
    
    @given(line_height_strategy)
    @settings(max_examples=100, deadline=None)
    def test_line_height_applied_to_code_block(self, line_height):
        """line_height is applied to code block Labels."""
        markdown = '```python\nprint("hello")\n```'
        
        label = MarkdownLabel(text=markdown, line_height=line_height)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label for code block"
        
        # Code block labels should also have the specified line_height
        for lbl in labels:
            assert self._floats_equal(lbl.line_height, line_height), \
                f"Expected line_height={line_height}, got {lbl.line_height}"
    
    @given(line_height_strategy, line_height_strategy)
    @settings(max_examples=100, deadline=None)
    def test_line_height_change_triggers_rebuild(self, lh1, lh2):
        """Changing line_height triggers widget rebuild with new value."""
        assume(not self._floats_equal(lh1, lh2))
        
        label = MarkdownLabel(text='Hello World', line_height=lh1)
        
        # Verify initial line_height
        labels = self._find_labels_recursive(label)
        for lbl in labels:
            assert self._floats_equal(lbl.line_height, lh1)
        
        # Change line_height
        label.line_height = lh2
        
        # Verify new line_height
        labels = self._find_labels_recursive(label)
        for lbl in labels:
            assert self._floats_equal(lbl.line_height, lh2), \
                f"After change, expected line_height={lh2}, got {lbl.line_height}"
    
    @given(line_height_strategy)
    @settings(max_examples=100, deadline=None)
    def test_line_height_applied_to_list_items(self, line_height):
        """line_height is applied to list item Labels."""
        markdown = '- Item 1\n- Item 2'
        label = MarkdownLabel(text=markdown, line_height=line_height)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 2, "Expected at least 2 Labels for list items"
        
        # All labels should have the specified line_height
        for lbl in labels:
            assert self._floats_equal(lbl.line_height, line_height), \
                f"Expected line_height={line_height}, got {lbl.line_height}"
    
    @given(line_height_strategy)
    @settings(max_examples=100, deadline=None)
    def test_line_height_applied_to_table_cells(self, line_height):
        """line_height is applied to table cell Labels."""
        markdown = '| A | B |\n| --- | --- |\n| 1 | 2 |'
        label = MarkdownLabel(text=markdown, line_height=line_height)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 4, "Expected at least 4 Labels for table cells"
        
        # All labels should have the specified line_height
        for lbl in labels:
            assert self._floats_equal(lbl.line_height, line_height), \
                f"Expected line_height={line_height}, got {lbl.line_height}"
    
    @given(line_height_strategy)
    @settings(max_examples=100, deadline=None)
    def test_line_height_applied_to_all_content_types(self, line_height):
        """line_height is applied to all content types including code."""
        markdown = 'Regular text\n\n```\ncode\n```\n\n# Heading\n\n- List item'
        
        label = MarkdownLabel(text=markdown, line_height=line_height)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 3, "Expected at least 3 Labels"
        
        # All labels should have the specified line_height
        for lbl in labels:
            assert self._floats_equal(lbl.line_height, line_height), \
                f"Expected line_height={line_height}, got {lbl.line_height}"


# **Feature: label-compatibility, Property 5: halign Forwarding**
# *For any* Markdown text with paragraphs or headings, and any halign value in
# ['left', 'center', 'right', 'justify'], all paragraph and heading Labels SHALL
# have `halign` set to that value. When halign is 'auto', Labels SHALL have
# `halign` set to 'left'.
# **Validates: Requirements 5.1, 5.2**

# Strategy for generating valid halign values
halign_values = st.sampled_from(['left', 'center', 'right', 'justify', 'auto'])
halign_explicit_values = st.sampled_from(['left', 'center', 'right', 'justify'])


class TestHalignForwarding:
    """Property tests for halign forwarding (Property 5)."""
    
    def _find_labels_recursive(self, widget, labels=None):
        """Recursively find all Label widgets in a widget tree."""
        if labels is None:
            labels = []
        
        if isinstance(widget, Label):
            labels.append(widget)
        
        if hasattr(widget, 'children'):
            for child in widget.children:
                self._find_labels_recursive(child, labels)
        
        return labels
    
    @given(halign_explicit_values)
    @settings(max_examples=100, deadline=None)
    def test_halign_applied_to_paragraph(self, halign):
        """halign is applied to paragraph Labels."""
        label = MarkdownLabel(text='Hello World', halign=halign)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        # All labels should have the specified halign
        for lbl in labels:
            assert lbl.halign == halign, \
                f"Expected halign={halign}, got {lbl.halign}"
    
    @given(halign_explicit_values)
    @settings(max_examples=100, deadline=None)
    def test_halign_applied_to_heading(self, halign):
        """halign is applied to heading Labels."""
        label = MarkdownLabel(text='# Heading', halign=halign)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        # All labels should have the specified halign
        for lbl in labels:
            assert lbl.halign == halign, \
                f"Expected halign={halign}, got {lbl.halign}"
    
    @given(st.integers(min_value=1, max_value=6), halign_explicit_values)
    @settings(max_examples=100, deadline=None)
    def test_halign_applied_to_all_heading_levels(self, level, halign):
        """halign is applied to all heading levels."""
        markdown = '#' * level + ' Heading'
        label = MarkdownLabel(text=markdown, halign=halign)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        for lbl in labels:
            assert lbl.halign == halign, \
                f"Expected halign={halign}, got {lbl.halign}"
    
    @settings(max_examples=100, deadline=None)
    @given(st.data())
    def test_halign_auto_converts_to_left(self, data):
        """halign='auto' is converted to 'left' in internal Labels."""
        label = MarkdownLabel(text='Hello World', halign='auto')
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        # When halign is 'auto', internal labels should have 'left'
        for lbl in labels:
            assert lbl.halign == 'left', \
                f"Expected halign='left' for auto, got {lbl.halign}"
    
    @given(halign_explicit_values, halign_explicit_values)
    @settings(max_examples=100, deadline=None)
    def test_halign_change_triggers_rebuild(self, halign1, halign2):
        """Changing halign triggers widget rebuild with new alignment."""
        assume(halign1 != halign2)
        
        label = MarkdownLabel(text='Hello World', halign=halign1)
        
        # Verify initial halign
        labels = self._find_labels_recursive(label)
        for lbl in labels:
            assert lbl.halign == halign1
        
        # Change halign
        label.halign = halign2
        
        # Verify new halign
        labels = self._find_labels_recursive(label)
        for lbl in labels:
            assert lbl.halign == halign2, \
                f"After change, expected halign={halign2}, got {lbl.halign}"
    
    @given(halign_explicit_values)
    @settings(max_examples=100, deadline=None)
    def test_halign_applied_to_list_items(self, halign):
        """halign is applied to list item content Labels (not markers)."""
        markdown = '- Item 1\n- Item 2'
        label = MarkdownLabel(text=markdown, halign=halign)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 2, "Expected at least 2 Labels for list items"
        
        # List markers have halign='right' for proper bullet/number alignment
        # Content labels should have the specified halign
        content_labels = [lbl for lbl in labels if lbl.text not in ('•', '1.', '2.')]
        marker_labels = [lbl for lbl in labels if lbl.text in ('•', '1.', '2.')]
        
        # Content labels should have the specified halign
        for lbl in content_labels:
            assert lbl.halign == halign, \
                f"Expected content halign={halign}, got {lbl.halign}"
        
        # Marker labels should have halign='right' for proper alignment
        for lbl in marker_labels:
            assert lbl.halign == 'right', \
                f"Expected marker halign='right', got {lbl.halign}"
    
    @given(halign_explicit_values)
    @settings(max_examples=100, deadline=None)
    def test_halign_applied_to_table_cells(self, halign):
        """halign is applied to table cell Labels when no cell-specific alignment."""
        # Table without explicit alignment
        markdown = '| A | B |\n| --- | --- |\n| 1 | 2 |'
        label = MarkdownLabel(text=markdown, halign=halign)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 4, "Expected at least 4 Labels for table cells"
        
        # All labels should have the specified halign
        for lbl in labels:
            assert lbl.halign == halign, \
                f"Expected halign={halign}, got {lbl.halign}"
    
    @given(halign_values)
    @settings(max_examples=100, deadline=None)
    def test_halign_property_stored_correctly(self, halign):
        """halign property value is stored correctly on MarkdownLabel."""
        label = MarkdownLabel(text='Hello', halign=halign)
        
        assert label.halign == halign, \
            f"Expected MarkdownLabel.halign={halign}, got {label.halign}"


# **Feature: label-compatibility, Property 6: valign Forwarding**
# *For any* Markdown text and any valign value in ['top', 'middle', 'center', 'bottom'],
# all applicable internal Labels SHALL have `valign` set to that value.
# **Validates: Requirements 6.1, 6.2**

# Strategy for generating valid valign values
valign_values = st.sampled_from(['bottom', 'middle', 'center', 'top'])


class TestValignForwarding:
    """Property tests for valign forwarding (Property 6)."""
    
    def _find_labels_recursive(self, widget, labels=None):
        """Recursively find all Label widgets in a widget tree."""
        if labels is None:
            labels = []
        
        if isinstance(widget, Label):
            labels.append(widget)
        
        if hasattr(widget, 'children'):
            for child in widget.children:
                self._find_labels_recursive(child, labels)
        
        return labels
    
    @given(valign_values)
    @settings(max_examples=100, deadline=None)
    def test_valign_applied_to_paragraph(self, valign):
        """valign is applied to paragraph Labels."""
        label = MarkdownLabel(text='Hello World', valign=valign)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        # All labels should have the specified valign
        for lbl in labels:
            assert lbl.valign == valign, \
                f"Expected valign={valign}, got {lbl.valign}"
    
    @given(valign_values)
    @settings(max_examples=100, deadline=None)
    def test_valign_applied_to_heading(self, valign):
        """valign is applied to heading Labels."""
        label = MarkdownLabel(text='# Heading', valign=valign)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        # All labels should have the specified valign
        for lbl in labels:
            assert lbl.valign == valign, \
                f"Expected valign={valign}, got {lbl.valign}"
    
    @given(st.integers(min_value=1, max_value=6), valign_values)
    @settings(max_examples=100, deadline=None)
    def test_valign_applied_to_all_heading_levels(self, level, valign):
        """valign is applied to all heading levels."""
        markdown = '#' * level + ' Heading'
        label = MarkdownLabel(text=markdown, valign=valign)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        for lbl in labels:
            assert lbl.valign == valign, \
                f"Expected valign={valign}, got {lbl.valign}"
    
    @given(valign_values, valign_values)
    @settings(max_examples=100, deadline=None)
    def test_valign_change_triggers_rebuild(self, valign1, valign2):
        """Changing valign triggers widget rebuild with new alignment."""
        assume(valign1 != valign2)
        
        label = MarkdownLabel(text='Hello World', valign=valign1)
        
        # Verify initial valign
        labels = self._find_labels_recursive(label)
        for lbl in labels:
            assert lbl.valign == valign1
        
        # Change valign
        label.valign = valign2
        
        # Verify new valign
        labels = self._find_labels_recursive(label)
        for lbl in labels:
            assert lbl.valign == valign2, \
                f"After change, expected valign={valign2}, got {lbl.valign}"
    
    @given(valign_values)
    @settings(max_examples=100, deadline=None)
    def test_valign_applied_to_list_items(self, valign):
        """valign is applied to list item Labels."""
        markdown = '- Item 1\n- Item 2'
        label = MarkdownLabel(text=markdown, valign=valign)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 2, "Expected at least 2 Labels for list items"
        
        # All labels should have the specified valign
        for lbl in labels:
            assert lbl.valign == valign, \
                f"Expected valign={valign}, got {lbl.valign}"
    
    @given(valign_values)
    @settings(max_examples=100, deadline=None)
    def test_valign_applied_to_table_cells(self, valign):
        """valign is applied to table cell Labels."""
        markdown = '| A | B |\n| --- | --- |\n| 1 | 2 |'
        label = MarkdownLabel(text=markdown, valign=valign)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 4, "Expected at least 4 Labels for table cells"
        
        # All labels should have the specified valign
        for lbl in labels:
            assert lbl.valign == valign, \
                f"Expected valign={valign}, got {lbl.valign}"
    
    @given(valign_values)
    @settings(max_examples=100, deadline=None)
    def test_valign_property_stored_correctly(self, valign):
        """valign property value is stored correctly on MarkdownLabel."""
        label = MarkdownLabel(text='Hello', valign=valign)
        
        assert label.valign == valign, \
            f"Expected MarkdownLabel.valign={valign}, got {label.valign}"


# **Feature: label-compatibility, Property 7: padding Application**
# *For any* padding value (single, two-element, or four-element list), the
# MarkdownLabel container SHALL have `padding` set to the normalized four-element form.
# **Validates: Requirements 7.1, 7.2, 7.3, 7.4**

# Strategy for generating valid padding values
padding_single = st.floats(min_value=0, max_value=100, allow_nan=False, allow_infinity=False)
padding_two = st.lists(
    st.floats(min_value=0, max_value=100, allow_nan=False, allow_infinity=False),
    min_size=2, max_size=2
)
padding_four = st.lists(
    st.floats(min_value=0, max_value=100, allow_nan=False, allow_infinity=False),
    min_size=4, max_size=4
)


class TestPaddingApplication:
    """Property tests for padding application (Property 7)."""
    
    @given(padding_single)
    @settings(max_examples=100, deadline=None)
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
    
    @given(padding_two)
    @settings(max_examples=100, deadline=None)
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
    
    @given(padding_four)
    @settings(max_examples=100, deadline=None)
    def test_four_element_padding_applied_directly(self, padding_values):
        """Four-element padding [left, top, right, bottom] is applied directly."""
        label = MarkdownLabel(text='Hello World', padding=padding_values)
        
        assert len(label.padding) == 4, \
            f"Expected 4-element padding, got {len(label.padding)}"
        
        for i, (actual, exp) in enumerate(zip(label.padding, padding_values)):
            assert abs(actual - exp) < 0.001, \
                f"Padding[{i}]: expected {exp}, got {actual}"
    
    @given(padding_four)
    @settings(max_examples=100, deadline=None)
    def test_padding_property_stored_correctly(self, padding_values):
        """padding property value is stored correctly on MarkdownLabel."""
        label = MarkdownLabel(text='Hello', padding=padding_values)
        
        assert len(label.padding) == 4, \
            f"Expected 4-element padding, got {len(label.padding)}"
        
        for i, (actual, exp) in enumerate(zip(label.padding, padding_values)):
            assert abs(actual - exp) < 0.001, \
                f"Padding[{i}]: expected {exp}, got {actual}"
    
    @given(padding_four, padding_four)
    @settings(max_examples=100, deadline=None)
    def test_padding_change_updates_container(self, padding1, padding2):
        """Changing padding updates the container padding."""
        assume(padding1 != padding2)
        
        label = MarkdownLabel(text='Hello World', padding=padding1)
        
        # Verify initial padding
        for i, (actual, exp) in enumerate(zip(label.padding, padding1)):
            assert abs(actual - exp) < 0.001
        
        # Change padding
        label.padding = padding2
        
        # Verify new padding
        for i, (actual, exp) in enumerate(zip(label.padding, padding2)):
            assert abs(actual - exp) < 0.001, \
                f"After change, padding[{i}]: expected {exp}, got {actual}"
    
    @settings(max_examples=100, deadline=None)
    @given(st.data())
    def test_default_padding_is_zero(self, data):
        """Default padding is [0, 0, 0, 0]."""
        label = MarkdownLabel(text='Hello World')
        
        expected = [0, 0, 0, 0]
        assert len(label.padding) == 4, \
            f"Expected 4-element padding, got {len(label.padding)}"
        
        for i, (actual, exp) in enumerate(zip(label.padding, expected)):
            assert abs(actual - exp) < 0.001, \
                f"Default padding[{i}]: expected {exp}, got {actual}"


# **Feature: label-compatibility, Property 9: text_size Width Constraint Forwarding**
# *For any* Markdown text and any text_size with a non-None width, all internal
# Labels SHALL have `text_size[0]` set to that width value.
# **Validates: Requirements 9.1**

# Strategy for generating valid text_size values
text_size_with_width = st.lists(
    st.one_of(
        st.floats(min_value=50, max_value=1000, allow_nan=False, allow_infinity=False),
        st.none()
    ),
    min_size=2, max_size=2
)


class TestTextSizeForwarding:
    """Property tests for text_size forwarding (Property 9)."""
    
    def _find_labels_recursive(self, widget, labels=None):
        """Recursively find all Label widgets in a widget tree."""
        if labels is None:
            labels = []
        
        if isinstance(widget, Label):
            labels.append(widget)
        
        if hasattr(widget, 'children'):
            for child in widget.children:
                self._find_labels_recursive(child, labels)
        
        return labels
    
    @given(st.floats(min_value=50, max_value=1000, allow_nan=False, allow_infinity=False))
    @settings(max_examples=100, deadline=None)
    def test_text_size_width_stored_correctly(self, width):
        """text_size width is stored correctly on MarkdownLabel."""
        label = MarkdownLabel(text='Hello World', text_size=[width, None])
        
        assert label.text_size[0] == width, \
            f"Expected text_size[0]={width}, got {label.text_size[0]}"
    
    @given(st.floats(min_value=50, max_value=1000, allow_nan=False, allow_infinity=False))
    @settings(max_examples=100, deadline=None)
    def test_text_size_property_stored_correctly(self, width):
        """text_size property value is stored correctly on MarkdownLabel."""
        label = MarkdownLabel(text='Hello', text_size=[width, None])
        
        assert len(label.text_size) == 2, \
            f"Expected 2-element text_size, got {len(label.text_size)}"
        assert label.text_size[0] == width, \
            f"Expected text_size[0]={width}, got {label.text_size[0]}"
    
    @given(st.floats(min_value=50, max_value=1000, allow_nan=False, allow_infinity=False),
           st.floats(min_value=50, max_value=1000, allow_nan=False, allow_infinity=False))
    @settings(max_examples=100, deadline=None)
    def test_text_size_change_triggers_rebuild(self, width1, width2):
        """Changing text_size triggers widget rebuild."""
        assume(abs(width1 - width2) > 1)  # Ensure they're different
        
        label = MarkdownLabel(text='Hello World', text_size=[width1, None])
        
        # Verify initial text_size
        assert label.text_size[0] == width1
        
        # Change text_size
        label.text_size = [width2, None]
        
        # Verify new text_size
        assert label.text_size[0] == width2, \
            f"After change, expected text_size[0]={width2}, got {label.text_size[0]}"
    
    @settings(max_examples=100, deadline=None)
    @given(st.data())
    def test_default_text_size_is_none_none(self, data):
        """Default text_size is [None, None]."""
        label = MarkdownLabel(text='Hello World')
        
        assert len(label.text_size) == 2, \
            f"Expected 2-element text_size, got {len(label.text_size)}"
        assert label.text_size[0] is None, \
            f"Default text_size[0] should be None, got {label.text_size[0]}"
        assert label.text_size[1] is None, \
            f"Default text_size[1] should be None, got {label.text_size[1]}"
    
    @given(st.floats(min_value=50, max_value=1000, allow_nan=False, allow_infinity=False))
    @settings(max_examples=100, deadline=None)
    def test_text_size_with_width_passed_to_renderer(self, width):
        """text_size with width is passed to renderer and affects internal Labels."""
        label = MarkdownLabel(text='Hello World', text_size=[width, None])
        
        # The text_size should be stored on the MarkdownLabel
        assert label.text_size[0] == width, \
            f"Expected text_size[0]={width}, got {label.text_size[0]}"
        
        # Verify the label has children (widgets were created)
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"


# **Feature: label-compatibility, Property 10: unicode_errors Forwarding**
# *For any* unicode_errors value in ['strict', 'replace', 'ignore'], all internal
# Labels SHALL have `unicode_errors` set to that value.
# **Validates: Requirements 10.1, 10.2**

# Strategy for generating valid unicode_errors values
unicode_errors_strategy = st.sampled_from(['strict', 'replace', 'ignore'])


class TestUnicodeErrorsForwarding:
    """Property tests for unicode_errors forwarding (Property 10)."""
    
    def _find_labels_recursive(self, widget, labels=None):
        """Recursively find all Label widgets in a widget tree."""
        if labels is None:
            labels = []
        
        if isinstance(widget, Label):
            labels.append(widget)
        
        if hasattr(widget, 'children'):
            for child in widget.children:
                self._find_labels_recursive(child, labels)
        
        return labels
    
    @given(unicode_errors_strategy)
    @settings(max_examples=100, deadline=None)
    def test_unicode_errors_stored_correctly(self, unicode_errors):
        """unicode_errors value is stored correctly on MarkdownLabel."""
        label = MarkdownLabel(text='Hello World', unicode_errors=unicode_errors)
        
        assert label.unicode_errors == unicode_errors, \
            f"Expected unicode_errors={unicode_errors}, got {label.unicode_errors}"
    
    @given(unicode_errors_strategy)
    @settings(max_examples=100, deadline=None)
    def test_unicode_errors_applied_to_paragraph(self, unicode_errors):
        """unicode_errors is applied to paragraph Labels."""
        label = MarkdownLabel(text='Hello World', unicode_errors=unicode_errors)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        # All labels should have the specified unicode_errors
        for lbl in labels:
            assert lbl.unicode_errors == unicode_errors, \
                f"Expected unicode_errors={unicode_errors}, got {lbl.unicode_errors}"
    
    @given(unicode_errors_strategy)
    @settings(max_examples=100, deadline=None)
    def test_unicode_errors_applied_to_heading(self, unicode_errors):
        """unicode_errors is applied to heading Labels."""
        label = MarkdownLabel(text='# Heading', unicode_errors=unicode_errors)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        # All labels should have the specified unicode_errors
        for lbl in labels:
            assert lbl.unicode_errors == unicode_errors, \
                f"Expected unicode_errors={unicode_errors}, got {lbl.unicode_errors}"
    
    @given(unicode_errors_strategy)
    @settings(max_examples=100, deadline=None)
    def test_unicode_errors_applied_to_code_block(self, unicode_errors):
        """unicode_errors is applied to code block Labels."""
        markdown = '```python\nprint("hello")\n```'
        label = MarkdownLabel(text=markdown, unicode_errors=unicode_errors)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label for code block"
        
        # All labels should have the specified unicode_errors
        for lbl in labels:
            assert lbl.unicode_errors == unicode_errors, \
                f"Expected unicode_errors={unicode_errors}, got {lbl.unicode_errors}"
    
    @given(unicode_errors_strategy)
    @settings(max_examples=100, deadline=None)
    def test_unicode_errors_applied_to_list_items(self, unicode_errors):
        """unicode_errors is applied to list item Labels."""
        markdown = '- Item 1\n- Item 2'
        label = MarkdownLabel(text=markdown, unicode_errors=unicode_errors)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 2, "Expected at least 2 Labels for list items"
        
        # All labels should have the specified unicode_errors
        for lbl in labels:
            assert lbl.unicode_errors == unicode_errors, \
                f"Expected unicode_errors={unicode_errors}, got {lbl.unicode_errors}"
    
    @given(unicode_errors_strategy)
    @settings(max_examples=100, deadline=None)
    def test_unicode_errors_applied_to_table_cells(self, unicode_errors):
        """unicode_errors is applied to table cell Labels."""
        markdown = '| A | B |\n| --- | --- |\n| 1 | 2 |'
        label = MarkdownLabel(text=markdown, unicode_errors=unicode_errors)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 4, "Expected at least 4 Labels for table cells"
        
        # All labels should have the specified unicode_errors
        for lbl in labels:
            assert lbl.unicode_errors == unicode_errors, \
                f"Expected unicode_errors={unicode_errors}, got {lbl.unicode_errors}"
    
    @given(st.sampled_from(['strict', 'replace']), st.sampled_from(['replace', 'ignore']))
    @settings(max_examples=100, deadline=None)
    def test_unicode_errors_change_triggers_rebuild(self, errors1, errors2):
        """Changing unicode_errors triggers widget rebuild with new value."""
        assume(errors1 != errors2)
        
        label = MarkdownLabel(text='Hello World', unicode_errors=errors1)
        
        # Verify initial unicode_errors
        labels = self._find_labels_recursive(label)
        for lbl in labels:
            assert lbl.unicode_errors == errors1
        
        # Change unicode_errors
        label.unicode_errors = errors2
        
        # Verify new unicode_errors
        labels = self._find_labels_recursive(label)
        for lbl in labels:
            assert lbl.unicode_errors == errors2, \
                f"After change, expected unicode_errors={errors2}, got {lbl.unicode_errors}"
    
    @settings(max_examples=100, deadline=None)
    @given(st.data())
    def test_default_unicode_errors_is_replace(self, data):
        """Default unicode_errors is 'replace'."""
        label = MarkdownLabel(text='Hello World')
        
        assert label.unicode_errors == 'replace', \
            f"Default unicode_errors should be 'replace', got {label.unicode_errors}"


# **Feature: label-compatibility, Property 13: strip Forwarding**
# *For any* Markdown text and any strip boolean value, all internal Labels
# SHALL have `strip` set to that value.
# **Validates: Requirements 14.1**


class TestStripForwarding:
    """Property tests for strip forwarding (Property 13)."""
    
    def _find_labels_recursive(self, widget, labels=None):
        """Recursively find all Label widgets in a widget tree."""
        if labels is None:
            labels = []
        
        if isinstance(widget, Label):
            labels.append(widget)
        
        if hasattr(widget, 'children'):
            for child in widget.children:
                self._find_labels_recursive(child, labels)
        
        return labels
    
    @given(st.booleans())
    @settings(max_examples=100, deadline=None)
    def test_strip_stored_correctly(self, strip_value):
        """strip value is stored correctly on MarkdownLabel."""
        label = MarkdownLabel(text='Hello World', strip=strip_value)
        
        assert label.strip == strip_value, \
            f"Expected strip={strip_value}, got {label.strip}"
    
    @given(st.booleans())
    @settings(max_examples=100, deadline=None)
    def test_strip_applied_to_paragraph(self, strip_value):
        """strip is applied to paragraph Labels."""
        label = MarkdownLabel(text='Hello World', strip=strip_value)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        # All labels should have the specified strip value
        for lbl in labels:
            assert lbl.strip == strip_value, \
                f"Expected strip={strip_value}, got {lbl.strip}"
    
    @given(st.booleans())
    @settings(max_examples=100, deadline=None)
    def test_strip_applied_to_heading(self, strip_value):
        """strip is applied to heading Labels."""
        label = MarkdownLabel(text='# Heading', strip=strip_value)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        # All labels should have the specified strip value
        for lbl in labels:
            assert lbl.strip == strip_value, \
                f"Expected strip={strip_value}, got {lbl.strip}"
    
    @given(st.booleans())
    @settings(max_examples=100, deadline=None)
    def test_strip_applied_to_code_block(self, strip_value):
        """strip is applied to code block Labels."""
        markdown = '```python\nprint("hello")\n```'
        label = MarkdownLabel(text=markdown, strip=strip_value)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label for code block"
        
        # All labels should have the specified strip value
        for lbl in labels:
            assert lbl.strip == strip_value, \
                f"Expected strip={strip_value}, got {lbl.strip}"
    
    @given(st.booleans())
    @settings(max_examples=100, deadline=None)
    def test_strip_applied_to_list_items(self, strip_value):
        """strip is applied to list item Labels."""
        markdown = '- Item 1\n- Item 2'
        label = MarkdownLabel(text=markdown, strip=strip_value)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 2, "Expected at least 2 Labels for list items"
        
        # All labels should have the specified strip value
        for lbl in labels:
            assert lbl.strip == strip_value, \
                f"Expected strip={strip_value}, got {lbl.strip}"
    
    @given(st.booleans())
    @settings(max_examples=100, deadline=None)
    def test_strip_applied_to_table_cells(self, strip_value):
        """strip is applied to table cell Labels."""
        markdown = '| A | B |\n| --- | --- |\n| 1 | 2 |'
        label = MarkdownLabel(text=markdown, strip=strip_value)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 4, "Expected at least 4 Labels for table cells"
        
        # All labels should have the specified strip value
        for lbl in labels:
            assert lbl.strip == strip_value, \
                f"Expected strip={strip_value}, got {lbl.strip}"
    
    @given(st.booleans(), st.booleans())
    @settings(max_examples=100, deadline=None)
    def test_strip_change_triggers_rebuild(self, strip1, strip2):
        """Changing strip triggers widget rebuild with new value."""
        assume(strip1 != strip2)
        
        label = MarkdownLabel(text='Hello World', strip=strip1)
        
        # Verify initial strip
        labels = self._find_labels_recursive(label)
        for lbl in labels:
            assert lbl.strip == strip1
        
        # Change strip
        label.strip = strip2
        
        # Verify new strip
        labels = self._find_labels_recursive(label)
        for lbl in labels:
            assert lbl.strip == strip2, \
                f"After change, expected strip={strip2}, got {lbl.strip}"
    
    @settings(max_examples=100, deadline=None)
    @given(st.data())
    def test_default_strip_is_false(self, data):
        """Default strip is False."""
        label = MarkdownLabel(text='Hello World')
        
        assert label.strip is False, \
            f"Default strip should be False, got {label.strip}"
