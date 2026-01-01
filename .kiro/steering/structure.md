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
        ├── conftest.py                   # Pytest configuration and fixtures
        ├── TESTING.md                    # Comprehensive testing guidelines
        ├── test_import.py                # Import and basic functionality tests
        ├── test_inline_renderer.py       # Inline markdown rendering tests
        ├── test_kivy_renderer.py         # Block-level rendering tests
        ├── test_core_functionality.py    # Core markdown parsing and rendering
        ├── test_core_functionality_properties.py # Core functionality property tests
        ├── test_label_compatibility.py   # Basic label property forwarding
        ├── test_font_properties.py       # Font-related property forwarding
        ├── test_color_properties.py      # Color and styling properties
        ├── test_text_properties.py       # Text-related property forwarding
        ├── test_padding_properties.py    # Padding and spacing properties
        ├── test_sizing_behavior.py       # Auto-sizing and layout behavior
        ├── test_advanced_compatibility.py # Advanced label features
        ├── test_serialization.py         # Round-trip serialization
        ├── test_performance.py           # Performance and stability tests
        ├── test_rebuild_scheduling.py    # Rebuild scheduling and timing tests
        ├── test_rebuild_semantics.py     # Rebuild contract semantics tests
        ├── test_clipping_behavior.py     # Text clipping and overflow behavior
        ├── test_texture_render_mode.py   # Texture rendering mode tests
        ├── test_texture_sizing.py        # Texture sizing behavior tests
        ├── test_rtl_alignment.py         # Right-to-left text alignment tests
        ├── test_shortening_and_coordinate.py # Text shortening and coordinate tests
        ├── test_refactoring_properties.py # Property refactoring validation tests
        ├── test_shared_infrastructure.py # Shared testing infrastructure tests
        ├── test_refactoring_properties.py # Property refactoring validation tests
        ├── test_utils.py                 # Shared test utilities and strategies
        ├── TESTING.md                    # Comprehensive testing guidelines
        ├── meta_tests/                   # Meta-testing infrastructure
        │   ├── test_assertion_analyzer.py
        │   ├── test_code_duplication_minimization.py
        │   ├── test_comment_format.py
        │   ├── test_comment_standardizer.py
        │   ├── test_coverage_preservation.py
        │   ├── test_documentation_compliance.py
        │   ├── test_duplicate_detector.py
        │   ├── test_file_analyzer.py
        │   ├── test_helper_availability.py
        │   ├── test_naming_convention_validator.py
        │   ├── test_strategy_classification.py
        │   └── test_test_file_parser.py
        └── modules/                      # Test analysis and utility modules
            ├── __init__.py
            ├── assertion_analyzer.py
            ├── comment_manager.py
            ├── duplicate_detector.py
            ├── file_analyzer.py
            ├── file_parser.py
            ├── max_examples_calculator.py
            ├── naming_convention_validator.py
            ├── optimization_detector.py
            ├── over_testing_validator.py
            ├── strategy_analyzer.py
            └── test_discovery.py
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
- `test_core_functionality_properties.py`: Core functionality property tests
- `test_*_properties.py`: Property forwarding tests (font, color, text, padding)
- `test_*_compatibility.py`: Label API compatibility
- `test_performance.py`: Performance and stability (uses Hypothesis property-based testing)
- `test_serialization.py`: Round-trip serialization tests
- `test_*_behavior.py`: Behavioral tests (sizing, clipping, etc.)
- `test_rebuild_*.py`: Rebuild contract and semantics testing
- `test_*_alignment.py`: Text alignment and RTL support tests
- `test_texture_*.py`: Texture rendering and sizing tests
- `test_strategy_classification.py`: Tests for optimization infrastructure (in meta_tests/)
- `test_file_analyzer.py`: Tests for test file analysis tools (in meta_tests/)
- `test_documentation_compliance.py`: Tests for max_examples documentation (in meta_tests/)
- `test_utils.py`: Shared test utilities and Hypothesis strategies
- `test_comment_*.py`: Comment format validation and standardization tests (in meta_tests/)
- `test_*_infrastructure.py`: Shared testing infrastructure tests
- `test_helper_availability.py`: Helper function availability tests (in meta_tests/)
- `test_refactoring_properties.py`: Property refactoring validation tests
- `TESTING.md`: Comprehensive testing guidelines and property-based testing optimization
- `meta_tests/`: Meta-testing infrastructure for test analysis and validation
- `modules/`: Test analysis and utility modules for code quality and duplication detection

**When adding tests**: Place in the appropriate functional test file, not necessarily matching the implementation file.

### Tools Directory (`tools/`)
Contains development and analysis tools:
- `README.md`: Documentation for available tools
- `measure_baseline_performance.py`: Performance measurement and baseline tracking
- `validate_comments.py`: Tool for validating and standardizing property-based test comments
- `validate_refactoring.py`: Tool for validating refactoring changes
- `hooks/`: Git hooks for development workflow
  - `pre-commit`: Pre-commit validation hook
**When modifying tests**: Use tools for validation and performance analysis

## External Dependencies (Submodules)

Located in `external/`:
- `kivy/`: Full Kivy framework source (git submodule)
- `mistune/`: Markdown parser source (git submodule)

**IMPORTANT**: These are for development/reference only. The package uses pip-installed versions, not these submodules directly.

## Configuration Files

- `setup.py`: Package metadata, dependencies, entry points
- `setup.cfg`: Flake8 configuration, code style rules (110 char line limit, PEP8 compliance)
- `pytest.ini`: Pytest configuration
- `kivy_garden/markdownlabel/tests/TESTING.md`: Comprehensive testing guidelines including property-based testing optimization

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
1. Review `kivy_garden/markdownlabel/tests/TESTING.md`
2. Use tools in `tools/` directory for validation and performance analysis
3. Adjust `max_examples` based on strategy complexity using standardized comment format
4. Add performance rationale comments to tests
5. Utilize test optimization infrastructure in `tests/modules/` and `tests/meta_tests/`
