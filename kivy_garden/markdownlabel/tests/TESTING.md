# Testing Guidelines for MarkdownLabel

This document provides comprehensive guidelines for writing, organizing, and maintaining tests in the MarkdownLabel project, including both general testing practices and specialized property-based testing with Hypothesis.

## Table of Contents

- [Test Organization](#test-organization)
- [Test Naming Conventions](#test-naming-conventions)
- [Test Types and Markers](#test-types-and-markers)
- [Rebuild Contract Testing](#rebuild-contract-testing)
  - [Using `force_rebuild()` in Tests](#using-force_rebuild-in-tests)
- [Property-Based Testing](#property-based-testing)
- [Property-Based Testing Optimization](#property-based-testing-optimization)
- [When to Use Hypothesis vs. @pytest.mark.parametrize](#when-to-use-hypothesis-vs-pytestmarkparametrize)
- [Helper Functions](#helper-functions)
- [Test File Structure](#test-file-structure)
- [Standardization Tools](#standardization-tools)
- [Validation and CI Integration](#validation-and-ci-integration)
- [Best Practices](#best-practices)

## Test Organization

### File Organization

Tests are organized by **functionality**, not by implementation file:

```
tests/
├── test_core_functionality.py      # Core parsing and rendering
├── test_label_compatibility.py     # Basic label property forwarding
├── test_font_properties.py         # Font-related property forwarding
├── test_color_properties.py        # Color and styling properties
├── test_text_properties.py         # Text-related property forwarding
├── test_padding_properties.py      # Padding and spacing properties
├── test_sizing_behavior.py         # Auto-sizing and layout behavior
├── test_advanced_compatibility.py  # Advanced label features
├── test_serialization.py           # Round-trip serialization
├── test_performance.py             # Performance and stability tests
├── test_strategy_classification.py # Tests for optimization infrastructure
├── test_file_analyzer.py           # Tests for test file analysis tools
├── test_documentation_compliance.py # Tests for max_examples documentation
└── test_utils.py                   # Shared test utilities and strategies
```

### Class Organization

Within each test file, organize tests into logical classes:

- **One class per property or behavior being tested**
- **Descriptive class names** that clearly indicate what is being tested
- **Related test methods** grouped within the same class

#### Good Class Organization Examples:

```python
class TestFontNamePropertyForwarding:
    """Tests for font_name property forwarding to child Labels."""
    
    def test_font_name_applied_to_paragraph(self):
        # Test font_name forwarding to paragraph labels
        
    def test_font_name_applied_to_heading(self):
        # Test font_name forwarding to heading labels
        
    def test_font_name_preserves_code_font(self):
        # Test that code blocks preserve their special font

class TestColorPropertyForwarding:
    """Tests for color property forwarding to child Labels."""
    
    def test_color_applied_to_paragraph(self):
        # Test color forwarding to paragraph labels
        
    def test_color_applied_to_heading(self):
        # Test color forwarding to heading labels
```

#### Poor Class Organization Examples:

```python
# DON'T: Mix unrelated functionality
class TestMixedFunctionality:
    def test_font_size_forwarding(self):
        pass
    def test_serialization_roundtrip(self):
        pass
    def test_performance_benchmark(self):
        pass

# DON'T: Vague class names
class TestBasicStuff:
    pass

class TestMisc:
    pass
```

#### Acceptable Variations

The "one class per property/behavior" guideline is a recommendation, not a strict rule. These patterns are acceptable:

- **Edge case classes**: A `TestKivyRendererEdgeCases` class grouping miscellaneous edge cases for a component is fine when the tests don't fit neatly into property-based categories
- **Comprehensive test classes**: A `TestComprehensiveTextureSizeCalculation` class testing many aspects of a single method is reasonable
- **Small test files**: Import tests or simple smoke tests don't need elaborate class hierarchies
- **Related behaviors**: Testing multiple closely-related properties (e.g., all color-related properties) in one class is acceptable

The goal is navigability and maintainability, not rigid adherence to structure.

## Test Naming Conventions

### Test Method Names

Test method names should **accurately reflect what they assert**:

#### Rebuild Testing Names

- `test_*_triggers_rebuild_*` - ONLY for tests that verify a rebuild occurred
- `test_*_preserves_widget_tree_*` - For tests that verify NO rebuild occurred
- `test_*_rebuilds_*` - For tests that verify rebuild behavior

#### Value/Property Testing Names

- `test_*_updates_value_*` - For tests that verify value changes without rebuild verification
- `test_*_changes_property_*` - For tests that verify property changes
- `test_*_forwards_to_*` - For tests that verify property forwarding
- `test_*_applied_to_*` - For tests that verify property application

#### Examples:

```python
# GOOD: Name matches assertion
def test_font_size_change_triggers_rebuild(self):
    """Test that changing font_size rebuilds the widget tree."""
    ids_before = collect_widget_ids(label)
    label.font_size = 20
    ids_after = collect_widget_ids(label)
    assert ids_before != ids_after  # Verifies rebuild occurred

def test_color_updates_value_immediately(self):
    """Test that color changes update Label.color immediately."""
    label.color = [1, 0, 0, 1]
    labels = find_labels_recursive(label)
    assert all(l.color == [1, 0, 0, 1] for l in labels)  # Verifies value change

# BAD: Name doesn't match assertion
def test_font_size_triggers_rebuild(self):
    """Test font size changes."""
    label.font_size = 20
    labels = find_labels_recursive(label)
    assert labels[0].font_size == 20  # Only tests value, not rebuild!
```

### Test Class Names

Use descriptive, specific class names:

- `Test[Property][Behavior]` - e.g., `TestFontSizeImmediateUpdates`
- `Test[Component][Functionality]` - e.g., `TestMarkdownLinkRendering`
- `Test[Feature][Aspect]` - e.g., `TestRebuildContractEnforcement`

## Test Types and Markers

### Pytest Markers

Use appropriate pytest markers to categorize tests:

```python
@pytest.mark.property        # Property-based tests using Hypothesis (see guidelines below)
@pytest.mark.parametrize     # Parameterized tests with concrete examples (see guidelines below)
@pytest.mark.unit            # Unit tests
@pytest.mark.slow            # Performance-intensive tests
@pytest.mark.needs_window    # Tests requiring Kivy window
@pytest.mark.test_tests      # Meta-tests (tests about test suite structure)
```

**Note:** See [When to Use Hypothesis vs. @pytest.mark.parametrize](#when-to-use-hypothesis-vs-pytestmarkparametrize) for guidance on choosing between `@pytest.mark.property` and `@pytest.mark.parametrize`.

#### Meta-Test Marking

Tests that validate the test suite itself must be marked with `@pytest.mark.test_tests`:

```python
@pytest.mark.test_tests
class TestHelperFunctionAvailability:
    """Tests that verify helper functions are available and consolidated."""
    
    def test_widget_traversal_helpers_available(self):
        # Test that helper functions exist in test_utils
```

### Test Categories

#### Unit Tests
- Test specific examples and edge cases
- Verify concrete behavior with known inputs
- Fast execution, deterministic results

#### Property-Based Tests
- Test universal properties across many inputs
- Use Hypothesis for input generation
- Verify behavior holds for all valid inputs

## Rebuild Contract Testing

> **📌 IMPORTANT NOTE ON HELPER FUNCTIONS**
>
> The rebuild testing helpers `assert_rebuild_occurred()` and `assert_no_rebuild()` require manual ID collection:
> ```python
> ids_before = collect_widget_ids(widget)  # You must do this first
> # ... make changes ...
> assert_rebuild_occurred(widget, ids_before)  # Pass ids_before, not a function
> ```
> They do NOT take a `change_func` parameter. See [Rebuild Testing Helpers](#rebuild-testing-helpers) for correct usage.

### Understanding the Rebuild Contract

MarkdownLabel distinguishes between two types of property changes:

1. **Style-only changes** - Update existing widgets in place (no rebuild)
2. **Structure changes** - Rebuild the entire widget tree

### Style-Only Properties

These properties update existing widgets without rebuilding:

- `color` - Updates Label.color on existing Labels
- `font_size` / `base_font_size` - Updates Label.font_size on existing Labels
- `font_name` - Updates Label.font_name on existing Labels (non-code Labels)
- `code_font_name` - Updates Label.font_name on code block Labels
- `line_height` - Updates Label.line_height on existing Labels
- `halign`, `valign` - Updates alignment on existing Labels
- `disabled`, `disabled_color` - Updates disabled state/color on existing Labels
- `base_direction` - Updates text direction on existing Labels
- `text_padding` - Updates Label.padding on existing Labels
- `padding` - Updates container padding (BoxLayout handles this automatically)
- `outline_width` - Updates Label.outline_width on existing Labels
- `outline_color`, `disabled_outline_color` - Updates outline colors on existing Labels
- `mipmap` - Updates Label.mipmap on existing Labels
- `text_language` - Updates Label.text_language on existing Labels
- `limit_render_to_text_bbox` - Updates Label.limit_render_to_text_bbox on existing Labels

### Structure Properties

These properties trigger a complete widget tree rebuild:

- `text` - Changes the markdown content structure
- `text_size` - Changes the text size constraints (affects wrapping and bindings)
- `render_mode` - Changes between widgets/texture rendering
- `link_style` - Changes link styling (affects markup generation)
- `strict_label_mode` - Changes label mode behavior (affects widget bindings)

### Testing Rebuild Behavior

#### Testing Style-Only Changes (No Rebuild)

```python
def test_color_change_preserves_widget_tree(self):
    """Test that color changes preserve widget identities (no rebuild)."""
    label = MarkdownLabel(text="Hello World")
    
    # Collect widget IDs before change
    ids_before = collect_widget_ids(label)
    
    # Change style-only property
    label.color = [1, 0, 0, 1]
    
    # Verify widget tree structure is preserved
    ids_after = collect_widget_ids(label)
    assert ids_before == ids_after, "Widget tree should not rebuild for style changes"
    
    # Verify the style change was applied
    labels = find_labels_recursive(label)
    assert all(l.color == [1, 0, 0, 1] for l in labels)
```

#### Testing Structure Changes (Rebuild Required)

```python
def test_text_change_triggers_rebuild(self):
    """Test that text changes rebuild the widget tree."""
    label = MarkdownLabel(text="Original text")
    
    # Collect widget IDs before change
    ids_before = collect_widget_ids(label)
    
    # Change structure property
    label.text = "New text with different structure"
    
    # Verify widget tree was rebuilt
    ids_after = collect_widget_ids(label)
    assert ids_before != ids_after, "Widget tree should rebuild for structure changes"
    
    # Verify the content change was applied
    assert label.text == "New text with different structure"
```

### Rebuild Testing Helpers

Use these helper functions from `test_utils.py`:

```python
def collect_widget_ids(widget, exclude_root=True):
    """Collect Python object IDs of all widgets in the tree.
    
    Returns a dict mapping widget IDs to widget objects for comparison.
    """
    
def assert_rebuild_occurred(widget, ids_before, exclude_root=True):
    """Assert that a widget tree rebuild occurred.
    
    Args:
        widget: Root widget to check
        ids_before: Dict from collect_widget_ids() before the change
        exclude_root: If True, exclude root widget from comparison
    """
    
def assert_no_rebuild(widget, ids_before, exclude_root=True):
    """Assert that no widget tree rebuild occurred.
    
    Args:
        widget: Root widget to check
        ids_before: Dict from collect_widget_ids() before the change
        exclude_root: If True, exclude root widget from comparison
    """
```

#### Using the Helper Functions

**IMPORTANT**: These helpers require you to collect widget IDs **before** making changes:

```python
def test_color_preserves_widget_tree_with_helper(self):
    """Test that color changes preserve widget tree using helper."""
    label = MarkdownLabel(text="Hello World")
    
    # Step 1: Collect IDs before change
    ids_before = collect_widget_ids(label)
    
    # Step 2: Make the change
    label.color = [1, 0, 0, 1]
    
    # Step 3: Use helper to verify no rebuild
    assert_no_rebuild(label, ids_before)
    
    # Step 4: Verify the change was applied
    labels = find_labels_recursive(label)
    assert all(l.color == [1, 0, 0, 1] for l in labels)
```

```python
def test_text_triggers_rebuild_with_helper(self):
    """Test that text changes trigger rebuild using helper."""
    label = MarkdownLabel(text="Original")
    
    # Step 1: Collect IDs before change
    ids_before = collect_widget_ids(label)
    
    # Step 2: Make the change (schedules deferred rebuild)
    label.text = "New text"
    
    # Step 3: Force immediate rebuild for testing
    label.force_rebuild()
    
    # Step 4: Use helper to verify rebuild occurred
    assert_rebuild_occurred(label, ids_before)
```

**Manual vs Helper Approach**: Both approaches are valid:

```python
# Manual approach (explicit, clear)
ids_before = collect_widget_ids(label)
label.color = [1, 0, 0, 1]
ids_after = collect_widget_ids(label)
assert ids_before == ids_after  # No rebuild

# Helper approach (more concise)
ids_before = collect_widget_ids(label)
label.color = [1, 0, 0, 1]
assert_no_rebuild(label, ids_before)
```

Both patterns are acceptable. Use helpers for consistency or manual comparison when you need custom error messages.

### Using `force_rebuild()` in Tests

MarkdownLabel uses **deferred rebuilds** via `Clock.create_trigger` for performance optimization. This means property changes don't rebuild the widget tree synchronously — they schedule a rebuild for the next frame.

For testing, this creates a challenge: tests need deterministic, synchronous behavior to verify rebuild outcomes immediately.

#### The `force_rebuild()` Method

`force_rebuild()` is a **public API method** specifically designed for scenarios requiring immediate synchronous updates, including testing:

```python
def force_rebuild(self):
    """Force an immediate synchronous rebuild.
    
    This is useful in scenarios where:
    - You need to query widget properties immediately after changes
    - You're performing measurements that depend on the rebuilt tree
    - You need deterministic timing for testing
    """
```

#### When to Use `force_rebuild()` in Tests

Use `force_rebuild()` when testing structure property changes that trigger deferred rebuilds:

```python
def test_font_name_change_triggers_rebuild(self):
    """Test that changing font_name triggers widget rebuild."""
    label = MarkdownLabel(text='Hello World', font_name='Roboto')
    
    # Collect widget IDs before change
    ids_before = collect_widget_ids(label)
    
    # Change structure property (schedules deferred rebuild)
    label.font_name = 'Roboto-Bold'
    
    # Force immediate rebuild for deterministic testing
    label.force_rebuild()
    
    # Now we can verify the rebuild occurred
    ids_after = collect_widget_ids(label)
    assert ids_before != ids_after, "Widget tree should rebuild"
    
    # Verify the new value is applied
    labels = find_labels_recursive(label)
    assert all(l.font_name == 'Roboto-Bold' for l in labels)
```

#### When NOT to Use `force_rebuild()`

Don't use `force_rebuild()` when:

1. **Testing style-only properties** — These update widgets in place without rebuilding, so no `force_rebuild()` is needed:
   ```python
   def test_color_updates_immediately(self):
       label = MarkdownLabel(text='Hello')
       label.color = [1, 0, 0, 1]  # Style-only, updates immediately
       # No force_rebuild() needed
       labels = find_labels_recursive(label)
       assert all(l.color == [1, 0, 0, 1] for l in labels)
   ```

2. **Testing the deferred rebuild mechanism itself** — When verifying that rebuilds are properly deferred, check `_pending_rebuild` before calling `force_rebuild()`:
   ```python
   def test_text_change_schedules_deferred_rebuild(self):
       label = MarkdownLabel(text='Initial')
       label.text = 'Changed'
       
       # Verify rebuild is pending (deferred, not immediate)
       assert label._pending_rebuild is True
       
       # Now force it to verify the rebuild works
       label.force_rebuild()
       assert label._pending_rebuild is False
   ```

#### Common Patterns for Rebuild Tests

**Pattern 1: Manual ID Comparison (Explicit)**

```python
def test_text_change_triggers_rebuild(self):
    """Test that text changes rebuild the widget tree."""
    # 1. Create widget with initial state
    label = MarkdownLabel(text='Original')
    
    # 2. Collect widget IDs before change
    ids_before = collect_widget_ids(label)
    
    # 3. Change the property (schedules deferred rebuild)
    label.text = 'New text'
    
    # 4. Force immediate rebuild for test determinism
    label.force_rebuild()
    
    # 5. Collect widget IDs after change
    ids_after = collect_widget_ids(label)
    
    # 6. Assert rebuild occurred
    assert ids_before != ids_after, "Widget tree should rebuild for text changes"
```

**Pattern 2: Using Helper Functions (Concise)**

```python
def test_text_change_triggers_rebuild_with_helper(self):
    """Test that text changes rebuild the widget tree."""
    # 1. Create widget with initial state
    label = MarkdownLabel(text='Original')
    
    # 2. Collect widget IDs before change
    ids_before = collect_widget_ids(label)
    
    # 3. Change the property and force rebuild
    label.text = 'New text'
    label.force_rebuild()
    
    # 4. Use helper to verify rebuild occurred
    assert_rebuild_occurred(label, ids_before)
```

**Pattern 3: Style-Only Properties (No Rebuild)**

```python
def test_color_change_preserves_widget_tree(self):
    """Test that color changes preserve widget tree (no rebuild)."""
    # 1. Create widget
    label = MarkdownLabel(text='Hello')
    
    # 2. Collect widget IDs before change
    ids_before = collect_widget_ids(label)
    
    # 3. Change style-only property (NO force_rebuild needed!)
    label.color = [1, 0, 0, 1]
    
    # 4. Verify no rebuild occurred (can use helper or manual)
    assert_no_rebuild(label, ids_before)
    # OR: ids_after = collect_widget_ids(label); assert ids_before == ids_after
    
    # 5. Verify the style change was applied
    labels = find_labels_recursive(label)
    assert all(l.color == [1, 0, 0, 1] for l in labels)
```

**⚠️ CRITICAL: Helper Functions Don't Eliminate Manual Steps**

The helpers `assert_rebuild_occurred()` and `assert_no_rebuild()` **require** you to:
1. Manually collect `ids_before` using `collect_widget_ids()`
2. Make your property change
3. Call `force_rebuild()` if testing structure properties
4. Pass `ids_before` to the helper

They do NOT take a `change_func` parameter. Both manual and helper approaches require the same steps.

## Property-Based Testing

### When to Use Property-Based Tests

Use property-based tests for:

- **Universal properties** that should hold for all inputs
- **Invariants** that must be preserved across operations
- **Round-trip properties** (serialize → deserialize → compare)
- **Metamorphic properties** (relationships between inputs/outputs)

### Property Test Structure

```python
from hypothesis import given, strategies as st, settings

class TestPropertyName:
    """Property tests for [specific behavior]."""
    
    @given(st.text(min_size=1, max_size=100))
    @settings(max_examples=20, deadline=None)  # Adjust based on complexity
    def test_property_description(self, input_value):
        """Test that [property] holds for all valid inputs."""
        # Test implementation
        assert property_holds(input_value)
```

## Property-Based Testing Optimization

### Overview

Property-based testing with Hypothesis generates random inputs to verify that properties hold across many examples. However, using excessive `max_examples` values can lead to unnecessary test execution time without proportional coverage benefits.

### Comment Format Requirements

All property-based tests with custom `max_examples` values MUST include a standardized comment:

```python
# [Strategy Type] strategy: [N] examples ([Rationale])
@settings(max_examples=N, deadline=None)
def test_example(value):
    pass
```

### Strategy Classifications

#### 1. Boolean Strategies

**Pattern:** `st.booleans()`
**Recommended max_examples:** `2`
**Format:** `Boolean strategy: 2 examples (True/False coverage)`

```python
@given(st.booleans())
# Boolean strategy: 2 examples (True/False coverage)
@settings(max_examples=2, deadline=None)
def test_boolean_property(value):
    assert isinstance(value, bool)
```

#### 2. Small Finite Strategies

**Pattern:** Small integer ranges (≤10 values), small `sampled_from` lists
**Recommended max_examples:** Equal to input space size
**Format:** `Small finite strategy: [N] examples (input space size: [N])`

```python
@given(st.integers(min_value=1, max_value=6))
# Small finite strategy: 6 examples (input space size: 6)
@settings(max_examples=6, deadline=None)
def test_dice_roll(value):
    assert 1 <= value <= 6
```

#### 3. Medium Finite Strategies

**Pattern:** Integer ranges or lists with 11-50 values
**Recommended max_examples:** Input space size, capped at 20-50
**Format:** `Medium finite strategy: [N] examples (adequate finite coverage)`

```python
@given(st.integers(min_value=1, max_value=20))
# Medium finite strategy: 20 examples (adequate finite coverage)
@settings(max_examples=20, deadline=None)
def test_medium_range(value):
    assert 1 <= value <= 20
```

#### 4. Combination Strategies (All Finite)

**Pattern:** Multiple finite strategies combined (tuples, multiple @given arguments) where ALL strategies are finite
**Recommended max_examples:** Product of individual strategy sizes, capped at 50
**Format:** `Combination strategy: [N] examples (combination coverage)`

```python
@given(st.tuples(st.booleans(), st.sampled_from(['a', 'b', 'c'])))
# Combination strategy: 6 examples (combination coverage)
@settings(max_examples=6, deadline=None)
def test_boolean_enum_combination(value):
    bool_val, enum_val = value
    assert isinstance(bool_val, bool)
    assert enum_val in ['a', 'b', 'c']
```

**Important:** This classification only applies when ALL combined strategies are finite. If any strategy is complex/infinite, use "Mixed finite/complex strategy" instead.

#### 5. Complex/Infinite Strategies

**Pattern:** Single `st.text()`, `st.floats()`, large ranges, or recursive strategies
**Recommended max_examples:** 10-50 based on complexity
**Format:** `Complex strategy: [N] examples (adequate coverage)` or `Complex strategy: [N] examples (performance optimized)`

```python
@given(st.text())
# Complex strategy: 10 examples (adequate coverage)
@settings(max_examples=10, deadline=None)
def test_text_length_property(text):
    assert len(text) >= 0
```

#### 6. Mixed Finite/Complex Strategies

**Pattern:** Combinations where at least one strategy is finite AND at least one is complex/infinite
**Recommended max_examples:** `finite_size × samples_per_finite_value` (typically 5-10 samples)
**Format:** `Mixed finite/complex strategy: [N] examples ([finite_size] finite × [samples] complex samples)`

The goal is to ensure each finite value gets paired with multiple samples from the complex/infinite space.

```python
# Example 1: Boolean + text
@given(st.booleans(), st.text(min_size=1, max_size=50))
# Mixed finite/complex strategy: 20 examples (2 finite × 10 complex samples)
@settings(max_examples=20, deadline=None)
def test_boolean_with_text(flag, text):
    # Each boolean value (True/False) gets ~10 text samples
    pass

# Example 2: Small enum + floats
@given(
    st.sampled_from(['left', 'center', 'right']),
    st.floats(min_value=0.0, max_value=1.0, allow_nan=False)
)
# Mixed finite/complex strategy: 30 examples (3 finite × 10 complex samples)
@settings(max_examples=30, deadline=None)
def test_alignment_with_opacity(halign, opacity):
    # Each alignment value gets ~10 float samples
    pass

# Example 3: Heading level + color (RGBA floats)
@given(
    st.integers(min_value=1, max_value=6),
    st.tuples(
        st.floats(0, 1, allow_nan=False),
        st.floats(0, 1, allow_nan=False),
        st.floats(0, 1, allow_nan=False),
        st.floats(0, 1, allow_nan=False)
    )
)
# Mixed finite/complex strategy: 30 examples (6 finite × 5 complex samples)
@settings(max_examples=30, deadline=None)
def test_heading_with_color(level, color):
    # Each heading level gets ~5 color samples
    pass
```

**Formula:** `max_examples = finite_space_size × samples_per_value`

| Finite Space Size | Samples per Value | max_examples |
|-------------------|-------------------|--------------|
| 2 (boolean)       | 10                | 20           |
| 3-6 (small enum)  | 5-10              | 15-60        |
| 7-10              | 3-5               | 21-50        |

**Why this matters:** Without this approach, Hypothesis might generate 20 examples that happen to all use `True` with different texts, leaving `False` untested. By sizing based on the finite dimension, we ensure coverage of all finite values.

### Right-Sizing Principles

- **Finite strategies:** Use input space size (test each value once)
- **Infinite strategies:** Use moderate counts based on property complexity
- **Combination strategies (all finite):** Calculate product, cap at 50
- **Mixed finite/complex:** Use `finite_size × samples` to ensure finite coverage

### Performance Impact

Following these guidelines typically results in:

- **Boolean tests:** 98% time reduction (100 → 2 examples)
- **Small finite tests:** 80-95% time reduction
- **Medium finite tests:** 50-80% time reduction  
- **Complex tests:** 0-50% time reduction (may already be appropriate)

### When to Use Hypothesis vs. @pytest.mark.parametrize

Choosing between Hypothesis and `@pytest.mark.parametrize` depends on the **number of dimensions** and the **size of the input space**.

#### Single Dimension: Prefer @pytest.mark.parametrize

For a single finite enumeration (≤10 items), `@pytest.mark.parametrize` is cleaner and guarantees full coverage:

```python
# ✅ GOOD: Single dimension, small enumeration - use parametrize
@pytest.mark.parametrize('halign', ['left', 'center', 'right', 'justify'])
def test_alignment_behavior(halign):
    label = MarkdownLabel(text='Test', halign=halign)
    assert label.halign == halign
```

#### Multiple Dimensions: Beware the Cartesian Product

**CRITICAL:** Multiple `@pytest.mark.parametrize` decorators create a cartesian product of ALL combinations:

```python
# ⚠️ DANGER: This creates 4 × 5 × 6 = 120 test cases!
@pytest.mark.parametrize('halign', ['left', 'center', 'right', 'justify'])  # 4
@pytest.mark.parametrize('direction', ['ltr', 'rtl', 'weak_ltr', 'weak_rtl', None])  # 5
@pytest.mark.parametrize('heading_level', [1, 2, 3, 4, 5, 6])  # 6
def test_alignment_with_direction_and_heading(halign, direction, heading_level):
    ...
```

Compare this to Hypothesis, which **samples** from the combined space:

```python
# ✅ BETTER: Hypothesis samples ~20 combinations from the space
@given(
    halign=st.sampled_from(['left', 'center', 'right', 'justify']),
    direction=st.sampled_from(['ltr', 'rtl', 'weak_ltr', 'weak_rtl', None]),
    heading_level=st.integers(min_value=1, max_value=6)
)
# Combination strategy: 20 examples (sampling from 120 combinations)
@settings(max_examples=20, deadline=None)
def test_alignment_with_direction_and_heading(halign, direction, heading_level):
    ...
```

#### Decision Matrix

| Scenario | Recommendation | Rationale |
|----------|---------------|-----------|
| Single enum, ≤10 values | `@pytest.mark.parametrize` | Full coverage, explicit test cases |
| Single enum, >10 values | Hypothesis `sampled_from` | Avoid excessive test count |
| 2 enums, product ≤20 | Either approach works | Parametrize gives full coverage |
| 2+ enums, product >20 | Hypothesis | Sampling avoids test explosion |
| Infinite/broad space | Hypothesis | Only option for text, floats, etc. |
| Mixed finite + infinite | Hypothesis with "Mixed finite/complex" | Use `finite_size × samples` formula |

#### Hybrid Approach: Parametrize Important Dimension, Sample Others

When one dimension is critical to test exhaustively but others aren't:

```python
# ✅ HYBRID: Test all alignments, sample directions
@pytest.mark.parametrize('halign', ['left', 'center', 'right', 'justify'])
@given(direction=st.sampled_from(['ltr', 'rtl', 'weak_ltr', 'weak_rtl', None]))
@settings(max_examples=5, deadline=None)
def test_alignment_with_sampled_direction(halign, direction):
    ...
```

#### Boundary Testing for Large Enumerations

For enumerations like heading levels (1-6), consider testing only boundaries:

```python
# ✅ GOOD: Test boundaries instead of all 6 levels
@pytest.mark.parametrize('heading_level', [1, 6])  # Min and max only
@pytest.mark.parametrize('direction', ['ltr', 'rtl'])  # Representative values
def test_heading_alignment_boundaries(heading_level, direction):
    ...
```

#### Summary

- **Single dimension, small set:** Use `@pytest.mark.parametrize`
- **Multiple dimensions with large product:** Use Hypothesis to sample
- **Need exhaustive coverage of one dimension:** Use hybrid approach
- **Infinite spaces:** Always use Hypothesis

## Helper Functions

### Using Shared Helpers

Always use helper functions from `test_utils.py` instead of duplicating code:

```python
from .test_utils import (
    find_labels_recursive,
    collect_widget_ids,
    colors_equal,
    padding_equal,
    floats_equal
)

def test_example(self):
    label = MarkdownLabel(text="Test")
    labels = find_labels_recursive(label)  # Use shared helper
    assert len(labels) > 0
```

### Available Helper Functions

#### Widget Traversal
- `find_labels_recursive(widget)` - Find all Label widgets in tree
- `collect_widget_ids(widget)` - Collect widget object IDs for rebuild testing

#### Comparison Utilities
- `colors_equal(color1, color2)` - Compare color values with tolerance
- `padding_equal(pad1, pad2)` - Compare padding values with tolerance
- `floats_equal(f1, f2, tolerance=1e-6)` - Compare floats with tolerance

#### Test Data Generation (Hypothesis Strategies)
- `markdown_heading()` - Generate valid markdown headings
- `markdown_paragraph()` - Generate valid markdown paragraphs
- `markdown_bold()` - Generate bold text markdown
- `simple_markdown_document()` - Generate simple markdown documents
- `color_strategy` - Generate valid RGBA color values

### Adding New Helpers

When adding new helper functions:

1. **Add to `test_utils.py`** - Never duplicate in individual test files
2. **Use descriptive names** - Make the purpose clear
3. **Add docstrings** - Document parameters and return values
4. **Write tests** - Add tests for complex helper functions

### When Local Helpers Are Acceptable

The guideline to consolidate helpers in `test_utils.py` applies to **reusable** helpers. These patterns are acceptable:

- **Test-file-specific helpers**: A helper like `_find_code_block_labels()` that's only meaningful for font property tests can stay in `test_font_properties.py`
- **Renderer-specific strategies**: Custom Hypothesis strategies for generating mistune token structures can stay in `test_inline_renderer.py` if they're not useful elsewhere
- **Serialization helpers**: Functions like `_normalize_ast()` that are specific to serialization testing can stay local
- **Custom widget traversal**: When `find_labels_recursive()` doesn't fit your use case (e.g., you need to filter by a specific attribute or traverse in a specific order), writing custom traversal logic inline is fine

**Rule of thumb**: If a helper is used in 2+ test files, move it to `test_utils.py`. If it's specific to one test file's domain, keeping it local is acceptable.

## Test File Structure

### Standard Test File Template

```python
"""
Brief description of what this test file covers.

This module contains tests for [specific functionality area],
including [list key areas tested].
"""

import pytest
from hypothesis import given, strategies as st, settings

from kivy_garden.markdownlabel import MarkdownLabel
from .test_utils import (
    # Import needed helpers
)


class TestDescriptiveClassName:
    """Property tests for [specific behavior]."""
    
    def test_specific_example(self):
        """Test [specific behavior] with concrete example."""
        # Unit test implementation
        
    @given(st.text())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_property_holds_universally(self, input_text):
        """Test that [property] holds for all valid inputs."""
        # Property test implementation
```

### File Naming

- `test_[functionality_area].py` - e.g., `test_font_properties.py`
- Use underscores for word separation
- Be descriptive about the functionality area
- Group related functionality in the same file

## Standardization Tools

### Command-Line Tools

#### validate_comments.py

Primary CLI tool for comment validation and standardization:

```bash
# Validate all test files
python tools/validate_comments.py validate kivy_garden/markdownlabel/tests/

# Generate detailed report
python tools/validate_comments.py report kivy_garden/markdownlabel/tests/ --output report.json

# Standardize comments (dry run)
python tools/validate_comments.py standardize kivy_garden/markdownlabel/tests/ --dry-run

# Apply standardization with backup
python tools/validate_comments.py standardize kivy_garden/markdownlabel/tests/ --backup-dir ./backups

# Optimize max_examples and add comments
python tools/validate_comments.py optimize kivy_garden/markdownlabel/tests/ --include-comments
```

#### analyze_tests.py

Analyzes test performance and comment compliance:

```bash
# Full analysis with comment validation
python tools/analyze_tests.py --include-comments

# Generate optimization report
python tools/analyze_tests.py --report-format json --output analysis.json
```

## Validation and CI Integration

### Pre-commit Hook

Add comment validation to your pre-commit hook:

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Validating test comments..."
python tools/validate_comments.py validate kivy_garden/markdownlabel/tests/

if [ $? -ne 0 ]; then
    echo "❌ Comment format violations detected."
    echo "Run: python tools/validate_comments.py standardize kivy_garden/markdownlabel/tests/ --dry-run"
    echo "to see suggested fixes."
    exit 1
fi

echo "✅ All comments properly formatted."
```

### GitHub Actions Integration

Add to your CI workflow:

```yaml
name: Test Quality Validation

on: [push, pull_request]

jobs:
  validate-comments:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install -e .
        pip install -e ".[dev]"
    
    - name: Validate comment format
      run: python tools/validate_comments.py validate kivy_garden/markdownlabel/tests/
    
    - name: Check for over-testing
      run: python tools/analyze_tests.py --include-comments
```

### Local Development Workflow

1. **Write your test** following the documentation format
2. **Validate locally:**
   ```bash
   python tools/validate_comments.py validate kivy_garden/markdownlabel/tests/test_your_file.py
   ```
3. **Fix any issues:**
   ```bash
   python tools/validate_comments.py standardize kivy_garden/markdownlabel/tests/test_your_file.py --dry-run
   ```
4. **Apply fixes if needed:**
   ```bash
   python tools/validate_comments.py standardize kivy_garden/markdownlabel/tests/test_your_file.py
   ```
5. **Run tests to ensure functionality:**
   ```bash
   pytest kivy_garden/markdownlabel/tests/test_your_file.py
   ```

## Best Practices

### Quick Reference: Rebuild Testing Patterns

```python
# ✅ CORRECT: Testing structure property changes (rebuild expected)
def test_text_triggers_rebuild(self):
    label = MarkdownLabel(text='Original')
    ids_before = collect_widget_ids(label)  # Step 1: Collect before
    label.text = 'New'                       # Step 2: Change property
    label.force_rebuild()                    # Step 3: Force sync rebuild
    assert_rebuild_occurred(label, ids_before)  # Step 4: Verify rebuild

# ✅ CORRECT: Testing style property changes (no rebuild expected)
def test_color_preserves_tree(self):
    label = MarkdownLabel(text='Hello')
    ids_before = collect_widget_ids(label)  # Step 1: Collect before
    label.color = [1, 0, 0, 1]              # Step 2: Change property (no force_rebuild!)
    assert_no_rebuild(label, ids_before)    # Step 3: Verify no rebuild

# ✅ CORRECT: Manual comparison (alternative to helpers)
def test_text_triggers_rebuild_manual(self):
    label = MarkdownLabel(text='Original')
    ids_before = collect_widget_ids(label)
    label.text = 'New'
    label.force_rebuild()
    ids_after = collect_widget_ids(label)
    assert ids_before != ids_after  # Manual comparison is fine

# ❌ WRONG: Helpers don't take functions
def test_wrong_pattern(self):
    label = MarkdownLabel(text='Original')
    # This signature doesn't exist!
    assert_rebuild_occurred(label, lambda: label.text = 'New')  # ❌ Wrong!
```

### Do's

✅ **Use descriptive test and class names**
✅ **Group related tests in the same class**
✅ **Use shared helper functions from test_utils.py when reusable**
✅ **Test both positive and negative cases**
✅ **Use appropriate pytest markers**
✅ **Write property tests for universal behaviors**
✅ **Test rebuild contracts explicitly**
✅ **Document complex test logic**
✅ **Follow standardized comment format for property tests**
✅ **Right-size max_examples based on strategy type**

### Don'ts

❌ **Don't duplicate helper functions across multiple test files** (local helpers in one file are fine)
❌ **Don't mix completely unrelated functionality in the same class** (related behaviors are fine)
❌ **Don't use vague test names like `test_basic` or `test_misc`**
❌ **Don't claim to test rebuilds without verifying them**
❌ **Don't write property tests for simple examples that don't benefit from fuzzing**
❌ **Don't ignore test failures or skip tests without good reason**
❌ **Don't test implementation details instead of behavior**
❌ **Don't use default max_examples=100 for all property tests**
❌ **Don't ignore finite input space sizes**
❌ **Don't use undocumented custom max_examples values**

### Guidelines vs. Rules

These guidelines aim to improve code quality and maintainability. Use judgment when applying them:

- **Import tests** don't need property-based testing or elaborate class hierarchies
- **Edge case classes** grouping miscellaneous tests for a component are acceptable
- **Local helpers** specific to one test file's domain don't need to be in test_utils.py
- **Manual widget traversal** is fine when shared helpers don't fit the use case
- **Test naming** should be clear, but perfect naming is subjective

The goal is readable, maintainable tests — not rigid adherence to rules.

### Performance Considerations

- **Mark slow tests** with `@pytest.mark.slow`
- **Use appropriate max_examples** for property tests based on strategy type
- **Avoid unnecessary widget creation** in test setup
- **Use `assume()` to filter invalid inputs** in property tests
- **Consider CI optimization** for complex strategies

### Debugging Tests

- **Use descriptive assertion messages** with context
- **Print intermediate values** when debugging complex failures
- **Use `pytest -v`** for verbose output
- **Use `pytest -x`** to stop on first failure
- **Use `pytest --tb=short`** for concise tracebacks

## Examples

### Complete Test Class Example

```python
class TestFontSizeImmediateUpdates:
    """Property tests for font size immediate updates."""
    
    def test_font_size_updates_single_label(self):
        """Test font_size updates immediately for single label."""
        label = MarkdownLabel(text="Hello", base_font_size=16)
        
        # Change font size
        label.base_font_size = 24
        
        # Verify immediate update
        labels = find_labels_recursive(label)
        assert labels[0].font_size == 24
    
    @given(
        st.floats(min_value=8.0, max_value=50.0, allow_nan=False),
        st.floats(min_value=8.0, max_value=50.0, allow_nan=False)
    )
    # Complex strategy: 30 examples (two continuous float ranges)
    @settings(max_examples=30, deadline=None)
    def test_font_size_updates_preserve_scale_factors(self, initial_size, new_size):
        """Test that font size updates preserve heading scale factors."""
        assume(abs(initial_size - new_size) > 1.0)
        
        label = MarkdownLabel(text="# Heading", base_font_size=initial_size)
        
        # Get heading scale factor
        heading_label = find_labels_recursive(label)[0]
        scale_factor = heading_label.font_size / initial_size
        
        # Change base font size
        label.base_font_size = new_size
        
        # Verify scale factor preserved
        expected_size = new_size * scale_factor
        assert abs(heading_label.font_size - expected_size) < 0.1
    
    @given(
        st.integers(min_value=1, max_value=6),  # heading level (finite)
        st.floats(min_value=8.0, max_value=50.0, allow_nan=False)  # font size (complex)
    )
    # Mixed finite/complex strategy: 30 examples (6 finite × 5 complex samples)
    @settings(max_examples=30, deadline=None)
    def test_heading_scale_varies_by_level(self, heading_level, base_size):
        """Test that heading scale factors vary correctly by level."""
        markdown = f"{'#' * heading_level} Heading"
        label = MarkdownLabel(text=markdown, base_font_size=base_size)
        
        heading_label = find_labels_recursive(label)[0]
        # Higher level headings (h1) should have larger scale factors
        expected_min_scale = 1.0 + (6 - heading_level) * 0.1
        assert heading_label.font_size >= base_size * expected_min_scale
```

### Validation Checklist

Before committing tests, verify:

1. **Boolean strategies use max_examples=2**
2. **Small finite strategies use input space size**
3. **Combination strategies (all finite) use product formula (capped at 50)**
4. **Complex strategies use 10-50 examples based on complexity**
5. **Mixed finite/complex strategies use `finite_size × samples` formula**
6. **All custom values include standardized comments**
7. **Comments follow the format: `# [Strategy Type] strategy: [N] examples ([Rationale])`**
8. **Strategy type classifications use standardized terminology**
9. **Rationale templates match the strategy type**
10. **Test names accurately reflect what they assert**
11. **Helper functions are used from test_utils.py**

This comprehensive testing guide ensures consistent, maintainable, and high-performance test coverage for the MarkdownLabel project.