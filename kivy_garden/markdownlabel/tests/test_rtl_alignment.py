"""
Property-based tests for RTL-aware auto alignment in MarkdownLabel.

This module contains tests for RTL alignment behavior in MarkdownLabel,
including auto alignment respecting base_direction, direction change updates,
and explicit alignment overriding auto behavior.
"""

import pytest
from hypothesis import given, strategies as st, settings

from kivy_garden.markdownlabel import MarkdownLabel
from .test_utils import find_labels_recursive, collect_widget_ids


# *For any* MarkdownLabel with halign='auto', when base_direction is 'rtl' or 'weak_rtl',
# all child Labels SHALL have halign='right'; when base_direction is 'ltr', 'weak_ltr',
# or None, all child Labels SHALL have halign='left'.

class TestAutoAlignmentRespectsDirection:
    """Property tests for auto alignment respecting direction (Property 11)."""

    @pytest.mark.unit
    @pytest.mark.needs_window
    @pytest.mark.parametrize('base_direction', ['rtl', 'weak_rtl'])
    def test_auto_alignment_rtl_directions_use_right(self, base_direction):
        """Auto alignment uses 'right' for RTL base directions.

        """
        label = MarkdownLabel(
            text='Hello World',
            halign='auto',
            base_direction=base_direction
        )

        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"

        # All labels should have halign='right' for RTL directions
        for lbl in labels:
            assert lbl.halign == 'right', \
                f"Expected halign='right' for base_direction={base_direction}, got {lbl.halign}"

    @pytest.mark.unit
    @pytest.mark.needs_window
    @pytest.mark.parametrize('base_direction', ['ltr', 'weak_ltr', None])
    def test_auto_alignment_ltr_directions_use_left(self, base_direction):
        """Auto alignment uses 'left' for LTR base directions and None.

        """
        label = MarkdownLabel(
            text='Hello World',
            halign='auto',
            base_direction=base_direction
        )

        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"

        # All labels should have halign='left' for LTR directions and None
        for lbl in labels:
            assert lbl.halign == 'left', \
                f"Expected halign='left' for base_direction={base_direction}, got {lbl.halign}"

    @pytest.mark.property
    @pytest.mark.needs_window
    @given(
        st.sampled_from(['rtl', 'weak_rtl']),
        st.integers(min_value=1, max_value=6)
    )
    # 2 directions × 6 heading_levels = 12 combinations
    # Use 12 examples for full coverage
    @settings(max_examples=12, deadline=None)
    def test_auto_alignment_rtl_applies_to_headings(self, base_direction, heading_level):
        """Auto alignment with RTL direction applies to heading Labels.

        """
        heading_text = '#' * heading_level + ' Test Heading'
        label = MarkdownLabel(
            text=heading_text,
            halign='auto',
            base_direction=base_direction
        )

        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"

        # All labels should have halign='right' for RTL directions
        for lbl in labels:
            assert lbl.halign == 'right', \
                f"Expected halign='right' for heading with base_direction={base_direction}, got {lbl.halign}"

    @pytest.mark.property
    @pytest.mark.needs_window
    @given(
        st.sampled_from(['ltr', 'weak_ltr', None]),
        st.integers(min_value=1, max_value=6)
    )
    # 3 directions × 6 heading_levels = 18 combinations
    # Use 18 examples for full coverage
    @settings(max_examples=18, deadline=None)
    def test_auto_alignment_ltr_applies_to_headings(self, base_direction, heading_level):
        """Auto alignment with LTR direction applies to heading Labels.

        """
        heading_text = '#' * heading_level + ' Test Heading'
        label = MarkdownLabel(
            text=heading_text,
            halign='auto',
            base_direction=base_direction
        )

        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"

        # All labels should have halign='left' for LTR directions and None
        for lbl in labels:
            assert lbl.halign == 'left', \
                f"Expected halign='left' for heading with base_direction={base_direction}, got {lbl.halign}"

    @pytest.mark.unit
    @pytest.mark.needs_window
    @pytest.mark.parametrize('base_direction', ['rtl', 'weak_rtl'])
    def test_auto_alignment_rtl_applies_to_mixed_content(self, base_direction):
        """Auto alignment with RTL direction applies to mixed content types.

        """
        markdown_text = '# Heading\n\nParagraph text\n\n- List item'
        label = MarkdownLabel(
            text=markdown_text,
            halign='auto',
            base_direction=base_direction
        )

        labels = find_labels_recursive(label)
        assert len(labels) >= 2, "Expected at least 2 Labels for mixed content"

        # Filter out list markers (which have halign='right' by design)
        content_labels = [lbl for lbl in labels if lbl.text not in ('•', '1.', '2.')]

        # All content labels should have halign='right' for RTL directions
        for lbl in content_labels:
            assert lbl.halign == 'right', \
                f"Expected halign='right' for mixed content with " \
                f"base_direction={base_direction}, got {lbl.halign}"

    @pytest.mark.unit
    @pytest.mark.needs_window
    @pytest.mark.parametrize('base_direction', ['ltr', 'weak_ltr', None])
    def test_auto_alignment_ltr_applies_to_mixed_content(self, base_direction):
        """Auto alignment with LTR direction applies to mixed content types.

        """
        markdown_text = '# Heading\n\nParagraph text\n\n- List item'
        label = MarkdownLabel(
            text=markdown_text,
            halign='auto',
            base_direction=base_direction
        )

        labels = find_labels_recursive(label)
        assert len(labels) >= 2, "Expected at least 2 Labels for mixed content"

        # Filter out list markers (which have halign='right' by design)
        content_labels = [lbl for lbl in labels if lbl.text not in ('•', '1.', '2.')]

        # All content labels should have halign='left' for LTR directions and None
        for lbl in content_labels:
            assert lbl.halign == 'left', \
                f"Expected halign='left' for mixed content with " \
                f"base_direction={base_direction}, got {lbl.halign}"


# *For any* MarkdownLabel with halign='auto' and rendered content, when base_direction
# changes, all child Label widgets SHALL have their halign updated to reflect the new
# effective alignment.

class TestDirectionChangeUpdatesAlignment:
    """Property tests for direction change updating alignment (Property 12)."""

    @pytest.mark.property
    @pytest.mark.needs_window
    @given(
        st.sampled_from(['ltr', 'weak_ltr', None]),
        st.sampled_from(['rtl', 'weak_rtl'])
    )
    # 3 initial_directions × 2 new_directions = 6 combinations
    # Use 6 examples for full coverage
    @settings(max_examples=6, deadline=None)
    def test_direction_change_ltr_to_rtl_updates_alignment(self, initial_direction, new_direction):
        """Changing base_direction from LTR to RTL updates alignment.

        """
        label = MarkdownLabel(
            text='Hello World',
            halign='auto',
            base_direction=initial_direction
        )

        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"

        # Verify initial alignment (should be 'left' for LTR/None)
        for lbl in labels:
            assert lbl.halign == 'left', \
                f"Expected initial halign='left' for base_direction={initial_direction}, got {lbl.halign}"

        # Change base_direction to RTL
        label.base_direction = new_direction

        # Verify alignment updated to 'right' for RTL
        labels_after = find_labels_recursive(label)
        for lbl in labels_after:
            assert lbl.halign == 'right', \
                f"Expected halign='right' after changing to base_direction={new_direction}, got {lbl.halign}"

    @pytest.mark.property
    @pytest.mark.needs_window
    @given(
        st.sampled_from(['rtl', 'weak_rtl']),
        st.sampled_from(['ltr', 'weak_ltr', None])
    )
    # 2 initial_directions × 3 new_directions = 6 combinations
    # Use 6 examples for full coverage
    @settings(max_examples=6, deadline=None)
    def test_direction_change_rtl_to_ltr_updates_alignment(self, initial_direction, new_direction):
        """Changing base_direction from RTL to LTR updates alignment.

        """
        label = MarkdownLabel(
            text='Hello World',
            halign='auto',
            base_direction=initial_direction
        )

        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"

        # Verify initial alignment (should be 'right' for RTL)
        for lbl in labels:
            assert lbl.halign == 'right', \
                f"Expected initial halign='right' for base_direction={initial_direction}, got {lbl.halign}"

        # Change base_direction to LTR/None
        label.base_direction = new_direction

        # Verify alignment updated to 'left' for LTR/None
        labels_after = find_labels_recursive(label)
        for lbl in labels_after:
            assert lbl.halign == 'left', \
                f"Expected halign='left' after changing to base_direction={new_direction}, got {lbl.halign}"

    @pytest.mark.property
    @pytest.mark.needs_window
    @given(
        st.integers(min_value=1, max_value=6),
        st.sampled_from(['ltr', 'weak_ltr', None]),
        st.sampled_from(['rtl', 'weak_rtl'])
    )
    # 6 heading_levels × 3 initial_directions × 2 new_directions = 36 combinations
    # Use 20 examples to sample adequately without exhaustive testing
    @settings(max_examples=20, deadline=None)
    def test_direction_change_updates_heading_alignment(
        self, heading_level, initial_direction, new_direction
    ):
        """Direction change updates heading alignment.

        """
        heading_text = '#' * heading_level + ' Test Heading'
        label = MarkdownLabel(
            text=heading_text,
            halign='auto',
            base_direction=initial_direction
        )

        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"

        # Verify initial alignment (should be 'left' for LTR/None)
        for lbl in labels:
            assert lbl.halign == 'left', \
                f"Expected initial halign='left' for heading with " \
                f"base_direction={initial_direction}, got {lbl.halign}"

        # Change base_direction to RTL
        label.base_direction = new_direction

        # Verify alignment updated to 'right' for RTL
        labels_after = find_labels_recursive(label)
        for lbl in labels_after:
            assert lbl.halign == 'right', \
                f"Expected halign='right' for heading after changing to " \
                f"base_direction={new_direction}, got {lbl.halign}"

    @pytest.mark.property
    @pytest.mark.needs_window
    @given(
        st.sampled_from(['ltr', 'weak_ltr', None]),
        st.sampled_from(['rtl', 'weak_rtl'])
    )
    # 3 initial_directions × 2 new_directions = 6 combinations
    # Use 6 examples for full coverage
    @settings(max_examples=6, deadline=None)
    def test_direction_change_preserves_widget_identities(self, initial_direction, new_direction):
        """Direction change preserves widget identities (no rebuild).

        """
        label = MarkdownLabel(
            text='Hello World',
            halign='auto',
            base_direction=initial_direction
        )

        # Collect widget IDs before change
        ids_before = collect_widget_ids(label)

        # Change base_direction
        label.base_direction = new_direction

        # Collect widget IDs after change
        ids_after = collect_widget_ids(label)

        # Widget identities should be preserved (in-place update, not rebuild)
        assert ids_before == ids_after, \
            f"Widget identities changed during direction change: " \
            f"{len(ids_before)} before, {len(ids_after)} after"

    @pytest.mark.property
    @pytest.mark.needs_window
    @given(
        st.sampled_from(['ltr', 'weak_ltr', None]),
        st.sampled_from(['rtl', 'weak_rtl'])
    )
    # 3 initial_directions × 2 new_directions = 6 combinations
    # Use 6 examples for full coverage
    @settings(max_examples=6, deadline=None)
    def test_direction_change_mixed_content_updates_alignment(self, initial_direction, new_direction):
        """Direction change updates alignment for mixed content types.

        """
        markdown_text = '# Heading\n\nParagraph text\n\n- List item'
        label = MarkdownLabel(
            text=markdown_text,
            halign='auto',
            base_direction=initial_direction
        )

        labels = find_labels_recursive(label)
        assert len(labels) >= 2, "Expected at least 2 Labels for mixed content"

        # Filter out list markers (which have halign='right' by design)
        content_labels = [lbl for lbl in labels if lbl.text not in ('•', '1.', '2.')]

        # Verify initial alignment (should be 'left' for LTR/None)
        for lbl in content_labels:
            assert lbl.halign == 'left', \
                f"Expected initial halign='left' for mixed content with " \
                f"base_direction={initial_direction}, got {lbl.halign}"

        # Change base_direction to RTL
        label.base_direction = new_direction

        # Verify alignment updated to 'right' for RTL
        labels_after = find_labels_recursive(label)
        content_labels_after = [lbl for lbl in labels_after if lbl.text not in ('•', '1.', '2.')]

        for lbl in content_labels_after:
            assert lbl.halign == 'right', \
                f"Expected halign='right' for mixed content after changing to " \
                f"base_direction={new_direction}, got {lbl.halign}"


# *For any* MarkdownLabel with halign explicitly set to 'left', 'center', 'right',
# or 'justify', all child Labels SHALL use that alignment regardless of base_direction value.

class TestExplicitAlignmentOverridesAuto:
    """Property tests for explicit alignment overriding auto (Property 13)."""

    @pytest.mark.property
    @pytest.mark.needs_window
    @given(
        st.sampled_from(['left', 'center', 'right', 'justify']),
        st.sampled_from(['rtl', 'weak_rtl', 'ltr', 'weak_ltr', None])
    )
    # 4 alignments × 5 directions = 20 combinations
    # Use 20 examples for full coverage
    @settings(max_examples=20, deadline=None)
    def test_explicit_alignment_overrides_base_direction(self, explicit_halign, base_direction):
        """Explicit halign overrides base_direction for all content.

        """
        label = MarkdownLabel(
            text='Hello World',
            halign=explicit_halign,
            base_direction=base_direction
        )

        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"

        # All labels should have the explicit halign, regardless of base_direction
        for lbl in labels:
            assert lbl.halign == explicit_halign, \
                f"Expected halign={explicit_halign} (explicit) with " \
                f"base_direction={base_direction}, got {lbl.halign}"

    @pytest.mark.property
    @pytest.mark.needs_window
    @given(
        st.sampled_from(['left', 'center', 'right', 'justify']),
        st.sampled_from(['rtl', 'weak_rtl']),
        st.integers(min_value=1, max_value=6)
    )
    # 4 alignments × 2 directions × 6 heading_levels = 48 combinations
    # Use 20 examples to sample adequately without exhaustive testing
    @settings(max_examples=20, deadline=None)
    def test_explicit_alignment_overrides_rtl_for_headings(
        self, explicit_halign, base_direction, heading_level
    ):
        """Explicit halign overrides RTL base_direction for headings.

        """
        heading_text = '#' * heading_level + ' Test Heading'
        label = MarkdownLabel(
            text=heading_text,
            halign=explicit_halign,
            base_direction=base_direction
        )

        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"

        # All labels should have the explicit halign, not 'right' from RTL
        for lbl in labels:
            assert lbl.halign == explicit_halign, \
                f"Expected halign={explicit_halign} (explicit) for heading " \
                f"with RTL base_direction={base_direction}, got {lbl.halign}"

    @pytest.mark.property
    @pytest.mark.needs_window
    @given(
        st.sampled_from(['left', 'center', 'right', 'justify']),
        st.sampled_from(['rtl', 'weak_rtl', 'ltr', 'weak_ltr', None])
    )
    # 4 alignments × 5 directions = 20 combinations
    # Use 20 examples for full coverage
    @settings(max_examples=20, deadline=None)
    def test_explicit_alignment_overrides_direction_for_mixed_content(self, explicit_halign, base_direction):
        """Explicit halign overrides base_direction for mixed content types.

        """
        markdown_text = '# Heading\n\nParagraph text\n\n- List item'
        label = MarkdownLabel(
            text=markdown_text,
            halign=explicit_halign,
            base_direction=base_direction
        )

        labels = find_labels_recursive(label)
        assert len(labels) >= 2, "Expected at least 2 Labels for mixed content"

        # Filter out list markers (which have halign='right' by design)
        content_labels = [lbl for lbl in labels if lbl.text not in ('•', '1.', '2.')]

        # All content labels should have the explicit halign, regardless of base_direction
        for lbl in content_labels:
            assert lbl.halign == explicit_halign, \
                f"Expected halign={explicit_halign} (explicit) for mixed " \
                f"content with base_direction={base_direction}, got {lbl.halign}"

    @pytest.mark.property
    @pytest.mark.needs_window
    @given(
        st.sampled_from(['left', 'center', 'right', 'justify']),
        st.sampled_from(['rtl', 'weak_rtl']),
        st.sampled_from(['ltr', 'weak_ltr', None])
    )
    # 4 alignments × 2 initial_directions × 3 new_directions = 24 combinations
    # Use 20 examples to sample adequately without exhaustive testing
    @settings(max_examples=20, deadline=None)
    def test_explicit_alignment_unchanged_by_direction_change(
        self, explicit_halign, initial_direction, new_direction
    ):
        """Explicit halign remains unchanged when base_direction changes.

        """
        label = MarkdownLabel(
            text='Hello World',
            halign=explicit_halign,
            base_direction=initial_direction
        )

        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"

        # Verify initial alignment (should be explicit halign)
        for lbl in labels:
            assert lbl.halign == explicit_halign, \
                f"Expected initial halign={explicit_halign} (explicit), got {lbl.halign}"

        # Change base_direction
        label.base_direction = new_direction

        # Verify alignment remains the explicit value
        labels_after = find_labels_recursive(label)
        for lbl in labels_after:
            assert lbl.halign == explicit_halign, \
                f"Expected halign={explicit_halign} (explicit) after direction change, got {lbl.halign}"

    @pytest.mark.property
    @pytest.mark.needs_window
    @given(
        st.sampled_from(['left', 'center', 'right', 'justify']),
        st.sampled_from(['rtl', 'weak_rtl', 'ltr', 'weak_ltr', None])
    )
    # 4 alignments × 5 directions = 20 combinations
    # Use 20 examples for full coverage
    @settings(max_examples=20, deadline=None)
    def test_explicit_alignment_stored_correctly_on_widget(self, explicit_halign, base_direction):
        """Explicit halign is stored correctly on MarkdownLabel widget.

        """
        label = MarkdownLabel(
            text='Hello World',
            halign=explicit_halign,
            base_direction=base_direction
        )

        # The MarkdownLabel should store the explicit halign value
        assert label.halign == explicit_halign, \
            f"Expected MarkdownLabel.halign={explicit_halign}, got {label.halign}"

        # The _get_effective_halign method should return the explicit value
        effective_halign = label._get_effective_halign()
        assert effective_halign == explicit_halign, \
            f"Expected _get_effective_halign()={explicit_halign}, got {effective_halign}"
