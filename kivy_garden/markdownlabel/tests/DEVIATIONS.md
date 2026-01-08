# Deviations

## test_inline_renderer.py

No deviations found in test_inline_renderer.py

## test_kivy_renderer.py

No deviations found in test_kivy_renderer.py

## test_core_functionality.py

- **Lines 237, 258, 287, 307, 325**: Missing `@pytest.mark.property` on Hypothesis-based property tests (`test_link_url_in_ref_tag`, `test_various_urls_in_links`, `test_nested_lists_render_without_exception`, `test_nested_quotes_render_without_exception`, `test_mixed_nesting_renders_without_exception`). Only `@pytest.mark.needs_window` present. Relevant code: `@pytest.mark.needs_window\n@given(...)`. Violates [Test Types and Markers](#test-types-and-markers) section: Property-based tests using Hypothesis must be marked `@pytest.mark.property`.

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

- **All Hypothesis-based test methods (e.g., lines 25, 36, 46, 58, 70, 94, 103, 111, 119, 127, 135, 155, 182, 191, 200, 209, 218, 237, 245, 253, 262, 281, 315, 324, 333, 342, 362, 375)**: Missing `@pytest.mark.property` marker on property-based tests using Hypothesis. Relevant code example (line 25):
```python
@given(st.floats(min_value=1, max_value=200, allow_nan=False, allow_infinity=False))
# Complex strategy: 50 examples (adequate coverage)
@settings(max_examples=50, deadline=None)
```
Violates [Test Types and Markers](#test-types-and-markers): Property-based tests using Hypothesis must be marked `@pytest.mark.property`.

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
  ```
  label.text_size = [None, height2]
  label.force_rebuild()  # Unnecessary for style-only property
  ```

  These tests should instead verify no rebuild occurs using `ids_before = collect_widget_ids(label)` before change, `assert_no_rebuild(label, ids_before)` after change (no `force_rebuild()`), and confirm child label values updated.

- **Lines 84-96 (`test_text_size_with_width_passed_to_renderer`)**: Method docstring claims "`text_size` with width is passed to renderer and affects internal Labels", but assertions only verify `label.text_size[0] == width` and `len(labels) >= 1`; does **not** assert child Labels have `text_size[0] == width`. Violates "`Test method names should **accurately reflect what they assert`**" ([`TESTING.md #Test Naming Conventions`](kivy_garden/markdownlabel/tests/TESTING.md:111-152)). Relevant code:
  ```
  labels = find_labels_recursive(label)
  assert len(labels) >= 1, "Expected at least one Label"
  # Missing: assert lbl.text_size[0] == width for lbl in labels
  ```

- **Lines 229-231, 242-244, 299-301**: Unnecessary defensive checks `if hasattr(lbl, 'text_size') and lbl.text_size:` before `assert lbl.text_size[1] is None`. All child widgets are `Label` instances with `text_size` ListProperty([None, None]), always present. Violates [Best Practices #Proper assertions, etc.](kivy_garden/markdownlabel/tests/TESTING.md:1022+) for clean, direct assertions. Example (line 229):
  ```
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

