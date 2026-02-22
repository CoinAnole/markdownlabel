.. _getting_started:

Getting Started
===============

Welcome to MarkdownLabel! This guide will help you get up and running with the widget.

What is MarkdownLabel?
----------------------

**MarkdownLabel** is a Kivy widget that renders Markdown text as interactive UI elements. Unlike a standard Kivy Label, MarkdownLabel:

- Renders full Markdown syntax (headings, lists, tables, code blocks, etc.)
- Supports interactive links with click events
- Provides a Label-compatible API for easy migration
- Extends BoxLayout (not Label) to accommodate complex Markdown structures

Quick Start
-----------

1. **Install the package** (see :doc:`installation`)

2. **Create a simple example**::

    from kivy.base import runTouchApp
    from kivy_garden.markdownlabel import MarkdownLabel

    MARKDOWN_TEXT = """
    # Hello MarkdownLabel

    This is a **simple** demonstration.

    ## Features

    - *Italic* text
    - **Bold** text
    - `inline code`
    - [Clickable links](https://kivy.org)
    """

    runTouchApp(MarkdownLabel(text=MARKDOWN_TEXT))

3. **Run your app**::

    python your_app.py

Next Steps
----------

- :doc:`usage_guide` - Learn comprehensive usage patterns
- :doc:`styling_guide` - Customize fonts, colors, and appearance
- :doc:`label_compatibility` - Understand Label API compatibility
- :doc:`examples` - See complete working examples
- :doc:`api` - Browse the API reference

Supported Markdown
------------------

MarkdownLabel supports standard Markdown syntax:

**Block Elements:**

- Headings (H1-H6)
- Paragraphs
- Unordered lists (``-``, ``*``, ``+``)
- Ordered lists (``1.``, ``2.``, etc.)
- Tables
- Code blocks (fenced with triple backticks)
- Blockquotes (``>``)
- Horizontal rules (``---``)

**Inline Elements:**

- Bold (``**text**`` or ``__text__``)
- Italic (``*text*`` or ``_text_``)
- Strikethrough (``~~text~~``)
- Inline code (single backticks around text)
- Links (``[text](url)``)
- Images (``![alt](url)``)

Key Concepts
------------

**Not a True Label**
    MarkdownLabel extends ``BoxLayout``, not ``Label``. This is necessary because Markdown content requires multiple child widgets (headings, lists, tables, etc.).

**Label-Compatible API**
    Most common Label properties work: ``font_name``, ``color``, ``halign``, ``valign``, ``padding``, ``text_size``, etc.

**Two Rendering Modes**
    - **Widget mode** (default ``render_mode='widgets'``): Renders as actual Kivy widgets
    - **Texture mode**: Renders to a texture for better performance with static content
      that does not include Markdown images. Content with ``![alt](url)`` falls
      back to widget mode automatically.

**Interactive Links**
    Use ``bind(on_ref_press=your_callback)`` to handle link clicks.

**Auto-Sizing**
    By default, ``auto_size_height`` is ``False``. Enable it with ``auto_size_height=True``.
