# Deviations from TESTING.md Guidelines

## test_core_functionality.py
- Line 56: Comment states "Should have exactly one child" but assertion checks `len(label.children) >= 1` (in `test_heading_produces_label_widget`).
- Line 87: Missing `@pytest.mark.needs_window` on `@pytest.mark.property` test `test_multiple_blocks_produce_multiple_widgets`; required for MarkdownLabel child building.
- Line 91: Uses Hypothesis `@given(st.integers(min_value=1, max_value=5))` for single-dimension small finite input space; guidelines prefer `@pytest.mark.parametrize`.
- Line 124: Test name `test_text_change_updates_widgets` verifies rebuild occurrence (lines 137-139) but does not follow `test_*_triggers_rebuild_*` naming convention for rebuild verification tests.
- ~~Lines 147-172 (`test_different_block_counts_update_correctly`): Tests structure property change (`text`) with `force_rebuild()` but does not verify rebuild occurred using `collect_widget_ids`, manual ID comparison, or `assert_rebuild_occurred`.~~ **FIXED**: Renamed to `test_different_block_counts_trigger_rebuild` and added rebuild verification.
- ~~Lines 175-192 (`test_clear_text_removes_widgets`): Tests structure property change (`text='')` with `force_rebuild()` but lacks rebuild verification via widget IDs or helpers.~~ **FIXED**: Renamed to `test_clear_text_triggers_rebuild_and_removes_widgets` and added rebuild verification.
- ~~Lines 194-220 (`test_ast_updates_with_text`): Tests structure property change (`text`) with `force_rebuild()` but lacks rebuild verification via widget IDs or helpers; only checks AST string representation and `text` value.~~ **FIXED**: Renamed to `test_ast_updates_with_text_and_triggers_rebuild` and added rebuild verification.

## test_font_properties.py
- ~~Lines 226-253 (`test_line_height_change_triggers_rebuild`): Incorrectly treats `line_height` (style-only property) as structure property. Uses `collect_widget_ids` before change, `force_rebuild()` (only for structure properties), and asserts rebuild occurred (`ids_before != ids_after`). Should assert no rebuild (`ids_before == ids_after`), omit `force_rebuild()`, use name like `test_line_height_preserves_widget_tree` or `test_line_height_updates_value_immediately`, per rebuild contract and naming guidelines.~~ **FIXED**: Renamed to `test_line_height_change_preserves_widget_tree`, removed `force_rebuild()`, and now correctly asserts no rebuild occurs (style-only property).

## test_color_properties.py
- Line 82: Test method name `test_color_change_updates_value_without_rebuild` deviates from naming convention for no-rebuild tests; should use `test_*_preserves_widget_tree_*` pattern as it verifies no rebuild occurred (line 101), whereas `test_*_updates_value_*` is for value changes without rebuild verification.
- Lines 166-189: `test_links_unstyled_by_default` and `test_links_styled_when_enabled` mix unrelated link markup styling tests into `TestColorPropertyForwarding` class (lines 24-25), which is designated for color property forwarding; violates organization guideline of one class per property/behavior with no mixed unrelated functionality.

## test_text_properties.py
- Lines 342, 353, 369, 385, 402, 419: Single-dimension small finite strategy (unicode_errors_strategy, size 3) tests use Hypothesis instead of preferred `@pytest.mark.parametrize` for single small finite domains.
- Lines 483, 495, 511, 527, 544, 561: Single-dimension boolean strategy (st.booleans()) tests use Hypothesis instead of preferred `@pytest.mark.parametrize` for single small finite domains.
- Line 239: Missing `@pytest.mark.unit` marker on unit test `test_default_text_size_maintains_none_height`.
- Line 21: `TestTextSizeForwarding` class docstring inaccurately describes tests as verifying "text_size forwarding to child Label widgets" when methods primarily test parent storage/assert existence.
- Line 85: `test_text_size_with_width_passed_to_renderer` docstring claims text_size "affects internal Labels" but test lacks assertions verifying child Label `text_size` values (only comments on dynamic binding).
- Lines 237, 248: Conditional `if hasattr(lbl, 'text_size') and lbl.text_size:` checks are unnecessary as all Label widgets have `text_size` ListProperty; use direct access.

## test_padding_properties.py
- Lines 70-80 and 85-95: `test_four_element_padding_applied_directly` and `test_padding_property_stored_correctly` redundantly test four-element padding storage/normalization on MarkdownLabel.padding.
- ~~Lines 100-117: `test_padding_change_updates_container` changes `padding` (structure property) but does not verify rebuild occurred (missing `collect_widget_ids` before/after and assertion).~~ **FIXED**: Renamed to `test_padding_change_triggers_rebuild` and added rebuild verification.
- Lines 135-279, 386-542, 546-615: Redundant classes `TestTextPaddingForwarding`, `TestPaddingWithNestedStructures`, `TestTextPaddingAppliesToChildLabels` all test `text_padding` forwarding/application to child Labels across similar markdown structures (paragraphs, headings, lists, tables, nested), violating "one class per property/behavior" organization guideline.
- Line 383: Docstring comment above `TestPaddingWithNestedStructures` refers to "`padding` property" but all tests set `text_padding`, inconsistent.
- ~~Lines 673-694: `test_padding_change_affects_container_only` changes `padding` (structure property) but does not verify rebuild occurred (missing `collect_widget_ids` before/after and assertion); test name uses "change_affects" but focuses on value preservation without rebuild check.~~ **FIXED**: Added rebuild verification with `collect_widget_ids` and `force_rebuild()`.
- ~~No dedicated tests anywhere verifying `padding` changes trigger rebuild (required for structure properties per TESTING.md), e.g., no `test_padding_triggers_rebuild_*` methods with `force_rebuild()` and ID comparison.~~ **FIXED**: `test_padding_change_triggers_rebuild` now properly verifies rebuild.
- ~~Line 100 (`test_padding_change_updates_container`): Test name uses `updates_*` pattern (for value changes without rebuild verification) but `padding` requires rebuild, making name inaccurate per naming conventions.~~ **FIXED**: Renamed to `test_padding_change_triggers_rebuild`.

## test_sizing_behavior.py
- Line 27: Test method name `test_auto_size_hint_enabled_sets_none` incorrectly references "auto_size_hint" instead of the actual property "auto_size_height".
- Lines 45 and 101: Test names `test_height_bound_to_minimum` and `test_auto_size_height_true_binds_height_to_minimum` claim to verify height binding to `minimum_height`, but only assert `size_hint_y` is `None` without checking `height == minimum_height`.
- Line 54: `test_empty_label_has_zero_height` claims to test zero height but does not assert `label.height == 0` or `label.minimum_height == 0`; only checks `len(label.children) == 0` and `size_hint_y is None`.
- Line 67: `test_more_content_means_more_height_potential` claims to test height increase with more content but only asserts `len(label.children) >= num_paragraphs` without height comparison.
- Lines 25, 87, 99, 153, 187, 212, 233, 255, 290, 404, 426, 477, 494, 512: Inconsistent strategy classification for `@given(simple_markdown_document())`; labeled "Complex strategy" at line 25 but "Mixed finite/complex strategy" elsewhere without a finite component in the strategy.
- Line 43: `@given(markdown_heading())` labeled "Mixed finite/complex strategy: 20 examples (5 finite × 4 complex samples)" but `markdown_heading()` appears to be a single complex strategy, not mixed.
- Lines 126, 170, 257, 339, 450: `@given(st.floats(...))` or combinations labeled "Complex strategy" or "Mixed finite/complex" with 50 examples; floats are complex/infinite, but rationale "(5 finite × 10 complex samples)" at line 170 assumes undocumented finite component from `simple_markdown_document()`.

## test_advanced_compatibility.py
- Lines 613-644 (`test_text_size_updates_value`): Incorrectly treats `text_size` as style-only property (no `force_rebuild()`, asserts no rebuild with `ids_before == ids_after`), but `TESTING.md` classifies `text_size` as structure property requiring rebuild.
- Lines 648-675 (`test_multiple_property_changes_rebuild_correctly`): Test name and docstring suggest verifying rebuild behavior, but performs no widget ID collection or rebuild assertions; only verifies property values after changes.
- ~~Lines 851-860 (`test_disabled_change_triggers_rebuild`): Duplicated code block (lines 856-860 identical to 851-855).~~ **FIXED**: Removed duplicated verification code block.

## test_performance.py
- Line 24: Class `TestStyleOnlyPropertyUpdates` mixes tests for style-only property preservation with structure property rebuild tests (lines 256-296), violating the guideline for one class per property/behavior and descriptive class names with no mixed classes.
- Lines 72-91: `test_color_change_preserves_widget_tree` fails to verify that the color change was applied to descendant labels, contrary to rebuild contract testing patterns requiring verification of property change application.
- Lines 114-132: `test_halign_change_preserves_widget_tree` does not verify that the halign change was applied to descendant labels.
- Lines 152-170: `test_valign_change_preserves_widget_tree` does not verify that the valign change was applied to descendant labels.
- Lines 193-211: `test_line_height_change_preserves_widget_tree` does not verify that the line_height change was applied to descendant labels.
- Lines 237-255: `test_disabled_change_preserves_widget_tree` does not verify that the disabled state change was propagated to descendant labels.
- Lines 307-330: `test_multiple_style_changes_preserve_widget_tree` does not verify that any of the multiple style changes were applied to descendant labels.
- Lines 234-237: `test_disabled_change_preserves_widget_tree` uses Hypothesis `@given(st.booleans())` for a single small finite dimension (2 values) instead of the preferred `@pytest.mark.parametrize` per guidelines on when to use Hypothesis vs. parametrize.

## test_rebuild_scheduling.py
- Line 71: Incorrect standardized comment for `@settings`; claims "2 finite × 8 complex samples" but there is only 1 finite strategy (`st_font_name` with 2 values), while `st_alphanumeric_text` and `st_font_size` are complex.
- ~~Lines 67-104 (`test_mixed_property_changes_batch_rebuilds`): `font_size` parameter generated by `@given` but never used (not assigned to `label.font_size`), making the test inefficient and the strategy comment inaccurate.~~ **FIXED**: Removed unused `font_size` parameter from `@given` decorator.
- Line 107: `@pytest.mark.property` on `TestDeferredRebuildScheduling` class inappropriate as it contains non-Hypothesis tests (`test_font_name_change_schedules_deferred_rebuild` uses `@pytest.mark.parametrize`, `test_rebuild_trigger_is_clock_trigger` is a unit test).

## test_rebuild_semantics.py
- Line 264: Non-standard strategy classification "Complex combination strategy" (should be "Mixed finite/complex strategy"); non-standard rationale "(120 finite combinations with 5 complex strategies)" (should follow "[finite_size] finite × [samples] complex samples").
- Line 434: Non-standard strategy classification "Complex combination strategy" (should be "Mixed finite/complex strategy"); non-standard rationale "(60 finite combinations with 3 complex strategies)".
- Line 659: Incorrect strategy classification "Mixed finite/complex strategy" for two complex `simple_markdown_document()` strategies (no finite strategies; should be "Complex strategy").
- Line 702: Rationale assumes "3 finite" for `st_font_name()` (verify if exactly 3 values; otherwise inaccurate).
- Line 799: Non-standard strategy classification "Complex combination strategy" (should be "Mixed finite/complex strategy"); non-standard rationale "(24 finite combinations with 4 complex strategies)".
- Line 841: Rationale uses "finite combinations" instead of direct "finite" count in mixed format.
- Lines 56, 247, 421, 651, 784: `@pytest.mark.property` and `@pytest.mark.slow` applied to classes rather than individual property test methods (guidelines examples show on methods).

## test_texture_render_mode.py
- Lines 205-206, 274-275, 313-314, 376-377, 417-418, 462-463: Duplicated `def capture_ref` function and `dispatched_refs = []` pattern across multiple tests in `TestDeterministicTextureHitTesting`; should be consolidated into a single local helper function to avoid code duplication.
- Line 113: Test name `test_aggregated_refs_populated_in_texture_mode` and docstring inaccurately reflect the assertion; test only verifies `_aggregated_refs` attribute existence and `dict` type, not population with link zones.
- Lines 34, 110, 561: Class docstrings describe contents as "Property tests" despite classes containing only unit and parametrized tests, no Hypothesis property-based tests (`@given`).
- ~~Lines 165-169: `test_multiple_links_collected` uses conditional assertion (`if label._aggregated_refs:`) which allows the test to pass without verifying links were collected if the dict is empty; does not strictly assert collection occurred.~~ **FIXED**: Added explicit assertion that `_aggregated_refs` is populated before checking expected refs.

