.. _label_compatibility:

Label API Compatibility
=======================

MarkdownLabel provides a Label-compatible API to make migration from standard Kivy Labels easy.

Compatibility Overview
----------------------

While MarkdownLabel extends ``BoxLayout`` (not ``Label``), it mirrors most common Label styling properties. This allows you to replace Labels with MarkdownLabels with minimal code changes.

Fully Supported Properties
--------------------------

These properties work exactly like Kivy Label:

**Styling Properties**

.. list-table::
   :header-rows: 1

   * - Property
     - Description
     - Notes
   * - ``font_name``
     - Font for all text (except code)
     - String or file path
   * - ``font_size``
     - Alias for ``base_font_size``
     - Accepts for compatibility
   * - ``color``
     - Text color [R,G,B,A]
     - Preserves link_color for links
   * - ``line_height``
     - Line spacing multiplier
     - 1.0 = normal, 1.2 = default
   * - ``disabled_color``
     - Color when disabled
     - Default: [0.5,0.5,0.5,1]

**Layout Properties**

.. list-table::
   :header-rows: 1

   * - Property
     - Values
     - Description
   * - ``halign``
     - 'left', 'center', 'right', 'justify', 'auto'
     - Horizontal alignment
   * - ``valign``
     - 'top', 'middle', 'center', 'bottom'
     - Vertical alignment
   * - ``padding``
     - [val], [h,v], or [l,t,r,b]
     - Container padding
   * - ``text_size``
     - [width, height]
     - Constrain text dimensions

**Advanced Font Properties**

.. list-table::
   :header-rows: 1

   * - Property
     - Description
   * - ``font_family``
     - Font family name
   * - ``font_context``
     - Font context for Pango
   * - ``font_features``
     - OpenType font features
   * - ``font_hinting``
     - 'normal', 'light', 'mono', 'none'
   * - ``font_kerning``
     - Enable/disable kerning
   * - ``font_blended``
     - Blended font rendering

**Text Processing**

.. list-table::
   :header-rows: 1

   * - Property
     - Description
   * - ``unicode_errors``
     - 'strict', 'replace', 'ignore'
   * - ``strip``
     - Strip leading/trailing whitespace

**Read-Only Properties**

.. list-table::
   :header-rows: 1

   * - Property
     - Description
   * - ``texture_size``
     - Aggregated from child Labels
   * - ``refs``
     - Reference positions for links
   * - ``anchors``
     - Anchor positions

Compatibility Properties (No-Op)
--------------------------------

These properties are accepted for compatibility but have no effect (Markdown controls formatting):

.. list-table::
   :header-rows: 1

   * - Property
     - Behavior
   * - ``bold``
     - Ignored (use ``**text**`` in Markdown)
   * - ``italic``
     - Ignored (use ``*text*`` in Markdown)
   * - ``underline``
     - Ignored (Markdown doesn't support)
   * - ``strikethrough``
     - Ignored (use ``~~text~~`` in Markdown)
   * - ``markup``
     - Always True for MarkdownLabel
   * - ``shorten``
     - No-op (not applicable)
   * - ``max_lines``
     - No-op (not applicable)

Key Differences from Label
--------------------------

**Not a True Label Subclass**

.. code-block:: python

    # This is False
    isinstance(markdown_label, Label)  # False

    # This is True
    isinstance(markdown_label, BoxLayout)  # True

**No Texture Property**

Standard Label has a ``texture`` property. MarkdownLabel provides this only when:

- ``render_mode='texture'`` is set, OR
- ``aggregate_texture_enabled=True`` (property exists but may be read-only)

**Size Behavior**

Labels default to ``size_hint_y=None``. MarkdownLabel defaults to ``size_hint_y=1`` but changes to ``None`` when ``auto_size_height=True`` (the default).

**Text Property**

In Label, ``text`` is plain text. In MarkdownLabel, ``text`` is Markdown source.

Migration Guide
---------------

**Basic Migration:**

.. code-block:: python

    # Before (Label)
    from kivy.uix.label import Label
    label = Label(text='Hello World', font_size=20)

    # After (MarkdownLabel)
    from kivy_garden.markdownlabel import MarkdownLabel
    label = MarkdownLabel(text='Hello World', font_size=20)

**Adding Markdown:**

.. code-block:: python

    # Simple upgrade to Markdown
    label = MarkdownLabel(text='# Hello\\n\\nThis is **bold**.')

**Preserving Compatibility:**

.. code-block:: python

    # Works with both Label and MarkdownLabel
    def create_label(widget_class, text, **kwargs):
        return widget_class(text=text, **kwargs)

    # Can switch between them
    label = create_label(Label, 'Plain text')
    md_label = create_label(MarkdownLabel, '# Markdown')

Property Mapping
----------------

Properties unique to MarkdownLabel that map to Label concepts:

.. list-table::
   :header-rows: 1

   * - MarkdownLabel Property
     - Equivalent To
   * - ``base_font_size``
     - ``font_size``
   * - ``auto_size_height``
     - ``size_hint_y=None`` behavior
   * - ``strict_label_mode``
     - Enforces Label-like sizing

Unsupported Label Features
--------------------------

These Label features are not available in MarkdownLabel:

- ``text`` as property reference (use Markdown link syntax)
- ``texture`` (only in texture mode)
- ``mipmap`` at Label level (applies to all rendered text)
- Direct canvas access for text

Best Practices
--------------

1. **Use Markdown for formatting** instead of trying to use bold/italic properties
2. **Set ``text_size`` for wrapping** just like with Label
3. **Use ``update_style()``** for batch property changes
4. **Check ``texture_size``** for layout calculations
5. **Remember it's a BoxLayout** when adding to parent layouts

Example: Switching from Label
------------------------------

.. code-block:: python

    from kivy.uix.boxlayout import BoxLayout
    from kivy_garden.markdownlabel import MarkdownLabel

    class MyWidget(BoxLayout):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

            # Works just like Label
            label = MarkdownLabel(
                text='# Title\\n\\nDescription',
                font_name='Arial',
                font_size=16,
                color=[0.2, 0.2, 0.2, 1],
                halign='left',
                padding=[10, 10],
                size_hint_y=None,
                text_size=[400, None]
            )
            label.bind(texture_size=label.setter('size'))

            self.add_widget(label)

See Also
--------

- :doc:`usage_guide` - General usage patterns
- :doc:`styling_guide` - Style customization
- `Kivy Label Documentation <https://kivy.org/doc/stable/api-kivy.uix.label.html>`_
