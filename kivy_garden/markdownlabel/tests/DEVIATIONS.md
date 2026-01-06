# Deviations

## test_import.py

### Line 12-16: Missing pytest marker
**Issue:** Test `test_markdownlabel_import` is missing `@pytest.mark.unit` marker.

**Guideline:** Section "Test Types and Markers" recommends using `@pytest.mark.unit` for unit tests.

**Current code:**
```python
def test_markdownlabel_import(self):
    """Test that MarkdownLabel can be imported."""
    from kivy_garden.markdownlabel import MarkdownLabel
    label = MarkdownLabel()
    assert hasattr(label, 'text')
```

**Expected code:**
```python
@pytest.mark.unit
def test_markdownlabel_import(self):
    """Test that MarkdownLabel can be imported."""
    from kivy_garden.markdownlabel import MarkdownLabel
    label = MarkdownLabel()
    assert hasattr(label, 'text')
```

---

### Line 18-22: Missing pytest marker
**Issue:** Test `test_markdownlabel_text_property` is missing `@pytest.mark.unit` marker.

**Guideline:** Section "Test Types and Markers" recommends using `@pytest.mark.unit` for unit tests.

**Current code:**
```python
def test_markdownlabel_text_property(self):
    """Test that MarkdownLabel has a text property."""
    from kivy_garden.markdownlabel import MarkdownLabel
    label = MarkdownLabel(text='# Hello')
    assert label.text == '# Hello'
```

---

## test_core_functionality.py

### Line 333-340: Missing pytest marker
**Issue:** Test `test_exactly_10_levels_renders_fully` is missing `@pytest.mark.needs_window` marker.

**Guideline:** Tests that create MarkdownLabel instances should use `@pytest.mark.needs_window` marker (as evidenced by other tests in same file that create MarkdownLabel instances, such as lines 32, 46, 64, 108, 156, 175, 205, 228, 249, 279, 298, 316).

**Current code:**
```python
def test_exactly_10_levels_renders_fully(self):
    """Exactly 10 levels of nesting renders without truncation warning."""
    markdown = self._generate_nested_list(10)
    label = MarkdownLabel(text=markdown)

    # Should render without exception
    assert isinstance(label, BoxLayout)
    assert len(label.children) >= 1
```

**Expected code:**
```python
@pytest.mark.needs_window
def test_exactly_10_levels_renders_fully(self):
    """Exactly 10 levels of nesting renders without truncation warning."""
    markdown = self._generate_nested_list(10)
    label = MarkdownLabel(text=markdown)

    # Should render without exception
    assert isinstance(label, BoxLayout)
    assert len(label.children) >= 1
```

---

### Line 342-350: Missing pytest marker
**Issue:** Test `test_beyond_10_levels_still_renders` is missing `@pytest.mark.needs_window` marker.

**Guideline:** Tests that create MarkdownLabel instances should use `@pytest.mark.needs_window` marker (as evidenced by other tests in same file that create MarkdownLabel instances, such as lines 32, 46, 64, 108, 156, 175, 205, 228, 249, 279, 298, 316).

**Current code:**
```python
def test_beyond_10_levels_still_renders(self):
    """Beyond 10 levels still renders (with truncation) without crashing."""
    markdown = self._generate_nested_list(15)
    label = MarkdownLabel(text=markdown)

    # Should render without exception
    assert isinstance(label, BoxLayout)
    # Should have at least some content
    assert len(label.children) >= 1
```

**Expected code:**
```python
@pytest.mark.needs_window
def test_beyond_10_levels_still_renders(self):
    """Beyond 10 levels still renders (with truncation) without crashing."""
    markdown = self._generate_nested_list(15)
    label = MarkdownLabel(text=markdown)

    # Should render without exception
    assert isinstance(label, BoxLayout)
    # Should have at least some content
    assert len(label.children) >= 1
```

**Expected code:**
```python
@pytest.mark.unit
def test_markdownlabel_text_property(self):
    """Test that MarkdownLabel has a text property."""
    from kivy_garden.markdownlabel import MarkdownLabel
    label = MarkdownLabel(text='# Hello')
    assert label.text == '# Hello'
```

---

## test_label_compatibility.py

### Line 410-433: Missing pytest marker for meta-test
**Issue:** Test `test_label_compatibility_imports_resolve` is a meta-test (tests about test suite itself) but is missing `@pytest.mark.test_tests` marker.

**Guideline:** Section "Test Types and Markers" - "Meta-Test Marking" states: "Tests that validate the test suite itself must be marked with `@pytest.mark.test_tests`."

**Current code:**
```python
def test_label_compatibility_imports_resolve(self):
    """Label compatibility module imports resolve successfully."""
    try:
        # Test that key classes are accessible
        from kivy_garden.markdownlabel.tests.test_label_compatibility import (
            TestFontSizeAliasBidirectionality,
            TestNoOpPropertiesAcceptance,
            TestNoOpPropertyAcceptanceAndStorage
        )

        # Verify classes exist and are classes
        assert TestFontSizeAliasBidirectionality is not None
        assert TestNoOpPropertiesAcceptance is not None
        assert TestNoOpPropertyAcceptanceAndStorage is not None

        # Verify they are actually classes
        assert isinstance(TestFontSizeAliasBidirectionality, type)
        assert isinstance(TestNoOpPropertiesAcceptance, type)
        assert isinstance(TestNoOpPropertyAcceptanceAndStorage, type)

    except ImportError as e:
        pytest.fail(f"Import failed for test_label_compatibility: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error importing test_label_compatibility: {e}")
```

**Expected code:**
```python
@pytest.mark.test_tests
def test_label_compatibility_imports_resolve(self):
    """Label compatibility module imports resolve successfully."""
    try:
        # Test that key classes are accessible
        from kivy_garden.markdownlabel.tests.test_label_compatibility import (
            TestFontSizeAliasBidirectionality,
            TestNoOpPropertiesAcceptance,
            TestNoOpPropertyAcceptanceAndStorage
        )

        # Verify classes exist and are classes
        assert TestFontSizeAliasBidirectionality is not None
        assert TestNoOpPropertiesAcceptance is not None
        assert TestNoOpPropertyAcceptanceAndStorage is not None

        # Verify they are actually classes
        assert isinstance(TestFontSizeAliasBidirectionality, type)
        assert isinstance(TestNoOpPropertiesAcceptance, type)
        assert isinstance(TestNoOpPropertyAcceptanceAndStorage, type)

    except ImportError as e:
        pytest.fail(f"Import failed for test_label_compatibility: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error importing test_label_compatibility: {e}")
```

---

### Line 435-462: Missing pytest marker for meta-test
**Issue:** Test `test_shared_utilities_imports_resolve` is a meta-test (tests about test suite itself) but is missing `@pytest.mark.test_tests` marker.

**Guideline:** Section "Test Types and Markers" - "Meta-Test Marking" states: "Tests that validate the test suite itself must be marked with `@pytest.mark.test_tests`."

**Current code:**
```python
def test_shared_utilities_imports_resolve(self):
    """Shared test utilities imports resolve successfully."""
    try:
        # Test importing utilities module
        from kivy_garden.markdownlabel.tests.test_utils import (
            markdown_heading,
            markdown_paragraph,
            simple_markdown_document,
            find_labels_recursive,
            colors_equal,
            KIVY_FONTS,
        )

        # Verify key functions exist
        assert callable(markdown_heading)
        assert callable(markdown_paragraph)
        assert callable(simple_markdown_document)
        assert callable(find_labels_recursive)
        assert callable(colors_equal)

        # Verify constants exist
        assert KIVY_FONTS is not None
        assert isinstance(KIVY_FONTS, list)

    except ImportError as e:
        pytest.fail(f"Import failed for test_utils: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error importing test_utils: {e}")
```

**Expected code:**
```python
@pytest.mark.test_tests
def test_shared_utilities_imports_resolve(self):
    """Shared test utilities imports resolve successfully."""
    try:
        # Test importing utilities module
        from kivy_garden.markdownlabel.tests.test_utils import (
            markdown_heading,
            markdown_paragraph,
            simple_markdown_document,
            find_labels_recursive,
            colors_equal,
            KIVY_FONTS,
        )

        # Verify key functions exist
        assert callable(markdown_heading)
        assert callable(markdown_paragraph)
        assert callable(simple_markdown_document)
        assert callable(find_labels_recursive)
        assert callable(colors_equal)

        # Verify constants exist
        assert KIVY_FONTS is not None
        assert isinstance(KIVY_FONTS, list)

    except ImportError as e:
        pytest.fail(f"Import failed for test_utils: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error importing test_utils: {e}")
```

---

### Line 464-483: Missing pytest marker for meta-test
**Issue:** Test `test_cross_module_imports_work` is a meta-test (tests about test suite itself) but is missing `@pytest.mark.test_tests` marker.

**Guideline:** Section "Test Types and Markers" - "Meta-Test Marking" states: "Tests that validate the test suite itself must be marked with `@pytest.mark.test_tests`."

**Current code:**
```python
def test_cross_module_imports_work(self):
    """Test modules can import from shared utilities."""
    try:
        # Import label compatibility module which uses test_utils
        from kivy_garden.markdownlabel.tests.test_label_compatibility import (
            TestFontSizeAliasBidirectionality,
        )

        # Verify that class can be instantiated (imports worked)
        test_instance = TestFontSizeAliasBidirectionality()
        assert test_instance is not None

        # Verify that test methods exist (they use imported strategies)
        assert hasattr(test_instance, 'test_font_size_sets_base_font_size')
        assert callable(test_instance.test_font_size_sets_base_font_size)

    except ImportError as e:
        pytest.fail(f"Cross-module import failed: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error in cross-module import: {e}")
```

---

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

**Expected code:**
```python
@pytest.mark.test_tests
def test_cross_module_imports_work(self):
    """Test modules can import from shared utilities."""
    try:
        # Import label compatibility module which uses test_utils
        from kivy_garden.markdownlabel.tests.test_label_compatibility import (
            TestFontSizeAliasBidirectionality,
        )

        # Verify that class can be instantiated (imports worked)
        test_instance = TestFontSizeAliasBidirectionality()
        assert test_instance is not None

        # Verify that test methods exist (they use imported strategies)
        assert hasattr(test_instance, 'test_font_size_sets_base_font_size')
        assert callable(test_instance.test_font_size_sets_base_font_size)

    except ImportError as e:
        pytest.fail(f"Cross-module import failed: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error in cross-module import: {e}")
```

---

## test_color_properties.py

### Line 158-169: Missing pytest marker
**Issue:** Test `test_links_unstyled_by_default` is missing `@pytest.mark.unit` marker.

**Guideline:** Section "Test Types and Markers" recommends using `@pytest.mark.unit` for unit tests that test specific examples and edge cases with fast execution and deterministic results.

**Current code:**
```python
def test_links_unstyled_by_default(self):
    """Default links remain unstyled while keeping ref markup."""
    markdown = 'Click [here](https://kivy.org)'
    label = MarkdownLabel(text=markdown)

    labels = find_labels_recursive(label)
    assert len(labels) >= 1, "Expected at least one Label"

    assert any('[ref=' in getattr(lbl, 'text', '') for lbl in labels), \
        "Expected ref markup for link"
    assert not any('[color=' in getattr(lbl, 'text', '') for lbl in labels), \
        "Default links should not inject color markup"
```

**Expected code:**
```python
@pytest.mark.unit
def test_links_unstyled_by_default(self):
    """Default links remain unstyled while keeping ref markup."""
    markdown = 'Click [here](https://kivy.org)'
    label = MarkdownLabel(text=markdown)

    labels = find_labels_recursive(label)
    assert len(labels) >= 1, "Expected at least one Label"

    assert any('[ref=' in getattr(lbl, 'text', '') for lbl in labels), \
        "Expected ref markup for link"
    assert not any('[color=' in getattr(lbl, 'text', '') for lbl in labels), \
        "Default links should not inject color markup"
```

---

### Line 171-180: Missing pytest marker
**Issue:** Test `test_links_styled_when_enabled` is missing `@pytest.mark.unit` marker.

**Guideline:** Section "Test Types and Markers" recommends using `@pytest.mark.unit` for unit tests that test specific examples and edge cases with fast execution and deterministic results.

**Current code:**
```python
def test_links_styled_when_enabled(self):
    """Links gain color markup when link_style='styled'."""
    markdown = 'Click [here](https://kivy.org)'
    label = MarkdownLabel(text=markdown, link_style='styled')

    labels = find_labels_recursive(label)
    assert len(labels) >= 1, "Expected at least one Label"

    assert any('[color=' in getattr(lbl, 'text', '') for lbl in labels), \
        "Expected colored markup when link_style='styled'"
```

---

## test_padding_properties.py

### Line 118-128: Missing pytest marker
**Issue:** Test `test_default_padding_is_zero` is missing `@pytest.mark.unit` marker.

**Guideline:** Section "Test Types and Markers" recommends using `@pytest.mark.unit` for unit tests that test specific examples and edge cases with fast execution and deterministic results.

**Current code:**
```python
def test_default_padding_is_zero(self):
"""Default padding is [0, 0, 0, 0]."""
label = MarkdownLabel(text='Hello World')

expected = [0, 0, 0, 0]
assert len(label.padding) == 4, \
    f"Expected 4-element padding, got {len(label.padding)}"

for i, (actual, exp) in enumerate(zip(label.padding, expected)):
    assert abs(actual - exp) < 0.001, \
        f"Default padding[{i}]: expected {exp}, got {actual}"
```

**Expected code:**
```python
@pytest.mark.unit
def test_default_padding_is_zero(self):
"""Default padding is [0, 0, 0, 0]."""
label = MarkdownLabel(text='Hello World')

expected = [0, 0, 0, 0]
assert len(label.padding) == 4, \
    f"Expected 4-element padding, got {len(label.padding)}"

for i, (actual, exp) in enumerate(zip(label.padding, expected)):
    assert abs(actual - exp) < 0.001, \
        f"Default padding[{i}]: expected {exp}, got {actual}"
```

---

### Line 265-275: Missing pytest marker
**Issue:** Test `test_default_padding_is_zero_for_all_labels` is missing `@pytest.mark.unit` marker.

**Guideline:** Section "Test Types and Markers" recommends using `@pytest.mark.unit` for unit tests that test specific examples and edge cases with fast execution and deterministic results.

**Current code:**
```python
def test_default_padding_is_zero_for_all_labels(self):
"""Default padding is [0, 0, 0, 0] for all labels."""
label = MarkdownLabel(text='Hello World')

labels = find_labels_recursive(label)
assert len(labels) >= 1, "Expected at least one Label"

# All labels should have default padding of [0, 0, 0, 0]
for lbl in labels:
    assert padding_equal(list(lbl.padding), [0, 0, 0, 0]), \
        f"Expected default padding=[0, 0, 0, 0], got {list(lbl.padding)}"
```

**Expected code:**
```python
@pytest.mark.unit
def test_default_padding_is_zero_for_all_labels(self):
"""Default padding is [0, 0, 0, 0] for all labels."""
label = MarkdownLabel(text='Hello World')

labels = find_labels_recursive(label)
assert len(labels) >= 1, "Expected at least one Label"

# All labels should have default padding of [0, 0, 0, 0]
for lbl in labels:
    assert padding_equal(list(lbl.padding), [0, 0, 0, 0]), \
        f"Expected default padding=[0, 0, 0, 0], got {list(lbl.padding)}"
```

---

### Line 765-777: Missing pytest marker
**Issue:** Test `test_default_values_synchronized` is missing `@pytest.mark.unit` marker.

**Guideline:** Section "Test Types and Markers" recommends using `@pytest.mark.unit` for unit tests that test specific examples and edge cases with fast execution and deterministic results.

**Current code:**
```python
def test_default_values_synchronized(self):
"""Default values of label_padding and text_padding are synchronized."""
label = MarkdownLabel(text='Hello World')

# Both should have the same default value
assert padding_equal(list(label.label_padding), list(label.text_padding)), \
    f"Expected label_padding={list(label.text_padding)}, got {list(label.label_padding)}"

# Both should be [0, 0, 0, 0] by default
assert padding_equal(list(label.label_padding), [0, 0, 0, 0]), \
    f"Expected default label_padding=[0, 0, 0, 0], got {list(label.label_padding)}"
assert padding_equal(list(label.text_padding), [0, 0, 0, 0]), \
    f"Expected default text_padding=[0, 0, 0, 0], got {list(label.text_padding)}"
```

**Expected code:**
```python
@pytest.mark.unit
def test_default_values_synchronized(self):
"""Default values of label_padding and text_padding are synchronized."""
label = MarkdownLabel(text='Hello World')

# Both should have the same default value
assert padding_equal(list(label.label_padding), list(label.text_padding)), \
    f"Expected label_padding={list(label.text_padding)}, got {list(label.label_padding)}"

# Both should be [0, 0, 0, 0] by default
assert padding_equal(list(label.label_padding), [0, 0, 0, 0]), \
    f"Expected default label_padding=[0, 0, 0, 0], got {list(label.label_padding)}"
assert padding_equal(list(label.text_padding), [0, 0, 0, 0]), \
    f"Expected default text_padding=[0, 0, 0, 0], got {list(label.text_padding)}"
```

**Expected code:**
```python
@pytest.mark.unit
def test_links_styled_when_enabled(self):
    """Links gain color markup when link_style='styled'."""
    markdown = 'Click [here](https://kivy.org)'
    label = MarkdownLabel(text=markdown, link_style='styled')

    labels = find_labels_recursive(label)
    assert len(labels) >= 1, "Expected at least one Label"

    assert any('[color=' in getattr(lbl, 'text', '') for lbl in labels), \
        "Expected colored markup when link_style='styled'"
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
```

---

## test_serialization.py

### Line 120-137: Missing pytest marker
**Issue:** Property-based test `test_heading_round_trip` is missing `@pytest.mark.property` marker.

**Guideline:** Section "Test Types and Markers" states: "Property-based tests using Hypothesis" should be marked with `@pytest.mark.property`.

**Current code:**
```python
@given(markdown_heading())
# Mixed finite/complex strategy: 20 examples (6 finite × ~3 complex samples)
@settings(max_examples=20, deadline=None)
def test_heading_round_trip(self, heading):
    """Heading round-trips through parse-serialize-parse."""
```

**Expected code:**
```python
@pytest.mark.property
@given(markdown_heading())
# Mixed finite/complex strategy: 20 examples (6 finite × ~3 complex samples)
@settings(max_examples=20, deadline=None)
def test_heading_round_trip(self, heading):
    """Heading round-trips through parse-serialize-parse."""
```

---

### Line 139-160: Missing pytest marker
**Issue:** Property-based test `test_paragraph_round_trip` is missing `@pytest.mark.property` marker.

**Guideline:** Section "Test Types and Markers" states: "Property-based tests using Hypothesis" should be marked with `@pytest.mark.property`.

**Current code:**
```python
@given(markdown_paragraph())
# Complex strategy: 20 examples (adequate coverage)
@settings(max_examples=20, deadline=None)
def test_paragraph_round_trip(self, paragraph):
    """Paragraph round-trips through parse-serialize-parse."""
```

**Expected code:**
```python
@pytest.mark.property
@given(markdown_paragraph())
# Complex strategy: 20 examples (adequate coverage)
@settings(max_examples=20, deadline=None)
def test_paragraph_round_trip(self, paragraph):
    """Paragraph round-trips through parse-serialize-parse."""
```

---

### Line 162-176: Missing pytest marker
**Issue:** Property-based test `test_bold_round_trip` is missing `@pytest.mark.property` marker.

**Guideline:** Section "Test Types and Markers" states: "Property-based tests using Hypothesis" should be marked with `@pytest.mark.property`.

**Current code:**
```python
@given(markdown_bold())
# Complex strategy: 20 examples (adequate coverage)
@settings(max_examples=20, deadline=None)
def test_bold_round_trip(self, bold_text):
    """Bold text round-trips through parse-serialize-parse."""
```

**Expected code:**
```python
@pytest.mark.property
@given(markdown_bold())
# Complex strategy: 20 examples (adequate coverage)
@settings(max_examples=20, deadline=None)
def test_bold_round_trip(self, bold_text):
    """Bold text round-trips through parse-serialize-parse."""
```

---

### Line 178-192: Missing pytest marker
**Issue:** Property-based test `test_italic_round_trip` is missing `@pytest.mark.property` marker.

**Guideline:** Section "Test Types and Markers" states: "Property-based tests using Hypothesis" should be marked with `@pytest.mark.property`.

**Current code:**
```python
@given(markdown_italic())
# Complex strategy: 20 examples (adequate coverage)
@settings(max_examples=20, deadline=None)
def test_italic_round_trip(self, italic_text):
    """Italic text round-trips through parse-serialize-parse."""
```

**Expected code:**
```python
@pytest.mark.property
@given(markdown_italic())
# Complex strategy: 20 examples (adequate coverage)
@settings(max_examples=20, deadline=None)
def test_italic_round_trip(self, italic_text):
    """Italic text round-trips through parse-serialize-parse."""
```

---

### Line 194-208: Missing pytest marker
**Issue:** Property-based test `test_link_round_trip` is missing `@pytest.mark.property` marker.

**Guideline:** Section "Test Types and Markers" states: "Property-based tests using Hypothesis" should be marked with `@pytest.mark.property`.

**Current code:**
```python
@given(markdown_link())
# Complex strategy: 20 examples (adequate coverage)
@settings(max_examples=20, deadline=None)
def test_link_round_trip(self, link_text):
    """Link round-trips through parse-serialize-parse."""
```

**Expected code:**
```python
@pytest.mark.property
@given(markdown_link())
# Complex strategy: 20 examples (adequate coverage)
@settings(max_examples=20, deadline=None)
def test_link_round_trip(self, link_text):
    """Link round-trips through parse-serialize-parse."""
```

---

### Line 210-228: Missing pytest marker
**Issue:** Property-based test `test_document_round_trip` is missing `@pytest.mark.property` marker.

**Guideline:** Section "Test Types and Markers" states: "Property-based tests using Hypothesis" should be marked with `@pytest.mark.property`.

**Current code:**
```python
@given(simple_markdown_document())
# Mixed finite/complex strategy: 20 examples (10 finite × 2 complex samples)
@settings(max_examples=20, deadline=None)
def test_document_round_trip(self, markdown_text):
    """Full document round-trips through parse-serialize-parse."""
```

**Expected code:**
```python
@pytest.mark.property
@given(simple_markdown_document())
# Mixed finite/complex strategy: 20 examples (10 finite × 2 complex samples)
@settings(max_examples=20, deadline=None)
def test_document_round_trip(self, markdown_text):
    """Full document round-trips through parse-serialize-parse."""
```

---

### Line 230-243: Missing pytest marker
**Issue:** Unit test `test_code_block_round_trip` is missing `@pytest.mark.unit` marker.

**Guideline:** Section "Test Types and Markers" recommends using `@pytest.mark.unit` for unit tests that test specific examples and edge cases with fast execution and deterministic results.

**Current code:**
```python
def test_code_block_round_trip(self):
    """Code block round-trips correctly."""
    markdown = '```python\nprint("hello")\n```'
```

**Expected code:**
```python
@pytest.mark.unit
def test_code_block_round_trip(self):
    """Code block round-trips correctly."""
    markdown = '```python\nprint("hello")\n```'
```

---

### Line 245-258: Missing pytest marker
**Issue:** Unit test `test_list_round_trip` is missing `@pytest.mark.unit` marker.

**Guideline:** Section "Test Types and Markers" recommends using `@pytest.mark.unit` for unit tests that test specific examples and edge cases with fast execution and deterministic results.

**Current code:**
```python
def test_list_round_trip(self):
    """List round-trips correctly."""
    markdown = '- Item 1\n- Item 2\n- Item 3'
```

**Expected code:**
```python
@pytest.mark.unit
def test_list_round_trip(self):
    """List round-trips correctly."""
    markdown = '- Item 1\n- Item 2\n- Item 3'
```

---

### Line 260-273: Missing pytest marker
**Issue:** Unit test `test_ordered_list_round_trip` is missing `@pytest.mark.unit` marker.

**Guideline:** Section "Test Types and Markers" recommends using `@pytest.mark.unit` for unit tests that test specific examples and edge cases with fast execution and deterministic results.

**Current code:**
```python
def test_ordered_list_round_trip(self):
    """Ordered list round-trips correctly."""
    markdown = '1. First\n2. Second\n3. Third'
```

**Expected code:**
```python
@pytest.mark.unit
def test_ordered_list_round_trip(self):
    """Ordered list round-trips correctly."""
    markdown = '1. First\n2. Second\n3. Third'
```

---

### Line 275-288: Missing pytest marker
**Issue:** Unit test `test_block_quote_round_trip` is missing `@pytest.mark.unit` marker.

**Guideline:** Section "Test Types and Markers" recommends using `@pytest.mark.unit` for unit tests that test specific examples and edge cases with fast execution and deterministic results.

**Current code:**
```python
def test_block_quote_round_trip(self):
    """Block quote round-trips correctly."""
    markdown = '> This is a quote'
```

**Expected code:**
```python
@pytest.mark.unit
def test_block_quote_round_trip(self):
    """Block quote round-trips correctly."""
    markdown = '> This is a quote'
```

---

### Line 290-303: Missing pytest marker
**Issue:** Unit test `test_thematic_break_round_trip` is missing `@pytest.mark.unit` marker.

**Guideline:** Section "Test Types and Markers" recommends using `@pytest.mark.unit` for unit tests that test specific examples and edge cases with fast execution and deterministic results.

**Current code:**
```python
def test_thematic_break_round_trip(self):
    """Thematic break round-trips correctly."""
    markdown = 'Before\n\n---\n\nAfter'
```

**Expected code:**
```python
@pytest.mark.unit
def test_thematic_break_round_trip(self):
    """Thematic break round-trips correctly."""
    markdown = 'Before\n\n---\n\nAfter'
```

---

### Line 305-318: Missing pytest marker
**Issue:** Unit test `test_table_round_trip` is missing `@pytest.mark.unit` marker.

**Guideline:** Section "Test Types and Markers" recommends using `@pytest.mark.unit` for unit tests that test specific examples and edge cases with fast execution and deterministic results.

**Current code:**
```python
def test_table_round_trip(self):
    """Table round-trips correctly."""
    markdown = '| A | B |\n| --- | --- |\n| 1 | 2 |'
```

**Expected code:**
```python
@pytest.mark.unit
def test_table_round_trip(self):
    """Table round-trips correctly."""
    markdown = '| A | B |\n| --- | --- |\n| 1 | 2 |'
```

---

### Line 320-338: Missing pytest marker
**Issue:** Unit test `test_table_alignment_round_trip` is missing `@pytest.mark.unit` marker.

**Guideline:** Section "Test Types and Markers" recommends using `@pytest.mark.unit` for unit tests that test specific examples and edge cases with fast execution and deterministic results.

**Current code:**
```python
def test_table_alignment_round_trip(self):
    """Table with alignment round-trips correctly."""
    markdown = '| Left | Center | Right |\n| :--- | :---: | ---: |\n| 1 | 2 | 3 |'
```

**Expected code:**
```python
@pytest.mark.unit
def test_table_alignment_round_trip(self):
    """Table with alignment round-trips correctly."""
    markdown = '| Left | Center | Right |\n| :--- | :---: | ---: |\n| 1 | 2 | 3 |'
```

---

### Line 340-353: Missing pytest marker
**Issue:** Unit test `test_inline_code_serialization` is missing `@pytest.mark.unit` marker.

**Guideline:** Section "Test Types and Markers" recommends using `@pytest.mark.unit` for unit tests that test specific examples and edge cases with fast execution and deterministic results.

**Current code:**
```python
def test_inline_code_serialization(self):
    """Inline code serialization."""
    markdown = 'Text with `code` included.'
```

**Expected code:**
```python
@pytest.mark.unit
def test_inline_code_serialization(self):
    """Inline code serialization."""
    markdown = 'Text with `code` included.'
```

---

### Line 355-368: Missing pytest marker
**Issue:** Unit test `test_strikethrough_serialization` is missing `@pytest.mark.unit` marker.

**Guideline:** Section "Test Types and Markers" recommends using `@pytest.mark.unit` for unit tests that test specific examples and edge cases with fast execution and deterministic results.

**Current code:**
```python
def test_strikethrough_serialization(self):
    """Strikethrough serialization."""
    markdown = 'Text with ~~strikethrough~~ included.'
```

**Expected code:**
```python
@pytest.mark.unit
def test_strikethrough_serialization(self):
    """Strikethrough serialization."""
    markdown = 'Text with ~~strikethrough~~ included.'
```

---

### Line 370-383: Missing pytest marker
**Issue:** Unit test `test_image_serialization` is missing `@pytest.mark.unit` marker.

**Guideline:** Section "Test Types and Markers" recommends using `@pytest.mark.unit` for unit tests that test specific examples and edge cases with fast execution and deterministic results.

**Current code:**
```python
def test_image_serialization(self):
    """Image serialization."""
    markdown = '![Alt text](http://example.com/image.png)'
```

**Expected code:**
```python
@pytest.mark.unit
def test_image_serialization(self):
    """Image serialization."""
    markdown = '![Alt text](http://example.com/image.png)'
```

---

### Line 385-405: Missing pytest marker
**Issue:** Unit test `test_softbreak_serialization` is missing `@pytest.mark.unit` marker.

**Guideline:** Section "Test Types and Markers" recommends using `@pytest.mark.unit` for unit tests that test specific examples and edge cases with fast execution and deterministic results.

**Current code:**
```python
def test_softbreak_serialization(self):
    """Softbreak serialization."""
    # A parseable softbreak usually requires a newline in the input that doesn't trigger a paragraph break
    markdown = 'Line 1\nLine 2'
```

**Expected code:**
```python
@pytest.mark.unit
def test_softbreak_serialization(self):
    """Softbreak serialization."""
    # A parseable softbreak usually requires a newline in the input that doesn't trigger a paragraph break
    markdown = 'Line 1\nLine 2'
```

---

### Line 407-421: Missing pytest marker
**Issue:** Unit test `test_hard_linebreak_serialization` is missing `@pytest.mark.unit` marker.

**Guideline:** Section "Test Types and Markers" recommends using `@pytest.mark.unit` for unit tests that test specific examples and edge cases with fast execution and deterministic results.

**Current code:**
```python
def test_hard_linebreak_serialization(self):
    """Hard linebreak serialization."""
    # Hard linebreak is two spaces at end of line
    markdown = 'Line 1  \nLine 2'
```

**Expected code:**
```python
@pytest.mark.unit
def test_hard_linebreak_serialization(self):
    """Hard linebreak serialization."""
    # Hard linebreak is two spaces at end of line
    markdown = 'Line 1  \nLine 2'
```

---

### Line 427-447: Missing pytest marker
**Issue:** Unit test `test_code_with_backticks` is missing `@pytest.mark.unit` marker.

**Guideline:** Section "Test Types and Markers" recommends using `@pytest.mark.unit` for unit tests that test specific examples and edge cases with fast execution and deterministic results.

**Current code:**
```python
def test_code_with_backticks(self):
    """Code containing backticks should use longer fence."""
    markdown = '```\ncode with ``` backticks\n```'
```

**Expected code:**
```python
@pytest.mark.unit
def test_code_with_backticks(self):
    """Code containing backticks should use longer fence."""
    markdown = '```\ncode with ``` backticks\n```'
```

---

### Line 449-458: Missing pytest marker
**Issue:** Unit test `test_code_with_four_backticks` is missing `@pytest.mark.unit` marker.

**Guideline:** Section "Test Types and Markers" recommends using `@pytest.mark.unit` for unit tests that test specific examples and edge cases with fast execution and deterministic results.

**Current code:**
```python
def test_code_with_four_backticks(self):
    """Code containing four backticks should use five backticks fence."""
    markdown = '```\ncode with ```` four backticks\n```'
```

**Expected code:**
```python
@pytest.mark.unit
def test_code_with_four_backticks(self):
    """Code containing four backticks should use five backticks fence."""
    markdown = '```\ncode with ```` four backticks\n```'
```

---

### Line 460-480: Missing pytest marker
**Issue:** Unit test `test_code_only_backticks` is missing `@pytest.mark.unit` marker.

**Guideline:** Section "Test Types and Markers" recommends using `@pytest.mark.unit` for unit tests that test specific examples and edge cases with fast execution and deterministic results.

**Current code:**
```python
def test_code_only_backticks(self):
    """Code containing only backticks should be handled correctly."""
    # Use a code block that actually contains backticks as content
    markdown = '```\n```backticks```\n```'
```

**Expected code:**
```python
@pytest.mark.unit
def test_code_only_backticks(self):
    """Code containing only backticks should be handled correctly."""
    # Use a code block that actually contains backticks as content
    markdown = '```\n```backticks```\n```'
```

---

### Line 482-499: Missing pytest marker
**Issue:** Unit test `test_empty_code_block` is missing `@pytest.mark.unit` marker.

**Guideline:** Section "Test Types and Markers" recommends using `@pytest.mark.unit` for unit tests that test specific examples and edge cases with fast execution and deterministic results.

**Current code:**
```python
def test_empty_code_block(self):
    """Empty code blocks should serialize correctly."""
    markdown = '```\n\n```'
```

**Expected code:**
```python
@pytest.mark.unit
def test_empty_code_block(self):
    """Empty code blocks should serialize correctly."""
    markdown = '```\n\n```'
```

---

### Line 501-520: Missing pytest marker
**Issue:** Unit test `test_code_with_language_and_backticks` is missing `@pytest.mark.unit` marker.

**Guideline:** Section "Test Types and Markers" recommends using `@pytest.mark.unit` for unit tests that test specific examples and edge cases with fast execution and deterministic results.

**Current code:**
```python
def test_code_with_language_and_backticks(self):
    """Code with language info and backticks should preserve both."""
    markdown = '```python\nprint("```")\n```'
```

**Expected code:**
```python
@pytest.mark.unit
def test_code_with_language_and_backticks(self):
    """Code with language info and backticks should preserve both."""
    markdown = '```python\nprint("```")\n```'
```

---

### Line 522-544: Missing pytest marker
**Issue:** Unit test `test_code_with_mixed_backtick_lengths` is missing `@pytest.mark.unit` marker.

**Guideline:** Section "Test Types and Markers" recommends using `@pytest.mark.unit` for unit tests that test specific examples and edge cases with fast execution and deterministic results.

**Current code:**
```python
def test_code_with_mixed_backtick_lengths(self):
    """Code with various backtick lengths should use appropriate fence."""
    code_content = 'single ` double `` triple ``` quadruple ````'
    markdown = f'```\n{code_content}\n```'
```

**Expected code:**
```python
@pytest.mark.unit
def test_code_with_mixed_backtick_lengths(self):
    """Code with various backtick lengths should use appropriate fence."""
    code_content = 'single ` double `` triple ``` quadruple ````'
    markdown = f'```\n{code_content}\n```'
```

---

### Line 550-611: Missing pytest marker
**Issue:** Property-based test `test_fence_collision_handling_property` is missing `@pytest.mark.property` marker.

**Guideline:** Section "Test Types and Markers" states: "Property-based tests using Hypothesis" should be marked with `@pytest.mark.property`.

**Current code:**
```python
@given(st.text(min_size=0, max_size=200))
# Complex strategy: 30 examples (adequate coverage)
@settings(max_examples=30, deadline=None)
def test_fence_collision_handling_property(self, code_content):
    """**Feature: test-improvements, Code fence collision handling**
```

**Expected code:**
```python
@pytest.mark.property
@given(st.text(min_size=0, max_size=200))
# Complex strategy: 30 examples (adequate coverage)
@settings(max_examples=30, deadline=None)
def test_fence_collision_handling_property(self, code_content):
    """**Feature: test-improvements, Code fence collision handling**
```

---

### Line 613-678: Missing pytest marker
**Issue:** Property-based test `test_code_serialization_round_trip_property` is missing `@pytest.mark.property` marker.

**Guideline:** Section "Test Types and Markers" states: "Property-based tests using Hypothesis" should be marked with `@pytest.mark.property`.

**Current code:**
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
def test_code_serialization_round_trip_property(self, code_content, language):
    """**Feature: test-improvements, Code serialization round-trip**
```

**Expected code:**
```python
@pytest.mark.property
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
def test_code_serialization_round_trip_property(self, code_content, language):
    """**Feature: test-improvements, Code serialization round-trip**
```

---

### Line 684-690: Missing pytest marker
**Issue:** Unit test `test_serialize_unknown_token` is missing `@pytest.mark.unit` marker.

**Guideline:** Section "Test Types and Markers" recommends using `@pytest.mark.unit` for unit tests that test specific examples and edge cases with fast execution and deterministic results.

**Current code:**
```python
def test_serialize_unknown_token(self):
    """Test that unknown token types return empty string."""
    serializer = MarkdownSerializer()
    # Token with unknown type
    token = {'type': 'unknown_thing', 'raw': 'content'}
```

**Expected code:**
```python
@pytest.mark.unit
def test_serialize_unknown_token(self):
    """Test that unknown token types return empty string."""
    serializer = MarkdownSerializer()
    # Token with unknown type
    token = {'type': 'unknown_thing', 'raw': 'content'}
```

---

### Line 692-698: Missing pytest marker
**Issue:** Unit test `test_serialize_inline_unknown` is missing `@pytest.mark.unit` marker.

**Guideline:** Section "Test Types and Markers" recommends using `@pytest.mark.unit` for unit tests that test specific examples and edge cases with fast execution and deterministic results.

**Current code:**
```python
def test_serialize_inline_unknown(self):
    """Test that unknown inline tokens fall back to raw content."""
    serializer = MarkdownSerializer()
    # Inline token with unknown type
    token = {'type': 'weird_inline', 'raw': 'content'}
```

**Expected code:**
```python
@pytest.mark.unit
def test_serialize_inline_unknown(self):
    """Test that unknown inline tokens fall back to raw content."""
    serializer = MarkdownSerializer()
    # Inline token with unknown type
    token = {'type': 'weird_inline', 'raw': 'content'}
```

---

### Line 700-704: Missing pytest marker
**Issue:** Unit test `test_blank_line` is missing `@pytest.mark.unit` marker.

**Guideline:** Section "Test Types and Markers" recommends using `@pytest.mark.unit` for unit tests that test specific examples and edge cases with fast execution and deterministic results.

**Current code:**
```python
def test_blank_line(self):
    """Test that blank_line tokens return None."""
    serializer = MarkdownSerializer()
    token = {'type': 'blank_line'}
    assert serializer.blank_line(token) is None
```

**Expected code:**
```python
@pytest.mark.unit
def test_blank_line(self):
    """Test that blank_line tokens return None."""
    serializer = MarkdownSerializer()
    token = {'type': 'blank_line'}
    assert serializer.blank_line(token) is None
```

---

### Line 706-711: Missing pytest marker
**Issue:** Unit test `test_table_edge_cases` is missing `@pytest.mark.unit` marker.

**Guideline:** Section "Test Types and Markers" recommends using `@pytest.mark.unit` for unit tests that test specific examples and edge cases with fast execution and deterministic results.

**Current code:**
```python
def test_table_edge_cases(self):
    """Test table serialization with empty children."""
    serializer = MarkdownSerializer()
    # Table with empty children
    token = {'type': 'table', 'children': []}
    assert serializer.table(token) == ''
```

**Expected code:**
```python
@pytest.mark.unit
def test_table_edge_cases(self):
    """Test table serialization with empty children."""
    serializer = MarkdownSerializer()
    # Table with empty children
    token = {'type': 'table', 'children': []}
    assert serializer.table(token) == ''
```

---

### Line 713-722: Missing pytest marker
**Issue:** Unit test `test_serialize_list_item_unknown_child` is missing `@pytest.mark.unit` marker.

**Guideline:** Section "Test Types and Markers" recommends using `@pytest.mark.unit` for unit tests that test specific examples and edge cases with fast execution and deterministic results.

**Current code:**
```python
def test_serialize_list_item_unknown_child(self):
    """Test list item serialization with unknown child type."""
    serializer = MarkdownSerializer()
    # List item with unknown child type
    item_token = {
        'type': 'list_item',
        'children': [{'type': 'unknown_block', 'raw': 'ignore me'}]
    }
```

**Expected code:**
```python
@pytest.mark.unit
def test_serialize_list_item_unknown_child(self):
    """Test list item serialization with unknown child type."""
    serializer = MarkdownSerializer()
    # List item with unknown child type
    item_token = {
        'type': 'list_item',
        'children': [{'type': 'unknown_block', 'raw': 'ignore me'}]
    }
```

---

### Line 724-732: Missing pytest marker
**Issue:** Unit test `test_serialize_list_item_known_child_returns_empty` is missing `@pytest.mark.unit` marker.

**Guideline:** Section "Test Types and Markers" recommends using `@pytest.mark.unit` for unit tests that test specific examples and edge cases with fast execution and deterministic results.

**Current code:**
```python
def test_serialize_list_item_known_child_returns_empty(self):
    """Test list item serialization with child that serializes to empty."""
    serializer = MarkdownSerializer()
    # List item with a child that serializes to empty (e.g. blank_line)
    item_token = {
        'type': 'list_item',
        'children': [{'type': 'blank_line'}]
    }
```

**Expected code:**
```python
@pytest.mark.unit
def test_serialize_list_item_known_child_returns_empty(self):
    """Test list item serialization with child that serializes to empty."""
    serializer = MarkdownSerializer()
    # List item with a child that serializes to empty (e.g. blank_line)
    item_token = {
        'type': 'list_item',
        'children': [{'type': 'blank_line'}]
    }
```

---

### Line 734-739: Missing pytest marker
**Issue:** Unit test `test_block_code_no_newline` is missing `@pytest.mark.unit` marker.

**Guideline:** Section "Test Types and Markers" recommends using `@pytest.mark.unit` for unit tests that test specific examples and edge cases with fast execution and deterministic results.

**Current code:**
```python
def test_block_code_no_newline(self):
    """Test block code serialization without trailing newline."""
    serializer = MarkdownSerializer()
    token = {'type': 'block_code', 'raw': 'code without newline'}
    result = serializer.block_code(token)
    assert result == '```\ncode without newline\n```'
```

**Expected code:**
```python
@pytest.mark.unit
def test_block_code_no_newline(self):
    """Test block code serialization without trailing newline."""
    serializer = MarkdownSerializer()
    token = {'type': 'block_code', 'raw': 'code without newline'}
    result = serializer.block_code(token)
    assert result == '```\ncode without newline\n```'
```

---

### Line 741-746: Missing pytest marker
**Issue:** Unit test `test_block_code_with_newline` is missing `@pytest.mark.unit` marker.

**Guideline:** Section "Test Types and Markers" recommends using `@pytest.mark.unit` for unit tests that test specific examples and edge cases with fast execution and deterministic results.

**Current code:**
```python
def test_block_code_with_newline(self):
    """Test block code serialization with trailing newline."""
    serializer = MarkdownSerializer()
    token = {'type': 'block_code', 'raw': 'code with newline\n'}
    result = serializer.block_code(token)
    assert result == '```\ncode with newline\n```'
```

**Expected code:**
```python
@pytest.mark.unit
def test_block_code_with_newline(self):
    """Test block code serialization with trailing newline."""
    serializer = MarkdownSerializer()
    token = {'type': 'block_code', 'raw': 'code with newline\n'}
    result = serializer.block_code(token)
    assert result == '```\ncode with newline\n```'
```

---

## test_clipping_behavior.py

### Line 121-138: Missing pytest marker
**Issue:** Test `test_clipping_uses_stencil_view` is missing `@pytest.mark.unit` marker.

**Guideline:** Section "Test Types and Markers" recommends using `@pytest.mark.unit` for unit tests that test specific examples and edge cases with fast execution and deterministic results.

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

---

### Line 235-242: Missing pytest marker
**Issue:** Test `test_default_settings_no_clipping` is missing `@pytest.mark.unit` marker.

**Guideline:** Section "Test Types and Markers" recommends using `@pytest.mark.unit` for unit tests that test specific examples and edge cases with fast execution and deterministic results.

**Current code:**
```python
def test_default_settings_no_clipping(self):
    """Default MarkdownLabel settings do not enable clipping."""
    label = MarkdownLabel(text="Test content")
    label.force_rebuild()

    assert not has_clipping_container(label), (
        "Default settings should not enable clipping"
    )
```

**Expected code:**
```python
@pytest.mark.unit
def test_default_settings_no_clipping(self):
    """Default MarkdownLabel settings do not enable clipping."""
    label = MarkdownLabel(text="Test content")
    label.force_rebuild()

    assert not has_clipping_container(label), (
        "Default settings should not enable clipping"
    )
```

---

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

## test_clipping_behavior.py

### Line 121-138: Missing pytest marker
**Issue:** Test `test_clipping_uses_stencil_view` is missing `@pytest.mark.unit` marker.

**Guideline:** Section "Test Types and Markers" recommends using `@pytest.mark.unit` for unit tests that test specific examples and edge cases with fast execution and deterministic results.

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

---

### Line 235-242: Missing pytest marker
**Issue:** Test `test_default_settings_no_clipping` is missing `@pytest.mark.unit` marker.

**Guideline:** Section "Test Types and Markers" recommends using `@pytest.mark.unit` for unit tests that test specific examples and edge cases with fast execution and deterministic results.

**Current code:**
```python
def test_default_settings_no_clipping(self):
    """Default MarkdownLabel settings do not enable clipping."""
    label = MarkdownLabel(text="Test content")
    label.force_rebuild()

    assert not has_clipping_container(label), (
        "Default settings should not enable clipping"
    )
```

**Expected code:**
```python
@pytest.mark.unit
def test_default_settings_no_clipping(self):
    """Default MarkdownLabel settings do not enable clipping."""
    label = MarkdownLabel(text="Test content")
    label.force_rebuild()

    assert not has_clipping_container(label), (
        "Default settings should not enable clipping"
    )
```

---

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

### Line 32-96: Missing pytest markers for unit tests
**Issue:** Tests in `TestTextureRenderModeStructure` class are missing `@pytest.mark.unit` markers.

**Guideline:** Section "Test Types and Markers" recommends using `@pytest.mark.unit` for unit tests that test specific examples and edge cases with fast execution and deterministic results.

**Current code:**
```python
@pytest.mark.slow
class TestTextureRenderModeStructure:
    """Property tests for texture render mode structure."""

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

**Expected code:**
```python
@pytest.mark.slow
class TestTextureRenderModeStructure:
    """Property tests for texture render mode structure."""

    @pytest.mark.unit
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

**Note:** This applies to all tests in this class: `test_texture_mode_creates_image_widget`, `test_texture_mode_with_empty_text_no_image`, `test_widgets_mode_no_image_widget`, `test_render_mode_property_values`, and `test_default_render_mode_is_widgets`.

---

### Line 103-157: Missing pytest markers for unit tests
**Issue:** Tests in `TestTextureModeLinksHandling` class are missing `@pytest.mark.unit` markers.

**Guideline:** Section "Test Types and Markers" recommends using `@pytest.mark.unit` for unit tests that test specific examples and edge cases with fast execution and deterministic results.

**Current code:**
```python
@pytest.mark.slow
class TestTextureModeLinksHandling:
    """Property tests for texture mode link handling."""

    def test_aggregated_refs_populated_in_texture_mode(self):
        """In texture mode, _aggregated_refs is populated with link zones."""
        label = MarkdownLabel(
            text='Click [here](http://example.com) for more info.',
            render_mode='texture',
            size=(400, 300),
            size_hint=(None, None)
        )
        label.force_rebuild()

        # Check that aggregated refs were collected
        # Note: The refs may be empty if texture rendering failed or
        # if link zones couldn't be calculated
        assert hasattr(label, '_aggregated_refs'), \
            "Expected _aggregated_refs attribute"
```

**Expected code:**
```python
@pytest.mark.slow
class TestTextureModeLinksHandling:
    """Property tests for texture mode link handling."""

    @pytest.mark.unit
    def test_aggregated_refs_populated_in_texture_mode(self):
        """In texture mode, _aggregated_refs is populated with link zones."""
        label = MarkdownLabel(
            text='Click [here](http://example.com) for more info.',
            render_mode='texture',
            size=(400, 300),
            size_hint=(None, None)
        )
        label.force_rebuild()

        # Check that aggregated refs were collected
        # Note: The refs may be empty if texture rendering failed or
        # if link zones couldn't be calculated
        assert hasattr(label, '_aggregated_refs'), \
            "Expected _aggregated_refs attribute"
```

**Note:** This applies to all tests in this class: `test_aggregated_refs_populated_in_texture_mode`, `test_widgets_mode_no_aggregated_refs`, and `test_multiple_links_collected`.

---

### Line 165-460: Missing pytest markers for unit tests and property tests
**Issue:** Tests in `TestDeterministicTextureHitTesting` class are missing appropriate pytest markers. Deterministic tests should use `@pytest.mark.unit` and property-based tests should use `@pytest.mark.property`.

**Guideline:** Section "Test Types and Markers" states: "Property-based tests using Hypothesis" should be marked with `@pytest.mark.property`, and unit tests should use `@pytest.mark.unit`.

**Current code:**
```python
@pytest.mark.slow
class TestDeterministicTextureHitTesting:
    """Deterministic tests for texture mode hit-testing without window dependency.

    These tests manually inject _aggregated_refs to verify hit-testing logic
    without relying on actual texture rendering.
    """

    def test_inside_zone_dispatch(self):
        """Touch inside ref zone dispatches on_ref_press and returns True."""
        # Create MarkdownLabel with render_mode='texture'
        label = MarkdownLabel(
            text='Test content',
            render_mode='texture',
            size=(400, 300),
            size_hint=(None, None),
            pos=(0, 0)
        )
```

**Expected code:**
```python
@pytest.mark.slow
class TestDeterministicTextureHitTesting:
    """Deterministic tests for texture mode hit-testing without window dependency.

    These tests manually inject _aggregated_refs to verify hit-testing logic
    without relying on actual texture rendering.
    """

    @pytest.mark.unit
    def test_inside_zone_dispatch(self):
        """Touch inside ref zone dispatches on_ref_press and returns True."""
        # Create MarkdownLabel with render_mode='texture'
        label = MarkdownLabel(
            text='Test content',
            render_mode='texture',
            size=(400, 300),
            size_hint=(None, None),
            pos=(0, 0)
        )
```

**Note:** This applies to:
- Unit tests: `test_inside_zone_dispatch`, `test_outside_zone_no_dispatch`, `test_multiple_zones_first_match`, `test_multiple_zones_non_overlapping`
- Property tests: `test_property_inside_zone_dispatch`, `test_property_outside_zone_no_dispatch` (should also add `@pytest.mark.property`)

---

### Line 471-538: Missing pytest markers for unit tests
**Issue:** Tests in `TestTextureFallbackBranch` class are missing `@pytest.mark.unit` markers.

**Guideline:** Section "Test Types and Markers" recommends using `@pytest.mark.unit` for unit tests that test specific examples and edge cases with fast execution and deterministic results.

**Current code:**
```python
@pytest.mark.slow
class TestTextureFallbackBranch:
    """Tests for texture mode fallback to widgets mode when rendering fails."""

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
```

**Expected code:**
```python
@pytest.mark.slow
class TestTextureFallbackBranch:
    """Tests for texture mode fallback to widgets mode when rendering fails."""

    @pytest.mark.unit
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
```

**Note:** This applies to both tests in this class: `test_texture_fallback_to_widgets_mode` and `test_texture_fallback_preserves_content`.

---

### Line 541-641: Missing pytest markers for unit tests
**Issue:** Tests in `TestAutoRenderModeSelection` class are missing `@pytest.mark.unit` markers.

**Guideline:** Section "Test Types and Markers" recommends using `@pytest.mark.unit` for unit tests that test specific examples and edge cases with fast execution and deterministic results.

**Current code:**
```python
@pytest.mark.slow
class TestAutoRenderModeSelection:
    """Property tests for auto render mode selection."""

    def test_auto_mode_uses_widgets_by_default(self):
        """Auto mode uses 'widgets' for simple content without constraints."""
        label = MarkdownLabel(
            text='Hello World',
            render_mode='auto',
            strict_label_mode=False
        )

        effective_mode = label._get_effective_render_mode()
        assert effective_mode == 'widgets', \
            f"Expected 'widgets' for simple content, got '{effective_mode}'"
```

**Expected code:**
```python
@pytest.mark.slow
class TestAutoRenderModeSelection:
    """Property tests for auto render mode selection."""

    @pytest.mark.unit
    def test_auto_mode_uses_widgets_by_default(self):
        """Auto mode uses 'widgets' for simple content without constraints."""
        label = MarkdownLabel(
            text='Hello World',
            render_mode='auto',
            strict_label_mode=False
        )

        effective_mode = label._get_effective_render_mode()
        assert effective_mode == 'widgets', \
            f"Expected 'widgets' for simple content, got '{effective_mode}'"
```

**Note:** This applies to all tests in this class: `test_auto_mode_uses_widgets_by_default`, `test_auto_mode_uses_texture_with_strict_mode_and_height`, `test_auto_mode_uses_texture_with_text_size_height`, `test_auto_mode_uses_widgets_without_strict_mode`, `test_auto_mode_selection_combinations`, `test_explicit_widgets_mode_overrides_auto_logic`, and `test_explicit_texture_mode_overrides_auto_logic`.

---

### Line 216-279: Missing @pytest.mark.property marker for property-based test
**Issue:** Property-based test `test_property_inside_zone_dispatch` is missing `@pytest.mark.property` marker.

**Guideline:** Section "Test Types and Markers" states: "Property-based tests using Hypothesis" should be marked with `@pytest.mark.property`.

**Current code:**
```python
    @given(
        zone=st.tuples(
            st.floats(min_value=0, max_value=300, allow_nan=False),
            st.floats(min_value=0, max_value=200, allow_nan=False),
            st.floats(min_value=10, max_value=100, allow_nan=False),
            st.floats(min_value=10, max_value=50, allow_nan=False)
        ),
        ref_name=st.from_regex(
            r'https?://[a-z]{3,10}\.[a-z]{2,5}/[a-z]{1,10}',
            fullmatch=True
        ),
        touch_offset_x=st.floats(min_value=0.1, max_value=0.9, allow_nan=False),
        touch_offset_y=st.floats(min_value=0.1, max_value=0.9, allow_nan=False)
    )
    # Mixed finite/complex strategy: 50 examples (multiple finite dimensions × complex samples)
    @settings(max_examples=50, deadline=None)
    def test_property_inside_zone_dispatch(
        self, zone, ref_name, touch_offset_x, touch_offset_y
    ):
```

**Expected code:**
```python
    @pytest.mark.property
    @given(
        zone=st.tuples(
            st.floats(min_value=0, max_value=300, allow_nan=False),
            st.floats(min_value=0, max_value=200, allow_nan=False),
            st.floats(min_value=10, max_value=100, allow_nan=False),
            st.floats(min_value=10, max_value=50, allow_nan=False)
        ),
        ref_name=st.from_regex(
            r'https?://[a-z]{3,10}\.[a-z]{2,5}/[a-z]{1,10}',
            fullmatch=True
        ),
        touch_offset_x=st.floats(min_value=0.1, max_value=0.9, allow_nan=False),
        touch_offset_y=st.floats(min_value=0.1, max_value=0.9, allow_nan=False)
    )
    # Mixed finite/complex strategy: 50 examples (multiple finite dimensions × complex samples)
    @settings(max_examples=50, deadline=None)
    def test_property_inside_zone_dispatch(
        self, zone, ref_name, touch_offset_x, touch_offset_y
    ):
```

---

### Line 319-379: Missing @pytest.mark.property marker for property-based test
**Issue:** Property-based test `test_property_outside_zone_no_dispatch` is missing `@pytest.mark.property` marker.

**Guideline:** Section "Test Types and Markers" states: "Property-based tests using Hypothesis" should be marked with `@pytest.mark.property`.

**Current code:**
```python
    @given(
        zone=st.tuples(
            st.floats(min_value=50, max_value=150, allow_nan=False),
            st.floats(min_value=50, max_value=100, allow_nan=False),
            st.floats(min_value=10, max_value=50, allow_nan=False),
            st.floats(min_value=10, max_value=30, allow_nan=False)
        ),
        ref_name=st.from_regex(
            r'https?://[a-z]{3,10}\.[a-z]{2,5}/[a-z]{1,10}',
            fullmatch=True
        ),
        outside_offset=st.floats(min_value=10, max_value=50, allow_nan=False)
    )
    # Mixed finite/complex strategy: 50 examples (multiple finite dimensions × complex samples)
    @settings(max_examples=50, deadline=None)
    def test_property_outside_zone_no_dispatch(self, zone, ref_name, outside_offset):
```

**Expected code:**
```python
    @pytest.mark.property
    @given(
        zone=st.tuples(
            st.floats(min_value=50, max_value=150, allow_nan=False),
            st.floats(min_value=50, max_value=100, allow_nan=False),
            st.floats(min_value=10, max_value=50, allow_nan=False),
            st.floats(min_value=10, max_value=30, allow_nan=False)
        ),
        ref_name=st.from_regex(
            r'https?://[a-z]{3,10}\.[a-z]{2,5}/[a-z]{1,10}',
            fullmatch=True
        ),
        outside_offset=st.floats(min_value=10, max_value=50, allow_nan=False)
    )
    # Mixed finite/complex strategy: 50 examples (multiple finite dimensions × complex samples)
    @settings(max_examples=50, deadline=None)
    def test_property_outside_zone_no_dispatch(self, zone, ref_name, outside_offset):
```

---

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

### Lines 31-33: Missing pytest marker for property-based test
**Issue:** Property-based test `test_texture_size_returns_tuple` is missing `@pytest.mark.property` marker.

**Guideline:** Section "Test Types and Markers" states: "Property-based tests using Hypothesis" should be marked with `@pytest.mark.property`.

**Current code:**
```python
@given(simple_markdown_document())
# Complex strategy: 20 examples (adequate coverage)
@settings(max_examples=20, deadline=None)
def test_texture_size_returns_tuple(self, markdown_text):
    """texture_size returns a list/tuple with two elements."""
```

**Expected code:**
```python
@pytest.mark.property
@given(simple_markdown_document())
# Complex strategy: 20 examples (adequate coverage)
@settings(max_examples=20, deadline=None)
def test_texture_size_returns_tuple(self, markdown_text):
    """texture_size returns a list/tuple with two elements."""
```

---

### Lines 45-47: Missing pytest marker for property-based test
**Issue:** Property-based test `test_texture_size_non_negative` is missing `@pytest.mark.property` marker.

**Guideline:** Section "Test Types and Markers" states: "Property-based tests using Hypothesis" should be marked with `@pytest.mark.property`.

**Current code:**
```python
@given(simple_markdown_document())
# Complex strategy: 20 examples (adequate coverage)
@settings(max_examples=20, deadline=None)
def test_texture_size_non_negative(self, markdown_text):
    """texture_size width and height are non-negative."""
```

**Expected code:**
```python
@pytest.mark.property
@given(simple_markdown_document())
# Complex strategy: 20 examples (adequate coverage)
@settings(max_examples=20, deadline=None)
def test_texture_size_non_negative(self, markdown_text):
    """texture_size width and height are non-negative."""
```

---

### Lines 68-70: Missing pytest marker for property-based test
**Issue:** Property-based test `test_heading_creates_label_widget` is missing `@pytest.mark.property` marker.

**Guideline:** Section "Test Types and Markers" states: "Property-based tests using Hypothesis" should be marked with `@pytest.mark.property`.

**Current code:**
```python
@given(markdown_heading())
# Complex strategy: 20 examples (adequate coverage)
@settings(max_examples=20, deadline=None)
def test_heading_creates_label_widget(self, heading):
    """Heading content creates a Label widget that is included in texture_size calculation."""
```

**Expected code:**
```python
@pytest.mark.property
@given(markdown_heading())
# Complex strategy: 20 examples (adequate coverage)
@settings(max_examples=20, deadline=None)
def test_heading_creates_label_widget(self, heading):
    """Heading content creates a Label widget that is included in texture_size calculation."""
```

---

### Lines 84-86: Missing pytest marker for property-based test
**Issue:** Property-based test `test_paragraph_creates_label_widget` is missing `@pytest.mark.property` marker.

**Guideline:** Section "Test Types and Markers" states: "Property-based tests using Hypothesis" should be marked with `@pytest.mark.property`.

**Current code:**
```python
@given(markdown_paragraph())
# Complex strategy: 20 examples (adequate coverage)
@settings(max_examples=20, deadline=None)
def test_paragraph_creates_label_widget(self, paragraph):
    """Paragraph content creates a Label widget that is included in texture_size calculation."""
```

**Expected code:**
```python
@pytest.mark.property
@given(markdown_paragraph())
# Complex strategy: 20 examples (adequate coverage)
@settings(max_examples=20, deadline=None)
def test_paragraph_creates_label_widget(self, paragraph):
    """Paragraph content creates a Label widget that is included in texture_size calculation."""
```

---

### Line 59-66: Missing pytest marker for unit test
**Issue:** Unit test `test_empty_label_texture_size_is_zero` is missing `@pytest.mark.unit` marker.

**Guideline:** Section "Test Types and Markers" recommends using `@pytest.mark.unit` for unit tests that test specific examples and edge cases with fast execution and deterministic results.

**Current code:**
```python
def test_empty_label_texture_size_is_zero(self):
    """Empty MarkdownLabel has texture_size [0, 0]."""
    label = MarkdownLabel(text='')

    texture_size = label.texture_size

    assert texture_size == [0, 0], \
        f"Expected texture_size [0, 0] for empty label, got {texture_size}"
```

**Expected code:**
```python
@pytest.mark.unit
def test_empty_label_texture_size_is_zero(self):
    """Empty MarkdownLabel has texture_size [0, 0]."""
    label = MarkdownLabel(text='')

    texture_size = label.texture_size

    assert texture_size == [0, 0], \
        f"Expected texture_size [0, 0] for empty label, got {texture_size}"
```

---

### Line 102-114: Missing pytest marker for unit test
**Issue:** Unit test `test_code_block_creates_container_widget` is missing `@pytest.mark.unit` marker.

**Guideline:** Section "Test Types and Markers" recommends using `@pytest.mark.unit` for unit tests that test specific examples and edge cases with fast execution and deterministic results.

**Current code:**
```python
def test_code_block_creates_container_widget(self):
    """Code block content creates a BoxLayout container that is included in texture_size calculation."""
    markdown = '```python\nprint("hello")\n```'
    label = MarkdownLabel(text=markdown)
```

**Expected code:**
```python
@pytest.mark.unit
def test_code_block_creates_container_widget(self):
    """Code block content creates a BoxLayout container that is included in texture_size calculation."""
    markdown = '```python\nprint("hello")\n```'
    label = MarkdownLabel(text=markdown)
```

---

### Line 116-128: Missing pytest marker for unit test
**Issue:** Unit test `test_list_creates_container_widget` is missing `@pytest.mark.unit` marker.

**Guideline:** Section "Test Types and Markers" recommends using `@pytest.mark.unit` for unit tests that test specific examples and edge cases with fast execution and deterministic results.

**Current code:**
```python
def test_list_creates_container_widget(self):
    """List content creates a BoxLayout container that is included in texture_size calculation."""
    markdown = '- Item 1\n- Item 2\n- Item 3'
    label = MarkdownLabel(text=markdown)
```

**Expected code:**
```python
@pytest.mark.unit
def test_list_creates_container_widget(self):
    """List content creates a BoxLayout container that is included in texture_size calculation."""
    markdown = '- Item 1\n- Item 2\n- Item 3'
    label = MarkdownLabel(text=markdown)
```

---

### Line 130-146: Missing pytest marker for unit test
**Issue:** Unit test `test_table_creates_gridlayout_widget` is missing `@pytest.mark.unit` marker.

**Guideline:** Section "Test Types and Markers" recommends using `@pytest.mark.unit` for unit tests that test specific examples and edge cases with fast execution and deterministic results.

**Current code:**
```python
def test_table_creates_gridlayout_widget(self):
    """Table content creates a GridLayout widget that is included in texture_size calculation."""
    markdown = '| A | B |\n| --- | --- |\n| 1 | 2 |'
    label = MarkdownLabel(text=markdown)
```

**Expected code:**
```python
@pytest.mark.unit
def test_table_creates_gridlayout_widget(self):
    """Table content creates a GridLayout widget that is included in texture_size calculation."""
    markdown = '| A | B |\n| --- | --- |\n| 1 | 2 |'
    label = MarkdownLabel(text=markdown)
```

---

### Line 148-160: Missing pytest marker for unit test
**Issue:** Unit test `test_block_quote_creates_container_widget` is missing `@pytest.mark.unit` marker.

**Guideline:** Section "Test Types and Markers" recommends using `@pytest.mark.unit` for unit tests that test specific examples and edge cases with fast execution and deterministic results.

**Current code:**
```python
def test_block_quote_creates_container_widget(self):
    """Block quote content creates a BoxLayout container that is included in texture_size calculation."""
    markdown = '> This is a quote'
    label = MarkdownLabel(text=markdown)
```

**Expected code:**
```python
@pytest.mark.unit
def test_block_quote_creates_container_widget(self):
    """Block quote content creates a BoxLayout container that is included in texture_size calculation."""
    markdown = '> This is a quote'
    label = MarkdownLabel(text=markdown)
```

---

### Line 162-172: Missing pytest marker for unit test
**Issue:** Unit test `test_thematic_break_contributes_to_texture_size` is missing `@pytest.mark.unit` marker.

**Guideline:** Section "Test Types and Markers" recommends using `@pytest.mark.unit` for unit tests that test specific examples and edge cases with fast execution and deterministic results.

**Current code:**
```python
def test_thematic_break_contributes_to_texture_size(self):
    """Thematic break (horizontal rule) contributes to texture_size with explicit height."""
    markdown = 'Before\n\n---\n\nAfter'
    label = MarkdownLabel(text=markdown)
```

**Expected code:**
```python
@pytest.mark.unit
def test_thematic_break_contributes_to_texture_size(self):
    """Thematic break (horizontal rule) contributes to texture_size with explicit height."""
    markdown = 'Before\n\n---\n\nAfter'
    label = MarkdownLabel(text=markdown)
```

---

### Lines 174-189: Missing pytest marker for property-based test
**Issue:** Property-based test `test_more_content_increases_texture_height` is missing `@pytest.mark.property` marker.

**Guideline:** Section "Test Types and Markers" states: "Property-based tests using Hypothesis" should be marked with `@pytest.mark.property`.

**Current code:**
```python
@given(st.integers(min_value=1, max_value=5))
# Small finite strategy: 5 examples (input space size: 5)
@settings(max_examples=5, deadline=None)
def test_more_content_increases_texture_height(self, num_paragraphs):
    """More content results in larger texture_size height."""
```

**Expected code:**
```python
@pytest.mark.property
@given(st.integers(min_value=1, max_value=5))
# Small finite strategy: 5 examples (input space size: 5)
@settings(max_examples=5, deadline=None)
def test_more_content_increases_texture_height(self, num_paragraphs):
    """More content results in larger texture_size height."""
```

---

### Line 191-216: Missing pytest marker for unit test
**Issue:** Unit test `test_mixed_content_creates_multiple_widgets` is missing `@pytest.mark.unit` marker.

**Guideline:** Section "Test Types and Markers" recommends using `@pytest.mark.unit` for unit tests that test specific examples and edge cases with fast execution and deterministic results.

**Current code:**
```python
def test_mixed_content_creates_multiple_widgets(self):
    """Mixed content (heading, paragraph, code, list) creates multiple widgets for texture_size."""
    markdown = '''# Heading

This is a paragraph.

```python
code = "block"
```

- List item 1
- List item 2

> A quote
'''
    label = MarkdownLabel(text=markdown)
```

**Expected code:**
```python
@pytest.mark.unit
def test_mixed_content_creates_multiple_widgets(self):
    """Mixed content (heading, paragraph, code, list) creates multiple widgets for texture_size."""
    markdown = '''# Heading

This is a paragraph.

```python
code = "block"
```

- List item 1
- List item 2

> A quote
'''
    label = MarkdownLabel(text=markdown)
```

---

### Lines 218-236: Missing pytest marker for property-based test
**Issue:** Property-based test `test_texture_size_accessible_for_all_content` is missing `@pytest.mark.property` marker.

**Guideline:** Section "Test Types and Markers" states: "Property-based tests using Hypothesis" should be marked with `@pytest.mark.property`.

**Current code:**
```python
@given(simple_markdown_document())
# Complex strategy: 20 examples (adequate coverage)
@settings(max_examples=20, deadline=None)
def test_texture_size_accessible_for_all_content(self, markdown_text):
    """texture_size is accessible and valid for all markdown content."""
```

**Expected code:**
```python
@pytest.mark.property
@given(simple_markdown_document())
# Complex strategy: 20 examples (adequate coverage)
@settings(max_examples=20, deadline=None)
def test_texture_size_accessible_for_all_content(self, markdown_text):
    """texture_size is accessible and valid for all markdown content."""
```

---

### Line 238-253: Missing pytest marker for unit test
**Issue:** Unit test `test_nested_list_creates_nested_containers` is missing `@pytest.mark.unit` marker.

**Guideline:** Section "Test Types and Markers" recommends using `@pytest.mark.unit` for unit tests that test specific examples and edge cases with fast execution and deterministic results.

**Current code:**
```python
def test_nested_list_creates_nested_containers(self):
    """Nested list content creates nested BoxLayout containers for texture_size calculation."""
    markdown = '''- Item 1
  - Nested 1
  - Nested 2
- Item 2'''
    label = MarkdownLabel(text=markdown)
```

**Expected code:**
```python
@pytest.mark.unit
def test_nested_list_creates_nested_containers(self):
    """Nested list content creates nested BoxLayout containers for texture_size calculation."""
    markdown = '''- Item 1
  - Nested 1
  - Nested 2
- Item 2'''
    label = MarkdownLabel(text=markdown)
```

---

### Line 255-267: Missing pytest marker for unit test
**Issue:** Unit test `test_ordered_list_creates_container_widget` is missing `@pytest.mark.unit` marker.

**Guideline:** Section "Test Types and Markers" recommends using `@pytest.mark.unit` for unit tests that test specific examples and edge cases with fast execution and deterministic results.

**Current code:**
```python
def test_ordered_list_creates_container_widget(self):
    """Ordered list content creates a BoxLayout container for texture_size calculation."""
    markdown = '1. First\n2. Second\n3. Third'
    label = MarkdownLabel(text=markdown)
```

**Expected code:**
```python
@pytest.mark.unit
def test_ordered_list_creates_container_widget(self):
    """Ordered list content creates a BoxLayout container for texture_size calculation."""
    markdown = '1. First\n2. Second\n3. Third'
    label = MarkdownLabel(text=markdown)
```

---

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

### Line 295-314: Missing pytest marker for unit test
**Issue:** Unit test `test_texture_size_with_image_markdown` is missing `@pytest.mark.unit` marker.

**Guideline:** Section "Test Types and Markers" recommends using `@pytest.mark.unit` for unit tests that test specific examples and edge cases with fast execution and deterministic results.

**Current code:**
```python
def test_texture_size_with_image_markdown(self):
    """Image markdown contributes to texture_size.

    Note: In Markdown, images are inline elements typically wrapped in paragraphs.
    The texture_size should account for the containing paragraph and/or image widget.
    """
    # Use image in a paragraph context (common usage)
    markdown = 'Here is an image:\n\n![Alt text](https://example.com/image.png)\n\nAfter image.'
    label = MarkdownLabel(text=markdown)
```

**Expected code:**
```python
@pytest.mark.unit
def test_texture_size_with_image_markdown(self):
    """Image markdown contributes to texture_size.

    Note: In Markdown, images are inline elements typically wrapped in paragraphs.
    The texture_size should account for the containing paragraph and/or image widget.
    """
    # Use image in a paragraph context (common usage)
    markdown = 'Here is an image:\n\n![Alt text](https://example.com/image.png)\n\nAfter image.'
    label = MarkdownLabel(text=markdown)
```

---

### Lines 316-331: Missing pytest marker for property-based test
**Issue:** Property-based test `test_all_heading_levels_create_label_widgets` is missing `@pytest.mark.property` marker.

**Guideline:** Section "Test Types and Markers" states: "Property-based tests using Hypothesis" should be marked with `@pytest.mark.property`.

**Current code:**
```python
@given(st.integers(min_value=1, max_value=6))
# Small finite strategy: 6 examples (input space size: 6)
@settings(max_examples=6, deadline=None)
def test_all_heading_levels_create_label_widgets(self, level):
    """All heading levels create Label widgets for texture_size calculation."""
```

**Expected code:**
```python
@pytest.mark.property
@given(st.integers(min_value=1, max_value=6))
# Small finite strategy: 6 examples (input space size: 6)
@settings(max_examples=6, deadline=None)
def test_all_heading_levels_create_label_widgets(self, level):
    """All heading levels create Label widgets for texture_size calculation."""
```

---

### Line 333-356: Missing pytest marker for unit test
**Issue:** Unit test `test_blank_lines_create_spacer_widgets` is missing `@pytest.mark.unit` marker.

**Guideline:** Section "Test Types and Markers" recommends using `@pytest.mark.unit` for unit tests that test specific examples and edge cases with fast execution and deterministic results.

**Current code:**
```python
def test_blank_lines_create_spacer_widgets(self):
    """Blank lines create spacer widgets with explicit height for texture_size."""
    markdown_no_blanks = 'Para 1\nPara 2'
    markdown_with_blanks = 'Para 1\n\n\n\nPara 2'
```

**Expected code:**
```python
@pytest.mark.unit
def test_blank_lines_create_spacer_widgets(self):
    """Blank lines create spacer widgets with explicit height for texture_size."""
    markdown_no_blanks = 'Para 1\nPara 2'
    markdown_with_blanks = 'Para 1\n\n\n\nPara 2'
```
