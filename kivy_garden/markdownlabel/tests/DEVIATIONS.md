# Deviations

## test_advanced_compatibility.py

- Line 35: Comment uses "Complex strategy" but strategy is `st.text()` with constrained alphabet (line 31-34). While text strategies are typically complex, this specific instance has a constrained input space. Should use "Complex strategy" or consider if constraints make it finite.
- Line 52: Comment uses "Complex strategy" but strategy is `st.text()` with constrained alphabet (line 48-51). Same issue as line 35.
- Line 69: Comment uses "Complex strategy" but strategy is `st.text()` with constrained alphabet (line 65-68). Same issue as line 35.
- Line 267: Comment uses "Complex strategy" but strategy is `st.lists(st.floats())` for RGBA colors (line 263-266). While correct classification, the comment format should be consistent.
- Line 280: Comment uses "Complex strategy" but strategy is `st.lists(st.floats())` for RGBA colors (line 276-279). Same issue as line 267.
- Line 307: Comment uses "Complex strategy" but strategy is `st.lists(st.floats())` for RGBA colors (line 303-306). Same issue as line 267.
- Line 535: Comment uses "Complex strategy" but strategy combines two complex strategies (rebuild_colors, rebuild_colors) (line 534). According to guidelines, when combining two complex strategies, it should still be "Complex strategy" or potentially "Combination strategy" if they were finite. The comment is technically correct but could be clearer.
- Line 573: Comment uses "Complex strategy" but strategy combines two complex strategies (rebuild_line_heights, rebuild_line_heights) (line 572). Same issue as line 535.
- Line 611: Comment uses "Complex strategy" but strategy combines two complex strategies (rebuild_text_size_widths, rebuild_text_size_widths) (line 610). Same issue as line 535.
- Line 735: Test name is `test_unicode_errors_updates_value` but the test calls `force_rebuild()` (line 748) and verifies rebuild behavior. According to guidelines, tests that verify rebuilds should use `test_*_triggers_rebuild_*` naming pattern. The current name suggests a value update without rebuild verification, but the test actually verifies rebuild behavior.
- Line 735-755: The test `test_unicode_errors_updates_value` has a name that doesn't match its assertions. The test name uses "updates_value" pattern (for no rebuild tests) but the test calls `force_rebuild()` and verifies widgets were rebuilt with new value. This should either be renamed to `test_unicode_errors_change_triggers_rebuild` or the test should be modified to not call `force_rebuild()` if it's truly a style-only property.
- Line 786: Test name is `test_disabled_change_triggers_rebuild` but the test does NOT verify rebuild occurred. It only verifies the color value changed (lines 814-819). According to guidelines, tests with "triggers_rebuild" in the name must verify rebuild occurred using `collect_widget_ids()` and comparison or `assert_rebuild_occurred()`. The current test only checks that the color value changed, not that the widget tree was rebuilt.
- Line 786-819: The test `test_disabled_change_triggers_rebuild` claims to test rebuild behavior but doesn't verify it. The test should either be renamed to `test_disabled_change_updates_value` (if disabled is a style-only property) or should be modified to actually verify rebuild occurred by collecting widget IDs before and after the change.
- Line 822: Comment uses "Mixed finite/complex strategy" but calculates "90 finite × ~0.2 complex samples" which doesn't make sense. The calculation should be `finite_size × samples_per_value` where samples_per_value is a reasonable number like 5-10. Having "~0.2 complex samples" is not meaningful.
- Line 822: The comment calculation "90 finite × ~0.2 complex samples" is incorrect. The strategy is `simple_markdown_document(), rebuild_font_names, rebuild_font_names` where `simple_markdown_document()` is complex and `rebuild_font_names` is small finite (3 values). The correct calculation should be something like "3 finite × ~7 complex samples" to get 20 examples, not "90 finite × ~0.2 complex samples".
- Line 847: Test name is `test_font_kerning_updates_value` but the test calls `force_rebuild()` (line 861) and verifies rebuild behavior. According to guidelines, tests that verify rebuilds should use `test_*_triggers_rebuild_*` naming pattern. The current name suggests a value update without rebuild verification, but the test actually verifies rebuild behavior.
- Line 847-868: The test `test_font_kerning_updates_value` has a name that doesn't match its assertions. The test name uses "updates_value" pattern (for no rebuild tests) but the test calls `force_rebuild()` and verifies widgets were rebuilt with new value. This should either be renamed to `test_font_kerning_change_triggers_rebuild` or the test should be modified to not call `force_rebuild()` if it's truly a style-only property.
- Line 873: Test name is `test_font_blended_updates_value` but the test calls `force_rebuild()` (line 887) and verifies rebuild behavior. According to guidelines, tests that verify rebuilds should use `test_*_triggers_rebuild_*` naming pattern. The current name suggests a value update without rebuild verification, but the test actually verifies rebuild behavior.
- Line 873-894: The test `test_font_blended_updates_value` has a name that doesn't match its assertions. The test name uses "updates_value" pattern (for no rebuild tests) but the test calls `force_rebuild()` and verifies widgets were rebuilt with new value. This should either be renamed to `test_font_blended_change_triggers_rebuild` or the test should be modified to not call `force_rebuild()` if it's truly a style-only property.

## test_clipping_behavior.py

- Line 91-96: Manual StencilView traversal code is duplicated from test_utils.py's has_clipping_container() helper. The test manually iterates through children to find StencilView instead of using the available helper function.
- Line 133-137: Manual StencilView traversal code is duplicated. Same issue as lines 91-96.
- Line 216-218: Manual StencilView traversal code is duplicated. Same issue as lines 91-96.

## test_color_properties.py

No deviations found

## test_core_functionality.py

- Line 116: Test name is `test_text_change_updates_widgets` but the test does NOT verify rebuild occurred. The test only checks that `label.text == text2` (line 130). According to guidelines, tests that change structure properties like `text` should verify rebuild behavior using `collect_widget_ids()` and comparison or `assert_rebuild_occurred()`. The current test only verifies the text value changed, not that the widget tree was rebuilt.
- Line 116-131: The test `test_text_change_updates_widgets` changes the `text` property (a structure property that triggers rebuilds) but doesn't verify the rebuild occurred. The test should either be renamed to `test_text_change_updates_value` (if it's only testing value changes) or should be modified to actually verify rebuild occurred by collecting widget IDs before and after the change and using `assert_rebuild_occurred()`.
- Line 138: Test name is `test_different_block_counts_update_correctly` but the test calls `force_rebuild()` (line 153) yet does NOT verify rebuild occurred. It only verifies `children_after >= count2` (line 158). According to guidelines, tests with "update_correctly" in the name that call `force_rebuild()` should verify rebuild behavior using `collect_widget_ids()` and comparison or `assert_rebuild_occurred()`. The current test only checks the child count changed, not that the widget tree was rebuilt.
- Line 138-159: The test `test_different_block_counts_update_correctly` changes the `text` property and calls `force_rebuild()` but doesn't verify the rebuild occurred. The test should either be modified to verify rebuild occurred by collecting widget IDs before and after the change, or the test name should be changed to reflect that it only tests value updates (not rebuild behavior).
- Line 166: Test name is `test_clear_text_removes_widgets` but the test calls `force_rebuild()` (line 176) yet does NOT verify rebuild occurred. It only verifies `len(label.children) == 0` (line 178). According to guidelines, tests that call `force_rebuild()` should verify rebuild behavior using `collect_widget_ids()` and comparison or `assert_rebuild_occurred()`. The current test only checks the child count is zero, not that the widget tree was rebuilt.
- Line 166-179: The test `test_clear_text_removes_widgets` changes the `text` property to empty and calls `force_rebuild()` but doesn't verify the rebuild occurred. The test should be modified to verify rebuild occurred by collecting widget IDs before and after the change and using `assert_rebuild_occurred()`.
- Line 186: Test name is `test_ast_updates_with_text` but the test calls `force_rebuild()` (line 196) yet does NOT verify rebuild occurred. It only verifies `label.text == text2` (line 203). According to guidelines, tests that call `force_rebuild()` should verify rebuild behavior using `collect_widget_ids()` and comparison or `assert_rebuild_occurred()`. The current test only checks the text value changed, not that the widget tree was rebuilt.
- Line 186-204: The test `test_ast_updates_with_text` changes the `text` property and calls `force_rebuild()` but doesn't verify the rebuild occurred. The test should either be modified to verify rebuild occurred by collecting widget IDs before and after the change, or the test name should be changed to reflect that it only tests value updates (not rebuild behavior).
- Line 135: Comment uses "Combination strategy" but the strategy combines two small finite strategies (both `st.integers(min_value=1, max_value=3)`). According to guidelines, this is correctly classified as "Combination strategy" for all finite strategies, which is correct.
- Line 135-137: The comment "Combination strategy: 9 examples (combination coverage)" is correct for two small finite strategies with 3 values each (3 × 3 = 9).
- Line 237: Comment uses "Complex strategy" but the strategy is `st_alphanumeric_text(min_size=1, max_size=20)` which is a complex strategy (text with constrained alphabet). This is correctly classified.
- Line 237-239: The comment "Complex strategy: 20 examples (adequate coverage)" is correct for a text-based strategy.
- Line 258: Comment uses "Complex strategy" but the strategy is `st.from_regex()` which generates URLs from a regex pattern. This is correctly classified as a complex strategy.
- Line 258-260: The comment "Complex strategy: 20 examples (adequate coverage)" is correct for a regex-based strategy.
- Line 288: Comment uses "Medium finite strategy" but the strategy is `st.integers(min_value=1, max_value=15)` which has 15 values. According to guidelines, integer ranges with 11-50 values are "Medium finite strategies", so this is correctly classified.
- Line 288-290: The comment "Medium finite strategy: 20 examples (adequate finite coverage)" is correct. The strategy has 15 possible values (input space size), but the test uses 20 examples which is more than the input space. This is acceptable as "adequate finite coverage" but could be optimized to use 15 examples to match the input space size exactly.
- Line 307: Comment uses "Medium finite strategy" but the strategy is `st.integers(min_value=1, max_value=15)` with 15 values. Same issue as line 288 - correctly classified but could be optimized to 15 examples.
- Line 307-309: The comment "Medium finite strategy: 20 examples (adequate finite coverage)" is correct but could be optimized to 15 examples to match the input space size exactly.
- Line 325: Comment uses "Medium finite strategy" but the strategy is `st.integers(min_value=1, max_value=15)` with 15 values. Same issue as line 288 - correctly classified but could be optimized to 15 examples.
- Line 325-327: The comment "Medium finite strategy: 20 examples (adequate finite coverage)" is correct but could be optimized to 15 examples to match the input space size exactly.
- Line 227-231: Manual widget traversal code to find Labels with ref markup. The test manually iterates through `label.children` to find Labels with `[ref=` and `[/ref]` in their text. According to guidelines, this should use the `find_labels_with_ref_markup()` helper from test_utils.py instead of duplicating the traversal logic.
- Line 248-253: Manual widget traversal code to find Labels with ref markup. Same issue as lines 227-231 - should use `find_labels_with_ref_markup()` helper.
- Line 272-276: Manual widget traversal code to find Labels with ref markup. Same issue as lines 227-231 - should use `find_labels_with_ref_markup()` helper.

## test_font_properties.py

No deviations found

## test_inline_renderer.py

No deviations found

## test_kivy_renderer.py

No deviations found

## test_label_compatibility.py

- Line 155-156: Comment says "32 finite × 2 complex samples" but max_examples=50. The calculation 32 × 2 = 64 doesn't match the actual max_examples value of 50. The comment calculation should match the actual max_examples value.
- Line 291-292: Comment says "10 finite × 5 complex samples" but max_examples=50. The strategy combines multiple complex dimensions (floats, RGBA color, text, dictionaries) with finite dimensions (boolean, sampled_from). The comment oversimplifies by suggesting only 5 samples from the complex space, but there are multiple complex dimensions being sampled, not just one. The comment should either be "Complex strategy: 50 examples (adequate coverage)" or accurately reflect the multi-dimensional nature of the complex sampling.
- Line 375-376: Comment says "10 finite × 2 complex samples" but max_examples=20. Similar to line 291, the strategy combines multiple complex dimensions (floats, RGBA color, text, dictionaries, markdown) with finite dimensions (boolean, sampled_from). The comment oversimplifies by suggesting only 2 samples from the complex space, but there are multiple complex dimensions being sampled. The comment should either be "Complex strategy: 20 examples (adequate coverage)" or accurately reflect the multi-dimensional nature of the complex sampling.

## test_padding_properties.py

No deviations found

## test_performance.py

- Line 238: Test name is `test_text_structure_property_rebuilds_tree` but according to guidelines, tests that verify rebuilds should use `test_*_triggers_rebuild_*` naming pattern. The current name uses "rebuilds_tree" which is not one of the standard patterns. This should be renamed to `test_text_change_triggers_rebuild` to follow the naming convention.
- Line 238-257: The test `test_text_structure_property_rebuilds_tree` correctly verifies rebuild behavior using `collect_widget_ids()` and comparison, but the test name doesn't follow the standard `test_*_triggers_rebuild_*` pattern. The test implementation is correct, only the naming needs to be updated.
- Line 259: Test name is `test_font_name_structure_property_rebuilds_tree` but according to guidelines, tests that verify rebuilds should use `test_*_triggers_rebuild_*` naming pattern. The current name uses "rebuilds_tree" which is not one of the standard patterns. This should be renamed to `test_font_name_change_triggers_rebuild` to follow the naming convention.
- Line 259-277: The test `test_font_name_structure_property_rebuilds_tree` correctly verifies rebuild behavior using `collect_widget_ids()` and comparison, but the test name doesn't follow the standard `test_*_triggers_rebuild_*` pattern. The test implementation is correct, only the naming needs to be updated.
- Line 286: Comment says "Mixed finite/complex strategy: 20 examples (9 finite × ~2 complex samples)" but the strategy combines multiple complex dimensions (st_font_size, st_rgba_color, st.floats) with finite dimensions (two sampled_from with 3 values each). The comment oversimplifies by suggesting only one complex dimension when there are actually multiple complex dimensions being sampled. The comment should be "Complex strategy: 20 examples (adequate coverage)" to accurately reflect that this is a multi-dimensional complex strategy, not a simple finite × complex combination.

## test_rebuild_scheduling.py

- Line 34: Test name is `test_multiple_text_changes_batch_to_single_rebuild` but according to guidelines, tests that verify rebuilds should use `test_*_triggers_rebuild_*` naming pattern. The test calls `force_rebuild()` and verifies that widgets changed after force_rebuild() (lines 62-64). The current name doesn't follow the standard naming convention.
- Line 34-64: The test `test_multiple_text_changes_batch_to_single_rebuild` correctly verifies rebuild behavior using `collect_widget_ids()` and manual comparison, but the test name doesn't follow the standard `test_*_triggers_rebuild_*` pattern. The test implementation is correct, only the naming needs to be updated.
- Line 71: Comment says "Mixed finite/complex strategy: 15 examples (2 finite × 8 complex samples)" but the calculation 2 × 8 = 16 doesn't match the actual max_examples value of 15. According to guidelines, the comment calculation should match the actual max_examples value. The correct calculation should be "2 finite × 7.5 complex samples" which is not meaningful, or max_examples should be adjusted to 16 to match the comment.
- Line 71: The comment calculation "2 finite × 8 complex samples" is incorrect. The strategy combines st_alphanumeric_text (complex), st_font_size (complex), and st_font_name with 2 values (finite). With max_examples=15, the calculation doesn't work out evenly (15/2 = 7.5). The comment should either be adjusted to "2 finite × 7-8 complex samples" or max_examples should be adjusted to 16 for a clean calculation.
- Line 73: Test name is `test_mixed_property_changes_batch_rebuilds` but according to guidelines, tests that verify rebuilds should use `test_*_triggers_rebuild_*` naming pattern. The test calls `force_rebuild()` and verifies that widgets changed after force_rebuild() (lines 102-104). The current name doesn't follow the standard naming convention.
- Line 73-104: The test `test_mixed_property_changes_batch_rebuilds` correctly verifies rebuild behavior using `collect_widget_ids()` and manual comparison, but the test name doesn't follow the standard `test_*_triggers_rebuild_*` pattern. The test implementation is correct, only the naming needs to be updated.
- Line 121: Test name is `test_text_change_schedules_deferred_rebuild` but according to guidelines, tests that verify rebuilds should use `test_*_triggers_rebuild_*` naming pattern. The test calls `force_rebuild()` and verifies that widgets changed after force_rebuild() (lines 149-151). While the test is specifically testing the deferred scheduling mechanism, it still verifies that a rebuild occurs after forcing, so the naming should follow the standard convention.
- Line 121-151: The test `test_text_change_schedules_deferred_rebuild` correctly verifies rebuild behavior using `collect_widget_ids()` and manual comparison. The test is specifically testing the deferred scheduling mechanism (that widgets don't change immediately but do after force_rebuild), which is a valid test scenario. However, the test name doesn't follow the standard `test_*_triggers_rebuild_*` pattern. Consider renaming to `test_text_change_triggers_deferred_rebuild` to better match the naming convention while preserving the intent.
- Line 154: Test name is `test_font_name_change_schedules_deferred_rebuild` but according to guidelines, tests that verify rebuilds should use `test_*_triggers_rebuild_*` naming pattern. The test calls `force_rebuild()` and verifies that widgets changed after force_rebuild() (lines 184-186). Similar to line 121, the test is specifically testing the deferred scheduling mechanism but should still follow the naming convention.
- Line 154-186: The test `test_font_name_change_schedules_deferred_rebuild` correctly verifies rebuild behavior using `collect_widget_ids()` and manual comparison. The test is specifically testing the deferred scheduling mechanism, which is a valid test scenario. However, the test name doesn't follow the standard `test_*_triggers_rebuild_*` pattern. Consider renaming to `test_font_name_change_triggers_deferred_rebuild` to better match the naming convention while preserving the intent.
- Line 228: Test name is `test_multiple_changes_all_deferred` but according to guidelines, tests that verify rebuilds should use `test_*_triggers_rebuild_*` naming pattern. The test calls `force_rebuild()` and verifies that widgets changed after force_rebuild() (lines 256-258). The current name doesn't follow the standard naming convention.
- Line 228-258: The test `test_multiple_changes_all_deferred` correctly verifies rebuild behavior using `collect_widget_ids()` and manual comparison. The test is specifically testing that multiple changes are all deferred (widgets don't change until force_rebuild()), which is a valid test scenario. However, the test name doesn't follow the standard `test_*_triggers_rebuild_*` pattern. Consider renaming to `test_multiple_changes_trigger_deferred_rebuild` to better match the naming convention while preserving the intent.

## test_rebuild_semantics.py

No deviations found

## test_rtl_alignment.py

No deviations found

## test_serialization.py

- Line 648: Comment uses "Complex strategy" but the strategy combines two complex strategies (st.text() and st.text() with constrained alphabet). According to guidelines, when combining multiple complex strategies (all infinite/complex), the classification should still be "Complex strategy" but the rationale should accurately reflect that multiple complex dimensions are being sampled, not "two complex strategies combined" which suggests a different classification. The comment should be "Complex strategy: 20 examples (adequate coverage)" to accurately reflect that this is a multi-dimensional complex strategy.
