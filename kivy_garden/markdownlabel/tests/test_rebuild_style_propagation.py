"""
Style property value propagation tests for MarkdownLabel.

This module contains tests that verify style property values are correctly
propagated to all descendant Label widgets after property changes.

Tests are designed to run in headless CI environments without requiring a Kivy window.
"""

import pytest
from hypothesis import given, strategies as st, settings, assume

from kivy_garden.markdownlabel import MarkdownLabel
from .test_utils import (
    simple_markdown_document,
    find_labels_recursive,
    colors_equal,
    floats_equal,
    st_rgba_color,
    collect_widget_ids,
    assert_no_rebuild
)


@pytest.mark.unit
class TestStylePropertyPropagation:
    """Tests for style property value propagation to descendant Labels.

    These tests verify that style property values are correctly propagated
    to all descendant Label widgets after property changes.

    """

    def test_color_propagates_to_descendants(self):
        """Color value propagates to all descendant Labels."""
        label = MarkdownLabel(text='# Heading\n\nParagraph text', color=[1, 1, 1, 1])
        ids_before = collect_widget_ids(label, exclude_root=True)

        # Change color
        new_color = [0.5, 0.5, 0.5, 1]
        label.color = new_color

        # Verify no rebuild occurred
        assert_no_rebuild(label, ids_before)

        # Verify all descendant Labels have the new color
        child_labels = find_labels_recursive(label)
        assert len(child_labels) >= 1, "Expected at least one child Label"

        for child_label in child_labels:
            assert colors_equal(list(child_label.color), new_color), \
                f"Expected color {new_color}, got {list(child_label.color)}"

    def test_halign_propagates_to_descendants(self):
        """Halign value propagates to all descendant Labels."""
        label = MarkdownLabel(text='# Heading\n\nParagraph text', halign='left')
        ids_before = collect_widget_ids(label, exclude_root=True)

        # Change halign
        new_halign = 'center'
        label.halign = new_halign

        # Verify no rebuild occurred
        assert_no_rebuild(label, ids_before)

        # Verify all descendant Labels have the new halign
        child_labels = find_labels_recursive(label)
        assert len(child_labels) >= 1, "Expected at least one child Label"

        for child_label in child_labels:
            assert child_label.halign == new_halign, \
                f"Expected halign {new_halign}, got {child_label.halign}"

    def test_valign_propagates_to_descendants(self):
        """Valign value propagates to all descendant Labels."""
        label = MarkdownLabel(text='# Heading\n\nParagraph text', valign='bottom')
        ids_before = collect_widget_ids(label, exclude_root=True)

        # Change valign
        new_valign = 'top'
        label.valign = new_valign

        # Verify no rebuild occurred
        assert_no_rebuild(label, ids_before)

        # Verify all descendant Labels have the new valign
        child_labels = find_labels_recursive(label)
        assert len(child_labels) >= 1, "Expected at least one child Label"

        for child_label in child_labels:
            assert child_label.valign == new_valign, \
                f"Expected valign {new_valign}, got {child_label.valign}"

    def test_line_height_propagates_to_descendants(self):
        """Line_height value propagates to all descendant Labels."""
        label = MarkdownLabel(text='# Heading\n\nParagraph text', line_height=1.0)
        ids_before = collect_widget_ids(label, exclude_root=True)

        # Change line_height
        new_line_height = 1.5
        label.line_height = new_line_height

        # Verify no rebuild occurred
        assert_no_rebuild(label, ids_before)

        # Verify all descendant Labels have the new line_height
        child_labels = find_labels_recursive(label)
        assert len(child_labels) >= 1, "Expected at least one child Label"

        for child_label in child_labels:
            assert floats_equal(child_label.line_height, new_line_height), \
                f"Expected line_height {new_line_height}, got {child_label.line_height}"

    def test_disabled_color_propagates_when_disabled(self):
        """Disabled_color propagates to descendants when disabled is True."""
        label = MarkdownLabel(
            text='# Heading\n\nParagraph text',
            color=[1, 1, 1, 1],
            disabled_color=[0.5, 0.5, 0.5, 0.5],
            disabled=False
        )
        ids_before = collect_widget_ids(label, exclude_root=True)

        # Enable disabled state
        label.disabled = True

        # Verify no rebuild occurred
        assert_no_rebuild(label, ids_before)

        # Verify all descendant Labels have the disabled_color
        child_labels = find_labels_recursive(label)
        assert len(child_labels) >= 1, "Expected at least one child Label"

        expected_color = [0.5, 0.5, 0.5, 0.5]
        for child_label in child_labels:
            assert colors_equal(list(child_label.color), expected_color), \
                f"Expected disabled_color {expected_color}, got {list(child_label.color)}"

    def test_base_direction_propagates_to_descendants(self):
        """Base_direction value propagates to all descendant Labels."""
        label = MarkdownLabel(text='# Heading\n\nParagraph text', base_direction=None)
        ids_before = collect_widget_ids(label, exclude_root=True)

        # Change base_direction
        new_base_direction = 'rtl'
        label.base_direction = new_base_direction

        # Verify no rebuild occurred
        assert_no_rebuild(label, ids_before)

        # Verify all descendant Labels have the new base_direction
        child_labels = find_labels_recursive(label)
        assert len(child_labels) >= 1, "Expected at least one child Label"

        for child_label in child_labels:
            assert child_label.base_direction == new_base_direction, \
                f"Expected base_direction {new_base_direction}, got {child_label.base_direction}"


@pytest.mark.property
@pytest.mark.slow
class TestStylePropertyPropagationPBT:
    """Property-based tests for style property propagation to descendants."""

    @given(
        markdown_text=simple_markdown_document(),
        color=st_rgba_color(),
        halign=st.sampled_from(['left', 'center', 'right', 'justify']),
        valign=st.sampled_from(['bottom', 'middle', 'top']),
        line_height=st.floats(min_value=0.5, max_value=3.0, allow_nan=False,
                               allow_infinity=False),
        base_direction=st.sampled_from([None, 'ltr', 'rtl', 'weak_ltr', 'weak_rtl'])
    )
    # Mixed finite/complex strategy: 50 examples (60 finite × 3 complex samples)
    @settings(max_examples=50, deadline=None)
    def test_style_property_values_propagate_to_descendants(
        self, markdown_text, color, halign, valign, line_height, base_direction
    ):
        """Style Property Values Propagate to Descendants.

        *For any* MarkdownLabel with non-empty content, and *for any* style-only
        property value, all descendant Label widgets SHALL have that property
        value after the change.
        """
        # Ensure we have non-empty content
        assume(markdown_text and markdown_text.strip())

        # Create MarkdownLabel with initial content
        label = MarkdownLabel(text=markdown_text)

        # Ensure we have children to test
        child_labels = find_labels_recursive(label)
        assume(len(child_labels) >= 1)

        # Capture IDs before
        ids_before = collect_widget_ids(label, exclude_root=True)

        # Apply style property changes
        color_list = list(color)
        label.color = color_list
        label.halign = halign
        label.valign = valign
        label.base_direction = base_direction
        label.line_height = line_height

        # Verify no rebuild occurred
        assert_no_rebuild(label, ids_before)

        # Verify all descendant Labels have the new property values
        child_labels = find_labels_recursive(label)

        for child_label in child_labels:
            # Check color
            assert colors_equal(list(child_label.color), color_list), (
                f"Color not propagated. Expected {color_list}, "
                f"got {list(child_label.color)}"
            )

            # Check halign
            assert child_label.halign == halign, (
                f"Halign not propagated. Expected {halign}, "
                f"got {child_label.halign}"
            )

            # Check valign
            assert child_label.valign == valign, (
                f"Valign not propagated. Expected {valign}, "
                f"got {child_label.valign}"
            )

            # Check line_height
            assert floats_equal(child_label.line_height, line_height), (
                f"Line_height not propagated. Expected {line_height}, "
                f"got {child_label.line_height}"
            )

            # Check base_direction
            assert child_label.base_direction == base_direction, (
                f"Base_direction not propagated. Expected {base_direction}, "
                f"got {child_label.base_direction}"
            )
