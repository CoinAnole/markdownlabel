# Deviations

## Deviations in test_label_compatibility.py

- Line 154: Imprecise rationale in Mixed finite/complex strategy comment (uses "~2")
- Line 291: Vague rationale missing specific finite_size and samples in Mixed finite/complex strategy comment
- Line 374: Vague rationale missing specific finite_size and samples in Mixed finite/complex strategy comment

## Deviations in test_advanced_compatibility.py

- Line 786: Wrong comment format for Combination strategy in test_disabled_change_triggers_rebuild

## Deviations in test_rebuild_scheduling.py

- Line 71: Imprecise rationale in Mixed finite/complex strategy comment (uses "~7")

## Deviations in test_rebuild_semantics.py

- Line 257: Incorrect rationale "(combination coverage)" for Mixed finite/complex strategy in test_style_property_changes_preserve_widget_tree

- Line 429: Incorrect rationale "(combination coverage)" for Mixed finite/complex strategy in test_style_property_values_propagate_to_descendants

- Line 699: Incorrect rationale "(input space size: 3)" for Mixed finite/complex strategy in test_font_name_change_triggers_rebuild_pbt

- Line 741: Incorrect rationale "(input space size: 2)" for Mixed finite/complex strategy in test_link_style_change_triggers_rebuild_pbt

- Line 795: Incorrect rationale "(combination coverage)" for Mixed finite/complex strategy in test_root_id_preserved_across_style_property_changes

- Line 837: Incorrect rationale "(combination coverage)" for Mixed finite/complex strategy in test_root_id_preserved_across_structure_property_changes

- Line 880: Incorrect rationale "(combination coverage)" for Mixed finite/complex strategy in test_root_id_preserved_across_mixed_property_changes

## Deviations in test_shortening_and_coordinate.py

- Line 291: Mixed finite/complex strategy comment uses vague "(finite × complex samples)" instead of specific "([finite_size] finite × [samples] complex samples)"
- Line 329: Boolean strategy comment incorrect for @given(st.booleans(), st.booleans()); should be Combination strategy for finite combination (space size: 4)

## Deviations in meta_tests/test_assertion_analyzer.py

- Line 156: [`# Combination strategy: 30 examples (combination coverage)`](kivy_garden/markdownlabel/tests/meta_tests/test_assertion_analyzer.py:156) incorrectly classifies mixed finite/complex strategy (st.sampled_from(5 items) + st.text()) in [`test_assertion_classification_consistency`](kivy_garden/markdownlabel/tests/meta_tests/test_assertion_analyzer.py:158); should be Mixed finite/complex strategy

## Deviations in meta_tests/test_comment_format.py

- Line 39: [`# Combination strategy: 50 examples (combination coverage)`](kivy_garden/markdownlabel/tests/meta_tests/test_comment_format.py:39) incorrectly classifies mixed finite/complex strategy as Combination in [`test_valid_comment_format_compliance`](kivy_garden/markdownlabel/tests/meta_tests/test_comment_format.py:41)
- Line 64: [`# Small finite strategy: 5 examples (input space size: 5)`](kivy_garden/markdownlabel/tests/meta_tests/test_comment_format.py:64) incorrect input space size (5 vs 6 for StrategyType sampled_from) in [`test_standard_comment_generation_compliance`](kivy_garden/markdownlabel/tests/meta_tests/test_comment_format.py:66)
- Line 225: [`# Complex strategy: 25 examples (adequate coverage)`](kivy_garden/markdownlabel/tests/meta_tests/test_comment_format.py:225) incorrectly classifies mixed finite/complex strategy as Complex in [`test_custom_max_examples_require_documentation`](kivy_garden/markdownlabel/tests/meta_tests/test_comment_format.py:227)
- Line 550: [`# Combination strategy: 30 examples (performance optimized)`](kivy_garden/markdownlabel/tests/meta_tests/test_comment_format.py:550) incorrectly classifies mixed finite/complex strategy as Combination in [`test_standardized_comments_are_machine_parseable`](kivy_garden/markdownlabel/tests/meta_tests/test_comment_format.py:552)
- Line 598: [`# Small finite strategy: 5 examples (input space size: 5)`](kivy_garden/markdownlabel/tests/meta_tests/test_comment_format.py:598) incorrect input space size (5 vs 6 for StrategyType sampled_from) in [`test_generated_comments_are_machine_parseable`](kivy_garden/markdownlabel/tests/meta_tests/test_comment_format.py:600)

## Deviations in meta_tests/test_comment_standardizer.py

- Line 43: [`# Boolean strategy: 2 examples (True/False coverage)`](kivy_garden/markdownlabel/tests/meta_tests/test_comment_standardizer.py:43) incorrectly classifies complex strategies (filtered integers + text) as Boolean strategy in [`test_boolean_strategy_comments_reference_true_false_coverage`](kivy_garden/markdownlabel/tests/meta_tests/test_comment_standardizer.py:45); should be Complex strategy

- Line 317: [`# Combination strategy: 25 examples (adequate coverage)`](kivy_garden/markdownlabel/tests/meta_tests/test_comment_standardizer.py:317) uses wrong rationale "(adequate coverage)"; should be "(combination coverage)" for [`test_finite_strategy_comments_reference_input_space_size`](kivy_garden/markdownlabel/tests/meta_tests/test_comment_standardizer.py:320)

- Line 391: [`# Combination strategy: 30 examples (adequate coverage)`](kivy_garden/markdownlabel/tests/meta_tests/test_comment_standardizer.py:391) incorrectly classifies complex strategies (lists(texts) + filtered integers) as Combination; wrong rationale; in [`test_sampled_from_finite_strategy_documentation`](kivy_garden/markdownlabel/tests/meta_tests/test_comment_standardizer.py:393)

- Line 611: [`# Small finite strategy: 5 examples (input space size: 5)`](kivy_garden/markdownlabel/tests/meta_tests/test_comment_standardizer.py:611) incorrectly classifies mixed finite/complex strategies (integers(1-5), sampled_from(3), text) as Small finite; in [`test_execution_time_performance_rationale_documented`](kivy_garden/markdownlabel/tests/meta_tests/test_comment_standardizer.py:613)

- Line 687: [`# Combination strategy: 4 examples (performance optimized)`](kivy_garden/markdownlabel/tests/meta_tests/test_comment_standardizer.py:687) incorrectly classifies mixed finite/complex strategies (sampled_from(5), integers(1-20), text) as Combination; in [`test_explicit_performance_comments_detected`](kivy_garden/markdownlabel/tests/meta_tests/test_comment_standardizer.py:689)

## Deviations in meta_tests/test_coverage_preservation.py

- Line 183: [`# Complex strategy: 10 examples (adequate coverage for different scenarios)`](kivy_garden/markdownlabel/tests/meta_tests/test_coverage_preservation.py:183) imprecise rationale (extra "for different scenarios"); in [`test_refactoring_preserves_coverage`](kivy_garden/markdownlabel/tests/meta_tests/test_coverage_preservation.py:185)

## Deviations in meta_tests/test_file_analyzer.py

- Line 467: [`# Small finite strategy: 20 examples (adequate coverage)`](kivy_garden/markdownlabel/tests/meta_tests/test_file_analyzer.py:467) incorrectly classifies combination strategy (sampled_from(5) × integers(1-100) × booleans()) as Small finite; wrong rationale "(adequate coverage)"; in [`test_tool_integration_compatibility`](kivy_garden/markdownlabel/tests/meta_tests/test_file_analyzer.py:469)

## Deviations in meta_tests/test_helper_availability.py

- Line 121: [`# Complex strategy: 1 example (strategy availability verification only)`](kivy_garden/markdownlabel/tests/meta_tests/test_helper_availability.py:121) uses incorrect rationale "(strategy availability verification only)"; should be "(adequate coverage)" or "(performance optimized)" for Complex strategy in [`test_color_strategy_available`](kivy_garden/markdownlabel/tests/meta_tests/test_helper_availability.py:124)
- Line 130: [`# Complex strategy: 1 example (strategy availability verification only)`](kivy_garden/markdownlabel/tests/meta_tests/test_helper_availability.py:130) uses incorrect rationale "(strategy availability verification only)"; should be "(adequate coverage)" or "(performance optimized)" for Complex strategy in [`test_text_padding_strategy_available`](kivy_garden/markdownlabel/tests/meta_tests/test_helper_availability.py:132)
- Line 139: [`# Complex strategy: 1 example (strategy availability verification only)`](kivy_garden/markdownlabel/tests/meta_tests/test_helper_availability.py:139) uses incorrect rationale "(strategy availability verification only)"; should be "(adequate coverage)" or "(performance optimized)" for Complex strategy in [`test_simple_markdown_document_strategy_available`](kivy_garden/markdownlabel/tests/meta_tests/test_helper_availability.py:141)

## Deviations in meta_tests/test_naming_convention_validator.py

- Line 135: [`# Combination strategy: 50 examples (combination coverage)`](kivy_garden/markdownlabel/tests/meta_tests/test_naming_convention_validator.py:135) incorrectly classifies mixed finite/complex strategy (st.sampled_from(2 items) + st.text()) as Combination strategy in [`test_naming_pattern_consistency_property`](kivy_garden/markdownlabel/tests/meta_tests/test_naming_convention_validator.py:137); should be Mixed finite/complex strategy

## Deviations in meta_tests/test_shared_infrastructure.py

- Line 173: [`# Combination strategy: 50 examples (combination coverage)`](kivy_garden/markdownlabel/tests/meta_tests/test_shared_infrastructure.py:173) incorrectly classifies two complex strategies (`color_strategy`, `color_strategy`) as Combination strategy in [`test_colors_equal_function_available`](kivy_garden/markdownlabel/tests/meta_tests/test_shared_infrastructure.py:175); should be Complex strategy
- Line 187: [`# Combination strategy: 50 examples (combination coverage)`](kivy_garden/markdownlabel/tests/meta_tests/test_shared_infrastructure.py:187) incorrectly classifies two complex strategies (`text_padding_strategy`, `text_padding_strategy`) as Combination strategy in [`test_padding_equal_function_available`](kivy_garden/markdownlabel/tests/meta_tests/test_shared_infrastructure.py:189); should be Complex strategy
- Line 201: [`# Combination strategy: 20 examples (combination coverage)`](kivy_garden/markdownlabel/tests/meta_tests/test_shared_infrastructure.py:201) incorrectly classifies two complex `st.floats(min_value=0.0, max_value=100.0)` strategies as Combination strategy in [`test_floats_equal_function_available`](kivy_garden/markdownlabel/tests/meta_tests/test_shared_infrastructure.py:203); should be Complex strategy

## Deviations in meta_tests/test_strategy_classification.py

- Line 76: [`# Small finite strategy: 3 examples (testing complex strategy classification)`](kivy_garden/markdownlabel/tests/meta_tests/test_strategy_classification.py:76) uses incorrect rationale "(testing complex strategy classification)"; should be "(input space size: 3)" for Small finite strategy in [`test_complex_strategy_classification`](kivy_garden/markdownlabel/tests/meta_tests/test_strategy_classification.py:78)
