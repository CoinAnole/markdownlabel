---
inclusion: always
---

# Project Structure & Architecture

## Critical Rules

- **Namespace**: Always use `kivy_garden.markdownlabel` imports, never legacy `garden.flower`
- **MarkdownLabel extends BoxLayout**, not Label (Markdown requires multiple child widgets)
- **Escape user content** in InlineRenderer to prevent markup injection
- **Test by functionality**, not by implementation file

## Package Layout

```
kivy_garden/markdownlabel/
├── __init__.py          # Main MarkdownLabel class (orchestration, events)
├── properties.py        # Property definitions, classification constants
├── rendering.py         # Widget tree building, style updates
├── kivy_renderer.py     # Block-level rendering (headings, lists, tables)
├── kivy_renderer_tables.py  # Table rendering mixin
├── inline_renderer.py   # Inline markup (bold, italic, links → BBCode strings)
├── markdown_serializer.py   # AST → Markdown serialization
└── tests/               # Organized by functionality
    ├── TESTING.md       # Testing guidelines, Hypothesis optimization rules
    ├── TEST_MAP.md      # Complete test suite catalog and navigation guide
    ├── modules/         # Test analysis infrastructure
    └── meta_tests/      # Test validation tests
```

## Three-Layer Rendering Pipeline

1. **Parsing**: mistune parses Markdown → AST tokens
2. **Block Rendering**: `KivyRenderer` converts blocks → Kivy widgets
3. **Inline Rendering**: `InlineRenderer` converts inline → markup strings

## Core Components

| Component | File | Role |
|-----------|------|------|
| MarkdownLabel | `__init__.py` | Main widget, Label API compatibility, event dispatch |
| MarkdownLabelProperties | `properties.py` | Property definitions, STYLE_ONLY/STRUCTURE classification |
| MarkdownLabelRendering | `rendering.py` | Widget tree building, `_update_*_in_place` methods |
| KivyRenderer | `kivy_renderer.py` | Block rendering, nesting depth protection |
| InlineRenderer | `inline_renderer.py` | Inline → BBCode (`[b]`, `[i]`, `[ref=url]`) |

## Architecture Pattern

```python
class MarkdownLabel(MarkdownLabelProperties, MarkdownLabelRendering, BoxLayout):
    # Multiple inheritance with mixins for separation of concerns
```

## Key Constraints

1. **Nesting depth protection**: KivyRenderer limits recursion depth
2. **Property forwarding**: Properties must propagate to child Label widgets
3. **Rebuild contract**: STYLE_ONLY_PROPERTIES update in-place; STRUCTURE_PROPERTIES trigger rebuild
4. **Backward compatibility**: Split modules re-export for existing imports

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

## External Dependencies

- `external/kivy/`, `external/mistune/`: Reference submodules only (use pip-installed versions)

## Configuration

- `setup.cfg`: Flake8 (110 char lines, PEP8)
- `pytest.ini`: Test configuration
- `.coveragerc`: Coverage settings
- `kivy_garden/markdownlabel/REBUILD_CONTRACT.md`: Property rebuild semantics documentation
