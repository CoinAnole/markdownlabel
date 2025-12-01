"""
InlineRenderer
==============

Converts inline Markdown AST tokens to Kivy markup strings.
"""

from typing import Any, Dict, List, Optional


class InlineRenderer:
    """Converts inline AST tokens to Kivy markup strings.
    
    This renderer handles inline Markdown elements like bold, italic,
    code spans, links, and strikethrough, converting them to Kivy's
    BBCode-like markup format.
    """
    
    def __init__(self, 
                 link_color: Optional[List[float]] = None,
                 code_font_name: str = 'RobotoMono-Regular'):
        """Initialize the InlineRenderer.
        
        Args:
            link_color: RGBA color list for link text (default: blue)
            code_font_name: Font name for inline code spans
        """
        self.link_color = link_color or [0, 0.5, 1, 1]
        self.code_font_name = code_font_name
    
    def render(self, children: List[Dict[str, Any]]) -> str:
        """Render inline tokens to a Kivy markup string.
        
        Args:
            children: List of inline AST tokens from mistune
            
        Returns:
            Kivy markup string
        """
        result = []
        for token in children:
            token_type = token.get('type', 'text')
            method = getattr(self, token_type, self._unknown)
            result.append(method(token))
        return ''.join(result)
    
    def _unknown(self, token: Dict[str, Any]) -> str:
        """Handle unknown token types by returning raw text if available."""
        return self._escape_markup(token.get('raw', ''))
    
    def _escape_markup(self, text: str) -> str:
        """Escape Kivy markup special characters.
        
        Kivy markup uses [ ] for tags and & for escape sequences.
        We need to escape these to prevent markup injection.
        
        Args:
            text: Raw text to escape
            
        Returns:
            Escaped text safe for Kivy markup
        """
        # Order matters: escape & first to avoid double-escaping
        text = text.replace('&', '&amp;')
        text = text.replace('[', '&bl;')
        text = text.replace(']', '&br;')
        return text
    
    def text(self, token: Dict[str, Any]) -> str:
        """Render plain text with Kivy markup escaping.
        
        Args:
            token: Token with 'raw' key containing text
            
        Returns:
            Escaped text
        """
        raw = token.get('raw', '')
        return self._escape_markup(raw)
    
    def strong(self, token: Dict[str, Any]) -> str:
        """Render bold text as [b]...[/b].
        
        Args:
            token: Token with 'children' containing nested tokens
            
        Returns:
            Kivy bold markup
        """
        children = token.get('children', [])
        inner = self.render(children)
        return f'[b]{inner}[/b]'
    
    def emphasis(self, token: Dict[str, Any]) -> str:
        """Render italic text as [i]...[/i].
        
        Args:
            token: Token with 'children' containing nested tokens
            
        Returns:
            Kivy italic markup
        """
        children = token.get('children', [])
        inner = self.render(children)
        return f'[i]{inner}[/i]'
    
    def codespan(self, token: Dict[str, Any]) -> str:
        """Render inline code with monospace font markup.
        
        Args:
            token: Token with 'raw' key containing code text
            
        Returns:
            Kivy font markup for monospace
        """
        raw = token.get('raw', '')
        escaped = self._escape_markup(raw)
        return f'[font={self.code_font_name}]{escaped}[/font]'
    
    def strikethrough(self, token: Dict[str, Any]) -> str:
        """Render strikethrough text as [s]...[/s].
        
        Args:
            token: Token with 'children' containing nested tokens
            
        Returns:
            Kivy strikethrough markup
        """
        children = token.get('children', [])
        inner = self.render(children)
        return f'[s]{inner}[/s]'
    
    def link(self, token: Dict[str, Any]) -> str:
        """Render link as [ref=url]...[/ref].
        
        Args:
            token: Token with 'children' and 'attrs' containing url
            
        Returns:
            Kivy ref markup for clickable links
        """
        children = token.get('children', [])
        attrs = token.get('attrs', {})
        url = attrs.get('url', '')
        inner = self.render(children)
        return f'[ref={url}]{inner}[/ref]'
    
    def softbreak(self, token: Dict[str, Any]) -> str:
        """Render soft line break as a space.
        
        Args:
            token: Softbreak token (no content)
            
        Returns:
            Single space
        """
        return ' '
    
    def linebreak(self, token: Dict[str, Any]) -> str:
        """Render hard line break as newline.
        
        Args:
            token: Linebreak token (no content)
            
        Returns:
            Newline character
        """
        return '\n'
    
    def image(self, token: Dict[str, Any]) -> str:
        """Render image as alt text (inline context).
        
        In inline context, images are rendered as their alt text.
        Block-level rendering handles actual image widgets.
        
        Args:
            token: Token with 'children' containing alt text tokens
            
        Returns:
            Alt text string
        """
        children = token.get('children', [])
        return self.render(children)
    
    def inline_html(self, token: Dict[str, Any]) -> str:
        """Render inline HTML as escaped text.
        
        Args:
            token: Token with 'raw' containing HTML
            
        Returns:
            Escaped HTML text
        """
        raw = token.get('raw', '')
        return self._escape_markup(raw)
