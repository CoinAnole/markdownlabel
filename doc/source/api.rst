.. _api_reference:

API Reference
=============

This section provides detailed API documentation for all public modules and classes in MarkdownLabel.

Main Widget
-----------

.. toctree::
   :maxdepth: 1

   modules/markdownlabel

Supporting Modules
------------------

.. toctree::
   :maxdepth: 1

   modules/properties
   modules/rendering
   modules/inline_renderer
   modules/kivy_renderer
   modules/kivy_renderer_tables
   modules/markdown_serializer
   modules/font_fallback
   modules/utils

Version Information
-------------------

The version string is available as ``kivy_garden.markdownlabel.__version__``.

Example::

    from kivy_garden.markdownlabel import __version__
    print(f"MarkdownLabel version: {__version__}")

Public API
----------

The following items are exported in the main ``kivy_garden.markdownlabel`` module:

- :class:`~kivy_garden.markdownlabel.MarkdownLabel` - The main widget class
- :class:`~kivy_garden.markdownlabel.InlineRenderer` - Inline markup renderer
- :class:`~kivy_garden.markdownlabel.KivyRenderer` - Block-level renderer
- :class:`~kivy_garden.markdownlabel.MarkdownSerializer` - AST to Markdown serializer
- :func:`~kivy_garden.markdownlabel.find_labels_recursive` - Widget traversal utility
- :func:`~kivy_garden.markdownlabel.collect_widget_ids` - Widget ID collector
- :func:`~kivy_garden.markdownlabel.extract_font_tags` - Font tag extractor
- ``__version__`` - Version string
