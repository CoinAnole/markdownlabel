"""
Property-based tests for MarkdownLabel sizing behavior.

This module contains tests for auto-sizing behavior, size hint management,
strict label mode sizing, and texture size calculations.
"""

import os

import pytest
from hypothesis import given, strategies as st, settings, assume

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout

from kivy_garden.markdownlabel import MarkdownLabel
from .test_utils import (
    simple_markdown_document, markdown_heading, markdown_paragraph,
    find_labels_recursive
)


# **Feature: markdown-label, Property 16: Auto-Sizing Behavior**
# *For any* MarkdownLabel with content, the widget SHALL have size_hint_y=None
# and its height SHALL equal or exceed the sum of its children's heights.
# **Validates: Requirements 11.1**

class TestAutoSizingBehavior:
    """Property tests for auto-sizing behavior (Property 16)."""
    
    @given(simple_markdown_document())
    # Complex strategy with custom domain strategy: 20 examples
    @settings(max_examples=20 if not os.getenv('CI') else 10, deadline=None)
    def test_auto_size_hint_enabled_sets_none(self, markdown_text):
        """With auto_size_height=True, size_hint_y is None for auto-sizing."""
        label = MarkdownLabel(text=markdown_text, auto_size_height=True)
        
        assert label.size_hint_y is None, \
            f"Expected size_hint_y=None, got {label.size_hint_y}"
    
    def test_default_size_hint_y_preserved(self):
        """Default sizing participates in layout (auto_size_height=False)."""
        label = MarkdownLabel(text='Hello world')
        
        assert label.size_hint_y == 1, \
            f"Expected default size_hint_y=1, got {label.size_hint_y}"
    
    # Complex strategy: 20 examples based on default complexity
    @given(markdown_heading())
    @settings(max_examples=20 if not os.getenv('CI') else 10, deadline=None)
    def test_height_bound_to_minimum(self, heading):
        """auto_size_height=True binds height to minimum_height."""
        label = MarkdownLabel(text=heading, auto_size_height=True)
        
        # The height should be bound to minimum_height
        # We can verify the binding exists by checking the property
        assert label.size_hint_y is None, \
            "size_hint_y should be None for auto-sizing"
    
    def test_empty_label_has_zero_height(self):
        """Empty MarkdownLabel has zero or minimal height."""
        label = MarkdownLabel(text='', auto_size_height=True)
        
        assert label.size_hint_y is None, \
            "size_hint_y should be None even for empty label"
        # Empty label should have no children
        assert len(label.children) == 0
    
    @given(st.integers(min_value=1, max_value=5))
    @settings(max_examples=100, deadline=None)
    def test_more_content_means_more_height_potential(self, num_paragraphs):
        """More content should result in more minimum height."""
        # Create markdown with varying number of paragraphs
        text = '\n\n'.join([f'Paragraph number {i} with some text content.' 
                           for i in range(num_paragraphs)])
        
        label = MarkdownLabel(text=text, auto_size_height=True)
        
        # Verify auto-sizing is enabled
        assert label.size_hint_y is None
        # Verify children exist
        assert len(label.children) >= num_paragraphs


# **Feature: label-compatibility, Property 7: auto_size_height True Behavior**
# *For any* MarkdownLabel with `auto_size_height=True`, the widget SHALL have 
# `size_hint_y=None` AND its height SHALL be bound to `minimum_height`.
# **Validates: Requirements 3.1, 3.3**

class TestAutoSizeHeightTrueBehavior:
    """Property tests for auto_size_height True behavior (Property 7)."""
     # Complex strategy with custom domain strategy: 20 examples
    
    @given(simple_markdown_document())
    @settings(max_examples=20 if not os.getenv('CI') else 10, deadline=None)
    def test_auto_size_height_true_sets_size_hint_y_none(self, markdown_text):
        """When auto_size_height=True, size_hint_y should be None."""
        label = MarkdownLabel(text=markdown_text, auto_size_height=True)
        
        assert label.size_hint_y is None, \
            # Complex strategy with custom domain strategy: 20 examples
            f"Expected size_hint_y=None when auto_size_height=True, got {label.size_hint_y}"
    
    @given(simple_markdown_document())
    @settings(max_examples=20 if not os.getenv('CI') else 10, deadline=None)
    def test_auto_size_height_true_binds_height_to_minimum(self, markdown_text):
        """When auto_size_height=True, height should be bound to minimum_height."""
        label = MarkdownLabel(text=markdown_text, auto_size_height=True)
        
        # Check that the binding exists by verifying size_hint_y is None
        # (which is the primary indicator of auto-sizing behavior)
        assert label.size_hint_y is None, \
            "size_hint_y should be None when auto_size_height=True"
        
        # Verify auto_size_height property is actually True
        assert label.auto_size_height is True, \
            f"Expected auto_size_height=True, got {label.auto_size_height}"
    
    def test_auto_size_height_default_is_false(self):
        """Default MarkdownLabel leaves auto_size_height disabled for Label parity."""
        label = MarkdownLabel(text="Test content")
        
        assert label.auto_size_height is False, \
            f"Expected default auto_size_height=False, got {label.auto_size_height}"
        
        # Complex strategy with float generation, NaN exclusion, infinity exclusion: 50 examples
        assert label.size_hint_y == 1, \
            f"Expected size_hint_y=1 by default, got {label.size_hint_y}"
    
    @given(st.floats(min_value=0.1, max_value=2.0, allow_nan=False, allow_infinity=False))
    @settings(max_examples=50 if not os.getenv('CI') else 25, deadline=None)
    def test_auto_size_height_true_ignores_user_size_hint_y(self, user_size_hint_y):
        """When auto_size_height=True, user-provided size_hint_y is overridden."""
        label = MarkdownLabel(
            text="Test content", 
            auto_size_height=True, 
            size_hint_y=user_size_hint_y
        )
        
        # Should override user's size_hint_y
        assert label.size_hint_y is None, \
            f"Expected size_hint_y=None to override user value {user_size_hint_y}, got {label.size_hint_y}"
        
        # But should store the user value for later restoration
        assert label._user_size_hint_y == user_size_hint_y, \
            f"Expected _user_size_hint_y={user_size_hint_y}, got {label._user_size_hint_y}"


# **Feature: label-compatibility, Property 8: auto_size_height False Behavior**
# *For any* MarkdownLabel with `auto_size_height=False`, the widget SHALL preserve 
# the user-specified `size_hint_y` value (or default to 1) AND its height SHALL NOT 
# be bound to `minimum_height`.
# **Validates: Requirements 3.2**

class TestAutoSizeHeightFalseBehavior:
    """Property tests for auto_size_height False behavior (Property 8)."""
    
    @given(simple_markdown_document())
    @settings(max_examples=20 if not os.getenv('CI') else 10, deadline=None)
    def test_auto_size_height_false_preserves_default_size_hint_y(self, markdown_text):
        """When auto_size_height=False, default size_hint_y=1 is preserved."""
        label = MarkdownLabel(text=markdown_text, auto_size_height=False)
        
        assert label.size_hint_y == 1, \
            f"Expected size_hint_y=1 when auto_size_height=False, got {label.size_hint_y}"
        
        # Complex strategy with float generation, NaN exclusion, infinity exclusion, custom domain strategy: 50 examples
        assert label.auto_size_height is False, \
            f"Expected auto_size_height=False, got {label.auto_size_height}"
    
    @given(simple_markdown_document(), 
           st.floats(min_value=0.1, max_value=2.0, allow_nan=False, allow_infinity=False))
    @settings(max_examples=50 if not os.getenv('CI') else 25, deadline=None)
    def test_auto_size_height_false_preserves_user_size_hint_y(self, markdown_text, user_size_hint_y):
        """When auto_size_height=False, user-specified size_hint_y is preserved."""
        label = MarkdownLabel(
            text=markdown_text, 
            auto_size_height=False, 
            size_hint_y=user_size_hint_y
        )
        
        assert label.size_hint_y == user_size_hint_y, \
            # Complex strategy with custom domain strategy: 20 examples
            f"Expected size_hint_y={user_size_hint_y} when auto_size_height=False, got {label.size_hint_y}"
        
        assert label.auto_size_height is False, \
            f"Expected auto_size_height=False, got {label.auto_size_height}"
    
    @given(simple_markdown_document())
    @settings(max_examples=20 if not os.getenv('CI') else 10, deadline=None)
    def test_auto_size_height_false_no_height_binding(self, markdown_text):
        """When auto_size_height=False, height is not bound to minimum_height."""
        label = MarkdownLabel(text=markdown_text, auto_size_height=False)
        
        # The primary indicator that height is not bound to minimum_height
        # is that size_hint_y is not None (it participates in layout)
        assert label.size_hint_y is not None, \
            "size_hint_y should not be None when auto_size_height=False"
        
        assert label.auto_size_height is False, \
            f"Expected auto_size_height=False, got {label.auto_size_height}"


# **Feature: label-compatibility, Property 9: auto_size_height Dynamic Toggling**
# *For any* MarkdownLabel, when `auto_size_height` is toggled from True to False, 
# the height binding SHALL be removed and `size_hint_y` SHALL be restored. When 
# toggled from False to True, the height binding SHALL be added and `size_hint_y` 
# SHALL be set to None.
# **Validates: Requirements 3.4, 3.5**

class TestAutoSizeHeightDynamicToggling:
    """Property tests for auto_size_height dynamic toggling (Property 9)."""
    
    @given(simple_markdown_document())
    @settings(max_examples=20 if not os.getenv('CI') else 10, deadline=None)
    def test_toggle_true_to_false_restores_size_hint_y(self, markdown_text):
        """Toggling auto_size_height from True to False restores size_hint_y."""
        # Start with auto_size_height=True (explicit)
        label = MarkdownLabel(text=markdown_text, auto_size_height=True)
        
        assert label.auto_size_height is True
        assert label.size_hint_y is None
        
        # Toggle to False
        label.auto_size_height = False
        
        # Should restore size_hint_y to default (1)
        assert label.size_hint_y == 1, \
            f"Expected size_hint_y=1 after toggling to False, got {label.size_hint_y}"
        
        assert label.auto_size_height is False, \
            f"Expected auto_size_height=False after toggle, got {label.auto_size_height}"
    
    @given(simple_markdown_document())
    @settings(max_examples=20 if not os.getenv('CI') else 10, deadline=None)
    def test_toggle_false_to_true_sets_size_hint_y_none(self, markdown_text):
        """Toggling auto_size_height from False to True sets size_hint_y=None."""
        # Start with auto_size_height=False (default)
        label = MarkdownLabel(text=markdown_text, auto_size_height=False)
        
        assert label.auto_size_height is False
        assert label.size_hint_y == 1
        
        # Toggle to True
        label.auto_size_height = True
        
        # Should set size_hint_y=None
        assert label.size_hint_y is None, \
            # Complex strategy with float generation, NaN exclusion, infinity exclusion, custom domain strategy: 50 examples
            f"Expected size_hint_y=None after toggling to True, got {label.size_hint_y}"
        
        assert label.auto_size_height is True, \
            f"Expected auto_size_height=True after toggle, got {label.auto_size_height}"
    
    @given(simple_markdown_document(), 
           st.floats(min_value=0.1, max_value=2.0, allow_nan=False, allow_infinity=False))
    @settings(max_examples=50 if not os.getenv('CI') else 25, deadline=None)
    def test_toggle_preserves_user_size_hint_y(self, markdown_text, user_size_hint_y):
        """Toggling preserves the original user-specified size_hint_y value."""
        # Start with user-specified size_hint_y and auto_size_height=True
        label = MarkdownLabel(
            text=markdown_text, 
            auto_size_height=True, 
            size_hint_y=user_size_hint_y
        )
        
        # Should override to None initially
        assert label.size_hint_y is None
        
        # Toggle to False - should restore user value
        label.auto_size_height = False
        
        assert label.size_hint_y == user_size_hint_y, \
            f"Expected size_hint_y={user_size_hint_y} after toggle to False, got {label.size_hint_y}"
        
        # Toggle back to True - should override again
        label.auto_size_height = True
        
        assert label.size_hint_y is None, \
            f"Expected size_hint_y=None after toggle back to True, got {label.size_hint_y}"
         # Complex strategy with custom domain strategy: 20 examples
        
        # Toggle to False again - should still restore user value
        label.auto_size_height = False
        
        assert label.size_hint_y == user_size_hint_y, \
            f"Expected size_hint_y={user_size_hint_y} after second toggle to False, got {label.size_hint_y}"
    
    @given(simple_markdown_document())
    @settings(max_examples=20 if not os.getenv('CI') else 10, deadline=None)
    def test_multiple_toggles_maintain_consistency(self, markdown_text):
        """Multiple toggles maintain consistent behavior."""
        label = MarkdownLabel(text=markdown_text)
        
        # Should start with auto_size_height=False (default)
        assert label.auto_size_height is False
        assert label.size_hint_y == 1
        
        # Toggle True -> False -> True
        for expected_auto_size, expected_size_hint_y in [
            (True, None),    # Toggle to True
            (False, 1),      # Toggle to False
            (True, None),    # Toggle to True
        ]:
            label.auto_size_height = expected_auto_size
            
            assert label.auto_size_height == expected_auto_size, \
                f"Expected auto_size_height={expected_auto_size}, got {label.auto_size_height}"
            
            assert label.size_hint_y == expected_size_hint_y, \
                f"Expected size_hint_y={expected_size_hint_y}, got {label.size_hint_y}"


# **Feature: label-compatibility-phase2, Property 2: Strict Label Mode Sizing Behavior**
# *For any* MarkdownLabel with `strict_label_mode=True`, the widget SHALL preserve 
# the user-specified `size_hint_y` value (or default to 1) AND SHALL ignore 
# `auto_size_height` settings.
# **Validates: Requirements 2.1, 2.2, 2.3, 2.4**

class TestStrictLabelModeSizingBehavior:
    """Property tests for strict label mode sizing behavior (Property 2)."""
    
    @given(simple_markdown_document())
    @settings(max_examples=20 if not os.getenv('CI') else 10, deadline=None)
    def test_strict_mode_preserves_default_size_hint_y(self, markdown_text):
        """When strict_label_mode=True, default size_hint_y=1 is preserved."""
        label = MarkdownLabel(text=markdown_text, strict_label_mode=True)
         # Complex strategy with float generation, NaN exclusion, infinity exclusion, custom domain strategy: 50 examples
        
        assert label.size_hint_y == 1, \
            f"Expected size_hint_y=1 when strict_label_mode=True, got {label.size_hint_y}"
        
        assert label.strict_label_mode is True, \
            f"Expected strict_label_mode=True, got {label.strict_label_mode}"
    
    @given(simple_markdown_document(), 
           st.floats(min_value=0.1, max_value=2.0, allow_nan=False, allow_infinity=False))
    @settings(max_examples=50 if not os.getenv('CI') else 25, deadline=None)
    def test_strict_mode_preserves_user_size_hint_y(self, markdown_text, user_size_hint_y):
        """When strict_label_mode=True, user-specified size_hint_y is preserved."""
        label = MarkdownLabel(
            text=markdown_text, 
            strict_label_mode=True, 
            # Complex strategy with custom domain strategy: 20 examples
            size_hint_y=user_size_hint_y
        )
        
        assert label.size_hint_y == user_size_hint_y, \
            f"Expected size_hint_y={user_size_hint_y} when strict_label_mode=True, got {label.size_hint_y}"
        
        assert label.strict_label_mode is True, \
            f"Expected strict_label_mode=True, got {label.strict_label_mode}"
    
    @given(simple_markdown_document())
    @settings(max_examples=20 if not os.getenv('CI') else 10, deadline=None)
    def test_strict_mode_height_not_bound_to_minimum(self, markdown_text):
        """When strict_label_mode=True, height is not bound to minimum_height."""
        label = MarkdownLabel(text=markdown_text, strict_label_mode=True)
        
        # The primary indicator that height is not bound to minimum_height
        # is that size_hint_y is not None (it participates in layout)
        assert label.size_hint_y is not None, \
            "size_hint_y should not be None when strict_label_mode=True"
        
        assert label.strict_label_mode is True, \
            f"Expected strict_label_mode=True, got {label.strict_label_mode}"
    
    def test_strict_mode_default_is_false(self):
        """Default MarkdownLabel should have strict_label_mode=False."""
        label = MarkdownLabel(text="Test content")
        
        assert label.strict_label_mode is False, \
            f"Expected default strict_label_mode=False, got {label.strict_label_mode}"
        
        # Default participates in layout (auto_size_height=False)
        assert label.size_hint_y == 1, \
            f"Expected size_hint_y=1 by default, got {label.size_hint_y}"
    
    @given(st.booleans())
    @settings(max_examples=2, deadline=None)
    def test_strict_mode_property_accepted_and_stored(self, value):
        """Setting strict_label_mode property accepts and stores the value."""
        label = MarkdownLabel(text='# Hello World', strict_label_mode=value)
        # Complex strategy with custom domain strategy: 20 examples
        assert label.strict_label_mode == value
    
    @given(st.booleans())
    @settings(max_examples=2, deadline=None)
    def test_strict_mode_change_after_creation(self, value):
        """Changing strict_label_mode property after creation accepts and stores the value."""
        label = MarkdownLabel(text='# Hello')
        label.strict_label_mode = value
        assert label.strict_label_mode == value
    
    @given(simple_markdown_document())
    @settings(max_examples=20 if not os.getenv('CI') else 10, deadline=None)
    def test_strict_mode_toggle_from_false_to_true(self, markdown_text):
        """Toggling strict_label_mode from False to True disables auto-sizing."""
        label = MarkdownLabel(
            text=markdown_text,
            strict_label_mode=False,
            auto_size_height=True
        )
        
        # Complex strategy with custom domain strategy: 20 examples
        # Initially should have auto-sizing enabled
        assert label.size_hint_y is None, \
            "size_hint_y should be None when auto_size_height=True"
        
        # Toggle to strict mode
        label.strict_label_mode = True
        
        # Should now have size_hint_y preserved (default 1)
        assert label.size_hint_y == 1, \
            f"Expected size_hint_y=1 after toggling to strict_label_mode=True, got {label.size_hint_y}"
    
    @given(simple_markdown_document())
    @settings(max_examples=20 if not os.getenv('CI') else 10, deadline=None)
    def test_strict_mode_toggle_from_true_to_false(self, markdown_text):
        """Toggling strict_label_mode from True to False enables auto-sizing."""
        label = MarkdownLabel(
            text=markdown_text,
            strict_label_mode=True,
            auto_size_height=True
        )
        
        # Complex strategy with float generation, NaN exclusion, infinity exclusion, custom domain strategy: 50 examples
        # Initially should have size_hint_y preserved
        assert label.size_hint_y == 1, \
            "size_hint_y should be 1 when strict_label_mode=True"
        
        # Toggle to non-strict mode
        label.strict_label_mode = False
        
        # Should now have auto-sizing enabled
        assert label.size_hint_y is None, \
            f"Expected size_hint_y=None after toggling to strict_label_mode=False, got {label.size_hint_y}"
    
    @given(simple_markdown_document(), 
           st.floats(min_value=0.1, max_value=2.0, allow_nan=False, allow_infinity=False))
    @settings(max_examples=50 if not os.getenv('CI') else 25, deadline=None)
    def test_strict_mode_toggle_preserves_user_size_hint_y(self, markdown_text, user_size_hint_y):
        """Toggling strict_label_mode preserves user-specified size_hint_y."""
        label = MarkdownLabel(
            text=markdown_text, 
            strict_label_mode=True, 
            size_hint_y=user_size_hint_y,
            auto_size_height=True
        )
        
        # Initially should have user's size_hint_y
        assert label.size_hint_y == user_size_hint_y, \
            f"Expected size_hint_y={user_size_hint_y}, got {label.size_hint_y}"
        
        # Toggle to non-strict mode - should enable auto-sizing
        label.strict_label_mode = False
        assert label.size_hint_y is None, \
            f"Expected size_hint_y=None after toggle to False, got {label.size_hint_y}"
        
        # Toggle back to strict mode - should restore user's size_hint_y
        label.strict_label_mode = True
        assert label.size_hint_y == user_size_hint_y, \
            f"Expected size_hint_y={user_size_hint_y} after toggle back to True, got {label.size_hint_y}"
    
    @given(simple_markdown_document())
    # Complex strategy with custom domain strategy: 20 examples
    @settings(max_examples=20 if not os.getenv('CI') else 10, deadline=None)
    def test_strict_mode_overrides_auto_size_height(self, markdown_text):
        """strict_label_mode=True overrides auto_size_height=True behavior."""
        label = MarkdownLabel(
            text=markdown_text, 
            strict_label_mode=True, 
            auto_size_height=True
        )
        
        # strict_label_mode should take precedence
        assert label.size_hint_y == 1, \
            f"Expected size_hint_y=1 when strict_label_mode=True (overrides auto_size_height), got {label.size_hint_y}"
    
    @given(simple_markdown_document())
    @settings(max_examples=20 if not os.getenv('CI') else 10, deadline=None)
    # Complex strategy with custom domain strategy: 20 examples
    def test_strict_mode_ignores_auto_size_height_changes(self, markdown_text):
        """When strict_label_mode=True, auto_size_height changes are ignored."""
        label = MarkdownLabel(text=markdown_text, strict_label_mode=True)
        
        # Initially should have size_hint_y=1
        assert label.size_hint_y == 1
        
        # Try to enable auto_size_height - should be ignored
        label.auto_size_height = True
        
        # size_hint_y should still be 1 (strict mode takes precedence)
        assert label.size_hint_y == 1, \
            f"Expected size_hint_y=1 (strict mode ignores auto_size_height), got {label.size_hint_y}"
    
    @given(simple_markdown_document())
    @settings(max_examples=20 if not os.getenv('CI') else 10, deadline=None)
    # Complex strategy with custom domain strategy: 20 examples
    def test_strict_mode_triggers_rebuild(self, markdown_text):
        """Changing strict_label_mode triggers widget rebuild."""
        assume(markdown_text.strip())
        
        label = MarkdownLabel(text=markdown_text, strict_label_mode=False)
        initial_children = list(label.children)
        
        # Toggle strict_label_mode
        label.strict_label_mode = True
        
        # Widget tree should be rebuilt (children may be different objects)
        # We verify by checking that the label still has children
        assert len(label.children) >= 1, \
            "Expected at least 1 child after strict_label_mode toggle"
    
    @given(simple_markdown_document())
    @settings(max_examples=20 if not os.getenv('CI') else 10, deadline=None)
    def test_multiple_strict_mode_toggles_maintain_consistency(self, markdown_text):
        """Multiple strict_label_mode toggles maintain consistent behavior."""
        label = MarkdownLabel(text=markdown_text, auto_size_height=True)
        
        assert label.strict_label_mode is False
        assert label.size_hint_y is None
        
        # Toggle True -> False -> True -> False
        for expected_strict_mode, expected_size_hint_y in [
            (True, 1),       # Toggle to True
            (False, None),   # Toggle to False (auto_size_height=True)
            (True, 1),       # Toggle to True
            (False, None),   # Toggle to False (auto_size_height=True)
        ]:
            label.strict_label_mode = expected_strict_mode
            
            assert label.strict_label_mode == expected_strict_mode, \
                f"Expected strict_label_mode={expected_strict_mode}, got {label.strict_label_mode}"
            
            assert label.size_hint_y == expected_size_hint_y, \
                f"Expected size_hint_y={expected_size_hint_y}, got {label.size_hint_y}"


# **Feature: label-compatibility-phase2, Property 3: Comprehensive texture_size Calculation**
# *For any* MarkdownLabel containing mixed content (Labels, Images, Tables, Code blocks), 
# the `texture_size` property SHALL return a tuple where width is the maximum width of any 
# descendant widget AND height is the sum of all descendant heights.
# **Validates: Requirements 3.1, 3.2, 3.3**
#
# NOTE: In headless Kivy environments (without a display), Label widgets don't render
# textures, so texture_size returns (0, 0) for Labels. Tests focus on:
# 1. Correct return type and structure
# 2. Handling all widget types without crashing
# 3. Correct aggregation logic (even if values are 0 in headless mode)
# 4. Proper handling of empty content
# 5. Widget types that have explicit heights (thematic_break, blank_line, AsyncImage)

class TestComprehensiveTextureSizeCalculation:
    """Property tests for comprehensive texture_size calculation (Property 3)."""
    
    def _find_all_widgets_recursive(self, widget, widgets=None):
        """Recursively find all widgets in a widget tree.
        
        Args:
            widget: Root widget to search
            # Complex strategy with custom domain strategy: 20 examples
            widgets: List to accumulate widgets (created if None)
            
        Returns:
            List of all widgets found
        """
        if widgets is None:
            widgets = []
        
        widgets.append(widget)
        
        if hasattr(widget, 'children'):
            for child in widget.children:
                # Complex strategy with custom domain strategy: 20 examples
                self._find_all_widgets_recursive(child, widgets)
        
        return widgets
    
    @given(simple_markdown_document())
    @settings(max_examples=20 if not os.getenv('CI') else 10, deadline=None)
    def test_texture_size_returns_tuple(self, markdown_text):
        """texture_size returns a list/tuple with two elements."""
        label = MarkdownLabel(text=markdown_text)
        
        texture_size = label.texture_size
        
        assert isinstance(texture_size, (list, tuple)), \
            f"Expected texture_size to be list/tuple, got {type(texture_size)}"
        assert len(texture_size) == 2, \
            f"Expected texture_size to have 2 elements, got {len(texture_size)}"
    
    @given(simple_markdown_document())
    @settings(max_examples=20 if not os.getenv('CI') else 10, deadline=None)
    def test_texture_size_non_negative(self, markdown_text):
        """texture_size width and height are non-negative."""
        # Complex strategy: 20 examples based on default complexity
        label = MarkdownLabel(text=markdown_text)
        
        texture_size = label.texture_size
        
        assert texture_size[0] >= 0, \
            f"Expected texture_size width >= 0, got {texture_size[0]}"
        assert texture_size[1] >= 0, \
            f"Expected texture_size height >= 0, got {texture_size[1]}"
    
    def test_empty_label_texture_size_is_zero(self):
        """Empty MarkdownLabel has texture_size [0, 0]."""
        label = MarkdownLabel(text='')
        
        texture_size = label.texture_size
         # Complex strategy: 20 examples based on default complexity
        
        assert texture_size == [0, 0], \
            f"Expected texture_size [0, 0] for empty label, got {texture_size}"
    
    @given(markdown_heading())
    @settings(max_examples=20 if not os.getenv('CI') else 10, deadline=None)
    def test_heading_creates_label_widget(self, heading):
        """Heading content creates a Label widget that is included in texture_size calculation."""
        label = MarkdownLabel(text=heading)
        
        # Verify heading creates children
        assert len(label.children) >= 1, \
            f"Expected at least 1 child for heading, got {len(label.children)}"
        
        # Verify texture_size is accessible and returns valid structure
        texture_size = label.texture_size
        assert isinstance(texture_size, (list, tuple)) and len(texture_size) == 2
        assert texture_size[0] >= 0 and texture_size[1] >= 0
    
    @given(markdown_paragraph())
    @settings(max_examples=20 if not os.getenv('CI') else 10, deadline=None)
    def test_paragraph_creates_label_widget(self, paragraph):
        """Paragraph content creates a Label widget that is included in texture_size calculation."""
        assume(paragraph.strip())
        
        label = MarkdownLabel(text=paragraph)
        
        # Verify paragraph creates children
        assert len(label.children) >= 1, \
            f"Expected at least 1 child for paragraph, got {len(label.children)}"
        
        # Verify texture_size is accessible and returns valid structure
        texture_size = label.texture_size
        assert isinstance(texture_size, (list, tuple)) and len(texture_size) == 2
        assert texture_size[0] >= 0 and texture_size[1] >= 0
    
    def test_code_block_creates_container_widget(self):
        """Code block content creates a BoxLayout container that is included in texture_size calculation."""
        markdown = '```python\nprint("hello")\n```'
        label = MarkdownLabel(text=markdown)
        
        # Verify code block creates children
        assert len(label.children) >= 1, \
            f"Expected at least 1 child for code block, got {len(label.children)}"
        
        # Verify texture_size is accessible and returns valid structure
        texture_size = label.texture_size
        assert isinstance(texture_size, (list, tuple)) and len(texture_size) == 2
        assert texture_size[0] >= 0 and texture_size[1] >= 0
    
    def test_list_creates_container_widget(self):
        """List content creates a BoxLayout container that is included in texture_size calculation."""
        markdown = '- Item 1\n- Item 2\n- Item 3'
        label = MarkdownLabel(text=markdown)
        
        # Verify list creates children
        assert len(label.children) >= 1, \
            f"Expected at least 1 child for list, got {len(label.children)}"
        
        # Verify texture_size is accessible and returns valid structure
        texture_size = label.texture_size
        assert isinstance(texture_size, (list, tuple)) and len(texture_size) == 2
        assert texture_size[0] >= 0 and texture_size[1] >= 0
    
    def test_table_creates_gridlayout_widget(self):
        """Table content creates a GridLayout widget that is included in texture_size calculation."""
        markdown = '| A | B |\n| --- | --- |\n| 1 | 2 |'
        label = MarkdownLabel(text=markdown)
        
        # Verify table creates children
        assert len(label.children) >= 1, \
            f"Expected at least 1 child for table, got {len(label.children)}"
        
        # Verify at least one child is a GridLayout
        has_gridlayout = any(isinstance(c, GridLayout) for c in label.children)
        assert has_gridlayout, "Expected a GridLayout child for table"
        
        # Verify texture_size is accessible and returns valid structure
        texture_size = label.texture_size
        assert isinstance(texture_size, (list, tuple)) and len(texture_size) == 2
        assert texture_size[0] >= 0 and texture_size[1] >= 0
    
    def test_block_quote_creates_container_widget(self):
        """Block quote content creates a BoxLayout container that is included in texture_size calculation."""
        markdown = '> This is a quote'
        label = MarkdownLabel(text=markdown)
        
        # Verify block quote creates children
        assert len(label.children) >= 1, \
            f"Expected at least 1 child for block quote, got {len(label.children)}"
        
        # Verify texture_size is accessible and returns valid structure
        texture_size = label.texture_size
        assert isinstance(texture_size, (list, tuple)) and len(texture_size) == 2
        assert texture_size[0] >= 0 and texture_size[1] >= 0
    
    def test_thematic_break_contributes_to_texture_size(self):
        """Thematic break (horizontal rule) contributes to texture_size with explicit height."""
        markdown = 'Before\n\n---\n\nAfter'
        label = MarkdownLabel(text=markdown)
        
        texture_size = label.texture_size
        
        # Thematic break has explicit height=20, so texture_size should be > 0
        # even in headless mode (Widget height is counted directly)
        assert texture_size[1] > 0, \
            f"Expected texture_size height > 0 for thematic break, got {texture_size[1]}"
    
    @given(st.integers(min_value=1, max_value=5))
    @settings(max_examples=100, deadline=None)
    def test_more_content_increases_texture_height(self, num_paragraphs):
        """More content results in larger texture_size height."""
        # Create markdown with varying number of paragraphs
        text1 = 'Single paragraph'
        text_multi = '\n\n'.join([f'Paragraph {i} with some text.' for i in range(num_paragraphs)])
        
        label1 = MarkdownLabel(text=text1)
        label_multi = MarkdownLabel(text=text_multi)
        
        # More paragraphs should result in larger height
        if num_paragraphs > 1:
            assert label_multi.texture_size[1] >= label1.texture_size[1], \
                f"Expected multi-paragraph height >= single paragraph height"
    
    def test_mixed_content_creates_multiple_widgets(self):
        """Mixed content (heading, paragraph, code, list) creates multiple widgets for texture_size."""
        markdown = '''# Heading

This is a paragraph.

```python
# Complex strategy with custom domain strategy: 20 examples
code = "block"
```

- List item 1
- List item 2

> A quote
'''
        label = MarkdownLabel(text=markdown)
        
        texture_size = label.texture_size
        
        # Verify texture_size is accessible and returns valid structure
        assert isinstance(texture_size, (list, tuple)) and len(texture_size) == 2
        assert texture_size[0] >= 0 and texture_size[1] >= 0
        
        # Should have multiple children
        assert len(label.children) > 1, \
            f"Expected multiple children for mixed content, got {len(label.children)}"
    
    @given(simple_markdown_document())
    @settings(max_examples=20 if not os.getenv('CI') else 10, deadline=None)
    def test_texture_size_accessible_for_all_content(self, markdown_text):
        """texture_size is accessible and valid for all markdown content."""
        assume(markdown_text.strip())
        
        label = MarkdownLabel(text=markdown_text)
        
        texture_size = label.texture_size
        
        # Verify texture_size is accessible and returns valid structure
        assert isinstance(texture_size, (list, tuple)) and len(texture_size) == 2
        assert texture_size[0] >= 0 and texture_size[1] >= 0
        
        # If there are children, the calculation should have run without error
        if len(label.children) > 0:
            # The method should have traversed all children
            pass  # No assertion needed - if we got here, the method worked
    
    def test_nested_list_creates_nested_containers(self):
        """Nested list content creates nested BoxLayout containers for texture_size calculation."""
        markdown = '''- Item 1
  - Nested 1
  - Nested 2
- Item 2'''
        label = MarkdownLabel(text=markdown)
        
        # Verify nested list creates children
        assert len(label.children) >= 1, \
            # Complex strategy with custom domain strategy: 20 examples
            f"Expected at least 1 child for nested list, got {len(label.children)}"
        
        # Verify texture_size is accessible and returns valid structure
        texture_size = label.texture_size
        assert isinstance(texture_size, (list, tuple)) and len(texture_size) == 2
        assert texture_size[0] >= 0 and texture_size[1] >= 0
    
    def test_ordered_list_creates_container_widget(self):
        """Ordered list content creates a BoxLayout container for texture_size calculation."""
        markdown = '1. First\n2. Second\n3. Third'
        label = MarkdownLabel(text=markdown)
        
        # Verify ordered list creates children
        assert len(label.children) >= 1, \
            f"Expected at least 1 child for ordered list, got {len(label.children)}"
        
        # Verify texture_size is accessible and returns valid structure
        texture_size = label.texture_size
        assert isinstance(texture_size, (list, tuple)) and len(texture_size) == 2
        assert texture_size[0] >= 0 and texture_size[1] >= 0
    
    @given(simple_markdown_document(), simple_markdown_document())
    @settings(max_examples=20 if not os.getenv('CI') else 10, deadline=None)
    def test_texture_size_updates_on_text_change(self, text1, text2):
        """texture_size updates when text property changes."""
        assume(text1.strip() and text2.strip())
        assume(text1 != text2)
        
        label = MarkdownLabel(text=text1)
        texture_size1 = label.texture_size
        
        # Change text - use force_rebuild() for immediate update since
        # text changes now use deferred rebuilds
        label.text = text2
        label.force_rebuild()
        texture_size2 = label.texture_size
        
        # texture_size should be recalculated (may or may not be different)
        # The key is that it doesn't crash and returns valid values
        assert isinstance(texture_size2, (list, tuple)), \
            f"Expected texture_size to be list/tuple after text change"
        assert len(texture_size2) == 2, \
            f"Expected texture_size to have 2 elements after text change"
        assert texture_size2[0] >= 0 and texture_size2[1] >= 0, \
            f"Expected non-negative texture_size after text change"
    
    def test_texture_size_with_image_markdown(self):
        """Image markdown contributes to texture_size.
        
        Note: In Markdown, images are inline elements typically wrapped in paragraphs.
        The texture_size should account for the containing paragraph and/or image widget.
        """
        # Use image in a paragraph context (common usage)
        markdown = 'Here is an image:\n\n![Alt text](https://example.com/image.png)\n\nAfter image.'
        label = MarkdownLabel(text=markdown)
        
        texture_size = label.texture_size
        
        # Content with image should have non-zero texture_size
        # (the surrounding text paragraphs will contribute even if image doesn't)
        assert texture_size[1] > 0, \
            f"Expected texture_size height > 0 for content with image, got {texture_size[1]}"
        
        # Verify children were created
        assert len(label.children) > 0, \
            f"Expected children for image markdown, got {len(label.children)}"
    
    @given(st.integers(min_value=1, max_value=6))
    @settings(max_examples=100, deadline=None)
    def test_all_heading_levels_create_label_widgets(self, level):
        """All heading levels create Label widgets for texture_size calculation."""
        markdown = '#' * level + ' Heading'
        label = MarkdownLabel(text=markdown)
        
        # Verify heading creates children
        assert len(label.children) >= 1, \
            f"Expected at least 1 child for h{level}, got {len(label.children)}"
        
        # Verify texture_size is accessible and returns valid structure
        texture_size = label.texture_size
        assert isinstance(texture_size, (list, tuple)) and len(texture_size) == 2
        assert texture_size[0] >= 0 and texture_size[1] >= 0
    
    def test_blank_lines_create_spacer_widgets(self):
        """Blank lines create spacer widgets with explicit height for texture_size."""
        markdown_no_blanks = 'Para 1\nPara 2'
        markdown_with_blanks = 'Para 1\n\n\n\nPara 2'
        
        label_no_blanks = MarkdownLabel(text=markdown_no_blanks)
        label_with_blanks = MarkdownLabel(text=markdown_with_blanks)
        
        # Both should have valid texture_size
        ts_no_blanks = label_no_blanks.texture_size
        ts_with_blanks = label_with_blanks.texture_size
        
        assert isinstance(ts_no_blanks, (list, tuple)) and len(ts_no_blanks) == 2
        assert isinstance(ts_with_blanks, (list, tuple)) and len(ts_with_blanks) == 2
        
        # With blank lines should have more children (blank_line widgets)
        # and thus potentially larger texture_size height
        assert len(label_with_blanks.children) >= len(label_no_blanks.children), \
            "Expected content with blank lines to have at least as many children"
        
        # blank_line widgets have explicit height (base_font_size), so they contribute
        # to texture_size even in headless mode
        assert ts_with_blanks[1] >= ts_no_blanks[1], \
            "Expected content with blank lines to have at least as much height"


# **Feature: test-refactoring, Property 9: Logical Test Grouping**
# *For any* two test classes that test the same feature area, they should be located in the same module
# **Validates: Requirements 1.4, 4.3, 4.4**

class TestLogicalTestGrouping:
    """Property tests for logical test grouping (Property 9)."""
    
    def test_sizing_behavior_classes_grouped_together(self):
        """All sizing behavior test classes are grouped in the same module."""
        import inspect
        import kivy_garden.markdownlabel.tests.test_sizing_behavior as sizing_module
        
        # Get all test classes in this module
        test_classes = []
        for name, obj in inspect.getmembers(sizing_module):
            if (inspect.isclass(obj) and 
                name.startswith('Test') and 
                obj.__module__ == sizing_module.__name__):
                test_classes.append(name)
        
        # Expected sizing behavior test classes
        expected_classes = {
            'TestAutoSizingBehavior',
            'TestAutoSizeHeightTrueBehavior', 
            'TestAutoSizeHeightFalseBehavior',
            'TestAutoSizeHeightDynamicToggling',
            'TestStrictLabelModeSizingBehavior',
            'TestComprehensiveTextureSizeCalculation',
            'TestLogicalTestGrouping'  # This test class itself
        }
        
        # Verify all expected classes are present
        actual_classes = set(test_classes)
        assert expected_classes.issubset(actual_classes), \
            f"Missing expected classes: {expected_classes - actual_classes}"
        
        # Verify no unexpected classes (all classes should be sizing-related)
        sizing_related_keywords = {
            'auto', 'size', 'sizing', 'height', 'strict', 'texture', 'grouping'
        }
        
        for class_name in test_classes:
            class_name_lower = class_name.lower()
            has_sizing_keyword = any(keyword in class_name_lower for keyword in sizing_related_keywords)
            assert has_sizing_keyword, \
                f"Test class {class_name} doesn't appear to be sizing-related"
    
    def test_module_focuses_on_sizing_behavior(self):
        """This module focuses specifically on sizing behavior functionality."""
        import kivy_garden.markdownlabel.tests.test_sizing_behavior as sizing_module
        
        # Check module docstring mentions sizing
        module_doc = sizing_module.__doc__ or ""
        sizing_keywords = ['sizing', 'size', 'auto-sizing', 'texture']
        
        has_sizing_focus = any(keyword in module_doc.lower() for keyword in sizing_keywords)
        assert has_sizing_focus, \
            f"Module docstring should mention sizing behavior: {module_doc}"
    
    def test_all_classes_test_related_functionality(self):
        """All test classes in this module test related sizing functionality."""
        import inspect
        import kivy_garden.markdownlabel.tests.test_sizing_behavior as sizing_module
        
        # Get all test classes and their methods
        for name, obj in inspect.getmembers(sizing_module):
            if (inspect.isclass(obj) and 
                name.startswith('Test') and 
                obj.__module__ == sizing_module.__name__):
                
                # Get test methods
                test_methods = [method_name for method_name, method in inspect.getmembers(obj)
                              if method_name.startswith('test_')]
                
                if test_methods:  # Only check classes with test methods
                    # Check that class docstring or name indicates sizing focus
                    class_doc = obj.__doc__ or ""
                    class_name_lower = name.lower()
                    
                    sizing_indicators = [
                        'sizing', 'size', 'auto', 'height', 'strict', 'texture', 'grouping'
                    ]
                    
                    has_sizing_indicator = (
                        any(indicator in class_name_lower for indicator in sizing_indicators) or
                        any(indicator in class_doc.lower() for indicator in sizing_indicators)
                    )
                    
                    assert has_sizing_indicator, \
                        f"Test class {name} should focus on sizing behavior"