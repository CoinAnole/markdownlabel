# MarkdownLabel Examples

This directory contains example applications demonstrating the MarkdownLabel widget from the `kivy_garden.markdownlabel` flower.

## Files

- **simple_demo.py** - A minimal example showing basic MarkdownLabel usage
- **full_featured_demo.py** - A comprehensive demo showcasing all Label-compatible properties
- **markdownlabel_test_pattern.png** - Local test image used by the full-featured demo
- **sample_markdown.md** - Sample Markdown content used by the full-featured demo

## Prerequisites

Ensure you have the MarkdownLabel package installed:

```bash
pip install kivy_garden.markdownlabel
```

Or install in development mode from the repository root:

```bash
pip install -e .
```

## Running the Examples

### Simple Demo

A minimal example demonstrating basic Markdown rendering:

```bash
python3 simple_demo.py
```

This example shows:
- Headings
- Bold and italic text
- Lists (ordered and unordered)
- Inline code
- Clickable links

### Full-Featured Demo

A comprehensive demonstration of all Label-compatible properties:

```bash
python3 full_featured_demo.py
```

This example demonstrates:
- **font_name** - Different font families
- **font_size** - Various text sizes (14, 20, 28)
- **color** - Different text colors
- **line_height** - Line spacing variations
- **halign** - Text alignment (left, center, right, justify)
- **padding** - Content padding
- **disabled** - Disabled state with custom colors
- **image rendering** - Local image, remote URL image, broken URL handling, texture-mode fallback behavior
- Full sample_markdown.md rendering

The full-featured demo opens a scrollable window (1400x900) with multiple sections, each demonstrating a specific property with side-by-side comparisons.

## Sample Markdown Content

The `sample_markdown.md` file contains comprehensive Markdown examples:

- All heading levels (H1-H6)
- Inline formatting (bold, italic, strikethrough, code)
- Lists (ordered, unordered, nested)
- Tables (with alignment)
- Code blocks
- Blockquotes
- Links

## Link Handling

Both demos print clicked URLs to the console rather than opening a browser. Check your terminal output when clicking links.

## Troubleshooting

### "ModuleNotFoundError: No module named 'kivy_garden.markdownlabel'"

Ensure the package is installed:

```bash
# From the repository root
pip install -e .
```

### SDL2 Library Errors (Linux)

Install required system libraries:

```bash
sudo apt-get install -y libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
```

### Window Size Issues

You can resize the window manually, or modify the `Config.set()` calls in `full_featured_demo.py` to adjust the default size.

## Additional Resources

- [Kivy Documentation](https://kivy.org/doc/stable/)
- [MarkdownLabel on GitHub](https://github.com/kivy-garden/markdownlabel)
- [Markdown Syntax Guide](https://www.markdownguide.org/basic-syntax/)
