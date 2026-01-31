# Agent Guidelines for Kivy Garden MarkdownLabel

This document provides comprehensive guidance for AI agents working on the MarkdownLabel project. It consolidates information from project structure, architecture, development practices, and testing guidelines.

---

## Product Overview

**MarkdownLabel** is a Kivy Garden flower (widget package) that renders Markdown documents as interactive Kivy UI elements.

### Purpose

Provides a Label-compatible API for common styling properties while supporting full Markdown syntax, allowing developers to display rich formatted text in Kivy applications. Note: MarkdownLabel extends BoxLayout (not Label) because Markdown rendering requires multiple widgets.

### Key Features

- Full Markdown syntax support (headings, lists, tables, code blocks, block quotes, images)
- Inline formatting (bold, italic, strikethrough, inline code, links)
- Interactive links with `on_ref_press` event handling
- Customizable styling (fonts, colors, sizes)
- Built on mistune parser (v3.0+) with plugin support
- Label API compatibility for easy migration from standard Kivy Labels

### Target Users

Kivy application developers who need to display formatted text content without manually constructing complex widget hierarchies.

---

## Project Structure & Architecture

### Critical Rules

- **Namespace**: Always use `kivy_garden.markdownlabel` imports, never legacy `garden.flower`
- **MarkdownLabel extends BoxLayout**, not Label (Markdown requires multiple child widgets)
- **Escape user content** in InlineRenderer to prevent markup injection
- **Test by functionality**, not by implementation file

### Package Layout

```
kivy_garden/markdownlabel/
├── __init__.py          # Main MarkdownLabel class (orchestration, events)
├── properties.py        # Property definitions, classification constants
├── rendering.py         # Widget tree building, style updates
├── kivy_renderer.py     # Block-level rendering (headings, lists, tables)
├── kivy_renderer_tables.py  # Table rendering mixin
├── inline_renderer.py   # Inline markup (bold, italic, links → BBCode strings)
├── markdown_serializer.py   # AST → Markdown serialization
├── utils.py             # Internal helper utilities (widget traversal, testing support)
└── tests/               # Organized by functionality
    ├── TESTING.md       # Testing guidelines, Hypothesis optimization rules
    ├── TEST_MAP.md      # Complete test suite catalog and navigation guide
    ├── modules/         # Test analysis infrastructure
    └── meta_tests/      # Test validation tests
```

### Three-Layer Rendering Pipeline

1. **Parsing**: mistune parses Markdown → AST tokens
2. **Block Rendering**: `KivyRenderer` converts blocks → Kivy widgets
3. **Inline Rendering**: `InlineRenderer` converts inline → markup strings

### Core Components

| Component | File | Role |
|-----------|------|------|
| MarkdownLabel | `__init__.py` | Main widget, Label API compatibility, event dispatch |
| MarkdownLabelProperties | `properties.py` | Property definitions, STYLE_ONLY/STRUCTURE classification |
| MarkdownLabelRendering | `rendering.py` | Widget tree building, `_update_*_in_place` methods |
| KivyRenderer | `kivy_renderer.py` | Block rendering, nesting depth protection |
| KivyRendererTables | `kivy_renderer_tables.py` | Table rendering mixin |
| InlineRenderer | `inline_renderer.py` | Inline → BBCode (`[b]`, `[i]`, `[ref=url]`) |
| MarkdownSerializer | `markdown_serializer.py` | AST→Markdown serialization for tests |
| Utils | `utils.py` | Internal helpers (widget traversal, testing support) |

### Architecture Pattern

```python
class MarkdownLabel(MarkdownLabelProperties, MarkdownLabelRendering, BoxLayout):
    # Multiple inheritance with mixins for separation of concerns
```

### Key Architectural Constraints

1. **Nesting depth protection**: KivyRenderer limits recursion depth to prevent stack overflow
2. **Property forwarding**: Properties must propagate to child Label widgets for Label API compatibility
3. **Rebuild contract**: STYLE_ONLY_PROPERTIES update in-place; STRUCTURE_PROPERTIES trigger full rebuild
4. **Backward compatibility**: Split modules re-export for existing imports
5. **Markup escaping**: InlineRenderer must escape user content to prevent markup injection

### Property System

Properties are classified as:
- **STYLE_ONLY_PROPERTIES**: Update in-place without rebuilding widget tree
- **STRUCTURE_PROPERTIES**: Trigger full rebuild of widget tree

See `kivy_garden/markdownlabel/REBUILD_CONTRACT.md` for detailed semantics.

---

## Modification Patterns

### Adding Markdown Feature
1. Check mistune support (may need plugin)
2. Add to `KivyRenderer` (blocks) or `InlineRenderer` (inline)
3. Add serialization in `MarkdownSerializer`
4. Add tests in appropriate functional test file

### Adding Label-Compatible Property
1. Define in `properties.py`
2. Forward in `rendering.py`
3. Test in `test_*_properties.py`

### Test Organization
- Tests grouped by **functionality**: `test_font_properties.py`, `test_rebuild_*`, etc.
- Property-based tests use Hypothesis with documented `max_examples`
- **Read `tests/TESTING.md`** for comprehensive testing guidelines and optimization rules
- **Read `tests/TEST_MAP.md`** for complete test suite catalog and navigation guide
- Documented exceptions for private method testing (e.g., `_get_effective_render_mode()`) are allowed when no public API equivalent exists
- Meta-tests in `tests/meta_tests/` validate test infrastructure

---

## Technology Stack

### Core Technologies

- **Kivy**: 2.0.0+ (UI framework)
- **mistune**: 3.0.0+ (Markdown parser)
- **Python**: 3.8+ (supports 3.8, 3.9, 3.10, 3.11, 3.12)

### Build System

- **setuptools**: Standard Python packaging
- **namespace packages**: Uses `find_namespace_packages` for `kivy_garden.*` structure
- **Virtual environment**: `.venv/` directory

### Development Dependencies

```
pytest>=3.6          # Testing framework
pytest-cov           # Coverage reporting
pytest-asyncio       # Async test support
hypothesis>=6.0.0    # Property-based testing
sphinx_rtd_theme     # Documentation theme
pycodestyle          # Code style checking
coveralls            # CI coverage integration
```

### External Dependencies

- `external/kivy/`, `external/mistune/`: Reference submodules only (use pip-installed versions)

---

## Python Development Setup

**CRITICAL**: This project uses Python 3 with a virtual environment.

### Commands

Commands should already be placed in PATH from `.venv/bin` automatically when terminal opens:

- **Run Python**: `python3 script.py`
- **Run pip**: `pip install package`
- **Run pytest**: `pytest tests/`
- **Run any Python tool**: `tool_name`

### Common Commands

#### Setup
```bash
# Install package in development mode
pip install -e .

# Install with dev dependencies
pip install -e ".[dev]"
```

#### Testing
```bash
# Run all tests
pytest kivy_garden/markdownlabel/tests/

# Run with coverage
pytest --cov=kivy_garden.markdownlabel kivy_garden/markdownlabel/tests/

# Run specific test file
pytest kivy_garden/markdownlabel/tests/test_core_functionality.py
```

**CRITICAL TESTING RULES:**
- **NEVER use `| head` with pytest commands** - this truncates test output and prevents tests from completing
- **NEVER use `2>&1 | head -100`** or similar output truncation with pytest
- Always let pytest run to completion to see full test results
- Use pytest's built-in options like `-v`, `--tb=short`, `-x` for controlling output instead of shell pipes

#### Code Quality
```bash
# Check code style (flake8)
python3 -m flake8 kivy_garden/

# Run pre-commit hook manually
./tools/hooks/pre-commit
```

#### Building Distribution
```bash
# Build wheel and source distribution
python3 setup.py bdist_wheel --universal
python3 setup.py sdist

# Check distribution
twine check dist/*

# Upload to PyPI (maintainers only)
twine upload dist/*
```

### Code Style

- **PEP8 compliance** with exceptions defined in `setup.cfg`
- **Max line length**: 110 characters
- **Flake8 configuration**: See `setup.cfg` for ignored rules
- Pre-commit hook available in `tools/hooks/pre-commit`

---

## Documentation

### Building Documentation
```bash
# Build documentation
cd doc
make html

# View docs
# Open doc/build/html/index.html in browser
```

Published at: https://kivy-garden.github.io/markdownlabel/

---

## CI/CD

- **GitHub Actions**: Automated testing on push/PR
- **Platforms tested**: Multiple OS environments
- **Coverage**: Tracked via coveralls
- **Artifacts**: Wheels generated for releases

---

## Configuration Files

- `setup.cfg`: Flake8 (110 char lines, PEP8)
- `pytest.ini`: Test configuration
- `.coveragerc`: Coverage settings
- `kivy_garden/markdownlabel/REBUILD_CONTRACT.md`: Property rebuild semantics documentation

---

## Testing Environment

Tests set `KIVY_NO_ARGS=1` and `KIVY_NO_CONSOLELOG=1` for headless runs. Keep these when running CI locally (e.g., `pytest` from repo root).

---

## Repository Structure Notes

- `external/`: Contains vendored upstream Kivy and Mistune sources/docs/examples; usually leave untouched unless updating vendored copies
- Modern Kivy Garden flower using namespace package `kivy_garden.markdownlabel` (not legacy `garden.*`)
- Import via: `from kivy_garden.markdownlabel import MarkdownLabel`
