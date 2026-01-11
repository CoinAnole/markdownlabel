"""
MarkdownLabel
=============

A Kivy widget that parses and renders Markdown documents as structured,
interactive Kivy UI elements. It mirrors the Label API for easy migration
but subclasses BoxLayout because Markdown rendering builds multiple widgets.

Example usage::

    from kivy_garden.markdownlabel import MarkdownLabel

    label = MarkdownLabel(text='# Hello World\\n\\nThis is **bold** text.')
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.stencilview import StencilView

import mistune
from mistune.plugins.table import table
from mistune.plugins.formatting import strikethrough

from ._version import __version__
from .inline_renderer import InlineRenderer
from .kivy_renderer import KivyRenderer
from .markdown_serializer import MarkdownSerializer
from .properties import MarkdownLabelProperties
from .rendering import MarkdownLabelRendering
from .utils import collect_widget_ids, find_labels_recursive

__all__ = (
    'MarkdownLabel',
    'InlineRenderer',
    'KivyRenderer',
    'MarkdownSerializer',
    'find_labels_recursive',
    'collect_widget_ids',
    '__version__',
)


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
        self.size_hint_y = None


class MarkdownLabel(MarkdownLabelProperties, MarkdownLabelRendering, BoxLayout):
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

    __events__ = ('on_ref_press',)

    def __init__(self, **kwargs):
        super(MarkdownLabel, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self._in_update_style = False

        # Deferred rebuild system for batching property changes
        self._pending_rebuild = False
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
            self.size_hint_y = self._user_size_hint_y

        # Bind auto_size_height changes to handler
        self.bind(auto_size_height=self._on_auto_size_height_changed)

        # Bind strict_label_mode changes to handler
        self.bind(strict_label_mode=self._on_strict_label_mode_changed)

        # Bind render_mode changes to handler
        self.bind(render_mode=self._on_render_mode_changed)

        # Store the parsed AST tokens
        self._ast_tokens = []

        # Create mistune parser with plugins
        self._parser = mistune.create_markdown(renderer=None)
        table(self._parser)
        strikethrough(self._parser)

        # Bind text property to rebuild widgets
        self.bind(text=self._on_text_changed)

        # Bind style-only properties
        self.bind(base_font_size=self._make_style_callback('base_font_size'))
        self.bind(color=self._make_style_callback('color'))
        self.bind(line_height=self._make_style_callback('line_height'))
        self.bind(halign=self._make_style_callback('halign'))
        self.bind(valign=self._make_style_callback('valign'))
        self.bind(disabled=self._make_style_callback('disabled'))
        self.bind(disabled_color=self._make_style_callback('disabled_color'))
        self.bind(base_direction=self._make_style_callback('base_direction'))
        self.bind(font_name=self._make_style_callback('font_name'))
        self.bind(code_font_name=self._make_style_callback('code_font_name'))
        self.bind(padding=self._make_style_callback('padding'))
        self.bind(text_padding=self._make_style_callback('text_padding'))
        self.bind(outline_width=self._make_style_callback('outline_width'))
        self.bind(outline_color=self._make_style_callback('outline_color'))
        self.bind(disabled_outline_color=self._make_style_callback('disabled_outline_color'))
        self.bind(mipmap=self._make_style_callback('mipmap'))
        self.bind(text_language=self._make_style_callback('text_language'))
        self.bind(limit_render_to_text_bbox=self._make_style_callback('limit_render_to_text_bbox'))

        # Bind structure properties (trigger rebuild)
        self.bind(link_style=self._make_style_callback('link_style'))
        # Color changes affect generated markup/backgrounds; treat as structure-level.
        self.bind(link_color=self._make_style_callback('link_color'))
        self.bind(code_bg_color=self._make_style_callback('code_bg_color'))

        # Special-case style-only properties with extra handling
        # text_size is style-only but needs binding refresh on existing Labels
        self.bind(text_size=self._make_style_callback('text_size'))

        # Bind other properties
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

        # Initial build if text is provided
        if self.text:
            self._rebuild_widgets()

    def _on_text_changed(self, instance, value):
        """Callback when text property changes."""
        self._schedule_rebuild()

    def _make_style_callback(self, prop_name):
        """Create a callback for a specific property that tracks which changed."""
        def callback(instance, value):
            self._on_style_changed(instance, value, prop_name)
        return callback

    def _on_style_changed(self, instance, value, prop_name=None):
        """Callback when a styling property changes."""
        if self._in_update_style:
            return

        if prop_name is None:
            self._schedule_rebuild()
            return

        if prop_name in ('base_font_size', 'font_size'):
            if self.children:
                self._update_font_sizes_in_place()
        elif prop_name == 'text_size':
            if self.children:
                self._update_text_size_bindings_in_place()
        elif prop_name in self.STYLE_ONLY_PROPERTIES:
            if self.children:
                self._update_styles_in_place()
        else:
            self._schedule_rebuild()

    def _on_auto_size_height_changed(self, instance, value):
        """Handle auto_size_height property changes."""
        if self.strict_label_mode:
            return

        if value:
            self.size_hint_y = None
            self.bind(minimum_height=self.setter('height'))
        else:
            self.unbind(minimum_height=self.setter('height'))
            self.size_hint_y = self._user_size_hint_y

    def _on_strict_label_mode_changed(self, instance, value):
        """Handle strict_label_mode property changes."""
        if value:
            self.unbind(minimum_height=self.setter('height'))
            self.size_hint_y = self._user_size_hint_y
        else:
            if self.auto_size_height:
                self.size_hint_y = None
                self.bind(minimum_height=self.setter('height'))

        self._schedule_rebuild()

    def _on_render_mode_changed(self, instance, value):
        """Handle render_mode property changes."""
        self._schedule_rebuild()

    def _schedule_rebuild(self):
        """Schedule a rebuild for the next frame."""
        self._pending_rebuild = True
        self._rebuild_trigger()

    def _do_rebuild(self, dt=None):
        """Execute the deferred rebuild."""
        if self._pending_rebuild:
            self._pending_rebuild = False
            self._rebuild_widgets()

    def force_rebuild(self):
        """Force an immediate synchronous rebuild."""
        self._rebuild_trigger.cancel()
        self._pending_rebuild = False
        self._rebuild_widgets()

    def _rebuild_widgets(self):
        """Parse the Markdown text and rebuild the widget tree."""
        self.clear_widgets()
        self._aggregated_refs = {}

        if not self.text:
            self._ast_tokens = []
            return

        # Parse Markdown to AST
        result = self._parser.parse(self.text)
        tokens = result[0] if isinstance(result, tuple) else result

        # Normalize degenerate single-marker inputs (e.g., "-" without list content)
        # to a paragraph token so they render as a Label, matching paragraph
        # expectations in the public API and tests.
        if (
            len(tokens) == 1
            and tokens[0].get('type') == 'list'
            and self.text.strip() in ('-', '*', '+')
        ):
            tokens = [{
                'type': 'paragraph',
                'children': [{'type': 'text', 'raw': self.text}]
            }]

        self._ast_tokens = tokens

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
            halign=self._get_effective_halign(),
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

        # Apply text_size bindings consistently using rendering mixin logic
        self._update_text_size_bindings_in_place(content)

        # Determine effective render mode
        effective_render_mode = self._get_effective_render_mode()

        # Handle texture render mode
        if effective_render_mode == 'texture':
            self._bind_ref_press_events(content)
            image = self._render_as_texture(content)

            if image is not None:
                needs_clipping = self._needs_clipping()

                if needs_clipping:
                    clipping_container = _ClippingContainer()

                    if self.text_size and self.text_size[1] is not None:
                        clipping_container.height = self.text_size[1]
                    elif self.strict_label_mode and self.height:
                        clipping_container.height = self.height
                        self.bind(height=clipping_container.setter('height'))

                    clipping_container.size_hint_x = None
                    self.bind(width=clipping_container.setter('width'))
                    clipping_container.width = self.width

                    clipping_container.add_widget(image)
                    self.add_widget(clipping_container)
                else:
                    self.add_widget(image)

                self._bind_child_size_changes(self)
                return

        # Widget render mode (default)
        self._bind_ref_press_events(content)
        needs_clipping = self._needs_clipping()

        if needs_clipping:
            clipping_container = _ClippingContainer()

            if self.text_size and self.text_size[1] is not None:
                clipping_container.height = self.text_size[1]
            elif self.strict_label_mode and self.height:
                clipping_container.height = self.height
                self.bind(height=clipping_container.setter('height'))

            clipping_container.size_hint_x = None
            self.bind(width=clipping_container.setter('width'))
            clipping_container.width = self.width

            for child in reversed(list(content.children)):
                content.remove_widget(child)
                clipping_container.add_widget(child)

            self.add_widget(clipping_container)
        else:
            for child in reversed(list(content.children)):
                content.remove_widget(child)
                self.add_widget(child)

        self._bind_child_size_changes(self)

    def on_touch_down(self, touch):
        """Handle touch events, including texture mode link hit-testing."""
        effective_mode = self._get_effective_render_mode()

        if effective_mode == 'texture' and self._aggregated_refs:
            if self.collide_point(*touch.pos):
                local_x = touch.x - self.x
                local_y = touch.y - self.y

                for ref_name, zones in self._aggregated_refs.items():
                    for zone in zones:
                        if self._point_in_zone((local_x, local_y), zone):
                            self.dispatch('on_ref_press', ref_name)
                            return True

        return super(MarkdownLabel, self).on_touch_down(touch)

    def on_ref_press(self, ref):
        """Event handler for link clicks."""
        pass

    def get_ast(self):
        """Return the parsed AST tokens."""
        return self._ast_tokens

    def to_markdown(self):
        """Serialize the current AST back to Markdown text."""
        serializer = MarkdownSerializer()
        return serializer.serialize(self._ast_tokens)

    def update_style(self, **kwargs):
        """Batch update style/structure properties with a single refresh.

        Style-only changes apply immediately in-place. Including any structure
        property schedules a rebuild after all assignments complete.
        """
        if not kwargs:
            return

        structure_changed = any(name in self.STRUCTURE_PROPERTIES for name in kwargs)
        font_changed = any(name in ('base_font_size', 'font_size') for name in kwargs)
        text_size_changed = 'text_size' in kwargs
        style_changed = any(
            name in self.STYLE_ONLY_PROPERTIES
            for name in kwargs
            if name not in ('base_font_size', 'font_size', 'text_size')
        )

        try:
            self._in_update_style = True
            for name, value in kwargs.items():
                setattr(self, name, value)
        finally:
            self._in_update_style = False

        if structure_changed:
            self._schedule_rebuild()
            return

        if not self.children:
            return

        if text_size_changed:
            self._update_text_size_bindings_in_place()

        if font_changed:
            self._update_font_sizes_in_place()

        if style_changed:
            self._update_styles_in_place()
