---
inclusion: always
---

# Project Structure & Architecture Guide

## Package Layout Rules

**CRITICAL**: This is a **Kivy Garden flower** using modern namespace package structure (`kivy_garden.markdownlabel`). Always use this import pattern, never legacy `garden.flower` format.

```
kivy_garden/
└── markdownlabel/           # Main package (namespace: kivy_garden.markdownlabel)
    ├── __init__.py          # MarkdownLabel widget class (main entry point)
    ├── _version.py          # Version string (__version__)
    ├── kivy_renderer.py     # Block-level Markdown → Kivy widgets
    ├── inline_renderer.py   # Inline Markdown → Kivy markup strings
    ├── markdown_serializer.py  # AST → Markdown serialization
    └── tests/               # Test suite (organized by functionality)
        ├── __init__.py
        ├── test_import.py
        ├── test_inline_renderer.py
        ├── test_kivy_renderer.py
        ├── test_core_functionality.py    # Core markdown parsing and rendering
        ├── test_label_compatibility.py   # Basic label property forwarding
        ├── test_font_properties.py       # Font-related property forwarding
        ├── test_color_properties.py      # Color and styling properties
        ├── test_text_properties.py       # Text-related property forwarding
        ├── test_padding_properties.py    # Padding and spacing properties
        ├── test_sizing_behavior.py       # Auto-sizing and layout behavior
        ├── test_advanced_compatibility.py # Advanced label features
        ├── test_serialization.py         # Round-trip serialization
        ├── test_performance.py           # Performance and stability tests
        ├── test_strategy_classification.py # Tests for optimization infrastructure
        ├── test_file_analyzer.py         # Tests for test file analysis tools
        ├── test_documentation_compliance.py # Tests for max_examples documentation
        └── test_utils.py                 # Shared test utilities and strategies
```

### Import Conventions
- **Always use**: `from kivy_garden.markdownlabel import MarkdownLabel`
- **Package namespace**: `kivy_garden.markdownlabel`
- **Never use**: Legacy `garden.flower` imports

## Architecture: Three-Layer Rendering Pipeline

The codebase follows a strict three-layer architecture for converting Markdown to Kivy UI:

1. **Parsing Layer**: mistune parses Markdown text → AST tokens
2. **Block Rendering Layer**: `KivyRenderer` converts block tokens → Kivy widgets
3. **Inline Rendering Layer**: `InlineRenderer` converts inline tokens → Kivy markup strings

### Core Component Responsibilities

#### MarkdownLabel (`__init__.py`)
- **Role**: Main widget class, extends `BoxLayout` (NOT Label - Markdown requires multiple widgets)
- **Responsibilities**:
  - Manages parsing and rendering lifecycle
  - Exposes Kivy Label-compatible properties for easy migration
  - Dispatches `on_ref_press` events for link clicks
- **When modifying**: Ensure Label API compatibility is maintained

#### KivyRenderer (`kivy_renderer.py`)
- **Role**: Block-level renderer (paragraphs, headings, lists, tables, code blocks, quotes)
- **Responsibilities**:
  - Creates widget hierarchies (BoxLayout, GridLayout, Label, AsyncImage)
  - Manages nesting depth protection (prevents infinite recursion)
  - Handles list indentation and numbering
- **Key pattern**: Each block type has a dedicated `render_*` method
- **When modifying**: Test nesting depth limits and complex nested structures

#### InlineRenderer (`inline_renderer.py`)
- **Role**: Inline markup converter (bold, italic, code, links, strikethrough)
- **Responsibilities**:
  - Converts inline tokens to Kivy markup strings (BBCode-like: `[b]`, `[i]`, `[ref=url]`)
  - Escapes special characters for markup safety
  - Handles nested inline formatting
- **Key pattern**: Returns strings, not widgets
- **When modifying**: Always escape user content to prevent markup injection

#### MarkdownSerializer (`markdown_serializer.py`)
- **Role**: AST → Markdown text serialization
- **Responsibilities**: Round-trip conversion (parse → serialize → parse should be idempotent)
- **When modifying**: Ensure round-trip tests pass

## File Organization Patterns

### Test Suite Organization
Tests are organized by **functionality**, not by implementation file:
- `test_core_functionality.py`: Core parsing and rendering
- `test_*_properties.py`: Property forwarding tests (font, color, text, padding)
- `test_*_compatibility.py`: Label API compatibility
- `test_performance.py`: Performance and stability (uses Hypothesis property-based testing)
- `test_utils.py`: Shared test utilities and Hypothesis strategies

**When adding tests**: Place in the appropriate functional test file, not necessarily matching the implementation file.

### Tools Directory (`tools/`)
Contains test optimization and analysis tools:
- `test_optimization/`: Hypothesis test performance optimization infrastructure
- `analyze_tests.py`: Command-line tool for analyzing test performance
- **When modifying tests**: Run `python tools/analyze_tests.py` to validate performance

## External Dependencies (Submodules)

Located in `external/`:
- `kivy/`: Full Kivy framework source (git submodule)
- `mistune/`: Markdown parser source (git submodule)

**IMPORTANT**: These are for development/reference only. The package uses pip-installed versions, not these submodules directly.

## Configuration Files

- `setup.py`: Package metadata, dependencies, entry points
- `setup.cfg`: Flake8 configuration, code style rules (80 char line limit, PEP8 compliance)
- `pytest.ini`: Pytest configuration
- `PROPERTY_BASED_TESTING_GUIDE.md`: Guidelines for optimizing property-based tests

## Documentation Structure

```
doc/
├── source/
│   ├── conf.py          # Sphinx configuration
│   ├── index.rst        # Documentation entry point
│   ├── api.rst          # API reference
│   ├── examples.rst     # Usage examples
│   └── ...
└── Makefile             # Build with: cd doc && make html
```

## Key Architectural Constraints

1. **MarkdownLabel extends BoxLayout**: Cannot extend Label directly because Markdown rendering requires multiple child widgets
2. **Nesting depth protection**: KivyRenderer limits nesting to prevent infinite recursion
3. **Markup safety**: InlineRenderer must escape all user content to prevent markup injection
4. **Label API compatibility**: MarkdownLabel exposes Label-compatible properties for easy migration from standard Kivy Labels
5. **Namespace package structure**: Uses `find_namespace_packages` in setup.py to support `kivy_garden.*` namespace

## Common Modification Patterns

### Adding a new Markdown feature
1. Check if mistune supports it (may need plugin)
2. Add block rendering in `KivyRenderer` or inline rendering in `InlineRenderer`
3. Add serialization support in `MarkdownSerializer`
4. Add tests in appropriate test file (by functionality, not by file)
5. Update documentation in `doc/source/`

### Adding a new Label-compatible property
1. Add property to `MarkdownLabel` in `__init__.py`
2. Forward to child Labels in rendering methods
3. Add tests in appropriate `test_*_properties.py` file
4. Document in API reference

### Optimizing test performance
1. Review `PROPERTY_BASED_TESTING_GUIDE.md`
2. Run `python tools/analyze_tests.py` to identify slow tests
3. Adjust `max_examples` based on strategy complexity
4. Add performance rationale comments to tests
