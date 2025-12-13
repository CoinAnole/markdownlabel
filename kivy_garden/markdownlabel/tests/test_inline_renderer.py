"""
Property-based tests for InlineRenderer.

Tests verify that inline Markdown formatting is correctly converted
to Kivy markup strings.
"""

import pytest
from hypothesis import given, strategies as st, settings

from kivy_garden.markdownlabel.inline_renderer import InlineRenderer


# Custom strategies for generating valid inline tokens
@st.composite
def text_token(draw):
    """Generate a text token with arbitrary text content."""
    raw = draw(st.text(min_size=0, max_size=100))
    return {'type': 'text', 'raw': raw}


@st.composite
def strong_token(draw):
    """Generate a strong (bold) token with text children."""
    raw = draw(st.text(min_size=1, max_size=50))
    return {
        'type': 'strong',
        'children': [{'type': 'text', 'raw': raw}]
    }


@st.composite
def emphasis_token(draw):
    """Generate an emphasis (italic) token with text children."""
    raw = draw(st.text(min_size=1, max_size=50))
    return {
        'type': 'emphasis',
        'children': [{'type': 'text', 'raw': raw}]
    }


@st.composite
def codespan_token(draw):
    """Generate a codespan token with code content."""
    raw = draw(st.text(min_size=1, max_size=50))
    return {'type': 'codespan', 'raw': raw}


@st.composite
def strikethrough_token(draw):
    """Generate a strikethrough token with text children."""
    raw = draw(st.text(min_size=1, max_size=50))
    return {
        'type': 'strikethrough',
        'children': [{'type': 'text', 'raw': raw}]
    }


@st.composite
def link_token(draw):
    """Generate a link token with URL and text children."""
    text = draw(st.text(min_size=1, max_size=50))
    # Generate a simple URL-like string
    url = draw(st.text(
        alphabet=st.sampled_from('abcdefghijklmnopqrstuvwxyz0123456789-._~:/?#@!$&()*+,;='),
        min_size=1,
        max_size=100
    ))
    return {
        'type': 'link',
        'children': [{'type': 'text', 'raw': text}],
        'attrs': {'url': url}
    }


# **Feature: markdown-label, Property 4: Inline Formatting Conversion**
# *For any* Markdown text containing inline formatting (bold, italic, code, strikethrough),
# the rendered Kivy markup SHALL contain the corresponding tags:
# **text** → [b]text[/b], *text* → [i]text[/i], `code` → [font=monospace]code[/font], ~~text~~ → [s]text[/s]
# **Validates: Requirements 3.2, 3.3, 3.4, 3.5**

class TestInlineFormattingConversion:
    """Property tests for inline formatting conversion (Property 4)."""
    
    @given(strong_token())
    @settings(max_examples=100)
    def test_strong_produces_bold_tags(self, token):
        """Strong tokens produce [b]...[/b] markup."""
        renderer = InlineRenderer()
        result = renderer.strong(token)
        
        assert result.startswith('[b]'), f"Strong should start with [b], got: {result}"
        assert result.endswith('[/b]'), f"Strong should end with [/b], got: {result}"
    
    @given(emphasis_token())
    @settings(max_examples=100)
    def test_emphasis_produces_italic_tags(self, token):
        """Emphasis tokens produce [i]...[/i] markup."""
        renderer = InlineRenderer()
        result = renderer.emphasis(token)
        
        assert result.startswith('[i]'), f"Emphasis should start with [i], got: {result}"
        assert result.endswith('[/i]'), f"Emphasis should end with [/i], got: {result}"
    
    @given(codespan_token())
    @settings(max_examples=100)
    def test_codespan_produces_font_tags(self, token):
        """Codespan tokens produce [font=...]...[/font] markup."""
        renderer = InlineRenderer()
        result = renderer.codespan(token)
        
        assert result.startswith('[font='), f"Codespan should start with [font=, got: {result}"
        assert result.endswith('[/font]'), f"Codespan should end with [/font], got: {result}"
    
    @given(strikethrough_token())
    @settings(max_examples=100)
    def test_strikethrough_produces_s_tags(self, token):
        """Strikethrough tokens produce [s]...[/s] markup."""
        renderer = InlineRenderer()
        result = renderer.strikethrough(token)
        
        assert result.startswith('[s]'), f"Strikethrough should start with [s], got: {result}"
        assert result.endswith('[/s]'), f"Strikethrough should end with [/s], got: {result}"
    
    @given(link_token())
    @settings(max_examples=100)
    def test_link_produces_ref_tags_unstyled(self, token):
        """Unstyled links produce [ref=url]...[/ref] without forced styling."""
        renderer = InlineRenderer(link_style='unstyled')
        result = renderer.link(token)
        url = token['attrs']['url']
        
        # Links should contain the ref tag with the URL
        assert f'[ref={url}]' in result, f"Link should contain [ref={url}], got: {result}"
        assert '[/ref]' in result, f"Link should contain [/ref], got: {result}"
        
        # Unstyled links should not inject color/underline markup
        assert '[color=' not in result, f"Unstyled link should not add color, got: {result}"
        assert '[u]' not in result and '[/u]' not in result, \
            f"Unstyled link should not add underline, got: {result}"
    
    @given(link_token())
    @settings(max_examples=100)
    def test_link_produces_ref_tags_styled(self, token):
        """Styled links wrap refs with color and underline."""
        renderer = InlineRenderer(link_style='styled')
        result = renderer.link(token)
        url = token['attrs']['url']
        
        # Links should contain the ref tag with the URL
        assert f'[ref={url}]' in result, f"Link should contain [ref={url}], got: {result}"
        assert '[/ref]' in result, f"Link should contain [/ref], got: {result}"
        
        # Styled links apply color and underline styling
        assert '[color=' in result, f"Link should have color styling, got: {result}"
        assert '[u]' in result, f"Link should have underline styling, got: {result}"
        assert '[/u]' in result, f"Link should close underline styling, got: {result}"
        assert '[/color]' in result, f"Link should close color styling, got: {result}"


# **Feature: markdown-label, Property 19: Special Character Escaping**
# *For any* Markdown text containing Kivy markup special characters ([, ], &),
# the rendered Label text SHALL properly escape them (&bl;, &br;, &amp;) to prevent markup injection.
# **Validates: Requirements 13.3**

class TestSpecialCharacterEscaping:
    """Property tests for special character escaping (Property 19)."""
    
    @given(text_token())
    @settings(max_examples=100)
    def test_text_escapes_special_characters(self, token):
        """Text tokens escape [, ], and & characters."""
        renderer = InlineRenderer()
        result = renderer.text(token)
        raw = token['raw']
        
        # After escaping, there should be no unescaped [ or ] or &
        # Check that [ becomes &bl;, ] becomes &br;, & becomes &amp;
        
        # Count special chars in input
        input_brackets_open = raw.count('[')
        input_brackets_close = raw.count(']')
        input_ampersands = raw.count('&')
        
        # Count escape sequences in output
        output_bl = result.count('&bl;')
        output_br = result.count('&br;')
        output_amp = result.count('&amp;')
        
        # Each [ should become &bl;
        assert output_bl == input_brackets_open, \
            f"Expected {input_brackets_open} &bl; escapes, got {output_bl}"
        
        # Each ] should become &br;
        assert output_br == input_brackets_close, \
            f"Expected {input_brackets_close} &br; escapes, got {output_br}"
        
        # Each & should become &amp;
        assert output_amp == input_ampersands, \
            f"Expected {input_ampersands} &amp; escapes, got {output_amp}"
    
    @given(st.text(alphabet='[]&', min_size=1, max_size=50))
    @settings(max_examples=100)
    def test_only_special_chars_fully_escaped(self, raw):
        """Text containing only special characters is fully escaped."""
        renderer = InlineRenderer()
        token = {'type': 'text', 'raw': raw}
        result = renderer.text(token)
        
        # Result should not contain any literal [ or ] characters
        # (they should all be escaped as &bl; or &br;)
        # Note: We need to check for unescaped brackets, not the escaped sequences
        
        # Remove all escape sequences to check for remaining special chars
        cleaned = result.replace('&bl;', '').replace('&br;', '').replace('&amp;', '')
        
        assert '[' not in cleaned, f"Found unescaped [ in: {result}"
        assert ']' not in cleaned, f"Found unescaped ] in: {result}"
        # & is tricky because &amp; contains &, so we check differently
        # After removing escape sequences, there should be no & left
        assert '&' not in cleaned, f"Found unescaped & in: {result}"
    
    @given(st.text(min_size=0, max_size=100))
    @settings(max_examples=100)
    def test_escape_is_reversible(self, raw):
        """Escaping can be reversed to get original text."""
        renderer = InlineRenderer()
        token = {'type': 'text', 'raw': raw}
        result = renderer.text(token)
        
        # Reverse the escaping (in correct order)
        unescaped = result.replace('&bl;', '[').replace('&br;', ']').replace('&amp;', '&')
        
        assert unescaped == raw, f"Round-trip failed: {raw!r} -> {result!r} -> {unescaped!r}"
