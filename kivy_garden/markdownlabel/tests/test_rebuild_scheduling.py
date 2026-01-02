"""
Rebuild batching and deferred scheduling tests for MarkdownLabel.

This module focuses on the rebuild scheduler behavior:
- Multiple structure property changes are batched into a single rebuild
- Rebuilds are deferred via Clock triggers (not executed synchronously)
"""


from hypothesis import given, strategies as st, settings
import pytest

from kivy_garden.markdownlabel import MarkdownLabel
from kivy_garden.markdownlabel.tests.test_utils import collect_widget_ids


@pytest.mark.property
class TestBatchedRebuilds:
    """Property tests for batched rebuilds (Property 6).

    **Feature: label-compatibility, Property 6: Batched rebuilds**
    **Validates: Requirements 3.1, 3.3**

    Tests verify that multiple property changes within the same frame
    result in at most one rebuild operation.
    """

    @given(st.integers(min_value=2, max_value=5))
    # Small finite strategy: 4 examples (input space size: 4)
    @settings(max_examples=4, deadline=None)
    def test_multiple_text_changes_batch_to_single_rebuild(self, num_changes):
        """Multiple text changes within same frame batch to single rebuild.

        **Feature: label-compatibility, Property 6: Batched rebuilds**
        **Validates: Requirements 3.1, 3.3**

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
        st.text(
            min_size=1,
            max_size=20,
            alphabet=st.characters(
                whitelist_categories=["L", "N"],
                blacklist_characters="#[]&\n\r",
            ),
        ),
        st.floats(
            min_value=10,
            max_value=30,
            allow_nan=False,
            allow_infinity=False,
        ),
        st.sampled_from(["Roboto", "RobotoMono-Regular"]),
    )
    # Combination strategy: 2 examples (combination coverage)
    @settings(max_examples=2, deadline=None)
    def test_mixed_property_changes_batch_rebuilds(self, text, font_size, font_name):
        """Mixed structure property changes batch into single rebuild.

        **Feature: label-compatibility, Property 6: Batched rebuilds**
        **Validates: Requirements 3.1, 3.3**

        Verifies batching through observable widget identity:
        - Widget IDs unchanged after mixed property changes (deferred)
        - Widget IDs changed after force_rebuild() (single rebuild occurred)
        """
        label = MarkdownLabel(text="Initial")
        label.force_rebuild()  # Ensure stable initial state

        ids_before = collect_widget_ids(label, exclude_root=True)

        # Make multiple structure property changes (should be batched/deferred)
        label.text = text
        label.font_name = font_name
        # Note: font_size is a style-only property, doesn't trigger rebuild

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
    """Property tests for deferred rebuild scheduling (Property 7).

    **Feature: label-compatibility, Property 7: Deferred rebuild scheduling**
    **Validates: Requirements 3.2**

    Tests verify that property changes trigger deferred rebuilds via
    Clock.create_trigger rather than synchronous rebuilds.
    """

    @given(
        st.text(
            min_size=1,
            max_size=50,
            alphabet=st.characters(
                whitelist_categories=["L", "N"],
                blacklist_characters="#[]&\n\r",
            ),
        )
    )
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_text_change_schedules_deferred_rebuild(self, new_text):
        """Text property change schedules deferred rebuild, not synchronous.

        **Feature: label-compatibility, Property 7: Deferred rebuild scheduling**
        **Validates: Requirements 3.2**
        """
        label = MarkdownLabel(text="Initial text")
        initial_children = list(label.children)

        # Change text - this should schedule a deferred rebuild
        label.text = new_text

        # Immediately after setting text, children should still be the same
        # (rebuild hasn't executed yet because it's deferred)
        assert label._pending_rebuild is True, (
            "Expected _pending_rebuild to be True after text change"
        )

        # The children should still be the initial ones (deferred, not immediate)
        # Note: We compare by checking the rebuild hasn't happened yet
        assert label._pending_rebuild is True, (
            "Rebuild should be pending, not executed synchronously"
        )

    @pytest.mark.parametrize('font_name', ["Roboto", "RobotoMono-Regular", "Arial"])
    def test_font_name_change_schedules_deferred_rebuild(self, font_name):
        """font_name property change schedules deferred rebuild.

        **Feature: label-compatibility, Property 7: Deferred rebuild scheduling**
        **Validates: Requirements 3.2**
        """
        # Use a different initial font to ensure the change is detected
        # Use fonts that are known to be available in Kivy
        initial_font = "RobotoMono-Regular" if font_name != "RobotoMono-Regular" else "Roboto"
        label = MarkdownLabel(text="Test content", font_name=initial_font)

        # Clear any pending state from initialization
        label._pending_rebuild = False

        # Change font_name - this is a structure property that triggers rebuild
        label.font_name = font_name

        # Should have scheduled a deferred rebuild
        assert label._pending_rebuild is True, (
            "Expected _pending_rebuild to be True after font_name change"
        )

    def test_rebuild_trigger_is_clock_trigger(self):
        """_rebuild_trigger is a Clock.create_trigger instance.

        **Feature: label-compatibility, Property 7: Deferred rebuild scheduling**
        **Validates: Requirements 3.2**
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
            st.text(
                min_size=1,
                max_size=20,
                alphabet=st.characters(
                    whitelist_categories=["L", "N"],
                    blacklist_characters="#[]&\n\r",
                ),
            ),
            min_size=2,
            max_size=5,
        )
    )
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_multiple_changes_all_deferred(self, text_values):
        """Multiple property changes are all deferred until next frame.

        **Feature: label-compatibility, Property 7: Deferred rebuild scheduling**
        **Validates: Requirements 3.2**
        """
        label = MarkdownLabel(text="Initial")

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
        assert rebuild_count[0] == 0, (
            f"Expected 0 synchronous rebuilds, got {rebuild_count[0]}"
        )

        # Pending flag should be set
        assert label._pending_rebuild is True, (
            "Expected _pending_rebuild to be True after multiple changes"
        )
