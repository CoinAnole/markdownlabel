"""
Property-based tests for RTL-aware auto alignment in MarkdownLabel.

Tests verify that the MarkdownLabel correctly handles RTL text direction
and auto alignment behavior.
"""

import os

import pytest
from hypothesis import given, strategies as st, settings, assume

from kivy.uix.label import Label

from kivy_garden.markdownlabel import MarkdownLabel


# **Feature: label-compatibility, Property 11: Auto alignment respects direction**
# *For any* MarkdownLabel with halign='auto', when base_direction is 'rtl' or 'weak_rtl',
# all child Labels SHALL have halign='right'; when base_direction is 'ltr', 'weak_ltr',
# or None, all child Labels SHALL have halign='left'.
# **Validates: Requirements 5.1, 5.2**

class TestAutoAlignmentRespectsDirection:
    """Property tests for auto alignment respecting direction (Property 11)."""
    
    def _find_labels_recursive(self, widget, labels=None):
        """Recursively find all Label widgets in a widget tree."""
        if labels is None:
            labels = []
        
        if isinstance(widget, Label):
            labels.append(widget)
        
        if hasattr(widget, 'children'):
            for child in widget.children:
                self._find_labels_recursive(child, labels)
        
        return labels
    
    @pytest.mark.parametrize('base_direction', ['rtl', 'weak_rtl'])
    def test_auto_alignment_rtl_directions_use_right(self, base_direction):
        """Auto alignment uses 'right' for RTL base directions.
        
        **Feature: label-compatibility, Property 11: Auto alignment respects direction**
        **Validates: Requirements 5.1, 5.2**
        """
        label = MarkdownLabel(
            text='Hello World',
            halign='auto',
            base_direction=base_direction
        )
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        # All labels should have halign='right' for RTL directions
        for lbl in labels:
            assert lbl.halign == 'right', \
                f"Expected halign='right' for base_direction={base_direction}, got {lbl.halign}"
    
    @pytest.mark.parametrize('base_direction', ['ltr', 'weak_ltr', None])
    def test_auto_alignment_ltr_directions_use_left(self, base_direction):
        """Auto alignment uses 'left' for LTR base directions and None.
        
        **Feature: label-compatibility, Property 11: Auto alignment respects direction**
        **Validates: Requirements 5.1, 5.2**
        """
        label = MarkdownLabel(
            text='Hello World',
            halign='auto',
            base_direction=base_direction
        )
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        # All labels should have halign='left' for LTR directions and None
        for lbl in labels:
            assert lbl.halign == 'left', \
                f"Expected halign='left' for base_direction={base_direction}, got {lbl.halign}"
    
    @given(
        st.sampled_from(['rtl', 'weak_rtl']),
        st.integers(min_value=1, max_value=6)
    )
    # Small finite strategy: 2 examples (input space size: 2)
    @settings(max_examples=2, deadline=None)
    def test_auto_alignment_rtl_applies_to_headings(self, base_direction, heading_level):
        """Auto alignment with RTL direction applies to heading Labels.
        
        **Feature: label-compatibility, Property 11: Auto alignment respects direction**
        **Validates: Requirements 5.1, 5.2**
        """
        heading_text = '#' * heading_level + ' Test Heading'
        label = MarkdownLabel(
            text=heading_text,
            halign='auto',
            base_direction=base_direction
        )
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        # All labels should have halign='right' for RTL directions
        for lbl in labels:
            assert lbl.halign == 'right', \
                f"Expected halign='right' for heading with base_direction={base_direction}, got {lbl.halign}"
    
    @given(
        st.sampled_from(['ltr', 'weak_ltr', None]),
        st.integers(min_value=1, max_value=6)
    )
    # Small finite strategy: 3 examples (input space size: 3)
    @settings(max_examples=3, deadline=None)
    def test_auto_alignment_ltr_applies_to_headings(self, base_direction, heading_level):
        """Auto alignment with LTR direction applies to heading Labels.
        
        **Feature: label-compatibility, Property 11: Auto alignment respects direction**
        **Validates: Requirements 5.1, 5.2**
        """
        heading_text = '#' * heading_level + ' Test Heading'
        label = MarkdownLabel(
            text=heading_text,
            halign='auto',
            base_direction=base_direction
        )
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        # All labels should have halign='left' for LTR directions and None
        for lbl in labels:
            assert lbl.halign == 'left', \
                f"Expected halign='left' for heading with base_direction={base_direction}, got {lbl.halign}"
    
    @pytest.mark.parametrize('base_direction', ['rtl', 'weak_rtl'])
    def test_auto_alignment_rtl_applies_to_mixed_content(self, base_direction):
        """Auto alignment with RTL direction applies to mixed content types.
        
        **Feature: label-compatibility, Property 11: Auto alignment respects direction**
        **Validates: Requirements 5.1, 5.2**
        """
        markdown_text = '# Heading\n\nParagraph text\n\n- List item'
        label = MarkdownLabel(
            text=markdown_text,
            halign='auto',
            base_direction=base_direction
        )
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 2, "Expected at least 2 Labels for mixed content"
        
        # Filter out list markers (which have halign='right' by design)
        content_labels = [lbl for lbl in labels if lbl.text not in ('•', '1.', '2.')]
        
        # All content labels should have halign='right' for RTL directions
        for lbl in content_labels:
            assert lbl.halign == 'right', \
                f"Expected halign='right' for mixed content with base_direction={base_direction}, got {lbl.halign}"
    
    @pytest.mark.parametrize('base_direction', ['ltr', 'weak_ltr', None])
    def test_auto_alignment_ltr_applies_to_mixed_content(self, base_direction):
        """Auto alignment with LTR direction applies to mixed content types.
        
        **Feature: label-compatibility, Property 11: Auto alignment respects direction**
        **Validates: Requirements 5.1, 5.2**
        """
        markdown_text = '# Heading\n\nParagraph text\n\n- List item'
        label = MarkdownLabel(
            text=markdown_text,
            halign='auto',
            base_direction=base_direction
        )
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 2, "Expected at least 2 Labels for mixed content"
        
        # Filter out list markers (which have halign='right' by design)
        content_labels = [lbl for lbl in labels if lbl.text not in ('•', '1.', '2.')]
        
        # All content labels should have halign='left' for LTR directions and None
        for lbl in content_labels:
            assert lbl.halign == 'left', \
                f"Expected halign='left' for mixed content with base_direction={base_direction}, got {lbl.halign}"


# **Feature: label-compatibility, Property 12: Direction change updates alignment**
# *For any* MarkdownLabel with halign='auto' and rendered content, when base_direction
# changes, all child Label widgets SHALL have their halign updated to reflect the new
# effective alignment.
# **Validates: Requirements 5.3**

class TestDirectionChangeUpdatesAlignment:
    """Property tests for direction change updating alignment (Property 12)."""
    
    def _find_labels_recursive(self, widget, labels=None):
        """Recursively find all Label widgets in a widget tree."""
        if labels is None:
            labels = []
        
        if isinstance(widget, Label):
            labels.append(widget)
        
        if hasattr(widget, 'children'):
            for child in widget.children:
                self._find_labels_recursive(child, labels)
        
        return labels
    
    @given(
        st.sampled_from(['ltr', 'weak_ltr', None]),
        st.sampled_from(['rtl', 'weak_rtl'])
    )
    # Small finite strategy: 3 examples (input space size: 3)
    @settings(max_examples=3, deadline=None)
    def test_direction_change_ltr_to_rtl_updates_alignment(self, initial_direction, new_direction):
        """Changing base_direction from LTR to RTL updates alignment.
        
        **Feature: label-compatibility, Property 12: Direction change updates alignment**
        **Validates: Requirements 5.3**
        """
        label = MarkdownLabel(
            text='Hello World',
            halign='auto',
            base_direction=initial_direction
        )
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        # Verify initial alignment (should be 'left' for LTR/None)
        for lbl in labels:
            assert lbl.halign == 'left', \
                f"Expected initial halign='left' for base_direction={initial_direction}, got {lbl.halign}"
        
        # Change base_direction to RTL
        label.base_direction = new_direction
        
        # Verify alignment updated to 'right' for RTL
        labels_after = self._find_labels_recursive(label)
        for lbl in labels_after:
            assert lbl.halign == 'right', \
                f"Expected halign='right' after changing to base_direction={new_direction}, got {lbl.halign}"
    
    @given(
        st.sampled_from(['rtl', 'weak_rtl']),
        st.sampled_from(['ltr', 'weak_ltr', None])
    )
    # Small finite strategy: 2 examples (input space size: 2)
    @settings(max_examples=2, deadline=None)
    def test_direction_change_rtl_to_ltr_updates_alignment(self, initial_direction, new_direction):
        """Changing base_direction from RTL to LTR updates alignment.
        
        **Feature: label-compatibility, Property 12: Direction change updates alignment**
        **Validates: Requirements 5.3**
        """
        label = MarkdownLabel(
            text='Hello World',
            halign='auto',
            base_direction=initial_direction
        )
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        # Verify initial alignment (should be 'right' for RTL)
        for lbl in labels:
            assert lbl.halign == 'right', \
                f"Expected initial halign='right' for base_direction={initial_direction}, got {lbl.halign}"
        
        # Change base_direction to LTR/None
        label.base_direction = new_direction
        
        # Verify alignment updated to 'left' for LTR/None
        labels_after = self._find_labels_recursive(label)
        for lbl in labels_after:
            assert lbl.halign == 'left', \
                f"Expected halign='left' after changing to base_direction={new_direction}, got {lbl.halign}"
    
    @given(
        st.integers(min_value=1, max_value=6),
        st.sampled_from(['ltr', 'weak_ltr', None]),
        st.sampled_from(['rtl', 'weak_rtl'])
    )
    # Small finite strategy: 6 examples (input space size: 6)
    @settings(max_examples=6, deadline=None)
    def test_direction_change_updates_heading_alignment(self, heading_level, initial_direction, new_direction):
        """Direction change updates heading alignment.
        
        **Feature: label-compatibility, Property 12: Direction change updates alignment**
        **Validates: Requirements 5.3**
        """
        heading_text = '#' * heading_level + ' Test Heading'
        label = MarkdownLabel(
            text=heading_text,
            halign='auto',
            base_direction=initial_direction
        )
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        # Verify initial alignment (should be 'left' for LTR/None)
        for lbl in labels:
            assert lbl.halign == 'left', \
                f"Expected initial halign='left' for heading with base_direction={initial_direction}, got {lbl.halign}"
        
        # Change base_direction to RTL
        label.base_direction = new_direction
        
        # Verify alignment updated to 'right' for RTL
        labels_after = self._find_labels_recursive(label)
        for lbl in labels_after:
            assert lbl.halign == 'right', \
                f"Expected halign='right' for heading after changing to base_direction={new_direction}, got {lbl.halign}"
    
    @given(
        st.sampled_from(['ltr', 'weak_ltr', None]),
        st.sampled_from(['rtl', 'weak_rtl'])
    )
    # Small finite strategy: 3 examples (input space size: 3)
    @settings(max_examples=3, deadline=None)
    def test_direction_change_preserves_widget_identities(self, initial_direction, new_direction):
        """Direction change preserves widget identities (no rebuild).
        
        **Feature: label-compatibility, Property 12: Direction change updates alignment**
        **Validates: Requirements 5.3**
        """
        label = MarkdownLabel(
            text='Hello World',
            halign='auto',
            base_direction=initial_direction
        )
        
        # Collect widget IDs before change
        def collect_widget_ids(widget):
            ids = [id(widget)]
            if hasattr(widget, 'children'):
                for child in widget.children:
                    ids.extend(collect_widget_ids(child))
            return set(ids)
        
        ids_before = collect_widget_ids(label)
        
        # Change base_direction
        label.base_direction = new_direction
        
        # Collect widget IDs after change
        ids_after = collect_widget_ids(label)
        
        # Widget identities should be preserved (in-place update, not rebuild)
        assert ids_before == ids_after, \
            f"Widget identities changed during direction change: {len(ids_before)} before, {len(ids_after)} after"
    
    @given(
        st.sampled_from(['ltr', 'weak_ltr', None]),
        st.sampled_from(['rtl', 'weak_rtl'])
    )
    # Small finite strategy: 3 examples (input space size: 3)
    @settings(max_examples=3, deadline=None)
    def test_direction_change_mixed_content_updates_alignment(self, initial_direction, new_direction):
        """Direction change updates alignment for mixed content types.
        
        **Feature: label-compatibility, Property 12: Direction change updates alignment**
        **Validates: Requirements 5.3**
        """
        markdown_text = '# Heading\n\nParagraph text\n\n- List item'
        label = MarkdownLabel(
            text=markdown_text,
            halign='auto',
            base_direction=initial_direction
        )
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 2, "Expected at least 2 Labels for mixed content"
        
        # Filter out list markers (which have halign='right' by design)
        content_labels = [lbl for lbl in labels if lbl.text not in ('•', '1.', '2.')]
        
        # Verify initial alignment (should be 'left' for LTR/None)
        for lbl in content_labels:
            assert lbl.halign == 'left', \
                f"Expected initial halign='left' for mixed content with base_direction={initial_direction}, got {lbl.halign}"
        
        # Change base_direction to RTL
        label.base_direction = new_direction
        
        # Verify alignment updated to 'right' for RTL
        labels_after = self._find_labels_recursive(label)
        content_labels_after = [lbl for lbl in labels_after if lbl.text not in ('•', '1.', '2.')]
        
        for lbl in content_labels_after:
            assert lbl.halign == 'right', \
                f"Expected halign='right' for mixed content after changing to base_direction={new_direction}, got {lbl.halign}"


# **Feature: label-compatibility, Property 13: Explicit alignment overrides auto**
# *For any* MarkdownLabel with halign explicitly set to 'left', 'center', 'right',
# or 'justify', all child Labels SHALL use that alignment regardless of base_direction value.
# **Validates: Requirements 5.4**

class TestExplicitAlignmentOverridesAuto:
    """Property tests for explicit alignment overriding auto (Property 13)."""
    
    def _find_labels_recursive(self, widget, labels=None):
        """Recursively find all Label widgets in a widget tree."""
        if labels is None:
            labels = []
        
        if isinstance(widget, Label):
            labels.append(widget)
        
        if hasattr(widget, 'children'):
            for child in widget.children:
                self._find_labels_recursive(child, labels)
        
        return labels
    
    @given(
        st.sampled_from(['left', 'center', 'right', 'justify']),
        st.sampled_from(['rtl', 'weak_rtl', 'ltr', 'weak_ltr', None])
    )
    # Small finite strategy: 3 examples (input space size: 3)
    @settings(max_examples=3, deadline=None)
    def test_explicit_alignment_overrides_base_direction(self, explicit_halign, base_direction):
        """Explicit halign overrides base_direction for all content.
        
        **Feature: label-compatibility, Property 13: Explicit alignment overrides auto**
        **Validates: Requirements 5.4**
        """
        label = MarkdownLabel(
            text='Hello World',
            halign=explicit_halign,
            base_direction=base_direction
        )
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        # All labels should have the explicit halign, regardless of base_direction
        for lbl in labels:
            assert lbl.halign == explicit_halign, \
                f"Expected halign={explicit_halign} (explicit) with base_direction={base_direction}, got {lbl.halign}"
    
    @given(
        st.sampled_from(['left', 'center', 'right', 'justify']),
        st.sampled_from(['rtl', 'weak_rtl']),
        st.integers(min_value=1, max_value=6)
    )
    # Small finite strategy: 4 examples (input space size: 4)
    @settings(max_examples=4, deadline=None)
    def test_explicit_alignment_overrides_rtl_for_headings(self, explicit_halign, base_direction, heading_level):
        """Explicit halign overrides RTL base_direction for headings.
        
        **Feature: label-compatibility, Property 13: Explicit alignment overrides auto**
        **Validates: Requirements 5.4**
        """
        heading_text = '#' * heading_level + ' Test Heading'
        label = MarkdownLabel(
            text=heading_text,
            halign=explicit_halign,
            base_direction=base_direction
        )
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        # All labels should have the explicit halign, not 'right' from RTL
        for lbl in labels:
            assert lbl.halign == explicit_halign, \
                f"Expected halign={explicit_halign} (explicit) for heading with RTL base_direction={base_direction}, got {lbl.halign}"
    
    @given(
        st.sampled_from(['left', 'center', 'right', 'justify']),
        st.sampled_from(['rtl', 'weak_rtl', 'ltr', 'weak_ltr', None])
    )
    # Small finite strategy: 4 examples (input space size: 4)
    @settings(max_examples=4, deadline=None)
    def test_explicit_alignment_overrides_direction_for_mixed_content(self, explicit_halign, base_direction):
        """Explicit halign overrides base_direction for mixed content types.
        
        **Feature: label-compatibility, Property 13: Explicit alignment overrides auto**
        **Validates: Requirements 5.4**
        """
        markdown_text = '# Heading\n\nParagraph text\n\n- List item'
        label = MarkdownLabel(
            text=markdown_text,
            halign=explicit_halign,
            base_direction=base_direction
        )
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 2, "Expected at least 2 Labels for mixed content"
        
        # Filter out list markers (which have halign='right' by design)
        content_labels = [lbl for lbl in labels if lbl.text not in ('•', '1.', '2.')]
        
        # All content labels should have the explicit halign, regardless of base_direction
        for lbl in content_labels:
            assert lbl.halign == explicit_halign, \
                f"Expected halign={explicit_halign} (explicit) for mixed content with base_direction={base_direction}, got {lbl.halign}"
    
    @given(
        st.sampled_from(['left', 'center', 'right', 'justify']),
        st.sampled_from(['rtl', 'weak_rtl']),
        st.sampled_from(['ltr', 'weak_ltr', None])
    )
    # Small finite strategy: 4 examples (input space size: 4)
    @settings(max_examples=4, deadline=None)
    def test_explicit_alignment_unchanged_by_direction_change(self, explicit_halign, initial_direction, new_direction):
        """Explicit halign remains unchanged when base_direction changes.
        
        **Feature: label-compatibility, Property 13: Explicit alignment overrides auto**
        **Validates: Requirements 5.4**
        """
        label = MarkdownLabel(
            text='Hello World',
            halign=explicit_halign,
            base_direction=initial_direction
        )
        
        labels = self._find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"
        
        # Verify initial alignment (should be explicit halign)
        for lbl in labels:
            assert lbl.halign == explicit_halign, \
                f"Expected initial halign={explicit_halign} (explicit), got {lbl.halign}"
        
        # Change base_direction
        label.base_direction = new_direction
        
        # Verify alignment remains the explicit value
        labels_after = self._find_labels_recursive(label)
        for lbl in labels_after:
            assert lbl.halign == explicit_halign, \
                f"Expected halign={explicit_halign} (explicit) after direction change, got {lbl.halign}"
    
    @given(
        st.sampled_from(['left', 'center', 'right', 'justify']),
        st.sampled_from(['rtl', 'weak_rtl', 'ltr', 'weak_ltr', None])
    )
    # Small finite strategy: 3 examples (input space size: 3)
    @settings(max_examples=3, deadline=None)
    def test_explicit_alignment_stored_correctly_on_widget(self, explicit_halign, base_direction):
        """Explicit halign is stored correctly on MarkdownLabel widget.
        
        **Feature: label-compatibility, Property 13: Explicit alignment overrides auto**
        **Validates: Requirements 5.4**
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