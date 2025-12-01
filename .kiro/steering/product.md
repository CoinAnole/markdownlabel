# Product Overview

**MarkdownLabel** is a Kivy Garden flower (widget package) that renders Markdown documents as interactive Kivy UI elements.

## Purpose

Provides a Label-compatible API for common styling properties while supporting full Markdown syntax, allowing developers to display rich formatted text in Kivy applications. Note: MarkdownLabel extends BoxLayout (not Label) because Markdown rendering requires multiple widgets.

## Key Features

- Full Markdown syntax support (headings, lists, tables, code blocks, block quotes, images)
- Inline formatting (bold, italic, strikethrough, inline code, links)
- Interactive links with `on_ref_press` event handling
- Customizable styling (fonts, colors, sizes)
- Built on mistune parser (v3.0+) with plugin support
- Label API compatibility for easy migration from standard Kivy Labels

## Target Users

Kivy application developers who need to display formatted text content without manually constructing complex widget hierarchies.
