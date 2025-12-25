### test_advanced_compatibility.py

- Line 183: Test name `test_font_kerning_change_updates_value` uses "updates_value" naming but docstring says "triggers widget rebuild with new value". According to guidelines, tests that verify rebuild behavior should use `test_*_triggers_rebuild_*` naming, while tests that verify value changes without rebuild verification should use `test_*_updates_value_*` naming. The test calls `label.force_rebuild()` and verifies the new value, which is inconsistent with the naming convention.

- Line 207: Test name `test_font_blended_change_updates_value` uses "updates_value" naming but docstring says "triggers widget rebuild with new value". Same naming convention issue as line 183.

- Line 390: Test name `test_disabled_change_updates_value` uses "updates_value" naming but docstring says "triggers widget rebuild". The test verifies color changes but doesn't verify whether a rebuild occurred (no `collect_widget_ids` comparison). According to guidelines, tests claiming to test rebuilds must verify them.

- Line 719: Test `test_halign_updates_value` has a docstring saying "updates value without rebuilding widgets" but the inline comment at line 738 says "Verify widgets were rebuilt with new halign". The test doesn't actually verify whether a rebuild occurred (no widget ID comparison). This is inconsistent - either the test should verify rebuild behavior, or it should be documented as testing value updates.

- Line 751: Test `test_valign_updates_value` has a docstring saying "updates value without rebuilding widgets" but the inline comment at line 770 says "Verify widgets were rebuilt with new valign". The test doesn't verify whether a rebuild occurred. Same inconsistency as line 719.

- Line 782: Test `test_unicode_errors_updates_value` has a docstring saying "updates value without rebuilding widgets" but the test calls `label.force_rebuild()` at line 800 and the inline comment at line 802 says "Verify widgets were rebuilt with new unicode_errors". The docstring and implementation are inconsistent.

- Line 812: Test `test_strip_updates_value` has a docstring saying "updates value without rebuilding widgets" but the test calls `label.force_rebuild()` at line 830 and the inline comment at line 832 says "Verify widgets were rebuilt with new strip". The docstring and implementation are inconsistent.

- Line 842: Test `test_disabled_color_updates_value` has a docstring saying "updates color without rebuilding widgets" but the inline comment at line 874 says "Verify widgets were rebuilt with correct color". The test doesn't verify whether a rebuild occurred. The docstring and implementation are inconsistent.

- Line 911: Test `test_font_kerning_updates_value` has a docstring saying "updates value without rebuilding widgets" but the test calls `label.force_rebuild()` at line 929 and the inline comment at line 931 says "Verify widgets were rebuilt with new font_kerning". The docstring and implementation are inconsistent.

- Line 941: Test `test_font_blended_updates_value` has a docstring saying "updates value without rebuilding widgets" but the test calls `label.force_rebuild()` at line 959 and the inline comment at line 961 says "Verify widgets were rebuilt with new font_blended". The docstring and implementation are inconsistent.

### test_clipping_behavior.py

- Line 19-33: Helper method `_has_clipping_container` is duplicated in both test classes (lines 19-33 and 157-171). According to guidelines section "Helper Functions", helper functions should be added to `test_utils.py` and imported, not duplicated in test files.

- Line 50: Property test `test_text_size_height_enables_clipping` is missing the required docstring format for property-based tests. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings.

- Line 74: Property test `test_strict_label_mode_with_fixed_height_enables_clipping` is missing the required docstring format for property-based tests. Should include feature and property information.

- Line 94: Property test `test_clipping_container_height_matches_text_size` is missing the required docstring format for property-based tests. Should include feature and property information.

- Line 123: Property test `test_heading_content_clipped_when_height_constrained` is missing the required docstring format for property-based tests. Should include feature and property information.

- Line 186: Property test `test_no_clipping_when_text_size_height_none` is missing the required docstring format for property-based tests. Should include feature and property information.

- Line 210: Property test `test_no_clipping_when_strict_label_mode_false` is missing the required docstring format for property-based tests. Should include feature and property information.

- Line 234: Property test `test_content_added_directly_when_unconstrained` is missing the required docstring format for property-based tests. Should include feature and property information.

- Line 253: Property test `test_heading_expands_naturally_when_unconstrained` is missing the required docstring format for property-based tests. Should include feature and property information.

- Line 277: Property test `test_text_size_width_only_no_clipping` is missing the required docstring format for property-based tests. Should include feature and property information.

- Line 157-171: Duplicate helper method `_has_clipping_container` in `TestNoClippingWhenUnconstrained` class. Same implementation as lines 19-33 in `TestContentClippingWhenHeightConstrained`. This violates the guideline to avoid duplicating helper function implementations and to use shared helpers from test_utils.py instead.

### test_color_properties.py

- Line 34: Property test `test_color_applied_to_paragraph` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring only says "color is applied to paragraph Labels." without the required feature and property information.

- Line 49: Property test `test_color_applied_to_heading` is missing the required docstring format. Should include feature and property information following the format `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**`.

- Line 64: Property test `test_code_block_preserves_light_color` is missing the required docstring format. Should include feature and property information.

- Line 82: Property test `test_color_change_updates_value` is missing the required docstring format. Should include feature and property information.

- Line 83: Test `test_color_change_updates_value` has a docstring saying "Changing color triggers widget rebuild with new color" but according to guidelines section "Rebuild Contract Testing", color is a style-only property that updates existing widgets without rebuilding. The test name correctly uses "updates_value" naming and the implementation only verifies color value changes (not rebuild behavior), but the docstring incorrectly claims it triggers a rebuild. The docstring should describe the actual behavior (updating color values) rather than claiming a rebuild occurs.

- Line 105: Property test `test_color_applied_to_list_items` is missing the required docstring format. Should include feature and property information.

- Line 121: Property test `test_color_applied_to_table_cells` is missing the required docstring format. Should include feature and property information.

- Line 137: Property test `test_mixed_content_color_separation` is missing the required docstring format. Should include feature and property information.

### test_comment_format.py

- Line 13: The file modifies `sys.path` to add the tools directory for imports. According to guidelines section "Test File Structure", test files should use standard import patterns. The recommended approach would be to ensure the tools directory is properly structured as a package or to use a different import strategy rather than modifying sys.path at runtime.

- Line 41: Property test `test_valid_comment_format_compliance` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring only says "Valid standardized comments are correctly validated and parsed." without the required feature and property information.

- Line 66: Property test `test_standard_comment_generation_compliance` is missing the required docstring format. Should include feature and property information following the format `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**`.

- Line 79: Property test `test_boolean_strategy_rationale_compliance` is missing the required docstring format. Should include feature and property information.

- Line 89: Property test `test_small_finite_strategy_rationale_compliance` is missing the required docstring format. Should include feature and property information.

- Line 99: Property test `test_invalid_format_detection` is missing the required docstring format. Should include feature and property information.

- Line 117: Property test `test_invalid_strategy_type_detection` is missing the required docstring format. Should include feature and property information.

- Line 126: Property test `test_invalid_max_examples_detection` is missing the required docstring format. Should include feature and property information.

- Line 141: Property test `test_case_insensitive_strategy_types` is missing the required docstring format. Should include feature and property information.

- Line 154: Property test `test_whitespace_tolerance` is missing the required docstring format. Should include feature and property information.

- Line 174: Property test `test_comment_pattern_to_standardized_format` is missing the required docstring format. Should include feature and property information.

- Line 187: Property test `test_comment_pattern_with_optional_fields` is missing the required docstring format. Should include feature and property information.

- Line 229: Property test `test_custom_max_examples_require_documentation` is missing the required docstring format. Should include feature and property information.

- Line 276: Property test `test_standard_max_examples_require_documentation` is missing the required docstring format. Should include feature and property information.

- Line 294: Property test `test_custom_value_detection_accuracy` is missing the required docstring format. Should include feature and property information.

- Line 305: Property test `test_missing_documentation_reporting` is missing the required docstring format. Should include feature and property information.

- Line 337: Property test `test_documentation_with_invalid_format_detection` is missing the required docstring format. Should include feature and property information.

- Line 393: Property test `test_strategy_type_classification_consistency` is missing the required docstring format. Should include feature and property information.

- Line 410: Property test `test_boolean_and_small_finite_terminology_consistency` is missing the required docstring format. Should include feature and property information.

- Line 423: Property test `test_complex_strategy_terminology_consistency` is missing the required docstring format. Should include feature and property information.

- Line 442: Property test `test_combination_strategy_terminology_consistency` is missing the required docstring format. Should include feature and property information.

- Line 459: Property test `test_strategy_type_mapping_consistency` is missing the required docstring format. Should include feature and property information.

- Line 475: Property test `test_rationale_template_consistency` is missing the required docstring format. Should include feature and property information.

- Line 494: Property test `test_edge_case_handling_consistency` is missing the required docstring format. Should include feature and property information.

- Line 509: Property test `test_classification_determinism` is missing the required docstring format. Should include feature and property information.

- Line 553: Property test `test_standardized_comments_are_machine_parseable` is missing the required docstring format. Should include feature and property information.

- Line 601: Property test `test_generated_comments_are_machine_parseable` is missing the required docstring format. Should include feature and property information.

- Line 620: Property test `test_parsing_extracts_all_required_fields` is missing the required docstring format. Should include feature and property information.

- Line 645: Property test `test_machine_readable_format_consistency` is missing the required docstring format. Should include feature and property information.

- Line 665: Property test `test_integration_with_analysis_tools` is missing the required docstring format. Should include feature and property information.

- Line 702: Property test `test_error_handling_in_machine_parsing` is missing the required docstring format. Should include feature and property information.

- Line 720: Property test `test_round_trip_parsing_consistency` is missing the required docstring format. Should include feature and property information.

- Line 212: The `setup_method` in `TestCustomValueDocumentation` class duplicates the sys.path modification from line 13. This is redundant and violates the DRY principle. The path modification should be done once at the module level rather than in each setup_method.

- Line 369: The `setup_method` in `TestStrategyTypeConsistency` class also duplicates the sys.path modification. Same issue as line 212.

- Line 532: The `setup_method` in `TestMachineReadableFormat` class also duplicates the sys.path modification. Same issue as line 212.

- Line 730: Import statement `from test_optimization.comment_format import CommentPattern` inside a test method. According to guidelines section "Helper Functions", imports should be at the module level, not inside test methods. This import should be moved to the top of the file with the other imports.
