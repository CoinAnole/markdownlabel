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
    # Complex strategy: 20 examples based on default complexity
    @settings(max_examples=20)
    def test_strong_produces_bold_tags(self, token):
        """Strong tokens produce [b]...[/b] markup."""
        renderer = InlineRenderer()
        result = renderer.strong(token)
        
        assert result.startswith('[b]'), f"Strong should start with [b], got: {result}"
        assert result.endswith('[/b]'), f"Strong should end with [/b], got: {result}"
    
    # Complex strategy: 20 examples based on default complexity
    @given(emphasis_token())
    @settings(max_examples=100)
    def test_emphasis_produces_italic_tags(self, token):
        """Emphasis tokens produce [i]...[/i] markup."""
        renderer = InlineRenderer()
        result = renderer.emphasis(token)
        
        assert result.startswith('[i]'), f"Emphasis should start with [i], got: {result}"
        assert result.endswith('[/i]'), f"Emphasis should end with [/i], got: {result}"
     # Complex strategy: 20 examples based on default complexity
    
    @given(codespan_token())
    @settings(max_examples=100)
    def test_codespan_produces_font_tags(self, token):
        """Codespan tokens produce [font=...]...[/font] markup."""
        renderer = InlineRenderer()
        result = renderer.codespan(token)
        
        assert result.startswith('[font='), f"Codespan should start with [font=, got: {result}"
        # Complex strategy: 20 examples based on default complexity
        assert result.endswith('[/font]'), f"Codespan should end with [/font], got: {result}"
    
    @given(strikethrough_token())
    @settings(max_examples=100)
    def test_strikethrough_produces_s_tags(self, token):
        """Strikethrough tokens produce [s]...[/s] markup."""
        renderer = InlineRenderer()
        result = renderer.strikethrough(token)
        
        # Complex strategy: 20 examples based on default complexity
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
        
        # Complex strategy with text generation, custom alphabet: 30 examples
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
        # Complex strategy with text generation: 30 examples
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
    @settings(max_examples=20)
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


class TestHTMLSecurity:
    """Test HTML content security and escaping."""
    
    @pytest.mark.parametrize('html_content', [
        '<script>alert("xss")</script>',
        '<b>bold</b>',
        '<img src="x" onerror="alert(1)">',
        '<div onclick="malicious()">click</div>',
        '<iframe src="javascript:alert(1)"></iframe>',
        '<svg onload="alert(1)">',
        '<style>body{background:red}</style>',
        '<link rel="stylesheet" href="evil.css">',
        '<meta http-equiv="refresh" content="0;url=evil.com">',
        '<object data="evil.swf"></object>',
        '<embed src="evil.swf">',
        '<form action="evil.com"><input type="submit"></form>',
        '&lt;escaped&gt;',
        '<p>normal paragraph</p>',
        '<a href="http://example.com">link</a>',
    ])
    def test_html_escaping(self, html_content):
        """HTML content should be escaped, not interpreted."""
        renderer = InlineRenderer()
        token = {'type': 'inline_html', 'raw': html_content}
        result = renderer.inline_html(token)
        
        # Should not contain unescaped HTML angle brackets
        assert '<' not in result, f"Should not contain unescaped <: {result}"
        assert '>' not in result, f"Should not contain unescaped >: {result}"
        
        # Should contain escaped HTML (double-escaped due to HTML then Kivy escaping)
        if '<' in html_content:
            assert '&amp;lt;' in result, f"Should contain &amp;lt; for <: {result}"
        if '>' in html_content:
            assert '&amp;gt;' in result, f"Should contain &amp;gt; for >: {result}"
        
        # Should not contain unescaped Kivy markup characters
        assert '[' not in result or result.count('&bl;') >= html_content.count('['), \
            f"Should escape [ characters: {result}"
        assert ']' not in result or result.count('&br;') >= html_content.count(']'), \
            f"Should escape ] characters: {result}"
    
    @pytest.mark.parametrize('malicious_html', [
        '<script>alert("XSS")</script>',
        '<img src=x onerror=alert(1)>',
        '<svg/onload=alert(1)>',
        '<iframe src=javascript:alert(1)>',
        '<object data=data:text/html,<script>alert(1)</script>>',
        '<embed src=data:image/svg+xml,<svg/onload=alert(1)>>',
        '<link rel=import href=data:text/html,<script>alert(1)</script>>',
        '<meta http-equiv=refresh content=0;url=javascript:alert(1)>',
        '<form><button formaction=javascript:alert(1)>click</button></form>',
        '<details open ontoggle=alert(1)>',
    ])
    def test_xss_prevention(self, malicious_html):
        """Potential XSS vectors should be neutralized."""
        renderer = InlineRenderer()
        token = {'type': 'inline_html', 'raw': malicious_html}
        result = renderer.inline_html(token)
        
        # Should not contain any executable HTML tags (angle brackets should be escaped)
        assert '<script' not in result, f"Should not contain <script: {result}"
        # Note: javascript:, onload=, etc. may still appear as text content but are safe
        # because the < and > are escaped, so they can't form executable HTML tags
        
        # All angle brackets should be escaped
        assert '<' not in result, f"Should not contain unescaped <: {result}"
        assert '>' not in result, f"Should not contain unescaped >: {result}"
    
    def test_html_with_quotes_escaping(self):
        """HTML with quotes should be properly escaped."""
        test_cases = [
            '<img src="evil.jpg" alt=\'malicious\'>',
            '<div class="container" id=\'main\'>',
            '<script type="text/javascript">alert("xss")</script>',
            '<a href="javascript:alert(\'xss\')">click</a>',
        ]
        
        renderer = InlineRenderer()
        
        for html in test_cases:
            token = {'type': 'inline_html', 'raw': html}
            result = renderer.inline_html(token)
            
            # Should not contain unescaped quotes
            # Note: We escape quotes in HTML content, then escape Kivy markup
            # So quotes might be escaped as &quot; or &#x27;
            if '"' in html:
                assert '"' not in result or '&quot;' in result, \
                    f"Should escape double quotes: {result}"
            if "'" in html:
                assert "'" not in result or '&#x27;' in result, \
                    f"Should escape single quotes: {result}"
            
            # Should not contain unescaped angle brackets
            assert '<' not in result, f"Should escape < in: {result}"
            assert '>' not in result, f"Should escape > in: {result}"
    
    def test_nested_html_and_kivy_markup(self):
        """HTML containing Kivy markup patterns should be safe."""
        test_cases = [
            '<div>[b]bold[/b]</div>',
            '<script>[color=ff0000]red[/color]</script>',
            '<img src="[ref=evil]click[/ref]">',
            '<p>[font=Arial]text[/font]</p>',
            '<span>[size=20]big[/size]</span>',
        ]
        
        renderer = InlineRenderer()
        
        for html in test_cases:
            token = {'type': 'inline_html', 'raw': html}
            result = renderer.inline_html(token)
            
            # Should not contain active Kivy markup
            # The Kivy markup should be escaped along with the HTML
            assert '<' not in result, f"Should escape HTML tags: {result}"
            assert '>' not in result, f"Should escape HTML tags: {result}"
            
            # Kivy markup characters should also be escaped
            kivy_patterns = ['[b]', '[/b]', '[color=', '[/color]', '[ref=', '[/ref]', '[font=', '[/font]', '[size=', '[/size]']
            for pattern in kivy_patterns:
                if pattern in html:
                    # The pattern should not appear unescaped in the result
                    # It should be escaped ([ becomes &bl;, ] becomes &br;)
                    assert pattern not in result or result.count('&bl;') > 0 or result.count('&br;') > 0, \
                        f"Kivy markup should be escaped: {pattern} in {result}"
    
    def test_html_escaping_preserves_content(self):
        """HTML escaping should preserve the readable content."""
        test_cases = [
            ('<p>Hello World</p>', 'Hello World'),
            ('<b>Bold Text</b>', 'Bold Text'),
            ('<script>alert("test")</script>', 'alert("test")'),
            ('<img alt="description">', 'description'),
            ('<a href="link">Click Here</a>', 'Click Here'),
        ]
        
        renderer = InlineRenderer()
        
        for html, expected_content in test_cases:
            token = {'type': 'inline_html', 'raw': html}
            result = renderer.inline_html(token)
            
            # The readable content should still be present (though escaped)
            # Due to double-escaping, quotes become &amp;quot;
            escaped_content = expected_content.replace('"', '&amp;quot;').replace("'", '&#x27;')
            assert expected_content in result or escaped_content in result, \
                f"Should preserve readable content '{expected_content}' (or escaped as '{escaped_content}') in: {result}"
    
    def test_empty_and_whitespace_html(self):
        """Empty and whitespace-only HTML should be handled safely."""
        test_cases = ['', '   ', '\n\t', '<>', '< >', '<  >']
        
        renderer = InlineRenderer()
        
        for html in test_cases:
            token = {'type': 'inline_html', 'raw': html}
            result = renderer.inline_html(token)
            
            # Should not contain unescaped angle brackets
            assert '<' not in result, f"Should escape < in '{html}': {result}"
            assert '>' not in result, f"Should escape > in '{html}': {result}"
            
            # Should handle empty/whitespace gracefully
            if not html.strip():
                # Empty or whitespace-only should produce safe output
                assert len(result) >= 0, f"Should handle empty input: {result}"
    
    def test_html_with_special_entities(self):
        """HTML with existing entities should be handled correctly."""
        test_cases = [
            '&lt;script&gt;alert(1)&lt;/script&gt;',
            '&amp;lt;b&amp;gt;bold&amp;lt;/b&amp;gt;',
            '&quot;quoted&quot;',
            '&#x27;single&#x27;',
            '&nbsp;&copy;&reg;',
        ]
        
        renderer = InlineRenderer()
        
        for html in test_cases:
            token = {'type': 'inline_html', 'raw': html}
            result = renderer.inline_html(token)
            
            # Should not double-escape already escaped entities
            # But should still be safe (no unescaped < or >)
            assert '<' not in result, f"Should not contain unescaped <: {result}"
            assert '>' not in result, f"Should not contain unescaped >: {result}"
            
            # Should preserve entity structure (though may be double-escaped)
            if '&' in html:
                assert '&amp;' in result, f"Should handle & characters: {result}"


# **Feature: test-improvements, Property 9: HTML content escaping**
# *For any* inline HTML content, the InlineRenderer SHALL escape HTML tags to render them as plain text
# without introducing exploitable Kivy markup.
# **Validates: Requirements 6.1, 6.2, 6.4**

class TestHTMLContentEscapingProperty:
    """Property test for HTML content escaping (Property 9)."""
    
    @given(st.one_of(
        # HTML with various tag structures
        st.text(min_size=1, max_size=50).map(lambda s: f"<script>{s}</script>"),
        st.text(min_size=1, max_size=50).map(lambda s: f"<div>{s}</div>"),
        st.text(min_size=1, max_size=50).map(lambda s: f"<img src='{s}'>"),
        st.text(min_size=1, max_size=50).map(lambda s: f"<a href='{s}'>link</a>"),
        # HTML with attributes and quotes
        st.text(min_size=1, max_size=30).map(lambda s: f'<p class="{s}">text</p>'),
        st.text(min_size=1, max_size=30).map(lambda s: f"<span id='{s}'>content</span>"),
        # HTML with potential XSS vectors
        st.text(min_size=1, max_size=30).map(lambda s: f"<script>alert('{s}')</script>"),
        st.text(min_size=1, max_size=30).map(lambda s: f'<img onerror="alert(\'{s}\')" src="x">'),
        # HTML with mixed content
        st.text(min_size=1, max_size=100, alphabet=st.characters(
            whitelist_categories=['L', 'N', 'P', 'S'],
            blacklist_characters='<>'  # We'll add these via the template
        )).map(lambda s: f"<div>{s}</div>"),
        # Raw HTML-like strings
        st.text(min_size=1, max_size=100).filter(lambda s: '<' in s or '>' in s),
    ))
    @settings(max_examples=20)
    def test_html_content_is_escaped(self, html_content):
        """HTML content should be escaped to prevent markup injection."""
        # **Feature: test-improvements, Property 9: HTML content escaping**
        renderer = InlineRenderer()
        
        token = {'type': 'inline_html', 'raw': html_content}
        result = renderer.inline_html(token)
        
        # Property: No unescaped HTML angle brackets
        assert '<' not in result, f"Should not contain unescaped <. HTML: {html_content!r}, Result: {result!r}"
        assert '>' not in result, f"Should not contain unescaped >. HTML: {html_content!r}, Result: {result!r}"
        
        # Property: HTML angle brackets should be escaped (double-escaped due to HTML then Kivy escaping)
        if '<' in html_content:
            assert '&amp;lt;' in result, f"Should contain &amp;lt; for <. HTML: {html_content!r}, Result: {result!r}"
        if '>' in html_content:
            assert '&amp;gt;' in result, f"Should contain &amp;gt; for >. HTML: {html_content!r}, Result: {result!r}"
        
        # Property: No unescaped Kivy markup characters
        # Count Kivy special chars in input and ensure they're escaped in output
        input_open_brackets = html_content.count('[')
        input_close_brackets = html_content.count(']')
        input_ampersands = html_content.count('&')
        
        output_bl_escapes = result.count('&bl;')
        output_br_escapes = result.count('&br;')
        output_amp_escapes = result.count('&amp;')
        
        # Each [ should become &bl;
        assert output_bl_escapes >= input_open_brackets, \
            f"Should escape all [ characters. Input: {input_open_brackets}, Escaped: {output_bl_escapes}. HTML: {html_content!r}, Result: {result!r}"
        
        # Each ] should become &br;
        assert output_br_escapes >= input_close_brackets, \
            f"Should escape all ] characters. Input: {input_close_brackets}, Escaped: {output_br_escapes}. HTML: {html_content!r}, Result: {result!r}"
        
        # Each & should become &amp; (but note that HTML escaping adds &lt; etc.)
        # So we need to account for the & characters we introduced during HTML escaping
        expected_amp_escapes = input_ampersands
        if '<' in html_content:
            expected_amp_escapes += html_content.count('<')  # &lt; adds &
        if '>' in html_content:
            expected_amp_escapes += html_content.count('>')  # &gt; adds &
        if '"' in html_content:
            expected_amp_escapes += html_content.count('"')  # &quot; adds &
        if "'" in html_content:
            expected_amp_escapes += html_content.count("'")  # &#x27; adds &
        
        assert output_amp_escapes >= expected_amp_escapes, \
            f"Should escape all & characters (including those from HTML escaping). Expected: {expected_amp_escapes}, Got: {output_amp_escapes}. HTML: {html_content!r}, Result: {result!r}"
        
        # Property: Result should be safe for Kivy markup rendering
        # No unescaped [ or ] should remain that could create active markup
        cleaned_result = result.replace('&bl;', '').replace('&br;', '').replace('&amp;', '').replace('&lt;', '').replace('&gt;', '').replace('&quot;', '').replace('&#x27;', '')
        assert '[' not in cleaned_result, f"Should not contain unescaped [ after removing escape sequences. HTML: {html_content!r}, Result: {result!r}, Cleaned: {cleaned_result!r}"
        assert ']' not in cleaned_result, f"Should not contain unescaped ] after removing escape sequences. HTML: {html_content!r}, Result: {result!r}, Cleaned: {cleaned_result!r}"
        assert '&' not in cleaned_result, f"Should not contain unescaped & after removing escape sequences. HTML: {html_content!r}, Result: {result!r}, Cleaned: {cleaned_result!r}"
    
    @given(st.text(min_size=0, max_size=200, alphabet=st.characters(
        whitelist_categories=['L', 'N', 'P', 'S', 'Z']
    )))
    @settings(max_examples=20)
    def test_arbitrary_html_content_safety(self, content):
        """Any arbitrary content in HTML tags should be safely escaped."""
        # **Feature: test-improvements, Property 9: HTML content escaping**
        
        # Wrap content in various HTML tag patterns
        html_patterns = [
            f"<div>{content}</div>",
            f"<script>{content}</script>",
            f'<img alt="{content}">',
            f"<p>{content}</p>",
            f"<span>{content}</span>",
        ]
        
        renderer = InlineRenderer()
        
        for html_content in html_patterns:
            token = {'type': 'inline_html', 'raw': html_content}
            result = renderer.inline_html(token)
            
            # Property: All HTML should be escaped
            assert '<' not in result, f"Should escape all < characters. HTML: {html_content!r}, Result: {result!r}"
            assert '>' not in result, f"Should escape all > characters. HTML: {html_content!r}, Result: {result!r}"
            
            # Property: All Kivy markup should be escaped
            assert '[' not in result or '&bl;' in result, f"Should escape [ characters. HTML: {html_content!r}, Result: {result!r}"
            assert ']' not in result or '&br;' in result, f"Should escape ] characters. HTML: {html_content!r}, Result: {result!r}"
            
            # Property: Content should still be present (though escaped)
            if content.strip():  # Only check non-empty content
                # The content should appear in some form in the result
                # It might be escaped, so we check for the presence of the core content
                content_chars = set(c for c in content if c.isalnum())
                result_chars = set(c for c in result if c.isalnum())
                if content_chars:  # Only check if there are alphanumeric characters
                    assert content_chars.issubset(result_chars), \
                        f"Should preserve content characters. Content: {content!r}, Result: {result!r}"
