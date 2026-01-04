---
inclusion: always
---

# Project Structure & Architecture Guide

## Package Layout Rules

**CRITICAL**: This is a **Kivy Garden flower** using modern namespace package structure (`kivy_garden.markdownlabel`). Always use this import pattern, never legacy `garden.flower` format.

```
kivy_garden/
└── markdownlabel/
    ├── __init__.py
    ├── _version.py
    ├── kivy_renderer.py
    ├── inline_renderer.py
    ├── markdown_serializer.py
    └── tests/
        ├── __init__.py
        ├── conftest.py
        ├── TESTING.md
        ├── test_import.py
        ├── test_inline_renderer.py
        ├── test_kivy_renderer.py
        ├── test_core_functionality.py
        ├── test_label_compatibility.py
        ├── test_font_properties.py
        ├── test_color_properties.py
        ├── test_text_properties.py
        ├── test_padding_properties.py
        ├── test_sizing_behavior.py
        ├── test_advanced_compatibility.py
        ├── test_serialization.py
        ├── test_performance.py
        ├── test_rebuild_scheduling.py
        ├── test_rebuild_semantics.py
        ├── test_clipping_behavior.py
        ├── test_texture_render_mode.py
        ├── test_texture_sizing.py
        ├── test_rtl_alignment.py
        ├── test_shortening_and_coordinate.py
        ├── test_utils.py
        ├── TESTING.md
        ├── meta_tests/
        │   ├── test_assertion_analyzer.py
        │   ├── test_code_duplication_minimization.py
        │   ├── test_comment_format.py
        │   ├── test_comment_standardizer.py
        │   ├── test_core_functionality_properties.py
        │   ├── test_coverage_preservation.py
        │   ├── test_documentation_compliance.py
        │   ├── test_file_analyzer.py
        │   ├── test_helper_availability.py
        │   ├── test_naming_convention_validator.py
        │   ├── test_refactoring_properties.py
        │   ├── test_shared_infrastructure.py
        │   ├── test_sizing_behavior_grouping.py
        │   ├── test_strategy_classification.py
        │   ├── test_test_file_parser.py
        │   ├── test_texture_sizing_grouping.py
        │   └── test_duplicate_detector.py
        └── modules/
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
- `test_import.py`: Tests for MarkdownLabel import functionality - verifying that MarkdownLabel can be imported and has the expected basic properties available
- `test_inline_renderer.py`: Property-based tests for InlineRenderer - verifying inline Markdown formatting is correctly converted to Kivy markup strings
- `test_kivy_renderer.py`: Property-based tests and edge case coverage for KivyRenderer - verifying block-level Markdown elements are correctly converted to Kivy widgets, targeting implementation details for edge cases and internal methods
- `test_core_functionality.py`: Core functionality tests for MarkdownLabel widget - tests for fundamental markdown parsing, rendering, and widget tree generation functionality
- `test_label_compatibility.py`: Label compatibility tests for MarkdownLabel widget - verifying MarkdownLabel maintains compatibility with Kivy Label API for basic properties like font_size aliases and no-op property acceptance
- `test_font_properties.py`: Property-based tests for font-related properties - verifying font properties (font_name, line_height, font_size, etc.) are correctly forwarded to child Label widgets and font scaling behavior works correctly for headings
- `test_color_properties.py`: Property-based tests for color-related properties - verifying color properties (color, disabled_color) are correctly forwarded to internal Label widgets and applied appropriately based on the widget's disabled state
- `test_text_properties.py`: Property-based tests for text-related property forwarding - verifying text-related properties like text_size, unicode_errors, and strip are correctly forwarded to child Label widgets
- `test_padding_properties.py`: Property-based tests for MarkdownLabel padding properties - verifying padding-related properties (padding, text_padding, label_padding) work correctly and are properly forwarded to child widgets
- `test_sizing_behavior.py`: Property-based tests for MarkdownLabel sizing behavior - tests for auto-sizing behavior, size hint management, and strict label mode sizing
- `test_advanced_compatibility.py`: Property-based tests for advanced MarkdownLabel compatibility features - tests for advanced Label API compatibility including advanced font properties forwarding, disabled color application, and reactive rebuild on property changes
- `test_serialization.py`: Tests for round-trip serialization functionality - verifying the MarkdownLabel can correctly serialize and deserialize Markdown content, maintaining semantic equivalence through parse-serialize-parse cycles
- `test_performance.py`: Performance and efficiency tests for MarkdownLabel widget - tests verifying performance-related behaviors including efficient style updates, batched rebuilds, deferred rebuild scheduling, and content clipping behavior
- `test_rebuild_scheduling.py`: Rebuild batching and deferred scheduling tests for MarkdownLabel - tests for rebuild scheduler behavior including batching multiple structure property changes into a single rebuild and deferring rebuilds via Clock triggers
- `test_rebuild_semantics.py`: Widget identity preservation and rebuild semantics tests for MarkdownLabel - tests verifying widget identity preservation for style-only property changes and widget tree rebuilding for structure property changes, designed for headless CI environments
- `test_clipping_behavior.py`: Clipping behavior tests for MarkdownLabel - tests for content clipping behavior including verification that content is wrapped in a StencilView clipping container when height-constrained and that content expands naturally when unconstrained
- `test_texture_render_mode.py`: Property-based tests for texture render mode in MarkdownLabel - tests for texture render mode feature including Image widget creation, render_mode property behavior, link zone aggregation, on_ref_press event dispatching, deterministic texture hit-testing, texture fallback branch, and auto render mode selection
- `test_texture_sizing.py`: Property-based tests for MarkdownLabel texture size calculations - tests for texture size calculation behavior and logical test grouping validation
- `test_rtl_alignment.py`: Property-based tests for RTL-aware auto alignment in MarkdownLabel - tests for RTL alignment behavior including auto alignment respecting base_direction, direction change updates, and explicit alignment overriding auto behavior
- `test_shortening_and_coordinate.py`: Property-based tests for text shortening and coordinate translation features - tests for label compatibility features including text shortening property forwarding and coordinate translation for refs and anchors
- `test_utils.py`: Shared test utilities and Hypothesis strategies for MarkdownLabel tests - common test utilities, Hypothesis strategies, and helper functions used across multiple test modules
- `TESTING.md`: Comprehensive testing guidelines and property-based testing optimization
- `meta_tests/`: Meta-testing infrastructure for test analysis and validation
  - `test_assertion_analyzer.py`: Tests for the assertion analyzer module - both unit tests and property-based tests for validating the assertion analyzer's ability to correctly identify assertion patterns and detect naming mismatches
  - `test_code_duplication_minimization.py`: Property-based tests for code duplication minimization validation - property tests that validate the refactoring successfully minimizes code duplication in the test suite
  - `test_comment_format.py`: Property-based tests for comment format specification and validation - tests the CommentFormatValidator's ability to correctly validate and parse standardized comment formats for max_examples documentation
  - `test_comment_standardizer.py`: Property-based tests for comment standardization functionality - tests the CommentStandardizer's ability to generate and apply standardized comments for property-based tests with proper strategy documentation
  - `test_core_functionality_properties.py`: Property-based tests for core functionality module refactoring - property-based tests that validate the refactoring process for the core functionality test module
  - `test_coverage_preservation.py`: Property-based tests for test coverage preservation validation - property tests that validate the refactoring preserves or improves test coverage metrics
  - `test_documentation_compliance.py`: Tests for documentation compliance of max_examples values - tests that custom max_examples values are properly documented according to the optimization guidelines
  - `test_file_analyzer.py`: Tests for the FileAnalyzer optimization tool - tests the FileAnalyzer's ability to correctly analyze test files and generate optimization recommendations for max_examples values
  - `test_helper_availability.py`: Property tests for helper function availability in test_utils - property-based tests that verify all required helper functions are available in test_utils.py and work correctly
  - `test_naming_convention_validator.py`: Tests for the naming convention validator module - both unit tests and property-based tests for validating the naming convention validator's ability to detect violations and suggest appropriate renames
  - `test_refactoring_properties.py`: Property-based tests for test refactoring validation - tests that validate the test refactoring process itself, including module naming consistency and other refactoring properties
  - `test_shared_infrastructure.py`: Meta tests for shared test infrastructure - tests validating that the shared test utilities and strategies work correctly and are available for use across all test modules
  - `test_sizing_behavior_grouping.py`: Meta tests for sizing behavior test grouping validation - tests validating that sizing behavior tests are properly organized and grouped
  - `test_strategy_classification.py`: Property-based tests for strategy classification system - tests the StrategyClassifier's ability to correctly identify and categorize Hypothesis strategies for max_examples optimization
  - `test_test_file_parser.py`: Property-based tests for test file parser - property tests that validate the test file parser correctly extracts metadata from test files
  - `test_texture_sizing_grouping.py`: Meta tests for texture sizing test grouping validation - tests validating that texture sizing tests are properly organized and grouped
  - `test_duplicate_detector.py`: Property-based tests for duplicate helper function detector - property tests that validate the duplicate detector correctly identifies duplicate helper functions across test files
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
