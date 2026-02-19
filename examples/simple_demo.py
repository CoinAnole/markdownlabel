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
