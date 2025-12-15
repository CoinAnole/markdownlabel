"""
Property-based tests for color-related properties in MarkdownLabel widget.

Tests verify that color properties (color, disabled_color) are correctly
forwarded to internal Label widgets and applied appropriately based on
the widget's disabled state.
"""

import os
# Set environment variable to use headless mode for Kivy
os.environ['KIVY_NO_ARGS'] = '1'
os.environ['KIVY_NO_CONSOLELOG'] = '1'

import pytest
from hypothesis import given, strategies as st, settings, assume

from kivy.uix.label import Label

from kivy_garden.markdownlabel import MarkdownLabel
from .test_utils import (
    color_strategy,
    find_labels_recursive,
    colors_equal
)


# **Feature: label-compatibility, Property 3: Color Forwarding**
# *For any* Markdown text and any color value, all internal Labels SHALL have
# `color` set to the specified value, except for code blocks which preserve
# their light color.
# **Validates: Requirements 3.1**

class TestColorForwarding:
    """Property tests for color forwarding (Property 3)."""
    
    @given(color_strategy)
    @settings(max_examples=100, deadline=None)
    def test_color_applied_to_paragraph(self, color):
        """color is applied to paragraph Labels."""
        label = MarkdownLabel(text='Hello World', color=color)
        
        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        # All labels should have the specified color
        for lbl in labels:
            assert colors_equal(list(lbl.color), color), \
                f"Expected color={color}, got {list(lbl.color)}"
    
    @given(color_strategy)
    @settings(max_examples=100, deadline=None)
    def test_color_applied_to_heading(self, color):
        """color is applied to heading Labels."""
        label = MarkdownLabel(text='# Heading', color=color)
        
        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        # All labels should have the specified color
        for lbl in labels:
            assert colors_equal(list(lbl.color), color), \
                f"Expected color={color}, got {list(lbl.color)}"
    
    @given(color_strategy)
    @settings(max_examples=100, deadline=None)
    def test_code_block_preserves_light_color(self, color):
        """Code blocks preserve their light text color regardless of color setting."""
        markdown = '```python\nprint("hello")\n```'
        code_color = [0.9, 0.9, 0.9, 1]  # Expected code block color
        
        label = MarkdownLabel(text=markdown, color=color)
        
        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label for code block"
        
        # Code block labels should use their own light color, not the specified color
        for lbl in labels:
            assert colors_equal(list(lbl.color), code_color), \
                f"Code label should use light color={code_color}, got {list(lbl.color)}"
    
    @given(color_strategy, color_strategy)
    @settings(max_examples=100, deadline=None)
    def test_color_change_triggers_rebuild(self, color1, color2):
        """Changing color triggers widget rebuild with new color."""
        assume(not colors_equal(color1, color2))
        
        label = MarkdownLabel(text='Hello World', color=color1)
        
        # Verify initial color
        labels = find_labels_recursive(label)
        for lbl in labels:
            assert colors_equal(list(lbl.color), color1)
        
        # Change color
        label.color = color2
        
        # Verify new color
        labels = find_labels_recursive(label)
        for lbl in labels:
            assert colors_equal(list(lbl.color), color2), \
                f"After change, expected color={color2}, got {list(lbl.color)}"
    
    @given(color_strategy)
    @settings(max_examples=100, deadline=None)
    def test_color_applied_to_list_items(self, color):
        """color is applied to list item Labels."""
        markdown = '- Item 1\n- Item 2'
        label = MarkdownLabel(text=markdown, color=color)
        
        labels = find_labels_recursive(label)
        assert len(labels) >= 2, "Expected at least 2 Labels for list items"
        
        # All labels should have the specified color
        for lbl in labels:
            assert colors_equal(list(lbl.color), color), \
                f"Expected color={color}, got {list(lbl.color)}"
    
    @given(color_strategy)
    @settings(max_examples=100, deadline=None)
    def test_color_applied_to_table_cells(self, color):
        """color is applied to table cell Labels."""
        markdown = '| A | B |\n| --- | --- |\n| 1 | 2 |'
        label = MarkdownLabel(text=markdown, color=color)
        
        labels = find_labels_recursive(label)
        assert len(labels) >= 4, "Expected at least 4 Labels for table cells"
        
        # All labels should have the specified color
        for lbl in labels:
            assert colors_equal(list(lbl.color), color), \
                f"Expected color={color}, got {list(lbl.color)}"
    
    @given(color_strategy)
    @settings(max_examples=100, deadline=None)
    def test_mixed_content_color_separation(self, color):
        """Mixed content correctly separates body color and code color."""
        code_color = [0.9, 0.9, 0.9, 1]
        markdown = 'Regular text\n\n```\ncode\n```\n\nMore text'
        
        label = MarkdownLabel(text=markdown, color=color)
        
        labels = find_labels_recursive(label)
        assert len(labels) >= 2, "Expected at least 2 Labels (text + code)"
        
        # Separate labels by color
        body_labels = [l for l in labels if colors_equal(list(l.color), color)]
        code_labels = [l for l in labels if colors_equal(list(l.color), code_color)]
        
        # Should have both body and code labels
        assert len(body_labels) >= 1, "Expected at least one body text label with specified color"
        assert len(code_labels) >= 1, "Expected at least one code label with light color"

    def test_links_unstyled_by_default(self):
        """Default links remain unstyled while keeping ref markup."""
        markdown = 'Click [here](https://kivy.org)'
        label = MarkdownLabel(text=markdown)
        
        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        assert any('[ref=' in getattr(lbl, 'text', '') for lbl in labels), \
            "Expected ref markup for link"
        assert not any('[color=' in getattr(lbl, 'text', '') for lbl in labels), \
            "Default links should not inject color markup"
    
    def test_links_styled_when_enabled(self):
        """Links gain color markup when link_style='styled'."""
        markdown = 'Click [here](https://kivy.org)'
        label = MarkdownLabel(text=markdown, link_style='styled')
        
        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        assert any('[color=' in getattr(lbl, 'text', '') for lbl in labels), \
            "Expected colored markup when link_style='styled'"


# **Feature: label-compatibility, Property 12: Disabled Color Application**
# *For any* MarkdownLabel with `disabled=True` and a `disabled_color` value,
# all internal Labels SHALL use `disabled_color` instead of `color`.
# **Validates: Requirements 12.1, 12.2**

class TestDisabledColorApplication:
    """Property tests for disabled_color application (Property 12)."""
    
    @given(st.lists(
        st.floats(min_value=0, max_value=1, allow_nan=False, allow_infinity=False),
        min_size=4, max_size=4
    ))
    @settings(max_examples=100, deadline=None)
    def test_disabled_color_stored_correctly(self, disabled_color):
        """disabled_color property stores the value correctly."""
        label = MarkdownLabel(text='Hello World', disabled_color=disabled_color)
        
        assert colors_equal(label.disabled_color, disabled_color), \
            f"Expected disabled_color={disabled_color}, got {list(label.disabled_color)}"
    
    @given(st.lists(
        st.floats(min_value=0, max_value=1, allow_nan=False, allow_infinity=False),
        min_size=4, max_size=4
    ))
    @settings(max_examples=100, deadline=None)
    def test_disabled_color_applied_when_disabled(self, disabled_color):
        """When disabled=True, internal Labels use disabled_color instead of color."""
        regular_color = [1, 0, 0, 1]  # Red
        
        label = MarkdownLabel(
            text='Hello World',
            color=regular_color,
            disabled_color=disabled_color,
            disabled=True
        )
        
        labels = find_labels_recursive(label)
        assert len(labels) > 0, "Expected at least one Label widget"
        
        for lbl in labels:
            # Skip code block labels which have their own color
            if hasattr(lbl, 'font_name') and 'Mono' in str(lbl.font_name):
                continue
            assert colors_equal(lbl.color, disabled_color), \
                f"Expected disabled_color={disabled_color}, got {list(lbl.color)}"
    
    @given(st.lists(
        st.floats(min_value=0, max_value=1, allow_nan=False, allow_infinity=False),
        min_size=4, max_size=4
    ))
    @settings(max_examples=100, deadline=None)
    def test_regular_color_applied_when_not_disabled(self, regular_color):
        """When disabled=False, internal Labels use regular color."""
        disabled_color = [0.5, 0.5, 0.5, 0.3]  # Gray semi-transparent
        
        label = MarkdownLabel(
            text='Hello World',
            color=regular_color,
            disabled_color=disabled_color,
            disabled=False
        )
        
        labels = find_labels_recursive(label)
        assert len(labels) > 0, "Expected at least one Label widget"
        
        for lbl in labels:
            # Skip code block labels which have their own color
            if hasattr(lbl, 'font_name') and 'Mono' in str(lbl.font_name):
                continue
            assert colors_equal(lbl.color, regular_color), \
                f"Expected color={regular_color}, got {list(lbl.color)}"
    
    @given(st.booleans())
    @settings(max_examples=100, deadline=None)
    def test_disabled_state_determines_color(self, disabled):
        """disabled property determines which color is used."""
        regular_color = [1, 0, 0, 1]  # Red
        disabled_color = [0.5, 0.5, 0.5, 0.3]  # Gray semi-transparent
        
        label = MarkdownLabel(
            text='Hello World',
            color=regular_color,
            disabled_color=disabled_color,
            disabled=disabled
        )
        
        expected_color = disabled_color if disabled else regular_color
        
        labels = find_labels_recursive(label)
        assert len(labels) > 0, "Expected at least one Label widget"
        
        for lbl in labels:
            # Skip code block labels which have their own color
            if hasattr(lbl, 'font_name') and 'Mono' in str(lbl.font_name):
                continue
            assert colors_equal(lbl.color, expected_color), \
                f"Expected color={expected_color}, got {list(lbl.color)}"
    
    def test_disabled_change_triggers_rebuild(self):
        """Changing disabled property triggers widget rebuild."""
        regular_color = [1, 0, 0, 1]  # Red
        disabled_color = [0.5, 0.5, 0.5, 0.3]  # Gray semi-transparent
        
        label = MarkdownLabel(
            text='Hello World',
            color=regular_color,
            disabled_color=disabled_color,
            disabled=False
        )
        
        # Verify initial state uses regular color
        labels = find_labels_recursive(label)
        for lbl in labels:
            if hasattr(lbl, 'font_name') and 'Mono' in str(lbl.font_name):
                continue
            assert colors_equal(lbl.color, regular_color), \
                f"Initially expected color={regular_color}, got {list(lbl.color)}"
        
        # Change to disabled
        label.disabled = True
        
        # Verify disabled state uses disabled_color
        labels = find_labels_recursive(label)
        for lbl in labels:
            if hasattr(lbl, 'font_name') and 'Mono' in str(lbl.font_name):
                continue
            assert colors_equal(lbl.color, disabled_color), \
                f"After disabling, expected disabled_color={disabled_color}, got {list(lbl.color)}"
        
        # Change back to enabled
        label.disabled = False
        
        # Verify enabled state uses regular color again
        labels = find_labels_recursive(label)
        for lbl in labels:
            if hasattr(lbl, 'font_name') and 'Mono' in str(lbl.font_name):
                continue
            assert colors_equal(lbl.color, regular_color), \
                f"After re-enabling, expected color={regular_color}, got {list(lbl.color)}"
    
    def test_disabled_color_applied_to_heading(self):
        """disabled_color is applied to heading Labels when disabled."""
        disabled_color = [0.5, 0.5, 0.5, 0.3]
        
        label = MarkdownLabel(
            text='# Heading',
            disabled_color=disabled_color,
            disabled=True
        )
        
        labels = find_labels_recursive(label)
        assert len(labels) > 0, "Expected at least one Label widget"
        
        for lbl in labels:
            assert colors_equal(lbl.color, disabled_color), \
                f"Expected disabled_color={disabled_color}, got {list(lbl.color)}"
    
    def test_disabled_color_applied_to_list_items(self):
        """disabled_color is applied to list item Labels when disabled."""
        disabled_color = [0.5, 0.5, 0.5, 0.3]
        
        label = MarkdownLabel(
            text='- Item 1\n- Item 2',
            disabled_color=disabled_color,
            disabled=True
        )
        
        labels = find_labels_recursive(label)
        assert len(labels) > 0, "Expected at least one Label widget"
        
        for lbl in labels:
            assert colors_equal(lbl.color, disabled_color), \
                f"Expected disabled_color={disabled_color}, got {list(lbl.color)}"
    
    def test_disabled_color_applied_to_table_cells(self):
        """disabled_color is applied to table cell Labels when disabled."""
        disabled_color = [0.5, 0.5, 0.5, 0.3]
        
        label = MarkdownLabel(
            text='| A | B |\n| --- | --- |\n| 1 | 2 |',
            disabled_color=disabled_color,
            disabled=True
        )
        
        labels = find_labels_recursive(label)
        assert len(labels) > 0, "Expected at least one Label widget"
        
        for lbl in labels:
            assert colors_equal(lbl.color, disabled_color), \
                f"Expected disabled_color={disabled_color}, got {list(lbl.color)}"
    
    def test_default_disabled_color(self):
        """Default disabled_color is [1, 1, 1, 0.3]."""
        label = MarkdownLabel(text='Hello World')
        
        expected = [1, 1, 1, 0.3]
        assert colors_equal(label.disabled_color, expected), \
            f"Default disabled_color should be {expected}, got {list(label.disabled_color)}"
    
    def test_default_disabled_is_false(self):
        """Default disabled is False."""
        label = MarkdownLabel(text='Hello World')
        
        assert label.disabled is False, \
            f"Default disabled should be False, got {label.disabled}"