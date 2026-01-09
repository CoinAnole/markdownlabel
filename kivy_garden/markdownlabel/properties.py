"""Property definitions and property-related methods for MarkdownLabel.

This module contains all Kivy property definitions and property update methods
that were extracted from the main MarkdownLabel class for better organization.
"""

from kivy.properties import (
    StringProperty,
    NumericProperty,
    ColorProperty,
    AliasProperty,
    BooleanProperty,
    OptionProperty,
    VariableListProperty,
    ListProperty,
    DictProperty
)


class MarkdownLabelProperties:
    """Mixin class containing all property definitions for MarkdownLabel.

    This class is designed to be mixed into the main MarkdownLabel class
    to provide all property definitions in a separate, organized module.
    """

    # Property categories for efficient updates
    STYLE_ONLY_PROPERTIES = frozenset({
        'color',
        'halign',
        'valign',
        'line_height',
        'disabled',
        'disabled_color',
        'base_direction',
        'text_padding',
        'outline_color',
        'disabled_outline_color',
        'outline_width',
        'mipmap',
        'text_language',
        'limit_render_to_text_bbox',
        'font_name',
        'code_font_name',
        'font_family',
        'font_context',
        'font_features',
        'font_hinting',
        'font_kerning',
        'font_blended',
        'unicode_errors',
        'strip',
        'shorten',
        'max_lines',
        'shorten_from',
        'split_str',
        'ellipsis_options',
        'text_size',
    })

    STRUCTURE_PROPERTIES = frozenset({
        'text',
        'link_style',
        'render_mode',
        'strict_label_mode',
    })

    # Core properties
    text = StringProperty('')
    base_font_size = NumericProperty(15)
    code_font_name = StringProperty('RobotoMono-Regular')
    link_color = ColorProperty([0, 0.5, 1, 1])
    link_style = OptionProperty('unstyled', options=['unstyled', 'styled'])
    code_bg_color = ColorProperty([0.15, 0.15, 0.15, 1])

    def _get_font_size(self):
        """Getter for font_size alias property."""
        return self.base_font_size

    def _set_font_size(self, value):
        """Setter for font_size alias property."""
        self.base_font_size = value

    font_size = AliasProperty(_get_font_size, _set_font_size, bind=['base_font_size'])

    # No-op properties for Label API compatibility
    bold = BooleanProperty(False)
    italic = BooleanProperty(False)
    underline = BooleanProperty(False)
    strikethrough = BooleanProperty(False)
    markup = BooleanProperty(True)

    # Forwarding properties
    font_name = StringProperty('Roboto')
    color = ColorProperty([1, 1, 1, 1])
    line_height = NumericProperty(1.0)
    halign = OptionProperty('auto', options=['left', 'center', 'right', 'justify', 'auto'])
    valign = OptionProperty('bottom', options=['bottom', 'middle', 'center', 'top'])
    padding = VariableListProperty([0, 0, 0, 0])
    text_padding = VariableListProperty([0, 0, 0, 0])

    def _get_label_padding(self):
        """Getter for label_padding alias property."""
        return self.text_padding

    def _set_label_padding(self, value):
        """Setter for label_padding alias property."""
        self.text_padding = value

    label_padding = AliasProperty(_get_label_padding, _set_label_padding, bind=['text_padding'])

    text_size = ListProperty([None, None])
    unicode_errors = OptionProperty('replace', options=['strict', 'replace', 'ignore'])
    strip = BooleanProperty(False)

    # Advanced font properties
    font_family = StringProperty(None, allownone=True)
    font_context = StringProperty(None, allownone=True)
    font_features = StringProperty('')
    font_hinting = OptionProperty('normal', options=[None, 'normal', 'light', 'mono'], allownone=True)
    font_kerning = BooleanProperty(True)
    font_blended = BooleanProperty(True)

    disabled_color = ColorProperty([1, 1, 1, 0.3])
    outline_width = NumericProperty(None, allownone=True)
    outline_color = ColorProperty([0, 0, 0, 1])
    disabled_outline_color = ColorProperty([0, 0, 0, 1])
    mipmap = BooleanProperty(False)
    base_direction = OptionProperty(
        None, options=['ltr', 'rtl', 'weak_rtl', 'weak_ltr', None], allownone=True
    )
    text_language = StringProperty(None, allownone=True)
    limit_render_to_text_bbox = BooleanProperty(False)

    # Truncation properties
    shorten = BooleanProperty(False)
    max_lines = NumericProperty(0)
    shorten_from = OptionProperty('center', options=['left', 'center', 'right'])
    split_str = StringProperty('')
    ellipsis_options = DictProperty({})

    # Internal property for texture_size updates
    _texture_size_version = NumericProperty(0)

    # Sizing properties
    auto_size_height = BooleanProperty(False)
    strict_label_mode = BooleanProperty(False)
    render_mode = OptionProperty('widgets', options=['widgets', 'texture', 'auto'])

    # Internal storage for texture mode
    _aggregated_refs = DictProperty({})

    # Aggregated texture property
    aggregate_texture_enabled = BooleanProperty(False)

    def _get_texture_size(self):
        """Compute aggregate texture_size from all descendant widgets."""
        from kivy.uix.label import Label
        from kivy.uix.image import AsyncImage
        from kivy.uix.gridlayout import GridLayout
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.widget import Widget

        if not self.children:
            return [0, 0]

        max_width = 0
        total_height = 0

        def collect_sizes(widget, visited=None):
            nonlocal max_width, total_height

            if visited is None:
                visited = set()

            widget_id = id(widget)
            if widget_id in visited:
                return
            visited.add(widget_id)

            if isinstance(widget, Label) and hasattr(widget, 'texture_size'):
                ts = widget.texture_size
                if ts[0] > max_width:
                    max_width = ts[0]
                total_height += ts[1]
            elif isinstance(widget, AsyncImage):
                if widget.width > max_width:
                    max_width = widget.width
                total_height += widget.height
            elif isinstance(widget, GridLayout):
                if hasattr(widget, 'minimum_width') and widget.minimum_width:
                    if widget.minimum_width > max_width:
                        max_width = widget.minimum_width
                if hasattr(widget, 'minimum_height') and widget.minimum_height:
                    total_height += widget.minimum_height
            elif isinstance(widget, BoxLayout):
                for child in widget.children:
                    collect_sizes(child, visited)
            elif isinstance(widget, Widget):
                total_height += widget.height

        for child in self.children:
            collect_sizes(child)

        return [max_width, total_height]

    texture_size = AliasProperty(_get_texture_size, bind=['children', 'text', '_texture_size_version'])

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

    def _get_refs(self):
        """Aggregate refs from child Labels using Label-style coordinates."""
        from kivy.uix.label import Label

        refs = {}

        def get_parent_offset(widget):
            offset_x = 0
            offset_y = 0
            current = widget.parent
            while current is not None and current is not self:
                offset_x += current.x
                offset_y += current.y
                current = current.parent
            return offset_x, offset_y

        def translate_box(label, box):
            tex_w, tex_h = getattr(label, 'texture_size', (0, 0))
            if not tex_w and not tex_h:
                tex_w, tex_h = label.width, label.height

            parent_offset_x, parent_offset_y = get_parent_offset(label)
            base_x = parent_offset_x + (label.center_x - tex_w / 2.0)
            base_y = parent_offset_y + (label.center_y + tex_h / 2.0)

            x1, y1, x2, y2 = box
            return [base_x + x1, base_y - y1, base_x + x2, base_y - y2]

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

    refs = AliasProperty(_get_refs, bind=['children', 'text', '_texture_size_version'])

    def _get_anchors(self):
        """Aggregate anchors from child Labels using Label-style coordinates."""
        from kivy.uix.label import Label

        anchors = {}

        def get_parent_offset(widget):
            offset_x = 0
            offset_y = 0
            current = widget.parent
            while current is not None and current is not self:
                offset_x += current.x
                offset_y += current.y
                current = current.parent
            return offset_x, offset_y

        def translate_anchor(label, pos):
            tex_w, tex_h = getattr(label, 'texture_size', (0, 0))
            if not tex_w and not tex_h:
                tex_w, tex_h = label.width, label.height

            parent_offset_x, parent_offset_y = get_parent_offset(label)
            base_x = parent_offset_x + (label.center_x - tex_w / 2.0)
            base_y = parent_offset_y + (label.center_y + tex_h / 2.0)

            return (base_x + pos[0], base_y - pos[1])

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

    anchors = AliasProperty(_get_anchors, bind=['children', 'text', '_texture_size_version'])
