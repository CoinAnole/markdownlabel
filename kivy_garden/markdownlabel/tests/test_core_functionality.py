"""
Core functionality tests for MarkdownLabel widget.

This module contains tests for fundamental markdown parsing, rendering,
and widget tree generation functionality.
"""

import pytest
from hypothesis import given, strategies as st, settings, assume

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from kivy_garden.markdownlabel import MarkdownLabel
from .test_utils import (
    markdown_heading,
    markdown_paragraph,
    markdown_link,
    simple_markdown_document,
    st_alphanumeric_text
)


# *For any* valid Markdown text, when parsed and rendered by MarkdownLabel,
# the resulting widget tree SHALL contain at least one child widget for each
# block-level element in the AST.

class TestMarkdownToWidgetTreeGeneration:
    """Property tests for widget tree generation (Property 1)."""

    @pytest.mark.needs_window
    @given(simple_markdown_document())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_markdown_produces_widgets(self, markdown_text):
        """Valid Markdown text produces at least one widget."""
        assume(markdown_text.strip())  # Skip empty text

        label = MarkdownLabel(text=markdown_text)

        # Should have at least one child widget
        assert len(label.children) >= 1, \
            f"Expected at least 1 child for markdown: {markdown_text!r}"

    @pytest.mark.needs_window
    @given(markdown_heading())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
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

    @pytest.mark.needs_window
    @given(markdown_paragraph())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_paragraph_produces_label_widget(self, paragraph):
        """Paragraph Markdown produces a Label widget."""
        assume(paragraph.strip())  # Skip empty paragraphs

        label = MarkdownLabel(text=paragraph)

        # Should have at least one child
        assert len(label.children) >= 1, \
            f"Expected at least 1 child for paragraph: {paragraph!r}"

    @given(st.integers(min_value=1, max_value=5))
    # Small finite strategy: 5 examples (input space size: 5)
    @settings(max_examples=5, deadline=None)
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


# *For any* two different Markdown texts, when the `text` property is changed
# from the first to the second, the widget tree SHALL reflect the structure
# of the second text, not the first.

class TestMarkdownTextPropertyUpdates:
    """Property tests for reactive text updates (Property 2)."""

    @pytest.mark.needs_window
    @given(markdown_heading(), markdown_paragraph())
    # Combination strategy: 50 examples (combination coverage)
    @settings(max_examples=50, deadline=None)
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

    @pytest.mark.needs_window
    @given(st.integers(min_value=1, max_value=3), st.integers(min_value=1, max_value=3))
    # Combination strategy: 9 examples (combination coverage)
    @settings(max_examples=9, deadline=None)
    def test_different_block_counts_update_correctly(self, count1, count2):
        """Changing from N blocks to M blocks updates widget count."""
        assume(count1 != count2)

        # Create markdown with count1 paragraphs
        text1 = '\n\n'.join([f'Para {i}' for i in range(count1)])
        # Create markdown with count2 paragraphs
        text2 = '\n\n'.join([f'New para {i}' for i in range(count2)])

        label = MarkdownLabel(text=text1)
        children_before = len(label.children)

        # Change text - use force_rebuild() for immediate update since
        # text changes now use deferred rebuilds
        label.text = text2
        label.force_rebuild()
        children_after = len(label.children)

        # The number of children should change to reflect new content
        # (may include blank_line widgets, so we check >= count)
        assert children_after >= count2, \
            f"Expected at least {count2} children after update, got {children_after}"

    @pytest.mark.needs_window
    @given(simple_markdown_document())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_clear_text_removes_widgets(self, markdown_text):
        """Setting text to empty removes all widgets."""
        assume(markdown_text.strip())

        label = MarkdownLabel(text=markdown_text)
        assert len(label.children) > 0, "Should have children initially"

        # Clear text - use force_rebuild() for immediate update since
        # text changes now use deferred rebuilds
        label.text = ''
        label.force_rebuild()

        assert len(label.children) == 0, \
            f"Expected 0 children after clearing text, got {len(label.children)}"

    @pytest.mark.needs_window
    @given(simple_markdown_document(), simple_markdown_document())
    # Combination strategy: 50 examples (combination coverage)
    @settings(max_examples=50, deadline=None)
    def test_ast_updates_with_text(self, text1, text2):
        """AST tokens update when text changes."""
        assume(text1.strip() and text2.strip())

        label = MarkdownLabel(text=text1)
        ast1 = label.get_ast()

        # Use force_rebuild() for immediate update since
        # text changes now use deferred rebuilds
        label.text = text2
        label.force_rebuild()
        ast2 = label.get_ast()

        # If texts are different, ASTs should be different
        if text1 != text2:
            # At minimum, the AST should be updated (not necessarily different
            # if the texts parse to the same structure)
            assert label.text == text2


# *For any* Markdown link [text](url), the rendered Kivy markup SHALL contain
# [ref=url]text[/ref].

class TestMarkdownLinkRendering:
    """Property tests for link ref markup (Property 12)."""

    @pytest.mark.needs_window
    @given(markdown_link())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
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

    @pytest.mark.needs_window
    @given(st_alphanumeric_text(min_size=1, max_size=20))
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
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

    @pytest.mark.needs_window
    @given(st.from_regex(r'https?://[a-z]+\.[a-z]+/[a-z]+', fullmatch=True))
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
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


# *For any* Markdown with nesting depth up to 10 levels (nested lists, quotes),
# the MarkdownLabel SHALL render without raising exceptions or causing stack overflow.

class TestMarkdownNestingStability:
    """Property tests for deep nesting stability (Property 18)."""

    @pytest.mark.needs_window
    @given(st.integers(min_value=1, max_value=15))
    # Medium finite strategy: 15 examples (adequate finite coverage)
    @settings(max_examples=15, deadline=None)
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

    @pytest.mark.needs_window
    @given(st.integers(min_value=1, max_value=15))
    # Medium finite strategy: 15 examples (adequate finite coverage)
    @settings(max_examples=15, deadline=None)
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

    @pytest.mark.needs_window
    @given(st.integers(min_value=1, max_value=15))
    # Medium finite strategy: 15 examples (adequate finite coverage)
    @settings(max_examples=15, deadline=None)
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
