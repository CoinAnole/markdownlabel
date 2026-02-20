.. _markdownlabel_module:

MarkdownLabel Widget
====================

The ``MarkdownLabel`` class is the main widget for rendering Markdown content in Kivy applications.

Module Contents
---------------

.. automodule:: kivy_garden.markdownlabel
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__

MarkdownLabel Class
-------------------

.. autoclass:: kivy_garden.markdownlabel.MarkdownLabel
   :members:
   :undoc-members:
   :show-inheritance:

   .. rubric:: Methods

   .. autosummary::
      :nosignatures:

      force_rebuild
      get_ast
      on_ref_press
      to_markdown
      update_style

   .. rubric:: Properties

   .. autosummary::
      :nosignatures:

      anchors
      ast_tokens
      auto_size_height
      base_direction
      base_font_size
      code_bg_color
      code_font_name
      color
      disabled
      disabled_color
      disabled_outline_color
      fallback_enabled
      fallback_fonts
      fallback_font_scales
      font_blended
      font_context
      font_family
      font_features
      font_hinting
      font_kerning
      font_name
      halign
      line_height
      limit_render_to_text_bbox
      link_color
      link_style
      mipmap
      outline_color
      outline_width
      padding
      refs
      render_mode
      strict_label_mode
      strip
      text
      text_language
      text_padding
      text_size
      texture
      texture_size
      unicode_errors
      valign

Internal Classes
----------------

.. autoclass:: kivy_garden.markdownlabel._ClippingContainer
   :members:
   :undoc-members:
   :show-inheritance:

Version Information
-------------------

.. autodata:: kivy_garden.markdownlabel.__version__
   :annotation:

Public Exports
--------------

.. data:: __all__

   Tuple of public exports from the module:

   - ``MarkdownLabel``
   - ``InlineRenderer``
   - ``KivyRenderer``
   - ``MarkdownSerializer``
   - ``find_labels_recursive``
   - ``collect_widget_ids``
   - ``extract_font_tags``
   - ``__version__``
