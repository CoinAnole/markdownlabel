# Implementation Plan: Strategy Consistency for Finite Enumerations

## Overview

This plan addresses the mixed strategy choice issue where some tests use Hypothesis for finite enumerations when they should use `@pytest.mark.parametrize`. The goal is to establish consistency across the test suite following the principle: **Hypothesis for broad spaces; parametrize for fixed lists / small domains.**

## Guideline to Establish

Add to `TESTING.md`:

```markdown
### When to Use Hypothesis vs. @pytest.mark.parametrize

**Use @pytest.mark.parametrize for:**
- Finite enumerations with ≤10 items (e.g., alignment values, font names, modes)
- Testing all possible values of a small, fixed domain
- When you want explicit test cases for each value
- Combinations of small finite domains (use `itertools.product` or multiple `@pytest.mark.parametrize` decorators)

**Use Hypothesis for:**
- Broad input spaces (text, floats, large integer ranges)
- Infinite or very large domains
- Testing universal properties across many examples
- Complex data structures with many possible combinations
- When you want Hypothesis to generate edge cases you might not think of

**Examples:**

```python
# ✅ CORRECT: Use parametrize for small finite enumeration
@pytest.mark.parametrize('halign', ['left', 'center', 'right', 'justify'])
def test_alignment_behavior(halign):
    label = MarkdownLabel(text='Test', halign=halign)
    assert label.halign == halign

# ❌ AVOID: Don't use Hypothesis for small finite enumeration
@given(st.sampled_from(['left', 'center', 'right', 'justify']))
def test_alignment_behavior(halign):
    label = MarkdownLabel(text='Test', halign=halign)
    assert label.halign == halign

# ✅ CORRECT: Use Hypothesis for broad input space
@given(st.text(min_size=1, max_size=100))
def test_text_rendering(text):
    label = MarkdownLabel(text=text)
    assert len(find_labels_recursive(label)) > 0
```
```

## Implementation Tasks

### Task 1: HIGH PRIORITY - test_rtl_alignment.py

**File:** `kivy_garden/markdownlabel/tests/test_rtl_alignment.py`

**Issue:** 13 tests use `st.sampled_from()` with 2-5 items, but the same file already correctly uses `@pytest.mark.parametrize` for similar enumerations (lines 26, 49, 130, 158), showing inconsistency.

**Tests to Convert:**

1. `test_auto_alignment_rtl_applies_to_headings` (lines 72-97)
   - Current: `st.sampled_from(['rtl', 'weak_rtl'])` + `st.integers(min_value=1, max_value=6)`
   - Convert to: `@pytest.mark.parametrize('base_direction', ['rtl', 'weak_rtl'])`
   - Keep heading_level as separate parametrize or keep as Hypothesis

2. `test_auto_alignment_ltr_applies_to_headings` (lines 101-126)
   - Current: `st.sampled_from(['ltr', 'weak_ltr', None])` + `st.integers(min_value=1, max_value=6)`
   - Convert to: `@pytest.mark.parametrize('base_direction', ['ltr', 'weak_ltr', None])`

3. `test_direction_change_ltr_to_rtl_updates_alignment` (lines 196-229)
   - Current: Two `st.sampled_from()` with 3 and 2 items
   - Convert to: Double parametrize or `itertools.product`

4. `test_direction_change_rtl_to_ltr_updates_alignment` (lines 233-266)
   - Current: Two `st.sampled_from()` with 2 and 3 items
   - Convert to: Double parametrize or `itertools.product`

5. `test_direction_change_updates_heading_alignment` (lines 268-309)
   - Current: Three strategies including two `st.sampled_from()`
   - Convert to: Triple parametrize or `itertools.product`

6. `test_direction_change_preserves_widget_identities` (lines 312-343)
   - Current: Two `st.sampled_from()` with 3 and 2 items
   - Convert to: Double parametrize

7. `test_direction_change_mixed_content_updates_alignment` (lines 346-388)
   - Current: Two `st.sampled_from()` with 3 and 2 items
   - Convert to: Double parametrize

8. `test_explicit_alignment_overrides_base_direction` (lines 401-426)
   - Current: Two `st.sampled_from()` with 4 and 5 items
   - Convert to: Double parametrize (20 test cases)

9. `test_explicit_alignment_overrides_rtl_for_headings` (lines 430-459)
   - Current: Three strategies including two `st.sampled_from()`
   - Convert to: Triple parametrize

10. `test_explicit_alignment_overrides_direction_for_mixed_content` (lines 463-492)
    - Current: Two `st.sampled_from()` with 4 and 5 items
    - Convert to: Double parametrize

11. `test_explicit_alignment_unchanged_by_direction_change` (lines 496-532)
    - Current: Three `st.sampled_from()` with 4, 2, and 3 items
    - Convert to: Triple parametrize

12. `test_explicit_alignment_stored_correctly_on_widget` (lines 535-561)
    - Current: Two `st.sampled_from()` with 4 and 5 items
    - Convert to: Double parametrize

**Expected Impact:** 13 tests converted from property-based to parametrized tests, improving consistency with existing tests in the same file.

---

### Task 2: MEDIUM PRIORITY - test_rebuild_scheduling.py

**File:** `kivy_garden/markdownlabel/tests/test_rebuild_scheduling.py`

**Issue:** Uses `st.sampled_from(["Roboto", "RobotoMono-Regular"])` with 2 items, while line 200 correctly uses `@pytest.mark.parametrize` for similar enumeration.

**Test to Convert:**

1. `test_mixed_property_changes_batch_rebuilds` (lines 66-117)
   - Current: `st.sampled_from(["Roboto", "RobotoMono-Regular"])` at line 81
   - Convert to: `@pytest.mark.parametrize('font_name', ["Roboto", "RobotoMono-Regular"])`
   - Keep text and font_size as Hypothesis strategies (broad spaces)

**Expected Impact:** 1 test converted, consistent with existing pattern in same file.

---

### Task 3: MEDIUM PRIORITY - test_rebuild_semantics.py

**File:** `kivy_garden/markdownlabel/tests/test_rebuild_semantics.py`

**Issue:** Multiple tests use `st.sampled_from()` with 2-5 items for finite enumerations.

**Tests to Convert:**

1. `test_style_property_changes_preserve_widget_tree` (lines 274-352)
   - Current: `st.sampled_from(['left', 'center', 'right', 'justify'])` (line 288)
   - Current: `st.sampled_from(['bottom', 'middle', 'top'])` (line 289)
   - Current: `st.sampled_from([None, 'ltr', 'rtl', 'weak_ltr', 'weak_rtl'])` (line 301)
   - Convert to: Multiple parametrize decorators or `itertools.product`
   - Keep broad strategies (markdown_text, base_font_size, color, line_height, disabled_color, disabled)

2. `test_style_property_values_propagate_to_descendants` (lines 494-577)
   - Current: `st.sampled_from(['left', 'center', 'right', 'justify'])` (line 506)
   - Current: `st.sampled_from(['bottom', 'middle', 'top'])` (line 507)
   - Current: `st.sampled_from([None, 'ltr', 'rtl', 'weak_ltr', 'weak_rtl'])` (line 510)
   - Convert to: Multiple parametrize decorators or `itertools.product`

3. `test_font_name_change_triggers_rebuild_pbt` (lines 808-853)
   - Current: `st.sampled_from(['Roboto', 'RobotoMono-Regular', 'Roboto-Bold'])` (line 810)
   - Convert to: `@pytest.mark.parametrize('font_name', ['Roboto', 'RobotoMono-Regular', 'Roboto-Bold'])`

4. `test_link_style_change_triggers_rebuild_pbt` (lines 855-900)
   - Current: `st.sampled_from(['unstyled', 'styled'])` (line 857)
   - Convert to: `@pytest.mark.parametrize('link_style', ['unstyled', 'styled'])`

5. `test_root_id_preserved_across_style_property_changes` (lines 912-969)
   - Current: `st.sampled_from(['left', 'center', 'right', 'justify'])` (line 927)
   - Current: `st.sampled_from(['bottom', 'middle', 'top'])` (line 928)
   - Convert to: Multiple parametrize decorators or `itertools.product`

6. `test_root_id_preserved_across_structure_property_changes` (lines 971-1016)
   - Current: `st.sampled_from(['Roboto', 'RobotoMono-Regular', 'Roboto-Bold'])` (line 974)
   - Current: `st.sampled_from(['unstyled', 'styled'])` (line 975)
   - Current: `st.sampled_from(['widgets', 'auto'])` (line 977)
   - Convert to: Multiple parametrize decorators or `itertools.product`

7. `test_root_id_preserved_across_mixed_property_changes` (lines 1018-1070)
   - Current: `st.sampled_from(['Roboto', 'RobotoMono-Regular', 'Roboto-Bold'])` (line 1033)
   - Current: `st.sampled_from(['unstyled', 'styled'])` (line 1034)
   - Convert to: Multiple parametrize decorators or `itertools.product`

**Expected Impact:** 7 tests converted, removing Hypothesis from small finite enumerations while keeping it for broad input spaces.

---

### Task 4: MEDIUM PRIORITY - test_shortening_and_coordinate.py

**File:** `kivy_garden/markdownlabel/tests/test_shortening_and_coordinate.py`

**Issue:** Uses `st.sampled_from()` with 3 colors and 3 alignments.

**Tests to Convert:**

1. `test_markup_color_propagates_to_label` (lines 203-217)
   - Current: `st.sampled_from([[1, 0, 0, 1], [0, 1, 0, 1], [0, 0, 1, 1]])` (line 204)
   - Convert to: `@pytest.mark.parametrize('markup_color', [[1, 0, 0, 1], [0, 1, 0, 1], [0, 0, 1, 1]])`

2. `test_markup_color_updates_on_change` (lines 219-233)
   - Current: Same as above (line 220)
   - Convert to: Same parametrize

3. `test_markup_color_independent_across_labels` (lines 235-249)
   - Current: Same as above (line 236)
   - Convert to: Same parametrize

4. `test_markup_color_with_multiple_labels` (lines 251-265)
   - Current: Same as above (line 253)
   - Convert to: Same parametrize

5. `test_shortening_behavior_with_alignment` (lines 280-295)
   - Current: `st.sampled_from(['left', 'center', 'right'])` (line 281)
   - Convert to: `@pytest.mark.parametrize('halign', ['left', 'center', 'right'])`

**Expected Impact:** 5 tests converted.

---

### Task 5: LOW PRIORITY - test_performance.py

**File:** `kivy_garden/markdownlabel/tests/test_performance.py`

**Issue:** Uses `st.sampled_from()` with 3 alignment values.

**Test to Convert:**

1. Find test with `st.sampled_from(['left', 'center', 'right'])` (line 343)
   - Convert to: `@pytest.mark.parametrize('halign', ['left', 'center', 'right'])`

2. Find test with `st.sampled_from(['top', 'middle', 'bottom'])` (line 344)
   - Convert to: `@pytest.mark.parametrize('valign', ['top', 'middle', 'bottom'])`

**Expected Impact:** 1-2 tests converted.

---

### Task 6: LOW PRIORITY - test_text_properties.py

**File:** `kivy_garden/markdownlabel/tests/test_text_properties.py`

**Issue:** Uses `st.sampled_from()` with 3 vertical alignment values.

**Test to Convert:**

1. Find test with `st.sampled_from(['top', 'middle', 'bottom'])` (line 159)
   - Convert to: `@pytest.mark.parametrize('valign', ['top', 'middle', 'bottom'])`

**Expected Impact:** 1 test converted.

---

### Task 7: LOW PRIORITY - test_font_properties.py

**File:** `kivy_garden/markdownlabel/tests/test_font_properties.py`

**Issue:** Uses `st.sampled_from()` with 4 font weight values.

**Test to Convert:**

1. Find test with `st.sampled_from([None, 'normal', 'light', 'mono'])` (line 500)
   - Convert to: `@pytest.mark.parametrize('font_weight', [None, 'normal', 'light', 'mono'])`

**Expected Impact:** 1 test converted.

---

### Task 8: LOW PRIORITY - test_advanced_compatibility.py

**File:** `kivy_garden/markdownlabel/tests/test_advanced_compatibility.py`

**Issue:** Uses `st.sampled_from()` with 3 font names.

**Test to Convert:**

1. Find test using `rebuild_font_names` strategy (line 538)
   - Current: `st.sampled_from(['Roboto', 'Roboto-Bold', 'Roboto-Italic'])`
   - Convert to: `@pytest.mark.parametrize('font_name', ['Roboto', 'Roboto-Bold', 'Roboto-Italic'])`

**Expected Impact:** 1 test converted.

---

### Task 9: LOW PRIORITY - test_kivy_renderer.py

**File:** `kivy_garden/markdownlabel/tests/test_kivy_renderer.py`

**Issue:** Uses `st.just({'type': 'thematic_break'})` with a single value.

**Tests to Convert:**

1. `test_thematic_break_renders_horizontal_rule` (lines 405-412)
   - Current: `st.just({'type': 'thematic_break'})` (line 405)
   - Convert to: Remove `@given` decorator, make it a simple unit test

2. `test_thematic_break_creates_horizontal_rule_widget` (lines 415-423)
   - Current: `st.just({'type': 'thematic_break'})` (line 415)
   - Convert to: Remove `@given` decorator, make it a simple unit test

3. `test_thematic_break_no_children` (lines 426-433)
   - Current: `st.just({'type': 'thematic_break'})` (line 426)
   - Convert to: Remove `@given` decorator, make it a simple unit test

**Expected Impact:** 3 tests converted from property-based to simple unit tests.

---

### Task 10: LOW PRIORITY - test_label_compatibility.py

**File:** `kivy_garden/markdownlabel/tests/test_label_compatibility.py`

**Issue:** Uses `st.sampled_from()` with 5 direction values.

**Test to Convert:**

1. Find test with `st.sampled_from([None, 'ltr', 'rtl', 'weak_ltr', 'weak_rtl'])` (line 299)
   - Convert to: `@pytest.mark.parametrize('base_direction', [None, 'ltr', 'rtl', 'weak_ltr', 'weak_rtl'])`

**Expected Impact:** 1 test converted.

---

### Task 11: Update TESTING.md

**File:** `kivy_garden/markdownlabel/tests/TESTING.md`

**Action:** Add the guideline section "When to Use Hypothesis vs. @pytest.mark.parametrize" (see Guideline section above).

**Location:** Add after "Property-Based Testing Optimization" section, before "Helper Functions" section.

**Expected Impact:** Clear documentation of when to use each approach.

---

### Task 12: Run Tests

**Action:** After all refactoring is complete, run the full test suite to ensure all changes work correctly.

```bash
cd /home/coinanole/repos/markdownlabel
pytest kivy_garden/markdownlabel/tests/ -v
```

**Expected Impact:** Verify all refactored tests pass.

---

### Task 13: Update Meta-Tests (if needed)

**Files to Check:**
- `test_strategy_classification.py`
- `test_comment_format.py`
- `test_comment_standardizer.py`

**Action:** Review meta-tests to ensure they don't expect Hypothesis usage for finite enumerations. Update if necessary.

**Expected Impact:** Meta-tests align with new guidelines.

---

## Implementation Order

1. **Phase 1 (High Priority):** test_rtl_alignment.py
2. **Phase 2 (Medium Priority):** test_rebuild_scheduling.py, test_rebuild_semantics.py, test_shortening_and_coordinate.py
3. **Phase 3 (Low Priority):** test_performance.py, test_text_properties.py, test_font_properties.py, test_advanced_compatibility.py, test_kivy_renderer.py, test_label_compatibility.py
4. **Phase 4 (Documentation):** Update TESTING.md
5. **Phase 5 (Validation):** Run tests, update meta-tests if needed

## Testing Strategy

For each file conversion:
1. Read the current test file
2. Identify all tests using `st.sampled_from()` or `st.just()` with small finite lists
3. Convert each test to use `@pytest.mark.parametrize`
4. For combinations, use multiple `@pytest.mark.parametrize` decorators or `itertools.product`
5. Keep Hypothesis for broad input spaces (text, floats, large ranges)
6. Remove `@given`, `@settings`, and Hypothesis imports for converted tests
7. Update test names if needed to reflect parametrized nature
8. Verify the converted tests maintain the same coverage

## Success Criteria

- All finite enumerations with ≤10 items use `@pytest.mark.parametrize`
- Hypothesis is only used for broad input spaces, infinite domains, or complex strategies
- All tests pass after conversion
- TESTING.md documents the new guideline
- Meta-tests align with the new approach
- Test suite is more consistent and maintainable

## Risk Mitigation

- **Risk:** Converting to parametrize might increase test count significantly (e.g., 4×5 = 20 tests)
  - **Mitigation:** This is acceptable; explicit test cases are more readable and maintainable

- **Risk:** Some tests might be testing properties that genuinely benefit from Hypothesis
  - **Mitigation:** Keep Hypothesis for broad input spaces; only convert finite enumerations

- **Risk:** Breaking existing tests during conversion
  - **Mitigation:** Test each file individually after conversion before proceeding to next

## Notes

- The test suite already has meta-tests encouraging `parametrize` usage
- Some files (like test_rtl_alignment.py) demonstrate both approaches inconsistently
- This refactoring will establish a clear, consistent pattern across the entire test suite
- The guideline will help prevent future inconsistencies
