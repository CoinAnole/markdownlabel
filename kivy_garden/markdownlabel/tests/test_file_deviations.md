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

### test_documentation_compliance.py

- Line 19-23: Test `test_custom_values_are_documented` is a meta-test (marked with `@pytest.mark.test_tests`) but its docstring is missing the required format for property-based tests. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. While this is a meta-test that validates the test suite itself, it still uses property-based testing concepts and should follow the documentation format.

- Line 123-124: Property test `test_custom_value_detection_property` has an incorrect strategy classification. The comment says `# Medium finite strategy: 20 examples (adequate finite coverage)` but the strategy `st.integers(min_value=11, max_value=200)` has an input space of 190 values (200-11+1). According to guidelines section "Property-Based Testing Optimization", medium finite strategies are for integer ranges with 11-50 values. This should be classified as a "Complex" strategy since it has a large finite input space.

- Line 126-127: Property test `test_custom_value_detection_property` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring only says "Property test for custom value detection logic." without the required feature and property information.

- Line 138-139: Property test `test_comment_detection_property` has a correct strategy classification as "Complex strategy" with `st.text(min_size=1, max_size=100)`, which aligns with the guidelines.

- Line 141-142: Property test `test_comment_detection_property` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring only says "Property test for explanatory comment detection." without the required feature and property information.

### test_file_analyzer.py

- Line 16: The file modifies `sys.path` to add the tools directory for imports. According to guidelines section "Test File Structure", test files should use standard import patterns. The recommended approach would be to ensure the tools directory is properly structured as a package or to use a different import strategy rather than modifying sys.path at runtime.

- Line 298-300: Property test `test_rationale_generation_for_strategy_types` uses `st.sampled_from(['boolean', 'small_finite', 'medium_finite', 'combination', 'complex'])` which is a small finite strategy with 5 values, but the comment says `# Small finite strategy: 5 examples (input space size: 5)`. While the comment format is correct, the strategy type classification should be "small_finite" not "Small finite" (capitalization inconsistency with the sampled_from values which use lowercase). According to guidelines section "Property-Based Testing Optimization", strategy type classifications should use standardized terminology with consistent casing.

- Line 298-300: Property test `test_rationale_generation_for_strategy_types` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring only says "Generates appropriate rationales for different strategy types." without the required feature and property information.

- Line 473-479: Property test `test_tool_integration_compatibility` uses `st.sampled_from(['Boolean', 'Small finite', 'Medium finite', 'Complex', 'Combination'])` which is a small finite strategy with 5 values, but the comment says `# Complex strategy: 20 examples (adequate coverage)`. This is incorrect - the strategy is actually a small finite strategy with an input space of 5 values, so the comment should be `# Small finite strategy: 5 examples (input space size: 5)` according to guidelines section "Property-Based Testing Optimization".

- Line 488-498: The test generates standardized comments dynamically with rationale mapping, but the strategy type names in the rationale_map use different casing than the sampled_from values (e.g., 'Boolean' vs 'Boolean', 'Small finite' vs 'Small finite'). This inconsistency could cause issues when the comment is parsed by tools that expect exact matching with strategy type names.

- Line 501-508: The strategy_code_map generates strategies for different types, but the 'Medium finite' strategy uses `st.sampled_from([f"item_{i}" for i in range(25)])` which is a small finite strategy with 25 values, not a medium finite strategy. According to guidelines section "Property-Based Testing Optimization", medium finite strategies are for integer ranges with 11-50 values. This should be classified as a "small_finite" strategy since it's a sampled_from list with 25 items.

- Line 501-508: The 'Combination' strategy uses `st.tuples(st.booleans(), st.integers(min_value=0, max_value=2))` which has 2 * 3 = 6 combinations, making it a small finite strategy rather than a combination strategy. According to guidelines section "Property-Based Testing Optimization", small finite strategies should use the format `# Small finite strategy: [N] examples (input space size: [N])` when the total combinations are small (≤10).

- Line 474: The sampled_from values use title case ('Boolean', 'Small finite', 'Medium finite', 'Complex', 'Combination') but the guidelines specify lowercase strategy type names ('boolean', 'small_finite', 'medium_finite', 'complex', 'combination'). This inconsistency could cause issues when tools try to match strategy types.

- Line 303: The test imports `StrategyAnalysis` and `StrategyType` inside the test method. According to guidelines section "Helper Functions", imports should be at the module level, not inside test methods. This import should be moved to the top of the file with the other imports.

### test_font_properties.py

- Line 38-48: Helper method `_is_code_label` is defined in the test class. According to guidelines section "Helper Functions", helper functions should be added to `test_utils.py` and imported, not duplicated in test files. This helper should be moved to test_utils.py.

- Line 124: Test name `test_font_name_change_updates_value` uses "updates_value" naming but docstring says "triggers widget rebuild with new font". According to guidelines section "Test Naming Conventions", tests that verify rebuild behavior should use `test_*_triggers_rebuild_*` naming. The test calls `label.force_rebuild()` which suggests it's testing rebuild behavior, so the name should be `test_font_name_change_triggers_rebuild` or similar.

- Line 232: Test name `test_line_height_change_updates_value` uses "updates_value" naming but docstring says "triggers widget rebuild with new value". According to guidelines section "Test Naming Conventions", tests that verify rebuild behavior should use `test_*_triggers_rebuild_*` naming. The test name should be `test_line_height_change_triggers_rebuild` or similar.

- Line 287: Property test `test_line_height_applied_to_all_content_types` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring only says "line_height is applied to all content types including code." without the required feature and property information.

- Line 348: Property test `test_font_family_excluded_from_code_blocks` has the required docstring format with feature and property information, which is correct.

- Line 372: Property test `test_font_family_forwarded_to_non_code_labels` has the required docstring format, which is correct.

- Line 397: Property test `test_font_context_forwarded_to_all_labels_including_code` has the required docstring format, which is correct.

- Line 422: Property test `test_font_features_forwarded_to_all_labels_including_code` has the required docstring format, which is correct.

- Line 442: Test `test_font_hinting_forwarded_to_all_labels_including_code` is not a property test (uses @pytest.mark.parametrize), so it doesn't need the property test docstring format. This is correct.

- Line 465: Property test `test_font_kerning_forwarded_to_all_labels_including_code` has the required docstring format, which is correct.

- Line 496: Property test `test_combined_font_properties_with_code_block` has the required docstring format, which is correct.

- Line 558: Property test `test_base_font_size_updates_all_labels_immediately` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring only says "Changing base_font_size immediately updates all child Label font_size properties." without the required feature and property information.

- Line 606: Property test `test_heading_font_size_updates_with_scale` is missing the required docstring format. Should include feature and property information following the format `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**`.

- Line 645: Property test `test_paragraph_font_size_updates_immediately` is missing the required docstring format. Should include feature and property information.

- Line 682: Property test `test_heading_scale_factors_preserved` is missing the required docstring format. Should include feature and property information.

- Line 723: Property test `test_multiple_headings_preserve_relative_scales` is missing the required docstring format. Should include feature and property information.

- Line 769: Property test `test_heading_scale_preserved_after_base_font_size_change` is missing the required docstring format. Should include feature and property information.

- Line 830: Property test `test_widget_identities_preserved_on_font_size_change` is missing the required docstring format. Should include feature and property information.

- Line 859: Property test `test_heading_widget_identity_preserved` is missing the required docstring format. Should include feature and property information.

- Line 901: Property test `test_multiple_font_size_changes_preserve_identities` is missing the required docstring format. Should include feature and property information.

- Line 927: Property test `test_rebuild_counter_not_incremented_on_font_size_change` is missing the required docstring format. Should include feature and property information.

- Line 815-821: Helper method `_collect_widget_ids` is defined in the test class. According to guidelines section "Helper Functions", helper functions should be added to `test_utils.py` and imported, not duplicated in test files. This helper should be moved to test_utils.py. Note that test_utils.py already has a `collect_widget_ids` function that could be used instead.

- Line 815-821: The `_collect_widget_ids` helper method is a duplicate of functionality that should be available in test_utils.py. According to guidelines section "Helper Functions", the file already imports from test_utils.py, so the `collect_widget_ids` function should be used instead of defining a duplicate method.

- Line 927-957: Test `test_rebuild_counter_not_incremented_on_font_size_change` verifies that rebuilds are not triggered by font size changes, which is correct behavior. However, the test only checks that rebuild_count[0] == 0 but doesn't verify that the font size was actually updated. The test finds a label but doesn't check its font_size value. According to guidelines section "Best Practices", tests should verify both the expected behavior (no rebuild) AND that the change was applied correctly.

### test_helper_availability.py

- Line 36: Property test `test_widget_traversal_helpers_available` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring only says "For any markdown content, widget traversal helpers should be available and functional." without the required feature and property information format.

- Line 62: Property test `test_comparison_helpers_available` is missing the required docstring format. Should include feature and property information following the format `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**`.

- Line 78: Property test `test_padding_comparison_helpers_available` is missing the required docstring format. Should include feature and property information.

- Line 95: Property test `test_float_comparison_helpers_available` is missing the required docstring format. Should include feature and property information.

- Line 111: Property test `test_rebuild_detection_helpers_available` is missing the required docstring format. Should include feature and property information.

- Line 146-182: Method `test_hypothesis_strategies_available` defines nested functions with @given decorators to test strategies. This is an unusual pattern - typically property tests should be standalone methods, not nested functions defined inside other test methods. According to guidelines section "Property-Based Testing", property tests should be defined as regular test methods with @given decorators, not nested inside other test methods.

- Line 154-159: Nested function `test_color_strategy` is defined with @given decorator inside the test method. This deviates from standard testing patterns where property tests should be standalone methods. The test should be refactored to be a proper test method rather than a nested function.

- Line 165-170: Nested function `test_padding_strategy` is defined with @given decorator inside the test method. Same issue as line 154-159.

- Line 176-180: Nested function `test_markdown_strategy` is defined with @given decorator inside the test method. Same issue as line 154-159.

- Line 189: Property test `test_no_duplicate_find_labels_recursive_implementations` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring only says "For any test file, there should be no duplicate _find_labels_recursive implementations." without the required feature and property information format.

- Line 223: Property test `test_no_duplicate_collect_widget_ids_implementations` is missing the required docstring format. Should include feature and property information.

- Line 257: Property test `test_all_test_files_import_from_test_utils` is missing the required docstring format. Should include feature and property information.

### test_import.py

No deviations found.

### test_inline_renderer.py

- Line 89: Property test `test_strong_produces_bold_tags` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring only says "Strong tokens produce [b]...[/b] markup." without the required feature and property information.

- Line 100: Property test `test_emphasis_produces_italic_tags` is missing the required docstring format. Should include feature and property information following the format `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**`.

- Line 111: Property test `test_codespan_produces_font_tags` is missing the required docstring format. Should include feature and property information.

- Line 122: Property test `test_strikethrough_produces_s_tags` is missing the required docstring format. Should include feature and property information.

- Line 133: Property test `test_link_produces_ref_tags_unstyled` is missing the required docstring format. Should include feature and property information.

- Line 151: Property test `test_link_produces_ref_tags_styled` is missing the required docstring format. Should include feature and property information.

- Line 179: Property test `test_text_escapes_special_characters` is missing the required docstring format. Should include feature and property information.

- Line 213: Property test `test_only_special_chars_fully_escaped` is missing the required docstring format. Should include feature and property information.

- Line 235: Property test `test_escape_is_reversible` is missing the required docstring format. Should include feature and property information.

- Line 421: Property test `test_urls_with_brackets_are_safe` is missing the required docstring format. Should include feature and property information.

- Line 680: Property test `test_html_content_is_escaped` is missing the required docstring format. Should include feature and property information.

- Line 743: Property test `test_arbitrary_html_content_safety` is missing the required docstring format. Should include feature and property information.
