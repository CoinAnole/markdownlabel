"""
Widget identity preservation and rebuild semantics tests for MarkdownLabel.

This module contains tests that verify widget identity preservation for style-only
property changes and widget tree rebuilding for structure property changes.
These tests are designed to run in headless CI environments without requiring
a Kivy window.

"""

import pytest
from hypothesis import given, strategies as st, settings, assume

from kivy.uix.label import Label

from kivy_garden.markdownlabel import MarkdownLabel
from .test_utils import (
    simple_markdown_document,
    find_labels_recursive,
    colors_equal,
    floats_equal,
    collect_widget_ids,
    st_font_size,
    st_font_name,
    st_rgba_color
)


# Style Properties for Testing
# These are properties that should preserve widget identities when changed
STYLE_ONLY_PROPERTIES = [
    'color',
    'halign',
    'valign',
    'line_height',
    'disabled',
    'disabled_color',
    'base_direction',
    'outline_color',
    'disabled_outline_color',
    'mipmap',
    'text_language',
    'limit_render_to_text_bbox',
]

# Structure Properties for Testing
# These are properties that should trigger a widget tree rebuild when changed
STRUCTURE_PROPERTIES = [
    'text',
    'font_name',
    'text_size',
    'link_style',
    'strict_label_mode',
    'render_mode',
]


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
    # Mixed finite/complex strategy: 50 examples (120 finite combinations with 5 complex strategies)
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


class TestStylePropertyPropagation:
    """Tests for style property value propagation to descendant Labels.

    These tests verify that style property values are correctly propagated
    to all descendant Label widgets after property changes.

    """

    def test_color_propagates_to_descendants(self):
        """Color value propagates to all descendant Labels."""
        label = MarkdownLabel(text='# Heading\n\nParagraph text', color=[1, 1, 1, 1])

        # Change color
        new_color = [0.5, 0.5, 0.5, 1]
        label.color = new_color

        # Verify all descendant Labels have the new color
        child_labels = find_labels_recursive(label)
        assert len(child_labels) >= 1, "Expected at least one child Label"

        for child_label in child_labels:
            assert colors_equal(list(child_label.color), new_color), \
                f"Expected color {new_color}, got {list(child_label.color)}"

    def test_halign_propagates_to_descendants(self):
        """Halign value propagates to all descendant Labels."""
        label = MarkdownLabel(text='# Heading\n\nParagraph text', halign='left')

        # Change halign
        new_halign = 'center'
        label.halign = new_halign

        # Verify all descendant Labels have the new halign
        child_labels = find_labels_recursive(label)
        assert len(child_labels) >= 1, "Expected at least one child Label"

        for child_label in child_labels:
            assert child_label.halign == new_halign, \
                f"Expected halign {new_halign}, got {child_label.halign}"

    def test_valign_propagates_to_descendants(self):
        """Valign value propagates to all descendant Labels."""
        label = MarkdownLabel(text='# Heading\n\nParagraph text', valign='bottom')

        # Change valign
        new_valign = 'top'
        label.valign = new_valign

        # Verify all descendant Labels have the new valign
        child_labels = find_labels_recursive(label)
        assert len(child_labels) >= 1, "Expected at least one child Label"

        for child_label in child_labels:
            assert child_label.valign == new_valign, \
                f"Expected valign {new_valign}, got {child_label.valign}"

    def test_line_height_propagates_to_descendants(self):
        """Line_height value propagates to all descendant Labels."""
        label = MarkdownLabel(text='# Heading\n\nParagraph text', line_height=1.0)

        # Change line_height
        new_line_height = 1.5
        label.line_height = new_line_height

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

        # Enable disabled state
        label.disabled = True

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

        # Change base_direction
        new_base_direction = 'rtl'
        label.base_direction = new_base_direction

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
    # Mixed finite/complex strategy: 50 examples (60 finite combinations with 3 complex strategies)
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

        # Apply style property changes
        color_list = list(color)
        label.color = color_list
        label.halign = halign
        label.valign = valign
        label.line_height = line_height
        label.base_direction = base_direction

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


class TestStructurePropertyRebuild:
    """Tests for structure property changes rebuilding the widget tree.

    These tests verify that changing structure properties (text, font_name,
    text_size, link_style, strict_label_mode, render_mode) rebuilds the widget
    tree with new widget instances, while the root MarkdownLabel ID remains
    unchanged.

    """

    def test_text_change_triggers_rebuild(self):
        """Changing text triggers widget rebuild with new widget instances."""
        label = MarkdownLabel(text='# Initial Heading\n\nInitial paragraph')
        root_id_before = id(label)

        # Capture children widget IDs before change
        children_ids_before = collect_widget_ids(label, exclude_root=True)

        # Apply property change and force_rebuild()
        label.text = '# New Heading\n\nNew paragraph with different content'
        label.force_rebuild()

        # Capture children widget IDs after change
        children_ids_after = collect_widget_ids(label, exclude_root=True)

        # Assert children widget IDs differ
        assert children_ids_before != children_ids_after, \
            "Children widget IDs should differ after text change"

        # Assert root MarkdownLabel ID unchanged
        assert id(label) == root_id_before, \
            "Root MarkdownLabel ID should remain unchanged"

    def test_font_name_change_preserves_widget_tree(self):
        """Changing font_name preserves widget tree (style-only property)."""
        label = MarkdownLabel(text='# Heading\n\nParagraph', font_name='Roboto')
        root_id_before = id(label)

        # Capture children widget IDs before change
        children_ids_before = collect_widget_ids(label, exclude_root=True)

        # Apply property change (style-only, no rebuild needed)
        label.font_name = 'RobotoMono-Regular'

        # Capture children widget IDs after change
        children_ids_after = collect_widget_ids(label, exclude_root=True)

        # Assert children widget IDs are preserved (no rebuild)
        assert children_ids_before == children_ids_after, \
            "Children widget IDs should be preserved for font_name change (style-only)"

        # Assert root MarkdownLabel ID unchanged
        assert id(label) == root_id_before, \
            "Root MarkdownLabel ID should remain unchanged"

        # Verify font_name was actually applied to child Labels
        labels = find_labels_recursive(label)
        for lbl in labels:
            # Code labels keep their code_font_name, others get the new font_name
            if not (hasattr(lbl, '_is_code') and lbl._is_code):
                assert lbl.font_name == 'RobotoMono-Regular', \
                    f"Expected font_name='RobotoMono-Regular', got '{lbl.font_name}'"

    def test_text_size_change_triggers_rebuild(self):
        """Changing text_size triggers widget rebuild with new widget instances."""
        label = MarkdownLabel(text='# Heading\n\nParagraph', text_size=[None, None])
        root_id_before = id(label)

        # Capture children widget IDs before change
        children_ids_before = collect_widget_ids(label, exclude_root=True)

        # Apply property change and force_rebuild()
        label.text_size = [200, None]
        label.force_rebuild()

        # Capture children widget IDs after change
        children_ids_after = collect_widget_ids(label, exclude_root=True)

        # Assert children widget IDs differ
        assert children_ids_before != children_ids_after, \
            "Children widget IDs should differ after text_size change"

        # Assert root MarkdownLabel ID unchanged
        assert id(label) == root_id_before, \
            "Root MarkdownLabel ID should remain unchanged"

    def test_link_style_change_triggers_rebuild(self):
        """Changing link_style triggers widget rebuild with new widget instances."""
        label = MarkdownLabel(
            text='# Heading\n\n[Link](http://example.com)',
            link_style='unstyled'
        )
        root_id_before = id(label)

        # Capture children widget IDs before change
        children_ids_before = collect_widget_ids(label, exclude_root=True)

        # Apply property change and force_rebuild()
        label.link_style = 'styled'
        label.force_rebuild()

        # Capture children widget IDs after change
        children_ids_after = collect_widget_ids(label, exclude_root=True)

        # Assert children widget IDs differ
        assert children_ids_before != children_ids_after, \
            "Children widget IDs should differ after link_style change"

        # Assert root MarkdownLabel ID unchanged
        assert id(label) == root_id_before, \
            "Root MarkdownLabel ID should remain unchanged"

    def test_strict_label_mode_change_triggers_rebuild(self):
        """Changing strict_label_mode triggers widget rebuild."""
        label = MarkdownLabel(text='# Heading\n\nParagraph', strict_label_mode=False)
        root_id_before = id(label)

        # Capture children widget IDs before change
        children_ids_before = collect_widget_ids(label, exclude_root=True)

        # Apply property change and force_rebuild()
        label.strict_label_mode = True
        label.force_rebuild()

        # Capture children widget IDs after change
        children_ids_after = collect_widget_ids(label, exclude_root=True)

        # Assert children widget IDs differ
        assert children_ids_before != children_ids_after, \
            "Children widget IDs should differ after strict_label_mode change"

        # Assert root MarkdownLabel ID unchanged
        assert id(label) == root_id_before, \
            "Root MarkdownLabel ID should remain unchanged"

    def test_render_mode_change_triggers_rebuild(self):
        """Changing render_mode triggers widget rebuild."""
        label = MarkdownLabel(text='# Heading\n\nParagraph', render_mode='widgets')
        root_id_before = id(label)

        # Capture children widget IDs before change
        children_ids_before = collect_widget_ids(label, exclude_root=True)

        # Apply property change and force_rebuild()
        label.render_mode = 'auto'
        label.force_rebuild()

        # Capture children widget IDs after change
        children_ids_after = collect_widget_ids(label, exclude_root=True)

        # Assert children widget IDs differ
        assert children_ids_before != children_ids_after, \
            "Children widget IDs should differ after render_mode change"

        # Assert root MarkdownLabel ID unchanged
        assert id(label) == root_id_before, \
            "Root MarkdownLabel ID should remain unchanged"


@pytest.mark.property
@pytest.mark.slow
class TestStructurePropertyRebuildPBT:
    """Property-based tests for structure property rebuild behavior."""

    @given(
        initial_text=simple_markdown_document(),
        new_text=simple_markdown_document()
    )
    # Mixed finite/complex strategy: 50 examples (complex samples)
    @settings(max_examples=50, deadline=None)
    def test_text_change_triggers_rebuild_pbt(self, initial_text, new_text):
        """Structure Property Changes Trigger Rebuild (text).

        *For any* MarkdownLabel with non-empty content, and *for any* structure
        property (text), changing that property and calling force_rebuild()
        SHALL result in different widget object IDs for children (excluding
        the root MarkdownLabel).
        """
        # Ensure we have different non-empty content
        assume(initial_text and initial_text.strip())
        assume(new_text and new_text.strip())
        assume(initial_text != new_text)

        # Create MarkdownLabel with initial content
        label = MarkdownLabel(text=initial_text)

        # Ensure we have children to test
        assume(len(label.children) > 0)

        # Capture children widget IDs before change
        children_ids_before = collect_widget_ids(label, exclude_root=True)
        assume(len(children_ids_before) > 0)

        # Apply property change and force_rebuild()
        label.text = new_text
        label.force_rebuild()

        # Capture children widget IDs after change
        children_ids_after = collect_widget_ids(label, exclude_root=True)

        # Assert: children widget IDs should differ
        assert children_ids_before != children_ids_after, (
            f"Children widget IDs should differ after text change. "
            f"Before: {len(children_ids_before)} widgets, "
            f"After: {len(children_ids_after)} widgets"
        )

    @given(
        markdown_text=simple_markdown_document(),
        font_name=st_font_name()
    )
    # Mixed finite/complex strategy: 15 examples (3 finite × 5 complex samples)
    @settings(max_examples=15, deadline=None)
    def test_font_name_change_preserves_widget_tree_pbt(self, markdown_text, font_name):
        """
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

        # Capture children widget IDs before change
        children_ids_before = collect_widget_ids(label, exclude_root=True)
        assume(len(children_ids_before) > 0)

        # Apply property change (style-only, no force_rebuild needed)
        label.font_name = font_name

        # Capture children widget IDs after change
        children_ids_after = collect_widget_ids(label, exclude_root=True)

        # Assert: children widget IDs should be preserved (style-only property)
        assert children_ids_before == children_ids_after, (
            f"Children widget IDs should be preserved for font_name change (style-only). "
            f"Before: {len(children_ids_before)} widgets, "
            f"After: {len(children_ids_after)} widgets"
        )

        # Verify font_name was actually applied
        labels = find_labels_recursive(label)
        for lbl in labels:
            if not (hasattr(lbl, '_is_code') and lbl._is_code):
                assert lbl.font_name == font_name, \
                    f"Expected font_name='{font_name}', got '{lbl.font_name}'"

    @given(
        markdown_text=simple_markdown_document(),
        link_style=st.sampled_from(['unstyled', 'styled'])
    )
    # Mixed finite/complex strategy: 10 examples (2 finite × 5 complex samples)
    @settings(max_examples=10, deadline=None)
    def test_link_style_change_triggers_rebuild_pbt(self, markdown_text, link_style):
        """
        *For any* MarkdownLabel with non-empty content, and *for any* structure
        property (link_style), changing that property and calling force_rebuild()
        SHALL result in different widget object IDs for children.
        """
        # Ensure we have non-empty content
        assume(markdown_text and markdown_text.strip())

        # Use a different initial link_style
        initial_style = 'unstyled' if link_style != 'unstyled' else 'styled'

        # Create MarkdownLabel with initial content
        label = MarkdownLabel(text=markdown_text, link_style=initial_style)

        # Ensure we have children to test
        assume(len(label.children) > 0)

        # Capture children widget IDs before change
        children_ids_before = collect_widget_ids(label, exclude_root=True)
        assume(len(children_ids_before) > 0)

        # Apply property change and force_rebuild()
        label.link_style = link_style
        label.force_rebuild()

        # Capture children widget IDs after change
        children_ids_after = collect_widget_ids(label, exclude_root=True)

        # Assert: children widget IDs should differ
        assert children_ids_before != children_ids_after, (
            f"Children widget IDs should differ after link_style change. "
            f"Before: {len(children_ids_before)} widgets, "
            f"After: {len(children_ids_after)} widgets"
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
    # Mixed finite/complex strategy: 50 examples (24 finite combinations with 4 complex strategies)
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
    # Mixed finite/complex strategy: 48 examples (24 finite combinations × 2 complex samples)
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


# =============================================================================
# Advanced Font Properties Widget Identity Preservation Tests
# =============================================================================
# These tests validate Property 1 from the design document:
# "Style-only property updates preserve widget identity"
# Specifically for the newly reclassified advanced font properties:
# font_family, font_context, font_features, font_hinting, font_kerning, font_blended
# =============================================================================


@pytest.mark.property
@pytest.mark.slow
class TestAdvancedFontPropertyIdentityPreservationPBT:
    """Property-based tests for advanced font property identity preservation.

    These tests verify that changing advanced font properties (font_family,
    font_context, font_features, font_hinting, font_kerning, font_blended)
    preserves all widget object IDs in the subtree.

    **Property 1: Style-only property updates preserve widget identity**
    **Validates: Requirements 1.1-1.7**
    """

    @given(
        markdown_text=simple_markdown_document(),
        font_family=st.one_of(st.none(), st.text(min_size=1, max_size=30, alphabet=st.characters(
            whitelist_categories=['L', 'N'],
            blacklist_characters='[]&\n\r'
        ))),
        font_context=st.one_of(st.none(), st.text(min_size=1, max_size=30, alphabet=st.characters(
            whitelist_categories=['L', 'N'],
            blacklist_characters='[]&\n\r'
        ))),
        font_features=st.text(min_size=0, max_size=30, alphabet=st.characters(
            whitelist_categories=['L', 'N', 'P'],
            blacklist_characters='[]&\n\r'
        )),
        font_hinting=st.sampled_from([None, 'normal', 'light', 'mono']),
        font_kerning=st.booleans(),
        font_blended=st.booleans()
    )
    # Feature: optimize-rebuild-contract, Property 1: Style-only property updates preserve widget identity
    # Mixed finite/complex strategy: 50 examples (8 finite combinations with 3 complex strategies)
    @settings(max_examples=50, deadline=None)
    def test_advanced_font_properties_preserve_widget_identity(
        self, markdown_text, font_family, font_context, font_features,
        font_hinting, font_kerning, font_blended
    ):
        """Advanced Font Properties Preserve Widget Identity.

        *For any* MarkdownLabel with non-empty content, and *for any* advanced
        font property (font_family, font_context, font_features, font_hinting,
        font_kerning, font_blended), changing that property SHALL preserve all
        widget object IDs in the subtree (the set of IDs before equals the set
        of IDs after).

        **Validates: Requirements 1.1-1.7**
        """
        # Ensure we have non-empty content
        assume(markdown_text and markdown_text.strip())

        # Create MarkdownLabel with initial content
        label = MarkdownLabel(text=markdown_text)

        # Ensure we have children to test
        assume(len(label.children) > 0)

        # Capture widget IDs before changes
        ids_before = collect_widget_ids(label)

        # Apply all advanced font property changes
        label.font_family = font_family
        label.font_context = font_context
        label.font_features = font_features
        label.font_hinting = font_hinting
        label.font_kerning = font_kerning
        label.font_blended = font_blended

        # Capture widget IDs after changes
        ids_after = collect_widget_ids(label)

        # Assert: widget IDs should be unchanged
        assert ids_before == ids_after, (
            f"Widget IDs changed after advanced font property updates. "
            f"Before: {len(ids_before)} widgets, After: {len(ids_after)} widgets"
        )

    @given(
        markdown_text=simple_markdown_document(),
        font_hinting=st.sampled_from([None, 'normal', 'light', 'mono'])
    )
    # Feature: optimize-rebuild-contract, Property 1: Style-only property updates preserve widget identity
    # Finite strategy: 4 font_hinting options × complex markdown
    @settings(max_examples=20, deadline=None)
    def test_font_hinting_preserves_widget_identity(self, markdown_text, font_hinting):
        """Font Hinting Preserves Widget Identity.

        *For any* MarkdownLabel with non-empty content, and *for any* font_hinting
        value (None, 'normal', 'light', 'mono'), changing font_hinting SHALL
        preserve all widget object IDs.

        **Validates: Requirements 1.4, 1.7**
        """
        # Ensure we have non-empty content
        assume(markdown_text and markdown_text.strip())

        # Create MarkdownLabel with initial content
        label = MarkdownLabel(text=markdown_text)

        # Ensure we have children to test
        assume(len(label.children) > 0)

        # Capture widget IDs before change
        ids_before = collect_widget_ids(label)

        # Apply font_hinting change
        label.font_hinting = font_hinting

        # Capture widget IDs after change
        ids_after = collect_widget_ids(label)

        # Assert: widget IDs should be unchanged
        assert ids_before == ids_after, (
            f"Widget IDs changed after font_hinting update to {font_hinting}. "
            f"Before: {len(ids_before)} widgets, After: {len(ids_after)} widgets"
        )

    @given(
        markdown_text=simple_markdown_document(),
        font_kerning=st.booleans()
    )
    # Feature: optimize-rebuild-contract, Property 1: Style-only property updates preserve widget identity
    # Finite strategy: 2 boolean options × complex markdown
    @settings(max_examples=20, deadline=None)
    def test_font_kerning_preserves_widget_identity(self, markdown_text, font_kerning):
        """Font Kerning Preserves Widget Identity.

        *For any* MarkdownLabel with non-empty content, and *for any* font_kerning
        value (True/False), changing font_kerning SHALL preserve all widget
        object IDs.

        **Validates: Requirements 1.5, 1.7**
        """
        # Ensure we have non-empty content
        assume(markdown_text and markdown_text.strip())

        # Create MarkdownLabel with initial content
        label = MarkdownLabel(text=markdown_text)

        # Ensure we have children to test
        assume(len(label.children) > 0)

        # Capture widget IDs before change
        ids_before = collect_widget_ids(label)

        # Apply font_kerning change
        label.font_kerning = font_kerning

        # Capture widget IDs after change
        ids_after = collect_widget_ids(label)

        # Assert: widget IDs should be unchanged
        assert ids_before == ids_after, (
            f"Widget IDs changed after font_kerning update to {font_kerning}. "
            f"Before: {len(ids_before)} widgets, After: {len(ids_after)} widgets"
        )

    @given(
        markdown_text=simple_markdown_document(),
        font_blended=st.booleans()
    )
    # Feature: optimize-rebuild-contract, Property 1: Style-only property updates preserve widget identity
    # Finite strategy: 2 boolean options × complex markdown
    @settings(max_examples=20, deadline=None)
    def test_font_blended_preserves_widget_identity(self, markdown_text, font_blended):
        """Font Blended Preserves Widget Identity.

        *For any* MarkdownLabel with non-empty content, and *for any* font_blended
        value (True/False), changing font_blended SHALL preserve all widget
        object IDs.

        **Validates: Requirements 1.6, 1.7**
        """
        # Ensure we have non-empty content
        assume(markdown_text and markdown_text.strip())

        # Create MarkdownLabel with initial content
        label = MarkdownLabel(text=markdown_text)

        # Ensure we have children to test
        assume(len(label.children) > 0)

        # Capture widget IDs before change
        ids_before = collect_widget_ids(label)

        # Apply font_blended change
        label.font_blended = font_blended

        # Capture widget IDs after change
        ids_after = collect_widget_ids(label)

        # Assert: widget IDs should be unchanged
        assert ids_before == ids_after, (
            f"Widget IDs changed after font_blended update to {font_blended}. "
            f"Before: {len(ids_before)} widgets, After: {len(ids_after)} widgets"
        )

    @given(
        markdown_text=simple_markdown_document(),
        font_family=st.one_of(st.none(), st.text(min_size=1, max_size=30, alphabet=st.characters(
            whitelist_categories=['L', 'N'],
            blacklist_characters='[]&\n\r'
        )))
    )
    # Feature: optimize-rebuild-contract, Property 1: Style-only property updates preserve widget identity
    # Complex strategy: font_family can be None or text
    @settings(max_examples=30, deadline=None)
    def test_font_family_preserves_widget_identity(self, markdown_text, font_family):
        """Font Family Preserves Widget Identity.

        *For any* MarkdownLabel with non-empty content, and *for any* font_family
        value (None or string), changing font_family SHALL preserve all widget
        object IDs.

        **Validates: Requirements 1.1, 1.7**
        """
        # Ensure we have non-empty content
        assume(markdown_text and markdown_text.strip())

        # Create MarkdownLabel with initial content
        label = MarkdownLabel(text=markdown_text)

        # Ensure we have children to test
        assume(len(label.children) > 0)

        # Capture widget IDs before change
        ids_before = collect_widget_ids(label)

        # Apply font_family change
        label.font_family = font_family

        # Capture widget IDs after change
        ids_after = collect_widget_ids(label)

        # Assert: widget IDs should be unchanged
        assert ids_before == ids_after, (
            f"Widget IDs changed after font_family update to {font_family}. "
            f"Before: {len(ids_before)} widgets, After: {len(ids_after)} widgets"
        )

    @given(
        markdown_text=simple_markdown_document(),
        font_context=st.one_of(st.none(), st.text(min_size=1, max_size=30, alphabet=st.characters(
            whitelist_categories=['L', 'N'],
            blacklist_characters='[]&\n\r'
        )))
    )
    # Feature: optimize-rebuild-contract, Property 1: Style-only property updates preserve widget identity
    # Complex strategy: font_context can be None or text
    @settings(max_examples=30, deadline=None)
    def test_font_context_preserves_widget_identity(self, markdown_text, font_context):
        """Font Context Preserves Widget Identity.

        *For any* MarkdownLabel with non-empty content, and *for any* font_context
        value (None or string), changing font_context SHALL preserve all widget
        object IDs.

        **Validates: Requirements 1.2, 1.7**
        """
        # Ensure we have non-empty content
        assume(markdown_text and markdown_text.strip())

        # Create MarkdownLabel with initial content
        label = MarkdownLabel(text=markdown_text)

        # Ensure we have children to test
        assume(len(label.children) > 0)

        # Capture widget IDs before change
        ids_before = collect_widget_ids(label)

        # Apply font_context change
        label.font_context = font_context

        # Capture widget IDs after change
        ids_after = collect_widget_ids(label)

        # Assert: widget IDs should be unchanged
        assert ids_before == ids_after, (
            f"Widget IDs changed after font_context update to {font_context}. "
            f"Before: {len(ids_before)} widgets, After: {len(ids_after)} widgets"
        )

    @given(
        markdown_text=simple_markdown_document(),
        font_features=st.text(min_size=0, max_size=30, alphabet=st.characters(
            whitelist_categories=['L', 'N', 'P'],
            blacklist_characters='[]&\n\r'
        ))
    )
    # Feature: optimize-rebuild-contract, Property 1: Style-only property updates preserve widget identity
    # Complex strategy: font_features is a text string
    @settings(max_examples=30, deadline=None)
    def test_font_features_preserves_widget_identity(self, markdown_text, font_features):
        """Font Features Preserves Widget Identity.

        *For any* MarkdownLabel with non-empty content, and *for any* font_features
        value (string), changing font_features SHALL preserve all widget
        object IDs.

        **Validates: Requirements 1.3, 1.7**
        """
        # Ensure we have non-empty content
        assume(markdown_text and markdown_text.strip())

        # Create MarkdownLabel with initial content
        label = MarkdownLabel(text=markdown_text)

        # Ensure we have children to test
        assume(len(label.children) > 0)

        # Capture widget IDs before change
        ids_before = collect_widget_ids(label)

        # Apply font_features change
        label.font_features = font_features

        # Capture widget IDs after change
        ids_after = collect_widget_ids(label)

        # Assert: widget IDs should be unchanged
        assert ids_before == ids_after, (
            f"Widget IDs changed after font_features update to '{font_features}'. "
            f"Before: {len(ids_before)} widgets, After: {len(ids_after)} widgets"
        )


# =============================================================================
# Text Processing Properties Widget Identity Preservation Tests
# =============================================================================
# These tests validate Property 1 from the design document:
# "Style-only property updates preserve widget identity"
# Specifically for the newly reclassified text processing properties:
# unicode_errors, strip
# =============================================================================


@pytest.mark.property
@pytest.mark.slow
class TestTextProcessingPropertyIdentityPreservationPBT:
    """Property-based tests for text processing property identity preservation.

    These tests verify that changing text processing properties (unicode_errors,
    strip) preserves all widget object IDs in the subtree.

    **Property 1: Style-only property updates preserve widget identity**
    **Validates: Requirements 2.1-2.3**
    """

    @given(
        markdown_text=simple_markdown_document(),
        unicode_errors=st.sampled_from(['strict', 'replace', 'ignore']),
        strip=st.booleans()
    )
    # Feature: optimize-rebuild-contract, Property 1: Style-only property updates preserve widget identity
    # Finite strategy: 3 unicode_errors × 2 strip = 6 combinations with complex markdown
    @settings(max_examples=30, deadline=None)
    def test_text_processing_properties_preserve_widget_identity(
        self, markdown_text, unicode_errors, strip
    ):
        """Text Processing Properties Preserve Widget Identity.

        *For any* MarkdownLabel with non-empty content, and *for any* text
        processing property (unicode_errors, strip), changing that property
        SHALL preserve all widget object IDs in the subtree (the set of IDs
        before equals the set of IDs after).

        **Validates: Requirements 2.1-2.3**
        """
        # Ensure we have non-empty content
        assume(markdown_text and markdown_text.strip())

        # Create MarkdownLabel with initial content
        label = MarkdownLabel(text=markdown_text)

        # Ensure we have children to test
        assume(len(label.children) > 0)

        # Capture widget IDs before changes
        ids_before = collect_widget_ids(label)

        # Apply all text processing property changes
        label.unicode_errors = unicode_errors
        label.strip = strip

        # Capture widget IDs after changes
        ids_after = collect_widget_ids(label)

        # Assert: widget IDs should be unchanged
        assert ids_before == ids_after, (
            f"Widget IDs changed after text processing property updates. "
            f"Before: {len(ids_before)} widgets, After: {len(ids_after)} widgets"
        )

    @given(
        markdown_text=simple_markdown_document(),
        unicode_errors=st.sampled_from(['strict', 'replace', 'ignore'])
    )
    # Feature: optimize-rebuild-contract, Property 1: Style-only property updates preserve widget identity
    # Finite strategy: 3 unicode_errors options × complex markdown
    @settings(max_examples=20, deadline=None)
    def test_unicode_errors_preserves_widget_identity(self, markdown_text, unicode_errors):
        """Unicode Errors Preserves Widget Identity.

        *For any* MarkdownLabel with non-empty content, and *for any* unicode_errors
        value ('strict', 'replace', 'ignore'), changing unicode_errors SHALL
        preserve all widget object IDs.

        **Validates: Requirements 2.1, 2.3**
        """
        # Ensure we have non-empty content
        assume(markdown_text and markdown_text.strip())

        # Create MarkdownLabel with initial content
        label = MarkdownLabel(text=markdown_text)

        # Ensure we have children to test
        assume(len(label.children) > 0)

        # Capture widget IDs before change
        ids_before = collect_widget_ids(label)

        # Apply unicode_errors change
        label.unicode_errors = unicode_errors

        # Capture widget IDs after change
        ids_after = collect_widget_ids(label)

        # Assert: widget IDs should be unchanged
        assert ids_before == ids_after, (
            f"Widget IDs changed after unicode_errors update to {unicode_errors}. "
            f"Before: {len(ids_before)} widgets, After: {len(ids_after)} widgets"
        )

    @given(
        markdown_text=simple_markdown_document(),
        strip=st.booleans()
    )
    # Feature: optimize-rebuild-contract, Property 1: Style-only property updates preserve widget identity
    # Finite strategy: 2 boolean options × complex markdown
    @settings(max_examples=20, deadline=None)
    def test_strip_preserves_widget_identity(self, markdown_text, strip):
        """Strip Preserves Widget Identity.

        *For any* MarkdownLabel with non-empty content, and *for any* strip
        value (True/False), changing strip SHALL preserve all widget
        object IDs.

        **Validates: Requirements 2.2, 2.3**
        """
        # Ensure we have non-empty content
        assume(markdown_text and markdown_text.strip())

        # Create MarkdownLabel with initial content
        label = MarkdownLabel(text=markdown_text)

        # Ensure we have children to test
        assume(len(label.children) > 0)

        # Capture widget IDs before change
        ids_before = collect_widget_ids(label)

        # Apply strip change
        label.strip = strip

        # Capture widget IDs after change
        ids_after = collect_widget_ids(label)

        # Assert: widget IDs should be unchanged
        assert ids_before == ids_after, (
            f"Widget IDs changed after strip update to {strip}. "
            f"Before: {len(ids_before)} widgets, After: {len(ids_after)} widgets"
        )


# =============================================================================
# Truncation Properties Widget Identity Preservation Tests
# =============================================================================
# These tests validate Property 1 from the design document:
# "Style-only property updates preserve widget identity"
# Specifically for the newly reclassified truncation properties:
# shorten, max_lines, shorten_from, split_str, ellipsis_options
# =============================================================================


@pytest.mark.property
@pytest.mark.slow
class TestTruncationPropertyIdentityPreservationPBT:
    """Property-based tests for truncation property identity preservation.

    These tests verify that changing truncation properties (shorten, max_lines,
    shorten_from, split_str, ellipsis_options) preserves all widget object IDs
    in the subtree.

    **Property 1: Style-only property updates preserve widget identity**
    **Validates: Requirements 3.1-3.6**
    """

    @given(
        markdown_text=simple_markdown_document(),
        shorten=st.booleans(),
        max_lines=st.integers(min_value=0, max_value=10),
        shorten_from=st.sampled_from(['left', 'center', 'right']),
        split_str=st.text(min_size=0, max_size=5, alphabet=st.characters(
            whitelist_categories=['L', 'N', 'P', 'Z'],
            blacklist_characters='[]&\n\r'
        )),
        ellipsis_options=st.fixed_dictionaries({}, optional={
            'color': st.tuples(
                st.floats(min_value=0, max_value=1),
                st.floats(min_value=0, max_value=1),
                st.floats(min_value=0, max_value=1),
                st.floats(min_value=0, max_value=1)
            )
        })
    )
    # Feature: optimize-rebuild-contract, Property 1: Style-only property updates preserve widget identity
    # Mixed finite/complex strategy: 50 examples (2×11×3 = 66 finite combinations with 2 complex strategies)
    @settings(max_examples=50, deadline=None)
    def test_truncation_properties_preserve_widget_identity(
        self, markdown_text, shorten, max_lines, shorten_from, split_str, ellipsis_options
    ):
        """Truncation Properties Preserve Widget Identity.

        *For any* MarkdownLabel with non-empty content, and *for any* truncation
        property (shorten, max_lines, shorten_from, split_str, ellipsis_options),
        changing that property SHALL preserve all widget object IDs in the subtree
        (the set of IDs before equals the set of IDs after).

        **Validates: Requirements 3.1-3.6**
        """
        # Ensure we have non-empty content
        assume(markdown_text and markdown_text.strip())

        # Create MarkdownLabel with initial content
        label = MarkdownLabel(text=markdown_text)

        # Ensure we have children to test
        assume(len(label.children) > 0)

        # Capture widget IDs before changes
        ids_before = collect_widget_ids(label)

        # Apply all truncation property changes
        label.shorten = shorten
        label.max_lines = max_lines
        label.shorten_from = shorten_from
        label.split_str = split_str
        label.ellipsis_options = ellipsis_options

        # Capture widget IDs after changes
        ids_after = collect_widget_ids(label)

        # Assert: widget IDs should be unchanged
        assert ids_before == ids_after, (
            f"Widget IDs changed after truncation property updates. "
            f"Before: {len(ids_before)} widgets, After: {len(ids_after)} widgets"
        )

    @given(
        markdown_text=simple_markdown_document(),
        shorten=st.booleans()
    )
    # Feature: optimize-rebuild-contract, Property 1: Style-only property updates preserve widget identity
    # Finite strategy: 2 boolean options × complex markdown
    @settings(max_examples=20, deadline=None)
    def test_shorten_preserves_widget_identity(self, markdown_text, shorten):
        """Shorten Preserves Widget Identity.

        *For any* MarkdownLabel with non-empty content, and *for any* shorten
        value (True/False), changing shorten SHALL preserve all widget
        object IDs.

        **Validates: Requirements 3.1, 3.6**
        """
        # Ensure we have non-empty content
        assume(markdown_text and markdown_text.strip())

        # Create MarkdownLabel with initial content
        label = MarkdownLabel(text=markdown_text)

        # Ensure we have children to test
        assume(len(label.children) > 0)

        # Capture widget IDs before change
        ids_before = collect_widget_ids(label)

        # Apply shorten change
        label.shorten = shorten

        # Capture widget IDs after change
        ids_after = collect_widget_ids(label)

        # Assert: widget IDs should be unchanged
        assert ids_before == ids_after, (
            f"Widget IDs changed after shorten update to {shorten}. "
            f"Before: {len(ids_before)} widgets, After: {len(ids_after)} widgets"
        )

    @given(
        markdown_text=simple_markdown_document(),
        max_lines=st.integers(min_value=0, max_value=10)
    )
    # Feature: optimize-rebuild-contract, Property 1: Style-only property updates preserve widget identity
    # Finite strategy: 11 integer options (0-10) × complex markdown
    @settings(max_examples=30, deadline=None)
    def test_max_lines_preserves_widget_identity(self, markdown_text, max_lines):
        """Max Lines Preserves Widget Identity.

        *For any* MarkdownLabel with non-empty content, and *for any* max_lines
        value (0-10), changing max_lines SHALL preserve all widget object IDs.

        **Validates: Requirements 3.2, 3.6**
        """
        # Ensure we have non-empty content
        assume(markdown_text and markdown_text.strip())

        # Create MarkdownLabel with initial content
        label = MarkdownLabel(text=markdown_text)

        # Ensure we have children to test
        assume(len(label.children) > 0)

        # Capture widget IDs before change
        ids_before = collect_widget_ids(label)

        # Apply max_lines change
        label.max_lines = max_lines

        # Capture widget IDs after change
        ids_after = collect_widget_ids(label)

        # Assert: widget IDs should be unchanged
        assert ids_before == ids_after, (
            f"Widget IDs changed after max_lines update to {max_lines}. "
            f"Before: {len(ids_before)} widgets, After: {len(ids_after)} widgets"
        )

    @given(
        markdown_text=simple_markdown_document(),
        shorten_from=st.sampled_from(['left', 'center', 'right'])
    )
    # Feature: optimize-rebuild-contract, Property 1: Style-only property updates preserve widget identity
    # Finite strategy: 3 options × complex markdown
    @settings(max_examples=20, deadline=None)
    def test_shorten_from_preserves_widget_identity(self, markdown_text, shorten_from):
        """Shorten From Preserves Widget Identity.

        *For any* MarkdownLabel with non-empty content, and *for any* shorten_from
        value ('left', 'center', 'right'), changing shorten_from SHALL preserve
        all widget object IDs.

        **Validates: Requirements 3.3, 3.6**
        """
        # Ensure we have non-empty content
        assume(markdown_text and markdown_text.strip())

        # Create MarkdownLabel with initial content
        label = MarkdownLabel(text=markdown_text)

        # Ensure we have children to test
        assume(len(label.children) > 0)

        # Capture widget IDs before change
        ids_before = collect_widget_ids(label)

        # Apply shorten_from change
        label.shorten_from = shorten_from

        # Capture widget IDs after change
        ids_after = collect_widget_ids(label)

        # Assert: widget IDs should be unchanged
        assert ids_before == ids_after, (
            f"Widget IDs changed after shorten_from update to {shorten_from}. "
            f"Before: {len(ids_before)} widgets, After: {len(ids_after)} widgets"
        )

    @given(
        markdown_text=simple_markdown_document(),
        split_str=st.text(min_size=0, max_size=5, alphabet=st.characters(
            whitelist_categories=['L', 'N', 'P', 'Z'],
            blacklist_characters='[]&\n\r'
        ))
    )
    # Feature: optimize-rebuild-contract, Property 1: Style-only property updates preserve widget identity
    # Complex strategy: split_str is a text string
    @settings(max_examples=30, deadline=None)
    def test_split_str_preserves_widget_identity(self, markdown_text, split_str):
        """Split Str Preserves Widget Identity.

        *For any* MarkdownLabel with non-empty content, and *for any* split_str
        value (string), changing split_str SHALL preserve all widget object IDs.

        **Validates: Requirements 3.4, 3.6**
        """
        # Ensure we have non-empty content
        assume(markdown_text and markdown_text.strip())

        # Create MarkdownLabel with initial content
        label = MarkdownLabel(text=markdown_text)

        # Ensure we have children to test
        assume(len(label.children) > 0)

        # Capture widget IDs before change
        ids_before = collect_widget_ids(label)

        # Apply split_str change
        label.split_str = split_str

        # Capture widget IDs after change
        ids_after = collect_widget_ids(label)

        # Assert: widget IDs should be unchanged
        assert ids_before == ids_after, (
            f"Widget IDs changed after split_str update to '{split_str}'. "
            f"Before: {len(ids_before)} widgets, After: {len(ids_after)} widgets"
        )

    @given(
        markdown_text=simple_markdown_document(),
        ellipsis_options=st.fixed_dictionaries({}, optional={
            'color': st.tuples(
                st.floats(min_value=0, max_value=1),
                st.floats(min_value=0, max_value=1),
                st.floats(min_value=0, max_value=1),
                st.floats(min_value=0, max_value=1)
            )
        })
    )
    # Feature: optimize-rebuild-contract, Property 1: Style-only property updates preserve widget identity
    # Complex strategy: ellipsis_options is a dictionary
    @settings(max_examples=30, deadline=None)
    def test_ellipsis_options_preserves_widget_identity(self, markdown_text, ellipsis_options):
        """Ellipsis Options Preserves Widget Identity.

        *For any* MarkdownLabel with non-empty content, and *for any* ellipsis_options
        value (dictionary), changing ellipsis_options SHALL preserve all widget
        object IDs.

        **Validates: Requirements 3.5, 3.6**
        """
        # Ensure we have non-empty content
        assume(markdown_text and markdown_text.strip())

        # Create MarkdownLabel with initial content
        label = MarkdownLabel(text=markdown_text)

        # Ensure we have children to test
        assume(len(label.children) > 0)

        # Capture widget IDs before change
        ids_before = collect_widget_ids(label)

        # Apply ellipsis_options change
        label.ellipsis_options = ellipsis_options

        # Capture widget IDs after change
        ids_after = collect_widget_ids(label)

        # Assert: widget IDs should be unchanged
        assert ids_before == ids_after, (
            f"Widget IDs changed after ellipsis_options update to {ellipsis_options}. "
            f"Before: {len(ids_before)} widgets, After: {len(ids_after)} widgets"
        )


# =============================================================================
# text_size Widget Identity Preservation Tests
# =============================================================================
# These tests validate Property 3 from the design document:
# "text_size updates preserve widget identity"
# Testing various text_size transitions including:
# [None, None], [width, None], [None, height], [width, height]
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
    # Mixed finite/complex strategy: 50 examples (4 text_size patterns with complex markdown)
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

    @given(
        markdown_text=simple_markdown_document(),
        initial_text_size=st.one_of(
            st.just([None, None]),
            st.tuples(
                st.floats(min_value=50, max_value=500, allow_nan=False, allow_infinity=False),
                st.none()
            ).map(list),
            st.tuples(
                st.none(),
                st.floats(min_value=50, max_value=500, allow_nan=False, allow_infinity=False)
            ).map(list),
            st.tuples(
                st.floats(min_value=50, max_value=500, allow_nan=False, allow_infinity=False),
                st.floats(min_value=50, max_value=500, allow_nan=False, allow_infinity=False)
            ).map(list)
        ),
        final_text_size=st.one_of(
            st.just([None, None]),
            st.tuples(
                st.floats(min_value=50, max_value=500, allow_nan=False, allow_infinity=False),
                st.none()
            ).map(list),
            st.tuples(
                st.none(),
                st.floats(min_value=50, max_value=500, allow_nan=False, allow_infinity=False)
            ).map(list),
            st.tuples(
                st.floats(min_value=50, max_value=500, allow_nan=False, allow_infinity=False),
                st.floats(min_value=50, max_value=500, allow_nan=False, allow_infinity=False)
            ).map(list)
        )
    )
    # Feature: optimize-rebuild-contract, Property 3: text_size updates preserve widget identity
    # Mixed finite/complex strategy: 50 examples (16 transition combinations with complex markdown)
    @settings(max_examples=50, deadline=None)
    def test_text_size_transitions_preserve_widget_identity(
        self, markdown_text, initial_text_size, final_text_size
    ):
        """text_size Transitions Preserve Widget Identity.

        *For any* MarkdownLabel with non-empty content, and *for any* transition
        between text_size values (e.g., [None, None] to [width, None], or
        [width, height] to [None, None]), the transition SHALL preserve all
        widget object IDs in the subtree.

        **Validates: Requirements 4.1, 4.4**
        """
        # Ensure we have non-empty content
        assume(markdown_text and markdown_text.strip())

        # Create MarkdownLabel with initial text_size
        label = MarkdownLabel(text=markdown_text, text_size=initial_text_size)

        # Ensure we have children to test
        assume(len(label.children) > 0)

        # Capture widget IDs before transition
        ids_before = collect_widget_ids(label)

        # Apply text_size transition
        label.text_size = final_text_size

        # Capture widget IDs after transition
        ids_after = collect_widget_ids(label)

        # Assert: widget IDs should be unchanged
        assert ids_before == ids_after, (
            f"Widget IDs changed after text_size transition from {initial_text_size} "
            f"to {final_text_size}. "
            f"Before: {len(ids_before)} widgets, After: {len(ids_after)} widgets"
        )

    @given(markdown_text=simple_markdown_document())
    # Feature: optimize-rebuild-contract, Property 3: text_size updates preserve widget identity
    # Complex strategy: markdown text only
    @settings(max_examples=30, deadline=None)
    def test_text_size_none_to_constrained_preserves_widget_identity(self, markdown_text):
        """text_size [None, None] to Constrained Preserves Widget Identity.

        *For any* MarkdownLabel with non-empty content, transitioning text_size
        from [None, None] to a constrained value SHALL preserve all widget
        object IDs.

        **Validates: Requirements 4.1, 4.4**
        """
        # Ensure we have non-empty content
        assume(markdown_text and markdown_text.strip())

        # Create MarkdownLabel with [None, None] text_size
        label = MarkdownLabel(text=markdown_text, text_size=[None, None])

        # Ensure we have children to test
        assume(len(label.children) > 0)

        # Capture widget IDs before change
        ids_before = collect_widget_ids(label)

        # Transition to constrained text_size
        label.text_size = [200, None]

        # Capture widget IDs after change
        ids_after = collect_widget_ids(label)

        # Assert: widget IDs should be unchanged
        assert ids_before == ids_after, (
            f"Widget IDs changed after text_size transition from [None, None] to [200, None]. "
            f"Before: {len(ids_before)} widgets, After: {len(ids_after)} widgets"
        )

    @given(markdown_text=simple_markdown_document())
    # Feature: optimize-rebuild-contract, Property 3: text_size updates preserve widget identity
    # Complex strategy: markdown text only
    @settings(max_examples=30, deadline=None)
    def test_text_size_constrained_to_none_preserves_widget_identity(self, markdown_text):
        """text_size Constrained to [None, None] Preserves Widget Identity.

        *For any* MarkdownLabel with non-empty content, transitioning text_size
        from a constrained value to [None, None] SHALL preserve all widget
        object IDs.

        **Validates: Requirements 4.1, 4.4**
        """
        # Ensure we have non-empty content
        assume(markdown_text and markdown_text.strip())

        # Create MarkdownLabel with constrained text_size
        label = MarkdownLabel(text=markdown_text, text_size=[200, None])

        # Ensure we have children to test
        assume(len(label.children) > 0)

        # Capture widget IDs before change
        ids_before = collect_widget_ids(label)

        # Transition to [None, None]
        label.text_size = [None, None]

        # Capture widget IDs after change
        ids_after = collect_widget_ids(label)

        # Assert: widget IDs should be unchanged
        assert ids_before == ids_after, (
            f"Widget IDs changed after text_size transition from [200, None] to [None, None]. "
            f"Before: {len(ids_before)} widgets, After: {len(ids_after)} widgets"
        )

    @given(
        markdown_text=simple_markdown_document(),
        width=st.floats(min_value=50, max_value=500, allow_nan=False, allow_infinity=False)
    )
    # Feature: optimize-rebuild-contract, Property 3: text_size updates preserve widget identity
    # Complex strategy: width float with complex markdown
    @settings(max_examples=30, deadline=None)
    def test_text_size_width_only_preserves_widget_identity(self, markdown_text, width):
        """text_size [width, None] Preserves Widget Identity.

        *For any* MarkdownLabel with non-empty content, and *for any* width value,
        setting text_size to [width, None] SHALL preserve all widget object IDs.

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

        # Apply text_size with width only
        label.text_size = [width, None]

        # Capture widget IDs after change
        ids_after = collect_widget_ids(label)

        # Assert: widget IDs should be unchanged
        assert ids_before == ids_after, (
            f"Widget IDs changed after text_size update to [{width}, None]. "
            f"Before: {len(ids_before)} widgets, After: {len(ids_after)} widgets"
        )

    @given(
        markdown_text=simple_markdown_document(),
        height=st.floats(min_value=50, max_value=500, allow_nan=False, allow_infinity=False)
    )
    # Feature: optimize-rebuild-contract, Property 3: text_size updates preserve widget identity
    # Complex strategy: height float with complex markdown
    @settings(max_examples=30, deadline=None)
    def test_text_size_height_only_preserves_widget_identity(self, markdown_text, height):
        """text_size [None, height] Preserves Widget Identity.

        *For any* MarkdownLabel with non-empty content, and *for any* height value,
        setting text_size to [None, height] SHALL preserve all widget object IDs.

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

        # Apply text_size with height only
        label.text_size = [None, height]

        # Capture widget IDs after change
        ids_after = collect_widget_ids(label)

        # Assert: widget IDs should be unchanged
        assert ids_before == ids_after, (
            f"Widget IDs changed after text_size update to [None, {height}]. "
            f"Before: {len(ids_before)} widgets, After: {len(ids_after)} widgets"
        )

    @given(
        markdown_text=simple_markdown_document(),
        width=st.floats(min_value=50, max_value=500, allow_nan=False, allow_infinity=False),
        height=st.floats(min_value=50, max_value=500, allow_nan=False, allow_infinity=False)
    )
    # Feature: optimize-rebuild-contract, Property 3: text_size updates preserve widget identity
    # Complex strategy: width and height floats with complex markdown
    @settings(max_examples=30, deadline=None)
    def test_text_size_both_constrained_preserves_widget_identity(
        self, markdown_text, width, height
    ):
        """text_size [width, height] Preserves Widget Identity.

        *For any* MarkdownLabel with non-empty content, and *for any* width and
        height values, setting text_size to [width, height] SHALL preserve all
        widget object IDs.

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

        # Apply text_size with both width and height
        label.text_size = [width, height]

        # Capture widget IDs after change
        ids_after = collect_widget_ids(label)

        # Assert: widget IDs should be unchanged
        assert ids_before == ids_after, (
            f"Widget IDs changed after text_size update to [{width}, {height}]. "
            f"Before: {len(ids_before)} widgets, After: {len(ids_after)} widgets"
        )


# =============================================================================
# Advanced Font Properties Value Propagation Tests
# =============================================================================
# These tests validate Property 2 from the design document:
# "Style-only property updates apply values to all child Labels"
# Specifically for the newly reclassified advanced font properties:
# font_family, font_context, font_features, font_hinting, font_kerning, font_blended
# =============================================================================


@pytest.mark.property
@pytest.mark.slow
class TestAdvancedFontPropertyValuePropagationPBT:
    """Property-based tests for advanced font property value propagation.

    These tests verify that changing advanced font properties (font_family,
    font_context, font_features, font_hinting, font_kerning, font_blended)
    applies the new values to all child Label widgets.

    **Property 2: Style-only property updates apply values to all child Labels**
    **Validates: Requirements 1.1-1.6**
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
        markdown_text=simple_markdown_document(),
        initial_font_family=st.one_of(st.none(), st.just('Roboto')),
        new_font_family=st.one_of(st.none(), st.text(min_size=1, max_size=30, alphabet=st.characters(
            whitelist_categories=['L', 'N'],
            blacklist_characters='[]&\n\r'
        )))
    )
    # Feature: optimize-rebuild-contract, Property 2: Style-only property updates apply values to all child Labels
    # Complex strategy: font_family can be None or text
    @settings(max_examples=30, deadline=None)
    def test_font_family_value_propagates_to_non_code_children(
        self, markdown_text, initial_font_family, new_font_family
    ):
        """font_family Value Propagates to Non-Code Children After Change.

        *For any* MarkdownLabel with non-empty content, and *for any* font_family
        value, changing font_family SHALL apply the new value to all non-code
        child Label widgets (code blocks preserve their monospace font).

        **Validates: Requirements 1.1**
        """
        # Ensure we have non-empty content
        assume(markdown_text and markdown_text.strip())
        # Ensure we're actually changing the value
        assume(initial_font_family != new_font_family)

        # Create MarkdownLabel with initial font_family
        label = MarkdownLabel(text=markdown_text, font_family=initial_font_family)

        # Ensure we have children to test
        non_code_labels = self._find_non_code_labels(label)
        assume(len(non_code_labels) >= 1)

        # Apply font_family change
        label.font_family = new_font_family

        # Verify all non-code child Labels have the new font_family value
        non_code_labels = self._find_non_code_labels(label)
        for child_label in non_code_labels:
            assert child_label.font_family == new_font_family, (
                f"font_family not propagated to child Label. "
                f"Expected {new_font_family!r}, got {child_label.font_family!r}"
            )

    @given(
        markdown_text=simple_markdown_document(),
        initial_font_context=st.one_of(st.none(), st.just('system')),
        new_font_context=st.one_of(st.none(), st.text(min_size=1, max_size=30, alphabet=st.characters(
            whitelist_categories=['L', 'N'],
            blacklist_characters='[]&\n\r'
        )))
    )
    # Feature: optimize-rebuild-contract, Property 2: Style-only property updates apply values to all child Labels
    # Complex strategy: font_context can be None or text
    @settings(max_examples=30, deadline=None)
    def test_font_context_value_propagates_to_all_children(
        self, markdown_text, initial_font_context, new_font_context
    ):
        """font_context Value Propagates to All Children After Change.

        *For any* MarkdownLabel with non-empty content, and *for any* font_context
        value, changing font_context SHALL apply the new value to all child
        Label widgets.

        **Validates: Requirements 1.2**
        """
        # Ensure we have non-empty content
        assume(markdown_text and markdown_text.strip())
        # Ensure we're actually changing the value
        assume(initial_font_context != new_font_context)

        # Create MarkdownLabel with initial font_context
        label = MarkdownLabel(text=markdown_text, font_context=initial_font_context)

        # Ensure we have children to test
        child_labels = find_labels_recursive(label)
        assume(len(child_labels) >= 1)

        # Apply font_context change
        label.font_context = new_font_context

        # Verify all child Labels have the new font_context value
        child_labels = find_labels_recursive(label)
        for child_label in child_labels:
            assert child_label.font_context == new_font_context, (
                f"font_context not propagated to child Label. "
                f"Expected {new_font_context!r}, got {child_label.font_context!r}"
            )

    @given(
        markdown_text=simple_markdown_document(),
        initial_font_features=st.just(''),
        new_font_features=st.text(min_size=0, max_size=30, alphabet=st.characters(
            whitelist_categories=['L', 'N', 'P'],
            blacklist_characters='[]&\n\r'
        ))
    )
    # Feature: optimize-rebuild-contract, Property 2: Style-only property updates apply values to all child Labels
    # Complex strategy: font_features is a text string
    @settings(max_examples=30, deadline=None)
    def test_font_features_value_propagates_to_all_children(
        self, markdown_text, initial_font_features, new_font_features
    ):
        """font_features Value Propagates to All Children After Change.

        *For any* MarkdownLabel with non-empty content, and *for any* font_features
        value, changing font_features SHALL apply the new value to all child
        Label widgets.

        **Validates: Requirements 1.3**
        """
        # Ensure we have non-empty content
        assume(markdown_text and markdown_text.strip())
        # Ensure we're actually changing the value
        assume(initial_font_features != new_font_features)

        # Create MarkdownLabel with initial font_features
        label = MarkdownLabel(text=markdown_text, font_features=initial_font_features)

        # Ensure we have children to test
        child_labels = find_labels_recursive(label)
        assume(len(child_labels) >= 1)

        # Apply font_features change
        label.font_features = new_font_features

        # Verify all child Labels have the new font_features value
        child_labels = find_labels_recursive(label)
        for child_label in child_labels:
            assert child_label.font_features == new_font_features, (
                f"font_features not propagated to child Label. "
                f"Expected {new_font_features!r}, got {child_label.font_features!r}"
            )

    @given(
        markdown_text=simple_markdown_document(),
        initial_font_hinting=st.sampled_from([None, 'normal']),
        new_font_hinting=st.sampled_from([None, 'normal', 'light', 'mono'])
    )
    # Feature: optimize-rebuild-contract, Property 2: Style-only property updates apply values to all child Labels
    # Finite strategy: 4 font_hinting options
    @settings(max_examples=20, deadline=None)
    def test_font_hinting_value_propagates_to_all_children(
        self, markdown_text, initial_font_hinting, new_font_hinting
    ):
        """font_hinting Value Propagates to All Children After Change.

        *For any* MarkdownLabel with non-empty content, and *for any* font_hinting
        value (None, 'normal', 'light', 'mono'), changing font_hinting SHALL
        apply the new value to all child Label widgets.

        **Validates: Requirements 1.4**
        """
        # Ensure we have non-empty content
        assume(markdown_text and markdown_text.strip())
        # Ensure we're actually changing the value
        assume(initial_font_hinting != new_font_hinting)

        # Create MarkdownLabel with initial font_hinting
        label = MarkdownLabel(text=markdown_text, font_hinting=initial_font_hinting)

        # Ensure we have children to test
        child_labels = find_labels_recursive(label)
        assume(len(child_labels) >= 1)

        # Apply font_hinting change
        label.font_hinting = new_font_hinting

        # Verify all child Labels have the new font_hinting value
        child_labels = find_labels_recursive(label)
        for child_label in child_labels:
            # font_hinting may be None or a string value
            if new_font_hinting is not None:
                assert child_label.font_hinting == new_font_hinting, (
                    f"font_hinting not propagated to child Label. "
                    f"Expected {new_font_hinting!r}, got {child_label.font_hinting!r}"
                )

    @given(
        markdown_text=simple_markdown_document(),
        initial_font_kerning=st.booleans(),
        new_font_kerning=st.booleans()
    )
    # Feature: optimize-rebuild-contract, Property 2: Style-only property updates apply values to all child Labels
    # Finite strategy: 2 boolean options
    @settings(max_examples=20, deadline=None)
    def test_font_kerning_value_propagates_to_all_children(
        self, markdown_text, initial_font_kerning, new_font_kerning
    ):
        """font_kerning Value Propagates to All Children After Change.

        *For any* MarkdownLabel with non-empty content, and *for any* font_kerning
        value (True/False), changing font_kerning SHALL apply the new value to
        all child Label widgets.

        **Validates: Requirements 1.5**
        """
        # Ensure we have non-empty content
        assume(markdown_text and markdown_text.strip())
        # Ensure we're actually changing the value
        assume(initial_font_kerning != new_font_kerning)

        # Create MarkdownLabel with initial font_kerning
        label = MarkdownLabel(text=markdown_text, font_kerning=initial_font_kerning)

        # Ensure we have children to test
        child_labels = find_labels_recursive(label)
        assume(len(child_labels) >= 1)

        # Apply font_kerning change
        label.font_kerning = new_font_kerning

        # Verify all child Labels have the new font_kerning value
        child_labels = find_labels_recursive(label)
        for child_label in child_labels:
            assert child_label.font_kerning == new_font_kerning, (
                f"font_kerning not propagated to child Label. "
                f"Expected {new_font_kerning}, got {child_label.font_kerning}"
            )

    @given(
        markdown_text=simple_markdown_document(),
        initial_font_blended=st.booleans(),
        new_font_blended=st.booleans()
    )
    # Feature: optimize-rebuild-contract, Property 2: Style-only property updates apply values to all child Labels
    # Finite strategy: 2 boolean options
    @settings(max_examples=20, deadline=None)
    def test_font_blended_value_propagates_to_all_children(
        self, markdown_text, initial_font_blended, new_font_blended
    ):
        """font_blended Value Propagates to All Children After Change.

        *For any* MarkdownLabel with non-empty content, and *for any* font_blended
        value (True/False), changing font_blended SHALL apply the new value to
        all child Label widgets.

        **Validates: Requirements 1.6**
        """
        # Ensure we have non-empty content
        assume(markdown_text and markdown_text.strip())
        # Ensure we're actually changing the value
        assume(initial_font_blended != new_font_blended)

        # Create MarkdownLabel with initial font_blended
        label = MarkdownLabel(text=markdown_text, font_blended=initial_font_blended)

        # Ensure we have children to test
        child_labels = find_labels_recursive(label)
        assume(len(child_labels) >= 1)

        # Apply font_blended change
        label.font_blended = new_font_blended

        # Verify all child Labels have the new font_blended value
        child_labels = find_labels_recursive(label)
        for child_label in child_labels:
            assert child_label.font_blended == new_font_blended, (
                f"font_blended not propagated to child Label. "
                f"Expected {new_font_blended}, got {child_label.font_blended}"
            )

    @given(
        markdown_text=simple_markdown_document(),
        font_family=st.one_of(st.none(), st.text(min_size=1, max_size=20, alphabet=st.characters(
            whitelist_categories=['L', 'N'],
            blacklist_characters='[]&\n\r'
        ))),
        font_context=st.one_of(st.none(), st.text(min_size=1, max_size=20, alphabet=st.characters(
            whitelist_categories=['L', 'N'],
            blacklist_characters='[]&\n\r'
        ))),
        font_features=st.text(min_size=0, max_size=20, alphabet=st.characters(
            whitelist_categories=['L', 'N', 'P'],
            blacklist_characters='[]&\n\r'
        )),
        font_hinting=st.sampled_from([None, 'normal', 'light', 'mono']),
        font_kerning=st.booleans(),
        font_blended=st.booleans()
    )
    # Feature: optimize-rebuild-contract, Property 2: Style-only property updates apply values to all child Labels
    # Mixed finite/complex strategy: 50 examples (8 finite combinations with 3 complex strategies)
    @settings(max_examples=50, deadline=None)
    def test_all_advanced_font_properties_propagate_to_children(
        self, markdown_text, font_family, font_context, font_features,
        font_hinting, font_kerning, font_blended
    ):
        """All Advanced Font Properties Propagate to Children After Change.

        *For any* MarkdownLabel with non-empty content, and *for any* combination
        of advanced font property values, changing those properties SHALL apply
        the new values to all child Label widgets (with font_family excluded
        from code blocks).

        **Validates: Requirements 1.1-1.6**
        """
        # Ensure we have non-empty content
        assume(markdown_text and markdown_text.strip())

        # Create MarkdownLabel with default values
        label = MarkdownLabel(text=markdown_text)

        # Ensure we have children to test
        child_labels = find_labels_recursive(label)
        assume(len(child_labels) >= 1)

        # Apply all advanced font property changes
        label.font_family = font_family
        label.font_context = font_context
        label.font_features = font_features
        label.font_hinting = font_hinting
        label.font_kerning = font_kerning
        label.font_blended = font_blended

        # Verify all child Labels have the new property values
        child_labels = find_labels_recursive(label)
        non_code_labels = self._find_non_code_labels(label)
        code_labels = self._find_code_block_labels(label)

        # Check non-code labels (should have all properties including font_family)
        for child_label in non_code_labels:
            assert child_label.font_family == font_family, (
                f"font_family not propagated to non-code Label. "
                f"Expected {font_family!r}, got {child_label.font_family!r}"
            )

        # Check all labels for properties that apply to all (including code blocks)
        for child_label in child_labels:
            assert child_label.font_context == font_context, (
                f"font_context not propagated to child Label. "
                f"Expected {font_context!r}, got {child_label.font_context!r}"
            )
            assert child_label.font_features == font_features, (
                f"font_features not propagated to child Label. "
                f"Expected {font_features!r}, got {child_label.font_features!r}"
            )
            if font_hinting is not None:
                assert child_label.font_hinting == font_hinting, (
                    f"font_hinting not propagated to child Label. "
                    f"Expected {font_hinting!r}, got {child_label.font_hinting!r}"
                )
            assert child_label.font_kerning == font_kerning, (
                f"font_kerning not propagated to child Label. "
                f"Expected {font_kerning}, got {child_label.font_kerning}"
            )
            assert child_label.font_blended == font_blended, (
                f"font_blended not propagated to child Label. "
                f"Expected {font_blended}, got {child_label.font_blended}"
            )

        # Verify code labels do NOT have font_family set (preserve monospace)
        for child_label in code_labels:
            assert child_label.font_family is None, (
                f"font_family should NOT be propagated to code Label. "
                f"Expected None, got {child_label.font_family!r}"
            )


# =============================================================================
# Text Processing Properties Value Propagation Tests
# =============================================================================
# These tests validate Property 2 from the design document:
# "Style-only property updates apply values to all child Labels"
# Specifically for the newly reclassified text processing properties:
# unicode_errors, strip
# =============================================================================


@pytest.mark.property
@pytest.mark.slow
class TestTextProcessingPropertyValuePropagationPBT:
    """Property-based tests for text processing property value propagation.

    These tests verify that changing text processing properties (unicode_errors,
    strip) applies the new values to all child Label widgets.

    **Property 2: Style-only property updates apply values to all child Labels**
    **Validates: Requirements 2.1-2.2**
    """

    @given(
        markdown_text=simple_markdown_document(),
        initial_unicode_errors=st.sampled_from(['strict', 'replace']),
        new_unicode_errors=st.sampled_from(['strict', 'replace', 'ignore'])
    )
    # Feature: optimize-rebuild-contract, Property 2: Style-only property updates apply values to all child Labels
    # Finite strategy: 3 unicode_errors options
    @settings(max_examples=20, deadline=None)
    def test_unicode_errors_value_propagates_to_all_children(
        self, markdown_text, initial_unicode_errors, new_unicode_errors
    ):
        """unicode_errors Value Propagates to All Children After Change.

        *For any* MarkdownLabel with non-empty content, and *for any* unicode_errors
        value ('strict', 'replace', 'ignore'), changing unicode_errors SHALL
        apply the new value to all child Label widgets.

        **Validates: Requirements 2.1**
        """
        # Ensure we have non-empty content
        assume(markdown_text and markdown_text.strip())
        # Ensure we're actually changing the value
        assume(initial_unicode_errors != new_unicode_errors)

        # Create MarkdownLabel with initial unicode_errors
        label = MarkdownLabel(text=markdown_text, unicode_errors=initial_unicode_errors)

        # Ensure we have children to test
        child_labels = find_labels_recursive(label)
        assume(len(child_labels) >= 1)

        # Apply unicode_errors change
        label.unicode_errors = new_unicode_errors

        # Verify all child Labels have the new unicode_errors value
        child_labels = find_labels_recursive(label)
        for child_label in child_labels:
            assert child_label.unicode_errors == new_unicode_errors, (
                f"unicode_errors not propagated to child Label. "
                f"Expected {new_unicode_errors!r}, got {child_label.unicode_errors!r}"
            )

    @given(
        markdown_text=simple_markdown_document(),
        initial_strip=st.booleans(),
        new_strip=st.booleans()
    )
    # Feature: optimize-rebuild-contract, Property 2: Style-only property updates apply values to all child Labels
    # Finite strategy: 2 boolean options
    @settings(max_examples=20, deadline=None)
    def test_strip_value_propagates_to_all_children(
        self, markdown_text, initial_strip, new_strip
    ):
        """strip Value Propagates to All Children After Change.

        *For any* MarkdownLabel with non-empty content, and *for any* strip
        value (True/False), changing strip SHALL apply the new value to all
        child Label widgets.

        **Validates: Requirements 2.2**
        """
        # Ensure we have non-empty content
        assume(markdown_text and markdown_text.strip())
        # Ensure we're actually changing the value
        assume(initial_strip != new_strip)

        # Create MarkdownLabel with initial strip
        label = MarkdownLabel(text=markdown_text, strip=initial_strip)

        # Ensure we have children to test
        child_labels = find_labels_recursive(label)
        assume(len(child_labels) >= 1)

        # Apply strip change
        label.strip = new_strip

        # Verify all child Labels have the new strip value
        child_labels = find_labels_recursive(label)
        for child_label in child_labels:
            assert child_label.strip == new_strip, (
                f"strip not propagated to child Label. "
                f"Expected {new_strip}, got {child_label.strip}"
            )

    @given(
        markdown_text=simple_markdown_document(),
        unicode_errors=st.sampled_from(['strict', 'replace', 'ignore']),
        strip=st.booleans()
    )
    # Feature: optimize-rebuild-contract, Property 2: Style-only property updates apply values to all child Labels
    # Finite strategy: 3 unicode_errors × 2 strip = 6 combinations with complex markdown
    @settings(max_examples=30, deadline=None)
    def test_all_text_processing_properties_propagate_to_children(
        self, markdown_text, unicode_errors, strip
    ):
        """All Text Processing Properties Propagate to Children After Change.

        *For any* MarkdownLabel with non-empty content, and *for any* combination
        of text processing property values (unicode_errors, strip), changing
        those properties SHALL apply the new values to all child Label widgets.

        **Validates: Requirements 2.1-2.2**
        """
        # Ensure we have non-empty content
        assume(markdown_text and markdown_text.strip())

        # Create MarkdownLabel with default values
        label = MarkdownLabel(text=markdown_text)

        # Ensure we have children to test
        child_labels = find_labels_recursive(label)
        assume(len(child_labels) >= 1)

        # Apply all text processing property changes
        label.unicode_errors = unicode_errors
        label.strip = strip

        # Verify all child Labels have the new property values
        child_labels = find_labels_recursive(label)
        for child_label in child_labels:
            assert child_label.unicode_errors == unicode_errors, (
                f"unicode_errors not propagated to child Label. "
                f"Expected {unicode_errors!r}, got {child_label.unicode_errors!r}"
            )
            assert child_label.strip == strip, (
                f"strip not propagated to child Label. "
                f"Expected {strip}, got {child_label.strip}"
            )


# =============================================================================
# Truncation Properties Value Propagation Tests
# =============================================================================
# These tests validate Property 2 from the design document:
# "Style-only property updates apply values to all child Labels"
# Specifically for the newly reclassified truncation properties:
# shorten, max_lines, shorten_from, split_str, ellipsis_options
# =============================================================================


@pytest.mark.property
@pytest.mark.slow
class TestTruncationPropertyValuePropagationPBT:
    """Property-based tests for truncation property value propagation.

    These tests verify that changing truncation properties (shorten, max_lines,
    shorten_from, split_str, ellipsis_options) applies the new values to all
    child Label widgets.

    **Property 2: Style-only property updates apply values to all child Labels**
    **Validates: Requirements 3.1-3.5**
    """

    @given(
        markdown_text=simple_markdown_document(),
        initial_shorten=st.booleans(),
        new_shorten=st.booleans()
    )
    # Feature: optimize-rebuild-contract, Property 2: Style-only property updates apply values to all child Labels
    # Finite strategy: 2 boolean options
    @settings(max_examples=20, deadline=None)
    def test_shorten_value_propagates_to_all_children(
        self, markdown_text, initial_shorten, new_shorten
    ):
        """shorten Value Propagates to All Children After Change.

        *For any* MarkdownLabel with non-empty content, and *for any* shorten
        value (True/False), changing shorten SHALL apply the new value to all
        child Label widgets.

        **Validates: Requirements 3.1**
        """
        # Ensure we have non-empty content
        assume(markdown_text and markdown_text.strip())
        # Ensure we're actually changing the value
        assume(initial_shorten != new_shorten)

        # Create MarkdownLabel with initial shorten
        label = MarkdownLabel(text=markdown_text, shorten=initial_shorten)

        # Ensure we have children to test
        child_labels = find_labels_recursive(label)
        assume(len(child_labels) >= 1)

        # Apply shorten change
        label.shorten = new_shorten

        # Verify all child Labels have the new shorten value
        child_labels = find_labels_recursive(label)
        for child_label in child_labels:
            assert child_label.shorten == new_shorten, (
                f"shorten not propagated to child Label. "
                f"Expected {new_shorten}, got {child_label.shorten}"
            )

    @given(
        markdown_text=simple_markdown_document(),
        initial_max_lines=st.integers(min_value=1, max_value=5),
        new_max_lines=st.integers(min_value=1, max_value=10)
    )
    # Feature: optimize-rebuild-contract, Property 2: Style-only property updates apply values to all child Labels
    # Finite strategy: 10 integer options (1-10)
    @settings(max_examples=30, deadline=None)
    def test_max_lines_value_propagates_to_all_children(
        self, markdown_text, initial_max_lines, new_max_lines
    ):
        """max_lines Value Propagates to All Children After Change.

        *For any* MarkdownLabel with non-empty content, and *for any* max_lines
        value (1-10), changing max_lines SHALL apply the new value to all
        child Label widgets.

        **Validates: Requirements 3.2**
        """
        # Ensure we have non-empty content
        assume(markdown_text and markdown_text.strip())
        # Ensure we're actually changing the value
        assume(initial_max_lines != new_max_lines)

        # Create MarkdownLabel with initial max_lines
        label = MarkdownLabel(text=markdown_text, max_lines=initial_max_lines)

        # Ensure we have children to test
        child_labels = find_labels_recursive(label)
        assume(len(child_labels) >= 1)

        # Apply max_lines change
        label.max_lines = new_max_lines

        # Verify all child Labels have the new max_lines value
        child_labels = find_labels_recursive(label)
        for child_label in child_labels:
            assert child_label.max_lines == new_max_lines, (
                f"max_lines not propagated to child Label. "
                f"Expected {new_max_lines}, got {child_label.max_lines}"
            )

    @given(
        markdown_text=simple_markdown_document(),
        initial_shorten_from=st.sampled_from(['left', 'center']),
        new_shorten_from=st.sampled_from(['left', 'center', 'right'])
    )
    # Feature: optimize-rebuild-contract, Property 2: Style-only property updates apply values to all child Labels
    # Finite strategy: 3 shorten_from options
    @settings(max_examples=20, deadline=None)
    def test_shorten_from_value_propagates_to_all_children(
        self, markdown_text, initial_shorten_from, new_shorten_from
    ):
        """shorten_from Value Propagates to All Children After Change.

        *For any* MarkdownLabel with non-empty content, and *for any* shorten_from
        value ('left', 'center', 'right'), changing shorten_from SHALL apply
        the new value to all child Label widgets.

        **Validates: Requirements 3.3**
        """
        # Ensure we have non-empty content
        assume(markdown_text and markdown_text.strip())
        # Ensure we're actually changing the value
        assume(initial_shorten_from != new_shorten_from)

        # Create MarkdownLabel with initial shorten_from
        label = MarkdownLabel(text=markdown_text, shorten_from=initial_shorten_from)

        # Ensure we have children to test
        child_labels = find_labels_recursive(label)
        assume(len(child_labels) >= 1)

        # Apply shorten_from change
        label.shorten_from = new_shorten_from

        # Verify all child Labels have the new shorten_from value
        child_labels = find_labels_recursive(label)
        for child_label in child_labels:
            assert child_label.shorten_from == new_shorten_from, (
                f"shorten_from not propagated to child Label. "
                f"Expected {new_shorten_from!r}, got {child_label.shorten_from!r}"
            )

    @given(
        markdown_text=simple_markdown_document(),
        initial_split_str=st.just(' '),
        new_split_str=st.text(min_size=0, max_size=5, alphabet=st.characters(
            whitelist_categories=['L', 'N', 'P', 'Z'],
            blacklist_characters='[]&\n\r'
        ))
    )
    # Feature: optimize-rebuild-contract, Property 2: Style-only property updates apply values to all child Labels
    # Complex strategy: split_str is a text string
    @settings(max_examples=30, deadline=None)
    def test_split_str_value_propagates_to_all_children(
        self, markdown_text, initial_split_str, new_split_str
    ):
        """split_str Value Propagates to All Children After Change.

        *For any* MarkdownLabel with non-empty content, and *for any* split_str
        value (string), changing split_str SHALL apply the new value to all
        child Label widgets.

        **Validates: Requirements 3.4**
        """
        # Ensure we have non-empty content
        assume(markdown_text and markdown_text.strip())
        # Ensure we're actually changing the value
        assume(initial_split_str != new_split_str)

        # Create MarkdownLabel with initial split_str
        label = MarkdownLabel(text=markdown_text, split_str=initial_split_str)

        # Ensure we have children to test
        child_labels = find_labels_recursive(label)
        assume(len(child_labels) >= 1)

        # Apply split_str change
        label.split_str = new_split_str

        # Verify all child Labels have the new split_str value
        child_labels = find_labels_recursive(label)
        for child_label in child_labels:
            assert child_label.split_str == new_split_str, (
                f"split_str not propagated to child Label. "
                f"Expected {new_split_str!r}, got {child_label.split_str!r}"
            )

    @given(
        markdown_text=simple_markdown_document(),
        initial_ellipsis_options=st.just({}),
        new_ellipsis_options=st.fixed_dictionaries({}, optional={
            'color': st.tuples(
                st.floats(min_value=0, max_value=1),
                st.floats(min_value=0, max_value=1),
                st.floats(min_value=0, max_value=1),
                st.floats(min_value=0, max_value=1)
            )
        })
    )
    # Feature: optimize-rebuild-contract, Property 2: Style-only property updates apply values to all child Labels
    # Complex strategy: ellipsis_options is a dictionary
    @settings(max_examples=30, deadline=None)
    def test_ellipsis_options_value_propagates_to_all_children(
        self, markdown_text, initial_ellipsis_options, new_ellipsis_options
    ):
        """ellipsis_options Value Propagates to All Children After Change.

        *For any* MarkdownLabel with non-empty content, and *for any* ellipsis_options
        value (dictionary), changing ellipsis_options SHALL apply the new value
        to all child Label widgets.

        **Validates: Requirements 3.5**
        """
        # Ensure we have non-empty content
        assume(markdown_text and markdown_text.strip())
        # Ensure we're actually changing the value
        assume(initial_ellipsis_options != new_ellipsis_options)

        # Create MarkdownLabel with initial ellipsis_options
        label = MarkdownLabel(text=markdown_text, ellipsis_options=initial_ellipsis_options)

        # Ensure we have children to test
        child_labels = find_labels_recursive(label)
        assume(len(child_labels) >= 1)

        # Apply ellipsis_options change
        label.ellipsis_options = new_ellipsis_options

        # Verify all child Labels have the new ellipsis_options value
        child_labels = find_labels_recursive(label)
        for child_label in child_labels:
            assert child_label.ellipsis_options == new_ellipsis_options, (
                f"ellipsis_options not propagated to child Label. "
                f"Expected {new_ellipsis_options}, got {child_label.ellipsis_options}"
            )

    @given(
        markdown_text=simple_markdown_document(),
        shorten=st.booleans(),
        max_lines=st.integers(min_value=1, max_value=10),
        shorten_from=st.sampled_from(['left', 'center', 'right']),
        split_str=st.text(min_size=0, max_size=5, alphabet=st.characters(
            whitelist_categories=['L', 'N', 'P', 'Z'],
            blacklist_characters='[]&\n\r'
        )),
        ellipsis_options=st.fixed_dictionaries({}, optional={
            'color': st.tuples(
                st.floats(min_value=0, max_value=1),
                st.floats(min_value=0, max_value=1),
                st.floats(min_value=0, max_value=1),
                st.floats(min_value=0, max_value=1)
            )
        })
    )
    # Feature: optimize-rebuild-contract, Property 2: Style-only property updates apply values to all child Labels
    # Mixed finite/complex strategy: 50 examples (2×10×3 = 60 finite combinations with 2 complex strategies)
    @settings(max_examples=50, deadline=None)
    def test_all_truncation_properties_propagate_to_children(
        self, markdown_text, shorten, max_lines, shorten_from, split_str, ellipsis_options
    ):
        """All Truncation Properties Propagate to Children After Change.

        *For any* MarkdownLabel with non-empty content, and *for any* combination
        of truncation property values (shorten, max_lines, shorten_from, split_str,
        ellipsis_options), changing those properties SHALL apply the new values
        to all child Label widgets.

        **Validates: Requirements 3.1-3.5**
        """
        # Ensure we have non-empty content
        assume(markdown_text and markdown_text.strip())

        # Create MarkdownLabel with default values
        label = MarkdownLabel(text=markdown_text)

        # Ensure we have children to test
        child_labels = find_labels_recursive(label)
        assume(len(child_labels) >= 1)

        # Apply all truncation property changes
        label.shorten = shorten
        label.max_lines = max_lines
        label.shorten_from = shorten_from
        label.split_str = split_str
        label.ellipsis_options = ellipsis_options

        # Verify all child Labels have the new property values
        child_labels = find_labels_recursive(label)
        for child_label in child_labels:
            assert child_label.shorten == shorten, (
                f"shorten not propagated to child Label. "
                f"Expected {shorten}, got {child_label.shorten}"
            )
            assert child_label.max_lines == max_lines, (
                f"max_lines not propagated to child Label. "
                f"Expected {max_lines}, got {child_label.max_lines}"
            )
            assert child_label.shorten_from == shorten_from, (
                f"shorten_from not propagated to child Label. "
                f"Expected {shorten_from!r}, got {child_label.shorten_from!r}"
            )
            assert child_label.split_str == split_str, (
                f"split_str not propagated to child Label. "
                f"Expected {split_str!r}, got {child_label.split_str!r}"
            )
            assert child_label.ellipsis_options == ellipsis_options, (
                f"ellipsis_options not propagated to child Label. "
                f"Expected {ellipsis_options}, got {child_label.ellipsis_options}"
            )


# =============================================================================
# Code Block Font Preservation Tests
# =============================================================================
# These tests validate Property 4 from the design document:
# "Code blocks preserve monospace font when font_family changes"
# Specifically verifying that code blocks keep their code_font_name when
# font_family is changed on the MarkdownLabel.
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
    # Feature: optimize-rebuild-contract, Property 4: Code blocks preserve monospace font when font_family changes
    # Complex strategy: font_family is text
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

    @given(
        initial_font_family=st.one_of(st.none(), st.just('Roboto')),
        new_font_family=st.text(min_size=1, max_size=30, alphabet=st.characters(
            whitelist_categories=['L', 'N'],
            blacklist_characters='[]&\n\r'
        ))
    )
    # Feature: optimize-rebuild-contract, Property 4: Code blocks preserve monospace font when font_family changes
    # Complex strategy: font_family transitions from None/Roboto to new value
    @settings(max_examples=30, deadline=None)
    def test_code_blocks_preserve_font_through_font_family_transitions(
        self, initial_font_family, new_font_family
    ):
        """Code Blocks Preserve Font Through font_family Transitions.

        *For any* MarkdownLabel containing code blocks and *for any* font_family
        transition (from None or initial value to new value), code blocks SHALL
        preserve their code_font_name throughout the transition.

        **Validates: Requirements 6.2**
        """
        # Ensure we're actually changing the value
        assume(initial_font_family != new_font_family)

        # Create markdown with code block
        markdown = '# Heading\n\n```\ncode block\n```\n\nParagraph'
        code_font = 'RobotoMono-Regular'

        # Create MarkdownLabel with initial font_family
        label = MarkdownLabel(
            text=markdown,
            font_family=initial_font_family,
            code_font_name=code_font
        )

        # Find code block labels
        code_labels = self._find_code_block_labels(label)
        assume(len(code_labels) >= 1)

        # Verify code blocks have code_font_name initially
        for code_label in code_labels:
            assert code_label.font_name == code_font, (
                f"Code block should have code_font_name={code_font!r} initially"
            )

        # Change font_family
        label.font_family = new_font_family

        # Verify code blocks STILL have code_font_name after transition
        code_labels = self._find_code_block_labels(label)
        for code_label in code_labels:
            assert code_label.font_name == code_font, (
                f"Code block should preserve code_font_name={code_font!r} after "
                f"font_family transition from {initial_font_family!r} to {new_font_family!r}"
            )

    @given(
        font_family=st.text(min_size=1, max_size=20, alphabet=st.characters(
            whitelist_categories=['L', 'N'],
            blacklist_characters='[]&\n\r'
        )),
        # Use only Kivy built-in fonts that are guaranteed to exist
        code_font_name=st.sampled_from(['RobotoMono-Regular', 'Roboto', 'Roboto-Bold'])
    )
    # Feature: optimize-rebuild-contract, Property 4: Code blocks preserve monospace font when font_family changes
    # Mixed finite/complex strategy: 15 examples (3 finite × 5 complex samples)
    @settings(max_examples=15, deadline=None)
    def test_code_blocks_preserve_custom_code_font_name(
        self, font_family, code_font_name
    ):
        """Code Blocks Preserve Custom code_font_name When font_family Changes.

        *For any* MarkdownLabel with a custom code_font_name and *for any*
        font_family value, changing font_family SHALL preserve the custom
        code_font_name on code block Labels.

        **Validates: Requirements 6.2**
        """
        # Create markdown with code block
        markdown = 'Text before\n\n```javascript\nconsole.log("test");\n```\n\nText after'

        # Create MarkdownLabel with custom code_font_name
        label = MarkdownLabel(text=markdown, code_font_name=code_font_name)

        # Find code block labels
        code_labels = self._find_code_block_labels(label)
        assume(len(code_labels) >= 1)

        # Verify code blocks have custom code_font_name initially
        for code_label in code_labels:
            assert code_label.font_name == code_font_name, (
                f"Code block should have code_font_name={code_font_name!r} initially"
            )

        # Change font_family
        label.font_family = font_family

        # Verify code blocks STILL have custom code_font_name
        code_labels = self._find_code_block_labels(label)
        for code_label in code_labels:
            assert code_label.font_name == code_font_name, (
                f"Code block should preserve custom code_font_name={code_font_name!r} "
                f"after font_family change to {font_family!r}"
            )


class TestPropertyClassificationSets:
    """Unit tests for property classification sets.

    These tests verify that STYLE_ONLY_PROPERTIES and STRUCTURE_PROPERTIES
    are correctly defined, mutually exclusive, and contain the expected
    properties after the optimization reclassification.

    **Property 5: Property classification sets are mutually exclusive and complete**
    **Validates: Requirements 5.1-5.6**
    """

    def test_reclassified_advanced_font_properties_in_style_only(self):
        """Reclassified advanced font properties are in STYLE_ONLY_PROPERTIES.

        **Validates: Requirements 5.1**
        """
        reclassified_font_props = {
            'font_family',
            'font_context',
            'font_features',
            'font_hinting',
            'font_kerning',
            'font_blended',
        }
        assert reclassified_font_props.issubset(MarkdownLabel.STYLE_ONLY_PROPERTIES), (
            f"Missing advanced font properties from STYLE_ONLY_PROPERTIES: "
            f"{reclassified_font_props - MarkdownLabel.STYLE_ONLY_PROPERTIES}"
        )

    def test_reclassified_text_processing_properties_in_style_only(self):
        """Reclassified text processing properties are in STYLE_ONLY_PROPERTIES.

        **Validates: Requirements 5.2**
        """
        reclassified_text_props = {
            'unicode_errors',
            'strip',
        }
        assert reclassified_text_props.issubset(MarkdownLabel.STYLE_ONLY_PROPERTIES), (
            f"Missing text processing properties from STYLE_ONLY_PROPERTIES: "
            f"{reclassified_text_props - MarkdownLabel.STYLE_ONLY_PROPERTIES}"
        )

    def test_reclassified_truncation_properties_in_style_only(self):
        """Reclassified truncation properties are in STYLE_ONLY_PROPERTIES.

        **Validates: Requirements 5.3**
        """
        reclassified_truncation_props = {
            'shorten',
            'max_lines',
            'shorten_from',
            'split_str',
            'ellipsis_options',
        }
        assert reclassified_truncation_props.issubset(MarkdownLabel.STYLE_ONLY_PROPERTIES), (
            f"Missing truncation properties from STYLE_ONLY_PROPERTIES: "
            f"{reclassified_truncation_props - MarkdownLabel.STYLE_ONLY_PROPERTIES}"
        )

    def test_reclassified_text_size_in_style_only(self):
        """Reclassified text_size property is in STYLE_ONLY_PROPERTIES.

        **Validates: Requirements 5.4**
        """
        assert 'text_size' in MarkdownLabel.STYLE_ONLY_PROPERTIES, (
            "text_size should be in STYLE_ONLY_PROPERTIES"
        )

    def test_all_reclassified_properties_in_style_only(self):
        """All 14 reclassified properties are in STYLE_ONLY_PROPERTIES.

        **Validates: Requirements 5.1-5.4**
        """
        all_reclassified = {
            # Advanced font properties (6)
            'font_family',
            'font_context',
            'font_features',
            'font_hinting',
            'font_kerning',
            'font_blended',
            # Text processing properties (2)
            'unicode_errors',
            'strip',
            # Truncation properties (5)
            'shorten',
            'max_lines',
            'shorten_from',
            'split_str',
            'ellipsis_options',
            # Sizing property (1)
            'text_size',
        }
        assert all_reclassified.issubset(MarkdownLabel.STYLE_ONLY_PROPERTIES), (
            f"Missing reclassified properties from STYLE_ONLY_PROPERTIES: "
            f"{all_reclassified - MarkdownLabel.STYLE_ONLY_PROPERTIES}"
        )

    def test_reclassified_properties_not_in_structure(self):
        """Reclassified properties are NOT in STRUCTURE_PROPERTIES.

        **Validates: Requirements 5.5**
        """
        all_reclassified = {
            'font_family', 'font_context', 'font_features', 'font_hinting',
            'font_kerning', 'font_blended', 'unicode_errors', 'strip',
            'shorten', 'max_lines', 'shorten_from', 'split_str',
            'ellipsis_options', 'text_size',
        }
        overlap = all_reclassified & MarkdownLabel.STRUCTURE_PROPERTIES
        assert len(overlap) == 0, (
            f"Reclassified properties should not be in STRUCTURE_PROPERTIES: {overlap}"
        )

    def test_structure_properties_contains_expected(self):
        """STRUCTURE_PROPERTIES contains only expected properties.

        **Validates: Requirements 5.6**
        """
        expected_structure = {'text', 'link_style', 'render_mode', 'strict_label_mode'}
        assert MarkdownLabel.STRUCTURE_PROPERTIES == expected_structure, (
            f"STRUCTURE_PROPERTIES mismatch. "
            f"Expected: {expected_structure}, "
            f"Got: {MarkdownLabel.STRUCTURE_PROPERTIES}"
        )

    def test_sets_are_mutually_exclusive(self):
        """STYLE_ONLY_PROPERTIES and STRUCTURE_PROPERTIES are mutually exclusive.

        **Property 5: Property classification sets are mutually exclusive**
        """
        overlap = MarkdownLabel.STYLE_ONLY_PROPERTIES & MarkdownLabel.STRUCTURE_PROPERTIES
        assert len(overlap) == 0, (
            f"Property sets should be mutually exclusive but share: {overlap}"
        )

    def test_original_style_properties_preserved(self):
        """Original style-only properties are still in STYLE_ONLY_PROPERTIES."""
        original_style_props = {
            'color',
            'halign',
            'valign',
            'line_height',
            'disabled',
            'disabled_color',
            'base_direction',
            'text_padding',
            'outline_color',
            'disabled_outline_color',
            'outline_width',
            'mipmap',
            'text_language',
            'limit_render_to_text_bbox',
            'font_name',
            'code_font_name',
        }
        assert original_style_props.issubset(MarkdownLabel.STYLE_ONLY_PROPERTIES), (
            f"Missing original style properties from STYLE_ONLY_PROPERTIES: "
            f"{original_style_props - MarkdownLabel.STYLE_ONLY_PROPERTIES}"
        )

    def test_style_only_properties_count(self):
        """STYLE_ONLY_PROPERTIES has expected count after reclassification.

        Original: 16 properties
        Reclassified: +14 properties
        Total: 30 properties
        """
        # Original style-only properties: 16
        # Reclassified properties: 14
        # Total expected: 30
        expected_count = 30
        actual_count = len(MarkdownLabel.STYLE_ONLY_PROPERTIES)
        assert actual_count == expected_count, (
            f"STYLE_ONLY_PROPERTIES count mismatch. "
            f"Expected: {expected_count}, Got: {actual_count}"
        )

    def test_structure_properties_count(self):
        """STRUCTURE_PROPERTIES has expected count after reclassification.

        After reclassification, only 4 properties remain:
        text, link_style, render_mode, strict_label_mode
        """
        expected_count = 4
        actual_count = len(MarkdownLabel.STRUCTURE_PROPERTIES)
        assert actual_count == expected_count, (
            f"STRUCTURE_PROPERTIES count mismatch. "
            f"Expected: {expected_count}, Got: {actual_count}"
        )

    def test_sets_are_frozensets(self):
        """Property classification sets are immutable frozensets."""
        assert isinstance(MarkdownLabel.STYLE_ONLY_PROPERTIES, frozenset), (
            "STYLE_ONLY_PROPERTIES should be a frozenset"
        )
        assert isinstance(MarkdownLabel.STRUCTURE_PROPERTIES, frozenset), (
            "STRUCTURE_PROPERTIES should be a frozenset"
        )
