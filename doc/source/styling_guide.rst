.. _styling_guide:

Styling Guide
=============

This guide covers customizing the appearance of MarkdownLabel content.

Font Customization
------------------

Primary Font
~~~~~~~~~~~~

Set the main font for all text (except code blocks)::

    label.font_name = 'Arial'

Or using a font file path::

    label.font_name = 'fonts/MyCustomFont.ttf'

Code Font
~~~~~~~~~

Set the font for inline and block code::

    label.code_font_name = 'monospace'

Font Fallback
~~~~~~~~~~~~~

Enable font fallback for multi-language support::

    label.fallback_enabled = True
    label.fallback_fonts = ['NotoSansCJK', 'NotoColorEmoji']

Base Font Size
~~~~~~~~~~~~~~

The ``base_font_size`` controls the normal text size. Headings scale from this::

    label.base_font_size = 16  # Normal text
    # H1 = 32, H2 = 24, etc. (scaled from base)

You can also use ``font_size`` as an alias::

    label.font_size = 16  # Same as base_font_size

Color Customization
-------------------

Text Color
~~~~~~~~~~

Set the main text color (RGB + Alpha)::

    label.color = [1, 1, 1, 1]  # White
    label.color = [0, 0, 0, 1]  # Black
    label.color = [1, 0, 0, 0.5]  # Semi-transparent red

Colors are specified as lists of four floats: ``[R, G, B, A]`` where each value is 0.0 to 1.0.

Link Color
~~~~~~~~~~

Customize link appearance::

    label.link_color = [0, 0.5, 1, 1]  # Blue

Code Background
~~~~~~~~~~~~~~~

Set the background color for code blocks::

    label.code_bg_color = [0.1, 0.1, 0.1, 1]  # Dark gray

Disabled State
~~~~~~~~~~~~~~

When the widget is disabled (default value shown)::

    label.disabled_color = [1, 1, 1, 0.3]

Alignment
---------

Horizontal Alignment
~~~~~~~~~~~~~~~~~~~~

Align text horizontally::

    label.halign = 'auto'      # Default
    label.halign = 'left'
    label.halign = 'center'
    label.halign = 'right'
    label.halign = 'justify'   # Full justification

**Note:** ``auto`` is also supported for RTL text detection.

Vertical Alignment
~~~~~~~~~~~~~~~~~~

When height is constrained::

    label.valign = 'bottom'    # Default
    label.valign = 'top'
    label.valign = 'middle'    # Or 'center'
    label.valign = 'center'

Spacing
-------

Container Padding
~~~~~~~~~~~~~~~~~

Padding around the entire content::

    label.padding = [10]              # All sides: 10px
    label.padding = [10, 20]          # Horizontal: 10, Vertical: 20
    label.padding = [10, 20, 10, 20]  # Left, Top, Right, Bottom

Text Padding
~~~~~~~~~~~~

Padding inside text blocks::

    label.text_padding = [5, 5, 5, 5]

Line Height
~~~~~~~~~~~

Adjust line spacing::

    label.line_height = 1.0  # Default
    label.line_height = 1.2  # 20% extra space
    label.line_height = 1.5  # 50% extra space

Link Styling
------------

Link Appearance
~~~~~~~~~~~~~~~

Control how links are rendered::

    label.link_style = 'styled'    # Default: colored + underlined
    label.link_style = 'unstyled'  # Label-like appearance

Advanced Styling
----------------

Outline
~~~~~~~

Add text outline::

    label.outline_width = 1
    label.outline_color = [0, 0, 0, 1]  # Black outline

Mipmap
~~~~~~

Enable mipmap for better scaling quality::

    label.mipmap = True

Text Language
~~~~~~~~~~~~~

Set text language for proper shaping::

    label.text_language = 'en_US'
    label.text_language = 'ar_AR'  # Arabic

Base Direction
~~~~~~~~~~~~~~

Set text direction::

    label.base_direction = None    # Default (automatic)
    label.base_direction = 'ltr'
    label.base_direction = 'rtl'   # Right-to-left

Advanced Font Properties
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    label.font_family = 'sans-serif'
    label.font_context = 'default'
    label.font_features = ''
    label.font_hinting = 'normal'   # 'normal', 'light', 'mono', 'none'
    label.font_kerning = True
    label.font_blended = True

Styling Examples
----------------

Dark Theme
~~~~~~~~~~

.. code-block:: python

    label = MarkdownLabel(
        text='# Dark Theme\\n\\nContent',
        color=[0.9, 0.9, 0.9, 1],          # Light gray text
        code_bg_color=[0.2, 0.2, 0.2, 1],  # Dark code blocks
        link_color=[0.4, 0.7, 1, 1],       # Light blue links
    )

Documentation Style
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    label = MarkdownLabel(
        text='# Docs',
        base_font_size=15,
        line_height=1.6,
        color=[0.2, 0.2, 0.2, 1],
        code_bg_color=[0.95, 0.95, 0.95, 1],
        padding=[20, 20],
    )

Terminal Style
~~~~~~~~~~~~~~

.. code-block:: python

    label = MarkdownLabel(
        text='# Terminal',
        font_name='monospace',
        color=[0, 1, 0, 1],                # Green text
        code_bg_color=[0, 0.1, 0, 1],      # Dark green background
    )

Dynamic Styling
---------------

Change styles at runtime::

    # Single property
    label.color = [1, 0, 0, 1]

    # Batch update
    label.update_style(
        color=[0, 0, 1, 1],
        base_font_size=20,
        halign='center'
    )

Style-Only Properties
---------------------

These properties update in-place without rebuilding::

- ``color`` - Text color
- ``font_name`` - Primary font
- ``base_font_size`` - Font size
- ``halign`` - Horizontal alignment
- ``valign`` - Vertical alignment
- ``padding`` - Container padding
- ``line_height`` - Line spacing
- ``outline_width``, ``outline_color`` - Text outline
- ``mipmap`` - Mipmap quality
- ``base_direction`` - Text direction
- ``text_language`` - Language hint

Structure Properties
--------------------

These properties require a full rebuild::

- ``link_color`` - Link color (affects BBCode generation)
- ``code_bg_color`` - Code background
- ``link_style`` - Link appearance style
- ``fallback_enabled`` - Font fallback
- ``fallback_fonts`` - Fallback font list

See Also
--------

- :doc:`usage_guide` - General usage patterns
- :doc:`label_compatibility` - Label property reference
- :doc:`../modules/properties` - Property system details
