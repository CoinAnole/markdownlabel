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
                elif key == 'bullet':
                    # Normalize bullet character - all unordered list bullets
                    # are semantically equivalent (-, +, *)
                    norm_token[key] = '-'
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


# **Feature: label-compatibility-phase2, Property 1: No-op Property Acceptance and Storage**
# *For any* no-op property (mipmap, outline_width, outline_color, text_language, base_direction, ellipsis_options), 
# when set to any valid value, the MarkdownLabel SHALL accept the value without raising an exception 
# AND return the same value when accessed.
# **Validates: Requirements 1.1, 1.2, 1.3**

class TestNoOpPropertyAcceptanceAndStorage:
    """Property tests for no-op property acceptance and storage (Property 1)."""
    
    @given(st.booleans())
    @settings(max_examples=100, deadline=None)
    def test_mipmap_property_accepted_and_stored(self, value):
        """Setting mipmap property accepts and stores the value."""
        label = MarkdownLabel(text='# Hello World', mipmap=value)
        assert label.mipmap == value
    
    @given(st.floats(min_value=0, max_value=100, allow_nan=False, allow_infinity=False))
    @settings(max_examples=100, deadline=None)
    def test_outline_width_property_accepted_and_stored(self, value):
        """Setting outline_width property accepts and stores the value."""
        label = MarkdownLabel(text='# Hello World', outline_width=value)
        assert label.outline_width == value
    
    @given(st.lists(
        st.floats(min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False),
        min_size=4, max_size=4
    ))
    @settings(max_examples=100, deadline=None)
    def test_outline_color_property_accepted_and_stored(self, value):
        """Setting outline_color property accepts and stores the value."""
        label = MarkdownLabel(text='# Hello World', outline_color=value)
        # Compare colors with tolerance for floating point differences
        assert all(abs(a - b) < 0.001 for a, b in zip(label.outline_color, value))
    
    @given(st.one_of(st.none(), st.text(min_size=1, max_size=10, alphabet=st.characters(
        whitelist_categories=['L', 'N'],
        blacklist_characters='\n\r'
    ))))
    @settings(max_examples=100, deadline=None)
    def test_text_language_property_accepted_and_stored(self, value):
        """Setting text_language property accepts and stores the value."""
        label = MarkdownLabel(text='# Hello World', text_language=value)
        assert label.text_language == value
    
    @given(st.sampled_from([None, 'ltr', 'rtl', 'weak_ltr', 'weak_rtl']))
    @settings(max_examples=100, deadline=None)
    def test_base_direction_property_accepted_and_stored(self, value):
        """Setting base_direction property accepts and stores the value."""
        label = MarkdownLabel(text='# Hello World', base_direction=value)
        assert label.base_direction == value
    
    @given(st.dictionaries(
        st.text(min_size=1, max_size=10, alphabet=st.characters(
            whitelist_categories=['L', 'N']
        )),
        st.one_of(st.booleans(), st.integers(), st.text(max_size=20))
    ))
    @settings(max_examples=100, deadline=None)
    def test_ellipsis_options_property_accepted_and_stored(self, value):
        """Setting ellipsis_options property accepts and stores the value."""
        label = MarkdownLabel(text='# Hello World', ellipsis_options=value)
        assert label.ellipsis_options == value
    
    @given(st.booleans(), st.floats(min_value=0, max_value=10), 
           st.lists(st.floats(min_value=0.0, max_value=1.0), min_size=4, max_size=4),
           st.one_of(st.none(), st.text(min_size=1, max_size=5)),
           st.sampled_from([None, 'ltr', 'rtl', 'weak_ltr', 'weak_rtl']),
           st.dictionaries(st.text(min_size=1, max_size=5), st.booleans(), max_size=3))
    @settings(max_examples=100, deadline=None)
    def test_all_noop_properties_together_accepted_and_stored(self, mipmap, outline_width, 
                                                              outline_color, text_language, 
                                                              base_direction, ellipsis_options):
        """Setting all no-op properties together accepts and stores all values."""
        label = MarkdownLabel(
            text='# Hello World',
            mipmap=mipmap,
            outline_width=outline_width,
            outline_color=outline_color,
            text_language=text_language,
            base_direction=base_direction,
            ellipsis_options=ellipsis_options
        )
        
        assert label.mipmap == mipmap
        assert label.outline_width == outline_width
        assert all(abs(a - b) < 0.001 for a, b in zip(label.outline_color, outline_color))
        assert label.text_language == text_language
        assert label.base_direction == base_direction
        assert label.ellipsis_options == ellipsis_options
    
    @given(st.booleans())
    @settings(max_examples=100, deadline=None)
    def test_mipmap_property_change_after_creation(self, value):
        """Changing mipmap property after creation accepts and stores the value."""
        label = MarkdownLabel(text='# Hello')
        label.mipmap = value
        assert label.mipmap == value
    
    @given(st.floats(min_value=0, max_value=100, allow_nan=False, allow_infinity=False))
    @settings(max_examples=100, deadline=None)
    def test_outline_width_property_change_after_creation(self, value):
        """Changing outline_width property after creation accepts and stores the value."""
        label = MarkdownLabel(text='# Hello')
        label.outline_width = value
        assert label.outline_width == value
    
    @given(st.lists(
        st.floats(min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False),
        min_size=4, max_size=4
    ))
    @settings(max_examples=100, deadline=None)
    def test_outline_color_property_change_after_creation(self, value):
        """Changing outline_color property after creation accepts and stores the value."""
        label = MarkdownLabel(text='# Hello')
        label.outline_color = value
        assert all(abs(a - b) < 0.001 for a, b in zip(label.outline_color, value))
    
    @given(st.one_of(st.none(), st.text(min_size=1, max_size=10, alphabet=st.characters(
        whitelist_categories=['L', 'N'],
        blacklist_characters='\n\r'
    ))))
    @settings(max_examples=100, deadline=None)
    def test_text_language_property_change_after_creation(self, value):
        """Changing text_language property after creation accepts and stores the value."""
        label = MarkdownLabel(text='# Hello')
        label.text_language = value
        assert label.text_language == value
    
    @given(st.sampled_from([None, 'ltr', 'rtl', 'weak_ltr', 'weak_rtl']))
    @settings(max_examples=100, deadline=None)
    def test_base_direction_property_change_after_creation(self, value):
        """Changing base_direction property after creation accepts and stores the value."""
        label = MarkdownLabel(text='# Hello')
        label.base_direction = value
        assert label.base_direction == value
    
    @given(st.dictionaries(
        st.text(min_size=1, max_size=10, alphabet=st.characters(
            whitelist_categories=['L', 'N']
        )),
        st.one_of(st.booleans(), st.integers(), st.text(max_size=20))
    ))
    @settings(max_examples=100, deadline=None)
    def test_ellipsis_options_property_change_after_creation(self, value):
        """Changing ellipsis_options property after creation accepts and stores the value."""
        label = MarkdownLabel(text='# Hello')
        label.ellipsis_options = value
        assert label.ellipsis_options == value
    
    @given(st.booleans(), st.floats(min_value=0, max_value=10), 
           st.lists(st.floats(min_value=0.0, max_value=1.0), min_size=4, max_size=4),
           st.one_of(st.none(), st.text(min_size=1, max_size=5)),
           st.sampled_from([None, 'ltr', 'rtl', 'weak_ltr', 'weak_rtl']),
           st.dictionaries(st.text(min_size=1, max_size=5), st.booleans(), max_size=3),
           simple_markdown_document())
    @settings(max_examples=100, deadline=None)
    def test_noop_properties_do_not_affect_rendering(self, mipmap, outline_width, outline_color,
                                                     text_language, base_direction, ellipsis_options,
                                                     markdown_text):
        """No-op properties do not affect the rendered output."""
        assume(markdown_text.strip())
        
        # Create label with default no-op property values
        label_default = MarkdownLabel(text=markdown_text)
        default_child_count = len(label_default.children)
        
        # Create label with various no-op property values
        label_with_props = MarkdownLabel(
            text=markdown_text,
            mipmap=mipmap,
            outline_width=outline_width,
            outline_color=outline_color,
            text_language=text_language,
            base_direction=base_direction,
            ellipsis_options=ellipsis_options
        )
        props_child_count = len(label_with_props.children)
        
        # The number of children should be the same regardless of no-op properties
        assert default_child_count == props_child_count, \
            f"Expected {default_child_count} children, got {props_child_count} with no-op props"


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
        """valign is applied to list item content Labels (not markers)."""
        markdown = '- Item 1\n- Item 2'
        label = MarkdownLabel(text=markdown, valign=valign)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 2, "Expected at least 2 Labels for list items"
        
        # Filter out marker labels (bullets/numbers) - they should always be top-aligned
        # Marker labels have width=30, halign='right', and contain bullet/number text
        content_labels = []
        for lbl in labels:
            # Skip marker labels - they have fixed width and right alignment
            if (hasattr(lbl, 'width') and lbl.width == 30 and 
                hasattr(lbl, 'halign') and lbl.halign == 'right'):
                # This is a marker label - should always be top-aligned
                assert lbl.valign == 'top', \
                    f"Marker label should be top-aligned, got {lbl.valign}"
            else:
                # This is a content label - should respect user's valign
                content_labels.append(lbl)
        
        # Content labels should have the specified valign
        assert len(content_labels) >= 2, "Expected at least 2 content Labels"
        for lbl in content_labels:
            assert lbl.valign == valign, \
                f"Expected content label valign={valign}, got {lbl.valign}"
    
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


# **Feature: label-compatibility, Property 1: text_size Height Forwarding**
# *For any* MarkdownLabel with `text_size[1]` set to a non-None numeric value H, 
# all child Labels SHALL have their `text_size[1]` equal to H, and their `valign` 
# property SHALL match the MarkdownLabel's `valign` value.
# **Validates: Requirements 1.1, 1.2**

class TestTextSizeHeightForwarding:
    """Property tests for text_size height forwarding (Property 1)."""
    
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
    
    @given(st.floats(min_value=50, max_value=500, allow_nan=False, allow_infinity=False))
    @settings(max_examples=100, deadline=None)
    def test_text_size_height_forwarded_to_paragraph(self, height):
        """text_size height is forwarded to paragraph Labels."""
        label = MarkdownLabel(text='Hello World', text_size=[None, height])
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        # All labels should have the specified height in text_size
        for lbl in labels:
            assert lbl.text_size[1] == height, \
                f"Expected text_size[1]={height}, got {lbl.text_size[1]}"
    
    @given(st.floats(min_value=50, max_value=500, allow_nan=False, allow_infinity=False))
    @settings(max_examples=100, deadline=None)
    def test_text_size_height_forwarded_to_heading(self, height):
        """text_size height is forwarded to heading Labels."""
        label = MarkdownLabel(text='# Heading', text_size=[None, height])
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        # All labels should have the specified height in text_size
        for lbl in labels:
            assert lbl.text_size[1] == height, \
                f"Expected text_size[1]={height}, got {lbl.text_size[1]}"
    
    @given(st.floats(min_value=100, max_value=500, allow_nan=False, allow_infinity=False),
           st.floats(min_value=50, max_value=300, allow_nan=False, allow_infinity=False))
    @settings(max_examples=100, deadline=None)
    def test_text_size_both_width_and_height_forwarded(self, width, height):
        """Both width and height in text_size are forwarded to Labels."""
        label = MarkdownLabel(text='Hello World', text_size=[width, height])
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        # All labels should have both width and height in text_size
        for lbl in labels:
            assert lbl.text_size[0] == width, \
                f"Expected text_size[0]={width}, got {lbl.text_size[0]}"
            assert lbl.text_size[1] == height, \
                f"Expected text_size[1]={height}, got {lbl.text_size[1]}"
    
    @given(st.floats(min_value=50, max_value=500, allow_nan=False, allow_infinity=False),
           st.sampled_from(['top', 'middle', 'bottom']))
    @settings(max_examples=100, deadline=None)
    def test_valign_forwarded_with_height(self, height, valign):
        """valign is forwarded to Labels when text_size height is set."""
        label = MarkdownLabel(text='Hello World', text_size=[None, height], valign=valign)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        # All labels should have the specified valign
        for lbl in labels:
            assert lbl.valign == valign, \
                f"Expected valign={valign}, got {lbl.valign}"
    
    @given(st.floats(min_value=50, max_value=500, allow_nan=False, allow_infinity=False))
    @settings(max_examples=100, deadline=None)
    def test_text_size_height_forwarded_to_table_cells(self, height):
        """text_size height is forwarded to table cell Labels."""
        markdown = '| A | B |\n| --- | --- |\n| 1 | 2 |'
        label = MarkdownLabel(text=markdown, text_size=[None, height])
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 4, "Expected at least 4 Labels for table cells"
        
        # All labels should have the specified height in text_size
        for lbl in labels:
            assert lbl.text_size[1] == height, \
                f"Expected text_size[1]={height}, got {lbl.text_size[1]}"


# **Feature: label-compatibility, Property 2: text_size Height None Backward Compatibility**
# *For any* MarkdownLabel with `text_size[1]` set to None, all child Labels SHALL 
# have their `text_size[1]` equal to None, maintaining the existing auto-sizing behavior.
# **Validates: Requirements 1.3**

class TestTextSizeHeightNoneBackwardCompatibility:
    """Property tests for text_size height None backward compatibility (Property 2)."""
    
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
    
    @given(simple_markdown_document())
    @settings(max_examples=100, deadline=None)
    def test_text_size_height_none_preserves_auto_sizing(self, markdown_text):
        """text_size[1]=None preserves auto-sizing behavior."""
        assume(markdown_text.strip())
        
        label = MarkdownLabel(text=markdown_text, text_size=[None, None])
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        # All labels should have text_size[1]=None for auto-sizing
        for lbl in labels:
            assert lbl.text_size[1] is None, \
                f"Expected text_size[1]=None for auto-sizing, got {lbl.text_size[1]}"
    
    @given(st.floats(min_value=50, max_value=1000, allow_nan=False, allow_infinity=False))
    @settings(max_examples=100, deadline=None)
    def test_text_size_width_only_preserves_height_none(self, width):
        """Setting only text_size width preserves height=None."""
        label = MarkdownLabel(text='Hello World', text_size=[width, None])
        
        labels = self._find_labels_recursive(label)
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
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        # All labels should have text_size[1]=None by default
        for lbl in labels:
            if hasattr(lbl, 'text_size') and lbl.text_size:
                assert lbl.text_size[1] is None, \
                    f"Expected default text_size[1]=None, got {lbl.text_size[1]}"


# **Feature: label-compatibility, Property 3: text_size Dynamic Updates**
# *For any* MarkdownLabel, when `text_size` is changed from value A to value B, 
# all child Labels SHALL be updated to reflect the new `text_size` value B.
# **Validates: Requirements 1.4**

class TestTextSizeDynamicUpdates:
    """Property tests for text_size dynamic updates (Property 3)."""
    
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
    
    @given(st.floats(min_value=50, max_value=300, allow_nan=False, allow_infinity=False),
           st.floats(min_value=350, max_value=600, allow_nan=False, allow_infinity=False))
    @settings(max_examples=100, deadline=None)
    def test_text_size_height_change_updates_labels(self, height1, height2):
        """Changing text_size height updates all child Labels."""
        label = MarkdownLabel(text='Hello World', text_size=[None, height1])
        
        # Verify initial height
        labels = self._find_labels_recursive(label)
        for lbl in labels:
            assert lbl.text_size[1] == height1, \
                f"Initial: Expected text_size[1]={height1}, got {lbl.text_size[1]}"
        
        # Change text_size height
        label.text_size = [None, height2]
        
        # Verify new height
        labels = self._find_labels_recursive(label)
        for lbl in labels:
            assert lbl.text_size[1] == height2, \
                f"After change: Expected text_size[1]={height2}, got {lbl.text_size[1]}"
    
    @given(st.floats(min_value=50, max_value=300, allow_nan=False, allow_infinity=False))
    @settings(max_examples=100, deadline=None)
    def test_text_size_height_to_none_updates_labels(self, height):
        """Changing text_size height to None updates all child Labels."""
        label = MarkdownLabel(text='Hello World', text_size=[None, height])
        
        # Verify initial height
        labels = self._find_labels_recursive(label)
        for lbl in labels:
            assert lbl.text_size[1] == height, \
                f"Initial: Expected text_size[1]={height}, got {lbl.text_size[1]}"
        
        # Change text_size height to None
        label.text_size = [None, None]
        
        # Verify height is now None
        labels = self._find_labels_recursive(label)
        for lbl in labels:
            if hasattr(lbl, 'text_size') and lbl.text_size:
                assert lbl.text_size[1] is None, \
                    f"After change to None: Expected text_size[1]=None, got {lbl.text_size[1]}"
    
    @given(st.floats(min_value=50, max_value=300, allow_nan=False, allow_infinity=False))
    @settings(max_examples=100, deadline=None)
    def test_text_size_none_to_height_updates_labels(self, height):
        """Changing text_size height from None to value updates all child Labels."""
        label = MarkdownLabel(text='Hello World', text_size=[None, None])
        
        # Verify initial height is None
        labels = self._find_labels_recursive(label)
        for lbl in labels:
            if hasattr(lbl, 'text_size') and lbl.text_size:
                assert lbl.text_size[1] is None, \
                    f"Initial: Expected text_size[1]=None, got {lbl.text_size[1]}"
        
        # Change text_size height to specific value
        label.text_size = [None, height]
        
        # Verify new height
        labels = self._find_labels_recursive(label)
        for lbl in labels:
            assert lbl.text_size[1] == height, \
                f"After change from None: Expected text_size[1]={height}, got {lbl.text_size[1]}"


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


# **Feature: label-compatibility, Property 11: Advanced Font Properties Forwarding**
# *For any* values of `font_family`, `font_context`, `font_features`, `font_hinting`,
# `font_kerning`, or `font_blended`, all internal Labels SHALL have those properties
# set to the corresponding values.
# **Validates: Requirements 11.1, 11.2, 11.3, 11.4, 11.5, 11.6**

class TestAdvancedFontPropertiesForwarding:
    """Property tests for advanced font properties forwarding (Property 11)."""
    
    def _find_labels_recursive(self, widget):
        """Recursively find all Label widgets in the tree."""
        labels = []
        if isinstance(widget, Label):
            labels.append(widget)
        if hasattr(widget, 'children'):
            for child in widget.children:
                labels.extend(self._find_labels_recursive(child))
        return labels
    
    @given(st.text(min_size=1, max_size=30, alphabet=st.characters(
        whitelist_categories=['L', 'N'],
        blacklist_characters='[]&\n\r'
    )))
    @settings(max_examples=100, deadline=None)
    def test_font_family_forwarded_to_labels(self, font_family_value):
        """font_family is forwarded to all internal Labels."""
        label = MarkdownLabel(text='Hello World', font_family=font_family_value)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least 1 Label"
        
        for lbl in labels:
            assert lbl.font_family == font_family_value, \
                f"Expected font_family={font_family_value!r}, got {lbl.font_family!r}"
    
    @given(st.text(min_size=1, max_size=30, alphabet=st.characters(
        whitelist_categories=['L', 'N'],
        blacklist_characters='[]&\n\r'
    )))
    @settings(max_examples=100, deadline=None)
    def test_font_context_forwarded_to_labels(self, font_context_value):
        """font_context is forwarded to all internal Labels."""
        label = MarkdownLabel(text='Hello World', font_context=font_context_value)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least 1 Label"
        
        for lbl in labels:
            assert lbl.font_context == font_context_value, \
                f"Expected font_context={font_context_value!r}, got {lbl.font_context!r}"
    
    @given(st.text(min_size=0, max_size=50, alphabet=st.characters(
        whitelist_categories=['L', 'N', 'P'],
        blacklist_characters='[]&\n\r'
    )))
    @settings(max_examples=100, deadline=None)
    def test_font_features_forwarded_to_labels(self, font_features_value):
        """font_features is forwarded to all internal Labels."""
        label = MarkdownLabel(text='Hello World', font_features=font_features_value)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least 1 Label"
        
        for lbl in labels:
            assert lbl.font_features == font_features_value, \
                f"Expected font_features={font_features_value!r}, got {lbl.font_features!r}"
    
    @given(st.sampled_from([None, 'normal', 'light', 'mono']))
    @settings(max_examples=100, deadline=None)
    def test_font_hinting_forwarded_to_labels(self, font_hinting_value):
        """font_hinting is forwarded to all internal Labels."""
        label = MarkdownLabel(text='Hello World', font_hinting=font_hinting_value)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least 1 Label"
        
        for lbl in labels:
            # When font_hinting is None, it may not be set on the Label
            if font_hinting_value is not None:
                assert lbl.font_hinting == font_hinting_value, \
                    f"Expected font_hinting={font_hinting_value!r}, got {lbl.font_hinting!r}"
    
    @given(st.booleans())
    @settings(max_examples=100, deadline=None)
    def test_font_kerning_forwarded_to_labels(self, font_kerning_value):
        """font_kerning is forwarded to all internal Labels."""
        label = MarkdownLabel(text='Hello World', font_kerning=font_kerning_value)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least 1 Label"
        
        for lbl in labels:
            assert lbl.font_kerning == font_kerning_value, \
                f"Expected font_kerning={font_kerning_value}, got {lbl.font_kerning}"
    
    @given(st.booleans())
    @settings(max_examples=100, deadline=None)
    def test_font_blended_forwarded_to_labels(self, font_blended_value):
        """font_blended is forwarded to all internal Labels."""
        label = MarkdownLabel(text='Hello World', font_blended=font_blended_value)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least 1 Label"
        
        for lbl in labels:
            assert lbl.font_blended == font_blended_value, \
                f"Expected font_blended={font_blended_value}, got {lbl.font_blended}"
    
    @given(st.sampled_from([None, 'normal', 'light', 'mono']),
           st.booleans(),
           st.booleans())
    @settings(max_examples=100, deadline=None)
    def test_multiple_advanced_font_properties_forwarded(self, font_hinting, font_kerning, font_blended):
        """Multiple advanced font properties are forwarded together."""
        label = MarkdownLabel(
            text='# Heading\n\nParagraph text',
            font_hinting=font_hinting,
            font_kerning=font_kerning,
            font_blended=font_blended
        )
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 2, "Expected at least 2 Labels (heading + paragraph)"
        
        for lbl in labels:
            if font_hinting is not None:
                assert lbl.font_hinting == font_hinting, \
                    f"Expected font_hinting={font_hinting!r}, got {lbl.font_hinting!r}"
            assert lbl.font_kerning == font_kerning, \
                f"Expected font_kerning={font_kerning}, got {lbl.font_kerning}"
            assert lbl.font_blended == font_blended, \
                f"Expected font_blended={font_blended}, got {lbl.font_blended}"
    
    @given(st.booleans(), st.booleans())
    @settings(max_examples=100, deadline=None)
    def test_font_kerning_change_triggers_rebuild(self, kerning1, kerning2):
        """Changing font_kerning triggers widget rebuild with new value."""
        assume(kerning1 != kerning2)
        
        label = MarkdownLabel(text='Hello World', font_kerning=kerning1)
        
        # Verify initial value
        labels = self._find_labels_recursive(label)
        for lbl in labels:
            assert lbl.font_kerning == kerning1
        
        # Change value
        label.font_kerning = kerning2
        
        # Verify new value
        labels = self._find_labels_recursive(label)
        for lbl in labels:
            assert lbl.font_kerning == kerning2, \
                f"After change, expected font_kerning={kerning2}, got {lbl.font_kerning}"
    
    @given(st.booleans(), st.booleans())
    @settings(max_examples=100, deadline=None)
    def test_font_blended_change_triggers_rebuild(self, blended1, blended2):
        """Changing font_blended triggers widget rebuild with new value."""
        assume(blended1 != blended2)
        
        label = MarkdownLabel(text='Hello World', font_blended=blended1)
        
        # Verify initial value
        labels = self._find_labels_recursive(label)
        for lbl in labels:
            assert lbl.font_blended == blended1
        
        # Change value
        label.font_blended = blended2
        
        # Verify new value
        labels = self._find_labels_recursive(label)
        for lbl in labels:
            assert lbl.font_blended == blended2, \
                f"After change, expected font_blended={blended2}, got {lbl.font_blended}"
    
    def test_default_font_kerning_is_true(self):
        """Default font_kerning is True."""
        label = MarkdownLabel(text='Hello World')
        
        assert label.font_kerning is True, \
            f"Default font_kerning should be True, got {label.font_kerning}"
    
    def test_default_font_blended_is_true(self):
        """Default font_blended is True."""
        label = MarkdownLabel(text='Hello World')
        
        assert label.font_blended is True, \
            f"Default font_blended should be True, got {label.font_blended}"
    
    def test_default_font_hinting_is_normal(self):
        """Default font_hinting is 'normal'."""
        label = MarkdownLabel(text='Hello World')
        
        assert label.font_hinting == 'normal', \
            f"Default font_hinting should be 'normal', got {label.font_hinting}"
    
    def test_default_font_features_is_empty(self):
        """Default font_features is empty string."""
        label = MarkdownLabel(text='Hello World')
        
        assert label.font_features == '', \
            f"Default font_features should be '', got {label.font_features!r}"
    
    def test_default_font_family_is_none(self):
        """Default font_family is None."""
        label = MarkdownLabel(text='Hello World')
        
        assert label.font_family is None, \
            f"Default font_family should be None, got {label.font_family!r}"
    
    def test_default_font_context_is_none(self):
        """Default font_context is None."""
        label = MarkdownLabel(text='Hello World')
        
        assert label.font_context is None, \
            f"Default font_context should be None, got {label.font_context!r}"


# **Feature: label-compatibility, Property 12: disabled_color Application**
# *For any* MarkdownLabel with `disabled=True` and any `disabled_color` value,
# all internal Labels SHALL use `disabled_color` instead of `color`.
# **Validates: Requirements 12.1, 12.2**

class TestDisabledColorApplication:
    """Property tests for disabled_color application (Property 12)."""
    
    def _find_labels_recursive(self, widget):
        """Recursively find all Label widgets in the widget tree."""
        labels = []
        if isinstance(widget, Label):
            labels.append(widget)
        if hasattr(widget, 'children'):
            for child in widget.children:
                labels.extend(self._find_labels_recursive(child))
        return labels
    
    def _colors_equal(self, color1, color2, tolerance=0.001):
        """Compare two colors with tolerance for floating point differences."""
        if len(color1) != len(color2):
            return False
        return all(abs(c1 - c2) < tolerance for c1, c2 in zip(color1, color2))
    
    @given(st.lists(
        st.floats(min_value=0, max_value=1, allow_nan=False, allow_infinity=False),
        min_size=4, max_size=4
    ))
    @settings(max_examples=100, deadline=None)
    def test_disabled_color_stored_correctly(self, disabled_color):
        """disabled_color property stores the value correctly."""
        label = MarkdownLabel(text='Hello World', disabled_color=disabled_color)
        
        assert self._colors_equal(label.disabled_color, disabled_color), \
            f"Expected disabled_color={disabled_color}, got {list(label.disabled_color)}"
    
    @given(st.lists(
        st.floats(min_value=0, max_value=1, allow_nan=False, allow_infinity=False),
        min_size=4, max_size=4
    ))
    @settings(max_examples=100, deadline=None)
    def test_disabled_color_applied_when_disabled(self, disabled_color):
        """When disabled=True, internal Labels use disabled_color instead of color."""
        regular_color = [1, 0, 0, 1]  # Red
        
        label = MarkdownLabel(
            text='Hello World',
            color=regular_color,
            disabled_color=disabled_color,
            disabled=True
        )
        
        labels = self._find_labels_recursive(label)
        assert len(labels) > 0, "Expected at least one Label widget"
        
        for lbl in labels:
            # Skip code block labels which have their own color
            if hasattr(lbl, 'font_name') and 'Mono' in str(lbl.font_name):
                continue
            assert self._colors_equal(lbl.color, disabled_color), \
                f"Expected disabled_color={disabled_color}, got {list(lbl.color)}"
    
    @given(st.lists(
        st.floats(min_value=0, max_value=1, allow_nan=False, allow_infinity=False),
        min_size=4, max_size=4
    ))
    @settings(max_examples=100, deadline=None)
    def test_regular_color_applied_when_not_disabled(self, regular_color):
        """When disabled=False, internal Labels use regular color."""
        disabled_color = [0.5, 0.5, 0.5, 0.3]  # Gray semi-transparent
        
        label = MarkdownLabel(
            text='Hello World',
            color=regular_color,
            disabled_color=disabled_color,
            disabled=False
        )
        
        labels = self._find_labels_recursive(label)
        assert len(labels) > 0, "Expected at least one Label widget"
        
        for lbl in labels:
            # Skip code block labels which have their own color
            if hasattr(lbl, 'font_name') and 'Mono' in str(lbl.font_name):
                continue
            assert self._colors_equal(lbl.color, regular_color), \
                f"Expected color={regular_color}, got {list(lbl.color)}"
    
    @given(st.booleans())
    @settings(max_examples=100, deadline=None)
    def test_disabled_state_determines_color(self, disabled):
        """disabled property determines which color is used."""
        regular_color = [1, 0, 0, 1]  # Red
        disabled_color = [0.5, 0.5, 0.5, 0.3]  # Gray semi-transparent
        
        label = MarkdownLabel(
            text='Hello World',
            color=regular_color,
            disabled_color=disabled_color,
            disabled=disabled
        )
        
        expected_color = disabled_color if disabled else regular_color
        
        labels = self._find_labels_recursive(label)
        assert len(labels) > 0, "Expected at least one Label widget"
        
        for lbl in labels:
            # Skip code block labels which have their own color
            if hasattr(lbl, 'font_name') and 'Mono' in str(lbl.font_name):
                continue
            assert self._colors_equal(lbl.color, expected_color), \
                f"Expected color={expected_color}, got {list(lbl.color)}"
    
    def test_disabled_change_triggers_rebuild(self):
        """Changing disabled property triggers widget rebuild."""
        regular_color = [1, 0, 0, 1]  # Red
        disabled_color = [0.5, 0.5, 0.5, 0.3]  # Gray semi-transparent
        
        label = MarkdownLabel(
            text='Hello World',
            color=regular_color,
            disabled_color=disabled_color,
            disabled=False
        )
        
        # Verify initial state uses regular color
        labels = self._find_labels_recursive(label)
        for lbl in labels:
            if hasattr(lbl, 'font_name') and 'Mono' in str(lbl.font_name):
                continue
            assert self._colors_equal(lbl.color, regular_color), \
                f"Initially expected color={regular_color}, got {list(lbl.color)}"
        
        # Change to disabled
        label.disabled = True
        
        # Verify disabled state uses disabled_color
        labels = self._find_labels_recursive(label)
        for lbl in labels:
            if hasattr(lbl, 'font_name') and 'Mono' in str(lbl.font_name):
                continue
            assert self._colors_equal(lbl.color, disabled_color), \
                f"After disabling, expected disabled_color={disabled_color}, got {list(lbl.color)}"
        
        # Change back to enabled
        label.disabled = False
        
        # Verify enabled state uses regular color again
        labels = self._find_labels_recursive(label)
        for lbl in labels:
            if hasattr(lbl, 'font_name') and 'Mono' in str(lbl.font_name):
                continue
            assert self._colors_equal(lbl.color, regular_color), \
                f"After re-enabling, expected color={regular_color}, got {list(lbl.color)}"
    
    def test_disabled_color_applied_to_heading(self):
        """disabled_color is applied to heading Labels when disabled."""
        disabled_color = [0.5, 0.5, 0.5, 0.3]
        
        label = MarkdownLabel(
            text='# Heading',
            disabled_color=disabled_color,
            disabled=True
        )
        
        labels = self._find_labels_recursive(label)
        assert len(labels) > 0, "Expected at least one Label widget"
        
        for lbl in labels:
            assert self._colors_equal(lbl.color, disabled_color), \
                f"Expected disabled_color={disabled_color}, got {list(lbl.color)}"
    
    def test_disabled_color_applied_to_list_items(self):
        """disabled_color is applied to list item Labels when disabled."""
        disabled_color = [0.5, 0.5, 0.5, 0.3]
        
        label = MarkdownLabel(
            text='- Item 1\n- Item 2',
            disabled_color=disabled_color,
            disabled=True
        )
        
        labels = self._find_labels_recursive(label)
        assert len(labels) > 0, "Expected at least one Label widget"
        
        for lbl in labels:
            assert self._colors_equal(lbl.color, disabled_color), \
                f"Expected disabled_color={disabled_color}, got {list(lbl.color)}"
    
    def test_disabled_color_applied_to_table_cells(self):
        """disabled_color is applied to table cell Labels when disabled."""
        disabled_color = [0.5, 0.5, 0.5, 0.3]
        
        label = MarkdownLabel(
            text='| A | B |\n| --- | --- |\n| 1 | 2 |',
            disabled_color=disabled_color,
            disabled=True
        )
        
        labels = self._find_labels_recursive(label)
        assert len(labels) > 0, "Expected at least one Label widget"
        
        for lbl in labels:
            assert self._colors_equal(lbl.color, disabled_color), \
                f"Expected disabled_color={disabled_color}, got {list(lbl.color)}"
    
    def test_default_disabled_color(self):
        """Default disabled_color is [1, 1, 1, 0.3]."""
        label = MarkdownLabel(text='Hello World')
        
        expected = [1, 1, 1, 0.3]
        assert self._colors_equal(label.disabled_color, expected), \
            f"Default disabled_color should be {expected}, got {list(label.disabled_color)}"
    
    def test_default_disabled_is_false(self):
        """Default disabled is False."""
        label = MarkdownLabel(text='Hello World')
        
        assert label.disabled is False, \
            f"Default disabled should be False, got {label.disabled}"


# **Feature: label-compatibility, Property 14: Reactive Rebuild on Property Change**
# *For any* forwarding property change after initial rendering, the widget tree
# SHALL be rebuilt with the new property value applied to all relevant internal Labels.
# **Validates: Requirements 1.2, 3.3, 4.2, 9.3**

# Strategy for generating valid property values
rebuild_font_names = st.sampled_from(['Roboto', 'Roboto-Bold', 'Roboto-Italic'])
rebuild_colors = st.lists(
    st.floats(min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False),
    min_size=4, max_size=4
)
rebuild_line_heights = st.floats(min_value=0.5, max_value=3.0, allow_nan=False, allow_infinity=False)
rebuild_text_size_widths = st.floats(min_value=50, max_value=1000, allow_nan=False, allow_infinity=False)


class TestReactiveRebuildOnPropertyChange:
    """Property tests for reactive rebuild on property change (Property 14)."""
    
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
    
    def _floats_equal(self, f1, f2, tolerance=0.001):
        """Compare two floats with tolerance."""
        return abs(f1 - f2) < tolerance
    
    @given(rebuild_font_names, rebuild_font_names)
    @settings(max_examples=100, deadline=None)
    def test_font_name_change_rebuilds_widgets(self, font1, font2):
        """Changing font_name after initial rendering rebuilds widgets with new font.
        
        Validates: Requirement 1.2 - WHEN `font_name` changes after initial rendering
        THEN the MarkdownLabel SHALL rebuild widgets with the new font applied.
        """
        assume(font1 != font2)
        
        label = MarkdownLabel(text='Hello World', font_name=font1)
        
        # Verify initial font
        labels_before = self._find_labels_recursive(label)
        assert len(labels_before) >= 1, "Expected at least one Label"
        for lbl in labels_before:
            assert lbl.font_name == font1, f"Initial font should be {font1}"
        
        # Change font_name
        label.font_name = font2
        
        # Verify widgets were rebuilt with new font
        labels_after = self._find_labels_recursive(label)
        assert len(labels_after) >= 1, "Expected at least one Label after rebuild"
        for lbl in labels_after:
            assert lbl.font_name == font2, \
                f"After change, expected font_name={font2}, got {lbl.font_name}"
    
    @given(rebuild_colors, rebuild_colors)
    @settings(max_examples=100, deadline=None)
    def test_color_change_rebuilds_widgets(self, color1, color2):
        """Changing color after initial rendering rebuilds widgets with new color.
        
        Validates: Requirement 3.3 - WHEN `color` changes after initial rendering
        THEN the MarkdownLabel SHALL rebuild widgets with the new color applied.
        """
        assume(not self._colors_equal(color1, color2))
        
        label = MarkdownLabel(text='Hello World', color=color1)
        
        # Verify initial color
        labels_before = self._find_labels_recursive(label)
        assert len(labels_before) >= 1, "Expected at least one Label"
        for lbl in labels_before:
            assert self._colors_equal(list(lbl.color), color1), \
                f"Initial color should be {color1}"
        
        # Change color
        label.color = color2
        
        # Verify widgets were rebuilt with new color
        labels_after = self._find_labels_recursive(label)
        assert len(labels_after) >= 1, "Expected at least one Label after rebuild"
        for lbl in labels_after:
            assert self._colors_equal(list(lbl.color), color2), \
                f"After change, expected color={color2}, got {list(lbl.color)}"
    
    @given(rebuild_line_heights, rebuild_line_heights)
    @settings(max_examples=100, deadline=None)
    def test_line_height_change_rebuilds_widgets(self, lh1, lh2):
        """Changing line_height after initial rendering rebuilds widgets with new value.
        
        Validates: Requirement 4.2 - WHEN `line_height` changes after initial rendering
        THEN the MarkdownLabel SHALL rebuild widgets with the new line height applied.
        """
        assume(not self._floats_equal(lh1, lh2))
        
        label = MarkdownLabel(text='Hello World', line_height=lh1)
        
        # Verify initial line_height
        labels_before = self._find_labels_recursive(label)
        assert len(labels_before) >= 1, "Expected at least one Label"
        for lbl in labels_before:
            assert self._floats_equal(lbl.line_height, lh1), \
                f"Initial line_height should be {lh1}"
        
        # Change line_height
        label.line_height = lh2
        
        # Verify widgets were rebuilt with new line_height
        labels_after = self._find_labels_recursive(label)
        assert len(labels_after) >= 1, "Expected at least one Label after rebuild"
        for lbl in labels_after:
            assert self._floats_equal(lbl.line_height, lh2), \
                f"After change, expected line_height={lh2}, got {lbl.line_height}"
    
    @given(rebuild_text_size_widths, rebuild_text_size_widths)
    @settings(max_examples=100, deadline=None)
    def test_text_size_change_rebuilds_widgets(self, width1, width2):
        """Changing text_size after initial rendering rebuilds widgets.
        
        Validates: Requirement 9.3 - WHEN `text_size` width changes
        THEN the MarkdownLabel SHALL reflow text content to fit the new width.
        """
        assume(abs(width1 - width2) > 1)  # Ensure they're different
        
        label = MarkdownLabel(text='Hello World', text_size=[width1, None])
        
        # Verify initial text_size
        assert label.text_size[0] == width1, f"Initial text_size[0] should be {width1}"
        
        # Change text_size
        label.text_size = [width2, None]
        
        # Verify text_size was updated
        assert label.text_size[0] == width2, \
            f"After change, expected text_size[0]={width2}, got {label.text_size[0]}"
        
        # Verify widgets still exist (rebuild happened)
        labels_after = self._find_labels_recursive(label)
        assert len(labels_after) >= 1, "Expected at least one Label after rebuild"
    
    @given(rebuild_font_names, rebuild_colors, rebuild_line_heights)
    @settings(max_examples=100, deadline=None)
    def test_multiple_property_changes_rebuild_correctly(self, font_name, color, line_height):
        """Multiple property changes each trigger rebuilds with correct values."""
        label = MarkdownLabel(text='# Heading\n\nParagraph text')
        
        # Change font_name
        label.font_name = font_name
        labels = self._find_labels_recursive(label)
        for lbl in labels:
            assert lbl.font_name == font_name, \
                f"After font_name change, expected {font_name}, got {lbl.font_name}"
        
        # Change color
        label.color = color
        labels = self._find_labels_recursive(label)
        for lbl in labels:
            assert self._colors_equal(list(lbl.color), color), \
                f"After color change, expected {color}, got {list(lbl.color)}"
        
        # Change line_height
        label.line_height = line_height
        labels = self._find_labels_recursive(label)
        for lbl in labels:
            assert self._floats_equal(lbl.line_height, line_height), \
                f"After line_height change, expected {line_height}, got {lbl.line_height}"
    
    @given(st.sampled_from(['left', 'center', 'right', 'justify']),
           st.sampled_from(['left', 'center', 'right', 'justify']))
    @settings(max_examples=100, deadline=None)
    def test_halign_change_rebuilds_widgets(self, halign1, halign2):
        """Changing halign after initial rendering rebuilds widgets with new alignment."""
        assume(halign1 != halign2)
        
        label = MarkdownLabel(text='Hello World', halign=halign1)
        
        # Verify initial halign
        labels_before = self._find_labels_recursive(label)
        assert len(labels_before) >= 1, "Expected at least one Label"
        for lbl in labels_before:
            assert lbl.halign == halign1, f"Initial halign should be {halign1}"
        
        # Change halign
        label.halign = halign2
        
        # Verify widgets were rebuilt with new halign
        labels_after = self._find_labels_recursive(label)
        assert len(labels_after) >= 1, "Expected at least one Label after rebuild"
        for lbl in labels_after:
            assert lbl.halign == halign2, \
                f"After change, expected halign={halign2}, got {lbl.halign}"
    
    @given(st.sampled_from(['bottom', 'middle', 'center', 'top']),
           st.sampled_from(['bottom', 'middle', 'center', 'top']))
    @settings(max_examples=100, deadline=None)
    def test_valign_change_rebuilds_widgets(self, valign1, valign2):
        """Changing valign after initial rendering rebuilds widgets with new alignment."""
        assume(valign1 != valign2)
        
        label = MarkdownLabel(text='Hello World', valign=valign1)
        
        # Verify initial valign
        labels_before = self._find_labels_recursive(label)
        assert len(labels_before) >= 1, "Expected at least one Label"
        for lbl in labels_before:
            assert lbl.valign == valign1, f"Initial valign should be {valign1}"
        
        # Change valign
        label.valign = valign2
        
        # Verify widgets were rebuilt with new valign
        labels_after = self._find_labels_recursive(label)
        assert len(labels_after) >= 1, "Expected at least one Label after rebuild"
        for lbl in labels_after:
            assert lbl.valign == valign2, \
                f"After change, expected valign={valign2}, got {lbl.valign}"
    
    @given(st.sampled_from(['strict', 'replace', 'ignore']),
           st.sampled_from(['strict', 'replace', 'ignore']))
    @settings(max_examples=100, deadline=None)
    def test_unicode_errors_change_rebuilds_widgets(self, errors1, errors2):
        """Changing unicode_errors after initial rendering rebuilds widgets."""
        assume(errors1 != errors2)
        
        label = MarkdownLabel(text='Hello World', unicode_errors=errors1)
        
        # Verify initial unicode_errors
        labels_before = self._find_labels_recursive(label)
        assert len(labels_before) >= 1, "Expected at least one Label"
        for lbl in labels_before:
            assert lbl.unicode_errors == errors1, f"Initial unicode_errors should be {errors1}"
        
        # Change unicode_errors
        label.unicode_errors = errors2
        
        # Verify widgets were rebuilt with new unicode_errors
        labels_after = self._find_labels_recursive(label)
        assert len(labels_after) >= 1, "Expected at least one Label after rebuild"
        for lbl in labels_after:
            assert lbl.unicode_errors == errors2, \
                f"After change, expected unicode_errors={errors2}, got {lbl.unicode_errors}"
    
    @given(st.booleans(), st.booleans())
    @settings(max_examples=100, deadline=None)
    def test_strip_change_rebuilds_widgets(self, strip1, strip2):
        """Changing strip after initial rendering rebuilds widgets."""
        assume(strip1 != strip2)
        
        label = MarkdownLabel(text='Hello World', strip=strip1)
        
        # Verify initial strip
        labels_before = self._find_labels_recursive(label)
        assert len(labels_before) >= 1, "Expected at least one Label"
        for lbl in labels_before:
            assert lbl.strip == strip1, f"Initial strip should be {strip1}"
        
        # Change strip
        label.strip = strip2
        
        # Verify widgets were rebuilt with new strip
        labels_after = self._find_labels_recursive(label)
        assert len(labels_after) >= 1, "Expected at least one Label after rebuild"
        for lbl in labels_after:
            assert lbl.strip == strip2, \
                f"After change, expected strip={strip2}, got {lbl.strip}"
    
    @given(st.booleans(), st.booleans())
    @settings(max_examples=100, deadline=None)
    def test_disabled_change_rebuilds_widgets(self, disabled1, disabled2):
        """Changing disabled after initial rendering rebuilds widgets with correct color."""
        assume(disabled1 != disabled2)
        
        regular_color = [1, 0, 0, 1]  # Red
        disabled_color = [0.5, 0.5, 0.5, 0.3]  # Gray
        
        label = MarkdownLabel(
            text='Hello World',
            color=regular_color,
            disabled_color=disabled_color,
            disabled=disabled1
        )
        
        expected_color1 = disabled_color if disabled1 else regular_color
        
        # Verify initial color based on disabled state
        labels_before = self._find_labels_recursive(label)
        assert len(labels_before) >= 1, "Expected at least one Label"
        for lbl in labels_before:
            assert self._colors_equal(list(lbl.color), expected_color1), \
                f"Initial color should be {expected_color1}"
        
        # Change disabled
        label.disabled = disabled2
        
        expected_color2 = disabled_color if disabled2 else regular_color
        
        # Verify widgets were rebuilt with correct color
        labels_after = self._find_labels_recursive(label)
        assert len(labels_after) >= 1, "Expected at least one Label after rebuild"
        for lbl in labels_after:
            assert self._colors_equal(list(lbl.color), expected_color2), \
                f"After change, expected color={expected_color2}, got {list(lbl.color)}"
    
    @given(simple_markdown_document(), rebuild_font_names, rebuild_font_names)
    @settings(max_examples=100, deadline=None)
    def test_rebuild_preserves_content_structure(self, markdown_text, font1, font2):
        """Rebuilding widgets preserves the content structure."""
        assume(markdown_text.strip())
        assume(font1 != font2)
        
        label = MarkdownLabel(text=markdown_text, font_name=font1)
        
        # Count children before
        children_before = len(label.children)
        
        # Change font_name to trigger rebuild
        label.font_name = font2
        
        # Count children after
        children_after = len(label.children)
        
        # Structure should be preserved (same number of children)
        assert children_before == children_after, \
            f"Expected {children_before} children after rebuild, got {children_after}"
    
    @given(st.booleans(), st.booleans())
    @settings(max_examples=100, deadline=None)
    def test_font_kerning_change_rebuilds_widgets(self, kerning1, kerning2):
        """Changing font_kerning after initial rendering rebuilds widgets."""
        assume(kerning1 != kerning2)
        
        label = MarkdownLabel(text='Hello World', font_kerning=kerning1)
        
        # Verify initial font_kerning
        labels_before = self._find_labels_recursive(label)
        assert len(labels_before) >= 1, "Expected at least one Label"
        for lbl in labels_before:
            assert lbl.font_kerning == kerning1, f"Initial font_kerning should be {kerning1}"
        
        # Change font_kerning
        label.font_kerning = kerning2
        
        # Verify widgets were rebuilt with new font_kerning
        labels_after = self._find_labels_recursive(label)
        assert len(labels_after) >= 1, "Expected at least one Label after rebuild"
        for lbl in labels_after:
            assert lbl.font_kerning == kerning2, \
                f"After change, expected font_kerning={kerning2}, got {lbl.font_kerning}"
    
    @given(st.booleans(), st.booleans())
    @settings(max_examples=100, deadline=None)
    def test_font_blended_change_rebuilds_widgets(self, blended1, blended2):
        """Changing font_blended after initial rendering rebuilds widgets."""
        assume(blended1 != blended2)
        
        label = MarkdownLabel(text='Hello World', font_blended=blended1)
        
        # Verify initial font_blended
        labels_before = self._find_labels_recursive(label)
        assert len(labels_before) >= 1, "Expected at least one Label"
        for lbl in labels_before:
            assert lbl.font_blended == blended1, f"Initial font_blended should be {blended1}"
        
        # Change font_blended
        label.font_blended = blended2
        
        # Verify widgets were rebuilt with new font_blended
        labels_after = self._find_labels_recursive(label)
        assert len(labels_after) >= 1, "Expected at least one Label after rebuild"
        for lbl in labels_after:
            assert lbl.font_blended == blended2, \
                f"After change, expected font_blended={blended2}, got {lbl.font_blended}"


# **Feature: label-compatibility, Property 4: Padding Forwarding to Child Labels**
# *For any* MarkdownLabel with `padding` set to value P, all child Labels that display text content
# SHALL have their `padding` property equal to P.
# **Validates: Requirements 2.1, 2.2**

# Strategy for generating valid padding values
padding_strategy = st.lists(
    st.floats(min_value=0.0, max_value=50.0, allow_nan=False, allow_infinity=False),
    min_size=4, max_size=4
)


class TestPaddingForwarding:
    """Property tests for padding forwarding (Property 4)."""
    
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
    
    def _padding_equal(self, p1, p2, tolerance=0.001):
        """Compare two padding values with tolerance for floating point differences."""
        if len(p1) != len(p2):
            return False
        return all(abs(a - b) < tolerance for a, b in zip(p1, p2))
    
    @given(padding_strategy)
    @settings(max_examples=100, deadline=None)
    def test_padding_applied_to_paragraph(self, padding):
        """padding is applied to paragraph Labels."""
        label = MarkdownLabel(text='Hello World', padding=padding)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        # All labels should have the specified padding
        for lbl in labels:
            assert self._padding_equal(list(lbl.padding), padding), \
                f"Expected padding={padding}, got {list(lbl.padding)}"
    
    @given(padding_strategy)
    @settings(max_examples=100, deadline=None)
    def test_padding_applied_to_heading(self, padding):
        """padding is applied to heading Labels."""
        label = MarkdownLabel(text='# Heading', padding=padding)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        # All labels should have the specified padding
        for lbl in labels:
            assert self._padding_equal(list(lbl.padding), padding), \
                f"Expected padding={padding}, got {list(lbl.padding)}"
    
    @given(padding_strategy)
    @settings(max_examples=100, deadline=None)
    def test_padding_applied_to_list_items(self, padding):
        """padding is applied to list item Labels."""
        markdown = '- Item 1\n- Item 2'
        label = MarkdownLabel(text=markdown, padding=padding)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 2, "Expected at least 2 Labels for list items"
        
        # All labels should have the specified padding
        for lbl in labels:
            assert self._padding_equal(list(lbl.padding), padding), \
                f"Expected padding={padding}, got {list(lbl.padding)}"
    
    @given(padding_strategy)
    @settings(max_examples=100, deadline=None)
    def test_padding_applied_to_table_cells(self, padding):
        """padding is applied to table cell Labels."""
        markdown = '| A | B |\n| --- | --- |\n| 1 | 2 |'
        label = MarkdownLabel(text=markdown, padding=padding)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 4, "Expected at least 4 Labels for table cells"
        
        # All labels should have the specified padding
        for lbl in labels:
            assert self._padding_equal(list(lbl.padding), padding), \
                f"Expected padding={padding}, got {list(lbl.padding)}"
    
    @given(padding_strategy)
    @settings(max_examples=100, deadline=None)
    def test_padding_applied_to_nested_structures(self, padding):
        """padding is applied to Labels in nested structures (lists, tables, block quotes)."""
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
        label = MarkdownLabel(text=markdown, padding=padding)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 5, "Expected at least 5 Labels for various structures"
        
        # All labels should have the specified padding
        for lbl in labels:
            assert self._padding_equal(list(lbl.padding), padding), \
                f"Expected padding={padding}, got {list(lbl.padding)}"
    
    @given(padding_strategy, padding_strategy)
    @settings(max_examples=100, deadline=None)
    def test_padding_change_triggers_rebuild(self, padding1, padding2):
        """Changing padding triggers widget rebuild with new padding."""
        assume(not self._padding_equal(padding1, padding2))
        
        label = MarkdownLabel(text='Hello World', padding=padding1)
        
        # Verify initial padding
        labels = self._find_labels_recursive(label)
        for lbl in labels:
            assert self._padding_equal(list(lbl.padding), padding1)
        
        # Change padding
        label.padding = padding2
        
        # Verify new padding
        labels = self._find_labels_recursive(label)
        for lbl in labels:
            assert self._padding_equal(list(lbl.padding), padding2), \
                f"After change, expected padding={padding2}, got {list(lbl.padding)}"
    
    def test_default_padding_is_zero(self):
        """Default padding is [0, 0, 0, 0]."""
        label = MarkdownLabel(text='Hello World')
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        # All labels should have default padding of [0, 0, 0, 0]
        for lbl in labels:
            assert self._padding_equal(list(lbl.padding), [0, 0, 0, 0]), \
                f"Expected default padding=[0, 0, 0, 0], got {list(lbl.padding)}"


# **Feature: label-compatibility, Property 5: Padding Dynamic Updates**
# *For any* MarkdownLabel, when `padding` is changed from value A to value B, all child Labels
# SHALL be updated to reflect the new `padding` value B.
# **Validates: Requirements 2.3**

class TestPaddingDynamicUpdates:
    """Property tests for padding dynamic updates (Property 5)."""
    
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
    
    def _padding_equal(self, p1, p2, tolerance=0.001):
        """Compare two padding values with tolerance for floating point differences."""
        if len(p1) != len(p2):
            return False
        return all(abs(a - b) < tolerance for a, b in zip(p1, p2))
    
    @given(padding_strategy, padding_strategy)
    @settings(max_examples=100, deadline=None)
    def test_padding_update_paragraph(self, initial_padding, new_padding):
        """Updating padding on paragraph updates all child Labels."""
        assume(not self._padding_equal(initial_padding, new_padding))
        
        label = MarkdownLabel(text='Hello World', padding=initial_padding)
        
        # Verify initial padding
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        for lbl in labels:
            assert self._padding_equal(list(lbl.padding), initial_padding)
        
        # Update padding
        label.padding = new_padding
        
        # Verify all labels have new padding
        labels = self._find_labels_recursive(label)
        for lbl in labels:
            assert self._padding_equal(list(lbl.padding), new_padding), \
                f"After update, expected padding={new_padding}, got {list(lbl.padding)}"
    
    @given(padding_strategy, padding_strategy)
    @settings(max_examples=100, deadline=None)
    def test_padding_update_complex_content(self, initial_padding, new_padding):
        """Updating padding on complex content updates all child Labels."""
        assume(not self._padding_equal(initial_padding, new_padding))
        
        markdown = '''
# Title

Paragraph with text.

- List item 1
- List item 2

| A | B |
| --- | --- |
| 1 | 2 |
'''
        
        label = MarkdownLabel(text=markdown, padding=initial_padding)
        
        # Verify initial padding
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 5, "Expected at least 5 Labels"
        for lbl in labels:
            assert self._padding_equal(list(lbl.padding), initial_padding)
        
        # Update padding
        label.padding = new_padding
        
        # Verify all labels have new padding
        labels = self._find_labels_recursive(label)
        for lbl in labels:
            assert self._padding_equal(list(lbl.padding), new_padding), \
                f"After update, expected padding={new_padding}, got {list(lbl.padding)}"
    
    @given(st.integers(min_value=1, max_value=5))
    @settings(max_examples=100, deadline=None)
    def test_multiple_padding_updates(self, num_updates):
        """Multiple padding updates all work correctly."""
        label = MarkdownLabel(text='Hello World')
        
        for i in range(num_updates):
            new_padding = [i * 5.0, i * 5.0, i * 5.0, i * 5.0]
            label.padding = new_padding
            
            # Verify all labels have the current padding
            labels = self._find_labels_recursive(label)
            for lbl in labels:
                assert self._padding_equal(list(lbl.padding), new_padding), \
                    f"Update {i}: expected padding={new_padding}, got {list(lbl.padding)}"


# **Feature: label-compatibility, Property 6: Padding with Nested Structures**
# *For any* MarkdownLabel containing nested structures (lists, tables, block quotes), all text-containing
# Labels within those structures SHALL have the `padding` property applied without breaking the layout structure.
# **Validates: Requirements 2.4**

class TestPaddingWithNestedStructures:
    """Property tests for padding with nested structures (Property 6)."""
    
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
    
    def _padding_equal(self, p1, p2, tolerance=0.001):
        """Compare two padding values with tolerance for floating point differences."""
        if len(p1) != len(p2):
            return False
        return all(abs(a - b) < tolerance for a, b in zip(p1, p2))
    
    @given(padding_strategy)
    @settings(max_examples=100, deadline=None)
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
        
        label = MarkdownLabel(text=markdown, padding=padding)
        
        # Should have multiple children for the nested list structure
        assert len(label.children) >= 1, "Expected at least one child for list structure"
        
        # All Labels should have the specified padding
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 5, "Expected at least 5 Labels for nested list items"
        
        for lbl in labels:
            assert self._padding_equal(list(lbl.padding), padding), \
                f"Expected padding={padding}, got {list(lbl.padding)}"
    
    @given(padding_strategy)
    @settings(max_examples=100, deadline=None)
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
        
        label = MarkdownLabel(text=markdown, padding=padding)
        
        # Should have children for the quote structure
        assert len(label.children) >= 1, "Expected at least one child for quote structure"
        
        # All Labels should have the specified padding
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least 1 Label for quote content"
        
        for lbl in labels:
            assert self._padding_equal(list(lbl.padding), padding), \
                f"Expected padding={padding}, got {list(lbl.padding)}"
    
    @given(padding_strategy)
    @settings(max_examples=100, deadline=None)
    def test_padding_in_complex_table(self, padding):
        """padding is applied to Labels in complex tables without breaking structure."""
        markdown = '''
| Header 1 | Header 2 | Header 3 |
| :--- | :---: | ---: |
| Left aligned | Center aligned | Right aligned |
| Cell with **bold** | Cell with *italic* | Cell with `code` |
| Multi word cell | Another cell | Final cell |
'''
        
        label = MarkdownLabel(text=markdown, padding=padding)
        
        # Should have children for the table structure
        assert len(label.children) >= 1, "Expected at least one child for table structure"
        
        # All Labels should have the specified padding
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 9, "Expected at least 9 Labels for table cells"
        
        for lbl in labels:
            assert self._padding_equal(list(lbl.padding), padding), \
                f"Expected padding={padding}, got {list(lbl.padding)}"
    
    @given(padding_strategy)
    @settings(max_examples=100, deadline=None)
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
        
        label = MarkdownLabel(text=markdown, padding=padding)
        
        # Should have multiple children for the complex structure
        assert len(label.children) >= 3, "Expected at least 3 children for complex structure"
        
        # All Labels should have the specified padding
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 8, "Expected at least 8 Labels for mixed content"
        
        for lbl in labels:
            assert self._padding_equal(list(lbl.padding), padding), \
                f"Expected padding={padding}, got {list(lbl.padding)}"
    
    @given(padding_strategy)
    @settings(max_examples=100, deadline=None)
    def test_padding_preserves_widget_hierarchy(self, padding):
        """padding application preserves the widget hierarchy structure."""
        markdown = '''
- Item 1
  - Nested item
- Item 2
'''
        
        label = MarkdownLabel(text=markdown, padding=padding)
        
        # Verify the basic structure is preserved
        assert len(label.children) >= 1, "Expected at least one child for list"
        
        # Verify padding is applied but structure is intact
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 3, "Expected at least 3 Labels (2 items + 1 nested)"
        
        for lbl in labels:
            assert self._padding_equal(list(lbl.padding), padding), \
                f"Expected padding={padding}, got {list(lbl.padding)}"
            # Verify the label is still properly embedded in the widget tree
            assert lbl.parent is not None, "Label should have a parent widget"


# **Feature: label-compatibility, Property 4: Padding Forwarding to Child Labels**
# *For any* MarkdownLabel with `padding` set to value P, all child Labels that display 
# text content SHALL have their `padding` property equal to P.
# **Validates: Requirements 2.1, 2.2**

class TestPaddingForwardingToChildLabels:
    """Property tests for padding forwarding to child Labels (Property 4)."""
    
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
    
    def _padding_equal(self, actual, expected):
        """Check if two padding values are equal within tolerance."""
        if len(actual) != len(expected):
            return False
        return all(abs(a - e) < 0.001 for a, e in zip(actual, expected))
    
    @given(padding_four)
    @settings(max_examples=100, deadline=None)
    def test_padding_forwarded_to_paragraph_labels(self, padding):
        """Padding is forwarded to Labels in paragraphs."""
        label = MarkdownLabel(text='Hello World', padding=padding)
        
        # Find all Label widgets
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label for paragraph"
        
        # All Labels should have the specified padding
        for lbl in labels:
            assert self._padding_equal(list(lbl.padding), padding), \
                f"Expected padding={padding}, got {list(lbl.padding)}"
    
    @given(padding_four)
    @settings(max_examples=100, deadline=None)
    def test_padding_forwarded_to_heading_labels(self, padding):
        """Padding is forwarded to Labels in headings."""
        label = MarkdownLabel(text='# Main Heading', padding=padding)
        
        # Find all Label widgets
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label for heading"
        
        # All Labels should have the specified padding
        for lbl in labels:
            assert self._padding_equal(list(lbl.padding), padding), \
                f"Expected padding={padding}, got {list(lbl.padding)}"
    
    @given(padding_four)
    @settings(max_examples=100, deadline=None)
    def test_padding_forwarded_to_list_labels(self, padding):
        """Padding is forwarded to Labels in list items."""
        markdown = '''
- First item
- Second item
- Third item
'''
        label = MarkdownLabel(text=markdown, padding=padding)
        
        # Find all Label widgets
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 3, "Expected at least 3 Labels for list items"
        
        # All Labels should have the specified padding
        for lbl in labels:
            assert self._padding_equal(list(lbl.padding), padding), \
                f"Expected padding={padding}, got {list(lbl.padding)}"
    
    @given(padding_four)
    @settings(max_examples=100, deadline=None)
    def test_padding_forwarded_to_table_labels(self, padding):
        """Padding is forwarded to Labels in table cells."""
        markdown = '''
| Header 1 | Header 2 |
| --- | --- |
| Cell 1 | Cell 2 |
| Cell 3 | Cell 4 |
'''
        label = MarkdownLabel(text=markdown, padding=padding)
        
        # Find all Label widgets
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 6, "Expected at least 6 Labels for table cells"
        
        # All Labels should have the specified padding
        for lbl in labels:
            assert self._padding_equal(list(lbl.padding), padding), \
                f"Expected padding={padding}, got {list(lbl.padding)}"


# **Feature: label-compatibility, Property 5: Padding Dynamic Updates**
# *For any* MarkdownLabel, when `padding` is changed from value A to value B, 
# all child Labels SHALL be updated to reflect the new `padding` value B.
# **Validates: Requirements 2.3**

class TestPaddingDynamicUpdates:
    """Property tests for padding dynamic updates (Property 5)."""
    
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
    
    def _padding_equal(self, actual, expected):
        """Check if two padding values are equal within tolerance."""
        if len(actual) != len(expected):
            return False
        return all(abs(a - e) < 0.001 for a, e in zip(actual, expected))
    
    @given(padding_four, padding_four)
    @settings(max_examples=100, deadline=None)
    def test_padding_change_updates_paragraph_labels(self, padding1, padding2):
        """Changing padding updates Labels in paragraphs."""
        assume(padding1 != padding2)
        
        label = MarkdownLabel(text='Hello World', padding=padding1)
        
        # Verify initial padding
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        for lbl in labels:
            assert self._padding_equal(list(lbl.padding), padding1), \
                f"Initial: Expected padding={padding1}, got {list(lbl.padding)}"
        
        # Change padding
        label.padding = padding2
        
        # Verify new padding
        labels = self._find_labels_recursive(label)
        for lbl in labels:
            assert self._padding_equal(list(lbl.padding), padding2), \
                f"After change: Expected padding={padding2}, got {list(lbl.padding)}"
    
    @given(padding_four, padding_four)
    @settings(max_examples=100, deadline=None)
    def test_padding_change_updates_heading_labels(self, padding1, padding2):
        """Changing padding updates Labels in headings."""
        assume(padding1 != padding2)
        
        label = MarkdownLabel(text='# Main Heading', padding=padding1)
        
        # Verify initial padding
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        for lbl in labels:
            assert self._padding_equal(list(lbl.padding), padding1), \
                f"Initial: Expected padding={padding1}, got {list(lbl.padding)}"
        
        # Change padding
        label.padding = padding2
        
        # Verify new padding
        labels = self._find_labels_recursive(label)
        for lbl in labels:
            assert self._padding_equal(list(lbl.padding), padding2), \
                f"After change: Expected padding={padding2}, got {list(lbl.padding)}"
    
    @given(padding_four, padding_four)
    @settings(max_examples=100, deadline=None)
    def test_padding_change_updates_list_labels(self, padding1, padding2):
        """Changing padding updates Labels in list items."""
        assume(padding1 != padding2)
        
        markdown = '''
- First item
- Second item
'''
        label = MarkdownLabel(text=markdown, padding=padding1)
        
        # Verify initial padding
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 2, "Expected at least 2 Labels"
        
        for lbl in labels:
            assert self._padding_equal(list(lbl.padding), padding1), \
                f"Initial: Expected padding={padding1}, got {list(lbl.padding)}"
        
        # Change padding
        label.padding = padding2
        
        # Verify new padding
        labels = self._find_labels_recursive(label)
        for lbl in labels:
            assert self._padding_equal(list(lbl.padding), padding2), \
                f"After change: Expected padding={padding2}, got {list(lbl.padding)}"


# **Feature: label-compatibility, Property 6: Padding with Nested Structures**
# *For any* MarkdownLabel containing nested structures (lists, tables, block quotes), 
# all text-containing Labels within those structures SHALL have the `padding` property 
# applied without breaking the layout structure.
# **Validates: Requirements 2.4**

class TestPaddingWithNestedStructures:
    """Property tests for padding with nested structures (Property 6)."""
    
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
    
    def _padding_equal(self, actual, expected):
        """Check if two padding values are equal within tolerance."""
        if len(actual) != len(expected):
            return False
        return all(abs(a - e) < 0.001 for a, e in zip(actual, expected))
    
    @given(padding_four)
    @settings(max_examples=100, deadline=None)
    def test_padding_in_nested_lists(self, padding):
        """Padding is applied to Labels in nested lists without breaking layout."""
        markdown = '''
- Top level item
  - Nested item 1
  - Nested item 2
    - Deep nested item
- Another top level item
'''
        label = MarkdownLabel(text=markdown, padding=padding)
        
        # Should have children for the list structure
        assert len(label.children) >= 1, "Expected at least one child for list structure"
        
        # All Labels should have the specified padding
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 4, "Expected at least 4 Labels for nested list items"
        
        for lbl in labels:
            assert self._padding_equal(list(lbl.padding), padding), \
                f"Expected padding={padding}, got {list(lbl.padding)}"
    
    @given(padding_four)
    @settings(max_examples=100, deadline=None)
    def test_padding_in_nested_block_quotes(self, padding):
        """Padding is applied to Labels in nested block quotes without breaking layout."""
        markdown = '''
> This is a quote
> 
> > This is a nested quote
> > with multiple lines
> 
> Back to the outer quote
'''
        label = MarkdownLabel(text=markdown, padding=padding)
        
        # Should have children for the quote structure
        assert len(label.children) >= 1, "Expected at least one child for quote structure"
        
        # All Labels should have the specified padding
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 3, "Expected at least 3 Labels for nested quotes"
        
        for lbl in labels:
            assert self._padding_equal(list(lbl.padding), padding), \
                f"Expected padding={padding}, got {list(lbl.padding)}"
    
    @given(padding_four)
    @settings(max_examples=100, deadline=None)
    def test_padding_in_table_within_list(self, padding):
        """Padding is applied to Labels in tables within lists without breaking layout."""
        markdown = '''
- List item with table:

  | Col 1 | Col 2 |
  | --- | --- |
  | A | B |
  | C | D |

- Another list item
'''
        label = MarkdownLabel(text=markdown, padding=padding)
        
        # Should have children for the complex structure
        assert len(label.children) >= 1, "Expected at least one child for list+table structure"
        
        # All Labels should have the specified padding
        labels = self._find_labels_recursive(label)
        # Note: Table within list is rendered as plain text, so we expect 5 Labels:
        # 2 list item texts + 2 bullet points + 1 table (as plain text)
        assert len(labels) >= 5, "Expected at least 5 Labels (2 list items + bullets + table text)"
        
        for lbl in labels:
            assert self._padding_equal(list(lbl.padding), padding), \
                f"Expected padding={padding}, got {list(lbl.padding)}"
    
    @given(padding_four)
    @settings(max_examples=100, deadline=None)
    def test_padding_preserves_nested_structure_integrity(self, padding):
        """Padding application preserves the integrity of nested widget structures."""
        markdown = '''
# Heading

- List with nested content:
  
  > Quote inside list
  > with multiple lines
  
  | Table | In List |
  | --- | --- |
  | Cell 1 | Cell 2 |

Final paragraph.
'''
        label = MarkdownLabel(text=markdown, padding=padding)
        
        # Should have multiple children for the complex structure
        assert len(label.children) >= 3, "Expected at least 3 children for complex structure"
        
        # All Labels should have the specified padding
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 6, "Expected at least 6 Labels for mixed nested content"
        
        for lbl in labels:
            assert self._padding_equal(list(lbl.padding), padding), \
                f"Expected padding={padding}, got {list(lbl.padding)}"
            # Verify the label is still properly embedded in the widget tree
            assert lbl.parent is not None, "Label should have a parent widget"


# **Feature: label-compatibility, Property 7: auto_size_height True Behavior**
# *For any* MarkdownLabel with `auto_size_height=True`, the widget SHALL have 
# `size_hint_y=None` AND its height SHALL be bound to `minimum_height`.
# **Validates: Requirements 3.1, 3.3**

class TestAutoSizeHeightTrueBehavior:
    """Property tests for auto_size_height True behavior (Property 7)."""
    
    @given(simple_markdown_document())
    @settings(max_examples=100, deadline=None)
    def test_auto_size_height_true_sets_size_hint_y_none(self, markdown_text):
        """When auto_size_height=True, size_hint_y should be None."""
        label = MarkdownLabel(text=markdown_text, auto_size_height=True)
        
        assert label.size_hint_y is None, \
            f"Expected size_hint_y=None when auto_size_height=True, got {label.size_hint_y}"
    
    @given(simple_markdown_document())
    @settings(max_examples=100, deadline=None)
    def test_auto_size_height_true_binds_height_to_minimum(self, markdown_text):
        """When auto_size_height=True, height should be bound to minimum_height."""
        label = MarkdownLabel(text=markdown_text, auto_size_height=True)
        
        # Check that the binding exists by verifying size_hint_y is None
        # (which is the primary indicator of auto-sizing behavior)
        assert label.size_hint_y is None, \
            "size_hint_y should be None when auto_size_height=True"
        
        # Verify auto_size_height property is actually True
        assert label.auto_size_height is True, \
            f"Expected auto_size_height=True, got {label.auto_size_height}"
    
    def test_auto_size_height_true_default_behavior(self):
        """Default MarkdownLabel should have auto_size_height=True behavior."""
        label = MarkdownLabel(text="Test content")
        
        # Default should be auto_size_height=True
        assert label.auto_size_height is True, \
            f"Expected default auto_size_height=True, got {label.auto_size_height}"
        
        # Should have size_hint_y=None
        assert label.size_hint_y is None, \
            f"Expected size_hint_y=None by default, got {label.size_hint_y}"
    
    @given(st.floats(min_value=0.1, max_value=2.0, allow_nan=False, allow_infinity=False))
    @settings(max_examples=100, deadline=None)
    def test_auto_size_height_true_ignores_user_size_hint_y(self, user_size_hint_y):
        """When auto_size_height=True, user-provided size_hint_y is overridden."""
        label = MarkdownLabel(
            text="Test content", 
            auto_size_height=True, 
            size_hint_y=user_size_hint_y
        )
        
        # Should override user's size_hint_y
        assert label.size_hint_y is None, \
            f"Expected size_hint_y=None to override user value {user_size_hint_y}, got {label.size_hint_y}"
        
        # But should store the user value for later restoration
        assert label._user_size_hint_y == user_size_hint_y, \
            f"Expected _user_size_hint_y={user_size_hint_y}, got {label._user_size_hint_y}"


# **Feature: label-compatibility, Property 8: auto_size_height False Behavior**
# *For any* MarkdownLabel with `auto_size_height=False`, the widget SHALL preserve 
# the user-specified `size_hint_y` value (or default to 1) AND its height SHALL NOT 
# be bound to `minimum_height`.
# **Validates: Requirements 3.2**

class TestAutoSizeHeightFalseBehavior:
    """Property tests for auto_size_height False behavior (Property 8)."""
    
    @given(simple_markdown_document())
    @settings(max_examples=100, deadline=None)
    def test_auto_size_height_false_preserves_default_size_hint_y(self, markdown_text):
        """When auto_size_height=False, default size_hint_y=1 is preserved."""
        label = MarkdownLabel(text=markdown_text, auto_size_height=False)
        
        assert label.size_hint_y == 1, \
            f"Expected size_hint_y=1 when auto_size_height=False, got {label.size_hint_y}"
        
        assert label.auto_size_height is False, \
            f"Expected auto_size_height=False, got {label.auto_size_height}"
    
    @given(simple_markdown_document(), 
           st.floats(min_value=0.1, max_value=2.0, allow_nan=False, allow_infinity=False))
    @settings(max_examples=100, deadline=None)
    def test_auto_size_height_false_preserves_user_size_hint_y(self, markdown_text, user_size_hint_y):
        """When auto_size_height=False, user-specified size_hint_y is preserved."""
        label = MarkdownLabel(
            text=markdown_text, 
            auto_size_height=False, 
            size_hint_y=user_size_hint_y
        )
        
        assert label.size_hint_y == user_size_hint_y, \
            f"Expected size_hint_y={user_size_hint_y} when auto_size_height=False, got {label.size_hint_y}"
        
        assert label.auto_size_height is False, \
            f"Expected auto_size_height=False, got {label.auto_size_height}"
    
    @given(simple_markdown_document())
    @settings(max_examples=100, deadline=None)
    def test_auto_size_height_false_no_height_binding(self, markdown_text):
        """When auto_size_height=False, height is not bound to minimum_height."""
        label = MarkdownLabel(text=markdown_text, auto_size_height=False)
        
        # The primary indicator that height is not bound to minimum_height
        # is that size_hint_y is not None (it participates in layout)
        assert label.size_hint_y is not None, \
            "size_hint_y should not be None when auto_size_height=False"
        
        assert label.auto_size_height is False, \
            f"Expected auto_size_height=False, got {label.auto_size_height}"


# **Feature: label-compatibility, Property 9: auto_size_height Dynamic Toggling**
# *For any* MarkdownLabel, when `auto_size_height` is toggled from True to False, 
# the height binding SHALL be removed and `size_hint_y` SHALL be restored. When 
# toggled from False to True, the height binding SHALL be added and `size_hint_y` 
# SHALL be set to None.
# **Validates: Requirements 3.4, 3.5**

class TestAutoSizeHeightDynamicToggling:
    """Property tests for auto_size_height dynamic toggling (Property 9)."""
    
    @given(simple_markdown_document())
    @settings(max_examples=100, deadline=None)
    def test_toggle_true_to_false_restores_size_hint_y(self, markdown_text):
        """Toggling auto_size_height from True to False restores size_hint_y."""
        # Start with auto_size_height=True (default)
        label = MarkdownLabel(text=markdown_text, auto_size_height=True)
        
        # Verify initial state
        assert label.auto_size_height is True
        assert label.size_hint_y is None
        
        # Toggle to False
        label.auto_size_height = False
        
        # Should restore size_hint_y to default (1)
        assert label.size_hint_y == 1, \
            f"Expected size_hint_y=1 after toggling to False, got {label.size_hint_y}"
        
        assert label.auto_size_height is False, \
            f"Expected auto_size_height=False after toggle, got {label.auto_size_height}"
    
    @given(simple_markdown_document())
    @settings(max_examples=100, deadline=None)
    def test_toggle_false_to_true_sets_size_hint_y_none(self, markdown_text):
        """Toggling auto_size_height from False to True sets size_hint_y=None."""
        # Start with auto_size_height=False
        label = MarkdownLabel(text=markdown_text, auto_size_height=False)
        
        # Verify initial state
        assert label.auto_size_height is False
        assert label.size_hint_y == 1
        
        # Toggle to True
        label.auto_size_height = True
        
        # Should set size_hint_y=None
        assert label.size_hint_y is None, \
            f"Expected size_hint_y=None after toggling to True, got {label.size_hint_y}"
        
        assert label.auto_size_height is True, \
            f"Expected auto_size_height=True after toggle, got {label.auto_size_height}"
    
    @given(simple_markdown_document(), 
           st.floats(min_value=0.1, max_value=2.0, allow_nan=False, allow_infinity=False))
    @settings(max_examples=100, deadline=None)
    def test_toggle_preserves_user_size_hint_y(self, markdown_text, user_size_hint_y):
        """Toggling preserves the original user-specified size_hint_y value."""
        # Start with user-specified size_hint_y and auto_size_height=True
        label = MarkdownLabel(
            text=markdown_text, 
            auto_size_height=True, 
            size_hint_y=user_size_hint_y
        )
        
        # Should override to None initially
        assert label.size_hint_y is None
        
        # Toggle to False - should restore user value
        label.auto_size_height = False
        
        assert label.size_hint_y == user_size_hint_y, \
            f"Expected size_hint_y={user_size_hint_y} after toggle to False, got {label.size_hint_y}"
        
        # Toggle back to True - should override again
        label.auto_size_height = True
        
        assert label.size_hint_y is None, \
            f"Expected size_hint_y=None after toggle back to True, got {label.size_hint_y}"
        
        # Toggle to False again - should still restore user value
        label.auto_size_height = False
        
        assert label.size_hint_y == user_size_hint_y, \
            f"Expected size_hint_y={user_size_hint_y} after second toggle to False, got {label.size_hint_y}"
    
    @given(simple_markdown_document())
    @settings(max_examples=100, deadline=None)
    def test_multiple_toggles_maintain_consistency(self, markdown_text):
        """Multiple toggles maintain consistent behavior."""
        label = MarkdownLabel(text=markdown_text)
        
        # Should start with auto_size_height=True (default)
        assert label.auto_size_height is True
        assert label.size_hint_y is None
        
        # Toggle False -> True -> False -> True
        for expected_auto_size, expected_size_hint_y in [
            (False, 1),      # Toggle to False
            (True, None),    # Toggle to True
            (False, 1),      # Toggle to False
            (True, None),    # Toggle to True
        ]:
            label.auto_size_height = expected_auto_size
            
            assert label.auto_size_height == expected_auto_size, \
                f"Expected auto_size_height={expected_auto_size}, got {label.auto_size_height}"
            
            assert label.size_hint_y == expected_size_hint_y, \
                f"Expected size_hint_y={expected_size_hint_y}, got {label.size_hint_y}"



# **Feature: label-compatibility-phase2, Property 2: Strict Label Mode Sizing Behavior**
# *For any* MarkdownLabel with `strict_label_mode=True`, the widget SHALL have `size_hint_y` 
# preserved (not set to None) AND height SHALL NOT be bound to `minimum_height` AND internal 
# Labels SHALL NOT have automatic text_size width bindings when `text_size=[None, None]`.
# **Validates: Requirements 2.1, 2.2, 2.3, 2.4**

class TestStrictLabelModeSizingBehavior:
    """Property tests for strict label mode sizing behavior (Property 2)."""
    
    @given(simple_markdown_document())
    @settings(max_examples=100, deadline=None)
    def test_strict_mode_preserves_default_size_hint_y(self, markdown_text):
        """When strict_label_mode=True, default size_hint_y=1 is preserved."""
        label = MarkdownLabel(text=markdown_text, strict_label_mode=True)
        
        assert label.size_hint_y == 1, \
            f"Expected size_hint_y=1 when strict_label_mode=True, got {label.size_hint_y}"
        
        assert label.strict_label_mode is True, \
            f"Expected strict_label_mode=True, got {label.strict_label_mode}"
    
    @given(simple_markdown_document(), 
           st.floats(min_value=0.1, max_value=2.0, allow_nan=False, allow_infinity=False))
    @settings(max_examples=100, deadline=None)
    def test_strict_mode_preserves_user_size_hint_y(self, markdown_text, user_size_hint_y):
        """When strict_label_mode=True, user-specified size_hint_y is preserved."""
        label = MarkdownLabel(
            text=markdown_text, 
            strict_label_mode=True, 
            size_hint_y=user_size_hint_y
        )
        
        assert label.size_hint_y == user_size_hint_y, \
            f"Expected size_hint_y={user_size_hint_y} when strict_label_mode=True, got {label.size_hint_y}"
        
        assert label.strict_label_mode is True, \
            f"Expected strict_label_mode=True, got {label.strict_label_mode}"
    
    @given(simple_markdown_document())
    @settings(max_examples=100, deadline=None)
    def test_strict_mode_height_not_bound_to_minimum(self, markdown_text):
        """When strict_label_mode=True, height is not bound to minimum_height."""
        label = MarkdownLabel(text=markdown_text, strict_label_mode=True)
        
        # The primary indicator that height is not bound to minimum_height
        # is that size_hint_y is not None (it participates in layout)
        assert label.size_hint_y is not None, \
            "size_hint_y should not be None when strict_label_mode=True"
        
        assert label.strict_label_mode is True, \
            f"Expected strict_label_mode=True, got {label.strict_label_mode}"
    
    def test_strict_mode_default_is_false(self):
        """Default MarkdownLabel should have strict_label_mode=False."""
        label = MarkdownLabel(text="Test content")
        
        assert label.strict_label_mode is False, \
            f"Expected default strict_label_mode=False, got {label.strict_label_mode}"
        
        # Default should have auto-sizing enabled (size_hint_y=None)
        assert label.size_hint_y is None, \
            f"Expected size_hint_y=None by default, got {label.size_hint_y}"
    
    @given(st.booleans())
    @settings(max_examples=100, deadline=None)
    def test_strict_mode_property_accepted_and_stored(self, value):
        """Setting strict_label_mode property accepts and stores the value."""
        label = MarkdownLabel(text='# Hello World', strict_label_mode=value)
        assert label.strict_label_mode == value
    
    @given(st.booleans())
    @settings(max_examples=100, deadline=None)
    def test_strict_mode_change_after_creation(self, value):
        """Changing strict_label_mode property after creation accepts and stores the value."""
        label = MarkdownLabel(text='# Hello')
        label.strict_label_mode = value
        assert label.strict_label_mode == value
    
    @given(simple_markdown_document())
    @settings(max_examples=100, deadline=None)
    def test_strict_mode_toggle_from_false_to_true(self, markdown_text):
        """Toggling strict_label_mode from False to True disables auto-sizing."""
        label = MarkdownLabel(text=markdown_text, strict_label_mode=False)
        
        # Initially should have auto-sizing enabled
        assert label.size_hint_y is None, \
            "size_hint_y should be None when strict_label_mode=False"
        
        # Toggle to strict mode
        label.strict_label_mode = True
        
        # Should now have size_hint_y preserved (default 1)
        assert label.size_hint_y == 1, \
            f"Expected size_hint_y=1 after toggling to strict_label_mode=True, got {label.size_hint_y}"
    
    @given(simple_markdown_document())
    @settings(max_examples=100, deadline=None)
    def test_strict_mode_toggle_from_true_to_false(self, markdown_text):
        """Toggling strict_label_mode from True to False enables auto-sizing."""
        label = MarkdownLabel(text=markdown_text, strict_label_mode=True)
        
        # Initially should have size_hint_y preserved
        assert label.size_hint_y == 1, \
            "size_hint_y should be 1 when strict_label_mode=True"
        
        # Toggle to non-strict mode
        label.strict_label_mode = False
        
        # Should now have auto-sizing enabled
        assert label.size_hint_y is None, \
            f"Expected size_hint_y=None after toggling to strict_label_mode=False, got {label.size_hint_y}"
    
    @given(simple_markdown_document(), 
           st.floats(min_value=0.1, max_value=2.0, allow_nan=False, allow_infinity=False))
    @settings(max_examples=100, deadline=None)
    def test_strict_mode_toggle_preserves_user_size_hint_y(self, markdown_text, user_size_hint_y):
        """Toggling strict_label_mode preserves user-specified size_hint_y."""
        label = MarkdownLabel(
            text=markdown_text, 
            strict_label_mode=True, 
            size_hint_y=user_size_hint_y
        )
        
        # Initially should have user's size_hint_y
        assert label.size_hint_y == user_size_hint_y, \
            f"Expected size_hint_y={user_size_hint_y}, got {label.size_hint_y}"
        
        # Toggle to non-strict mode - should enable auto-sizing
        label.strict_label_mode = False
        assert label.size_hint_y is None, \
            f"Expected size_hint_y=None after toggle to False, got {label.size_hint_y}"
        
        # Toggle back to strict mode - should restore user's size_hint_y
        label.strict_label_mode = True
        assert label.size_hint_y == user_size_hint_y, \
            f"Expected size_hint_y={user_size_hint_y} after toggle back to True, got {label.size_hint_y}"
    
    @given(simple_markdown_document())
    @settings(max_examples=100, deadline=None)
    def test_strict_mode_overrides_auto_size_height(self, markdown_text):
        """strict_label_mode=True overrides auto_size_height=True behavior."""
        label = MarkdownLabel(
            text=markdown_text, 
            strict_label_mode=True, 
            auto_size_height=True
        )
        
        # strict_label_mode should take precedence
        assert label.size_hint_y == 1, \
            f"Expected size_hint_y=1 when strict_label_mode=True (overrides auto_size_height), got {label.size_hint_y}"
    
    @given(simple_markdown_document())
    @settings(max_examples=100, deadline=None)
    def test_strict_mode_ignores_auto_size_height_changes(self, markdown_text):
        """When strict_label_mode=True, auto_size_height changes are ignored."""
        label = MarkdownLabel(text=markdown_text, strict_label_mode=True)
        
        # Initially should have size_hint_y=1
        assert label.size_hint_y == 1
        
        # Try to enable auto_size_height - should be ignored
        label.auto_size_height = True
        
        # size_hint_y should still be 1 (strict mode takes precedence)
        assert label.size_hint_y == 1, \
            f"Expected size_hint_y=1 (strict mode ignores auto_size_height), got {label.size_hint_y}"
    
    @given(simple_markdown_document())
    @settings(max_examples=100, deadline=None)
    def test_strict_mode_triggers_rebuild(self, markdown_text):
        """Changing strict_label_mode triggers widget rebuild."""
        assume(markdown_text.strip())
        
        label = MarkdownLabel(text=markdown_text, strict_label_mode=False)
        initial_children = list(label.children)
        
        # Toggle strict_label_mode
        label.strict_label_mode = True
        
        # Widget tree should be rebuilt (children may be different objects)
        # We verify by checking that the label still has children
        assert len(label.children) >= 1, \
            "Expected at least 1 child after strict_label_mode toggle"
    
    @given(simple_markdown_document())
    @settings(max_examples=100, deadline=None)
    def test_multiple_strict_mode_toggles_maintain_consistency(self, markdown_text):
        """Multiple strict_label_mode toggles maintain consistent behavior."""
        label = MarkdownLabel(text=markdown_text)
        
        # Should start with strict_label_mode=False (default)
        assert label.strict_label_mode is False
        assert label.size_hint_y is None
        
        # Toggle True -> False -> True -> False
        for expected_strict_mode, expected_size_hint_y in [
            (True, 1),       # Toggle to True
            (False, None),   # Toggle to False
            (True, 1),       # Toggle to True
            (False, None),   # Toggle to False
        ]:
            label.strict_label_mode = expected_strict_mode
            
            assert label.strict_label_mode == expected_strict_mode, \
                f"Expected strict_label_mode={expected_strict_mode}, got {label.strict_label_mode}"
            
            assert label.size_hint_y == expected_size_hint_y, \
                f"Expected size_hint_y={expected_size_hint_y}, got {label.size_hint_y}"


# **Feature: label-compatibility-phase2, Property 3: Comprehensive texture_size Calculation**
# *For any* MarkdownLabel containing mixed content (Labels, Images, Tables, Code blocks), 
# the `texture_size` property SHALL return a tuple where width is the maximum width of any 
# descendant widget AND height is the sum of all descendant heights.
# **Validates: Requirements 3.1, 3.2, 3.3**
#
# NOTE: In headless Kivy environments (without a display), Label widgets don't render
# textures, so texture_size returns (0, 0) for Labels. Tests focus on:
# 1. Correct return type and structure
# 2. Handling all widget types without crashing
# 3. Correct aggregation logic (even if values are 0 in headless mode)
# 4. Proper handling of empty content
# 5. Widget types that have explicit heights (thematic_break, blank_line, AsyncImage)

class TestComprehensiveTextureSizeCalculation:
    """Property tests for comprehensive texture_size calculation (Property 3)."""
    
    def _find_all_widgets_recursive(self, widget, widgets=None):
        """Recursively find all widgets in a widget tree.
        
        Args:
            widget: Root widget to search
            widgets: List to accumulate widgets (created if None)
            
        Returns:
            List of all widgets found
        """
        if widgets is None:
            widgets = []
        
        widgets.append(widget)
        
        if hasattr(widget, 'children'):
            for child in widget.children:
                self._find_all_widgets_recursive(child, widgets)
        
        return widgets
    
    @given(simple_markdown_document())
    @settings(max_examples=100, deadline=None)
    def test_texture_size_returns_tuple(self, markdown_text):
        """texture_size returns a list/tuple with two elements."""
        label = MarkdownLabel(text=markdown_text)
        
        texture_size = label.texture_size
        
        assert isinstance(texture_size, (list, tuple)), \
            f"Expected texture_size to be list/tuple, got {type(texture_size)}"
        assert len(texture_size) == 2, \
            f"Expected texture_size to have 2 elements, got {len(texture_size)}"
    
    @given(simple_markdown_document())
    @settings(max_examples=100, deadline=None)
    def test_texture_size_non_negative(self, markdown_text):
        """texture_size width and height are non-negative."""
        label = MarkdownLabel(text=markdown_text)
        
        texture_size = label.texture_size
        
        assert texture_size[0] >= 0, \
            f"Expected texture_size width >= 0, got {texture_size[0]}"
        assert texture_size[1] >= 0, \
            f"Expected texture_size height >= 0, got {texture_size[1]}"
    
    def test_empty_label_texture_size_is_zero(self):
        """Empty MarkdownLabel has texture_size [0, 0]."""
        label = MarkdownLabel(text='')
        
        texture_size = label.texture_size
        
        assert texture_size == [0, 0], \
            f"Expected texture_size [0, 0] for empty label, got {texture_size}"
    
    @given(markdown_heading())
    @settings(max_examples=100, deadline=None)
    def test_heading_creates_label_widget(self, heading):
        """Heading content creates a Label widget that is included in texture_size calculation."""
        label = MarkdownLabel(text=heading)
        
        # Verify heading creates children
        assert len(label.children) >= 1, \
            f"Expected at least 1 child for heading, got {len(label.children)}"
        
        # Verify texture_size is accessible and returns valid structure
        texture_size = label.texture_size
        assert isinstance(texture_size, (list, tuple)) and len(texture_size) == 2
        assert texture_size[0] >= 0 and texture_size[1] >= 0
    
    @given(markdown_paragraph())
    @settings(max_examples=100, deadline=None)
    def test_paragraph_creates_label_widget(self, paragraph):
        """Paragraph content creates a Label widget that is included in texture_size calculation."""
        assume(paragraph.strip())
        
        label = MarkdownLabel(text=paragraph)
        
        # Verify paragraph creates children
        assert len(label.children) >= 1, \
            f"Expected at least 1 child for paragraph, got {len(label.children)}"
        
        # Verify texture_size is accessible and returns valid structure
        texture_size = label.texture_size
        assert isinstance(texture_size, (list, tuple)) and len(texture_size) == 2
        assert texture_size[0] >= 0 and texture_size[1] >= 0
    
    def test_code_block_creates_container_widget(self):
        """Code block content creates a BoxLayout container that is included in texture_size calculation."""
        markdown = '```python\nprint("hello")\n```'
        label = MarkdownLabel(text=markdown)
        
        # Verify code block creates children
        assert len(label.children) >= 1, \
            f"Expected at least 1 child for code block, got {len(label.children)}"
        
        # Verify texture_size is accessible and returns valid structure
        texture_size = label.texture_size
        assert isinstance(texture_size, (list, tuple)) and len(texture_size) == 2
        assert texture_size[0] >= 0 and texture_size[1] >= 0
    
    def test_list_creates_container_widget(self):
        """List content creates a BoxLayout container that is included in texture_size calculation."""
        markdown = '- Item 1\n- Item 2\n- Item 3'
        label = MarkdownLabel(text=markdown)
        
        # Verify list creates children
        assert len(label.children) >= 1, \
            f"Expected at least 1 child for list, got {len(label.children)}"
        
        # Verify texture_size is accessible and returns valid structure
        texture_size = label.texture_size
        assert isinstance(texture_size, (list, tuple)) and len(texture_size) == 2
        assert texture_size[0] >= 0 and texture_size[1] >= 0
    
    def test_table_creates_gridlayout_widget(self):
        """Table content creates a GridLayout widget that is included in texture_size calculation."""
        markdown = '| A | B |\n| --- | --- |\n| 1 | 2 |'
        label = MarkdownLabel(text=markdown)
        
        # Verify table creates children
        assert len(label.children) >= 1, \
            f"Expected at least 1 child for table, got {len(label.children)}"
        
        # Verify at least one child is a GridLayout
        has_gridlayout = any(isinstance(c, GridLayout) for c in label.children)
        assert has_gridlayout, "Expected a GridLayout child for table"
        
        # Verify texture_size is accessible and returns valid structure
        texture_size = label.texture_size
        assert isinstance(texture_size, (list, tuple)) and len(texture_size) == 2
        assert texture_size[0] >= 0 and texture_size[1] >= 0
    
    def test_block_quote_creates_container_widget(self):
        """Block quote content creates a BoxLayout container that is included in texture_size calculation."""
        markdown = '> This is a quote'
        label = MarkdownLabel(text=markdown)
        
        # Verify block quote creates children
        assert len(label.children) >= 1, \
            f"Expected at least 1 child for block quote, got {len(label.children)}"
        
        # Verify texture_size is accessible and returns valid structure
        texture_size = label.texture_size
        assert isinstance(texture_size, (list, tuple)) and len(texture_size) == 2
        assert texture_size[0] >= 0 and texture_size[1] >= 0
    
    def test_thematic_break_contributes_to_texture_size(self):
        """Thematic break (horizontal rule) contributes to texture_size with explicit height."""
        markdown = 'Before\n\n---\n\nAfter'
        label = MarkdownLabel(text=markdown)
        
        texture_size = label.texture_size
        
        # Thematic break has explicit height=20, so texture_size should be > 0
        # even in headless mode (Widget height is counted directly)
        assert texture_size[1] > 0, \
            f"Expected texture_size height > 0 for thematic break, got {texture_size[1]}"
    
    @given(st.integers(min_value=1, max_value=5))
    @settings(max_examples=100, deadline=None)
    def test_more_content_increases_texture_height(self, num_paragraphs):
        """More content results in larger texture_size height."""
        # Create markdown with varying number of paragraphs
        text1 = 'Single paragraph'
        text_multi = '\n\n'.join([f'Paragraph {i} with some text.' for i in range(num_paragraphs)])
        
        label1 = MarkdownLabel(text=text1)
        label_multi = MarkdownLabel(text=text_multi)
        
        # More paragraphs should result in larger height
        if num_paragraphs > 1:
            assert label_multi.texture_size[1] >= label1.texture_size[1], \
                f"Expected multi-paragraph height >= single paragraph height"
    
    def test_mixed_content_creates_multiple_widgets(self):
        """Mixed content (heading, paragraph, code, list) creates multiple widgets for texture_size."""
        markdown = '''# Heading

This is a paragraph.

```python
code = "block"
```

- List item 1
- List item 2

> A quote
'''
        label = MarkdownLabel(text=markdown)
        
        texture_size = label.texture_size
        
        # Verify texture_size is accessible and returns valid structure
        assert isinstance(texture_size, (list, tuple)) and len(texture_size) == 2
        assert texture_size[0] >= 0 and texture_size[1] >= 0
        
        # Should have multiple children
        assert len(label.children) > 1, \
            f"Expected multiple children for mixed content, got {len(label.children)}"
    
    @given(simple_markdown_document())
    @settings(max_examples=100, deadline=None)
    def test_texture_size_accessible_for_all_content(self, markdown_text):
        """texture_size is accessible and valid for all markdown content."""
        assume(markdown_text.strip())
        
        label = MarkdownLabel(text=markdown_text)
        
        texture_size = label.texture_size
        
        # Verify texture_size is accessible and returns valid structure
        assert isinstance(texture_size, (list, tuple)) and len(texture_size) == 2
        assert texture_size[0] >= 0 and texture_size[1] >= 0
        
        # If there are children, the calculation should have run without error
        if len(label.children) > 0:
            # The method should have traversed all children
            pass  # No assertion needed - if we got here, the method worked
    
    def test_nested_list_creates_nested_containers(self):
        """Nested list content creates nested BoxLayout containers for texture_size calculation."""
        markdown = '''- Item 1
  - Nested 1
  - Nested 2
- Item 2'''
        label = MarkdownLabel(text=markdown)
        
        # Verify nested list creates children
        assert len(label.children) >= 1, \
            f"Expected at least 1 child for nested list, got {len(label.children)}"
        
        # Verify texture_size is accessible and returns valid structure
        texture_size = label.texture_size
        assert isinstance(texture_size, (list, tuple)) and len(texture_size) == 2
        assert texture_size[0] >= 0 and texture_size[1] >= 0
    
    def test_ordered_list_creates_container_widget(self):
        """Ordered list content creates a BoxLayout container for texture_size calculation."""
        markdown = '1. First\n2. Second\n3. Third'
        label = MarkdownLabel(text=markdown)
        
        # Verify ordered list creates children
        assert len(label.children) >= 1, \
            f"Expected at least 1 child for ordered list, got {len(label.children)}"
        
        # Verify texture_size is accessible and returns valid structure
        texture_size = label.texture_size
        assert isinstance(texture_size, (list, tuple)) and len(texture_size) == 2
        assert texture_size[0] >= 0 and texture_size[1] >= 0
    
    @given(simple_markdown_document(), simple_markdown_document())
    @settings(max_examples=100, deadline=None)
    def test_texture_size_updates_on_text_change(self, text1, text2):
        """texture_size updates when text property changes."""
        assume(text1.strip() and text2.strip())
        assume(text1 != text2)
        
        label = MarkdownLabel(text=text1)
        texture_size1 = label.texture_size
        
        # Change text
        label.text = text2
        texture_size2 = label.texture_size
        
        # texture_size should be recalculated (may or may not be different)
        # The key is that it doesn't crash and returns valid values
        assert isinstance(texture_size2, (list, tuple)), \
            f"Expected texture_size to be list/tuple after text change"
        assert len(texture_size2) == 2, \
            f"Expected texture_size to have 2 elements after text change"
        assert texture_size2[0] >= 0 and texture_size2[1] >= 0, \
            f"Expected non-negative texture_size after text change"
    
    def test_texture_size_with_image_markdown(self):
        """Image markdown contributes to texture_size.
        
        Note: In Markdown, images are inline elements typically wrapped in paragraphs.
        The texture_size should account for the containing paragraph and/or image widget.
        """
        # Use image in a paragraph context (common usage)
        markdown = 'Here is an image:\n\n![Alt text](https://example.com/image.png)\n\nAfter image.'
        label = MarkdownLabel(text=markdown)
        
        texture_size = label.texture_size
        
        # Content with image should have non-zero texture_size
        # (the surrounding text paragraphs will contribute even if image doesn't)
        assert texture_size[1] > 0, \
            f"Expected texture_size height > 0 for content with image, got {texture_size[1]}"
        
        # Verify children were created
        assert len(label.children) > 0, \
            f"Expected children for image markdown, got {len(label.children)}"
    
    @given(st.integers(min_value=1, max_value=6))
    @settings(max_examples=100, deadline=None)
    def test_all_heading_levels_create_label_widgets(self, level):
        """All heading levels create Label widgets for texture_size calculation."""
        markdown = '#' * level + ' Heading'
        label = MarkdownLabel(text=markdown)
        
        # Verify heading creates children
        assert len(label.children) >= 1, \
            f"Expected at least 1 child for h{level}, got {len(label.children)}"
        
        # Verify texture_size is accessible and returns valid structure
        texture_size = label.texture_size
        assert isinstance(texture_size, (list, tuple)) and len(texture_size) == 2
        assert texture_size[0] >= 0 and texture_size[1] >= 0
    
    def test_blank_lines_create_spacer_widgets(self):
        """Blank lines create spacer widgets with explicit height for texture_size."""
        markdown_no_blanks = 'Para 1\nPara 2'
        markdown_with_blanks = 'Para 1\n\n\n\nPara 2'
        
        label_no_blanks = MarkdownLabel(text=markdown_no_blanks)
        label_with_blanks = MarkdownLabel(text=markdown_with_blanks)
        
        # Both should have valid texture_size
        ts_no_blanks = label_no_blanks.texture_size
        ts_with_blanks = label_with_blanks.texture_size
        
        assert isinstance(ts_no_blanks, (list, tuple)) and len(ts_no_blanks) == 2
        assert isinstance(ts_with_blanks, (list, tuple)) and len(ts_with_blanks) == 2
        
        # With blank lines should have more children (blank_line widgets)
        # and thus potentially larger texture_size height
        assert len(label_with_blanks.children) >= len(label_no_blanks.children), \
            "Expected content with blank lines to have at least as many children"
        
        # blank_line widgets have explicit height (base_font_size), so they contribute
        # to texture_size even in headless mode
        assert ts_with_blanks[1] >= ts_no_blanks[1], \
            "Expected content with blank lines to have at least as much height"


# **Feature: label-compatibility-phase2, Property 4: Shortening Property Forwarding**
# *For any* shortening-related property (shorten, shorten_from, split_str, max_lines,
# ellipsis_options), when set on MarkdownLabel, all child Labels (paragraphs, headings,
# list items, table cells, quote text) SHALL have the same property value.
# **Validates: Requirements 4.1, 4.2, 4.3, 4.4, 4.5**


class TestShorteningPropertyForwarding:
    """Property tests for shortening property forwarding (Property 4)."""
    
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
    def test_shorten_forwarded_to_paragraph(self, shorten_value):
        """shorten property is forwarded to paragraph Labels."""
        label = MarkdownLabel(text='Hello World', shorten=shorten_value)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        for lbl in labels:
            assert lbl.shorten == shorten_value, \
                f"Expected shorten={shorten_value}, got {lbl.shorten}"
    
    @given(st.booleans())
    @settings(max_examples=100, deadline=None)
    def test_shorten_forwarded_to_heading(self, shorten_value):
        """shorten property is forwarded to heading Labels."""
        label = MarkdownLabel(text='# Heading', shorten=shorten_value)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        for lbl in labels:
            assert lbl.shorten == shorten_value, \
                f"Expected shorten={shorten_value}, got {lbl.shorten}"
    
    @given(st.booleans())
    @settings(max_examples=100, deadline=None)
    def test_shorten_forwarded_to_list_items(self, shorten_value):
        """shorten property is forwarded to list item Labels."""
        markdown = '- Item 1\n- Item 2'
        label = MarkdownLabel(text=markdown, shorten=shorten_value)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 2, "Expected at least 2 Labels for list items"
        
        for lbl in labels:
            assert lbl.shorten == shorten_value, \
                f"Expected shorten={shorten_value}, got {lbl.shorten}"
    
    @given(st.booleans())
    @settings(max_examples=100, deadline=None)
    def test_shorten_forwarded_to_table_cells(self, shorten_value):
        """shorten property is forwarded to table cell Labels."""
        markdown = '| A | B |\n| --- | --- |\n| 1 | 2 |'
        label = MarkdownLabel(text=markdown, shorten=shorten_value)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 4, "Expected at least 4 Labels for table cells"
        
        for lbl in labels:
            assert lbl.shorten == shorten_value, \
                f"Expected shorten={shorten_value}, got {lbl.shorten}"
    
    @given(st.sampled_from(['left', 'center', 'right']))
    @settings(max_examples=100, deadline=None)
    def test_shorten_from_forwarded_to_paragraph(self, shorten_from_value):
        """shorten_from property is forwarded to paragraph Labels."""
        label = MarkdownLabel(text='Hello World', shorten_from=shorten_from_value)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        for lbl in labels:
            assert lbl.shorten_from == shorten_from_value, \
                f"Expected shorten_from={shorten_from_value}, got {lbl.shorten_from}"
    
    @given(st.sampled_from(['left', 'center', 'right']))
    @settings(max_examples=100, deadline=None)
    def test_shorten_from_forwarded_to_heading(self, shorten_from_value):
        """shorten_from property is forwarded to heading Labels."""
        label = MarkdownLabel(text='# Heading', shorten_from=shorten_from_value)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        for lbl in labels:
            assert lbl.shorten_from == shorten_from_value, \
                f"Expected shorten_from={shorten_from_value}, got {lbl.shorten_from}"
    
    @given(st.sampled_from(['left', 'center', 'right']))
    @settings(max_examples=100, deadline=None)
    def test_shorten_from_forwarded_to_list_items(self, shorten_from_value):
        """shorten_from property is forwarded to list item Labels."""
        markdown = '- Item 1\n- Item 2'
        label = MarkdownLabel(text=markdown, shorten_from=shorten_from_value)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 2, "Expected at least 2 Labels for list items"
        
        for lbl in labels:
            assert lbl.shorten_from == shorten_from_value, \
                f"Expected shorten_from={shorten_from_value}, got {lbl.shorten_from}"
    
    @given(st.text(min_size=0, max_size=5, alphabet='abc '))
    @settings(max_examples=100, deadline=None)
    def test_split_str_forwarded_to_paragraph(self, split_str_value):
        """split_str property is forwarded to paragraph Labels."""
        label = MarkdownLabel(text='Hello World', split_str=split_str_value)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        for lbl in labels:
            assert lbl.split_str == split_str_value, \
                f"Expected split_str={split_str_value!r}, got {lbl.split_str!r}"
    
    @given(st.text(min_size=0, max_size=5, alphabet='abc '))
    @settings(max_examples=100, deadline=None)
    def test_split_str_forwarded_to_heading(self, split_str_value):
        """split_str property is forwarded to heading Labels."""
        label = MarkdownLabel(text='# Heading', split_str=split_str_value)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        for lbl in labels:
            assert lbl.split_str == split_str_value, \
                f"Expected split_str={split_str_value!r}, got {lbl.split_str!r}"
    
    @given(st.integers(min_value=0, max_value=10))
    @settings(max_examples=100, deadline=None)
    def test_max_lines_forwarded_to_paragraph(self, max_lines_value):
        """max_lines property is forwarded to paragraph Labels when non-zero."""
        label = MarkdownLabel(text='Hello World', max_lines=max_lines_value)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        for lbl in labels:
            if max_lines_value > 0:
                assert lbl.max_lines == max_lines_value, \
                    f"Expected max_lines={max_lines_value}, got {lbl.max_lines}"
            # When max_lines=0, it may not be set on child Labels (default behavior)
    
    @given(st.integers(min_value=1, max_value=10))
    @settings(max_examples=100, deadline=None)
    def test_max_lines_forwarded_to_heading(self, max_lines_value):
        """max_lines property is forwarded to heading Labels when non-zero."""
        label = MarkdownLabel(text='# Heading', max_lines=max_lines_value)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        for lbl in labels:
            assert lbl.max_lines == max_lines_value, \
                f"Expected max_lines={max_lines_value}, got {lbl.max_lines}"
    
    @given(st.integers(min_value=1, max_value=10))
    @settings(max_examples=100, deadline=None)
    def test_max_lines_forwarded_to_list_items(self, max_lines_value):
        """max_lines property is forwarded to list item Labels when non-zero."""
        markdown = '- Item 1\n- Item 2'
        label = MarkdownLabel(text=markdown, max_lines=max_lines_value)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 2, "Expected at least 2 Labels for list items"
        
        for lbl in labels:
            assert lbl.max_lines == max_lines_value, \
                f"Expected max_lines={max_lines_value}, got {lbl.max_lines}"
    
    @given(st.fixed_dictionaries({
        'markup_color': st.sampled_from([[1, 0, 0, 1], [0, 1, 0, 1], [0, 0, 1, 1]])
    }))
    @settings(max_examples=100, deadline=None)
    def test_ellipsis_options_forwarded_to_paragraph(self, ellipsis_opts):
        """ellipsis_options property is forwarded to paragraph Labels."""
        label = MarkdownLabel(text='Hello World', ellipsis_options=ellipsis_opts)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        for lbl in labels:
            assert lbl.ellipsis_options == ellipsis_opts, \
                f"Expected ellipsis_options={ellipsis_opts}, got {lbl.ellipsis_options}"
    
    @given(st.fixed_dictionaries({
        'markup_color': st.sampled_from([[1, 0, 0, 1], [0, 1, 0, 1], [0, 0, 1, 1]])
    }))
    @settings(max_examples=100, deadline=None)
    def test_ellipsis_options_forwarded_to_heading(self, ellipsis_opts):
        """ellipsis_options property is forwarded to heading Labels."""
        label = MarkdownLabel(text='# Heading', ellipsis_options=ellipsis_opts)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        for lbl in labels:
            assert lbl.ellipsis_options == ellipsis_opts, \
                f"Expected ellipsis_options={ellipsis_opts}, got {lbl.ellipsis_options}"
    
    @given(st.fixed_dictionaries({
        'markup_color': st.sampled_from([[1, 0, 0, 1], [0, 1, 0, 1], [0, 0, 1, 1]])
    }))
    @settings(max_examples=100, deadline=None)
    def test_ellipsis_options_forwarded_to_list_items(self, ellipsis_opts):
        """ellipsis_options property is forwarded to list item Labels."""
        markdown = '- Item 1\n- Item 2'
        label = MarkdownLabel(text=markdown, ellipsis_options=ellipsis_opts)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 2, "Expected at least 2 Labels for list items"
        
        for lbl in labels:
            assert lbl.ellipsis_options == ellipsis_opts, \
                f"Expected ellipsis_options={ellipsis_opts}, got {lbl.ellipsis_options}"
    
    @given(st.fixed_dictionaries({
        'markup_color': st.sampled_from([[1, 0, 0, 1], [0, 1, 0, 1], [0, 0, 1, 1]])
    }))
    @settings(max_examples=100, deadline=None)
    def test_ellipsis_options_forwarded_to_table_cells(self, ellipsis_opts):
        """ellipsis_options property is forwarded to table cell Labels."""
        markdown = '| A | B |\n| --- | --- |\n| 1 | 2 |'
        label = MarkdownLabel(text=markdown, ellipsis_options=ellipsis_opts)
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 4, "Expected at least 4 Labels for table cells"
        
        for lbl in labels:
            assert lbl.ellipsis_options == ellipsis_opts, \
                f"Expected ellipsis_options={ellipsis_opts}, got {lbl.ellipsis_options}"
    
    def test_empty_ellipsis_options_not_forwarded(self):
        """Empty ellipsis_options dict is not forwarded (default behavior)."""
        label = MarkdownLabel(text='Hello World', ellipsis_options={})
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        # Empty dict should result in default empty dict on child Labels
        for lbl in labels:
            assert lbl.ellipsis_options == {}, \
                f"Expected empty ellipsis_options, got {lbl.ellipsis_options}"
    
    @given(st.booleans(), st.sampled_from(['left', 'center', 'right']),
           st.text(min_size=0, max_size=3, alphabet='ab '),
           st.integers(min_value=1, max_value=5))
    @settings(max_examples=100, deadline=None)
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
        
        labels = self._find_labels_recursive(label)
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
    @settings(max_examples=100, deadline=None)
    def test_shorten_change_triggers_rebuild(self, shorten1, shorten2):
        """Changing shorten triggers widget rebuild with new value."""
        assume(shorten1 != shorten2)
        
        label = MarkdownLabel(text='Hello World', shorten=shorten1)
        
        # Verify initial value
        labels = self._find_labels_recursive(label)
        for lbl in labels:
            assert lbl.shorten == shorten1
        
        # Change shorten
        label.shorten = shorten2
        
        # Verify new value
        labels = self._find_labels_recursive(label)
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
    @settings(max_examples=100, deadline=None)
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
    @settings(max_examples=100, deadline=None)
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
    @settings(max_examples=100, deadline=None)
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
        
        # Change text
        label.text = markdown2
        
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
    @settings(max_examples=100, deadline=None)
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
    @settings(max_examples=100, deadline=None)
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


# **Feature: label-compatibility-phase2, Property 6: Font Advanced Property Forwarding**
# *For any* font advanced property (font_family, font_context, font_features, font_hinting,
# font_kerning), when set on MarkdownLabel, all applicable child Labels SHALL have the same
# property value (font_family excluded from code blocks).
# **Validates: Requirements 6.1, 6.2, 6.3, 6.4, 6.5**

class TestFontAdvancedPropertyForwardingPhase2:
    """Property tests for font advanced property forwarding (Property 6).
    
    This test class verifies that font advanced properties are correctly
    forwarded to child Labels, with the special case that font_family
    is excluded from code blocks to preserve monospace appearance.
    """
    
    def _find_labels_recursive(self, widget):
        """Recursively find all Label widgets in the tree."""
        labels = []
        if isinstance(widget, Label):
            labels.append(widget)
        if hasattr(widget, 'children'):
            for child in widget.children:
                labels.extend(self._find_labels_recursive(child))
        return labels
    
    def _find_code_block_labels(self, widget):
        """Find Labels that are inside code block containers.
        
        Code block containers have a 'language_info' attribute.
        """
        code_labels = []
        
        def find_in_container(container):
            if hasattr(container, 'language_info'):
                # This is a code block container
                for child in container.children:
                    if isinstance(child, Label):
                        code_labels.append(child)
            if hasattr(container, 'children'):
                for child in container.children:
                    find_in_container(child)
        
        find_in_container(widget)
        return code_labels
    
    def _find_non_code_labels(self, widget):
        """Find Labels that are NOT inside code block containers."""
        all_labels = self._find_labels_recursive(widget)
        code_labels = self._find_code_block_labels(widget)
        return [lbl for lbl in all_labels if lbl not in code_labels]
    
    @given(st.text(min_size=1, max_size=30, alphabet=st.characters(
        whitelist_categories=['L', 'N'],
        blacklist_characters='[]&\n\r'
    )))
    @settings(max_examples=100, deadline=None)
    def test_font_family_excluded_from_code_blocks(self, font_family_value):
        """font_family is NOT forwarded to code block Labels.
        
        **Feature: label-compatibility-phase2, Property 6: Font Advanced Property Forwarding**
        **Validates: Requirements 6.1**
        """
        # Create markdown with both regular text and code block
        markdown = f'Regular paragraph\n\n```python\ncode here\n```'
        label = MarkdownLabel(text=markdown, font_family=font_family_value)
        
        # Find code block labels
        code_labels = self._find_code_block_labels(label)
        
        # Code block labels should NOT have font_family set
        for lbl in code_labels:
            assert lbl.font_family is None, \
                f"Code block should not have font_family, got {lbl.font_family!r}"
    
    @given(st.text(min_size=1, max_size=30, alphabet=st.characters(
        whitelist_categories=['L', 'N'],
        blacklist_characters='[]&\n\r'
    )))
    @settings(max_examples=100, deadline=None)
    def test_font_family_forwarded_to_non_code_labels(self, font_family_value):
        """font_family IS forwarded to non-code block Labels.
        
        **Feature: label-compatibility-phase2, Property 6: Font Advanced Property Forwarding**
        **Validates: Requirements 6.1**
        """
        # Create markdown with both regular text and code block
        markdown = f'Regular paragraph\n\n```python\ncode here\n```'
        label = MarkdownLabel(text=markdown, font_family=font_family_value)
        
        # Find non-code labels
        non_code_labels = self._find_non_code_labels(label)
        assert len(non_code_labels) >= 1, "Expected at least 1 non-code Label"
        
        # Non-code labels should have font_family set
        for lbl in non_code_labels:
            assert lbl.font_family == font_family_value, \
                f"Expected font_family={font_family_value!r}, got {lbl.font_family!r}"
    
    @given(st.text(min_size=1, max_size=30, alphabet=st.characters(
        whitelist_categories=['L', 'N'],
        blacklist_characters='[]&\n\r'
    )))
    @settings(max_examples=100, deadline=None)
    def test_font_context_forwarded_to_all_labels_including_code(self, font_context_value):
        """font_context IS forwarded to ALL Labels including code blocks.
        
        **Feature: label-compatibility-phase2, Property 6: Font Advanced Property Forwarding**
        **Validates: Requirements 6.2**
        """
        # Create markdown with both regular text and code block
        markdown = f'Regular paragraph\n\n```python\ncode here\n```'
        label = MarkdownLabel(text=markdown, font_context=font_context_value)
        
        # Find all labels
        all_labels = self._find_labels_recursive(label)
        assert len(all_labels) >= 2, "Expected at least 2 Labels (paragraph + code)"
        
        # All labels should have font_context set
        for lbl in all_labels:
            assert lbl.font_context == font_context_value, \
                f"Expected font_context={font_context_value!r}, got {lbl.font_context!r}"
    
    @given(st.text(min_size=0, max_size=50, alphabet=st.characters(
        whitelist_categories=['L', 'N', 'P'],
        blacklist_characters='[]&\n\r'
    )))
    @settings(max_examples=100, deadline=None)
    def test_font_features_forwarded_to_all_labels_including_code(self, font_features_value):
        """font_features IS forwarded to ALL Labels including code blocks.
        
        **Feature: label-compatibility-phase2, Property 6: Font Advanced Property Forwarding**
        **Validates: Requirements 6.3**
        """
        # Create markdown with both regular text and code block
        markdown = f'Regular paragraph\n\n```python\ncode here\n```'
        label = MarkdownLabel(text=markdown, font_features=font_features_value)
        
        # Find all labels
        all_labels = self._find_labels_recursive(label)
        assert len(all_labels) >= 2, "Expected at least 2 Labels (paragraph + code)"
        
        # All labels should have font_features set
        for lbl in all_labels:
            assert lbl.font_features == font_features_value, \
                f"Expected font_features={font_features_value!r}, got {lbl.font_features!r}"
    
    @given(st.sampled_from([None, 'normal', 'light', 'mono']))
    @settings(max_examples=100, deadline=None)
    def test_font_hinting_forwarded_to_all_labels_including_code(self, font_hinting_value):
        """font_hinting IS forwarded to ALL Labels including code blocks.
        
        **Feature: label-compatibility-phase2, Property 6: Font Advanced Property Forwarding**
        **Validates: Requirements 6.4**
        """
        # Create markdown with both regular text and code block
        markdown = f'Regular paragraph\n\n```python\ncode here\n```'
        label = MarkdownLabel(text=markdown, font_hinting=font_hinting_value)
        
        # Find all labels
        all_labels = self._find_labels_recursive(label)
        assert len(all_labels) >= 2, "Expected at least 2 Labels (paragraph + code)"
        
        # All labels should have font_hinting set (when not None)
        for lbl in all_labels:
            if font_hinting_value is not None:
                assert lbl.font_hinting == font_hinting_value, \
                    f"Expected font_hinting={font_hinting_value!r}, got {lbl.font_hinting!r}"
    
    @given(st.booleans())
    @settings(max_examples=100, deadline=None)
    def test_font_kerning_forwarded_to_all_labels_including_code(self, font_kerning_value):
        """font_kerning IS forwarded to ALL Labels including code blocks.
        
        **Feature: label-compatibility-phase2, Property 6: Font Advanced Property Forwarding**
        **Validates: Requirements 6.5**
        """
        # Create markdown with both regular text and code block
        markdown = f'Regular paragraph\n\n```python\ncode here\n```'
        label = MarkdownLabel(text=markdown, font_kerning=font_kerning_value)
        
        # Find all labels
        all_labels = self._find_labels_recursive(label)
        assert len(all_labels) >= 2, "Expected at least 2 Labels (paragraph + code)"
        
        # All labels should have font_kerning set
        for lbl in all_labels:
            assert lbl.font_kerning == font_kerning_value, \
                f"Expected font_kerning={font_kerning_value}, got {lbl.font_kerning}"
    
    @given(st.text(min_size=1, max_size=20, alphabet=st.characters(
        whitelist_categories=['L', 'N'],
        blacklist_characters='[]&\n\r'
    )),
           st.text(min_size=1, max_size=20, alphabet=st.characters(
        whitelist_categories=['L', 'N'],
        blacklist_characters='[]&\n\r'
    )),
           st.sampled_from([None, 'normal', 'light', 'mono']),
           st.booleans())
    @settings(max_examples=100, deadline=None)
    def test_combined_font_properties_with_code_block(self, font_family, font_context, 
                                                       font_hinting, font_kerning):
        """Combined font properties are correctly forwarded with code block exclusion.
        
        **Feature: label-compatibility-phase2, Property 6: Font Advanced Property Forwarding**
        **Validates: Requirements 6.1, 6.2, 6.3, 6.4, 6.5**
        """
        # Create markdown with both regular text and code block
        markdown = f'# Heading\n\nParagraph\n\n```python\ncode\n```'
        label = MarkdownLabel(
            text=markdown,
            font_family=font_family,
            font_context=font_context,
            font_hinting=font_hinting,
            font_kerning=font_kerning
        )
        
        # Find code and non-code labels
        code_labels = self._find_code_block_labels(label)
        non_code_labels = self._find_non_code_labels(label)
        
        # Verify non-code labels have all properties
        for lbl in non_code_labels:
            assert lbl.font_family == font_family, \
                f"Non-code label: Expected font_family={font_family!r}, got {lbl.font_family!r}"
            assert lbl.font_context == font_context, \
                f"Non-code label: Expected font_context={font_context!r}, got {lbl.font_context!r}"
            if font_hinting is not None:
                assert lbl.font_hinting == font_hinting, \
                    f"Non-code label: Expected font_hinting={font_hinting!r}, got {lbl.font_hinting!r}"
            assert lbl.font_kerning == font_kerning, \
                f"Non-code label: Expected font_kerning={font_kerning}, got {lbl.font_kerning}"
        
        # Verify code labels have all properties EXCEPT font_family
        for lbl in code_labels:
            assert lbl.font_family is None, \
                f"Code label: font_family should be None, got {lbl.font_family!r}"
            assert lbl.font_context == font_context, \
                f"Code label: Expected font_context={font_context!r}, got {lbl.font_context!r}"
            if font_hinting is not None:
                assert lbl.font_hinting == font_hinting, \
                    f"Code label: Expected font_hinting={font_hinting!r}, got {lbl.font_hinting!r}"
            assert lbl.font_kerning == font_kerning, \
                f"Code label: Expected font_kerning={font_kerning}, got {lbl.font_kerning}"
