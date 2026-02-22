.. _utils_module:

Utils Module
============

The ``utils`` module provides internal helper utilities for widget traversal, testing support, and other common operations.

Module Contents
---------------

.. automodule:: kivy_garden.markdownlabel.utils
   :members:
   :undoc-members:
   :show-inheritance:

Utility Functions
-----------------

.. autofunction:: kivy_garden.markdownlabel.find_labels_recursive

.. autofunction:: kivy_garden.markdownlabel.collect_widget_ids

.. autofunction:: kivy_garden.markdownlabel.extract_font_tags

Widget Traversal
----------------

**find_labels_recursive**
   Recursively finds all Label widgets within a widget tree. Useful for:

   - Applying properties to all text labels
   - Testing and validation
   - Style updates

**collect_widget_ids**
   Collects all widgets with IDs from a widget tree. Returns a dictionary mapping IDs to widgets.

**extract_font_tags**
   Extracts font tag information from BBCode markup strings.

Example Usage
-------------

.. code-block:: python

    from kivy_garden.markdownlabel import MarkdownLabel, find_labels_recursive

    label = MarkdownLabel(text='# Test\\n\\nContent')

    # Find all child Labels
    child_labels = find_labels_recursive(label)
    print(f"Found {len(child_labels)} labels")

    # Collect widgets by ID
    from kivy_garden.markdownlabel.utils import collect_widget_ids
    widgets_by_id = collect_widget_ids(label)

Internal Use
------------

These utilities are primarily used internally by:

- ``MarkdownLabelRendering`` for style updates
- Test suite for validation
- Custom renderers extending the base classes

Note
----

These functions are part of the public API and can be used in your applications, but they are primarily intended for internal use and advanced customization.

See Also
--------

- :doc:`markdownlabel` - Main widget that uses these utilities
- :doc:`rendering` - Rendering mixin that uses widget traversal
