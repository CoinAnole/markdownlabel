# Implementation Plan: Strategy Consistency for Finite Enumerations (Revised)

## Overview

This plan addresses mixed strategy choices where some tests use Hypothesis for finite enumerations when `@pytest.mark.parametrize` would be more appropriate. 

**Key Principle:** The choice depends on dimensionality and product size, not just whether inputs are finite.

## Decision Rules

| Scenario | Action |
|----------|--------|
| Single `sampled_from` with ≤10 items | Convert to `@pytest.mark.parametrize` |
| Single `st.just()` (1 value) | Remove `@given`, make unit test |
| Multiple `sampled_from` with product ≤20 | Either approach acceptable |
| Multiple `sampled_from` with product >20 | Keep Hypothesis (sampling is more efficient) |
| Any combination with infinite strategies | Keep Hypothesis |

## Implementation Tasks

### Task 1: test_kivy_renderer.py - Remove Trivial @given

**Priority:** HIGH (simplest wins)

Three tests use `st.just({'type': 'thematic_break'})` - a single constant value. This is pointless Hypothesis usage.

**Tests to Convert:**
1. `test_thematic_break_renders_horizontal_rule` (line ~405)
2. `test_thematic_break_creates_horizontal_rule_widget` (line ~415)  
3. `test_thematic_break_no_children` (line ~426)

**Action:** Remove `@given` decorator entirely, inline the constant:

```python
# Before
@given(st.just({'type': 'thematic_break'}))
def test_thematic_break_renders_horizontal_rule(self, token):
    ...

# After
def test_thematic_break_renders_horizontal_rule(self):
    token = {'type': 'thematic_break'}
    ...
```

---

### Task 2: Single-Dimension sampled_from Conversions

**Priority:** MEDIUM

These tests use `sampled_from` with a single small enumeration. Converting to parametrize gives explicit coverage and cleaner test output.

**Candidates:**

1. **test_rebuild_semantics.py**
   - `test_font_name_change_triggers_rebuild_pbt`: `sampled_from(['Roboto', 'RobotoMono-Regular', 'Roboto-Bold'])` (3 items)
   - `test_link_style_change_triggers_rebuild_pbt`: `sampled_from(['unstyled', 'styled'])` (2 items)

2. **test_font_properties.py**
   - Test with `sampled_from([None, 'normal', 'light', 'mono'])` (4 items)

3. **test_advanced_compatibility.py**
   - Test with `sampled_from(['Roboto', 'Roboto-Bold', 'Roboto-Italic'])` (3 items)

4. **test_label_compatibility.py**
   - Test with `sampled_from([None, 'ltr', 'rtl', 'weak_ltr', 'weak_rtl'])` (5 items)

5. **test_text_properties.py**
   - Test with `sampled_from(['top', 'middle', 'bottom'])` (3 items)

**Action:** Convert each to `@pytest.mark.parametrize`.

---

### Task 3: DO NOT Convert Multi-Dimensional Tests

**Priority:** N/A (no action needed)

The following tests should **remain as Hypothesis** because their cartesian products are large:

1. **test_rtl_alignment.py** - Most tests combine 2-3 dimensions:
   - `test_direction_change_updates_heading_alignment`: 6 × 3 × 2 = 36 combinations
   - `test_explicit_alignment_overrides_rtl_for_headings`: 4 × 2 × 6 = 48 combinations
   - `test_explicit_alignment_unchanged_by_direction_change`: 4 × 2 × 3 = 24 combinations
   
   **Keep Hypothesis with appropriate `max_examples` (10-20).**

2. **test_rebuild_semantics.py** - Tests combining multiple style properties:
   - `test_style_property_changes_preserve_widget_tree`: Multiple dimensions
   - `test_style_property_values_propagate_to_descendants`: Multiple dimensions
   
   **Keep Hypothesis.**

3. **test_shortening_and_coordinate.py** - Tests with color + alignment combinations:
   - Keep Hypothesis for multi-dimensional tests
   - Single-dimension color tests (3 items) could be parametrized

---

### Task 4: Optimize max_examples for Multi-Dimensional Tests

**Priority:** MEDIUM

For tests that remain as Hypothesis with multiple `sampled_from`, ensure `max_examples` is right-sized:

- Product ≤ 20: Use product size (full coverage)
- Product 20-50: Use 20 examples
- Product > 50: Use 20-30 examples (sampling)

**Example:**
```python
# 3 directions × 2 new_directions × 6 heading_levels = 36 combinations
# Use 20 examples to sample adequately without exhaustive testing
@given(
    initial_direction=st.sampled_from(['ltr', 'weak_ltr', None]),
    new_direction=st.sampled_from(['rtl', 'weak_rtl']),
    heading_level=st.integers(min_value=1, max_value=6)
)
# Combination strategy: 20 examples (sampling from 36 combinations)
@settings(max_examples=20, deadline=None)
def test_direction_change_updates_heading_alignment(...):
    ...
```

---

### Task 5: Update TESTING.md

**Status:** COMPLETED

The "When to Use Hypothesis vs. @pytest.mark.parametrize" section has been updated with:
- Decision matrix based on dimensionality
- Warning about cartesian product explosion
- Hybrid approach examples
- Boundary testing suggestions

---

## Implementation Order

1. **Phase 1:** Task 1 (trivial `st.just()` removal) - 3 tests
2. **Phase 2:** Task 2 (single-dimension conversions) - ~8 tests  
3. **Phase 3:** Task 4 (optimize multi-dimensional max_examples) - review existing tests
4. **Phase 4:** Run full test suite, verify timing improvement

## Expected Impact

- **Tests converted:** ~11 (only single-dimension cases)
- **Tests unchanged:** All multi-dimensional tests remain as Hypothesis
- **Timing impact:** Modest improvement from removing trivial Hypothesis overhead
- **Coverage:** Maintained or improved (explicit parametrize = guaranteed coverage)

## What NOT To Do

❌ Do not convert multi-dimensional `sampled_from` combinations to multiple `@pytest.mark.parametrize` decorators - this causes test explosion

❌ Do not blindly apply "parametrize for finite enumerations" - consider the product size

❌ Do not use `itertools.product` with `@pytest.mark.parametrize` for large combinations

## Success Criteria

- Single-dimension finite enumerations use `@pytest.mark.parametrize`
- Multi-dimensional tests use Hypothesis with right-sized `max_examples`
- No `st.just()` with single constant values
- Test suite timing remains reasonable (target: <60s for full suite)
- All tests pass
