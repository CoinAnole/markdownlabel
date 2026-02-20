.. _font_fallback_module:

Font Fallback Module
====================

The ``font_fallback`` module provides font fallback helpers for cases where
primary fonts do not contain required glyphs.

Module Contents
---------------

.. automodule:: kivy_garden.markdownlabel.font_fallback
   :members:
   :undoc-members:
   :show-inheritance:

Font Fallback System
--------------------

When ``fallback_enabled`` is True, MarkdownLabel can use alternative fonts for characters not present in the primary font. This is especially useful for:

- Multi-language content
- Mathematical symbols
- Emoji support
- Special characters

Key Functions
-------------

- ``apply_fallback_markup()`` - Apply fallback font markup runs
- ``escape_kivy_markup()`` - Escape markup control characters safely

Configuration
-------------

Font fallback is configured via properties:

- ``fallback_enabled`` - Enable/disable fallback
- ``fallback_fonts`` - List of fallback font names/paths
- ``fallback_font_scales`` - Scale factors for fallback fonts

Example
-------

.. code-block:: python

    label = MarkdownLabel(
        text='Hello 世界 🌍',
        font_name='Arial',
        fallback_enabled=True,
        fallback_fonts=['NotoSansCJK', 'NotoColorEmoji'],
        fallback_font_scales={'NotoColorEmoji': 1.2}
    )

See Also
--------

- :doc:`properties` - Fallback-related properties
- :doc:`../styling_guide` - Font customization guide
