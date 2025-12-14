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
from kivy.clock import Clock
from kivy.properties import (
    StringProperty, 
    NumericProperty, 
    ColorProperty,
    AliasProperty,
    BooleanProperty,
    OptionProperty,
    VariableListProperty,
    ListProperty,
    ObjectProperty,
    DictProperty
)

import mistune
from mistune.plugins.table import table
from mistune.plugins.formatting import strikethrough

from kivy.uix.stencilview import StencilView

from .inline_renderer import InlineRenderer
from .kivy_renderer import KivyRenderer
from .markdown_serializer import MarkdownSerializer

__all__ = ('MarkdownLabel', 'InlineRenderer', 'KivyRenderer', 'MarkdownSerializer')


class _ClippingContainer(StencilView):
    """Internal container that clips content to its bounds.
    
    This class extends StencilView to provide content clipping when:
    - text_size[1] is not None (height-constrained), OR
    - strict_label_mode is True with a fixed height
    
    The StencilView uses stencil graphics instructions to efficiently clip
    any drawing outside its bounding box.
    
    Note: StencilView is not a Layout, so it doesn't have minimum_height.
    The height must be set explicitly by the parent MarkdownLabel.
    """
    
    def __init__(self, **kwargs):
        super(_ClippingContainer, self).__init__(**kwargs)
        # Disable size_hint_y so we can set explicit height
        self.size_hint_y = None

from ._version import __version__


class MarkdownLabel(BoxLayout):
    """A :class:`~kivy.uix.boxlayout.BoxLayout` based widget that renders
    Markdown text as a Kivy widget tree.
    
    The MarkdownLabel parses Markdown text using mistune and renders it as
    a hierarchy of Kivy widgets. It supports headings, paragraphs, lists,
    tables, code blocks, block quotes, images, and inline formatting.
    
    Note:
        MarkdownLabel is NOT a true Label subclass. It mirrors most Label styling
        properties (including outline, mipmap, base_direction, text_language)
        but extends BoxLayout because Markdown rendering builds multiple widgets
        (headings, lists, tables, images, code blocks). The `texture` property is
        available as an aggregated texture when ``aggregate_texture_enabled`` is True.
        Properties like `texture_size`, `refs`, and `anchors` are provided as
        aggregated read-only properties from child Label widgets.
    
    Events:
        on_ref_press: Dispatched when a link is clicked. The event data
            contains the URL of the clicked link.
    
    Example::
    
        label = MarkdownLabel(text='# Hello\\n\\nThis is **bold** text.')
        label.bind(on_ref_press=lambda instance, ref: print(f'Clicked: {ref}'))
    """
    
    # Property categories for efficient updates
    # Style-only properties can be updated in-place without rebuilding widgets
    # Structure properties require a full widget tree rebuild
    
    STYLE_ONLY_PROPERTIES = frozenset({
        'color',
        'halign',
        'valign',
        'line_height',
        'disabled',
        'disabled_color',
    })
    """Properties that affect only visual styling and can be updated in-place.
    
    Changes to these properties can update existing child widgets without
    rebuilding the entire widget tree, improving performance.
    """
    
    STRUCTURE_PROPERTIES = frozenset({
        'text',
        'font_name',
        'code_font_name',
        'link_style',
        'text_size',
        'strict_label_mode',
        'padding',
        'text_padding',
        'outline_width',
        'outline_color',
        'disabled_outline_color',
        'mipmap',
        'base_direction',
        'text_language',
        'limit_render_to_text_bbox',
    })
    """Properties that affect widget structure and require a full rebuild.
    
    Changes to these properties require rebuilding the widget tree because
    they affect the structure, layout, or fundamental rendering of content.
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

    link_style = OptionProperty(
        'unstyled',
        options=['unstyled', 'styled']
    )
    """Link rendering style.
    
    - 'unstyled' (default): produces Label-like refs without forced color/underline.
    - 'styled': applies link_color and underline for visual emphasis.
    
    :attr:`link_style` is a :class:`~kivy.properties.OptionProperty`
    and defaults to 'unstyled'.
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

    text_padding = VariableListProperty([0, 0, 0, 0])
    """Padding applied to internal Label widgets.
    
    This mirrors :attr:`kivy.uix.label.Label.padding` without affecting the
    MarkdownLabel container layout. Use this to inset rendered text while
    keeping outer BoxLayout padding independent.
    
    :attr:`text_padding` is a :class:`~kivy.properties.VariableListProperty`
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

    outline_width = NumericProperty(None, allownone=True)
    """Outline width for text rendering (mirrors Label.outline_width)."""

    outline_color = ColorProperty([0, 0, 0, 1])
    """Outline color for text (mirrors Label.outline_color)."""

    disabled_outline_color = ColorProperty([0, 0, 0, 1])
    """Outline color when the widget is disabled (Label.disabled_outline_color)."""

    mipmap = BooleanProperty(False)
    """Enable mipmapping on text textures (Label.mipmap)."""

    base_direction = OptionProperty(
        None,
        options=['ltr', 'rtl', 'weak_rtl', 'weak_ltr', None],
        allownone=True
    )
    """Base text direction hint (Label.base_direction)."""

    text_language = StringProperty(None, allownone=True)
    """Language tag for text shaping (Label.text_language)."""

    limit_render_to_text_bbox = BooleanProperty(False)
    """Limit rendering to text bounding box (Label.limit_render_to_text_bbox)."""
    
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
    
    ellipsis_options = DictProperty({})
    """Ellipsis options for text shortening.
    
    This dictionary is forwarded to all child Labels that support it.
    See Kivy Label documentation for available options.
    
    :attr:`ellipsis_options` is a :class:`~kivy.properties.DictProperty`
    and defaults to {}.
    """
    
    # Internal property to trigger texture_size updates when children resize
    _texture_size_version = NumericProperty(0)
    """Internal version counter to trigger texture_size recalculation.
    
    This property is incremented when child widget sizes change,
    causing the texture_size AliasProperty to be recalculated.
    """
    
    auto_size_height = BooleanProperty(False)
    """Control automatic height sizing behavior.
    
    When True:
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
    and defaults to False for Label-like sizing semantics.
    """
    
    strict_label_mode = BooleanProperty(False)
    """Enable strict Label API compatibility mode.
    
    This property controls how MarkdownLabel handles sizing and text_size
    semantics, allowing it to behave more like Kivy's standard Label widget.
    
    When False (default):
        - auto_size_height can be toggled on explicitly (default is off)
        - Internal Labels bind their width to the parent for text wrapping
        - Widget uses Markdown-friendly auto-wrap behavior by default
    
    When True (strict Label compatibility mode):
        - auto_size_height behavior is disabled (size_hint_y is preserved)
        - Internal Labels do NOT automatically bind width to parent
        - text_size bindings only apply when text_size is explicitly set
        - Widget follows Label's exact sizing semantics
        - Ideal for drop-in replacement scenarios where Label sizing is expected
    
    Use strict_label_mode=True when you need MarkdownLabel to behave exactly
    like a standard Label for layout purposes, such as when replacing Labels
    in existing kv files or applications.
    
    :attr:`strict_label_mode` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to False.
    """
    
    # Read-only aggregated properties from child Labels
    
    def _get_texture_size(self):
        """Compute aggregate texture_size from all descendant widgets.
        
        Returns the bounding box size that encompasses all content:
        - Width: maximum width of any descendant
        - Height: sum of all descendant heights
        
        Includes: Labels, AsyncImages, GridLayouts (tables),
        BoxLayouts (code blocks, quotes), and Widgets (spacers, rules).
        """
        from kivy.uix.image import AsyncImage
        from kivy.uix.gridlayout import GridLayout
        from kivy.uix.widget import Widget
        
        if not self.children:
            return [0, 0]
        
        max_width = 0
        total_height = 0
        
        def collect_sizes(widget, visited=None):
            """Recursively collect sizes from widget tree.
            
            Args:
                widget: Widget to collect size from
                visited: Set of already visited widgets to prevent cycles
            """
            nonlocal max_width, total_height
            
            if visited is None:
                visited = set()
            
            # Prevent infinite loops from circular references
            widget_id = id(widget)
            if widget_id in visited:
                return
            visited.add(widget_id)
            
            # For Labels, use texture_size
            if isinstance(widget, Label) and hasattr(widget, 'texture_size'):
                ts = widget.texture_size
                if ts[0] > max_width:
                    max_width = ts[0]
                total_height += ts[1]
            # For AsyncImage, use actual size
            elif isinstance(widget, AsyncImage):
                if widget.width > max_width:
                    max_width = widget.width
                total_height += widget.height
            # For GridLayout (tables), use minimum_size
            elif isinstance(widget, GridLayout):
                if hasattr(widget, 'minimum_width') and widget.minimum_width:
                    if widget.minimum_width > max_width:
                        max_width = widget.minimum_width
                if hasattr(widget, 'minimum_height') and widget.minimum_height:
                    total_height += widget.minimum_height
            # For BoxLayout containers (code blocks, quotes), recurse into children
            elif isinstance(widget, BoxLayout):
                for child in widget.children:
                    collect_sizes(child, visited)
            # For plain Widgets (spacers, rules), use height
            elif isinstance(widget, Widget):
                total_height += widget.height
        
        for child in self.children:
            collect_sizes(child)
        
        return [max_width, total_height]
    
    texture_size = AliasProperty(
        _get_texture_size,
        bind=['children', 'text', '_texture_size_version']
    )
    """Aggregated texture size from all descendant widgets.
    
    Returns the bounding box size [width, height] that encompasses all
    descendant widgets including Labels, Images, Tables, Code blocks,
    and spacer widgets.
    
    - Width: maximum width of any descendant
    - Height: sum of all descendant heights
    
    Note:
        This is a read-only property. Unlike Kivy's Label.texture_size, it
        represents the aggregate of multiple internal widgets, not a single
        texture. The value updates when child widget sizes change.
    
    :attr:`texture_size` is a read-only :class:`~kivy.properties.AliasProperty`.
    """

    aggregate_texture_enabled = BooleanProperty(False)
    """Enable rendering the entire widget tree to a single texture.
    
    When True, the :attr:`texture` property returns an aggregated texture
    produced via :meth:`export_as_image`. This is opt-in and may be
    expensive; it is disabled by default to avoid unnecessary FBO work.
    """

    def _get_texture(self):
        """Return an aggregated texture when enabled."""
        if not self.aggregate_texture_enabled:
            return None
        
        try:
            image = self.export_as_image()
        except Exception:
            return None
        
        return getattr(image, 'texture', None)
    
    texture = AliasProperty(
        _get_texture,
        bind=['aggregate_texture_enabled', '_texture_size_version', 'size', 'pos', 'children', 'text']
    )
    """Aggregated texture mirroring Label.texture when enabled."""
    
    def _get_refs(self):
        """Aggregate refs from child Labels using Label-style coordinates.
        
        Returned bounding boxes are translated from each Label's texture space
        into the MarkdownLabel's local coordinate system, mirroring how
        ``Label.refs`` is interpreted when converted to widget coordinates.
        """
        refs = {}
        
        def get_parent_offset(widget):
            """Return cumulative parent offset relative to MarkdownLabel."""
            offset_x = 0
            offset_y = 0
            current = widget.parent
            while current is not None and current is not self:
                offset_x += current.x
                offset_y += current.y
                current = current.parent
            return offset_x, offset_y
        
        def translate_box(label, box):
            """Translate a ref box from label texture space to local coords."""
            tex_w, tex_h = getattr(label, 'texture_size', (0, 0))
            if not tex_w and not tex_h:
                tex_w, tex_h = label.width, label.height
            
            parent_offset_x, parent_offset_y = get_parent_offset(label)
            base_x = parent_offset_x + (label.center_x - tex_w / 2.0)
            base_y = parent_offset_y + (label.center_y + tex_h / 2.0)
            
            x1, y1, x2, y2 = box
            return [
                base_x + x1,
                base_y - y1,
                base_x + x2,
                base_y - y2,
            ]
        
        def collect_refs(widget):
            if isinstance(widget, Label) and hasattr(widget, 'refs') and widget.refs:
                for ref_name, ref_boxes in widget.refs.items():
                    if ref_name not in refs:
                        refs[ref_name] = []
                    for box in ref_boxes:
                        refs[ref_name].append(translate_box(widget, box))
            
            if hasattr(widget, 'children'):
                for child in widget.children:
                    collect_refs(child)
        
        for child in self.children:
            collect_refs(child)
        
        return refs
    
    refs = AliasProperty(
        _get_refs,
        bind=['children', 'text', '_texture_size_version']
    )
    """Aggregated refs from all child Label widgets.
    
    Returns a dictionary mapping ref names (typically URLs) to lists of
    bounding box coordinates where those refs appear. This aggregates
    refs from all internal Label widgets.
    
    Coordinates are translated to MarkdownLabel's local coordinate space,
    making them suitable for hit testing and overlay positioning.
    
    :attr:`refs` is a read-only :class:`~kivy.properties.AliasProperty`.
    """
    
    def _get_anchors(self):
        """Aggregate anchors from child Labels using Label-style coordinates.
        
        Anchor positions are translated from each Label's texture space into
        MarkdownLabel's local coordinates to mirror ``Label.anchors`` usage.
        """
        anchors = {}
        
        def get_parent_offset(widget):
            """Return cumulative parent offset relative to MarkdownLabel."""
            offset_x = 0
            offset_y = 0
            current = widget.parent
            while current is not None and current is not self:
                offset_x += current.x
                offset_y += current.y
                current = current.parent
            return offset_x, offset_y
        
        def translate_anchor(label, pos):
            """Translate an anchor point from label texture space to local coords."""
            tex_w, tex_h = getattr(label, 'texture_size', (0, 0))
            if not tex_w and not tex_h:
                tex_w, tex_h = label.width, label.height
            
            parent_offset_x, parent_offset_y = get_parent_offset(label)
            base_x = parent_offset_x + (label.center_x - tex_w / 2.0)
            base_y = parent_offset_y + (label.center_y + tex_h / 2.0)
            
            return (
                base_x + pos[0],
                base_y - pos[1],
            )
        
        def collect_anchors(widget):
            if isinstance(widget, Label) and hasattr(widget, 'anchors') and widget.anchors:
                for anchor_name, pos in widget.anchors.items():
                    anchors[anchor_name] = translate_anchor(widget, pos)
            
            if hasattr(widget, 'children'):
                for child in widget.children:
                    collect_anchors(child)
        
        for child in self.children:
            collect_anchors(child)
        
        return anchors
    
    anchors = AliasProperty(
        _get_anchors,
        bind=['children', 'text', '_texture_size_version']
    )
    """Aggregated anchors from all child Label widgets.
    
    Returns a dictionary mapping anchor names to position tuples. This
    aggregates anchors from all internal Label widgets.
    
    Coordinates are translated to MarkdownLabel's local coordinate space,
    making them suitable for positioning and overlay calculations.
    
    :attr:`anchors` is a read-only :class:`~kivy.properties.AliasProperty`.
    """
    
    __events__ = ('on_ref_press',)
    
    def __init__(self, **kwargs):
        super(MarkdownLabel, self).__init__(**kwargs)
        self.orientation = 'vertical'
        
        # Deferred rebuild system for batching property changes
        # _pending_rebuild tracks whether a rebuild is scheduled
        self._pending_rebuild = False
        # _rebuild_trigger is a Clock trigger for deferred rebuilds
        # timeout=-1 means it fires on the next frame
        self._rebuild_trigger = Clock.create_trigger(
            self._do_rebuild, timeout=-1
        )
        
        # Store user's size_hint_y value before potential override
        self._user_size_hint_y = kwargs.get('size_hint_y', 1)
        
        # Apply auto-sizing only when auto_size_height is True
        # AND strict_label_mode is False
        if self.auto_size_height and not self.strict_label_mode:
            self.size_hint_y = None
            self.bind(minimum_height=self.setter('height'))
        elif self.strict_label_mode:
            # In strict mode, preserve size_hint_y and don't bind height
            self.size_hint_y = self._user_size_hint_y
        
        # Bind auto_size_height changes to handler
        self.bind(auto_size_height=self._on_auto_size_height_changed)
        
        # Bind strict_label_mode changes to handler
        self.bind(strict_label_mode=self._on_strict_label_mode_changed)
        
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
        # Bind style-only properties (can be updated in-place)
        self.bind(base_font_size=self._make_style_callback('base_font_size'))
        self.bind(color=self._make_style_callback('color'))
        self.bind(line_height=self._make_style_callback('line_height'))
        self.bind(halign=self._make_style_callback('halign'))
        self.bind(valign=self._make_style_callback('valign'))
        self.bind(disabled=self._make_style_callback('disabled'))
        self.bind(disabled_color=self._make_style_callback('disabled_color'))

        # Bind structure properties (require full rebuild)
        self.bind(font_name=self._make_style_callback('font_name'))
        self.bind(link_style=self._make_style_callback('link_style'))
        self.bind(text_size=self._make_style_callback('text_size'))
        self.bind(padding=self._make_style_callback('padding'))
        self.bind(text_padding=self._make_style_callback('text_padding'))
        self.bind(outline_width=self._make_style_callback('outline_width'))
        self.bind(outline_color=self._make_style_callback('outline_color'))
        self.bind(disabled_outline_color=self._make_style_callback('disabled_outline_color'))
        self.bind(mipmap=self._make_style_callback('mipmap'))
        self.bind(base_direction=self._make_style_callback('base_direction'))
        self.bind(text_language=self._make_style_callback('text_language'))
        self.bind(limit_render_to_text_bbox=self._make_style_callback('limit_render_to_text_bbox'))

        # Bind other properties (require full rebuild)
        self.bind(unicode_errors=self._make_style_callback('unicode_errors'))
        self.bind(strip=self._make_style_callback('strip'))
        self.bind(font_family=self._make_style_callback('font_family'))
        self.bind(font_context=self._make_style_callback('font_context'))
        self.bind(font_features=self._make_style_callback('font_features'))
        self.bind(font_hinting=self._make_style_callback('font_hinting'))
        self.bind(font_kerning=self._make_style_callback('font_kerning'))
        self.bind(font_blended=self._make_style_callback('font_blended'))
        self.bind(shorten=self._make_style_callback('shorten'))
        self.bind(max_lines=self._make_style_callback('max_lines'))
        self.bind(shorten_from=self._make_style_callback('shorten_from'))
        self.bind(split_str=self._make_style_callback('split_str'))
        self.bind(ellipsis_options=self._make_style_callback('ellipsis_options'))
        
        # Bind padding to the container (self is a BoxLayout)
        self.bind(padding=self._on_padding_changed)
        
        # Initial build if text is provided
        if self.text:
            self._rebuild_widgets()
    
    def _on_text_changed(self, instance, value):
        """Callback when text property changes.
        
        Uses deferred rebuild to batch multiple text changes within the
        same frame into a single rebuild operation.
        """
        self._schedule_rebuild()

    def _make_style_callback(self, prop_name):
        """Create a callback for a specific property that tracks which changed.

        This factory method creates callbacks that know which property
        triggered them, enabling conditional updates based on property type.

        Args:
            prop_name: Name of the property this callback is for

        Returns:
            Callback function that handles the property change
        """
        def callback(instance, value):
            self._on_style_changed(instance, value, prop_name)
        return callback

    def _on_style_changed(self, instance, value, prop_name=None):
        """Callback when a styling property changes.

        For style-only properties (font_size, color, halign, valign,
        line_height, disabled, disabled_color), updates are applied
        in-place without rebuilding the widget tree.

        For structure properties (text, font_name, code_font_name,
        text_size, strict_label_mode, padding) and other properties,
        a deferred widget rebuild is scheduled to batch multiple changes.

        Args:
            instance: The widget instance (self)
            value: The new property value
            prop_name: Name of the property that changed (optional)
        """
        # If we don't know which property changed, schedule a rebuild
        if prop_name is None:
            self._schedule_rebuild()
            return

        # Check if this is a font size property that can be updated in-place
        if prop_name in ('base_font_size', 'font_size'):
            # Only update in-place if we have children to update
            if self.children:
                self._update_font_sizes_in_place()
            # No rebuild needed for font size changes
        # Check if this is a style-only property that can be updated in-place
        elif prop_name in self.STYLE_ONLY_PROPERTIES:
            # Only update in-place if we have children to update
            if self.children:
                self._update_styles_in_place()
            # No rebuild needed for style-only changes
        else:
            # Structure property or other - schedule deferred rebuild
            self._schedule_rebuild()

    def _update_font_sizes_in_place(self):
        """Update font sizes on existing child widgets without rebuild.

        This method updates font_size properties on all descendant Label
        widgets using their stored _font_scale metadata to preserve
        heading scale factors. This is more efficient than a full rebuild
        when only font size changes.

        Note:
            This method preserves widget identities and only updates
            font_size properties, leaving all other styling unchanged.
        """
        def update_font_size(widget):
            """Recursively update font_size on widget and children.

            Args:
                widget: Widget to update font size on
            """
            if isinstance(widget, Label):
                # Update font_size using base_font_size and scale metadata
                if hasattr(widget, '_font_scale'):
                    # Use the stored scale factor to compute font size
                    widget.font_size = self.base_font_size * widget._font_scale
                else:
                    # Fallback for Labels without scale metadata (use base_font_size)
                    widget.font_size = self.base_font_size

            # Recursively update children
            if hasattr(widget, 'children'):
                for child in widget.children:
                    update_font_size(child)

        # Update all children
        for child in self.children:
            update_font_size(child)

    def _update_styles_in_place(self):
        """Update style properties on existing child widgets without rebuild.

        This method updates purely stylistic properties (color,
        halign, valign, line_height, disabled state) on all descendant Label
        widgets without reconstructing the widget tree.

        This is more efficient than a full rebuild when only visual styling
        changes, as it preserves widget identities and avoids the overhead
        of parsing and widget creation.

        Note:
            This method only updates properties that don't affect widget
            structure. For structural changes (text, font_name, text_size,
            etc.), use _rebuild_widgets() instead. For font size changes,
            use _update_font_sizes_in_place() instead.
        """
        # Determine effective color based on disabled state
        effective_color = (
            list(self.disabled_color) if self.disabled else list(self.color)
        )
        effective_outline_color = (
            list(self.disabled_outline_color) if self.disabled else list(self.outline_color)
        )

        # Determine effective halign (convert 'auto' to 'left')
        effective_halign = 'left' if self.halign == 'auto' else self.halign

        def update_widget(widget):
            """Recursively update style properties on widget and children.

            Args:
                widget: Widget to update styles on
            """
            if isinstance(widget, Label):
                widget.color = effective_color
                widget.halign = effective_halign
                widget.valign = self.valign
                widget.line_height = self.line_height
                if hasattr(widget, 'outline_color'):
                    widget.outline_color = effective_outline_color
                if hasattr(widget, 'disabled_outline_color'):
                    widget.disabled_outline_color = list(self.disabled_outline_color)
                if hasattr(widget, 'mipmap'):
                    widget.mipmap = self.mipmap
                if hasattr(widget, 'base_direction'):
                    widget.base_direction = self.base_direction
                if hasattr(widget, 'text_language'):
                    widget.text_language = self.text_language
                if hasattr(widget, 'limit_render_to_text_bbox'):
                    widget.limit_render_to_text_bbox = self.limit_render_to_text_bbox
                if hasattr(widget, 'ellipsis_options'):
                    widget.ellipsis_options = dict(self.ellipsis_options)

            # Recursively update children
            if hasattr(widget, 'children'):
                for child in widget.children:
                    update_widget(child)

        # Update all children
        for child in self.children:
            update_widget(child)
    
    def _on_padding_changed(self, instance, value):
        """Callback when padding property changes.
        
        Note: padding is applied directly to the BoxLayout (self),
        not passed to the renderer.
        """
        # BoxLayout handles padding directly, no rebuild needed
        pass
    
    def _on_auto_size_height_changed(self, instance, value):
        """Handle auto_size_height property changes."""
        # In strict_label_mode, auto_size_height changes are ignored
        if self.strict_label_mode:
            return
        
        if value:
            # Enable auto-sizing
            self.size_hint_y = None
            self.bind(minimum_height=self.setter('height'))
        else:
            # Disable auto-sizing
            self.unbind(minimum_height=self.setter('height'))
            self.size_hint_y = self._user_size_hint_y
    
    def _on_strict_label_mode_changed(self, instance, value):
        """Handle strict_label_mode property changes.
        
        When strict_label_mode is enabled:
        - Disable auto-sizing (unbind height from minimum_height)
        - Restore size_hint_y to user-specified value
        
        When strict_label_mode is disabled:
        - Re-enable auto-sizing if auto_size_height is True
        """
        if value:
            # Strict mode: disable auto-sizing, preserve size_hint_y
            self.unbind(minimum_height=self.setter('height'))
            self.size_hint_y = self._user_size_hint_y
        else:
            # Markdown-friendly mode: enable auto-sizing if auto_size_height
            if self.auto_size_height:
                self.size_hint_y = None
                self.bind(minimum_height=self.setter('height'))
        
        # Schedule deferred rebuild to apply new mode behavior
        self._schedule_rebuild()
    
    def _schedule_rebuild(self):
        """Schedule a rebuild for the next frame.
        
        This method sets the _pending_rebuild flag and triggers the deferred
        rebuild via Clock.create_trigger. Multiple calls within the same frame
        will result in only one rebuild operation, enabling efficient batching
        of property changes.
        
        Use this method instead of calling _rebuild_widgets() directly when
        you want to batch multiple property changes into a single rebuild.
        """
        self._pending_rebuild = True
        self._rebuild_trigger()
    
    def _do_rebuild(self, dt=None):
        """Execute the deferred rebuild.
        
        This is the callback for _rebuild_trigger. It checks if a rebuild
        is actually pending and executes it if so.
        
        Args:
            dt: Delta time from Clock (unused but required by Clock API)
        """
        if self._pending_rebuild:
            self._pending_rebuild = False
            self._rebuild_widgets()

    def force_rebuild(self):
        """Force an immediate synchronous rebuild.
        
        This method cancels any pending deferred rebuild and executes
        the rebuild synchronously. Use this when you need the widget
        tree to be updated immediately rather than waiting for the
        next frame.
        
        This is useful in scenarios where:
        - You need to query widget properties immediately after changes
        - You're performing measurements that depend on the rebuilt tree
        - You need deterministic timing for testing
        
        Note:
            In most cases, you should let the deferred rebuild system
            handle updates automatically. Use force_rebuild() only when
            immediate synchronous updates are required.
        """
        self._rebuild_trigger.cancel()
        self._pending_rebuild = False
        self._rebuild_widgets()

    def _needs_clipping(self):
        """Determine if content clipping is needed.
        
        Clipping is needed when:
        - text_size[1] is not None (height-constrained), OR
        - strict_label_mode is True AND height is explicitly set
        
        Returns:
            bool: True if clipping should be applied
        """
        # Check if text_size height is constrained
        if self.text_size and self.text_size[1] is not None:
            return True
        
        # Check if strict_label_mode is True with explicit height
        if self.strict_label_mode and self.size_hint_y is None:
            return True
        
        return False

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
            link_style=self.link_style,
            code_bg_color=list(self.code_bg_color),
            font_name=self.font_name,
            color=list(self.color),
            outline_width=self.outline_width,
            outline_color=list(self.outline_color),
            disabled_outline_color=list(self.disabled_outline_color),
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
            mipmap=self.mipmap,
            base_direction=self.base_direction,
            text_language=self.text_language,
            shorten=self.shorten,
            max_lines=int(self.max_lines),
            shorten_from=self.shorten_from,
            split_str=self.split_str,
            text_padding=list(self.text_padding),
            strict_label_mode=self.strict_label_mode,
            ellipsis_options=dict(self.ellipsis_options),
            limit_render_to_text_bbox=self.limit_render_to_text_bbox
        )
        
        # Render AST to widget tree
        content = renderer(self._ast_tokens, None)
        
        # Bind ref_press events from child Labels to bubble up
        self._bind_ref_press_events(content)
        
        # Determine if clipping is needed
        needs_clipping = self._needs_clipping()
        
        if needs_clipping:
            # Wrap content in a clipping container
            clipping_container = _ClippingContainer()
            
            # Set the clipping container height based on constraints
            if self.text_size and self.text_size[1] is not None:
                # Use text_size height as the clipping height
                clipping_container.height = self.text_size[1]
            elif self.strict_label_mode and self.height:
                # Use widget height as the clipping height
                clipping_container.height = self.height
                # Bind to parent height changes
                self.bind(height=clipping_container.setter('height'))
            
            # Bind width to parent for proper layout
            clipping_container.size_hint_x = None
            self.bind(width=clipping_container.setter('width'))
            clipping_container.width = self.width
            
            # Add rendered content to clipping container
            for child in reversed(list(content.children)):
                content.remove_widget(child)
                clipping_container.add_widget(child)
            
            # Add clipping container to self
            self.add_widget(clipping_container)
        else:
            # No clipping needed - add content directly
            for child in reversed(list(content.children)):
                content.remove_widget(child)
                self.add_widget(child)
        
        # Bind to child widget size changes for texture_size updates
        self._bind_child_size_changes(self)
    
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
    
    def _bind_child_size_changes(self, widget):
        """Recursively bind to child widget size changes for texture_size updates.
        
        Args:
            widget: Widget to bind size changes from
        """
        from kivy.uix.image import AsyncImage
        from kivy.uix.gridlayout import GridLayout
        from kivy.uix.widget import Widget
        
        def on_child_size_change(instance, value):
            """Callback when a child widget's size changes."""
            self._texture_size_version += 1
        
        # Bind to size changes for relevant widget types
        if isinstance(widget, Label):
            # For Labels, bind to texture_size changes
            if hasattr(widget, 'texture_size'):
                widget.bind(texture_size=on_child_size_change)
        elif isinstance(widget, AsyncImage):
            # For AsyncImage, bind to size changes
            widget.bind(size=on_child_size_change)
        elif isinstance(widget, GridLayout):
            # For GridLayout (tables), bind to minimum_size changes
            if hasattr(widget, 'minimum_size'):
                widget.bind(minimum_size=on_child_size_change)
        elif isinstance(widget, Widget):
            # For plain Widgets (spacers, rules), bind to height changes
            widget.bind(height=on_child_size_change)
        
        # Recursively bind for container widgets
        if hasattr(widget, 'children'):
            for child in widget.children:
                self._bind_child_size_changes(child)
    
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
