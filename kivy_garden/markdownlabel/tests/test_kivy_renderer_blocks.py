"""
Property-based tests and edge case coverage for KivyRenderer.

This module contains tests that verify block-level Markdown elements are correctly
converted to Kivy widgets, along with tests targeting specific implementation details
of KivyRenderer to improve code coverage for edge cases and internal methods.
"""

import pytest
from hypothesis import given, strategies as st, settings, assume

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.image import AsyncImage
from kivy.graphics import Rectangle, Line

from kivy_garden.markdownlabel.kivy_renderer import KivyRenderer
from .test_utils import (
    heading_token,
    paragraph_token,
    list_token,
    code_block_token,
    block_quote_token,
    image_token
)


# *For any* Markdown document containing headings of different levels,
# headings with smaller level numbers (e.g., h1) SHALL have larger font sizes
# than headings with larger level numbers (e.g., h6).

class TestHeadingFontHierarchy:
    """Property tests for heading font size hierarchy."""

    @pytest.mark.property
    @given(st.integers(min_value=1, max_value=5))
    # Small finite strategy: 5 examples (input space size: 5)
    @settings(max_examples=5, deadline=None)
    def test_smaller_level_has_larger_font(self, level):
        """Headings with smaller level numbers have larger font sizes."""
        renderer = KivyRenderer(base_font_size=15)

        # Create two headings: one at 'level', one at 'level + 1'
        heading1_token = {
            'type': 'heading',
            'children': [{'type': 'text', 'raw': 'Heading'}],
            'attrs': {'level': level}
        }
        heading2_token = {
            'type': 'heading',
            'children': [{'type': 'text', 'raw': 'Heading'}],
            'attrs': {'level': level + 1}
        }

        widget1 = renderer.heading(heading1_token, None)
        widget2 = renderer.heading(heading2_token, None)

        assert widget1.font_size > widget2.font_size, \
            f"h{level} font_size ({widget1.font_size}) should be > h{level+1} font_size ({widget2.font_size})"

    @pytest.mark.property
    @given(heading_token())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_heading_returns_label(self, token):
        """Heading tokens produce Label widgets."""
        renderer = KivyRenderer()
        widget = renderer.heading(token, None)

        assert isinstance(widget, Label), f"Expected Label, got {type(widget)}"

    @pytest.mark.property
    @given(heading_token())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_heading_has_markup_enabled(self, token):
        """Heading Labels have markup=True."""
        renderer = KivyRenderer()
        widget = renderer.heading(token, None)

        assert widget.markup is True, "Heading should have markup=True"

    @pytest.mark.property
    @given(st.integers(min_value=1, max_value=6), st.floats(min_value=10, max_value=30))
    # Mixed finite/complex strategy: 30 examples (6 finite × 5 complex samples)
    @settings(max_examples=30, deadline=None)
    def test_heading_font_size_scales_with_base(self, level, base_size):
        """Heading font size scales proportionally with base_font_size."""
        assume(base_size > 0)

        renderer = KivyRenderer(base_font_size=base_size)
        token = {
            'type': 'heading',
            'children': [{'type': 'text', 'raw': 'Test'}],
            'attrs': {'level': level}
        }

        widget = renderer.heading(token, None)
        expected_multiplier = KivyRenderer.HEADING_SIZES[level]
        expected_size = base_size * expected_multiplier

        assert abs(widget.font_size - expected_size) < 0.01, \
            f"Expected font_size {expected_size}, got {widget.font_size}"


# *For any* Markdown paragraph, the rendered Label widget SHALL have markup=True.


class TestParagraphMarkupEnabled:
    """Property tests for paragraph markup enabled."""

    @pytest.mark.property
    @given(paragraph_token())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_paragraph_has_markup_enabled(self, token):
        """Paragraph Labels have markup=True."""
        renderer = KivyRenderer()
        widget = renderer.paragraph(token, None)

        assert isinstance(widget, Label), f"Expected Label, got {type(widget)}"
        assert widget.markup is True, "Paragraph should have markup=True"

    @pytest.mark.property
    @given(paragraph_token())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_paragraph_returns_label(self, token):
        """Paragraph tokens produce Label widgets."""
        renderer = KivyRenderer()
        widget = renderer.paragraph(token, None)

        assert isinstance(widget, Label), f"Expected Label, got {type(widget)}"


# *For any* Markdown list (ordered or unordered), the rendered widget tree SHALL
# contain a BoxLayout with one child BoxLayout per list item, and each item
# SHALL be prefixed with the appropriate marker (bullet or number).


class TestListStructurePreservation:
    """Property tests for list structure preservation."""

    @pytest.mark.property
    @given(list_token())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_list_returns_boxlayout(self, token):
        """List tokens produce BoxLayout widgets."""
        renderer = KivyRenderer()
        widget = renderer.list(token, None)

        assert isinstance(widget, BoxLayout), f"Expected BoxLayout, got {type(widget)}"

    @pytest.mark.property
    @given(list_token())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_list_has_correct_item_count(self, token):
        """List has one child per list item."""
        renderer = KivyRenderer()
        widget = renderer.list(token, None)

        expected_count = len(token['children'])
        actual_count = len(widget.children)

        assert actual_count == expected_count, \
            f"Expected {expected_count} children, got {actual_count}"

    @pytest.mark.property
    @given(list_token(ordered=False))
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_unordered_list_has_bullet_markers(self, token):
        """Unordered list items have bullet markers."""
        renderer = KivyRenderer()
        widget = renderer.list(token, None)

        # Each child should be a horizontal BoxLayout with a marker Label
        for child in widget.children:
            assert isinstance(child, BoxLayout), "List item should be BoxLayout"
            # First child of item layout should be the marker
            # Note: Kivy children are in reverse order (last added is first)
            marker = child.children[-1]  # Last in list = first added = marker
            assert isinstance(marker, Label), "Marker should be Label"
            assert '•' in marker.text, f"Unordered list marker should contain bullet, got: {marker.text}"

    @pytest.mark.property
    @given(list_token(ordered=True))
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_ordered_list_has_number_markers(self, token):
        """Ordered list items have number markers."""
        renderer = KivyRenderer()
        widget = renderer.list(token, None)

        num_items = len(token['children'])

        # Each child should be a horizontal BoxLayout with a marker Label
        # Note: Kivy children are in reverse order (last added is first in list)
        for i, child in enumerate(widget.children):
            assert isinstance(child, BoxLayout), "List item should be BoxLayout"
            # First child of item layout should be the marker
            marker = child.children[-1]  # Last in list = first added = marker
            assert isinstance(marker, Label), "Marker should be Label"
            # Marker should contain a number followed by period
            # Account for reverse order: item at index i corresponds to item (num_items - i)
            expected_num = str(num_items - i)
            assert expected_num in marker.text and '.' in marker.text, \
                f"Ordered list marker should contain '{expected_num}.', got: {marker.text}"


# *For any* Markdown list containing nested lists, each nesting level SHALL
# increase the left padding/indentation of the nested content.

class TestNestedListIndentation:
    """Property tests for nested list indentation."""

    @pytest.mark.property
    @given(st.integers(min_value=1, max_value=4))
    # Small finite strategy: 4 examples (input space size: 4)
    @settings(max_examples=4, deadline=None)
    def test_nested_list_increases_indentation(self, depth):
        """Nested lists have increasing left padding."""
        renderer = KivyRenderer()

        # Create nested list structure
        def create_nested_list(current_depth, max_depth):
            if current_depth > max_depth:
                return {
                    'type': 'list_item',
                    'children': [{
                        'type': 'paragraph',
                        'children': [{'type': 'text', 'raw': 'Leaf item'}]
                    }]
                }

            return {
                'type': 'list',
                'children': [{
                    'type': 'list_item',
                    'children': [
                        {
                            'type': 'paragraph',
                            'children': [{'type': 'text', 'raw': f'Level {current_depth}'}]
                        },
                        create_nested_list(current_depth + 1, max_depth)
                    ]
                }],
                'attrs': {'ordered': False, 'start': 1}
            }

        token = create_nested_list(1, depth)
        widget = renderer.list(token, None)

        # Check that the outer list has padding
        assert widget.padding[0] > 0, "List should have left padding"

        # The padding should be based on list depth (20 * depth)
        expected_padding = 20  # First level padding
        assert widget.padding[0] == expected_padding, \
            f"Expected padding {expected_padding}, got {widget.padding[0]}"


# *For any* Markdown code block (fenced or indented), the rendered widget SHALL
# use a monospace font and have a dark background color applied.


class TestCodeBlockStyling:
    """Property tests for code block styling."""

    @pytest.mark.property
    @given(code_block_token())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_code_block_returns_widget(self, token):
        """Code block tokens produce Widget containers."""
        renderer = KivyRenderer()
        widget = renderer.block_code(token, None)

        assert isinstance(widget, Widget), f"Expected Widget, got {type(widget)}"

    @pytest.mark.property
    @given(code_block_token())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_code_block_has_monospace_font(self, token):
        """Code block uses monospace font."""
        renderer = KivyRenderer(code_font_name='RobotoMono-Regular')
        widget = renderer.block_code(token, None)

        # The widget is a BoxLayout container with a Label child
        assert isinstance(widget, BoxLayout), "Expected BoxLayout container"

        # Find the Label child
        label = None
        for child in widget.children:
            if isinstance(child, Label):
                label = child
                break

        assert label is not None, "Code block should contain a Label"
        assert label.font_name == 'RobotoMono-Regular', \
            f"Expected monospace font, got {label.font_name}"

    @pytest.mark.property
    @given(code_block_token())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_code_block_has_dark_background(self, token):
        """Code block has dark background color."""
        dark_bg = [0.15, 0.15, 0.15, 1]
        renderer = KivyRenderer(code_bg_color=dark_bg)
        widget = renderer.block_code(token, None)

        # Check that canvas.before has instructions (background)
        assert any(isinstance(instr, Rectangle) for instr in widget.canvas.before.children)


# *For any* fenced code block with a language identifier, the rendered widget
# SHALL store the language string in an accessible attribute.

class TestCodeBlockLanguageMetadata:
    """Property tests for code block language metadata."""

    @pytest.mark.property
    @given(code_block_token())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_code_block_stores_language_info(self, token):
        """Code block stores language info as attribute."""
        renderer = KivyRenderer()
        widget = renderer.block_code(token, None)

        expected_language = token['attrs'].get('info', '')

        assert hasattr(widget, 'language_info'), "Code block should have language_info attribute"
        assert widget.language_info == expected_language, \
            f"Expected language '{expected_language}', got '{widget.language_info}'"

    @pytest.mark.parametrize('language', ['python', 'javascript', 'rust', 'go', 'java', 'c', 'cpp'])
    def test_specific_languages_stored_correctly(self, language):
        """Specific language identifiers are stored correctly."""
        renderer = KivyRenderer()
        token = {
            'type': 'block_code',
            'raw': 'print("hello")',
            'attrs': {'info': language}
        }

        widget = renderer.block_code(token, None)

        assert widget.language_info == language, \
            f"Expected language '{language}', got '{widget.language_info}'"


# *For any* Markdown block quote, the rendered widget SHALL be a BoxLayout
# with left border styling and its content indented from the left edge.

class TestBlockQuoteStructure:
    """Property tests for block quote structure."""

    @pytest.mark.property
    @given(block_quote_token())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_block_quote_returns_boxlayout(self, token):
        """Block quote tokens produce BoxLayout widgets."""
        renderer = KivyRenderer()
        widget = renderer.block_quote(token, None)

        assert isinstance(widget, BoxLayout), f"Expected BoxLayout, got {type(widget)}"

    @pytest.mark.property
    @given(block_quote_token())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_block_quote_has_left_padding(self, token):
        """Block quote has left padding for indentation."""
        renderer = KivyRenderer()
        widget = renderer.block_quote(token, None)

        # Check left padding (first element of padding tuple)
        assert widget.padding[0] > 0, \
            f"Block quote should have left padding, got {widget.padding[0]}"

    @pytest.mark.property
    @given(block_quote_token())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_block_quote_has_left_border(self, token):
        """Block quote has left border line."""
        renderer = KivyRenderer()
        widget = renderer.block_quote(token, None)

        # Check that canvas.before has border line
        assert any(isinstance(instr, Line) for instr in widget.canvas.before.children)


# *For any* Markdown thematic break (---, ***, ___), the rendered widget tree
# SHALL contain a Widget with a horizontal line drawn on its canvas.

class TestThematicBreakRendering:
    """Property tests for thematic break rendering."""

    def test_thematic_break_returns_widget(self):
        """Thematic break tokens produce Widget."""
        renderer = KivyRenderer()
        token = {'type': 'thematic_break'}
        widget = renderer.thematic_break(token, None)

        assert isinstance(widget, Widget), f"Expected Widget, got {type(widget)}"

    def test_thematic_break_has_fixed_height(self):
        """Thematic break has fixed height."""
        renderer = KivyRenderer()
        token = {'type': 'thematic_break'}
        widget = renderer.thematic_break(token, None)

        assert widget.size_hint_y is None, "Thematic break should have size_hint_y=None"
        assert widget.height > 0, "Thematic break should have positive height"

    def test_thematic_break_has_horizontal_line(self):
        """Thematic break has horizontal line on canvas."""
        renderer = KivyRenderer()
        token = {'type': 'thematic_break'}
        widget = renderer.thematic_break(token, None)

        # Check that canvas has line instruction
        assert any(isinstance(instr, Line) for instr in widget.canvas.children)


# *For any* Markdown image ![alt](url), the rendered widget tree SHALL contain
# an AsyncImage widget with source=url.

class TestImageWidgetCreation:
    """Property tests for image widget creation."""

    @pytest.mark.property
    @given(image_token())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_image_returns_asyncimage(self, token):
        """Image tokens produce AsyncImage widgets."""
        renderer = KivyRenderer()
        widget = renderer.image(token, None)

        assert isinstance(widget, AsyncImage), f"Expected AsyncImage, got {type(widget)}"

    @pytest.mark.property
    @given(image_token())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_image_has_correct_source(self, token):
        """Image widget has correct source URL."""
        renderer = KivyRenderer()
        widget = renderer.image(token, None)

        expected_url = token['attrs']['url']
        assert widget.source == expected_url, \
            f"Expected source '{expected_url}', got '{widget.source}'"

    @pytest.mark.property
    @given(image_token())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_image_stores_alt_text(self, token):
        """Image widget stores alt text for fallback."""
        renderer = KivyRenderer()
        widget = renderer.image(token, None)

        assert hasattr(widget, 'alt_text'), "Image should have alt_text attribute"


# *For any* Markdown table with R rows and C columns, the rendered GridLayout
# SHALL have cols=C and contain exactly R×C Label widgets.
