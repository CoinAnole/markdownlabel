# Deviations

## test_core_functionality.py

- **Lines 67-80 (`test_paragraph_produces_label_widget`)**: Docstring states `"Paragraph Markdown produces a Label widget."`, but assertion only `assert len(label.children) >= 1` (no `isinstance(child, Label)` check, unlike similar `test_heading_produces_label_widget`). Violates [Test Naming Conventions](#test-naming-conventions): Docstrings must accurately reflect assertions.

- **Lines 111-132 (`test_text_change_updates_widgets`)**: Docstring `"Changing text property updates the widget tree."` and method name imply widget tree verification, but only asserts `label.text == text2` (trivial setter check). `initial_children = len(label.children)` (line 122) collected but unused (dead code). Relevant code snippet:

  ```python

  initial_children = len(label.children)  # unused

  label.text = text2

  assert label.text == text2

  ```

Violates [Test Naming Conventions](#test-naming-conventions) and [Best Practices](#best-practices).

- **Lines 182-204 (`test_ast_updates_with_text`)**: Docstring `"AST tokens update when text changes."` implies AST verification, but `ast1 = label.get_ast()` (line 191) and `ast2 = label.get_ast()` (line 197) unused. Only asserts `label.text == text2` if texts differ. Relevant code snippet:

  ```python

  ast1 = label.get_ast()  # unused

  ...

  ast2 = label.get_ast()  # unused

  if text1 != text2:

    assert label.text == text2

  ```

  Violates [Test Naming Conventions](#test-naming-conventions) and [Best Practices](#best-practices).

## test_label_compatibility.py

- **Lines 32, 42, 55, 67, 79, 84 (TestFontSizeAliasBidirectionality methods)**: Float equality assertions use direct `==` instead of `floats_equal()` helper from [`test_utils.py`](kivy_garden/markdownlabel/tests/test_utils.py). Example (line 32):

  ```python

  assert label.base_font_size == font_size_value

  ```
  Violates [Helper Functions](#helper-functions) section: "Always use helper functions from `test_utils.py` instead of duplicating code".

- **Lines 260, 310, 340 (outline_color assertions in TestNoOpPropertyAcceptanceAndStorage)**: Color equality uses manual `all(abs(a - b) < 0.001 for a, b in zip(...))` instead of `colors_equal()` helper from [`test_utils.py`](kivy_garden/markdownlabel/tests/test_utils.py). Example (line 260):

  ```python

  assert all(abs(a - b) < 0.001 for a, b in zip(label.outline_color, value))

  ```

  Violates [Helper Functions](#helper-functions) section: "Always use helper functions from `test_utils.py` instead of duplicating code".

- **Lines 407-486 (TestImportFunctionality class)**: Contains meta-tests with `@pytest.mark.test_tests` in a file for "Basic label property forwarding". Meta-tests should be in `meta_tests/` directory per project structure. Violates [Test Organization](#test-organization) > File Organization.

- **Lines 157-181 (`test_noop_properties_do_not_affect_rendering`), 377-402 (`test_advanced_noop_properties_do_not_affect_rendering`)**: Checks rendering unaffected using `len(children)` on separately created labels instead of `collect_widget_ids()` and `assert_no_rebuild()` after setting properties on the same instance. Example (line 164):
  ```python

  default_child_count = len(label_default.children)

  ```
  Violates [Rebuild Contract Testing](#rebuild-contract-testing) and [Helper Functions](#helper-functions): Use rebuild helpers for proper structure preservation verification.

## test_color_properties.py

- **Lines 1-7 (file docstring)**: Claims "color properties (color, disabled_color) are correctly forwarded [...] based on the widget's disabled state", but no tests for `disabled_color` forwarding, application, or disabled state behavior. Violates [Test File Structure](#test-file-structure) and [Best Practices](#best-practices): File docstrings must accurately describe tests provided.

- **Lines 79-101 (`test_color_change_updates_value`)**: Docstring claims "Changing color updates color on existing widgets without rebuild", implying preservation of widget instances/tree, but test performs no rebuild verification (no `collect_widget_ids()` before change, no `assert_no_rebuild()` or ID comparison after). Only verifies value update via `find_labels_recursive()`. Violates [Test Naming Conventions](#test-naming-conventions): Docstrings must accurately reflect assertions. Deviates from [Rebuild Contract Testing](#rebuild-contract-testing) > Testing Style-Only Changes (No Rebuild) pattern which requires tree preservation check:

  ```python

    @given(color_strategy, color_strategy)

    # Complex strategy: 50 examples (adequate coverage)

    @settings(max_examples=50, deadline=None)

    def test_color_change_updates_value(self, color1, color2):

        """Changing color updates color on existing widgets without rebuild."""  # Unverified claim

        assume(not colors_equal(color1, color2))

        label = MarkdownLabel(text='Hello World', color=color1)

        # Verify initial

        labels = find_labels_recursive(label)

        for lbl in labels:

            assert colors_equal(list(lbl.color), color1)

        # Missing preservation check:

        # ids_before = collect_widget_ids(label)

        label.color = color2  # Style-only change

        # Missing: assert_no_rebuild(label, ids_before)

        # Recollects labels (would be new if rebuilt)

        labels = find_labels_recursive(label)

        for lbl in labels:

            assert colors_equal(list(lbl.color), color2)

  ```
## test_text_properties.py

- **Lines 270, 294, 320**: Unnecessary `label.force_rebuild()` calls in `TestTextSizeDynamicUpdates` class methods (`test_text_size_height_change_updates_labels`, `test_text_size_height_to_none_updates_labels`, `test_text_size_none_to_height_updates_labels`). `text_size` is listed as a style-only property ([`TESTING.md #Rebuild Contract Testing > Style-Only Properties`](kivy_garden/markdownlabel/tests/TESTING.md:231)). Guideline states: "When NOT to Use `force_rebuild()`: 1. **Testing style-only properties** — These update widgets in place without rebuilding, so no `force_rebuild()` is needed" ([`TESTING.md`](kivy_garden/markdownlabel/tests/TESTING.md:424-436)). Example relevant code (line 270):

  ```python
  label.text_size = [None, height2]

  label.force_rebuild()  # Unnecessary for style-only property

  ```
  These tests should instead verify no rebuild occurs using `ids_before = collect_widget_ids(label)` before change, `assert_no_rebuild(label, ids_before)` after change (no `force_rebuild()`), and confirm child label values updated.

- **Lines 84-96 (`test_text_size_with_width_passed_to_renderer`)**: Method docstring claims "`text_size` with width is passed to renderer and affects internal Labels", but assertions only verify `label.text_size[0] == width` and `len(labels) >= 1`; does **not** assert child Labels have `text_size[0] == width`. Violates "`Test method names should **accurately reflect what they assert`**" ([`TESTING.md #Test Naming Conventions`](kivy_garden/markdownlabel/tests/TESTING.md:111-152)). Relevant code:

  ```python
  labels = find_labels_recursive(label)

  assert len(labels) >= 1, "Expected at least one Label"

  # Missing: assert lbl.text_size[0] == width for lbl in labels

  ```

- **Lines 229-231, 242-244, 299-301**: Unnecessary defensive checks `if hasattr(lbl, 'text_size') and lbl.text_size:` before `assert lbl.text_size[1] is None`. All child widgets are `Label` instances with `text_size` ListProperty([None, None]), always present. Violates [Best Practices #Proper assertions, etc.](kivy_garden/markdownlabel/tests/TESTING.md:1022+) for clean, direct assertions. Example (line 229):

  ```python
  if hasattr(lbl, 'text_size') and lbl.text_size:

      assert lbl.text_size[1] is None, ...
  ```

## test_padding_properties.py

- **Line 136** (TestPaddingForwarding docstring): `"Property tests for padding forwarding."` but all tests in class set `label.text_padding=padding` and verify child label padding (text_padding forwarding). `padding` property affects container only. Inaccurate description. Violates [Test Organization](#test-organization) > Class Organization and [Test Naming Conventions](#test-naming-conventions).

- **Lines 239, 290, 322** (`test_padding_change_updates_in_place`, `test_padding_update_updates_in_place`, `test_padding_update_updates_in_place_complex_content`): Test names refer to "padding" change/update but code changes `label.text_padding`. Relevant code (line 254): `label.text_padding = padding2`. Violates [Test Naming Conventions](#test-naming-conventions): names must accurately reflect assertions/property tested.

- **Lines 239, 290, 322**: Tests verify no rebuild (`ids_before == ids_after`) for text_padding changes (style-only) but use `test_*_updates_in_place` naming instead of `test_*_preserves_widget_tree_*`. Example assertion (line 258): `assert ids_before == ids_after, "Widget tree should NOT rebuild for text_padding changes"`. Violates [Test Naming Conventions](#test-naming-conventions) > Rebuild Testing Names (line 118).

- **Lines 40-46, 59-64, 73-79, 89-94, 107-108, 114-116, 123-129**: Manual `for i, (actual, exp) in enumerate(zip(...)): assert abs(actual - exp) < 0.001` for padding float comparisons instead of imported `padding_equal(label.padding, expected)`. Example (lines 40-46):

  ```python

  for i, (actual, exp) in enumerate(zip(label.padding, expected)):

      assert abs(actual - exp) < 0.001, f"Padding[{i}]: expected {exp}, got {actual}"

  ```
  Violates [Helper Functions](#helper-functions): Always use helpers like `padding_equal` from [`test_utils.py`](kivy_garden/markdownlabel/tests/test_utils.py).

## test_sizing_behavior.py

- **Lines 515-529 (`test_strict_mode_updates_value`)**: Test name and docstring `"Changing strict_label_mode triggers widget rebuild."` claim rebuild verification, but no `collect_widget_ids()`, `assert_rebuild_occurred()`, `force_rebuild()`, or ID comparison. `initial_children = list(label.children)` (line 520) unused dead code. Assertion `len(label.children) >= 1` (lines 528-529) holds pre-toggle. Relevant code:

  ```python
  initial_children = list(label.children)  # unused (line 520)

  label.strict_label_mode = True  # (line 523)

  assert len(label.children) >= 1  # (lines 528-529)

  ```
  Violates [Rebuild Contract Testing](#rebuild-contract-testing) (requires ID collection/helpers for rebuild verification) and [Test Naming Conventions](#test-naming-conventions) (name/doc mismatch assertion).

- **Lines 45-54 (`test_height_bound_to_minimum`)**: Docstring `"auto_size_height=True binds height to minimum_height."` claims height binding verification, but only asserts `label.size_hint_y is None` (line 53). No `height`/`minimum_height` check. Violates [Test Naming Conventions](#test-naming-conventions).

- **Lines 67-79 (`test_more_content_means_more_height_potential`)**: Docstring `"More content should result in more minimum height."` but asserts `len(label.children) >= num_paragraphs` (line 77) and `size_hint_y is None` (line 75); no `minimum_height`/`height` comparison across content lengths. Violates [Test Naming Conventions](#test-naming-conventions).

- **Lines 101-113 (`test_auto_size_height_true_binds_height_to_minimum`)**: Docstring `"When auto_size_height=True, height should be bound to minimum_height."` but only asserts `size_hint_y is None` (line 107) and property value. No binding verification. Violates [Test Naming Conventions](#test-naming-conventions).

- **Lines 557-587 (`test_all_classes_test_related_functionality`)**: `@pytest.mark.test_tests` meta-test validating file class organization placed in `TestStrictLabelModeSizingBehavior` class (unrelated). Violates [Test Organization](#test-organization) > Class Organization ("One class per property or behavior", related methods grouped). Meta-tests exampled in `meta_tests/` directory.

- **Multiple Hypothesis `@settings` comments (e.g., lines 88-89, 154-155, etc.)**: Classify `@given(simple_markdown_document())`/`markdown_heading()` as `"Mixed finite/complex strategy: 20 examples (5 finite × 4 complex samples)"` inconsistent with line 25 `"Complex strategy"` and guideline for single composite strategies (Complex/Infinite). `markdown_heading()` internal finite levels (6) vs comment "5 finite". Violates [Property-Based Testing Optimization](#property-based-testing-optimization) > Comment Format Requirements/Strategy Classifications.

## test_advanced_compatibility.py

- **Lines 154-181, 847-869 (`test_font_kerning_change_triggers_rebuild`)** and **Lines 185-212, 871-894 (`test_font_blended_change_triggers_rebuild`)**: Exact duplicate test methods across `TestAdvancedFontPropertiesForwarding` and `TestReactiveRebuildOnPropertyChange` classes. 
  ```python

  @given(st.booleans(), st.booleans())

  # Combination strategy: 4 examples (combination coverage)

  @settings(max_examples=4, deadline=None)

  def test_font_kerning_change_triggers_rebuild(self, kerning1, kerning2):

    # Identical implementation duplicated

  ``` 
  Violates [Best Practices](#best-practices) against code duplication (cf. [Helper Functions](#helper-functions) "no duplication").

- **Lines 824-844 (`test_rebuild_preserves_content_structure`)**: Structure property change (`font_name`) without `label.force_rebuild()` after change. Deferred rebuild not synchronized for verification. 
  ```python

  label.font_name = font2

  # Missing: label.force_rebuild()

  children_after = len(label.children)

  assert children_before == children_after

  ``` 
  Violates [Using `force_rebuild()` in Tests](#using-force_rebuild-in-tests): Required for structure changes.

- **Lines 682-702 (`test_halign_updates_value`)** and **Lines 709-729 (`test_valign_updates_value`)**: Style-only properties (`halign`, `valign` per Style-Only Properties list) missing no-rebuild verification. No `collect_widget_ids()`/`ids_before == ids_after`. 
  ```python

  label.halign = halign2

  # Missing: ids_before = collect_widget_ids(label) before change

  # assert_no_rebuild(label, ids_before) or manual comparison

  labels_after = find_labels_recursive(label)

  ``` 
  Violates [Testing Style-Only Changes (No Rebuild)](#testing-style-only-changes-no-rebuild).

- **Lines 735-756 (`test_unicode_errors_change_triggers_rebuild`)**: Name/doc claims "triggers rebuild", calls `force_rebuild()`, but no rebuild verification (`ids_before != ids_after` or `assert_rebuild_occurred`). 
  ```python

  label.unicode_errors = errors2

  label.force_rebuild()

  # Missing rebuild occurrence assert

  labels_after = find_labels_recursive(label)

  ``` 
Violates [Testing Structure Changes (Rebuild Required)](#testing-structure-changes-rebuild-required).

- **Lines 760-782 (`test_strip_updates_value`)**: Calls `force_rebuild()` (structure-like) but name/doc "updates_value" implies style-only no rebuild. No rebuild verification. Inconsistent naming. 
  ```python

  label.strip = strip2

  label.force_rebuild()

  # No ids comparison

  ``` 
  Violates [Test Naming Conventions](#test-naming-conventions) > Rebuild Testing Names.

- **Lines 611-644 (`test_text_size_updates_value`)**: Verifies `label.text_size` update and no rebuild, but not child Labels' `text_size` (unlike `test_color_updates_value`, `test_line_height_updates_value`). Incomplete forwarding check. 
  ```python
  assert label.text_size[0] == width2
  labels_after = find_labels_recursive(label)
  assert len(labels_after) >= 1
  # Missing: assert lbl.text_size[0] == width2 for lbl in labels_after
  ```
  Best Practices: proper/complete assertions consistent with forwarding patterns.

- **Lines 786-820 (`test_disabled_change_updates_value`)**: Changes `disabled` (rebuild-triggering per lines 357-407), no `force_rebuild()`, no rebuild verification. Relies on deferred rebuild. 
  ```python
  label.disabled = disabled2
  # Missing force_rebuild() and rebuild check
  labels_after = find_labels_recursive(label)
  ```
  Violates [Rebuild Contract Testing](#rebuild-contract-testing) patterns.

- **Lines 142-203 (TestPaddingForwarding: `test_padding_applied_to_paragraph/heading/list_items/table_cells`) and 554-614 (TestTextPaddingAppliesToChildLabels: `test_text_padding_applied_to_paragraph_labels` etc.)**: Duplicate tests verifying `text_padding` forwarding to paragraph/heading/list/table Labels. Identical pattern: `label.text_padding=padding`; `labels = find_labels_recursive(label)`; `padding_equal(lbl.padding, padding)` for all lbl. Violates best practices against duplication [Helper Functions](#helper-functions), [Test Organization](#test-organization).

## test_serialization.py

- **Line 648** (`test_code_serialization_round_trip_property` method): Non-standard rationale in Hypothesis `@settings` comment `# Complex strategy: 20 examples (two complex strategies combined)`. Both strategies are `st.text()` (Complex/Infinite). Relevant code:
  ```python
  @given(
      st.text(min_size=0, max_size=200),
      st.text(
          alphabet=st.characters(whitelist_categories=('L', 'N')),
          min_size=0,
          max_size=20
      )
  )
  # Complex strategy: 20 examples (two complex strategies combined)

  @settings(max_examples=20, deadline=None)
  ```
  Violates [Property-Based Testing Optimization](#property-based-testing-optimization) > Comment Format Requirements: For Complex strategies, rationale must be `(adequate coverage)` or `(performance optimized)`; custom rationales not standardized.

## test_performance.py

- **Lines 30-55 (`test_font_size_change_preserves_widget_tree`)**: Verifies no rebuild but lacks assertion that `font_size` change was applied to child Labels. Relevant code (lines 45-53):
  ```python
  label.font_size = new_size
  ids_after = collect_widget_ids(label)
  assert ids_before == ids_after
  ```
  No `labels = find_labels_recursive(label)`; `assert lbl.font_size == new_size`. Violates [Rebuild Contract Testing](#rebuild-contract-testing) > Style-Only Changes example (lines 261-264).

- **Lines 239-258 (`test_text_structure_property_rebuilds_tree`)**: Verifies rebuild but lacks post-rebuild content verification. Relevant code (lines 249-257):
  ```python
  label.text = 'Second paragraph with different content.'
  label.force_rebuild()
  ids_after = collect_widget_ids(label, exclude_root=True)
  assert ids_before != ids_after
  ```
  Missing `assert label.text == 'Second paragraph with different content.'`. Violates [Testing Structure Changes](#testing-structure-changes-rebuild-required) example (lines 284-285).

- **Lines 259-278 (`test_font_name_structure_property_rebuilds_tree`)**: Wrongly expects rebuild for style-only `font_name` (lines 269-276):
  ```python
  label.font_name = 'RobotoMono-Regular'
  label.force_rebuild()
  assert ids_before != ids_after
  ```
  `font_name` is style-only ([Style-Only Properties](##style-only-properties) lines 226-232). Should verify no rebuild and `lbl.font_name` updated. Naming also violates Rebuild Testing Names (lines 117-120).

- **Lines 95, 336, 344, 351 (`test_color_change_updates_descendant_labels`, `test_disabled_color_switching`)**: Manual `list(child_label.color) == [...]` instead of `colors_equal()`. Example (line 95):
  ```python
  assert list(child_label.color) == new_color_list
  ```
  Violates [Helper Functions](#helper-functions).

- **Line 213 (`test_line_height_change_updates_descendant_labels`)**: `child_label.line_height == new_line_height` without tolerance, should use `floats_equal()`. Violates [Helper Functions](#helper-functions).

## test_rebuild_semantics.py

- **Lines 51-78 (`TestWidgetIdentityHelpers` class)**: Validates `test_utils.py` helper `collect_widget_ids()` but missing `@pytest.mark.test_tests`. Example: `class TestWidgetIdentityHelpers:\n    """Tests for the collect_widget_ids helper function."""\n    def test_collect_widget_ids_includes_root(self):`. Violates [Test Types and Markers](#test-types-and-markers) > #### Meta-Test Marking (lines 178-190): Tests validating test suite must use `@pytest.mark.test_tests`.

- **Lines 414-419 (`TestStylePropertyPropagationPBT` docstring)**: Malformed: `"""Property-based tests for style property propagation to descendants.\n\n    to Descendants**"""`. Violates [Test File Structure](#test-file-structure) > Standard Test File Template requiring proper docstrings.

- **Lines 646-651 (`TestStructurePropertyRebuildPBT` docstring)**: Malformed: `"""Property-based tests for structure property rebuild behavior.\n\n    Rebuild Widget Tree**"""`. Same violation as above.

- **Incorrect Hypothesis `@settings` comments (multiple)**:
  - Line 257: `# Complex combination strategy: 50 examples (120 finite combinations with 5 complex strategies)` — "Complex combination" invalid term; incorrect rationale format.
  - Line 429: Similar invalid "Complex combination".
  - Line 656: `# Mixed finite/complex strategy: 50 examples (complex samples)` — Both strategies complex (`simple_markdown_document()`), should be "Complex strategy: 50 examples (adequate coverage)".
  - Line 699: `# Mixed finite/complex strategy: 15 examples (3 finite × 5 complex samples)` — No clear 3 finite strategies.
  - Line 795: Invalid "Complex combination".
  - Line 837: `# Mixed finite/complex strategy: 48 examples (24 finite combinations × 2 complex samples)` — Finite product miscounted (~8: 2×2×2).
  Example code (line 257): `@given(...)\n# Complex combination strategy...\n@settings(max_examples=50, deadline=None)`.
  Violates [Property-Based Testing Optimization](#property-based-testing-optimization) > Comment Format Requirements / Strategy Classifications (lines 563-692).

- **Lines 43, 527-547 (`test_font_name_change_triggers_rebuild`), 701-736 (`test_font_name_change_triggers_rebuild_pbt`)**: `font_name` wrongly in `STRUCTURE_PROPERTIES` and tested as triggering rebuild (`label.font_name = ...; label.force_rebuild(); assert children_ids_before != children_ids_after`). But style-only: "`font_name` - Updates Label.font_name on existing Labels" ([Rebuild Contract Testing](#rebuild-contract-testing) lines 226-232). Should preserve tree, no `force_rebuild()`. Naming `test_*_change_triggers_rebuild` violates contract. Also [Test Naming Conventions](#test-naming-conventions) > Rebuild Testing Names (lines 115-120).

- **Lines 44, 550-571 (`test_text_size_change_triggers_rebuild`)**: `text_size` wrongly in `STRUCTURE_PROPERTIES`, test asserts rebuild. But style-only: "`text_size` - Updates Label.text_size on existing Labels" (line 231). Same violations as `font_name`.

## test_texture_render_mode.py

- **Lines 113-129 (`test_aggregated_refs_populated_in_texture_mode`)**: Test name and docstring imply `_aggregated_refs` is populated (non-empty with link zones), but assertion only `assert hasattr(label, '_aggregated_refs')` (trivial check, attribute likely always exists even if empty dict). Comment notes "`refs may be empty if texture rendering failed`". Relevant code:
  ```python
  # Check that aggregated refs were collected
  # Note: The refs may be empty if texture rendering failed or
  # if the link zones couldn't be calculated
  assert hasattr(label, '_aggregated_refs'), \
      "Expected _aggregated_refs attribute"
  ```
  Violates [Test Naming Conventions](#test-naming-conventions): "Test method names should **accurately reflect what they assert**" (cf. BAD example lines 146-151 claiming rebuild but testing value only).

- **Lines 182-476 (`TestDeterministicTextureHitTesting` class methods)**: Exact duplication of `dispatched_refs = []` initialization and inline `def capture_ref(instance, ref): dispatched_refs.append(ref)` helper function across **six** test methods:
  - Lines 200-204 (`test_inside_zone_dispatch`)
  - Lines 270-273 (`test_property_inside_zone_dispatch`)
  - Lines 309-313 (`test_outside_zone_no_dispatch`)
  - Lines 371-375 (`test_property_outside_zone_no_dispatch`)
  - Lines 416-418 (`test_multiple_zones_first_match`)
  - Lines 459-462 (`test_multiple_zones_non_overlapping`)
  
  Relevant duplicated code:
  ```python
  dispatched_refs = []
  def capture_ref(instance, ref):
      dispatched_refs.append(ref)
  label.bind(on_ref_press=capture_ref)
  ```
  Violates [Helper Functions](#helper-functions): "Always use helper functions from `test_utils.py` instead of duplicating code" and general best practices against code duplication.

## test_texture_sizing.py

- **Lines 73-88 (`test_heading_creates_label_widget`)**: Test name and docstring `"Heading content creates a Label widget that is included in texture_size calculation."` claim creation of Label widget, but assertion only `assert len(label.children) >= 1`; no verification that child is Label (e.g., `len(find_labels_recursive(label)) >= 1` or `isinstance(next(iter(label.children)), Label)`). Relevant code:
  ```python
  assert len(label.children) >= 1, \
      f"Expected at least 1 child for heading, got {len(label.children)}"
  ```
  Violates [Test Naming Conventions](#test-naming-conventions): "Test method names should **accurately reflect what they assert**".

- **Lines 90-107 (`test_paragraph_creates_label_widget`)**: Same violation as above for paragraph test. Docstring claims "Paragraph content creates a Label widget...", but only asserts `len(label.children) >= 1`.

- **Lines 335-351 (`test_all_heading_levels_create_label_widgets`)**: Same violation as above. Claims "All heading levels create Label widgets...", asserts only `len(label.children) >= 1`.

- **Lines 286-289 (`test_texture_size_updates_on_text_change`)**: Non-standard Hypothesis comment `# Complex strategy: 50 examples (two complex strategies combined)`. For two `simple_markdown_document()` (both Complex/Infinite strategies), rationale should be `(adequate coverage)` per standardized format. Relevant code:
  ```python
  @given(simple_markdown_document(), simple_markdown_document())
  # Complex strategy: 50 examples (two complex strategies combined)
  @settings(max_examples=50, deadline=None)
  ```
  Violates [Property-Based Testing Optimization](#property-based-testing-optimization) > Comment Format Requirements: "MUST include a standardized comment" with "exact rationale format".
  