# Test Suite Deviations from TESTING.md Guidelines

Files not listed have no deviations.

## test_color_properties.py
- Line 82: Test method name "test_color_change_updates_value_without_rebuild" uses value update pattern but verifies no widget tree rebuild occurred; should use "test_*_preserves_widget_tree_*" pattern for no-rebuild verification tests (Test Naming Conventions)

## test_font_properties.py
- Lines 317-342: Helper functions _find_code_block_labels and _find_non_code_labels use internal undocumented 'language_info' attribute to identify code block containers (Best Practices)
- Lines 570, 640, 680, 726: Imports inside test methods of internal `kivy_garden.markdownlabel.kivy_renderer.KivyRenderer.HEADING_SIZES` to compute expected values (Best Practices)
- Lines 598-604, 800-807, 815-822: Manual iteration over `label.children` assuming direct single `Label` child, testing specific internal widget tree structure (Best Practices)

## test_inline_renderer.py
- Line 831: Testing private method renderer._unknown(token) directly without justification comment (Best Practices, Testing Exceptions)
- Lines 848-852: Testing private method renderer._escape_markup() directly without justification comment (Best Practices, Testing Exceptions)

## test_kivy_renderer_blocks.py
- Lines 225-266: Test name `test_nested_list_increases_indentation` and docstring claim verification of increasing padding per nesting level, but assertions only check fixed outer list padding without traversing nested lists or verifying increases (Test Naming Conventions)
- Lines 477-569: Entire `TestDeepNestingTruncation` class directly sets private `_nesting_depth` attribute and calls private `_render_token` method without justification or listed exception (Best Practices, Testing Exceptions)
- Lines 582-611: `test_render_list_item_nested_structures` calls private `_render_list_item` method (Best Practices, Testing Exceptions)
- Lines 613-638: `test_image_on_texture_callback` tests internal texture callback implementation details via patching and manual invocation (Best Practices)
- Lines 640-656: `test_block_code_update_bg_logic` tests internal background update logic by manually setting pos/size post-creation and inspecting patched Rectangle (Best Practices)
- Lines 658-670: `test_block_quote_update_border_logic` tests internal border update logic similarly (Best Practices)
- Lines 672-679: `test_deep_nesting_truncation_method` sets private `_nesting_depth` and calls `_render_token` (Best Practices, Testing Exceptions)
- Lines 681-684: `test_unknown_token_render` calls private `_render_token` (Best Practices, Testing Exceptions)
- Lines 706-711, 713-718: `test_text_size_binding_strict_mode` and `test_text_size_binding_height_only` call private `_apply_text_size_binding` method (Best Practices, Testing Exceptions)

## test_kivy_renderer_tables.py
- Lines 150, 221: Direct calls to private method `renderer._render_table_cell()` without justification (Best Practices, Testing Exceptions)
- Lines 235-239: Verifying internal attribute `child.cell_align` without public equivalent or justification (Best Practices, Testing Exceptions)
- Lines 198-208: Manual indexing of `widget.children` assuming reversed row-major order specific to GridLayout implementation (Best Practices)
- Line 254: `test_table_internals_coverage` name and docstring claim testing internal methods but only asserts public `table()` returns non-None GridLayout (Test Naming Conventions)

## test_padding_properties.py
- Lines 390-546: Class `TestPaddingWithNestedStructures` and contained test methods have vague/misleading names and docstrings referring to generic "padding" applied to Labels, but actually test `text_padding` forwarding to Labels in nested structures (Test Organization, Test Naming Conventions)

## test_rebuild_identity_preservation.py
- Lines 26-55: TestWidgetIdentityHelpers class mixes unrelated meta-tests for general helper functions with MarkdownLabel-specific rebuild identity preservation tests (Test Organization)
- Line 276: Incorrect max_examples rationale ("120 finite × 5 complex samples" where 120×5=600 ≠50) (Property-Based Testing Optimization)
- Line 338: Incorrect max_examples rationale ("24 finite × 4 complex samples" where 24×4=96 ≠50) (Property-Based Testing Optimization)
- Line 380: Incorrect max_examples rationale ("24 finite × 2 complex samples" where finite product=2×2×2=8 ≠24) (Property-Based Testing Optimization)
- Line 380: Misclassifies font_name (style-only property) as structure property in test claiming "structure property changes" (Rebuild Contract Testing)
- Line 459: Incorrect max_examples rationale ("3 finite × 5 complex samples" but no finite strategies; both strategies complex) (Property-Based Testing Optimization)

## test_shortening_properties.py
- Lines 44, 58, 73, 156, 173, 187, 219, 235, 252: Missing `@pytest.mark.property` marker on property-based tests using Hypothesis (Test Types and Markers)
- Line 325: `max_examples=2` for combination of two `st.booleans()` strategies (finite space size=4); recommended product of sizes for all-finite combination strategies (Property-Based Testing Optimization)

## test_serialization.py
- Line 718: Testing private method `_serialize_token` without justification (Best Practices, Testing Exceptions)
- Line 754: Testing private method `_serialize_list_item` without justification (Best Practices, Testing Exceptions)
- Line 765: Testing private method `_serialize_list_item` without justification (Best Practices, Testing Exceptions)

## test_sizing_behavior.py
- Line 159: Testing private attribute `label._user_size_hint_y` without justification or inclusion in acceptable exceptions list (Best Practices, Testing Exceptions)
- Lines 45, 110, 203, 380: Test names `test_height_bound_to_minimum`, `test_auto_size_height_true_binds_height_to_minimum`, `test_auto_size_height_false_no_height_binding`, `test_strict_mode_height_not_bound_to_minimum` assert `size_hint_y` preconditions/participation in layout but do not verify actual height binding to `minimum_height`, mismatching assertions (Test Naming Conventions)
- Lines 409-416, 418-426: Hypothesis `@given(st.booleans())` `@pytest.mark.property` for trivial single-dimension boolean property set/get verification; prefer `@pytest.mark.parametrize` for cleaner exhaustive coverage of small finite input space (When to Use Hypothesis vs. @pytest.mark.parametrize)

## test_texture_sizing.py
- Lines 82-86, 103-107, 121-124, 138-141, 155-160, 174-177, 274-277, 290-294: Duplicated manual checks for specific child widget presence and types instead of using or defining helper functions (Helper Functions)
- Lines 39-47, 56-62, 88-92, 109-113, 126-130, 143-147, 162-166, 179-183, 233-238, 255-258, 279-283, 296-300, 320-327: Duplicated assertions validating texture_size structure, length, and non-negativity instead of using helper functions (Helper Functions)
- Lines 197-202, 350-355: Use of Hypothesis for small finite single-dimension strategies instead of @pytest.mark.parametrize (When to Use Hypothesis vs. @pytest.mark.parametrize)
