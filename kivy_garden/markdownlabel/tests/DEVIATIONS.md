# Test Suite Deviations Analysis

This document analyzes potential deviations from the testing guidelines in `TESTING.md`. After careful review, many reported "deviations" are actually acceptable patterns or misunderstandings of the guidelines.

## Analysis Categories

- **ACTUAL DEVIATIONS**: Clear violations of documented guidelines that should be fixed
- **DEBATABLE**: Patterns that could be improved but aren't clear violations
- **NOT ACTUAL DEVIATIONS**: Reported issues that are actually correct or acceptable patterns
- **VALID SUGGESTIONS**: Coverage gaps or quality improvements (not guideline violations)
- **MINOR**: Small issues that don't significantly impact code quality

## Critical Clarification: Rebuild Testing Helpers

The original deviation list incorrectly stated that `assert_rebuild_occurred()` and `assert_no_rebuild()` take a `change_func` parameter. **This is wrong.** The actual signatures are:

```python
def assert_rebuild_occurred(widget: Widget, ids_before: Dict[int, Widget], exclude_root: bool = True)
def assert_no_rebuild(widget: Widget, ids_before: Dict[int, Widget], exclude_root: bool = True)
```

These helpers require manual ID collection before the change. The current test patterns using manual `collect_widget_ids()` calls are CORRECT and follow the documented approach in TESTING.md.

---

## test_import.py

**OPINION: NOT ACTUAL DEVIATIONS** - This is a basic smoke test file for import functionality. The guidelines encourage property-based testing but don't mandate it for all tests. Simple import tests are appropriate as unit tests without Hypothesis. The class organization is reasonable for a small import test file.

- ~~Line 9: Class name issue~~ - **NOT A DEVIATION**: The class tests import-related functionality. Having a few basic property checks in the same class is reasonable for a smoke test.
- ~~Line 12-16: Test naming issue~~ - **NOT A DEVIATION**: The test name is acceptable. It tests that import works and the object has expected attributes.
- ~~Line 18-22: Test naming issue~~ - **NOT A DEVIATION**: The name `test_markdownlabel_text_property` is clear enough for a basic property test.
- ~~No property-based testing~~ - **NOT A DEVIATION**: Import tests are appropriately simple unit tests. Not everything needs Hypothesis.

## test_inline_renderer.py

**ACTUAL DEVIATIONS:**

- **Line 15-73: Custom strategies defined in test file** - VALID DEVIATION: These token-generating strategies are specific to testing InlineRenderer and mistune token structures. They could be moved to test_utils.py if reused elsewhere, but keeping them local is acceptable for renderer-specific test data.
- **Line 205-207: Incorrect strategy classification** - VALID DEVIATION: `st.text(alphabet='[]&', min_size=1, max_size=50)` is indeed a complex/infinite strategy (3^50 combinations), not "Medium finite". Should be "Complex strategy".
- **Line 401-411, 657-676: st.one_of misclassification** - DEBATABLE: `st.one_of` combining text patterns is technically a combination, but since the underlying strategies are complex/infinite, "Complex strategy" is more accurate than "Combination strategy".
- **Line 760-762: Large max_size strategy** - MINOR: The classification is acceptable, though the rationale could be more specific about the large character space.

**NOT DEVIATIONS:**

- ~~Line 84, 96, 108, etc.: Identical max_examples=20~~ - NOT A DEVIATION: If these are all genuinely complex strategies, using the same max_examples is appropriate. The comment format is standardized.

## test_kivy_renderer.py

**ACTUAL DEVIATIONS:**

- **Line 38-40: Incorrect input space size** - VALID DEVIATION: If heading levels are 1-6 (6 values) but the strategy uses 1-5, this is a bug. Either the strategy or the comment needs correction.
- **Line 83-85: Mixed finite/infinite misclassification** - VALID DEVIATION: Combining finite integers with infinite floats should be "Complex strategy", not "Combination strategy".
- **Line 997-1011: Duplicate test** - VALID DEVIATION: If this test truly duplicates existing coverage, it should be removed.

**DEBATABLE:**

- **Line 776-1083: TestKivyRendererEdgeCases class organization** - DEBATABLE: While the guideline says "one class per property/behavior", having a catch-all "edge cases" class for miscellaneous renderer edge cases is a common and reasonable pattern. These are implementation-detail tests that don't fit neatly into property-based categories. Splitting into 9+ tiny classes might be over-engineering. However, if the class is hard to navigate, splitting could help.

## test_core_functionality.py

**NOT ACTUAL DEVIATIONS:**

- ~~Line 111-126, 178-195: Test naming issues~~ - **OPINION: ACCEPTABLE**: These test names are reasonable. Testing that "text change updates widgets" or "AST updates with text" are valid descriptions even if the assertion is simplified. Perfect naming is subjective.
- ~~Line 111-195: Not using rebuild helpers~~ - **INCORRECT DEVIATION**: The TESTING.md shows that `assert_rebuild_occurred()` and `assert_no_rebuild()` require `ids_before` to be collected manually first - they don't take a `change_func` parameter. The current manual approach IS the correct pattern. These helpers don't simplify the code as much as implied.
- ~~Line 217-226, 239-246, 262-269: Manual widget traversal~~ - **ACCEPTABLE**: While `find_labels_recursive()` exists, sometimes manual traversal with specific logic is clearer for the test's intent. Using helpers is encouraged but not mandatory for all cases.

## test_font_properties.py

**ACTUAL DEVIATIONS:**

- **Line 27: Custom strategy in test file** - MINOR DEVIATION: `line_height_strategy` could be moved to test_utils.py if reused elsewhere, but a single local strategy is acceptable.
- **Lines 319-337, 339-343, 529-542: Custom helper methods** - VALID DEVIATION: These helpers (`_find_code_block_labels`, `_find_non_code_labels`, `collect_labels_and_scales`) should be in test_utils.py if they're useful for other tests. If they're truly specific to font property tests, keeping them local is acceptable.

**NOT ACTUAL DEVIATIONS:**

- ~~Line 111, 226: Test naming with force_rebuild()~~ - **INCORRECT DEVIATION**: The TESTING.md explicitly documents that `force_rebuild()` is the correct approach for testing deferred rebuilds. The test name "triggers_rebuild" is accurate - the property change DOES trigger a rebuild (deferred), and `force_rebuild()` is called to make it synchronous for testing. This is the documented pattern.
- ~~Line 125, 242: Manual force_rebuild() instead of helpers~~ - **INCORRECT DEVIATION**: The helper functions `assert_rebuild_occurred()` and `assert_no_rebuild()` don't eliminate the need for `force_rebuild()`. They still require manual ID collection before/after. The current pattern is correct per TESTING.md.
- ~~Lines 578-583, 616-620, etc.: Manual widget traversal~~ - **ACCEPTABLE**: Using `find_labels_recursive()` is encouraged but not mandatory. Sometimes custom traversal logic is clearer.
- ~~Lines 111-135, 226-252, 789-810, etc.: Manual ID comparison~~ - **INCORRECT DEVIATION**: The helpers don't take a `change_func` - they require manual ID collection. The current approach IS correct.

## test_color_properties.py

**DEBATABLE:**

- **Line 24-180: Class organization** - DEBATABLE: `TestColorPropertyForwarding` testing multiple color-related behaviors is reasonable. The behaviors are all related to color forwarding. Splitting into 4+ classes might be over-engineering unless the class is hard to navigate.

**VALID SUGGESTION (not a deviation):**

- **Line 82-100: Missing rebuild preservation test** - VALID SUGGESTION: Adding a test to verify that color changes preserve the widget tree (no rebuild) would strengthen the rebuild contract testing. This is a gap in coverage, not a deviation from guidelines.

## test_text_properties.py

**NOT ACTUAL DEVIATIONS:**

- ~~Line 259-277, 435-461, 577-603: Manual ID collection~~ - **INCORRECT DEVIATION**: The helper functions require manual ID collection anyway. The pattern shown is correct. The helpers `assert_rebuild_occurred()` and `assert_no_rebuild()` take `ids_before` as a parameter - they don't eliminate the manual collection step.

## test_sizing_behavior.py

**VALID SUGGESTIONS (not deviations):**

- **Line 515-529: Test naming and coverage** - VALID SUGGESTION: The test name could be more precise, and adding rebuild verification would improve coverage. However, this is a gap in test quality, not a deviation from guidelines.
- **Line 207-314, 320-555: Missing rebuild contract tests** - VALID SUGGESTION: Adding rebuild contract verification would strengthen the test suite. This is a coverage gap, not a guideline deviation.

## test_advanced_compatibility.py

**VALID SUGGESTIONS (not deviations):**

- **Line 689-708, 716-735: Missing rebuild verification** - VALID SUGGESTION: Adding widget tree preservation checks would improve rebuild contract testing. This is a coverage gap, not a guideline deviation.
- **Line 834-852: Test naming** - MINOR: The name is acceptable but could be more precise.

**NOT ACTUAL DEVIATIONS:**

- ~~Line 155-181, 187-213, etc.: Manual ID collection~~ - **INCORRECT DEVIATION**: The helpers require manual ID collection. The current pattern is correct and matches the documented approach in TESTING.md.

## test_serialization.py

**ACTUAL DEVIATIONS:**

- **Line 27-77: Custom helper methods** - VALID DEVIATION: `_normalize_ast` and `_merge_adjacent_text` are serialization-specific helpers. If they're only used in this test file, keeping them local is acceptable. If they could be useful elsewhere, move to test_utils.py.
- **Line 613-620: Incorrect strategy classification** - VALID DEVIATION: Combining two complex/infinite text strategies should be "Complex strategy", not "Combination strategy".

## test_performance.py

**ACTUAL DEVIATIONS:**

- **Line 30-33, 55-57, 77-79, 279-287: Incorrect strategy classifications** - VALID DEVIATION: All of these misclassify complex/infinite strategies (floats, RGBA colors) as "Combination strategy". They should be "Complex strategy" since they involve continuous ranges, not finite combinations.

## test_rebuild_semantics.py

**ACTUAL DEVIATIONS:**

- **Multiple strategy misclassifications** - VALID DEVIATION: Lines 245-258, 420-430, 652-657, 695-700, 737-742, 784-796, 829-838, 872-881 all incorrectly classify strategies that combine complex/infinite strategies with finite strategies. When ANY strategy in a combination is complex/infinite, the overall classification should be "Complex strategy", not "Combination strategy" or "Small finite strategy".

**NOT ACTUAL DEVIATIONS:**

- ~~Line 503-643: Manual ID collection in rebuild tests~~ - **INCORRECT DEVIATION**: The helpers require manual ID collection. The current pattern is correct.
- ~~Line 88-209: Manual ID collection in preservation tests~~ - **INCORRECT DEVIATION**: The helpers require manual ID collection. The current pattern is correct.

## test_shortening_and_coordinate.py

**MINOR ISSUE:**

- **Line 331: Test naming** - MINOR: The name `test_shorten_change_updates_value` could be more precise if it's testing rebuild behavior. However, if the test primarily verifies value updates (with rebuild as a side effect), the name is acceptable.

## test_texture_render_mode.py

**ACTUAL DEVIATIONS:**

- **Line 26: Unused import** - VALID DEVIATION: Importing unused functions creates unnecessary dependencies. Should be removed.
- **Line 216-231, 319-333: Incorrect strategy classifications** - VALID DEVIATION: Combining continuous float ranges and regex patterns should be "Complex strategy", not "Combination strategy".

## test_texture_sizing.py

**DEBATABLE:**

- **Line 28-356: Class organization** - DEBATABLE: `TestComprehensiveTextureSizeCalculation` is a large class testing many texture_size behaviors. The guideline "one class per property/behavior" suggests splitting, but for a comprehensive test of a single method (`texture_size`), having one large class is defensible. Consider splitting if navigation becomes difficult.

**VALID SUGGESTION:**

- **Line 269-293: Missing rebuild verification** - VALID SUGGESTION: The test uses `force_rebuild()` but doesn't verify that a rebuild occurred. Adding rebuild verification would improve test quality. This is a coverage gap, not a guideline deviation.

## meta_tests/test_assertion_analyzer.py

**ACTUAL DEVIATIONS:**

- **Line 95-99, 142-155: Custom strategies in test file** - MINOR DEVIATION: These strategies are specific to testing the assertion analyzer. If they're only used here, keeping them local is acceptable. If reused elsewhere, move to test_utils.py.
- **Line 156-157: Incorrect strategy classification** - VALID DEVIATION: Combining finite `sampled_from` with complex/infinite text generation should be "Complex strategy", not "Combination strategy".

---

## Summary

**Key Findings:**

1. **MAJOR MISUNDERSTANDING**: Many "deviations" incorrectly claim tests should use `assert_rebuild_occurred(widget, change_func)` and `assert_no_rebuild(widget, change_func)`. The actual signatures are `assert_rebuild_occurred(widget, ids_before)` and `assert_no_rebuild(widget, ids_before)` - they require manual ID collection first. The current test patterns are CORRECT.

2. **VALID STRATEGY CLASSIFICATION ISSUES**: Many tests incorrectly classify strategies that combine complex/infinite strategies (floats, text, colors) with finite strategies as "Combination strategy". The rule is: if ANY strategy in the combination is complex/infinite, use "Complex strategy" classification.

3. **ACCEPTABLE PATTERNS**: 
   - Local helper functions specific to one test file are acceptable
   - Large "comprehensive" or "edge cases" classes are debatable but not clear violations
   - Manual widget traversal is acceptable when `find_labels_recursive()` doesn't fit the use case
   - Using `force_rebuild()` in tests is the CORRECT documented pattern

4. **COVERAGE GAPS vs DEVIATIONS**: Many items are suggestions for improving test coverage (adding rebuild verification, better naming) rather than actual deviations from guidelines.

**Recommendation**: Focus on fixing the strategy classification issues. The other items are mostly acceptable patterns or coverage improvement suggestions rather than guideline violations.
