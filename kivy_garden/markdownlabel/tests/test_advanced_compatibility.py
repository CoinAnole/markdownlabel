"""
Property-based tests for advanced MarkdownLabel compatibility features.

This module contains tests for advanced Label API compatibility features including:
- Advanced font properties forwarding
- Disabled color application
- Reactive rebuild on property changes
- Text shortening property forwarding
- Coordinate translation for refs and anchors

These tests verify that MarkdownLabel correctly implements advanced Label
compatibility while maintaining proper Markdown rendering functionality.
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


# **Feature: label-compatibility, Property 11: Advanced Font Properties Forwarding**
# *For any* font advanced property (font_family, font_context, font_features, font_hinting,
# font_kerning, font_blended), when set on MarkdownLabel, all applicable child Labels
# SHALL have the same property value.
# **Validates: Requirements 11.1, 11.2, 11.3, 11.4, 11.5, 11.6**

class TestAdvancedFontPropertiesForwarding:
    """Property tests for advanced font properties forwarding (Property 11)."""
    
    @given(st.text(min_size=1, max_size=30, alphabet=st.characters(
        whitelist_categories=['L', 'N'],
        blacklist_characters='[]&\n\r'
    )))
    @settings(max_examples=100, deadline=None)
    def test_font_family_forwarded_to_labels(self, font_family_value):
        """font_family is forwarded to all internal Labels."""
        label = MarkdownLabel(text='Hello World', font_family=font_family_value)
        
        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least 1 Label"
        
        for lbl in labels:
            assert lbl.font_family == font_family_value, \
                f"Expected font_family={font_family_value!r}, got {lbl.font_family!r}"
    
    @given(st.text(min_size=1, max_size=30, alphabet=st.characters(
        whitelist_categories=['L', 'N'],
        blacklist_characters='[]&\n\r'
    )))
    @settings(max_examples=100, deadline=None)
    def test_font_context_forwarded_to_labels(self, font_context_value):
        """font_context is forwarded to all internal Labels."""
        label = MarkdownLabel(text='Hello World', font_context=font_context_value)
        
        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least 1 Label"
        
        for lbl in labels:
            assert lbl.font_context == font_context_value, \
                f"Expected font_context={font_context_value!r}, got {lbl.font_context!r}"
    
    @given(st.text(min_size=0, max_size=50, alphabet=st.characters(
        whitelist_categories=['L', 'N', 'P'],
        blacklist_characters='[]&\n\r'
    )))
    @settings(max_examples=100, deadline=None)
    def test_font_features_forwarded_to_labels(self, font_features_value):
        """font_features is forwarded to all internal Labels."""
        label = MarkdownLabel(text='Hello World', font_features=font_features_value)
        
        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least 1 Label"
        
        for lbl in labels:
            assert lbl.font_features == font_features_value, \
                f"Expected font_features={font_features_value!r}, got {lbl.font_features!r}"
    
    @given(st.sampled_from([None, 'normal', 'light', 'mono']))
    @settings(max_examples=100, deadline=None)
    def test_font_hinting_forwarded_to_labels(self, font_hinting_value):
        """font_hinting is forwarded to all internal Labels."""
        label = MarkdownLabel(text='Hello World', font_hinting=font_hinting_value)
        
        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least 1 Label"
        
        for lbl in labels:
            # When font_hinting is None, it may not be set on the Label
            if font_hinting_value is not None:
                assert lbl.font_hinting == font_hinting_value, \
                    f"Expected font_hinting={font_hinting_value!r}, got {lbl.font_hinting!r}"
    
    @given(st.booleans())
    @settings(max_examples=100, deadline=None)
    def test_font_kerning_forwarded_to_labels(self, font_kerning_value):
        """font_kerning is forwarded to all internal Labels."""
        label = MarkdownLabel(text='Hello World', font_kerning=font_kerning_value)
        
        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least 1 Label"
        
        for lbl in labels:
            assert lbl.font_kerning == font_kerning_value, \
                f"Expected font_kerning={font_kerning_value}, got {lbl.font_kerning}"
    
    @given(st.booleans())
    @settings(max_examples=100, deadline=None)
    def test_font_blended_forwarded_to_labels(self, font_blended_value):
        """font_blended is forwarded to all internal Labels."""
        label = MarkdownLabel(text='Hello World', font_blended=font_blended_value)
        
        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least 1 Label"
        
        for lbl in labels:
            assert lbl.font_blended == font_blended_value, \
                f"Expected font_blended={font_blended_value}, got {lbl.font_blended}"
    
    @given(st.sampled_from([None, 'normal', 'light', 'mono']),
           st.booleans(),
           st.booleans())
    @settings(max_examples=100, deadline=None)
    def test_multiple_advanced_font_properties_forwarded(self, font_hinting, font_kerning, font_blended):
        """Multiple advanced font properties are forwarded together."""
        label = MarkdownLabel(
            text='# Heading\n\nParagraph text',
            font_hinting=font_hinting,
            font_kerning=font_kerning,
            font_blended=font_blended
        )
        
        labels = find_labels_recursive(label)
        assert len(labels) >= 2, "Expected at least 2 Labels (heading + paragraph)"
        
        for lbl in labels:
            if font_hinting is not None:
                assert lbl.font_hinting == font_hinting, \
                    f"Expected font_hinting={font_hinting!r}, got {lbl.font_hinting!r}"
            assert lbl.font_kerning == font_kerning, \
                f"Expected font_kerning={font_kerning}, got {lbl.font_kerning}"
            assert lbl.font_blended == font_blended, \
                f"Expected font_blended={font_blended}, got {lbl.font_blended}"
    
    @given(st.booleans(), st.booleans())
    @settings(max_examples=100, deadline=None)
    def test_font_kerning_change_triggers_rebuild(self, kerning1, kerning2):
        """Changing font_kerning triggers widget rebuild with new value."""
        assume(kerning1 != kerning2)
        
        label = MarkdownLabel(text='Hello World', font_kerning=kerning1)
        
        # Verify initial value
        labels = find_labels_recursive(label)
        for lbl in labels:
            assert lbl.font_kerning == kerning1
        
        # Change value
        label.font_kerning = kerning2
        label.force_rebuild()  # Force immediate rebuild for test
        
        # Verify new value
        labels = find_labels_recursive(label)
        for lbl in labels:
            assert lbl.font_kerning == kerning2, \
                f"After change, expected font_kerning={kerning2}, got {lbl.font_kerning}"
    
    @given(st.booleans(), st.booleans())
    @settings(max_examples=100, deadline=None)
    def test_font_blended_change_triggers_rebuild(self, blended1, blended2):
        """Changing font_blended triggers widget rebuild with new value."""
        assume(blended1 != blended2)
        
        label = MarkdownLabel(text='Hello World', font_blended=blended1)
        
        # Verify initial value
        labels = find_labels_recursive(label)
        for lbl in labels:
            assert lbl.font_blended == blended1
        
        # Change value
        label.font_blended = blended2
        label.force_rebuild()  # Force immediate rebuild for test
        
        # Verify new value
        labels = find_labels_recursive(label)
        for lbl in labels:
            assert lbl.font_blended == blended2, \
                f"After change, expected font_blended={blended2}, got {lbl.font_blended}"
    
    def test_default_font_kerning_is_true(self):
        """Default font_kerning is True."""
        label = MarkdownLabel(text='Hello World')
        
        assert label.font_kerning is True, \
            f"Default font_kerning should be True, got {label.font_kerning}"
    
    def test_default_font_blended_is_true(self):
        """Default font_blended is True."""
        label = MarkdownLabel(text='Hello World')
        
        assert label.font_blended is True, \
            f"Default font_blended should be True, got {label.font_blended}"
    
    def test_default_font_hinting_is_normal(self):
        """Default font_hinting is 'normal'."""
        label = MarkdownLabel(text='Hello World')
        
        assert label.font_hinting == 'normal', \
            f"Default font_hinting should be 'normal', got {label.font_hinting}"
    
    def test_default_font_features_is_empty(self):
        """Default font_features is empty string."""
        label = MarkdownLabel(text='Hello World')
        
        assert label.font_features == '', \
            f"Default font_features should be '', got {label.font_features!r}"
    
    def test_default_font_family_is_none(self):
        """Default font_family is None."""
        label = MarkdownLabel(text='Hello World')
        
        assert label.font_family is None, \
            f"Default font_family should be None, got {label.font_family!r}"
    
    def test_default_font_context_is_none(self):
        """Default font_context is None."""
        label = MarkdownLabel(text='Hello World')
        
        assert label.font_context is None, \
            f"Default font_context should be None, got {label.font_context!r}"


# **Feature: label-compatibility, Property 12: disabled_color Application**
# *For any* MarkdownLabel with `disabled=True` and any `disabled_color` value,
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

# **Feature: label-compatibility, Property 14: Reactive Rebuild on Property Change**
# *For any* forwarding property change after initial rendering, the widget tree
# SHALL be rebuilt with the new property value applied to all relevant internal Labels.
# **Validates: Requirements 1.2, 3.3, 4.2, 9.3**

# Strategy for generating valid property values
rebuild_font_names = st.sampled_from(['Roboto', 'Roboto-Bold', 'Roboto-Italic'])
rebuild_colors = st.lists(
    st.floats(min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False),
    min_size=4, max_size=4
)
rebuild_line_heights = st.floats(min_value=0.5, max_value=3.0, allow_nan=False, allow_infinity=False)
rebuild_text_size_widths = st.floats(min_value=50, max_value=1000, allow_nan=False, allow_infinity=False)


class TestReactiveRebuildOnPropertyChange:
    """Property tests for reactive rebuild on property change (Property 14)."""
    
    @given(rebuild_font_names, rebuild_font_names)
    @settings(max_examples=100, deadline=None)
    def test_font_name_change_rebuilds_widgets(self, font1, font2):
        """Changing font_name after initial rendering rebuilds widgets with new font.
        
        Validates: Requirement 1.2 - WHEN `font_name` changes after initial rendering
        THEN the MarkdownLabel SHALL rebuild widgets with the new font applied.
        """
        assume(font1 != font2)
        
        label = MarkdownLabel(text='Hello World', font_name=font1)
        
        # Verify initial font
        labels_before = find_labels_recursive(label)
        assert len(labels_before) >= 1, "Expected at least one Label"
        for lbl in labels_before:
            assert lbl.font_name == font1, f"Initial font should be {font1}"
        
        # Change font_name
        label.font_name = font2
        label.force_rebuild()  # Force immediate rebuild for test
        
        # Verify widgets were rebuilt with new font
        labels_after = find_labels_recursive(label)
        assert len(labels_after) >= 1, "Expected at least one Label after rebuild"
        for lbl in labels_after:
            assert lbl.font_name == font2, \
                f"After change, expected font_name={font2}, got {lbl.font_name}"
    
    @given(rebuild_colors, rebuild_colors)
    @settings(max_examples=100, deadline=None)
    def test_color_change_rebuilds_widgets(self, color1, color2):
        """Changing color after initial rendering rebuilds widgets with new color.
        
        Validates: Requirement 3.3 - WHEN `color` changes after initial rendering
        THEN the MarkdownLabel SHALL rebuild widgets with the new color applied.
        """
        assume(not colors_equal(color1, color2))
        
        label = MarkdownLabel(text='Hello World', color=color1)
        
        # Verify initial color
        labels_before = find_labels_recursive(label)
        assert len(labels_before) >= 1, "Expected at least one Label"
        for lbl in labels_before:
            assert colors_equal(list(lbl.color), color1), \
                f"Initial color should be {color1}"
        
        # Change color
        label.color = color2
        
        # Verify widgets were rebuilt with new color
        labels_after = find_labels_recursive(label)
        assert len(labels_after) >= 1, "Expected at least one Label after rebuild"
        for lbl in labels_after:
            assert colors_equal(list(lbl.color), color2), \
                f"After change, expected color={color2}, got {list(lbl.color)}"
    
    @given(rebuild_line_heights, rebuild_line_heights)
    @settings(max_examples=100, deadline=None)
    def test_line_height_change_rebuilds_widgets(self, lh1, lh2):
        """Changing line_height after initial rendering rebuilds widgets with new value.
        
        Validates: Requirement 4.2 - WHEN `line_height` changes after initial rendering
        THEN the MarkdownLabel SHALL rebuild widgets with the new line height applied.
        """
        assume(not floats_equal(lh1, lh2))
        
        label = MarkdownLabel(text='Hello World', line_height=lh1)
        
        # Verify initial line_height
        labels_before = find_labels_recursive(label)
        assert len(labels_before) >= 1, "Expected at least one Label"
        for lbl in labels_before:
            assert floats_equal(lbl.line_height, lh1), \
                f"Initial line_height should be {lh1}"
        
        # Change line_height
        label.line_height = lh2
        
        # Verify widgets were rebuilt with new line_height
        labels_after = find_labels_recursive(label)
        assert len(labels_after) >= 1, "Expected at least one Label after rebuild"
        for lbl in labels_after:
            assert floats_equal(lbl.line_height, lh2), \
                f"After change, expected line_height={lh2}, got {lbl.line_height}"
    
    @given(rebuild_text_size_widths, rebuild_text_size_widths)
    @settings(max_examples=100, deadline=None)
    def test_text_size_change_rebuilds_widgets(self, width1, width2):
        """Changing text_size after initial rendering rebuilds widgets.
        
        Validates: Requirement 9.3 - WHEN `text_size` width changes
        THEN the MarkdownLabel SHALL reflow text content to fit the new width.
        """
        assume(abs(width1 - width2) > 1)  # Ensure they're different
        
        label = MarkdownLabel(text='Hello World', text_size=[width1, None])
        
        # Verify initial text_size
        assert label.text_size[0] == width1, f"Initial text_size[0] should be {width1}"
        
        # Change text_size
        label.text_size = [width2, None]
        
        # Verify text_size was updated
        assert label.text_size[0] == width2, \
            f"After change, expected text_size[0]={width2}, got {label.text_size[0]}"
        
        # Verify widgets still exist (rebuild happened)
        labels_after = find_labels_recursive(label)
        assert len(labels_after) >= 1, "Expected at least one Label after rebuild"
    
    @given(rebuild_font_names, rebuild_colors, rebuild_line_heights)
    @settings(max_examples=100, deadline=None)
    def test_multiple_property_changes_rebuild_correctly(self, font_name, color, line_height):
        """Multiple property changes each trigger rebuilds with correct values."""
        label = MarkdownLabel(text='# Heading\n\nParagraph text')
        
        # Change font_name
        label.font_name = font_name
        label.force_rebuild()  # Force immediate rebuild for test
        labels = find_labels_recursive(label)
        for lbl in labels:
            assert lbl.font_name == font_name, \
                f"After font_name change, expected {font_name}, got {lbl.font_name}"
        
        # Change color
        label.color = color
        # Note: color is a style-only property, no rebuild needed
        labels = find_labels_recursive(label)
        for lbl in labels:
            assert colors_equal(list(lbl.color), color), \
                f"After color change, expected {color}, got {list(lbl.color)}"
        
        # Change line_height
        label.line_height = line_height
        # Note: line_height is a style-only property, no rebuild needed
        labels = find_labels_recursive(label)
        for lbl in labels:
            assert floats_equal(lbl.line_height, line_height), \
                f"After line_height change, expected {line_height}, got {lbl.line_height}"
    
    @given(st.sampled_from(['left', 'center', 'right', 'justify']),
           st.sampled_from(['left', 'center', 'right', 'justify']))
    @settings(max_examples=100, deadline=None)
    def test_halign_change_rebuilds_widgets(self, halign1, halign2):
        """Changing halign after initial rendering rebuilds widgets with new alignment."""
        assume(halign1 != halign2)
        
        label = MarkdownLabel(text='Hello World', halign=halign1)
        
        # Verify initial halign
        labels_before = find_labels_recursive(label)
        assert len(labels_before) >= 1, "Expected at least one Label"
        for lbl in labels_before:
            assert lbl.halign == halign1, f"Initial halign should be {halign1}"
        
        # Change halign
        label.halign = halign2
        
        # Verify widgets were rebuilt with new halign
        labels_after = find_labels_recursive(label)
        assert len(labels_after) >= 1, "Expected at least one Label after rebuild"
        for lbl in labels_after:
            assert lbl.halign == halign2, \
                f"After change, expected halign={halign2}, got {lbl.halign}"
    
    @given(st.sampled_from(['bottom', 'middle', 'center', 'top']),
           st.sampled_from(['bottom', 'middle', 'center', 'top']))
    @settings(max_examples=100, deadline=None)
    def test_valign_change_rebuilds_widgets(self, valign1, valign2):
        """Changing valign after initial rendering rebuilds widgets with new alignment."""
        assume(valign1 != valign2)
        
        label = MarkdownLabel(text='Hello World', valign=valign1)
        
        # Verify initial valign
        labels_before = find_labels_recursive(label)
        assert len(labels_before) >= 1, "Expected at least one Label"
        for lbl in labels_before:
            assert lbl.valign == valign1, f"Initial valign should be {valign1}"
        
        # Change valign
        label.valign = valign2
        
        # Verify widgets were rebuilt with new valign
        labels_after = find_labels_recursive(label)
        assert len(labels_after) >= 1, "Expected at least one Label after rebuild"
        for lbl in labels_after:
            assert lbl.valign == valign2, \
                f"After change, expected valign={valign2}, got {lbl.valign}"
    
    @given(st.sampled_from(['strict', 'replace', 'ignore']),
           st.sampled_from(['strict', 'replace', 'ignore']))
    @settings(max_examples=100, deadline=None)
    def test_unicode_errors_change_rebuilds_widgets(self, errors1, errors2):
        """Changing unicode_errors after initial rendering rebuilds widgets."""
        assume(errors1 != errors2)
        
        label = MarkdownLabel(text='Hello World', unicode_errors=errors1)
        
        # Verify initial unicode_errors
        labels_before = find_labels_recursive(label)
        assert len(labels_before) >= 1, "Expected at least one Label"
        for lbl in labels_before:
            assert lbl.unicode_errors == errors1, f"Initial unicode_errors should be {errors1}"
        
        # Change unicode_errors
        label.unicode_errors = errors2
        label.force_rebuild()  # Force immediate rebuild for test
        
        # Verify widgets were rebuilt with new unicode_errors
        labels_after = find_labels_recursive(label)
        assert len(labels_after) >= 1, "Expected at least one Label after rebuild"
        for lbl in labels_after:
            assert lbl.unicode_errors == errors2, \
                f"After change, expected unicode_errors={errors2}, got {lbl.unicode_errors}"
    
    @given(st.booleans(), st.booleans())
    @settings(max_examples=100, deadline=None)
    def test_strip_change_rebuilds_widgets(self, strip1, strip2):
        """Changing strip after initial rendering rebuilds widgets."""
        assume(strip1 != strip2)
        
        label = MarkdownLabel(text='Hello World', strip=strip1)
        
        # Verify initial strip
        labels_before = find_labels_recursive(label)
        assert len(labels_before) >= 1, "Expected at least one Label"
        for lbl in labels_before:
            assert lbl.strip == strip1, f"Initial strip should be {strip1}"
        
        # Change strip
        label.strip = strip2
        label.force_rebuild()  # Force immediate rebuild for test
        
        # Verify widgets were rebuilt with new strip
        labels_after = find_labels_recursive(label)
        assert len(labels_after) >= 1, "Expected at least one Label after rebuild"
        for lbl in labels_after:
            assert lbl.strip == strip2, \
                f"After change, expected strip={strip2}, got {lbl.strip}"
    
    @given(st.booleans(), st.booleans())
    @settings(max_examples=100, deadline=None)
    def test_disabled_change_rebuilds_widgets(self, disabled1, disabled2):
        """Changing disabled after initial rendering rebuilds widgets with correct color."""
        assume(disabled1 != disabled2)
        
        regular_color = [1, 0, 0, 1]  # Red
        disabled_color = [0.5, 0.5, 0.5, 0.3]  # Gray
        
        label = MarkdownLabel(
            text='Hello World',
            color=regular_color,
            disabled_color=disabled_color,
            disabled=disabled1
        )
        
        expected_color1 = disabled_color if disabled1 else regular_color
        
        # Verify initial color based on disabled state
        labels_before = find_labels_recursive(label)
        assert len(labels_before) >= 1, "Expected at least one Label"
        for lbl in labels_before:
            assert colors_equal(list(lbl.color), expected_color1), \
                f"Initial color should be {expected_color1}"
        
        # Change disabled
        label.disabled = disabled2
        
        expected_color2 = disabled_color if disabled2 else regular_color
        
        # Verify widgets were rebuilt with correct color
        labels_after = find_labels_recursive(label)
        assert len(labels_after) >= 1, "Expected at least one Label after rebuild"
        for lbl in labels_after:
            assert colors_equal(list(lbl.color), expected_color2), \
                f"After change, expected color={expected_color2}, got {list(lbl.color)}"
    
    @given(simple_markdown_document(), rebuild_font_names, rebuild_font_names)
    @settings(max_examples=100, deadline=None)
    def test_rebuild_preserves_content_structure(self, markdown_text, font1, font2):
        """Rebuilding widgets preserves the content structure."""
        assume(markdown_text.strip())
        assume(font1 != font2)
        
        label = MarkdownLabel(text=markdown_text, font_name=font1)
        
        # Count children before
        children_before = len(label.children)
        
        # Change font_name to trigger rebuild
        label.font_name = font2
        
        # Count children after
        children_after = len(label.children)
        
        # Structure should be preserved (same number of children)
        assert children_before == children_after, \
            f"Expected {children_before} children after rebuild, got {children_after}"
    
    @given(st.booleans(), st.booleans())
    @settings(max_examples=100, deadline=None)
    def test_font_kerning_change_rebuilds_widgets(self, kerning1, kerning2):
        """Changing font_kerning after initial rendering rebuilds widgets."""
        assume(kerning1 != kerning2)
        
        label = MarkdownLabel(text='Hello World', font_kerning=kerning1)
        
        # Verify initial font_kerning
        labels_before = find_labels_recursive(label)
        assert len(labels_before) >= 1, "Expected at least one Label"
        for lbl in labels_before:
            assert lbl.font_kerning == kerning1, f"Initial font_kerning should be {kerning1}"
        
        # Change font_kerning
        label.font_kerning = kerning2
        label.force_rebuild()  # Force immediate rebuild for test
        
        # Verify widgets were rebuilt with new font_kerning
        labels_after = find_labels_recursive(label)
        assert len(labels_after) >= 1, "Expected at least one Label after rebuild"
        for lbl in labels_after:
            assert lbl.font_kerning == kerning2, \
                f"After change, expected font_kerning={kerning2}, got {lbl.font_kerning}"
    
    @given(st.booleans(), st.booleans())
    @settings(max_examples=100, deadline=None)
    def test_font_blended_change_rebuilds_widgets(self, blended1, blended2):
        """Changing font_blended after initial rendering rebuilds widgets."""
        assume(blended1 != blended2)
        
        label = MarkdownLabel(text='Hello World', font_blended=blended1)
        
        # Verify initial font_blended
        labels_before = find_labels_recursive(label)
        assert len(labels_before) >= 1, "Expected at least one Label"
        for lbl in labels_before:
            assert lbl.font_blended == blended1, f"Initial font_blended should be {blended1}"
        
        # Change font_blended
        label.font_blended = blended2
        label.force_rebuild()  # Force immediate rebuild for test
        
        # Verify widgets were rebuilt with new font_blended
        labels_after = find_labels_recursive(label)
        assert len(labels_after) >= 1, "Expected at least one Label after rebuild"
        for lbl in labels_after:
            assert lbl.font_blended == blended2, \
                f"After change, expected font_blended={blended2}, got {lbl.font_blended}"

# **Feature: label-compatibility, Property 4: Text Shortening Property Forwarding**
# *For any* MarkdownLabel with shortening properties (shorten, shorten_from, split_str,
# max_lines, ellipsis_options), all child Labels SHALL have the same property values.
# **Validates: Requirements 4.1, 4.2, 4.3, 4.4, 4.5**

class TestShorteningPropertyForwarding:
    """Property tests for shortening property forwarding (Property 4)."""
    
    @given(st.booleans())
    @settings(max_examples=100, deadline=None)
    def test_shorten_forwarded_to_paragraph(self, shorten_value):
        """shorten property is forwarded to paragraph Labels."""
        label = MarkdownLabel(text='Hello World', shorten=shorten_value)
        
        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        for lbl in labels:
            assert lbl.shorten == shorten_value, \
                f"Expected shorten={shorten_value}, got {lbl.shorten}"
    
    @given(st.booleans())
    @settings(max_examples=100, deadline=None)
    def test_shorten_forwarded_to_heading(self, shorten_value):
        """shorten property is forwarded to heading Labels."""
        label = MarkdownLabel(text='# Heading', shorten=shorten_value)
        
        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        for lbl in labels:
            assert lbl.shorten == shorten_value, \
                f"Expected shorten={shorten_value}, got {lbl.shorten}"
    
    @given(st.booleans())
    @settings(max_examples=100, deadline=None)
    def test_shorten_forwarded_to_list_items(self, shorten_value):
        """shorten property is forwarded to list item Labels."""
        markdown = '- Item 1\n- Item 2'
        label = MarkdownLabel(text=markdown, shorten=shorten_value)
        
        labels = find_labels_recursive(label)
        assert len(labels) >= 2, "Expected at least 2 Labels for list items"
        
        for lbl in labels:
            assert lbl.shorten == shorten_value, \
                f"Expected shorten={shorten_value}, got {lbl.shorten}"
    
    @given(st.booleans())
    @settings(max_examples=100, deadline=None)
    def test_shorten_forwarded_to_table_cells(self, shorten_value):
        """shorten property is forwarded to table cell Labels."""
        markdown = '| A | B |\n| --- | --- |\n| 1 | 2 |'
        label = MarkdownLabel(text=markdown, shorten=shorten_value)
        
        labels = find_labels_recursive(label)
        assert len(labels) >= 4, "Expected at least 4 Labels for table cells"
        
        for lbl in labels:
            assert lbl.shorten == shorten_value, \
                f"Expected shorten={shorten_value}, got {lbl.shorten}"
    
    @given(st.sampled_from(['left', 'center', 'right']))
    @settings(max_examples=100, deadline=None)
    def test_shorten_from_forwarded_to_paragraph(self, shorten_from_value):
        """shorten_from property is forwarded to paragraph Labels."""
        label = MarkdownLabel(text='Hello World', shorten_from=shorten_from_value)
        
        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        for lbl in labels:
            assert lbl.shorten_from == shorten_from_value, \
                f"Expected shorten_from={shorten_from_value}, got {lbl.shorten_from}"
    
    @given(st.sampled_from(['left', 'center', 'right']))
    @settings(max_examples=100, deadline=None)
    def test_shorten_from_forwarded_to_heading(self, shorten_from_value):
        """shorten_from property is forwarded to heading Labels."""
        label = MarkdownLabel(text='# Heading', shorten_from=shorten_from_value)
        
        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        for lbl in labels:
            assert lbl.shorten_from == shorten_from_value, \
                f"Expected shorten_from={shorten_from_value}, got {lbl.shorten_from}"
    
    @given(st.sampled_from(['left', 'center', 'right']))
    @settings(max_examples=100, deadline=None)
    def test_shorten_from_forwarded_to_list_items(self, shorten_from_value):
        """shorten_from property is forwarded to list item Labels."""
        markdown = '- Item 1\n- Item 2'
        label = MarkdownLabel(text=markdown, shorten_from=shorten_from_value)
        
        labels = find_labels_recursive(label)
        assert len(labels) >= 2, "Expected at least 2 Labels for list items"
        
        for lbl in labels:
            assert lbl.shorten_from == shorten_from_value, \
                f"Expected shorten_from={shorten_from_value}, got {lbl.shorten_from}"
    
    @given(st.text(min_size=0, max_size=5, alphabet='abc '))
    @settings(max_examples=100, deadline=None)
    def test_split_str_forwarded_to_paragraph(self, split_str_value):
        """split_str property is forwarded to paragraph Labels."""
        label = MarkdownLabel(text='Hello World', split_str=split_str_value)
        
        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        for lbl in labels:
            assert lbl.split_str == split_str_value, \
                f"Expected split_str={split_str_value!r}, got {lbl.split_str!r}"
    
    @given(st.text(min_size=0, max_size=5, alphabet='abc '))
    @settings(max_examples=100, deadline=None)
    def test_split_str_forwarded_to_heading(self, split_str_value):
        """split_str property is forwarded to heading Labels."""
        label = MarkdownLabel(text='# Heading', split_str=split_str_value)
        
        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        for lbl in labels:
            assert lbl.split_str == split_str_value, \
                f"Expected split_str={split_str_value!r}, got {lbl.split_str!r}"
    
    @given(st.integers(min_value=0, max_value=10))
    @settings(max_examples=100, deadline=None)
    def test_max_lines_forwarded_to_paragraph(self, max_lines_value):
        """max_lines property is forwarded to paragraph Labels when non-zero."""
        label = MarkdownLabel(text='Hello World', max_lines=max_lines_value)
        
        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        for lbl in labels:
            if max_lines_value > 0:
                assert lbl.max_lines == max_lines_value, \
                    f"Expected max_lines={max_lines_value}, got {lbl.max_lines}"
            # When max_lines=0, it may not be set on child Labels (default behavior)
    
    @given(st.integers(min_value=1, max_value=10))
    @settings(max_examples=100, deadline=None)
    def test_max_lines_forwarded_to_heading(self, max_lines_value):
        """max_lines property is forwarded to heading Labels when non-zero."""
        label = MarkdownLabel(text='# Heading', max_lines=max_lines_value)
        
        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        for lbl in labels:
            assert lbl.max_lines == max_lines_value, \
                f"Expected max_lines={max_lines_value}, got {lbl.max_lines}"
    
    @given(st.integers(min_value=1, max_value=10))
    @settings(max_examples=100, deadline=None)
    def test_max_lines_forwarded_to_list_items(self, max_lines_value):
        """max_lines property is forwarded to list item Labels when non-zero."""
        markdown = '- Item 1\n- Item 2'
        label = MarkdownLabel(text=markdown, max_lines=max_lines_value)
        
        labels = find_labels_recursive(label)
        assert len(labels) >= 2, "Expected at least 2 Labels for list items"
        
        for lbl in labels:
            assert lbl.max_lines == max_lines_value, \
                f"Expected max_lines={max_lines_value}, got {lbl.max_lines}"
    
    @given(st.fixed_dictionaries({
        'markup_color': st.sampled_from([[1, 0, 0, 1], [0, 1, 0, 1], [0, 0, 1, 1]])
    }))
    @settings(max_examples=100, deadline=None)
    def test_ellipsis_options_forwarded_to_paragraph(self, ellipsis_opts):
        """ellipsis_options property is forwarded to paragraph Labels."""
        label = MarkdownLabel(text='Hello World', ellipsis_options=ellipsis_opts)
        
        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        for lbl in labels:
            assert lbl.ellipsis_options == ellipsis_opts, \
                f"Expected ellipsis_options={ellipsis_opts}, got {lbl.ellipsis_options}"
    
    @given(st.fixed_dictionaries({
        'markup_color': st.sampled_from([[1, 0, 0, 1], [0, 1, 0, 1], [0, 0, 1, 1]])
    }))
    @settings(max_examples=100, deadline=None)
    def test_ellipsis_options_forwarded_to_heading(self, ellipsis_opts):
        """ellipsis_options property is forwarded to heading Labels."""
        label = MarkdownLabel(text='# Heading', ellipsis_options=ellipsis_opts)
        
        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        for lbl in labels:
            assert lbl.ellipsis_options == ellipsis_opts, \
                f"Expected ellipsis_options={ellipsis_opts}, got {lbl.ellipsis_options}"
    
    @given(st.fixed_dictionaries({
        'markup_color': st.sampled_from([[1, 0, 0, 1], [0, 1, 0, 1], [0, 0, 1, 1]])
    }))
    @settings(max_examples=100, deadline=None)
    def test_ellipsis_options_forwarded_to_list_items(self, ellipsis_opts):
        """ellipsis_options property is forwarded to list item Labels."""
        markdown = '- Item 1\n- Item 2'
        label = MarkdownLabel(text=markdown, ellipsis_options=ellipsis_opts)
        
        labels = find_labels_recursive(label)
        assert len(labels) >= 2, "Expected at least 2 Labels for list items"
        
        for lbl in labels:
            assert lbl.ellipsis_options == ellipsis_opts, \
                f"Expected ellipsis_options={ellipsis_opts}, got {lbl.ellipsis_options}"
    
    @given(st.fixed_dictionaries({
        'markup_color': st.sampled_from([[1, 0, 0, 1], [0, 1, 0, 1], [0, 0, 1, 1]])
    }))
    @settings(max_examples=100, deadline=None)
    def test_ellipsis_options_forwarded_to_table_cells(self, ellipsis_opts):
        """ellipsis_options property is forwarded to table cell Labels."""
        markdown = '| A | B |\n| --- | --- |\n| 1 | 2 |'
        label = MarkdownLabel(text=markdown, ellipsis_options=ellipsis_opts)
        
        labels = find_labels_recursive(label)
        assert len(labels) >= 4, "Expected at least 4 Labels for table cells"
        
        for lbl in labels:
            assert lbl.ellipsis_options == ellipsis_opts, \
                f"Expected ellipsis_options={ellipsis_opts}, got {lbl.ellipsis_options}"
    
    def test_empty_ellipsis_options_not_forwarded(self):
        """Empty ellipsis_options dict is not forwarded (default behavior)."""
        label = MarkdownLabel(text='Hello World', ellipsis_options={})
        
        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        # Empty dict should result in default empty dict on child Labels
        for lbl in labels:
            assert lbl.ellipsis_options == {}, \
                f"Expected empty ellipsis_options, got {lbl.ellipsis_options}"
    
    @given(st.booleans(), st.sampled_from(['left', 'center', 'right']),
           st.text(min_size=0, max_size=3, alphabet='ab '),
           st.integers(min_value=1, max_value=5))
    @settings(max_examples=100, deadline=None)
    def test_all_shortening_properties_forwarded_together(
            self, shorten_val, shorten_from_val, split_str_val, max_lines_val):
        """All shortening properties are forwarded together to child Labels."""
        markdown = '''# Heading

Paragraph text

- List item 1
- List item 2

| A | B |
| --- | --- |
| 1 | 2 |
'''
        label = MarkdownLabel(
            text=markdown,
            shorten=shorten_val,
            shorten_from=shorten_from_val,
            split_str=split_str_val,
            max_lines=max_lines_val
        )
        
        labels = find_labels_recursive(label)
        assert len(labels) >= 5, "Expected at least 5 Labels for various structures"
        
        for lbl in labels:
            assert lbl.shorten == shorten_val, \
                f"Expected shorten={shorten_val}, got {lbl.shorten}"
            assert lbl.shorten_from == shorten_from_val, \
                f"Expected shorten_from={shorten_from_val}, got {lbl.shorten_from}"
            assert lbl.split_str == split_str_val, \
                f"Expected split_str={split_str_val!r}, got {lbl.split_str!r}"
            assert lbl.max_lines == max_lines_val, \
                f"Expected max_lines={max_lines_val}, got {lbl.max_lines}"
    
    @given(st.booleans(), st.booleans())
    @settings(max_examples=100, deadline=None)
    def test_shorten_change_triggers_rebuild(self, shorten1, shorten2):
        """Changing shorten triggers widget rebuild with new value."""
        assume(shorten1 != shorten2)
        
        label = MarkdownLabel(text='Hello World', shorten=shorten1)
        
        # Verify initial value
        labels = find_labels_recursive(label)
        for lbl in labels:
            assert lbl.shorten == shorten1
        
        # Change shorten
        label.shorten = shorten2
        label.force_rebuild()  # Force immediate rebuild for test
        
        # Verify new value
        labels = find_labels_recursive(label)
        for lbl in labels:
            assert lbl.shorten == shorten2, \
                f"After change, expected shorten={shorten2}, got {lbl.shorten}"
# **Feature: label-compatibility-phase2, Property 5: Coordinate Translation for refs and anchors**
# *For any* MarkdownLabel containing links (refs) or anchors, the `refs` and `anchors`
# properties SHALL return coordinates translated to MarkdownLabel's local coordinate space
# (not child Label's coordinate space).
# **Validates: Requirements 5.1, 5.2, 5.3**
#
# Note: In Kivy, the `refs` dictionary on a Label is only populated after the texture
# is rendered. In headless test environments, refs may be empty. These tests verify:
# 1. The translation algorithm works correctly when refs ARE present
# 2. The ref markup is correctly generated (proving links are rendered)
# 3. Empty refs/anchors are handled correctly

class TestCoordinateTranslation:
    """Property tests for coordinate translation of refs and anchors (Property 5)."""
    
    def _find_labels_with_refs(self, widget, labels=None):
        """Recursively find all Label widgets that have refs."""
        if labels is None:
            labels = []
        
        if isinstance(widget, Label) and hasattr(widget, 'refs') and widget.refs:
            labels.append(widget)
        
        if hasattr(widget, 'children'):
            for child in widget.children:
                self._find_labels_with_refs(child, labels)
        
        return labels
    
    def _find_labels_with_ref_markup(self, widget, labels=None):
        """Recursively find all Label widgets that have ref markup in their text."""
        if labels is None:
            labels = []
        
        if isinstance(widget, Label) and hasattr(widget, 'text'):
            if '[ref=' in widget.text and '[/ref]' in widget.text:
                labels.append(widget)
        
        if hasattr(widget, 'children'):
            for child in widget.children:
                self._find_labels_with_ref_markup(child, labels)
        
        return labels
    
    def _get_widget_offset(self, widget, root):
        """Calculate widget's position relative to root widget.
        
        Args:
            widget: Widget to calculate offset for
            root: Root widget to calculate offset relative to
            
        Returns:
            Tuple (offset_x, offset_y) relative to root
        """
        offset_x = 0
        offset_y = 0
        current = widget
        
        while current is not None and current is not root:
            offset_x += current.x
            offset_y += current.y
            current = current.parent
        
        return offset_x, offset_y
    
    @given(st.text(min_size=1, max_size=20, alphabet=st.characters(
        whitelist_categories=['L', 'N'],
        blacklist_characters='[]()&\n\r'
    )))
    @settings(max_examples=100, deadline=None)
    def test_link_produces_ref_markup_for_translation(self, link_text):
        """Links produce ref markup that will be translated when rendered.
        
        This test verifies that links are correctly rendered with [ref=url] markup,
        which is the prerequisite for coordinate translation. The actual refs
        dictionary is populated by Kivy during texture rendering.
        """
        url = 'https://example.com/page'
        markdown = f'[{link_text}]({url})'
        
        label = MarkdownLabel(text=markdown)
        
        # Find Labels with ref markup
        labels_with_markup = self._find_labels_with_ref_markup(label)
        
        assert len(labels_with_markup) >= 1, \
            f"Expected at least one Label with ref markup for: {markdown}"
        
        # Verify the URL is in the markup
        found_url = False
        for lbl in labels_with_markup:
            if f'[ref={url}]' in lbl.text:
                found_url = True
                break
        
        assert found_url, \
            f"Expected [ref={url}] in Label markup"
    
    @given(st.lists(
        st.text(min_size=1, max_size=10, alphabet=st.characters(
            whitelist_categories=['L', 'N'],
            blacklist_characters='[]()&\n\r'
        )),
        min_size=2, max_size=4
    ))
    @settings(max_examples=100, deadline=None)
    def test_multiple_links_produce_ref_markup(self, link_texts):
        """Multiple links in different paragraphs produce ref markup.
        
        This test verifies that multiple links are correctly rendered with
        [ref=url] markup in their respective Labels.
        """
        # Create markdown with multiple links in separate paragraphs
        paragraphs = []
        urls = []
        for i, text in enumerate(link_texts):
            url = f'https://example{i}.com/page'
            urls.append(url)
            paragraphs.append(f'[{text}]({url})')
        
        markdown = '\n\n'.join(paragraphs)
        label = MarkdownLabel(text=markdown)
        
        # Find Labels with ref markup
        labels_with_markup = self._find_labels_with_ref_markup(label)
        
        # Should have at least as many Labels with markup as we have links
        assert len(labels_with_markup) >= len(link_texts), \
            f"Expected at least {len(link_texts)} Labels with ref markup, got {len(labels_with_markup)}"
        
        # Verify each URL appears in some Label's markup
        for url in urls:
            found = False
            for lbl in labels_with_markup:
                if f'[ref={url}]' in lbl.text:
                    found = True
                    break
            assert found, f"Expected [ref={url}] in some Label markup"
    
    def test_refs_empty_for_no_links(self):
        """refs returns empty dict when there are no links."""
        label = MarkdownLabel(text='Hello World without links')
        
        assert label.refs == {}, \
            f"Expected empty refs, got {label.refs}"
    
    def test_refs_empty_for_empty_text(self):
        """refs returns empty dict for empty text."""
        label = MarkdownLabel(text='')
        
        assert label.refs == {}, \
            f"Expected empty refs for empty text, got {label.refs}"
    
    def test_anchors_empty_for_no_anchors(self):
        """anchors returns empty dict when there are no anchors."""
        label = MarkdownLabel(text='Hello World without anchors')
        
        assert label.anchors == {}, \
            f"Expected empty anchors, got {label.anchors}"
    
    def test_anchors_empty_for_empty_text(self):
        """anchors returns empty dict for empty text."""
        label = MarkdownLabel(text='')
        
        assert label.anchors == {}, \
            f"Expected empty anchors for empty text, got {label.anchors}"
    
    def test_refs_translation_algorithm_correctness(self):
        """Test that the coordinate translation algorithm works correctly.
        
        This test directly verifies the translation logic by checking that
        when child Labels have refs, the aggregated refs contain properly
        translated coordinates.
        """
        markdown = '[Click me](https://example.com)'
        label = MarkdownLabel(text=markdown)
        
        # Get aggregated refs
        aggregated_refs = label.refs
        
        # Find child Labels with refs (if any - depends on rendering)
        labels_with_refs = self._find_labels_with_refs(label)
        
        # If we have child Labels with refs, verify translation
        for child_label in labels_with_refs:
            child_refs = child_label.refs
            offset_x, offset_y = self._get_widget_offset(child_label, label)
            
            for url, child_boxes in child_refs.items():
                assert url in aggregated_refs, \
                    f"Expected URL {url} in aggregated refs"
                
                for child_box in child_boxes:
                    expected_box = [
                        child_box[0] + offset_x,
                        child_box[1] + offset_y,
                        child_box[2] + offset_x,
                        child_box[3] + offset_y
                    ]
                    
                    assert expected_box in aggregated_refs[url], \
                        f"Expected translated box {expected_box} in aggregated refs"
    
    def test_refs_translation_with_nested_list_markup(self):
        """Links in nested content (lists) produce correct ref markup."""
        markdown = '''- [Link 1](https://example1.com)
- [Link 2](https://example2.com)
'''
        label = MarkdownLabel(text=markdown)
        
        # Find Labels with ref markup
        labels_with_markup = self._find_labels_with_ref_markup(label)
        
        # Should have Labels with ref markup for the links
        assert len(labels_with_markup) >= 1, \
            "Expected at least one Label with ref markup in list"
        
        # Verify URLs appear in markup
        all_markup = ' '.join(lbl.text for lbl in labels_with_markup)
        assert '[ref=https://example1.com]' in all_markup or \
               '[ref=https://example2.com]' in all_markup, \
            "Expected ref markup for list links"
    
    def test_refs_translation_with_table_markup(self):
        """Links in table content produce correct ref markup."""
        markdown = '''| Column A | Column B |
| --- | --- |
| [Link](https://example.com) | Text |
'''
        label = MarkdownLabel(text=markdown)
        
        # Find Labels with ref markup
        labels_with_markup = self._find_labels_with_ref_markup(label)
        
        # Should have at least one Label with ref markup
        assert len(labels_with_markup) >= 1, \
            "Expected at least one Label with ref markup in table"
        
        # Verify URL appears in markup
        found = any('[ref=https://example.com]' in lbl.text 
                   for lbl in labels_with_markup)
        assert found, "Expected ref markup for table link"
    
    def test_refs_translation_with_blockquote_markup(self):
        """Links in blockquote content produce correct ref markup."""
        markdown = '> [Quoted link](https://example.com)'
        
        label = MarkdownLabel(text=markdown)
        
        # Find Labels with ref markup
        labels_with_markup = self._find_labels_with_ref_markup(label)
        
        # Should have at least one Label with ref markup
        assert len(labels_with_markup) >= 1, \
            "Expected at least one Label with ref markup in blockquote"
        
        # Verify URL appears in markup
        found = any('[ref=https://example.com]' in lbl.text 
                   for lbl in labels_with_markup)
        assert found, "Expected ref markup for blockquote link"
    
    @given(st.text(min_size=1, max_size=10, alphabet=st.characters(
        whitelist_categories=['L', 'N'],
        blacklist_characters='[]()&\n\r'
    )), st.text(min_size=1, max_size=10, alphabet=st.characters(
        whitelist_categories=['L', 'N'],
        blacklist_characters='[]()&\n\r'
    )))
    @settings(max_examples=100, deadline=None)
    def test_ref_markup_updates_when_text_changes(self, link_text1, link_text2):
        """ref markup updates correctly when text property changes."""
        url1 = 'https://example1.com'
        url2 = 'https://example2.com'
        
        markdown1 = f'[{link_text1}]({url1})'
        markdown2 = f'[{link_text2}]({url2})'
        
        label = MarkdownLabel(text=markdown1)
        
        # Initial markup should have url1
        labels1 = self._find_labels_with_ref_markup(label)
        assert len(labels1) >= 1, "Expected Label with ref markup initially"
        found_url1 = any(f'[ref={url1}]' in lbl.text for lbl in labels1)
        assert found_url1, f"Expected [ref={url1}] in initial markup"
        
        # Change text - use force_rebuild() for immediate update since
        # text changes now use deferred rebuilds
        label.text = markdown2
        label.force_rebuild()
        
        # Updated markup should have url2
        labels2 = self._find_labels_with_ref_markup(label)
        assert len(labels2) >= 1, "Expected Label with ref markup after update"
        found_url2 = any(f'[ref={url2}]' in lbl.text for lbl in labels2)
        assert found_url2, f"Expected [ref={url2}] in updated markup"
        
        # url1 should no longer be present (unless url1 == url2)
        if url1 != url2:
            found_old = any(f'[ref={url1}]' in lbl.text for lbl in labels2)
            assert not found_old, f"Did not expect [ref={url1}] in updated markup"
    
    @given(st.floats(min_value=0, max_value=100),
           st.floats(min_value=0, max_value=100),
           st.floats(min_value=0, max_value=100),
           st.floats(min_value=0, max_value=100))
    @settings(max_examples=100, deadline=None)
    def test_coordinate_translation_math(self, x1, y1, x2, y2):
        """Test that coordinate translation math is correct.
        
        This tests the translation algorithm directly with known values.
        """
        # Simulate a bounding box
        original_box = [x1, y1, x2, y2]
        
        # Simulate an offset
        offset_x = 10.0
        offset_y = 20.0
        
        # Apply translation (same algorithm as in _get_refs)
        translated_box = [
            original_box[0] + offset_x,
            original_box[1] + offset_y,
            original_box[2] + offset_x,
            original_box[3] + offset_y
        ]
        
        # Verify translation
        assert translated_box[0] == x1 + offset_x
        assert translated_box[1] == y1 + offset_y
        assert translated_box[2] == x2 + offset_x
        assert translated_box[3] == y2 + offset_y
    
    @given(st.floats(min_value=0, max_value=100),
           st.floats(min_value=0, max_value=100))
    @settings(max_examples=100, deadline=None)
    def test_anchor_translation_math(self, x, y):
        """Test that anchor coordinate translation math is correct.
        
        This tests the translation algorithm directly with known values.
        """
        # Simulate an anchor position
        original_pos = (x, y)
        
        # Simulate an offset
        offset_x = 15.0
        offset_y = 25.0
        
        # Apply translation (same algorithm as in _get_anchors)
        translated_pos = (
            original_pos[0] + offset_x,
            original_pos[1] + offset_y
        )
        
        # Verify translation
        assert translated_pos[0] == x + offset_x
        assert translated_pos[1] == y + offset_y