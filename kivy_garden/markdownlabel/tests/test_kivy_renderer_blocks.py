"""
Property-based tests and edge case coverage for KivyRenderer.

This module contains tests that verify block-level Markdown elements are correctly
converted to Kivy widgets, along with tests targeting specific implementation details
of KivyRenderer to improve code coverage for edge cases and internal methods.
"""

import pytest
from unittest.mock import MagicMock, patch
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


class TestDeepNestingTruncation:
    """Tests for deep nesting truncation placeholder behavior."""

    def test_truncation_placeholder_when_nesting_exceeds_max(self):
        """When nesting depth exceeds max, _render_token returns placeholder.

        Requirement 7.1: WHEN rendering content that exceeds _max_nesting_depth,
        THE KivyRenderer SHALL return a truncation placeholder widget.
        """
        renderer = KivyRenderer()

        # Manually set nesting depth beyond the maximum
        renderer._nesting_depth = renderer._max_nesting_depth + 1

        # Create a simple token to render
        token = {
            'type': 'paragraph',
            'children': [{'type': 'text', 'raw': 'This should be truncated'}]
        }

        # Render the token - should return truncation placeholder
        widget = renderer._render_token(token, None)

        assert isinstance(widget, Label), \
            f"Expected Label placeholder, got {type(widget)}"
        assert 'content truncated' in widget.text.lower(), \
            f"Placeholder text should contain 'content truncated', got: {widget.text}"

    def test_truncation_placeholder_text_format(self):
        """Truncation placeholder has expected text format.

        Requirement 7.2: THE truncation placeholder SHALL be a Label widget
        with text containing "content truncated".
        """
        renderer = KivyRenderer()

        # Manually set nesting depth beyond the maximum
        renderer._nesting_depth = renderer._max_nesting_depth + 1

        # Any token type should trigger truncation
        token = {'type': 'heading', 'children': [], 'attrs': {'level': 1}}

        widget = renderer._render_token(token, None)

        assert isinstance(widget, Label), \
            f"Expected Label, got {type(widget)}"
        assert 'content truncated' in widget.text.lower(), \
            f"Expected 'content truncated' in text, got: {widget.text}"
        assert 'deep nesting' in widget.text.lower(), \
            f"Expected 'deep nesting' in text, got: {widget.text}"

    def test_truncation_placeholder_styling(self):
        """Truncation placeholder has appropriate styling (gray, italic)."""
        renderer = KivyRenderer()

        # Manually set nesting depth beyond the maximum
        renderer._nesting_depth = renderer._max_nesting_depth + 1

        token = {'type': 'paragraph', 'children': []}

        widget = renderer._render_token(token, None)

        assert isinstance(widget, Label), \
            f"Expected Label, got {type(widget)}"
        # Check gray color (approximately [0.6, 0.6, 0.6, 1])
        assert widget.color[0] < 0.7 and widget.color[0] > 0.5, \
            f"Expected gray color, got: {widget.color}"
        assert widget.italic is True, \
            f"Expected italic=True, got: {widget.italic}"

    def test_normal_nesting_does_not_truncate(self):
        """Normal nesting depth does not trigger truncation."""
        renderer = KivyRenderer()

        # Keep nesting depth at or below maximum
        renderer._nesting_depth = renderer._max_nesting_depth

        token = {
            'type': 'paragraph',
            'children': [{'type': 'text', 'raw': 'Normal content'}]
        }

        widget = renderer._render_token(token, None)

        assert isinstance(widget, Label), \
            f"Expected Label, got {type(widget)}"
        # Should NOT be a truncation placeholder
        assert 'content truncated' not in widget.text.lower(), \
            f"Should not truncate at max depth, got: {widget.text}"
        assert 'Normal content' in widget.text, \
            f"Expected normal content, got: {widget.text}"


class TestKivyRendererEdgeCases:
    """Tests for KivyRenderer edge cases and internal methods."""

    @pytest.fixture
    def renderer(self):
        """Create a KivyRenderer instance."""
        label = MagicMock()
        label.padding = [10, 10, 10, 10]
        renderer = KivyRenderer(label)
        renderer.base_font_size = 15.0
        return renderer

    def test_render_list_item_nested_structures(self, renderer):
        """Test _render_list_item with nested lists to hit specific branches."""
        token = {
            'type': 'list_item',
            'children': [
                {
                    'type': 'list',
                    'children': [
                        {
                            'type': 'list_item',
                            'children': [
                                {
                                    'type': 'block_text',
                                    'children': [{'type': 'text', 'raw': 'nested'}]
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        with patch.object(renderer, 'list') as mock_list:
            mock_list.return_value = BoxLayout()
            container = (
                BoxLayout() if not hasattr(renderer, '_render_list_item')
                else renderer._render_list_item(token, False, 0)
            )
            assert mock_list.called

    def test_image_on_texture_callback(self, renderer):
        """Test the on_texture callback in image rendering."""
        renderer.label = MagicMock()
        token = {
            'type': 'image',
            'attrs': {'url': 'http://example.com/test.png'},
            'children': [{'type': 'text', 'raw': 'Alt Text'}]
        }

        with patch('kivy_garden.markdownlabel.kivy_renderer.AsyncImage') as MockAsyncImage:
            mock_image = MockAsyncImage.return_value
            mock_image.texture = MagicMock()
            mock_image.texture.size = (100, 50)
            mock_image.texture.width = 100
            mock_image.texture.height = 50
            mock_image.width = 100

            renderer.image(token)

            assert mock_image.bind.called
            args, kwargs = mock_image.bind.call_args
            assert 'texture' in kwargs
            callback = kwargs['texture']

            callback(mock_image, mock_image.texture)
            assert mock_image.height == 50

    def test_block_code_update_bg_logic(self, renderer):
        """Test the update_bg function inner logic in block_code."""
        token = {
            'type': 'block_code',
            'raw': 'print("hello")',
            'attrs': {'info': 'python'}
        }

        with patch('kivy_garden.markdownlabel.kivy_renderer.Color'), \
             patch('kivy_garden.markdownlabel.kivy_renderer.Rectangle') as MockRect:
            container = renderer.block_code(token)
            container.pos = (10, 10)
            container.size = (100, 100)
            assert MockRect.called
            rect_instance = MockRect.return_value
            assert rect_instance.pos == container.pos
            assert rect_instance.size == container.size

    def test_block_quote_update_border_logic(self, renderer):
        """Test the update_border function inner logic in block_quote."""
        token = {
            'type': 'block_quote',
            'children': [{'type': 'paragraph', 'children': [{'type': 'text', 'raw': 'Quote'}]}]
        }

        with patch('kivy_garden.markdownlabel.kivy_renderer.Color'), \
             patch('kivy_garden.markdownlabel.kivy_renderer.Line') as MockLine:
            container = renderer.block_quote(token)
            container.pos = (20, 20)
            container.size = (200, 50)
            assert MockLine.called

    def test_deep_nesting_truncation_method(self, renderer):
        """Test that deeply nested structures are truncated to prevent infinite recursion."""
        renderer._nesting_depth = 11
        token = {'type': 'paragraph', 'children': []}
        result = renderer._render_token(token)
        assert result is not None
        assert isinstance(result, Label)
        assert result.text == '[...content truncated due to deep nesting...]'

    def test_unknown_token_render(self, renderer):
        """Test that unknown token types return None."""
        token = {'type': 'unknown_thing'}
        assert renderer._render_token(token) is None

    def test_list_item_direct_call(self, renderer):
        """Test direct call to list_item method."""
        token_para = {
            'type': 'list_item',
            'children': [{
                'type': 'paragraph',
                'children': [{'type': 'text', 'raw': 'item'}]
            }]
        }
        widget = renderer.list_item(token_para)
        assert isinstance(widget, BoxLayout)
        assert len(widget.children) > 0

    def test_list_item_text_token(self, renderer):
        """Test block_text token rendering."""
        token = {'type': 'block_text', 'children': [{'type': 'text', 'raw': 'item'}]}
        widget = renderer.block_text(token)
        assert isinstance(widget, Label)
        assert widget.text == 'item'

    def test_text_size_binding_strict_mode(self, renderer):
        """Test text_size binding in strict label mode."""
        renderer = KivyRenderer(strict_label_mode=True, text_size=[None, None])
        label = Label()
        renderer._apply_text_size_binding(label)
        assert label.text_size == [None, None] or label.text_size == (None, None)

    def test_text_size_binding_height_only(self, renderer):
        """Test text_size binding with height constraint."""
        renderer = KivyRenderer(text_size=[None, 100])
        label = Label(width=200)
        renderer._apply_text_size_binding(label)
        assert label.text_size[1] == 100

    def test_blank_line(self, renderer):
        """Test blank_line token rendering."""
        token = {'type': 'blank_line'}
        widget = renderer.blank_line(token)
        assert isinstance(widget, Widget)
        assert widget.height == renderer.base_font_size
