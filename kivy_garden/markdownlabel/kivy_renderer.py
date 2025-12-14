"""
KivyRenderer
============

Renders mistune AST to Kivy widgets for block-level elements.
"""

import logging
from typing import Any, Dict, List, Optional

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.image import AsyncImage
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle, Line

from .inline_renderer import InlineRenderer

logger = logging.getLogger(__name__)


class KivyRenderer:
    """Renders mistune AST to Kivy widgets.
    
    This renderer handles block-level Markdown elements like paragraphs,
    headings, lists, code blocks, tables, and block quotes, converting
    them to appropriate Kivy widgets.
    """
    
    NAME = "kivy"
    
    # Heading font size multipliers relative to base_font_size
    HEADING_SIZES = {
        1: 2.5,   # h1
        2: 2.0,   # h2
        3: 1.75,  # h3
        4: 1.5,   # h4
        5: 1.25,  # h5
        6: 1.0,   # h6
    }
    
    def __init__(self,
                 base_font_size: float = 15,
                 code_font_name: str = 'RobotoMono-Regular',
                 link_color: Optional[List[float]] = None,
                 link_style: str = 'unstyled',
                 code_bg_color: Optional[List[float]] = None,
                 font_name: str = 'Roboto',
                 color: Optional[List[float]] = None,
                 outline_width: Optional[float] = None,
                 outline_color: Optional[List[float]] = None,
                 disabled_outline_color: Optional[List[float]] = None,
                 line_height: float = 1.0,
                 halign: str = 'auto',
                 valign: str = 'bottom',
                 text_size: Optional[List] = None,
                 unicode_errors: str = 'replace',
                 strip: bool = False,
                 font_family: Optional[str] = None,
                 font_context: Optional[str] = None,
                 font_features: str = '',
                 font_hinting: Optional[str] = 'normal',
                 font_kerning: bool = True,
                 font_blended: bool = True,
                 disabled: bool = False,
                 disabled_color: Optional[List[float]] = None,
                 mipmap: bool = False,
                 base_direction: Optional[str] = None,
                 text_language: Optional[str] = None,
                 limit_render_to_text_bbox: bool = False,
                 shorten: bool = False,
                 max_lines: int = 0,
                 shorten_from: str = 'center',
                 split_str: str = '',
                 text_padding: Optional[List[float]] = None,
                 strict_label_mode: bool = False,
                 ellipsis_options: Optional[Dict] = None):
        """Initialize the KivyRenderer.
        
        Args:
            base_font_size: Base font size in sp for body text
            code_font_name: Font name for code blocks and inline code
            link_color: RGBA color list for link text (default: blue)
            link_style: 'unstyled' (Label-like) or 'styled' (color + underline)
            code_bg_color: RGBA color list for code block background
            font_name: Font name for body text (default: 'Roboto')
            color: RGBA color list for body text (default: white)
            outline_width: Outline width for text (default: None)
            outline_color: Outline color for text (default: black)
            disabled_outline_color: Outline color when disabled (default: black)
            line_height: Line height multiplier for text (default: 1.0)
            halign: Horizontal alignment for text (default: 'auto', converted to 'left')
            valign: Vertical alignment for text (default: 'bottom')
            text_size: Bounding box size [width, height] for text wrapping
            unicode_errors: Unicode error handling mode (default: 'replace')
            strip: Whether to strip leading/trailing whitespace (default: False)
            font_family: Font family for text (default: None)
            font_context: Font context for text (default: None)
            font_features: OpenType font features string (default: '')
            font_hinting: Font hinting mode (default: 'normal')
            font_kerning: Whether to enable font kerning (default: True)
            font_blended: Whether to use blended font rendering (default: True)
            disabled: Whether the widget is disabled (default: False)
            disabled_color: RGBA color list for disabled text (default: semi-transparent white)
            mipmap: Whether to enable mipmapping on text textures (default: False)
            base_direction: Base text direction, matches Label.base_direction (default: None)
            text_language: Language tag for text shaping (default: None)
            limit_render_to_text_bbox: Whether to limit rendering to the text bbox (default: False)
            shorten: Whether to shorten text with ellipsis (default: False)
            max_lines: Maximum number of lines to display, 0 for no limit (default: 0)
            shorten_from: Direction to truncate from: 'left', 'center', 'right' (default: 'center')
            split_str: String used as word boundary for shortening (default: '')
            text_padding: Padding values [left, top, right, bottom] for child Labels (default: [0, 0, 0, 0])
            strict_label_mode: When True, only apply text_size bindings if text_size is
                explicitly set. When False (default), auto-bind width for text wrapping.
            ellipsis_options: Dictionary of ellipsis options for text shortening (default: {})
        """
        self.base_font_size = base_font_size
        self.code_font_name = code_font_name
        self.link_color = link_color or [0, 0.5, 1, 1]
        self.link_style = link_style
        self.code_bg_color = code_bg_color or [0.15, 0.15, 0.15, 1]
        self.font_name = font_name
        self.color = color or [1, 1, 1, 1]
        self.outline_width = outline_width
        self.outline_color = outline_color or [0, 0, 0, 1]
        self.disabled_outline_color = disabled_outline_color or [0, 0, 0, 1]
        self.line_height = line_height
        # Use the effective halign passed from MarkdownLabel
        self.halign = halign
        self.valign = valign
        self.text_size = text_size or [None, None]
        self.unicode_errors = unicode_errors
        self.strip = strip
        self.font_family = font_family
        self.font_context = font_context
        self.font_features = font_features
        self.font_hinting = font_hinting
        self.font_kerning = font_kerning
        self.font_blended = font_blended
        self.disabled = disabled
        self.disabled_color = disabled_color or [1, 1, 1, 0.3]
        self.mipmap = mipmap
        self.base_direction = base_direction
        self.text_language = text_language
        self.limit_render_to_text_bbox = limit_render_to_text_bbox
        self.shorten = shorten
        self.max_lines = max_lines
        self.shorten_from = shorten_from
        self.split_str = split_str
        self.text_padding = text_padding or [0, 0, 0, 0]
        self.strict_label_mode = strict_label_mode
        self.ellipsis_options = ellipsis_options or {}
        
        # Compute effective color based on disabled state
        self.effective_color = self.disabled_color if self.disabled else self.color
        self.effective_outline_color = (
            self.disabled_outline_color if self.disabled else self.outline_color
        )
        
        self.inline_renderer = InlineRenderer(
            link_color=self.link_color,
            code_font_name=self.code_font_name,
            link_style=self.link_style,
        )

        # Track nesting depth for deep nesting protection
        self._nesting_depth = 0
        self._max_nesting_depth = 10
        
        # Track list nesting for indentation
        self._list_depth = 0
        self._list_counters = []  # Stack of counters for ordered lists
    
    def _apply_text_size_binding(self, label: Label) -> None:
        """Apply text_size binding to a Label based on mode and text_size settings.
        
        In strict_label_mode with text_size=[None, None], no automatic width
        binding is applied (Label handles sizing naturally).
        
        In non-strict mode (default), width is bound to text_size for auto-wrap.
        
        Args:
            label: The Label widget to apply bindings to
        """
        text_width = self.text_size[0]
        text_height = self.text_size[1]
        
        if text_width is not None:
            if text_height is not None:
                # Both width and height specified
                label.text_size = (text_width, text_height)
            else:
                # Only width specified - bind to maintain width
                label.bind(width=lambda inst, val, tw=text_width: setattr(
                    inst, 'text_size', (tw, None)))
        else:
            if text_height is not None:
                # Only height specified - set initial text_size and bind width
                label.text_size = (label.width, text_height)
                label.bind(width=lambda inst, val, th=text_height: setattr(
                    inst, 'text_size', (val, th)))
            else:
                # Neither specified
                if self.strict_label_mode:
                    # Strict mode: don't auto-bind width, let Label handle naturally
                    pass
                else:
                    # Markdown-friendly mode: auto-bind width for text wrapping
                    label.bind(width=lambda inst, val: setattr(
                        inst, 'text_size', (val, None)))
        
        # Always bind texture_size to height for proper sizing
        label.bind(texture_size=lambda inst, val: setattr(inst, 'height', val[1]))
    
    def __call__(self, tokens: List[Dict[str, Any]], state: Any = None) -> BoxLayout:
        """Render tokens to a BoxLayout containing all widgets.
        
        Args:
            tokens: List of AST tokens from mistune
            state: Block state from mistune (optional)
            
        Returns:
            BoxLayout containing rendered widgets
        """
        root = BoxLayout(orientation='vertical', size_hint_y=None)
        root.bind(minimum_height=root.setter('height'))
        
        for token in tokens:
            widget = self._render_token(token, state)
            if widget is not None:
                root.add_widget(widget)
        
        return root
    
    def _render_token(self, token: Dict[str, Any], state: Any = None) -> Optional[Widget]:
        """Render a single token to a widget.
        
        Args:
            token: AST token dictionary
            state: Block state from mistune
            
        Returns:
            Rendered widget or None
        """
        # Check nesting depth limit
        if self._nesting_depth > self._max_nesting_depth:
            logger.warning(
                f"Maximum nesting depth ({self._max_nesting_depth}) exceeded. "
                f"Truncating nested content at depth {self._nesting_depth}."
            )
            # Return a placeholder widget indicating truncation
            return self._create_truncation_placeholder()
        
        token_type = token.get('type', '')
        method = getattr(self, token_type, None)
        
        if method is not None:
            return method(token, state)
        
        # Unknown token type - skip with warning
        return None
    
    def _create_truncation_placeholder(self) -> Widget:
        """Create a placeholder widget for truncated deeply nested content.
        
        Returns:
            Label widget indicating content was truncated
        """
        label = Label(
            text='[...content truncated due to deep nesting...]',
            markup=False,
            font_size=self.base_font_size,
            size_hint_y=None,
            color=[0.6, 0.6, 0.6, 1],  # Gray text
            italic=True
        )
        label.bind(texture_size=label.setter('size'))
        return label
    
    def _render_inline(self, children: List[Dict[str, Any]]) -> str:
        """Render inline tokens to Kivy markup string.
        
        Args:
            children: List of inline tokens
            
        Returns:
            Kivy markup string
        """
        return self.inline_renderer.render(children)
    
    def paragraph(self, token: Dict[str, Any], state: Any = None) -> Label:
        """Render a paragraph as a Label with markup enabled.
        
        Args:
            token: Paragraph token with 'children'
            state: Block state
            
        Returns:
            Label widget with markup=True
        """
        children = token.get('children', [])
        text = self._render_inline(children)
        
        label_kwargs = {
            'text': text,
            'markup': True,
            'font_name': self.font_name,
            'font_size': self.base_font_size,
            'color': self.effective_color,
            'line_height': self.line_height,
            'size_hint_y': None,
            'size_hint_x': 1,
            'halign': self.halign,
            'valign': self.valign,
            'unicode_errors': self.unicode_errors,
            'strip': self.strip,
            'font_features': self.font_features,
            'font_kerning': self.font_kerning,
            'font_blended': self.font_blended,
            'shorten': self.shorten,
            'shorten_from': self.shorten_from,
            'split_str': self.split_str,
            'padding': self.text_padding,
            'mipmap': self.mipmap,
            'outline_width': self.outline_width,
            'outline_color': self.effective_outline_color,
            'disabled_outline_color': self.disabled_outline_color,
            'base_direction': self.base_direction,
            'text_language': self.text_language,
            'limit_render_to_text_bbox': self.limit_render_to_text_bbox,
            'ellipsis_options': self.ellipsis_options,
        }
        
        # Add max_lines only if set (non-zero)
        if self.max_lines > 0:
            label_kwargs['max_lines'] = self.max_lines
        
        # Add optional font properties if set
        if self.font_family is not None:
            label_kwargs['font_family'] = self.font_family
        if self.font_context is not None:
            label_kwargs['font_context'] = self.font_context
        if self.font_hinting is not None:
            label_kwargs['font_hinting'] = self.font_hinting
        
        # Add ellipsis_options if non-empty
        if self.ellipsis_options:
            label_kwargs['ellipsis_options'] = self.ellipsis_options
        
        label = Label(**label_kwargs)
        
        # Apply text_size binding based on mode
        self._apply_text_size_binding(label)
        
        # Set font scale metadata for body text
        label._font_scale = 1.0
        
        return label
    
    def block_text(self, token: Dict[str, Any], state: Any = None) -> Label:
        """Render block text (used in list items) as a Label with markup enabled.
        
        Args:
            token: Block text token with 'children'
            state: Block state
            
        Returns:
            Label widget with markup=True
        """
        children = token.get('children', [])
        text = self._render_inline(children)
        
        label_kwargs = {
            'text': text,
            'markup': True,
            'font_name': self.font_name,
            'font_size': self.base_font_size,
            'color': self.effective_color,
            'line_height': self.line_height,
            'size_hint_y': None,
            'size_hint_x': 1,
            'halign': self.halign,
            'valign': self.valign,
            'unicode_errors': self.unicode_errors,
            'strip': self.strip,
            'font_features': self.font_features,
            'font_kerning': self.font_kerning,
            'font_blended': self.font_blended,
            'shorten': self.shorten,
            'shorten_from': self.shorten_from,
            'split_str': self.split_str,
            'padding': self.text_padding,
            'mipmap': self.mipmap,
            'outline_width': self.outline_width,
            'outline_color': self.effective_outline_color,
            'disabled_outline_color': self.disabled_outline_color,
            'base_direction': self.base_direction,
            'text_language': self.text_language,
            'limit_render_to_text_bbox': self.limit_render_to_text_bbox,
            'ellipsis_options': self.ellipsis_options,
        }
        
        # Add max_lines only if set (non-zero)
        if self.max_lines > 0:
            label_kwargs['max_lines'] = self.max_lines
        
        # Add optional font properties if set
        if self.font_family is not None:
            label_kwargs['font_family'] = self.font_family
        if self.font_context is not None:
            label_kwargs['font_context'] = self.font_context
        if self.font_hinting is not None:
            label_kwargs['font_hinting'] = self.font_hinting
        
        # Add ellipsis_options if non-empty
        if self.ellipsis_options:
            label_kwargs['ellipsis_options'] = self.ellipsis_options
        
        label = Label(**label_kwargs)
        
        # Apply text_size binding based on mode
        self._apply_text_size_binding(label)
        
        # Set font scale metadata for body text
        label._font_scale = 1.0
        
        return label
    
    def heading(self, token: Dict[str, Any], state: Any = None) -> Label:
        """Render a heading as a Label with scaled font size.
        
        Font sizes are based on heading level:
        - h1: 2.5x base
        - h2: 2.0x base
        - h3: 1.75x base
        - h4: 1.5x base
        - h5: 1.25x base
        - h6: 1.0x base
        
        Args:
            token: Heading token with 'children' and 'attrs'
            state: Block state
            
        Returns:
            Label widget with scaled font size
        """
        children = token.get('children', [])
        attrs = token.get('attrs', {})
        level = attrs.get('level', 1)
        
        # Clamp level to valid range
        level = max(1, min(6, level))
        
        text = self._render_inline(children)
        multiplier = self.HEADING_SIZES.get(level, 1.0)
        font_size = self.base_font_size * multiplier
        
        label_kwargs = {
            'text': text,
            'markup': True,
            'font_name': self.font_name,
            'font_size': font_size,
            'color': self.effective_color,
            'line_height': self.line_height,
            'size_hint_y': None,
            'size_hint_x': 1,
            'bold': True,
            'halign': self.halign,
            'valign': self.valign,
            'unicode_errors': self.unicode_errors,
            'strip': self.strip,
            'font_features': self.font_features,
            'font_kerning': self.font_kerning,
            'font_blended': self.font_blended,
            'shorten': self.shorten,
            'shorten_from': self.shorten_from,
            'split_str': self.split_str,
            'padding': self.text_padding,
            'mipmap': self.mipmap,
            'outline_width': self.outline_width,
            'outline_color': self.effective_outline_color,
            'disabled_outline_color': self.disabled_outline_color,
            'base_direction': self.base_direction,
            'text_language': self.text_language,
            'limit_render_to_text_bbox': self.limit_render_to_text_bbox,
            'ellipsis_options': self.ellipsis_options,
        }
        
        # Add max_lines only if set (non-zero)
        if self.max_lines > 0:
            label_kwargs['max_lines'] = self.max_lines
        
        # Add optional font properties if set
        if self.font_family is not None:
            label_kwargs['font_family'] = self.font_family
        if self.font_context is not None:
            label_kwargs['font_context'] = self.font_context
        if self.font_hinting is not None:
            label_kwargs['font_hinting'] = self.font_hinting
        
        # Add ellipsis_options if non-empty
        if self.ellipsis_options:
            label_kwargs['ellipsis_options'] = self.ellipsis_options
        
        label = Label(**label_kwargs)
        
        # Apply text_size binding based on mode
        self._apply_text_size_binding(label)
        
        # Store heading level as metadata
        label.heading_level = level
        
        # Set font scale metadata for headings
        label._font_scale = multiplier
        
        return label
    
    def blank_line(self, token: Dict[str, Any], state: Any = None) -> Widget:
        """Render a blank line as an empty widget with height.
        
        Args:
            token: Blank line token
            state: Block state
            
        Returns:
            Empty widget with fixed height
        """
        widget = Widget(size_hint_y=None, height=self.base_font_size)
        return widget

    def list(self, token: Dict[str, Any], state: Any = None) -> BoxLayout:
        """Render a list as a vertical BoxLayout.
        
        Args:
            token: List token with 'children' and 'attrs'
            state: Block state
            
        Returns:
            BoxLayout containing list items
        """
        attrs = token.get('attrs', {})
        ordered = attrs.get('ordered', False)
        start = attrs.get('start', 1)
        children = token.get('children', [])
        
        # Track list depth for indentation and nesting depth for protection
        self._list_depth += 1
        self._nesting_depth += 1
        
        # Push counter for ordered lists
        if ordered:
            self._list_counters.append(start)
        
        # Add bottom spacing only for top-level lists
        bottom_padding = self.base_font_size if self._list_depth == 1 else 0
        
        container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            padding=[self._list_depth * 20, 0, 0, bottom_padding]  # Left indent + bottom spacing
        )
        container.bind(minimum_height=container.setter('height'))
        
        for i, child in enumerate(children):
            item_widget = self._render_list_item(child, ordered, i, state)
            if item_widget is not None:
                container.add_widget(item_widget)
        
        # Pop counter for ordered lists
        if ordered:
            self._list_counters.pop()
        
        self._list_depth -= 1
        self._nesting_depth -= 1
        
        return container
    
    def _render_list_item(self, token: Dict[str, Any], ordered: bool, 
                          index: int, state: Any = None) -> BoxLayout:
        """Render a list item with bullet/number prefix.
        
        Args:
            token: List item token
            ordered: Whether this is an ordered list
            index: Item index (0-based)
            state: Block state
            
        Returns:
            BoxLayout with marker and content
        """
        # Create horizontal layout for marker + content
        item_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None
        )
        item_layout.bind(minimum_height=item_layout.setter('height'))
        
        # Create marker (bullet or number)
        if ordered:
            counter = self._list_counters[-1] if self._list_counters else 1
            marker_text = f'{counter + index}.'
        else:
            marker_text = '•'
        
        marker_kwargs = {
            'text': marker_text,
            'font_name': self.font_name,
            'font_size': self.base_font_size,
            'color': self.effective_color,
            'line_height': self.line_height,
            'size_hint': (None, 1),  # Match content height
            'width': 30,
            'halign': 'right',
            # Force top alignment so bullets align with the first line of nested content
            'valign': 'top',
            'unicode_errors': self.unicode_errors,
            'strip': self.strip,
            'font_features': self.font_features,
            'font_kerning': self.font_kerning,
            'font_blended': self.font_blended,
            'shorten': self.shorten,
            'shorten_from': self.shorten_from,
            'split_str': self.split_str,
            'padding': self.text_padding,
            'mipmap': self.mipmap,
            'outline_width': self.outline_width,
            'outline_color': self.effective_outline_color,
            'disabled_outline_color': self.disabled_outline_color,
            'base_direction': self.base_direction,
            'text_language': self.text_language,
            'limit_render_to_text_bbox': self.limit_render_to_text_bbox,
            'ellipsis_options': self.ellipsis_options,
        }
        
        # Add max_lines only if set (non-zero)
        if self.max_lines > 0:
            marker_kwargs['max_lines'] = self.max_lines
        
        # Add optional font properties if set
        if self.font_family is not None:
            marker_kwargs['font_family'] = self.font_family
        if self.font_context is not None:
            marker_kwargs['font_context'] = self.font_context
        if self.font_hinting is not None:
            marker_kwargs['font_hinting'] = self.font_hinting
        
        # Add ellipsis_options if non-empty
        if self.ellipsis_options:
            marker_kwargs['ellipsis_options'] = self.ellipsis_options
        
        marker = Label(**marker_kwargs)
        # Bind text_size to enable valign to work properly
        marker.bind(size=lambda inst, val: setattr(inst, 'text_size', val))
        
        # Set font scale metadata for list markers
        marker._font_scale = 1.0
        
        item_layout.add_widget(marker)
        
        # Create content container
        content = BoxLayout(
            orientation='vertical',
            size_hint_y=None
        )
        content.bind(minimum_height=content.setter('height'))
        
        # Render children of list item
        children = token.get('children', [])
        for child in children:
            child_widget = self._render_token(child, state)
            if child_widget is not None:
                content.add_widget(child_widget)
        
        item_layout.add_widget(content)
        
        return item_layout
    
    def list_item(self, token: Dict[str, Any], state: Any = None) -> BoxLayout:
        """Render a list item (called directly if needed).
        
        Note: Usually list items are rendered via _render_list_item from list().
        
        Args:
            token: List item token
            state: Block state
            
        Returns:
            BoxLayout with content
        """
        content = BoxLayout(
            orientation='vertical',
            size_hint_y=None
        )
        content.bind(minimum_height=content.setter('height'))
        
        children = token.get('children', [])
        for child in children:
            child_widget = self._render_token(child, state)
            if child_widget is not None:
                content.add_widget(child_widget)
        
        return content

    def block_code(self, token: Dict[str, Any], state: Any = None) -> Widget:
        """Render a code block with monospace font and dark background.
        
        Args:
            token: Code block token with 'raw' and optional 'attrs'
            state: Block state
            
        Returns:
            Widget containing styled code block
        """
        raw = token.get('raw', '')
        attrs = token.get('attrs', {})
        language = attrs.get('info', '')
        
        # Escape the code text for Kivy markup
        escaped_text = self.inline_renderer._escape_markup(raw.rstrip('\n'))
        
        # Create container with background
        container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            padding=[10, 10, 10, 10]
        )
        
        # Add dark background using canvas
        with container.canvas.before:
            Color(*self.code_bg_color)
            container._bg_rect = Rectangle(pos=container.pos, size=container.size)
        
        # Bind background to container size/pos
        def update_bg(instance, value):
            container._bg_rect.pos = instance.pos
            container._bg_rect.size = instance.size
        
        container.bind(pos=update_bg, size=update_bg)
        
        # Create label with monospace font
        # Note: code blocks use code_font_name and fixed light color, not font_name/color
        # font_family is intentionally excluded from code blocks to preserve monospace
        # appearance (Requirement 6.1). Other font properties (font_context, font_features,
        # font_hinting, font_kerning, font_blended) are forwarded per Requirements 6.2-6.5.
        label_kwargs = {
            'text': escaped_text,
            'markup': True,
            'font_name': self.code_font_name,
            'font_size': self.base_font_size,
            'line_height': self.line_height,
            'size_hint_y': None,
            'halign': 'left',
            'valign': 'top',
            'color': self.disabled_color if self.disabled else [0.9, 0.9, 0.9, 1],
            'unicode_errors': self.unicode_errors,
            'strip': self.strip,
            'font_features': self.font_features,
            'font_kerning': self.font_kerning,
            'font_blended': self.font_blended,
            'mipmap': self.mipmap,
            'outline_width': self.outline_width,
            'outline_color': self.effective_outline_color,
            'disabled_outline_color': self.disabled_outline_color,
            'base_direction': self.base_direction,
            'text_language': self.text_language,
            'limit_render_to_text_bbox': self.limit_render_to_text_bbox,
            'ellipsis_options': self.ellipsis_options,
        }
        
        # Add optional font properties if set (excluding font_family for code blocks)
        if self.font_context is not None:
            label_kwargs['font_context'] = self.font_context
        if self.font_hinting is not None:
            label_kwargs['font_hinting'] = self.font_hinting
        
        label = Label(**label_kwargs)
        label.bind(texture_size=label.setter('size'))
        label.bind(size=lambda instance, value: setattr(instance, 'text_size', (value[0], None)))
        
        # Set font scale metadata for code blocks
        label._font_scale = 1.0
        label._is_code = True
        
        container.add_widget(label)
        container.bind(minimum_height=container.setter('height'))
        
        # Store language info as metadata
        container.language_info = language
        
        return container

    def block_quote(self, token: Dict[str, Any], state: Any = None) -> BoxLayout:
        """Render a block quote with left border and indentation.
        
        Args:
            token: Block quote token with 'children'
            state: Block state
            
        Returns:
            BoxLayout with left border styling
        """
        children = token.get('children', [])
        
        # Track nesting depth
        self._nesting_depth += 1
        
        # Create container with left padding for indentation
        container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            padding=[20, 5, 5, 5]  # Left padding for quote indentation
        )
        container.bind(minimum_height=container.setter('height'))
        
        # Add left border using canvas
        border_color = [0.5, 0.5, 0.5, 1]  # Gray border
        with container.canvas.before:
            Color(*border_color)
            container._border_line = Line(
                points=[container.x + 5, container.y, container.x + 5, container.y + container.height],
                width=2
            )
        
        # Bind border to container size/pos
        def update_border(instance, value):
            container._border_line.points = [
                instance.x + 5, instance.y,
                instance.x + 5, instance.y + instance.height
            ]
        
        container.bind(pos=update_border, size=update_border)
        
        # Render children
        for child in children:
            child_widget = self._render_token(child, state)
            if child_widget is not None:
                container.add_widget(child_widget)
        
        self._nesting_depth -= 1
        
        return container

    def thematic_break(self, token: Dict[str, Any], state: Any = None) -> Widget:
        """Render a thematic break (horizontal rule) as a widget with a line.
        
        Args:
            token: Thematic break token
            state: Block state
            
        Returns:
            Widget with horizontal line on canvas
        """
        widget = Widget(
            size_hint_y=None,
            height=20  # Fixed height for the rule
        )
        
        # Draw horizontal line on canvas
        line_color = [0.5, 0.5, 0.5, 1]  # Gray line
        with widget.canvas:
            Color(*line_color)
            widget._hr_line = Line(
                points=[widget.x, widget.center_y, widget.x + widget.width, widget.center_y],
                width=1
            )
        
        # Bind line to widget size/pos
        def update_line(instance, value):
            widget._hr_line.points = [
                instance.x, instance.center_y,
                instance.x + instance.width, instance.center_y
            ]
        
        widget.bind(pos=update_line, size=update_line)
        
        return widget

    def image(self, token: Dict[str, Any], state: Any = None) -> Widget:
        """Render an image as an AsyncImage widget.
        
        Args:
            token: Image token with 'attrs' containing url
            state: Block state
            
        Returns:
            AsyncImage widget or Label with alt text on failure
        """
        attrs = token.get('attrs', {})
        url = attrs.get('url', '')
        children = token.get('children', [])
        
        # Get alt text from children
        alt_text = self._render_inline(children) if children else ''
        
        # Create AsyncImage
        image = AsyncImage(
            source=url,
            size_hint_y=None,
            allow_stretch=True,
            keep_ratio=True
        )
        
        # Store alt text for fallback
        image.alt_text = alt_text
        
        # Set initial height based on texture when loaded
        def on_texture(instance, value):
            if value:
                # Calculate height maintaining aspect ratio
                ratio = value.height / value.width if value.width > 0 else 1
                instance.height = instance.width * ratio
            else:
                # Fallback height if no texture
                instance.height = 100
        
        image.bind(texture=on_texture)
        
        # Set default height until texture loads
        image.height = 100
        
        return image
    
    def newline(self, token: Dict[str, Any], state: Any = None) -> Widget:
        """Render a newline as a small spacer widget.
        
        Args:
            token: Newline token
            state: Block state
            
        Returns:
            Small spacer widget
        """
        return Widget(size_hint_y=None, height=5)

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
        # but fall back to the renderer's halign if not specified
        align = attrs.get('align', None)
        cell_halign = align if align in ('left', 'center', 'right') else self.halign
        
        # Render inline content
        text = self._render_inline(children) if children else ''
        
        # Create label with appropriate styling
        label_kwargs = {
            'text': text,
            'markup': True,
            'font_name': self.font_name,
            'font_size': self.base_font_size,
            'color': self.effective_color,
            'line_height': self.line_height,
            'size_hint_y': None,
            'size_hint_x': 1,
            'halign': cell_halign,
            'valign': self.valign,
            'bold': is_head,  # Bold for header cells
            'unicode_errors': self.unicode_errors,
            'strip': self.strip,
            'font_features': self.font_features,
            'font_kerning': self.font_kerning,
            'font_blended': self.font_blended,
            'shorten': self.shorten,
            'shorten_from': self.shorten_from,
            'split_str': self.split_str,
            'padding': self.text_padding,
            'mipmap': self.mipmap,
            'outline_width': self.outline_width,
            'outline_color': self.effective_outline_color,
            'disabled_outline_color': self.disabled_outline_color,
            'base_direction': self.base_direction,
            'text_language': self.text_language,
            'limit_render_to_text_bbox': self.limit_render_to_text_bbox,
            'ellipsis_options': self.ellipsis_options,
        }
        
        # Add max_lines only if set (non-zero)
        if self.max_lines > 0:
            label_kwargs['max_lines'] = self.max_lines
        
        # Add optional font properties if set
        if self.font_family is not None:
            label_kwargs['font_family'] = self.font_family
        if self.font_context is not None:
            label_kwargs['font_context'] = self.font_context
        if self.font_hinting is not None:
            label_kwargs['font_hinting'] = self.font_hinting
        
        # Add ellipsis_options if non-empty
        if self.ellipsis_options:
            label_kwargs['ellipsis_options'] = self.ellipsis_options
        
        label = Label(**label_kwargs)
        
        # Apply text_size binding based on mode
        self._apply_text_size_binding(label)
        
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
