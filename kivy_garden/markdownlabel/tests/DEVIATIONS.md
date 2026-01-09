# Test Suite Deviations from TESTING.md Guidelines

Files not listed have no deviations.

## Remaining Deviations (Post-Guideline Update)

After the TESTING.md updates, the following items remain as actual deviations:

### test_inline_renderer.py
- Lines 827-831: The test `test_unknown_token_type` already tests via public API (`renderer.render([token])`), then redundantly calls `renderer._unknown(token)` directly. The direct call on line 831 is unnecessary and could be removed.

### test_kivy_renderer_blocks.py
- Lines 225-266: Test name `test_nested_list_increases_indentation` claims verification of increasing padding per nesting level, but assertions only check fixed outer list padding. Either fix the test or rename to `test_nested_list_has_left_padding`.

### test_rebuild_identity_preservation.py
- Line 276: Comment says "120 finite × 5 complex samples" but 120×5=600 ≠ 50 (the actual max_examples)
- Line 338: Comment says "24 finite × 4 complex samples" but 24×4=96 ≠ 50
- Line 380: Comment says "24 finite × 2 complex samples" but the finite product is 8, not 24; also `font_name` should be removed since it's style-only (not structure)
- Line 459: Comment says "3 finite × 5 complex samples" but both strategies appear complex

### test_shortening_properties.py
- Lines 44, 58, 73, 187, 219, 235, 252: Missing `@pytest.mark.property` marker on property-based tests using Hypothesis

### test_sizing_behavior.py
- Lines 154-156: Test accesses private `label._user_size_hint_y` to verify internal state. Consider testing the observable restoration behavior (toggle auto_size_height and verify size_hint_y restores correctly) instead.

## Resolved Deviations (Now Acceptable)

The following items from the original DEVIATIONS.md are now acceptable per the updated guidelines:

### test_color_properties.py
- ✅ Line 82: Hybrid test name `test_color_change_updates_value_without_rebuild` is now explicitly allowed.

### test_font_properties.py
- ✅ Lines 317-342: `language_info` is a documented public attribute, not an implementation detail.
- ✅ Lines 570, 640, 680, 726: `HEADING_SIZES` is a public constant; imports inside test methods are unusual but not prohibited.
- ✅ Lines 598-604, 800-807, 815-822: Manual widget traversal is acceptable per guidelines.

### test_inline_renderer.py
- ✅ Lines 848-852: Edge case tests for `_escape_markup` are now acceptable under "Coverage-Focused Tests" guidance, though could add comment explaining why.

### test_kivy_renderer_blocks.py
- ✅ Lines 477-569: `TestDeepNestingTruncation` accessing `_nesting_depth` and `_render_token` is now acceptable under "Coverage-Focused Tests" since it tests behavior not easily triggered through public API and has clear requirement references in docstrings.
- ✅ Lines 582-684, 706-718: `TestKivyRendererEdgeCases` accessing private methods for coverage is acceptable.

### test_kivy_renderer_tables.py
- ✅ Lines 150, 221, 235-239, 198-208: Coverage-focused edge case tests are acceptable.

### test_padding_properties.py
- ✅ Lines 390-546: Class names being slightly imprecise is acceptable per "test naming should be clear, but perfect naming is subjective."

### test_rebuild_identity_preservation.py
- ✅ Lines 26-55: Meta-tests for helpers in the same file is acceptable with `@pytest.mark.test_tests`.

### test_serialization.py
- ✅ Lines 718, 754, 765: Coverage-focused tests may access private methods when justified.

### test_sizing_behavior.py
- ✅ Lines 45, 110, 203, 380: Docstrings explain the headless testing limitation; names are acceptable given that context.
- ✅ Lines 409-426: Hypothesis for boolean properties is acceptable (both approaches are valid for small finite cases).

### test_texture_sizing.py
- ✅ Duplicated assertions and using Hypothesis for finite cases are acceptable.
- ✅ Lines 197-202, 350-355: Hypothesis is acceptable for small finite cases.

### test_shortening_properties.py
- ✅ Line 325: `max_examples=2` is correct because `assume(shorten1 != shorten2)` filters to 2 valid combinations.
