"""
Structure property rebuild tests for MarkdownLabel.

This module contains tests that verify structure property changes trigger
widget tree rebuilds with new widget instances, while preserving the root
MarkdownLabel ID.

Tests are designed to run in headless CI environments without requiring a Kivy window.
"""

import pytest
from hypothesis import given, strategies as st, settings, assume

from kivy_garden.markdownlabel import MarkdownLabel
from .test_utils import (
    simple_markdown_document,
    collect_widget_ids
)


class TestStructurePropertyRebuild:
    """Tests for structure property changes rebuilding the widget tree.

    These tests verify that changing structure properties (text,
    link_style, strict_label_mode, render_mode) rebuilds the widget
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
        link_style=st.sampled_from(['unstyled', 'styled'])
    )
    # Mixed finite/complex strategy: 10 examples (2 finite × 5 complex samples)
    @settings(max_examples=10, deadline=None)
    def test_link_style_change_triggers_rebuild_pbt(self, markdown_text, link_style):
        """
        *For any* MarkdownLabel with non-empty content, and *for any* structure
        property (link_style), changing that property and calling force_rebuild
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
