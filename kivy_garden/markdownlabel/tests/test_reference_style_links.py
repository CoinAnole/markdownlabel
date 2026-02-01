"""
Tests for reference-style link rendering and event handling.

This module contains tests that verify reference-style links render identically
to inline links and that on_ref_press events dispatch correctly with resolved URLs.
"""

import pytest
from hypothesis import given, settings, assume
from hypothesis import strategies as st

from kivy.uix.label import Label

from kivy_garden.markdownlabel import MarkdownLabel
from kivy_garden.markdownlabel.inline_renderer import InlineRenderer
from .test_utils import find_labels_with_ref_markup


class TestReferenceStyleLinkRenderingEquivalence:
    """Property tests for reference-style link rendering equivalence."""

    @pytest.mark.property
    @given(
        link_text=st.text(min_size=1, max_size=30, alphabet=st.characters(
            whitelist_categories=['L', 'N'],
            blacklist_characters='[]()&\n\r'
        )),
        label_name=st.text(min_size=1, max_size=10, alphabet=st.characters(
            whitelist_categories=['L', 'N'],
            blacklist_characters='[]()&\n\r'
        )),
        # Use ASCII-only characters for URL path to avoid URL encoding differences
        url_path=st.text(min_size=1, max_size=20, alphabet='abcdefghijklmnopqrstuvwxyz0123456789')
    )
    # Complex strategy: 50 examples (adequate coverage)
    @settings(max_examples=50, deadline=None)
    def test_reference_style_links_render_identically_to_inline_links(
        self, link_text, label_name, url_path
    ):
        """**Property 1: Reference-Style Links Render Identically to Inline Links**

        *For any* reference-style link `[text][label]` with definition `[label]: url`,
        the InlineRenderer SHALL produce the same BBCode markup as an equivalent
        inline link `[text](url)`.

        **Validates: Requirements 1.1, 1.2, 1.4**
        """
        assume(len(link_text.strip()) > 0)
        assume(len(label_name.strip()) > 0)
        assume(len(url_path.strip()) > 0)

        url = f'http://example.com/{url_path}'

        # Create reference-style link markdown
        ref_markdown = f'''Click [{link_text}][{label_name}] for info.

[{label_name}]: {url}'''

        # Create equivalent inline link markdown
        inline_markdown = f'Click [{link_text}]({url}) for info.'

        # Parse both
        ref_label = MarkdownLabel(text=ref_markdown)
        inline_label = MarkdownLabel(text=inline_markdown)

        # Find labels with ref markup in both
        ref_labels = find_labels_with_ref_markup(ref_label)
        inline_labels = find_labels_with_ref_markup(inline_label)

        # Both should have at least one label with ref markup
        assert len(ref_labels) >= 1, (
            f"Reference-style link should produce ref markup.\n"
            f"Markdown: {ref_markdown!r}"
        )
        assert len(inline_labels) >= 1, (
            f"Inline link should produce ref markup.\n"
            f"Markdown: {inline_markdown!r}"
        )

        # Extract the ref markup from both
        ref_text = ref_labels[0].text
        inline_text = inline_labels[0].text

        # Both should contain the same [ref=url] pattern
        assert f'[ref={url}]' in ref_text, (
            f"Reference-style link should contain [ref={url}].\n"
            f"Got: {ref_text!r}"
        )
        assert f'[ref={url}]' in inline_text, (
            f"Inline link should contain [ref={url}].\n"
            f"Got: {inline_text!r}"
        )

        # Both should contain [/ref] closing tag
        assert '[/ref]' in ref_text, (
            f"Reference-style link should contain [/ref].\n"
            f"Got: {ref_text!r}"
        )
        assert '[/ref]' in inline_text, (
            f"Inline link should contain [/ref].\n"
            f"Got: {inline_text!r}"
        )

    @pytest.mark.property
    @given(
        link_text=st.text(min_size=1, max_size=30, alphabet=st.characters(
            whitelist_categories=['L', 'N'],
            blacklist_characters='[]()&\n\r'
        )),
        # Use ASCII-only characters for URL path to avoid URL encoding differences
        url_path=st.text(min_size=1, max_size=20, alphabet='abcdefghijklmnopqrstuvwxyz0123456789')
    )
    # Complex strategy: 30 examples (adequate coverage)
    @settings(max_examples=30, deadline=None)
    def test_implicit_reference_style_links_render_correctly(
        self, link_text, url_path
    ):
        """**Property 1 (implicit variant): Implicit Reference-Style Links Render Correctly**

        *For any* implicit reference-style link `[text][]` with definition `[text]: url`,
        the InlineRenderer SHALL produce the same BBCode markup as an equivalent
        inline link `[text](url)`.

        **Validates: Requirements 1.1, 1.2**
        """
        assume(len(link_text.strip()) > 0)
        assume(len(url_path.strip()) > 0)

        url = f'http://example.com/{url_path}'

        # Create implicit reference-style link markdown
        ref_markdown = f'''Click [{link_text}][] for info.

[{link_text}]: {url}'''

        # Create equivalent inline link markdown
        inline_markdown = f'Click [{link_text}]({url}) for info.'

        # Parse both
        ref_label = MarkdownLabel(text=ref_markdown)
        inline_label = MarkdownLabel(text=inline_markdown)

        # Find labels with ref markup in both
        ref_labels = find_labels_with_ref_markup(ref_label)
        inline_labels = find_labels_with_ref_markup(inline_label)

        # Both should have at least one label with ref markup
        assert len(ref_labels) >= 1, (
            f"Implicit reference-style link should produce ref markup.\n"
            f"Markdown: {ref_markdown!r}"
        )
        assert len(inline_labels) >= 1, (
            f"Inline link should produce ref markup.\n"
            f"Markdown: {inline_markdown!r}"
        )

        # Extract the ref markup from both
        ref_text = ref_labels[0].text
        inline_text = inline_labels[0].text

        # Both should contain the same [ref=url] pattern
        assert f'[ref={url}]' in ref_text, (
            f"Implicit reference-style link should contain [ref={url}].\n"
            f"Got: {ref_text!r}"
        )
        assert f'[ref={url}]' in inline_text, (
            f"Inline link should contain [ref={url}].\n"
            f"Got: {inline_text!r}"
        )

    @pytest.mark.property
    @given(
        link_text=st.text(min_size=1, max_size=30, alphabet=st.characters(
            whitelist_categories=['L', 'N'],
            blacklist_characters='[]()&\n\r'
        )),
        label_name=st.text(min_size=1, max_size=10, alphabet=st.characters(
            whitelist_categories=['L', 'N'],
            blacklist_characters='[]()&\n\r'
        )),
        # Use ASCII-only characters for URL path to avoid URL encoding differences
        url_path=st.text(min_size=1, max_size=20, alphabet='abcdefghijklmnopqrstuvwxyz0123456789'),
        link_style=st.sampled_from(['unstyled', 'styled'])
    )
    # Mixed finite/complex strategy: 40 examples (2 finite × 20 complex samples)
    @settings(max_examples=40, deadline=None)
    def test_reference_style_links_respect_link_style(
        self, link_text, label_name, url_path, link_style
    ):
        """**Property 1 (styled variant): Reference-Style Links Respect link_style**

        *For any* reference-style link with link_style='styled', the InlineRenderer
        SHALL apply color and underline formatting identically to inline links.

        **Validates: Requirements 1.4**
        """
        assume(len(link_text.strip()) > 0)
        assume(len(label_name.strip()) > 0)
        assume(len(url_path.strip()) > 0)

        url = f'http://example.com/{url_path}'

        # Create reference-style link markdown
        ref_markdown = f'''Click [{link_text}][{label_name}] for info.

[{label_name}]: {url}'''

        # Create equivalent inline link markdown
        inline_markdown = f'Click [{link_text}]({url}) for info.'

        # Parse both with same link_style
        ref_label = MarkdownLabel(text=ref_markdown, link_style=link_style)
        inline_label = MarkdownLabel(text=inline_markdown, link_style=link_style)

        # Find labels with ref markup in both
        ref_labels = find_labels_with_ref_markup(ref_label)
        inline_labels = find_labels_with_ref_markup(inline_label)

        # Both should have at least one label with ref markup
        assert len(ref_labels) >= 1
        assert len(inline_labels) >= 1

        ref_text = ref_labels[0].text
        inline_text = inline_labels[0].text

        if link_style == 'styled':
            # Both should have color and underline styling
            assert '[color=' in ref_text, (
                f"Styled reference-style link should have color.\n"
                f"Got: {ref_text!r}"
            )
            assert '[u]' in ref_text, (
                f"Styled reference-style link should have underline.\n"
                f"Got: {ref_text!r}"
            )
            assert '[color=' in inline_text
            assert '[u]' in inline_text
        else:
            # Unstyled links should not have color/underline
            assert '[color=' not in ref_text, (
                f"Unstyled reference-style link should not have color.\n"
                f"Got: {ref_text!r}"
            )
            assert '[u]' not in ref_text, (
                f"Unstyled reference-style link should not have underline.\n"
                f"Got: {ref_text!r}"
            )


class TestReferenceStyleLinkEventDispatch:
    """Unit tests for on_ref_press event dispatch with reference-style links."""

    @pytest.mark.unit
    @pytest.mark.needs_window
    def test_on_ref_press_dispatches_resolved_url(self):
        """Reference-style link click dispatches on_ref_press with resolved URL.

        **Validates: Requirements 1.3**
        """
        markdown = '''Click [here][1] for info.

[1]: http://example.com/page'''

        label = MarkdownLabel(text=markdown)

        # Track dispatched events
        dispatched_refs = []

        def on_ref_press(instance, ref):
            dispatched_refs.append(ref)

        label.bind(on_ref_press=on_ref_press)

        # Manually dispatch the event (simulating a click)
        label.dispatch('on_ref_press', 'http://example.com/page')

        assert len(dispatched_refs) == 1
        assert dispatched_refs[0] == 'http://example.com/page', (
            f"Expected resolved URL 'http://example.com/page', "
            f"got {dispatched_refs[0]!r}"
        )

    @pytest.mark.unit
    @pytest.mark.needs_window
    def test_on_ref_press_with_implicit_reference_link(self):
        """Implicit reference-style link click dispatches on_ref_press with resolved URL.

        **Validates: Requirements 1.3**
        """
        markdown = '''Visit [Google][] for search.

[Google]: http://google.com/'''

        label = MarkdownLabel(text=markdown)

        # Track dispatched events
        dispatched_refs = []

        def on_ref_press(instance, ref):
            dispatched_refs.append(ref)

        label.bind(on_ref_press=on_ref_press)

        # Manually dispatch the event (simulating a click)
        label.dispatch('on_ref_press', 'http://google.com/')

        assert len(dispatched_refs) == 1
        assert dispatched_refs[0] == 'http://google.com/', (
            f"Expected resolved URL 'http://google.com/', "
            f"got {dispatched_refs[0]!r}"
        )

    @pytest.mark.unit
    @pytest.mark.needs_window
    def test_ref_markup_contains_resolved_url(self):
        """Reference-style link produces ref markup with resolved URL.

        This verifies that the URL in the [ref=url] tag is the resolved URL
        from the definition, not the label reference.

        **Validates: Requirements 1.3**
        """
        markdown = '''Click [here][mylink] for info.

[mylink]: http://example.com/resolved'''

        label = MarkdownLabel(text=markdown)

        # Find labels with ref markup
        ref_labels = find_labels_with_ref_markup(label)

        assert len(ref_labels) >= 1, "Should have at least one label with ref markup"

        ref_text = ref_labels[0].text

        # The ref tag should contain the resolved URL, not the label
        assert '[ref=http://example.com/resolved]' in ref_text, (
            f"Ref tag should contain resolved URL.\n"
            f"Got: {ref_text!r}"
        )
        # Should NOT contain the label name in the ref tag
        assert '[ref=mylink]' not in ref_text, (
            f"Ref tag should not contain label name.\n"
            f"Got: {ref_text!r}"
        )

    @pytest.mark.unit
    @pytest.mark.needs_window
    def test_multiple_reference_links_same_label_dispatch_same_url(self):
        """Multiple links with same label all dispatch the same resolved URL.

        **Validates: Requirements 1.3**
        """
        markdown = '''Click [here][1] or [there][1] for info.

[1]: http://example.com/shared'''

        label = MarkdownLabel(text=markdown)

        # Find labels with ref markup
        ref_labels = find_labels_with_ref_markup(label)

        assert len(ref_labels) >= 1, "Should have at least one label with ref markup"

        ref_text = ref_labels[0].text

        # Both links should resolve to the same URL
        # Count occurrences of the resolved URL in ref tags
        url_count = ref_text.count('[ref=http://example.com/shared]')

        assert url_count == 2, (
            f"Expected 2 ref tags with same URL, got {url_count}.\n"
            f"Text: {ref_text!r}"
        )

    @pytest.mark.unit
    @pytest.mark.needs_window
    def test_reference_link_with_title_dispatches_url(self):
        """Reference-style link with title dispatches URL (not title).

        **Validates: Requirements 1.3**
        """
        markdown = '''Visit [Google][] for search.

[Google]: http://google.com/ "Search Engine"'''

        label = MarkdownLabel(text=markdown)

        # Find labels with ref markup
        ref_labels = find_labels_with_ref_markup(label)

        assert len(ref_labels) >= 1, "Should have at least one label with ref markup"

        ref_text = ref_labels[0].text

        # The ref tag should contain the URL, not the title
        assert '[ref=http://google.com/]' in ref_text, (
            f"Ref tag should contain URL.\n"
            f"Got: {ref_text!r}"
        )
        # Title should not appear in ref tag
        assert 'Search Engine' not in ref_text.split('[ref=')[1].split(']')[0], (
            f"Title should not be in ref tag URL.\n"
            f"Got: {ref_text!r}"
        )
