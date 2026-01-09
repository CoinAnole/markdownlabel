# Test Files Deviations Summary

Generated from analysis against TESTING.md guidelines.

## test_advanced_compatibility.py
- [x] Lines 154-181: test_font_kerning_change_triggers_rebuild incorrectly uses force_rebuild() and asserts rebuild occurred for style-only property (FIXED: Renamed to test_font_kerning_change_preserves_widget_tree, removed force_rebuild, asserted widget tree preserved)
- [x] Lines 185-212: test_font_blended_change_triggers_rebuild incorrectly uses force_rebuild() and asserts rebuild occurred for style-only property (FIXED: Renamed to test_font_blended_change_preserves_widget_tree, removed force_rebuild, asserted widget tree preserved)
- [x] Lines 297-301, 323-327, 350-354, 374-378, 390-394, 401-405: Uses implementation-dependent check ('Mono' in str(font_name)) to skip code blocks (FIXED: Replaced with getattr(lbl, '_is_code', False))
- [x] Lines 358-407: test_disabled_change_triggers_rebuild incorrectly uses force_rebuild() and asserts rebuild occurred for style-only property (FIXED: Renamed to test_disabled_change_preserves_widget_tree, removed force_rebuild, asserted widget tree preserved)
- [x] Lines 609-642: test_text_size_updates_value fails to verify text_size updated on internal Labels (FIXED: Renamed and added verification of internal Label properties)
- [x] Lines 744-772: test_unicode_errors_change_triggers_rebuild incorrectly uses force_rebuild() and asserts rebuild occurred for style-only property (FIXED: Renamed and updated assertions)
- [x] Lines 776-805: test_strip_change_triggers_rebuild incorrectly uses force_rebuild() and asserts rebuild occurred for style-only property (FIXED: Renamed and updated assertions)
- [x] Lines 809-851: test_disabled_change_triggers_rebuild (complex) incorrectly uses force_rebuild() and asserts rebuild occurred for style-only property (FIXED: Renamed and updated assertions)
- [x] Lines 497-531, 535-569, 571-607, 677-704, 711-738: No-rebuild tests use naming not matching recommended patterns (FIXED: Renamed all to follow test_*_preserves_widget_tree pattern)

## test_coordinate_translation.py

- Lines 34, 65, 233, 273, 302, 593, 928: Missing @pytest.mark.property (Test Types and Markers)
- Lines 175-194: Test name "test_refs_translation_with_nested_list_markup" does not accurately reflect assertions - tests markup production, not coordinate translation (Test Naming Conventions)
- Lines 195-214: Test name "test_refs_translation_with_table_markup" does not accurately reflect assertions - tests markup production, not coordinate translation (Test Naming Conventions)
- Lines 215-231: Test name "test_refs_translation_with_blockquote_markup" does not accurately reflect assertions - tests markup production, not coordinate translation (Test Naming Conventions)

## test_font_properties.py

- Lines 527-541: Defines local collect_labels_and_scales accessing private '_font_scale' attribute (Best Practices: no implementation testing)
- Lines 577-601: Accesses private '_font_scale' attribute and internal KivyRenderer.HEADING_SIZES constant (Best Practices: no implementation testing)
- Lines 650-673: Accesses private '_font_scale' attribute and internal KivyRenderer.HEADING_SIZES constant (Best Practices: no implementation testing)
- Lines 684-685: Non-standard rationale in Hypothesis strategy comment ("~57 finite list combinations × sampled" instead of exact "N finite × M complex samples") (Property-Based Testing Optimization)
- Lines 695-724: Accesses private '_font_scale' attribute and internal KivyRenderer.HEADING_SIZES constant (Best Practices: no implementation testing)
- Lines 739-769: Accesses private '_font_scale' attribute and internal KivyRenderer.HEADING_SIZES constant (Best Practices: no implementation testing)
- Lines 894-919: Monkeypatches private _rebuild_widgets method to count invocations (Best Practices: no implementation testing)

## test_kivy_renderer_blocks.py

- Line 102: Accessing internal constant [`KivyRenderer.HEADING_SIZES`](kivy_garden/markdownlabel/kivy_renderer.py) (Best practices: no implementation testing)
- Line 264: Asserting specific hardcoded padding value `20` (Best practices: no implementation testing)
- Line 320: Checking private attribute `_bg_rect` (Best practices: no implementation testing)
- Line 400: Checking private attribute `_border_line` (Best practices: no implementation testing)
- Line 433: Checking private attribute `_hr_line` (Best practices: no implementation testing)

## test_kivy_renderer_tables.py

- Lines 246-338: TestDeepNestingTruncation class tests general _render_token truncation behavior, unrelated to table rendering (Test Organization: No mixing unrelated functionality)
- Lines 343-650: TestKivyRendererEdgeCases includes tests for non-table components (list_item, image, block_code, block_quote, text_size_binding, blank_line) (Test Organization: No mixing unrelated functionality)
- Lines 152,223: Direct calls to private method renderer._render_table_cell (Best Practices: no implementation testing)
- Lines 267,288,306,329,572,586: Direct calls to private method renderer._render_token (Best Practices: no implementation testing)
- Line 388: Direct call to private method renderer._render_list_item (Best Practices: no implementation testing)
- Lines 258,302,571: Direct manipulation of private attribute renderer._nesting_depth (Best Practices: no implementation testing)
- Lines 237-241: Asserts existence and value of implementation-specific 'cell_align' attribute on Labels (Best Practices: no implementation testing)
- Lines 397-650 (multiple methods in TestKivyRendererEdgeCases): Uses patching/mocking to verify internal method calls, manual callback invocations, and coverage-focused assertions (e.g., mock_list.called, mock_image.bind.called, MockRect verification) (Best Practices: no implementation testing)
- Lines 1-6: Module docstring claims focus on "table-specific features" but file includes unrelated tests (Test File Structure: Standard template)

## test_rebuild_advanced_properties.py

- Line 130: Incorrect strategy classification "Finite strategy" instead of "Mixed finite/complex strategy" (includes complex markdown_text strategy) (Property-Based Testing Optimization)
- Lines 418-419: Incorrect strategy classification "Finite strategy" instead of "Mixed finite/complex strategy" (includes complex markdown_text strategy) (Property-Based Testing Optimization)

## test_rebuild_identity_preservation.py

- Line 232: Non-standard phrasing in standardized max_examples comment ("120 finite combinations with 5 complex strategies" instead of "[finite_size] finite × [samples] complex samples") (Property-Based Testing Optimization)
- Line 294: Non-standard phrasing in standardized max_examples comment ("24 finite combinations with 4 complex strategies" instead of "[finite_size] finite × [samples] complex samples") (Property-Based Testing Optimization)
- Line 336: Inaccurate finite count (actual 8 finite combinations from 2×2×2, reported 24) in standardized max_examples comment (Property-Based Testing Optimization)

## test_rebuild_structure_changes.py

- Lines 23-181: Class TestStructurePropertyRebuild mixes style-only properties (font_name, text_size) with structure properties, violating "One class per property or behavior" and "No mixing unrelated functionality" (Test Organization).
- Lines 27, 87-108: Class docstring lists text_size as structure property; test_text_size_change_triggers_rebuild incorrectly expects rebuild and uses force_rebuild() for style-only text_size (Rebuild Contract Testing).
- Lines 56-86, 237-277: test_font_name_change_preserves_widget_tree and PBT version use private attribute '_is_code' to identify code labels, violating "no implementation testing" (Best Practices).
- Line 191: Incorrect strategy classification "Mixed finite/complex strategy: 50 examples (complex samples)" for two complex simple_markdown_document() strategies; should use "Complex strategy" classification (Property-Based Testing Optimization).

## test_rebuild_style_propagation.py

- Lines 23-208: Tests verify style property value propagation but do not verify widget tree preservation (no rebuild) for style-only property changes, missing collect_widget_ids/assert_no_rebuild usage (Rebuild Contract Testing - Testing Style-Only Changes (No Rebuild))
- Line 147: Standardized comment rationale does not match required format for mixed finite/complex strategy ("60 finite combinations with 3 complex strategies" vs "[finite_size] finite × [samples] complex samples") (Property-Based Testing Optimization)

## test_rebuild_text_size_and_code_blocks.py

- Lines 62-64: Non-standardized multi-line comment above @settings; extra "Feature" line and rationale "(4 text_size patterns with complex markdown)" does not precisely match "Mixed finite/complex strategy: finite*samples (N finite × M complex)" template (Property-Based Testing Optimization)
- Lines 255-259: Non-standardized multi-line comment above @settings; rationale "(font_family is text)" does not match required "adequate coverage/performance optimized" for Complex strategy (Property-Based Testing Optimization)
- Line 105: Missing @pytest.mark.unit marker on TestTextSizeBindingTransitions class (Test Types and Markers)
- Lines 139-140: Meaningless assertion `assert child_label.text_size is not None` (always true, Label.text_size is ListProperty); fails to verify text_size updated to reflect width constraint as method docstring claims (Test Naming Conventions, Best Practices)
- Lines 163-169: No actual assertion in test_text_size_width_constrained_to_none_updates_bindings; conditional `pass` comment does not verify binding update (Test Naming Conventions, Best Practices)

## test_rtl_alignment.py

- Line 280: Method name 'test_direction_change_preserves_widget_identities' does not follow 'test_*_preserves_widget_tree_*' pattern for no-rebuild tests (Test Naming Conventions)
- Lines 477-492: Tests private method '_get_effective_halign()' and trivial MarkdownLabel.halign assertion (Best Practices: no implementation testing)

## test_serialization.py

- Line 649: Non-standard rationale "(two complex strategies combined)" in standardized property-based testing comment (Property-Based Testing Optimization)

## test_shortening_properties.py

- Lines 26-346: Missing @pytest.mark.property decorator on all property-based tests using Hypothesis (Test Types and Markers)
- Lines 318-346: test_shorten_change_triggers_rebuild incorrectly expects widget tree rebuild (ids_before != ids_after), uses force_rebuild(), and has "triggers_rebuild" name for style-only 'shorten' property; should expect no rebuild (ids_before == ids_after), no force_rebuild(), and "preserves_widget_tree" name (Rebuild Contract Testing: Truncation Properties style-only, Using `force_rebuild()` in Tests, Test Naming Conventions: Rebuild Testing Names)
- Lines 263-274: test_empty_ellipsis_options_not_forwarded has misleading name and docstring claiming "not forwarded" but asserts lbl.ellipsis_options == {} (forwarded as default) (Test Naming Conventions: method names accurately reflect assertions)

## test_sizing_behavior.py

Line 25: Incorrect standardized comment rationale "(variable-length document with complex text)" (Property-Based Testing Optimization)
Line 43: Incorrect standardized comment rationale "(6 heading levels × complex text content)" (Property-Based Testing Optimization)
Line 97: Incorrect standardized comment rationale "(variable-length document with complex text)" (Property-Based Testing Optimization)
Line 108: Incorrect standardized comment rationale "(variable-length document with complex text)" (Property-Based Testing Optimization)
Line 168: Incorrect standardized comment rationale "(variable-length document with complex text)" (Property-Based Testing Optimization)
Line 183: Incorrect standardized comment rationale "(two complex inputs: document + float)" (Property-Based Testing Optimization)
Line 201: Incorrect standardized comment rationale "(variable-length document with complex text)" (Property-Based Testing Optimization)
Line 232: Incorrect standardized comment rationale "(variable-length document with complex text)" (Property-Based Testing Optimization)
Line 255: Incorrect standardized comment rationale "(variable-length document with complex text)" (Property-Based Testing Optimization)
Line 277: Incorrect standardized comment rationale "(two complex inputs: document + float)" (Property-Based Testing Optimization)
Line 346: Incorrect standardized comment rationale "(variable-length document with complex text)" (Property-Based Testing Optimization)
Line 361: Incorrect standardized comment rationale "(two complex inputs: document + float)" (Property-Based Testing Optimization)
Line 379: Incorrect standardized comment rationale "(variable-length document with complex text)" (Property-Based Testing Optimization)
Line 430: Incorrect standardized comment rationale "(variable-length document with complex text)" (Property-Based Testing Optimization)
Line 453: Incorrect standardized comment rationale "(variable-length document with complex text)" (Property-Based Testing Optimization)
Line 477: Incorrect standardized comment rationale "(two complex inputs: document + float)" (Property-Based Testing Optimization)
Line 504: Incorrect standardized comment rationale "(variable-length document with complex text)" (Property-Based Testing Optimization)
Line 539: Incorrect standardized comment rationale "(variable-length document with complex text)" (Property-Based Testing Optimization)
Line 563: Incorrect standardized comment rationale "(variable-length document with complex text)" (Property-Based Testing Optimization)

## test_text_properties.py

Line 272: Uses force_rebuild() after style-only text_size change (Using force_rebuild() in Tests)
Line 296: Uses force_rebuild() after style-only text_size change (Using force_rebuild() in Tests)
Line 322: Uses force_rebuild() after style-only text_size change (Using force_rebuild() in Tests)
Line 421: test_unicode_errors_change_triggers_rebuild method name incorrectly claims rebuild trigger for style-only unicode_errors property (Test Naming Conventions)
Line 422: Docstring claims "triggers widget rebuild" for style-only unicode_errors change (Rebuild Contract Testing)
Line 435: Uses force_rebuild() after style-only unicode_errors change (Using force_rebuild() in Tests)
Lines 438-439: Asserts widget tree rebuild occurred (ids_before != ids_after) for style-only unicode_errors change (Rebuild Contract Testing)
Line 539: test_strip_change_triggers_rebuild method name incorrectly claims rebuild trigger for style-only strip property (Test Naming Conventions)
Line 540: Docstring claims "triggers widget rebuild" for style-only strip change (Rebuild Contract Testing)
Line 553: Uses force_rebuild() after style-only strip change (Using force_rebuild() in Tests)
Lines 556-557: Asserts widget tree rebuild occurred (ids_before != ids_after) for style-only strip change (Rebuild Contract Testing)

## test_texture_render_mode.py

Lines 146-149: Asserting hasattr(label, '_aggregated_refs') and isinstance(label._aggregated_refs, dict) (Best Practices: no implementation testing)
Line 167: Asserting label._aggregated_refs == {} (Best Practices: no implementation testing)
Lines 187-193: Asserting label._aggregated_refs truthiness and ref in label._aggregated_refs (Best Practices: no implementation testing)
Lines 581, 596, 610, 624, 644, 660, 673: Calling label._get_effective_render_mode() (Best Practices: no implementation testing)

## test_texture_sizing.py

Line 76: test_heading_creates_label_widget docstring claims "Label widget" but no assertion verifying Label type (Test Naming Conventions)
Line 93: test_paragraph_creates_label_widget docstring claims "Label widget" but no Label type assertion (Test Naming Conventions)
Line 109: test_code_block_creates_container_widget docstring claims "BoxLayout container" but no BoxLayout assertion (Test Naming Conventions)
Line 124: test_list_creates_container_widget docstring claims "BoxLayout container" but no BoxLayout assertion (Test Naming Conventions)
Line 158: test_block_quote_creates_container_widget docstring claims "BoxLayout container" but no BoxLayout assertion (Test Naming Conventions)
Line 253: test_nested_list_creates_nested_containers docstring claims "nested BoxLayout containers" but no assertion for nesting or BoxLayout (Test Naming Conventions)
Line 271: test_ordered_list_creates_container_widget docstring claims "BoxLayout container" but no BoxLayout assertion (Test Naming Conventions)
Line 338: test_all_heading_levels_create_label_widgets docstring claims "Label widgets" but no Label assertion (Test Naming Conventions)
Line 353: test_blank_lines_create_spacer_widgets docstring claims "spacer widgets" but no assertion verifying spacer widgets (Test Naming Conventions)
Line 287: Non-standard rationale in Hypothesis settings comment "(two complex strategies combined)"; expected "(adequate coverage/performance optimized)" for complex strategy (Property-Based Testing Optimization)

