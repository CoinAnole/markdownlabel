# Review of DEVIATIONS.md for `kivy_garden/markdownlabel/tests`

I've examined the deviations listed in `DEVIATIONS.md` against the actual test code and the `TESTING.md` guidelines. Here's my assessment of each deviation's legitimacy and worthiness of fixing:

## **test_advanced_compatibility.py**

### Lines 173, 203, 382, 519, 557, 595, 629, 695, 729, 762, 794, 837, 869 — Manual `assert ids_before == ids_after`
- **Legitimate:** ✅ Yes, the tests use manual assertions rather than the `assert_no_rebuild()` helper
- **Worth fixing:** ⚠️ **Low priority** — The `assert_no_rebuild()` helper exists in `test_utils.py` but these tests were written before the helper was standardized. The manual assertion is functionally equivalent and includes descriptive error messages.

### Lines 296, 323, 349, 373, 388, 399 — Access to `lbl._is_code`
- **Legitimate:** ✅ Yes, these access the private `_is_code` attribute
- **Worth fixing:** ⚠️ **Low priority** — This pattern is used to skip code block Labels when verifying color changes. It's documented behavior that code blocks preserve their own color. The `_is_code` marker is an implementation detail, but there's no public API equivalent. Consider adding `_is_code` to the documented exceptions in `TESTING.md` if frequently used.

### [RESOLVED] Lines 489-491 — Class name `TestReactiveRebuildOnPropertyChange` misleading
- **Legitimate:** ✅ Yes, the class tests that **no** rebuild occurs (widget preservation)
- **Worth fixing:** ✅ **Medium priority** — RESOLVED: Renamed to `TestStylePropertyReactiveUpdates`.

---

## **test_coordinate_translation.py**

### Lines 106, 113, 120, 127, 177, 198, 218 — Missing `@pytest.mark.unit` marker
- **Legitimate:** ✅ Yes, these are unit tests without the marker
- **Worth fixing:** ⚠️ **Low priority** — Per TESTING.md, unit tests should have `@pytest.mark.unit`. However, the tests work correctly without it.

### [RESOLVED] Line 174 — Exact list containment check for float coordinates
- **Legitimate:** ✅ Yes, uses exact `in` check: `expected_box in aggregated_refs[url]`
- **Worth fixing:** ✅ **Medium priority** — RESOLVED: Updated to use `any()` with `padding_equal()`.

### [RESOLVED] Lines 300-303, 329-330 — Exact equality assertions on float computations
- **Legitimate:** ✅ Yes, uses `==` for float comparisons
- **Worth fixing:** ✅ **Medium priority** — RESOLVED: Updated to use `floats_equal()`.

### Lines 425-427, 486-488, 545-547, etc. — Manual float comparisons `abs(diff) < 0.001`
- **Legitimate:** ✅ Yes, uses manual tolerance checks instead of `floats_equal`
- **Worth fixing:** ⚠️ **Low priority** — This is a style inconsistency. The manual check is functionally correct but less readable than `floats_equal()`. Could refactor for consistency.

---

## **test_core_functionality.py**

### Lines 327-329, 346-348, 365-367 — `max_examples=20` for 15-value finite strategy
- **Legitimate:** ✅ Yes, `st.integers(min_value=1, max_value=15)` has 15 values, but `max_examples=20` is used
- **Worth fixing:** ⚠️ **Low priority** — Having more examples than input space is not harmful, just slightly wasteful. Comment says "adequate finite coverage" which is accurate. Could reduce to `max_examples=15` for strictness.

---

## **test_kivy_renderer_blocks.py**

### Lines 527, 550, 570, 588, 591, 536, 557, 597 — Private method/attribute access
- **Legitimate:** ✅ Yes, tests access `renderer._nesting_depth`, `renderer._max_nesting_depth`, and `renderer._render_token()`
- **Worth fixing:** ⚠️ **Questionable** — The `TestDeepNestingTruncation` class tests edge case behavior (truncation when nesting exceeds max), which is difficult to trigger through public API. Per TESTING.md "Edge case classes may access private methods when behavior cannot be easily triggered through public API." The class could benefit from a docstring explicitly stating it's an edge case class.

---

## **test_kivy_renderer_tables.py**

### Lines 152, 225 — Direct calls to `renderer._render_table_cell()`
- **Legitimate:** ✅ Yes, tests call private method directly
- **Worth fixing:** ⚠️ **Low priority** — Both test methods have comments explaining why direct access is needed (isolating specific alignment values, testing fallback behavior). These are edge case tests. Consider adding a class-level docstring indicating edge case testing.

---

## **test_padding_properties.py**

### Lines 118, 265, 317, 362, 620 — Manual `assert ids_before == ids_after`
- **Legitimate:** ✅ Yes, uses manual assertion instead of `assert_no_rebuild()`
- **Worth fixing:** ⚠️ **Low priority** — Functionally equivalent, could refactor for consistency.


### Lines 40-46, 59-65, etc. — Manual `abs(actual - exp) < 0.001` instead of `padding_equal`
- **Legitimate:** ✅ Yes, uses manual tolerance checks
- **Worth fixing:** ⚠️ **Low priority** — Style inconsistency with `padding_equal` helper available.

### Lines 390-546 — Class name `TestPaddingWithNestedStructures`
- **Legitimate:** ✅ Yes, class tests `text_padding` but name suggests container `padding`
- **Worth fixing:** ⚠️ **Low priority** — The tests do test `text_padding` application. Could rename to `TestTextPaddingWithNestedStructures` for clarity.

---

## **test_rebuild_advanced_properties.py**

### Lines 101-104, 164-167, 244-247 — Manual widget ID equality
- **Legitimate:** ✅ Yes, uses manual assertion
- **Worth fixing:** ⚠️ **Low priority** — Could use `assert_no_rebuild()`.

### Lines 268-289 — Access to `_is_code`
- **Legitimate:** ✅ Yes, accesses private marker
- **Worth fixing:** ⚠️ **Low priority** — Same as test_advanced_compatibility.py. Used to identify code block labels.

### Lines 61, 207, 316, 495 — Inaccurate Hypothesis strategy comments
- **Legitimate:** ✅ Partially — Looking at the code:
  - Line 61: `# Mixed finite/complex strategy: 48 examples (8 finite × 6 complex samples)` — The strategy has 8 finite combinations (4 font_hinting × 2 booleans), this seems accurate
- **Worth fixing:** ⚠️ **Low priority** — Comments could be double-checked for accuracy.

---

## **test_rebuild_identity_preservation.py**

### Line 277 — Mixed strategy comment uses incorrect rationale
- **Legitimate:** ✅ Yes, comment says "(sampling from 120 finite combinations)" instead of "(X finite × Y complex samples)"
- **Worth fixing:** ⚠️ **Low priority** — The comment format doesn't strictly follow TESTING.md line 140. However, the rationale is still clear and meaningful.

### [RESOLVED] Line 339 — Mixed strategy comment inaccurately counts complex strategies
- **Legitimate:** ✅ Yes, comment says "24 finite × 2 complex" but there are actually 4 complex strategies (2 × st_rgba_color)
- **Worth fixing:** ✅ **Medium priority** — RESOLVED: Updated to 48 examples (24 finite × 2 complex samples).

---

## **test_rebuild_scheduling.py**


### [RESOLVED] Lines 105-250 — Class with `@pytest.mark.property` contains non-Hypothesis tests
- **Legitimate:** ✅ Yes, `TestDeferredRebuildScheduling` is marked with `@pytest.mark.property` but contains parametrized (line 151) and unit (line 180) tests
- **Worth fixing:** ✅ **Medium priority** — RESOLVED: Moved markers to individual test methods.

---

## **test_sizing_behavior.py**


### Line 555 — Manual `assert ids_before != ids_after` instead of `assert_rebuild_occurred`
- **Legitimate:** ✅ Yes, uses manual assertion
- **Worth fixing:** ⚠️ **Low priority** — Could use `assert_rebuild_occurred()`.

---

## **test_text_properties.py**

### Lines 260-279, 284-304, 309-329 — Lack widget tree preservation assertions
- **Legitimate:** ❌ **Not a clear deviation** — Looking at the actual code:
  - `test_text_size_height_change_updates_labels` (lines 259-278): Tests that text_size updates propagate to child labels. These are value propagation tests, not rebuild contract tests.
  - The tests verify that the **value changes** are applied in-place (no `force_rebuild()` needed), which implicitly demonstrates in-place updates.
- **Worth fixing:** ⚠️ **Low priority** — Could add explicit widget tree preservation assertions for completeness.

---

# Summary Table

| Priority | Count | Description |
|----------|-------|-------------|
| **High** | 0 | None identified |
| **Medium** | 0 | All identified Medium Priority issues resolved |
| **Low** | 12 | Style inconsistencies, missing helpers usage |

## Recommendations

1. **Fix Medium Priority:**
   - Rename `TestReactiveRebuildOnPropertyChange` to better reflect preservation behavior
   - Add tolerance-based float comparisons in coordinate translation tests
   - Fix incorrect comment in `test_rebuild_identity_preservation.py` line 339
   - Address class-level `@pytest.mark.property` marker in `test_rebuild_scheduling.py`

2. **Consider Low Priority (batch fix):**
   - Replace manual `assert ids_before == ids_after` with `assert_no_rebuild()`
   - Replace manual float tolerance checks with `floats_equal()`/`padding_equal()`