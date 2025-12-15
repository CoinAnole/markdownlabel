"""
Rebuild batching and deferred scheduling tests for MarkdownLabel.

This module focuses on the rebuild scheduler behavior:
- Multiple structure property changes are batched into a single rebuild
- Rebuilds are deferred via Clock triggers (not executed synchronously)
"""

import os

# Set environment variable to use headless mode for Kivy
os.environ["KIVY_NO_ARGS"] = "1"
os.environ["KIVY_NO_CONSOLELOG"] = "1"

from hypothesis import given, strategies as st, settings

from kivy_garden.markdownlabel import MarkdownLabel


class TestBatchedRebuilds:
    """Property tests for batched rebuilds (Property 6).

    **Feature: label-compatibility, Property 6: Batched rebuilds**
    **Validates: Requirements 3.1, 3.3**

    Tests verify that multiple property changes within the same frame
    result in at most one rebuild operation.
    """

    @given(st.integers(min_value=2, max_value=5))
    @settings(max_examples=100, deadline=None)
    def test_multiple_text_changes_batch_to_single_rebuild(self, num_changes):
        """Multiple text changes within same frame batch to single rebuild.

        **Feature: label-compatibility, Property 6: Batched rebuilds**
        **Validates: Requirements 3.1, 3.3**
        """
        label = MarkdownLabel(text="Initial text")

        # Track rebuild calls by patching _rebuild_widgets
        rebuild_count = [0]
        original_rebuild = label._rebuild_widgets

        def counting_rebuild():
            rebuild_count[0] += 1
            original_rebuild()

        label._rebuild_widgets = counting_rebuild

        # Make multiple text changes (these should be batched)
        for i in range(num_changes):
            label.text = f"Text change {i}"

        # Before force_rebuild, no rebuilds should have happened yet
        # (they're deferred to next frame)
        assert rebuild_count[0] == 0, (
            f"Expected 0 rebuilds before frame tick, got {rebuild_count[0]}"
        )

        # Force the rebuild to execute
        label.force_rebuild()

        # Should have exactly 1 rebuild (from force_rebuild)
        assert rebuild_count[0] == 1, (
            f"Expected exactly 1 rebuild after force_rebuild, got {rebuild_count[0]}"
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
        st.floats(min_value=10, max_value=30, allow_nan=False, allow_infinity=False),
        st.sampled_from(["Roboto", "RobotoMono-Regular"]),
    )
    @settings(max_examples=100, deadline=None)
    def test_mixed_property_changes_batch_rebuilds(self, text, font_size, font_name):
        """Mixed structure property changes batch into single rebuild.

        **Feature: label-compatibility, Property 6: Batched rebuilds**
        **Validates: Requirements 3.1, 3.3**
        """
        label = MarkdownLabel(text="Initial")

        # Track rebuild calls
        rebuild_count = [0]
        original_rebuild = label._rebuild_widgets

        def counting_rebuild():
            rebuild_count[0] += 1
            original_rebuild()

        label._rebuild_widgets = counting_rebuild

        # Make multiple structure property changes
        label.text = text
        label.font_name = font_name
        # Note: font_size is a style-only property, doesn't trigger rebuild

        # Before force_rebuild, no rebuilds should have happened
        assert rebuild_count[0] == 0, (
            f"Expected 0 rebuilds before frame tick, got {rebuild_count[0]}"
        )

        # Force the rebuild
        label.force_rebuild()

        # Should have exactly 1 rebuild
        assert rebuild_count[0] == 1, f"Expected exactly 1 rebuild, got {rebuild_count[0]}"

    def test_pending_rebuild_flag_prevents_duplicate_scheduling(self):
        """_pending_rebuild flag prevents duplicate rebuild scheduling.

        **Feature: label-compatibility, Property 6: Batched rebuilds**
        **Validates: Requirements 3.1, 3.3**
        """
        label = MarkdownLabel(text="Initial")

        # Clear any pending state
        label._pending_rebuild = False

        # Schedule multiple rebuilds
        label._schedule_rebuild()
        assert label._pending_rebuild is True, (
            "Expected _pending_rebuild to be True after first schedule"
        )

        label._schedule_rebuild()
        assert label._pending_rebuild is True, (
            "Expected _pending_rebuild to remain True after second schedule"
        )

        label._schedule_rebuild()
        assert label._pending_rebuild is True, (
            "Expected _pending_rebuild to remain True after third schedule"
        )

        # Force rebuild clears the flag
        label.force_rebuild()
        assert label._pending_rebuild is False, (
            "Expected _pending_rebuild to be False after force_rebuild"
        )


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
    @settings(max_examples=100, deadline=None)
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

    @given(st.sampled_from(["Roboto", "RobotoMono-Regular", "Arial"]))
    @settings(max_examples=100, deadline=None)
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

    def test_schedule_rebuild_sets_pending_flag(self):
        """_schedule_rebuild() sets _pending_rebuild flag.

        **Feature: label-compatibility, Property 7: Deferred rebuild scheduling**
        **Validates: Requirements 3.2**
        """
        label = MarkdownLabel(text="Test")

        # Clear pending state
        label._pending_rebuild = False

        # Call _schedule_rebuild
        label._schedule_rebuild()

        # Flag should be set
        assert label._pending_rebuild is True, (
            "Expected _pending_rebuild to be True after _schedule_rebuild()"
        )

    def test_do_rebuild_clears_pending_flag(self):
        """_do_rebuild() clears _pending_rebuild flag when executing.

        **Feature: label-compatibility, Property 7: Deferred rebuild scheduling**
        **Validates: Requirements 3.2**
        """
        label = MarkdownLabel(text="Test")

        # Set pending state
        label._pending_rebuild = True

        # Call _do_rebuild (simulating clock callback)
        label._do_rebuild()

        # Flag should be cleared
        assert label._pending_rebuild is False, (
            "Expected _pending_rebuild to be False after _do_rebuild()"
        )

    def test_do_rebuild_skips_when_not_pending(self):
        """_do_rebuild() skips rebuild when _pending_rebuild is False.

        **Feature: label-compatibility, Property 7: Deferred rebuild scheduling**
        **Validates: Requirements 3.2**
        """
        label = MarkdownLabel(text="Test")

        # Track rebuild calls
        rebuild_count = [0]
        original_rebuild = label._rebuild_widgets

        def counting_rebuild():
            rebuild_count[0] += 1
            original_rebuild()

        label._rebuild_widgets = counting_rebuild

        # Ensure not pending
        label._pending_rebuild = False

        # Call _do_rebuild
        label._do_rebuild()

        # Should not have called _rebuild_widgets
        assert rebuild_count[0] == 0, (
            f"Expected 0 rebuilds when not pending, got {rebuild_count[0]}"
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
    @settings(max_examples=100, deadline=None)
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


