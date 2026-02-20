.. _properties_module:

Properties Module
=================

The ``properties`` module defines all Kivy properties for the MarkdownLabel widget, including property classifications for style updates vs full rebuilds.

Module Contents
---------------

.. automodule:: kivy_garden.markdownlabel.properties
   :members:
   :undoc-members:
   :show-inheritance:

Property Classification
-----------------------

Properties in MarkdownLabel are classified into two categories:

**STYLE_ONLY_PROPERTIES**
   Changes to these properties update the widget tree in-place without rebuilding. This is faster and preserves widget identity.

   Examples: ``color``, ``font_name``, ``halign``, ``valign``, ``padding``, ``outline_width``

**STRUCTURE_PROPERTIES**
   Changes to these properties require a full rebuild of the widget tree because they affect the generated markup or widget structure.

   Examples: ``link_color``, ``code_bg_color``, ``link_style``, ``fallback_enabled``

MarkdownLabelProperties Class
-------------------------------

.. autoclass:: kivy_garden.markdownlabel.properties.MarkdownLabelProperties
   :members:
   :undoc-members:
   :show-inheritance:

Key Properties
--------------

**Text Content:**

.. autodata:: kivy_garden.markdownlabel.properties.MarkdownLabelProperties.text
   :annotation:

**Font Properties:**

.. autodata:: kivy_garden.markdownlabel.properties.MarkdownLabelProperties.font_name
   :annotation:

.. autodata:: kivy_garden.markdownlabel.properties.MarkdownLabelProperties.base_font_size
   :annotation:

.. autodata:: kivy_garden.markdownlabel.properties.MarkdownLabelProperties.code_font_name
   :annotation:

**Color Properties:**

.. autodata:: kivy_garden.markdownlabel.properties.MarkdownLabelProperties.color
   :annotation:

.. autodata:: kivy_garden.markdownlabel.properties.MarkdownLabelProperties.link_color
   :annotation:

.. autodata:: kivy_garden.markdownlabel.properties.MarkdownLabelProperties.code_bg_color
   :annotation:

**Layout Properties:**

.. autodata:: kivy_garden.markdownlabel.properties.MarkdownLabelProperties.halign
   :annotation:

.. autodata:: kivy_garden.markdownlabel.properties.MarkdownLabelProperties.valign
   :annotation:

.. autodata:: kivy_garden.markdownlabel.properties.MarkdownLabelProperties.padding
   :annotation:

See Also
--------

- :doc:`rendering` - How property changes trigger rendering updates
- :doc:`../usage_guide` - Practical usage of these properties
