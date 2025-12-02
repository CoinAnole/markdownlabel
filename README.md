MarkdownLabel
=============

[![Github Build Status](https://github.com/kivy-garden/markdownlabel/workflows/Garden%20flower/badge.svg)](https://github.com/kivy-garden/markdownlabel/actions)

A Kivy widget that parses and renders Markdown documents as structured, interactive Kivy UI elements. It serves as a drop-in replacement for Kivy's standard Label widget but supports full Markdown syntax.

See https://kivy-garden.github.io/markdownlabel/ for the rendered flower docs.

Please see the garden [instructions](https://kivy-garden.github.io) for how to use kivy garden flowers.

Features
--------

* Full Markdown syntax support (headings, paragraphs, lists, tables, code blocks, block quotes, images)
* Inline formatting (bold, italic, strikethrough, inline code, links)
* Interactive links with `on_ref_press` event
* Customizable styling (font sizes, colors, code font)
* Built on mistune parser with plugin support
* Auto-sizing widget that adapts to content

Installation
------------

```bash
pip install kivy_garden.markdownlabel
```

Usage
-----

```python
from kivy_garden.markdownlabel import MarkdownLabel

# Basic usage
label = MarkdownLabel(text='# Hello World\n\nThis is **bold** text.')

# Handle link clicks
def on_link_click(instance, url):
    print(f'Clicked: {url}')

label.bind(on_ref_press=on_link_click)

# Customize styling
label.base_font_size = 18
label.link_color = [0, 0.7, 1, 1]
label.code_bg_color = [0.1, 0.1, 0.1, 1]
```

CI
--

Every push or pull request run the [GitHub Action](https://github.com/kivy-garden/markdownlabel/actions) CI.
It tests the code on various OS and also generates wheels that can be released on PyPI upon a
tag. Docs are also generated and uploaded to the repo as well as artifacts of the CI.

Contributing
--------------

Check out our [contribution guide](CONTRIBUTING.md) and feel free to improve the flower.

License
---------

This software is released under the terms of the MIT License.
Please see the [LICENSE.txt](LICENSE.txt) file.

How to release
===============

See the garden [instructions](https://kivy-garden.github.io/#makingareleaseforyourflower) for how to make a new release.
