# Deviations

## test_font_properties.py

### Line 420-436: Inconsistent use of @pytest.mark.property in TestAdvancedFontPropertyForwarding class
**Issue:** Test `test_font_hinting_forwarded_to_all_labels_including_code` uses `@pytest.mark.parametrize` while all other tests in the same class use `@pytest.mark.property` with Hypothesis. This creates inconsistency in testing approach within the same test class.

**Guideline:** Section "Property-Based Testing" and "When to Use Hypothesis vs. @pytest.mark.parametrize" provide guidance on choosing between these approaches. While `@pytest.mark.parametrize` is acceptable for small finite enumerations (4 values in this case), mixing approaches within the same class reduces consistency and maintainability.

**Current code:**
```python
@pytest.mark.parametrize('font_hinting_value', [None, 'normal', 'light', 'mono'])
def test_font_hinting_forwarded_to_all_labels_including_code(self, font_hinting_value):
    """font_hinting IS forwarded to ALL Labels including code blocks."""
    # Create markdown with both regular text and code block
    markdown = 'Regular paragraph\n\n```python\ncode here\n```'
    label = MarkdownLabel(text=markdown, font_hinting=font_hinting_value)

    # Find all labels
    all_labels = find_labels_recursive(label)
    assert len(all_labels) >= 2, "Expected at least 2 Labels (paragraph + code)"

    # All labels should have font_hinting set (when not None)
    for lbl in all_labels:
        if font_hinting_value is not None:
            assert lbl.font_hinting == font_hinting_value, \
                f"Expected font_hinting={font_hinting_value!r}, got {lbl.font_hinting!r}"
```

**Expected code (for consistency with class):**
```python
@pytest.mark.property
@given(st.sampled_from([None, 'normal', 'light', 'mono']))
# Small finite strategy: 4 examples (input space size: 4)
@settings(max_examples=4, deadline=None)
def test_font_hinting_forwarded_to_all_labels_including_code(self, font_hinting_value):
    """font_hinting IS forwarded to ALL Labels including code blocks."""
    # Create markdown with both regular text and code block
    markdown = 'Regular paragraph\n\n```python\ncode here\n```'
    label = MarkdownLabel(text=markdown, font_hinting=font_hinting_value)

    # Find all labels
    all_labels = find_labels_recursive(label)
    assert len(all_labels) >= 2, "Expected at least 2 Labels (paragraph + code)"

    # All labels should have font_hinting set (when not None)
    for lbl in all_labels:
        if font_hinting_value is not None:
            assert lbl.font_hinting == font_hinting_value, \
                f"Expected font_hinting={font_hinting_value!r}, got {lbl.font_hinting!r}"
```

**Note:** While the current implementation using `@pytest.mark.parametrize` is technically acceptable for a 4-value enumeration (the guidelines state "Single enum, ≤10 values: @pytest.mark.parametrize"), inconsistency within the class is the issue. The class `TestAdvancedFontPropertyForwarding` uses property-based testing for all other similar tests (`test_font_family_excluded_from_code_blocks`, `test_font_family_forwarded_to_non_code_labels`, `test_font_context_forwarded_to_all_labels_including_code`, `test_font_features_forwarded_to_all_labels_including_code`, `test_font_kerning_forwarded_to_all_labels_including_code`), so this one test should follow the same pattern for consistency.

---

## test_sizing_behavior.py

### Line 556-586: Missing pytest marker for meta-test
**Issue:** Test `test_all_classes_test_related_functionality` is a meta-test (validates) test suite structure itself) but is missing `@pytest.mark.test_tests` marker.

**Guideline:** Section "Test Types and Markers" - "Meta-Test Marking" states: "Tests that validate the test suite itself must be marked with `@pytest.mark.test_tests`."

**Current code:**
```python
def test_all_classes_test_related_functionality(self):
    """All test classes in this module test related sizing functionality."""
    import inspect
    import kivy_garden.markdownlabel.tests.test_sizing_behavior as sizing_module

    # Get all test classes and their methods
    for name, obj in inspect.getmembers(sizing_module):
        if (inspect.isclass(obj) and
            name.startswith('Test') and
                obj.__module__ == sizing_module.__name__):

            # Get test methods
            test_methods = [method_name for method_name, method in inspect.getmembers(obj)
                          if method_name.startswith('test_')]

            if test_methods:  # Only check classes with test methods
                # Check that class docstring or name indicates sizing focus
                class_doc = obj.__doc__ or ""
                class_name_lower = name.lower()

                sizing_indicators = [
                    'sizing', 'size', 'auto', 'height', 'strict', 'grouping'
                ]

                has_sizing_indicator = (
                    any(indicator in class_name_lower for indicator in sizing_indicators) or
                    any(indicator in class_doc.lower() for indicator in sizing_indicators)
                )

                assert has_sizing_indicator, \
                    f"Test class {name} should focus on sizing behavior"
```

**Expected code:**
```python
@pytest.mark.test_tests
def test_all_classes_test_related_functionality(self):
    """All test classes in this module test related sizing functionality."""
    import inspect
    import kivy_garden.markdownlabel.tests.test_sizing_behavior as sizing_module

    # Get all test classes and their methods
    for name, obj in inspect.getmembers(sizing_module):
        if (inspect.isclass(obj) and
            name.startswith('Test') and
                obj.__module__ == sizing_module.__name__):

            # Get test methods
            test_methods = [method_name for method_name, method in inspect.getmembers(obj)
                          if method_name.startswith('test_')]

            if test_methods:  # Only check classes with test methods
                # Check that class docstring or name indicates sizing focus
                class_doc = obj.__doc__ or ""
                class_name_lower = name.lower()

                sizing_indicators = [
                    'sizing', 'size', 'auto', 'height', 'strict', 'grouping'
                ]

                has_sizing_indicator = (
                    any(indicator in class_name_lower for indicator in sizing_indicators) or
                    any(indicator in class_doc.lower() for indicator in sizing_indicators)
                )

                assert has_sizing_indicator, \
                    f"Test class {name} should focus on sizing behavior"
```

---

## test_clipping_behavior.py

### Line 121-138: Duplicated helper function logic
**Issue:** Test `test_clipping_uses_stencil_view` manually searches for StencilView instead of using the available helper function `has_clipping_container()` from test_utils.py.

**Guideline:** Section "Helper Functions" states: "Always use helper functions from `test_utils.py` instead of duplicating code."

**Current code:**
```python
def test_clipping_uses_stencil_view(self):
    """Clipping mechanism uses StencilView."""
    from kivy.uix.stencilview import StencilView

    label = MarkdownLabel(
        text="Test content",
        text_size=[None, 50],
    )
    label.force_rebuild()

    # Verify clipping container is a StencilView
    found_stencil = False
    for child in label.children:
        if isinstance(child, StencilView):
            found_stencil = True
            break

    assert found_stencil, "Expected StencilView for clipping"
```

**Expected code:**
```python
@pytest.mark.unit
def test_clipping_uses_stencil_view(self):
    """Clipping mechanism uses StencilView."""
    label = MarkdownLabel(
        text="Test content",
        text_size=[None, 50],
    )
    label.force_rebuild()

    # Verify clipping container is a StencilView using helper
    assert has_clipping_container(label), "Expected StencilView for clipping"
```

**Note:** The current implementation manually searches for StencilView (lines 132-136), which duplicates the logic in `has_clipping_container()` from test_utils.py (lines 638-641). Since the test only needs to verify that a StencilView exists (not access its properties), it should use the shared helper function.

---

## test_rtl_alignment.py

### Line 280-300: Missing rebuild contract testing helper usage
**Issue:** Test `test_direction_change_preserves_widget_identities` manually compares widget IDs instead of using the helper function `assert_no_rebuild()` from test_utils.py.

**Guideline:** Section "Rebuild Testing Helpers" states: "Use these helper functions from `test_utils.py`" and provides examples of using `assert_no_rebuild()` for verifying no rebuild occurred.

**Current code:**
```python
@pytest.mark.property
@pytest.mark.needs_window
@given(
    st.sampled_from(['ltr', 'weak_ltr', None]),
    st.sampled_from(['rtl', 'weak_rtl'])
)
# Combination strategy: 6 examples (combination coverage)
@settings(max_examples=6, deadline=None)
def test_direction_change_preserves_widget_identities(self, initial_direction, new_direction):
    """Direction change preserves widget identities (no rebuild)."""
    label = MarkdownLabel(
        text='Hello World',
        halign='auto',
        base_direction=initial_direction
    )

    # Collect widget IDs before change
    ids_before = collect_widget_ids(label)

    # Change base_direction
    label.base_direction = new_direction

    # Collect widget IDs after change
    ids_after = collect_widget_ids(label)

    # Widget identities should be preserved (in-place update, not rebuild)
    assert ids_before == ids_after, \
        f"Widget identities changed during direction change: " \
        f"{len(ids_before)} before, {len(ids_after)} after"
```

**Expected code:**
```python
@pytest.mark.property
@pytest.mark.needs_window
@given(
    st.sampled_from(['ltr', 'weak_ltr', None]),
    st.sampled_from(['rtl', 'weak_rtl'])
)
# Combination strategy: 6 examples (combination coverage)
@settings(max_examples=6, deadline=None)
def test_direction_change_preserves_widget_identities(self, initial_direction, new_direction):
    """Direction change preserves widget identities (no rebuild)."""
    label = MarkdownLabel(
        text='Hello World',
        halign='auto',
        base_direction=initial_direction
    )

    # Collect widget IDs before change
    ids_before = collect_widget_ids(label)

    # Change base_direction
    label.base_direction = new_direction

    # Widget identities should be preserved (in-place update, not rebuild)
    assert_no_rebuild(label, ids_before)
```

**Note:** The current implementation manually collects and compares widget IDs (lines 289-300), which duplicates the logic in `assert_no_rebuild()` helper from test_utils.py. Using the helper function provides better consistency with other rebuild contract tests and clearer intent.

---

## test_texture_render_mode.py

### Line 43-55: Missing rebuild contract testing for render_mode change
**Issue:** Test `test_texture_mode_creates_image_widget` changes `render_mode` property but doesn't verify rebuild occurred using rebuild contract testing helpers.

**Guideline:** Section "Rebuild Contract Testing" states that structure properties like `render_mode` trigger a complete widget tree rebuild and should be tested using `collect_widget_ids()` and `assert_rebuild_occurred()` or `assert_no_rebuild()` helpers.

**Current code:**
```python
    @pytest.mark.parametrize('text', [
        'Hello World',
        '# Heading',
        '**Bold** and *italic*',
        '- List item 1\n- List item 2',
        '[Link](http://example.com)',
    ])
    def test_texture_mode_creates_image_widget(self, text):
        """When render_mode='texture', widget tree contains an Image widget."""
        label = MarkdownLabel(
            text=text,
            render_mode='texture',
            size=(400, 300),
            size_hint=(None, None)
        )
        label.force_rebuild()

        images = find_images(label)
        assert len(images) >= 1, \
            f"Expected at least 1 Image widget in texture mode, found {len(images)}"
```

**Note:** This test creates a label with `render_mode='texture'` and calls `force_rebuild()`, but doesn't verify that a rebuild actually occurred. According to guidelines, structure properties like `render_mode` should trigger rebuilds, and this should be verified.

**Expected code:**
```python
    @pytest.mark.parametrize('text', [
        'Hello World',
        '# Heading',
        '**Bold** and *italic*',
        '- List item 1\n- List item 2',
        '[Link](http://example.com)',
    ])
    def test_texture_mode_creates_image_widget(self, text):
        """When render_mode='texture', widget tree contains an Image widget."""
        label = MarkdownLabel(
            text=text,
            render_mode='widgets',  # Start with widgets mode
            size=(400, 300),
            size_hint=(None, None)
        )
        label.force_rebuild()
        
        # Collect widget IDs before changing render_mode
        ids_before = collect_widget_ids(label)
        
        # Change to texture mode (should trigger rebuild)
        label.render_mode = 'texture'
        label.force_rebuild()

        # Verify rebuild occurred
        assert_rebuild_occurred(label, ids_before)

        # Verify Image widget exists
        images = find_images(label)
        assert len(images) >= 1, \
            f"Expected at least 1 Image widget in texture mode, found {len(images)}"
```

**Note:** Similar rebuild contract testing should be applied to other tests that change structure properties (e.g., `test_widgets_mode_no_image_widget` when changing between modes).

---

### Line 71-83: Missing rebuild contract testing for render_mode change
**Issue:** Test `test_widgets_mode_no_image_widget` changes `render_mode` property but doesn't verify rebuild occurred using rebuild contract testing helpers.

**Guideline:** Section "Rebuild Contract Testing" states that structure properties like `render_mode` trigger a complete widget tree rebuild and should be tested using `collect_widget_ids()` and `assert_rebuild_occurred()` or `assert_no_rebuild()` helpers.

**Current code:**
```python
    def test_widgets_mode_no_image_widget(self):
        """When render_mode='widgets', no Image widget is created."""
        label = MarkdownLabel(
            text='Hello World',
            render_mode='widgets',
            size=(400, 300),
            size_hint=(None, None)
        )
        label.force_rebuild()

        images = find_images(label)
        assert len(images) == 0, \
            f"Expected no Image widgets in widgets mode, found {len(images)}"
```

**Note:** This test creates a label with `render_mode='widgets'` and calls `force_rebuild()`, but doesn't verify that a rebuild occurred. According to guidelines, structure properties like `render_mode` should trigger rebuilds, and this should be verified.

**Expected code:**
```python
    def test_widgets_mode_no_image_widget(self):
        """When render_mode='widgets', no Image widget is created."""
        label = MarkdownLabel(
            text='Hello World',
            render_mode='texture',  # Start with texture mode
            size=(400, 300),
            size_hint=(None, None)
        )
        label.force_rebuild()
        
        # Collect widget IDs before changing render_mode
        ids_before = collect_widget_ids(label)
        
        # Change to widgets mode (should trigger rebuild)
        label.render_mode = 'widgets'
        label.force_rebuild()

        # Verify rebuild occurred
        assert_rebuild_occurred(label, ids_before)

        # Verify no Image widget exists
        images = find_images(label)
        assert len(images) == 0, \
            f"Expected no Image widgets in widgets mode, found {len(images)}"
```

**Note:** Similar rebuild contract testing should be applied to other tests that change structure properties (e.g., `test_texture_mode_creates_image_widget` when changing between modes).

---

### Line 475-509: Missing rebuild contract testing for texture fallback
**Issue:** Test `test_texture_fallback_to_widgets_mode` simulates a texture rendering failure that should trigger a rebuild to widgets mode, but doesn't verify rebuild occurred using rebuild contract testing helpers.

**Guideline:** Section "Rebuild Contract Testing" states that structure changes should trigger rebuilds and should be tested using `collect_widget_ids()` and `assert_rebuild_occurred()` helpers.

**Current code:**
```python
    def test_texture_fallback_to_widgets_mode(self, monkeypatch):
        """When _render_as_texture returns None, fallback to widgets mode.

        This test verifies that when texture rendering fails (returns None),
        MarkdownLabel falls back to widgets-mode rendering, ensuring
        content is always displayed.
        """
        # Monkeypatch _render_as_texture to return None (simulate failure)
        monkeypatch.setattr(
            MarkdownLabel,
            '_render_as_texture',
            lambda self, content: None
        )

        # Create MarkdownLabel with render_mode='texture' and non-empty text
        label = MarkdownLabel(
            text='# Hello World\n\nThis is **bold** text.',
            render_mode='texture',
            size=(400, 300),
            size_hint=(None, None)
        )

        # Call force_rebuild() to trigger rendering
        label.force_rebuild()

        # Assert no Image widget in tree (texture mode failed)
        images = find_images(label)
        assert len(images) == 0, \
            f"Expected no Image widgets after texture fallback, found {len(images)}"

        # Assert at least one Label widget exists (widgets-mode fallback)
        labels = find_labels_recursive(label)
        assert len(labels) >= 1, \
            f"Expected at least 1 Label widget in fallback mode, found {len(labels)}"
```

**Note:** This test simulates a texture rendering failure that should trigger a fallback rebuild to widgets mode, but doesn't verify that a rebuild occurred. The test should verify that the widget tree was rebuilt when the fallback occurred.

**Expected code:**
```python
    def test_texture_fallback_to_widgets_mode(self, monkeypatch):
        """When _render_as_texture returns None, fallback to widgets mode.

        This test verifies that when texture rendering fails (returns None),
        MarkdownLabel falls back to widgets-mode rendering, ensuring
        content is always displayed.
        """
        # Monkeypatch _render_as_texture to return None (simulate failure)
        monkeypatch.setattr(
            MarkdownLabel,
            '_render_as_texture',
            lambda self, content: None
        )

        # Create MarkdownLabel with render_mode='texture' and non-empty text
        label = MarkdownLabel(
            text='# Hello World\n\nThis is **bold** text.',
            render_mode='texture',
            size=(400, 300),
            size_hint=(None, None)
        )
        
        # Collect widget IDs before rebuild
        ids_before = collect_widget_ids(label)

        # Call force_rebuild() to trigger rendering
        label.force_rebuild()
        
        # Verify rebuild occurred (texture fallback should trigger rebuild)
        assert_rebuild_occurred(label, ids_before)

        # Assert no Image widget in tree (texture mode failed)
        images = find_images(label)
        assert len(images) == 0, \
            f"Expected no Image widgets after texture fallback, found {len(images)}"

        # Assert at least one Label widget exists (widgets-mode fallback)
        labels = find_labels_recursive(label)
        assert len(labels) >= 1, \
            f"Expected at least 1 Label widget in fallback mode, found {len(labels)}"
```

---

## test_texture_sizing.py

### Lines 269-293: Missing pytest marker for property-based test and incorrect comment
**Issue:** Property-based test `test_texture_size_updates_on_text_change` is missing `@pytest.mark.property` marker, and the comment incorrectly describes the strategy as having "100 finite combinations × 0.5 complex samples" when it actually uses two complex strategies (`simple_markdown_document()` twice).

**Guideline:** Section "Test Types and Markers" states: "Property-based tests using Hypothesis" should be marked with `@pytest.mark.property`. Section "Property-Based Testing Optimization" requires accurate strategy type classifications in comments.

**Current code:**
```python
@given(simple_markdown_document(), simple_markdown_document())
# Mixed finite/complex strategy: 50 examples (100 finite combinations × 0.5 complex samples)
@settings(max_examples=50, deadline=None)
def test_texture_size_updates_on_text_change(self, text1, text2):
    """texture_size updates when text property changes."""
```

**Expected code:**
```python
@pytest.mark.property
@given(simple_markdown_document(), simple_markdown_document())
# Complex strategy: 50 examples (two complex strategies combined)
@settings(max_examples=50, deadline=None)
def test_texture_size_updates_on_text_change(self, text1, text2):
    """texture_size updates when text property changes."""
```

---
