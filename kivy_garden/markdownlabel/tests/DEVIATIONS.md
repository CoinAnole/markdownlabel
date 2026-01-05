## Deviations in kivy_garden/markdownlabel/tests/test_inline_renderer.py

- In `test_only_special_chars_fully_escaped` (lines 206-208): Incorrect strategy classification and rationale: "Medium finite strategy: 50 examples (adequate finite coverage)" instead of "Complex strategy: 50 examples (adequate coverage)" for `st.text(alphabet='[]&', min_size=1, max_size=50)`, which matches Complex/Infinite pattern (st.text()).

## Deviations in kivy_garden/markdownlabel/tests/test_kivy_renderer.py

- In `test_heading_font_size_scales_with_base` (lines 83-86): Incorrect strategy classification and rationale: "Combination strategy: 10 examples (performance optimized)" instead of "Mixed finite/complex strategy: 30 examples (6 finite × 5 complex samples)" for `st.integers(min_value=1, max_value=6), st.floats(min_value=10, max_value=30)`, which is Mixed finite/complex (finite range + floats).

## Deviations in kivy_garden/markdownlabel/tests/test_core_functionality.py

- In `test_text_change_updates_widgets` (lines 108-111): Incorrect strategy classification and rationale: "Combination strategy: 50 examples (combination coverage)" instead of "Complex strategy: 50 examples (adequate coverage)" for `markdown_heading(), markdown_paragraph()`, which are both Complex/Infinite text strategies.
- In `test_ast_updates_with_text` (lines 175-178): Incorrect strategy classification and rationale: "Combination strategy: 50 examples (combination coverage)" instead of "Complex strategy: 50 examples (adequate coverage)" for `simple_markdown_document(), simple_markdown_document()`, which are both Complex/Infinite text strategies.
- In `test_nested_lists_render_without_exception` (lines 279-282): Incorrect max_examples: 15 instead of 20-50 for Medium finite strategy `st.integers(min_value=1, max_value=15)`
- In `test_nested_quotes_render_without_exception` (lines 298-301): Incorrect max_examples: 15 instead of 20-50 for Medium finite strategy `st.integers(min_value=1, max_value=15)`
- In `test_mixed_nesting_renders_without_exception` (lines 316-319): Incorrect max_examples: 15 instead of 20-50 for Medium finite strategy `st.integers(min_value=1, max_value=15)`

## Deviations in kivy_garden/markdownlabel/tests/test_label_compatibility.py

- In `test_font_size_change_updates_base_font_size` (lines 45-48): Incorrect strategy classification and rationale: "Combination strategy: 50 examples (combination coverage)" instead of "Complex strategy: 50 examples (adequate coverage)" for `st.floats(min_value=1, max_value=200, allow_nan=False, allow_infinity=False), st.floats(min_value=1, max_value=200, allow_nan=False, allow_infinity=False)` (both Complex/Infinite float ranges).
- In `test_base_font_size_change_updates_font_size` (lines 57-60): Incorrect strategy classification and rationale: "Combination strategy: 50 examples (combination coverage)" instead of "Complex strategy: 50 examples (adequate coverage)" for `st.floats(min_value=1, max_value=200, allow_nan=False, allow_infinity=False), st.floats(min_value=1, max_value=200, allow_nan=False, allow_infinity=False)` (both Complex/Infinite float ranges).
- In `test_all_noop_properties_together` (lines 134-138): Comment format mismatch: multi-line explanatory comments ("# 2 × 2 × 2 × 2 × 2 = 32 combinations
# Use 32 examples for full coverage") instead of exact "# Combination strategy: 32 examples (combination coverage)" for five `st.booleans()` (all finite Combination, product=32).
- In `test_noop_properties_do_not_affect_rendering` (lines 156-158): Incorrect strategy classification and rationale: "Combination strategy: 50 examples (combination coverage)" instead of "Mixed finite/complex strategy: 50 examples (32 finite × ~2 complex samples)" for five `st.booleans()` + `simple_markdown_document()` (finite booleans + complex text).
- In `test_all_noop_properties_together_accepted_and_stored` (lines 287-293): Incorrect strategy classification and rationale: "Combination strategy: 50 examples (combination coverage)" instead of "Mixed finite/complex strategy: 50 examples (finite × complex samples)" for mixture of `st.booleans()`, `st.floats()`, `st_rgba_color()`, `st.dictionaries(...)`, etc. (mixed finite/complex).
- In `test_advanced_noop_properties_do_not_affect_rendering` (lines 370-378): Incorrect strategy classification and rationale: "Combination strategy: 2 examples (combination coverage)"; also incorrect max_examples: 2 instead of 20-50; for complex mixed strategies including `simple_markdown_document()`, `st_rgba_color()`, `st.dictionaries(...)`, etc.

## Deviations in kivy_garden/markdownlabel/tests/test_font_properties.py

- In `test_line_height_change_triggers_rebuild` (lines 223-225): Incorrect strategy classification and rationale: "Combination strategy: 20 examples (combination coverage)" instead of "Complex strategy: 20 examples (adequate coverage)" for `line_height_strategy, line_height_strategy` (two complex `st.floats()` ranges).
- In `test_combined_font_properties_with_code_block` (lines 456-462): Incorrect strategy classification and rationale: "Combination strategy: 20 examples (combination coverage)" instead of "Mixed finite/complex strategy: 20 examples (8 finite × 2.5 complex samples)" for `st_alphanumeric_text() x2, st.sampled_from([None, 'normal', 'light', 'mono']), st.booleans()` (finite + complex).
- In `test_base_font_size_updates_all_labels_immediately` (lines 512-519): Incorrect strategy classification and rationale: "Combination strategy: 20 examples (combination coverage)" instead of "Complex strategy: 20 examples (adequate coverage)" for `simple_markdown_document(), st_font_size(), st_font_size()` (all complex/infinite).
- In `test_heading_font_size_updates_with_scale` (lines 562-569): Incorrect strategy classification and rationale: "Combination strategy: 20 examples (combination coverage)" instead of "Mixed finite/complex strategy: 20 examples (6 finite × ~3 complex samples)" for `st.integers(1,6), st_font_size(), st_font_size()`.
- In `test_heading_scale_factors_preserved` (lines 639-645): Incorrect strategy classification and rationale: "Combination strategy: 20 examples (combination coverage)" instead of "Mixed finite/complex strategy: 20 examples (6 finite × ~3 complex samples)" for `st.integers(1,6), st_font_size()`.
- In `test_multiple_headings_preserve_relative_scales` (lines 677-687): Incorrect strategy classification and rationale: "Combination strategy: 20 examples (combination coverage)" instead of "Mixed finite/complex strategy: 20 examples (large finite lists × complex)" for `st.lists(st.integers(1,6), min_size=2, max_size=6, unique=True), st_font_size()`.
- In `test_heading_scale_preserved_after_base_font_size_change` (lines 729-735): Incorrect strategy classification and rationale: "Combination strategy: 20 examples (combination coverage)" instead of "Mixed finite/complex strategy: 20 examples (6 finite × ~3 complex samples)" for `st.integers(1,6), st_font_size(), st_font_size()`.
- In `test_widget_identities_preserved_on_font_size_change` (lines 781-788): Incorrect strategy classification and rationale: "Combination strategy: 20 examples (combination coverage)" instead of "Complex strategy: 20 examples (adequate coverage)" for `simple_markdown_document(), st_font_size(), st_font_size()` (all complex).
- In `test_heading_widget_identity_preserved` (lines 813-819): Incorrect strategy classification, rationale, and max_examples: "Small finite strategy: 6 examples (input space size: 6)" instead of "Mixed finite/complex strategy: 30 examples (6 finite × 5 complex samples)" for `st.integers(1,6), st_font_size(), st_font_size()`.
- In `test_multiple_font_size_changes_preserve_identities` (lines 856-862): Incorrect strategy classification and rationale: "Combination strategy: 20 examples (combination coverage)" instead of "Complex strategy: 20 examples (adequate coverage)" for three `st_font_size()` (all complex floats).

## Deviations in kivy_garden/markdownlabel/tests/test_color_properties.py

- In `test_color_change_updates_value` (lines 79-81): Incorrect strategy classification and rationale: "Combination strategy: 50 examples (combination coverage)" instead of "Complex strategy: 50 examples (adequate coverage)" for `@given(color_strategy, color_strategy)`, which are two Complex/Infinite strategies (RGBA float tuples).

## Deviations in kivy_garden/markdownlabel/tests/test_text_properties.py

- In `test_valign_forwarded_with_height` (lines 156-161): Incorrect comment format for Mixed finite/complex strategy (`st.floats(...)` + `st.sampled_from(['top', 'middle', 'bottom'])`): multi-line custom comments instead of "# Mixed finite/complex strategy: 20 examples (3 finite × 7 complex samples)" 
- In `test_unicode_errors_change_triggers_rebuild` (lines 431-435): Incorrect comment format for Combination strategy (two `unicode_errors_strategy`, product=9): multi-line custom comments instead of "# Combination strategy: 9 examples (combination coverage)" 
- In `test_strip_change_triggers_rebuild` (lines 572-577): Incorrect comment format for Combination strategy (two `st.booleans()`, product=4): multi-line custom comments instead of "# Combination strategy: 4 examples (combination coverage)" 

## Deviations in kivy_garden/markdownlabel/tests/test_advanced_compatibility.py

- In `test_font_family_forwarded_to_labels` (lines 31-36): Incorrect strategy classification and rationale: "Medium finite strategy: 20 examples (adequate finite coverage)" instead of "Complex strategy: 20 examples (adequate coverage)" for `st.text(min_size=1, max_size=30, alphabet=st.characters(whitelist_categories=['L', 'N'], blacklist_characters='[]&\\\r'))`, which matches Complex/Infinite pattern (st.text()).
- In `test_font_context_forwarded_to_labels` (lines 48-53): Incorrect strategy classification and rationale: "Medium finite strategy: 20 examples (adequate finite coverage)" instead of "Complex strategy: 20 examples (adequate coverage)" for `st.text(...)` (Complex/Infinite).
- In `test_font_features_forwarded_to_labels` (lines 66-70): Incorrect strategy classification and rationale: "Medium finite strategy: 20 examples (adequate finite coverage)" instead of "Complex strategy: 20 examples (adequate coverage)" for `st.text(...)` (Complex/Infinite).
- In `test_font_kerning_change_triggers_rebuild` (lines 152-155): Comment format mismatch: multi-line explanatory comments ("# 2 × 2 = 4 combinations
# Use 4 examples for full coverage") instead of exact "# Combination strategy: 4 examples (combination coverage)" for `st.booleans(), st.booleans()` (all finite Combination, product=4).
- In `test_font_blended_change_triggers_rebuild` (lines 183-186): Comment format mismatch: multi-line explanatory comments ("# 2 × 2 = 4 combinations
# Use 4 examples for full coverage") instead of exact "# Combination strategy: 4 examples (combination coverage)" for `st.booleans(), st.booleans()` (all finite Combination, product=4).
- In `test_disabled_color_stored_correctly` (lines 266-270): Incorrect strategy classification and rationale: "Medium finite strategy: 20 examples (adequate finite coverage)" instead of "Complex strategy: 20 examples (adequate coverage)" for `st.lists(st.floats(min_value=0, max_value=1, allow_nan=False, allow_infinity=False), min_size=4, max_size=4)` (Complex continuous floats).
- In `test_disabled_color_applied_when_disabled` (lines 279-283): Incorrect strategy classification and rationale: "Medium finite strategy: 20 examples (adequate finite coverage)" instead of "Complex strategy: 20 examples (adequate coverage)" for `st.lists(...)` (Complex).
- In `test_regular_color_applied_when_not_disabled` (lines 306-310): Incorrect strategy classification and rationale: "Medium finite strategy: 20 examples (adequate finite coverage)" instead of "Complex strategy: 20 examples (adequate coverage)" for `st.lists(...)` (Complex).
- In `test_font_name_triggers_rebuild` (lines 498-501): Comment format mismatch: multi-line explanatory comments ("# 3 font_names × 3 font_names = 9 combinations
# Use 9 examples for full coverage") instead of exact "# Combination strategy: 9 examples (combination coverage)" for `rebuild_font_names, rebuild_font_names` (sampled_from(['Roboto', 'Roboto-Bold', 'Roboto-Italic']), all finite Combination, product=9).
- In `test_color_updates_value` (lines 537-540): Incorrect strategy classification and rationale: "# Large combination space (continuous values)
# Use 20 examples to sample adequately" instead of "Complex strategy: 20 examples (adequate coverage)" for `rebuild_colors, rebuild_colors` (lists of floats, Complex/Infinite).
- In `test_line_height_updates_value` (lines 576-579): Incorrect strategy classification and rationale: "# Large combination space (continuous values)
# Use 20 examples to sample adequately" instead of "Complex strategy: 20 examples (adequate coverage)" for `rebuild_line_heights, rebuild_line_heights` (floats, Complex/Infinite).
- In `test_text_size_updates_value` (lines 615-618): Incorrect strategy classification and rationale: "# Large combination space (continuous values)
# Use 20 examples to sample adequately" instead of "Complex strategy: 20 examples (adequate coverage)" for `rebuild_text_size_widths, rebuild_text_size_widths` (floats, Complex/Infinite).
- In `test_multiple_property_changes_rebuild_correctly` (lines 651-654): Incorrect strategy classification and rationale: "# 3 font_names × continuous colors × continuous line_heights
# Use 20 examples to sample adequately" instead of "Mixed finite/complex strategy: 20 examples (3 finite × ~7 complex samples)" for `rebuild_font_names, rebuild_colors, rebuild_line_heights` (finite sampled_from + two Complex).
- In `test_rebuild_preserves_content_structure` (lines 830-833): Incorrect strategy classification and rationale: "# Complex markdown × 3 font_names × 3 font_names
# Use 20 examples to sample adequately" instead of "Mixed finite/complex strategy: 20 examples (9 finite × ~2 complex samples)" for `simple_markdown_document(), rebuild_font_names, rebuild_font_names` (Complex text + two finite sampled_from).
- In `test_strip_updates_value` (lines 764-767): Comment format mismatch: multi-line explanatory comments ("# 2 × 2 = 4 combinations
# Use 4 examples for full coverage") instead of exact "# Combination strategy: 4 examples (combination coverage)" for `st.booleans(), st.booleans()` (all finite Combination, product=4).
- In `test_font_kerning_updates_value` (lines 854-857): Comment format mismatch: multi-line explanatory comments ("# 2 × 2 = 4 combinations
# Use 4 examples for full coverage") instead of exact "# Combination strategy: 4 examples (combination coverage)" for `st.booleans(), st.booleans()` (all finite Combination, product=4).
- In `test_font_blended_updates_value` (lines 881-884): Comment format mismatch: multi-line explanatory comments ("# 2 × 2 = 4 combinations
# Use 4 examples for full coverage") instead of exact "# Combination strategy: 4 examples (combination coverage)" for `st.booleans(), st.booleans()` (all finite Combination, product=4).

## Deviations in kivy_garden/markdownlabel/tests/test_serialization.py

- In `test_code_serialization_round_trip_property` (lines 613-622): Incorrect strategy classification and rationale: "Combination strategy: 20 examples (adequate coverage)" instead of "Complex strategy: 20 examples (adequate coverage)" for `st.text(min_size=0, max_size=200), st.text(alphabet=st.characters(whitelist_categories=("L", "N"), min_size=0, max_size=20)` (both Complex/Infinite st.text() strategies).

## Deviations in kivy_garden/markdownlabel/tests/test_performance.py

- In `test_font_size_change_preserves_widget_tree` (lines 30-33): Incorrect strategy classification and rationale: "Combination strategy: 20 examples (adequate coverage)" instead of "Complex strategy: 20 examples (adequate coverage)" for `st_font_size(min_value=10, max_value=50), st_font_size(min_value=10, max_value=50)` (two Complex/Infinite float ranges).
- In `test_color_change_preserves_widget_tree` (lines 55-57): Incorrect strategy classification and rationale: "Combination strategy: 20 examples (adequate coverage)" instead of "Complex strategy: 20 examples (adequate coverage)" for `st_rgba_color()` (Complex/Infinite RGBA float tuple).
- In `test_color_change_updates_descendant_labels` (lines 77-79): Incorrect strategy classification and rationale: "Combination strategy: 20 examples (adequate coverage)" instead of "Complex strategy: 20 examples (adequate coverage)" for `st_rgba_color()` (Complex/Infinite RGBA float tuple).
- In `test_multiple_style_changes_preserve_widget_tree` (lines 279-287): Incorrect strategy classification and rationale: "Combination strategy: 20 examples (adequate coverage)" instead of "Mixed finite/complex strategy: 20 examples (9 finite × ~2 complex samples)" for `st_font_size(min_value=10, max_value=30), st_rgba_color(), st.sampled_from(['left', 'center', 'right']), st.sampled_from(['top', 'middle', 'bottom']), st.floats(min_value=0.8, max_value=2.0, allow_nan=False, allow_infinity=False)` (mixed finite sampled_from + multiple Complex strategies).

## Deviations in kivy_garden/markdownlabel/tests/test_rebuild_scheduling.py

- In `test_mixed_property_changes_batch_rebuilds` (lines 67-72): Incorrect strategy classification and rationale: "Combination strategy: 2 examples (combination coverage)" instead of "Mixed finite/complex strategy: 10-20 examples (2 finite × 5-10 complex samples)" for `st_alphanumeric_text(min_size=1, max_size=20), st_font_size(min_value=10, max_value=30), st_font_name(fonts=["Roboto", "RobotoMono-Regular"])` (complex text + complex floats + small finite 2 fonts); incorrect max_examples: 2 instead of 10-20.

## Deviations in kivy_garden/markdownlabel/tests/test_rebuild_semantics.py

- In `test_style_property_changes_preserve_widget_tree` (lines 245/258): Incorrect strategy classification: "Combination strategy" instead of "Mixed finite/complex strategy" for strategies with multiple finite (sampled_from, booleans) + complex (simple_markdown_document, st_font_size, st_rgba_color, st.floats)
- In `test_style_property_values_propagate_to_descendants` (lines 421/431): Incorrect strategy classification: "Combination strategy" instead of "Mixed finite/complex strategy" for strategies with finite (sampled_from) + complex (simple_markdown_document, st_rgba_color, st.floats)
- In `test_text_change_triggers_rebuild_pbt` (lines 652/658): Incorrect strategy classification: "Combination strategy" instead of "Complex strategy" for two `simple_markdown_document()` (complex text strategies)
- In `test_font_name_change_triggers_rebuild_pbt` (lines 696/701): Incorrect strategy classification: "Small finite strategy" instead of "Mixed finite/complex strategy" for `st_font_name()` (finite) + `simple_markdown_document()` (complex)
- In `test_link_style_change_triggers_rebuild_pbt` (lines 739/743): Incorrect strategy classification: "Small finite strategy" instead of "Mixed finite/complex strategy" for `st.sampled_from(['unstyled', 'styled'])` (finite) + `simple_markdown_document()` (complex)
- In `test_root_id_preserved_across_style_property_changes` (lines 784/797): Incorrect strategy classification: "Combination strategy" instead of "Mixed finite/complex strategy" for strategies with finite (sampled_from, booleans) + complex (simple_markdown_document, st_font_size, st_rgba_color, st.floats)
- In `test_root_id_preserved_across_structure_property_changes` (lines 829/839): Incorrect strategy classification: "Combination strategy" instead of "Mixed finite/complex strategy" for finite (sampled_from, booleans) + complex (`simple_markdown_document()` x2, st_font_name)
- In `test_root_id_preserved_across_mixed_property_changes` (lines 872/882): Incorrect strategy classification: "Combination strategy" instead of "Mixed finite/complex strategy" for finite (sampled_from) + complex (simple_markdown_document, st_font_size, st_rgba_color, st_font_name)

## Deviations in kivy_garden/markdownlabel/tests/test_clipping_behavior.py

- In `test_heading_content_clipped_when_height_constrained` (lines 104-109): Incorrect strategy classification and rationale: "Small finite strategy: 6 examples (input space size: 6)" instead of "Mixed finite/complex strategy: 30 examples (6 finite × 5 complex samples)" for `st.integers(min_value=1, max_value=6), st.floats(min_value=50.0, max_value=200.0, allow_nan=False, allow_infinity=False)`, which is Mixed finite/complex.

## Deviations in kivy_garden/markdownlabel/tests/test_texture_render_mode.py

- In `test_property_inside_zone_dispatch` (lines 216-231): Incorrect strategy classification and rationale: "Combination strategy: 50 examples (combination coverage)" instead of "Complex strategy: 50 examples (adequate coverage)" for multiple complex/infinite strategies (`st.tuples(st.floats(...))`, `st.from_regex(...)`, `st.floats(...)`).
- In `test_property_outside_zone_no_dispatch` (lines 320-333): Incorrect strategy classification and rationale: "Combination strategy: 50 examples (combination coverage)" instead of "Complex strategy: 50 examples (adequate coverage)" for multiple complex/infinite strategies (`st.tuples(st.floats(...))`, `st.from_regex(...)`, `st.floats(...)`).

## Deviations in kivy_garden/markdownlabel/tests/test_texture_sizing.py

- In `test_texture_size_updates_on_text_change` (lines 269-272): Incorrect strategy classification and rationale: "Combination strategy: 50 examples (product of strategy sizes, capped)" instead of "Complex strategy: 50 examples (adequate coverage)" for `simple_markdown_document(), simple_markdown_document()` (both Complex/Infinite text strategies).

## Deviations in kivy_garden/markdownlabel/tests/test_rtl_alignment.py

- In `test_auto_alignment_rtl_applies_to_headings` (lines 63-70): Comment format mismatch: multi-line explanatory comments ("# 2 directions × 6 heading_levels = 12 combinations
# Use 12 examples for full coverage") instead of exact "# Combination strategy: 12 examples (combination coverage)" for `st.sampled_from(['rtl', 'weak_rtl']), st.integers(min_value=1, max_value=6)` (all finite Combination, product=12).
- In `test_auto_alignment_ltr_applies_to_headings` (lines 89-96): Comment format mismatch: multi-line explanatory comments ("# 3 directions × 6 heading_levels = 18 combinations
# Use 18 examples for full coverage") instead of exact "# Combination strategy: 18 examples (combination coverage)" for `st.sampled_from(['ltr', 'weak_ltr', None]), st.integers(min_value=1, max_value=6)` (all finite Combination, product=18).
- In `test_direction_change_ltr_to_rtl_updates_alignment` (lines 171-178): Comment format mismatch: multi-line explanatory comments ("# 3 initial_directions × 2 new_directions = 6 combinations
# Use 6 examples for full coverage") instead of exact "# Combination strategy: 6 examples (combination coverage)" for `st.sampled_from(['ltr', 'weak_ltr', None]), st.sampled_from(['rtl', 'weak_rtl'])` (all finite Combination, product=6).
- In `test_direction_change_rtl_to_ltr_updates_alignment` (lines 205-212): Comment format mismatch: multi-line explanatory comments ("# 2 initial_directions × 3 new_directions = 6 combinations
# Use 6 examples for full coverage") instead of exact "# Combination strategy: 6 examples (combination coverage)" for `st.sampled_from(['rtl', 'weak_rtl']), st.sampled_from(['ltr', 'weak_ltr', None])` (all finite Combination, product=6).
- In `test_direction_change_updates_heading_alignment` (lines 239-247): Comment format mismatch: multi-line explanatory comments ("# 6 heading_levels × 3 initial_directions × 2 new_directions = 36 combinations
# Use 20 examples to sample adequately without exhaustive testing") instead of exact "# Combination strategy: 36 examples (combination coverage)" for `st.integers(min_value=1, max_value=6), st.sampled_from(['ltr', 'weak_ltr', None]), st.sampled_from(['rtl', 'weak_rtl'])` (all finite Combination, product=36); also incorrect max_examples: 20 instead of 36.
- In `test_direction_change_preserves_widget_identities` (lines 281-286): Comment format mismatch: multi-line explanatory comments ("# 3 initial_directions × 2 new_directions = 6 combinations
# Use 6 examples for full coverage") instead of exact "# Combination strategy: 6 examples (combination coverage)" for `st.sampled_from(['ltr', 'weak_ltr', None]), st.sampled_from(['rtl', 'weak_rtl'])` (all finite Combination, product=6).
- In `test_direction_change_mixed_content_updates_alignment` (lines 310-316): Comment format mismatch: multi-line explanatory comments ("# 3 initial_directions × 2 new_directions = 6 combinations
# Use 6 examples for full coverage") instead of exact "# Combination strategy: 6 examples (combination coverage)" for `st.sampled_from(['ltr', 'weak_ltr', None]), st.sampled_from(['rtl', 'weak_rtl'])` (all finite Combination, product=6).
- In `test_explicit_alignment_overrides_base_direction` (lines 359-366): Comment format mismatch: multi-line explanatory comments ("# 4 alignments × 5 directions = 20 combinations
# Use 20 examples for full coverage") instead of exact "# Combination strategy: 20 examples (combination coverage)" for `st.sampled_from(['left', 'center', 'right', 'justify']), st.sampled_from(['rtl', 'weak_rtl', 'ltr', 'weak_ltr', None])` (all finite Combination, product=20).
- In `test_explicit_alignment_overrides_rtl_for_headings` (lines 384-393): Comment format mismatch: multi-line explanatory comments ("# 4 alignments × 2 directions × 6 heading_levels = 48 combinations
# Use 20 examples to sample adequately without exhaustive testing") instead of exact "# Combination strategy: 48 examples (combination coverage)" for `st.sampled_from(['left', 'center', 'right', 'justify']), st.sampled_from(['rtl', 'weak_rtl']), st.integers(min_value=1, max_value=6)` (all finite Combination, product=48); also incorrect max_examples: 20 instead of 48.
- In `test_explicit_alignment_overrides_direction_for_mixed_content` (lines 415-422): Comment format mismatch: multi-line explanatory comments ("# 4 alignments × 5 directions = 20 combinations
# Use 20 examples for full coverage") instead of exact "# Combination strategy: 20 examples (combination coverage)" for `st.sampled_from(['left', 'center', 'right', 'justify']), st.sampled_from(['rtl', 'weak_rtl', 'ltr', 'weak_ltr', None])` (all finite Combination, product=20).
- In `test_explicit_alignment_unchanged_by_direction_change` (lines 445-453): Comment format mismatch: multi-line explanatory comments ("# 4 alignments × 2 initial_directions × 3 new_directions = 24 combinations
# Use 20 examples to sample adequately without exhaustive testing") instead of exact "# Combination strategy: 24 examples (combination coverage)" for `st.sampled_from(['left', 'center', 'right', 'justify']), st.sampled_from(['rtl', 'weak_rtl']), st.sampled_from(['ltr', 'weak_ltr', None])` (all finite Combination, product=24); also incorrect max_examples: 20 instead of 24.
- In `test_explicit_alignment_stored_correctly_on_widget` (lines 482-489): Comment format mismatch: multi-line explanatory comments ("# 4 alignments × 5 directions = 20 combinations
# Use 20 examples for full coverage") instead of exact "# Combination strategy: 20 examples (combination coverage)" for `st.sampled_from(['left', 'center', 'right', 'justify']), st.sampled_from(['rtl', 'weak_rtl', 'ltr', 'weak_ltr', None])` (all finite Combination, product=20).

## Deviations in kivy_garden/markdownlabel/tests/test_shortening_and_coordinate.py

- In `test_ellipsis_options_forwarded_to_paragraph` (lines 210-214): Incorrect strategy classification and rationale: "Small finite strategy: 3 examples (input space size: 3)" instead of "Complex strategy: N examples (adequate coverage)" for `st.fixed_dictionaries({'markup_color': st_rgba_color()})` (Complex/Infinite RGBA floats); also incorrect max_examples: 3 instead of 10-50.
- In `test_ellipsis_options_forwarded_to_heading` (lines 226-230): Incorrect strategy classification and rationale: "Small finite strategy: 3 examples (input space size: 3)" instead of "Complex strategy: N examples (adequate coverage)" for `st.fixed_dictionaries({'markup_color': st_rgba_color()})` (Complex/Infinite RGBA floats); also incorrect max_examples: 3 instead of 10-50.
- In `test_ellipsis_options_forwarded_to_list_items` (lines 242-246): Incorrect strategy classification and rationale: "Small finite strategy: 3 examples (input space size: 3)" instead of "Complex strategy: N examples (adequate coverage)" for `st.fixed_dictionaries({'markup_color': st_rgba_color()})` (Complex/Infinite RGBA floats); also incorrect max_examples: 3 instead of 10-50.
- In `test_ellipsis_options_forwarded_to_table_cells` (lines 259-263): Incorrect strategy classification and rationale: "Small finite strategy: 3 examples (input space size: 3)" instead of "Complex strategy: N examples (adequate coverage)" for `st.fixed_dictionaries({'markup_color': st_rgba_color()})` (Complex/Infinite RGBA floats); also incorrect max_examples: 3 instead of 10-50.
- In `test_all_shortening_properties_forwarded_together` (lines 288-292): Incorrect strategy classification: "Combination strategy: 50 examples (combination coverage)" instead of "Mixed finite/complex strategy: N examples (F finite × S complex samples)" for `st.booleans(), st.sampled_from(['left', 'center', 'right']), st.text(...), st.integers(1,5)` (finites + st.text()).
- In `test_link_produces_ref_markup_for_translation` (lines 366-368): Incorrect strategy classification: "Combination strategy: 20 examples (adequate coverage)" instead of "Complex strategy: 20 examples (adequate coverage)" for `st_alphanumeric_text()` (st.text()).
- In `test_property_refs_coordinate_translation_math` (lines 943-945): Comment rationale mismatch: "adequate coverage for 12-parameter float strategy" instead of "(adequate coverage)"; incorrect max_examples: 100 instead of 10-50 for Complex strategy (12 st.floats()).
- In `test_property_anchors_coordinate_translation_math` (lines 1277-1279): Comment rationale mismatch: "with 10 float parameters: 100 examples for adequate coverage" instead of "(adequate coverage)"; incorrect max_examples: 100 instead of 10-50 for Complex strategy (10 st.floats()).