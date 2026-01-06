# Deviations

## test_sizing_behavior.py

### Line 24-26: `test_auto_size_hint_enabled_sets_none`
- **Issue**: Incorrect strategy classification
- **Current comment**: `# Complex strategy: 20 examples (adequate coverage)`
- **Expected comment**: `# Mixed finite/complex strategy: 20 examples (5 finite × 4 complex samples)` or similar
- **Reason**: `simple_markdown_document()` is a mixed finite/complex strategy (generates 1-5 elements with complex text content), not a pure complex strategy

### Line 42-44: `test_height_bound_to_minimum`
- **Issue**: Incorrect strategy classification
- **Current comment**: `# Complex strategy: 20 examples (adequate coverage)`
- **Expected comment**: `# Mixed finite/complex strategy: 20 examples (6 finite × ~3 complex samples)` or similar
- **Reason**: `markdown_heading()` is a mixed finite/complex strategy (level 1-6 with complex text content), not a pure complex strategy

### Line 87-89: `test_auto_size_height_true_sets_size_hint_y_none`
- **Issue**: Incorrect strategy classification
- **Current comment**: `# Complex strategy: 20 examples (adequate coverage)`
- **Expected comment**: `# Mixed finite/complex strategy: 20 examples (5 finite × 4 complex samples)` or similar
- **Reason**: `simple_markdown_document()` is a mixed finite/complex strategy, not a pure complex strategy

### Line 98-100: `test_auto_size_height_true_binds_height_to_minimum`
- **Issue**: Incorrect strategy classification
- **Current comment**: `# Complex strategy: 20 examples (adequate coverage)`
- **Expected comment**: `# Mixed finite/complex strategy: 20 examples (5 finite × 4 complex samples)` or similar
- **Reason**: `simple_markdown_document()` is a mixed finite/complex strategy, not a pure complex strategy

### Line 125-127: `test_auto_size_height_true_ignores_user_size_hint_y`
- **Issue**: Incorrect strategy classification
- **Current comment**: `# Complex strategy: 50 examples (adequate coverage)`
- **Expected comment**: `# Mixed finite/complex strategy: 50 examples (5 finite × 10 complex samples)` or similar
- **Reason**: Combines `simple_markdown_document()` (mixed finite/complex) with `st.floats()` (complex), should use mixed finite/complex classification

### Line 153-155: `test_auto_size_height_false_preserves_default_size_hint_y`
- **Issue**: Incorrect strategy classification
- **Current comment**: `# Complex strategy: 20 examples (adequate coverage)`
- **Expected comment**: `# Mixed finite/complex strategy: 20 examples (5 finite × 4 complex samples)` or similar
- **Reason**: `simple_markdown_document()` is a mixed finite/complex strategy, not a pure complex strategy

### Line 167-170: `test_auto_size_height_false_preserves_user_size_hint_y`
- **Issue**: Incorrect strategy classification
- **Current comment**: `# Complex strategy: 50 examples (adequate coverage)`
- **Expected comment**: `# Mixed finite/complex strategy: 50 examples (5 finite × 10 complex samples)` or similar
- **Reason**: Combines `simple_markdown_document()` (mixed finite/complex) with `st.floats()` (complex), should use mixed finite/complex classification

### Line 186-188: `test_auto_size_height_false_no_height_binding`
- **Issue**: Incorrect strategy classification
- **Current comment**: `# Complex strategy: 20 examples (adequate coverage)`
- **Expected comment**: `# Mixed finite/complex strategy: 20 examples (5 finite × 4 complex samples)` or similar
- **Reason**: `simple_markdown_document()` is a mixed finite/complex strategy, not a pure complex strategy

### Line 211-213: `test_toggle_true_to_false_restores_size_hint_y`
- **Issue**: Incorrect strategy classification
- **Current comment**: `# Complex strategy: 20 examples (adequate coverage)`
- **Expected comment**: `# Mixed finite/complex strategy: 20 examples (5 finite × 4 complex samples)` or similar
- **Reason**: `simple_markdown_document()` is a mixed finite/complex strategy, not a pure complex strategy

### Line 233-235: `test_toggle_false_to_true_sets_size_hint_y_none`
- **Issue**: Incorrect strategy classification
- **Current comment**: `# Complex strategy: 20 examples (adequate coverage)`
- **Expected comment**: `# Mixed finite/complex strategy: 20 examples (5 finite × 4 complex samples)` or similar
- **Reason**: `simple_markdown_document()` is a mixed finite/complex strategy, not a pure complex strategy

### Line 255-258: `test_toggle_preserves_user_size_hint_y`
- **Issue**: Incorrect strategy classification
- **Current comment**: `# Complex strategy: 50 examples (adequate coverage)`
- **Expected comment**: `# Mixed finite/complex strategy: 50 examples (5 finite × 10 complex samples)` or similar
- **Reason**: Combines `simple_markdown_document()` (mixed finite/complex) with `st.floats()` (complex), should use mixed finite/complex classification

### Line 290-292: `test_multiple_toggles_maintain_consistency`
- **Issue**: Incorrect strategy classification
- **Current comment**: `# Complex strategy: 20 examples (adequate coverage)`
- **Expected comment**: `# Mixed finite/complex strategy: 20 examples (5 finite × 4 complex samples)` or similar
- **Reason**: `simple_markdown_document()` is a mixed finite/complex strategy, not a pure complex strategy

### Line 324-326: `test_strict_mode_preserves_default_size_hint_y`
- **Issue**: Incorrect strategy classification
- **Current comment**: `# Complex strategy: 20 examples (adequate coverage)`
- **Expected comment**: `# Mixed finite/complex strategy: 20 examples (5 finite × 4 complex samples)` or similar
- **Reason**: `simple_markdown_document()` is a mixed finite/complex strategy, not a pure complex strategy

### Line 338-341: `test_strict_mode_preserves_user_size_hint_y`
- **Issue**: Incorrect strategy classification
- **Current comment**: `# Complex strategy: 50 examples (adequate coverage)`
- **Expected comment**: `# Mixed finite/complex strategy: 50 examples (5 finite × 10 complex samples)` or similar
- **Reason**: Combines `simple_markdown_document()` (mixed finite/complex) with `st.floats()` (complex), should use mixed finite/complex classification

### Line 357-359: `test_strict_mode_height_not_bound_to_minimum`
- **Issue**: Incorrect strategy classification
- **Current comment**: `# Complex strategy: 20 examples (adequate coverage)`
- **Expected comment**: `# Mixed finite/complex strategy: 20 examples (5 finite × 4 complex samples)` or similar
- **Reason**: `simple_markdown_document()` is a mixed finite/complex strategy, not a pure complex strategy

### Line 403-405: `test_strict_mode_toggle_from_false_to_true`
- **Issue**: Incorrect strategy classification
- **Current comment**: `# Complex strategy: 20 examples (adequate coverage)`
- **Expected comment**: `# Mixed finite/complex strategy: 20 examples (5 finite × 4 complex samples)` or similar
- **Reason**: `simple_markdown_document()` is a mixed finite/complex strategy, not a pure complex strategy

### Line 426-428: `test_strict_mode_toggle_from_true_to_false`
- **Issue**: Incorrect strategy classification
- **Current comment**: `# Complex strategy: 20 examples (adequate coverage)`
- **Expected comment**: `# Mixed finite/complex strategy: 20 examples (5 finite × 4 complex samples)` or similar
- **Reason**: `simple_markdown_document()` is a mixed finite/complex strategy, not a pure complex strategy

### Line 449-452: `test_strict_mode_toggle_preserves_user_size_hint_y`
- **Issue**: Incorrect strategy classification
- **Current comment**: `# Complex strategy: 50 examples (adequate coverage)`
- **Expected comment**: `# Mixed finite/complex strategy: 50 examples (5 finite × 10 complex samples)` or similar
- **Reason**: Combines `simple_markdown_document()` (mixed finite/complex) with `st.floats()` (complex), should use mixed finite/complex classification

### Line 477-479: `test_strict_mode_overrides_auto_size_height`
- **Issue**: Incorrect strategy classification
- **Current comment**: `# Complex strategy: 20 examples (adequate coverage)`
- **Expected comment**: `# Mixed finite/complex strategy: 20 examples (5 finite × 4 complex samples)` or similar
- **Reason**: `simple_markdown_document()` is a mixed finite/complex strategy, not a pure complex strategy

### Line 494-496: `test_strict_mode_ignores_auto_size_height_changes`
- **Issue**: Incorrect strategy classification
- **Current comment**: `# Complex strategy: 20 examples (adequate coverage)`
- **Expected comment**: `# Mixed finite/complex strategy: 20 examples (5 finite × 4 complex samples)` or similar
- **Reason**: `simple_markdown_document()` is a mixed finite/complex strategy, not a pure complex strategy

### Line 511-513: `test_strict_mode_updates_value`
- **Issue**: Incorrect strategy classification
- **Current comment**: `# Complex strategy: 20 examples (adequate coverage)`
- **Expected comment**: `# Mixed finite/complex strategy: 20 examples (5 finite × 4 complex samples)` or similar
- **Reason**: `simple_markdown_document()` is a mixed finite/complex strategy, not a pure complex strategy

### Line 531-533: `test_multiple_strict_mode_toggles_maintain_consistency`
- **Issue**: Incorrect strategy classification
- **Current comment**: `# Complex strategy: 20 examples (adequate coverage)`
- **Expected comment**: `# Mixed finite/complex strategy: 20 examples (5 finite × 4 complex samples)` or similar
- **Reason**: `simple_markdown_document()` is a mixed finite/complex strategy, not a pure complex strategy

## test_advanced_compatibility.py

### Line 481-485: `rebuild_colors` strategy definition comment
- **Issue**: Incorrect strategy classification
- **Current comment**: `# Medium finite strategy: 20 examples (adequate finite coverage)`
- **Expected comment**: `# Complex strategy: 20 examples (adequate coverage)`
- **Reason**: `st.lists(st.floats(min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False), min_size=4, max_size=4)` generates continuous float values, not a finite input space. This is a complex strategy, not a medium finite strategy.

### Line 822-823: `test_rebuild_preserves_content_structure`
- **Issue**: Incorrect finite space size calculation in comment
- **Current comment**: `# Mixed finite/complex strategy: 20 examples (9 finite × ~2 complex samples)`
- **Expected comment**: `# Mixed finite/complex strategy: 20 examples (90 finite combinations × ~0.2 complex samples)` or similar
- **Reason**: The finite space is calculated incorrectly. The strategy combines:
  - `simple_markdown_document()`: num_elements (1-5) × element_type (2) = 10 finite combinations
  - Two `rebuild_font_names`: 3 × 3 = 9 finite combinations
  - Total finite space: 10 × 9 = 90 combinations
  - The comment only mentions "9 finite" which omits the document structure finite combinations

## test_serialization.py

### Line 120-123: `test_heading_round_trip`
- **Issue**: Incorrect strategy classification
- **Current comment**: `# Complex strategy: 20 examples (adequate coverage)`
- **Expected comment**: `# Mixed finite/complex strategy: 20 examples (6 finite × ~3 complex samples)` or similar
- **Reason**: `markdown_heading()` combines `st.integers(min_value=1, max_value=6)` (6 finite values for heading levels) with `st.text()` (complex/infinite text generation), making it a mixed finite/complex strategy, not a pure complex strategy.

### Line 210-213: `test_document_round_trip`
- **Issue**: Incorrect strategy classification
- **Current comment**: `# Complex strategy: 20 examples (adequate coverage)`
- **Expected comment**: `# Mixed finite/complex strategy: 20 examples (10 finite × 2 complex samples)` or similar
- **Reason**: `simple_markdown_document()` combines finite elements (num_elements: 1-5 values, element_type: 2 values = 10 finite combinations) with complex text generation from `markdown_heading()` and `markdown_paragraph()`, making it a mixed finite/complex strategy, not a pure complex strategy.

### Line 613-622: `test_code_serialization_round_trip_property`
- **Issue**: Incorrect strategy classification for multiple complex strategies
- **Current comment**: `# Complex strategy: 20 examples (adequate coverage)`
- **Expected comment**: `# Complex strategy: 20 examples (two complex strategies combined)` or similar
- **Reason**: While this correctly identifies it as a complex strategy, the comment doesn't accurately reflect that it combines two separate complex strategies (`st.text()` for code_content and `st.text()` with alphabet filtering for language). The rationale should mention the combination of multiple complex strategies.

## test_rebuild_semantics.py

### Line 245-258: `test_style_property_changes_preserve_widget_tree`
- **Issue**: Incorrect strategy classification and rationale
- **Current comment**: `# Mixed finite/complex strategy: 50 examples (120 finite × 0 complex samples)`
- **Expected comment**: `# Mixed finite/complex strategy: 50 examples (120 finite × ~0.4 complex samples)` or `# Mixed finite/complex strategy: 50 examples (multiple finite dimensions × complex samples)`
- **Reason**: The strategy combines multiple finite dimensions (halign: 4, valign: 3, disabled: 2, base_direction: 5 = 120 combinations) with complex strategies (base_font_size, color, disabled_color, line_height). The current rationale incorrectly states "0 complex samples" when there are 4 complex strategies. Additionally, `simple_markdown_document()` is itself a mixed finite/complex strategy (10 finite combinations × complex text), making total finite space larger than stated.

### Line 420-430: `test_style_property_values_propagate_to_descendants`
- **Issue**: Incorrect strategy classification and rationale
- **Current comment**: `# Mixed finite/complex strategy: 50 examples (60 finite × 0 complex samples)`
- **Expected comment**: `# Mixed finite/complex strategy: 50 examples (60 finite × ~0.8 complex samples)` or `# Mixed finite/complex strategy: 50 examples (multiple finite dimensions × complex samples)`
- **Reason**: Similar to test above, this strategy combines multiple finite dimensions (halign: 4, valign: 3, base_direction: 5 = 60 combinations) with complex strategies (color, line_height). The current rationale incorrectly states "0 complex samples" when there are 2 complex strategies. Also, `simple_markdown_document()` is a mixed finite/complex strategy.

### Line 652-657: `test_text_change_triggers_rebuild_pbt`
- **Issue**: Incorrect strategy classification
- **Current comment**: `# Complex strategy: 50 examples (performance optimized)`
- **Expected comment**: `# Mixed finite/complex strategy: 50 examples (complex samples)` or `# Complex strategy: 50 examples (adequate coverage)`
- **Reason**: The strategy uses `simple_markdown_document()` twice (initial_text and new_text), which is a mixed finite/complex strategy (10 finite combinations × complex text generation), not a pure complex strategy. While "performance optimized" is an acceptable rationale for complex strategies, strategy type should be "Mixed finite/complex" to accurately reflect that `simple_markdown_document()` has finite dimensions (num_elements: 1-5, element_type: 2).

### Line 695-700: `test_font_name_change_triggers_rebuild_pbt`
- **Issue**: Incorrect strategy classification and rationale
- **Current comment**: `# Mixed finite/complex strategy: 3 examples (3 finite × 1 complex sample)`
- **Expected comment**: `# Mixed finite/complex strategy: 3 examples (3 finite × 1 complex sample)` or similar with accurate finite space calculation
- **Reason**: The strategy combines `st_font_name()` (3 finite values) with `simple_markdown_document()` (mixed finite/complex: 10 finite combinations × complex text). The current rationale only counts the 3 font names as finite, ignoring the 10 finite combinations from `simple_markdown_document()`. The total finite space should be 3 × 10 = 30 combinations, not 3.

### Line 737-742: `test_link_style_change_triggers_rebuild_pbt`
- **Issue**: Incorrect strategy classification and rationale
- **Current comment**: `# Mixed finite/complex strategy: 2 examples (2 finite × 1 complex sample)`
- **Expected comment**: `# Mixed finite/complex strategy: 2 examples (2 finite × 1 complex sample)` or similar with accurate finite space calculation
- **Reason**: The strategy combines `st.sampled_from(['unstyled', 'styled'])` (2 finite values) with `simple_markdown_document()` (mixed finite/complex: 10 finite combinations × complex text). The current rationale only counts the 2 link styles as finite, ignoring the 10 finite combinations from `simple_markdown_document()`. The total finite space should be 2 × 10 = 20 combinations, not 2.

### Line 784-796: `test_root_id_preserved_across_style_property_changes`
- **Issue**: Incorrect strategy classification and rationale
- **Current comment**: `# Mixed finite/complex strategy: 50 examples (24 finite × 0 complex samples)`
- **Expected comment**: `# Mixed finite/complex strategy: 50 examples (24 finite × ~2 complex samples)` or `# Mixed finite/complex strategy: 50 examples (multiple finite dimensions × complex samples)`
- **Reason**: The strategy combines multiple finite dimensions (halign: 4, valign: 3, disabled: 2 = 24 combinations) with complex strategies (base_font_size, color, line_height). The current rationale incorrectly states "0 complex samples" when there are 3 complex strategies. Also, `simple_markdown_document()` is a mixed finite/complex strategy.

### Line 829-838: `test_root_id_preserved_across_structure_property_changes`
- **Issue**: Incorrect strategy classification and rationale
- **Current comment**: `# Mixed finite/complex strategy: 50 examples (8 finite × 0 complex samples)`
- **Expected comment**: `# Mixed finite/complex strategy: 50 examples (8 finite × ~6 complex samples)` or `# Mixed finite/complex strategy: 50 examples (multiple finite dimensions × complex samples)`
- **Reason**: The strategy combines multiple finite dimensions (link_style: 2, strict_label_mode: 2, render_mode: 2 = 8 combinations) with complex strategies (simple_markdown_document() twice, st_font_name()). The current rationale incorrectly states "0 complex samples" when there are 3 complex strategies. Additionally, `simple_markdown_document()` is itself a mixed finite/complex strategy.

### Line 872-881: `test_root_id_preserved_across_mixed_property_changes`
- **Issue**: Incorrect strategy classification and rationale
- **Current comment**: `# Mixed finite/complex strategy: 50 examples (2 finite × 0 complex samples)`
- **Expected comment**: `# Mixed finite/complex strategy: 50 examples (2 finite × 25 complex samples)` or `# Mixed finite/complex strategy: 50 examples (multiple finite dimensions × complex samples)`
- **Reason**: The strategy combines a finite dimension (link_style: 2 values) with complex strategies (simple_markdown_document(), st_font_size(), st_rgba_color()). The current rationale incorrectly states "0 complex samples" when there are 3 complex strategies. Also, `simple_markdown_document()` is a mixed finite/complex strategy.

## test_texture_render_mode.py

### Line 230-231: `test_property_inside_zone_dispatch`
- **Issue**: Incorrect strategy classification
- **Current comment**: `# Complex strategy: 50 examples (adequate coverage)`
- **Expected comment**: `# Mixed finite/complex strategy: 50 examples (multiple finite dimensions × complex samples)` or similar
- **Reason**: The strategy combines a finite strategy (`st.from_regex(r'https?://[a-z]{3,10}\.[a-z]{2,5}/[a-z]{1,10}', fullmatch=True)` generates a finite set of URLs due to constrained pattern) with complex strategies (four `st.floats()` strategies for zone coordinates and touch offsets). This should be classified as "Mixed finite/complex strategy" rather than pure "Complex strategy".

### Line 332-333: `test_property_outside_zone_no_dispatch`
- **Issue**: Incorrect strategy classification
- **Current comment**: `# Complex strategy: 50 examples (adequate coverage)`
- **Expected comment**: `# Mixed finite/complex strategy: 50 examples (multiple finite dimensions × complex samples)` or similar
- **Reason**: Same as above - combines a finite `st.from_regex()` strategy for URL generation with multiple complex `st.floats()` strategies for zone coordinates and offset values. Should be classified as "Mixed finite/complex strategy" rather than pure "Complex strategy".

## test_texture_sizing.py

### Line 269-271: `test_texture_size_updates_on_text_change`
- **Issue**: Incorrect strategy classification and rationale
- **Current comment**: `# Complex strategy: 50 examples (adequate coverage)`
- **Expected comment**: `# Mixed finite/complex strategy: 50 examples (100 finite combinations × 0.5 complex samples)` or similar
- **Reason**: The strategy combines two `simple_markdown_document()` strategies, each of which is a mixed finite/complex strategy (num_elements: 1-5 values, element_type: 2 values = 10 finite combinations per strategy). The total finite space is 10 × 10 = 100 combinations. The current classification as "Complex strategy" doesn't accurately reflect the finite dimensions present in the combined strategy space. While "adequate coverage" is an acceptable rationale, the strategy type should be "Mixed finite/complex" to accurately reflect that both strategies have finite dimensions.

## test_shortening_and_coordinate.py

### Line 288-292: `test_all_shortening_properties_forwarded_together`
- **Issue**: Incorrect strategy classification and rationale
- **Current comment**: `# Mixed finite/complex strategy: 50 examples (30 finite × 50 complex samples)`
- **Expected comment**: `# Mixed finite/complex strategy: 50 examples (30 finite × ~1.7 complex samples)` or similar
- **Reason**: The strategy combines:
  - `st.booleans()`: 2 finite values
  - `st.sampled_from(['left', 'center', 'right'])`: 3 finite values
  - `st.text(min_size=0, max_size=3, alphabet='ab ')`: complex strategy (text generation)
  - `st.integers(min_value=1, max_value=5)`: 5 finite values
  - Total finite space: 2 × 3 × 5 = 30 combinations
  - With max_examples=50, each finite combination gets approximately 50/30 = 1.7 complex text samples
  - The current rationale incorrectly states "50 complex samples" when it should be approximately 1.7 complex samples per finite value

## test_code_duplication_minimization.py

### Line 130-132: `test_duplication_below_threshold`
- **Issue**: Incorrect strategy classification
- **Current comment**: `# Complex strategy: 15 examples (adequate coverage for duplication patterns)`
- **Expected comment**: `# Mixed finite/complex strategy: 15 examples (18 finite × ~0.8 complex samples)` or similar
- **Reason**: The custom strategy `_test_suite_with_duplicates()` combines finite dimensions (num_files: 3-8 = 6 values, duplication_level: 3 values, total finite combinations: 6 × 3 = 18) with complex nested structure generation (test file contents). While the strategy generates complex structures, it has clear finite dimensions that should be acknowledged in the classification.

## test_comment_format.py

### Line 27-41: `test_valid_comment_format_compliance`
- **Issue**: Incorrect rationale for mixed finite/complex strategy
- **Current comment**: `# Mixed finite/complex strategy: 50 examples (combination coverage)`
- **Expected comment**: `# Mixed finite/complex strategy: 50 examples (6 finite × ~8 complex samples)` or similar
- **Reason**: The strategy combines `st.sampled_from([s.value for s in StrategyType])` (6 finite values) with `st.integers(min_value=1, max_value=1000)` (complex) and `st.text(...)` (complex). According to guidelines, mixed finite/complex strategies should use format "Mixed finite/complex strategy: [N] examples ([finite_size] finite × [samples] complex samples)", not "combination coverage" which is for all-finite combination strategies.

### Line 60-66: `test_standard_comment_generation_compliance`
- **Issue**: Incorrect max_examples for small finite strategy
- **Current comment**: `# Small finite strategy: 5 examples (input space size: 6)`
- **Expected comment**: `# Small finite strategy: 6 examples (input space size: 6)`
- **Reason**: The strategy uses `st.sampled_from([s.value for s in StrategyType])` which has exactly 6 finite values. According to guidelines, small finite strategies should use max_examples equal to input space size, not less.

### Line 218-227: `test_custom_max_examples_require_documentation`
- **Issue**: Incorrect rationale for mixed finite/complex strategy
- **Current comment**: `# Mixed finite/complex strategy: 25 examples (adequate coverage)`
- **Expected comment**: `# Mixed finite/complex strategy: 25 examples (6 finite × ~4 complex samples)` or similar
- **Reason**: The strategy combines `st.sampled_from([s.value for s in StrategyType])` (6 finite values) with `st.integers(min_value=1, max_value=1000).filter(...)` (complex). According to guidelines, mixed finite/complex strategies should use format "Mixed finite/complex strategy: [N] examples ([finite_size] finite × [samples] complex samples)", not "adequate coverage" which is for complex strategies.

### Line 398-404: `test_boolean_and_small_finite_terminology_consistency`
- **Issue**: Incorrect strategy classification
- **Current comment**: `# Small finite strategy: 2 examples (input space size: 2)`
- **Expected comment**: `# Mixed finite/complex strategy: 2 examples (2 finite × 1 complex sample)` or similar
- **Reason**: The strategy samples from `['st.booleans()', 'st.integers(min_value=0, max_value=5)']` which are 2 finite string values, not the strategies themselves. While this is technically a small finite strategy (2 values), the test is checking strategy classification consistency, and the rationale "input space size: 2" is misleading since it's not actually testing strategy classification on the strategies mentioned in the sample list.

### Line 541-552: `test_standardized_comments_are_machine_parseable`
- **Issue**: Incorrect rationale for mixed finite/complex strategy
- **Current comment**: `# Mixed finite/complex strategy: 30 examples (performance optimized)`
- **Expected comment**: `# Mixed finite/complex strategy: 30 examples (6 finite × 5 complex samples)` or similar
- **Reason**: The strategy combines `st.sampled_from([s.value for s in StrategyType])` (6 finite values) with `st.integers(min_value=1, max_value=1000)` (complex) and `st.sampled_from([...])` for rationale_base (5 finite values). According to guidelines, mixed finite/complex strategies should use format "Mixed finite/complex strategy: [N] examples ([finite_size] finite × [samples] complex samples)", not "performance optimized" which is for complex strategies.

### Line 594-600: `test_generated_comments_are_machine_parseable`
- **Issue**: Incorrect max_examples for small finite strategy
- **Current comment**: `# Small finite strategy: 5 examples (input space size: 6)`
- **Expected comment**: `# Small finite strategy: 6 examples (input space size: 6)`
- **Reason**: The strategy uses `st.sampled_from([s.value for s in StrategyType])` which has exactly 6 finite values. According to guidelines, small finite strategies should use max_examples equal to input space size, not less.

## test_comment_standardizer.py

### Line 309-318: `test_finite_strategy_comments_reference_input_space_size`
- **Issue**: Incorrect strategy classification
- **Current comment**: `# Combination strategy: 25 examples (combination coverage)`
- **Expected comment**: `# Mixed finite/complex strategy: 25 examples (440 finite × ~0.06 complex samples)` or similar
- **Reason**: The strategy combines finite strategies (`min_value=st.integers(min_value=0, max_value=10)` = 11 values, `max_value=st.integers(min_value=11, max_value=50)` = 40 values) with a complex strategy (`max_examples=st.integers(min_value=1, max_value=100).filter(...)`). According to guidelines, "Combination strategy" is only for ALL finite strategies. When there's at least one complex strategy, it should be classified as "Mixed finite/complex strategy". Total finite space: 11 × 40 = 440 combinations.

### Line 34-44: `test_boolean_strategy_comments_reference_true_false_coverage`
- **Issue**: Incorrect strategy classification
- **Current comment**: `# Complex strategy: 2 examples (adequate coverage)`
- **Expected comment**: `# Mixed finite/complex strategy: 2 examples (adequate coverage)` or similar
- **Reason**: The strategy combines `st.integers(min_value=1, max_value=100).filter(...)` (complex/infinite) with `st.text(...)` (complex/infinite). While both are complex, max_examples=2 is unusually low for complex strategies (guidelines recommend 10-50). However, this may be intentional for a meta-test testing the standardizer itself. The classification as "Complex strategy" is technically correct, but the low max_examples value is notable.

### Line 384-392: `test_sampled_from_finite_strategy_documentation`
- **Issue**: Incorrect strategy classification
- **Current comment**: `# Complex strategy: 30 examples (adequate coverage)`
- **Expected comment**: `# Mixed finite/complex strategy: 30 examples (adequate coverage)` or similar
- **Reason**: The strategy combines `st.lists(st.text(...), ...)` (complex/infinite) with `st.integers(min_value=1, max_value=50).filter(...)` (complex/infinite). While both are complex, the test is specifically about finite strategy documentation (it generates test code using `st.sampled_from([...])` which is finite). The classification should reflect that this is a meta-test about finite strategies.

### Line 603-612: `test_execution_time_performance_rationale_documented`
- **Issue**: Incorrect strategy classification
- **Current comment**: `# Mixed strategy: 5 examples (performance optimized)`
- **Expected comment**: `# Mixed finite/complex strategy: 5 examples (15 finite × ~0.33 complex samples)` or similar
- **Reason**: The strategy combines `st.integers(min_value=1, max_value=5)` (5 finite values), `st.sampled_from(['text', 'floats', 'composite'])` (3 finite values), and `st.text(...)` (complex/infinite). Total finite space: 5 × 3 = 15 combinations. According to guidelines, mixed finite/complex strategies should use format "Mixed finite/complex strategy: [N] examples ([finite_size] finite × [samples] complex samples)", not just "Mixed strategy".

### Line 673-688: `test_explicit_performance_comments_detected`
- **Issue**: Incorrect strategy classification
- **Current comment**: `# Mixed strategy: 4 examples (performance optimized)`
- **Expected comment**: `# Mixed finite/complex strategy: 4 examples (5 finite × ~0.8 complex samples)` or similar
- **Reason**: The strategy combines `st.sampled_from([...])` (5 finite values for performance_keywords), `st.integers(min_value=1, max_value=20)` (complex/infinite), and `st.text(...)` (complex/infinite). Total finite space: 5 values. According to guidelines, mixed finite/complex strategies should use format "Mixed finite/complex strategy: [N] examples ([finite_size] finite × [samples] complex samples)", not just "Mixed strategy".

## test_coverage_preservation.py

### Line 182-184: `test_refactoring_preserves_coverage`
- **Issue**: Incorrect strategy classification and max_examples
- **Current comment**: `# Complex strategy: 10 examples (adequate coverage)`
- **Expected comment**: `# Mixed finite/complex strategy: 12 examples (12 finite × 1 complex sample)` or similar
- **Reason**: The custom strategy `_test_suite_with_coverage()` combines finite dimensions:
  - `num_files = draw(st.integers(min_value=2, max_value=5))`: 4 finite values (2, 3, 4, 5)
  - `coverage_level = draw(st.sampled_from(['low', 'medium', 'high']))`: 3 finite values
  - Total finite space: 4 × 3 = 12 combinations
  - The strategy generates complex nested structures (source files and test files with various content)
  - According to guidelines, this should be classified as "Mixed finite/complex strategy" with format "Mixed finite/complex strategy: [N] examples ([finite_size] finite × [samples] complex samples)"
  - The current classification as "Complex strategy" doesn't acknowledge the finite dimensions present in the strategy

### Line 457-459: `test_coverage_tolerance_reasonable`
- **Issue**: max_examples below recommended range for complex strategy
- **Current comment**: `# Complex strategy: 6 examples (adequate coverage)`
- **Expected comment**: `# Complex strategy: 10-50 examples (adequate coverage)` with max_examples in the recommended range
- **Reason**: The strategy uses `st.floats(min_value=50.0, max_value=95.0)` which is a complex/infinite continuous strategy. According to guidelines, complex strategies should use max_examples in the range of 10-50 based on complexity. The current max_examples=6 is below the recommended minimum of 10. While the classification as "Complex strategy" is correct, the max_examples value should be increased to at least 10 to follow the guidelines.

## test_file_analyzer.py

### Line 460-468: `test_tool_integration_compatibility`
- **Issue**: Incorrect finite space calculation in comment
- **Current comment**: `# Mixed finite/complex strategy: 20 examples (10 finite × 2 complex samples)`
- **Expected comment**: `# Mixed finite/complex strategy: 20 examples (4 finite × 5 complex samples)` or similar
- **Reason**: The strategy combines:
  - `st.sampled_from(['Boolean', 'Small finite', 'Small finite', 'Small finite', 'Small finite'])`: 5 items in list, but only 2 unique values ('Boolean' and 'Small finite')
  - `st.booleans()`: 2 finite values
  - `st.integers(min_value=1, max_value=100)`: complex/infinite
  - Total finite combinations: 2 × 2 = 4 (not 10)
  - With max_examples=20, each finite combination gets approximately 20/4 = 5 complex samples (not 2)
  - The current rationale incorrectly states "10 finite" when the actual finite space is 4 combinations

## test_helper_availability.py

### Line 91-93: `test_rebuild_detection_helpers_available`
- **Issue**: Incorrect strategy classification
- **Current comment**: `# Complex strategy: 5 examples (adequate coverage)`
- **Expected comment**: `# Mixed finite/complex strategy: 5 examples (10 finite × ~0.5 complex samples)` or similar
- **Reason**: `simple_markdown_document()` combines finite dimensions (num_elements: 1-5 values, element_type: 2 values = 10 finite combinations) with complex text generation from `markdown_heading()` and `markdown_paragraph()`, making it a mixed finite/complex strategy, not a pure complex strategy.

### Line 121-123: `test_color_strategy_available`
- **Issue**: max_examples below recommended range for complex strategy
- **Current comment**: `# Complex strategy: 1 example (adequate coverage)`
- **Expected comment**: `# Complex strategy: 10-50 examples (adequate coverage)` with max_examples in the recommended range
- **Reason**: The strategy uses `color_strategy` which generates continuous float values (4-tuples of RGBA floats), making it a complex/infinite strategy. According to guidelines, complex strategies should use max_examples in the range of 10-50 based on complexity. The current max_examples=1 is significantly below the recommended minimum of 10.

### Line 130-132: `test_text_padding_strategy_available`
- **Issue**: max_examples below recommended range for complex strategy
- **Current comment**: `# Complex strategy: 1 example (adequate coverage)`
- **Expected comment**: `# Complex strategy: 10-50 examples (adequate coverage)` with max_examples in the recommended range
- **Reason**: The strategy uses `text_padding_strategy` which generates lists of 4 continuous float values, making it a complex/infinite strategy. According to guidelines, complex strategies should use max_examples in the range of 10-50 based on complexity. The current max_examples=1 is significantly below the recommended minimum of 10.

### Line 139-141: `test_simple_markdown_document_strategy_available`
- **Issue**: Incorrect strategy classification and max_examples below recommended range
- **Current comment**: `# Complex strategy: 1 example (adequate coverage)`
- **Expected comment**: `# Mixed finite/complex strategy: 10-50 examples (10 finite × 1-5 complex samples)` with max_examples in the recommended range
- **Reason**: The strategy uses `simple_markdown_document()` which combines finite dimensions (num_elements: 1-5 values, element_type: 2 values = 10 finite combinations) with complex text generation, making it a mixed finite/complex strategy. Additionally, max_examples=1 is below the recommended minimum of 10 for complex strategies. The classification should be "Mixed finite/complex strategy" and max_examples should be increased to at least 10.

## test_shared_infrastructure.py

### Line 33-35: `test_markdown_heading_strategy_generates_valid_headings`
- **Issue**: Incorrect strategy classification
- **Current comment**: `# Complex strategy: 20 examples (adequate coverage)`
- **Expected comment**: `# Mixed finite/complex strategy: 20 examples (6 finite × ~3 complex samples)` or similar
- **Reason**: `markdown_heading()` combines `st.integers(min_value=1, max_value=6)` (6 finite values for heading levels) with `st.text()` (complex text generation), making it a mixed finite/complex strategy, not a pure complex strategy.

### Line 92-94: `test_simple_markdown_document_strategy_generates_valid_documents`
- **Issue**: Incorrect strategy classification
- **Current comment**: `# Complex strategy: 20 examples (adequate coverage)`
- **Expected comment**: `# Mixed finite/complex strategy: 20 examples (10 finite × 2 complex samples)` or similar
- **Reason**: `simple_markdown_document()` combines finite dimensions (num_elements: 1-5 values, element_type: 2 values = 10 finite combinations) with complex text generation from `markdown_heading()` and `markdown_paragraph()`, making it a mixed finite/complex strategy, not a pure complex strategy.

## test_test_file_parser.py

### Line 27-29: `test_rebuild_test_names_match_assertions`
- **Issue**: Incorrect strategy classification and rationale
- **Current comment**: `# Complex strategy: 20 examples (adequate coverage)`
- **Expected comment**: `# Mixed finite/complex strategy: 20 examples (28 finite × ~0.7 complex samples)` or similar
- **Reason**: The `rebuild_test_file_strategy()` combines finite dimensions with complex string generation:
  - `st.sampled_from([...])` for test_name: 4 finite values
  - `st.booleans()` for has_rebuild_assertion: 2 finite values
  - `st.sampled_from([...])` for assertion_code: 4 finite values (when has_rebuild_assertion=True) or 3 finite values (when False)
  - Total finite space: 4 × 2 × 4 = 16 (True) + 4 × 2 × 3 = 12 (False) = 28 combinations
  - The strategy also generates complex test code strings
  - According to guidelines, when combining finite and complex strategies, it should be classified as "Mixed finite/complex strategy" with format "Mixed finite/complex strategy: [N] examples ([finite_size] finite × [samples] complex samples)"

## test_duplicate_detector.py

### Line 30-32: `test_duplicate_detection_finds_duplicates`
- **Issue**: Incorrect strategy classification
- **Current comment**: `# Complex strategy: 20 examples (adequate coverage)`
- **Expected comment**: `# Mixed finite/complex strategy: 20 examples (36 finite × ~0.6 complex samples)` or similar
- **Reason**: The `duplicate_helper_functions()` strategy combines finite dimensions with complex content generation:
  - `st.sampled_from([...])` for function_name: 6 finite values
  - `st.booleans()` for make_identical: 2 finite values
  - `st.integers(min_value=2, max_value=4)` for num_files: 3 finite values
  - `st.sampled_from(body_templates)` for body selection: 3 finite values
  - Total finite space: 6 × 2 × 3 = 36 combinations
  - The strategy also generates complex file content strings
  - According to guidelines, when combining finite and complex strategies, it should be classified as "Mixed finite/complex strategy" with format "Mixed finite/complex strategy: [N] examples ([finite_size] finite × [samples] complex samples)"
