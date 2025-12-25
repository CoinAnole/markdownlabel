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

### test_kivy_renderer.py

- Line 24-37: Custom strategy `heading_token` is defined in the test file. According to guidelines section "Helper Functions", custom Hypothesis strategies should be added to test_utils.py and imported, not duplicated in test files. This strategy is used in multiple tests and should be consolidated.

- Line 40-50: Custom strategy `paragraph_token` is defined in the test file. According to guidelines section "Helper Functions", this strategy should be moved to test_utils.py and imported.

- Line 53-66: Custom strategy `list_item_token` is defined in the test file. According to guidelines section "Helper Functions", this strategy should be moved to test_utils.py and imported.

- Line 69-85: Custom strategy `list_token` is defined in the test file. According to guidelines section "Helper Functions", this strategy should be moved to test_utils.py and imported.

- Line 88-100: Custom strategy `code_block_token` is defined in the test file. According to guidelines section "Helper Functions", this strategy should be moved to test_utils.py and imported.

- Line 103-116: Custom strategy `block_quote_token` is defined in the test file. According to guidelines section "Helper Functions", this strategy should be moved to test_utils.py and imported.

- Line 119-132: Custom strategy `image_token` is defined in the test file. According to guidelines section "Helper Functions", this strategy should be moved to test_utils.py and imported.

- Line 586-651: Custom strategies `table_cell_token`, `table_row_token`, and `table_token` are defined in the test file. According to guidelines section "Helper Functions", these strategies should be moved to test_utils.py and imported.

- Line 189-191: Property test `test_heading_font_size_scales_with_base` uses `st.integers(min_value=1, max_value=6), st.floats(min_value=10, max_value=30)` which is a combination strategy with 6 * 21 = 126 possible combinations, but the comment says `# Complex strategy: 10 examples (adequate coverage)`. According to guidelines section "Property-Based Testing Optimization", this should be classified as a "Combination strategy" with the comment `# Combination strategy: 10 examples (combination coverage)` or the max_examples should be increased to cover more combinations (capped at 50).

- Line 189-208: Property test `test_heading_font_size_scales_with_base` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring only says "Heading font size scales proportionally with base_font_size." without the required feature and property information.

- Line 219-228: Property test `test_paragraph_has_markup_enabled` is missing the required docstring format. Should include feature and property information following the format `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**`.

- Line 230-238: Property test `test_paragraph_returns_label` is missing the required docstring format. Should include feature and property information.

- Line 251-259: Property test `test_list_returns_boxlayout` is missing the required docstring format. Should include feature and property information.

- Line 261-273: Property test `test_list_has_correct_item_count` is missing the required docstring format. Should include feature and property information.

- Line 275-290: Property test `test_unordered_list_has_bullet_markers` is missing the required docstring format. Should include feature and property information.

- Line 292-313: Property test `test_ordered_list_has_number_markers` is missing the required docstring format. Should include feature and property information.

- Line 324-366: Property test `test_nested_list_increases_indentation` is missing the required docstring format. Should include feature and property information.

- Line 378-386: Property test `test_code_block_returns_widget` is missing the required docstring format. Should include feature and property information.

- Line 388-408: Property test `test_code_block_has_monospace_font` is missing the required docstring format. Should include feature and property information.

- Line 410-421: Property test `test_code_block_has_dark_background` is missing the required docstring format. Should include feature and property information.

- Line 430-442: Property test `test_code_block_stores_language_info` is missing the required docstring format. Should include feature and property information.

- Line 468-476: Property test `test_block_quote_returns_boxlayout` is missing the required docstring format. Should include feature and property information.

- Line 478-488: Property test `test_block_quote_has_left_padding` is missing the required docstring format. Should include feature and property information.

- Line 490-499: Property test `test_block_quote_has_left_border` is missing the required docstring format. Should include feature and property information.

- Line 510-518: Property test `test_thematic_break_returns_widget` is missing the required docstring format. Should include feature and property information.

- Line 520-529: Property test `test_thematic_break_has_fixed_height` is missing the required docstring format. Should include feature and property information.

- Line 531-540: Property test `test_thematic_break_has_horizontal_line` is missing the required docstring format. Should include feature and property information.

- Line 551-559: Property test `test_image_returns_asyncimage` is missing the required docstring format. Should include feature and property information.

- Line 561-571: Property test `test_image_has_correct_source` is missing the required docstring format. Should include feature and property information.

- Line 573-582: Property test `test_image_stores_alt_text` is missing the required docstring format. Should include feature and property information.

- Line 662-703: Property test `test_table_has_correct_column_count` is missing the required docstring format. Should include feature and property information.

- Line 705-745: Property test `test_table_has_correct_cell_count` is missing the required docstring format. Should include feature and property information.

- Line 747-755: Property test `test_table_returns_gridlayout` is missing the required docstring format. Should include feature and property information.

- Line 757-766: Property test `test_table_cells_are_labels` is missing the required docstring format. Should include feature and property information.

- Line 777-792: Test `test_cell_alignment_applied` uses @pytest.mark.parametrize, so it's not a property test and doesn't need the property test docstring format. This is correct.

- Line 794-845: Property test `test_table_preserves_column_alignments` is missing the required docstring format. Should include feature and property information.

- Line 847-861: Test `test_invalid_alignment_defaults_to_left` uses @pytest.mark.parametrize, so it's not a property test and doesn't need the property test docstring format. This is correct.

- Line 863-874: Property test `test_cell_stores_alignment_metadata` is missing the required docstring format. Should include feature and property information.

- Line 882-972: Tests in `TestDeepNestingTruncation` class are not property tests (they don't use @given decorators), so they don't need the property test docstring format. This is correct.

### test_label_compatibility.py

- Line 29: Property test `test_font_size_sets_base_font_size` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring only says "Setting font_size updates base_font_size to the same value." without the required feature and property information.

- Line 39: Property test `test_base_font_size_returns_via_font_size` is missing the required docstring format. Should include feature and property information following the format `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**`.

- Line 50: Property test `test_font_size_change_updates_base_font_size` is missing the required docstring format. Should include feature and property information.

- Line 62: Property test `test_base_font_size_change_updates_font_size` is missing the required docstring format. Should include feature and property information.

- Line 73: Property test `test_bidirectional_equivalence` is missing the required docstring format. Should include feature and property information.

- Line 99: Property test `test_bold_property_accepted` is missing the required docstring format. Should include feature and property information following the format `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**`.

- Line 108: Property test `test_italic_property_accepted` is missing the required docstring format. Should include feature and property information.

- Line 116: Property test `test_underline_property_accepted` is missing the required docstring format. Should include feature and property information.

- Line 124: Property test `test_strikethrough_property_accepted` is missing the required docstring format. Should include feature and property information.

- Line 132: Property test `test_markup_property_accepted` is missing the required docstring format. Should include feature and property information.

- Line 140: Property test `test_all_noop_properties_together` is missing the required docstring format. Should include feature and property information.

- Line 160: Property test `test_noop_properties_do_not_affect_rendering` is missing the required docstring format. Should include feature and property information.

- Line 187: Property test `test_bold_property_change_after_creation` is missing the required docstring format. Should include feature and property information.

- Line 196: Property test `test_italic_property_change_after_creation` is missing the required docstring format. Should include feature and property information.

- Line 205: Property test `test_underline_property_change_after_creation` is missing the required docstring format. Should include feature and property information.

- Line 214: Property test `test_strikethrough_property_change_after_creation` is missing the required docstring format. Should include feature and property information.

- Line 223: Property test `test_markup_property_change_after_creation` is missing the required docstring format. Should include feature and property information.

- Line 243: Property test `test_mipmap_property_accepted_and_stored` is missing the required docstring format. Should include feature and property information following the format `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**`.

- Line 251: Property test `test_outline_width_property_accepted_and_stored` is missing the required docstring format. Should include feature and property information.

- Line 262: Property test `test_outline_color_property_accepted_and_stored` is missing the required docstring format. Should include feature and property information.

- Line 274: Property test `test_text_language_property_accepted_and_stored` is missing the required docstring format. Should include feature and property information.

- Line 280: Test `test_base_direction_property_accepted_and_stored` uses @pytest.mark.parametrize, so it's not a property test and doesn't need the property test docstring format. This is correct.

- Line 293: Property test `test_ellipsis_options_property_accepted_and_stored` is missing the required docstring format. Should include feature and property information.

- Line 305: Property test `test_all_noop_properties_together_accepted_and_stored` is missing the required docstring format. Should include feature and property information.

- Line 329: Property test `test_mipmap_property_change_after_creation` is missing the required docstring format. Should include feature and property information.

- Line 338: Property test `test_outline_width_property_change_after_creation` is missing the required docstring format. Should include feature and property information.

- Line 350: Property test `test_outline_color_property_change_after_creation` is missing the required docstring format. Should include feature and property information.

- Line 362: Property test `test_text_language_property_change_after_creation` is missing the required docstring format. Should include feature and property information.

- Line 369: Test `test_base_direction_property_change_after_creation` uses @pytest.mark.parametrize, so it's not a property test and doesn't need the property test docstring format. This is correct.

- Line 383: Property test `test_ellipsis_options_property_change_after_creation` is missing the required docstring format. Should include feature and property information.

- Line 397: Property test `test_advanced_noop_properties_do_not_affect_rendering` is missing the required docstring format. Should include feature and property information.

- Line 433: Test `test_label_compatibility_imports_resolve` is in a class marked with `@pytest.mark.test_tests`, which is correct for meta-tests. However, this is not a property test (doesn't use @given), so it doesn't need the property test docstring format. This is correct.

- Line 461: Test `test_shared_utilities_imports_resolve` is also in the meta-test class and is not a property test, so it doesn't need the property test docstring format. This is correct.

- Line 497: Test `test_cross_module_imports_work` is also in the meta-test class and is not a property test, so it doesn't need the property test docstring format. This is correct.

### test_padding_properties.py

- Line 24-33: Custom strategies `padding_single`, `padding_two`, and `padding_four` are defined in the test file. According to guidelines section "Helper Functions", custom Hypothesis strategies should be added to test_utils.py and imported, not duplicated in test files. These strategies are used throughout the file and should be consolidated.

- Line 44-60: Property test `test_single_padding_applied_uniformly` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring only says "Single padding value is applied uniformly to all sides." without the required feature and property information.

- Line 61-77: Property test `test_two_element_padding_applied_to_axes` is missing the required docstring format. Should include feature and property information following the format `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**`.

- Line 78: A stray comment `# Complex strategy: 20 examples (adequate coverage)` appears on line 78 that doesn't correspond to any @settings decorator. This is a misplaced comment that should be removed.

- Line 80-92: Property test `test_four_element_padding_applied_directly` is missing the required docstring format. Should include feature and property information.

- Line 94-106: Property test `test_padding_property_stored_correctly` is missing the required docstring format. Should include feature and property information.

- Line 108-127: Property test `test_padding_change_updates_container` is missing the required docstring format. Should include feature and property information.

- Line 129-142: Property test `test_default_padding_is_zero` is missing the required docstring format. Should include feature and property information.

- Line 153-166: Property test `test_padding_applied_to_paragraph` is missing the required docstring format. Should include feature and property information.

- Line 168-181: Property test `test_padding_applied_to_heading` is missing the required docstring format. Should include feature and property information.

- Line 183-197: Property test `test_padding_applied_to_list_items` is missing the required docstring format. Should include feature and property information.

- Line 199-213: Property test `test_padding_applied_to_table_cells` is missing the required docstring format. Should include feature and property information.

- Line 215-243: Property test `test_padding_applied_to_nested_structures` is missing the required docstring format. Should include feature and property information.

- Line 245-267: Property test `test_padding_change_updates_value` is missing the required docstring format. Should include feature and property information.

- Line 269-279: Test `test_default_padding_is_zero_for_all_labels` is not a property test (doesn't use @given), so it doesn't need the property test docstring format. This is correct.

- Line 290-313: Property test `test_padding_update_paragraph` is missing the required docstring format. Should include feature and property information.

- Line 315-351: Property test `test_padding_update_complex_content` is missing the required docstring format. Should include feature and property information.

- Line 353-369: Property test `test_multiple_padding_updates` is missing the required docstring format. Should include feature and property information.

- Line 380-405: Property test `test_padding_in_nested_lists` is missing the required docstring format. Should include feature and property information.

- Line 407-432: Property test `test_padding_in_nested_quotes` is missing the required docstring format. Should include feature and property information.

- Line 434-458: Property test `test_padding_in_complex_table` is missing the required docstring format. Should include feature and property information.

- Line 460-500: Property test `test_padding_in_mixed_nested_structures` is missing the required docstring format. Should include feature and property information.

- Line 502-526: Property test `test_padding_preserves_widget_hierarchy` is missing the required docstring format. Should include feature and property information.

- Line 537-550: Property test `test_text_padding_applied_to_paragraph_labels` is missing the required docstring format. Should include feature and property information.

- Line 552-565: Property test `test_text_padding_applied_to_heading_labels` is missing the required docstring format. Should include feature and property information.

- Line 567-581: Property test `test_text_padding_applied_to_list_labels` is missing the required docstring format. Should include feature and property information.

- Line 583-597: Property test `test_text_padding_applied_to_table_labels` is missing the required docstring format. Should include feature and property information.

- Line 608-626: Property test `test_padding_applied_to_container_only` is missing the required docstring format. Should include feature and property information.

- Line 628-651: Property test `test_padding_and_text_padding_independent` is missing the required docstring format. Should include feature and property information.

- Line 653-676: Property test `test_padding_change_affects_container_only` is missing the required docstring format. Should include feature and property information.

- Line 686-698: Property test `test_label_padding_setter_updates_text_padding` is missing the required docstring format. Should include feature and property information.

- Line 700-709: Property test `test_label_padding_getter_returns_text_padding` is missing the required docstring format. Should include feature and property information.

- Line 711-723: Property test `test_text_padding_setter_updates_label_padding` is missing the required docstring format. Should include feature and property information.

- Line 725-746: Property test `test_bidirectional_synchronization` is missing the required docstring format. Should include feature and property information.

- Line 748-760: Test `test_default_values_synchronized` is not a property test (doesn't use @given), so it doesn't need the property test docstring format. This is correct.

### test_performance.py

- Line 63-70: Property test `test_color_change_preserves_widget_tree` has an incorrect strategy classification. The test uses `st.tuples(st.floats(...), st.floats(...), st.floats(...), st.floats(...))` which is a combination strategy (tuple of 4 float strategies), but the comment says `# Complex strategy: 20 examples (adequate coverage)`. According to guidelines section "Property-Based Testing Optimization", combination strategies should use the format `# Combination strategy: [N] examples (combination coverage)`.

- Line 94-101: Property test `test_color_change_updates_descendant_labels` has an incorrect strategy classification. The test uses `st.tuples(st.floats(...), st.floats(...), st.floats(...), st.floats(...))` which is a combination strategy, but the comment says `# Complex strategy: 20 examples (adequate coverage)`. Should be `# Combination strategy: 20 examples (combination coverage)`.

- Line 341-354: Property test `test_multiple_style_changes_preserve_widget_tree` uses a combination strategy with 5 different strategies (floats, tuples, sampled_from, sampled_from, floats) but the comment says `# Complex strategy: 20 examples (adequate coverage)`. According to guidelines section "Property-Based Testing Optimization", this is a combination strategy and should use the format `# Combination strategy: 20 examples (combination coverage)`.

- Line 349-350: The test uses `st.sampled_from(['left', 'center', 'right'])` which is a small finite strategy with 3 values, but it's combined with other strategies. When part of a combination strategy, the overall strategy should be classified as "Combination strategy" not "Complex strategy".

- Line 350-351: The test uses `st.sampled_from(['top', 'middle', 'bottom'])` which is a small finite strategy with 3 values. Same issue as above - it's part of a combination strategy.

- Line 383-398: Property test `test_disabled_color_switching` uses `st.tuples(st.floats(...), st.floats(...), st.floats(...), st.floats(...))` twice which is a combination strategy (two 4-float tuples combined), but the comment says `# Complex strategy: 20 examples (adequate coverage)`. Should be `# Combination strategy: 20 examples (combination coverage)`.

- Line 12-15: Unused imports `BoxLayout`, `Label`, `Widget`, and `GridLayout` from kivy.uix are imported but never used in the test file. According to guidelines section "Best Practices", unused imports should be removed to keep the code clean and maintainable.

- Line 317-339: Test `test_font_name_structure_property_rebuilds_tree` has a docstring saying "Changing font_name (structure property) rebuilds the widget tree" but according to guidelines section "Rebuild Contract Testing", font_name is listed as a style-only property that updates existing widgets without rebuilding (line 201 in TESTING.md). The test implementation calls `force_rebuild()` and verifies a rebuild occurred, but this contradicts the guidelines which state font_name should be a style-only property. Either the test is incorrect or the guidelines need clarification.

### test_rebuild_scheduling.py

No deviations found.

### test_rebuild_semantics.py

- Line 311-312: Property test `test_style_property_changes_preserve_widget_identities` has a standardized comment `# Combination strategy: 100 examples (combination coverage)` but the strategy uses 8 different parameters (markdown_text, base_font_size, color, halign, valign, disabled, disabled_color, base_direction, line_height). According to guidelines section "Property-Based Testing Optimization", combination strategies should have their max_examples capped at 50, not 100. The comment should be `# Combination strategy: 50 examples (combination coverage)` or the max_examples should be reduced to 50.

- Line 311-312: Property test `test_style_property_changes_preserve_widget_identities` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring includes feature and property information but is missing the `**Validates: Requirements X.Y**` section.

- Line 520-521: Property test `test_style_property_values_propagate_to_descendants` has a standardized comment `# Combination strategy: 100 examples (combination coverage)` but the strategy uses 5 different parameters (markdown_text, color, halign, valign, line_height, base_direction). According to guidelines section "Property-Based Testing Optimization", combination strategies should have their max_examples capped at 50, not 100. The comment should be `# Combination strategy: 50 examples (combination coverage)` or the max_examples should be reduced to 50.

- Line 520-521: Property test `test_style_property_values_propagate_to_descendants` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring includes feature and property information but is missing the `**Validates: Requirements X.Y**` section.

- Line 775-776: Property test `test_text_change_rebuilds_widget_tree_pbt` has a standardized comment `# Complex strategy: 100 examples (adequate coverage)` but the strategy uses `simple_markdown_document()` twice (initial_text and new_text), which is a combination strategy. According to guidelines section "Property-Based Testing Optimization", combination strategies should use the format `# Combination strategy: [N] examples (combination coverage)` and should be capped at 50 examples.

- Line 775-776: Property test `test_text_change_rebuilds_widget_tree_pbt` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring includes feature and property information but is missing the `**Validates: Requirements X.Y**` section.

- Line 822-823: Property test `test_font_name_change_rebuilds_widget_tree_pbt` has a standardized comment `# Complex strategy: 100 examples (adequate coverage)` but the strategy uses `simple_markdown_document()` and `st.sampled_from(...)`, which is a combination strategy. According to guidelines section "Property-Based Testing Optimization", combination strategies should use the format `# Combination strategy: [N] examples (combination coverage)` and should be capped at 50 examples.

- Line 822-823: Property test `test_font_name_change_rebuilds_widget_tree_pbt` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring includes feature and property information but is missing the `**Validates: Requirements X.Y**` section.

- Line 869-870: Property test `test_link_style_change_rebuilds_widget_tree_pbt` has a standardized comment `# Complex strategy: 100 examples (adequate coverage)` but the strategy uses `simple_markdown_document()` and `st.sampled_from(...)`, which is a combination strategy. According to guidelines section "Property-Based Testing Optimization", combination strategies should use the format `# Combination strategy: [N] examples (combination coverage)` and should be capped at 50 examples.

- Line 869-870: Property test `test_link_style_change_rebuilds_widget_tree_pbt` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring includes feature and property information but is missing the `**Validates: Requirements X.Y**` section.

- Line 944-945: Property test `test_root_id_preserved_across_style_property_changes` has a standardized comment `# Combination strategy: 100 examples (combination coverage)` but the strategy uses 6 different parameters (markdown_text, base_font_size, color, halign, valign, line_height, disabled). According to guidelines section "Property-Based Testing Optimization", combination strategies should have their max_examples capped at 50, not 100. The comment should be `# Combination strategy: 50 examples (combination coverage)` or the max_examples should be reduced to 50.

- Line 944-945: Property test `test_root_id_preserved_across_style_property_changes` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring includes feature and property information but is missing the `**Validates: Requirements X.Y**` section.

- Line 990-991: Property test `test_root_id_preserved_across_structure_property_changes` has a standardized comment `# Combination strategy: 100 examples (combination coverage)` but the strategy uses 5 different parameters (initial_text, new_text, font_name, link_style, strict_label_mode, render_mode). According to guidelines section "Property-Based Testing Optimization", combination strategies should have their max_examples capped at 50, not 100. The comment should be `# Combination strategy: 50 examples (combination coverage)` or the max_examples should be reduced to 50.

- Line 990-991: Property test `test_root_id_preserved_across_structure_property_changes` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring includes feature and property information but is missing the `**Validates: Requirements X.Y**` section.

- Line 1047-1048: Property test `test_root_id_preserved_across_mixed_property_changes` has a standardized comment `# Combination strategy: 100 examples (combination coverage)` but the strategy uses 5 different parameters (markdown_text, base_font_size, color, font_name, link_style). According to guidelines section "Property-Based Testing Optimization", combination strategies should have their max_examples capped at 50, not 100. The comment should be `# Combination strategy: 50 examples (combination coverage)` or the max_examples should be reduced to 50.

- Line 1047-1048: Property test `test_root_id_preserved_across_mixed_property_changes` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring includes feature and property information but is missing the `**Validates: Requirements X.Y**` section.

### test_refactoring_properties.py

No deviations found.

### test_rtl_alignment.py

No deviations found.

### test_serialization.py

- Line 115-117: Property test `test_heading_round_trip` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring only says "Heading round-trips through parse-serialize-parse." without the required feature and property information.

- Line 134-136: Property test `test_paragraph_round_trip` is missing the required docstring format. Should include feature and property information following the format `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**`.

- Line 158-160: Property test `test_bold_round_trip` is missing the required docstring format. Should include feature and property information.

- Line 174-176: Property test `test_italic_round_trip` is missing the required docstring format. Should include feature and property information.

- Line 190-192: Property test `test_link_round_trip` is missing the required docstring format. Should include feature and property information.

- Line 206-208: Property test `test_document_round_trip` is missing the required docstring format. Should include feature and property information.

- Line 504-506: Property test `test_code_serialization_round_trip_property` has an incorrect strategy classification. The test uses two separate text strategies (`st.text(min_size=0, max_size=200)` for code_content and `st.text(alphabet=st.characters(whitelist_categories=('L', 'N')), min_size=0, max_size=20)` for language), which is a combination strategy (multiple @given arguments), but the comment says `# Complex strategy: 20 examples (adequate coverage)`. According to guidelines section "Property-Based Testing Optimization", combination strategies should use the format `# Combination strategy: [N] examples (combination coverage)`.

### test_shared_infrastructure.py

- Line 53: Property test `test_markdown_paragraph_strategy_generates_valid_paragraphs` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring only says "Paragraph strategy generates valid paragraph text." without the required feature and property information.

- Line 65: Property test `test_markdown_bold_strategy_generates_valid_bold_text` is missing the required docstring format. Should include feature and property information following the format `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**`.

- Line 74: Property test `test_markdown_italic_strategy_generates_valid_italic_text` is missing the required docstring format. Should include feature and property information.

- Line 85: Property test `test_markdown_link_strategy_generates_valid_links` is missing the required docstring format. Should include feature and property information.

- Line 98: Property test `test_simple_markdown_document_strategy_generates_valid_documents` is missing the required docstring format. Should include feature and property information.

- Line 110: Property test `test_color_strategy_generates_valid_colors` is missing the required docstring format. Should include feature and property information.

- Line 125: Property test `test_text_padding_strategy_generates_valid_padding` is missing the required docstring format. Should include feature and property information.

- Line 149: A stray comment `# Complex strategy: 30 examples (adequate coverage)` appears on line 149 that doesn't correspond to any @settings decorator. This is a misplaced comment that should be removed.

- Line 181: Property test `test_colors_equal_function_available` is missing the required docstring format. Should include feature and property information following the format `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**`.

- Line 195: Property test `test_padding_equal_function_available` is missing the required docstring format. Should include feature and property information.

- Line 209: Property test `test_floats_equal_function_available` is missing the required docstring format. Should include feature and property information.

### test_shortening_and_coordinate.py

- Line 37: Property test `test_shorten_forwarded_to_paragraph` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring only says "shorten property is forwarded to paragraph Labels." without the required feature and property information.

- Line 51: Property test `test_shorten_forwarded_to_heading` is missing the required docstring format. Should include feature and property information following the format `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**`.

- Line 65: Property test `test_shorten_forwarded_to_list_items` is missing the required docstring format. Should include feature and property information.

- Line 80: Property test `test_shorten_forwarded_to_table_cells` is missing the required docstring format. Should include feature and property information.

- Line 132: Property test `test_split_str_forwarded_to_paragraph` is missing the required docstring format. Should include feature and property information.

- Line 146: Property test `test_split_str_forwarded_to_heading` is missing the required docstring format. Should include feature and property information.

- Line 160: Property test `test_max_lines_forwarded_to_paragraph` is missing the required docstring format. Should include feature and property information.

- Line 176: Property test `test_max_lines_forwarded_to_heading` is missing the required docstring format. Should include feature and property information.

- Line 190: Property test `test_max_lines_forwarded_to_list_items` is missing the required docstring format. Should include feature and property information.

- Line 207: Property test `test_ellipsis_options_forwarded_to_paragraph` is missing the required docstring format. Should include feature and property information.

- Line 223: Property test `test_ellipsis_options_forwarded_to_heading` is missing the required docstring format. Should include feature and property information.

- Line 239: Property test `test_ellipsis_options_forwarded_to_list_items` is missing the required docstring format. Should include feature and property information.

- Line 256: Property test `test_ellipsis_options_forwarded_to_table_cells` is missing the required docstring format. Should include feature and property information.

- Line 285: Property test `test_all_shortening_properties_forwarded_together` is missing the required docstring format. Should include feature and property information.

- Line 323: Test name `test_shorten_change_updates_value` uses "updates_value" naming but docstring says "triggers widget rebuild with new value". According to guidelines section "Test Naming Conventions", tests that verify rebuild behavior should use `test_*_triggers_rebuild_*` naming, while tests that verify value changes without rebuild verification should use `test_*_updates_value_*` naming. The test calls `label.force_rebuild()` and verifies the new value, which is inconsistent with the naming convention. The name should be `test_shorten_change_triggers_rebuild` or similar.

- Line 323: Property test `test_shorten_change_updates_value` is missing the required docstring format. Should include feature and property information.

- Line 416: Property test `test_link_produces_ref_markup_for_translation` is missing the required docstring format. Should include feature and property information.

- Line 453: Property test `test_multiple_links_produce_ref_markup` is missing the required docstring format. Should include feature and property information.

- Line 624: Property test `test_ref_markup_updates_when_text_changes` is missing the required docstring format. Should include feature and property information.

- Line 662: Property test `test_coordinate_translation_math` is missing the required docstring format. Should include feature and property information.

- Line 692: Property test `test_anchor_translation_math` is missing the required docstring format. Should include feature and property information.

- Line 1002: Property test `test_property_refs_coordinate_translation_math` has a docstring that includes feature and property information but is missing the `**Validates: Requirements X.Y**` section. According to guidelines section "Property-Based Testing", property tests should include both feature/property information and validation requirements.

- Line 1342: Property test `test_property_anchors_coordinate_translation_math` has a docstring that includes feature and property information but is missing the `**Validates: Requirements X.Y**` section. Should include validation requirements.

- Line 360-408: Helper methods `_find_labels_with_refs`, `_find_labels_with_ref_markup`, and `_get_widget_offset` are defined in the test class. According to guidelines section "Helper Functions", helper functions should be added to `test_utils.py` and imported, not duplicated in test files. These helpers are used in multiple tests and should be consolidated in test_utils.py.

- Line 615-623: Property test `test_ref_markup_updates_when_text_changes` uses two text strategies which is a combination strategy. The comment says `# Complex strategy: 20 examples (adequate coverage)` but according to guidelines section "Property-Based Testing Optimization", this should be classified as a "Combination strategy" with the comment `# Combination strategy: 20 examples (combination coverage)`.

- Line 656-661: Property test `test_coordinate_translation_math` uses four float strategies which is a combination strategy. The comment says `# Complex strategy: 20 examples (adequate coverage)` but should be `# Combination strategy: 20 examples (combination coverage)` according to guidelines.

- Line 688-691: Property test `test_anchor_translation_math` uses two float strategies which is a combination strategy. The comment says `# Complex strategy: 20 examples (adequate coverage)` but should be `# Combination strategy: 20 examples (combination coverage)` according to guidelines.

- Line 983-1004: Property test `test_property_refs_coordinate_translation_math` uses 12 float parameters which is a combination strategy. The comment says `# Complex strategy with 12 float parameters: 100 examples for adequate coverage` but according to guidelines section "Property-Based Testing Optimization", combination strategies should use the format `# Combination strategy: [N] examples (combination coverage)` and should be capped at 50 examples, not 100.

- Line 1324-1343: Property test `test_property_anchors_coordinate_translation_math` uses 10 float parameters which is a combination strategy. The comment says `# Complex strategy with 10 float parameters: 100 examples for adequate coverage` but according to guidelines section "Property-Based Testing Optimization", combination strategies should use the format `# Combination strategy: [N] examples (combination coverage)` and should be capped at 50 examples, not 100.

### test_sizing_behavior.py

- Line 31-34: Property test `test_auto_size_hint_enabled_sets_none` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring only says "With auto_size_height=True, size_hint_y is None for auto-sizing." without the required feature and property information.

- Line 49-52: Property test `test_height_bound_to_minimum` is missing the required docstring format. Should include feature and property information following the format `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**`.

- Line 71-74: Property test `test_more_content_means_more_height_potential` is missing the required docstring format. Should include feature and property information.

- Line 96-99: Property test `test_auto_size_height_true_sets_size_hint_y_none` is missing the required docstring format. Should include feature and property information.

- Line 107-110: Property test `test_auto_size_height_true_binds_height_to_minimum` is missing the required docstring format. Should include feature and property information.

- Line 134-137: Property test `test_auto_size_height_true_ignores_user_size_hint_y` is missing the required docstring format. Should include feature and property information.

- Line 164-167: Property test `test_auto_size_height_false_preserves_default_size_hint_y` is missing the required docstring format. Should include feature and property information.

- Line 178-182: Property test `test_auto_size_height_false_preserves_user_size_hint_y` is missing the required docstring format. Should include feature and property information.

- Line 197-200: Property test `test_auto_size_height_false_no_height_binding` is missing the required docstring format. Should include feature and property information.

- Line 224-227: Property test `test_toggle_true_to_false_restores_size_hint_y` is missing the required docstring format. Should include feature and property information.

- Line 246-249: Property test `test_toggle_false_to_true_sets_size_hint_y_none` is missing the required docstring format. Should include feature and property information.

- Line 268-272: Property test `test_toggle_preserves_user_size_hint_y` is missing the required docstring format. Should include feature and property information.

- Line 303-306: Property test `test_multiple_toggles_maintain_consistency` is missing the required docstring format. Should include feature and property information.

- Line 340-343: Property test `test_strict_mode_preserves_default_size_hint_y` is missing the required docstring format. Should include feature and property information.

- Line 354-358: Property test `test_strict_mode_preserves_user_size_hint_y` is missing the required docstring format. Should include feature and property information.

- Line 373-376: Property test `test_strict_mode_height_not_bound_to_minimum` is missing the required docstring format. Should include feature and property information.

- Line 420-423: Property test `test_strict_mode_toggle_from_false_to_true` is missing the required docstring format. Should include feature and property information.

- Line 442-445: Property test `test_strict_mode_toggle_from_true_to_false` is missing the required docstring format. Should include feature and property information.

- Line 465-469: Property test `test_strict_mode_toggle_preserves_user_size_hint_y` is missing the required docstring format. Should include feature and property information.

- Line 493-496: Property test `test_strict_mode_overrides_auto_size_height` is missing the required docstring format. Should include feature and property information.

- Line 509-512: Property test `test_strict_mode_ignores_auto_size_height_changes` is missing the required docstring format. Should include feature and property information.

- Line 527-530: Property test `test_strict_mode_updates_value` is missing the required docstring format. Should include feature and property information.

- Line 546-549: Property test `test_multiple_strict_mode_toggles_maintain_consistency` is missing the required docstring format. Should include feature and property information.

- Line 11-14: Unused imports `BoxLayout`, `Label`, `Widget`, and `GridLayout` from kivy.uix are imported but never used in the test file. According to guidelines section "Best Practices", unused imports should be removed to keep the code clean and maintainable.

### test_strategy_classification.py

- Line 10-12: The file modifies `sys.path` to add the tools directory for imports. According to guidelines section "Test File Structure", test files should use standard import patterns. The recommended approach would be to ensure the tools directory is properly structured as a package or to use a different import strategy rather than modifying sys.path at runtime.

- Line 28-30: Property test `test_boolean_strategy_classification` uses `st.just('st.booleans()')` which is a small finite strategy with 1 value, but the comment says `# Small finite strategy: 1 examples (input space size: 1)`. While the comment format is correct, the rationale "input space size: 1" is misleading because the test is actually testing the classification of boolean strategies, which should have an input space size of 2. The comment should clarify that this is testing the classification logic, not the actual boolean strategy itself.

- Line 31-35: Property test `test_boolean_strategy_classification` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring includes property information but is missing the `**Validates: Requirements X.Y**` section.

- Line 42-44: Property test `test_small_integer_range_classification` has a correct comment format `# Combination strategy: 50 examples (combination coverage)` for the combination strategy used. This is correct.

- Line 45-55: Property test `test_small_integer_range_classification` is missing the required docstring format. Should include feature and property information following the format `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**`.

- Line 57-59: Property test `test_small_sampled_from_classification` has a correct comment format for the strategy used. This is correct.

- Line 60-69: Property test `test_small_sampled_from_classification` is missing the required docstring format. Should include feature and property information.

- Line 71-73: Property test `test_medium_finite_classification` has a correct comment format `# Medium finite strategy: 40 examples (adequate finite coverage)` for the strategy used. This is correct.

- Line 74-81: Property test `test_medium_finite_classification` is missing the required docstring format. Should include feature and property information.

- Line 83-85: Property test `test_complex_strategy_classification` has a correct comment format `# Small finite strategy: 3 examples (testing complex strategy classification)` for the strategy used. This is correct.

- Line 86-92: Property test `test_complex_strategy_classification` is missing the required docstring format. Should include feature and property information.

- Line 116-118: Property test `test_small_finite_uses_input_space_size` has a correct comment format. This is correct.

- Line 119-128: Property test `test_small_finite_uses_input_space_size` is missing the required docstring format. Should include feature and property information.

- Line 130-132: Property test `test_sampled_from_uses_list_length` has a correct comment format. This is correct.

- Line 133-141: Property test `test_sampled_from_uses_list_length` is missing the required docstring format. Should include feature and property information.

- Line 150-152: Property test `test_medium_finite_capped_appropriately` has a correct comment format. This is correct.

- Line 153-160: Property test `test_medium_finite_capped_appropriately` is missing the required docstring format. Should include feature and property information.

- Line 163-165: Property test `test_complex_strategy_uses_complexity_based_examples` has a correct comment format. This is correct.

- Line 166-185: Property test `test_complex_strategy_uses_complexity_based_examples` is missing the required docstring format. Should include feature and property information.

- Line 197-199: Property test `test_combination_uses_product_formula` has a correct comment format. This is correct.

- Line 200-216: Property test `test_combination_uses_product_formula` is missing the required docstring format. Should include feature and property information.

- Line 236-238: Property test `test_large_combination_capped_at_fifty` has a correct comment format. This is correct.

- Line 239-251: Property test `test_large_combination_capped_at_fifty` is missing the required docstring format. Should include feature and property information.

- Line 297-299: Property test `test_boolean_over_testing_detected` has a correct comment format. This is correct.

- Line 300-313: Property test `test_boolean_over_testing_detected` is missing the required docstring format. Should include feature and property information.

- Line 315-317: Property test `test_small_finite_over_testing_detected` has a correct comment format. This is correct.

- Line 318-326: Property test `test_small_finite_over_testing_detected` is missing the required docstring format. Should include feature and property information.

### test_text_properties.py

- Line 21: Custom strategy `unicode_errors_strategy` is defined in the test file. According to guidelines section "Helper Functions", custom Hypothesis strategies should be added to test_utils.py and imported, not duplicated in test files.

- Line 31: Property test `test_text_size_width_stored_correctly` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring only says "text_size width is stored correctly on MarkdownLabel." without the required feature and property information.

- Line 42: Property test `test_text_size_property_stored_correctly` is missing the required docstring format. Should include feature and property information following the format `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**`.

- Line 56: Property test `test_text_size_change_updates_value` is missing the required docstring format. Should include feature and property information.

- Line 56: Test name `test_text_size_change_updates_value` uses "updates_value" naming but docstring says "triggers widget rebuild". According to guidelines section "Test Naming Conventions", tests that verify rebuild behavior should use `test_*_triggers_rebuild_*` naming, while tests that verify value changes without rebuild verification should use `test_*_updates_value_*` naming. The test doesn't verify whether a rebuild occurred (no widget ID comparison), so the docstring is inconsistent with the naming convention.

- Line 88: Property test `test_text_size_with_width_passed_to_renderer` is missing the required docstring format. Should include feature and property information.

- Line 108: A decorator comment `# Complex strategy: 50 examples (adequate coverage)` is placed between the class definition and its docstring. According to guidelines, such comments are meant to be used with @settings decorators, not as standalone comments in class bodies. The comment should be removed as it doesn't correspond to any decorator.

- Line 115: Property test `test_text_size_height_forwarded_to_paragraph` is missing the required docstring format. Should include feature and property information.

- Line 131: Property test `test_text_size_height_forwarded_to_heading` is missing the required docstring format. Should include feature and property information.

- Line 148: Property test `test_text_size_both_width_and_height_forwarded` is missing the required docstring format. Should include feature and property information.

- Line 167: Property test `test_valign_forwarded_with_height` is missing the required docstring format. Should include feature and property information.

- Line 183: Property test `test_text_size_height_forwarded_to_table_cells` is missing the required docstring format. Should include feature and property information.

- Line 209: Property test `test_text_size_height_none_preserves_auto_sizing` is missing the required docstring format. Should include feature and property information.

- Line 227: Property test `test_text_size_width_only_preserves_height_none` is missing the required docstring format. Should include feature and property information.

- Line 269: Property test `test_text_size_height_change_updates_labels` is missing the required docstring format. Should include feature and property information.

- Line 293: Property test `test_text_size_height_to_none_updates_labels` is missing the required docstring format. Should include feature and property information.

- Line 318: Property test `test_text_size_none_to_height_updates_labels` is missing the required docstring format. Should include feature and property information.

- Line 352: Property test `test_unicode_errors_stored_correctly` is missing the required docstring format. Should include feature and property information.

- Line 363: Property test `test_unicode_errors_applied_to_paragraph` is missing the required docstring format. Should include feature and property information.

- Line 379: Property test `test_unicode_errors_applied_to_heading` is missing the required docstring format. Should include feature and property information.

- Line 395: Property test `test_unicode_errors_applied_to_code_block` is missing the required docstring format. Should include feature and property information.

- Line 412: Property test `test_unicode_errors_applied_to_list_items` is missing the required docstring format. Should include feature and property information.

- Line 429: Property test `test_unicode_errors_applied_to_table_cells` is missing the required docstring format. Should include feature and property information.

- Line 446: Property test `test_unicode_errors_change_updates_value` is missing the required docstring format. Should include feature and property information.

- Line 446: Test name `test_unicode_errors_change_updates_value` uses "updates_value" naming but docstring says "triggers widget rebuild with new value". According to guidelines section "Test Naming Conventions", tests that verify rebuild behavior should use `test_*_triggers_rebuild_*` naming. The test calls `label.force_rebuild()` and verifies the new value, which is inconsistent with the naming convention.

- Line 488: Property test `test_strip_stored_correctly` is missing the required docstring format. Should include feature and property information.

- Line 499: Property test `test_strip_applied_to_paragraph` is missing the required docstring format. Should include feature and property information.

- Line 515: Property test `test_strip_applied_to_heading` is missing the required docstring format. Should include feature and property information.

- Line 531: Property test `test_strip_applied_to_code_block` is missing the required docstring format. Should include feature and property information.

- Line 548: Property test `test_strip_applied_to_list_items` is missing the required docstring format. Should include feature and property information.

- Line 565: Property test `test_strip_applied_to_table_cells` is missing the required docstring format. Should include feature and property information.

- Line 582: Property test `test_strip_change_updates_value` is missing the required docstring format. Should include feature and property information.

- Line 582: Test name `test_strip_change_updates_value` uses "updates_value" naming but docstring says "triggers widget rebuild with new value". According to guidelines section "Test Naming Conventions", tests that verify rebuild behavior should use `test_*_triggers_rebuild_*` naming. The test calls `label.force_rebuild()` and verifies the new value, which is inconsistent with the naming convention.

### test_texture_render_mode.py

- Line 23-31: Helper method `find_images` is defined in the test file. According to guidelines section "Helper Functions", helper functions should be added to `test_utils.py` and imported, not duplicated in test files. This helper should be moved to test_utils.py for consistency with other test files.

- Line 50: Test `test_texture_mode_creates_image_widget` is not a property test (uses @pytest.mark.parametrize), so it doesn't need the property test docstring format. However, the docstring includes feature and property information but is missing the `**Validates: Requirements X.Y**` section. According to guidelines section "Property-Based Testing", while property tests need the full format, regular tests should still be clear about what they validate.

- Line 68: Test `test_texture_mode_with_empty_text_no_image` is not a property test. The docstring includes feature and property information but is missing the `**Validates: Requirements X.Y**` section. Same issue as line 50.

- Line 86: Test `test_widgets_mode_no_image_widget` is not a property test. The docstring includes feature and property information but is missing the `**Validates: Requirements X.Y**` section. Same issue as line 50.

- Line 105: Test `test_render_mode_property_values` is not a property test. The docstring includes feature and property information but is missing the `**Validates: Requirements X.Y**` section. Same issue as line 50.

- Line 115: Test `test_default_render_mode_is_widgets` is not a property test. The docstring includes feature and property information but is missing the `**Validates: Requirements X.Y**` section. Same issue as line 50.

- Line 136: Test `test_aggregated_refs_populated_in_texture_mode` is not a property test. The docstring includes feature and property information but is missing the `**Validates: Requirements X.Y**` section. Same issue as line 50.

- Line 156: Test `test_widgets_mode_no_aggregated_refs` is not a property test. The docstring includes feature and property information but is missing the `**Validates: Requirements X.Y**` section. Same issue as line 50.

- Line 179: Test `test_multiple_links_collected` is not a property test. The docstring includes feature and property information but is missing the `**Validates: Requirements X.Y**` section. Same issue as line 50.

- Line 216: Test `test_inside_zone_dispatch` is not a property test. The docstring includes feature and property information but is missing the `**Validates: Requirements X.Y**` section. Same issue as line 50.

- Line 279: Property test `test_property_inside_zone_dispatch` has the required feature and property information in the docstring but is missing the `**Validates: Requirements X.Y**` section. According to guidelines section "Property-Based Testing", property tests should include both feature/property information and validation requirements.

- Line 330: Test `test_outside_zone_no_dispatch` is not a property test. The docstring includes feature and property information but is missing the `**Validates: Requirements X.Y**` section. Same issue as line 50.

- Line 387: Property test `test_property_outside_zone_no_dispatch` has the required feature and property information in the docstring but is missing the `**Validates: Requirements X.Y**` section. Same issue as line 279.

- Line 436: Test `test_multiple_zones_first_match` is not a property test. The docstring includes feature and property information but is missing the `**Validates: Requirements X.Y**` section. Same issue as line 50.

- Line 483: Test `test_multiple_zones_non_overlapping` is not a property test. The docstring includes feature and property information but is missing the `**Validates: Requirements X.Y**` section. Same issue as line 50.
