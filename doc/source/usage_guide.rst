.. _usage_guide:

Usage Guide
===========

This guide covers comprehensive usage patterns for MarkdownLabel.

Basic Usage
-----------

Setting Markdown Content
~~~~~~~~~~~~~~~~~~~~~~~~

Use the ``text`` property to set Markdown content::

    from kivy_garden.markdownlabel import MarkdownLabel

    label = MarkdownLabel(text='# Hello\\n\\nThis is **bold** text.')

You can update content dynamically::

    label.text = '# New Content\\n\\nUpdated **markdown**.'

Handling Link Clicks
~~~~~~~~~~~~~~~~~~~~

Bind to the ``on_ref_press`` event::

    def on_link_click(instance, url):
        print(f'Clicked: {url}')

    label.bind(on_ref_press=on_link_click)

See :doc:`events` for detailed event handling documentation.

Label-Compatible Properties
---------------------------

Many Kivy Label properties work with MarkdownLabel:

.. code-block:: python

    label = MarkdownLabel(
        text='# Content',
        font_name='Arial',
        font_size=16,           # Maps to base_font_size
        color=[1, 1, 1, 1],     # White text
        halign='center',        # Horizontal alignment
        valign='middle',        # Vertical alignment
        padding=[10, 10],       # Container padding
        line_height=1.2,        # Line spacing
    )

See :doc:`label_compatibility` for the complete compatibility reference.

Auto-Sizing Behavior
--------------------

By default, MarkdownLabel automatically sizes to fit its content.

Enable Auto-Size (Default)
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    label = MarkdownLabel(
        text='# Heading\\n\\nContent',
        auto_size_height=True,   # Default
        size_hint_y=None         # Required for auto-size
    )

Disable Auto-Size
~~~~~~~~~~~~~~~~~

.. code-block:: python

    label = MarkdownLabel(
        text='# Heading',
        auto_size_height=False,
        size_hint_y=1           # Fill available space
    )

Text Wrapping
-------------

Use ``text_size`` to constrain text width and enable wrapping:

.. code-block:: python

    label = MarkdownLabel(
        text='Long text that should wrap to multiple lines...',
        text_size=[400, None],  # Fixed width, auto height
    )

**Constrain both dimensions:**

.. code-block:: python

    label = MarkdownLabel(
        text='Content',
        text_size=[400, 300],   # Fixed width and height
    )

Rendering Modes
---------------

Widget Mode (Default)
~~~~~~~~~~~~~~~~~~~~~

Renders as actual Kivy widgets. Best for:

- Interactive content (links)
- Dynamic styling changes
- Mixed content types

.. code-block:: python

    label = MarkdownLabel(text='Content', render_mode='widget')

Texture Mode
~~~~~~~~~~~~

Renders to a texture for better performance. Best for:

- Static content
- Large documents
- Performance-critical applications

.. code-block:: python

    label = MarkdownLabel(text='Content', render_mode='texture')

**Note:** Links still work in texture mode via hit-testing.

Strict Label Mode
~~~~~~~~~~~~~~~~~

Enforces Label-like behavior with fixed height:

.. code-block:: python

    label = MarkdownLabel(
        text='Content',
        strict_label_mode=True,
        text_size=[400, 200]
    )

Updating Styles
---------------

Individual Properties
~~~~~~~~~~~~~~~~~~~~~

Change properties directly::

    label.color = [1, 0, 0, 1]      # Red text
    label.base_font_size = 20        # Larger font
    label.halign = 'right'           # Right alignment

Batch Updates
~~~~~~~~~~~~~

Use ``update_style()`` for multiple changes with single refresh::

    label.update_style(
        color=[0, 0, 1, 1],
        base_font_size=18,
        halign='center'
    )

Working with the AST
--------------------

Access the parsed AST::

    ast = label.get_ast()
    print(ast)  # List of token dictionaries

Serialize back to Markdown::

    markdown = label.to_markdown()
    print(markdown)

Performance Tips
----------------

1. **Use texture mode** for large static documents
2. **Batch style updates** with ``update_style()``
3. **Set appropriate text_size** to avoid unnecessary calculations
4. **Disable auto_size_height** if you don't need dynamic sizing
5. **Use ``force_rebuild()``** only when necessary

Common Patterns
---------------

Scrollable Content
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from kivy.uix.scrollview import ScrollView

    scroll = ScrollView()
    label = MarkdownLabel(
        text=long_markdown_content,
        size_hint_y=None
    )
    label.bind(texture_size=label.setter('size'))
    scroll.add_widget(label)

Responsive Design
~~~~~~~~~~~~~~~~~

.. code-block:: python

    from kivy.core.window import Window

    label = MarkdownLabel(text='Content')

    def on_window_size(instance, size):
        label.text_size = [size[0] * 0.9, None]

    Window.bind(size=on_window_size)

See Also
--------

- :doc:`styling_guide` - Font and color customization
- :doc:`label_compatibility` - Complete Label API reference
- :doc:`events` - Event handling details
- :doc:`examples` - Working code examples
