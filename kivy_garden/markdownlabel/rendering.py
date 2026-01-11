"""Rendering logic for MarkdownLabel.

This module contains all rendering-related methods including widget tree
building, texture rendering, and style updates.
"""

from kivy.uix.label import Label
from kivy.uix.image import Image, AsyncImage
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.graphics import Fbo, ClearColor, ClearBuffers


def clear_text_size_bindings(label):
    """Remove previously attached text_size-related bindings from a Label."""
    width_cb = getattr(label, '_md_text_size_width_cb', None)
    if width_cb:
        label.unbind(width=width_cb)

    tex_cb = getattr(label, '_md_text_size_tex_cb', None)
    if tex_cb:
        label.unbind(texture_size=tex_cb)

    label._md_text_size_width_cb = None
    label._md_text_size_tex_cb = None


def apply_text_size_binding(label, text_size, strict_label_mode):
    """Apply text_size binding logic consistently for both build and updates."""
    clear_text_size_bindings(label)

    text_width, text_height = text_size if text_size else (None, None)
    strict = strict_label_mode

    tex_cb = lambda inst, val: setattr(inst, 'height', val[1])
    label._md_text_size_tex_cb = tex_cb
    label.bind(texture_size=tex_cb)

    if text_width is not None:
        if text_height is not None:
            # Both width and height specified
            label.text_size = (text_width, text_height)
        else:
            # Only width specified - keep fixed width, no binding needed
            label.text_size = (text_width, None)
    else:
        if text_height is not None:
            # Only height specified - set initial text_size and bind width
            label.text_size = (label.width, text_height)
            width_cb = lambda inst, val, th=text_height: setattr(inst, 'text_size', (val, th))
            label._md_text_size_width_cb = width_cb
            label.bind(width=width_cb)
        else:
            # Neither specified
            if strict:
                # Strict mode: don't auto-bind width, let Label handle naturally
                label.text_size = (None, None)
            else:
                # Markdown-friendly mode: auto-bind width for text wrapping
                label.text_size = (label.width, None)
                width_cb = lambda inst, val: setattr(inst, 'text_size', (val, None))
                label._md_text_size_width_cb = width_cb
                label.bind(width=width_cb)

    # Always bind texture_size to height for proper sizing
    if getattr(label, '_md_text_size_tex_cb', None) is None:
        tex_cb = lambda inst, val: setattr(inst, 'height', val[1])
        label._md_text_size_tex_cb = tex_cb
        label.bind(texture_size=tex_cb)


class MarkdownLabelRendering:
    """Mixin class containing rendering logic for MarkdownLabel.

    This class is designed to be mixed into the main MarkdownLabel class
    to provide rendering functionality in a separate, organized module.
    """

    def _update_font_sizes_in_place(self):
        """Update font sizes on existing child widgets without rebuild."""
        def update_font_size(widget):
            if isinstance(widget, Label):
                if hasattr(widget, '_font_scale'):
                    widget.font_size = self.base_font_size * widget._font_scale
                else:
                    widget.font_size = self.base_font_size

            if hasattr(widget, 'children'):
                for child in widget.children:
                    update_font_size(child)

        for child in self.children:
            update_font_size(child)

    def _get_effective_halign(self):
        """Compute effective halign based on auto and base_direction."""
        if self.halign != 'auto':
            return self.halign

        if self.base_direction in ('rtl', 'weak_rtl'):
            return 'right'
        return 'left'

    def _update_styles_in_place(self):
        """Update style properties on existing child widgets without rebuild."""
        effective_color = (
            list(self.disabled_color) if self.disabled else list(self.color)
        )
        effective_outline_color = (
            list(self.disabled_outline_color) if self.disabled else list(self.outline_color)
        )
        effective_halign = self._get_effective_halign()
        effective_text_padding = list(self.text_padding)

        def update_widget(widget):
            if isinstance(widget, Label):
                widget.color = effective_color
                widget.halign = effective_halign
                widget.valign = self.valign
                widget.line_height = self.line_height
                widget.padding = effective_text_padding

                if hasattr(widget, '_is_code') and widget._is_code:
                    widget.font_name = self.code_font_name
                else:
                    widget.font_name = self.font_name
                    if hasattr(widget, 'font_family'):
                        widget.font_family = self.font_family

                if hasattr(widget, 'font_context'):
                    widget.font_context = self.font_context
                if hasattr(widget, 'font_features'):
                    widget.font_features = self.font_features
                if hasattr(widget, 'font_hinting'):
                    widget.font_hinting = self.font_hinting
                if hasattr(widget, 'font_kerning'):
                    widget.font_kerning = self.font_kerning
                if hasattr(widget, 'font_blended'):
                    widget.font_blended = self.font_blended

                if hasattr(widget, 'outline_width'):
                    widget.outline_width = self.outline_width
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

                if hasattr(widget, 'unicode_errors'):
                    widget.unicode_errors = self.unicode_errors
                if hasattr(widget, 'strip'):
                    widget.strip = self.strip

                if hasattr(widget, 'shorten'):
                    widget.shorten = self.shorten
                if hasattr(widget, 'max_lines'):
                    if self.max_lines > 0:
                        widget.max_lines = self.max_lines
                    else:
                        widget.max_lines = 0
                if hasattr(widget, 'shorten_from'):
                    widget.shorten_from = self.shorten_from
                if hasattr(widget, 'split_str'):
                    widget.split_str = self.split_str

            if hasattr(widget, 'children'):
                for child in widget.children:
                    update_widget(child)

        for child in self.children:
            update_widget(child)

    def _clear_text_size_bindings(self, label):
        """Remove previously attached text_size-related bindings from a Label."""
        clear_text_size_bindings(label)

    def _apply_text_size_to_label(self, label):
        """Apply current text_size/strict_label_mode to a Label with clean bindings."""
        apply_text_size_binding(label, self.text_size, self.strict_label_mode)

    def _update_text_size_bindings_in_place(self, root=None):
        """Reapply text_size bindings to all descendant Labels.

        Args:
            root: optional root widget to traverse; defaults to self.
        """
        traversal_root = root if root is not None else self

        def update(widget):
            if isinstance(widget, Label):
                self._apply_text_size_to_label(widget)
            if hasattr(widget, 'children'):
                for child in widget.children:
                    update(child)

        if hasattr(traversal_root, 'children'):
            for child in traversal_root.children:
                update(child)

    def _needs_clipping(self):
        """Determine if content clipping is needed."""
        if self.text_size and self.text_size[1] is not None:
            return True

        if self.strict_label_mode and self.size_hint_y is None:
            return True

        return False

    def _get_effective_render_mode(self):
        """Determine the effective render mode based on settings and content."""
        if self.render_mode == 'widgets':
            return 'widgets'
        elif self.render_mode == 'texture':
            return 'texture'
        else:  # 'auto' mode
            if self.strict_label_mode:
                has_height_constraint = (
                    (self.text_size and self.text_size[1] is not None) or
                    self.size_hint_y is None
                )
                if has_height_constraint:
                    return 'texture'

            return 'widgets'

    def _render_as_texture(self, content):
        """Render content widget tree to a single texture."""
        import warnings

        MAX_FBO_DIM = 8192  # guardrail for GPU-backed FBO dimensions

        content_width = self.width if self.width > 0 else 800
        content_height = 0

        # Layout children with the intended width so measurements are accurate
        content.size_hint = (None, None)
        content.width = content_width
        content.do_layout()

        for child in content.children:
            if isinstance(child, Label):
                child.texture_update()
                if child.texture_size[1] > 0:
                    content_height += child.texture_size[1]
                else:
                    content_height += child.height
            elif isinstance(child, GridLayout):
                if hasattr(child, 'minimum_height') and child.minimum_height:
                    content_height += child.minimum_height
                else:
                    content_height += child.height
            else:
                content_height += child.height

        if content_height <= 0:
            content_height = 100
        if content_width <= 0:
            content_width = 100

        if content_width > MAX_FBO_DIM or content_height > MAX_FBO_DIM:
            warnings.warn(
                f"Texture render size too large ({content_width}x{content_height}); "
                "falling back to widget mode.",
                RuntimeWarning,
            )
            return None

        content.size = (content_width, content_height)
        content.pos = (0, 0)
        content.do_layout()

        self._collect_refs_for_texture(content, content_height)

        def _has_unloaded_images(widget):
            if isinstance(widget, AsyncImage) and not widget.texture:
                return True
            if hasattr(widget, 'children'):
                return any(_has_unloaded_images(child) for child in widget.children)
            return False

        has_unloaded_images = _has_unloaded_images(content)

        try:
            fbo = Fbo(size=(int(content_width), int(content_height)))

            with fbo:
                ClearColor(0, 0, 0, 0)
                ClearBuffers()

            fbo.add(content.canvas)
            fbo.draw()

            texture = fbo.texture

            image = Image(
                texture=texture,
                size=(content_width, content_height),
                size_hint=(None, None),
                allow_stretch=True,
                keep_ratio=False
            )

            fbo.remove(content.canvas)

            if has_unloaded_images:
                warnings.warn(
                    "Texture render completed but some AsyncImage textures were not loaded; "
                    "images may appear blank until re-rendered.",
                    RuntimeWarning,
                )

            return image

        except Exception as e:
            warnings.warn(
                f"Texture rendering failed, falling back to widget mode: {e}",
                RuntimeWarning
            )
            return None

    def _collect_refs_for_texture(self, widget, content_height, offset_x=0, offset_y=0):
        """Collect reference zones from widget tree for texture mode hit-testing."""
        if widget is self or (hasattr(widget, 'parent') and widget.parent is self):
            self._aggregated_refs = {}

        if isinstance(widget, Label) and hasattr(widget, 'refs') and widget.refs:
            label_x = offset_x + widget.x
            label_y = offset_y + widget.y

            tex_w, tex_h = getattr(widget, 'texture_size', (widget.width, widget.height))
            if tex_w <= 0:
                tex_w = widget.width
            if tex_h <= 0:
                tex_h = widget.height

            base_x = label_x + (widget.width - tex_w) / 2.0
            base_y = label_y + (widget.height - tex_h) / 2.0

            for ref_name, ref_boxes in widget.refs.items():
                if ref_name not in self._aggregated_refs:
                    self._aggregated_refs[ref_name] = []

                for box in ref_boxes:
                    x1, y1, x2, y2 = box

                    zone_x = base_x + x1
                    zone_y = base_y + (tex_h - y2)
                    zone_width = x2 - x1
                    zone_height = y2 - y1

                    self._aggregated_refs[ref_name].append(
                        (zone_x, zone_y, zone_width, zone_height)
                    )

        if hasattr(widget, 'children'):
            child_offset_x = offset_x + widget.x
            child_offset_y = offset_y + widget.y
            for child in widget.children:
                self._collect_refs_for_texture(
                    child, content_height, child_offset_x, child_offset_y
                )

    def _bind_ref_press_events(self, widget):
        """Recursively bind on_ref_press events from child Labels."""
        if isinstance(widget, Label) and widget.markup:
            widget.bind(on_ref_press=self._on_child_ref_press)

        if hasattr(widget, 'children'):
            for child in widget.children:
                self._bind_ref_press_events(child)

    def _bind_child_size_changes(self, widget):
        """Recursively bind to child widget size changes for texture_size updates."""
        def on_child_size_change(instance, value):
            self._texture_size_version += 1

        if isinstance(widget, Label):
            if hasattr(widget, 'texture_size'):
                widget.bind(texture_size=on_child_size_change)
        elif isinstance(widget, AsyncImage):
            widget.bind(size=on_child_size_change)
        elif isinstance(widget, GridLayout):
            if hasattr(widget, 'minimum_size'):
                widget.bind(minimum_size=on_child_size_change)
        elif isinstance(widget, Widget):
            widget.bind(height=on_child_size_change)

        if hasattr(widget, 'children'):
            for child in widget.children:
                self._bind_child_size_changes(child)

    def _on_child_ref_press(self, instance, ref):
        """Handle ref_press from child Label and bubble up."""
        self.dispatch('on_ref_press', ref)

    def _point_in_zone(self, point, zone):
        """Check if a point is within a bounding zone."""
        px, py = point
        zx, zy, zw, zh = zone

        return (zx <= px <= zx + zw) and (zy <= py <= zy + zh)
