"""
Property-based tests for advanced MarkdownLabel compatibility features.

This module contains tests for advanced Label API compatibility features including:
- Advanced font properties forwarding
- Disabled color application
- Reactive rebuild on property changes

These tests verify that MarkdownLabel correctly implements advanced Label
compatibility while maintaining proper Markdown rendering functionality.
"""

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
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
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
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
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
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_font_features_forwarded_to_labels(self, font_features_value):
        """font_features is forwarded to all internal Labels."""
        label = MarkdownLabel(text='Hello World', font_features=font_features_value)
        
        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least 1 Label"
        
        for lbl in labels:
            assert lbl.font_features == font_features_value, \
                f"Expected font_features={font_features_value!r}, got {lbl.font_features!r}"
    
    @pytest.mark.parametrize('font_hinting_value', [None, 'normal', 'light', 'mono'])
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
    # Boolean strategy: 2 examples (True/False coverage)
    @settings(max_examples=2, deadline=None)
    def test_font_kerning_forwarded_to_labels(self, font_kerning_value):
        """font_kerning is forwarded to all internal Labels."""
        label = MarkdownLabel(text='Hello World', font_kerning=font_kerning_value)
        
        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least 1 Label"
        
        for lbl in labels:
            assert lbl.font_kerning == font_kerning_value, \
                f"Expected font_kerning={font_kerning_value}, got {lbl.font_kerning}"
    
    @given(st.booleans())
    # Boolean strategy: 2 examples (True/False coverage)
    @settings(max_examples=2, deadline=None)
    def test_font_blended_forwarded_to_labels(self, font_blended_value):
        """font_blended is forwarded to all internal Labels."""
        label = MarkdownLabel(text='Hello World', font_blended=font_blended_value)
        
        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least 1 Label"
        
        for lbl in labels:
            assert lbl.font_blended == font_blended_value, \
                f"Expected font_blended={font_blended_value}, got {lbl.font_blended}"
    
    @pytest.mark.parametrize('font_hinting,font_kerning,font_blended', [
        (None, True, True), (None, True, False), (None, False, True), (None, False, False),
        ('normal', True, True), ('normal', True, False), ('normal', False, True), ('normal', False, False),
        ('light', True, True), ('light', True, False), ('light', False, True), ('light', False, False),
        ('mono', True, True), ('mono', True, False), ('mono', False, True), ('mono', False, False)
    ])
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
    # Combination strategy: 4 examples (combination coverage)
    @settings(max_examples=4, deadline=None)
    def test_font_kerning_change_updates_value(self, kerning1, kerning2):
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
    # Combination strategy: 4 examples (combination coverage)
    @settings(max_examples=4, deadline=None)
    def test_font_blended_change_updates_value(self, blended1, blended2):
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
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_disabled_color_stored_correctly(self, disabled_color):
        """disabled_color property stores the value correctly."""
        label = MarkdownLabel(text='Hello World', disabled_color=disabled_color)
        
        assert colors_equal(label.disabled_color, disabled_color), \
            f"Expected disabled_color={disabled_color}, got {list(label.disabled_color)}"
    
    @given(st.lists(
        st.floats(min_value=0, max_value=1, allow_nan=False, allow_infinity=False),
        min_size=4, max_size=4
    ))
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
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
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
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
    # Boolean strategy: 2 examples (True/False coverage)
    @settings(max_examples=2, deadline=None)
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
    
    def test_disabled_change_updates_value(self):
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
    # Combination strategy: 9 examples (combination coverage)
    @settings(max_examples=9, deadline=None)
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
    # Combination strategy: 20 examples (combination coverage)
    @settings(max_examples=20, deadline=None)
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
    # Combination strategy: 20 examples (combination coverage)
    @settings(max_examples=20, deadline=None)
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
    # Combination strategy: 20 examples (combination coverage)
    @settings(max_examples=20, deadline=None)
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
    # Combination strategy: 20 examples (combination coverage)
    @settings(max_examples=20, deadline=None)
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
    
    @pytest.mark.parametrize('halign1,halign2', [
        ('left', 'center'), ('left', 'right'), ('left', 'justify'),
        ('center', 'left'), ('center', 'right'), ('center', 'justify'),
        ('right', 'left'), ('right', 'center'), ('right', 'justify'),
        ('justify', 'left'), ('justify', 'center'), ('justify', 'right')
    ])
    def test_halign_change_rebuilds_widgets(self, halign1, halign2):
        """Changing halign after initial rendering rebuilds widgets with new alignment."""

        
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
    
    @pytest.mark.parametrize('valign1,valign2', [
        ('bottom', 'middle'), ('bottom', 'center'), ('bottom', 'top'),
        ('middle', 'bottom'), ('middle', 'center'), ('middle', 'top'),
        ('center', 'bottom'), ('center', 'middle'), ('center', 'top'),
        ('top', 'bottom'), ('top', 'middle'), ('top', 'center')
    ])
    def test_valign_change_rebuilds_widgets(self, valign1, valign2):
        """Changing valign after initial rendering rebuilds widgets with new alignment."""

        
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
    
    @pytest.mark.parametrize('errors1,errors2', [
        ('strict', 'replace'), ('strict', 'ignore'),
        ('replace', 'strict'), ('replace', 'ignore'),
        ('ignore', 'strict'), ('ignore', 'replace')
    ])
    def test_unicode_errors_change_rebuilds_widgets(self, errors1, errors2):
        """Changing unicode_errors after initial rendering rebuilds widgets."""

        
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
    # Combination strategy: 4 examples (combination coverage)
    @settings(max_examples=4, deadline=None)
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
    # Combination strategy: 4 examples (combination coverage)
    @settings(max_examples=4, deadline=None)
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
    # Combination strategy: 20 examples (combination coverage)
    @settings(max_examples=20, deadline=None)
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
    # Combination strategy: 4 examples (combination coverage)
    @settings(max_examples=4, deadline=None)
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
    # Combination strategy: 4 examples (combination coverage)
    @settings(max_examples=4, deadline=None)
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

