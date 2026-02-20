.. _rendering_module:

Rendering Module
================

The ``rendering`` module contains the ``MarkdownLabelRendering`` mixin class that handles widget tree building and style updates.

Module Contents
---------------

.. automodule:: kivy_garden.markdownlabel.rendering
   :members:
   :undoc-members:
   :show-inheritance:

Rendering Pipeline
------------------

The rendering process follows a three-layer pipeline:

1. **Parsing**: mistune parses Markdown text into an Abstract Syntax Tree (AST)
2. **Block Rendering**: ``KivyRenderer`` converts AST blocks to Kivy widgets
3. **Inline Rendering**: ``InlineRenderer`` converts inline elements to BBCode markup strings

Render Modes
------------

**Widget Mode** (default)
   Renders Markdown as actual Kivy widget hierarchy. Supports full interactivity and dynamic styling.

**Texture Mode**
   Renders Markdown to a texture for better performance with static content. Uses ``_render_as_texture()`` method.

**Strict Label Mode**
   When enabled, maintains fixed height and uses ``text_size`` for text wrapping, similar to standard Kivy Label behavior.

Clipping Behavior
-----------------

Content clipping is handled by ``_ClippingContainer`` (a ``StencilView`` subclass) when:

- ``text_size[1]`` is set (height-constrained rendering)
- ``strict_label_mode`` is enabled with a fixed height

In-Place Updates
----------------

For **STYLE_ONLY_PROPERTIES**, the rendering system can update styles without rebuilding the widget tree:

- ``_update_styles_in_place()`` - Applies all style properties
- ``_update_font_sizes_in_place()`` - Updates font sizes efficiently
- ``_update_text_size_bindings_in_place()`` - Refreshes text wrapping bindings

See Also
--------

- :doc:`properties` - Property classification that triggers different update modes
- :doc:`kivy_renderer` - Block-level rendering implementation
- :doc:`inline_renderer` - Inline markup rendering
