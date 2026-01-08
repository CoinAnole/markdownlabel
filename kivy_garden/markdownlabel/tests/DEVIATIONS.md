# Test Deviations from TESTING.md Guidelines

## test_font_properties.py
- Line 685: Violated guideline: standardized comment format for Mixed finite/complex strategies requires specific numerical rationale like "(finite_size finite × samples complex samples)". Current: "(large finite lists × complex)" vague without numbers.

## test_color_properties.py
- Line 82: Violated guideline: "test_*_preserves_widget_tree_* for tests verifying NO rebuild". Name `test_color_change_updates_value_without_rebuild` uses updates_value pattern but verifies rebuild preservation.

## test_padding_properties.py
- Lines 247, 298, 330: Violated guideline: "test_*_preserves_widget_tree_* for no rebuild verification". Names use `updates_in_place` instead.
- Line 605: Violated guideline: "test_*_triggers_rebuild_* ONLY for rebuild verification". `test_padding_change_affects_container_only` verifies rebuild but lacks triggers_rebuild in name.

## test_sizing_behavior.py
- Lines 25,87,98,153,211,233,290,403,426,477,494,512,537: Inconsistent Hypothesis strategy classification for `simple_markdown_document()` (Complex vs Mixed).
- Lines 45-53,102-113,190-200,361-371: Names/docstrings claim height binding verification but assert only size_hint_y, not height vs minimum_height.
- Line 528: Manual `assert ids_before != ids_after` instead of `assert_rebuild_occurred` helper.

## test_advanced_compatibility.py
- Lines 611-645: `test_text_size_updates_value` asserts no rebuild, but text_size is structure property requiring rebuild.
- Lines 357-407: `TestDisabledColorApplication.test_disabled_change_triggers_rebuild` asserts rebuild for style-only disabled property.
- Lines 812-854: `TestReactiveRebuildOnPropertyChange.test_disabled_change_triggers_rebuild` same issue.

## test_serialization.py
- Line 649: Complex strategy rationale "(two complex strategies combined)" instead of "(adequate coverage)" or "(performance optimized)".

## test_rebuild_semantics.py
- Line 264: Rationale "(120 finite combinations with 5 complex strategies)" should be "(120 finite × 5 complex samples)".
- Line 434: "(60 finite combinations with 3 complex strategies)" same.
- Line 659: Misclassified as Mixed finite/complex (two complex strategies), should be Complex; rationale "(complex samples)" invalid.
- Line 799: "(24 finite combinations with 4 complex strategies)" phrasing issue.
- Line 841: "(24 finite combinations × 2 complex samples)" incorrect "finite combinations ×".

## test_clipping_behavior.py
- Lines 83-101,124-140,214-220: Manual StencilView detection duplicates `has_clipping_container` helper logic.
- Lines 83,124,214: StencilView import inside methods instead of top-level.

## test_texture_sizing.py
- Lines 76,93,109,124,158,253,271,338,353: Names/docstrings claim specific widget creation but assert only len(children) without isinstance checks.
- Line 287: Complex rationale "(two complex strategies combined)" non-standard.

## test_rtl_alignment.py
- Line 280: `test_direction_change_preserves_widget_identities` verifies no rebuild but uses "identities" not "widget_tree".
