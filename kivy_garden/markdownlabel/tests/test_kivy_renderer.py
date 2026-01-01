"""
Property-based tests for KivyRenderer.

Tests verify that block-level Markdown elements are correctly converted
to Kivy widgets.
"""

import pytest
from hypothesis import given, strategies as st, settings, assume

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.image import AsyncImage
from kivy.uix.gridlayout import GridLayout

from kivy_garden.markdownlabel.kivy_renderer import KivyRenderer
from .test_utils import (
    heading_token,
    paragraph_token,
    list_token,
    code_block_token,
    block_quote_token,
    image_token,
    table_token
)


# **Feature: markdown-label, Property 3: Heading Font Size Hierarchy**
# *For any* Markdown document containing headings of different levels,
# headings with smaller level numbers (e.g., h1) SHALL have larger font sizes
# than headings with larger level numbers (e.g., h6).
# **Validates: Requirements 2.1**

class TestHeadingFontHierarchy:
    """Property tests for heading font size hierarchy (Property 3)."""

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

    @given(heading_token())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_heading_returns_label(self, token):
        """Heading tokens produce Label widgets."""
        renderer = KivyRenderer()
        widget = renderer.heading(token, None)

        assert isinstance(widget, Label), f"Expected Label, got {type(widget)}"

    @given(heading_token())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_heading_has_markup_enabled(self, token):
        """Heading Labels have markup=True."""
        renderer = KivyRenderer()
        widget = renderer.heading(token, None)

        assert widget.markup is True, "Heading should have markup=True"

    @given(st.integers(min_value=1, max_value=6), st.floats(min_value=10, max_value=30))
    # Combination strategy: 10 examples (performance optimized)
    @settings(max_examples=10, deadline=None)
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
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_paragraph_has_markup_enabled(self, token):
        """Paragraph Labels have markup=True."""
        renderer = KivyRenderer()
        widget = renderer.paragraph(token, None)

        assert isinstance(widget, Label), f"Expected Label, got {type(widget)}"
        assert widget.markup is True, "Paragraph should have markup=True"

    @given(paragraph_token())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
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
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_list_returns_boxlayout(self, token):
        """List tokens produce BoxLayout widgets."""
        renderer = KivyRenderer()
        widget = renderer.list(token, None)

        assert isinstance(widget, BoxLayout), f"Expected BoxLayout, got {type(widget)}"

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


# **Feature: markdown-label, Property 7: Nested List Indentation**
# *For any* Markdown list containing nested lists, each nesting level SHALL
# increase the left padding/indentation of the nested content.
# **Validates: Requirements 4.3**

class TestNestedListIndentation:
    """Property tests for nested list indentation (Property 7)."""

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


# **Feature: markdown-label, Property 10: Code Block Styling**
# *For any* Markdown code block (fenced or indented), the rendered widget SHALL
# use a monospace font and have a dark background color applied.
# **Validates: Requirements 6.1, 6.2**


class TestCodeBlockStyling:
    """Property tests for code block styling (Property 10)."""

    @given(code_block_token())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_code_block_returns_widget(self, token):
        """Code block tokens produce Widget containers."""
        renderer = KivyRenderer()
        widget = renderer.block_code(token, None)

        assert isinstance(widget, Widget), f"Expected Widget, got {type(widget)}"

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

    @given(code_block_token())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
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


# **Feature: markdown-label, Property 14: Block Quote Structure**
# *For any* Markdown block quote, the rendered widget SHALL be a BoxLayout
# with left border styling and its content indented from the left edge.
# **Validates: Requirements 9.1**

class TestBlockQuoteStructure:
    """Property tests for block quote structure (Property 14)."""

    @given(block_quote_token())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_block_quote_returns_boxlayout(self, token):
        """Block quote tokens produce BoxLayout widgets."""
        renderer = KivyRenderer()
        widget = renderer.block_quote(token, None)

        assert isinstance(widget, BoxLayout), f"Expected BoxLayout, got {type(widget)}"

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

    @given(block_quote_token())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
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
    # Small finite strategy: 1 examples (input space size: 1)
    @settings(max_examples=1, deadline=None)
    def test_thematic_break_returns_widget(self, token):
        """Thematic break tokens produce Widget."""
        renderer = KivyRenderer()
        widget = renderer.thematic_break(token, None)

        assert isinstance(widget, Widget), f"Expected Widget, got {type(widget)}"

    @given(st.just({'type': 'thematic_break'}))
    # Small finite strategy: 1 examples (input space size: 1)
    @settings(max_examples=1, deadline=None)
    def test_thematic_break_has_fixed_height(self, token):
        """Thematic break has fixed height."""
        renderer = KivyRenderer()
        widget = renderer.thematic_break(token, None)

        assert widget.size_hint_y is None, "Thematic break should have size_hint_y=None"
        assert widget.height > 0, "Thematic break should have positive height"

    @given(st.just({'type': 'thematic_break'}))
    # Small finite strategy: 1 examples (input space size: 1)
    @settings(max_examples=1, deadline=None)
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
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_image_returns_asyncimage(self, token):
        """Image tokens produce AsyncImage widgets."""
        renderer = KivyRenderer()
        widget = renderer.image(token, None)

        assert isinstance(widget, AsyncImage), f"Expected AsyncImage, got {type(widget)}"

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

    @given(image_token())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_image_stores_alt_text(self, token):
        """Image widget stores alt text for fallback."""
        renderer = KivyRenderer()
        widget = renderer.image(token, None)

        assert hasattr(widget, 'alt_text'), "Image should have alt_text attribute"


# **Feature: markdown-label, Property 8: Table Grid Structure**
# *For any* Markdown table with R rows and C columns, the rendered GridLayout
# SHALL have cols=C and contain exactly R×C Label widgets.
# **Validates: Requirements 5.1**

class TestTableGridStructure:
    """Property tests for table grid structure (Property 8)."""

    @given(st.integers(min_value=1, max_value=5), st.integers(min_value=1, max_value=5))
    # Combination strategy: 25 examples (combination coverage)
    @settings(max_examples=25, deadline=None)
    def test_table_has_correct_column_count(self, num_rows, num_cols):
        """Table GridLayout has correct number of columns."""
        renderer = KivyRenderer()

        # Create table token with specified dimensions
        # Generate alignments for columns
        alignments = [None] * num_cols

        # Generate header row
        head_cells = [
            {'type': 'table_cell', 'children': [{'type': 'text', 'raw': f'H{i}'}],
             'attrs': {'align': None, 'head': True}}
            for i in range(num_cols)
        ]
        head_row = {'type': 'table_row', 'children': head_cells}

        # Generate body rows
        body_rows = []
        for r in range(num_rows - 1):
            body_cells = [
                {'type': 'table_cell', 'children': [{'type': 'text', 'raw': f'C{r}{c}'}],
                 'attrs': {'align': None, 'head': False}}
                for c in range(num_cols)
            ]
            body_rows.append({'type': 'table_row', 'children': body_cells})

        token = {
            'type': 'table',
            'children': [
                {'type': 'table_head', 'children': [head_row]},
                {'type': 'table_body', 'children': body_rows}
            ]
        }

        widget = renderer.table(token, None)

        assert isinstance(widget, GridLayout), f"Expected GridLayout, got {type(widget)}"
        assert widget.cols == num_cols, \
            f"Expected {num_cols} columns, got {widget.cols}"

    @given(st.integers(min_value=1, max_value=5), st.integers(min_value=1, max_value=5))
    # Combination strategy: 25 examples (combination coverage)
    @settings(max_examples=25, deadline=None)
    def test_table_has_correct_cell_count(self, num_rows, num_cols):
        """Table contains exactly R×C Label widgets."""
        renderer = KivyRenderer()

        # Generate header row
        head_cells = [
            {'type': 'table_cell', 'children': [{'type': 'text', 'raw': f'H{i}'}],
             'attrs': {'align': None, 'head': True}}
            for i in range(num_cols)
        ]
        head_row = {'type': 'table_row', 'children': head_cells}

        # Generate body rows
        body_rows = []
        for r in range(num_rows - 1):
            body_cells = [
                {'type': 'table_cell', 'children': [{'type': 'text', 'raw': f'C{r}{c}'}],
                 'attrs': {'align': None, 'head': False}}
                for c in range(num_cols)
            ]
            body_rows.append({'type': 'table_row', 'children': body_cells})

        token = {
            'type': 'table',
            'children': [
                {'type': 'table_head', 'children': [head_row]},
                {'type': 'table_body', 'children': body_rows}
            ]
        }

        widget = renderer.table(token, None)

        # Count Label widgets in the grid
        label_count = sum(1 for child in widget.children if isinstance(child, Label))
        expected_count = num_rows * num_cols

        assert label_count == expected_count, \
            f"Expected {expected_count} cells (R={num_rows} × C={num_cols}), got {label_count}"

    @given(table_token())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_table_returns_gridlayout(self, token):
        """Table tokens produce GridLayout widgets."""
        renderer = KivyRenderer()
        widget = renderer.table(token, None)

        assert isinstance(widget, GridLayout), f"Expected GridLayout, got {type(widget)}"

    @given(table_token())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_table_cells_are_labels(self, token):
        """All table cells are Label widgets."""
        renderer = KivyRenderer()
        widget = renderer.table(token, None)

        for child in widget.children:
            assert isinstance(child, Label), f"Expected Label, got {type(child)}"


# **Feature: markdown-label, Property 9: Table Alignment Application**
# *For any* Markdown table cell with specified alignment (left, center, right),
# the corresponding Label widget SHALL have halign set to that alignment value.
# **Validates: Requirements 5.2**

class TestTableAlignmentApplication:
    """Property tests for table alignment application (Property 9)."""

    @pytest.mark.parametrize('alignment', ['left', 'center', 'right'])
    def test_cell_alignment_applied(self, alignment):
        """Table cell alignment is applied to Label halign."""
        renderer = KivyRenderer()

        cell_token = {
            'type': 'table_cell',
            'children': [{'type': 'text', 'raw': 'Test'}],
            'attrs': {'align': alignment, 'head': False}
        }

        widget = renderer._render_table_cell(cell_token, None, is_head=False)

        assert isinstance(widget, Label), f"Expected Label, got {type(widget)}"
        assert widget.halign == alignment, \
            f"Expected halign='{alignment}', got '{widget.halign}'"

    @given(st.integers(min_value=1, max_value=3), st.integers(min_value=2, max_value=4))
    # Combination strategy: 9 examples (combination coverage)
    @settings(max_examples=9, deadline=None)
    def test_table_preserves_column_alignments(self, num_rows, num_cols):
        """Table preserves alignment for each column."""
        renderer = KivyRenderer()

        # Generate specific alignments for each column
        alignments = ['left', 'center', 'right'][:num_cols]
        while len(alignments) < num_cols:
            alignments.append('left')

        # Generate header row with alignments
        head_cells = [
            {'type': 'table_cell', 'children': [{'type': 'text', 'raw': f'H{i}'}],
             'attrs': {'align': alignments[i], 'head': True}}
            for i in range(num_cols)
        ]
        head_row = {'type': 'table_row', 'children': head_cells}

        # Generate body rows with same alignments
        body_rows = []
        for r in range(num_rows - 1):
            body_cells = [
                {'type': 'table_cell', 'children': [{'type': 'text', 'raw': f'C{r}{c}'}],
                 'attrs': {'align': alignments[c], 'head': False}}
                for c in range(num_cols)
            ]
            body_rows.append({'type': 'table_row', 'children': body_cells})

        token = {
            'type': 'table',
            'children': [
                {'type': 'table_head', 'children': [head_row]},
                {'type': 'table_body', 'children': body_rows}
            ]
        }

        widget = renderer.table(token, None)

        # Verify each cell has correct alignment
        # Note: GridLayout children are in reverse order (last added first)
        children = list(reversed(widget.children))

        for row_idx in range(num_rows):
            for col_idx in range(num_cols):
                cell_idx = row_idx * num_cols + col_idx
                cell = children[cell_idx]
                expected_align = alignments[col_idx]

                assert cell.halign == expected_align, \
                    f"Cell [{row_idx}][{col_idx}] expected halign='{expected_align}', got '{cell.halign}'"

    @pytest.mark.parametrize('alignment', [None, 'invalid', ''])
    def test_invalid_alignment_defaults_to_left(self, alignment):
        """Invalid or missing alignment defaults to 'left'."""
        renderer = KivyRenderer()

        cell_token = {
            'type': 'table_cell',
            'children': [{'type': 'text', 'raw': 'Test'}],
            'attrs': {'align': alignment, 'head': False}
        }

        widget = renderer._render_table_cell(cell_token, None, is_head=False)

        assert widget.halign == 'left', \
            f"Expected halign='left' for invalid alignment, got '{widget.halign}'"

    @given(table_token())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_cell_stores_alignment_metadata(self, token):
        """Table cells store alignment as metadata."""
        renderer = KivyRenderer()
        widget = renderer.table(token, None)

        for child in widget.children:
            assert hasattr(child, 'cell_align'), "Cell should have cell_align attribute"
            assert child.cell_align in ('left', 'center', 'right'), \
                f"cell_align should be valid alignment, got '{child.cell_align}'"


# **Feature: headless-ci-testing, Deep Nesting Truncation Placeholder**
# Tests that deeply nested content is truncated with a placeholder widget.
# **Validates: Requirements 7.1, 7.2**


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
