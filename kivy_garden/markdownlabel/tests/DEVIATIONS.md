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

## Summary

**Total deviations found**: 24 (22 from test_sizing_behavior.py + 2 from test_advanced_compatibility.py)

**Patterns**:
1. **test_sizing_behavior.py**: All tests using `simple_markdown_document()` or `markdown_heading()` strategies are incorrectly classified as "Complex strategy" when they should be classified as "Mixed finite/complex strategy" because these strategies combine finite elements (number of elements, element types, heading levels) with complex text generation.
2. **test_advanced_compatibility.py**:
   - One strategy definition incorrectly classifies continuous float generation as "Medium finite strategy"
   - One test incorrectly calculates the finite space size when combining multiple finite strategies

**Correctly classified tests**:
- test_sizing_behavior.py:
  - Line 64-66: `test_more_content_means_more_height_potential` - Correctly uses "Small finite strategy"
  - Line 384-386: `test_strict_mode_property_accepted_and_stored` - Correctly uses "Boolean strategy"
  - Line 393-395: `test_strict_mode_change_after_creation` - Correctly uses "Boolean strategy"
- test_advanced_compatibility.py: All other tests with custom max_examples are correctly classified

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

## Summary

**Total deviations found**: 27 (24 from previous files + 3 from test_serialization.py)

**New patterns in test_serialization.py**:
1. **test_heading_round_trip**: Incorrectly classifies `markdown_heading()` as pure complex when it's mixed finite/complex (6 heading levels × complex text)
2. **test_document_round_trip**: Incorrectly classifies `simple_markdown_document()` as pure complex when it's mixed finite/complex (10 finite combinations × complex text)
3. **test_code_serialization_round_trip_property**: Correctly identifies as complex strategy but the rationale doesn't accurately describe the combination of two complex strategies

**Correctly classified tests in test_serialization.py**:
- Line 139-142: `test_paragraph_round_trip` - Correctly uses "Complex strategy" (pure complex text generation)
- Line 162-165: `test_bold_round_trip` - Correctly uses "Complex strategy" (pure complex text generation)
- Line 178-181: `test_italic_round_trip` - Correctly uses "Complex strategy" (pure complex text generation)
- Line 194-197: `test_link_round_trip` - Correctly uses "Complex strategy" (pure complex text + URL generation)
- Line 550-553: `test_fence_collision_handling_property` - Correctly uses "Complex strategy" (pure complex text generation)

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

## Summary

**Total deviations found**: 35 (27 from previous files + 8 from test_rebuild_semantics.py)

**New patterns in test_rebuild_semantics.py**:
1. **Incorrect rationale with "0 complex samples"**: Multiple tests incorrectly state "0 complex samples" in their rationale when they actually have multiple complex strategies (st_font_size, st_rgba_color, st.floats, etc.)
2. **Undercounting finite combinations**: Tests using `simple_markdown_document()` fail to account for its finite dimensions (num_elements: 1-5, element_type: 2 = 10 combinations) when calculating finite space
3. **Misclassification of simple_markdown_document()**: Several tests classify `simple_markdown_document()` as pure complex when it's actually a mixed finite/complex strategy

**Correctly classified tests in test_rebuild_semantics.py**:
- All unit tests (without @given decorator) are not subject to strategy classification guidelines
- No property-based tests in this file have correct strategy classifications

**Common issues across all files**:
1. `simple_markdown_document()` is consistently misclassified as pure complex when it's mixed finite/complex
2. Rationales claiming "0 complex samples" are incorrect when complex strategies are present
3. Finite space calculations often omit dimensions from mixed strategies

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

## Summary

**Total deviations found**: 37 (35 from previous files + 2 from test_texture_render_mode.py)

**New patterns in test_texture_render_mode.py**:
1. **st.from_regex() with constrained patterns**: Tests using `st.from_regex()` with highly constrained patterns (limited character sets and length ranges) are classified as pure complex when they should be mixed finite/complex because the constrained pattern generates a finite input space combined with other complex strategies.

**Correctly classified tests in test_texture_render_mode.py**:
- All unit tests (without @given decorator) are not subject to strategy classification guidelines
- All other property-based tests in this file have correct strategy classifications

## test_texture_sizing.py

### Line 269-271: `test_texture_size_updates_on_text_change`
- **Issue**: Incorrect strategy classification and rationale
- **Current comment**: `# Complex strategy: 50 examples (adequate coverage)`
- **Expected comment**: `# Mixed finite/complex strategy: 50 examples (100 finite combinations × 0.5 complex samples)` or similar
- **Reason**: The strategy combines two `simple_markdown_document()` strategies, each of which is a mixed finite/complex strategy (num_elements: 1-5 values, element_type: 2 values = 10 finite combinations per strategy). The total finite space is 10 × 10 = 100 combinations. The current classification as "Complex strategy" doesn't accurately reflect the finite dimensions present in the combined strategy space. While "adequate coverage" is an acceptable rationale, the strategy type should be "Mixed finite/complex" to accurately reflect that both strategies have finite dimensions.

## Summary

**Total deviations found**: 38 (37 from previous files + 1 from test_texture_sizing.py)

**New patterns in test_texture_sizing.py**:
1. **Combining mixed finite/complex strategies**: When combining multiple `simple_markdown_document()` strategies, the finite dimensions multiply (10 × 10 = 100 combinations), which should be reflected in the strategy classification and rationale.

**Correctly classified tests in test_texture_sizing.py**:
- Line 31-33: `test_texture_size_returns_tuple` - Correctly uses "Complex strategy" (single complex strategy)
- Line 45-47: `test_texture_size_non_negative` - Correctly uses "Complex strategy" (single complex strategy)
- Line 68-70: `test_heading_creates_label_widget` - Correctly uses "Complex strategy" (single complex strategy)
- Line 84-86: `test_paragraph_creates_label_widget` - Correctly uses "Complex strategy" (single complex strategy)
- Line 174-176: `test_more_content_increases_texture_height` - Correctly uses "Small finite strategy" (5 finite values)
- Line 218-220: `test_texture_size_accessible_for_all_content` - Correctly uses "Complex strategy" (single complex strategy)
- Line 316-318: `test_all_heading_levels_create_label_widgets` - Correctly uses "Small finite strategy" (6 finite values)
- All unit tests (without @given decorator) are not subject to strategy classification guidelines

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

## Summary

**Total deviations found**: 39 (38 from previous files + 1 from test_shortening_and_coordinate.py)

**New patterns in test_shortening_and_coordinate.py**:
1. **Incorrect complex samples calculation in rationale**: When combining multiple finite strategies with one complex strategy, rationale incorrectly states total max_examples as the number of complex samples instead of calculating samples per finite value (max_examples ÷ finite_combinations).

**Correctly classified tests in test_shortening_and_coordinate.py**:
- Line 42-44: `test_shorten_forwarded_to_paragraph` - Correctly uses "Boolean strategy" (2 examples)
- Line 56-58: `test_shorten_forwarded_to_heading` - Correctly uses "Boolean strategy" (2 examples)
- Line 70-72: `test_shorten_forwarded_to_list_items` - Correctly uses "Boolean strategy" (2 examples)
- Line 86-88: `test_shorten_forwarded_to_table_cells` - Correctly uses "Boolean strategy" (2 examples)
- Line 137-139: `test_split_str_forwarded_to_paragraph` - Correctly uses "Complex strategy" (30 examples)
- Line 151-153: `test_split_str_forwarded_to_heading` - Correctly uses "Complex strategy" (30 examples)
- Line 165-167: `test_max_lines_forwarded_to_paragraph` - Correctly uses "Medium finite strategy" (11 examples)
- Line 181-183: `test_max_lines_forwarded_to_heading` - Correctly uses "Small finite strategy" (10 examples)
- Line 195-197: `test_max_lines_forwarded_to_list_items` - Correctly uses "Small finite strategy" (10 examples)
- Line 210-214: `test_ellipsis_options_forwarded_to_paragraph` - Correctly uses "Complex strategy" (20 examples)
- Line 226-230: `test_ellipsis_options_forwarded_to_heading` - Correctly uses "Complex strategy" (20 examples)
- Line 242-246: `test_ellipsis_options_forwarded_to_list_items` - Correctly uses "Complex strategy" (20 examples)
- Line 258-262: `test_ellipsis_options_forwarded_to_table_cells` - Correctly uses "Complex strategy" (20 examples)
- Line 328-330: `test_shorten_change_updates_value` - Correctly uses "Combination strategy" (2 examples)
- Line 366-368: `test_link_produces_ref_markup_for_translation` - Correctly uses "Complex strategy" (20 examples)
- Line 397-402: `test_multiple_links_produce_ref_markup` - Correctly uses "Complex strategy" (20 examples)
- Line 565-568: `test_ref_markup_updates_when_text_changes` - Correctly uses "Complex strategy" (20 examples)
- Line 601-605: `test_coordinate_translation_math` - Correctly uses "Complex strategy" (20 examples)
- Line 633-636: `test_anchor_translation_math` - Correctly uses "Complex strategy" (20 examples)
- Line 925-945: `test_property_refs_coordinate_translation_math` - Correctly uses "Complex strategy" (50 examples)
- Line 1260-1278: `test_property_anchors_coordinate_translation_math` - Correctly uses "Complex strategy" (50 examples)
- All unit tests (without @given decorator) are not subject to strategy classification guidelines
- All tests using `@pytest.mark.parametrize` are not subject to strategy classification guidelines

