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
* **Label compatibility**: Drop-in replacement for Kivy's Label widget with support for common properties like `font_name`, `color`, `halign`, `valign`, `padding`, `text_size`, and more

Installation
------------

```bash
pip install kivy_garden.markdownlabel
```

Usage
-----

### Basic Usage

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

### Label Compatibility

MarkdownLabel supports many properties from Kivy's standard Label widget, making it easy to switch between the two:

```python
# Use familiar Label properties
label = MarkdownLabel(
    text='# Markdown Content\n\nWith **formatting**',
    font_name='Arial',           # Custom font for all text
    font_size=16,                # Alias for base_font_size
    color=[1, 1, 1, 1],          # Text color
    halign='center',             # Horizontal alignment
    valign='middle',             # Vertical alignment
    padding=[10, 10, 10, 10],    # Container padding
    text_size=[400, None],       # Width constraint for wrapping
    line_height=1.2,             # Line spacing
    disabled_color=[1, 1, 1, 0.3]  # Color when disabled
)

# Advanced font properties
label.font_family = 'sans-serif'
label.font_kerning = True
label.font_hinting = 'normal'

# Text processing
label.unicode_errors = 'replace'
label.strip = True

# No-op properties (accepted for compatibility, but ignored)
label.bold = True      # Markdown controls formatting
label.italic = True    # These don't raise errors
label.markup = True    # Always True for MarkdownLabel
```

### Supported Label Properties

**Styling Properties:**
- `font_name` - Font for all text (except code blocks)
- `font_size` - Alias for `base_font_size`
- `color` - Text color (preserves `link_color` for links)
- `line_height` - Line spacing multiplier
- `disabled_color` - Color when widget is disabled

**Layout Properties:**
- `halign` - Horizontal alignment ('left', 'center', 'right', 'justify', 'auto')
- `valign` - Vertical alignment ('top', 'middle', 'center', 'bottom')
- `padding` - Container padding (single value, [h, v], or [l, t, r, b])
- `text_size` - Width/height constraints for text wrapping

**Advanced Font Properties:**
- `font_family`, `font_context`, `font_features`
- `font_hinting`, `font_kerning`, `font_blended`

**Text Processing:**
- `unicode_errors` - Unicode error handling ('strict', 'replace', 'ignore')
- `strip` - Strip leading/trailing whitespace

**Compatibility Properties (no-op):**
- `bold`, `italic`, `underline`, `strikethrough`, `markup` - Accepted but ignored (Markdown controls formatting)

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
