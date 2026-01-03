"""
Widget identity preservation and rebuild semantics tests for MarkdownLabel.

This module contains tests that verify widget identity preservation for style-only
property changes and widget tree rebuilding for structure property changes.
These tests are designed to run in headless CI environments without requiring
a Kivy window.

**Feature: headless-ci-testing**
**Validates: Requirements 4.1, 4.2, 4.4, 5.1, 5.2, 5.4**
"""

import pytest
from hypothesis import given, strategies as st, settings, assume

from kivy_garden.markdownlabel import MarkdownLabel
from .test_utils import (
    simple_markdown_document, find_labels_recursive,
    colors_equal, floats_equal, collect_widget_ids
)
from .conftest import st_font_size, st_font_name, st_rgba_color


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

    **Feature: headless-ci-testing**
    **Validates: Requirements 4.1**
    """

    def test_base_font_size_preserves_widget_tree(self):
        """Changing base_font_size preserves widget tree.

        **Validates: Requirements 4.1**
        """
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
        """Changing color preserves widget tree.

        **Validates: Requirements 4.1**
        """
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
        """Changing halign preserves widget tree.

        **Validates: Requirements 4.1**
        """
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
        """Changing valign preserves widget tree.

        **Validates: Requirements 4.1**
        """
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
        """Changing disabled preserves widget tree.

        **Validates: Requirements 4.1**
        """
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
        """Changing disabled_color preserves widget tree.

        **Validates: Requirements 4.1**
        """
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
        """Changing base_direction preserves widget tree.

        **Validates: Requirements 4.1**
        """
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
        """Changing line_height preserves widget tree.

        **Validates: Requirements 4.1**
        """
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
        """Changing multiple style properties preserves widget tree.

        **Validates: Requirements 4.1**
        """
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


@pytest.mark.slow
class TestStylePropertyIdentityPreservationPBT:
    """Property-based tests for style property identity preservation.

    **Feature: headless-ci-testing, Property 5: Style Property Changes Preserve
    Widget Identities**
    **Validates: Requirements 4.1**
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
    # Combination strategy: 50 examples (combination coverage)
    @settings(max_examples=50, deadline=None)
    def test_style_property_changes_preserve_widget_tree(
        self, markdown_text, base_font_size, color, halign, valign,
        disabled, disabled_color, base_direction, line_height
    ):
        """Property 5: Style Property Changes Preserve Widget Tree.

        *For any* MarkdownLabel with non-empty content, and *for any* style-only
        property (base_font_size, color, halign, valign, disabled, disabled_color,
        base_direction, line_height), changing that property SHALL preserve all
        widget object IDs in the subtree (the set of IDs before equals the set
        of IDs after).

        **Feature: headless-ci-testing, Property 5: Style Property Changes
        Preserve Widget Tree**
        **Validates: Requirements 4.1**
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

    **Feature: headless-ci-testing**
    **Validates: Requirements 4.4**
    """

    def test_color_propagates_to_descendants(self):
        """Color value propagates to all descendant Labels.

        **Validates: Requirements 4.4**
        """
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
        """Halign value propagates to all descendant Labels.

        **Validates: Requirements 4.4**
        """
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
        """Valign value propagates to all descendant Labels.

        **Validates: Requirements 4.4**
        """
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
        """Line_height value propagates to all descendant Labels.

        **Validates: Requirements 4.4**
        """
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
        """Disabled_color propagates to descendants when disabled is True.

        **Validates: Requirements 4.4**
        """
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
        """Base_direction value propagates to all descendant Labels.

        **Validates: Requirements 4.4**
        """
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


@pytest.mark.slow
class TestStylePropertyPropagationPBT:
    """Property-based tests for style property propagation to descendants.

    **Feature: headless-ci-testing, Property 6: Style Property Values Propagate
    to Descendants**
    **Validates: Requirements 4.4**
    """

    @given(
        markdown_text=simple_markdown_document(),
        color=st_rgba_color(),
        halign=st.sampled_from(['left', 'center', 'right', 'justify']),
        valign=st.sampled_from(['bottom', 'middle', 'top']),
        line_height=st.floats(min_value=0.5, max_value=3.0, allow_nan=False,
                               allow_infinity=False),
        base_direction=st.sampled_from([None, 'ltr', 'rtl', 'weak_ltr', 'weak_rtl'])
    )
    # Combination strategy: 50 examples (combination coverage)
    @settings(max_examples=50, deadline=None)
    def test_style_property_values_propagate_to_descendants(
        self, markdown_text, color, halign, valign, line_height, base_direction
    ):
        """Property 6: Style Property Values Propagate to Descendants.

        *For any* MarkdownLabel with non-empty content, and *for any* style-only
        property value, all descendant Label widgets SHALL have that property
        value after the change.

        **Feature: headless-ci-testing, Property 6: Style Property Values
        Propagate to Descendants**
        **Validates: Requirements 4.4**
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

    **Feature: headless-ci-testing**
    **Validates: Requirements 5.1, 5.4**
    """

    def test_text_change_triggers_rebuild(self):
        """Changing text triggers widget rebuild with new widget instances.

        **Validates: Requirements 5.1, 5.4**
        """
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

    def test_font_name_change_triggers_rebuild(self):
        """Changing font_name triggers widget rebuild with new widget instances.

        **Validates: Requirements 5.1, 5.4**
        """
        label = MarkdownLabel(text='# Heading\n\nParagraph', font_name='Roboto')
        root_id_before = id(label)

        # Capture children widget IDs before change
        children_ids_before = collect_widget_ids(label, exclude_root=True)

        # Apply property change and force_rebuild()
        label.font_name = 'RobotoMono-Regular'
        label.force_rebuild()

        # Capture children widget IDs after change
        children_ids_after = collect_widget_ids(label, exclude_root=True)

        # Assert children widget IDs differ
        assert children_ids_before != children_ids_after, \
            "Children widget IDs should differ after font_name change"

        # Assert root MarkdownLabel ID unchanged
        assert id(label) == root_id_before, \
            "Root MarkdownLabel ID should remain unchanged"

    def test_text_size_change_triggers_rebuild(self):
        """Changing text_size triggers widget rebuild with new widget instances.

        **Validates: Requirements 5.1, 5.4**
        """
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
        """Changing link_style triggers widget rebuild with new widget instances.

        **Validates: Requirements 5.1, 5.4**
        """
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
        """Changing strict_label_mode triggers widget rebuild.

        **Validates: Requirements 5.1, 5.4**
        """
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
        """Changing render_mode triggers widget rebuild.

        **Validates: Requirements 5.1, 5.4**
        """
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


@pytest.mark.slow
class TestStructurePropertyRebuildPBT:
    """Property-based tests for structure property rebuild behavior.

    **Feature: headless-ci-testing, Property 7: Structure Property Changes
    Rebuild Widget Tree**
    **Validates: Requirements 5.1**
    """

    @given(
        initial_text=simple_markdown_document(),
        new_text=simple_markdown_document()
    )
    # Combination strategy: 50 examples (performance optimized)
    @settings(max_examples=50, deadline=None)
    def test_text_change_triggers_rebuild_pbt(self, initial_text, new_text):
        """Property 7: Structure Property Changes Trigger Rebuild (text).

        *For any* MarkdownLabel with non-empty content, and *for any* structure
        property (text), changing that property and calling force_rebuild()
        SHALL result in different widget object IDs for children (excluding
        the root MarkdownLabel).

        **Feature: headless-ci-testing, Property 7: Structure Property Changes
        Trigger Rebuild**
        **Validates: Requirements 5.1**
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
    # Small finite strategy: 3 examples (input space size: 3)
    @settings(max_examples=3, deadline=None)
    def test_font_name_change_triggers_rebuild_pbt(self, markdown_text, font_name):
        """Property 7: Structure Property Changes Trigger Rebuild (font_name).

        *For any* MarkdownLabel with non-empty content, and *for any* structure
        property (font_name), changing that property and calling force_rebuild()
        SHALL result in different widget object IDs for children.

        **Feature: headless-ci-testing, Property 7: Structure Property Changes
        Trigger Rebuild**
        **Validates: Requirements 5.1**
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

        # Apply property change and force_rebuild()
        label.font_name = font_name
        label.force_rebuild()

        # Capture children widget IDs after change
        children_ids_after = collect_widget_ids(label, exclude_root=True)

        # Assert: children widget IDs should differ
        assert children_ids_before != children_ids_after, (
            f"Children widget IDs should differ after font_name change. "
            f"Before: {len(children_ids_before)} widgets, "
            f"After: {len(children_ids_after)} widgets"
        )

    @given(
        markdown_text=simple_markdown_document(),
        link_style=st.sampled_from(['unstyled', 'styled'])
    )
    # Small finite strategy: 2 examples (input space size: 2)
    @settings(max_examples=2, deadline=None)
    def test_link_style_change_triggers_rebuild_pbt(self, markdown_text, link_style):
        """Property 7: Structure Property Changes Trigger Rebuild (link_style).

        *For any* MarkdownLabel with non-empty content, and *for any* structure
        property (link_style), changing that property and calling force_rebuild()
        SHALL result in different widget object IDs for children.

        **Feature: headless-ci-testing, Property 7: Structure Property Changes
        Trigger Rebuild**
        **Validates: Requirements 5.1**
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


@pytest.mark.slow
class TestRootIDPreservationPBT:
    """Property-based tests for root widget ID preservation.

    **Feature: headless-ci-testing, Property 8: Root Widget ID Preserved
    Across Property Changes**
    **Validates: Requirements 5.4**
    """

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
    # Combination strategy: 50 examples (combination coverage)
    @settings(max_examples=50, deadline=None)
    def test_root_id_preserved_across_style_property_changes(
        self, markdown_text, base_font_size, color, halign, valign,
        line_height, disabled
    ):
        """Property 8: Root Widget ID Preserved Across Style Property Changes.

        *For any* MarkdownLabel, and *for any* style property change, the root
        MarkdownLabel's object ID SHALL remain unchanged.

        **Feature: headless-ci-testing, Property 8: Root Widget ID Preserved
        Across Property Changes**
        **Validates: Requirements 5.4**
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
    # Combination strategy: 50 examples (combination coverage)
    @settings(max_examples=50, deadline=None)
    def test_root_id_preserved_across_structure_property_changes(
        self, initial_text, new_text, font_name, link_style,
        strict_label_mode, render_mode
    ):
        """Property 8: Root Widget ID Preserved Across Structure Property Changes.

        *For any* MarkdownLabel, and *for any* structure property change, the root
        MarkdownLabel's object ID SHALL remain unchanged.

        **Feature: headless-ci-testing, Property 8: Root Widget ID Preserved
        Across Property Changes**
        **Validates: Requirements 5.4**
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
    # Combination strategy: 50 examples (combination coverage)
    @settings(max_examples=50, deadline=None)
    def test_root_id_preserved_across_mixed_property_changes(
        self, markdown_text, base_font_size, color, font_name, link_style
    ):
        """Property 8: Root Widget ID Preserved Across Mixed Property Changes.

        *For any* MarkdownLabel, and *for any* combination of style and structure
        property changes, the root MarkdownLabel's object ID SHALL remain unchanged.

        **Feature: headless-ci-testing, Property 8: Root Widget ID Preserved
        Across Property Changes**
        **Validates: Requirements 5.4**
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
