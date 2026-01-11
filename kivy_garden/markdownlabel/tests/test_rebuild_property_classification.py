"""
Property classification tests for MarkdownLabel rebuild semantics.

This module contains tests that verify the STYLE_ONLY_PROPERTIES and
STRUCTURE_PROPERTIES sets are correctly defined, mutually exclusive,
and contain the expected properties after optimization reclassification.

Tests are designed to run in headless CI environments without requiring a Kivy window.
"""

from kivy_garden.markdownlabel import MarkdownLabel


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
        expected_structure = {
            'text',
            'link_style',
            'render_mode',
            'strict_label_mode',
            'link_color',
            'code_bg_color',
        }
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
            'padding',
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

        Original: 17 properties (including padding)
        Reclassified: +14 properties
        Total: 31 properties
        """
        # Original style-only properties: 17 (including padding)
        # Reclassified properties: 14
        # Total expected: 31
        expected_count = 31
        actual_count = len(MarkdownLabel.STYLE_ONLY_PROPERTIES)
        assert actual_count == expected_count, (
            f"STYLE_ONLY_PROPERTIES count mismatch. "
            f"Expected: {expected_count}, Got: {actual_count}"
        )

    def test_structure_properties_count(self):
        """STRUCTURE_PROPERTIES has expected count after reclassification.

        After reclassification, 6 properties remain:
        text, link_style, render_mode, strict_label_mode, link_color, code_bg_color
        """
        expected_count = 6
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
