.. _properties_module:

Properties Module
=================

The ``properties`` module defines Kivy properties used by
``MarkdownLabelProperties`` and classifies them by update behavior.

Module Contents
---------------

.. automodule:: kivy_garden.markdownlabel.properties
   :no-members:

Property Classification
-----------------------

Properties in MarkdownLabel are classified into two categories:

**STYLE_ONLY_PROPERTIES**
   Changing these updates existing child widgets in place.

   Typical examples: ``color``, ``font_name``, ``halign``, ``valign``,
   ``padding``, ``line_height``, ``text_size``

**STRUCTURE_PROPERTIES**
   Changing these schedules a full rebuild of the rendered widget tree.

   Typical examples: ``text``, ``render_mode``, ``strict_label_mode``,
   ``image_size_mode``, ``link_style``, ``link_color``, ``code_bg_color``,
   ``fallback_enabled``, ``fallback_fonts``

Key Properties
--------------

Commonly used properties include:

- ``text`` - Markdown source text
- ``font_name`` / ``code_font_name`` - Body/code font selection
- ``font_size`` (alias of ``base_font_size``) - Base text size
- ``color`` / ``link_color`` / ``code_bg_color`` - Core colors
- ``halign`` / ``valign`` / ``padding`` / ``text_size`` - Layout and alignment
- ``render_mode`` - ``'widgets'``, ``'texture'``, or ``'auto'``
- ``image_size_mode`` - ``'contain_no_upscale'`` or ``'fill_width'`` for Markdown images
- ``auto_size_height`` / ``strict_label_mode`` - Sizing behavior

See Also
--------

- :doc:`rendering` - How property changes trigger rendering updates
- :doc:`../usage_guide` - Practical usage of these properties
- :doc:`../label_compatibility` - Label API compatibility details
