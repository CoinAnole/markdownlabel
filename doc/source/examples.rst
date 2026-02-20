.. _examples:

Examples
========

This page provides complete working examples demonstrating MarkdownLabel features.

Simple Demo
-----------

A minimal example showing basic MarkdownLabel usage.

**File:** ``examples/simple_demo.py``

.. code-block:: python

    #!/usr/bin/env python3
    """
    Simple MarkdownLabel Demo

    A minimal example demonstrating the MarkdownLabel widget.
    Run with: python3 simple_demo.py
    """
    from kivy.base import runTouchApp
    from kivy_garden.markdownlabel import MarkdownLabel

    MARKDOWN_TEXT = """
    # Hello MarkdownLabel

    This is a **simple** demonstration of the MarkdownLabel widget.

    ## Features

    - *Italic* text
    - **Bold** text
    - `inline code`
    - [Clickable links](https://kivy.org)

    ### Lists

    1. First item
    2. Second item
    3. Third item

    > This is a blockquote.
    > It can span multiple lines.

    Enjoy using MarkdownLabel in your Kivy apps!
    """

    if __name__ == '__main__':
        runTouchApp(MarkdownLabel(
            text=MARKDOWN_TEXT,
            link_style='styled',  # Makes links blue and underlined
        ))

**Features Demonstrated:**

- Headings (H1-H3)
- Bold and italic text
- Inline code
- Unordered and ordered lists
- Blockquotes
- Clickable links

Running the Simple Demo
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    cd examples
    python simple_demo.py

Full-Featured Demo
------------------

A comprehensive demonstration of all Label-compatible properties.

**File:** ``examples/full_featured_demo.py``

This example showcases:

- **font_name** - Different font families
- **font_size** - Various text sizes
- **color** - Different text colors
- **line_height** - Line spacing variations
- **halign** - Text alignment options
- **padding** - Content padding
- **disabled** - Disabled state with custom colors
- Full sample_markdown.md rendering

**Running the Demo:**

.. code-block:: bash

    cd examples
    python full_featured_demo.py

The demo opens a scrollable window (1400x900) with multiple sections, each demonstrating a specific property with side-by-side comparisons.

Sample Markdown
---------------

The ``examples/sample_markdown.md`` file contains comprehensive Markdown examples used by the full-featured demo:

.. code-block:: markdown

    # Sample Markdown Document

    This document demonstrates various Markdown features.

    ## Text Formatting

    - **Bold text** using double asterisks
    - *Italic text* using single asterisks
    - ***Bold and italic*** using triple asterisks
    - ~~Strikethrough~~ using tildes
    - `Inline code` using backticks

    ## Lists

    ### Unordered
    - Item 1
    - Item 2
      - Nested item
      - Another nested item
    - Item 3

    ### Ordered
    1. First item
    2. Second item
    3. Third item

    ## Tables

    | Feature | Supported | Notes |
    |:--------|:---------:|------:|
    | Bold    | Yes       | **text** |
    | Italic  | Yes       | *text* |

    ## Code Blocks

    ```python
    def hello():
        print("Hello, World!")
    ```

    ## Blockquotes

    > This is a blockquote.
    > It can span multiple lines.

    ## Links

    Visit [Kivy](https://kivy.org) for more information.

Link Handling Example
---------------------

Example showing how to handle link clicks:

.. code-block:: python

    from kivy.app import App
    from kivy.uix.boxlayout import BoxLayout
    from kivy_garden.markdownlabel import MarkdownLabel
    import webbrowser

    class LinkExampleApp(App):
        def build(self):
            layout = BoxLayout(orientation='vertical', padding=20)

            markdown_text = """
    # Link Examples

    Click these links to test:

    - [Open Kivy Website](https://kivy.org)
    - [Python Documentation](https://docs.python.org)
    - [Markdown Guide](https://www.markdownguide.org)
    """

            label = MarkdownLabel(
                text=markdown_text,
                link_style='styled',
                link_color=[0.2, 0.6, 1, 1],
                base_font_size=16
            )
            label.bind(on_ref_press=self.on_link_click)

            layout.add_widget(label)
            return layout

        def on_link_click(self, instance, url):
            print(f'Opening: {url}')
            webbrowser.open(url)

    if __name__ == '__main__':
        LinkExampleApp().run()

Styling Examples
----------------

Dark Theme Example
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from kivy.base import runTouchApp
    from kivy_garden.markdownlabel import MarkdownLabel

    dark_label = MarkdownLabel(
        text='# Dark Mode\\n\\nContent here',
        color=[0.9, 0.9, 0.9, 1],          # Light text
        code_bg_color=[0.15, 0.15, 0.15, 1],  # Dark background
        link_color=[0.4, 0.7, 1, 1],       # Light blue links
        base_font_size=15,
        padding=[20, 20]
    )

    runTouchApp(dark_label)

Documentation Style
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    doc_label = MarkdownLabel(
        text='# Documentation',
        base_font_size=15,
        line_height=1.6,
        color=[0.2, 0.2, 0.2, 1],
        code_bg_color=[0.95, 0.95, 0.95, 1],
        padding=[30, 30]
    )

Auto-Sizing Example
-------------------

Example with automatic height sizing:

.. code-block:: python

    from kivy.uix.boxlayout import BoxLayout
    from kivy_garden.markdownlabel import MarkdownLabel

    layout = BoxLayout(orientation='vertical')

    # This label will automatically size to fit content
    label = MarkdownLabel(
        text='# Auto-sized\\n\\nContent here',
        auto_size_height=True,   # Default
        size_hint_y=None         # Required for auto-size
    )

    layout.add_widget(label)

Scrollable Content
------------------

Example with ScrollView:

.. code-block:: python

    from kivy.uix.scrollview import ScrollView
    from kivy.uix.boxlayout import BoxLayout
    from kivy_garden.markdownlabel import MarkdownLabel

    scroll = ScrollView()

    label = MarkdownLabel(
        text=long_markdown_content,  # Your long content
        size_hint_y=None
    )
    label.bind(texture_size=label.setter('size'))

    scroll.add_widget(label)

Prerequisites
-------------

All examples require the MarkdownLabel package:

.. code-block:: bash

    pip install kivy_garden.markdownlabel

Or install in development mode from the repository:

.. code-block:: bash

    pip install -e .

Troubleshooting
---------------

**ModuleNotFoundError**
    Ensure the package is installed (see Prerequisites)

**SDL2 Errors (Linux)**
    Install required libraries:

    .. code-block:: bash

        sudo apt-get install -y libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev

**Window Too Small**
    Resize manually or modify ``Config.set()`` in the demo files

See Also
--------

- :doc:`usage_guide` - Comprehensive usage patterns
- :doc:`styling_guide` - Style customization guide
- :doc:`events` - Event handling details
- `examples/README.md <https://github.com/kivy-garden/markdownlabel/blob/master/examples/README.md>`_ - Additional example documentation
