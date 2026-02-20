.. _markdown_serializer_module:

Markdown Serializer Module
==========================

The ``markdown_serializer`` module provides functionality to convert the
Abstract Syntax Tree (AST) back to Markdown text. This is primarily used for
testing and debugging.

Module Contents
---------------

.. automodule:: kivy_garden.markdownlabel.markdown_serializer
   :members:
   :undoc-members:
   :show-inheritance:

Use Cases
---------

**Testing**
   Verify that parsed content can be accurately serialized back to Markdown

**Debugging**
   Inspect the AST structure by viewing the serialized output

**Round-trip Validation**
   Ensure no data is lost during parse-serialize cycles

Example Usage
-------------

.. code-block:: python

    from kivy_garden.markdownlabel import MarkdownLabel, MarkdownSerializer

    label = MarkdownLabel(text='# Hello\\n\\nWorld')

    # Get the AST
    ast = label.get_ast()

    # Serialize back to Markdown
    serializer = MarkdownSerializer()
    markdown = serializer.serialize(ast)

    print(markdown)  # Outputs: # Hello\\n\\nWorld

Supported Elements
------------------

The serializer supports all Markdown elements that the parser produces:

- Inline: text, emphasis, strong, codespan, links, strikethrough
- Blocks: paragraphs, headings, lists, code blocks, block quotes
- Tables: table structure with headers and cells

Limitations
-----------

- Original formatting (line breaks, indentation) may not be preserved
- Reference-style links are converted to inline links
- Some HTML elements may not serialize cleanly

See Also
--------

- :doc:`markdownlabel` - Using ``get_ast()`` and ``to_markdown()`` methods
