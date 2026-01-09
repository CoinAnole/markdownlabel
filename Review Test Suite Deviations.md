# Review of DEVIATIONS.md

Based on my analysis of the test files and the TESTING.md guidelines, here's my assessment of each deviation:

## test_rtl_alignment.py

### Deviation 1: Line 280 - Method name pattern

**Identified:** [test_direction_change_preserves_widget_identities](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_rtl_alignment.py:271:4-299:63) does not follow `test_*_preserves_widget_tree_*` pattern

**Verdict: ✅ LEGITIMATE - Worth Fixing (Low Priority)**

Looking at lines 280-300, the test name uses [_preserves_widget_identities](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_rtl_alignment.py:271:4-299:63) while the TESTING.md section on "Rebuild Testing Names" (lines 117-119) recommends `test_*_preserves_widget_tree_*` for tests that verify NO rebuild occurred. The test does exactly that (verifies `ids_before == ids_after`), so renaming to `test_direction_change_preserves_widget_tree` or similar would improve consistency.

### Deviation 2: Lines 477-492 - Tests private method `_get_effective_halign()`

**Identified:** Testing private method

**Verdict: ✅ LEGITIMATE - Worth Fixing (Medium Priority)**

Looking at lines 477-493, the test calls `label._get_effective_halign()` directly. Per TESTING.md's "Best Practices" (mentioned but not shown fully), tests should verify **observable behavior**, not implementation details. The private method `_get_effective_halign()` could be refactored without breaking the public API, so this test creates brittleness. The test should instead verify the effective alignment through the child Label widgets' `halign` property—which is already done in the first assertion.

---

## test_serialization.py

### Deviation 1: Line 649 - Non-standard rationale

**Identified:** `"(two complex strategies combined)"` instead of recommended rationale

**Verdict: ✅ LEGITIMATE - Worth Fixing (Low Priority)**

Looking at lines 648-649:

```python
# Complex strategy: 20 examples (two complex strategies combined)
```

Per TESTING.md (lines 675-680), the recommended format for complex strategies is `"Complex strategy: [N] examples (adequate coverage)"` or `"(performance optimized)"`. The phrase `"(two complex strategies combined)"` doesn't follow the standard rationale format. This should be either `"(adequate coverage)"` or `"(performance optimized)"`.

---

## test_shortening_properties.py

### Deviation 1: Lines 26-346 - Missing @pytest.mark.property

**Identified:** Property-based tests lack the `@pytest.mark.property` marker

**Verdict: ✅ LEGITIMATE - Worth Fixing (Medium Priority)**

Examining the file, I see tests using `@given()` decorators (lines 29, 43, 57, etc.) but missing `@pytest.mark.property`. Per TESTING.md lines 168, property-based tests with Hypothesis should have this marker to allow selective test execution.

### Deviation 2: Lines 318-346 - [test_shorten_change_triggers_rebuild](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_shortening_properties.py:314:4-345:79)

**Identified:** Test expects rebuild for style-only [shorten](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_shortening_properties.py:42:4-54:70) property, uses `force_rebuild()`, and has misleading name

**Verdict: ✅ LEGITIMATE - Worth Fixing (High Priority)**

This is a significant deviation. Looking at lines 318-346:

```python
def test_shorten_change_triggers_rebuild(self, shorten1, shorten2):
    """Changing shorten triggers widget rebuild with new value."""
    ...
    label.force_rebuild()  # Force immediate rebuild for test
    ...
    assert ids_before != ids_after, \
        "Expected widget tree rebuild when shorten property changed"
```

According to TESTING.md lines 263-268, [shorten](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_shortening_properties.py:42:4-54:70) is explicitly listed as a **style-only property** under "Truncation Properties":

> - [shorten](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_shortening_properties.py:42:4-54:70) - Updates Label.shorten on existing Labels

The test should:

1. NOT call `force_rebuild()` (per TESTING.md lines 467-475)
2. Assert `ids_before == ids_after` (no rebuild)
3. Be renamed to `test_shorten_change_preserves_widget_tree` (per naming conventions)

### Deviation 3: Lines 263-274 - Misleading test name

**Identified:** [test_empty_ellipsis_options_not_forwarded](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_shortening_properties.py:262:4-272:78) claims "not forwarded" but asserts forwarding works

**Verdict: ✅ LEGITIMATE - Worth Fixing (Low Priority)**

Looking at lines 263-274:

```python
def test_empty_ellipsis_options_not_forwarded(self):
    """Empty ellipsis_options dict is not forwarded (default behavior)."""
    ...
    for lbl in labels:
        assert lbl.ellipsis_options == {}, \
            f"Expected empty ellipsis_options, got {lbl.ellipsis_options}"
```

The test name says "not forwarded" but the assertion actually verifies that `{}` IS forwarded (and equals `{}`). More accurate would be `test_empty_ellipsis_options_forwards_default_value` or similar.

---

## test_sizing_behavior.py

### Deviations: Lines 25, 43, 97, 108, 168, 183, 201, 232, 255, 277, 346, 361, 379, 430, 453, 477, 504, 539, 563

**Identified:** Non-standard comment rationales

**Verdict: ✅ LEGITIMATE - Worth Fixing (Low Priority, Batch Fix)**

Looking at examples:

- Line 25: `"(variable-length document with complex text)"`
- Line 183: `"(two complex inputs: document + float)"`

These should use standard rationales from TESTING.md. For single complex strategies: `"(adequate coverage)"`. For combinations of two complex/infinite strategies, this is actually a valid pattern - the document + float combination is a legitimate "Complex strategy" scenario. However, the phrasing should match the template more closely.

---

## test_text_properties.py

### Deviations: Lines 272, 296, 322 - `force_rebuild()` after style-only changes

**Identified:** Using `force_rebuild()` after [text_size](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_text_properties.py:45:4-64:85) changes

**Verdict: ⚠️ BORDERLINE - Needs Investigation**

Looking at the tests:

```python
# Line 272
label.text_size = [None, height2]
label.force_rebuild()  # Force immediate rebuild for test
```

[text_size](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_text_properties.py:45:4-64:85) IS listed in TESTING.md line 271 as a style-only property:

> - [text_size](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_text_properties.py:45:4-64:85) - Updates Label.text_size on existing Labels with binding management

However, looking at the implementation context, [text_size](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_text_properties.py:45:4-64:85) changes may involve binding updates that require some processing. The tests are verifying that this property IS UPDATED (not that a rebuild occurs), and `force_rebuild()` ensures synchronous execution for test determinism. This is a **gray area** - the `force_rebuild()` may be unnecessary if the property truly updates in-place immediately.

**Recommendation:** Investigate if [text_size](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_text_properties.py:45:4-64:85) updates happen synchronously; if so, remove `force_rebuild()`.

### Deviations: Lines 421, 422, 435, 438-439 - [unicode_errors](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_text_properties.py:336:4-342:83) treated as structure property

**Identified:** Test claims [unicode_errors](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_text_properties.py:336:4-342:83) triggers rebuild

**Verdict: ✅ LEGITIMATE - Worth Fixing (High Priority)**

Looking at lines 421-445:

```python
def test_unicode_errors_change_triggers_rebuild(self, errors1, errors2):
    """Changing unicode_errors triggers widget rebuild with new value."""
    ...
    label.force_rebuild()  # Force immediate rebuild for test
    ...
    assert ids_before != ids_after, "Widget tree should rebuild for unicode_errors changes"
```

TESTING.md lines 260-261 explicitly list [unicode_errors](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_text_properties.py:336:4-342:83) as style-only:

> - [unicode_errors](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_text_properties.py:336:4-342:83) - Updates Label.unicode_errors on existing Labels

This test incorrectly expects a rebuild. Should be renamed to `test_unicode_errors_change_preserves_widget_tree` and assert `ids_before == ids_after`.

### Deviations: Lines 539, 540, 553, 556-557 - [strip](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_text_properties.py:461:4-467:62) treated as structure property

**Identified:** Test claims [strip](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_text_properties.py:461:4-467:62) triggers rebuild

**Verdict: ✅ LEGITIMATE - Worth Fixing (High Priority)**

Same issue as above. TESTING.md lines 261 lists [strip](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_text_properties.py:461:4-467:62) as style-only:

> - [strip](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_text_properties.py:461:4-467:62) - Updates Label.strip on existing Labels

The test should verify NO rebuild (preserve widget tree).

---

## test_texture_render_mode.py

### Deviations: Lines 146-149, 167, 187-193 - Accessing [_aggregated_refs](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_texture_render_mode.py:153:4-167:92)

**Identified:** Testing private attribute [_aggregated_refs](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_texture_render_mode.py:153:4-167:92)

**Verdict: ⚠️ CONTEXT-DEPENDENT - May Be Acceptable**

This is a nuanced case. The tests are verifying internal state required for texture-mode link handling. However, there's no public API to verify this behavior otherwise. Options:

1. Accept as necessary for testing texture mode internals
2. Create a public API method like `get_link_zones()` for testing

**Recommendation:** Document this as a known exception or consider exposing a test-friendly API.

### Deviations: Lines 581, 596, 610, 624, 644, 660, 673 - Calling `_get_effective_render_mode()`

**Identified:** Testing private method

**Verdict: ⚠️ CONTEXT-DEPENDENT - May Be Acceptable**

Looking at the tests, they call `label._get_effective_render_mode()` to verify the auto mode selection logic. This is similar to the previous case - without exposing this as a public API, there's no way to test the auto-selection behavior.

**Recommendation:** Consider renaming to `get_effective_render_mode()` as a public API if this is user-relevant behavior, or document the exception.

---

## test_texture_sizing.py

### Deviations: Lines 76, 93, 109, 124, 158, 253, 271, 338, 353 - Docstrings claim specific widget types but assertions don't verify

**Identified:** Claims like "creates Label widget" but no `isinstance(widget, Label)` assertion

**Verdict: ✅ LEGITIMATE - Worth Fixing (Low Priority)**

Example from lines 76-87:

```python
def test_heading_creates_label_widget(self, heading):
    """Heading content creates a Label widget that is included in texture_size calculation."""
    ...
    assert len(label.children) >= 1, ...
    # No assertion that children are Label widgets!
```

The tests verify children exist and texture_size works, but the docstrings claim "creates Label widget" or "creates BoxLayout container" without actually asserting the widget types. Either add type assertions or update docstrings to match what's actually verified.

### Deviation: Line 287 - Non-standard comment rationale

**Identified:** `"(two complex strategies combined)"`

**Verdict: ✅ LEGITIMATE - Worth Fixing (Low Priority)**

Same as the serialization file - should use standard rationale format.

---

# Summary

| Priority   | Count | Category                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| ---------- | ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **High**   | 4     | Incorrect rebuild contract tests ([unicode_errors](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_text_properties.py:336:4-342:83), [strip](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_text_properties.py:461:4-467:62), [shorten](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_shortening_properties.py:42:4-54:70)) |
| **Medium** | 3     | Missing markers, private method testing                                                                                                                                                                                                                                                                                                                                                                                                                |
| **Low**    | ~20   | Comment format, naming conventions, docstring accuracy                                                                                                                                                                                                                                                                                                                                                                                                 |

## Recommended Fix Order

1. **High Priority:** Fix the tests that incorrectly expect rebuilds for style-only properties ([shorten](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_shortening_properties.py:42:4-54:70), [unicode_errors](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_text_properties.py:336:4-342:83), [strip](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_text_properties.py:461:4-467:62)). This represents incorrect test semantics.

2. **Medium Priority:** Add missing `@pytest.mark.property` markers to enable proper test categorization.

3. **Low Priority:** Batch-update comment rationales to match the standard format (can be automated with the standardization tools mentioned in TESTING.md).

4. **Consider:** Whether to expose `_get_effective_render_mode()` and similar methods as public APIs for testing, or document them as acceptable testing exceptions.