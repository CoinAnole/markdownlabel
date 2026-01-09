# Review of Test Suite Deviations

Based on my analysis of the DEVIATIONS.md file against the TESTING.md guidelines and the actual test code, here is my assessment of each identified deviation:

## test_color_properties.py

### Line 82: Test method naming pattern
**Deviation:** [test_color_change_updates_value_without_rebuild](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_color_properties.py:77:4-106:79) uses "updates value" pattern but also verifies no rebuild occurred.

**Assessment:** ✅ **Legitimate but LOW priority**

Looking at line 82-101, the test *does* verify no rebuild occurred (lines 99-101 `assert ids_before == ids_after`). The TESTING.md guidelines at lines 117-118 state:
- `test_*_triggers_rebuild_*` - ONLY for tests that verify a rebuild occurred
- `test_*_preserves_widget_tree_*` - For tests that verify NO rebuild occurred

The name [test_color_change_updates_value_without_rebuild](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_color_properties.py:77:4-106:79) is technically a hybrid — it describes both behaviors. A cleaner name would be `test_color_change_preserves_widget_tree` or `test_color_property_preserves_widget_tree_and_updates_value`. However, the current name is reasonably descriptive and not misleading.

**Recommendation:** Low priority fix. The name is acceptable but could be improved.

---

## test_font_properties.py

### Lines 317-342: Helper functions using [language_info](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_kivy_renderer_blocks.py:327:4-340:84) attribute
**Deviation:** [_find_code_block_labels](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_font_properties.py:316:4-334:26) and [_find_non_code_labels](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_font_properties.py:336:4-340:68) use internal [language_info](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_kivy_renderer_blocks.py:327:4-340:84) attribute.

**Assessment:** ✅ **Legitimate but ACCEPTABLE**

Looking at lines 317-342 in the actual code, these are **local helper functions** (prefixed with `_`) that identify code block containers by their [language_info](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_kivy_renderer_blocks.py:327:4-340:84) attribute. The TESTING.md at lines 897-904 explicitly allows:

> **Test-file-specific helpers**: A helper like [_find_code_block_labels()](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_font_properties.py:316:4-334:26) that's only meaningful for font property tests can stay in [test_font_properties.py](cci:7://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_font_properties.py:0:0-0:0)

The [language_info](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_kivy_renderer_blocks.py:327:4-340:84) attribute is a **documented public attribute** set on code block widgets (see [test_kivy_renderer_blocks.py](cci:7://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_kivy_renderer_blocks.py:0:0-0:0) lines 339-341 where it's explicitly tested). This is not a private implementation detail.

**Recommendation:** No fix needed. This is acceptable per guidelines.

### Lines 570, 640, 680, 726: Imports of HEADING_SIZES inside tests
**Deviation:** Tests import `KivyRenderer.HEADING_SIZES` inside test methods.

**Assessment:** ✅ **Legitimate but LOW priority**

The imports access `HEADING_SIZES` which is a **public constant** (`KivyRenderer.HEADING_SIZES`), not a private attribute. The deviation notes it as "internal" but `HEADING_SIZES` is documented in the public API for heading scale factors. Importing inside test methods is unusual but not prohibited.

**Recommendation:** Minor cleanup — move imports to top of file for consistency, but not a guideline violation.

### Lines 598-604, 800-807, 815-822: Manual iteration over `label.children`
**Deviation:** Tests iterate over `label.children` assuming specific widget tree structure.

**Assessment:** ✅ **Legitimate but LOW priority**

Looking at lines 598-604, the code finds a paragraph Label via `for child in label.children: if isinstance(child, Label)`. This is actually **testing observable behavior** — verifying that child Labels exist and have certain properties. The TESTING.md recommends using `find_labels_recursive()` for consistency, but manual traversal is acceptable per line 902.

**Recommendation:** Could be cleaned up to use shared helpers, but not a guideline violation.

---

## test_inline_renderer.py

### Lines 831 and 848-852: Testing private methods without justification
**Deviation:** Direct calls to `renderer._unknown(token)` and `renderer._escape_markup()`.

**Assessment:** ✅ **Legitimate and MEDIUM priority**

Looking at lines 821-832 and 846-852, these tests directly call private methods ([_unknown](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_inline_renderer.py:820:4-830:64) and [_escape_markup](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_inline_renderer.py:845:4-851:58)). The TESTING.md "Testing Exceptions" section (lines 1135-1143) lists specific allowed exceptions:
- `_get_effective_render_mode()`
- `_aggregated_refs`
- `_get_effective_halign()`

[_unknown](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_inline_renderer.py:820:4-830:64) and [_escape_markup](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_inline_renderer.py:845:4-851:58) are **not listed**. 

- **[_escape_markup](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_inline_renderer.py:845:4-851:58)**: This has a clear public behavioral equivalent — you can test escaping by rendering a [text](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_inline_renderer.py:14:0-18:39) token and verifying the output. The test at line 850 (`assert renderer._escape_markup('[b]') == '&bl;b&br;'`) could instead use `renderer.text({'type': 'text', 'raw': '[b]'})`.

- **[_unknown](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_inline_renderer.py:820:4-830:64)**: Line 831 tests the fallback behavior for unknown token types. This *could* be tested via `renderer.render([token])` (which is done on line 827), making the direct [_unknown](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_inline_renderer.py:820:4-830:64) call redundant.

**Recommendation:** Medium priority fix. Remove direct private method calls or add justification comments if they're truly necessary.

---

## test_kivy_renderer_blocks.py

### Lines 225-266: [test_nested_list_increases_indentation](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_kivy_renderer_blocks.py:220:4-263:75) name/assertion mismatch
**Deviation:** Name claims verification of increasing padding per nesting level, but only checks fixed outer list padding.

**Assessment:** ✅ **Legitimate and MEDIUM priority**

Looking at lines 225-264, the test name is [test_nested_list_increases_indentation](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_kivy_renderer_blocks.py:220:4-263:75) and docstring says "Nested lists have increasing left padding." However, the assertions only verify:
```python
assert widget.padding[0] > 0, "List should have left padding"
expected_padding = 20  # First level padding
assert widget.padding[0] == expected_padding
```

This only checks the **outer list** padding, not the nested lists. To verify "increases indentation," it should traverse into nested lists and confirm each level has greater padding.

**Recommendation:** Medium priority. Either fix the test to verify nested indentation increases, or rename to `test_nested_list_has_left_padding`.

### Lines 477-569: [TestDeepNestingTruncation](cci:2://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_kivy_renderer_blocks.py:476:0-566:58) class uses private `_nesting_depth` and `_render_token`
**Deviation:** Directly sets `renderer._nesting_depth` and calls `renderer._render_token`.

**Assessment:** ✅ **Legitimate and HIGH priority**

Looking at lines 477-569, this class extensively uses private internals:
- `renderer._nesting_depth = renderer._max_nesting_depth + 1` (lines 489, 513, 533, 552)
- `renderer._render_token(token, None)` (lines 498, 519, 537, 559)

These are not in the documented exceptions list in TESTING.md.

**However**, the docstrings provide clear justification:
> "Requirement 7.1: WHEN rendering content that exceeds _max_nesting_depth, THE KivyRenderer SHALL return a truncation placeholder widget."

This tests **nesting depth protection** which is a documented core constraint (structure.md line 56). There's no public API to trigger max nesting depth without creating deeply nested actual content.

**Recommendation:** Medium priority. Add these methods to the "Testing Exceptions" list in TESTING.md and add justification comments to the tests.

### Lines 582-611, 613-638, 640-670, 672-684, 706-718: Other private method access
**Deviation:** Multiple tests call private methods ([_render_list_item](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_kivy_renderer_blocks.py:581:4-609:35), `_apply_text_size_binding`, etc.).

**Assessment:** ✅ **Legitimate and MEDIUM priority**

These tests are in [TestKivyRendererEdgeCases](cci:2://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_kivy_renderer_blocks.py:569:0-723:55) which explicitly targets "internal methods" for code coverage. While this violates the "test behavior, not implementation" principle, some internal method testing is pragmatic for coverage.

**Recommendation:** Either add justification comments or document these as acceptable exceptions for coverage-focused tests.

---

## test_kivy_renderer_tables.py

### Lines 150, 221, 235-239, 198-208: Private method and internal attribute access
**Assessment:** ✅ **Legitimate and MEDIUM priority** — similar pattern to blocks tests.

### Line 254: Name/assertion mismatch
**Deviation:** `test_table_internals_coverage` only asserts public [table()](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_color_properties.py:125:4-140:64) returns non-None GridLayout.

**Assessment:** ✅ **Legitimate and LOW priority**

The name suggests testing "internals" but the assertion is public. Either rename or verify additional internal behavior.

---

## test_padding_properties.py

### Lines 390-546: Class name/docstring mismatch
**Deviation:** `TestPaddingWithNestedStructures` tests `text_padding` forwarding, not generic "padding."

**Assessment:** ✅ **Legitimate and LOW priority**

The class name could be more specific (`TestTextPaddingWithNestedStructures`), but this is a minor naming issue.

---

## test_rebuild_identity_preservation.py

### Lines 26-55: Mixed meta-tests with regular tests
**Deviation:** [TestWidgetIdentityHelpers](cci:2://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_rebuild_identity_preservation.py:25:0-52:35) mixes helper function tests with MarkdownLabel tests.

**Assessment:** ✅ **Legitimate and LOW priority**

Looking at lines 26-55, this class tests the [collect_widget_ids](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_rebuild_identity_preservation.py:30:4-34:31) helper function. The tests are marked with `@pytest.mark.test_tests` as required. While they could be moved to `meta_tests/`, having them in the same file as the tests that use the helper is reasonable for discoverability.

**Recommendation:** Acceptable. Could move to meta_tests for stricter organization.

### Lines 276, 338, 380, 459: Incorrect `max_examples` rationale math
**Assessment:** ✅ **Legitimate and HIGH priority**

These are factual errors:
- Line 276: "120 finite × 5 complex samples" but 120×5=600 ≠ 50
- Line 338: "24 finite × 4 complex samples" but 24×4=96 ≠ 50
- Line 380: "24 finite × 2 complex samples" but the finite product is 8, not 24
- Line 459: "3 finite × 5 complex samples" but both strategies appear complex

**Recommendation:** High priority. Fix the comments to accurately reflect the rationale.

### Line 380: [font_name](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_font_properties.py:49:4-60:70) misclassified as structure property
**Deviation:** Test claims "structure property changes" but includes [font_name](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_font_properties.py:49:4-60:70) which is style-only.

**Assessment:** ✅ **Legitimate and MEDIUM priority**

Looking at line 380-413, the test [test_root_id_preserved_across_structure_property_changes](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_rebuild_identity_preservation.py:371:4-412:9) includes [font_name](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_font_properties.py:49:4-60:70) in its parameters. According to TESTING.md line 234: "font_name - Updates Label.font_name on existing Labels (non-code Labels)" — this is a **style-only property**.

**Recommendation:** Medium priority. Either rename the test or remove [font_name](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_font_properties.py:49:4-60:70) from the test parameters.

---

## test_shortening_properties.py

### Lines 44, 58, 73, 156, 173, 187, 219, 235, 252: Missing `@pytest.mark.property`
**Deviation:** Property-based tests using Hypothesis lack the `@pytest.mark.property` marker.

**Assessment:** ✅ **Legitimate and MEDIUM priority**

Looking at these lines, tests like [test_shorten_forwarded_to_heading](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_shortening_properties.py:43:4-55:70) use `@given(st.booleans())` but lack `@pytest.mark.property`. The TESTING.md line 168 requires: `@pytest.mark.property # Property-based tests using Hypothesis`.

**Recommendation:** Medium priority. Add missing markers.

### Line 325: `max_examples=2` for finite space of 4
**Deviation:** Two booleans create 4 combinations but only 2 examples used.

**Assessment:** ✅ **Legitimate and LOW priority**

Looking at lines 323-326, the test combines two booleans (4 combinations) but uses `max_examples=2`. According to TESTING.md line 660: "Product of individual strategy sizes, capped at 50."

**However**, the test has `assume(shorten1 != shorten2)` which filters out 2 of the 4 cases (True,True and False,False), leaving only 2 valid combinations.

**Recommendation:** Low priority. The `assume()` filters make `max_examples=2` actually reasonable here. The comment could be updated to explain this.

---

## test_serialization.py

### Lines 718, 754, 765: Testing private methods
**Assessment:** ✅ **Legitimate and MEDIUM priority** — similar to other private method access issues. Add justification or document as exceptions.

---

## test_sizing_behavior.py

### Line 159: Testing private [_user_size_hint_y](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_sizing_behavior.py:273:4-306:108)
**Deviation:** Accesses private `label._user_size_hint_y`.

**Assessment:** ✅ **Legitimate and MEDIUM priority**

Looking at lines 154-156, the test verifies internal state tracking:
```python
assert label._user_size_hint_y == user_size_hint_y
```

This tests an implementation detail (how user's original value is stored for restoration). The behavior could be tested via public API: toggle [auto_size_height](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_sizing_behavior.py:127:4-135:73) and verify [size_hint_y](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_sizing_behavior.py:33:4-38:70) restoration.

**Recommendation:** Medium priority. Consider testing restoration behavior instead of internal state.

### Lines 45, 110, 203, 380: Test name/assertion mismatch
**Deviation:** Names mention "height bound to minimum" but assertions only verify [size_hint_y](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_sizing_behavior.py:33:4-38:70) preconditions.

**Assessment:** ✅ **Legitimate but ACCEPTABLE**

Looking at these tests, the docstrings explain the limitation:
> "In headless testing, we verify the precondition (size_hint_y=None) rather than the computed height values which require a window for layout calculation."

The names could be more precise, but the docstrings clarify what's actually being tested. This is a practical accommodation for headless CI testing.

**Recommendation:** Low priority. Names are reasonable given the documented limitation.

### Lines 409-426: Hypothesis for trivial boolean verification
**Deviation:** Uses `@given(st.booleans())` for simple set/get verification.

**Assessment:** ✅ **Legitimate and LOW priority**

Looking at lines 409-426, these tests simply set and get a boolean property. TESTING.md lines 768-774 recommend `@pytest.mark.parametrize` for single dimension, ≤10 values.

**Recommendation:** Low priority. Could use parametrize for cleaner exhaustive coverage, but `max_examples=2` with booleans achieves the same result.

---

## test_texture_sizing.py

### Duplicated manual checks and assertions
**Deviation:** Duplicated code for child widget presence and texture_size validation.

**Assessment:** ✅ **Legitimate and LOW priority**

These could be consolidated into helper functions. However, some duplication in tests is acceptable for clarity and independence.

### Hypothesis for small finite strategies
**Assessment:** Same as test_sizing_behavior.py — could use parametrize but not strictly necessary.

---

# Summary

## High Priority Fixes (Should Fix)
1. **test_rebuild_identity_preservation.py lines 276, 338, 380, 459**: Fix incorrect `max_examples` rationale math in comments
2. **test_kivy_renderer_blocks.py**: Add `_nesting_depth` and `_render_token` to Testing Exceptions in TESTING.md or add justification comments

## Medium Priority Fixes (Recommended)
1. **test_inline_renderer.py lines 831, 848-852**: Remove direct private method calls or add justification
2. **test_kivy_renderer_blocks.py lines 225-266**: Fix test name/assertion mismatch for nested list indentation
3. **test_rebuild_identity_preservation.py line 380**: Correct [font_name](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_font_properties.py:49:4-60:70) classification (it's style-only, not structure)
4. **test_shortening_properties.py**: Add missing `@pytest.mark.property` markers
5. **test_sizing_behavior.py line 159**: Test restoration behavior instead of private [_user_size_hint_y](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_sizing_behavior.py:273:4-306:108)

## Low Priority Fixes (Optional)
1. Test naming refinements (various files)
2. Move helper imports to top of files
3. Replace Hypothesis with parametrize for trivial finite cases
4. Consolidate duplicated assertions in test_texture_sizing.py

## Acceptable/No Fix Needed
- **test_font_properties.py** helper functions using [language_info](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_kivy_renderer_blocks.py:327:4-340:84) — explicitly allowed by TESTING.md
- **test_rebuild_identity_preservation.py** [TestWidgetIdentityHelpers](cci:2://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_rebuild_identity_preservation.py:25:0-52:35) location — acceptable with `@pytest.mark.test_tests`
- **test_sizing_behavior.py** name/assertion limitations — documented headless testing accommodation