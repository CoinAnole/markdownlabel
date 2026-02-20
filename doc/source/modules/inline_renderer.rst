.. _inline_renderer_module:

Inline Renderer Module
======================

The ``inline_renderer`` module handles rendering of inline Markdown elements (bold, italic, links, etc.) to BBCode markup strings.

Module Contents
---------------

.. automodule:: kivy_garden.markdownlabel.inline_renderer
   :members:
   :undoc-members:
   :show-inheritance:

InlineRenderer Class
--------------------

.. autoclass:: kivy_garden.markdownlabel.InlineRenderer
   :members:
   :undoc-members:
   :show-inheritance:

   .. rubric:: Render Methods

   .. autosummary::
      :nosignatures:

      render_inline_text
      text
      emphasis  # italic
      strong    # bold
      codespan  # inline code
      link
      linebreak
      strikethrough

BBCode Conversion
-----------------

The ``InlineRenderer`` converts inline Markdown elements to Kivy BBCode:

=================== ===========================
Markdown            BBCode Output
=================== ===========================
``**bold**``        ``[b]bold[/b]``
``*italic*``         ``[i]italic[/i]``
``~~strikethrough~~`` ``[s]strikethrough[/s]``
`` `code` ``          ``[font=mono]code[/font]``
``[text](url)``       ``[ref=url][u][color=...]text[/color][/u][/ref]``
=================== ===========================

Security Note
-------------

User content is escaped to prevent markup injection. The ``escape_text()`` method ensures that literal text cannot interfere with BBCode parsing.

Link Styling
------------

Links can be rendered in two styles:

**Styled** (``link_style='styled'``)
   Links are rendered with underline and link color

**Plain** (``link_style='plain'``)
   Links are rendered without special styling

Example Usage
-------------

.. code-block:: python

    from kivy_garden.markdownlabel import InlineRenderer

    renderer = InlineRenderer(
        link_color=[0, 0.5, 1, 1],
        link_style='styled'
    )

    # Render inline elements
    result = renderer.render_inline_text(tokens)

See Also
--------

- :doc:`kivy_renderer` - Block-level rendering
- `Kivy BBCode Documentation <https://kivy.org/doc/stable/api-kivy.core.text.markup.html>`_
