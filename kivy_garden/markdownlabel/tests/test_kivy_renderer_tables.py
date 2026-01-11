"""
Tests for KivyRenderer table functionality.

This module contains tests that verify table rendering including grid structure,
cell alignment, and table-specific internal rendering logic.
"""

import pytest
from unittest.mock import MagicMock
from hypothesis import given, strategies as st, settings

from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

from kivy_garden.markdownlabel.kivy_renderer import KivyRenderer
from .test_utils import table_token


class TestTableGridStructure:
    """Property tests for table grid structure."""

    @pytest.mark.property
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

    @pytest.mark.property
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

    @pytest.mark.property
    @given(table_token())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_table_returns_gridlayout(self, token):
        """Table tokens produce GridLayout widgets."""
        renderer = KivyRenderer()
        widget = renderer.table(token, None)

        assert isinstance(widget, GridLayout), f"Expected GridLayout, got {type(widget)}"

    @pytest.mark.property
    @given(table_token())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_table_cells_are_labels(self, token):
        """All table cells are Label widgets."""
        renderer = KivyRenderer()
        widget = renderer.table(token, None)

        for child in widget.children:
            assert isinstance(child, Label), f"Expected Label, got {type(child)}"


# *For any* Markdown table cell with specified alignment (left, center, right),
# the corresponding Label widget SHALL have halign set to that alignment value.

class TestTableAlignmentApplication:
    """Property tests for table alignment application."""

    @pytest.mark.parametrize('alignment', ['left', 'center', 'right'])
    def test_cell_alignment_applied(self, alignment):
        """Table cell alignment is applied to Label halign.

        This test directly accesses the private `_render_table_cell` method to
        verify that specific alignment values are correctly applied to the
        resulting Label widget, which is difficult to isolate through the
        public `table` method.
        """
        renderer = KivyRenderer()

        cell_token = {
            'type': 'table_cell',
            'children': [{'type': 'text', 'raw': 'Test'}],
            'attrs': {'align': alignment, 'head': False}
        }

        # Edge case: Testing alignment application requires direct call to
        # _render_table_cell to isolate specific alignment values
        widget = renderer._render_table_cell(cell_token, None, is_head=False)

        assert isinstance(widget, Label), f"Expected Label, got {type(widget)}"
        assert widget.halign == alignment, \
            f"Expected halign='{alignment}', got '{widget.halign}'"

    @pytest.mark.property
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
        """Invalid or missing alignment defaults to 'left'.

        This test directly accesses the private `_render_table_cell` method to
        verify fallback behavior for invalid or missing alignment attributes in
        the token, ensuring robust handling of malformed input.
        """
        renderer = KivyRenderer()

        cell_token = {
            'type': 'table_cell',
            'children': [{'type': 'text', 'raw': 'Test'}],
            'attrs': {'align': alignment, 'head': False}
        }

        # Edge case: Testing fallback behavior requires direct call to
        # _render_table_cell to isolate invalid input handling
        widget = renderer._render_table_cell(cell_token, None, is_head=False)

        assert widget.halign == 'left', \
            f"Expected halign='left' for invalid alignment, got '{widget.halign}'"

    @pytest.mark.property
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


class TestTableEdgeCases:
    """Tests for KivyRenderer table edge cases and internal methods."""

    @pytest.fixture
    def renderer(self):
        """Create a KivyRenderer instance."""
        label = MagicMock()
        label.padding = [10, 10, 10, 10]
        renderer = KivyRenderer(label)
        renderer.base_font_size = 15.0
        return renderer

    def test_table_internals_coverage(self, renderer):
        """Test table internal methods directly to ensure coverage.

        Verifies that table rendering properly handles table_head and
        table_body structures with various alignments.
        """
        # Mock token structure for table
        token = {
            'type': 'table',
            'children': [
                {
                    'type': 'table_head',
                    'children': [
                        {
                            'type': 'table_cell',
                            'children': [{'type': 'text', 'raw': 'H1'}],
                            'attrs': {'align': 'left'}
                        },
                        {
                            'type': 'table_cell',
                            'children': [{'type': 'text', 'raw': 'H2'}],
                            'attrs': {'align': 'center'}
                        }
                    ]
                },
                {
                    'type': 'table_body',
                    'children': [
                        {
                            'type': 'table_row',
                            'children': [
                                {'type': 'table_cell', 'children': [{'type': 'text', 'raw': 'R1C1'}]},
                                {
                                    'type': 'table_cell',
                                    'children': [{'type': 'text', 'raw': 'R1C2'}],
                                    'attrs': {'align': 'right'}
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        # Let's test table rendering
        table_widget = renderer.table(token)
        # Should be GridLayout or similar
        assert table_widget is not None
        assert isinstance(table_widget, GridLayout)

        # Verify cell alignments and header status
        # Note: children are in reverse order of addition
        cells = list(reversed(table_widget.children))

        # Header row
        assert cells[0].text == 'H1'
        assert cells[0].halign == 'left'
        assert cells[0].is_header is True

        assert cells[1].text == 'H2'
        assert cells[1].halign == 'center'
        assert cells[1].is_header is True

        # Body row
        assert cells[2].text == 'R1C1'
        assert cells[2].halign == 'left'  # Default
        assert cells[2].is_header is False

        assert cells[3].text == 'R1C2'
        assert cells[3].halign == 'right'
        assert cells[3].is_header is False
