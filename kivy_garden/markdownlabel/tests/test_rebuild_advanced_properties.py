"""
Advanced property tests for MarkdownLabel rebuild semantics.

This module contains tests for advanced font properties, text processing properties,
and truncation properties. These tests verify both widget identity preservation
and value propagation for style-only property changes.

Tests are designed to run in headless CI environments without requiring a Kivy window.
"""

import pytest
from hypothesis import given, strategies as st, settings, assume

from kivy.uix.label import Label

from kivy_garden.markdownlabel import MarkdownLabel
from .test_utils import (
    simple_markdown_document,
    find_labels_recursive,
    collect_widget_ids
)


# =============================================================================
# Advanced Font Properties Widget Identity Preservation Tests
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
    # Mixed finite/complex strategy: 48 examples (8 finite × 6 complex samples)
    @settings(max_examples=48, deadline=None)
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


# =============================================================================
# Text Processing Properties Widget Identity Preservation Tests
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
    # Mixed finite/complex strategy: 30 examples (6 finite × 5 complex samples)
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


# =============================================================================
# Truncation Properties Widget Identity Preservation Tests
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
    # Mixed finite/complex strategy: 66 examples (66 finite × 1 complex samples)
    @settings(max_examples=66, deadline=None)
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


# =============================================================================
# Advanced Font Properties Value Propagation Tests
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
    # Feature: optimize-rebuild-contract, Property 2: Style-only property
    # updates apply values to all child Labels
    # Mixed finite/complex strategy: 48 examples (8 finite × 6 complex samples)
    @settings(max_examples=48, deadline=None)
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
        unicode_errors=st.sampled_from(['strict', 'replace', 'ignore']),
        strip=st.booleans()
    )
    # Feature: optimize-rebuild-contract, Property 2: Style-only property
    # updates apply values to all child Labels
    # Mixed finite/complex strategy: 30 examples (6 finite × 5 complex samples)
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
    # Feature: optimize-rebuild-contract, Property 2: Style-only property
    # updates apply values to all child Labels
    # Mixed finite/complex strategy: 60 examples (60 finite × 1 complex samples)
    @settings(max_examples=60, deadline=None)
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
