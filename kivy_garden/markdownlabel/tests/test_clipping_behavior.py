"""
Clipping behavior tests for MarkdownLabel.

This module focuses on verifying that MarkdownLabel:
- wraps content in a clipping container when height-constrained
- does not clip content when unconstrained
"""

import os



from hypothesis import given, strategies as st, settings, assume

from kivy_garden.markdownlabel import MarkdownLabel


class TestContentClippingWhenHeightConstrained:
    """Property tests for content clipping when height-constrained (Property 1)."""

    def _has_clipping_container(self, widget):
        """Check if widget contains a _ClippingContainer (StencilView).

        Args:
            widget: Widget to check

        Returns:
            bool: True if a clipping container is found
        """
        from kivy.uix.stencilview import StencilView

        for child in widget.children:
            if isinstance(child, StencilView):
                return True
        return False

    @given(
        st.text(
            min_size=1,
            max_size=100,
            alphabet=st.characters(
                whitelist_categories=["L", "N", "P", "S", "Z"],
                blacklist_characters="#[]&\n\r*_`~\\",
            ),
        ),
        st.floats(min_value=10.0, max_value=500.0, allow_nan=False, allow_infinity=False),
    )
    @settings(max_examples=100, deadline=None)
    def test_text_size_height_enables_clipping(self, text, height):
        """Setting text_size[1] to a value enables content clipping."""
        assume(text.strip())

        label = MarkdownLabel(text=text, text_size=[None, height])
        label.force_rebuild()

        assert self._has_clipping_container(label), (
            f"Expected clipping container when text_size[1]={height}"
        )

    @given(
        st.text(
            min_size=1,
            max_size=100,
            alphabet=st.characters(
                whitelist_categories=["L", "N", "P", "S", "Z"],
                blacklist_characters="#[]&\n\r*_`~\\",
            ),
        ),
        st.floats(min_value=10.0, max_value=500.0, allow_nan=False, allow_infinity=False),
    )
    @settings(max_examples=100, deadline=None)
    def test_strict_label_mode_with_fixed_height_enables_clipping(self, text, height):
        """strict_label_mode=True with size_hint_y=None enables clipping."""
        assume(text.strip())

        label = MarkdownLabel(
            text=text,
            strict_label_mode=True,
            size_hint_y=None,
            height=height,
        )
        label.force_rebuild()

        assert self._has_clipping_container(label), (
            f"Expected clipping container when strict_label_mode=True and height={height}"
        )

    @given(st.floats(min_value=10.0, max_value=500.0, allow_nan=False, allow_infinity=False))
    @settings(max_examples=100, deadline=None)
    def test_clipping_container_height_matches_text_size(self, height):
        """Clipping container height matches text_size[1]."""
        from kivy.uix.stencilview import StencilView

        label = MarkdownLabel(
            text="# Heading\n\nSome paragraph text here.",
            text_size=[None, height],
        )
        label.force_rebuild()

        # Find the clipping container
        clipping_container = None
        for child in label.children:
            if isinstance(child, StencilView):
                clipping_container = child
                break

        assert clipping_container is not None, "Expected clipping container"
        assert clipping_container.height == height, (
            f"Expected container height={height}, got {clipping_container.height}"
        )

    @given(
        st.integers(min_value=1, max_value=6),
        st.floats(min_value=50.0, max_value=200.0, allow_nan=False, allow_infinity=False),
    )
    @settings(max_examples=100, deadline=None)
    def test_heading_content_clipped_when_height_constrained(self, level, height):
        """Heading content is clipped when height is constrained."""
        heading = "#" * level + " Test Heading"

        label = MarkdownLabel(text=heading, text_size=[None, height])
        label.force_rebuild()

        assert self._has_clipping_container(label), (
            f"Expected clipping for heading level {level} with height={height}"
        )

    def test_clipping_uses_stencil_view(self):
        """Clipping mechanism uses StencilView."""
        from kivy.uix.stencilview import StencilView

        label = MarkdownLabel(
            text="Test content",
            text_size=[None, 50],
        )
        label.force_rebuild()

        # Verify the clipping container is a StencilView
        found_stencil = False
        for child in label.children:
            if isinstance(child, StencilView):
                found_stencil = True
                break

        assert found_stencil, "Expected StencilView for clipping"


class TestNoClippingWhenUnconstrained:
    """Property tests for no clipping when unconstrained (Property 2)."""

    def _has_clipping_container(self, widget):
        """Check if widget contains a _ClippingContainer (StencilView).

        Args:
            widget: Widget to check

        Returns:
            bool: True if a clipping container is found
        """
        from kivy.uix.stencilview import StencilView

        for child in widget.children:
            if isinstance(child, StencilView):
                return True
        return False

    @given(
        st.text(
            min_size=1,
            max_size=100,
            alphabet=st.characters(
                whitelist_categories=["L", "N", "P", "S", "Z"],
                blacklist_characters="#[]&\n\r*_`~\\",
            ),
        )
    )
    @settings(max_examples=100, deadline=None)
    def test_no_clipping_when_text_size_height_none(self, text):
        """No clipping when text_size[1] is None."""
        assume(text.strip())

        label = MarkdownLabel(text=text, text_size=[None, None])
        label.force_rebuild()

        assert not self._has_clipping_container(label), (
            "Expected no clipping container when text_size[1] is None"
        )

    @given(
        st.text(
            min_size=1,
            max_size=100,
            alphabet=st.characters(
                whitelist_categories=["L", "N", "P", "S", "Z"],
                blacklist_characters="#[]&\n\r*_`~\\",
            ),
        )
    )
    @settings(max_examples=100, deadline=None)
    def test_no_clipping_when_strict_label_mode_false(self, text):
        """No clipping when strict_label_mode is False (default)."""
        assume(text.strip())

        label = MarkdownLabel(text=text, strict_label_mode=False)
        label.force_rebuild()

        assert not self._has_clipping_container(label), (
            "Expected no clipping container when strict_label_mode=False"
        )

    @given(
        st.text(
            min_size=1,
            max_size=100,
            alphabet=st.characters(
                whitelist_categories=["L", "N", "P", "S", "Z"],
                blacklist_characters="#[]&\n\r*_`~\\",
            ),
        )
    )
    @settings(max_examples=100, deadline=None)
    def test_content_added_directly_when_unconstrained(self, text):
        """Content is added directly to MarkdownLabel when unconstrained."""
        assume(text.strip())

        label = MarkdownLabel(text=text)
        label.force_rebuild()

        # Children should be Labels or other content widgets, not StencilView
        from kivy.uix.stencilview import StencilView

        for child in label.children:
            assert not isinstance(child, StencilView), (
                "Content should be added directly, not wrapped in StencilView"
            )

    @given(st.integers(min_value=1, max_value=6))
    @settings(max_examples=100, deadline=None)
    def test_heading_expands_naturally_when_unconstrained(self, level):
        """Heading content expands naturally when unconstrained."""
        heading = "#" * level + " Test Heading"

        label = MarkdownLabel(text=heading)
        label.force_rebuild()

        assert not self._has_clipping_container(label), (
            f"Expected no clipping for heading level {level} when unconstrained"
        )

    def test_default_settings_no_clipping(self):
        """Default MarkdownLabel settings do not enable clipping."""
        label = MarkdownLabel(text="Test content")
        label.force_rebuild()

        assert not self._has_clipping_container(label), (
            "Default settings should not enable clipping"
        )

    @given(st.floats(min_value=100.0, max_value=500.0, allow_nan=False, allow_infinity=False))
    @settings(max_examples=100, deadline=None)
    def test_text_size_width_only_no_clipping(self, width):
        """Setting only text_size width (not height) does not enable clipping."""
        label = MarkdownLabel(
            text="Test content",
            text_size=[width, None],
        )
        label.force_rebuild()

        assert not self._has_clipping_container(label), (
            f"Expected no clipping when only text_size width={width} is set"
        )


