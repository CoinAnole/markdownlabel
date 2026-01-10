"""
text_size and code block font preservation tests for MarkdownLabel.

This module contains tests for text_size property identity preservation,
binding transitions, and code block font preservation when font_family changes.

Tests are designed to run in headless CI environments without requiring a Kivy window.
"""

import pytest
from hypothesis import given, strategies as st, settings, assume

from kivy.uix.label import Label

from kivy_garden.markdownlabel import MarkdownLabel
from .test_utils import (
    simple_markdown_document,
    find_labels_recursive,
    collect_widget_ids
)


# =============================================================================
# text_size Widget Identity Preservation Tests
# =============================================================================


@pytest.mark.property
@pytest.mark.slow
class TestTextSizePropertyIdentityPreservationPBT:
    """Property-based tests for text_size property identity preservation.

    These tests verify that changing text_size preserves all widget object IDs
    in the subtree, regardless of the transition type.

    **Property 3: text_size updates preserve widget identity**
    **Validates: Requirements 4.1, 4.4**
    """

    @given(
        markdown_text=simple_markdown_document(),
        text_size=st.one_of(
            # [None, None] - no constraints
            st.just([None, None]),
            # [width, None] - width constrained only
            st.tuples(
                st.floats(min_value=50, max_value=500, allow_nan=False, allow_infinity=False),
                st.none()
            ).map(list),
            # [None, height] - height constrained only
            st.tuples(
                st.none(),
                st.floats(min_value=50, max_value=500, allow_nan=False, allow_infinity=False)
            ).map(list),
            # [width, height] - both constrained
            st.tuples(
                st.floats(min_value=50, max_value=500, allow_nan=False, allow_infinity=False),
                st.floats(min_value=50, max_value=500, allow_nan=False, allow_infinity=False)
            ).map(list)
        )
    )
    # Feature: optimize-rebuild-contract, Property 3: text_size updates preserve widget identity
    # Mixed finite/complex strategy: 50 examples (4 finite × 12 complex samples)
    @settings(max_examples=50, deadline=None)
    def test_text_size_preserves_widget_identity(self, markdown_text, text_size):
        """text_size Updates Preserve Widget Identity.

        *For any* MarkdownLabel with non-empty content, and *for any* valid
        text_size value (including [None, None], [width, None], [None, height],
        [width, height]), changing text_size SHALL preserve all widget object
        IDs in the subtree (the set of IDs before equals the set of IDs after).

        **Validates: Requirements 4.1, 4.4**
        """
        # Ensure we have non-empty content
        assume(markdown_text and markdown_text.strip())

        # Create MarkdownLabel with initial content
        label = MarkdownLabel(text=markdown_text)

        # Ensure we have children to test
        assume(len(label.children) > 0)

        # Capture widget IDs before change
        ids_before = collect_widget_ids(label)

        # Apply text_size change
        label.text_size = text_size

        # Capture widget IDs after change
        ids_after = collect_widget_ids(label)

        # Assert: widget IDs should be unchanged
        assert ids_before == ids_after, (
            f"Widget IDs changed after text_size update to {text_size}. "
            f"Before: {len(ids_before)} widgets, After: {len(ids_after)} widgets"
        )


# =============================================================================
# text_size Binding Transition Tests
# =============================================================================


@pytest.mark.unit
class TestTextSizeBindingTransitions:
    """Unit tests for text_size binding transitions.

    These tests verify that text_size binding transitions work correctly,
    ensuring that bindings are properly updated when transitioning between
    [None, None] and constrained values.

    **Validates: Requirements 4.2, 4.3**
    """

    def test_text_size_none_to_width_constrained_updates_bindings(self):
        """Transition from [None, None] to [width, None] updates bindings correctly.

        When text_size changes from [None, None] to a width-constrained value,
        the child Labels should have their text_size updated to reflect the
        new width constraint.

        **Validates: Requirements 4.2**
        """
        # Create MarkdownLabel with [None, None] text_size
        label = MarkdownLabel(text='# Heading\n\nParagraph text', text_size=[None, None])

        # Get child Labels
        child_labels = find_labels_recursive(label)
        assert len(child_labels) >= 1, "Expected at least one child Label"

        # Transition to width-constrained text_size
        label.text_size = [200, None]

        # Verify child Labels have updated text_size
        # Verify child Labels have updated text_size
        for child_label in child_labels:
            # The text_size width should be 200
            # The text_size width should be 200
            assert child_label.text_size[0] == 200, \
                f"Child Label text_size width should be 200, got {child_label.text_size[0]}"

    def test_text_size_width_constrained_to_none_updates_bindings(self):
        """Transition from [width, None] to [None, None] updates bindings correctly.

        When text_size changes from a width-constrained value to [None, None],
        the child Labels should have their text_size updated appropriately
        based on the strict_label_mode setting.

        **Validates: Requirements 4.3**
        """
        # Create MarkdownLabel with width-constrained text_size
        label = MarkdownLabel(text='# Heading\n\nParagraph text', text_size=[200, None])

        # Get child Labels
        child_labels = find_labels_recursive(label)
        assert len(child_labels) >= 1, "Expected at least one child Label"

        # Transition to [None, None]
        label.text_size = [None, None]

        # Verify child Labels have updated text_size
        # In non-strict mode, text_size should use widget width for wrapping
        for child_label in child_labels:
            # text_size should be updated (not still [200, None])
            # Width should be widget width, not the old 200
            assert child_label.text_size[0] != 200, \
                "Child Label text_size width should have updated from 200"

            # In non-strict mode, it should likely match the widget width
            assert child_label.text_size[0] == child_label.width, \
                (f"Child Label text_size width {child_label.text_size[0]} "
                 f"should match widget width {child_label.width}")

    def test_text_size_transition_preserves_widget_identity(self):
        """text_size transitions preserve widget identity.

        Regardless of the transition direction, widget IDs should be preserved.

        **Validates: Requirements 4.2, 4.3, 4.4**
        """
        # Create MarkdownLabel with [None, None] text_size
        label = MarkdownLabel(text='# Heading\n\nParagraph text', text_size=[None, None])

        # Capture widget IDs before transition
        ids_before = collect_widget_ids(label)

        # Transition to constrained
        label.text_size = [200, 100]

        # Capture widget IDs after first transition
        ids_after_constrained = collect_widget_ids(label)

        # Verify widget IDs preserved
        assert ids_before == ids_after_constrained, \
            "Widget IDs changed after transition to constrained text_size"

        # Transition back to [None, None]
        label.text_size = [None, None]

        # Capture widget IDs after second transition
        ids_after_none = collect_widget_ids(label)

        # Verify widget IDs still preserved
        assert ids_before == ids_after_none, \
            "Widget IDs changed after transition back to [None, None]"

    def test_text_size_rebinds_width_after_mode_changes(self):
        """text_size transitions drop stale bindings and respect explicit widths."""
        label = MarkdownLabel(text='Hello World', text_size=[None, None])
        ids_before = collect_widget_ids(label)

        child_labels = find_labels_recursive(label)
        assert len(child_labels) >= 1, "Expected at least one child Label"
        child = child_labels[0]

        # Height-only: width should follow widget width via binding
        label.text_size = [None, 60]
        child.width = 150
        assert child.text_size[0] == child.width
        assert child.text_size[1] == 60

        # Switch to explicit width: previous width binding should be removed
        label.text_size = [140, None]
        child.width = 260  # should NOT override explicit width
        assert child.text_size[0] == 140
        assert child.text_size[1] is None

        ids_after = collect_widget_ids(label)
        assert ids_before == ids_after, "text_size transitions should not rebuild"


# =============================================================================
# Code Block Font Preservation Tests
# =============================================================================


@pytest.mark.property
@pytest.mark.slow
class TestCodeBlockFontPreservationPBT:
    """Property-based tests for code block font preservation.

    These tests verify that code blocks preserve their monospace font
    (code_font_name) when font_family is changed on the MarkdownLabel.

    **Property 4: Code blocks preserve monospace font when font_family changes**
    **Validates: Requirements 6.2**
    """

    def _find_code_block_labels(self, widget):
        """Find Labels that are inside code block containers.

        Code block containers have a 'language_info' attribute or '_is_code' marker.
        """
        code_labels = []

        def find_in_container(container):
            if hasattr(container, 'language_info'):
                # This is a code block container
                for child in container.children:
                    if isinstance(child, Label):
                        code_labels.append(child)
            if isinstance(container, Label) and hasattr(container, '_is_code') and container._is_code:
                code_labels.append(container)
            if hasattr(container, 'children'):
                for child in container.children:
                    find_in_container(child)

        find_in_container(widget)
        return code_labels

    def _find_non_code_labels(self, widget):
        """Find Labels that are NOT inside code block containers."""
        all_labels = find_labels_recursive(widget)
        code_labels = self._find_code_block_labels(widget)
        return [lbl for lbl in all_labels if lbl not in code_labels]

    @given(
        font_family=st.text(min_size=1, max_size=30, alphabet=st.characters(
            whitelist_categories=['L', 'N'],
            blacklist_characters='[]&\n\r'
        ))
    )
    # Complex strategy: 30 examples (adequate coverage)
    @settings(max_examples=30, deadline=None)
    def test_code_blocks_preserve_code_font_name_when_font_family_changes(
        self, font_family
    ):
        """Code Blocks Preserve Monospace Font When font_family Changes.

        *For any* MarkdownLabel containing code blocks and *for any* font_family
        value, changing font_family SHALL update non-code Labels but preserve
        the code_font_name on code block Labels.

        **Validates: Requirements 6.2**
        """
        # Create markdown with both regular text and code block
        markdown = 'Regular paragraph\n\n```python\nprint("hello world")\n```\n\nMore text'
        code_font = 'RobotoMono-Regular'

        # Create MarkdownLabel with code block
        label = MarkdownLabel(text=markdown, code_font_name=code_font)

        # Find code block labels before change
        code_labels_before = self._find_code_block_labels(label)
        assume(len(code_labels_before) >= 1)

        # Verify code blocks have code_font_name initially
        for code_label in code_labels_before:
            assert code_label.font_name == code_font, (
                f"Code block should have code_font_name={code_font!r} initially, "
                f"got {code_label.font_name!r}"
            )

        # Change font_family
        label.font_family = font_family

        # Find code block labels after change
        code_labels_after = self._find_code_block_labels(label)

        # Verify code blocks STILL have code_font_name (not affected by font_family)
        for code_label in code_labels_after:
            assert code_label.font_name == code_font, (
                f"Code block should preserve code_font_name={code_font!r} after "
                f"font_family change, got {code_label.font_name!r}"
            )
            # Also verify font_family is NOT set on code blocks
            assert code_label.font_family is None, (
                f"Code block should NOT have font_family set, "
                f"got {code_label.font_family!r}"
            )

        # Verify non-code labels DO have font_family set
        non_code_labels = self._find_non_code_labels(label)
        for non_code_label in non_code_labels:
            assert non_code_label.font_family == font_family, (
                f"Non-code label should have font_family={font_family!r}, "
                f"got {non_code_label.font_family!r}"
            )
