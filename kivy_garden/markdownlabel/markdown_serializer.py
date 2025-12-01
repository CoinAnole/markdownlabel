"""
MarkdownSerializer
==================

Serializes mistune AST tokens back to Markdown text for round-trip testing.
"""

from typing import Any, Dict, List


class MarkdownSerializer:
    """Serializes AST tokens back to Markdown text.
    
    This serializer converts mistune AST tokens back to Markdown string
    representation, enabling round-trip testing to verify parsing correctness.
    """
    
    def __init__(self):
        """Initialize the MarkdownSerializer."""
        pass
    
    def serialize(self, tokens: List[Dict[str, Any]]) -> str:
        """Convert AST tokens to Markdown string.
        
        Args:
            tokens: List of AST tokens from mistune
            
        Returns:
            Markdown string representation
        """
        result = []
        for i, token in enumerate(tokens):
            serialized = self._serialize_token(token)
            if serialized is not None:
                result.append(serialized)
        
        return '\n\n'.join(result)
    
    def _serialize_token(self, token: Dict[str, Any]) -> str:
        """Serialize a single token to Markdown.
        
        Args:
            token: AST token dictionary
            
        Returns:
            Markdown string or None
        """
        token_type = token.get('type', '')
        method = getattr(self, token_type, None)
        
        if method is not None:
            return method(token)
        
        # Unknown token type - return empty string
        return ''
    
    def serialize_inline(self, children: List[Dict[str, Any]]) -> str:
        """Serialize inline tokens to Markdown string.
        
        Args:
            children: List of inline tokens
            
        Returns:
            Markdown string
        """
        result = []
        for token in children:
            token_type = token.get('type', 'text')
            method = getattr(self, f'inline_{token_type}', None)
            if method is not None:
                result.append(method(token))
            else:
                # Fallback to raw text
                result.append(token.get('raw', ''))
        return ''.join(result)

    
    # Block-level serializers
    
    def paragraph(self, token: Dict[str, Any]) -> str:
        """Serialize a paragraph token.
        
        Args:
            token: Paragraph token with 'children'
            
        Returns:
            Markdown paragraph text
        """
        children = token.get('children', [])
        return self.serialize_inline(children)
    
    def heading(self, token: Dict[str, Any]) -> str:
        """Serialize a heading token.
        
        Args:
            token: Heading token with 'children' and 'attrs'
            
        Returns:
            Markdown heading (e.g., '# Heading')
        """
        children = token.get('children', [])
        attrs = token.get('attrs', {})
        level = attrs.get('level', 1)
        
        text = self.serialize_inline(children)
        return '#' * level + ' ' + text
    
    def list(self, token: Dict[str, Any]) -> str:
        """Serialize a list token.
        
        Args:
            token: List token with 'children' and 'attrs'
            
        Returns:
            Markdown list
        """
        attrs = token.get('attrs', {})
        ordered = attrs.get('ordered', False)
        start = attrs.get('start', 1)
        children = token.get('children', [])
        
        items = []
        for i, child in enumerate(children):
            item_text = self._serialize_list_item(child)
            if ordered:
                marker = f'{start + i}.'
            else:
                marker = '-'
            items.append(f'{marker} {item_text}')
        
        return '\n'.join(items)
    
    def _serialize_list_item(self, token: Dict[str, Any]) -> str:
        """Serialize a list item token.
        
        Args:
            token: List item token with 'children'
            
        Returns:
            List item content
        """
        children = token.get('children', [])
        parts = []
        
        for child in children:
            child_type = child.get('type', '')
            if child_type == 'paragraph':
                parts.append(self.paragraph(child))
            elif child_type == 'block_text':
                # block_text is used for tight list items
                parts.append(self.block_text(child))
            elif child_type == 'list':
                # Nested list - indent each line
                nested = self.list(child)
                indented = '\n'.join('  ' + line for line in nested.split('\n'))
                parts.append('\n' + indented)
            else:
                serialized = self._serialize_token(child)
                if serialized:
                    parts.append(serialized)
        
        return ''.join(parts)
    
    def block_text(self, token: Dict[str, Any]) -> str:
        """Serialize a block_text token (used in tight lists).
        
        Args:
            token: Block text token with 'children'
            
        Returns:
            Inline text content
        """
        children = token.get('children', [])
        return self.serialize_inline(children)
    
    def block_code(self, token: Dict[str, Any]) -> str:
        """Serialize a code block token.
        
        Args:
            token: Code block token with 'raw' and optional 'attrs'
            
        Returns:
            Markdown fenced code block
        """
        raw = token.get('raw', '')
        attrs = token.get('attrs', {})
        language = attrs.get('info', '')
        
        # Use fenced code block format
        fence = '```'
        return f'{fence}{language}\n{raw}{fence}'
    
    def block_quote(self, token: Dict[str, Any]) -> str:
        """Serialize a block quote token.
        
        Args:
            token: Block quote token with 'children'
            
        Returns:
            Markdown block quote
        """
        children = token.get('children', [])
        
        # Serialize children and prefix each line with >
        inner_parts = []
        for child in children:
            serialized = self._serialize_token(child)
            if serialized:
                inner_parts.append(serialized)
        
        inner_text = '\n\n'.join(inner_parts)
        
        # Prefix each line with >
        lines = inner_text.split('\n')
        quoted_lines = ['> ' + line for line in lines]
        return '\n'.join(quoted_lines)
    
    def thematic_break(self, token: Dict[str, Any]) -> str:
        """Serialize a thematic break token.
        
        Args:
            token: Thematic break token
            
        Returns:
            Markdown horizontal rule
        """
        return '---'
    
    def blank_line(self, token: Dict[str, Any]) -> str:
        """Serialize a blank line token.
        
        Args:
            token: Blank line token
            
        Returns:
            Empty string (blank lines are handled by join)
        """
        return None  # Skip blank lines in output

    
    def table(self, token: Dict[str, Any]) -> str:
        """Serialize a table token.
        
        Args:
            token: Table token with 'children' containing head and body
            
        Returns:
            Markdown table
        """
        children = token.get('children', [])
        
        rows = []
        alignments = []
        
        for child in children:
            child_type = child.get('type', '')
            if child_type == 'table_head':
                head_rows, alignments = self._serialize_table_head(child)
                rows.extend(head_rows)
            elif child_type == 'table_body':
                body_rows = self._serialize_table_body(child)
                rows.extend(body_rows)
        
        return '\n'.join(rows)
    
    def _serialize_table_head(self, token: Dict[str, Any]) -> tuple:
        """Serialize table head and return rows with alignments.
        
        Args:
            token: Table head token
            
        Returns:
            Tuple of (rows list, alignments list)
        """
        children = token.get('children', [])
        rows = []
        alignments = []
        cell_texts = []
        
        # In mistune, table_head children are directly the cells (no row wrapper)
        for cell in children:
            cell_type = cell.get('type', '')
            if cell_type == 'table_cell':
                cell_children = cell.get('children', [])
                cell_text = self.serialize_inline(cell_children)
                cell_texts.append(cell_text)
                
                # Get alignment from cell attrs
                attrs = cell.get('attrs', {})
                align = attrs.get('align', None)
                alignments.append(align)
            elif cell_type == 'table_row':
                # Handle case where there's a row wrapper
                row_cells = cell.get('children', [])
                for row_cell in row_cells:
                    cell_children = row_cell.get('children', [])
                    cell_text = self.serialize_inline(cell_children)
                    cell_texts.append(cell_text)
                    
                    attrs = row_cell.get('attrs', {})
                    align = attrs.get('align', None)
                    alignments.append(align)
        
        if cell_texts:
            rows.append('| ' + ' | '.join(cell_texts) + ' |')
        
        # Add separator row with alignment markers
        separator_cells = []
        for align in alignments:
            if align == 'left':
                separator_cells.append(':---')
            elif align == 'center':
                separator_cells.append(':---:')
            elif align == 'right':
                separator_cells.append('---:')
            else:
                separator_cells.append('---')
        
        if separator_cells:
            rows.append('| ' + ' | '.join(separator_cells) + ' |')
        
        return rows, alignments
    
    def _serialize_table_body(self, token: Dict[str, Any]) -> List[str]:
        """Serialize table body rows.
        
        Args:
            token: Table body token
            
        Returns:
            List of row strings
        """
        children = token.get('children', [])
        rows = []
        
        for row in children:
            cells = row.get('children', [])
            cell_texts = []
            
            for cell in cells:
                cell_children = cell.get('children', [])
                cell_text = self.serialize_inline(cell_children)
                cell_texts.append(cell_text)
            
            rows.append('| ' + ' | '.join(cell_texts) + ' |')
        
        return rows
    
    # Inline serializers
    
    def inline_text(self, token: Dict[str, Any]) -> str:
        """Serialize plain text token.
        
        Args:
            token: Text token with 'raw'
            
        Returns:
            Plain text
        """
        return token.get('raw', '')
    
    def inline_strong(self, token: Dict[str, Any]) -> str:
        """Serialize bold text token.
        
        Args:
            token: Strong token with 'children'
            
        Returns:
            Markdown bold text
        """
        children = token.get('children', [])
        inner = self.serialize_inline(children)
        return f'**{inner}**'
    
    def inline_emphasis(self, token: Dict[str, Any]) -> str:
        """Serialize italic text token.
        
        Args:
            token: Emphasis token with 'children'
            
        Returns:
            Markdown italic text
        """
        children = token.get('children', [])
        inner = self.serialize_inline(children)
        return f'*{inner}*'
    
    def inline_codespan(self, token: Dict[str, Any]) -> str:
        """Serialize inline code token.
        
        Args:
            token: Codespan token with 'raw'
            
        Returns:
            Markdown inline code
        """
        raw = token.get('raw', '')
        return f'`{raw}`'
    
    def inline_strikethrough(self, token: Dict[str, Any]) -> str:
        """Serialize strikethrough text token.
        
        Args:
            token: Strikethrough token with 'children'
            
        Returns:
            Markdown strikethrough text
        """
        children = token.get('children', [])
        inner = self.serialize_inline(children)
        return f'~~{inner}~~'
    
    def inline_link(self, token: Dict[str, Any]) -> str:
        """Serialize link token.
        
        Args:
            token: Link token with 'children' and 'attrs'
            
        Returns:
            Markdown link
        """
        children = token.get('children', [])
        attrs = token.get('attrs', {})
        url = attrs.get('url', '')
        
        text = self.serialize_inline(children)
        return f'[{text}]({url})'
    
    def inline_image(self, token: Dict[str, Any]) -> str:
        """Serialize image token.
        
        Args:
            token: Image token with 'children' (alt text) and 'attrs'
            
        Returns:
            Markdown image
        """
        children = token.get('children', [])
        attrs = token.get('attrs', {})
        url = attrs.get('url', '')
        
        alt = self.serialize_inline(children)
        return f'![{alt}]({url})'
    
    def inline_softbreak(self, token: Dict[str, Any]) -> str:
        """Serialize soft line break.
        
        Args:
            token: Softbreak token
            
        Returns:
            Space character
        """
        return ' '
    
    def inline_linebreak(self, token: Dict[str, Any]) -> str:
        """Serialize hard line break.
        
        Args:
            token: Linebreak token
            
        Returns:
            Markdown hard break (two spaces + newline)
        """
        return '  \n'
