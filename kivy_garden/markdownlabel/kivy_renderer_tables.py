"""
KivyRenderer Table Support
==========================

Table rendering functionality for KivyRenderer as a mixin class.
"""

from typing import Any, Dict

from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label


class KivyRendererTableMixin:
    """Mixin class providing table rendering functionality for KivyRenderer."""

    def table(self, token: Dict[str, Any], state: Any = None) -> GridLayout:
        """Render a table as a GridLayout with bottom spacing.

        Args:
            token: Table token with 'children' containing head and body
            state: Block state

        Returns:
            GridLayout containing table cells
        """
        children = token.get('children', [])

        # Determine number of columns from the first row
        num_cols = self._get_table_column_count(token)

        # Create GridLayout with correct number of columns and bottom padding
        grid = GridLayout(
            cols=num_cols,
            size_hint_y=None,
            spacing=[2, 2],
            padding=[5, 5, 5, 5 + self.base_font_size]  # Add bottom spacing via padding
        )
        grid.bind(minimum_height=grid.setter('height'))

        # Process table head and body
        for child in children:
            child_type = child.get('type', '')
            if child_type == 'table_head':
                self._render_table_section(child, grid, state, is_head=True)
            elif child_type == 'table_body':
                self._render_table_section(child, grid, state, is_head=False)

        return grid

    def _get_table_column_count(self, token: Dict[str, Any]) -> int:
        """Get the number of columns in a table.

        Args:
            token: Table token

        Returns:
            Number of columns
        """
        children = token.get('children', [])
        for child in children:
            child_type = child.get('type', '')
            if child_type in ('table_head', 'table_body'):
                rows = child.get('children', [])
                if rows:
                    first_item = rows[0]
                    # table_head has direct table_cell children
                    # table_body has table_row children which contain table_cell children
                    if first_item.get('type') == 'table_cell':
                        return len(rows)
                    elif first_item.get('type') == 'table_row':
                        cells = first_item.get('children', [])
                        return len(cells)
        return 1  # Default to 1 column if structure is unclear

    def _render_table_section(self, section: Dict[str, Any], grid: GridLayout,
                               state: Any, is_head: bool = False) -> None:
        """Render a table section (head or body) into the grid.

        Args:
            section: Table head or body token
            grid: GridLayout to add cells to
            state: Block state
            is_head: Whether this is the header section
        """
        children = section.get('children', [])
        if not children:
            return

        # Check if children are table_cell (table_head) or table_row (table_body)
        first_child_type = children[0].get('type', '')

        if first_child_type == 'table_cell':
            # table_head: direct table_cell children
            for cell in children:
                cell_widget = self._render_table_cell(cell, state, is_head)
                grid.add_widget(cell_widget)
        elif first_child_type == 'table_row':
            # table_body: table_row children containing table_cell children
            for row in children:
                self._render_table_row(row, grid, state, is_head)

    def _render_table_row(self, row: Dict[str, Any], grid: GridLayout,
                          state: Any, is_head: bool = False) -> None:
        """Render a table row into the grid.

        Args:
            row: Table row token
            grid: GridLayout to add cells to
            state: Block state
            is_head: Whether this row is in the header
        """
        cells = row.get('children', [])
        for cell in cells:
            cell_widget = self._render_table_cell(cell, state, is_head)
            grid.add_widget(cell_widget)

    def _render_table_cell(self, cell: Dict[str, Any], state: Any,
                           is_head: bool = False) -> Label:
        """Render a table cell as a Label.

        Args:
            cell: Table cell token
            state: Block state
            is_head: Whether this cell is in the header

        Returns:
            Label widget for the cell
        """
        children = cell.get('children', [])
        attrs = cell.get('attrs', {})

        # Get alignment from attrs - table cells use their own alignment from markdown
        # but fall back to the renderer's halign if not specified or invalid
        align = attrs.get('align', None)
        if align in ('left', 'center', 'right'):
            cell_halign = align
        else:
            # Fall back to renderer's halign, but convert 'auto' to 'left' for table cells
            cell_halign = 'left' if self.halign == 'auto' else self.halign

        # Render inline content
        text = self._render_inline(children) if children else ''

        # Create label with appropriate styling
        label_kwargs = self._build_label_kwargs(
            text=text,
            font_size=self.base_font_size,
            halign=cell_halign,
            bold=is_head,
            size_hint_y=None,
            size_hint_x=1,
        )

        label = Label(**label_kwargs)

        # Store alignment as metadata
        label.cell_align = cell_halign
        label.is_header = is_head

        # Set font scale metadata for table cells
        label._font_scale = 1.0

        return label

    def table_head(self, token: Dict[str, Any], state: Any = None) -> None:
        """Handle table_head token (processed by table()).

        This method exists for completeness but table_head is typically
        processed as part of the table() method.

        Args:
            token: Table head token
            state: Block state

        Returns:
            None (processed by parent table)
        """
        return None

    def table_body(self, token: Dict[str, Any], state: Any = None) -> None:
        """Handle table_body token (processed by table()).

        This method exists for completeness but table_body is typically
        processed as part of the table() method.

        Args:
            token: Table body token
            state: Block state

        Returns:
            None (processed by parent table)
        """
        return None

    def table_row(self, token: Dict[str, Any], state: Any = None) -> None:
        """Handle table_row token (processed by table()).

        This method exists for completeness but table_row is typically
        processed as part of the table() method.

        Args:
            token: Table row token
            state: Block state

        Returns:
            None (processed by parent table)
        """
        return None

    def table_cell(self, token: Dict[str, Any], state: Any = None) -> Label:
        """Handle table_cell token directly.

        This method can be called directly if needed, but cells are typically
        processed as part of the table() method.

        Args:
            token: Table cell token
            state: Block state

        Returns:
            Label widget for the cell
        """
        return self._render_table_cell(token, state, is_head=False)
