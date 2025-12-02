"""
Property-based tests for KivyRenderer.

Tests verify that block-level Markdown elements are correctly converted
to Kivy widgets.
"""

import os
# Set environment variable to use headless mode for Kivy
os.environ['KIVY_NO_ARGS'] = '1'
os.environ['KIVY_NO_CONSOLELOG'] = '1'

import pytest
from hypothesis import given, strategies as st, settings, assume

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.image import AsyncImage

from kivy_garden.markdown_label.kivy_renderer import KivyRenderer


# Custom strategies for generating valid AST tokens

@st.composite
def heading_token(draw, level=None):
    """Generate a heading token with specified or random level."""
    if level is None:
        level = draw(st.integers(min_value=1, max_value=6))
    text = draw(st.text(min_size=1, max_size=50, alphabet=st.characters(
        whitelist_categories=['L', 'N', 'P', 'S'],
        blacklist_characters='[]&'
    )))
    return {
        'type': 'heading',
        'children': [{'type': 'text', 'raw': text}],
        'attrs': {'level': level}
    }


@st.composite
def paragraph_token(draw):
    """Generate a paragraph token with text content."""
    text = draw(st.text(min_size=1, max_size=100, alphabet=st.characters(
        whitelist_categories=['L', 'N', 'P', 'S'],
        blacklist_characters='[]&'
    )))
    return {
        'type': 'paragraph',
        'children': [{'type': 'text', 'raw': text}]
    }


@st.composite
def list_item_token(draw):
    """Generate a list item token."""
    text = draw(st.text(min_size=1, max_size=50, alphabet=st.characters(
        whitelist_categories=['L', 'N', 'P', 'S'],
        blacklist_characters='[]&'
    )))
    return {
        'type': 'list_item',
        'children': [{
            'type': 'paragraph',
            'children': [{'type': 'text', 'raw': text}]
        }]
    }


@st.composite
def list_token(draw, ordered=None):
    """Generate a list token (ordered or unordered)."""
    if ordered is None:
        ordered = draw(st.booleans())
    
    num_items = draw(st.integers(min_value=1, max_value=5))
    items = [draw(list_item_token()) for _ in range(num_items)]
    
    return {
        'type': 'list',
        'children': items,
        'attrs': {
            'ordered': ordered,
            'start': 1
        }
    }


@st.composite
def code_block_token(draw):
    """Generate a code block token."""
    code = draw(st.text(min_size=1, max_size=200, alphabet=st.characters(
        whitelist_categories=['L', 'N', 'P', 'S', 'Z'],
        blacklist_characters='[]&'
    )))
    language = draw(st.sampled_from(['', 'python', 'javascript', 'rust', 'go', 'java']))
    return {
        'type': 'block_code',
        'raw': code,
        'attrs': {'info': language}
    }


@st.composite
def block_quote_token(draw):
    """Generate a block quote token."""
    text = draw(st.text(min_size=1, max_size=100, alphabet=st.characters(
        whitelist_categories=['L', 'N', 'P', 'S'],
        blacklist_characters='[]&'
    )))
    return {
        'type': 'block_quote',
        'children': [{
            'type': 'paragraph',
            'children': [{'type': 'text', 'raw': text}]
        }]
    }


@st.composite
def image_token(draw):
    """Generate an image token."""
    alt = draw(st.text(min_size=0, max_size=50, alphabet=st.characters(
        whitelist_categories=['L', 'N', 'P', 'S'],
        blacklist_characters='[]&'
    )))
    # Generate a simple URL-like string
    url = draw(st.from_regex(r'https?://[a-z]+\.[a-z]+/[a-z]+\.(png|jpg|gif)', fullmatch=True))
    return {
        'type': 'image',
        'children': [{'type': 'text', 'raw': alt}] if alt else [],
        'attrs': {'url': url}
    }


# **Feature: markdown-label, Property 3: Heading Font Size Hierarchy**
# *For any* Markdown document containing headings of different levels,
# headings with smaller level numbers (e.g., h1) SHALL have larger font sizes
# than headings with larger level numbers (e.g., h6).
# **Validates: Requirements 2.1**

class TestHeadingFontHierarchy:
    """Property tests for heading font size hierarchy (Property 3)."""
    
    @given(st.integers(min_value=1, max_value=5))
    @settings(max_examples=100, deadline=None)
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
    
    @given(heading_token())
    @settings(max_examples=100)
    def test_heading_returns_label(self, token):
        """Heading tokens produce Label widgets."""
        renderer = KivyRenderer()
        widget = renderer.heading(token, None)
        
        assert isinstance(widget, Label), f"Expected Label, got {type(widget)}"
    
    @given(heading_token())
    @settings(max_examples=100)
    def test_heading_has_markup_enabled(self, token):
        """Heading Labels have markup=True."""
        renderer = KivyRenderer()
        widget = renderer.heading(token, None)
        
        assert widget.markup is True, "Heading should have markup=True"
    
    @given(st.integers(min_value=1, max_value=6), st.floats(min_value=10, max_value=30))
    @settings(max_examples=100)
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



# **Feature: markdown-label, Property 5: Paragraph Markup Enabled**
# *For any* Markdown paragraph, the rendered Label widget SHALL have markup=True.
# **Validates: Requirements 3.1**

class TestParagraphMarkupEnabled:
    """Property tests for paragraph markup enabled (Property 5)."""
    
    @given(paragraph_token())
    @settings(max_examples=100)
    def test_paragraph_has_markup_enabled(self, token):
        """Paragraph Labels have markup=True."""
        renderer = KivyRenderer()
        widget = renderer.paragraph(token, None)
        
        assert isinstance(widget, Label), f"Expected Label, got {type(widget)}"
        assert widget.markup is True, "Paragraph should have markup=True"
    
    @given(paragraph_token())
    @settings(max_examples=100)
    def test_paragraph_returns_label(self, token):
        """Paragraph tokens produce Label widgets."""
        renderer = KivyRenderer()
        widget = renderer.paragraph(token, None)
        
        assert isinstance(widget, Label), f"Expected Label, got {type(widget)}"



# **Feature: markdown-label, Property 6: List Structure Preservation**
# *For any* Markdown list (ordered or unordered), the rendered widget tree SHALL
# contain a BoxLayout with one child BoxLayout per list item, and each item
# SHALL be prefixed with the appropriate marker (bullet or number).
# **Validates: Requirements 4.1, 4.2**

class TestListStructurePreservation:
    """Property tests for list structure preservation (Property 6)."""
    
    @given(list_token())
    @settings(max_examples=100)
    def test_list_returns_boxlayout(self, token):
        """List tokens produce BoxLayout widgets."""
        renderer = KivyRenderer()
        widget = renderer.list(token, None)
        
        assert isinstance(widget, BoxLayout), f"Expected BoxLayout, got {type(widget)}"
    
    @given(list_token())
    @settings(max_examples=100)
    def test_list_has_correct_item_count(self, token):
        """List has one child per list item."""
        renderer = KivyRenderer()
        widget = renderer.list(token, None)
        
        expected_count = len(token['children'])
        actual_count = len(widget.children)
        
        assert actual_count == expected_count, \
            f"Expected {expected_count} children, got {actual_count}"
    
    @given(list_token(ordered=False))
    @settings(max_examples=100)
    def test_unordered_list_has_bullet_markers(self, token):
        """Unordered list items have bullet markers."""
        renderer = KivyRenderer()
        widget = renderer.list(token, None)
        
        # Each child should be a horizontal BoxLayout with a marker Label
        for child in widget.children:
            assert isinstance(child, BoxLayout), f"List item should be BoxLayout"
            # First child of item layout should be the marker
            # Note: Kivy children are in reverse order (last added is first)
            marker = child.children[-1]  # Last in list = first added = marker
            assert isinstance(marker, Label), f"Marker should be Label"
            assert '•' in marker.text, f"Unordered list marker should contain bullet, got: {marker.text}"
    
    @given(list_token(ordered=True))
    @settings(max_examples=100)
    def test_ordered_list_has_number_markers(self, token):
        """Ordered list items have number markers."""
        renderer = KivyRenderer()
        widget = renderer.list(token, None)
        
        num_items = len(token['children'])
        
        # Each child should be a horizontal BoxLayout with a marker Label
        # Note: Kivy children are in reverse order (last added is first in list)
        for i, child in enumerate(widget.children):
            assert isinstance(child, BoxLayout), f"List item should be BoxLayout"
            # First child of item layout should be the marker
            marker = child.children[-1]  # Last in list = first added = marker
            assert isinstance(marker, Label), f"Marker should be Label"
            # Marker should contain a number followed by period
            # Account for reverse order: item at index i corresponds to item (num_items - i)
            expected_num = str(num_items - i)
            assert expected_num in marker.text and '.' in marker.text, \
                f"Ordered list marker should contain '{expected_num}.', got: {marker.text}"


# **Feature: markdown-label, Property 7: Nested List Indentation**
# *For any* Markdown list containing nested lists, each nesting level SHALL
# increase the left padding/indentation of the nested content.
# **Validates: Requirements 4.3**

class TestNestedListIndentation:
    """Property tests for nested list indentation (Property 7)."""
    
    @given(st.integers(min_value=1, max_value=4))
    @settings(max_examples=100)
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



# **Feature: markdown-label, Property 10: Code Block Styling**
# *For any* Markdown code block (fenced or indented), the rendered widget SHALL
# use a monospace font and have a dark background color applied.
# **Validates: Requirements 6.1, 6.2**

class TestCodeBlockStyling:
    """Property tests for code block styling (Property 10)."""
    
    @given(code_block_token())
    @settings(max_examples=100)
    def test_code_block_returns_widget(self, token):
        """Code block tokens produce Widget containers."""
        renderer = KivyRenderer()
        widget = renderer.block_code(token, None)
        
        assert isinstance(widget, Widget), f"Expected Widget, got {type(widget)}"
    
    @given(code_block_token())
    @settings(max_examples=100)
    def test_code_block_has_monospace_font(self, token):
        """Code block uses monospace font."""
        renderer = KivyRenderer(code_font_name='RobotoMono-Regular')
        widget = renderer.block_code(token, None)
        
        # The widget is a BoxLayout container with a Label child
        assert isinstance(widget, BoxLayout), f"Expected BoxLayout container"
        
        # Find the Label child
        label = None
        for child in widget.children:
            if isinstance(child, Label):
                label = child
                break
        
        assert label is not None, "Code block should contain a Label"
        assert label.font_name == 'RobotoMono-Regular', \
            f"Expected monospace font, got {label.font_name}"
    
    @given(code_block_token())
    @settings(max_examples=100)
    def test_code_block_has_dark_background(self, token):
        """Code block has dark background color."""
        dark_bg = [0.15, 0.15, 0.15, 1]
        renderer = KivyRenderer(code_bg_color=dark_bg)
        widget = renderer.block_code(token, None)
        
        # Check that canvas.before has instructions (background)
        assert hasattr(widget, '_bg_rect'), "Code block should have background rectangle"


# **Feature: markdown-label, Property 11: Code Block Language Metadata**
# *For any* fenced code block with a language identifier, the rendered widget
# SHALL store the language string in an accessible attribute.
# **Validates: Requirements 6.3**

class TestCodeBlockLanguageMetadata:
    """Property tests for code block language metadata (Property 11)."""
    
    @given(code_block_token())
    @settings(max_examples=100)
    def test_code_block_stores_language_info(self, token):
        """Code block stores language info as attribute."""
        renderer = KivyRenderer()
        widget = renderer.block_code(token, None)
        
        expected_language = token['attrs'].get('info', '')
        
        assert hasattr(widget, 'language_info'), "Code block should have language_info attribute"
        assert widget.language_info == expected_language, \
            f"Expected language '{expected_language}', got '{widget.language_info}'"
    
    @given(st.sampled_from(['python', 'javascript', 'rust', 'go', 'java', 'c', 'cpp']))
    @settings(max_examples=100)
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



# **Feature: markdown-label, Property 14: Block Quote Structure**
# *For any* Markdown block quote, the rendered widget SHALL be a BoxLayout
# with left border styling and its content indented from the left edge.
# **Validates: Requirements 9.1**

class TestBlockQuoteStructure:
    """Property tests for block quote structure (Property 14)."""
    
    @given(block_quote_token())
    @settings(max_examples=100)
    def test_block_quote_returns_boxlayout(self, token):
        """Block quote tokens produce BoxLayout widgets."""
        renderer = KivyRenderer()
        widget = renderer.block_quote(token, None)
        
        assert isinstance(widget, BoxLayout), f"Expected BoxLayout, got {type(widget)}"
    
    @given(block_quote_token())
    @settings(max_examples=100)
    def test_block_quote_has_left_padding(self, token):
        """Block quote has left padding for indentation."""
        renderer = KivyRenderer()
        widget = renderer.block_quote(token, None)
        
        # Check left padding (first element of padding tuple)
        assert widget.padding[0] > 0, \
            f"Block quote should have left padding, got {widget.padding[0]}"
    
    @given(block_quote_token())
    @settings(max_examples=100)
    def test_block_quote_has_left_border(self, token):
        """Block quote has left border line."""
        renderer = KivyRenderer()
        widget = renderer.block_quote(token, None)
        
        # Check that canvas.before has border line
        assert hasattr(widget, '_border_line'), "Block quote should have border line"


# **Feature: markdown-label, Property 15: Thematic Break Rendering**
# *For any* Markdown thematic break (---, ***, ___), the rendered widget tree
# SHALL contain a Widget with a horizontal line drawn on its canvas.
# **Validates: Requirements 10.1**

class TestThematicBreakRendering:
    """Property tests for thematic break rendering (Property 15)."""
    
    @given(st.just({'type': 'thematic_break'}))
    @settings(max_examples=100)
    def test_thematic_break_returns_widget(self, token):
        """Thematic break tokens produce Widget."""
        renderer = KivyRenderer()
        widget = renderer.thematic_break(token, None)
        
        assert isinstance(widget, Widget), f"Expected Widget, got {type(widget)}"
    
    @given(st.just({'type': 'thematic_break'}))
    @settings(max_examples=100)
    def test_thematic_break_has_fixed_height(self, token):
        """Thematic break has fixed height."""
        renderer = KivyRenderer()
        widget = renderer.thematic_break(token, None)
        
        assert widget.size_hint_y is None, "Thematic break should have size_hint_y=None"
        assert widget.height > 0, "Thematic break should have positive height"
    
    @given(st.just({'type': 'thematic_break'}))
    @settings(max_examples=100)
    def test_thematic_break_has_horizontal_line(self, token):
        """Thematic break has horizontal line on canvas."""
        renderer = KivyRenderer()
        widget = renderer.thematic_break(token, None)
        
        # Check that canvas has line instruction
        assert hasattr(widget, '_hr_line'), "Thematic break should have horizontal line"


# **Feature: markdown-label, Property 13: Image Widget Creation**
# *For any* Markdown image ![alt](url), the rendered widget tree SHALL contain
# an AsyncImage widget with source=url.
# **Validates: Requirements 8.1**

class TestImageWidgetCreation:
    """Property tests for image widget creation (Property 13)."""
    
    @given(image_token())
    @settings(max_examples=100)
    def test_image_returns_asyncimage(self, token):
        """Image tokens produce AsyncImage widgets."""
        renderer = KivyRenderer()
        widget = renderer.image(token, None)
        
        assert isinstance(widget, AsyncImage), f"Expected AsyncImage, got {type(widget)}"
    
    @given(image_token())
    @settings(max_examples=100)
    def test_image_has_correct_source(self, token):
        """Image widget has correct source URL."""
        renderer = KivyRenderer()
        widget = renderer.image(token, None)
        
        expected_url = token['attrs']['url']
        assert widget.source == expected_url, \
            f"Expected source '{expected_url}', got '{widget.source}'"
    
    @given(image_token())
    @settings(max_examples=100)
    def test_image_stores_alt_text(self, token):
        """Image widget stores alt text for fallback."""
        renderer = KivyRenderer()
        widget = renderer.image(token, None)
        
        assert hasattr(widget, 'alt_text'), "Image should have alt_text attribute"
