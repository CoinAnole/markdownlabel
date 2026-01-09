# Test Files Deviations Summary

Generated from analysis against TESTING.md guidelines.

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

