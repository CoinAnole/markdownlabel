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
from kivy.graphics import Color, Rectangle, Line

from .font_fallback import apply_fallback_markup
from .inline_renderer import InlineRenderer, escape_kivy_markup
from .kivy_renderer_tables import KivyRendererTableMixin
from .rendering import apply_text_size_binding as _apply_text_size_binding_helper

logger = logging.getLogger(__name__)


class KivyRenderer(KivyRendererTableMixin):
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
                 ellipsis_options: Optional[Dict] = None,
                 fallback_enabled: bool = False,
                 fallback_fonts: Optional[List[str]] = None,
                 fallback_font_scales: Optional[Dict[str, float]] = None):
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
        self.fallback_enabled = fallback_enabled
        self.fallback_fonts = fallback_fonts or []
        self.fallback_font_scales = fallback_font_scales or {}

        # Compute effective color based on disabled state
        self.effective_color = self.disabled_color if self.disabled else self.color
        self.effective_outline_color = (
            self.disabled_outline_color if self.disabled else self.outline_color
        )

        self.inline_renderer = InlineRenderer(
            link_color=self.link_color,
            code_font_name=self.code_font_name,
            link_style=self.link_style,
            font_name=self.font_name,
            fallback_enabled=self.fallback_enabled,
            fallback_fonts=self.fallback_fonts,
            base_font_size=self.base_font_size,
            fallback_font_scales=self.fallback_font_scales,
        )

        # Track nesting depth for deep nesting protection
        self._nesting_depth = 0
        self._max_nesting_depth = 10

        # Track list nesting for indentation
        self._list_depth = 0
        self._list_counters = []  # Stack of counters for ordered lists

    def _apply_text_size_binding(self, label: Label) -> None:
        """Backward-compatible text_size binding using shared logic."""
        _apply_text_size_binding_helper(label, self.text_size, self.strict_label_mode)

    def _build_label_kwargs(self, *, text: str, font_size: float, halign: Optional[str] = None,
                            valign: Optional[str] = None, bold: bool = False,
                            markup: bool = True, padding: Optional[List[float]] = None,
                            size_hint_x: Optional[float] = 1, size_hint_y: Optional[float] = None,
                            color: Optional[List[float]] = None) -> Dict[str, Any]:
        """Assemble common Label kwargs used by block-level renderers."""
        kwargs = {
            'text': text,
            'markup': markup,
            'font_name': self.font_name,
            'font_size': font_size,
            'color': color if color is not None else self.effective_color,
            'line_height': self.line_height,
            'size_hint_x': size_hint_x,
            'size_hint_y': size_hint_y,
            'halign': halign if halign is not None else self.halign,
            'valign': valign if valign is not None else self.valign,
            'unicode_errors': self.unicode_errors,
            'strip': self.strip,
            'font_features': self.font_features,
            'font_kerning': self.font_kerning,
            'font_blended': self.font_blended,
            'shorten': self.shorten,
            'shorten_from': self.shorten_from,
            'split_str': self.split_str,
            'padding': padding if padding is not None else self.text_padding,
            'mipmap': self.mipmap,
            'outline_width': self.outline_width,
            'outline_color': self.effective_outline_color,
            'disabled_outline_color': self.disabled_outline_color,
            'base_direction': self.base_direction,
            'text_language': self.text_language,
            'limit_render_to_text_bbox': self.limit_render_to_text_bbox,
            'ellipsis_options': self.ellipsis_options,
        }

        if bold:
            kwargs['bold'] = True

        if self.max_lines > 0:
            kwargs['max_lines'] = self.max_lines

        if self.font_family is not None:
            kwargs['font_family'] = self.font_family
        if self.font_context is not None:
            kwargs['font_context'] = self.font_context
        if self.font_hinting is not None:
            kwargs['font_hinting'] = self.font_hinting

        # Avoid passing empty ellipsis options explicitly when not set
        if not self.ellipsis_options:
            kwargs.pop('ellipsis_options', None)

        return kwargs

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

        if method is None:
            logger.debug(
                "Skipping unknown token type '%s' (keys=%s)",
                token_type,
                sorted(token.keys()),
            )
            return None

        return method(token, state)

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
        # NOTE: Don't bind texture_size->height here; MarkdownLabel applies a
        # consistent binding pass across all Labels after rendering.
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

        label_kwargs = self._build_label_kwargs(
            text=text,
            font_size=self.base_font_size,
            size_hint_y=None,
            size_hint_x=1,
        )

        label = Label(**label_kwargs)

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

        label_kwargs = self._build_label_kwargs(
            text=text,
            font_size=self.base_font_size,
            size_hint_y=None,
            size_hint_x=1,
        )

        label = Label(**label_kwargs)

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

        label_kwargs = self._build_label_kwargs(
            text=text,
            font_size=font_size,
            bold=True,
            size_hint_y=None,
            size_hint_x=1,
        )

        label = Label(**label_kwargs)

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
        indent = self._list_depth * 20
        align_right = self.halign == 'right'

        container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            padding=[0, 0, indent, bottom_padding] if align_right else [indent, 0, 0, bottom_padding]
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

        marker_kwargs = self._build_label_kwargs(
            text=marker_text,
            font_size=self.base_font_size,
            halign='right',
            valign='top',  # Force top alignment so bullets align with first line
            markup=False,
            size_hint_x=None,
            # IMPORTANT: do NOT use size_hint_y=1 here. item_layout's height is
            # driven by minimum_height (children heights), and a child whose
            # height is driven by the parent creates a feedback loop that can
            # hit Clock.max_iteration.
            size_hint_y=None,
        )

        marker = Label(**marker_kwargs)
        marker.width = 30
        # The marker's height is driven by the list item content column height
        # (see binding below). Disable auto texture_size->height binding to avoid
        # a feedback loop (height changes -> size changes -> text_size changes ->
        # texture_size changes -> height changes ...).
        marker._md_disable_tex_height_binding = True

        # Bind text_size to enable valign to work properly. Use width/height
        # bindings rather than size to reduce churn.
        def _update_marker_text_size(*_args):
            marker.text_size = (marker.width, marker.height)

        marker.bind(width=_update_marker_text_size, height=_update_marker_text_size)
        _update_marker_text_size()

        # Set font scale metadata for list markers
        marker._font_scale = 1.0

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

        align_right = self.halign == 'right'
        if align_right:
            item_layout.add_widget(content)
            item_layout.add_widget(marker)
        else:
            item_layout.add_widget(marker)
            item_layout.add_widget(content)

        # Keep the marker column aligned to the content column height without
        # introducing a parent-driven size_hint_y cycle.
        content.bind(height=marker.setter('height'))
        marker.height = content.height

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
        escaped_text = apply_fallback_markup(
            raw.rstrip('\n'),
            primary_font=self.code_font_name,
            fallback_fonts=self.fallback_fonts,
            enabled=self.fallback_enabled,
            wrap_primary=True,
            base_font_size=self.base_font_size,
            font_scales=self.fallback_font_scales
        )

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
        # NOTE: Don't bind size/texture_size here; MarkdownLabel applies a
        # consistent text_size + texture_size->height binding pass across all
        # Labels after rendering. Duplicating bindings here can create layout
        # thrash and trigger Clock.max_iteration warnings on complex content.

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
        )
        # Kivy 2.2+ deprecates allow_stretch/keep_ratio in favor of fit_mode.
        # We want aspect-preserving resizing to fit within the widget (equivalent
        # to allow_stretch=True, keep_ratio=True).
        try:
            if 'fit_mode' in image.properties():
                image.fit_mode = 'contain'
            else:
                image.allow_stretch = True
                image.keep_ratio = True
        except Exception:
            # Defensive: never fail rendering due to a sizing hint.
            pass

        # Store alt text for fallback (always set attribute for testing consistency)
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

        # Return image, but handle loading errors with fallback?
        # For now, AsyncImage handles its own loading.
        return image

    def block_html(self, token: Dict[str, Any], state: Any = None) -> Label:
        """Render block HTML as a plain text Label (showing source).

        Args:
            token: HTML token with 'raw' content
            state: Block state

        Returns:
            Label widget with escaped HTML source
        """
        raw = token.get('raw', '')
        # User requested plain text styling, same as paragraph
        text = escape_kivy_markup(raw.rstrip('\n'))

        label_kwargs = self._build_label_kwargs(
            text=text,
            font_size=self.base_font_size,
            size_hint_y=None,
            size_hint_x=1,
            # Use default font_name (Roboto), not code_font_name
        )

        label = Label(**label_kwargs)
        # Set font scale metadata (same as paragraph)
        label._font_scale = 1.0

        return label

    def newline(self, token: Dict[str, Any], state: Any = None) -> Widget:
        """Render a newline as a small spacer widget.

        Args:
            token: Newline token
            state: Block state

        Returns:
            Small spacer widget
        """
        return Widget(size_hint_y=None, height=5)
