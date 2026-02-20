.. _kivy_renderer_tables_module:

Kivy Renderer Tables Module
===========================

The ``kivy_renderer_tables`` module provides table rendering support as a mixin for ``KivyRenderer``.

Module Contents
---------------

.. automodule:: kivy_garden.markdownlabel.kivy_renderer_tables
   :members:
   :undoc-members:
   :show-inheritance:

KivyRendererTables Mixin
------------------------

.. autoclass:: kivy_garden.markdownlabel.kivy_renderer_tables.KivyRendererTables
   :members:
   :undoc-members:
   :show-inheritance:

   .. rubric:: Table Render Methods

   .. autosummary::
      :nosignatures:

      table
      table_head
      table_body
      table_row
      table_cell

Table Support
-------------

Tables are rendered using Kivy's ``GridLayout`` with appropriate column constraints. The mixin extends ``KivyRenderer`` to handle:

- Table headers (bold text)
- Table body rows
- Cell alignment (left, center, right)
- Column widths based on content

Markdown Table Syntax
---------------------

MarkdownLabel supports standard Markdown table syntax::

    | Header 1 | Header 2 | Header 3 |
    |----------|----------|----------|
    | Cell 1   | Cell 2   | Cell 3   |
    | Cell 4   | Cell 5   | Cell 6   |

Alignment can be specified in the separator line::

    | Left | Center | Right |
    |:-----|:------:|------:|
    | L    |   C    |     R |

Implementation Details
----------------------

- Tables are rendered as nested layouts
- Each row is a horizontal BoxLayout
- Cells use the same styling as regular text
- Header rows use bold formatting automatically

See Also
--------

- :doc:`kivy_renderer` - Main block renderer
- `mistune Table Plugin <https://mistune.lepture.com/en/latest/plugins.html#table>`_
