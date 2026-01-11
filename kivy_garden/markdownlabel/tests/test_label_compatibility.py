"""
Label compatibility tests for MarkdownLabel widget.

Tests verify that MarkdownLabel maintains compatibility with Kivy Label API
for basic properties like font_size aliases and no-op property acceptance.
"""

import pytest
from hypothesis import given, strategies as st, settings, assume

from kivy_garden.markdownlabel import MarkdownLabel
from .test_utils import (
    simple_markdown_document,
    st_alphanumeric_text,
    st_rgba_color,
    colors_equal
)


# *For any* numeric value V, setting `font_size` to V SHALL result in `base_font_size`
# equaling V, and setting `base_font_size` to V SHALL result in `font_size` returning V.

class TestFontSizeAliasBidirectionality:
    """Property tests for font_size/base_font_size alias."""

    @pytest.mark.property
    @given(st.floats(min_value=1, max_value=200, allow_nan=False, allow_infinity=False))
    # Complex strategy: 50 examples (adequate coverage)
    @settings(max_examples=50, deadline=None)
    def test_font_size_sets_base_font_size(self, font_size_value):
        """Setting font_size updates base_font_size to the same value."""
        label = MarkdownLabel(font_size=font_size_value)

        assert label.base_font_size == font_size_value, \
            f"Expected base_font_size={font_size_value}, got {label.base_font_size}"

    @pytest.mark.property
    @given(st.floats(min_value=1, max_value=200, allow_nan=False, allow_infinity=False))
    # Complex strategy: 50 examples (adequate coverage)
    @settings(max_examples=50, deadline=None)
    def test_base_font_size_returns_via_font_size(self, base_font_size_value):
        """Setting base_font_size is returned when reading font_size."""
        label = MarkdownLabel(base_font_size=base_font_size_value)

        assert label.font_size == base_font_size_value, \
            f"Expected font_size={base_font_size_value}, got {label.font_size}"

    @pytest.mark.property
    @given(st.floats(min_value=1, max_value=200, allow_nan=False, allow_infinity=False),
           st.floats(min_value=1, max_value=200, allow_nan=False, allow_infinity=False))
    # Complex strategy: 50 examples (adequate coverage)
    @settings(max_examples=50, deadline=None)
    def test_font_size_change_updates_base_font_size(self, initial_value, new_value):
        """Changing font_size after creation updates base_font_size."""
        label = MarkdownLabel(font_size=initial_value)
        label.font_size = new_value

        assert label.base_font_size == new_value, \
            f"Expected base_font_size={new_value}, got {label.base_font_size}"

    @pytest.mark.property
    @given(st.floats(min_value=1, max_value=200, allow_nan=False, allow_infinity=False),
           st.floats(min_value=1, max_value=200, allow_nan=False, allow_infinity=False))
    # Complex strategy: 50 examples (adequate coverage)
    @settings(max_examples=50, deadline=None)
    def test_base_font_size_change_updates_font_size(self, initial_value, new_value):
        """Changing base_font_size after creation updates font_size."""
        label = MarkdownLabel(base_font_size=initial_value)
        label.base_font_size = new_value

        assert label.font_size == new_value, \
            f"Expected font_size={new_value}, got {label.font_size}"

    @pytest.mark.property
    @given(st.floats(min_value=1, max_value=200, allow_nan=False, allow_infinity=False))
    # Complex strategy: 50 examples (adequate coverage)
    @settings(max_examples=50, deadline=None)
    def test_bidirectional_equivalence(self, value):
        """font_size and base_font_size are always equivalent."""
        label = MarkdownLabel()

        # Set via font_size
        label.font_size = value
        assert label.font_size == label.base_font_size, \
            f"font_size ({label.font_size}) != base_font_size ({label.base_font_size})"

        # Set via base_font_size
        label.base_font_size = value + 1
        assert label.font_size == label.base_font_size, \
            f"font_size ({label.font_size}) != base_font_size ({label.base_font_size})"


# *For any* no-op property (bold, italic, underline, strikethrough, markup), when set to any
# valid value, the MarkdownLabel SHALL accept the value without raising an exception.

class TestNoOpPropertiesAcceptance:
    """Property tests for no-op properties acceptance."""

    @pytest.mark.property
    @given(st.booleans())
    # Boolean strategy: 2 examples (True/False coverage)
    @settings(max_examples=2, deadline=None)
    def test_bold_property_accepted(self, value):
        """Setting bold property does not raise an exception."""
        # Should not raise any exception
        label = MarkdownLabel(text='# Hello World', bold=value)
        assert label.bold == value

    @pytest.mark.property
    @given(st.booleans())
    # Boolean strategy: 2 examples (True/False coverage)
    @settings(max_examples=2, deadline=None)
    def test_italic_property_accepted(self, value):
        """Setting italic property does not raise an exception."""
        label = MarkdownLabel(text='# Hello World', italic=value)
        assert label.italic == value

    @pytest.mark.property
    @given(st.booleans())
    # Boolean strategy: 2 examples (True/False coverage)
    @settings(max_examples=2, deadline=None)
    def test_underline_property_accepted(self, value):
        """Setting underline property does not raise an exception."""
        label = MarkdownLabel(text='# Hello World', underline=value)
        assert label.underline == value

    @pytest.mark.property
    @given(st.booleans())
    # Boolean strategy: 2 examples (True/False coverage)
    @settings(max_examples=2, deadline=None)
    def test_strikethrough_property_accepted(self, value):
        """Setting strikethrough property does not raise an exception."""
        label = MarkdownLabel(text='# Hello World', strikethrough=value)
        assert label.strikethrough == value

    @pytest.mark.property
    @given(st.booleans())
    # Boolean strategy: 2 examples (True/False coverage)
    @settings(max_examples=2, deadline=None)
    def test_markup_property_accepted(self, value):
        """Setting markup property does not raise an exception."""
        label = MarkdownLabel(text='# Hello World', markup=value)
        assert label.markup == value

    @pytest.mark.property
    @given(st.booleans(), st.booleans(), st.booleans(), st.booleans(), st.booleans())
    # Combination strategy: 32 examples (combination coverage)
    @settings(max_examples=32, deadline=None)
    def test_all_noop_properties_together(self, bold, italic, underline, strikethrough, markup):
        """Setting all no-op properties together does not raise an exception."""
        label = MarkdownLabel(
            text='# Hello World',
            bold=bold,
            italic=italic,
            underline=underline,
            strikethrough=strikethrough,
            markup=markup
        )
        assert label.bold == bold
        assert label.italic == italic
        assert label.underline == underline
        assert label.strikethrough == strikethrough
        assert label.markup == markup

    @pytest.mark.property
    @given(st.booleans(), st.booleans(), st.booleans(), st.booleans(), st.booleans(),
           simple_markdown_document())
    # Mixed finite/complex strategy: 50 examples (32 finite × 2 complex samples)
    @settings(max_examples=50, deadline=None)
    def test_noop_properties_do_not_affect_rendering(self, bold, italic, underline,
                                                      strikethrough, markup, markdown_text):
        """No-op properties do not affect the rendered output."""
        assume(markdown_text.strip())

        # Create label with default no-op property values
        label_default = MarkdownLabel(text=markdown_text)
        default_child_count = len(label_default.children)

        # Create label with various no-op property values
        label_with_props = MarkdownLabel(
            text=markdown_text,
            bold=bold,
            italic=italic,
            underline=underline,
            strikethrough=strikethrough,
            markup=markup
        )
        props_child_count = len(label_with_props.children)

        # The number of children should be the same regardless of no-op properties
        assert default_child_count == props_child_count, \
            f"Expected {default_child_count} children, got {props_child_count} with no-op props"

    @pytest.mark.property
    @given(st.booleans())
    # Boolean strategy: 2 examples (True/False coverage)
    @settings(max_examples=2, deadline=None)
    def test_bold_property_change_after_creation(self, value):
        """Changing bold property after creation does not raise an exception."""
        label = MarkdownLabel(text='# Hello')
        label.bold = value
        assert label.bold == value

    @pytest.mark.property
    @given(st.booleans())
    # Boolean strategy: 2 examples (True/False coverage)
    @settings(max_examples=2, deadline=None)
    def test_italic_property_change_after_creation(self, value):
        """Changing italic property after creation does not raise an exception."""
        label = MarkdownLabel(text='# Hello')
        label.italic = value
        assert label.italic == value

    @pytest.mark.property
    @given(st.booleans())
    # Boolean strategy: 2 examples (True/False coverage)
    @settings(max_examples=2, deadline=None)
    def test_underline_property_change_after_creation(self, value):
        """Changing underline property after creation does not raise an exception."""
        label = MarkdownLabel(text='# Hello')
        label.underline = value
        assert label.underline == value

    @pytest.mark.property
    @given(st.booleans())
    # Boolean strategy: 2 examples (True/False coverage)
    @settings(max_examples=2, deadline=None)
    def test_strikethrough_property_change_after_creation(self, value):
        """Changing strikethrough property after creation does not raise an exception."""
        label = MarkdownLabel(text='# Hello')
        label.strikethrough = value
        assert label.strikethrough == value

    @pytest.mark.property
    @given(st.booleans())
    # Boolean strategy: 2 examples (True/False coverage)
    @settings(max_examples=2, deadline=None)
    def test_markup_property_change_after_creation(self, value):
        """Changing markup property after creation does not raise an exception."""
        label = MarkdownLabel(text='# Hello')
        label.markup = value
        assert label.markup == value


# *For any* no-op property (mipmap, outline_width, outline_color, text_language,
# base_direction, ellipsis_options),
# when set to any valid value, the MarkdownLabel SHALL accept the value without
# raising an exception
# AND return the same value when accessed.

class TestNoOpPropertyAcceptanceAndStorage:
    """Property tests for no-op property acceptance and storage."""

    @pytest.mark.property
    @given(st.booleans())
    # Boolean strategy: 2 examples (True/False coverage)
    @settings(max_examples=2, deadline=None)
    def test_mipmap_property_accepted_and_stored(self, value):
        """Setting mipmap property accepts and stores the value."""
        label = MarkdownLabel(text='# Hello World', mipmap=value)
        assert label.mipmap == value

    @pytest.mark.property
    @given(st.floats(min_value=0, max_value=100, allow_nan=False, allow_infinity=False))
    # Complex strategy: 50 examples (adequate coverage)
    @settings(max_examples=50, deadline=None)
    def test_outline_width_property_accepted_and_stored(self, value):
        """Setting outline_width property accepts and stores the value."""
        label = MarkdownLabel(text='# Hello World', outline_width=value)
        assert label.outline_width == value

    @pytest.mark.property
    @given(st_rgba_color())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_outline_color_property_accepted_and_stored(self, value):
        """Setting outline_color property accepts and stores the value."""
        label = MarkdownLabel(text='# Hello World', outline_color=value)
        # Compare colors with tolerance for floating point differences
        assert colors_equal(list(label.outline_color), list(value))

    @pytest.mark.property
    @given(st.one_of(st.none(), st_alphanumeric_text(min_size=1, max_size=10)))
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_text_language_property_accepted_and_stored(self, value):
        """Setting text_language property accepts and stores the value."""
        label = MarkdownLabel(text='# Hello World', text_language=value)
        assert label.text_language == value

    @pytest.mark.parametrize('value', [None, 'ltr', 'rtl', 'weak_ltr', 'weak_rtl'])
    def test_base_direction_property_accepted_and_stored(self, value):
        """Setting base_direction property accepts and stores the value."""
        label = MarkdownLabel(text='# Hello World', base_direction=value)
        assert label.base_direction == value

    @pytest.mark.property
    @given(st.dictionaries(
        st_alphanumeric_text(min_size=1, max_size=10),
        st.one_of(st.booleans(), st.integers(), st.text(max_size=20))
    ))
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_ellipsis_options_property_accepted_and_stored(self, value):
        """Setting ellipsis_options property accepts and stores the value."""
        label = MarkdownLabel(text='# Hello World', ellipsis_options=value)
        assert label.ellipsis_options == value

    @given(st.booleans(), st.floats(min_value=0, max_value=10),
           st_rgba_color(),
           st.one_of(st.none(), st.text(min_size=1, max_size=5)),
           st.sampled_from([None, 'ltr', 'rtl', 'weak_ltr', 'weak_rtl']),
           st.dictionaries(st.text(min_size=1, max_size=5), st.booleans(), max_size=3))
    # Mixed finite/complex strategy: 50 examples (10 finite × 5 complex samples)
    @settings(max_examples=50, deadline=None)
    def test_all_noop_properties_together_accepted_and_stored(self, mipmap, outline_width,
                                                              outline_color, text_language,
                                                              base_direction, ellipsis_options):
        """Setting all no-op properties together accepts and stores all values."""
        label = MarkdownLabel(
            text='# Hello World',
            mipmap=mipmap,
            outline_width=outline_width,
            outline_color=outline_color,
            text_language=text_language,
            base_direction=base_direction,
            ellipsis_options=ellipsis_options
        )

        assert label.mipmap == mipmap
        assert label.outline_width == outline_width
        assert colors_equal(list(label.outline_color), list(outline_color))
        assert label.text_language == text_language
        assert label.base_direction == base_direction
        assert label.ellipsis_options == ellipsis_options

    @pytest.mark.property
    @given(st.booleans())
    # Boolean strategy: 2 examples (True/False coverage)
    @settings(max_examples=2, deadline=None)
    def test_mipmap_property_change_after_creation(self, value):
        """Changing mipmap property after creation accepts and stores the value."""
        label = MarkdownLabel(text='# Hello')
        label.mipmap = value
        assert label.mipmap == value

    @pytest.mark.property
    @given(st.floats(min_value=0, max_value=100, allow_nan=False, allow_infinity=False))
    # Complex strategy: 50 examples (adequate coverage)
    @settings(max_examples=50, deadline=None)
    def test_outline_width_property_change_after_creation(self, value):
        """Changing outline_width property after creation accepts and stores the value."""
        label = MarkdownLabel(text='# Hello')
        label.outline_width = value
        assert label.outline_width == value

    @pytest.mark.property
    @given(st_rgba_color())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_outline_color_property_change_after_creation(self, value):
        """Changing outline_color property after creation accepts and stores the value."""
        label = MarkdownLabel(text='# Hello')
        label.outline_color = value
        assert colors_equal(list(label.outline_color), list(value))

    @pytest.mark.property
    @given(st.one_of(st.none(), st_alphanumeric_text(min_size=1, max_size=10)))
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_text_language_property_change_after_creation(self, value):
        """Changing text_language property after creation accepts and stores the value."""
        label = MarkdownLabel(text='# Hello')
        label.text_language = value
        assert label.text_language == value

    @pytest.mark.parametrize('value', [None, 'ltr', 'rtl', 'weak_ltr', 'weak_rtl'])
    def test_base_direction_property_change_after_creation(self, value):
        """Changing base_direction property after creation accepts and stores the value."""
        label = MarkdownLabel(text='# Hello')
        label.base_direction = value
        assert label.base_direction == value

    @pytest.mark.property
    @given(st.dictionaries(
        st_alphanumeric_text(min_size=1, max_size=10),
        st.one_of(st.booleans(), st.integers(), st.text(max_size=20))
    ))
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_ellipsis_options_property_change_after_creation(self, value):
        """Changing ellipsis_options property after creation accepts and stores the value."""
        label = MarkdownLabel(text='# Hello')
        label.ellipsis_options = value
        assert label.ellipsis_options == value

    @pytest.mark.property
    @given(st.booleans(), st.floats(min_value=0, max_value=10),
           st_rgba_color(),
           st.one_of(st.none(), st.text(min_size=1, max_size=5)),
           st.sampled_from([None, 'ltr', 'rtl', 'weak_ltr', 'weak_rtl']),
           st.dictionaries(st.text(min_size=1, max_size=5), st.booleans(), max_size=3),
           simple_markdown_document())
    # Mixed finite/complex strategy: 20 examples (10 finite × 2 complex samples)
    @settings(max_examples=20, deadline=None)
    def test_advanced_noop_properties_do_not_affect_rendering(self, mipmap, outline_width, outline_color,
                                                              text_language, base_direction, ellipsis_options,
                                                              markdown_text):
        """Advanced no-op properties do not affect the rendered output."""
        assume(markdown_text.strip())

        # Create label with default no-op property values
        label_default = MarkdownLabel(text=markdown_text)
        default_child_count = len(label_default.children)

        # Create label with various no-op property values
        label_with_props = MarkdownLabel(
            text=markdown_text,
            mipmap=mipmap,
            outline_width=outline_width,
            outline_color=outline_color,
            text_language=text_language,
            base_direction=base_direction,
            ellipsis_options=ellipsis_options
        )
        props_child_count = len(label_with_props.children)

        # The number of children should be the same regardless of no-op properties
        assert default_child_count == props_child_count, \
            f"Expected {default_child_count} children, got {props_child_count} with no-op props"
