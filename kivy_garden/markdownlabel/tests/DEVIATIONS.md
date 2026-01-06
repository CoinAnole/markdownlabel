# Deviations

## test_import.py

### Line 12-16: Missing pytest marker
**Issue:** Test `test_markdownlabel_import` is missing the `@pytest.mark.unit` marker.

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
**Issue:** Test `test_markdownlabel_text_property` is missing the `@pytest.mark.unit` marker.

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
**Issue:** Test `test_exactly_10_levels_renders_fully` is missing the `@pytest.mark.needs_window` marker.

**Guideline:** Tests that create MarkdownLabel instances should use `@pytest.mark.needs_window` marker (as evidenced by other tests in the same file that create MarkdownLabel instances, such as lines 32, 46, 64, 108, 156, 175, 205, 228, 249, 279, 298, 316).

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
**Issue:** Test `test_beyond_10_levels_still_renders` is missing the `@pytest.mark.needs_window` marker.

**Guideline:** Tests that create MarkdownLabel instances should use `@pytest.mark.needs_window` marker (as evidenced by other tests in the same file that create MarkdownLabel instances, such as lines 32, 46, 64, 108, 156, 175, 205, 228, 249, 279, 298, 316).

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
**Issue:** Test `test_label_compatibility_imports_resolve` is a meta-test (tests about the test suite itself) but is missing the `@pytest.mark.test_tests` marker.

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
**Issue:** Test `test_shared_utilities_imports_resolve` is a meta-test (tests about the test suite itself) but is missing the `@pytest.mark.test_tests` marker.

**Guideline:** Section "Test Types and Markers" - "Meta-Test Marking" states: "Tests that validate the test suite itself must be marked with `@pytest.mark.test_tests`."

**Current code:**
```python
def test_shared_utilities_imports_resolve(self):
    """Shared test utilities imports resolve successfully."""
    try:
        # Test importing the utilities module
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
        # Test importing the utilities module
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
**Issue:** Test `test_cross_module_imports_work` is a meta-test (tests about the test suite itself) but is missing the `@pytest.mark.test_tests` marker.

**Guideline:** Section "Test Types and Markers" - "Meta-Test Marking" states: "Tests that validate the test suite itself must be marked with `@pytest.mark.test_tests`."

**Current code:**
```python
def test_cross_module_imports_work(self):
    """Test modules can import from shared utilities."""
    try:
        # Import the label compatibility module which uses test_utils
        from kivy_garden.markdownlabel.tests.test_label_compatibility import (
            TestFontSizeAliasBidirectionality,
        )

        # Verify that the class can be instantiated (imports worked)
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

**Note:** While the current implementation using `@pytest.mark.parametrize` is technically acceptable for a 4-value enumeration (the guidelines state "Single enum, ≤10 values: @pytest.mark.parametrize"), the inconsistency within the class is the issue. The class `TestAdvancedFontPropertyForwarding` uses property-based testing for all other similar tests (`test_font_family_excluded_from_code_blocks`, `test_font_family_forwarded_to_non_code_labels`, `test_font_context_forwarded_to_all_labels_including_code`, `test_font_features_forwarded_to_all_labels_including_code`, `test_font_kerning_forwarded_to_all_labels_including_code`), so this one test should follow the same pattern for consistency.


**Expected code:**
```python
@pytest.mark.test_tests
def test_cross_module_imports_work(self):
    """Test modules can import from shared utilities."""
    try:
        # Import the label compatibility module which uses test_utils
        from kivy_garden.markdownlabel.tests.test_label_compatibility import (
            TestFontSizeAliasBidirectionality,
        )

        # Verify that the class can be instantiated (imports worked)
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
**Issue:** Test `test_links_unstyled_by_default` is missing the `@pytest.mark.unit` marker.

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
**Issue:** Test `test_links_styled_when_enabled` is missing the `@pytest.mark.unit` marker.

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
**Issue:** Test `test_default_padding_is_zero` is missing the `@pytest.mark.unit` marker.

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
**Issue:** Test `test_default_padding_is_zero_for_all_labels` is missing the `@pytest.mark.unit` marker.

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
**Issue:** Test `test_default_values_synchronized` is missing the `@pytest.mark.unit` marker.

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

---

## test_performance.py

No deviations found. The test file follows all testing guidelines:

- ✅ Test naming conventions accurately reflect what they assert
- ✅ Proper pytest markers used (@pytest.mark.slow for class)
- ✅ Property-based testing optimization with appropriate max_examples values and standardized comments
- ✅ Helper functions used from test_utils.py (find_labels_recursive, collect_widget_ids, st_font_size, st_rgba_color)
- ✅ Rebuild contract testing patterns followed correctly (manual ID collection for style-only and structure property tests)
- ✅ Test file structure and organization is appropriate
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
