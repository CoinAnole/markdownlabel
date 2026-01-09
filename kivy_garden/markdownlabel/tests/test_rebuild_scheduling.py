"""
Rebuild batching and deferred scheduling tests for MarkdownLabel.

This module focuses on the rebuild scheduler behavior:
- Multiple structure property changes are batched into a single rebuild
- Rebuilds are deferred via Clock triggers (not executed synchronously)
"""


from hypothesis import given, strategies as st, settings
import pytest

from kivy_garden.markdownlabel import MarkdownLabel
from kivy_garden.markdownlabel.tests.test_utils import (
    collect_widget_ids,
    find_labels_recursive,
    st_alphanumeric_text,
)


@pytest.mark.property
class TestBatchedRebuilds:
    """Property tests for batched rebuilds.


    Tests verify that multiple property changes within the same frame
    result in at most one rebuild operation.
    """

    @given(st.integers(min_value=2, max_value=5))
    # Small finite strategy: 4 examples (input space size: 4)
    @settings(max_examples=4, deadline=None)
    def test_multiple_text_changes_batch_to_single_rebuild(self, num_changes):
        """Multiple text changes within same frame batch to single rebuild.


        Verifies batching through observable widget identity:
        - Widget IDs unchanged after multiple text changes (deferred)
        - Widget IDs changed after force_rebuild() (single rebuild occurred)
        """
        label = MarkdownLabel(text="Initial text")
        label.force_rebuild()  # Ensure stable initial state

        ids_before = collect_widget_ids(label, exclude_root=True)

        # Make multiple text changes (these should be batched/deferred)
        for i in range(num_changes):
            label.text = f"Text change {i}"

        # Before force_rebuild, widgets should be unchanged (rebuild is deferred)
        ids_during = collect_widget_ids(label, exclude_root=True)
        assert ids_before == ids_during, (
            "Expected widgets unchanged before force_rebuild (rebuild should be deferred)"
        )

        # Force the rebuild to execute
        label.force_rebuild()

        # After force_rebuild, widgets should have changed (rebuild occurred)
        ids_after = collect_widget_ids(label, exclude_root=True)
        assert ids_before != ids_after, (
            "Expected widgets changed after force_rebuild (rebuild should have occurred)"
        )

    @given(
        st_alphanumeric_text(min_size=1, max_size=20),
        st.sampled_from(['widgets', 'texture']),
    )
    # Mixed finite/complex strategy: 16 examples (2 finite × 8 complex samples)
    @settings(max_examples=16, deadline=None)
    def test_mixed_property_changes_batch_rebuilds(self, text, render_mode):
        """Mixed structure property changes (text and render_mode) batch into single rebuild.


        Verifies batching through observable widget identity:
        - Widget IDs unchanged after mixed structure property changes (deferred)
        - Widget IDs changed after force_rebuild() (single rebuild occurred)
        """
        label = MarkdownLabel(text="Initial", render_mode='widgets')
        label.force_rebuild()  # Ensure stable initial state

        ids_before = collect_widget_ids(label, exclude_root=True)

        # Make multiple structure property changes: text and render_mode (both trigger rebuilds)
        label.text = text
        label.render_mode = render_mode

        # Before force_rebuild, widgets should be unchanged (rebuild is deferred)
        ids_during = collect_widget_ids(label, exclude_root=True)
        assert ids_before == ids_during, (
            "Expected widgets unchanged before force_rebuild (rebuild should be deferred)"
        )

        # Force the rebuild
        label.force_rebuild()

        # After force_rebuild, widgets should have changed (rebuild occurred)
        ids_after = collect_widget_ids(label, exclude_root=True)
        assert ids_before != ids_after, (
            "Expected widgets changed after force_rebuild (rebuild should have occurred)"
        )


@pytest.mark.property
class TestDeferredRebuildScheduling:
    """Property tests for deferred rebuild scheduling.


    Tests verify that property changes trigger deferred rebuilds via
    Clock.create_trigger rather than synchronous rebuilds.
    """

    @given(
        st_alphanumeric_text(min_size=1, max_size=50)
    )
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_text_change_schedules_deferred_rebuild(self, new_text):
        """Text property change schedules deferred rebuild, not synchronous.


        Verifies deferral through observable widget identity:
        - Widget IDs unchanged immediately after text property change (deferred)
        - Widget IDs changed after force_rebuild() (rebuild occurred)
        """
        label = MarkdownLabel(text="Initial text")
        label.force_rebuild()  # Ensure stable initial state

        ids_before = collect_widget_ids(label, exclude_root=True)

        # Change text - this should schedule a deferred rebuild
        label.text = new_text

        # Immediately after setting text, widgets should be unchanged
        # (rebuild hasn't executed yet because it's deferred)
        ids_during = collect_widget_ids(label, exclude_root=True)
        assert ids_before == ids_during, (
            "Expected widgets unchanged immediately after text change (rebuild should be deferred)"
        )

        # Force the rebuild to execute
        label.force_rebuild()

        # After force_rebuild, widgets should have changed (rebuild occurred)
        ids_after = collect_widget_ids(label, exclude_root=True)
        assert ids_before != ids_after, (
            "Expected widgets changed after force_rebuild (rebuild should have occurred)"
        )

    @pytest.mark.parametrize('font_name', ["Roboto", "RobotoMono-Regular"])
    def test_font_name_change_updates_immediately_no_rebuild(self, font_name):
        """font_name property change updates widgets in-place immediately (style-only).

        Verifies that font_name is a style-only property:
        - Widget IDs unchanged after font_name property change (no rebuild)
        - Font name is applied immediately to child Labels
        """
        # Use a different initial font to ensure the change is detected
        initial_font = "RobotoMono-Regular" if font_name != "RobotoMono-Regular" else "Roboto"
        label = MarkdownLabel(text="Test content", font_name=initial_font)
        label.force_rebuild()  # Ensure stable initial state

        ids_before = collect_widget_ids(label, exclude_root=True)

        # Change font_name - this is a style-only property that updates in-place
        label.font_name = font_name

        # Widget IDs should be unchanged (no rebuild, just in-place update)
        ids_after = collect_widget_ids(label, exclude_root=True)
        assert ids_before == ids_after, (
            "Expected widgets unchanged after font_name change (style-only, no rebuild)"
        )

        # Verify font_name was applied to child Labels
        labels = find_labels_recursive(label)
        for lbl in labels:
            assert lbl.font_name == font_name, \
                f"Expected font_name='{font_name}', got '{lbl.font_name}'"

    def test_rebuild_trigger_is_clock_trigger(self):
        """_rebuild_trigger is a Clock.create_trigger instance.

        **ARCHITECTURAL DOCUMENTATION TEST**

        This test intentionally accesses internal state (_rebuild_trigger) to document
        and verify a critical architectural decision: MarkdownLabel uses Kivy's Clock
        system for deferred rebuilds rather than synchronous rebuilds.

        Unlike other tests in this module that verify observable behavior, this test
        serves as architectural documentation. It ensures that the rebuild system
        continues to use Clock.create_trigger for deferral, which is essential for:
        - Performance (batching multiple changes)
        - UI responsiveness (avoiding blocking operations)
        - Kivy integration (respecting the frame-based update cycle)

        If this test fails, it indicates a significant architectural change that
        requires careful review of the rebuild system's design and performance
        characteristics.

        """
        from kivy.clock import ClockEvent

        label = MarkdownLabel(text="Test")

        # Verify _rebuild_trigger exists and is a clock event
        assert hasattr(label, "_rebuild_trigger"), "Expected _rebuild_trigger attribute"
        assert isinstance(label._rebuild_trigger, ClockEvent), (
            f"Expected ClockEvent, got {type(label._rebuild_trigger)}"
        )

    @given(
        st.lists(
            st_alphanumeric_text(min_size=1, max_size=20),
            min_size=2,
            max_size=5,
        )
    )
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_multiple_changes_all_deferred(self, text_values):
        """Multiple property changes are all deferred until next frame.


        Verifies deferral through observable widget identity:
        - Widget IDs unchanged after multiple text changes (all deferred)
        - Widget IDs changed after force_rebuild() (single rebuild occurred)
        """
        label = MarkdownLabel(text="Initial")
        label.force_rebuild()  # Ensure stable initial state

        ids_before = collect_widget_ids(label, exclude_root=True)

        # Make multiple text changes (all should be deferred)
        for text in text_values:
            label.text = text

        # After all changes, widgets should still be unchanged (all deferred)
        ids_during = collect_widget_ids(label, exclude_root=True)
        assert ids_before == ids_during, (
            "Expected widgets unchanged after multiple changes (all should be deferred)"
        )

        # Force the rebuild to execute
        label.force_rebuild()

        # After force_rebuild, widgets should have changed (rebuild occurred)
        ids_after = collect_widget_ids(label, exclude_root=True)
        assert ids_before != ids_after, (
            "Expected widgets changed after force_rebuild (rebuild should have occurred)"
        )
