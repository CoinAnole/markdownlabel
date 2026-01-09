"""
Widget identity preservation tests for MarkdownLabel rebuild semantics.

This module contains tests that verify widget identity preservation for style-only
property changes. These tests ensure that changing style properties does not
rebuild the widget tree, preserving all widget object IDs.

Tests are designed to run in headless CI environments without requiring a Kivy window.
"""

import pytest
from hypothesis import given, strategies as st, settings, assume

from kivy_garden.markdownlabel import MarkdownLabel
from .test_utils import (
    simple_markdown_document,
    collect_widget_ids,
    st_font_size,
    st_font_name,
    st_rgba_color,
    find_labels_recursive,
    is_code_label
)


@pytest.mark.test_tests
class TestWidgetIdentityHelpers:
    """Tests for the collect_widget_ids helper function."""

    def test_collect_widget_ids_includes_root(self):
        """collect_widget_ids includes root widget by default."""
        label = MarkdownLabel(text='Test')
        ids = collect_widget_ids(label)
        assert id(label) in ids

    def test_collect_widget_ids_excludes_root_when_requested(self):
        """collect_widget_ids excludes root widget when exclude_root=True."""
        label = MarkdownLabel(text='Test')
        ids = collect_widget_ids(label, exclude_root=True)
        assert id(label) not in ids

    def test_collect_widget_ids_includes_children(self):
        """collect_widget_ids includes all child widgets."""
        label = MarkdownLabel(text='# Heading\n\nParagraph')
        ids = collect_widget_ids(label)

        # Should have more than just the root
        assert len(ids) > 1

        # All children should be included
        for child in label.children:
            assert id(child) in ids


class TestStylePropertyIdentityPreservation:
    """Tests for style property changes preserving widget identities.

    These tests verify that changing style-only properties (base_font_size,
    color, halign, valign, disabled, disabled_color, base_direction, line_height)
    preserves all widget object IDs in the subtree.

    """

    def test_base_font_size_preserves_widget_tree(self):
        """Changing base_font_size preserves widget tree."""
        label = MarkdownLabel(text='# Heading\n\nParagraph text', base_font_size=15)

        # Capture widget IDs before change
        ids_before = collect_widget_ids(label)

        # Apply property change
        label.base_font_size = 20

        # Assert widget IDs unchanged
        ids_after = collect_widget_ids(label)
        assert ids_before == ids_after, \
            "Widget IDs changed after base_font_size update"

    def test_color_preserves_widget_tree(self):
        """Changing color preserves widget tree."""
        label = MarkdownLabel(text='# Heading\n\nParagraph text', color=[1, 1, 1, 1])

        # Capture widget IDs before change
        ids_before = collect_widget_ids(label)

        # Apply property change
        label.color = [0.5, 0.5, 0.5, 1]

        # Assert widget IDs unchanged
        ids_after = collect_widget_ids(label)
        assert ids_before == ids_after, \
            "Widget IDs changed after color update"

    def test_halign_preserves_widget_tree(self):
        """Changing halign preserves widget tree."""
        label = MarkdownLabel(text='# Heading\n\nParagraph text', halign='left')

        # Capture widget IDs before change
        ids_before = collect_widget_ids(label)

        # Apply property change
        label.halign = 'center'

        # Assert widget IDs unchanged
        ids_after = collect_widget_ids(label)
        assert ids_before == ids_after, \
            "Widget IDs changed after halign update"

    def test_valign_preserves_widget_tree(self):
        """Changing valign preserves widget tree."""
        label = MarkdownLabel(text='# Heading\n\nParagraph text', valign='bottom')

        # Capture widget IDs before change
        ids_before = collect_widget_ids(label)

        # Apply property change
        label.valign = 'top'

        # Assert widget IDs unchanged
        ids_after = collect_widget_ids(label)
        assert ids_before == ids_after, \
            "Widget IDs changed after valign update"

    def test_disabled_preserves_widget_tree(self):
        """Changing disabled preserves widget tree."""
        label = MarkdownLabel(text='# Heading\n\nParagraph text', disabled=False)

        # Capture widget IDs before change
        ids_before = collect_widget_ids(label)

        # Apply property change
        label.disabled = True

        # Assert widget IDs unchanged
        ids_after = collect_widget_ids(label)
        assert ids_before == ids_after, \
            "Widget IDs changed after disabled update"

    def test_disabled_color_preserves_widget_tree(self):
        """Changing disabled_color preserves widget tree."""
        label = MarkdownLabel(
            text='# Heading\n\nParagraph text',
            disabled_color=[1, 1, 1, 0.3]
        )

        # Capture widget IDs before change
        ids_before = collect_widget_ids(label)

        # Apply property change
        label.disabled_color = [0.5, 0.5, 0.5, 0.5]

        # Assert widget IDs unchanged
        ids_after = collect_widget_ids(label)
        assert ids_before == ids_after, \
            "Widget IDs changed after disabled_color update"

    def test_base_direction_preserves_widget_tree(self):
        """Changing base_direction preserves widget tree."""
        label = MarkdownLabel(text='# Heading\n\nParagraph text', base_direction=None)

        # Capture widget IDs before change
        ids_before = collect_widget_ids(label)

        # Apply property change
        label.base_direction = 'ltr'

        # Assert widget IDs unchanged
        ids_after = collect_widget_ids(label)
        assert ids_before == ids_after, \
            "Widget IDs changed after base_direction update"

    def test_line_height_preserves_widget_tree(self):
        """Changing line_height preserves widget tree."""
        label = MarkdownLabel(text='# Heading\n\nParagraph text', line_height=1.0)

        # Capture widget IDs before change
        ids_before = collect_widget_ids(label)

        # Apply property change
        label.line_height = 1.5

        # Assert widget IDs unchanged
        ids_after = collect_widget_ids(label)
        assert ids_before == ids_after, \
            "Widget IDs changed after line_height update"

    def test_multiple_style_properties_preserve_widget_tree(self):
        """Changing multiple style properties preserves widget tree."""
        label = MarkdownLabel(
            text='# Heading\n\nParagraph text',
            base_font_size=15,
            color=[1, 1, 1, 1],
            halign='left',
            valign='bottom',
            line_height=1.0
        )

        # Capture widget IDs before changes
        ids_before = collect_widget_ids(label)

        # Apply multiple property changes
        label.base_font_size = 20
        label.color = [0.8, 0.8, 0.8, 1]
        label.halign = 'center'
        label.valign = 'top'
        label.line_height = 1.5
        label.disabled = True
        label.base_direction = 'rtl'

        # Assert widget IDs unchanged
        ids_after = collect_widget_ids(label)
        assert ids_before == ids_after, \
            "Widget IDs changed after multiple style property updates"

    def test_font_name_change_preserves_widget_tree(self):
        """Changing font_name preserves widget tree (style-only property)."""
        label = MarkdownLabel(text='# Heading\n\nParagraph', font_name='Roboto')

        # Capture widget IDs before change
        ids_before = collect_widget_ids(label)

        # Apply property change
        # Use a distinct font that is NOT the code font (RobotoMono-Regular)
        # to ensure we can verify it applied correctly.
        label.font_name = 'Roboto-Italic'

        # Assert widget IDs unchanged
        ids_after = collect_widget_ids(label)
        assert ids_before == ids_after, \
            "Widget IDs changed after font_name update"

        # Verify font_name was actually applied to child Labels
        labels = find_labels_recursive(label)
        for lbl in labels:
            # Code labels keep their code_font_name, others get the new font_name
            if not is_code_label(lbl):
                assert lbl.font_name == 'Roboto-Italic', \
                    f"Expected font_name='Roboto-Italic', got '{lbl.font_name}'"

    def test_text_size_change_preserves_widget_tree(self):
        """Changing text_size preserves widget tree (style-only property)."""
        label = MarkdownLabel(text='# Heading\n\nParagraph', text_size=[None, None])

        # Capture widget IDs before change
        ids_before = collect_widget_ids(label)

        # Apply property change
        label.text_size = [200, None]

        # Assert widget IDs unchanged
        ids_after = collect_widget_ids(label)
        assert ids_before == ids_after, \
            "Widget IDs changed after text_size update"


@pytest.mark.property
@pytest.mark.slow
class TestStylePropertyIdentityPreservationPBT:
    """Property-based tests for style property identity preservation.
    """

    @given(
        markdown_text=simple_markdown_document(),
        base_font_size=st_font_size(),
        color=st_rgba_color(),
        halign=st.sampled_from(['left', 'center', 'right', 'justify']),
        valign=st.sampled_from(['bottom', 'middle', 'top']),
        disabled=st.booleans(),
        disabled_color=st_rgba_color(),
        base_direction=st.sampled_from([None, 'ltr', 'rtl', 'weak_ltr', 'weak_rtl']),
        line_height=st.floats(min_value=0.5, max_value=3.0, allow_nan=False,
                               allow_infinity=False)
    )
    # Mixed finite/complex strategy: 50 examples (120 finite × 5 complex samples)
    @settings(max_examples=50, deadline=None)
    def test_style_property_changes_preserve_widget_tree(
        self, markdown_text, base_font_size, color, halign, valign,
        disabled, disabled_color, base_direction, line_height
    ):
        """Style Property Changes Preserve Widget Tree.

        *For any* MarkdownLabel with non-empty content, and *for any* style-only
        property (base_font_size, color, halign, valign, disabled, disabled_color,
        base_direction, line_height), changing that property SHALL preserve all
        widget object IDs in the subtree (the set of IDs before equals the set
        of IDs after).
        """
        # Ensure we have non-empty content
        assume(markdown_text and markdown_text.strip())

        # Create MarkdownLabel with initial content
        label = MarkdownLabel(text=markdown_text)

        # Ensure we have children to test
        assume(len(label.children) > 0)

        # Capture widget IDs before changes
        ids_before = collect_widget_ids(label)

        # Apply all style property changes
        label.base_font_size = base_font_size
        label.color = list(color)
        label.halign = halign
        label.valign = valign
        label.disabled = disabled
        label.disabled_color = list(disabled_color)
        label.base_direction = base_direction
        label.line_height = line_height

        # Capture widget IDs after changes
        ids_after = collect_widget_ids(label)

        # Assert: widget IDs should be unchanged
        assert ids_before == ids_after, (
            f"Widget IDs changed after style property updates. "
            f"Before: {len(ids_before)} widgets, After: {len(ids_after)} widgets"
        )


@pytest.mark.property
@pytest.mark.slow
class TestRootIDPreservationPBT:
    """Property-based tests for root widget ID preservation."""

    @given(
        markdown_text=simple_markdown_document(),
        # Style properties
        base_font_size=st_font_size(),
        color=st_rgba_color(),
        halign=st.sampled_from(['left', 'center', 'right', 'justify']),
        valign=st.sampled_from(['bottom', 'middle', 'top']),
        line_height=st.floats(min_value=0.5, max_value=3.0, allow_nan=False,
                               allow_infinity=False),
        disabled=st.booleans()
    )
    # Mixed finite/complex strategy: 50 examples (24 finite × 4 complex samples)
    @settings(max_examples=50, deadline=None)
    def test_root_id_preserved_across_style_property_changes(
        self, markdown_text, base_font_size, color, halign, valign,
        line_height, disabled
    ):
        """Root Widget ID Preserved Across Style Property Changes.

        *For any* MarkdownLabel, and *for any* style property change, the root
        MarkdownLabel's object ID SHALL remain unchanged.
        """
        # Ensure we have non-empty content
        assume(markdown_text and markdown_text.strip())

        # Create MarkdownLabel with initial content
        label = MarkdownLabel(text=markdown_text)

        # Capture root ID before changes
        root_id_before = id(label)

        # Apply style property changes
        label.base_font_size = base_font_size
        label.color = list(color)
        label.halign = halign
        label.valign = valign
        label.line_height = line_height
        label.disabled = disabled

        # Assert: root ID should be unchanged
        assert id(label) == root_id_before, (
            f"Root MarkdownLabel ID changed after style property updates. "
            f"Before: {root_id_before}, After: {id(label)}"
        )

    @given(
        initial_text=simple_markdown_document(),
        new_text=simple_markdown_document(),
        font_name=st_font_name(),
        link_style=st.sampled_from(['unstyled', 'styled']),
        strict_label_mode=st.booleans(),
        render_mode=st.sampled_from(['widgets', 'auto'])
    )
    # Mixed finite/complex strategy: 48 examples (24 finite × 2 complex samples)
    @settings(max_examples=48, deadline=None)
    def test_root_id_preserved_across_structure_property_changes(
        self, initial_text, new_text, font_name, link_style,
        strict_label_mode, render_mode
    ):
        """Root Widget ID Preserved Across Structure Property Changes.

        *For any* MarkdownLabel, and *for any* structure property change, the root
        MarkdownLabel's object ID SHALL remain unchanged.
        """
        # Ensure we have non-empty content
        assume(initial_text and initial_text.strip())
        assume(new_text and new_text.strip())

        # Create MarkdownLabel with initial content
        label = MarkdownLabel(text=initial_text)

        # Capture root ID before changes
        root_id_before = id(label)

        # Apply structure property changes and force_rebuild()
        label.text = new_text
        label.font_name = font_name
        label.link_style = link_style
        label.strict_label_mode = strict_label_mode
        label.render_mode = render_mode
        label.force_rebuild()

        # Assert: root ID should be unchanged
        assert id(label) == root_id_before, (
            f"Root MarkdownLabel ID changed after structure property updates. "
            f"Before: {root_id_before}, After: {id(label)}"
        )

    @given(
        markdown_text=simple_markdown_document(),
        # Mix of style and structure properties
        base_font_size=st_font_size(),
        color=st_rgba_color(),
        font_name=st_font_name(),
        link_style=st.sampled_from(['unstyled', 'styled'])
    )
    # Mixed finite/complex strategy: 50 examples (2 finite × 25 complex samples)
    @settings(max_examples=50, deadline=None)
    def test_root_id_preserved_across_mixed_property_changes(
        self, markdown_text, base_font_size, color, font_name, link_style
    ):
        """Root Widget ID Preserved Across Mixed Property Changes.

        *For any* MarkdownLabel, and *for any* combination of style and structure
        property changes, the root MarkdownLabel's object ID SHALL remain unchanged.
        """
        # Ensure we have non-empty content
        assume(markdown_text and markdown_text.strip())

        # Create MarkdownLabel with initial content
        label = MarkdownLabel(text=markdown_text)

        # Capture root ID before changes
        root_id_before = id(label)

        # Apply mixed property changes
        label.base_font_size = base_font_size
        label.color = list(color)
        label.font_name = font_name
        label.link_style = link_style
        label.force_rebuild()

        # Assert: root ID should be unchanged
        assert id(label) == root_id_before, (
            f"Root MarkdownLabel ID changed after mixed property updates. "
            f"Before: {root_id_before}, After: {id(label)}"
        )

    @given(
        markdown_text=simple_markdown_document(),
        font_name=st_font_name()
    )
    # Mixed finite/complex strategy: 15 examples (3 finite × 5 complex samples)
    @settings(max_examples=15, deadline=None)
    def test_font_name_change_preserves_widget_tree(self, markdown_text, font_name):
        """Font Name Change Preserves Widget Tree.

        *For any* MarkdownLabel with non-empty content, and *for any* font_name,
        changing font_name SHALL preserve widget object IDs (style-only property)
        while updating the font_name on child Labels.
        """
        # Ensure we have non-empty content
        assume(markdown_text and markdown_text.strip())

        # Use a different initial font_name
        initial_font = 'Roboto' if font_name != 'Roboto' else 'RobotoMono-Regular'

        # Create MarkdownLabel with initial content
        label = MarkdownLabel(text=markdown_text, font_name=initial_font)

        # Ensure we have children to test
        assume(len(label.children) > 0)

        # Capture widget IDs before change
        ids_before = collect_widget_ids(label)

        # Apply property change
        label.font_name = font_name

        # Assert widget IDs unchanged
        ids_after = collect_widget_ids(label)
        assert ids_before == ids_after, (
            f"Widget IDs changed after font_name update. "
            f"Before: {len(ids_before)} widgets, After: {len(ids_after)} widgets"
        )

        # Verify font_name was actually applied
        labels = find_labels_recursive(label)
        for lbl in labels:
            if not is_code_label(lbl):
                assert lbl.font_name == font_name, \
                    f"Expected font_name='{font_name}', got '{lbl.font_name}'"
