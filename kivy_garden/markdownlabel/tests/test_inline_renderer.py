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


class TestURLMarkupSafety:
    """Test URL handling for markup injection prevention."""
    
    @pytest.mark.parametrize('unsafe_url', [
        'http://example.com]malicious[/ref][b]bold',
        'https://test.com[color=ff0000]red[/color]',
        'ftp://site.com]]][[[ref=evil]click[/ref]',
        'http://example.com]close[ref=nested]nested[/ref]',
        'https://site.com][/ref][ref=hijack]hijack[/ref]',
        'http://test.com][b]bold][/b][/ref]',
    ])
    def test_url_markup_escaping(self, unsafe_url):
        """URLs with markup characters should be escaped."""
        renderer = InlineRenderer()
        token = {
            'type': 'link',
            'children': [{'type': 'text', 'raw': 'link text'}],
            'attrs': {'url': unsafe_url}
        }
        result = renderer.link(token)
        
        # Should not contain unescaped closing brackets that could break markup
        # Count [ref= tags - should be exactly 1 opening and 1 closing
        ref_opens = result.count('[ref=')
        ref_closes = result.count('[/ref]')
        
        assert ref_opens == 1, f"Should have exactly 1 [ref= tag, got {ref_opens} in: {result}"
        assert ref_closes == 1, f"Should have exactly 1 [/ref] tag, got {ref_closes} in: {result}"
        
        # Should still be a valid link structure
        assert '[ref=' in result, f"Should contain [ref= tag: {result}"
        assert '[/ref]' in result, f"Should contain [/ref] tag: {result}"
        assert 'link text' in result, f"Should contain link text: {result}"
    
    @pytest.mark.parametrize('unsafe_url', [
        'http://example.com]',
        'https://test.com[',
        'ftp://site.com][',
        'http://example.com]]]',
        'https://site.com[[[',
    ])
    def test_bracket_escaping_in_urls(self, unsafe_url):
        """URLs with brackets should be URL-encoded."""
        renderer = InlineRenderer()
        token = {
            'type': 'link',
            'children': [{'type': 'text', 'raw': 'test'}],
            'attrs': {'url': unsafe_url}
        }
        result = renderer.link(token)
        
        # Extract the URL from the [ref=URL] markup
        ref_start = result.find('[ref=') + 5
        ref_end = result.find(']', ref_start)
        escaped_url = result[ref_start:ref_end]
        
        # Should not contain literal brackets
        assert '[' not in escaped_url, f"URL should not contain literal [: {escaped_url}"
        assert ']' not in escaped_url, f"URL should not contain literal ]: {escaped_url}"
        
        # Should contain URL-encoded brackets if original had them
        if '[' in unsafe_url:
            assert '%5B' in escaped_url, f"Should contain %5B for [: {escaped_url}"
        if ']' in unsafe_url:
            assert '%5D' in escaped_url, f"Should contain %5D for ]: {escaped_url}"
    
    def test_url_escaping_preserves_functionality(self):
        """Escaped URLs should still function as clickable links."""
        renderer = InlineRenderer()
        
        # Test a URL that needs escaping
        unsafe_url = 'http://example.com/path]with]brackets'
        token = {
            'type': 'link',
            'children': [{'type': 'text', 'raw': 'click me'}],
            'attrs': {'url': unsafe_url}
        }
        result = renderer.link(token)
        
        # Should produce valid markup structure
        assert result.startswith('[ref='), f"Should start with [ref=: {result}"
        assert result.endswith('[/ref]'), f"Should end with [/ref]: {result}"
        assert 'click me' in result, f"Should contain link text: {result}"
        
        # URL should be escaped but still recognizable
        assert 'http://example.com/path' in result, f"Should contain base URL: {result}"
        assert '%5D' in result, f"Should contain escaped brackets: {result}"
    
    def test_nested_markup_prevention(self):
        """URLs with nested markup should not break the link structure."""
        renderer = InlineRenderer()
        
        # URL that tries to inject nested markup
        malicious_url = 'http://evil.com][/ref][b]injected[/b][ref=http://real.com'
        token = {
            'type': 'link',
            'children': [{'type': 'text', 'raw': 'safe text'}],
            'attrs': {'url': malicious_url}
        }
        result = renderer.link(token)
        
        # Should have exactly one ref tag pair
        assert result.count('[ref=') == 1, f"Should have exactly 1 [ref= tag: {result}"
        assert result.count('[/ref]') == 1, f"Should have exactly 1 [/ref] tag: {result}"
        
        # Should not contain injected bold markup
        # The [b] and [/b] should be part of the escaped URL, not active markup
        bold_count = result.count('[b]')
        if bold_count > 0:
            # If [b] appears, it should be in the URL part, not as active markup
            ref_start = result.find('[ref=')
            ref_end = result.find(']', ref_start + 5)
            url_part = result[ref_start:ref_end + 1]
            text_part = result[ref_end + 1:]
            
            # [b] should not appear in the text part as active markup
            assert '[b]' not in text_part or text_part.count('[b]') == text_part.count('[/b]'), \
                f"Unmatched bold tags in text part: {text_part}"
    
    def test_multiple_brackets_handling(self):
        """URLs with multiple brackets should be handled safely."""
        renderer = InlineRenderer()
        
        test_cases = [
            'http://example.com]]]',
            'http://example.com[[[',
            'http://example.com][][][]',
            'http://example.com[test][more]',
        ]
        
        for url in test_cases:
            token = {
                'type': 'link',
                'children': [{'type': 'text', 'raw': 'test'}],
                'attrs': {'url': url}
            }
            result = renderer.link(token)
            
            # Should maintain proper markup structure
            assert result.count('[ref=') == 1, f"URL {url} should have 1 [ref= tag: {result}"
            assert result.count('[/ref]') == 1, f"URL {url} should have 1 [/ref] tag: {result}"
            
            # Extract escaped URL
            ref_start = result.find('[ref=') + 5
            ref_end = result.find(']', ref_start)
            escaped_url = result[ref_start:ref_end]
            
            # Should not contain literal brackets
            assert '[' not in escaped_url, f"Escaped URL should not contain [: {escaped_url}"
            assert ']' not in escaped_url, f"Escaped URL should not contain ]: {escaped_url}"


# **Feature: test-improvements, Property 6: URL markup safety**
# *For any* URL containing Kivy markup characters (], [, or markup patterns),
# the InlineRenderer SHALL escape or quote the URL to prevent markup injection
# while preserving link functionality.
# **Validates: Requirements 4.1, 4.2, 4.4**

class TestURLMarkupSafetyProperty:
    """Property test for URL markup safety (Property 6)."""
    
    @given(st.one_of(
        # URLs with closing brackets
        st.text(min_size=1, max_size=100).map(lambda s: f"http://example.com/{s}]"),
        # URLs with opening brackets  
        st.text(min_size=1, max_size=100).map(lambda s: f"http://example.com/[{s}"),
        # URLs with both brackets
        st.text(min_size=1, max_size=100).map(lambda s: f"http://example.com/[{s}]"),
        # URLs with multiple brackets
        st.text(min_size=1, max_size=50).map(lambda s: f"http://example.com/{s}]]]"),
        st.text(min_size=1, max_size=50).map(lambda s: f"http://example.com/[[[{s}"),
    ))
    @settings(max_examples=100)
    def test_urls_with_brackets_are_safe(self, full_url):
        """URLs containing brackets should be safely escaped."""
        # **Feature: test-improvements, Property 6: URL markup safety**
        renderer = InlineRenderer()
        
        token = {
            'type': 'link',
            'children': [{'type': 'text', 'raw': 'test link'}],
            'attrs': {'url': full_url}
        }
        
        result = renderer.link(token)
        
        # Property: Should have exactly one ref tag pair (no markup injection)
        ref_opens = result.count('[ref=')
        ref_closes = result.count('[/ref]')
        
        assert ref_opens == 1, f"Should have exactly 1 [ref= tag, got {ref_opens}. URL: {full_url!r}, Result: {result!r}"
        assert ref_closes == 1, f"Should have exactly 1 [/ref] tag, got {ref_closes}. URL: {full_url!r}, Result: {result!r}"
        
        # Property: Should still be a functional link
        assert '[ref=' in result, f"Should contain [ref= tag. URL: {full_url!r}, Result: {result!r}"
        assert '[/ref]' in result, f"Should contain [/ref] tag. URL: {full_url!r}, Result: {result!r}"
        assert 'test link' in result, f"Should preserve link text. URL: {full_url!r}, Result: {result!r}"
        
        # Property: Escaped URL should not contain literal brackets
        ref_start = result.find('[ref=') + 5
        ref_end = result.find(']', ref_start)
        escaped_url = result[ref_start:ref_end]
        
        assert '[' not in escaped_url, f"Escaped URL should not contain literal [. URL: {full_url!r}, Escaped: {escaped_url!r}"
        assert ']' not in escaped_url, f"Escaped URL should not contain literal ]. URL: {full_url!r}, Escaped: {escaped_url!r}"
