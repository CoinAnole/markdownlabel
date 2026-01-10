# Testing Guidelines for MarkdownLabel

Guidelines for writing and maintaining tests, including property-based testing with Hypothesis.

## Table of Contents

- [Test Organization](#test-organization)
- [Test Naming Conventions](#test-naming-conventions)
- [Test Types and Markers](#test-types-and-markers)
- [Rebuild Contract Testing](#rebuild-contract-testing)
- [Property-Based Testing](#property-based-testing)
- [Hypothesis vs. @pytest.mark.parametrize](#hypothesis-vs-pytestmarkparametrize)
- [Helper Functions](#helper-functions)
- [Best Practices](#best-practices)

## Test Organization

Tests are organized by **functionality**, not by implementation file. See `.kiro/steering/structure.md` for the test file layout.

### Class Organization

- **One class per property or behavior** (recommendation, not strict rule)
- **Descriptive class names** that indicate what's being tested
- **Related test methods** grouped within the same class

**Acceptable variations:**
- Edge case classes grouping miscellaneous tests for a component
- Comprehensive test classes testing many aspects of a single method
- Small test files without elaborate class hierarchies
- Testing multiple closely-related properties in one class

The goal is navigability and maintainability, not rigid adherence to structure.

## Test Naming Conventions

Test method names should **accurately reflect what they assert**:

| Pattern | Use When |
|---------|----------|
| `test_*_triggers_rebuild_*` | Verifying a rebuild occurred |
| `test_*_preserves_widget_tree_*` | Verifying NO rebuild occurred |
| `test_*_updates_value_*` | Verifying value changes (no rebuild check) |
| `test_*_forwards_to_*` | Verifying property forwarding |
| `test_*_updates_value_without_rebuild` | Hybrid: both value update AND no rebuild |

```python
# GOOD: Name matches assertion
def test_font_size_change_triggers_rebuild(self):
    ids_before = collect_widget_ids(label)
    label.font_size = 20
    ids_after = collect_widget_ids(label)
    assert ids_before != ids_after  # Verifies rebuild occurred

# BAD: Name doesn't match assertion
def test_font_size_triggers_rebuild(self):
    label.font_size = 20
    assert labels[0].font_size == 20  # Only tests value, not rebuild!
```

## Test Types and Markers

```python
@pytest.mark.property        # Property-based tests using Hypothesis
@pytest.mark.parametrize     # Parameterized tests with concrete examples
@pytest.mark.unit            # Unit tests
@pytest.mark.slow            # Performance-intensive tests
@pytest.mark.needs_window    # Tests requiring Kivy window
@pytest.mark.test_tests      # Meta-tests (tests about test suite structure)
```

## Rebuild Contract Testing

MarkdownLabel distinguishes between:
1. **Style-only changes** — Update existing widgets in place (no rebuild)
2. **Structure changes** — Rebuild the entire widget tree

See `REBUILD_CONTRACT.md` in the project root for detailed property classifications, implementation details, and performance implications.

### Property Classifications

**Style-Only Properties** (update in place):
- Basic: `color`, `font_size`/`base_font_size`, `line_height`, `halign`, `valign`, `disabled`
- Font: `font_name`, `code_font_name`, `font_family`, `font_context`, `font_features`, `font_hinting`, `font_kerning`, `font_blended`
- Text: `base_direction`, `text_language`, `unicode_errors`, `strip`
- Padding: `text_padding`, `padding`
- Outline: `outline_width`, `outline_color`, `disabled_outline_color`
- Truncation: `shorten`, `max_lines`, `shorten_from`, `split_str`, `ellipsis_options`
- Layout: `text_size`, `mipmap`, `limit_render_to_text_bbox`

**Structure Properties** (trigger rebuild):
- `text`, `render_mode`, `link_style`, `strict_label_mode`

### Testing Patterns

> **⚠️ Helper functions require manual ID collection first!**

```python
# Style-only property (no rebuild)
def test_color_preserves_widget_tree(self):
    label = MarkdownLabel(text="Hello")
    ids_before = collect_widget_ids(label)
    label.color = [1, 0, 0, 1]
    assert_no_rebuild(label, ids_before)  # Or: assert ids_before == collect_widget_ids(label)

# Structure property (rebuild expected)
def test_text_triggers_rebuild(self):
    label = MarkdownLabel(text="Original")
    ids_before = collect_widget_ids(label)
    label.text = "New"
    label.force_rebuild()  # Required for deferred rebuilds
    assert_rebuild_occurred(label, ids_before)
```

### Using `force_rebuild()`

MarkdownLabel uses deferred rebuilds via `Clock.create_trigger`. Use `force_rebuild()` for deterministic testing of structure property changes. Don't use it for style-only properties (they update immediately).

## Property-Based Testing

Use property-based tests for universal properties, invariants, round-trips, and metamorphic properties.

### Comment Format

All property tests with custom `max_examples` MUST include:

```python
# [Strategy Type] strategy: [N] examples ([Rationale])
@settings(max_examples=N, deadline=None)
```

### Strategy Classifications

| Strategy Type | Pattern | max_examples | Comment Format |
|--------------|---------|--------------|----------------|
| Boolean | `st.booleans()` | 2 | `Boolean strategy: 2 examples (True/False coverage)` |
| Small finite | ≤10 values | Input space size | `Small finite strategy: N examples (input space size: N)` |
| Medium finite | 11-50 values | Size, capped at 50 | `Medium finite strategy: N examples (adequate finite coverage)` |
| Combination (all finite) | Multiple finite combined | Product, capped at 50 | `Combination strategy: N examples (combination coverage)` |
| Complex/Infinite | `st.text()`, `st.floats()`, large ranges | 10-50 | `Complex strategy: N examples (adequate coverage)` |
| Mixed finite/complex | Finite + infinite combined | finite × samples | `Mixed finite/complex strategy: N examples (X finite × Y complex samples)` |

**Examples:**

```python
@given(st.booleans())
# Boolean strategy: 2 examples (True/False coverage)
@settings(max_examples=2, deadline=None)
def test_boolean_property(value): ...

@given(st.integers(min_value=1, max_value=6))
# Small finite strategy: 6 examples (input space size: 6)
@settings(max_examples=6, deadline=None)
def test_heading_level(level): ...

@given(st.booleans(), st.text(min_size=1, max_size=50))
# Mixed finite/complex strategy: 20 examples (2 finite × 10 complex samples)
@settings(max_examples=20, deadline=None)
def test_boolean_with_text(flag, text): ...
```

## Hypothesis vs. @pytest.mark.parametrize

| Scenario | Recommendation |
|----------|---------------|
| Single enum, ≤10 values | Either (parametrize preferred) |
| Single enum, >10 values | Hypothesis `sampled_from` |
| 2 enums, product ≤20 | Either approach works |
| 2+ enums, product >20 | Hypothesis (sampling avoids explosion) |
| Infinite/broad space | Hypothesis |
| Mixed finite + infinite | Hypothesis with mixed strategy |

**Warning:** Multiple `@pytest.mark.parametrize` decorators create cartesian products:

```python
# ⚠️ Creates 4 × 5 × 6 = 120 test cases!
@pytest.mark.parametrize('halign', ['left', 'center', 'right', 'justify'])
@pytest.mark.parametrize('direction', ['ltr', 'rtl', 'weak_ltr', 'weak_rtl', None])
@pytest.mark.parametrize('heading_level', [1, 2, 3, 4, 5, 6])
def test_combination(halign, direction, heading_level): ...

# ✅ Better: Hypothesis samples ~20 combinations
@given(
    halign=st.sampled_from(['left', 'center', 'right', 'justify']),
    direction=st.sampled_from(['ltr', 'rtl', 'weak_ltr', 'weak_rtl', None]),
    heading_level=st.integers(min_value=1, max_value=6)
)
# Combination strategy: 20 examples (sampling from 120 combinations)
@settings(max_examples=20, deadline=None)
def test_combination(halign, direction, heading_level): ...
```

## Helper Functions

Use helpers from `test_utils.py`:

| Function | Purpose |
|----------|---------|
| `find_labels_recursive(widget)` | Find all Label widgets in tree |
| `collect_widget_ids(widget)` | Collect widget IDs for rebuild testing |
| `assert_rebuild_occurred(widget, ids_before)` | Assert rebuild happened |
| `assert_no_rebuild(widget, ids_before)` | Assert no rebuild |
| `colors_equal(c1, c2)` | Compare colors with tolerance |
| `padding_equal(p1, p2)` | Compare padding with tolerance |
| `floats_equal(f1, f2)` | Compare floats with tolerance |

**When local helpers are acceptable:**
- Test-file-specific helpers only meaningful in one context
- Custom Hypothesis strategies for specific token structures
- Custom widget traversal when shared helpers don't fit

**Rule of thumb:** If used in 2+ files, move to `test_utils.py`.

## Best Practices

### Do's

✅ Use descriptive test and class names
✅ Group related tests in the same class
✅ Use shared helpers from test_utils.py when reusable
✅ Test both positive and negative cases
✅ Use appropriate pytest markers
✅ Test rebuild contracts explicitly
✅ Right-size max_examples based on strategy type
✅ Follow standardized comment format for property tests

### Don'ts

❌ Duplicate helper functions across multiple test files
❌ Mix completely unrelated functionality in the same class
❌ Use vague names like `test_basic` or `test_misc`
❌ Claim to test rebuilds without verifying them
❌ Use default max_examples=100 for all property tests
❌ Ignore finite input space sizes

### Guidelines vs. Rules

Use judgment — these are guidelines, not rigid rules:

- Import tests don't need elaborate class hierarchies
- Edge case classes grouping miscellaneous tests are acceptable
- Local helpers specific to one file don't need to be in test_utils.py
- Both Hypothesis and parametrize are valid for small finite cases
- Public constants like `KivyRenderer.HEADING_SIZES` are not "implementation details"
- Documented widget attributes like `language_info` are public API

### Testing Exceptions

Certain private methods are **acceptable exceptions** for testing when no public API equivalent exists:

**Documented exceptions:**
- `_get_effective_render_mode()` — verifying auto-selection logic
- `_aggregated_refs` — verifying internal link coordinate maps
- `_get_effective_halign()` — (prefer child `Label.halign` when possible)
- `_is_code` — identifying code block labels for style exclusion logic

**Edge case classes** (e.g., `TestKivyRendererEdgeCases`) may access private methods when:
1. Class name/docstring indicates it's for coverage or edge cases
2. Behavior cannot be easily triggered through public API
3. Test documents why direct access is necessary

### Validation Tools

```bash
# Validate comment format
python tools/validate_comments.py validate kivy_garden/markdownlabel/tests/

# Standardize comments (dry run first)
python tools/validate_comments.py standardize kivy_garden/markdownlabel/tests/ --dry-run

# Analyze test performance
python tools/analyze_tests.py --include-comments
```

### Debugging Tests

- Use `pytest -v` for verbose output
- Use `pytest -x` to stop on first failure
- Use `pytest --tb=short` for concise tracebacks
- Use descriptive assertion messages with context
