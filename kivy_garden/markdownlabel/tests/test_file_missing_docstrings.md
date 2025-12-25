### test_clipping_behavior.py

- Line 50: Property test `test_text_size_height_enables_clipping` is missing the required docstring format for property-based tests. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings.

- Line 74: Property test `test_strict_label_mode_with_fixed_height_enables_clipping` is missing the required docstring format for property-based tests. Should include feature and property information.

- Line 94: Property test `test_clipping_container_height_matches_text_size` is missing the required docstring format for property-based tests. Should include feature and property information.

- Line 123: Property test `test_heading_content_clipped_when_height_constrained` is missing the required docstring format for property-based tests. Should include feature and property information.

- Line 186: Property test `test_no_clipping_when_text_size_height_none` is missing the required docstring format for property-based tests. Should include feature and property information.

- Line 210: Property test `test_no_clipping_when_strict_label_mode_false` is missing the required docstring format for property-based tests. Should include feature and property information.

- Line 234: Property test `test_content_added_directly_when_unconstrained` is missing the required docstring format for property-based tests. Should include feature and property information.

- Line 253: Property test `test_heading_expands_naturally_when_unconstrained` is missing the required docstring format for property-based tests. Should include feature and property information.

- Line 277: Property test `test_text_size_width_only_no_clipping` is missing the required docstring format for property-based tests. Should include feature and property information.

### test_color_properties.py

- Line 34: Property test `test_color_applied_to_paragraph` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring only says "color is applied to paragraph Labels." without the required feature and property information.

- Line 49: Property test `test_color_applied_to_heading` is missing the required docstring format. Should include feature and property information following the format `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**`.

- Line 64: Property test `test_code_block_preserves_light_color` is missing the required docstring format. Should include feature and property information.

- Line 82: Property test `test_color_change_updates_value` is missing the required docstring format. Should include feature and property information.

- Line 105: Property test `test_color_applied_to_list_items` is missing the required docstring format. Should include feature and property information.

- Line 121: Property test `test_color_applied_to_table_cells` is missing the required docstring format. Should include feature and property information.

- Line 137: Property test `test_mixed_content_color_separation` is missing the required docstring format. Should include feature and property information.

### test_comment_format.py

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

### test_comment_standardizer.py

- Line 42: Property test `test_boolean_strategy_comments_reference_true_false_coverage` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring only says "Boolean strategy comments always reference True/False coverage." without the required feature and property information.

- Line 306: Property test `test_finite_strategy_comments_reference_input_space_size` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring only says "Finite strategy comments reference input space size in rationale." without the required feature and property information.

- Line 373: Property test `test_sampled_from_finite_strategy_documentation` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring only says "Sampled_from finite strategies are properly documented." without the required feature and property information.

- Line 596: Property test `test_execution_time_performance_rationale_documented` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring only says "Execution time performance rationale is properly documented." without the required feature and property information.

- Line 661: Property test `test_explicit_performance_comments_detected` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring only says "Explicit performance comments are properly detected and preserved." without the required feature and property information.

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

### test_documentation_compliance.py

- Line 19-23: Test `test_custom_values_are_documented` is a meta-test (marked with `@pytest.mark.test_tests`) but its docstring is missing the required format for property-based tests. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. While this is a meta-test that validates the test suite itself, it still uses property-based testing concepts and should follow the documentation format.

- Line 126-127: Property test `test_custom_value_detection_property` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring only says "Property test for custom value detection logic." without the required feature and property information.

- Line 141-142: Property test `test_comment_detection_property` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring only says "Property test for explanatory comment detection." without the required feature and property information.

### test_file_analyzer.py

- Line 298-300: Property test `test_rationale_generation_for_strategy_types` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring only says "Generates appropriate rationales for different strategy types." without the required feature and property information.

### test_font_properties.py

- Line 287: Property test `test_line_height_applied_to_all_content_types` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring only says "line_height is applied to all content types including code." without the required feature and property information.

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

### test_helper_availability.py

- Line 36: Property test `test_widget_traversal_helpers_available` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring only says "For any markdown content, widget traversal helpers should be available and functional." without the required feature and property information format.

- Line 62: Property test `test_comparison_helpers_available` is missing the required docstring format. Should include feature and property information following the format `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**`.

- Line 78: Property test `test_padding_comparison_helpers_available` is missing the required docstring format. Should include feature and property information.

- Line 95: Property test `test_float_comparison_helpers_available` is missing the required docstring format. Should include feature and property information.

- Line 111: Property test `test_rebuild_detection_helpers_available` is missing the required docstring format. Should include feature and property information.

- Line 189: Property test `test_no_duplicate_find_labels_recursive_implementations` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring only says "For any test file, there should be no duplicate _find_labels_recursive implementations." without the required feature and property information format.

- Line 223: Property test `test_no_duplicate_collect_widget_ids_implementations` is missing the required docstring format. Should include feature and property information.

- Line 257: Property test `test_all_test_files_import_from_test_utils` is missing the required docstring format. Should include feature and property information.

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

- Line 794-845: Property test `test_table_preserves_column_alignments` is missing the required docstring format. Should include feature and property information.

- Line 863-874: Property test `test_cell_stores_alignment_metadata` is missing the required docstring format. Should include feature and property information.

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

- Line 293: Property test `test_ellipsis_options_property_accepted_and_stored` is missing the required docstring format. Should include feature and property information.

- Line 305: Property test `test_all_noop_properties_together_accepted_and_stored` is missing the required docstring format. Should include feature and property information.

- Line 329: Property test `test_mipmap_property_change_after_creation` is missing the required docstring format. Should include feature and property information.

- Line 338: Property test `test_outline_width_property_change_after_creation` is missing the required docstring format. Should include feature and property information.

- Line 350: Property test `test_outline_color_property_change_after_creation` is missing the required docstring format. Should include feature and property information.

- Line 362: Property test `test_text_language_property_change_after_creation` is missing the required docstring format. Should include feature and property information.

- Line 383: Property test `test_ellipsis_options_property_change_after_creation` is missing the required docstring format. Should include feature and property information.

- Line 397: Property test `test_advanced_noop_properties_do_not_affect_rendering` is missing the required docstring format. Should include feature and property information.

### test_padding_properties.py

- Line 44-60: Property test `test_single_padding_applied_uniformly` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring only says "Single padding value is applied uniformly to all sides." without the required feature and property information.

- Line 61-77: Property test `test_two_element_padding_applied_to_axes` is missing the required docstring format. Should include feature and property information following the format `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**`.

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

### test_serialization.py

- Line 115-117: Property test `test_heading_round_trip` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring only says "Heading round-trips through parse-serialize-parse." without the required feature and property information.

- Line 134-136: Property test `test_paragraph_round_trip` is missing the required docstring format. Should include feature and property information following the format `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**`.

- Line 158-160: Property test `test_bold_round_trip` is missing the required docstring format. Should include feature and property information.

- Line 174-176: Property test `test_italic_round_trip` is missing the required docstring format. Should include feature and property information.

- Line 190-192: Property test `test_link_round_trip` is missing the required docstring format. Should include feature and property information.

- Line 206-208: Property test `test_document_round_trip` is missing the required docstring format. Should include feature and property information.

### test_shared_infrastructure.py

- Line 53: Property test `test_markdown_paragraph_strategy_generates_valid_paragraphs` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring only says "Paragraph strategy generates valid paragraph text." without the required feature and property information.

- Line 65: Property test `test_markdown_bold_strategy_generates_valid_bold_text` is missing the required docstring format. Should include feature and property information following the format `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**`.

- Line 74: Property test `test_markdown_italic_strategy_generates_valid_italic_text` is missing the required docstring format. Should include feature and property information.

- Line 85: Property test `test_markdown_link_strategy_generates_valid_links` is missing the required docstring format. Should include feature and property information.

- Line 98: Property test `test_simple_markdown_document_strategy_generates_valid_documents` is missing the required docstring format. Should include feature and property information.

- Line 110: Property test `test_color_strategy_generates_valid_colors` is missing the required docstring format. Should include feature and property information.

- Line 125: Property test `test_text_padding_strategy_generates_valid_padding` is missing the required docstring format. Should include feature and property information.

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

- Line 323: Property test `test_shorten_change_updates_value` is missing the required docstring format. Should include feature and property information.

- Line 416: Property test `test_link_produces_ref_markup_for_translation` is missing the required docstring format. Should include feature and property information.

- Line 453: Property test `test_multiple_links_produce_ref_markup` is missing the required docstring format. Should include feature and property information.

- Line 624: Property test `test_ref_markup_updates_when_text_changes` is missing the required docstring format. Should include feature and property information.

- Line 662: Property test `test_coordinate_translation_math` is missing the required docstring format. Should include feature and property information.

- Line 692: Property test `test_anchor_translation_math` is missing the required docstring format. Should include feature and property information.

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

### test_strategy_classification.py

- Line 31-35: Property test `test_boolean_strategy_classification` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring includes property information but is missing the `**Validates: Requirements X.Y**` section.

- Line 45-55: Property test `test_small_integer_range_classification` is missing the required docstring format. Should include feature and property information following the format `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**`.

- Line 60-69: Property test `test_small_sampled_from_classification` is missing the required docstring format. Should include feature and property information.

- Line 74-81: Property test `test_medium_finite_classification` is missing the required docstring format. Should include feature and property information.

- Line 86-92: Property test `test_complex_strategy_classification` is missing the required docstring format. Should include feature and property information.

- Line 119-128: Property test `test_small_finite_uses_input_space_size` is missing the required docstring format. Should include feature and property information.

- Line 133-141: Property test `test_sampled_from_uses_list_length` is missing the required docstring format. Should include feature and property information.

- Line 153-160: Property test `test_medium_finite_capped_appropriately` is missing the required docstring format. Should include feature and property information.

- Line 166-185: Property test `test_complex_strategy_uses_complexity_based_examples` is missing the required docstring format. Should include feature and property information.

- Line 200-216: Property test `test_combination_uses_product_formula` is missing the required docstring format. Should include feature and property information.

- Line 239-251: Property test `test_large_combination_capped_at_fifty` is missing the required docstring format. Should include feature and property information.

- Line 300-313: Property test `test_boolean_over_testing_detected` is missing the required docstring format. Should include feature and property information.

- Line 318-326: Property test `test_small_finite_over_testing_detected` is missing the required docstring format. Should include feature and property information.

### test_text_properties.py

- Line 31: Property test `test_text_size_width_stored_correctly` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring only says "text_size width is stored correctly on MarkdownLabel." without the required feature and property information.

- Line 42: Property test `test_text_size_property_stored_correctly` is missing the required docstring format. Should include feature and property information following the format `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**`.

- Line 56: Property test `test_text_size_change_updates_value` is missing the required docstring format. Should include feature and property information.

- Line 88: Property test `test_text_size_with_width_passed_to_renderer` is missing the required docstring format. Should include feature and property information.

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

- Line 488: Property test `test_strip_stored_correctly` is missing the required docstring format. Should include feature and property information.

- Line 499: Property test `test_strip_applied_to_paragraph` is missing the required docstring format. Should include feature and property information.

- Line 515: Property test `test_strip_applied_to_heading` is missing the required docstring format. Should include feature and property information.

- Line 531: Property test `test_strip_applied_to_code_block` is missing the required docstring format. Should include feature and property information.

- Line 548: Property test `test_strip_applied_to_list_items` is missing the required docstring format. Should include feature and property information.

- Line 565: Property test `test_strip_applied_to_table_cells` is missing the required docstring format. Should include feature and property information.

- Line 582: Property test `test_strip_change_updates_value` is missing the required docstring format. Should include feature and property information.

### test_texture_sizing.py

- Line 42: Property test `test_texture_size_returns_tuple` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring only says "texture_size returns a list/tuple with two elements." without the required feature and property information.

- Line 56: Property test `test_texture_size_non_negative` is missing the required docstring format. Should include feature and property information following the format `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**`.

- Line 79: Property test `test_heading_creates_label_widget` is missing the required docstring format. Should include feature and property information.

- Line 95: Property test `test_paragraph_creates_label_widget` is missing the required docstring format. Should include feature and property information.

- Line 185: Property test `test_more_content_increases_texture_height` is missing the required docstring format. Should include feature and property information.

- Line 229: Property test `test_texture_size_accessible_for_all_content` is missing the required docstring format. Should include feature and property information.

- Line 280: Property test `test_texture_size_updates_on_text_change` is missing the required docstring format. Should include feature and property information.

- Line 327: Property test `test_all_heading_levels_create_label_widgets` is missing the required docstring format. Should include feature and property information.

- Line 376: Property test `test_texture_sizing_classes_grouped_together` is missing the required docstring format. Should include feature and property information.

- Line 410: Property test `test_module_focuses_on_texture_sizing` is missing the required docstring format. Should include feature and property information.

### tools/test_analysis/test_assertion_analyzer.py

- Line 100-107: Property test `test_value_change_test_naming_property` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring includes property information but is missing the feature and validation requirements sections.

- Line 149-150: Property test `test_assertion_classification_consistency` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring only says "Test that assertion classification is consistent across different test structures." without the required feature and validation requirements sections.

### tools/test_analysis/test_code_duplication_minimization.py

- Line 137-140: Property test `test_duplication_below_threshold` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring only says "Test suite should have code duplication below acceptable threshold." without the required feature and property information.

- Line 192-195: Property test `test_consolidation_reduces_duplication` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring only says "Consolidating duplicates should reduce overall duplication metrics." without the required feature and property information.

- Line 393-396: Property test `test_similarity_threshold_affects_detection` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring only says "Different similarity thresholds should affect duplicate detection." without the required feature and property information.

### tools/test_analysis/test_coverage_preservation.py

- Line 191-193: Property test `test_refactoring_preserves_coverage` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring only says "Refactoring operations should preserve or improve test coverage." without the required feature and property information.

- Line 316-318: Property test `test_test_count_preservation` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring only says "Refactoring should preserve or increase the number of tests." without the required feature and property information.

- Line 494-496: Property test `test_coverage_tolerance_reasonable` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring only says "Coverage tolerance should be reasonable for measurement variance." without the required feature and property information.

### tools/test_analysis/test_duplicate_detector.py

- Line 101-151: Property test `test_duplicate_detection_finds_duplicates` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring only says "Duplicate detector should find helper functions that appear in multiple files." without the required feature and property information.

- Line 153-197: Property test `test_detector_handles_no_duplicates` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring only says "Detector should handle files with no duplicate functions correctly." without the required feature and property information.

### tools/test_analysis/test_naming_convention_validator.py

- Line 181-228: Property test `test_file_level_consistency` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring only says "Test that naming consistency is checked at the file level." without the required feature and property information.

### tools/test_analysis/test_test_file_parser.py

- Line 94: Property test `test_rebuild_test_names_match_assertions` is missing the required docstring format. According to guidelines section "Property-Based Testing", property tests should include `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` in their docstrings. The current docstring only says "Tests with 'triggers_rebuild' in name should have rebuild assertions." without the required feature and property information.

- Line 134: Property test `test_parser_handles_valid_python_files` is missing the required docstring format. Should include feature and property information following the format `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**`.
