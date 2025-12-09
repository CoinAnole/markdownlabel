# Project Structure

## Package Layout

This is a **Kivy Garden flower** using the modern namespace package structure (`kivy_garden.markdownlabel`), not the legacy `garden.flower` format.

```
kivy_garden/
└── markdownlabel/           # Main package (namespace: kivy_garden.markdownlabel)
    ├── __init__.py          # MarkdownLabel widget class (main entry point)
    ├── _version.py          # Version string (__version__)
    ├── kivy_renderer.py     # Block-level Markdown → Kivy widgets
    ├── inline_renderer.py   # Inline Markdown → Kivy markup strings
    ├── markdown_serializer.py  # AST → Markdown serialization
    └── tests/               # Test suite
        ├── __init__.py
        ├── test_import.py
        ├── test_inline_renderer.py
        ├── test_kivy_renderer.py
        └── test_markdown_label.py
```

## Architecture

### Three-Layer Rendering Pipeline

1. **Parsing**: mistune parses Markdown text → AST tokens
2. **Block Rendering**: `KivyRenderer` converts block tokens → Kivy widgets (BoxLayout, Label, GridLayout, etc.)
3. **Inline Rendering**: `InlineRenderer` converts inline tokens → Kivy markup strings (BBCode-like)

### Key Components

- **MarkdownLabel** (`__init__.py`): Main widget class, extends BoxLayout
  - Manages parsing and rendering lifecycle
  - Exposes Kivy Label-compatible properties
  - Dispatches `on_ref_press` events for link clicks

- **KivyRenderer** (`kivy_renderer.py`): Block-level renderer
  - Handles paragraphs, headings, lists, tables, code blocks, quotes
  - Creates widget hierarchies (BoxLayout, GridLayout, Label, AsyncImage)
  - Manages nesting depth protection and list indentation

- **InlineRenderer** (`inline_renderer.py`): Inline markup converter
  - Converts bold, italic, code, links, strikethrough to Kivy markup
  - Escapes special characters for markup safety
  - Generates `[b]`, `[i]`, `[ref=url]`, etc. tags

- **MarkdownSerializer** (`markdown_serializer.py`): AST serialization
  - Converts parsed AST back to Markdown text
  - Used for round-trip conversion

## External Dependencies

### Submodules (external/)

- **kivy**: Full Kivy framework source (git submodule)
- **mistune**: Markdown parser source (git submodule)

These are included for development/reference but not used directly in the package (dependencies are installed via pip).

## Documentation

```
doc/
├── source/
│   ├── conf.py          # Sphinx configuration
│   ├── index.rst        # Documentation entry point
│   ├── api.rst          # API reference
│   ├── examples.rst     # Usage examples
│   └── ...
└── Makefile             # Build documentation
```

## Configuration Files

- **setup.py**: Package metadata, dependencies, entry points
- **setup.cfg**: Flake8 configuration, code style rules
- **README.md**: User-facing documentation
- **CHANGELOG.md**: Version history
- **CONTRIBUTING.md**: Contribution guidelines
- **LICENSE.txt**: MIT license

## Namespace Package Convention

This package uses Python namespace packages to integrate with the Kivy Garden ecosystem:

- Import as: `from kivy_garden.markdownlabel import MarkdownLabel`
- Package name: `kivy_garden.markdownlabel`
- PyPI name: `kivy_garden.markdownlabel`

All Kivy Garden flowers share the `kivy_garden` namespace, allowing multiple flowers to coexist without conflicts.
