"""
Performance and efficiency tests for MarkdownLabel widget.

This module contains tests that verify performance-related behaviors including
efficient style updates, batched rebuilds, deferred rebuild scheduling, and
content clipping behavior.
"""

import os
# Set environment variable to use headless mode for Kivy
os.environ['KIVY_NO_ARGS'] = '1'
os.environ['KIVY_NO_CONSOLELOG'] = '1'

import pytest
from hypothesis import given, strategies as st, settings, assume

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout

from kivy_garden.markdownlabel import MarkdownLabel
from .test_utils import (
    markdown_heading, markdown_paragraph, markdown_bold, markdown_italic,
    markdown_link, simple_markdown_document, color_strategy, text_padding_strategy,
    find_labels_recursive, colors_equal, padding_equal, floats_equal, KIVY_FONTS
)

class TestEfficientStyleUpdates:
    """Property tests for efficient style updates (Property 7).
    
    Tests verify that style-only property changes update descendant widgets
    in place without rebuilding the widget tree, while structure property
    changes trigger a full rebuild.
    """
    
    def _collect_widget_ids(self, widget):
        """Collect Python object ids of all widgets in the tree.
        
        Args:
            widget: Root widget to collect from
            
        Returns:
            Set of widget object ids
        """
        ids = {id(widget)}
        if hasattr(widget, 'children'):
            for child in widget.children:
                ids.update(self._collect_widget_ids(child))
        return ids
    
    def _find_labels_recursive(self, widget):
        """Find all Label widgets recursively.
        
        Args:
            widget: Root widget to search from
            
        Returns:
            List of Label widgets
        """
        labels = []
        if isinstance(widget, Label):
            labels.append(widget)
        if hasattr(widget, 'children'):
            for child in widget.children:
                labels.extend(self._find_labels_recursive(child))
        return labels
    
    @given(st.floats(min_value=10, max_value=50, allow_nan=False, allow_infinity=False),
           st.floats(min_value=10, max_value=50, allow_nan=False, allow_infinity=False))
    @settings(max_examples=100, deadline=None)
    def test_font_size_change_preserves_widget_tree(self, initial_size, new_size):
        """Changing font_size preserves widget tree structure (widget identities).
        
        **Feature: label-compatibility-phase2, Property 7: Efficient Style Updates**
        **Validates: Requirements 7.1**
        """
        assume(initial_size != new_size)
        
        # Create label with some content
        markdown = '# Heading\n\nParagraph text here.'
        label = MarkdownLabel(text=markdown, font_size=initial_size)
        
        # Collect widget ids before change
        ids_before = self._collect_widget_ids(label)
        
        # Change font_size (style-only property)
        label.font_size = new_size
        
        # Collect widget ids after change
        ids_after = self._collect_widget_ids(label)
        
        # Widget tree structure should be preserved (same widget objects)
        assert ids_before == ids_after, \
            f"Widget tree changed after font_size update. Before: {len(ids_before)}, After: {len(ids_after)}"
    
    @given(st.tuples(
        st.floats(min_value=0, max_value=1, allow_nan=False, allow_infinity=False),
        st.floats(min_value=0, max_value=1, allow_nan=False, allow_infinity=False),
        st.floats(min_value=0, max_value=1, allow_nan=False, allow_infinity=False),
        st.floats(min_value=0, max_value=1, allow_nan=False, allow_infinity=False)
    ))
    @settings(max_examples=100, deadline=None)
    def test_color_change_preserves_widget_tree(self, new_color):
        """Changing color preserves widget tree structure (widget identities).
        
        **Feature: label-compatibility-phase2, Property 7: Efficient Style Updates**
        **Validates: Requirements 7.1**
        """
        # Create label with some content
        markdown = 'Simple paragraph text.'
        label = MarkdownLabel(text=markdown, color=[1, 1, 1, 1])
        
        # Collect widget ids before change
        ids_before = self._collect_widget_ids(label)
        
        # Change color (style-only property)
        label.color = list(new_color)
        
        # Collect widget ids after change
        ids_after = self._collect_widget_ids(label)
        
        # Widget tree structure should be preserved
        assert ids_before == ids_after, \
            "Widget tree changed after color update"
    
    @given(st.tuples(
        st.floats(min_value=0, max_value=1, allow_nan=False, allow_infinity=False),
        st.floats(min_value=0, max_value=1, allow_nan=False, allow_infinity=False),
        st.floats(min_value=0, max_value=1, allow_nan=False, allow_infinity=False),
        st.floats(min_value=0, max_value=1, allow_nan=False, allow_infinity=False)
    ))
    @settings(max_examples=100, deadline=None)
    def test_color_change_updates_descendant_labels(self, new_color):
        """Changing color updates all descendant Label widgets.
        
        **Feature: label-compatibility-phase2, Property 7: Efficient Style Updates**
        **Validates: Requirements 7.1**
        """
        # Create label with some content
        markdown = '# Heading\n\nParagraph text.'
        label = MarkdownLabel(text=markdown, color=[1, 1, 1, 1])
        
        # Change color
        new_color_list = list(new_color)
        label.color = new_color_list
        
        # All descendant labels should have the new color
        child_labels = self._find_labels_recursive(label)
        assert len(child_labels) >= 1, "Expected at least one child Label"
        
        for child_label in child_labels:
            assert list(child_label.color) == new_color_list, \
                f"Expected color {new_color_list}, got {list(child_label.color)}"
    
    @given(st.sampled_from(['left', 'center', 'right', 'justify']))
    @settings(max_examples=100, deadline=None)
    def test_halign_change_preserves_widget_tree(self, new_halign):
        """Changing halign preserves widget tree structure (widget identities).
        
        **Feature: label-compatibility-phase2, Property 7: Efficient Style Updates**
        **Validates: Requirements 7.1**
        """
        # Create label with some content
        markdown = 'Paragraph text for alignment test.'
        label = MarkdownLabel(text=markdown, halign='left')
        
        # Collect widget ids before change
        ids_before = self._collect_widget_ids(label)
        
        # Change halign (style-only property)
        label.halign = new_halign
        
        # Collect widget ids after change
        ids_after = self._collect_widget_ids(label)
        
        # Widget tree structure should be preserved
        assert ids_before == ids_after, \
            "Widget tree changed after halign update"
    
    @given(st.sampled_from(['left', 'center', 'right', 'justify']))
    @settings(max_examples=100, deadline=None)
    def test_halign_change_updates_descendant_labels(self, new_halign):
        """Changing halign updates all descendant Label widgets.
        
        **Feature: label-compatibility-phase2, Property 7: Efficient Style Updates**
        **Validates: Requirements 7.1**
        """
        # Create label with some content
        markdown = '# Heading\n\nParagraph text.'
        label = MarkdownLabel(text=markdown, halign='left')
        
        # Change halign
        label.halign = new_halign
        
        # All descendant labels should have the new halign
        child_labels = self._find_labels_recursive(label)
        assert len(child_labels) >= 1, "Expected at least one child Label"
        
        for child_label in child_labels:
            assert child_label.halign == new_halign, \
                f"Expected halign {new_halign}, got {child_label.halign}"
    
    @given(st.sampled_from(['top', 'middle', 'bottom']))
    @settings(max_examples=100, deadline=None)
    def test_valign_change_preserves_widget_tree(self, new_valign):
        """Changing valign preserves widget tree structure (widget identities).
        
        **Feature: label-compatibility-phase2, Property 7: Efficient Style Updates**
        **Validates: Requirements 7.1**
        """
        # Create label with some content
        markdown = 'Paragraph text for valign test.'
        label = MarkdownLabel(text=markdown, valign='top')
        
        # Collect widget ids before change
        ids_before = self._collect_widget_ids(label)
        
        # Change valign (style-only property)
        label.valign = new_valign
        
        # Collect widget ids after change
        ids_after = self._collect_widget_ids(label)
        
        # Widget tree structure should be preserved
        assert ids_before == ids_after, \
            "Widget tree changed after valign update"
    
    @given(st.sampled_from(['top', 'middle', 'bottom']))
    @settings(max_examples=100, deadline=None)
    def test_valign_change_updates_descendant_labels(self, new_valign):
        """Changing valign updates all descendant Label widgets.
        
        **Feature: label-compatibility-phase2, Property 7: Efficient Style Updates**
        **Validates: Requirements 7.1**
        """
        # Create label with some content
        markdown = '# Heading\n\nParagraph text.'
        label = MarkdownLabel(text=markdown, valign='top')
        
        # Change valign
        label.valign = new_valign
        
        # All descendant labels should have the new valign
        child_labels = self._find_labels_recursive(label)
        assert len(child_labels) >= 1, "Expected at least one child Label"
        
        for child_label in child_labels:
            assert child_label.valign == new_valign, \
                f"Expected valign {new_valign}, got {child_label.valign}"
    
    @given(st.floats(min_value=0.5, max_value=3.0, allow_nan=False, allow_infinity=False))
    @settings(max_examples=100, deadline=None)
    def test_line_height_change_preserves_widget_tree(self, new_line_height):
        """Changing line_height preserves widget tree structure (widget identities).
        
        **Feature: label-compatibility-phase2, Property 7: Efficient Style Updates**
        **Validates: Requirements 7.1**
        """
        # Create label with some content
        markdown = 'Paragraph text for line height test.'
        label = MarkdownLabel(text=markdown, line_height=1.0)
        
        # Collect widget ids before change
        ids_before = self._collect_widget_ids(label)
        
        # Change line_height (style-only property)
        label.line_height = new_line_height
        
        # Collect widget ids after change
        ids_after = self._collect_widget_ids(label)
        
        # Widget tree structure should be preserved
        assert ids_before == ids_after, \
            "Widget tree changed after line_height update"
    
    @given(st.floats(min_value=0.5, max_value=3.0, allow_nan=False, allow_infinity=False))
    @settings(max_examples=100, deadline=None)
    def test_line_height_change_updates_descendant_labels(self, new_line_height):
        """Changing line_height updates all descendant Label widgets.
        
        **Feature: label-compatibility-phase2, Property 7: Efficient Style Updates**
        **Validates: Requirements 7.1**
        """
        # Create label with some content
        markdown = '# Heading\n\nParagraph text.'
        label = MarkdownLabel(text=markdown, line_height=1.0)
        
        # Change line_height
        label.line_height = new_line_height
        
        # All descendant labels should have the new line_height
        child_labels = self._find_labels_recursive(label)
        assert len(child_labels) >= 1, "Expected at least one child Label"
        
        for child_label in child_labels:
            assert child_label.line_height == new_line_height, \
                f"Expected line_height {new_line_height}, got {child_label.line_height}"
    
    @given(st.booleans())
    @settings(max_examples=100, deadline=None)
    def test_disabled_change_preserves_widget_tree(self, new_disabled):
        """Changing disabled preserves widget tree structure (widget identities).
        
        **Feature: label-compatibility-phase2, Property 7: Efficient Style Updates**
        **Validates: Requirements 7.1**
        """
        # Create label with some content
        markdown = 'Paragraph text for disabled test.'
        label = MarkdownLabel(text=markdown, disabled=False)
        
        # Collect widget ids before change
        ids_before = self._collect_widget_ids(label)
        
        # Change disabled (style-only property)
        label.disabled = new_disabled
        
        # Collect widget ids after change
        ids_after = self._collect_widget_ids(label)
        
        # Widget tree structure should be preserved
        assert ids_before == ids_after, \
            "Widget tree changed after disabled update"
    
    def test_text_change_rebuilds_widget_tree(self):
        """Changing text (structure property) rebuilds the widget tree.
        
        **Feature: label-compatibility-phase2, Property 7: Efficient Style Updates**
        **Validates: Requirements 7.2**
        """
        # Create label with some content
        markdown1 = 'First paragraph.'
        label = MarkdownLabel(text=markdown1)
        
        # Collect widget ids before change
        ids_before = self._collect_widget_ids(label)
        
        # Change text (structure property) - use force_rebuild() for immediate
        # update since text changes now use deferred rebuilds
        label.text = 'Second paragraph with different content.'
        label.force_rebuild()
        
        # Collect widget ids after change
        ids_after = self._collect_widget_ids(label)
        
        # Widget tree should be rebuilt (different widget objects)
        # The MarkdownLabel itself stays the same, but children change
        children_before = ids_before - {id(label)}
        children_after = ids_after - {id(label)}
        
        assert children_before != children_after, \
            "Widget tree should be rebuilt after text change"
    
    def test_font_name_change_rebuilds_widget_tree(self):
        """Changing font_name (structure property) rebuilds the widget tree.
        
        **Feature: label-compatibility-phase2, Property 7: Efficient Style Updates**
        **Validates: Requirements 7.3**
        """
        # Create label with some content
        markdown = 'Paragraph text.'
        label = MarkdownLabel(text=markdown, font_name='Roboto')
        
        # Collect widget ids before change
        ids_before = self._collect_widget_ids(label)
        
        # Change font_name (structure property)
        label.font_name = 'RobotoMono-Regular'
        label.force_rebuild()  # Force immediate rebuild for test
        
        # Collect widget ids after change
        ids_after = self._collect_widget_ids(label)
        
        # Widget tree should be rebuilt (different widget objects)
        children_before = ids_before - {id(label)}
        children_after = ids_after - {id(label)}
        
        assert children_before != children_after, \
            "Widget tree should be rebuilt after font_name change"
    
    @given(
        st.floats(min_value=10, max_value=30, allow_nan=False, allow_infinity=False),
        st.tuples(
            st.floats(min_value=0, max_value=1, allow_nan=False, allow_infinity=False),
            st.floats(min_value=0, max_value=1, allow_nan=False, allow_infinity=False),
            st.floats(min_value=0, max_value=1, allow_nan=False, allow_infinity=False),
            st.floats(min_value=0, max_value=1, allow_nan=False, allow_infinity=False)
        ),
        st.sampled_from(['left', 'center', 'right']),
        st.sampled_from(['top', 'middle', 'bottom']),
        st.floats(min_value=0.8, max_value=2.0, allow_nan=False, allow_infinity=False)
    )
    @settings(max_examples=100, deadline=None)
    def test_multiple_style_changes_preserve_widget_tree(self, font_size, color, 
                                                          halign, valign, line_height):
        """Multiple style-only property changes preserve widget tree structure.
        
        **Feature: label-compatibility-phase2, Property 7: Efficient Style Updates**
        **Validates: Requirements 7.1**
        """
        # Create label with some content
        markdown = '# Heading\n\nParagraph text here.'
        label = MarkdownLabel(text=markdown)
        
        # Collect widget ids before changes
        ids_before = self._collect_widget_ids(label)
        
        # Apply multiple style changes
        label.font_size = font_size
        label.color = list(color)
        label.halign = halign
        label.valign = valign
        label.line_height = line_height
        
        # Collect widget ids after changes
        ids_after = self._collect_widget_ids(label)
        
        # Widget tree structure should be preserved through all changes
        assert ids_before == ids_after, \
            "Widget tree changed after multiple style updates"
    
    @given(
        st.tuples(
            st.floats(min_value=0, max_value=1, allow_nan=False, allow_infinity=False),
            st.floats(min_value=0, max_value=1, allow_nan=False, allow_infinity=False),
            st.floats(min_value=0, max_value=1, allow_nan=False, allow_infinity=False),
            st.floats(min_value=0, max_value=1, allow_nan=False, allow_infinity=False)
        ),
        st.tuples(
            st.floats(min_value=0, max_value=1, allow_nan=False, allow_infinity=False),
            st.floats(min_value=0, max_value=1, allow_nan=False, allow_infinity=False),
            st.floats(min_value=0, max_value=1, allow_nan=False, allow_infinity=False),
            st.floats(min_value=0, max_value=1, allow_nan=False, allow_infinity=False)
        )
    )
    @settings(max_examples=100, deadline=None)
    def test_disabled_color_switching(self, normal_color, disabled_color):
        """Disabled state correctly switches between color and disabled_color.
        
        **Feature: label-compatibility-phase2, Property 7: Efficient Style Updates**
        **Validates: Requirements 7.1**
        """
        # Create label with some content
        markdown = 'Paragraph text.'
        label = MarkdownLabel(
            text=markdown, 
            color=list(normal_color),
            disabled_color=list(disabled_color),
            disabled=False
        )
        
        # Get child labels
        child_labels = self._find_labels_recursive(label)
        assert len(child_labels) >= 1, "Expected at least one child Label"
        
        # Initially should use normal color
        for child_label in child_labels:
            assert list(child_label.color) == list(normal_color), \
                f"Expected normal color {list(normal_color)}, got {list(child_label.color)}"
        
        # Enable disabled state
        label.disabled = True
        
        # Should now use disabled_color
        for child_label in child_labels:
            assert list(child_label.color) == list(disabled_color), \
                f"Expected disabled color {list(disabled_color)}, got {list(child_label.color)}"
        
        # Disable disabled state
        label.disabled = False
        
        # Should return to normal color
        for child_label in child_labels:
            assert list(child_label.color) == list(normal_color), \
                f"Expected normal color {list(normal_color)}, got {list(child_label.color)}"


class TestBatchedRebuilds:
    """Property tests for batched rebuilds (Property 6).
    
    **Feature: label-compatibility, Property 6: Batched rebuilds**
    **Validates: Requirements 3.1, 3.3**
    
    Tests verify that multiple property changes within the same frame
    result in at most one rebuild operation.
    """
    
    @given(st.integers(min_value=2, max_value=5))
    @settings(max_examples=100, deadline=None)
    def test_multiple_text_changes_batch_to_single_rebuild(self, num_changes):
        """Multiple text changes within same frame batch to single rebuild.
        
        **Feature: label-compatibility, Property 6: Batched rebuilds**
        **Validates: Requirements 3.1, 3.3**
        """
        label = MarkdownLabel(text='Initial text')
        
        # Track rebuild calls by patching _rebuild_widgets
        rebuild_count = [0]
        original_rebuild = label._rebuild_widgets
        
        def counting_rebuild():
            rebuild_count[0] += 1
            original_rebuild()
        
        label._rebuild_widgets = counting_rebuild
        
        # Make multiple text changes (these should be batched)
        for i in range(num_changes):
            label.text = f'Text change {i}'
        
        # Before force_rebuild, no rebuilds should have happened yet
        # (they're deferred to next frame)
        assert rebuild_count[0] == 0, \
            f"Expected 0 rebuilds before frame tick, got {rebuild_count[0]}"
        
        # Force the rebuild to execute
        label.force_rebuild()
        
        # Should have exactly 1 rebuild (from force_rebuild)
        assert rebuild_count[0] == 1, \
            f"Expected exactly 1 rebuild after force_rebuild, got {rebuild_count[0]}"
    
    @given(
        st.text(min_size=1, max_size=20, alphabet=st.characters(
            whitelist_categories=['L', 'N'],
            blacklist_characters='#[]&\n\r'
        )),
        st.floats(min_value=10, max_value=30, allow_nan=False, allow_infinity=False),
        st.sampled_from(['Roboto', 'RobotoMono-Regular'])
    )
    @settings(max_examples=100, deadline=None)
    def test_mixed_property_changes_batch_rebuilds(self, text, font_size, font_name):
        """Mixed structure property changes batch into single rebuild.
        
        **Feature: label-compatibility, Property 6: Batched rebuilds**
        **Validates: Requirements 3.1, 3.3**
        """
        label = MarkdownLabel(text='Initial')
        
        # Track rebuild calls
        rebuild_count = [0]
        original_rebuild = label._rebuild_widgets
        
        def counting_rebuild():
            rebuild_count[0] += 1
            original_rebuild()
        
        label._rebuild_widgets = counting_rebuild
        
        # Make multiple structure property changes
        label.text = text
        label.font_name = font_name
        # Note: font_size is a style-only property, doesn't trigger rebuild
        
        # Before force_rebuild, no rebuilds should have happened
        assert rebuild_count[0] == 0, \
            f"Expected 0 rebuilds before frame tick, got {rebuild_count[0]}"
        
        # Force the rebuild
        label.force_rebuild()
        
        # Should have exactly 1 rebuild
        assert rebuild_count[0] == 1, \
            f"Expected exactly 1 rebuild, got {rebuild_count[0]}"
    
    def test_pending_rebuild_flag_prevents_duplicate_scheduling(self):
        """_pending_rebuild flag prevents duplicate rebuild scheduling.
        
        **Feature: label-compatibility, Property 6: Batched rebuilds**
        **Validates: Requirements 3.1, 3.3**
        """
        label = MarkdownLabel(text='Initial')
        
        # Clear any pending state
        label._pending_rebuild = False
        
        # Schedule multiple rebuilds
        label._schedule_rebuild()
        assert label._pending_rebuild is True, \
            "Expected _pending_rebuild to be True after first schedule"
        
        label._schedule_rebuild()
        assert label._pending_rebuild is True, \
            "Expected _pending_rebuild to remain True after second schedule"
        
        label._schedule_rebuild()
        assert label._pending_rebuild is True, \
            "Expected _pending_rebuild to remain True after third schedule"
        
        # Force rebuild clears the flag
        label.force_rebuild()
        assert label._pending_rebuild is False, \
            "Expected _pending_rebuild to be False after force_rebuild"


class TestDeferredRebuildScheduling:
    """Property tests for deferred rebuild scheduling (Property 7).
    
    **Feature: label-compatibility, Property 7: Deferred rebuild scheduling**
    **Validates: Requirements 3.2**
    
    Tests verify that property changes trigger deferred rebuilds via
    Clock.create_trigger rather than synchronous rebuilds.
    """
    
    @given(st.text(min_size=1, max_size=50, alphabet=st.characters(
        whitelist_categories=['L', 'N'],
        blacklist_characters='#[]&\n\r'
    )))
    @settings(max_examples=100, deadline=None)
    def test_text_change_schedules_deferred_rebuild(self, new_text):
        """Text property change schedules deferred rebuild, not synchronous.
        
        **Feature: label-compatibility, Property 7: Deferred rebuild scheduling**
        **Validates: Requirements 3.2**
        """
        label = MarkdownLabel(text='Initial text')
        initial_children = list(label.children)
        
        # Change text - this should schedule a deferred rebuild
        label.text = new_text
        
        # Immediately after setting text, children should still be the same
        # (rebuild hasn't executed yet because it's deferred)
        assert label._pending_rebuild is True, \
            "Expected _pending_rebuild to be True after text change"
        
        # The children should still be the initial ones (deferred, not immediate)
        # Note: We compare by checking the rebuild hasn't happened yet
        assert label._pending_rebuild is True, \
            "Rebuild should be pending, not executed synchronously"
    
    @given(st.sampled_from(['Roboto', 'RobotoMono-Regular', 'Arial']))
    @settings(max_examples=100, deadline=None)
    def test_font_name_change_schedules_deferred_rebuild(self, font_name):
        """font_name property change schedules deferred rebuild.
        
        **Feature: label-compatibility, Property 7: Deferred rebuild scheduling**
        **Validates: Requirements 3.2**
        """
        # Use a different initial font to ensure the change is detected
        # Use fonts that are known to be available in Kivy
        initial_font = 'RobotoMono-Regular' if font_name != 'RobotoMono-Regular' else 'Roboto'
        label = MarkdownLabel(text='Test content', font_name=initial_font)
        
        # Clear any pending state from initialization
        label._pending_rebuild = False
        
        # Change font_name - this is a structure property that triggers rebuild
        label.font_name = font_name
        
        # Should have scheduled a deferred rebuild
        assert label._pending_rebuild is True, \
            "Expected _pending_rebuild to be True after font_name change"
    
    def test_rebuild_trigger_is_clock_trigger(self):
        """_rebuild_trigger is a Clock.create_trigger instance.
        
        **Feature: label-compatibility, Property 7: Deferred rebuild scheduling**
        **Validates: Requirements 3.2**
        """
        from kivy.clock import ClockEvent
        
        label = MarkdownLabel(text='Test')
        
        # Verify _rebuild_trigger exists and is a clock event
        assert hasattr(label, '_rebuild_trigger'), \
            "Expected _rebuild_trigger attribute"
        assert isinstance(label._rebuild_trigger, ClockEvent), \
            f"Expected ClockEvent, got {type(label._rebuild_trigger)}"
    
    def test_schedule_rebuild_sets_pending_flag(self):
        """_schedule_rebuild() sets _pending_rebuild flag.
        
        **Feature: label-compatibility, Property 7: Deferred rebuild scheduling**
        **Validates: Requirements 3.2**
        """
        label = MarkdownLabel(text='Test')
        
        # Clear pending state
        label._pending_rebuild = False
        
        # Call _schedule_rebuild
        label._schedule_rebuild()
        
        # Flag should be set
        assert label._pending_rebuild is True, \
            "Expected _pending_rebuild to be True after _schedule_rebuild()"
    
    def test_do_rebuild_clears_pending_flag(self):
        """_do_rebuild() clears _pending_rebuild flag when executing.
        
        **Feature: label-compatibility, Property 7: Deferred rebuild scheduling**
        **Validates: Requirements 3.2**
        """
        label = MarkdownLabel(text='Test')
        
        # Set pending state
        label._pending_rebuild = True
        
        # Call _do_rebuild (simulating clock callback)
        label._do_rebuild()
        
        # Flag should be cleared
        assert label._pending_rebuild is False, \
            "Expected _pending_rebuild to be False after _do_rebuild()"
    
    def test_do_rebuild_skips_when_not_pending(self):
        """_do_rebuild() skips rebuild when _pending_rebuild is False.
        
        **Feature: label-compatibility, Property 7: Deferred rebuild scheduling**
        **Validates: Requirements 3.2**
        """
        label = MarkdownLabel(text='Test')
        
        # Track rebuild calls
        rebuild_count = [0]
        original_rebuild = label._rebuild_widgets
        
        def counting_rebuild():
            rebuild_count[0] += 1
            original_rebuild()
        
        label._rebuild_widgets = counting_rebuild
        
        # Ensure not pending
        label._pending_rebuild = False
        
        # Call _do_rebuild
        label._do_rebuild()
        
        # Should not have called _rebuild_widgets
        assert rebuild_count[0] == 0, \
            f"Expected 0 rebuilds when not pending, got {rebuild_count[0]}"
    
    @given(st.lists(
        st.text(min_size=1, max_size=20, alphabet=st.characters(
            whitelist_categories=['L', 'N'],
            blacklist_characters='#[]&\n\r'
        )),
        min_size=2,
        max_size=5
    ))
    @settings(max_examples=100, deadline=None)
    def test_multiple_changes_all_deferred(self, text_values):
        """Multiple property changes are all deferred until next frame.
        
        **Feature: label-compatibility, Property 7: Deferred rebuild scheduling**
        **Validates: Requirements 3.2**
        """
        label = MarkdownLabel(text='Initial')
        
        # Track rebuild calls
        rebuild_count = [0]
        original_rebuild = label._rebuild_widgets
        
        def counting_rebuild():
            rebuild_count[0] += 1
            original_rebuild()
        
        label._rebuild_widgets = counting_rebuild
        
        # Make multiple text changes
        for text in text_values:
            label.text = text
        
        # No rebuilds should have happened yet (all deferred)
        assert rebuild_count[0] == 0, \
            f"Expected 0 synchronous rebuilds, got {rebuild_count[0]}"
        
        # Pending flag should be set
        assert label._pending_rebuild is True, \
            "Expected _pending_rebuild to be True after multiple changes"


class TestContentClippingWhenHeightConstrained:
    """Property tests for content clipping when height-constrained (Property 1)."""
    
    def _has_clipping_container(self, widget):
        """Check if widget contains a _ClippingContainer (StencilView).
        
        Args:
            widget: Widget to check
            
        Returns:
            bool: True if a clipping container is found
        """
        from kivy.uix.stencilview import StencilView
        
        for child in widget.children:
            if isinstance(child, StencilView):
                return True
        return False
    
    @given(
        st.text(min_size=1, max_size=100, alphabet=st.characters(
            whitelist_categories=['L', 'N', 'P', 'S', 'Z'],
            blacklist_characters='#[]&\n\r*_`~\\'
        )),
        st.floats(min_value=10.0, max_value=500.0, allow_nan=False, allow_infinity=False)
    )
    @settings(max_examples=100, deadline=None)
    def test_text_size_height_enables_clipping(self, text, height):
        """Setting text_size[1] to a value enables content clipping."""
        assume(text.strip())
        
        label = MarkdownLabel(text=text, text_size=[None, height])
        label.force_rebuild()
        
        assert self._has_clipping_container(label), \
            f"Expected clipping container when text_size[1]={height}"
    
    @given(
        st.text(min_size=1, max_size=100, alphabet=st.characters(
            whitelist_categories=['L', 'N', 'P', 'S', 'Z'],
            blacklist_characters='#[]&\n\r*_`~\\'
        )),
        st.floats(min_value=10.0, max_value=500.0, allow_nan=False, allow_infinity=False)
    )
    @settings(max_examples=100, deadline=None)
    def test_strict_label_mode_with_fixed_height_enables_clipping(self, text, height):
        """strict_label_mode=True with size_hint_y=None enables clipping."""
        assume(text.strip())
        
        label = MarkdownLabel(
            text=text,
            strict_label_mode=True,
            size_hint_y=None,
            height=height
        )
        label.force_rebuild()
        
        assert self._has_clipping_container(label), \
            f"Expected clipping container when strict_label_mode=True and height={height}"
    
    @given(
        st.floats(min_value=10.0, max_value=500.0, allow_nan=False, allow_infinity=False)
    )
    @settings(max_examples=100, deadline=None)
    def test_clipping_container_height_matches_text_size(self, height):
        """Clipping container height matches text_size[1]."""
        from kivy.uix.stencilview import StencilView
        
        label = MarkdownLabel(
            text='# Heading\n\nSome paragraph text here.',
            text_size=[None, height]
        )
        label.force_rebuild()
        
        # Find the clipping container
        clipping_container = None
        for child in label.children:
            if isinstance(child, StencilView):
                clipping_container = child
                break
        
        assert clipping_container is not None, "Expected clipping container"
        assert clipping_container.height == height, \
            f"Expected container height={height}, got {clipping_container.height}"
    
    @given(
        st.integers(min_value=1, max_value=6),
        st.floats(min_value=50.0, max_value=200.0, allow_nan=False, allow_infinity=False)
    )
    @settings(max_examples=100, deadline=None)
    def test_heading_content_clipped_when_height_constrained(self, level, height):
        """Heading content is clipped when height is constrained."""
        heading = '#' * level + ' Test Heading'
        
        label = MarkdownLabel(text=heading, text_size=[None, height])
        label.force_rebuild()
        
        assert self._has_clipping_container(label), \
            f"Expected clipping for heading level {level} with height={height}"
    
    def test_clipping_uses_stencil_view(self):
        """Clipping mechanism uses StencilView."""
        from kivy.uix.stencilview import StencilView
        
        label = MarkdownLabel(
            text='Test content',
            text_size=[None, 50]
        )
        label.force_rebuild()
        
        # Verify the clipping container is a StencilView
        found_stencil = False
        for child in label.children:
            if isinstance(child, StencilView):
                found_stencil = True
                break
        
        assert found_stencil, "Expected StencilView for clipping"


class TestNoClippingWhenUnconstrained:
    """Property tests for no clipping when unconstrained (Property 2)."""
    
    def _has_clipping_container(self, widget):
        """Check if widget contains a _ClippingContainer (StencilView).
        
        Args:
            widget: Widget to check
            
        Returns:
            bool: True if a clipping container is found
        """
        from kivy.uix.stencilview import StencilView
        
        for child in widget.children:
            if isinstance(child, StencilView):
                return True
        return False
    
    @given(
        st.text(min_size=1, max_size=100, alphabet=st.characters(
            whitelist_categories=['L', 'N', 'P', 'S', 'Z'],
            blacklist_characters='#[]&\n\r*_`~\\'
        ))
    )
    @settings(max_examples=100, deadline=None)
    def test_no_clipping_when_text_size_height_none(self, text):
        """No clipping when text_size[1] is None."""
        assume(text.strip())
        
        label = MarkdownLabel(text=text, text_size=[None, None])
        label.force_rebuild()
        
        assert not self._has_clipping_container(label), \
            "Expected no clipping container when text_size[1] is None"
    
    @given(
        st.text(min_size=1, max_size=100, alphabet=st.characters(
            whitelist_categories=['L', 'N', 'P', 'S', 'Z'],
            blacklist_characters='#[]&\n\r*_`~\\'
        ))
    )
    @settings(max_examples=100, deadline=None)
    def test_no_clipping_when_strict_label_mode_false(self, text):
        """No clipping when strict_label_mode is False (default)."""
        assume(text.strip())
        
        label = MarkdownLabel(text=text, strict_label_mode=False)
        label.force_rebuild()
        
        assert not self._has_clipping_container(label), \
            "Expected no clipping container when strict_label_mode=False"
    
    @given(
        st.text(min_size=1, max_size=100, alphabet=st.characters(
            whitelist_categories=['L', 'N', 'P', 'S', 'Z'],
            blacklist_characters='#[]&\n\r*_`~\\'
        ))
    )
    @settings(max_examples=100, deadline=None)
    def test_content_added_directly_when_unconstrained(self, text):
        """Content is added directly to MarkdownLabel when unconstrained."""
        assume(text.strip())
        
        label = MarkdownLabel(text=text)
        label.force_rebuild()
        
        # Children should be Labels or other content widgets, not StencilView
        from kivy.uix.stencilview import StencilView
        
        for child in label.children:
            assert not isinstance(child, StencilView), \
                "Content should be added directly, not wrapped in StencilView"
    
    @given(
        st.integers(min_value=1, max_value=6)
    )
    @settings(max_examples=100, deadline=None)
    def test_heading_expands_naturally_when_unconstrained(self, level):
        """Heading content expands naturally when unconstrained."""
        heading = '#' * level + ' Test Heading'
        
        label = MarkdownLabel(text=heading)
        label.force_rebuild()
        
        assert not self._has_clipping_container(label), \
            f"Expected no clipping for heading level {level} when unconstrained"
    
    def test_default_settings_no_clipping(self):
        """Default MarkdownLabel settings do not enable clipping."""
        label = MarkdownLabel(text='Test content')
        label.force_rebuild()
        
        assert not self._has_clipping_container(label), \
            "Default settings should not enable clipping"
    
    @given(
        st.floats(min_value=100.0, max_value=500.0, allow_nan=False, allow_infinity=False)
    )
    @settings(max_examples=100, deadline=None)
    def test_text_size_width_only_no_clipping(self, width):
        """Setting only text_size width (not height) does not enable clipping."""
        label = MarkdownLabel(
            text='Test content',
            text_size=[width, None]
        )
        label.force_rebuild()
        
        assert not self._has_clipping_container(label), \
            f"Expected no clipping when only text_size width={width} is set"

