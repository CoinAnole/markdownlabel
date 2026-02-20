"""
Property-based tests for MarkdownLabel sizing behavior.

This module contains tests for auto-sizing behavior, size hint management,
and strict label mode sizing.
"""

import pytest
from hypothesis import given, strategies as st, settings, assume

from kivy_garden.markdownlabel import MarkdownLabel
from .test_utils import (
    simple_markdown_document, markdown_heading, collect_widget_ids,
    assert_rebuild_occurred
)


# *For any* MarkdownLabel with content, the widget SHALL have size_hint_y=None
# and its height SHALL equal or exceed the sum of its children's heights.

class TestAutoSizingBehavior:
    """Property tests for auto-sizing behavior."""

    @pytest.mark.property
    @given(simple_markdown_document())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_auto_size_height_enabled_sets_size_hint_y_none(self, markdown_text):
        """With auto_size_height=True, size_hint_y is None for auto-sizing."""
        label = MarkdownLabel(text=markdown_text, auto_size_height=True)

        assert label.size_hint_y is None, \
            f"Expected size_hint_y=None, got {label.size_hint_y}"

    def test_default_size_hint_y_preserved(self):
        """Default sizing participates in layout (auto_size_height=False)."""
        label = MarkdownLabel(text='Hello world')

        assert label.size_hint_y == 1, \
            f"Expected default size_hint_y=1, got {label.size_hint_y}"

    @pytest.mark.property
    @given(markdown_heading())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_height_bound_to_minimum(self, heading):
        """auto_size_height=True enables height binding via size_hint_y=None.

        When auto_size_height=True, size_hint_y is set to None which allows
        the height binding to minimum_height to take effect. In headless testing,
        we verify the precondition (size_hint_y=None) rather than the computed
        height values which require a window for layout calculation.
        """
        label = MarkdownLabel(text=heading, auto_size_height=True)

        # Verify size_hint_y is None (required for height binding to work)
        assert label.size_hint_y is None, \
            "size_hint_y should be None for auto-sizing"

        # Verify auto_size_height is enabled
        assert label.auto_size_height is True, \
            f"Expected auto_size_height=True, got {label.auto_size_height}"

    def test_empty_label_has_no_children(self):
        """Empty MarkdownLabel has no children and auto-sizing enabled."""
        label = MarkdownLabel(text='', auto_size_height=True)

        assert label.size_hint_y is None, \
            "size_hint_y should be None even for empty label"
        # Empty label should have no children
        assert len(label.children) == 0

    @pytest.mark.property
    @given(st.integers(min_value=1, max_value=5))
    # Small finite strategy: 5 examples (input space size: 5)
    @settings(max_examples=5, deadline=None)
    def test_more_content_creates_more_children(self, num_paragraphs):
        """More content should result in more child widgets."""
        text = '\n\n'.join([f'Paragraph number {i} with some text content.'
                           for i in range(num_paragraphs)])

        label = MarkdownLabel(text=text, auto_size_height=True)

        # Verify auto-sizing is enabled
        assert label.size_hint_y is None
        # Verify children exist proportional to content
        assert len(label.children) >= num_paragraphs


# *For any* MarkdownLabel with `auto_size_height=True`, the widget SHALL have
# `size_hint_y=None` AND its height SHALL be bound to `minimum_height`.

class TestAutoSizeHeightTrueBehavior:
    """Property tests for auto_size_height True behavior."""

    @pytest.mark.property
    @given(simple_markdown_document())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_auto_size_height_true_sets_size_hint_y_none(self, markdown_text):
        """When auto_size_height=True, size_hint_y should be None."""
        label = MarkdownLabel(text=markdown_text, auto_size_height=True)

        assert label.size_hint_y is None, \
            f"Expected size_hint_y=None when auto_size_height=True, got {label.size_hint_y}"

    @pytest.mark.property
    @given(simple_markdown_document())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_auto_size_height_true_binds_height_to_minimum(self, markdown_text):
        """auto_size_height=True enables height binding via size_hint_y=None.

        When auto_size_height=True, size_hint_y is set to None which allows
        the height binding to minimum_height to take effect. In headless testing,
        we verify the precondition (size_hint_y=None) rather than the computed
        height values which require a window for layout calculation.
        """
        label = MarkdownLabel(text=markdown_text, auto_size_height=True)

        # Verify size_hint_y is None (required for height binding to work)
        assert label.size_hint_y is None, \
            "size_hint_y should be None when auto_size_height=True"

        # Verify auto_size_height property is actually True
        assert label.auto_size_height is True, \
            f"Expected auto_size_height=True, got {label.auto_size_height}"

    def test_auto_size_height_default_is_false(self):
        """Default MarkdownLabel leaves auto_size_height disabled for Label parity."""
        label = MarkdownLabel(text="Test content")

        assert label.auto_size_height is False, \
            f"Expected default auto_size_height=False, got {label.auto_size_height}"

        assert label.size_hint_y == 1, \
            f"Expected size_hint_y=1 by default, got {label.size_hint_y}"

    @pytest.mark.property
    @given(st.floats(min_value=0.1, max_value=2.0, allow_nan=False, allow_infinity=False))
    # Complex strategy: 50 examples (adequate coverage)
    @settings(max_examples=50, deadline=None)
    def test_auto_size_height_true_overrides_user_size_hint_y(self, user_size_hint_y):
        """When auto_size_height=True, user-provided size_hint_y is overridden but restorable."""
        label = MarkdownLabel(
            text="Test content",
            auto_size_height=True,
            size_hint_y=user_size_hint_y
        )

        # Should override user's size_hint_y initially
        assert label.size_hint_y is None, \
            f"Expected size_hint_y=None to override user value {user_size_hint_y}, got {label.size_hint_y}"

        # Verify restoration behavior (observable behavior)
        label.auto_size_height = False
        assert label.size_hint_y == user_size_hint_y, \
            f"Expected size_hint_y to restore to {user_size_hint_y}, got {label.size_hint_y}"


# *For any* MarkdownLabel with `auto_size_height=False`, the widget SHALL preserve
# the user-specified `size_hint_y` value (or default to 1) AND its height SHALL NOT
# be bound to `minimum_height`.

class TestAutoSizeHeightFalseBehavior:
    """Property tests for auto_size_height False behavior."""

    @pytest.mark.property
    @given(simple_markdown_document())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_auto_size_height_false_preserves_default_size_hint_y(self, markdown_text):
        """When auto_size_height=False, default size_hint_y=1 is preserved."""
        label = MarkdownLabel(text=markdown_text, auto_size_height=False)

        assert label.size_hint_y == 1, \
            f"Expected size_hint_y=1 when auto_size_height=False, got {label.size_hint_y}"

        assert label.auto_size_height is False, \
            f"Expected auto_size_height=False, got {label.auto_size_height}"

    @pytest.mark.property
    @given(simple_markdown_document(),
           st.floats(min_value=0.1, max_value=2.0, allow_nan=False, allow_infinity=False))
    # Complex strategy: 50 examples (adequate coverage)
    @settings(max_examples=50, deadline=None)
    def test_auto_size_height_false_preserves_user_size_hint_y(self, markdown_text, user_size_hint_y):
        """When auto_size_height=False, user-specified size_hint_y is preserved."""
        label = MarkdownLabel(
            text=markdown_text,
            auto_size_height=False,
            size_hint_y=user_size_hint_y
        )

        assert label.size_hint_y == user_size_hint_y, \
            f"Expected size_hint_y={user_size_hint_y} when auto_size_height=False, got {label.size_hint_y}"

        assert label.auto_size_height is False, \
            f"Expected auto_size_height=False, got {label.auto_size_height}"

    @pytest.mark.property
    @given(simple_markdown_document())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_auto_size_height_false_no_height_binding(self, markdown_text):
        """When auto_size_height=False, height is not bound to minimum_height."""
        label = MarkdownLabel(text=markdown_text, auto_size_height=False)

        # The primary indicator that height is not bound to minimum_height
        # is that size_hint_y is not None (it participates in layout)
        assert label.size_hint_y is not None, \
            "size_hint_y should not be None when auto_size_height=False"

        assert label.auto_size_height is False, \
            f"Expected auto_size_height=False, got {label.auto_size_height}"

        # Verify height is NOT bound to minimum_height (they can differ)
        # When size_hint_y is not None, height is controlled by layout, not minimum_height
        # We verify the binding doesn't exist by checking the property value is preserved
        assert label.size_hint_y == 1, \
            f"Expected default size_hint_y=1, got {label.size_hint_y}"


# *For any* MarkdownLabel, when `auto_size_height` is toggled from True to False,
# the height binding SHALL be removed and `size_hint_y` SHALL be restored. When
# toggled from False to True, the height binding SHALL be added and `size_hint_y`
# SHALL be set to None.

class TestAutoSizeHeightDynamicToggling:
    """Property tests for auto_size_height dynamic toggling."""

    @pytest.mark.property
    @given(simple_markdown_document())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_toggle_true_to_false_restores_size_hint_y(self, markdown_text):
        """Toggling auto_size_height from True to False restores size_hint_y."""
        # Start with auto_size_height=True (explicit)
        label = MarkdownLabel(text=markdown_text, auto_size_height=True)

        assert label.auto_size_height is True
        assert label.size_hint_y is None

        # Toggle to False
        label.auto_size_height = False

        # Should restore size_hint_y to default (1)
        assert label.size_hint_y == 1, \
            f"Expected size_hint_y=1 after toggling to False, got {label.size_hint_y}"

        assert label.auto_size_height is False, \
            f"Expected auto_size_height=False after toggle, got {label.auto_size_height}"

    @pytest.mark.property
    @given(simple_markdown_document())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_toggle_false_to_true_sets_size_hint_y_none(self, markdown_text):
        """Toggling auto_size_height from False to True sets size_hint_y=None."""
        # Start with auto_size_height=False (default)
        label = MarkdownLabel(text=markdown_text, auto_size_height=False)

        assert label.auto_size_height is False
        assert label.size_hint_y == 1

        # Toggle to True
        label.auto_size_height = True

        # Should set size_hint_y=None
        assert label.size_hint_y is None, \
            f"Expected size_hint_y=None after toggling to True, got {label.size_hint_y}"

        assert label.auto_size_height is True, \
            f"Expected auto_size_height=True after toggle, got {label.auto_size_height}"

    @pytest.mark.property
    @given(simple_markdown_document(),
           st.floats(min_value=0.1, max_value=2.0, allow_nan=False, allow_infinity=False))
    # Complex strategy: 50 examples (adequate coverage)
    @settings(max_examples=50, deadline=None)
    def test_toggle_preserves_user_size_hint_y(self, markdown_text, user_size_hint_y):
        """Toggling preserves the original user-specified size_hint_y value."""
        # Start with user-specified size_hint_y and auto_size_height=True
        label = MarkdownLabel(
            text=markdown_text,
            auto_size_height=True,
            size_hint_y=user_size_hint_y
        )

        # Should override to None initially
        assert label.size_hint_y is None

        # Toggle to False - should restore user value
        label.auto_size_height = False

        assert label.size_hint_y == user_size_hint_y, \
            f"Expected size_hint_y={user_size_hint_y} after toggle to False, got {label.size_hint_y}"

        # Toggle back to True - should override again
        label.auto_size_height = True

        assert label.size_hint_y is None, \
            f"Expected size_hint_y=None after toggle back to True, got {label.size_hint_y}"

        # Toggle to False again - should still restore user value
        label.auto_size_height = False

        assert label.size_hint_y == user_size_hint_y, \
            f"Expected size_hint_y={user_size_hint_y} after second toggle to False, got {label.size_hint_y}"

    @pytest.mark.property
    @given(simple_markdown_document())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_multiple_toggles_maintain_consistency(self, markdown_text):
        """Multiple toggles maintain consistent behavior."""
        label = MarkdownLabel(text=markdown_text)

        # Should start with auto_size_height=False (default)
        assert label.auto_size_height is False
        assert label.size_hint_y == 1

        # Toggle True -> False -> True
        for expected_auto_size, expected_size_hint_y in [
            (True, None),    # Toggle to True
            (False, 1),      # Toggle to False
            (True, None),    # Toggle to True
        ]:
            label.auto_size_height = expected_auto_size

            assert label.auto_size_height == expected_auto_size, \
                f"Expected auto_size_height={expected_auto_size}, got {label.auto_size_height}"

            assert label.size_hint_y == expected_size_hint_y, \
                f"Expected size_hint_y={expected_size_hint_y}, got {label.size_hint_y}"


# *For any* MarkdownLabel with `strict_label_mode=True`, the widget SHALL preserve
# the user-specified `size_hint_y` value (or default to 1) AND SHALL ignore
# `auto_size_height` settings.

class TestStrictLabelModeSizingBehavior:
    """Property tests for strict label mode sizing behavior."""

    @pytest.mark.property
    @given(simple_markdown_document())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_strict_mode_preserves_default_size_hint_y(self, markdown_text):
        """When strict_label_mode=True, default size_hint_y=1 is preserved."""
        label = MarkdownLabel(text=markdown_text, strict_label_mode=True)

        assert label.size_hint_y == 1, \
            f"Expected size_hint_y=1 when strict_label_mode=True, got {label.size_hint_y}"

        assert label.strict_label_mode is True, \
            f"Expected strict_label_mode=True, got {label.strict_label_mode}"

    @pytest.mark.property
    @given(simple_markdown_document(),
           st.floats(min_value=0.1, max_value=2.0, allow_nan=False, allow_infinity=False))
    # Complex strategy: 50 examples (adequate coverage)
    @settings(max_examples=50, deadline=None)
    def test_strict_mode_preserves_user_size_hint_y(self, markdown_text, user_size_hint_y):
        """When strict_label_mode=True, user-specified size_hint_y is preserved."""
        label = MarkdownLabel(
            text=markdown_text,
            strict_label_mode=True,
            size_hint_y=user_size_hint_y
        )

        assert label.size_hint_y == user_size_hint_y, \
            f"Expected size_hint_y={user_size_hint_y} when strict_label_mode=True, got {label.size_hint_y}"

        assert label.strict_label_mode is True, \
            f"Expected strict_label_mode=True, got {label.strict_label_mode}"

    @pytest.mark.property
    @given(simple_markdown_document())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_strict_mode_height_not_bound_to_minimum(self, markdown_text):
        """When strict_label_mode=True, height is not bound to minimum_height."""
        label = MarkdownLabel(text=markdown_text, strict_label_mode=True)

        # The primary indicator that height is not bound to minimum_height
        # is that size_hint_y is not None (it participates in layout)
        assert label.size_hint_y is not None, \
            "size_hint_y should not be None when strict_label_mode=True"

        assert label.strict_label_mode is True, \
            f"Expected strict_label_mode=True, got {label.strict_label_mode}"

        # Verify height is NOT bound to minimum_height
        # When size_hint_y is not None, height is controlled by layout, not minimum_height
        assert label.size_hint_y == 1, \
            f"Expected default size_hint_y=1, got {label.size_hint_y}"

    def test_strict_mode_default_is_false(self):
        """Default MarkdownLabel should have strict_label_mode=False."""
        label = MarkdownLabel(text="Test content")

        assert label.strict_label_mode is False, \
            f"Expected default strict_label_mode=False, got {label.strict_label_mode}"

        # Default participates in layout (auto_size_height=False)
        assert label.size_hint_y == 1, \
            f"Expected size_hint_y=1 by default, got {label.size_hint_y}"

    @pytest.mark.property
    @given(st.booleans())
    # Boolean strategy: 2 examples (True/False coverage)
    @settings(max_examples=2, deadline=None)
    def test_strict_mode_property_accepted_and_stored(self, value):
        """Setting strict_label_mode property accepts and stores the value."""
        label = MarkdownLabel(text='# Hello World', strict_label_mode=value)
        assert label.strict_label_mode == value

    @pytest.mark.property
    @given(st.booleans())
    # Boolean strategy: 2 examples (True/False coverage)
    @settings(max_examples=2, deadline=None)
    def test_strict_mode_change_after_creation(self, value):
        """Changing strict_label_mode property after creation accepts and stores the value."""
        label = MarkdownLabel(text='# Hello')
        label.strict_label_mode = value
        assert label.strict_label_mode == value

    @pytest.mark.property
    @given(simple_markdown_document())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_strict_mode_toggle_from_false_to_true(self, markdown_text):
        """Toggling strict_label_mode from False to True disables auto-sizing."""
        label = MarkdownLabel(
            text=markdown_text,
            strict_label_mode=False,
            auto_size_height=True
        )

        # Initially should have auto-sizing enabled
        assert label.size_hint_y is None, \
            "size_hint_y should be None when auto_size_height=True"

        # Toggle to strict mode
        label.strict_label_mode = True

        # Should now have size_hint_y preserved (default 1)
        assert label.size_hint_y == 1, \
            f"Expected size_hint_y=1 after toggling to strict_label_mode=True, got {label.size_hint_y}"

    @pytest.mark.property
    @given(simple_markdown_document())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_strict_mode_toggle_from_true_to_false(self, markdown_text):
        """Toggling strict_label_mode from True to False enables auto-sizing."""
        label = MarkdownLabel(
            text=markdown_text,
            strict_label_mode=True,
            auto_size_height=True
        )

        # Initially should have size_hint_y preserved
        assert label.size_hint_y == 1, \
            "size_hint_y should be 1 when strict_label_mode=True"

        # Toggle to non-strict mode
        label.strict_label_mode = False

        # Should now have auto-sizing enabled
        assert label.size_hint_y is None, \
            f"Expected size_hint_y=None after toggling to strict_label_mode=False, got {label.size_hint_y}"

    @pytest.mark.property
    @given(simple_markdown_document(),
           st.floats(min_value=0.1, max_value=2.0, allow_nan=False, allow_infinity=False))
    # Complex strategy: 50 examples (adequate coverage)
    @settings(max_examples=50, deadline=None)
    def test_strict_mode_toggle_preserves_user_size_hint_y(self, markdown_text, user_size_hint_y):
        """Toggling strict_label_mode preserves user-specified size_hint_y."""
        label = MarkdownLabel(
            text=markdown_text,
            strict_label_mode=True,
            size_hint_y=user_size_hint_y,
            auto_size_height=True
        )

        # Initially should have user's size_hint_y
        assert label.size_hint_y == user_size_hint_y, \
            f"Expected size_hint_y={user_size_hint_y}, got {label.size_hint_y}"

        # Toggle to non-strict mode - should enable auto-sizing
        label.strict_label_mode = False
        assert label.size_hint_y is None, \
            f"Expected size_hint_y=None after toggle to False, got {label.size_hint_y}"

        # Toggle back to strict mode - should restore user's size_hint_y
        label.strict_label_mode = True
        assert label.size_hint_y == user_size_hint_y, \
            f"Expected size_hint_y={user_size_hint_y} after toggle back to True, got {label.size_hint_y}"

    @pytest.mark.property
    @given(simple_markdown_document())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_strict_mode_overrides_auto_size_height(self, markdown_text):
        """strict_label_mode=True overrides auto_size_height=True behavior."""
        label = MarkdownLabel(
            text=markdown_text,
            strict_label_mode=True,
            auto_size_height=True
        )

        # strict_label_mode should take precedence
        assert label.size_hint_y == 1, \
            f"Expected size_hint_y=1 when strict_label_mode=True " \
            f"(overrides auto_size_height), got {label.size_hint_y}"

    @pytest.mark.property
    @given(simple_markdown_document())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_strict_mode_ignores_auto_size_height_changes(self, markdown_text):
        """When strict_label_mode=True, auto_size_height changes are ignored."""
        label = MarkdownLabel(text=markdown_text, strict_label_mode=True)

        # Initially should have size_hint_y=1
        assert label.size_hint_y == 1

        # Try to enable auto_size_height - should be ignored
        label.auto_size_height = True

        # size_hint_y should still be 1 (strict mode takes precedence)
        assert label.size_hint_y == 1, \
            f"Expected size_hint_y=1 (strict mode ignores auto_size_height), got {label.size_hint_y}"

    @pytest.mark.property
    @given(simple_markdown_document())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_strict_mode_change_triggers_rebuild(self, markdown_text):
        """Changing strict_label_mode triggers widget rebuild."""
        assume(markdown_text.strip())

        label = MarkdownLabel(text=markdown_text, strict_label_mode=False)
        ids_before = collect_widget_ids(label, exclude_root=True)

        # Toggle strict_label_mode
        label.strict_label_mode = True
        label.force_rebuild()

        # Widget tree should be rebuilt (children may be different objects)
        assert_rebuild_occurred(label, ids_before)

        # Verify the label still has children
        assert len(label.children) >= 1, \
            "Expected at least 1 child after strict_label_mode toggle"

    @pytest.mark.property
    @given(simple_markdown_document())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_multiple_strict_mode_toggles_maintain_consistency(self, markdown_text):
        """Multiple strict_label_mode toggles maintain consistent behavior."""
        label = MarkdownLabel(text=markdown_text, auto_size_height=True)

        assert label.strict_label_mode is False
        assert label.size_hint_y is None

        # Toggle True -> False -> True -> False
        for expected_strict_mode, expected_size_hint_y in [
            (True, 1),       # Toggle to True
            (False, None),   # Toggle to False (auto_size_height=True)
            (True, 1),       # Toggle to True
            (False, None),   # Toggle to False (auto_size_height=True)
        ]:
            label.strict_label_mode = expected_strict_mode

            assert label.strict_label_mode == expected_strict_mode, \
                f"Expected strict_label_mode={expected_strict_mode}, got {label.strict_label_mode}"

            assert label.size_hint_y == expected_size_hint_y, \
                f"Expected size_hint_y={expected_size_hint_y}, got {label.size_hint_y}"

# NOTE: Meta-test for class organization has been moved to
# meta_tests/test_sizing_behavior_grouping.py
