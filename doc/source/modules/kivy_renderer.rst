.. _kivy_renderer_module:

Kivy Renderer Module
====================

The ``kivy_renderer`` module provides the ``KivyRenderer`` class that converts Markdown AST tokens to Kivy widget trees.

Module Contents
---------------

.. automodule:: kivy_garden.markdownlabel.kivy_renderer
   :members:
   :undoc-members:
   :show-inheritance:

KivyRenderer Class
------------------

.. autoclass:: kivy_garden.markdownlabel.KivyRenderer
   :members:
   :undoc-members:
   :show-inheritance:

   .. rubric:: Block Render Methods

   .. autosummary::
      :nosignatures:

      __call__
      render_tokens
      paragraph
      heading
      list
      list_item
      block_code
      block_quote
      thematic_break
      blank_line

Block Elements Supported
------------------------

**Paragraphs**
   Standard text blocks rendered as Labels

**Headings** (H1-H6)
   Rendered with progressively larger font sizes based on ``base_font_size``

**Lists**
   Both ordered (numbered) and unordered (bullet) lists with proper indentation

**Code Blocks**
   Fenced code blocks with background color from ``code_bg_color``

**Block Quotes**
   Indented quotes with optional styling

**Tables**
   Supported via the ``KivyRendererTables`` mixin (see :doc:`kivy_renderer_tables`)

**Horizontal Rules**
   Thematic breaks as visual separators

Nesting Depth Protection
------------------------

The renderer includes recursion depth limiting to prevent stack overflow with deeply nested structures. The maximum depth is controlled by the ``MAX_NESTING_DEPTH`` constant.

Rendering Context
-----------------

The renderer maintains context during rendering:

- Current nesting level
- List type and numbering
- Indentation state
- Style properties

Example Usage
-------------

.. code-block:: python

    from kivy_garden.markdownlabel import KivyRenderer

    renderer = KivyRenderer(
        base_font_size=16,
        halign='left',
        color=[1, 1, 1, 1]
    )

    # Render AST tokens to widget tree
    widget_tree = renderer(ast_tokens, None)

See Also
--------

- :doc:`inline_renderer` - Inline element rendering
- :doc:`kivy_renderer_tables` - Table rendering support
- :doc:`rendering` - Overall rendering pipeline
