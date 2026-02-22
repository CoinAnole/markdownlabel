.. _inline_renderer_module:

Inline Renderer Module
======================

The ``inline_renderer`` module handles rendering of inline Markdown elements
to Kivy BBCode markup strings.

Module Contents
---------------

.. automodule:: kivy_garden.markdownlabel.inline_renderer
   :members:
   :undoc-members:
   :show-inheritance:

BBCode Conversion
-----------------

The ``InlineRenderer`` converts inline Markdown elements to Kivy BBCode:

- ``**bold**`` -> ``[b]bold[/b]``
- ``*italic*`` -> ``[i]italic[/i]``
- ``~~strikethrough~~`` -> ``[s]strikethrough[/s]``
- `` `code` `` -> ``[font=...]code[/font]``
- ``[text](url)`` -> ``[ref=url]text[/ref]`` (optionally styled)

Security Note
-------------

User content is escaped to prevent markup injection. The
``escape_kivy_markup()`` helper ensures literal text cannot interfere with
BBCode parsing.

Link Styling
------------

Links can be rendered in two styles:

**Styled** (``link_style='styled'``)
   Links are rendered with underline and link color

**Unstyled** (``link_style='unstyled'``)
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
    result = renderer.render(tokens)

See Also
--------

- :doc:`kivy_renderer` - Block-level rendering
- `Kivy BBCode Documentation <https://kivy.org/doc/stable/api-kivy.core.text.markup.html>`_
