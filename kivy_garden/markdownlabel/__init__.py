"""
MarkdownLabel
=============

A Kivy widget that parses and renders Markdown documents as structured,
interactive Kivy UI elements. It serves as a drop-in replacement for Kivy's
standard Label widget but supports full Markdown syntax.

Example usage::

    from kivy_garden.markdownlabel import MarkdownLabel
    
    label = MarkdownLabel(text='# Hello World\\n\\nThis is **bold** text.')
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import (
    StringProperty, 
    NumericProperty, 
    ColorProperty,
    AliasProperty,
    BooleanProperty,
    OptionProperty,
    VariableListProperty,
    ListProperty,
    ObjectProperty
)

import mistune
from mistune.plugins.table import table
from mistune.plugins.formatting import strikethrough

from .inline_renderer import InlineRenderer
from .kivy_renderer import KivyRenderer
from .markdown_serializer import MarkdownSerializer

__all__ = ('MarkdownLabel', 'InlineRenderer', 'KivyRenderer', 'MarkdownSerializer')

from ._version import __version__


class MarkdownLabel(BoxLayout):
    """A :class:`~kivy.uix.boxlayout.BoxLayout` based widget that renders
    Markdown text as a Kivy widget tree.
    
    The MarkdownLabel parses Markdown text using mistune and renders it as
    a hierarchy of Kivy widgets. It supports headings, paragraphs, lists,
    tables, code blocks, block quotes, images, and inline formatting.
    
    Note:
        MarkdownLabel is NOT a true Label subclass. It provides a Label-compatible
        API for common styling properties, but because Markdown rendering requires
        multiple widgets (headings, lists, tables, images, code blocks), it extends
        BoxLayout instead. Some Label-specific APIs like `texture`, `mipmap`,
        `outline_*`, `base_direction`, and `text_language` are not available.
        
        Properties like `texture_size`, `refs`, and `anchors` are provided as
        aggregated read-only properties from child Label widgets.
    
    Events:
        on_ref_press: Dispatched when a link is clicked. The event data
            contains the URL of the clicked link.
    
    Example::
    
        label = MarkdownLabel(text='# Hello\\n\\nThis is **bold** text.')
        label.bind(on_ref_press=lambda instance, ref: print(f'Clicked: {ref}'))
    """
    
    text = StringProperty('')
    """Markdown text to render.
    
    :attr:`text` is a :class:`~kivy.properties.StringProperty` and defaults
    to an empty string.
    """
    
    base_font_size = NumericProperty(15)
    """Base font size in sp for body text.
    
    Heading sizes are calculated as multiples of this value:
    - h1: 2.5x
    - h2: 2.0x
    - h3: 1.75x
    - h4: 1.5x
    - h5: 1.25x
    - h6: 1.0x
    
    :attr:`base_font_size` is a :class:`~kivy.properties.NumericProperty`
    and defaults to 15.
    """
    
    code_font_name = StringProperty('RobotoMono-Regular')
    """Font name for code blocks and inline code.
    
    :attr:`code_font_name` is a :class:`~kivy.properties.StringProperty`
    and defaults to 'RobotoMono-Regular'.
    """
    
    link_color = ColorProperty([0, 0.5, 1, 1])
    """RGBA color for link text.
    
    :attr:`link_color` is a :class:`~kivy.properties.ColorProperty`
    and defaults to [0, 0.5, 1, 1] (blue).
    """
    
    code_bg_color = ColorProperty([0.15, 0.15, 0.15, 1])
    """RGBA background color for code blocks.
    
    :attr:`code_bg_color` is a :class:`~kivy.properties.ColorProperty`
    and defaults to [0.15, 0.15, 0.15, 1] (dark gray).
    """
    
    def _get_font_size(self):
        """Getter for font_size alias property."""
        return self.base_font_size
    
    def _set_font_size(self, value):
        """Setter for font_size alias property."""
        self.base_font_size = value
    
    font_size = AliasProperty(
        _get_font_size,
        _set_font_size,
        bind=['base_font_size']
    )
    """Alias for :attr:`base_font_size` for Label API compatibility.
    
    Setting this property updates :attr:`base_font_size`, and reading it
    returns the current :attr:`base_font_size` value. This allows
    MarkdownLabel to be used as a drop-in replacement for Label.
    
    :attr:`font_size` is an :class:`~kivy.properties.AliasProperty` that
    maps to :attr:`base_font_size`.
    """
    
    # No-op properties for Label API compatibility
    # These are accepted but have no effect on rendering since
    # Markdown syntax controls formatting
    
    bold = BooleanProperty(False)
    """No-op property for Label API compatibility.
    
    This property is accepted but has no effect on rendering.
    Markdown syntax (e.g., **text**) controls bold formatting.
    
    :attr:`bold` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to False.
    """
    
    italic = BooleanProperty(False)
    """No-op property for Label API compatibility.
    
    This property is accepted but has no effect on rendering.
    Markdown syntax (e.g., *text*) controls italic formatting.
    
    :attr:`italic` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to False.
    """
    
    underline = BooleanProperty(False)
    """No-op property for Label API compatibility.
    
    This property is accepted but has no effect on rendering.
    
    :attr:`underline` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to False.
    """
    
    strikethrough = BooleanProperty(False)
    """No-op property for Label API compatibility.
    
    This property is accepted but has no effect on rendering.
    Markdown syntax (e.g., ~~text~~) controls strikethrough formatting.
    
    :attr:`strikethrough` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to False.
    """
    
    markup = BooleanProperty(True)
    """No-op property for Label API compatibility.
    
    This property is accepted but has no effect on rendering.
    MarkdownLabel always uses markup internally for rendering.
    The value is always treated as True regardless of what is set.
    
    :attr:`markup` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to True.
    """
    
    # Forwarding properties - these are passed to KivyRenderer and applied to internal Labels
    
    font_name = StringProperty('Roboto')
    """Font name for body text in internal Labels.
    
    This font is applied to all internal Label widgets except code blocks
    and inline code, which use :attr:`code_font_name`.
    
    :attr:`font_name` is a :class:`~kivy.properties.StringProperty`
    and defaults to 'Roboto'.
    """
    
    color = ColorProperty([1, 1, 1, 1])
    """RGBA color for body text in internal Labels.
    
    This color is applied to all internal Label widgets for body text.
    Links use :attr:`link_color` instead.
    
    :attr:`color` is a :class:`~kivy.properties.ColorProperty`
    and defaults to [1, 1, 1, 1] (white).
    """
    
    line_height = NumericProperty(1.0)
    """Line height multiplier for internal Labels.
    
    This value is applied to all internal Label widgets to control
    spacing between lines of text.
    
    :attr:`line_height` is a :class:`~kivy.properties.NumericProperty`
    and defaults to 1.0.
    """
    
    halign = OptionProperty('auto', options=['left', 'center', 'right', 'justify', 'auto'])
    """Horizontal alignment for text in internal Labels.
    
    This value is applied to all internal Label widgets for paragraphs
    and headings. When set to 'auto', left alignment is used.
    
    :attr:`halign` is an :class:`~kivy.properties.OptionProperty`
    and defaults to 'auto'.
    """
    
    valign = OptionProperty('bottom', options=['bottom', 'middle', 'center', 'top'])
    """Vertical alignment for text in internal Labels.
    
    This value is applied to all internal Label widgets where applicable.
    
    :attr:`valign` is an :class:`~kivy.properties.OptionProperty`
    and defaults to 'bottom'.
    """
    
    padding = VariableListProperty([0, 0, 0, 0])
    """Padding for the MarkdownLabel container.
    
    Can be specified as a single value (applied to all sides),
    two values [horizontal, vertical], or four values [left, top, right, bottom].
    
    :attr:`padding` is a :class:`~kivy.properties.VariableListProperty`
    and defaults to [0, 0, 0, 0].
    """
    
    text_size = ListProperty([None, None])
    """Bounding box size for text wrapping.
    
    When a width is specified, internal Labels will constrain text to that width.
    When [None, None], text flows naturally without width constraints.
    
    :attr:`text_size` is a :class:`~kivy.properties.ListProperty`
    and defaults to [None, None].
    """
    
    unicode_errors = OptionProperty('replace', options=['strict', 'replace', 'ignore'])
    """Unicode error handling mode for internal Labels.
    
    This value is applied to all internal Label widgets to control
    how unicode encoding errors are handled.
    
    Options:
        - 'strict': Raise an exception on encoding errors
        - 'replace': Replace invalid characters with a replacement character
        - 'ignore': Ignore invalid characters
    
    :attr:`unicode_errors` is an :class:`~kivy.properties.OptionProperty`
    and defaults to 'replace'.
    """
    
    strip = BooleanProperty(False)
    """Strip leading and trailing whitespace from each displayed line.
    
    When True, internal Labels will strip leading and trailing whitespace
    from each line of text. When False, whitespace is preserved as specified
    in the Markdown source.
    
    :attr:`strip` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to False.
    """
    
    # Advanced font properties
    
    font_family = StringProperty(None, allownone=True)
    """Font family for internal Labels.
    
    This value is forwarded to all internal Label widgets.
    
    :attr:`font_family` is a :class:`~kivy.properties.StringProperty`
    and defaults to None.
    """
    
    font_context = StringProperty(None, allownone=True)
    """Font context for internal Labels.
    
    This value is forwarded to all internal Label widgets.
    
    :attr:`font_context` is a :class:`~kivy.properties.StringProperty`
    and defaults to None.
    """
    
    font_features = StringProperty('')
    """Font features for internal Labels.
    
    This value is forwarded to all internal Label widgets.
    OpenType font features can be specified as a string.
    
    :attr:`font_features` is a :class:`~kivy.properties.StringProperty`
    and defaults to ''.
    """
    
    font_hinting = OptionProperty('normal', options=[None, 'normal', 'light', 'mono'], allownone=True)
    """Font hinting mode for internal Labels.
    
    This value is forwarded to all internal Label widgets.
    
    Options:
        - None: No hinting
        - 'normal': Normal hinting (default)
        - 'light': Light hinting
        - 'mono': Monochrome hinting
    
    :attr:`font_hinting` is an :class:`~kivy.properties.OptionProperty`
    and defaults to 'normal'.
    """
    
    font_kerning = BooleanProperty(True)
    """Font kerning for internal Labels.
    
    When True, kerning is enabled for text rendering.
    This value is forwarded to all internal Label widgets.
    
    :attr:`font_kerning` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to True.
    """
    
    font_blended = BooleanProperty(True)
    """Font blending for internal Labels.
    
    When True, blended rendering is used for smoother text.
    This value is forwarded to all internal Label widgets.
    
    :attr:`font_blended` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to True.
    """
    
    disabled_color = ColorProperty([1, 1, 1, 0.3])
    """RGBA color for text when the widget is disabled.
    
    When :attr:`disabled` is True, this color is applied to all internal
    Label widgets instead of :attr:`color`.
    
    :attr:`disabled_color` is a :class:`~kivy.properties.ColorProperty`
    and defaults to [1, 1, 1, 0.3] (semi-transparent white).
    """
    
    # Truncation properties
    
    shorten = BooleanProperty(False)
    """Enable text shortening with ellipsis.
    
    When True and text_size is constrained, text that exceeds the bounds
    will be truncated with an ellipsis.
    
    :attr:`shorten` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to False.
    """
    
    max_lines = NumericProperty(0)
    """Maximum number of lines to display.
    
    When set to a positive integer, limits visible content to that number
    of lines. A value of 0 means no limit.
    
    :attr:`max_lines` is a :class:`~kivy.properties.NumericProperty`
    and defaults to 0.
    """
    
    shorten_from = OptionProperty('center', options=['left', 'center', 'right'])
    """Direction from which to truncate text when shortening.
    
    Options:
        - 'left': Truncate from the left side
        - 'center': Truncate from the center (default)
        - 'right': Truncate from the right side
    
    :attr:`shorten_from` is an :class:`~kivy.properties.OptionProperty`
    and defaults to 'center'.
    """
    
    split_str = StringProperty('')
    """String used as word boundary for shortening.
    
    When shortening text, this string is used to determine word boundaries.
    An empty string means split on any character.
    
    :attr:`split_str` is a :class:`~kivy.properties.StringProperty`
    and defaults to ''.
    """
    
    auto_size_height = BooleanProperty(True)
    """Control automatic height sizing behavior.
    
    When True (default):
        - size_hint_y is set to None
        - height is bound to minimum_height
        - Widget auto-sizes to fit content
    
    When False:
        - size_hint_y is preserved (user-specified or default)
        - height is NOT bound to minimum_height
        - Widget participates in normal size hint layout
    
    This property allows MarkdownLabel to be used in layouts that expect
    widgets to participate in size hints by setting auto_size_height=False.
    
    :attr:`auto_size_height` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to True.
    """
    
    # Read-only aggregated properties from child Labels
    
    def _get_texture_size(self):
        """Compute aggregate texture_size from all child Labels.
        
        Returns the bounding box size that encompasses all child Label textures.
        Width is the maximum width of any child, height is the sum of all heights.
        """
        if not self.children:
            return [0, 0]
        
        max_width = 0
        total_height = 0
        
        def collect_sizes(widget):
            nonlocal max_width, total_height
            if isinstance(widget, Label) and hasattr(widget, 'texture_size'):
                ts = widget.texture_size
                if ts[0] > max_width:
                    max_width = ts[0]
                total_height += ts[1]
            if hasattr(widget, 'children'):
                for child in widget.children:
                    collect_sizes(child)
        
        for child in self.children:
            collect_sizes(child)
        
        return [max_width, total_height]
    
    texture_size = AliasProperty(_get_texture_size, bind=['children', 'text'])
    """Aggregated texture size from all child Label widgets.
    
    Returns the bounding box size [width, height] that encompasses all child
    Label textures. Width is the maximum width of any child Label, height is
    the sum of all child Label heights.
    
    Note:
        This is a read-only property. Unlike Kivy's Label.texture_size, it
        represents the aggregate of multiple internal Labels, not a single
        texture. The value may not update immediately after text changes
        due to texture rendering being asynchronous.
    
    :attr:`texture_size` is a read-only :class:`~kivy.properties.AliasProperty`.
    """
    
    def _get_refs(self):
        """Aggregate refs from all child Labels.
        
        Returns a merged dictionary of all ref positions from child Labels.
        Keys are ref names (URLs), values are lists of bounding box coordinates.
        """
        refs = {}
        
        def collect_refs(widget):
            if isinstance(widget, Label) and hasattr(widget, 'refs'):
                for ref_name, ref_boxes in widget.refs.items():
                    if ref_name not in refs:
                        refs[ref_name] = []
                    refs[ref_name].extend(ref_boxes)
            if hasattr(widget, 'children'):
                for child in widget.children:
                    collect_refs(child)
        
        for child in self.children:
            collect_refs(child)
        
        return refs
    
    refs = AliasProperty(_get_refs, bind=['children', 'text'])
    """Aggregated refs from all child Label widgets.
    
    Returns a dictionary mapping ref names (typically URLs) to lists of
    bounding box coordinates where those refs appear. This aggregates
    refs from all internal Label widgets.
    
    Note:
        Coordinates are relative to each child Label's position, not the
        MarkdownLabel container. For hit testing, use the `on_ref_press`
        event instead, which handles coordinate translation automatically.
    
    :attr:`refs` is a read-only :class:`~kivy.properties.AliasProperty`.
    """
    
    def _get_anchors(self):
        """Aggregate anchors from all child Labels.
        
        Returns a merged dictionary of all anchor positions from child Labels.
        Keys are anchor names, values are position tuples.
        """
        anchors = {}
        
        def collect_anchors(widget):
            if isinstance(widget, Label) and hasattr(widget, 'anchors'):
                anchors.update(widget.anchors)
            if hasattr(widget, 'children'):
                for child in widget.children:
                    collect_anchors(child)
        
        for child in self.children:
            collect_anchors(child)
        
        return anchors
    
    anchors = AliasProperty(_get_anchors, bind=['children', 'text'])
    """Aggregated anchors from all child Label widgets.
    
    Returns a dictionary mapping anchor names to position tuples. This
    aggregates anchors from all internal Label widgets.
    
    Note:
        Coordinates are relative to each child Label's position, not the
        MarkdownLabel container.
    
    :attr:`anchors` is a read-only :class:`~kivy.properties.AliasProperty`.
    """
    
    __events__ = ('on_ref_press',)
    
    def __init__(self, **kwargs):
        super(MarkdownLabel, self).__init__(**kwargs)
        self.orientation = 'vertical'
        
        # Store user's size_hint_y value before potential override
        self._user_size_hint_y = kwargs.get('size_hint_y', 1)
        
        # Apply auto-sizing only when auto_size_height is True
        if self.auto_size_height:
            self.size_hint_y = None
            self.bind(minimum_height=self.setter('height'))
        
        # Bind auto_size_height changes to handler
        self.bind(auto_size_height=self._on_auto_size_height_changed)
        
        # Store the parsed AST tokens
        self._ast_tokens = []
        
        # Create mistune parser with plugins
        self._parser = mistune.create_markdown(renderer=None)
        # Enable table and strikethrough plugins
        table(self._parser)
        strikethrough(self._parser)
        
        # Bind text property to rebuild widgets
        self.bind(text=self._on_text_changed)
        
        # Bind forwarding properties to trigger widget rebuild
        self.bind(font_name=self._on_style_changed)
        self.bind(color=self._on_style_changed)
        self.bind(line_height=self._on_style_changed)
        self.bind(halign=self._on_style_changed)
        self.bind(valign=self._on_style_changed)
        self.bind(text_size=self._on_style_changed)
        self.bind(unicode_errors=self._on_style_changed)
        self.bind(strip=self._on_style_changed)
        self.bind(font_family=self._on_style_changed)
        self.bind(font_context=self._on_style_changed)
        self.bind(font_features=self._on_style_changed)
        self.bind(font_hinting=self._on_style_changed)
        self.bind(font_kerning=self._on_style_changed)
        self.bind(font_blended=self._on_style_changed)
        self.bind(disabled=self._on_style_changed)
        self.bind(disabled_color=self._on_style_changed)
        self.bind(shorten=self._on_style_changed)
        self.bind(max_lines=self._on_style_changed)
        self.bind(shorten_from=self._on_style_changed)
        self.bind(split_str=self._on_style_changed)
        self.bind(padding=self._on_style_changed)
        
        # Bind padding to the container (self is a BoxLayout)
        self.bind(padding=self._on_padding_changed)
        
        # Initial build if text is provided
        if self.text:
            self._rebuild_widgets()
    
    def _on_text_changed(self, instance, value):
        """Callback when text property changes."""
        self._rebuild_widgets()
    
    def _on_style_changed(self, instance, value):
        """Callback when a styling property changes."""
        self._rebuild_widgets()
    
    def _on_padding_changed(self, instance, value):
        """Callback when padding property changes.
        
        Note: padding is applied directly to the BoxLayout (self),
        not passed to the renderer.
        """
        # BoxLayout handles padding directly, no rebuild needed
        pass
    
    def _on_auto_size_height_changed(self, instance, value):
        """Handle auto_size_height property changes."""
        if value:
            # Enable auto-sizing
            self.size_hint_y = None
            self.bind(minimum_height=self.setter('height'))
        else:
            # Disable auto-sizing
            self.unbind(minimum_height=self.setter('height'))
            self.size_hint_y = self._user_size_hint_y
    
    def _rebuild_widgets(self):
        """Parse the Markdown text and rebuild the widget tree."""
        # Clear existing children
        self.clear_widgets()
        
        # Handle empty text
        if not self.text:
            self._ast_tokens = []
            return
        
        # Parse Markdown to AST
        # mistune.parse() returns a tuple of (tokens, state)
        result = self._parser.parse(self.text)
        self._ast_tokens = result[0] if isinstance(result, tuple) else result
        
        # Create renderer with current styling properties
        renderer = KivyRenderer(
            base_font_size=self.base_font_size,
            code_font_name=self.code_font_name,
            link_color=list(self.link_color),
            code_bg_color=list(self.code_bg_color),
            font_name=self.font_name,
            color=list(self.color),
            line_height=self.line_height,
            halign=self.halign,
            valign=self.valign,
            text_size=list(self.text_size) if self.text_size else [None, None],
            unicode_errors=self.unicode_errors,
            strip=self.strip,
            font_family=self.font_family,
            font_context=self.font_context,
            font_features=self.font_features,
            font_hinting=self.font_hinting,
            font_kerning=self.font_kerning,
            font_blended=self.font_blended,
            disabled=self.disabled,
            disabled_color=list(self.disabled_color),
            shorten=self.shorten,
            max_lines=int(self.max_lines),
            shorten_from=self.shorten_from,
            split_str=self.split_str,
            padding=list(self.padding)
        )
        
        # Render AST to widget tree
        content = renderer(self._ast_tokens, None)
        
        # Bind ref_press events from child Labels to bubble up
        self._bind_ref_press_events(content)
        
        # Add rendered content
        # Note: content.children is in reverse order, so we reverse it to maintain document order
        for child in reversed(list(content.children)):
            content.remove_widget(child)
            self.add_widget(child)
    
    def _bind_ref_press_events(self, widget):
        """Recursively bind on_ref_press events from child Labels.
        
        Args:
            widget: Widget to search for Labels with ref markup
        """
        if isinstance(widget, Label) and widget.markup:
            widget.bind(on_ref_press=self._on_child_ref_press)
        
        # Recursively bind for container widgets
        if hasattr(widget, 'children'):
            for child in widget.children:
                self._bind_ref_press_events(child)
    
    def _on_child_ref_press(self, instance, ref):
        """Handle ref_press from child Label and bubble up.
        
        Args:
            instance: The Label that was clicked
            ref: The URL/reference string
        """
        self.dispatch('on_ref_press', ref)
    
    def on_ref_press(self, ref):
        """Event handler for link clicks.
        
        Override this method or bind to the event to handle link clicks.
        
        Args:
            ref: The URL of the clicked link
        """
        pass
    
    def get_ast(self):
        """Return the parsed AST tokens.
        
        Returns:
            List of AST token dictionaries from mistune
        """
        return self._ast_tokens
    
    def to_markdown(self):
        """Serialize the current AST back to Markdown text.
        
        Returns:
            Markdown string representation of the current AST
        """
        serializer = MarkdownSerializer()
        return serializer.serialize(self._ast_tokens)
