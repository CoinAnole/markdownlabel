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

### test_comment_standardizer.py

- Line 15: The file modifies `sys.path` to add the tools directory for imports. According to guidelines section "Test File Structure", test files should use standard import patterns. The recommended approach would be to ensure the tools directory is properly structured as a package or to use a different import strategy rather than modifying sys.path at runtime.

- Line 42: Property test `test_boolean_strategy_comments_reference_true_false_coverage` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring only says "Boolean strategy comments always reference True/False coverage." without the required feature and property information.

- Line 40: The standardized comment `# Complex strategy: 20 examples (adequate coverage)` is incorrect for the strategy used. The test uses `st.integers(min_value=1, max_value=100).filter(lambda x: x not in {2, 5, 10, 20, 50, 100})` and `st.text(min_size=5, max_size=30, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd', 'Pc'))).map(lambda x: f"test_{x}")` which is a combination strategy, not a "Complex" strategy. According to guidelines section "Property-Based Testing Optimization", combination strategies should use the format `# Combination strategy: [N] examples (combination coverage)`.

- Line 91: Method `test_boolean_strategy_comment_generation_consistency` is missing a docstring. According to guidelines section "Best Practices", all test methods should have docstrings that describe what they test.

- Line 109: Method `test_boolean_strategy_detection_accuracy` is missing a docstring. According to guidelines section "Best Practices", all test methods should have docstrings that describe what they test.

- Line 170: Method `test_boolean_strategy_rationale_templates` is missing a docstring. According to guidelines section "Best Practices", all test methods should have docstrings that describe what they test.

- Line 198: Method `test_boolean_strategy_edge_cases` is missing a docstring. According to guidelines section "Best Practices", all test methods should have docstrings that describe what they test.

- Line 238: Method `test_boolean_strategy_integration_with_analysis` is missing a docstring. According to guidelines section "Best Practices", all test methods should have docstrings that describe what they test.

- Line 306: Property test `test_finite_strategy_comments_reference_input_space_size` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring only says "Finite strategy comments reference input space size in rationale." without the required feature and property information.

- Line 304: The standardized comment `# Complex strategy: 25 examples (adequate coverage)` is incorrect for the strategy used. The test uses `st.integers(min_value=0, max_value=10)`, `st.integers(min_value=11, max_value=50)`, and `st.integers(min_value=1, max_value=100).filter(...)` which is a combination strategy, not a "Complex" strategy. According to guidelines section "Property-Based Testing Optimization", combination strategies should use the format `# Combination strategy: [N] examples (combination coverage)`.

- Line 372: The standardized comment `# Complex strategy: 30 examples (adequate coverage)` is incorrect for the strategy used. The test uses `st.lists(st.text(min_size=1, max_size=10), min_size=1, max_size=20)` and `st.integers(min_value=1, max_value=50).filter(...)` which is a combination strategy, not a "Complex" strategy. According to guidelines section "Property-Based Testing Optimization", combination strategies should use the format `# Combination strategy: [N] examples (combination coverage)`.

- Line 373: Property test `test_sampled_from_finite_strategy_documentation` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring only says "Sampled_from finite strategies are properly documented." without the required feature and property information.

- Line 418: Method `test_finite_strategy_size_classification` is missing a docstring. According to guidelines section "Best Practices", all test methods should have docstrings that describe what they test.

- Line 469: Method `test_finite_strategy_rationale_consistency` is missing a docstring. According to guidelines section "Best Practices", all test methods should have docstrings that describe what they test.

- Line 504: Method `test_safety_checks_and_validation` is missing a docstring. According to guidelines section "Best Practices", all test methods should have docstrings that describe what they test.

- Line 536: Method `test_error_handling_in_backup_operations` is missing a docstring. According to guidelines section "Best Practices", all test methods should have docstrings that describe what they test.

- Line 596: Property test `test_execution_time_performance_rationale_documented` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring only says "Execution time performance rationale is properly documented." without the required feature and property information.

- Line 595: The standardized comment `# Complex strategy: 3 examples (performance optimized)` is incorrect for the strategy used. The test uses `st.integers(min_value=1, max_value=5)`, `st.sampled_from(['text', 'floats', 'composite'])`, and `st.text(min_size=5, max_size=30, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd', 'Pc'))).map(lambda x: f"test_{x}")` which is a combination strategy, not a "Complex" strategy. According to guidelines section "Property-Based Testing Optimization", combination strategies should use the format `# Combination strategy: [N] examples (combination coverage)`.

- Line 661: Property test `test_explicit_performance_comments_detected` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring only says "Explicit performance comments are properly detected and preserved." without the required feature and property information.

- Line 660: The standardized comment `# Complex strategy: 4 examples (performance optimized)` is incorrect for the strategy used. The test uses `st.sampled_from([...])` and `st.integers(min_value=1, max_value=20)` which is a combination strategy, not a "Complex" strategy. According to guidelines section "Property-Based Testing Optimization", combination strategies should use the format `# Combination strategy: [N] examples (combination coverage)`.

- Line 708: Method `test_performance_rationale_integration_with_standardizer` is missing a docstring. According to guidelines section "Best Practices", all test methods should have docstrings that describe what they test.

- Line 773: Method `test_performance_rationale_enhancement_of_existing_comments` is missing a docstring. According to guidelines section "Best Practices", all test methods should have docstrings that describe what they test.

- Line 802: Method `test_performance_pattern_analysis_across_files` is missing a docstring. According to guidelines section "Best Practices", all test methods should have docstrings that describe what they test.

- Line 857: The `setup_method` in `TestCommentStandardizationIntegration` class modifies `sys.path` by inserting the tools directory. This is redundant since the path modification was already done at the module level (line 15). According to guidelines section "Helper Functions", redundant operations should be avoided.

- Line 861: The import of `CommentAnalyzer` is done inside the `setup_method` with a try/except block. According to guidelines section "Helper Functions", imports should be at the module level, not inside test methods or setup methods. This import should be moved to the top of the file with the other imports.

- Line 865: Method `test_end_to_end_standardization_workflow` has a docstring but is missing the required docstring format for property tests. However, this is not a property test (it doesn't use @pytest.mark.property), so this is acceptable. The docstring format is appropriate for a unit test.

- Line 933: Method `test_batch_standardization_workflow` has a docstring but is missing the required docstring format for property tests. However, this is not a property test, so this is acceptable.

- Line 987: Method `test_backup_and_rollback_functionality` has a docstring but the implementation is just `assert True` with a comment saying "Backup functionality no longer exercised in tests." According to guidelines section "Best Practices", tests should not be empty or contain only assertions that always pass. If this functionality is no longer tested, the test should be removed or properly implemented.

- Line 995: Method `test_standardization_tool_integration_compatibility` has a docstring but is missing the required docstring format for property tests. However, this is not a property test, so this is acceptable.

- Line 1062: Method `test_error_handling_and_recovery` has a docstring but is missing the required docstring format for property tests. However, this is not a property test, so this is acceptable.

### test_core_functionality_properties.py

No deviations found.

### test_core_functionality.py

- Line 33: Property test `test_markdown_produces_widgets` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring only says "Valid Markdown text produces at least one widget." without the required feature and property information.

- Line 46: Property test `test_heading_produces_label_widget` is missing the required docstring format. Should include feature and property information following the format `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**`.

- Line 63: Property test `test_paragraph_produces_label_widget` is missing the required docstring format. Should include feature and property information.

- Line 76: Property test `test_multiple_blocks_produce_multiple_widgets` is missing the required docstring format. Should include feature and property information.

- Line 109: Property test `test_text_change_updates_widgets` is missing the required docstring format. Should include feature and property information.

- Line 129: Property test `test_different_block_counts_update_correctly` is missing the required docstring format. Should include feature and property information.

- Line 155: Property test `test_clear_text_removes_widgets` is missing the required docstring format. Should include feature and property information.

- Line 173: Property test `test_ast_updates_with_text` is missing the required docstring format. Should include feature and property information.

- Line 204: Property test `test_link_produces_ref_markup` is missing the required docstring format. Should include feature and property information.

- Line 229: Property test `test_link_url_in_ref_tag` is missing the required docstring format. Should include feature and property information.

- Line 250: Property test `test_various_urls_in_links` is missing the required docstring format. Should include feature and property information.

- Line 281: Property test `test_nested_lists_render_without_exception` is missing the required docstring format. Should include feature and property information.

- Line 299: Property test `test_nested_quotes_render_without_exception` is missing the required docstring format. Should include feature and property information.

- Line 316: Property test `test_mixed_nesting_renders_without_exception` is missing the required docstring format. Should include feature and property information.

- Line 103: A decorator comment `# Complex strategy: 20 examples (adequate coverage)` is placed between the class definition and its docstring. According to guidelines, such comments are meant to be used with @settings decorators, not as standalone comments in class bodies. The comment should be removed as it doesn't correspond to any decorator.

- Line 242: A comment `# Complex strategy: 20 examples (adequate coverage)` appears inside a test method before a return statement. This is a misplaced property test comment that doesn't correspond to any @settings decorator and should be removed.
