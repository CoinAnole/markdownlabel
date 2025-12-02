"""
KivyRenderer
============

Renders mistune AST to Kivy widgets for block-level elements.
"""

from typing import Any, Dict, List, Optional

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.image import AsyncImage
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle, Line

from .inline_renderer import InlineRenderer


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
                 code_bg_color: Optional[List[float]] = None):
        """Initialize the KivyRenderer.
        
        Args:
            base_font_size: Base font size in sp for body text
            code_font_name: Font name for code blocks and inline code
            link_color: RGBA color list for link text (default: blue)
            code_bg_color: RGBA color list for code block background
        """
        self.base_font_size = base_font_size
        self.code_font_name = code_font_name
        self.link_color = link_color or [0, 0.5, 1, 1]
        self.code_bg_color = code_bg_color or [0.15, 0.15, 0.15, 1]
        
        self.inline_renderer = InlineRenderer(
            link_color=self.link_color,
            code_font_name=self.code_font_name
        )

        # Track nesting depth for deep nesting protection
        self._nesting_depth = 0
        self._max_nesting_depth = 10
        
        # Track list nesting for indentation
        self._list_depth = 0
        self._list_counters = []  # Stack of counters for ordered lists
    
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
        token_type = token.get('type', '')
        method = getattr(self, token_type, None)
        
        if method is not None:
            return method(token, state)
        
        # Unknown token type - skip with warning
        return None
    
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
        
        label = Label(
            text=text,
            markup=True,
            font_size=self.base_font_size,
            size_hint_y=None,
            text_size=(None, None),
            halign='left',
            valign='top'
        )
        label.bind(texture_size=label.setter('size'))
        
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
        
        label = Label(
            text=text,
            markup=True,
            font_size=font_size,
            size_hint_y=None,
            bold=True,
            halign='left',
            valign='top'
        )
        label.bind(texture_size=label.setter('size'))
        
        # Store heading level as metadata
        label.heading_level = level
        
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
        
        # Track list depth for indentation
        self._list_depth += 1
        
        # Push counter for ordered lists
        if ordered:
            self._list_counters.append(start)
        
        container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            padding=[self._list_depth * 20, 0, 0, 0]  # Left indent based on depth
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
        
        marker = Label(
            text=marker_text,
            font_size=self.base_font_size,
            size_hint=(None, None),
            width=30,
            halign='right',
            valign='top'
        )
        marker.bind(texture_size=lambda inst, val: setattr(inst, 'height', val[1]))
        
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
        label = Label(
            text=escaped_text,
            markup=True,
            font_name=self.code_font_name,
            font_size=self.base_font_size,
            size_hint_y=None,
            halign='left',
            valign='top',
            color=[0.9, 0.9, 0.9, 1]  # Light text on dark background
        )
        label.bind(texture_size=label.setter('size'))
        
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
