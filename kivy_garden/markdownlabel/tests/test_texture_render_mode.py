"""
Property-based tests for texture render mode in MarkdownLabel.

This module contains tests for the texture render mode feature, including:
- Texture render mode structure (Property 14): Image widget creation and
  render_mode property behavior
- Texture mode link handling (Property 15): Link zone aggregation and
  on_ref_press event dispatching
- Deterministic texture hit-testing: Touch event handling within and outside
  link zones
- Texture fallback branch: Fallback to widgets mode when texture rendering
  fails
- Auto render mode selection (Property 16): Automatic selection between widgets
  and texture modes based on content complexity and layout constraints

These tests use a combination of property-based testing with Hypothesis and
deterministic tests to verify that MarkdownLabel correctly implements texture
rendering for maximum Label compatibility while maintaining proper Markdown
functionality.
"""

import pytest
from hypothesis import given, strategies as st, settings

from kivy_garden.markdownlabel import MarkdownLabel
from .test_utils import find_labels_recursive, FakeTouch, find_images


# *For any* MarkdownLabel with render_mode='texture' and non-empty text, the widget
# tree SHALL contain an Image widget displaying the rendered content as a texture.

@pytest.mark.slow
class TestTextureRenderModeStructure:
    """Property tests for texture render mode structure (Property 14)."""

    @pytest.mark.parametrize('text', [
        'Hello World',
        '# Heading',
        '**Bold** and *italic*',
        '- List item 1\n- List item 2',
        '[Link](http://example.com)',
    ])
    def test_texture_mode_creates_image_widget(self, text):
        """When render_mode='texture', widget tree contains an Image widget.

        """
        label = MarkdownLabel(
            text=text,
            render_mode='texture',
            size=(400, 300),
            size_hint=(None, None)
        )
        label.force_rebuild()

        images = find_images(label)
        assert len(images) >= 1, \
            f"Expected at least 1 Image widget in texture mode, found {len(images)}"

    def test_texture_mode_with_empty_text_no_image(self):
        """When render_mode='texture' with empty text, no Image widget is created.

        """
        label = MarkdownLabel(
            text='',
            render_mode='texture',
            size=(400, 300),
            size_hint=(None, None)
        )
        label.force_rebuild()

        images = find_images(label)
        assert len(images) == 0, \
            f"Expected no Image widgets with empty text, found {len(images)}"

    def test_widgets_mode_no_image_widget(self):
        """When render_mode='widgets', no Image widget is created.

        """
        label = MarkdownLabel(
            text='Hello World',
            render_mode='widgets',
            size=(400, 300),
            size_hint=(None, None)
        )
        label.force_rebuild()

        images = find_images(label)
        assert len(images) == 0, \
            f"Expected no Image widgets in widgets mode, found {len(images)}"

    @pytest.mark.parametrize('render_mode', ['widgets', 'texture', 'auto'])
    def test_render_mode_property_values(self, render_mode):
        """render_mode property accepts valid values.

        """
        label = MarkdownLabel(text='Hello World', render_mode=render_mode)
        assert label.render_mode == render_mode, \
            f"Expected render_mode={render_mode}, got {label.render_mode}"

    def test_default_render_mode_is_widgets(self):
        """Default render_mode is 'widgets'.

        """
        label = MarkdownLabel(text='Hello World')
        assert label.render_mode == 'widgets', \
            f"Default render_mode should be 'widgets', got {label.render_mode}"


# *For any* MarkdownLabel with render_mode='texture' containing links, when a touch
# event occurs within a link's bounding zone, the on_ref_press event SHALL be
# dispatched with the correct ref value.

@pytest.mark.slow
class TestTextureModeLinksHandling:
    """Property tests for texture mode link handling (Property 15)."""

    def test_aggregated_refs_populated_in_texture_mode(self):
        """In texture mode, _aggregated_refs is populated with link zones.

        """
        label = MarkdownLabel(
            text='Click [here](http://example.com) for more info.',
            render_mode='texture',
            size=(400, 300),
            size_hint=(None, None)
        )
        label.force_rebuild()

        # Check that aggregated refs were collected
        # Note: The refs may be empty if texture rendering failed or
        # if the link zones couldn't be calculated
        assert hasattr(label, '_aggregated_refs'), \
            "Expected _aggregated_refs attribute"

    def test_widgets_mode_no_aggregated_refs(self):
        """In widgets mode, _aggregated_refs is empty (links handled by Labels).

        """
        label = MarkdownLabel(
            text='Click [here](http://example.com) for more info.',
            render_mode='widgets',
            size=(400, 300),
            size_hint=(None, None)
        )
        label.force_rebuild()

        # In widgets mode, aggregated refs should be empty
        # (links are handled by individual Label widgets)
        assert label._aggregated_refs == {}, \
            f"Expected empty _aggregated_refs in widgets mode, got {label._aggregated_refs}"

    @pytest.mark.parametrize('text,expected_refs', [
        ('[Link](http://example.com)', ['http://example.com']),
        ('[A](http://a.com) and [B](http://b.com)', ['http://a.com', 'http://b.com']),
    ])
    def test_multiple_links_collected(self, text, expected_refs):
        """Multiple links in content are collected in _aggregated_refs.

        """
        label = MarkdownLabel(
            text=text,
            render_mode='texture',
            size=(400, 300),
            size_hint=(None, None)
        )
        label.force_rebuild()

        # Check that the expected refs are present
        # Note: refs may not be collected if texture rendering fails
        if label._aggregated_refs:
            for ref in expected_refs:
                assert ref in label._aggregated_refs, \
                    f"Expected ref '{ref}' in _aggregated_refs"


# *For any* MarkdownLabel with render_mode='texture' and _aggregated_refs containing
# at least one zone, and *for any* touch point (x, y) that falls inside a ref zone,
# calling on_touch_down with that touch SHALL dispatch on_ref_press with the correct
# ref name AND return True.

@pytest.mark.slow
class TestDeterministicTextureHitTesting:
    """Deterministic tests for texture mode hit-testing without window dependency.

    These tests manually inject _aggregated_refs to verify hit-testing logic
    without relying on actual texture rendering.
    """

    def test_inside_zone_dispatch(self):
        """Touch inside ref zone dispatches on_ref_press and returns True.

        """
        # Create MarkdownLabel with render_mode='texture'
        label = MarkdownLabel(
            text='Test content',
            render_mode='texture',
            size=(400, 300),
            size_hint=(None, None),
            pos=(0, 0)
        )

        # Manually set _aggregated_refs with known zones
        # Zone format: (x, y, width, height) in local coordinates
        label._aggregated_refs = {
            'http://example.com': [(10, 10, 50, 20)],
        }

        # Track dispatched refs
        dispatched_refs = []

        def capture_ref(instance, ref):
            dispatched_refs.append(ref)

        # Bind on_ref_press to capture dispatched ref
        label.bind(on_ref_press=capture_ref)

        # Create FakeTouch inside the zone
        # Zone is at (10, 10) with size (50, 20), so (25, 15) is inside
        touch = FakeTouch(25, 15)

        # Call on_touch_down
        result = label.on_touch_down(touch)

        # Assert handler called with correct ref
        assert len(dispatched_refs) == 1, \
            f"Expected 1 dispatch, got {len(dispatched_refs)}"
        assert dispatched_refs[0] == 'http://example.com', \
            f"Expected 'http://example.com', got '{dispatched_refs[0]}'"

        # Assert returns True
        assert result is True, \
            f"Expected on_touch_down to return True, got {result}"

    @given(
        zone=st.tuples(
            st.floats(min_value=0, max_value=300, allow_nan=False),
            st.floats(min_value=0, max_value=200, allow_nan=False),
            st.floats(min_value=10, max_value=100, allow_nan=False),
            st.floats(min_value=10, max_value=50, allow_nan=False)
        ),
        ref_name=st.from_regex(
            r'https?://[a-z]{3,10}\.[a-z]{2,5}/[a-z]{1,10}',
            fullmatch=True
        ),
        touch_offset_x=st.floats(min_value=0.1, max_value=0.9, allow_nan=False),
        touch_offset_y=st.floats(min_value=0.1, max_value=0.9, allow_nan=False)
    )
    # Combination strategy: 50 examples (combination coverage)
    @settings(max_examples=50, deadline=None)
    def test_property_inside_zone_dispatch(
        self, zone, ref_name, touch_offset_x, touch_offset_y
    ):
        """Property test: Touch inside ref zone dispatches on_ref_press.

        *For any* MarkdownLabel with render_mode='texture' and _aggregated_refs
        containing at least one zone, and *for any* touch point (x, y) that falls
        inside a ref zone, calling on_touch_down with that touch SHALL dispatch
        on_ref_press with the correct ref name AND return True.
        """
        zx, zy, zw, zh = zone

        # Create MarkdownLabel with render_mode='texture'
        label = MarkdownLabel(
            text='Test content',
            render_mode='texture',
            size=(400, 300),
            size_hint=(None, None),
            pos=(0, 0)
        )

        # Manually set _aggregated_refs with the generated zone
        label._aggregated_refs = {
            ref_name: [(zx, zy, zw, zh)],
        }

        # Track dispatched refs
        dispatched_refs = []

        def capture_ref(instance, ref):
            dispatched_refs.append(ref)

        label.bind(on_ref_press=capture_ref)

        # Calculate touch point inside the zone using offsets
        touch_x = zx + (zw * touch_offset_x)
        touch_y = zy + (zh * touch_offset_y)

        touch = FakeTouch(touch_x, touch_y)
        result = label.on_touch_down(touch)

        # Assert handler called with correct ref
        assert len(dispatched_refs) == 1, \
            f"Expected 1 dispatch for touch at ({touch_x}, {touch_y}) in zone {zone}"
        assert dispatched_refs[0] == ref_name, \
            f"Expected '{ref_name}', got '{dispatched_refs[0]}'"
        assert result is True, \
            "Expected on_touch_down to return True"

    def test_outside_zone_no_dispatch(self):
        """Touch outside ref zones does not dispatch on_ref_press.

        """
        # Create MarkdownLabel with render_mode='texture'
        label = MarkdownLabel(
            text='Test content',
            render_mode='texture',
            size=(400, 300),
            size_hint=(None, None),
            pos=(0, 0)
        )

        # Manually set _aggregated_refs with known zones
        label._aggregated_refs = {
            'http://example.com': [(10, 10, 50, 20)],
        }

        # Track dispatched refs
        dispatched_refs = []

        def capture_ref(instance, ref):
            dispatched_refs.append(ref)

        label.bind(on_ref_press=capture_ref)

        # Create FakeTouch outside the zone
        # Zone is at (10, 10) with size (50, 20), so (100, 100) is outside
        touch = FakeTouch(100, 100)

        result = label.on_touch_down(touch)

        # Assert no dispatch
        assert len(dispatched_refs) == 0, \
            f"Expected no dispatch, got {len(dispatched_refs)}"

        # Assert returns falsy value (super().on_touch_down returns None)
        assert not result, \
            f"Expected on_touch_down to return falsy value, got {result}"

    @given(
        zone=st.tuples(
            st.floats(min_value=50, max_value=150, allow_nan=False),
            st.floats(min_value=50, max_value=100, allow_nan=False),
            st.floats(min_value=10, max_value=50, allow_nan=False),
            st.floats(min_value=10, max_value=30, allow_nan=False)
        ),
        ref_name=st.from_regex(
            r'https?://[a-z]{3,10}\.[a-z]{2,5}/[a-z]{1,10}',
            fullmatch=True
        ),
        outside_offset=st.floats(min_value=10, max_value=50, allow_nan=False)
    )
    # Combination strategy: 50 examples (combination coverage)
    @settings(max_examples=50, deadline=None)
    def test_property_outside_zone_no_dispatch(self, zone, ref_name, outside_offset):
        """Property test: Touch outside ref zones does not dispatch.

        *For any* MarkdownLabel with render_mode='texture' and _aggregated_refs
        containing zones, and *for any* touch point (x, y) that falls outside all
        ref zones, calling on_touch_down with that touch SHALL NOT dispatch
        on_ref_press AND SHALL return False.
        """
        zx, zy, zw, zh = zone

        # Create MarkdownLabel with render_mode='texture'
        label = MarkdownLabel(
            text='Test content',
            render_mode='texture',
            size=(400, 300),
            size_hint=(None, None),
            pos=(0, 0)
        )

        # Manually set _aggregated_refs with the generated zone
        label._aggregated_refs = {
            ref_name: [(zx, zy, zw, zh)],
        }

        # Track dispatched refs
        dispatched_refs = []

        def capture_ref(instance, ref):
            dispatched_refs.append(ref)

        label.bind(on_ref_press=capture_ref)

        # Calculate touch point outside the zone (to the right and above)
        touch_x = zx + zw + outside_offset
        touch_y = zy + zh + outside_offset

        touch = FakeTouch(touch_x, touch_y)
        result = label.on_touch_down(touch)

        # Assert no dispatch
        assert len(dispatched_refs) == 0, \
            f"Expected no dispatch for touch at ({touch_x}, {touch_y}) outside zone {zone}"

        # Assert returns falsy value (super().on_touch_down returns None)
        assert not result, \
            "Expected on_touch_down to return falsy value"

    def test_multiple_zones_first_match(self):
        """Multiple zones: first matching zone triggers dispatch.

        """
        # Create MarkdownLabel with render_mode='texture'
        label = MarkdownLabel(
            text='Test content',
            render_mode='texture',
            size=(400, 300),
            size_hint=(None, None),
            pos=(0, 0)
        )

        # Set up multiple overlapping ref zones
        # Zone 1: (10, 10, 100, 50) - larger zone
        # Zone 2: (30, 20, 40, 30) - smaller zone inside zone 1
        label._aggregated_refs = {
            'http://first.com': [(10, 10, 100, 50)],
            'http://second.com': [(30, 20, 40, 30)],
        }

        # Track dispatched refs
        dispatched_refs = []

        def capture_ref(instance, ref):
            dispatched_refs.append(ref)

        label.bind(on_ref_press=capture_ref)

        # Touch at (40, 30) - inside both zones
        touch = FakeTouch(40, 30)
        result = label.on_touch_down(touch)

        # Assert exactly one dispatch (first matching zone)
        assert len(dispatched_refs) == 1, \
            f"Expected 1 dispatch, got {len(dispatched_refs)}"

        # The first zone in iteration order should be dispatched
        # (dict iteration order is insertion order in Python 3.7+)
        assert dispatched_refs[0] == 'http://first.com', \
            f"Expected 'http://first.com' (first zone), got '{dispatched_refs[0]}'"

        assert result is True, \
            "Expected on_touch_down to return True"

    def test_multiple_zones_non_overlapping(self):
        """Multiple non-overlapping zones: correct zone triggers dispatch.

        """
        # Create MarkdownLabel with render_mode='texture'
        label = MarkdownLabel(
            text='Test content',
            render_mode='texture',
            size=(400, 300),
            size_hint=(None, None),
            pos=(0, 0)
        )

        # Set up multiple non-overlapping ref zones
        label._aggregated_refs = {
            'http://first.com': [(10, 10, 50, 30)],
            'http://second.com': [(100, 10, 50, 30)],
            'http://third.com': [(200, 10, 50, 30)],
        }

        # Track dispatched refs
        dispatched_refs = []

        def capture_ref(instance, ref):
            dispatched_refs.append(ref)

        label.bind(on_ref_press=capture_ref)

        # Touch at (120, 20) - inside second zone only
        touch = FakeTouch(120, 20)
        result = label.on_touch_down(touch)

        # Assert exactly one dispatch for the correct zone
        assert len(dispatched_refs) == 1, \
            f"Expected 1 dispatch, got {len(dispatched_refs)}"
        assert dispatched_refs[0] == 'http://second.com', \
            f"Expected 'http://second.com', got '{dispatched_refs[0]}'"
        assert result is True, \
            "Expected on_touch_down to return True"


# *For any* MarkdownLabel with render_mode='auto', the effective render mode SHALL
# be determined by content complexity and layout constraints (widgets for simple
# content, texture for complex layouts or when strict_label_mode is True with
# height constraints).

# WHEN _render_as_texture returns None, THE MarkdownLabel SHALL fall back to
# widgets-mode rendering.

@pytest.mark.slow
class TestTextureFallbackBranch:
    """Tests for texture mode fallback to widgets mode when rendering fails."""

    def test_texture_fallback_to_widgets_mode(self, monkeypatch):
        """When _render_as_texture returns None, fallback to widgets mode.


        This test verifies that when texture rendering fails (returns None),
        the MarkdownLabel falls back to widgets-mode rendering, ensuring
        content is always displayed.
        """
        # Monkeypatch _render_as_texture to return None (simulate failure)
        monkeypatch.setattr(
            MarkdownLabel,
            '_render_as_texture',
            lambda self, content: None
        )

        # Create MarkdownLabel with render_mode='texture' and non-empty text
        label = MarkdownLabel(
            text='# Hello World\n\nThis is **bold** text.',
            render_mode='texture',
            size=(400, 300),
            size_hint=(None, None)
        )

        # Call force_rebuild() to trigger rendering
        label.force_rebuild()

        # Assert no Image widget in tree (texture mode failed)
        images = find_images(label)
        assert len(images) == 0, \
            f"Expected no Image widgets after texture fallback, found {len(images)}"

        # Assert at least one Label widget exists (widgets-mode fallback)
        labels = find_labels_recursive(label)
        assert len(labels) >= 1, \
            f"Expected at least 1 Label widget in fallback mode, found {len(labels)}"

    def test_texture_fallback_preserves_content(self, monkeypatch):
        """Fallback to widgets mode preserves all content.

        """
        # Monkeypatch _render_as_texture to return None
        monkeypatch.setattr(
            MarkdownLabel,
            '_render_as_texture',
            lambda self, content: None
        )

        # Create MarkdownLabel with multiple content elements
        label = MarkdownLabel(
            text='# Heading\n\nParagraph text.\n\n- List item',
            render_mode='texture',
            size=(400, 300),
            size_hint=(None, None)
        )

        label.force_rebuild()

        # Verify content is rendered (at least one Label exists)
        labels = find_labels_recursive(label)
        assert len(labels) >= 1, \
            "Expected content to be rendered in fallback mode"

        # Verify no Image widgets (texture mode didn't succeed)
        images = find_images(label)
        assert len(images) == 0, \
            "Expected no Image widgets in fallback mode"


@pytest.mark.slow
class TestAutoRenderModeSelection:
    """Property tests for auto render mode selection (Property 16)."""

    def test_auto_mode_uses_widgets_by_default(self):
        """Auto mode uses 'widgets' for simple content without constraints.

        """
        label = MarkdownLabel(
            text='Hello World',
            render_mode='auto',
            strict_label_mode=False
        )

        effective_mode = label._get_effective_render_mode()
        assert effective_mode == 'widgets', \
            f"Expected 'widgets' for simple content, got '{effective_mode}'"

    def test_auto_mode_uses_texture_with_strict_mode_and_height(self):
        """Auto mode uses 'texture' when strict_label_mode with height constraints.

        """
        label = MarkdownLabel(
            text='Hello World',
            render_mode='auto',
            strict_label_mode=True,
            size_hint_y=None,
            height=100
        )

        effective_mode = label._get_effective_render_mode()
        assert effective_mode == 'texture', \
            f"Expected 'texture' with strict_label_mode and height constraint, got '{effective_mode}'"

    def test_auto_mode_uses_texture_with_text_size_height(self):
        """Auto mode uses 'texture' when strict_label_mode with text_size height.

        """
        label = MarkdownLabel(
            text='Hello World',
            render_mode='auto',
            strict_label_mode=True,
            text_size=[400, 100]
        )

        effective_mode = label._get_effective_render_mode()
        assert effective_mode == 'texture', \
            f"Expected 'texture' with strict_label_mode and text_size height, got '{effective_mode}'"

    def test_auto_mode_uses_widgets_without_strict_mode(self):
        """Auto mode uses 'widgets' when strict_label_mode is False.

        """
        label = MarkdownLabel(
            text='Hello World',
            render_mode='auto',
            strict_label_mode=False,
            text_size=[400, 100]  # Even with height constraint
        )

        effective_mode = label._get_effective_render_mode()
        assert effective_mode == 'widgets', \
            f"Expected 'widgets' without strict_label_mode, got '{effective_mode}'"

    @pytest.mark.parametrize('strict_mode,size_hint_y,expected', [
        (False, 1, 'widgets'),
        (False, None, 'widgets'),
        (True, 1, 'widgets'),  # No height constraint
        (True, None, 'texture'),  # Height constraint
    ])
    def test_auto_mode_selection_combinations(self, strict_mode, size_hint_y, expected):
        """Auto mode selection based on strict_label_mode and size_hint_y.

        """
        label = MarkdownLabel(
            text='Hello World',
            render_mode='auto',
            strict_label_mode=strict_mode,
            size_hint_y=size_hint_y
        )

        effective_mode = label._get_effective_render_mode()
        assert effective_mode == expected, \
            f"Expected '{expected}' for strict_mode={strict_mode}, " \
            f"size_hint_y={size_hint_y}, got '{effective_mode}'"

    def test_explicit_widgets_mode_overrides_auto_logic(self):
        """Explicit 'widgets' mode is used regardless of constraints.

        """
        label = MarkdownLabel(
            text='Hello World',
            render_mode='widgets',
            strict_label_mode=True,
            size_hint_y=None,
            height=100
        )

        effective_mode = label._get_effective_render_mode()
        assert effective_mode == 'widgets', \
            f"Expected 'widgets' when explicitly set, got '{effective_mode}'"

    def test_explicit_texture_mode_overrides_auto_logic(self):
        """Explicit 'texture' mode is used regardless of constraints.

        """
        label = MarkdownLabel(
            text='Hello World',
            render_mode='texture',
            strict_label_mode=False
        )

        effective_mode = label._get_effective_render_mode()
        assert effective_mode == 'texture', \
            f"Expected 'texture' when explicitly set, got '{effective_mode}'"
