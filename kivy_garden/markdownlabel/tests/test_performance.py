"""
Performance and efficiency tests for MarkdownLabel widget.

This module contains tests that verify performance-related behaviors including
efficient style updates, batched rebuilds, deferred rebuild scheduling, and
content clipping behavior.
"""

import pytest
from hypothesis import given, strategies as st, settings, assume

from kivy_garden.markdownlabel import MarkdownLabel
from .test_utils import (
    find_labels_recursive,
    collect_widget_ids,
    st_font_size,
    st_rgba_color,
    colors_equal,
    floats_equal
)


@pytest.mark.slow
class TestStyleOnlyPropertyUpdates:
    """Property tests for efficient style updates.

    Tests verify that style-only property changes update descendant widgets
    in place without rebuilding the widget tree, while structure property
    changes trigger a full rebuild.
    """

    @pytest.mark.property
    @given(st_font_size(min_value=10, max_value=50),
           st_font_size(min_value=10, max_value=50))
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_font_size_change_preserves_widget_tree(self, initial_size, new_size):
        """Changing font_size preserves widget tree structure (widget identities)."""
        assume(initial_size != new_size)

        # Create label with some content
        markdown = '# Heading\n\nParagraph text here.'
        label = MarkdownLabel(text=markdown, font_size=initial_size)

        # Collect widget ids before change
        ids_before = collect_widget_ids(label)

        # Change font_size (style-only property)
        label.font_size = new_size

        # Collect widget ids after change
        ids_after = collect_widget_ids(label)

        # Widget tree structure should be preserved (same widget objects)
        assert ids_before == ids_after, \
            f"Widget tree changed after font_size update. Before: {len(ids_before)}, After: {len(ids_after)}"

        # Verify the font_size change was actually applied to child Labels
        child_labels = find_labels_recursive(label)
        assert len(child_labels) >= 1, "Expected at least one child Label"
        # Note: Heading labels have scaled font sizes, so we check base_font_size on the parent
        assert floats_equal(label.base_font_size, new_size), \
            f"Expected base_font_size={new_size}, got {label.base_font_size}"

    @pytest.mark.property
    @given(st_rgba_color())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_color_change_preserves_widget_tree(self, new_color):
        """Changing color preserves widget tree structure (widget identities)."""
        # Create label with some content
        markdown = 'Simple paragraph text.'
        label = MarkdownLabel(text=markdown, color=[1, 1, 1, 1])

        # Collect widget ids before change
        ids_before = collect_widget_ids(label)

        # Change color (style-only property)
        label.color = list(new_color)

        # Collect widget ids after change
        ids_after = collect_widget_ids(label)

        # Widget tree structure should be preserved
        assert ids_before == ids_after, \
            "Widget tree changed after color update"

    @pytest.mark.property
    @given(st_rgba_color())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_color_change_updates_descendant_labels(self, new_color):
        """Changing color updates all descendant Label widgets."""
        # Create label with some content
        markdown = '# Heading\n\nParagraph text.'
        label = MarkdownLabel(text=markdown, color=[1, 1, 1, 1])

        # Change color
        new_color_list = list(new_color)
        label.color = new_color_list

        # All descendant labels should have the new color
        child_labels = find_labels_recursive(label)
        assert len(child_labels) >= 1, "Expected at least one child Label"

        for child_label in child_labels:
            assert colors_equal(list(child_label.color), new_color_list), \
                f"Expected color {new_color_list}, got {list(child_label.color)}"

    @pytest.mark.parametrize('new_halign', ['left', 'center', 'right', 'justify'])
    def test_halign_change_preserves_widget_tree(self, new_halign):
        """Changing halign preserves widget tree structure (widget identities)."""
        # Create label with some content
        markdown = 'Paragraph text for alignment test.'
        label = MarkdownLabel(text=markdown, halign='left')

        # Collect widget ids before change
        ids_before = collect_widget_ids(label)

        # Change halign (style-only property)
        label.halign = new_halign

        # Collect widget ids after change
        ids_after = collect_widget_ids(label)

        # Widget tree structure should be preserved
        assert ids_before == ids_after, \
            "Widget tree changed after halign update"

    @pytest.mark.parametrize('new_halign', ['left', 'center', 'right', 'justify'])
    def test_halign_change_updates_descendant_labels(self, new_halign):
        """Changing halign updates all descendant Label widgets."""
        # Create label with some content
        markdown = '# Heading\n\nParagraph text.'
        label = MarkdownLabel(text=markdown, halign='left')

        # Change halign
        label.halign = new_halign

        # All descendant labels should have the new halign
        child_labels = find_labels_recursive(label)
        assert len(child_labels) >= 1, "Expected at least one child Label"

        for child_label in child_labels:
            assert child_label.halign == new_halign, \
                f"Expected halign {new_halign}, got {child_label.halign}"

    @pytest.mark.parametrize('new_valign', ['top', 'middle', 'bottom'])
    def test_valign_change_preserves_widget_tree(self, new_valign):
        """Changing valign preserves widget tree structure (widget identities)."""
        # Create label with some content
        markdown = 'Paragraph text for valign test.'
        label = MarkdownLabel(text=markdown, valign='top')

        # Collect widget ids before change
        ids_before = collect_widget_ids(label)

        # Change valign (style-only property)
        label.valign = new_valign

        # Collect widget ids after change
        ids_after = collect_widget_ids(label)

        # Widget tree structure should be preserved
        assert ids_before == ids_after, \
            "Widget tree changed after valign update"

    @pytest.mark.parametrize('new_valign', ['top', 'middle', 'bottom'])
    def test_valign_change_updates_descendant_labels(self, new_valign):
        """Changing valign updates all descendant Label widgets."""
        # Create label with some content
        markdown = '# Heading\n\nParagraph text.'
        label = MarkdownLabel(text=markdown, valign='top')

        # Change valign
        label.valign = new_valign

        # All descendant labels should have the new valign
        child_labels = find_labels_recursive(label)
        assert len(child_labels) >= 1, "Expected at least one child Label"

        for child_label in child_labels:
            assert child_label.valign == new_valign, \
                f"Expected valign {new_valign}, got {child_label.valign}"

    @pytest.mark.property
    @given(st.floats(min_value=0.5, max_value=3.0, allow_nan=False, allow_infinity=False))
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_line_height_change_preserves_widget_tree(self, new_line_height):
        """Changing line_height preserves widget tree structure (widget identities)."""
        # Create label with some content
        markdown = 'Paragraph text for line height test.'
        label = MarkdownLabel(text=markdown, line_height=1.0)

        # Collect widget ids before change
        ids_before = collect_widget_ids(label)

        # Change line_height (style-only property)
        label.line_height = new_line_height

        # Collect widget ids after change
        ids_after = collect_widget_ids(label)

        # Widget tree structure should be preserved
        assert ids_before == ids_after, \
            "Widget tree changed after line_height update"

    @pytest.mark.property
    @given(st.floats(min_value=0.5, max_value=3.0, allow_nan=False, allow_infinity=False))
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_line_height_change_updates_descendant_labels(self, new_line_height):
        """Changing line_height updates all descendant Label widgets."""
        # Create label with some content
        markdown = '# Heading\n\nParagraph text.'
        label = MarkdownLabel(text=markdown, line_height=1.0)

        # Change line_height
        label.line_height = new_line_height

        # All descendant labels should have the new line_height
        child_labels = find_labels_recursive(label)
        assert len(child_labels) >= 1, "Expected at least one child Label"

        for child_label in child_labels:
            assert floats_equal(child_label.line_height, new_line_height), \
                f"Expected line_height {new_line_height}, got {child_label.line_height}"

    @pytest.mark.property
    @given(st.booleans())
    # Boolean strategy: 2 examples (True/False coverage)
    @settings(max_examples=2, deadline=None)
    def test_disabled_change_preserves_widget_tree(self, new_disabled):
        """Changing disabled preserves widget tree structure (widget identities)."""
        # Create label with some content
        markdown = 'Paragraph text for disabled test.'
        label = MarkdownLabel(text=markdown, disabled=False)

        # Collect widget ids before change
        ids_before = collect_widget_ids(label)

        # Change disabled (style-only property)
        label.disabled = new_disabled

        # Collect widget ids after change
        ids_after = collect_widget_ids(label)

        # Widget tree structure should be preserved
        assert ids_before == ids_after, \
            "Widget tree changed after disabled update"

    def test_text_structure_property_rebuilds_tree(self):
        """Changing text (structure property) rebuilds the widget tree."""
        # Create label with some content
        markdown1 = 'First paragraph.'
        label = MarkdownLabel(text=markdown1)

        # Collect widget ids before change
        ids_before = collect_widget_ids(label, exclude_root=True)

        # Change text (structure property) - use force_rebuild() for immediate
        # update since text changes now use deferred rebuilds
        label.text = 'Second paragraph with different content.'
        label.force_rebuild()

        # Collect widget ids after change
        ids_after = collect_widget_ids(label, exclude_root=True)

        # Widget tree should be rebuilt (different widget objects)
        assert ids_before != ids_after, \
            "Widget tree should be rebuilt after text change"

    def test_font_name_structure_property_rebuilds_tree(self):
        """Changing font_name (structure property) rebuilds the widget tree."""
        # Create label with some content
        markdown = 'Paragraph text.'
        label = MarkdownLabel(text=markdown, font_name='Roboto')

        # Collect widget ids before change
        ids_before = collect_widget_ids(label, exclude_root=True)

        # Change font_name (structure property)
        label.font_name = 'RobotoMono-Regular'
        label.force_rebuild()  # Force immediate rebuild for test

        # Collect widget ids after change
        ids_after = collect_widget_ids(label, exclude_root=True)

        # Widget tree should be rebuilt (different widget objects)
        assert ids_before != ids_after, \
            "Widget tree should be rebuilt after font_name change"

    @pytest.mark.property
    @given(
        st_font_size(min_value=10, max_value=30),
        st_rgba_color(),
        st.sampled_from(['left', 'center', 'right']),
        st.sampled_from(['top', 'middle', 'bottom']),
        st.floats(min_value=0.8, max_value=2.0, allow_nan=False, allow_infinity=False)
    )
    # Mixed finite/complex strategy: 27 examples (9 finite combinations × 3 complex samples)
    @settings(max_examples=27, deadline=None)
    def test_multiple_style_changes_preserve_widget_tree(self, font_size, color,
                                                          halign, valign, line_height):
        """Multiple style-only property changes preserve widget tree structure."""
        # Create label with some content
        markdown = '# Heading\n\nParagraph text here.'
        label = MarkdownLabel(text=markdown)

        # Collect widget ids before changes
        ids_before = collect_widget_ids(label)

        # Apply multiple style changes
        label.font_size = font_size
        label.color = list(color)
        label.halign = halign
        label.valign = valign
        label.line_height = line_height

        # Collect widget ids after changes
        ids_after = collect_widget_ids(label)

        # Widget tree structure should be preserved through all changes
        assert ids_before == ids_after, \
            "Widget tree changed after multiple style updates"

    @pytest.mark.property
    @given(
        st_rgba_color(),
        st_rgba_color()
    )
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_disabled_color_switching(self, normal_color, disabled_color):
        """Disabled state correctly switches between color and disabled_color."""
        # Create label with some content
        markdown = 'Paragraph text.'
        label = MarkdownLabel(
            text=markdown,
            color=list(normal_color),
            disabled_color=list(disabled_color),
            disabled=False
        )

        # Get child labels
        child_labels = find_labels_recursive(label)
        assert len(child_labels) >= 1, "Expected at least one child Label"

        # Initially should use normal color
        for child_label in child_labels:
            assert colors_equal(list(child_label.color), list(normal_color)), \
                f"Expected normal color {list(normal_color)}, got {list(child_label.color)}"

        # Enable disabled state
        label.disabled = True

        # Should now use disabled_color
        for child_label in child_labels:
            assert colors_equal(list(child_label.color), list(disabled_color)), \
                f"Expected disabled color {list(disabled_color)}, got {list(child_label.color)}"

        # Disable disabled state
        label.disabled = False

        # Should return to normal color
        for child_label in child_labels:
            assert colors_equal(list(child_label.color), list(normal_color)), \
                f"Expected normal color {list(normal_color)}, got {list(child_label.color)}"
