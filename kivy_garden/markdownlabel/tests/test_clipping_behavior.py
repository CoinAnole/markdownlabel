"""
Clipping behavior tests for MarkdownLabel.

This module contains tests for content clipping behavior in MarkdownLabel,
including verification that content is wrapped in a StencilView clipping container
when height-constrained and that content expands naturally when unconstrained.
Tests cover both property-based testing with Hypothesis and unit tests for
specific clipping scenarios.
"""


import pytest
from hypothesis import given, strategies as st, settings, assume

from kivy_garden.markdownlabel import MarkdownLabel
from .test_utils import has_clipping_container


class TestContentClippingWhenHeightConstrained:
    """Property tests for content clipping when height-constrained."""

    @pytest.mark.property
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
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_text_size_height_enables_clipping(self, text, height):
        """Setting text_size[1] to a value enables content clipping."""
        assume(text.strip())

        label = MarkdownLabel(text=text, text_size=[None, height])
        label.force_rebuild()

        assert has_clipping_container(label), (
            f"Expected clipping container when text_size[1]={height}"
        )

    @pytest.mark.property
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
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
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

        assert has_clipping_container(label), (
            f"Expected clipping container when strict_label_mode=True and height={height}"
        )

    @pytest.mark.property
    @given(st.floats(min_value=10.0, max_value=500.0, allow_nan=False, allow_infinity=False))
    # Complex strategy: 15 examples (adequate coverage)
    @settings(max_examples=15, deadline=None)
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

    @pytest.mark.property
    @given(
        st.integers(min_value=1, max_value=6),
        st.floats(min_value=50.0, max_value=200.0, allow_nan=False, allow_infinity=False),
    )
    # Small finite strategy: 6 examples (input space size: 6)
    @settings(max_examples=6, deadline=None)
    def test_heading_content_clipped_when_height_constrained(self, level, height):
        """Heading content is clipped when height is constrained."""
        heading = "#" * level + " Test Heading"

        label = MarkdownLabel(text=heading, text_size=[None, height])
        label.force_rebuild()

        assert has_clipping_container(label), (
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
    """Property tests for no clipping when unconstrained."""

    @pytest.mark.property
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
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_no_clipping_when_text_size_height_none(self, text):
        """No clipping when text_size[1] is None."""
        assume(text.strip())

        label = MarkdownLabel(text=text, text_size=[None, None])
        label.force_rebuild()

        assert not has_clipping_container(label), (
            "Expected no clipping container when text_size[1] is None"
        )

    @pytest.mark.property
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
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_no_clipping_when_strict_label_mode_false(self, text):
        """No clipping when strict_label_mode is False (default)."""
        assume(text.strip())

        label = MarkdownLabel(text=text, strict_label_mode=False)
        label.force_rebuild()

        assert not has_clipping_container(label), (
            "Expected no clipping container when strict_label_mode=False"
        )

    @pytest.mark.property
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
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
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

    @pytest.mark.property
    @given(st.integers(min_value=1, max_value=6))
    # Small finite strategy: 6 examples (input space size: 6)
    @settings(max_examples=6, deadline=None)
    def test_heading_expands_naturally_when_unconstrained(self, level):
        """Heading content expands naturally when unconstrained."""
        heading = "#" * level + " Test Heading"

        label = MarkdownLabel(text=heading)
        label.force_rebuild()

        assert not has_clipping_container(label), (
            f"Expected no clipping for heading level {level} when unconstrained"
        )

    def test_default_settings_no_clipping(self):
        """Default MarkdownLabel settings do not enable clipping."""
        label = MarkdownLabel(text="Test content")
        label.force_rebuild()

        assert not has_clipping_container(label), (
            "Default settings should not enable clipping"
        )

    @pytest.mark.property
    @given(st.floats(min_value=100.0, max_value=500.0, allow_nan=False, allow_infinity=False))
    # Complex strategy: 15 examples (adequate coverage)
    @settings(max_examples=15, deadline=None)
    def test_text_size_width_only_no_clipping(self, width):
        """Setting only text_size width (not height) does not enable clipping."""
        label = MarkdownLabel(
            text="Test content",
            text_size=[width, None],
        )
        label.force_rebuild()

        assert not has_clipping_container(label), (
            f"Expected no clipping when only text_size width={width} is set"
        )
