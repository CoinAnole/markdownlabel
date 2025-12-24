## Tool Result 1


Subtask f4e5f4ae-05c3-42ec-936a-4a6a0b3fc0cb completed.

Result:
I've provided a comprehensive summary of all testing guidelines from [`TESTING.md`](kivy_garden/markdownlabel/tests/TESTING.md). The summary covers 12 main areas:

1. **Test Organization** - File and class organization principles
2. **Test Naming Conventions** - Standard patterns for test methods and classes
3. **Test Types and Markers** - Pytest markers and test categories
4. **Rebuild Contract Testing** - Style-only vs structure properties and testing approaches
5. **Property-Based Testing** - When to use and how to structure property tests
6. **Property-Based Testing Optimization** - Strategy classifications and max_examples guidelines
7. **Helper Functions** - Shared utilities from [`test_utils.py`](kivy_garden/markdownlabel/tests/test_utils.py)
8. **Test File Structure** - Standard templates and naming conventions
9. **Standardization Tools** - CLI tools for validation and optimization
10. **Validation and CI Integration** - Pre-commit hooks and GitHub Actions
11. **Best Practices** - Do's, don'ts, performance considerations, and debugging tips
12. **Validation Checklist** - 10-point checklist before committing tests

The guidelines emphasize descriptive naming, proper organization, right-sizing property-based tests based on input space, using shared helpers, and following standardized comment formats for Hypothesis strategies.

---

## Tool Result 2


Subtask 44c965b8-586e-4859-b2b2-dd3834029804 completed.

Result:
Here is the complete list of Python test files in the `kivy_garden/markdownlabel/tests/` directory:

## Main tests directory:
- [`kivy_garden/markdownlabel/tests/test_advanced_compatibility.py`](kivy_garden/markdownlabel/tests/test_advanced_compatibility.py)
- [`kivy_garden/markdownlabel/tests/test_clipping_behavior.py`](kivy_garden/markdownlabel/tests/test_clipping_behavior.py)
- [`kivy_garden/markdownlabel/tests/test_color_properties.py`](kivy_garden/markdownlabel/tests/test_color_properties.py)
- [`kivy_garden/markdownlabel/tests/test_comment_format.py`](kivy_garden/markdownlabel/tests/test_comment_format.py)
- [`kivy_garden/markdownlabel/tests/test_comment_standardizer.py`](kivy_garden/markdownlabel/tests/test_comment_standardizer.py)
- [`kivy_garden/markdownlabel/tests/test_core_functionality_properties.py`](kivy_garden/markdownlabel/tests/test_core_functionality_properties.py)
- [`kivy_garden/markdownlabel/tests/test_core_functionality.py`](kivy_garden/markdownlabel/tests/test_core_functionality.py)
- [`kivy_garden/markdownlabel/tests/test_documentation_compliance.py`](kivy_garden/markdownlabel/tests/test_documentation_compliance.py)
- [`kivy_garden/markdownlabel/tests/test_file_analyzer.py`](kivy_garden/markdownlabel/tests/test_file_analyzer.py)
- [`kivy_garden/markdownlabel/tests/test_font_properties.py`](kivy_garden/markdownlabel/tests/test_font_properties.py)
- [`kivy_garden/markdownlabel/tests/test_helper_availability.py`](kivy_garden/markdownlabel/tests/test_helper_availability.py)
- [`kivy_garden/markdownlabel/tests/test_import.py`](kivy_garden/markdownlabel/tests/test_import.py)
- [`kivy_garden/markdownlabel/tests/test_inline_renderer.py`](kivy_garden/markdownlabel/tests/test_inline_renderer.py)
- [`kivy_garden/markdownlabel/tests/test_kivy_renderer.py`](kivy_garden/markdownlabel/tests/test_kivy_renderer.py)
- [`kivy_garden/markdownlabel/tests/test_label_compatibility.py`](kivy_garden/markdownlabel/tests/test_label_compatibility.py)
- [`kivy_garden/markdownlabel/tests/test_padding_properties.py`](kivy_garden/markdownlabel/tests/test_padding_properties.py)
- [`kivy_garden/markdownlabel/tests/test_performance.py`](kivy_garden/markdownlabel/tests/test_performance.py)
- [`kivy_garden/markdownlabel/tests/test_rebuild_scheduling.py`](kivy_garden/markdownlabel/tests/test_rebuild_scheduling.py)
- [`kivy_garden/markdownlabel/tests/test_rebuild_semantics.py`](kivy_garden/markdownlabel/tests/test_rebuild_semantics.py)
- [`kivy_garden/markdownlabel/tests/test_refactoring_properties.py`](kivy_garden/markdownlabel/tests/test_refactoring_properties.py)
- [`kivy_garden/markdownlabel/tests/test_rtl_alignment.py`](kivy_garden/markdownlabel/tests/test_rtl_alignment.py)
- [`kivy_garden/markdownlabel/tests/test_serialization.py`](kivy_garden/markdownlabel/tests/test_serialization.py)
- [`kivy_garden/markdownlabel/tests/test_shared_infrastructure.py`](kivy_garden/markdownlabel/tests/test_shared_infrastructure.py)
- [`kivy_garden/markdownlabel/tests/test_shortening_and_coordinate.py`](kivy_garden/markdownlabel/tests/test_shortening_and_coordinate.py)
- [`kivy_garden/markdownlabel/tests/test_sizing_behavior.py`](kivy_garden/markdownlabel/tests/test_sizing_behavior.py)
- [`kivy_garden/markdownlabel/tests/test_strategy_classification.py`](kivy_garden/markdownlabel/tests/test_strategy_classification.py)
- [`kivy_garden/markdownlabel/tests/test_text_properties.py`](kivy_garden/markdownlabel/tests/test_text_properties.py)
- [`kivy_garden/markdownlabel/tests/test_texture_render_mode.py`](kivy_garden/markdownlabel/tests/test_texture_render_mode.py)
- [`kivy_garden/markdownlabel/tests/test_texture_sizing.py`](kivy_garden/markdownlabel/tests/test_texture_sizing.py)
- [`kivy_garden/markdownlabel/tests/test_utils.py`](kivy_garden/markdownlabel/tests/test_utils.py)

## tools/test_analysis subdirectory:
- [`kivy_garden/markdownlabel/tests/tools/test_analysis/test_assertion_analyzer.py`](kivy_garden/markdownlabel/tests/tools/test_analysis/test_assertion_analyzer.py)
- [`kivy_garden/markdownlabel/tests/tools/test_analysis/test_code_duplication_minimization.py`](kivy_garden/markdownlabel/tests/tools/test_analysis/test_code_duplication_minimization.py)
- [`kivy_garden/markdownlabel/tests/tools/test_analysis/test_coverage_preservation.py`](kivy_garden/markdownlabel/tests/tools/test_analysis/test_coverage_preservation.py)
- [`kivy_garden/markdownlabel/tests/tools/test_analysis/test_duplicate_detector.py`](kivy_garden/markdownlabel/tests/tools/test_analysis/test_duplicate_detector.py)
- [`kivy_garden/markdownlabel/tests/tools/test_analysis/test_naming_convention_validator.py`](kivy_garden/markdownlabel/tests/tools/test_analysis/test_naming_convention_validator.py)
- [`kivy_garden/markdownlabel/tests/tools/test_analysis/test_test_file_parser.py`](kivy_garden/markdownlabel/tests/tools/test_analysis/test_test_file_parser.py)

**Total: 35 test files** (29 in main directory + 6 in tools/test_analysis subdirectory)

---

## Tool Result 3


Subtask 7286c2c9-a82c-4e11-905b-6f6779e932e5 completed.

Result:
I have completed a detailed analysis of [`test_advanced_compatibility.py`](kivy_garden/markdownlabel/tests/test_advanced_compatibility.py:1) against the testing guidelines in [`TESTING.md`](kivy_garden/markdownlabel/tests/TESTING.md:1).

## Summary: 12 Deviations Found

The file generally follows testing guidelines well but has areas for improvement:

### High Priority Deviations:

1. **Test Naming Convention Violations (Lines 161, 185, 481, 511, 540, 570, 631, 659, 686, 712, 738, 776, 799, 825)**: Tests named as "rebuild" tests don't follow the naming convention from lines 102-106 of TESTING.md. Tests verifying rebuild should use `test_*_triggers_rebuild_*`, while tests verifying value changes should use `test_*_updates_value_*`.

2. **Missing Rebuild Verification (Lines 481-506, 511-536, 540-565, 570-592)**: Tests with names suggesting rebuild verification don't actually verify rebuilds occurred. According to lines 217-258 of TESTING.md, proper rebuild testing requires using `collect_widget_ids()` to compare widget IDs before/after changes.

### Medium Priority Deviations:

3. **Missing Module-Level Strategy Documentation (Lines 466-472)**: Module-level strategies (`rebuild_font_names`, `rebuild_colors`, etc.) lack the standardized comment format required by lines 312-395 of TESTING.md.

4. **Missing Strategy Comments (Lines 478, 508, 537, 567, 594)**: Tests using pre-defined strategies lack required comments before `@settings()` decorators.

5. **Incorrect Strategy Classification (Lines 42-43, 59-60, 76-77, 261-262, 274-275, 301-302)**: Tests using constrained `st.text()` are classified as "Complex strategy" when they should be "Medium finite strategy" per lines 353-365 of TESTING.md.

6. **Missing Feature/Property Documentation (Lines 44, 61, 78, 90, 106, 120, 263, 276, 303, 327)**: Property-based test methods lack the standardized docstring format with feature/property information specified in lines 289-304 of TESTING.md.

### Low Priority Deviations:

7. **Missing Pytest Markers (Lines 35, 254, 475)**: Test classes lack appropriate markers like `@pytest.mark.property`.

8. **Unused Imports (Lines 16, 18, 19)**: `BoxLayout`, `Widget`, and `GridLayout` are imported but never used.

9. **Inconsistent `assume()` Usage (Lines 163, 187, 487, 517, 546, 576, 779, 801, 827)**: Pattern of using `assume()` to filter inputs is inconsistent across similar tests.

10. **Missing Documentation for Default Value Tests (Lines 206-246)**: Tests for default values don't reference the property/feature being tested.

### Positive Aspects:

- ✅ Proper file naming follows `test_<feature>[_<subfeature>].py` pattern
- ✅ Well-organized into logical classes with descriptive names
- ✅ Properly imports and uses helpers from test_utils.py
- ✅ Feature/property comments at class level
- ✅ Appropriate `max_examples` values for strategy types
- ✅ Consistent use of `@settings(max_examples=..., deadline=None)`
- ✅ Descriptive assertion messages throughout

The full report above contains specific line numbers, detailed descriptions of each deviation, what the guideline states, and recommendations for fixing each issue.

---

## Tool Result 4


Subtask 97e3c0b7-ff28-4065-b6e7-1738bf4a4121 completed.

Result:
## Analysis Report Complete

I've analyzed [`test_clipping_behavior.py`](kivy_garden/markdownlabel/tests/test_clipping_behavior.py:1) against the guidelines in [`TESTING.md`](kivy_garden/markdownlabel/tests/TESTING.md:1) and found **4 deviations**:

### Deviations Found:

1. **Missing pytest Markers** (Lines 47, 71, 90, 118, 129, 180, 203, 226, 244, 255, 267)
   - Tests lack `@pytest.mark.unit`, `@pytest.mark.property`, or other markers
   - Guideline requires categorizing tests with appropriate markers (lines 148-184)

2. **Duplicated Helper Function** (Lines 18-32, 152-166)
   - `_has_clipping_container` is duplicated in both test classes
   - Guideline requires consolidating helpers in [`test_utils.py`](kivy_garden/markdownlabel/tests/test_utils.py:1) (lines 412-458)

3. **Missing Import from test_utils.py** (Line 10)
   - No imports from `test_utils.py` despite having helper functions
   - Guideline shows standard import pattern (lines 416-431)

4. **Missing Property Documentation Format** (Lines 48, 72, 91, 119, 181, 204, 227, 245)
   - Property test docstrings lack standardized format
   - Guideline requires: `**Feature: feature-name, Property N: Property Description**` and `**Validates: Requirements X.Y**` (lines 288-304)

### Compliant Aspects:
- ✅ Test file structure and organization
- ✅ Test naming conventions (`test_clipping_behavior.py`, `test_<scenario>` methods)
- ✅ Property-based testing practices (`@given`, `@settings`, `max_examples`)
- ✅ Standard Hypothesis strategy comments (`# [Strategy Type] strategy: [N] examples ([Rationale])`)

---

## Tool Result 5


Subtask eb4188f2-7d4b-45eb-91be-ecee1f3fdc0e completed.

Result:
## Test Analysis Report: test_color_properties.py

After analyzing [`test_color_properties.py`](kivy_garden/markdownlabel/tests/test_color_properties.py) against the testing guidelines in [`TESTING.md`](kivy_garden/markdownlabel/tests/TESTING.md), I found **2 deviations**:

---

### Deviation 1: Misleading Docstring for Rebuild Behavior

**Location:** Line 83

**Nature of Deviation:** The docstring for [`test_color_change_updates_value()`](kivy_garden/markdownlabel/tests/test_color_properties.py:82) incorrectly states that changing color triggers a widget rebuild.

```python
def test_color_change_updates_value(self, color1, color2):
    """Changing color triggers widget rebuild with new color."""
```

**Guideline Requirement:** According to the Rebuild Contract section (lines 196-206 in TESTING.md), `color` is classified as a **style-only property** that should update existing widgets **without** triggering a rebuild. The correct naming pattern for tests that verify rebuild behavior is `test_*_triggers_rebuild_*` (lines 104-106), while `test_*_updates_value_*` (lines 110) should only verify value changes.

**What Should Be Done Instead:**
- Change the docstring to accurately reflect that the test verifies value updates without claiming a rebuild occurs:
```python
def test_color_change_updates_value(self, color1, color2):
    """Changing color updates the color value on all internal Labels."""
```

---

### Deviation 2: Missing Feature Documentation in Test Docstrings

**Location:** Lines 35, 50, 65, 83, 106, 122, 138, 156, 169

**Nature of Deviation:** Individual test method docstrings do not follow the standard template format that includes `**Feature:**` and `**Validates:**` tags.

**Current Examples:**
```python
def test_color_applied_to_paragraph(self, color):
    """color is applied to paragraph Labels."""
```

**Guideline Requirement:** The Standard Test File Template (lines 481-502 in TESTING.md) specifies that property-based test docstrings should include feature documentation:

```python
def test_property_holds_universally(self, input_text):
    """Test that [property] holds for all valid inputs.
    
    **Feature: feature-name, Property N: Property Description**
    **Validates: Requirements X.Y**
    """
```

**What Should Be Done Instead:**
Update each test docstring to include the feature documentation tags. For example:

```python
def test_color_applied_to_paragraph(self, color):
    """Test that color is applied to paragraph Labels for all valid color values.
    
    **Feature: label-compatibility, Property 3: Color Forwarding**
    **Validates: Requirements 3.1**
    """
```

**Note:** The file does include a feature comment block at the top (lines 22-26) with this information, but the guidelines suggest it should also be included in individual test docstrings for completeness.

---

## Aspects That Comply with Guidelines

1. **Test file structure and organization** ✓
   - Proper module docstring (lines 1-7)
   - Organized imports (lines 9-19)
   - Single descriptive class `TestColorPropertyForwarding`
   - Feature comment block present (lines 22-26)

2. **Test naming conventions** ✓
   - File name follows `test_<feature>.py` pattern
   - All test methods follow `test_<scenario>` pattern

3. **Use of pytest markers** ✓
   - No markers needed (tests are not slow, don't need window, not meta-tests)

4. **Property-based testing practices** ✓
   - Proper use of `@given` decorator
   - Appropriate `max_examples` values (20 for complex, 50 for combinations)
   - Correct use of `assume()` for filtering invalid inputs (line 84)
   - All strategies imported from test_utils.py

5. **Use of helper functions** ✓
   - `color_strategy` used from test_utils.py
   - `find_labels_recursive` used from test_utils.py
   - `colors_equal` used from test_utils.py

6. **Standard comment formats** ✓
   - All property tests include standardized comments:
     - `# Complex strategy: 20 examples (adequate coverage)`
     - `# Combination strategy: 50 examples (combination coverage)`

7. **Best practices** ✓
   - Descriptive test and class names
   - Related tests grouped in same class
   - Shared helper functions used
   - Both positive and negative cases tested
   - Complex test logic documented

---

## Tool Result 6


Subtask 970976d2-b9bc-4a17-aaa0-96c5625c2f19 completed.

Result:
# Test Compliance Analysis Report: test_comment_format.py

## Summary

After analyzing [`test_comment_format.py`](kivy_garden/markdownlabel/tests/test_comment_format.py) against the testing guidelines in [`TESTING.md`](kivy_garden/markdownlabel/tests/TESTING.md), I found **6 deviations** from the specified best practices.

---

## Detailed Deviations

### Deviation 1: Missing `@pytest.mark.test_tests` Marker

**Line(s):** Entire file (lines 1-736)

**Nature:** The file contains meta-tests that validate the test suite infrastructure (comment format validation, strategy classification, etc.) but is missing the required `@pytest.mark.test_tests` marker.

**Guideline:** According to [`TESTING.md`](kivy_garden/markdownlabel/tests/TESTING.md:162-171):

> Tests that validate the test suite itself must be marked with `@pytest.mark.test_tests`:
> ```python
> @pytest.mark.test_tests
> class TestHelperFunctionAvailability:
>     """Tests that verify helper functions are available and consolidated."""
> ```

**Recommendation:** Add `@pytest.mark.test_tests` decorator to all test classes in the file:
```python
@pytest.mark.test_tests
class TestCommentFormatValidation:
    """Property tests for comment format validation (Property 1)."""
```

---

### Deviation 2: Missing `@pytest.mark.property` Marker

**Line(s):** Multiple property-based tests throughout the file:
- Lines 32-38: [`test_valid_comment_format_compliance`](kivy_garden/markdownlabel/tests/test_comment_format.py:39)
- Lines 58-62: [`test_standard_comment_generation_compliance`](kivy_garden/markdownlabel/tests/test_comment_format.py:63)
- Lines 217-222: [`test_custom_max_examples_require_documentation`](kivy_garden/markdownlabel/tests/test_comment_format.py:223)
- Lines 267-268: [`test_standard_max_examples_require_documentation`](kivy_garden/markdownlabel/tests/test_comment_format.py:269)
- Lines 373-383: [`test_strategy_type_classification_consistency`](kivy_garden/markdownlabel/tests/test_comment_format.py:384)
- Lines 395-399: [`test_boolean_and_small_finite_terminology_consistency`](kivy_garden/markdownlabel/tests/test_comment_format.py:400)
- Lines 534-540: [`test_standardized_comments_are_machine_parseable`](kivy_garden/markdownlabel/tests/test_comment_format.py:541)
- Lines 586-587: [`test_generated_comments_are_machine_parseable`](kivy_garden/markdownlabel/tests/test_comment_format.py:588)

**Nature:** Property-based tests using `@given` and `@settings` are missing the `@pytest.mark.property` marker.

**Guideline:** According to [`TESTING.md`](kivy_garden/markdownlabel/tests/TESTING.md:148-158), pytest markers should be used to categorize tests. While the guidelines don't explicitly show `@pytest.mark.property`, the pattern suggests property-based tests should be appropriately marked.

**Recommendation:** Add `@pytest.mark.property` decorator to all property-based tests:
```python
@pytest.mark.property
@given(
    strategy_type=st.sampled_from([s.value for s in StrategyType]),
    max_examples=st.integers(min_value=1, max_value=1000),
    rationale=st.text(min_size=1, max_size=50, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd', 'Pc', 'Pd', 'Zs')))
)
# Combination strategy: 50 examples (combination coverage)
@settings(max_examples=50, deadline=None)
def test_valid_comment_format_compliance(self, strategy_type, max_examples, rationale):
```

---

### Deviation 3: Repeated `sys.path.insert()` in `setup_method`

**Line(s):** 
- Line 207 (in [`TestCustomValueDocumentation.setup_method`](kivy_garden/markdownlabel/tests/test_comment_format.py:205))
- Line 362 (in [`TestStrategyTypeConsistency.setup_method`](kivy_garden/markdownlabel/tests/test_comment_format.py:360))
- Line 522 (in [`TestMachineReadableFormat.setup_method`](kivy_garden/markdownlabel/tests/test_comment_format.py:520))

**Nature:** `sys.path.insert(0, ...)` is called multiple times in different `setup_method` functions, which is inefficient and a code smell.

**Guideline:** While not explicitly stated in TESTING.md, this is a general best practice violation. Path manipulation should be done once at module level or in `conftest.py`.

**Recommendation:** Move the path insertion to module level (already done at lines 12-13) and remove redundant calls:
```python
# Already at module level (lines 12-13):
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'tools'))

# Remove from setup_method methods
```

---

### Deviation 4: Missing Property Documentation Format in Docstrings

**Line(s):** 
- Lines 299-312: [`test_missing_documentation_reporting`](kivy_garden/markdownlabel/tests/test_comment_format.py:298)
- Lines 330-346: [`test_documentation_with_invalid_format_detection`](kivy_garden/markdownlabel/tests/test_comment_format.py:330)

**Nature:** These tests have docstrings but don't include the property documentation format with "**Feature: feature-name, Property N: Property Description**" and "**Validates: Requirements X.Y**".

**Guideline:** According to [`TESTING.md`](kivy_garden/markdownlabel/tests/TESTING.md:298-301):

```python
def test_property_holds_universally(self, input_text):
    """Test that [property] holds for all valid inputs.
    
    **Feature: feature-name, Property N: Property Description**
    **Validates: Requirements X.Y**
    """
```

**Recommendation:** Add the property documentation format to docstrings:
```python
def test_missing_documentation_reporting(self):
    """Missing documentation is correctly reported with function details.
    
    **Feature: test-comment-standardization, Property 2: Custom Value Documentation**
    **Validates: Requirements 1.1, 4.5**
    """
```

---

### Deviation 5: No Helper Functions Used from test_utils.py

**Line(s):** Entire file

**Nature:** The file does not import or use any helper functions from [`test_utils.py`](kivy_garden/markdownlabel/tests/test_utils.py).

**Guideline:** According to [`TESTING.md`](kivy_garden/markdownlabel/tests/TESTING.md:416-431):

> Always use helper functions from `test_utils.py` instead of duplicating code:
> ```python
> from .test_utils import (
>     find_labels_recursive,
>     collect_widget_ids,
>     colors_equal,
>     padding_equal,
>     floats_equal
> )
> ```

**Recommendation:** While this is a meta-test file and may not need widget traversal helpers, consider using available comparison utilities (`colors_equal`, `padding_equal`, `floats_equal`) if applicable in test assertions.

---

### Deviation 6: Test File Naming Convention

**Line(s):** File name: `test_comment_format.py`

**Nature:** The file name follows the pattern `test_[feature].py`, which is acceptable. However, the file tests infrastructure tools rather than MarkdownLabel functionality directly.

**Guideline:** According to [`TESTING.md`](kivy_garden/markdownlabel/tests/TESTING.md:506-509):

> - `test_[functionality_area].py` - e.g., `test_font_properties.py`
> - Be descriptive about the functionality area

**Recommendation:** The file name is acceptable, but consider whether `test_documentation_compliance.py` (as mentioned in the file organization example at line 39) would be more descriptive since this file tests documentation compliance infrastructure.

---

## Summary of Findings

| # | Deviation | Severity | Line(s) |
|---|-----------|----------|---------|
| 1 | Missing `@pytest.mark.test_tests` marker | High | Entire file |
| 2 | Missing `@pytest.mark.property` marker | Medium | 32-38, 58-62, 217-222, 267-268, 373-383, 395-399, 534-540, 586-587 |
| 3 | Repeated `sys.path.insert()` in setup_method | Low | 207, 362, 522 |
| 4 | Missing property documentation format in docstrings | Low | 299-312, 330-346 |
| 5 | No helper functions used from test_utils.py | Low | Entire file |
| 6 | File naming could be more descriptive | Very Low | File name |

---

## What is Compliant

The following aspects are properly implemented according to the guidelines:

1. ✅ **Test file structure** - Well-organized with logical class groupings
2. ✅ **Test naming conventions** - Methods follow `test_<scenario>` pattern
3. ✅ **Comment format placement** - Comments correctly placed between `@given` and `@settings`
4. ✅ **Strategy classifications** - Uses appropriate strategy type terminology
5. ✅ **max_examples settings** - Properly right-sized based on strategy complexity
6. ✅ **Comment format pattern** - Follows `# [Strategy Type] strategy: [N] examples ([Rationale])` format
7. ✅ **Rationale templates** - Uses standardized rationales for each strategy type
8. ✅ **Class docstrings** - Each class has descriptive docstrings
9. ✅ **Module docstring** - Has clear module-level documentation
10. ✅ **Deadline=None** - All property tests use `deadline=None` to avoid timeouts

---

## Tool Result 7


Subtask 43f61308-6d31-4e4f-a98f-d01aa1a0b241 completed.

Result:
Analysis complete. I found 4 deviations in [`test_comment_standardizer.py`](kivy_garden/markdownlabel/tests/test_comment_standardizer.py) against the testing guidelines in [`TESTING.md`](kivy_garden/markdownlabel/tests/TESTING.md):

## Deviations Found

### 1. Missing `@pytest.mark.test_tests` Marker (Medium Severity)
- **Location:** All test classes (lines 21-1105)
- **Guideline:** Lines 150-158 require `@pytest.mark.test_tests` for meta-tests
- **Fix:** Add `@pytest.mark.test_tests` to all test classes since this file tests test infrastructure tools

### 2. Missing `@pytest.mark.property` Marker (Low Severity)
- **Location:** All property-based test methods (e.g., lines 34-87, 295-360, 583-639, 641-698)
- **Guideline:** Lines 174-184 distinguish unit tests from property-based tests
- **Fix:** Add `@pytest.mark.property` to tests using `@given` decorator

### 3. No Use of Helper Functions from test_utils.py (Low Severity)
- **Location:** Lines 7-19 (imports section)
- **Guideline:** Lines 412-458 require using shared helpers instead of duplicating code
- **Fix:** Import and use available helpers like `find_labels_recursive`, `collect_widget_ids`, `colors_equal`, etc. where applicable

### 4. Overly Complex Test Methods (Low Severity)
- **Location:** Lines 34-87 (54 lines), 295-360 (66 lines), 583-639 (57 lines), 641-698 (58 lines)
- **Guideline:** Lines 624-648 emphasize focused, single-responsibility tests
- **Fix:** Consider breaking down complex tests into smaller helper methods or using parameterized tests

## Positive Compliance
The file correctly follows:
- File naming pattern: `test_<feature>[_<subfeature>].py`
- Test method naming: `test_<scenario>`
- Class organization with descriptive names
- Standard comment format: `# [Strategy Type] strategy: [N] examples ([Rationale])`
- Feature/Property documentation comments where needed
- Appropriate `max_examples` values with justifications

---

## Tool Result 8


Subtask 09eabecb-13e8-4525-9ded-2dd6ed35d2f7 completed.

Result:
# Test Analysis Report: test_core_functionality_properties.py

## Executive Summary

After analyzing [`test_core_functionality_properties.py`](kivy_garden/markdownlabel/tests/test_core_functionality_properties.py) against the testing guidelines in [`TESTING.md`](kivy_garden/markdownlabel/tests/TESTING.md), **NO DEVIATIONS WERE FOUND**. The file is a meta-test file (tests about the test suite structure) and follows the appropriate conventions for its purpose.

---

## Detailed Analysis by Category

### 1. Test File Structure and Organization ✅ COMPLIANT

The file has proper organization:
- Clear module docstring (lines 1-6)
- Properly organized imports (lines 8-13)
- Test classes logically grouped by property being tested
- Descriptive class docstrings
- Related test methods grouped within classes

---

### 2. Test Naming Conventions ✅ COMPLIANT

| Aspect | Guideline Requirement | Actual Implementation | Status |
|--------|----------------------|----------------------|--------|
| File naming | `test_<feature>[_<subfeature>].py` | `test_core_functionality_properties.py` | ✅ |
| Method naming | `test_<scenario>` | All methods follow this pattern | ✅ |
| Class naming | `Test<DescriptiveName>` | All classes follow this pattern | ✅ |

---

### 3. Use of Pytest Markers ✅ COMPLIANT

All test classes are marked with `@pytest.mark.test_tests`, which is **appropriate for meta-tests** (tests that validate the test suite itself).

**Note:** The markers `@pytest.mark.unit`, `@pytest.mark.integration`, and `@pytest.mark.property` mentioned in the task description are **not defined** in the actual [`TESTING.md`](kivy_garden/markdownlabel/tests/TESTING.md). The standard markers are `@pytest.mark.slow`, `@pytest.mark.needs_window`, and `@pytest.mark.test_tests`.

---

### 4. Property-Based Testing Practices ✅ NOT APPLICABLE

This file does **not** use property-based testing with Hypothesis. All tests are either regular unit tests or parametrized tests. This is **not a deviation** because the file's purpose is meta-testing, not testing MarkdownLabel functionality.

---

### 5. Use of Helper Functions from test_utils.py ✅ NOT APPLICABLE

The file does **not** import or use helper functions from [`test_utils.py`](kivy_garden/markdownlabel/tests/test_utils.py). This is **not a deviation** because:
- The helpers in [`test_utils.py`](kivy_garden/markdownlabel/tests/test_utils.py) are designed for testing MarkdownLabel functionality
- This file is a meta-test that validates test suite structure
- The file implements its own helper methods appropriate for meta-testing

---

### 6. Standard Comment Formats for Hypothesis Strategies ✅ NOT APPLICABLE

The file does **not** use Hypothesis strategies or `@settings` decorators, so standard comment formats are not applicable.

---

### 7. Best Practices Review ✅ COMPLIANT

Minor observations (not deviations):
- **Print statements** (lines 654-657): Acceptable for informational meta-test visibility
- **`assert True` no-op** (line 660): Acceptable for informational test that always passes
- **Self-skipping logic**: Appropriate for meta-tests to avoid self-reference issues

---

## Summary Table

| Category | Status | Notes |
|----------|--------|-------|
| Test file structure | ✅ Compliant | Well-organized with clear docstrings |
| Test naming conventions | ✅ Compliant | Follows `test_<feature>[_<subfeature>].py` and `test_<scenario>` patterns |
| Pytest markers | ✅ Compliant | Uses `@pytest.mark.test_tests` appropriately for meta-tests |
| Property-based testing | ✅ N/A | File doesn't use Hypothesis (not a deviation) |
| Helper functions from test_utils.py | ✅ N/A | Meta-tests don't need MarkdownLabel testing helpers |
| Hypothesis strategy comments | ✅ N/A | No Hypothesis strategies used |
| Best practices | ✅ Compliant | Minor observations are acceptable for meta-test context |

---

## Conclusion

**NO DEVIATIONS FOUND.** The file [`test_core_functionality_properties.py`](kivy_garden/markdownlabel/tests/test_core_functionality_properties.py) is a well-structured meta-test file that appropriately follows the testing guidelines defined in [`TESTING.md`](kivy_garden/markdownlabel/tests/TESTING.md) for its specific purpose of validating test suite structure and properties.

---

## Tool Result 9


Subtask f66709e2-c9b8-45f3-b582-2a4768e85d6c completed.

Result:
## Test Compliance Analysis Report: `test_core_functionality.py`

### Summary
After analyzing [`test_core_functionality.py`](kivy_garden/markdownlabel/tests/test_core_functionality.py:1) against the guidelines in [`TESTING.md`](kivy_garden/markdownlabel/tests/TESTING.md:1), **NO DEVIATIONS were found**. The file fully complies with all testing guidelines.

---

### Detailed Analysis by Aspect

#### 1. Test File Structure and Organization ✅
- **Compliant**: The file follows the standard template structure (lines 1-18)
- Proper module docstring describing the purpose
- Imports organized correctly
- Feature/Property documentation blocks used consistently (lines 21-26, 96-100, 193-196, 270-273)
- Tests organized into logical classes, one per property/behavior

#### 2. Test Naming Conventions ✅
- **File naming**: `test_core_functionality.py` follows `test_<feature>[_<subfeature>].py` pattern
- **Method naming**: All test methods follow `test_<scenario>` pattern:
  - [`test_markdown_produces_widgets`](kivy_garden/markdownlabel/tests/test_core_functionality.py:33)
  - [`test_heading_produces_label_widget`](kivy_garden/markdownlabel/tests/test_core_functionality.py:46)
  - [`test_paragraph_produces_label_widget`](kivy_garden/markdownlabel/tests/test_core_functionality.py:63)
  - [`test_multiple_blocks_produce_multiple_widgets`](kivy_garden/markdownlabel/tests/test_core_functionality.py:76)
  - [`test_empty_text_produces_no_widgets`](kivy_garden/markdownlabel/tests/test_core_functionality.py:88)
  - [`test_text_change_updates_widgets`](kivy_garden/markdownlabel/tests/test_core_functionality.py:109)
  - [`test_different_block_counts_update_correctly`](kivy_garden/markdownlabel/tests/test_core_functionality.py:129)
  - [`test_clear_text_removes_widgets`](kivy_garden/markdownlabel/tests/test_core_functionality.py:155)
  - [`test_ast_updates_with_text`](kivy_garden/markdownlabel/tests/test_core_functionality.py:173)
  - [`test_link_produces_ref_markup`](kivy_garden/markdownlabel/tests/test_core_functionality.py:204)
  - [`test_link_url_in_ref_tag`](kivy_garden/markdownlabel/tests/test_core_functionality.py:229)
  - [`test_various_urls_in_links`](kivy_garden/markdownlabel/tests/test_core_functionality.py:250)
  - [`test_nested_lists_render_without_exception`](kivy_garden/markdownlabel/tests/test_core_functionality.py:281)
  - [`test_nested_quotes_render_without_exception`](kivy_garden/markdownlabel/tests/test_core_functionality.py:299)
  - [`test_mixed_nesting_renders_without_exception`](kivy_garden/markdownlabel/tests/test_core_functionality.py:316)
  - [`test_exactly_10_levels_renders_fully`](kivy_garden/markdownlabel/tests/test_core_functionality.py:330)
  - [`test_beyond_10_levels_still_renders`](kivy_garden/markdownlabel/tests/test_core_functionality.py:339)

- **Class naming**: All classes follow descriptive naming pattern:
  - [`TestMarkdownToWidgetTreeGeneration`](kivy_garden/markdownlabel/tests/test_core_functionality.py:27)
  - [`TestMarkdownTextPropertyUpdates`](kivy_garden/markdownlabel/tests/test_core_functionality.py:102)
  - [`TestMarkdownLinkRendering`](kivy_garden/markdownlabel/tests/test_core_functionality.py:198)
  - [`TestMarkdownNestingStability`](kivy_garden/markdownlabel/tests/test_core_functionality.py:275)

#### 3. Pytest Markers ✅
- No inappropriate marker usage found
- The file does not use `@pytest.mark.unit`, `@pytest.mark.integration`, `@pytest.mark.property`, or `@pytest.mark.slow`, which is acceptable as these markers are optional and the guidelines state they should be used "when appropriate"
- The tests are property-based tests that don't require slow test markers

#### 4. Property-Based Testing Practices ✅
- **Hypothesis decorators**: All property tests properly use `@given` with appropriate strategies
- **Strategy classifications**: All custom `max_examples` values have proper comments:
  - Lines 31, 44, 61: `# Complex strategy: 20 examples (adequate coverage)`
  - Line 74: `# Small finite strategy: 5 examples (input space size: 5)`
  - Lines 107, 171: `# Combination strategy: 50 examples (combination coverage)`
  - Lines 127, 153: `# Combination strategy: 9 examples (combination coverage)`
  - Lines 202, 227, 248: `# Complex strategy: 20 examples (adequate coverage)`
  - Lines 279, 297, 314: `# Medium finite strategy: 15 examples (adequate finite coverage)`

- **max_examples settings**: All values are appropriately sized based on strategy type:
  - Small finite strategies (1-5 range): `max_examples=5` (line 75)
  - Small finite strategies (1-3 range): `max_examples=9` for combinations (line 128)
  - Medium finite strategies (1-15 range): `max_examples=15` (lines 280, 298, 315)
  - Complex strategies: `max_examples=20` (multiple locations)
  - Combination strategies: `max_examples=50` (lines 108, 172)

- **Comment format**: All comments follow the standard format `# [Strategy Type] strategy: [N] examples ([Rationale])` as specified in lines 316-321 of TESTING.md

#### 5. Use of Helper Functions from test_utils.py ✅
- Line 16-18: Properly imports helper functions:
  ```python
  from .test_utils import (
      markdown_heading, markdown_paragraph, markdown_link, simple_markdown_document
  )
  ```
- All imported helpers are used appropriately throughout the test file

#### 6. Standard Comment Formats for Hypothesis Strategies ✅
- All property-based tests with custom `max_examples` values include standardized comments
- Comments use correct terminology:
  - "Complex strategy"
  - "Small finite strategy"
  - "Medium finite strategy"
  - "Combination strategy"
- Rationales match the strategy type:
  - "adequate coverage" for complex strategies
  - "input space size: N" for finite strategies
  - "combination coverage" for combination strategies
  - "adequate finite coverage" for medium finite strategies

#### 7. Additional Best Practices ✅
- **Feature/Property documentation**: Each test class includes proper documentation blocks (lines 21-26, 96-100, 193-196, 270-273)
- **Descriptive docstrings**: All test methods have clear docstrings
- **Descriptive assertion messages**: All assertions include helpful context (e.g., line 40-41)
- **assume() usage**: Properly used to filter invalid inputs (lines 35, 111-112, 131, 157, 175)
- **Helper methods**: Private helper methods are well-documented with docstrings (lines 349-395)

---

### Conclusion

**No deviations were found.** The file [`test_core_functionality.py`](kivy_garden/markdownlabel/tests/test_core_functionality.py:1) fully complies with all testing guidelines specified in [`TESTING.md`](kivy_garden/markdownlabel/tests/TESTING.md:1).

---

## Tool Result 10


Subtask 4668b63f-bc37-4e8b-b323-7982cb58b7d1 completed.

Result:
I've completed the analysis of [`test_documentation_compliance.py`](kivy_garden/markdownlabel/tests/test_documentation_compliance.py) against the testing guidelines in [`TESTING.md`](kivy_garden/markdownlabel/tests/TESTING.md).

## Summary

The file is **mostly compliant** with the testing guidelines. Here are the findings:

### ✅ Compliant Aspects
- Test file structure and organization
- Test naming conventions (file: `test_<feature>.py`, methods: `test_<scenario>`)
- Pytest markers (line 14: [`@pytest.mark.test_tests`](kivy_garden/markdownlabel/tests/test_documentation_compliance.py:14) correctly used for meta-tests)
- No need for helper functions from test_utils.py (meta-test file)

### ❌ Deviations Found

| Line | Deviation | Severity | Fix |
|------|-----------|----------|-----|
| 124 | Incorrect strategy type: "Complex" instead of "Medium finite" for `st.integers(min_value=11, max_value=200)` | High | Change to "Medium finite strategy: 20 examples (adequate finite coverage)" |
| 124 | Missing "finite" in rationale template | Medium | Use "adequate finite coverage" instead of "adequate coverage" |
| 139 | Generic rationale could be more specific | Low | Optional: Change to "performance optimized" |

### Required Fixes

**Line 124** - Change:
```python
# Complex strategy: 20 examples (adequate coverage)
```
To:
```python
# Medium finite strategy: 20 examples (adequate finite coverage)
```

This aligns with TESTING.md lines 353-365 which specify medium finite strategies (integer ranges with 11-50 values) should use the format: `Medium finite strategy: [N] examples (adequate finite coverage)`.

The strategy `st.integers(min_value=11, max_value=200)` has an input space of 190 values, qualifying it as a medium finite strategy rather than complex.

---

## Tool Result 11


Subtask 4a8a4961-0547-4fed-a526-367389eaade1 completed.

Result:
# Test File Analysis Report: `test_file_analyzer.py`

## Executive Summary

After analyzing [`test_file_analyzer.py`](kivy_garden/markdownlabel/tests/test_file_analyzer.py) against the guidelines in [`TESTING.md`](kivy_garden/markdownlabel/tests/TESTING.md), I found **5 deviations** from the testing guidelines. The file generally follows good practices but has specific issues with pytest markers, property-based testing conventions, and the use of helper functions.

---

## Detailed Findings

### Deviation 1: Incorrect pytest marker usage

**Line(s):** 25, 87, 228, 290, 328, 399, 465

**Deviation:** The file uses `@pytest.mark.test_tests` marker on test classes, but the guidelines specify that meta-tests (tests about test suite structure) should use this marker. However, the guidelines also list other standard markers that should be used for categorizing tests:

- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.property` - Property-based tests
- `@pytest.mark.slow` - Performance-intensive tests

**Guideline Reference:** [`TESTING.md:148-158`](kivy_garden/markdownlabel/tests/TESTING.md:148-158)

**What Should Be Done Instead:** 
- Use `@pytest.mark.unit` for unit tests that test specific examples and edge cases
- Use `@pytest.mark.integration` for integration tests that test multiple components together
- Use `@pytest.mark.property` for property-based tests using Hypothesis
- Use `@pytest.mark.test_tests` only for meta-tests that validate the test suite itself

**Specific Classes Affected:**
- [`TestFileAnalyzerBasics`](kivy_garden/markdownlabel/tests/test_file_analyzer.py:26) (line 25) - Should use `@pytest.mark.unit`
- [`TestPropertyTestExtraction`](kivy_garden/markdownlabel/tests/test_file_analyzer.py:88) (line 87) - Should use `@pytest.mark.unit`
- [`TestValidationReport`](kivy_garden/markdownlabel/tests/test_file_analyzer.py:229) (line 228) - Should use `@pytest.mark.unit`
- [`TestRationaleGeneration`](kivy_garden/markdownlabel/tests/test_file_analyzer.py:291) (line 290) - Should use `@pytest.mark.property`
- [`TestErrorHandling`](kivy_garden/markdownlabel/tests/test_file_analyzer.py:329) (line 328) - Should use `@pytest.mark.unit`
- [`TestIntegrationWithOptimizationTools`](kivy_garden/markdownlabel/tests/test_file_analyzer.py:400) (line 399) - Should use `@pytest.mark.integration`
- [`TestToolIntegrationCompatibility`](kivy_garden/markdownlabel/tests/test_file_analyzer.py:466) (line 465) - Should use `@pytest.mark.property`

---

### Deviation 2: Property-based test missing standardized comment format

**Line(s):** 298-300

**Deviation:** The property-based test [`test_rationale_generation_for_strategy_types`](kivy_garden/markdownlabel/tests/test_file_analyzer.py:301) uses `st.sampled_from()` strategy with `max_examples=5`, but the comment format does not match the standardized format required by the guidelines.

**Current Code:**
```python
@given(st.sampled_from(['boolean', 'small_finite', 'medium_finite', 'combination', 'complex']))
# Small finite strategy: 5 examples (input space size: 5)
@settings(max_examples=5, deadline=None)
```

**Guideline Reference:** [`TESTING.md:312-395`](kivy_garden/markdownlabel/tests/TESTING.md:312-395)

**What Should Be Done Instead:**
The strategy is actually a `sampled_from` with 5 items, which is a **Small finite strategy**. The comment format is correct for this classification. However, the actual strategy being used (`st.sampled_from`) doesn't match the comment's rationale ("input space size: 5"). The comment should be:

```python
@given(st.sampled_from(['boolean', 'small_finite', 'medium_finite', 'combination', 'complex']))
# Small finite strategy: 5 examples (input space size: 5)
@settings(max_examples=5, deadline=None)
```

This is actually **correct** - the comment format matches the guidelines. No deviation here.

---

### Deviation 3: Property-based test with non-standard strategy classification in comment

**Line(s):** 473-479

**Deviation:** The property-based test [`test_tool_integration_compatibility`](kivy_garden/markdownlabel.py:480) uses a combination strategy but the comment classifies it as "Combination strategy" which is correct. However, the strategy uses `st.sampled_from()` with 5 values and `st.integers()` with range 1-100, which is actually a **Complex strategy** (not a pure combination strategy).

**Current Code:**
```python
@given(
    strategy_type=st.sampled_from(['Boolean', 'Small finite', 'Medium finite', 'Complex', 'Combination']),
    max_examples=st.integers(min_value=1, max_value=100),
    has_comment=st.booleans()
)
# Combination strategy: 20 examples (combination coverage)
@settings(max_examples=20, deadline=None)
```

**Guideline Reference:** [`TESTING.md:367-381`](kivy_garden/markdownlabel/tests/TESTING.md:367-381)

**What Should Be Done Instead:**
The strategy combines `st.sampled_from()` (5 values) × `st.integers(1, 100)` (100 values) × `st.booleans()` (2 values) = 1000 possible combinations. This is a **Complex strategy** because one of the inputs has a large range. The comment should be:

```python
@given(
    strategy_type=st.sampled_from(['Boolean', 'Small finite', 'Medium finite', 'Complex', 'Combination']),
    max_examples=st.integers(min_value=1, max_value=100),
    has_comment=st.booleans()
)
# Complex strategy: 20 examples (adequate coverage)
@settings(max_examples=20, deadline=None)
```

---

### Deviation 4: Missing use of helper functions from test_utils.py

**Line(s):** Throughout the file

**Deviation:** The test file does not import or use any helper functions from [`test_utils.py`](kivy_garden/markdownlabel/tests/test_utils.py). While the tests in this file are testing a different module (FileAnalyzer), the guidelines emphasize using shared helper functions to avoid code duplication.

**Guideline Reference:** [`TESTING.md:412-459`](kivy_garden/markdownlabel/tests/TESTING.md:412-459)

**What Should Be Done Instead:**
The guidelines state: "Always use helper functions from `test_utils.py` instead of duplicating code." While this specific test file doesn't need widget-related helpers (like `find_labels_recursive` or `collect_widget_ids`), it should still import the module and use appropriate helpers if they become relevant. Consider adding:

```python
from .test_utils import (
    # Import relevant helpers if needed
)
```

---

### Deviation 5: Test method naming inconsistency

**Line(s):** 159, 193

**Deviation:** Some test method names include "_file_analyzer" suffix which is redundant given the file name already indicates the component being tested.

**Current Names:**
- [`test_appropriate_examples_not_flagged_file_analyzer`](kivy_garden/markdownlabel/tests/test_file_analyzer.py:159) (line 159)
- [`test_multiline_given_decorator`](kivy_garden/markdownlabel/tests/test_file_analyzer.py:193) (line 193) - this one is fine

**Guideline Reference:** [`TESTING.md:96-147`](kivy_garden/markdownlabel/tests/TESTING.md:96-147)

**What Should Be Done Instead:**
Test method names should accurately reflect what they assert without redundant prefixes. The name should be:

```python
def test_appropriate_examples_not_flagged(self):
    """Appropriate max_examples values are not flagged by file analyzer."""
```

The "_file_analyzer" suffix is redundant since the file is already named `test_file_analyzer.py`.

---

## Summary of Deviations by Category

| Category | Count | Severity |
|----------|-------|----------|
| Pytest Marker Usage | 7 | Medium |
| Property-based Testing | 1 | Low |
| Helper Function Usage | 1 | Low |
| Naming Conventions | 1 | Low |

---

## Compliant Aspects

The following aspects of the test file **comply** with the guidelines:

1. ✅ **File naming convention**: `test_file_analyzer.py` follows the `test_[feature].py` pattern
2. ✅ **Class organization**: Tests are organized into logical classes with descriptive names
3. ✅ **Test method naming**: Most test methods follow the `test_<scenario>` pattern
4. ✅ **Property-based testing structure**: Tests use `@given`, `@settings` decorators correctly
5. ✅ **Documentation**: Docstrings are present and descriptive
6. ✅ **Standard comment format**: Most Hypothesis strategy comments follow the required format

---

## Recommendations

1. **Update pytest markers** to use the appropriate category markers (`@pytest.mark.unit`, `@pytest.mark.integration`, `@pytest.mark.property`)
2. **Review property-based test comments** to ensure strategy classifications match the actual strategies used
3. **Consider using helper functions** from `test_utils.py` if any widget-related testing is added in the future
4. **Remove redundant suffixes** from test method names where the file name already provides context
5. **Add feature documentation comments** to property-based tests following the template in the guidelines (e.g., `**Feature: feature-name, Property N: Property Description**`)

---

## Tool Result 12


Subtask 84d3eb78-b392-4a3e-9cac-4abe7745183d completed.

Result:
## Test File Analysis Report: test_font_properties.py

### Summary
**No deviations found.** The file [`test_font_properties.py`](kivy_garden/markdownlabel/tests/test_font_properties.py) fully complies with all testing guidelines specified in [`TESTING.md`](kivy_garden/markdownlabel/tests/TESTING.md).

---

### Detailed Analysis by Category

#### 1. Test File Structure and Organization ✅

**Guideline:** Tests should be organized by functionality with one class per property/behavior.

**Compliance:**
- **File naming:** `test_font_properties.py` follows the pattern `test_<feature>.py` ✅
- **Class organization:** 5 distinct test classes, each focused on a specific property/behavior:
  - [`TestFontNamePropertyForwarding`](kivy_garden/markdownlabel/tests/test_font_properties.py:35)
  - [`TestLineHeightPropertyForwarding`](kivy_garden/markdownlabel/tests/test_font_properties.py:179)
  - [`TestAdvancedFontPropertyForwarding`](kivy_garden/markdownlabel/tests/test_font_properties.py:308)
  - [`TestFontSizeImmediateUpdates`](kivy_garden/markdownlabel/tests/test_font_properties.py:548)
  - [`TestHeadingScalePreservation`](kivy_garden/markdownlabel/tests/test_font_properties.py:673)
  - [`TestNoRebuildOnFontSizeChange`](kivy_garden/markdownlabel/tests/test_font_properties.py:812)
- **Docstrings:** Each class has a clear docstring indicating what is being tested ✅

---

#### 2. Test Naming Conventions ✅

**Guideline:** Test method names should follow `test_<scenario>` pattern and accurately reflect what they assert.

**Compliance:** All 30 test methods follow proper naming conventions:

| Test Method | Naming Pattern | Assertion Match |
|-------------|----------------|-----------------|
| [`test_font_name_applied_to_paragraph`](kivy_garden/markdownlabel/tests/test_font_properties.py:51) | `test_<property>_applied_to_<element>` | ✅ |
| [`test_code_block_preserves_code_font_name`](kivy_garden/markdownlabel/tests/test_font_properties.py:77) | `test_<element>_preserves_<property>` | ✅ |
| [`test_font_name_change_updates_value`](kivy_garden/markdownlabel/tests/test_font_properties.py:124) | `test_<property>_change_updates_value` | ✅ |
| [`test_line_height_applied_to_heading`](kivy_garden/markdownlabel/tests/test_font_properties.py:200) | `test_<property>_applied_to_<element>` | ✅ |
| [`test_font_family_excluded_from_code_blocks`](kivy_garden/markdownlabel/tests/test_font_properties.py:348) | `test_<property>_excluded_from_<element>` | ✅ |
| [`test_base_font_size_updates_all_labels_immediately`](kivy_garden/markdownlabel/tests/test_font_properties.py:558) | `test_<property>_updates_<target>_immediately` | ✅ |
| [`test_widget_identities_preserved_on_font_size_change`](kivy_garden/markdownlabel/tests/test_font_properties.py:830) | `test_<subject>_preserved_on_<change>` | ✅ |

All method names accurately describe their assertions.

---

#### 3. Pytest Markers ✅

**Guideline:** Use appropriate pytest markers (@pytest.mark.unit, @pytest.mark.integration, @pytest.mark.property, @pytest.mark.slow).

**Compliance:** The file uses `@pytest.mark.parametrize` appropriately for parameterized tests (lines 50, 63, 76, 96, 119, 145, 159, 441). No slow or integration tests are present that would require additional markers.

---

#### 4. Property-Based Testing Practices ✅

**Guideline:** Use @given decorator, strategy classifications, and appropriate max_examples settings.

**Compliance:** All 19 property-based tests follow proper patterns:

| Test | Strategy | max_examples | Comment Format |
|------|----------|--------------|----------------|
| [`test_line_height_applied_to_paragraph`](kivy_garden/markdownlabel/tests/test_font_properties.py:182) | `line_height_strategy` | 20 | ✅ "Complex strategy: 20 examples (adequate coverage)" |
| [`test_line_height_change_updates_value`](kivy_garden/markdownlabel/tests/test_font_properties.py:229) | `line_height_strategy × 2` | 20 | ✅ "Combination strategy: 20 examples (combination coverage)" |
| [`test_font_family_excluded_from_code_blocks`](kivy_garden/markdownlabel/tests/test_font_properties.py:342) | `st.text(...)` | 20 | ✅ "Complex strategy: 20 examples (adequate coverage)" |
| [`test_font_kerning_forwarded_to_all_labels_including_code`](kivy_garden/markdownlabel/tests/test_font_properties.py:462) | `st.booleans()` | 2 | ✅ "Boolean strategy: 2 examples (True/False coverage)" |
| [`test_heading_scale_factors_preserved`](kivy_garden/markdownlabel/tests/test_font_properties.py:676) | `integers × floats` | 6 | ✅ "Combination strategy: 6 examples (combination coverage)" |

**Strategy Classifications Applied Correctly:**
- **Boolean strategy** (2 examples): Used for `st.booleans()` ✅
- **Small finite strategy** (6 examples): Used for heading levels (1-6) ✅
- **Combination strategy** (6-20 examples): Used for multiple strategies combined ✅
- **Complex strategy** (20-50 examples): Used for text/float strategies ✅

---

#### 5. Helper Functions from test_utils.py ✅

**Guideline:** Use shared helper functions instead of duplicating code.

**Compliance:** The file imports and correctly uses:
- [`KIVY_FONTS`](kivy_garden/markdownlabel/tests/test_utils.py:35) - Used in parameterized tests ✅
- [`simple_markdown_document()`](kivy_garden/markdownlabel/tests/test_utils.py:100) - Used for generating test markdown ✅
- [`find_labels_recursive()`](kivy_garden/markdownlabel/tests/test_utils.py:134) - Used extensively for finding Label widgets ✅
- [`floats_equal()`](kivy_garden/markdownlabel/tests/test_utils.py:189) - Used for float comparisons ✅

No duplicate helper function implementations found.

---

#### 6. Standard Comment Formats for Hypothesis Strategies ✅

**Guideline:** All property-based tests with custom max_examples must include standardized comments.

**Compliance:** All 19 property-based tests have properly formatted comments following the pattern:
```python
# [Strategy Type] strategy: [N] examples ([Rationale])
```

Examples:
- Line 183: `# Complex strategy: 20 examples (adequate coverage)`
- Line 230: `# Combination strategy: 20 examples (combination coverage)`
- Line 463: `# Boolean strategy: 2 examples (True/False coverage)`
- Line 680: `# Combination strategy: 6 examples (combination coverage)`
- Line 643: `# Complex strategy: 50 examples (adequate coverage)`

All comments use standardized terminology and rationale templates.

---

#### 7. Feature Documentation Headers ✅

**Guideline:** Each test class should include feature documentation with property number.

**Compliance:** All test classes include proper documentation headers:

```python
# **Feature: label-compatibility, Property 2: font_name Forwarding**
# *For any* Markdown text and any font_name value, all internal Labels SHALL have
# `font_name` set to the specified value, except code blocks which preserve their
# code_font_name setting.
# **Validates: Requirements 2.1**
```

This pattern is consistently applied across all test classes.

---

### Conclusion

The file [`test_font_properties.py`](kivy_garden/markdownlabel/tests/test_font_properties.py) demonstrates excellent adherence to all testing guidelines in [`TESTING.md`](kivy_garden/markdownlabel/tests/TESTING.md). No deviations were found in any of the seven analyzed categories:
1. Test file structure and organization
2. Test naming conventions
3. Pytest marker usage
4. Property-based testing practices
5. Helper function usage
6. Standard comment formats
7. Best practices compliance

The file serves as an excellent example of well-structured, maintainable test code following the project's testing standards.

---

## Tool Result 13


Subtask 8c8f3c76-18d7-47a5-b001-6cdf2072db78 completed.

Result:
Analysis complete. I found **8 deviations** in [`test_helper_availability.py`](kivy_garden/markdownlabel/tests/test_helper_availability.py) related to missing standardized comment format for Hypothesis strategies.

## Key Findings:

**COMPLIANT Areas:**
1. ✅ Test file structure and organization
2. ✅ Test naming conventions (file and method names)
3. ✅ Use of helper functions from test_utils.py

**NON-COMPLIANT Areas:**

### High Priority: Missing Strategy Comments (8 occurrences)

All property-based tests with custom `max_examples` values are missing the required standardized comment format defined in [`TESTING.md`](kivy_garden/markdownlabel/tests/TESTING.md:312-322).

| Line | Test Method | Missing Comment |
|------|-------------|-----------------|
| 33-34 | [`test_widget_traversal_helpers_available`](kivy_garden/markdownlabel/tests/test_helper_availability.py:35) | `# Complex strategy: 10 examples (adequate coverage)` |
| 58-59 | [`test_comparison_helpers_available`](kivy_garden/markdownlabel/tests/test_helper_availability.py:60) | `# Combination strategy: 10 examples (combination coverage)` |
| 73-74 | [`test_padding_comparison_helpers_available`](kivy_garden/markdownlabel/tests/test_helper_availability.py:75) | `# Combination strategy: 10 examples (combination coverage)` |
| 88-90 | [`test_float_comparison_helpers_available`](kivy_garden/markdownlabel/tests/test_helper_availability.py:91) | `# Combination strategy: 10 examples (combination coverage)` |
| 104-105 | [`test_rebuild_detection_helpers_available`](kivy_garden/markdownlabel/tests/test_helper_availability.py:106) | `# Complex strategy: 5 examples (adequate coverage)` |
| 148-149 | Nested test in [`test_hypothesis_strategies_available`](kivy_garden/markdownlabel/tests/test_helper_availability.py:150) | `# Complex strategy: 1 example (minimal validation)` |
| 158-159 | Nested test in [`test_hypothesis_strategies_available`](kivy_garden/markdownlabel/tests/test_helper_availability.py:160) | `# Complex strategy: 1 example (minimal validation)` |
| 168-169 | Nested test in [`test_hypothesis_strategies_available`](kivy_garden/markdownlabel/tests/test_helper_availability.py:170) | `# Complex strategy: 1 example (minimal validation)` |

### Low Priority: Missing Pytest Markers

The file uses `@pytest.mark.test_tests` appropriately but does not use `@pytest.mark.unit`, `@pytest.mark.property`, or `@pytest.mark.slow` markers as suggested in the guidelines.

**Required Fix Format:**
```python
@given(st.text(min_size=1, max_size=50))
# Complex strategy: 10 examples (adequate coverage)
@settings(max_examples=10, deadline=None)
def test_widget_traversal_helpers_available(self, markdown_text):
```

---

## Tool Result 14


Subtask 45dcadbd-a0d7-4d8c-836e-2167c3456a1a completed.

Result:
I've completed the analysis of [`test_import.py`](kivy_garden/markdownlabel/tests/test_import.py:1) against the testing guidelines in [`TESTING.md`](kivy_garden/markdownlabel/tests/TESTING.md:1). The analysis found **3 deviations**:

## Deviation 1: Missing Module Docstring
**Location:** Lines 1-15 (entire file)

The file lacks a module-level docstring. According to lines 464-470 of the guidelines, test files should include a docstring describing what the file covers and listing key areas tested.

**Fix:** Add at the top of the file:
```python
"""
Tests for MarkdownLabel import functionality.

This module contains tests for verifying that MarkdownLabel can be imported
and has the expected basic properties available.
"""
```

## Deviation 2: Missing Test Class Organization
**Location:** Lines 4-15 (test functions at module level)

Tests are defined as module-level functions instead of being organized into logical classes. Lines 43-94 specify that tests should be organized into descriptive classes with related test methods grouped together.

**Fix:** Organize tests into a class:
```python
class TestMarkdownLabelImport:
    """Tests for MarkdownLabel import functionality."""
    
    def test_markdownlabel_import(self):
        # ... existing code ...
    
    def test_markdownlabel_text_property(self):
        # ... existing code ...
```

## Deviation 3: Missing Pytest Markers
**Location:** Lines 4-15 (test functions)

No pytest markers are used to categorize the tests. Lines 149-158 specify that appropriate pytest markers should be used to categorize tests (e.g., `@pytest.mark.slow`, `@pytest.mark.needs_window`, `@pytest.mark.test_tests`).

**Fix:** Add appropriate markers:
```python
@pytest.mark.unit
def test_markdownlabel_import(self):
    # ... existing code ...
```

## Compliant Aspects
- ✅ File naming convention follows `test_<feature>.py` pattern
- ✅ Test method naming follows `test_<scenario>` pattern
- ✅ No property-based testing issues (not applicable)
- ✅ No helper function issues (not applicable for simple tests)
- ✅ No Hypothesis strategy comment issues (not applicable)

The deviations are structural and organizational issues rather than functional problems with the tests themselves.

---

## Tool Result 15


Subtask 9beea301-51ad-4ce9-ae09-899838ad17d2 completed.

Result:
## Analysis Complete: No Deviations Found

The file [`test_inline_renderer.py`](kivy_garden/markdownlabel/tests/test_inline_renderer.py:1) **fully complies** with all testing guidelines in [`TESTING.md`](kivy_garden/markdownlabel/tests/TESTING.md:1).

### Summary of Compliance:

1. **Test File Structure** ✅ - Follows standard template with docstring, imports, strategies, and organized test classes

2. **Naming Conventions** ✅ - File name follows `test_<feature>.py`, methods use `test_<scenario>`, classes use `Test<Feature><Behavior>`

3. **Pytest Markers** ✅ - No unnecessary markers; correctly omits `@pytest.mark.unit`/`@pytest.mark.integration`/`@pytest.mark.property` (not required by guidelines)

4. **Property-Based Testing** ✅ - All tests use `@given`, `@settings(max_examples=...)`, and appropriate strategy classifications

5. **Helper Functions** ✅ - Correctly does not import from test_utils.py (widget traversal helpers are not applicable to token-level InlineRenderer tests)

6. **Comment Formats** ✅ - All property tests include standardized comments: `# Complex strategy: N examples (rationale)`

7. **Best Practices** ✅ - No deviations from documented best practices found

The test file demonstrates exemplary adherence to the project's testing guidelines.

---

## Tool Result 16


Subtask 44bc0239-3a04-4804-afb7-5a4cf032f800 completed.

Result:
# Test File Analysis Report: test_kivy_renderer.py

## Summary

After analyzing [`test_kivy_renderer.py`](kivy_garden/markdownlabel/tests/test_kivy_renderer.py:1) against the testing guidelines in [`TESTING.md`](kivy_garden/markdownlabel/tests/TESTING.md:1), **no deviations were found**. The file follows all testing best practices and conventions.

---

## Detailed Analysis by Category

### 1. Test File Structure and Organization ✅

**Status:** COMPLIANT

The file follows the standard structure defined in the guidelines:
- Module docstring at the top (lines 1-6)
- Imports organized logically (lines 8-19)
- Custom Hypothesis strategies defined before test classes (lines 22-133, 584-651)
- Test classes organized by functionality with descriptive names
- Each test class has a clear docstring indicating the property being tested

### 2. Test Naming Conventions ✅

**Status:** COMPLIANT

**File naming:** `test_kivy_renderer.py` follows the pattern `test_<feature>.py`

**Method naming:** All test methods follow the pattern `test_<scenario>`:
- [`test_smaller_level_has_larger_font`](kivy_garden/markdownlabel/tests/test_kivy_renderer.py:147)
- [`test_heading_returns_label`](kivy_garden/markdownlabel/tests/test_kivy_renderer.py:172)
- [`test_paragraph_has_markup_enabled`](kivy_garden/markdownlabel/tests/test_kivy_renderer.py:222)
- [`test_list_returns_boxlayout`](kivy_garden/markdownlabel/tests/test_kivy_renderer.py:254)
- [`test_code_block_has_monospace_font`](kivy_garden/markdownlabel/tests/test_kivy_renderer.py:391)
- [`test_image_returns_asyncimage`](kivy_garden/markdownlabel/tests/test_kivy_renderer.py:554)
- [`test_table_has_correct_column_count`](kivy_garden/markdownlabel/tests/test_kivy_renderer.py:665)
- [`test_truncation_placeholder_when_nesting_exceeds_max`](kivy_garden/markdownlabel/tests/test_kivy_renderer.py:885)

**Class naming:** All test classes use descriptive names:
- [`TestHeadingFontHierarchy`](kivy_garden/markdownlabel/tests/test_kivy_renderer.py:141)
- [`TestParagraphMarkupEnabled`](kivy_garden/markdownlabel/tests/test_kivy_renderer.py:216)
- [`TestListStructurePreservation`](kivy_garden/markdownlabel/tests/test_kivy_renderer.py:248)
- [`TestCodeBlockStyling`](kivy_garden/markdownlabel/tests/test_kivy_renderer.py:375)
- [`TestTableGridStructure`](kivy_garden/markdownlabel/tests/test_kivy_renderer.py:659)
- [`TestDeepNestingTruncation`](kivy_garden/markdownlabel/tests/test_kivy_renderer.py:882)

### 3. Use of Pytest Markers ✅

**Status:** COMPLIANT

The file uses appropriate pytest markers where applicable:
- [`@pytest.mark.parametrize`](kivy_garden/markdownlabel/tests/test_kivy_renderer.py:444) for parameterized tests
- [`@pytest.mark.parametrize`](kivy_garden/markdownlabel/tests/test_kivy_renderer.py:777) for alignment tests
- [`@pytest.mark.parametrize`](kivy_garden/markdownlabel/tests/test_kivy_renderer.py:847) for invalid alignment tests

Note: The guidelines mention `@pytest.mark.unit`, `@pytest.mark.integration`, `@pytest.mark.property`, `@pytest.mark.slow` as optional markers. The file does not use these specific markers, which is acceptable as they are not mandatory.

### 4. Property-Based Testing Practices ✅

**Status:** COMPLIANT

**Use of `@given` decorator:** All property-based tests correctly use the `@given` decorator.

**Strategy classifications with proper comments:**

| Line | Strategy Type | Comment Format | Status |
|------|---------------|----------------|--------|
| 145 | Small finite | `# Small finite strategy: 5 examples (input space size: 5)` | ✅ |
| 170 | Complex | `# Complex strategy: 20 examples (adequate coverage)` | ✅ |
| 180 | Complex | `# Complex strategy: 20 examples (adequate coverage)` | ✅ |
| 190 | Complex | `# Complex strategy: 10 examples (adequate coverage)` | ✅ |
| 220 | Complex | `# Complex strategy: 20 examples (adequate coverage)` | ✅ |
| 252 | Complex | `# Complex strategy: 20 examples (adequate coverage)` | ✅ |
| 325 | Small finite | `# Small finite strategy: 4 examples (input space size: 4)` | ✅ |
| 379 | Complex | `# Complex strategy: 20 examples (adequate coverage)` | ✅ |
| 431 | Complex | `# Complex strategy: 20 examples (adequate coverage)` | ✅ |
| 511 | Small finite | `# Small finite strategy: 1 examples (input space size: 1)` | ✅ |
| 552 | Complex | `# Complex strategy: 20 examples (adequate coverage)` | ✅ |
| 663 | Combination | `# Combination strategy: 25 examples (combination coverage)` | ✅ |
| 706 | Combination | `# Combination strategy: 25 examples (combination coverage)` | ✅ |
| 748 | Complex | `# Complex strategy: 20 examples (adequate coverage)` | ✅ |
| 794 | Combination | `# Combination strategy: 9 examples (combination coverage)` | ✅ |
| 864 | Complex | `# Complex strategy: 20 examples (adequate coverage)` | ✅ |

**max_examples settings:** All values are appropriately sized based on strategy type:
- Boolean strategies: Not used in this file
- Small finite strategies: Use exact input space size (1, 4, 5)
- Combination strategies: Use product of individual strategy sizes (9, 25)
- Complex strategies: Use moderate values (10, 20) for adequate coverage

### 5. Use of Helper Functions from test_utils.py ✅

**Status:** COMPLIANT

The file defines its own custom strategies (e.g., [`heading_token()`](kivy_garden/markdownlabel/tests/test_kivy_renderer.py:24), [`paragraph_token()`](kivy_garden/markdownlabel/tests/test_kivy_renderer.py:40)) which is appropriate for this test file's specific needs. These are AST token generation strategies, not general-purpose markdown generation strategies.

The general-purpose helper functions from [`test_utils.py`](kivy_garden/markdownlabel/tests/test_utils.py:1) (like `find_labels_recursive`, `collect_widget_ids`, `colors_equal`) are not needed for this file's testing approach, which directly tests the `KivyRenderer` class methods rather than the full `MarkdownLabel` widget tree.

### 6. Standard Comment Formats for Hypothesis Strategies ✅

**Status:** COMPLIANT

All property-based tests with custom `max_examples` values include the standardized comment format:

```python
# [Strategy Type] strategy: [N] examples ([Rationale])
@settings(max_examples=N, deadline=None)
```

Examples found in the file:
- `# Small finite strategy: 5 examples (input space size: 5)` (line 145)
- `# Complex strategy: 20 examples (adequate coverage)` (line 170)
- `# Combination strategy: 25 examples (combination coverage)` (line 663)
- `# Small finite strategy: 1 examples (input space size: 1)` (line 511)

All comments follow the exact format specified in the guidelines.

### 7. Deviations from Best Practices ✅

**Status:** NO DEVIATIONS FOUND

The file follows all best practices outlined in the guidelines:

✅ Uses descriptive test and class names  
✅ Groups related tests in the same class  
✅ Tests both positive and negative cases  
✅ Uses appropriate pytest markers  
✅ Writes property tests for universal behaviors  
✅ Documents complex test logic with docstrings  
✅ Follows standardized comment format for property tests  
✅ Right-sizes max_examples based on strategy type  
✅ Includes property documentation comments (e.g., lines 135-139, 212-214)  
✅ Uses `assume()` to filter invalid inputs (line 194)  
✅ Has module docstring explaining file purpose  

---

## Conclusion

**No deviations were found.** The file [`test_kivy_renderer.py`](kivy_garden/markdownlabel/tests/test_kivy_renderer.py:1) fully complies with all testing guidelines specified in [`TESTING.md`](kivy_garden/markdownlabel/tests/TESTING.md:1). It demonstrates excellent adherence to:

1. File structure and organization
2. Test naming conventions
3. Pytest marker usage
4. Property-based testing best practices
5. Standard comment formats for Hypothesis strategies
6. Overall testing best practices

The file serves as a good example of following the project's testing standards.

---

## Tool Result 17


Subtask 0b8df3e9-a8ed-4872-99d7-635dcf714adf completed.

Result:
# Test File Analysis Report: test_label_compatibility.py

## Summary

The file [`test_label_compatibility.py`](kivy_garden/markdownlabel/tests/test_label_compatibility.py) was analyzed against the testing guidelines in [`TESTING.md`](kivy_garden/markdownlabel/tests/TESTING.md). **No deviations from best practices were found.**

---

## Detailed Analysis by Category

### 1. Test File Structure and Organization ✅

**Status:** COMPLIANT

The file follows the standard test file structure:

- **Module docstring** (lines 1-6): Clear description of what the test file covers
- **Logical grouping**: Tests organized into three distinct classes:
  - [`TestFontSizeAliasBidirectionality`](kivy_garden/markdownlabel/tests/test_label_compatibility.py:23) - Font size alias behavior
  - [`TestNoOpPropertiesAcceptance`](kivy_garden/markdownlabel/tests/test_label_compatibility.py:93) - No-op property acceptance
  - [`TestNoOpPropertyAcceptanceAndStorage`](kivy_garden/markdownlabel/tests/test_label_compatibility.py:237) - No-op property storage
  - [`TestImportFunctionality`](kivy_garden/markdownlabel/tests/test_label_compatibility.py:430) - Import validation

**Guideline Reference:** Section "Test File Structure" (lines 461-510 in TESTING.md)

---

### 2. Test Naming Conventions ✅

**Status:** COMPLIANT

**File naming:** `test_label_compatibility.py` follows pattern `test_<feature>.py`

**Method naming:** All test methods follow the pattern `test_<scenario>` with descriptive names:

| Line | Method Name | Compliance |
|------|-------------|-------------|
| 29 | [`test_font_size_sets_base_font_size`](kivy_garden/markdownlabel/tests/test_label_compatibility.py:29) | ✅ Descriptive |
| 39 | [`test_base_font_size_returns_via_font_size`](kivy_garden/markdownlabel/tests/test_label_compatibility.py:39) | ✅ Descriptive |
| 50 | [`test_font_size_change_updates_base_font_size`](kivy_garden/markdownlabel/tests/test_label_compatibility.py:50) | ✅ Uses `_updates_` pattern |
| 62 | [`test_base_font_size_change_updates_font_size`](kivy_garden/markdownlabel/tests/test_label_compatibility.py:62) | ✅ Uses `_updates_` pattern |
| 99 | [`test_bold_property_accepted`](kivy_garden/markdownlabel/tests/test_label_compatibility.py:99) | ✅ Descriptive |
| 140 | [`test_all_noop_properties_together`](kivy_garden/markdownlabel/tests/test_label_compatibility.py:140) | ✅ Descriptive |
| 187 | [`test_bold_property_change_after_creation`](kivy_garden/markdownlabel/tests/test_label_compatibility.py:187) | ✅ Descriptive |
| 433 | [`test_label_compatibility_imports_resolve`](kivy_garden/markdownlabel/tests/test_label_compatibility.py:433) | ✅ Descriptive |

**Guideline Reference:** Section "Test Naming Conventions" (lines 96-147 in TESTING.md)

---

### 3. Use of Pytest Markers ✅

**Status:** COMPLIANT

Meta-tests are properly marked with `@pytest.mark.test_tests`:

| Line | Class | Marker |
|------|-------|--------|
| 236 | [`TestNoOpPropertyAcceptanceAndStorage`](kivy_garden/markdownlabel/tests/test_label_compatibility.py:236) | `@pytest.mark.test_tests` |
| 429 | [`TestImportFunctionality`](kivy_garden/markdownlabel/tests/test_label_compatibility.py:429) | `@pytest.mark.test_tests` |

These classes contain tests that validate the test suite itself (import functionality), which correctly requires the meta-test marker.

**Guideline Reference:** Section "Test Types and Markers" → "Meta-Test Marking" (lines 160-172 in TESTING.md)

---

### 4. Property-Based Testing Practices ✅

**Status:** COMPLIANT

All property-based tests follow best practices:

#### A. Use of @given decorator
All property tests properly use the `@given` decorator with appropriate strategies.

#### B. Strategy Classifications and max_examples Settings

| Line | Strategy Type | max_examples | Comment Format | Compliance |
|------|--------------|--------------|----------------|------------|
| 26-28 | `st.floats()` (complex) | 50 | `Complex strategy: 50 examples (adequate coverage)` | ✅ |
| 36-38 | `st.floats()` (complex) | 50 | `Complex strategy: 50 examples (adequate coverage)` | ✅ |
| 46-49 | `st.floats()` × 2 (combination) | 50 | `Combination strategy: 50 examples (combination coverage)` | ✅ |
| 58-61 | `st.floats()` × 2 (combination) | 50 | `Combination strategy: 50 examples (combination coverage)` | ✅ |
| 70-72 | `st.floats()` (complex) | 50 | `Complex strategy: 50 examples (adequate coverage)` | ✅ |
| 96-98 | `st.booleans()` (boolean) | 2 | `Boolean strategy: 2 examples (True/False coverage)` | ✅ |
| 105-107 | `st.booleans()` (boolean) | 2 | `Boolean strategy: 2 examples (True/False coverage)` | ✅ |
| 113-115 | `st.booleans()` (boolean) | 2 | `Boolean strategy: 2 examples (True/False coverage)` | ✅ |
| 121-123 | `st.booleans()` (boolean) | 2 | `Boolean strategy: 2 examples (True/False coverage)` | ✅ |
| 129-131 | `st.booleans()` (boolean) | 2 | `Boolean strategy: 2 examples (True/False coverage)` | ✅ |
| 137-139 | `st.booleans()` × 5 (combination) | 2 | `Combination strategy: 2 examples (combination coverage)` | ✅ |
| 156-159 | `st.booleans()` × 5 + custom (combination) | 2 | `Combination strategy: 2 examples (combination coverage)` | ✅ |
| 184-186 | `st.booleans()` (boolean) | 2 | `Boolean strategy: 2 examples (True/False coverage)` | ✅ |
| 240-242 | `st.booleans()` (boolean) | 2 | `Boolean strategy: 2 examples (True/False coverage)` | ✅ |
| 248-250 | `st.floats()` (complex) | 50 | `Complex strategy: 50 examples (adequate coverage)` | ✅ |
| 256-261 | `st.lists()` (complex) | 20 | `Complex strategy: 20 examples (adequate coverage)` | ✅ |
| 268-273 | `st.one_of()` (complex) | 20 | `Complex strategy: 20 examples (adequate coverage)` | ✅ |
| 285-292 | `st.dictionaries()` (complex) | 20 | `Complex strategy: 20 examples (adequate coverage)` | ✅ |
| 298-304 | Multiple strategies (combination) | 50 | `Combination strategy: 50 examples (combination coverage)` | ✅ |
| 326-328 | `st.booleans()` (boolean) | 2 | `Boolean strategy: 2 examples (True/False coverage)` | ✅ |
| 335-337 | `st.floats()` (complex) | 50 | `Complex strategy: 50 examples (adequate coverage)` | ✅ |
| 344-349 | `st.lists()` (complex) | 20 | `Complex strategy: 20 examples (adequate coverage)` | ✅ |
| 356-361 | `st.one_of()` (complex) | 20 | `Complex strategy: 20 examples (adequate coverage)` | ✅ |
| 375-382 | `st.dictionaries()` (complex) | 20 | `Complex strategy: 20 examples (adequate coverage)` | ✅ |
| 389-396 | Multiple strategies + custom (combination) | 2 | `Combination strategy: 2 examples (combination coverage)` | ✅ |

**Guideline Reference:** Section "Property-Based Testing Optimization" (lines 306-411 in TESTING.md)

---

### 5. Use of Helper Functions from test_utils.py ✅

**Status:** COMPLIANT

The file properly imports and uses helper functions:

**Import statement (line 15):**
```python
from .test_utils import simple_markdown_document
```

**Usage in tests:**
- Line 157: [`simple_markdown_document()`](kivy_garden/markdownlabel/tests/test_label_compatibility.py:157) - Used in [`test_noop_properties_do_not_affect_rendering`](kivy_garden/markdownlabel/tests/test_label_compatibility.py:160)
- Line 394: [`simple_markdown_document()`](kivy_garden/markdownlabel/tests/test_label_compatibility.py:394) - Used in [`test_advanced_noop_properties_do_not_affect_rendering`](kivy_garden/markdownlabel/tests/test_label_compatibility.py:397)

**Guideline Reference:** Section "Helper Functions" (lines 412-459 in TESTING.md)

---

### 6. Standard Comment Formats for Hypothesis Strategies ✅

**Status:** COMPLIANT

All custom `max_examples` values include the required standardized comment format:

**Format:** `# [Strategy Type] strategy: [N] examples ([Rationale])`

**Examples from the file:**
- Line 27: `# Complex strategy: 50 examples (adequate coverage)`
- Line 37: `# Complex strategy: 50 examples (adequate coverage)`
- Line 48: `# Combination strategy: 50 examples (combination coverage)`
- Line 97: `# Boolean strategy: 2 examples (True/False coverage)`
- Line 260: `# Complex strategy: 20 examples (adequate coverage)`

All comments use the standardized terminology:
- **Boolean strategy** - for `st.booleans()`
- **Complex strategy** - for `st.floats()`, `st.lists()`, `st.one_of()`, `st.dictionaries()`
- **Combination strategy** - for multiple strategies combined

**Guideline Reference:** Section "Comment Format Requirements" (lines 312-321 in TESTING.md)

---

### 7. Additional Observations ✅

**Feature Comments:** The file includes well-structured feature documentation comments (lines 18-21, 88-91, 230-234, 424-427) following the format:
```python
# **Feature: feature-name, Property N: Property Description**
# *For any* [universal quantification], the system SHALL [behavior].
# **Validates: Requirements X.Y**
```

**Class Docstrings:** All test classes have descriptive docstrings:
- Line 24: `"""Property tests for font_size/base_font_size alias (Property 1)."""`
- Line 94: `"""Property tests for no-op properties acceptance (Property 8)."""`
- Line 238: `"""Property tests for no-op property acceptance and storage (Property 1)."""`
- Line 431: `"""Property test for import functionality (Property 4)."""`

**Test Method Docstrings:** All test methods have clear docstrings explaining what they test.

**Settings Usage:** All property tests use `@settings(max_examples=N, deadline=None)` to avoid timeout issues.

---

## Conclusion

**No deviations from best practices were found.** The file [`test_label_compatibility.py`](kivy_garden/markdownlabel/tests/test_label_compatibility.py) fully complies with all testing guidelines specified in [`TESTING.md`](kivy_garden/markdownlabel/tests/TESTING.md).

The file demonstrates:
- ✅ Proper test file structure and organization
- ✅ Correct test naming conventions
- ✅ Appropriate use of pytest markers
- ✅ Proper property-based testing practices
- ✅ Correct use of helper functions
- ✅ Standardized comment formats for Hypothesis strategies
- ✅ Well-documented test classes and methods

---

## Tool Result 18


Subtask b8430eb4-a18c-49be-afc0-55397092cae9 completed.

Result:
## Analysis Complete: test_padding_properties.py Deviations Report

I have analyzed [`test_padding_properties.py`](kivy_garden/markdownlabel/tests/test_padding_properties.py) against the guidelines in [`TESTING.md`](kivy_garden/markdownlabel/tests/TESTING.md) and found **7 distinct deviations** affecting approximately 30+ lines of code.

---

### Critical Deviation

#### 1. Duplicate Helper Function - `_padding_equal` (Lines 154-158, 298-302, 395-399, 559-563, 637-641, 721-725)

**Nature:** Each test class defines its own private `_padding_equal` method instead of using the imported [`padding_equal`](kivy_garden/markdownlabel/tests/test_utils.py) from [`test_utils.py`](kivy_garden/markdownlabel/tests/test_utils.py:20).

**Guideline:** Section "Helper Functions" states: "Always use helper functions from `test_utils.py` instead of duplicating code"

**Fix:** Remove all 6 duplicate `_padding_equal` method definitions and replace all `self._padding_equal(...)` calls with the imported `padding_equal(...)` function.

---

### Medium Deviations

#### 2. Unused Import - `padding_equal` (Line 20)

**Nature:** [`padding_equal`](kivy_garden/markdownlabel/tests/test_utils.py) is imported but never used because the file uses duplicate local methods instead.

**Fix:** Remove the unused import after fixing deviation #1.

#### 3. Incorrect Strategy Classification - `padding_two` (Line 62-63)

**Nature:** Comment classifies `padding_two` as "Small finite strategy" when it's actually a complex/infinite strategy (uses `st.floats()` which generates continuous values).

**Guideline:** Lines 385-387 define "Complex/Infinite strategies" as including `st.floats()`.

**Fix:** Change to "Complex strategy: 20 examples (adequate coverage)" and increase `max_examples` to 20.

#### 4. Incorrect Strategy Classification - `padding_four` (Multiple locations: 81-82, 95-96, 161-162, 176-177, 207-208, 222-223, 401-402, 428-429, 455-456, 481-482, 523-524, 565-566, 580-581, 595-596, 611-612, 643-644, 688-689, 727-728, 741-742, 752-753)

**Nature:** Comments classify `padding_four` as "Small finite strategy" when it's actually a complex/infinite strategy (uses `st.floats()`).

**Fix:** Change all occurrences to "Complex strategy: 20 examples (adequate coverage)" and increase `max_examples` to 20.

---

### Minor Deviations

#### 5. Orphaned Comment (Line 78)

**Nature:** A comment "# Complex strategy: 20 examples (adequate coverage)" appears between test methods without any associated decorator.

**Fix:** Remove this orphaned comment.

#### 6. Missing Pytest Markers (Lines 276, 789)

**Nature:** Unit tests `test_default_padding_is_zero_for_all_labels` and `test_default_values_synchronized` lack `@pytest.mark.unit` decorator.

**Guideline:** Section "Test Types and Markers" recommends using appropriate pytest markers.

**Fix:** Add `@pytest.mark.unit` decorator to these unit tests.

#### 7. Unused Kivy Widget Imports (Lines 11-14)

**Nature:** `BoxLayout`, `Label`, `Widget`, and `GridLayout` are imported but never used.

**Fix:** Remove these unused imports.

---

### Summary Table

| # | Deviation | Severity | Affected Lines |
|---|-----------|----------|----------------|
| 1 | Duplicate `_padding_equal` methods | Critical | 154-158, 298-302, 395-399, 559-563, 637-641, 721-725 |
| 2 | Unused `padding_equal` import | Medium | 20 |
| 3 | Incorrect `padding_two` classification | Medium | 62-63 |
| 4 | Incorrect `padding_four` classification | Medium | 81-82, 95-96, 161-162, 176-177, 207-208, 222-223, 401-402, 428-429, 455-456, 481-482, 523-524, 565-566, 580-581, 595-596, 611-612, 643-644, 688-689, 727-728, 741-742, 752-753 |
| 5 | Orphaned comment | Minor | 78 |
| 6 | Missing `@pytest.mark.unit` | Low | 276, 789 |
| 7 | Unused widget imports | Low | 11-14 |

**Total: 7 deviations found**

---

## Tool Result 19


Subtask fc1de61f-b27d-4f18-92d3-06edf6bf9728 completed.

Result:
## Detailed Deviation Report for `test_performance.py`

Based on my analysis of [`test_performance.py`](kivy_garden/markdownlabel/tests/test_performance.py:1) against the testing guidelines in [`TESTING.md`](kivy_garden/markdownlabel/tests/TESTING.md:1), I found **one deviation**:

---

### Deviation #1: Duplicated Helper Function Implementation

**Location:** Lines 33-46

**Code:**
```python
def _collect_widget_ids(self, widget):
    """Collect Python object ids of all widgets in the tree.
    
    Args:
        widget: Root widget to collect from
    
    Returns:
        Set of widget object ids
    """
    ids = {id(widget)}
    if hasattr(widget, 'children'):
        for child in widget.children:
            ids.update(self._collect_widget_ids(child))
    return ids
```

**Nature of Deviation:**
The test file implements its own `_collect_widget_ids()` method instead of using the shared `collect_widget_ids()` helper function from [`test_utils.py`](kivy_garden/markdownlabel/tests/test_utils.py:205).

**What the Guideline Says:**
From [`TESTING.md`](kivy_garden/markdownlabel/tests/TESTING.md:412) lines 412-431:

> ### Using Shared Helpers
> Always use helper functions from `test_utils.py` instead of duplicating code:
> ```python
> from .test_utils import (
>     find_labels_recursive,
>     collect_widget_ids,
>     colors_equal,
>     padding_equal,
>     floats_equal
> )
> ```

And from lines 434-438:

> #### Widget Traversal
> - `find_labels_recursive(widget)` - Find all Label widgets in tree
> - `collect_widget_ids(widget)` - Collect widget object IDs for rebuild testing

Additionally, from lines 640-641:

> ❌ **Don't duplicate helper function implementations**

**Impact:**
1. Code duplication violates the DRY principle
2. The custom implementation returns a `set` while `collect_widget_ids()` returns a `dict` (which prevents Python's garbage collector from reusing memory addresses during identity comparison tests - see the docstring in [`test_utils.py`](kivy_garden/markdownlabel/tests/test_utils.py:205) lines 205-211)
3. Makes maintenance harder - changes to rebuild testing logic need to be made in multiple places

**Recommended Fix:**
Replace the custom `_collect_widget_ids()` method with the shared `collect_widget_ids()` helper:

1. Add `collect_widget_ids` to the imports on line 18:
```python
from .test_utils import (
    markdown_heading, markdown_paragraph, markdown_bold, markdown_italic,
    markdown_link, simple_markdown_document, color_strategy, text_padding_strategy,
    find_labels_recursive, colors_equal, padding_equal, floats_equal, KIVY_FONTS,
    collect_widget_ids  # Add this
)
```

2. Remove the `_collect_widget_ids()` method (lines 33-46)

3. Update all usages to use `collect_widget_ids()` instead of `self._collect_widget_ids()`

---

## Summary of Compliance

| Aspect | Status |
|--------|--------|
| Test file structure and organization | ✅ Compliant |
| Test naming conventions (files) | ✅ Compliant (`test_performance.py`) |
| Test naming conventions (methods) | ✅ Compliant (all methods follow `test_<scenario>`) |
| Pytest markers | ✅ Compliant (`@pytest.mark.slow` used appropriately) |
| Property-based testing practices | ✅ Compliant |
| Helper functions usage | ❌ Deviation found (duplicated `_collect_widget_ids`) |
| Standard comment formats | ✅ Compliant (all comments follow `# [Strategy Type] strategy: [N] examples ([Rationale])`) |

---

## Additional Notes

The following aspects are **fully compliant** with the guidelines:

1. **File naming**: `test_performance.py` follows the pattern `test_<feature>.py`
2. **Class naming**: `TestStyleOnlyPropertyUpdates` is descriptive and clear
3. **Method naming**: All test methods follow `test_<scenario>` pattern and accurately reflect what they assert
4. **Pytest markers**: `@pytest.mark.slow` is appropriately applied to the entire class (line 24) since these are performance-intensive tests
5. **Hypothesis strategies**: All `@given` decorators are properly used with appropriate strategies
6. **max_examples settings**: All custom values are properly documented with standardized comments
7. **Comment formats**: Comments like `# Complex strategy: 20 examples (adequate coverage)` (line 50) follow the required format from lines 312-321 of the guidelines
8. **Helper imports**: The file correctly imports and uses `find_labels_recursive`, `colors_equal`, `padding_equal`, `floats_equal`, and strategy helpers from test_utils.py

---

## Tool Result 20


Subtask d1de63ba-78fa-4a4b-93b4-b18681137547 completed.

Result:
## Analysis Report: test_rebuild_scheduling.py vs TESTING.md Guidelines

Based on my analysis of [`test_rebuild_scheduling.py`](kivy_garden/markdownlabel/tests/test_rebuild_scheduling.py:1) against the testing guidelines in [`TESTING.md`](kivy_garden/markdownlabel/tests/TESTING.md:1), I found the following deviations:

---

### Deviations Found

#### 1. Missing pytest Markers for Test Categories

**Location:** Lines 16-134, 136-334 (entire test file)

**Nature of Deviation:** The test classes and methods lack appropriate pytest markers (`@pytest.mark.unit`, `@pytest.mark.integration`, `@pytest.mark.property`, or `@pytest.mark.slow`) to categorize tests as specified in the guidelines.

**Guideline Reference:** [`TESTING.md:148-184`](kivy_garden/markdownlabel/tests/TESTING.md:148) - "Test Types and Markers" section

**What Should Be Done Instead:**
```python
@pytest.mark.property  # or @pytest.mark.unit for non-property tests
class TestBatchedRebuilds:
    """Property tests for batched rebuilds (Property 6)."""
    ...

@pytest.mark.property
class TestDeferredRebuildScheduling:
    """Property tests for deferred rebuild scheduling (Property 7)."""
    ...
```

---

#### 2. Incorrect Strategy Classification Comment

**Location:** Line 65-67

**Nature of Deviation:** The test [`test_mixed_property_changes_batch_rebuilds`](kivy_garden/markdownlabel/tests/test_rebuild_scheduling.py:68) combines multiple strategies (`st.text()`, `st.floats()`, `st.sampled_from()`) but is incorrectly classified as "Small finite strategy" instead of "Combination strategy".

**Guideline Reference:** [`TESTING.md:367-381`](kivy_garden/markdownlabel/tests/TESTING.md:367) - "Combination Strategies" section

**Current Code:**
```python
@given(st.text(...), st.floats(...), st.sampled_from(["Roboto", "RobotoMono-Regular"]))
# Small finite strategy: 2 examples (input space size: 2)  # INCORRECT
@settings(max_examples=2, deadline=None)
def test_mixed_property_changes_batch_rebuilds(self, text, font_size, font_name):
```

**What Should Be Done Instead:**
```python
@given(st.text(...), st.floats(...), st.sampled_from(["Roboto", "RobotoMono-Regular"]))
# Combination strategy: 2 examples (combination coverage)
@settings(max_examples=2, deadline=None)
def test_mixed_property_changes_batch_rebuilds(self, text, font_size, font_name):
```

---

#### 3. Duplicated Rebuild Counting Logic Instead of Using Helper Functions

**Location:** Lines 37-45, 76-84, 268-275, 312-320

**Nature of Deviation:** The file duplicates rebuild counting logic across multiple test methods instead of using the available helper functions from [`test_utils.py`](kivy_garden/markdownlabel/tests/test_utils.py:1) such as `collect_widget_ids`, `assert_rebuild_occurred`, and `assert_no_rebuild`.

**Guideline Reference:** [`TESTING.md:416-431`](kivy_garden/markdownlabel/tests/TESTING.md:416) - "Using Shared Helpers" section

**Current Code (Lines 37-45):**
```python
# Track rebuild calls by patching _rebuild_widgets
rebuild_count = [0]
original_rebuild = label._rebuild_widgets

def counting_rebuild():
    rebuild_count[0] += 1
    original_rebuild()

label._rebuild_widgets = counting_rebuild
```

**What Should Be Done Instead:**
```python
from .test_utils import collect_widget_ids, assert_rebuild_occurred, assert_no_rebuild

# Before changes
ids_before = collect_widget_ids(label, exclude_root=True)

# Make changes...

# Verify rebuild behavior
assert_no_rebuild(label, ids_before)  # or assert_rebuild_occurred(...)
```

---

### Aspects That Comply with Guidelines

1. **Test file structure and organization** ✓ - Proper docstring, imports, and logical class organization
2. **Test naming conventions** ✓ - File name follows `test_<feature>.py` pattern; methods follow `test_<scenario>` pattern
3. **Property-based testing practices** ✓ - Proper use of `@given` and `@settings` decorators
4. **Standard comment formats** ✓ (with the one exception noted above) - Most strategy comments follow the required format

---

### Summary

**3 deviations found:**
1. Missing pytest markers for test categorization (Lines 16-334)
2. Incorrect strategy classification as "Small finite" instead of "Combination" (Line 66)
3. Duplicated rebuild counting logic instead of using helper functions (Lines 37-45, 76-84, 268-275, 312-320)

---

## Tool Result 21


Subtask 3c086a61-5bf1-4ee1-a512-8304e9a04bd3 completed.

Result:
## Test File Analysis Report: test_rebuild_semantics.py

### Summary
The file [`test_rebuild_semantics.py`](kivy_garden/markdownlabel/tests/test_rebuild_semantics.py) **adheres to most testing guidelines** but contains **one minor deviation** related to comment format for Hypothesis strategies.

---

### Detailed Findings

#### ✅ 1. Test File Structure and Organization - **COMPLIANT**

**Status:** No deviations found.

The file follows the standard structure with:
- Module docstring (lines 1-11)
- Imports section (lines 13-23)
- Constants definitions (lines 26-47)
- Test classes organized by functionality

**Classes are well-organized:**
- [`TestWidgetIdentityHelpers`](kivy_garden/markdownlabel/tests/test_rebuild_semantics.py:50) - Tests for helper function
- [`TestStylePropertyIdentityPreservation`](kivy_garden/markdownlabel/tests/test_rebuild_semantics.py:80) - Style property identity preservation tests
- [`TestStylePropertyIdentityPreservationPBT`](kivy_garden/markdownlabel/tests/test_rebuild_semantics.py:272) - Property-based tests for identity preservation
- [`TestStylePropertyPropagation`](kivy_garden/markdownlabel/tests/test_rebuild_semantics.py:362) - Style property propagation tests
- [`TestStylePropertyPropagationPBT`](kivy_garden/markdownlabel/tests/test_rebuild_semantics.py:494) - Property-based tests for propagation
- [`TestStructurePropertyRebuild`](kivy_garden/markdownlabel/tests/test_rebuild_semantics.py:589) - Structure property rebuild tests
- [`TestStructurePropertyRebuildPBT`](kivy_garden/markdownlabel/tests/test_rebuild_semantics.py:763) - Property-based tests for rebuild
- [`TestRootIDPreservationPBT`](kivy_garden/markdownlabel/tests/test_rebuild_semantics.py:915) - Root ID preservation tests

---

#### ✅ 2. Test Naming Conventions - **COMPLIANT**

**Status:** No deviations found.

**File naming:** `test_rebuild_semantics.py` follows the pattern `test_<feature>.py` ✅

**Method naming:** All test methods follow the `test_<scenario>` pattern:
- [`test_collect_widget_ids_includes_root`](kivy_garden/markdownlabel/tests/test_rebuild_semantics.py:53) ✅
- [`test_base_font_size_preserves_widget_ids`](kivy_garden/markdownlabel/tests/test_rebuild_semantics.py:91) ✅
- [`test_text_change_rebuilds_widget_tree`](kivy_garden/markdownlabel/tests/test_rebuild_semantics.py:601) ✅
- [`test_style_property_changes_preserve_widget_identities`](kivy_garden/markdownlabel/tests/test_rebuild_semantics.py:313) ✅

---

#### ✅ 3. Pytest Markers - **COMPLIANT**

**Status:** No deviations found.

The file correctly uses `@pytest.mark.slow` for property-based test classes:
- [`TestStylePropertyIdentityPreservationPBT`](kivy_garden/markdownlabel/tests/test_rebuild_semantics.py:271) - Line 271 ✅
- [`TestStylePropertyPropagationPBT`](kivy_garden/markdownlabel/tests/test_rebuild_semantics.py:493) - Line 493 ✅
- [`TestStructurePropertyRebuildPBT`](kivy_garden/markdownlabel/tests/test_rebuild_semantics.py:762) - Line 762 ✅
- [`TestRootIDPreservationPBT`](kivy_garden/markdownlabel/tests/test_rebuild_semantics.py:914) - Line 914 ✅

Unit test classes do not use markers (appropriate per guidelines).

---

#### ⚠️ 4. Property-Based Testing Practices - **MINOR DEVIATION**

**Status:** One deviation found.

| Line | Deviation | Guideline Requirement |
|------|-----------|----------------------|
| 311 | Comment: `# Complex strategy with many parameters: 100 examples for comprehensive coverage` | Should use standard format: `# [Strategy Type] strategy: [N] examples ([Rationale])` |
| 520 | Comment: `# Complex strategy with many parameters: 100 examples for comprehensive coverage` | Should use standard format: `# [Strategy Type] strategy: [N] examples ([Rationale])` |
| 775 | Comment: `# Complex strategy: 100 examples for comprehensive coverage` | Should use standard format: `# [Strategy Type] strategy: [N] examples ([Rationale])` |
| 822 | Comment: `# Complex strategy: 100 examples for comprehensive coverage` | Should use standard format: `# [Strategy Type] strategy: [N] examples ([Rationale])` |
| 869 | Comment: `# Complex strategy: 100 examples for comprehensive coverage` | Should use standard format: `# [Strategy Type] strategy: [N] examples ([Rationale])` |
| 944 | Comment: `# Complex strategy with many parameters: 100 examples for comprehensive coverage` | Should use standard format: `# [Strategy Type] strategy: [N] examples ([Rationale])` |
| 990 | Comment: `# Complex strategy with many parameters: 100 examples for comprehensive coverage` | Should use standard format: `# [Strategy Type] strategy: [N] examples ([Rationale])` |
| 1047 | Comment: `# Complex strategy with many parameters: 100 examples for comprehensive coverage` | Should use standard format: `# [Strategy Type] strategy: [N] examples ([Rationale])` |

**Guideline Reference (TESTING.md lines 312-322):**
```python
# [Strategy Type] strategy: [N] examples ([Rationale])
@settings(max_examples=N, deadline=None)
def test_example(value):
    pass
```

**Recommended Fix:**
The comments should be standardized to one of these formats based on the strategy type:
- `# Combination strategy: 100 examples (combination coverage)` - for multi-parameter strategies
- `# Complex strategy: 100 examples (adequate coverage)` - for complex strategies
- `# Complex strategy: 100 examples (performance optimized)` - if optimized for performance

---

#### ✅ 5. Use of Helper Functions from test_utils.py - **COMPLIANT**

**Status:** No deviations found.

The file correctly imports and uses helper functions from [`test_utils.py`](kivy_garden/markdownlabel/tests/test_utils.py:1):
- [`simple_markdown_document()`](kivy_garden/markdownlabel/tests/test_rebuild_semantics.py:281) - Used for generating markdown text
- [`color_strategy`](kivy_garden/markdownlabel/tests/test_rebuild_semantics.py:21) - Imported but not used in this file
- [`find_labels_recursive()`](kivy_garden/markdownlabel/tests/test_rebuild_semantics.py:384) - Used for finding Label widgets
- [`colors_equal()`](kivy_garden/markdownlabel/tests/test_rebuild_semantics.py:388) - Used for comparing colors
- [`floats_equal()`](kivy_garden/markdownlabel/tests/test_rebuild_semantics.py:445) - Used for comparing floats
- [`collect_widget_ids()`](kivy_garden/markdownlabel/tests/test_rebuild_semantics.py:56) - Used for rebuild testing

---

#### ✅ 6. Standard Comment Formats for Hypothesis Strategies - **PARTIALLY COMPLIANT**

**Status:** See Section 4 above. The comments exist but use non-standard wording.

**Current Format Used:** `# Complex strategy with many parameters: 100 examples for comprehensive coverage`  
**Standard Format Required:** `# [Strategy Type] strategy: [N] examples ([Rationale])`

---

### Deviation Summary

| Aspect | Status | Deviation Count |
|--------|--------|-----------------|
| Test file structure | ✅ Compliant | 0 |
| Test naming conventions | ✅ Compliant | 0 |
| Pytest markers | ✅ Compliant | 0 |
| Property-based testing practices | ⚠️ Minor deviation | 8 |
| Helper functions usage | ✅ Compliant | 0 |
| Comment formats | ⚠️ Minor deviation | 8 |

### Recommendations

1. **Standardize the 8 comment format deviations** to match the required pattern from TESTING.md:
   - Lines 311, 520, 944, 990, 1047: Change to `# Combination strategy: 100 examples (combination coverage)`
   - Lines 775, 822, 869: Change to `# Complex strategy: 100 examples (adequate coverage)`

2. Consider whether `max_examples=100` is appropriate for all these tests, or if some could be optimized based on strategy complexity (per the "Property-Based Testing Optimization" section in TESTING.md).

### Overall Assessment

The test file demonstrates **excellent adherence** to the testing guidelines with **well-organized structure**, **proper naming conventions**, **appropriate pytest markers**, and **consistent use of helper functions**. The only deviations are minor comment format issues that can be easily corrected using the standardization tools mentioned in the guidelines.

---

## Tool Result 22


Subtask cfe9a8fd-40e5-4587-9c70-fb42e5fe0be4 completed.

Result:
# Analysis Report: test_refactoring_properties.py vs TESTING.md Guidelines

## Executive Summary

After analyzing [`test_refactoring_properties.py`](kivy_garden/markdownlabel/tests/test_refactoring_properties.py:1) against the testing guidelines in [`TESTING.md`](kivy_garden/markdownlabel/tests/TESTING.md:1), I found **no deviations**. The file follows all the specified testing guidelines.

## Detailed Analysis by Category

### 1. Test File Structure and Organization ✅

**Status:** COMPLIANT

The file follows the standard structure outlined in the guidelines:

- **Module docstring** (lines 1-6): Provides a clear description of the module's purpose
- **Feature/Property comments** (lines 19-23, 73-76, 204-208, 370-373, 784-787): Uses the standardized format:
  ```python
  # **Feature: feature-name, Property N: Property Description**
  # *For any* [universal quantification], the system SHALL [behavior].
  # **Validates: Requirements X.Y**
  ```

### 2. Test Naming Conventions ✅

**Status:** COMPLIANT

**File naming:**
- File name [`test_refactoring_properties.py`](kivy_garden/markdownlabel/tests/test_refactoring_properties.py:1) follows the pattern `test_<feature_area>.py` where `refactoring_properties` clearly indicates the functionality being tested (TESTING.md lines 506-509)

**Class naming:**
- All class names use descriptive, specific names following `Test[Property][Behavior]` pattern (TESTING.md lines 144-146):
  - [`TestModuleNamingConsistency`](kivy_garden/markdownlabel/tests/test_refactoring_properties.py:26)
  - [`TestDiscoveryPerformance`](kivy_garden/markdownlabel/tests/test_refactoring_properties.py:79)
  - [`TestRebuildContractEnforcement`](kivy_garden/markdownlabel/tests/test_refactoring_properties.py:211)
  - [`TestTestClassOrganization`](kivy_garden/markdownlabel/tests/test_refactoring_properties.py:376)
  - [`TestMetaTestMarking`](kivy_garden/markdownlabel/tests/test_refactoring_properties.py:790)

**Method naming:**
- All test methods follow `test_<scenario>` pattern (TESTING.md lines 98-138):
  - [`test_module_names_follow_pattern`](kivy_garden/markdownlabel/tests/test_refactoring_properties.py:43)
  - [`test_fast_test_discovery_baseline`](kivy_garden/markdownlabel/tests/test_refactoring_properties.py:82)
  - [`test_rebuild_contract_enforcement`](kivy_garden/markdownlabel/tests/test_refactoring_properties.py:263)
  - [`test_test_classes_have_descriptive_names`](kivy_garden/markdownlabel/tests/test_refactoring_properties.py:610)
  - [`test_meta_test_marking_compliance`](kivy_garden/markdownlabel/tests/test_refactoring_properties.py:868)

### 3. Pytest Markers ✅

**Status:** COMPLIANT

The file correctly uses pytest markers as specified in TESTING.md (lines 150-158):

- **`@pytest.mark.test_tests` marker** is correctly applied to all meta-test classes (lines 25, 78, 210, 375, 789):
  - This marker is required for "tests that validate the test suite itself" (TESTING.md line 162)
  - All classes that test test suite structure are properly marked

The guidelines mention other markers (`@pytest.mark.unit`, `@pytest.mark.integration`, `@pytest.mark.property`, `@pytest.mark.slow`), but these are not required for this specific file which focuses on meta-testing.

### 4. Property-Based Testing Practices ✅

**Status:** COMPLIANT (N/A for this file)

This file does not contain property-based tests using Hypothesis (`@given` decorator). It contains meta-tests that validate the test suite structure itself. Therefore, the property-based testing guidelines (TESTING.md lines 275-410) do not apply to this file.

The file uses:
- **Parametrized tests** with `@pytest.mark.parametrize` (lines 29-42, 119-130) - which is appropriate for testing multiple module names
- **Regular unit tests** for validation logic

### 5. Helper Functions from test_utils.py ✅

**Status:** COMPLIANT

The file correctly imports and uses helper functions from [`test_utils.py`](kivy_garden/markdownlabel/tests/test_utils.py:1) (TESTING.md lines 412-458):

Line 16:
```python
from .test_utils import find_labels_recursive, collect_widget_ids
```

The imported helpers are:
- [`find_labels_recursive`](kivy_garden/markdownlabel/tests/test_utils.py:134) - Widget traversal helper
- [`collect_widget_ids`](kivy_garden/markdownlabel/tests/test_utils.py:205) - Rebuild detection helper

These are the exact helpers mentioned in TESTING.md (lines 436-437).

### 6. Standard Comment Formats for Hypothesis Strategies ✅

**Status:** COMPLIANT (N/A for this file)

Since this file does not contain property-based tests with custom `max_examples` values, the comment format requirements (TESTING.md lines 312-410) do not apply.

### 7. Best Practices Compliance ✅

**Status:** COMPLIANT

The file follows all best practices from TESTING.md (lines 623-649):

✅ **Uses descriptive test and class names** - All names clearly indicate what is being tested
✅ **Groups related tests in the same class** - Each class focuses on a specific property/behavior
✅ **Uses shared helper functions from test_utils.py** - Imports and uses available helpers
✅ **Uses appropriate pytest markers** - All meta-tests marked with `@pytest.mark.test_tests`
✅ **Documents complex test logic** - Helper methods have clear docstrings (lines 214-233, 234-261, etc.)
✅ **Test names accurately reflect what they assert** - Method names match their assertions

### Additional Observations

The file demonstrates good practices beyond the guidelines:

1. **Helper methods for test logic**: The file defines private helper methods (e.g., [`_has_rebuild_verification`](kivy_garden/markdownlabel/tests/test_refactoring_properties.py:214), [`_extract_test_method`](kivy_garden/markdownlabel/tests/test_refactoring_properties.py:234)) to keep test methods clean and maintainable

2. **Self-validating tests**: The file includes tests that validate its own detection patterns (e.g., [`test_rebuild_verification_patterns_work`](kivy_garden/markdownlabel/tests/test_refactoring_properties.py:316), [`test_meta_test_detection_patterns_work`](kivy_garden/markdownlabel/tests/test_refactoring_properties.py:934))

3. **Comprehensive docstrings**: Each test class and method has clear docstrings explaining the purpose and validation criteria

## Conclusion

**No deviations found.** The file [`test_refactoring_properties.py`](kivy_garden/markdownlabel/tests/test_refactoring_properties.py:1) fully complies with all testing guidelines specified in [`TESTING.md`](kivy_garden/markdownlabel/tests/TESTING.md:1). The file is well-structured, follows naming conventions, uses appropriate markers, imports helper functions correctly, and adheres to all documented best practices.

---

## Tool Result 23


Subtask 24345937-c784-46de-89c6-01bb76376d45 completed.

Result:
## Analysis Complete: test_rtl_alignment.py vs TESTING.md Guidelines

### Summary
The file [`test_rtl_alignment.py`](kivy_garden/markdownlabel/tests/test_rtl_alignment.py) is **mostly compliant** with the testing guidelines, with **one significant deviation** regarding pytest markers.

### Deviations Found

#### ❌ Deviation #1: Missing Pytest Markers
**Location:** All test methods (lines 29-519)

**Nature:** The file lacks pytest markers (`@pytest.mark.unit`, `@pytest.mark.property`, `@pytest.mark.needs_window`) required by lines 148-172 of [`TESTING.md`](kivy_garden/markdownlabel/tests/TESTING.md:148-172).

**Guideline Requirement:** Tests must be categorized with appropriate markers such as `@pytest.mark.unit`, `@pytest.mark.property`, `@pytest.mark.slow`, or `@pytest.mark.needs_window`.

**What Should Be Done Instead:**
- Add `@pytest.mark.unit` to parametrized unit tests (lines 29-47, 49-68, 124-147, 149-172)
- Add `@pytest.mark.property` to all property-based tests with `@given` decorator (all other test methods)
- Add `@pytest.mark.needs_window` to all tests since they create Kivy widgets

### Compliant Aspects ✅

1. **Test file structure** - Follows standard template with docstrings, imports, and feature comments
2. **Test naming conventions** - All names accurately reflect what they assert (e.g., `test_direction_change_preserves_widget_identities`)
3. **Property-based testing** - Proper use of `@given`, strategy classifications, and appropriate `max_examples` settings
4. **Helper functions** - Correctly uses `find_labels_recursive` and `collect_widget_ids` from [`test_utils.py`](kivy_garden/markdownlabel/tests/test_utils.py:1)
5. **Standard comment formats** - All Hypothesis strategy comments follow the format: `# [Strategy Type] strategy: [N] examples ([Rationale])`
6. **Documentation** - Feature/Property/Requirements tags included in docstrings

### Recommendation
Add pytest markers to all test methods to achieve full compliance with the testing guidelines.

---

## Tool Result 24


Subtask 8f3551ec-f91f-48d9-b282-1fa2023ec858 completed.

Result:
# Analysis Report: test_serialization.py vs TESTING.md Guidelines

## Summary
**No deviations found.** The file [`test_serialization.py`](kivy_garden/markdownlabel/tests/test_serialization.py) follows all the testing guidelines specified in [`TESTING.md`](kivy_garden/markdownlabel/tests/TESTING.md).

---

## Detailed Analysis by Category

### 1. Test File Structure and Organization ✅

**Guideline:** Tests should be organized by functionality with descriptive class names.

**Compliance:**
- **Line 24-314**: [`TestMarkdownRoundTripSerialization`](kivy_garden/markdownlabel/tests/test_serialization.py:24) - Clear class name indicating round-trip serialization tests
- **Line 317-438**: [`TestCodeBlockSerialization`](kivy_garden/markdownlabel/tests/test_serialization.py:317) - Clear class name for code block serialization edge cases
- **Line 440-556**: [`TestCodeFenceCollisionProperty`](kivy_garden/markdownlabel/tests/test_serialization.py:440) - Clear class name for property-based tests on fence collision handling

All classes have descriptive docstrings explaining their purpose.

---

### 2. Test Naming Conventions ✅

**Guideline:** Test methods should follow pattern `test_<scenario>` and accurately reflect what they assert.

**Compliance:** All test methods follow the naming convention:

- [`test_heading_round_trip`](kivy_garden/markdownlabel/tests/test_serialization.py:118) - Tests heading round-trip behavior
- [`test_paragraph_round_trip`](kivy_garden/markdownlabel/tests/test_serialization.py:137) - Tests paragraph round-trip behavior
- [`test_bold_round_trip`](kivy_garden/markdownlabel/tests/test_serialization.py:161) - Tests bold text round-trip behavior
- [`test_italic_round_trip`](kivy_garden/markdownlabel/tests/test_serialization.py:177) - Tests italic text round-trip behavior
- [`test_link_round_trip`](kivy_garden/markdownlabel/tests/test_serialization.py:193) - Tests link round-trip behavior
- [`test_document_round_trip`](kivy_garden/markdownlabel/tests/test_serialization.py:209) - Tests full document round-trip behavior
- [`test_code_block_round_trip`](kivy_garden/markdownlabel/tests/test_serialization.py:226) - Tests code block round-trip behavior
- [`test_list_round_trip`](kivy_garden/markdownlabel/tests/test_serialization.py:241) - Tests list round-trip behavior
- [`test_ordered_list_round_trip`](kivy_garden/markdownlabel/tests/test_serialization.py:256) - Tests ordered list round-trip behavior
- [`test_block_quote_round_trip`](kivy_garden/markdownlabel/tests/test_serialization.py:271) - Tests block quote round-trip behavior
- [`test_thematic_break_round_trip`](kivy_garden/markdownlabel/tests/test_serialization.py:286) - Tests thematic break round-trip behavior
- [`test_table_round_trip`](kivy_garden/markdownlabel/tests/test_serialization.py:301) - Tests table round-trip behavior
- [`test_code_with_backticks`](kivy_garden/markdownlabel/tests/test_serialization.py:320) - Tests code with backticks handling
- [`test_code_with_four_backticks`](kivy_garden/markdownlabel/tests/test_serialization.py:342) - Tests code with four backticks handling
- [`test_code_only_backticks`](kivy_garden/markdownlabel/tests/test_serialization.py:353) - Tests code containing only backticks
- [`test_empty_code_block`](kivy_garden/markdownlabel/tests/test_serialization.py:375) - Tests empty code block serialization
- [`test_code_with_language_and_backticks`](kivy_garden/markdownlabel/tests/test_serialization.py:394) - Tests code with language info and backticks
- [`test_code_with_mixed_backtick_lengths`](kivy_garden/markdownlabel/tests/test_serialization.py:415) - Tests code with various backtick lengths
- [`test_fence_collision_handling_property`](kivy_garden/markdownlabel/tests/test_serialization.py:446) - Tests fence collision handling property
- [`test_code_serialization_round_trip_property`](kivy_garden/markdownlabel/tests/test_serialization.py:507) - Tests code serialization round-trip property

---

### 3. Pytest Markers ✅

**Guideline:** Use appropriate pytest markers (@pytest.mark.unit, @pytest.mark.integration, @pytest.mark.property, @pytest.mark.slow).

**Analysis:** The file does not use pytest markers, which is acceptable because:
1. The guidelines state markers are optional for categorization
2. The test file structure (class organization) already provides clear categorization
3. No slow tests or tests requiring special environments are present that would need `@pytest.mark.slow` or `@pytest.mark.needs_window`

---

### 4. Property-Based Testing Practices ✅

**Guideline:** Use @given decorator, appropriate strategy classifications, and max_examples settings with standardized comments.

**Compliance:** All property-based tests follow the required format:

| Test Method | Strategy | Comment Format | max_examples |
|-------------|----------|----------------|--------------|
| [`test_heading_round_trip`](kivy_garden/markdownlabel/tests/test_serialization.py:115-117) | `markdown_heading()` | `# Complex strategy: 20 examples (adequate coverage)` | 20 |
| [`test_paragraph_round_trip`](kivy_garden/markdownlabel/tests/test_serialization.py:134-136) | `markdown_paragraph()` | `# Complex strategy: 20 examples (adequate coverage)` | 20 |
| [`test_bold_round_trip`](kivy_garden/markdownlabel/tests/test_serialization.py:158-160) | `markdown_bold()` | `# Complex strategy: 20 examples (adequate coverage)` | 20 |
| [`test_italic_round_trip`](kivy_garden/markdownlabel/tests/test_serialization.py:174-176) | `markdown_italic()` | `# Complex strategy: 20 examples (adequate coverage)` | 20 |
| [`test_link_round_trip`](kivy_garden/markdownlabel/tests/test_serialization.py:190-192) | `markdown_link()` | `# Complex strategy: 20 examples (adequate coverage)` | 20 |
| [`test_document_round_trip`](kivy_garden/markdownlabel/tests/test_serialization.py:206-208) | `simple_markdown_document()` | `# Complex strategy: 20 examples (adequate coverage)` | 20 |
| [`test_fence_collision_handling_property`](kivy_garden/markdownlabel/tests/test_serialization.py:443-445) | `st.text(min_size=0, max_size=200)` | `# Complex strategy: 30 examples (adequate coverage)` | 30 |
| [`test_code_serialization_round_trip_property`](kivy_garden/markdownlabel/tests/test_serialization.py:504-506) | `st.text()`, `st.text(...)` | `# Complex strategy: 20 examples (adequate coverage)` | 20 |

All comments follow the standard format: `# [Strategy Type] strategy: [N] examples ([Rationale])`

---

### 5. Use of Helper Functions from test_utils.py ✅

**Guideline:** Always use helper functions from test_utils.py instead of duplicating code.

**Compliance:**
- **Lines 14-21**: Properly imports helper functions from [`test_utils.py`](kivy_garden/markdownlabel/tests/test_utils.py):
  - [`markdown_heading()`](kivy_garden/markdownlabel/tests/test_serialization.py:15)
  - [`markdown_paragraph()`](kivy_garden/markdownlabel/tests/test_serialization.py:16)
  - [`markdown_bold()`](kivy_garden/markdownlabel/tests/test_serialization.py:17)
  - [`markdown_italic()`](kivy_garden/markdownlabel/tests/test_serialization.py:18)
  - [`markdown_link()`](kivy_garden/markdownlabel/tests/test_serialization.py:19)
  - [`simple_markdown_document()`](kivy_garden/markdownlabel/tests/test_serialization.py:20)

The file also defines its own internal helper methods ([`_normalize_ast()`](kivy_garden/markdownlabel/tests/test_serialization.py:27) and [`_merge_adjacent_text()`](kivy_garden/markdownlabel/tests/test_serialization.py:74)) which are specific to the serialization testing needs and appropriately scoped within the test class.

---

### 6. Standard Comment Formats for Hypothesis Strategies ✅

**Guideline:** All property-based tests with custom max_examples must include standardized comments.

**Compliance:** All property-based tests have properly formatted comments following the pattern:
- Format: `# [Strategy Type] strategy: [N] examples ([Rationale])`
- Strategy types used: "Complex strategy" (appropriate for text-based infinite strategies)
- Rationales: "adequate coverage" (appropriate for complex strategies)

Examples:
- **Line 116**: `# Complex strategy: 20 examples (adequate coverage)`
- **Line 135**: `# Complex strategy: 20 examples (adequate coverage)`
- **Line 159**: `# Complex strategy: 20 examples (adequate coverage)`
- **Line 175**: `# Complex strategy: 20 examples (adequate coverage)`
- **Line 191**: `# Complex strategy: 20 examples (adequate coverage)`
- **Line 207**: `# Complex strategy: 20 examples (adequate coverage)`
- **Line 444**: `# Complex strategy: 30 examples (adequate coverage)`
- **Line 505**: `# Complex strategy: 20 examples (adequate coverage)`

---

### 7. Additional Observations

**Minor Issue (Not a deviation from guidelines):**
- **Line 156**: There is a duplicate comment `# Complex strategy: 20 examples (adequate coverage)` that appears to be orphaned (no associated @given decorator). This appears to be a copy-paste artifact but does not violate any specific guideline in TESTING.md. It could be cleaned up for code clarity, but it's not a formal deviation.

---

## Conclusion

The file [`test_serialization.py`](kivy_garden/markdownlabel/tests/test_serialization.py) demonstrates excellent adherence to all testing guidelines in [`TESTING.md`](kivy_garden/markdownlabel/tests/TESTING.md). It properly:

1. ✅ Organizes tests by functionality with descriptive class names
2. ✅ Follows the `test_<scenario>` naming convention
3. ✅ Uses appropriate pytest markers (or appropriately omits them when not needed)
4. ✅ Implements property-based testing with proper @given decorators, strategy classifications, and max_examples settings
5. ✅ Uses helper functions from test_utils.py
6. ✅ Follows standard comment formats for Hypothesis strategies

No deviations from the testing guidelines were found.

---

## Tool Result 25


Subtask ea62087e-b2bf-43b9-ab74-d527e1de94b8 completed.

Result:
# Test Analysis Report: test_shared_infrastructure.py

## Executive Summary

After analyzing [`test_shared_infrastructure.py`](kivy_garden/markdownlabel/tests/test_shared_infrastructure.py) against the testing guidelines in [`TESTING.md`](kivy_garden/markdownlabel/tests/TESTING.md), I found **no deviations** from the best practices. The file is well-structured and follows all guidelines correctly.

---

## Detailed Analysis by Category

### 1. Test File Structure and Organization ✅

**Status: COMPLIANT**

The file follows the standard structure template:

- **Lines 1-6**: Module docstring provides clear description of what the file covers
- **Lines 8-26**: Proper imports organized logically (pytest, hypothesis, project imports, test_utils imports)
- **Lines 29-152**: First test class (`TestSharedStrategyAvailability`)
- **Lines 154-219**: Second test class (`TestSharedInfrastructureHelpers`)

**Guideline Reference**: Lines 462-502 in TESTING.md (Standard Test File Template)

---

### 2. Test Naming Conventions ✅

**Status: COMPLIANT**

**File Naming**: `test_shared_infrastructure.py` follows the pattern `test_<feature>.py`

**Class Naming**:
- Line 30: `TestSharedStrategyAvailability` - Descriptive, follows `Test[Component][Functionality]` pattern
- Line 155: `TestSharedInfrastructureHelpers` - Descriptive, follows `Test[Component][Functionality]` pattern

**Method Naming**: All test methods follow `test_<scenario>` pattern:
- Line 36: `test_markdown_heading_strategy_generates_valid_headings`
- Line 53: `test_markdown_paragraph_strategy_generates_valid_paragraphs`
- Line 65: `test_markdown_bold_strategy_generates_valid_bold_text`
- Line 74: `test_markdown_italic_strategy_generates_valid_italic_text`
- Line 85: `test_markdown_link_strategy_generates_valid_links`
- Line 98: `test_simple_markdown_document_strategy_generates_valid_documents`
- Line 110: `test_color_strategy_generates_valid_colors`
- Line 125: `test_text_padding_strategy_generates_valid_padding`
- Line 137: `test_kivy_fonts_constant_available`
- Line 161: `test_find_labels_recursive_function_available`
- Line 181: `test_colors_equal_function_available`
- Line 195: `test_padding_equal_function_available`
- Line 209: `test_floats_equal_function_available`

**Guideline Reference**: Lines 96-147 in TESTING.md (Test Naming Conventions)

---

### 3. Pytest Markers ✅

**Status: COMPLIANT**

Both test classes are properly marked with `@pytest.mark.test_tests`:
- Line 29: `@pytest.mark.test_tests` for `TestSharedStrategyAvailability`
- Line 154: `@pytest.mark.test_tests` for `TestSharedInfrastructureHelpers`

This is correct because these are meta-tests that validate the test suite itself.

**Guideline Reference**: Lines 150-172 in TESTING.md (Test Types and Markers)

---

### 4. Property-Based Testing Practices ✅

**Status: COMPLIANT**

All property-based tests properly use Hypothesis decorators:

| Line | Decorator | Strategy Type | Max Examples | Comment Format |
|------|-----------|---------------|--------------|----------------|
| 33 | `@given(markdown_heading())` | Complex | 20 | Line 34: `# Complex strategy: 20 examples (adequate coverage)` |
| 50 | `@given(markdown_paragraph())` | Complex | 20 | Line 51: `# Complex strategy: 20 examples (adequate coverage)` |
| 62 | `@given(markdown_bold())` | Complex | 20 | Line 63: `# Complex strategy: 20 examples (adequate coverage)` |
| 71 | `@given(markdown_italic())` | Complex | 20 | Line 72: `# Complex strategy: 20 examples (adequate coverage)` |
| 82 | `@given(markdown_link())` | Complex | 20 | Line 83: `# Complex strategy: 20 examples (adequate coverage)` |
| 95 | `@given(simple_markdown_document())` | Complex | 20 | Line 96: `# Complex strategy: 20 examples (adequate coverage)` |
| 107 | `@given(color_strategy)` | Complex | 20 | Line 108: `# Complex strategy: 20 examples (adequate coverage)` |
| 122 | `@given(text_padding_strategy)` | Complex | 20 | Line 123: `# Complex strategy: 20 examples (adequate coverage)` |
| 158 | `@given(st.text(min_size=1, max_size=50))` | Complex | 50 | Line 159: `# Complex strategy: 50 examples (adequate coverage)` |
| 178 | `@given(color_strategy, color_strategy)` | Combination | 50 | Line 179: `# Combination strategy: 50 examples (combination coverage)` |
| 192 | `@given(text_padding_strategy, text_padding_strategy)` | Combination | 50 | Line 193: `# Combination strategy: 50 examples (combination coverage)` |
| 205-206 | `@given(st.floats(...), st.floats(...))` | Combination | 20 | Line 207: `# Combination strategy: 20 examples (combination coverage)` |

All comments follow the required format: `# [Strategy Type] strategy: [N] examples ([Rationale])`

**Guideline Reference**: Lines 275-411 in TESTING.md (Property-Based Testing and Optimization)

---

### 5. Use of Helper Functions from test_utils.py ✅

**Status: COMPLIANT**

All required helper functions are properly imported from `test_utils.py` (lines 12-26):
- `markdown_heading`, `markdown_paragraph`, `markdown_bold`, `markdown_italic`, `markdown_link`
- `simple_markdown_document`
- `color_strategy`, `text_padding_strategy`
- `find_labels_recursive`
- `colors_equal`, `padding_equal`, `floats_equal`
- `KIVY_FONTS`

These helpers are used throughout the tests instead of duplicating code.

**Guideline Reference**: Lines 412-459 in TESTING.md (Helper Functions)

---

### 6. Standard Comment Formats for Hypothesis Strategies ✅

**Status: COMPLIANT**

All property-based tests with custom `max_examples` values include standardized comments in the correct format:

**Complex Strategy Comments** (Lines 34, 51, 63, 72, 83, 96, 108, 123, 159):
```
# Complex strategy: [N] examples (adequate coverage)
```

**Combination Strategy Comments** (Lines 179, 193, 207):
```
# Combination strategy: [N] examples (combination coverage)
```

All comments are placed immediately before the `@settings` decorator, as required.

**Guideline Reference**: Lines 312-395 in TESTING.md (Comment Format Requirements and Strategy Classifications)

---

### 7. Test Documentation ✅

**Status: COMPLIANT**

Property tests include proper docstrings with feature/property tags where applicable:
- Line 37-41: `**Feature: test-refactoring, Property 6: Shared Strategy Availability**` with `**Validates: Requirements 3.2**`
- Line 162-166: `**Feature: test-refactoring, Property 7: Helper Function Consolidation**` with `**Validates: Requirements 3.3**`

Unit tests have clear, descriptive docstrings (e.g., lines 54, 66, 75, 86, 99, 111, 126, 138, 182, 196, 210).

**Guideline Reference**: Lines 288-304 in TESTING.md (Property Test Structure)

---

## Conclusion

**No deviations found.** The file [`test_shared_infrastructure.py`](kivy_garden/markdownlabel/tests/test_shared_infrastructure.py) is fully compliant with all testing guidelines specified in [`TESTING.md`](kivy_garden/markdownlabel/tests/TESTING.md). It demonstrates excellent adherence to:

- Proper file and test naming conventions
- Correct use of pytest markers
- Appropriate property-based testing practices with Hypothesis
- Standardized comment formats for strategy classifications
- Consistent use of shared helper functions
- Clear documentation and organization

---

## Tool Result 26


Subtask 464952f6-2ff5-404c-9165-9b6d024d7b17 completed.

Result:
## Test File Analysis Report: `test_shortening_and_coordinate.py`

### Executive Summary
The test file generally follows the testing guidelines well. **1 deviation** was found related to unused imports.

---

### Detailed Analysis by Category

#### 1. Test File Structure and Organization ✅ **COMPLIANT**

The file follows the standard structure correctly with proper module docstring, feature documentation comments, and logical class organization.

**No deviations found.**

---

#### 2. Test Naming Conventions ✅ **COMPLIANT**

**File Naming:** `test_shortening_and_coordinate.py` follows the pattern `test_<feature>[_<subfeature>].py`

**Method Naming:** All 30 test methods follow the pattern `test_<scenario>`.

**No deviations found.**

---

#### 3. Use of pytest Markers ✅ **COMPLIANT**

| Marker | Line(s) | Usage |
|--------|---------|-------|
| `@pytest.mark.slow` | 729, 1090 | Applied to slow test classes |
| `@pytest.mark.needs_window` | 518 | Applied to test requiring Kivy window |

**No deviations found.**

---

#### 4. Property-Based Testing Practices ✅ **COMPLIANT**

All property tests use Hypothesis correctly with appropriate `@given` decorators and `@settings(max_examples=N, deadline=None)`.

**No deviations found.**

---

#### 5. Use of Helper Functions from test_utils.py ⚠️ **DEVIATION FOUND**

**Lines 25-26: Unused imports**

```python
from .test_utils import (
    markdown_heading, markdown_paragraph, markdown_bold, markdown_italic,
    markdown_link, simple_markdown_document, color_strategy, text_padding_strategy,
    find_labels_recursive, colors_equal, padding_equal, floats_equal, KIVY_FONTS
)
```

**12 of 13 imported helpers are unused:**
- Unused: `markdown_heading`, `markdown_paragraph`, `markdown_bold`, `markdown_italic`, `markdown_link`, `simple_markdown_document`, `color_strategy`, `text_padding_strategy`, `colors_equal`, `padding_equal`, `floats_equal`, `KIVY_FONTS`
- Used: `find_labels_recursive` (used extensively throughout the file)

**Guideline Reference:** [`TESTING.md:416-431`](kivy_garden/markdownlabel/tests/TESTING.md:416-431) emphasizes using helpers from `test_utils.py`, which implicitly discourages importing unused ones.

**Recommendation:** Replace with:
```python
from .test_utils import find_labels_recursive
```

---

#### 6. Standard Comment Formats for Hypothesis Strategies ✅ **COMPLIANT**

All 19 property-based tests include the required standardized comment format following the pattern: `# [Strategy Type] strategy: [N] examples ([Rationale])`

**No deviations found.**

---

### Deviations Summary

| # | Line(s) | Deviation | Severity |
|---|---------|-----------|----------|
| 1 | 25-26 | Unused helper function imports (12 of 13 imports) | Low |

---

### Conclusion

The test file demonstrates **strong adherence** to the testing guidelines. The file is well-organized, follows proper naming conventions, uses appropriate pytest markers, implements property-based testing correctly, and includes standardized comments for all Hypothesis strategies.

The only deviation is a minor code cleanliness issue with unused imports, which should be cleaned up for maintainability but does not affect test functionality.

---

## Tool Result 27


Subtask df355830-9204-44f0-917a-835d4d60ff98 completed.

Result:
# Test File Analysis Report: test_sizing_behavior.py

## Executive Summary

After analyzing [`test_sizing_behavior.py`](kivy_garden/markdownlabel/tests/test_sizing_behavior.py:1) against the guidelines in [`TESTING.md`](kivy_garden/markdownlabel/tests/TESTING.md:1), I found **2 deviations** from best practices. The file generally follows the testing guidelines well, with proper structure, naming conventions, and use of helper functions.

---

## Detailed Deviations

### Deviation 1: Missing pytest.mark.property Marker on Property-Based Tests

**Location:** Lines 31-33, 49-51, 70-72, 96-98, 106-108, 132-134, 161-163, 174-177, 192-194, 218-220, 239-241, 260-263, 294-296, 330-332, 343-346, 361-363, 387-389, 395-397, 404-406, 426-428, 448-451, 475-477, 490-493, 508-510, 527-529, 537-539

**Nature of Deviation:** Property-based tests that use `@given` decorator are not marked with `@pytest.mark.property` as recommended in the guidelines.

**Guideline Reference:** [`TESTING.md`](kivy_garden/markdownlabel/tests/TESTING.md:149) lines 149-158, which states:
> Use appropriate pytest markers to categorize tests:
> - `@pytest.mark.slow` - Performance-intensive tests
> - `@pytest.mark.needs_window` - Tests requiring Kivy window
> - `@pytest.mark.test_tests` - Meta-tests (tests about test suite structure)

While the guideline doesn't explicitly mention `@pytest.mark.property`, the pattern established in the guidelines suggests property-based tests should be marked to distinguish them from unit tests. The file already uses `@pytest.mark.test_tests` correctly on meta-test classes (lines 326 and 557).

**Example of Deviation:**
```python
# Line 31-33
@given(simple_markdown_document())
# Complex strategy: 20 examples (adequate coverage)
@settings(max_examples=20, deadline=None)
def test_auto_size_hint_enabled_sets_none(self, markdown_text):
```

**What Should Be Done Instead:**
```python
@pytest.mark.property
@given(simple_markdown_document())
# Complex strategy: 20 examples (adequate coverage)
@settings(max_examples=20, deadline=None)
def test_auto_size_hint_enabled_sets_none(self, markdown_text):
```

---

### Deviation 2: Inconsistent Comment Placement for Hypothesis Strategy Comments

**Location:** Lines 48-49, 94-95, 107-108, 133-134, 162-163, 176-177, 193-194, 219-220, 240-241, 261-263, 295-296, 331-332, 345-346, 362-363, 405-406, 427-428, 450-451, 476-477, 490-492, 509-511, 528-529, 538-539

**Nature of Deviation:** The standardized comment format for Hypothesis strategies is inconsistently placed. Some tests have the comment before the `@settings` decorator, while others have it after `@given` but before `@settings`. Additionally, line 261-263 has two consecutive strategy comments.

**Guideline Reference:** [`TESTING.md`](kivy_garden/markdownlabel/tests/TESTING.md:312) lines 312-321, which specifies:
```python
# [Strategy Type] strategy: [N] examples ([Rationale])
@settings(max_examples=N, deadline=None)
def test_example(value):
    pass
```

The comment should be placed immediately before `@settings`, not before `@given`.

**Examples of Deviation:**

**Example 1 - Comment before @given (Lines 48-49):**
```python
@given(markdown_heading())
# Complex strategy: 20 examples (adequate coverage)
@settings(max_examples=20, deadline=None)
```

**Example 2 - Comment before @given (Lines 94-95):**
```python
@given(simple_markdown_document())
# Complex strategy: 20 examples (adequate coverage)
@settings(max_examples=20, deadline=None)
```

**Example 3 - Duplicate comments (Lines 261-263):**
```python
@given(simple_markdown_document(), 
       st.floats(min_value=0.1, max_value=2.0, allow_nan=False, allow_infinity=False))
# Complex strategy: 50 examples (adequate coverage)
# Complex strategy: 20 examples (adequate coverage)
@settings(max_examples=50, deadline=None)
```

**Example 4 - Comment before @given (Lines 490-492):**
```python
@given(simple_markdown_document())
# Complex strategy: 20 examples (adequate coverage)
# Complex strategy: 20 examples (adequate coverage)
@settings(max_examples=20, deadline=None)
```

**What Should Be Done Instead:**
```python
@given(simple_markdown_document())
@settings(max_examples=20, deadline=None)
# Complex strategy: 20 examples (adequate coverage)
def test_example(self, markdown_text):
```

For combination strategies (Lines 261-263, 490-492), only one comment should be used, and it should reflect the combination:
```python
@given(simple_markdown_document(), 
       st.floats(min_value=0.1, max_value=2.0, allow_nan=False, allow_infinity=False))
@settings(max_examples=50, deadline=None)
# Combination strategy: 50 examples (combination coverage)
def test_example(self, markdown_text, user_size_hint_y):
```

---

## Areas of Compliance

The following aspects are **fully compliant** with the guidelines:

1. **Test File Structure and Organization** ✅
   - Proper module docstring (lines 1-6)
   - Logical class organization by feature/property
   - One class per property being tested

2. **Test Naming Conventions** ✅
   - File name follows `test_<feature>.py` pattern
   - Method names follow `test_<scenario>` pattern
   - Class names are descriptive and follow `Test[Property][Behavior]` pattern

3. **Helper Functions from test_utils.py** ✅
   - Properly imports `simple_markdown_document`, `markdown_heading`, `markdown_paragraph`, `find_labels_recursive` (lines 17-20)
   - No duplication of helper functions

4. **Standard Comment Formats for Hypothesis Strategies** ✅
   - Comments follow the format `# [Strategy Type] strategy: [N] examples ([Rationale])`
   - Strategy type classifications are appropriate (Boolean, Small finite, Complex, Combination)

5. **max_examples Settings** ✅
   - Boolean strategies correctly use `max_examples=2` (lines 388-389, 396-397)
   - Small finite strategies use input space size (line 71-72: 5 examples for range 1-5)
   - Complex strategies use 20-50 examples appropriately
   - Combination strategies use capped values (50 examples)

6. **Meta-Test Marking** ✅
   - `TestStrictLabelModeSizingBehavior` and `TestLogicalTestGrouping` correctly marked with `@pytest.mark.test_tests` (lines 326, 557)

7. **Class Docstrings** ✅
   - All test classes have descriptive docstrings
   - Feature and property documentation included in class comments

---

## Summary Table

| Aspect | Status | Notes |
|--------|--------|-------|
| File Structure | ✅ Compliant | Well-organized with proper docstrings |
| Naming Conventions | ✅ Compliant | Follows all naming patterns |
| Pytest Markers | ⚠️ Partial | Missing `@pytest.mark.property` on property tests |
| Strategy Comments | ⚠️ Partial | Incorrect placement, some duplicates |
| max_examples Settings | ✅ Compliant | Properly sized for strategy types |
| Helper Functions | ✅ Compliant | Properly imported and used |
| Meta-Test Marking | ✅ Compliant | Correctly uses `@pytest.mark.test_tests` |

---

## Recommendations

1. **Add `@pytest.mark.property` decorator** to all property-based tests that use `@given` to distinguish them from unit tests.

2. **Standardize comment placement** - Move all strategy comments to immediately before the `@settings` decorator, not before `@given`.

3. **Remove duplicate comments** - Tests with multiple strategy comments (lines 261-263, 490-492, 509-511) should have a single comment reflecting the combination strategy.

4. **Consider using combination strategy classification** for tests with multiple `@given` parameters instead of repeating "Complex strategy" comments.

---

## Tool Result 28


Subtask ae49c4b3-4ef8-4216-a478-fdafd37396e3 completed.

Result:
## Detailed Analysis Report: `test_strategy_classification.py` vs `TESTING.md` Guidelines

### Executive Summary
The test file [`test_strategy_classification.py`](kivy_garden/markdownlabel/tests/test_strategy_classification.py) is **mostly compliant** with the testing guidelines, with **3 notable deviations** identified.

---

### Deviation #1: Missing pytest Markers on Test Classes/Methods

**Location:** Lines 19-283 (Classes [`TestStrategyClassification`](kivy_garden/markdownlabel/tests/test_strategy_classification.py:19), [`TestMaxExamplesCalculation`](kivy_garden/markdownlabel/tests/test_strategy_classification.py:105), [`TestCombinationStrategies`](kivy_garden/markdownlabel/tests/test_strategy_classification.py:185))

**Nature of Deviation:**
The guidelines specify that tests should be categorized using appropriate pytest markers:
- `@pytest.mark.unit` - for unit tests
- `@pytest.mark.integration` - for integration tests  
- `@pytest.mark.property` - for property-based tests
- `@pytest.mark.slow` - for performance-intensive tests

Only the [`TestOverTestingDetection`](kivy_garden/markdownlabel/tests/test_strategy_classification.py:285) class (line 284) has the `@pytest.mark.test_tests` marker, which is correct for meta-tests. However, the other three test classes lack any pytest markers.

**Guideline Reference (Lines 148-158 of TESTING.md):**
```python
@pytest.mark.slow           # Performance-intensive tests
@pytest.mark.needs_window   # Tests requiring Kivy window
@pytest.mark.test_tests     # Meta-tests (tests about test suite structure)
```

**What Should Be Done Instead:**
Since these are property-based tests testing the optimization infrastructure, they should be marked appropriately:
```python
@pytest.mark.property
class TestStrategyClassification:
    """Property tests for strategy classification (Property 1)."""
```

---

### Deviation #2: No Helper Functions Imported from test_utils.py

**Location:** Lines 1-16 (Imports section)

**Nature of Deviation:**
The file does not import or use any helper functions from [`test_utils.py`](kivy_garden/markdownlabel/tests/test_utils.py). While this test file focuses on testing the optimization infrastructure (StrategyClassifier, MaxExamplesCalculator) rather than MarkdownLabel directly, the guidelines emphasize using shared helpers.

**Guideline Reference (Lines 413-431 of TESTING.md):**
```python
from .test_utils import (
    find_labels_recursive,
    collect_widget_ids,
    colors_equal,
    padding_equal,
    floats_equal
)
```

And specifically:
> "Always use helper functions from test_utils.py instead of duplicating code"

**What Should Be Done Instead:**
While this is a minor deviation (the test file doesn't need widget traversal helpers), if any comparison or utility functions are needed, they should be imported from `test_utils.py` rather than implemented inline.

---

### Deviation #3: Inaccurate Strategy Classification Comments

**Location:** Lines 56-58, 82-84

**Nature of Deviation:**
The comment format does not accurately describe the actual strategy type in two cases:

**Case 1 (Lines 56-58):**
```python
@given(st.lists(st.text(min_size=1, max_size=3, alphabet='abc'), min_size=1, max_size=10))
# Complex strategy: 10 examples (adequate coverage)
@settings(max_examples=10, deadline=None)
def test_small_sampled_from_classification(self, items):
```

The comment says "Complex strategy" but the actual strategy generates small lists with limited text. This should be classified as a "Small finite strategy" or "Medium finite strategy" based on the input space size.

**Case 2 (Lines 82-84):**
```python
@given(st.sampled_from(['st.text()', 'st.floats()', 'st.integers()']))
# Small finite strategy: 3 examples (input space size: 3)
@settings(max_examples=3, deadline=None)
def test_complex_strategy_classification(self, strategy_code):
```

The comment says "Small finite strategy" but the test purpose is to verify that complex/infinite strategy code strings are classified as `COMPLEX`. The strategy itself is small finite (3 items), but the test's purpose is about classification of complex strategies, making the comment potentially misleading.

**Guideline Reference (Lines 323-395 of TESTING.md):**
The guidelines specify exact formats for each strategy type:
- Boolean: `# Boolean strategy: 2 examples (True/False coverage)`
- Small finite: `# Small finite strategy: [N] examples (input space size: [N])`
- Medium finite: `# Medium finite strategy: [N] examples (adequate finite coverage)`
- Combination: `# Combination strategy: [N] examples (combination coverage)`
- Complex: `# Complex strategy: [N] examples (adequate coverage)`

**What Should Be Done Instead:**

For Case 1 (line 57):
```python
# Medium finite strategy: 10 examples (adequate finite coverage)
```

For Case 2 (line 83):
The comment is technically correct for the strategy itself (3 items from sampled_from), but could be clarified:
```python
# Small finite strategy: 3 examples (testing complex strategy classification)
```

---

### Compliant Aspects

The following aspects are **fully compliant** with the guidelines:

1. **Test file structure and organization** - Proper module docstring, logical class grouping, descriptive class names
2. **Test naming conventions** - File follows `test_<feature>.py` pattern; methods follow `test_<scenario>` pattern
3. **Property-based testing practices** - Correct use of `@given`, `@settings`, and `max_examples`
4. **Feature comment format** - Lines 26, 113, 160, 193, 293 properly use the `# **Feature: ..., Property N: ...**` format
5. **Test class organization** - One class per property/behavior being tested
6. **Meta-test marking** - [`TestOverTestingDetection`](kivy_garden/markdownlabel/tests/test_strategy_classification.py:285) correctly marked with `@pytest.mark.test_tests`

---

### Summary Table

| Aspect | Status | Notes |
|--------|--------|-------|
| Test file structure | ✅ Compliant | Good organization and docstrings |
| Test naming conventions | ✅ Compliant | Follows `test_<feature>.py` and `test_<scenario>` patterns |
| Pytest markers | ⚠️ Deviation | Missing `@pytest.mark.property` on test classes |
| Property-based testing practices | ✅ Compliant | Proper use of `@given`, `@settings`, `max_examples` |
| Helper functions from test_utils.py | ⚠️ Minor Deviation | No imports (though may not be needed for this test type) |
| Strategy comment formats | ⚠️ Deviation | 2 comments with inaccurate strategy type descriptions |
| Feature comment format | ✅ Compliant | Properly formatted feature/property comments |

---

## Tool Result 29


Subtask 1a4af235-e1af-4cae-95a5-e82233bb8b13 completed.

Result:
## Analysis Complete: test_text_properties.py vs TESTING.md Guidelines

### Summary
The file [`test_text_properties.py`](kivy_garden/markdownlabel/tests/test_text_properties.py) follows most naming conventions and uses helper functions correctly, but has **several deviations** from the testing guidelines.

### Deviations Found

#### 1. Missing pytest Markers (Lines 24-589)
**Nature**: No pytest markers (`@pytest.mark.unit`, `@pytest.mark.integration`, `@pytest.mark.property`, `@pytest.mark.slow`) are used on any test class or method.

**Guideline**: Lines 150-172 in [`TESTING.md`](kivy_garden/markdownlabel/tests/TESTING.md:150-172) specify "Use appropriate pytest markers to categorize tests"

#### 2. Comment Format Placement - Comments BEFORE @given (Lines 106, 110, 141, 159, 174, 199, 216, 257, 280, 304)
**Nature**: Comments are placed BEFORE the `@given` decorator instead of AFTER it.

**Guideline**: Lines 316-321 in [`TESTING.md`](kivy_garden/markdownlabel/tests/TESTING.md:316-321) specify the comment should be AFTER `@given` and BEFORE `@settings`

**Current**:
```python
@given(st.floats(...))
# Complex strategy: 50 examples (adequate coverage)
@settings(max_examples=50, deadline=None)
```

**Expected**:
```python
@given(st.floats(...))
# Complex strategy: 50 examples (adequate coverage)
@settings(max_examples=50, deadline=None)
```

#### 3. Unnecessary Use of Hypothesis for Default Value Tests (Lines 69-81, 450-458, 581-589)
**Nature**: Tests that verify constant default values use `@given(st.data())` unnecessarily. The `data` parameter is never used.

**Guideline**: Lines 278-304 in [`TESTING.md`](kivy_garden/markdownlabel/tests/TESTING.md:278-304) suggest using property-based tests for universal properties, but simple default value tests don't need Hypothesis.

**Affected tests**:
- [`test_default_text_size_is_none_none()`](kivy_garden/markdownlabel/tests/test_text_properties.py:72-81) (Lines 69-81)
- [`test_default_unicode_errors_is_replace()`](kivy_garden/markdownlabel/tests/test_text_properties.py:453-458) (Lines 450-458)
- [`test_default_strip_is_false()`](kivy_garden/markdownlabel/tests/test_text_properties.py:584-589) (Lines 581-589)

**Expected**: Convert to simple unit tests without `@given` decorator.

#### 4. Inconsistent Use of parametrize vs Hypothesis (Lines 424-448)
**Nature**: [`test_unicode_errors_change_updates_value()`](kivy_garden/markdownlabel/tests/test_text_properties.py:429-448) uses `@pytest.mark.parametrize` with explicit values instead of using `@given` with the existing `unicode_errors_strategy` defined at line 21.

**Guideline**: Lines 278-304 in [`TESTING.md`](kivy_garden/markdownlabel/tests/TESTING.md:278-304) suggest using property-based tests for universal properties.

**Expected**: Use `@given(unicode_errors_strategy, unicode_errors_strategy)` with `assume(errors1 != errors2)`.

### Aspects That Follow Guidelines ✅
1. ✅ Test file structure and organization
2. ✅ Test naming conventions (`test_<scenario>`)
3. ✅ Property-based testing practices with appropriate `max_examples` settings
4. ✅ Use of helper functions from [`test_utils.py`](kivy_garden/markdownlabel/tests/test_utils.py)
5. ✅ Standard comment formats for Hypothesis strategies (correct format, just wrong placement)

---

## Tool Result 30


Subtask 623dda81-3fa0-4e22-9b58-095cc074f6c1 completed.

Result:
# Detailed Deviation Report: test_texture_render_mode.py

## Summary
The file [`test_texture_render_mode.py`](kivy_garden/markdownlabel/tests/test_texture_render_mode.py) contains **4 significant deviations** from the testing guidelines in [`TESTING.md`](kivy_garden/markdownlabel/tests/TESTING.md).

---

## Deviation 1: Missing Standardized Comment Format for Property Tests

### Location
- **Lines 279-293**: [`test_property_inside_zone_dispatch()`](kivy_garden/markdownlabel/tests/test_texture_render_mode.py:294)
- **Lines 387-400**: [`test_property_outside_zone_no_dispatch()`](kivy_garden/markdownlabel/tests/test_texture_render_mode.py:401)

### Nature of Deviation
Both property tests use `@settings(max_examples=100)` but **do not include the required standardized comment format** before the `@settings` decorator.

### Current Code (Line 293)
```python
    )
    @settings(max_examples=100)
    def test_property_inside_zone_dispatch(
```

### Guideline Requirement (TESTING.md lines 312-322)
All property-based tests with custom `max_examples` values MUST include a standardized comment:

```python
# [Strategy Type] strategy: [N] examples ([Rationale])
@settings(max_examples=N, deadline=None)
def test_example(value):
    pass
```

### Recommended Fix
```python
    )
    # Combination strategy: 100 examples (combination coverage)
    @settings(max_examples=100, deadline=None)
    def test_property_inside_zone_dispatch(
```

---

## Deviation 2: Excessive max_examples Value Without Rationale

### Location
- **Lines 279-293**: [`test_property_inside_zone_dispatch()`](kivy_garden/markdownlabel/tests/test_texture_render_mode.py:294)
- **Lines 387-400**: [`test_property_outside_zone_no_dispatch()`](kivy_garden/markdownlabel/tests/test_texture_render_mode.py:401)

### Nature of Deviation
Both property tests use `max_examples=100`, which exceeds the recommended limits for the strategy types used.

### Guideline Requirements (TESTING.md lines 367-381)
- **Combination strategies**: Product of individual strategy sizes, **capped at 50**
- **Complex strategies**: 10-50 examples based on complexity

The tests use a combination of 4 strategies (zone, ref_name, touch_offset_x, touch_offset_y), which creates a large combination space. According to the guidelines, this should be capped at 50 examples, not 100.

### Recommended Fix
```python
    )
    # Combination strategy: 50 examples (combination coverage)
    @settings(max_examples=50, deadline=None)
    def test_property_inside_zone_dispatch(
```

---

## Deviation 3: Unused Static Method Strategy Definitions

### Location
- **Lines 261-269**: [`_zone_strategy()`](kivy_garden/markdownlabel/tests/test_texture_render_mode.py:262) static method
- **Lines 271-277**: [`_ref_name_strategy()`](kivy_garden/markdownlabel/tests/test_texture_render_mode.py:272) static method

### Nature of Deviation
These strategies are defined as static methods but are **never used**. Instead, the strategies are inlined directly in the `@given` decorators.

### Current Code (Lines 261-277)
```python
    # Property test strategies for hit-testing
    @staticmethod
    def _zone_strategy():
        """Strategy for generating valid ref zones."""
        return st.tuples(
            st.floats(min_value=0, max_value=300, allow_nan=False),
            st.floats(min_value=0, max_value=200, allow_nan=False),
            st.floats(min_value=10, max_value=100, allow_nan=False),
            st.floats(min_value=10, max_value=50, allow_nan=False)
        )
    
    @staticmethod
    def _ref_name_strategy():
        """Strategy for generating valid ref names (URLs)."""
        return st.from_regex(
            r'https?://[a-z]{3,10}\.[a-z]{2,5}/[a-z]{1,10}',
            fullmatch=True
        )
```

But the actual test uses inline strategies (Lines 279-292):
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
```

### Guideline Requirement (TESTING.md lines 412-432)
Helper functions and strategies should be defined in `test_utils.py` for reuse, and if defined locally, they should be used.

### Recommended Fix
Either:
1. **Remove the unused static methods** (lines 261-277), or
2. **Use them in the @given decorator** instead of inlining the strategies

---

## Deviation 4: Missing Pytest Markers

### Location
- All test classes and methods in the file

### Nature of Deviation
The file does not use any pytest markers as recommended in the guidelines.

### Guideline Requirement (TESTING.md lines 148-158)
Use appropriate pytest markers to categorize tests:
```python
@pytest.mark.slow           # Performance-intensive tests
@pytest.mark.needs_window   # Tests requiring Kivy window
@pytest.mark.test_tests     # Meta-tests (tests about test suite structure)
```

### Recommended Fix
Consider adding appropriate markers. For example, tests that involve widget tree creation and texture rendering might benefit from `@pytest.mark.slow` if they are performance-intensive.

---

## What Follows the Guidelines

The following aspects correctly follow the guidelines:

1. ✅ **File naming**: [`test_texture_render_mode.py`](kivy_garden/markdownlabel/tests/test_texture_render_mode.py:1) follows the `test_<feature>[_<subfeature>].py` pattern
2. ✅ **Module docstring**: Lines 1-11 provide a clear description of what the module tests
3. ✅ **Test method naming**: All methods follow the `test_<scenario>` pattern
4. ✅ **Test class naming**: Classes use descriptive names like `TestTextureRenderModeStructure`, `TestTextureModeLinksHandling`, etc.
5. ✅ **Class organization**: One class per property/behavior being tested
6. ✅ **Use of helper functions**: [`find_labels_recursive()`](kivy_garden/markdownlabel/tests/test_utils.py:134) and [`FakeTouch`](kivy_garden/markdownlabel/tests/test_utils.py:16) are imported from [`test_utils.py`](kivy_garden/markdownlabel/tests/test_utils.py:1)
7. ✅ **Feature/Property documentation**: Each class includes proper feature and property documentation comments (e.g., lines 34-37, 125-129)
8. ✅ **Test docstrings**: Each test method includes a descriptive docstring with feature and requirement references

---

## Summary of Required Changes

| Line(s) | Issue | Required Action |
|---------|-------|-----------------|
| 261-277 | Unused static method strategies | Remove or use them in @given decorators |
| 293 | Missing comment format | Add `# Combination strategy: 50 examples (combination coverage)` |
| 293 | Excessive max_examples | Change `max_examples=100` to `max_examples=50` |
| 400 | Missing comment format | Add `# Combination strategy: 50 examples (combination coverage)` |
| 400 | Excessive max_examples | Change `max_examples=100` to `max_examples=50` |
| File-wide | Missing pytest markers | Consider adding appropriate markers like `@pytest.mark.slow` |

---

## Tool Result 31


Subtask 7b1e85ca-d1a6-4ae7-9e4a-6053d871e386 completed.

Result:
## Test File Analysis Report: test_texture_sizing.py

### Summary
The file [`test_texture_sizing.py`](kivy_garden/markdownlabel/tests/test_texture_sizing.py) is **mostly compliant** with the testing guidelines in [`TESTING.md`](kivy_garden/markdownlabel/tests/TESTING.md). I found **one deviation** that needs attention.

---

### Deviations Found

#### 1. Duplicate Helper Function (Lines 39-59)

**Location:** Lines 39-59 in [`test_texture_sizing.py`](kivy_garden/markdownlabel/tests/test_texture_sizing.py:39)

```python
def _find_all_widgets_recursive(self, widget, widgets=None):
    """Recursively find all widgets in a widget tree.

    Args:
        widget: Root widget to search
        widgets: List to accumulate widgets (created if None)
        
    Returns:
        List of all widgets found
    """
    if widgets is None:
        widgets = []
    
    widgets.append(widget)
    
    if hasattr(widget, 'children'):
        for child in widget.children:
            # Complex strategy: 20 examples (adequate coverage)
            self._find_all_widgets_recursive(child, widgets)
    
    return widgets
```

**Nature of Deviation:** 
This method duplicates functionality that should be consolidated into [`test_utils.py`](kivy_garden/markdownlabel/tests/test_utils.py). While [`test_utils.py`](kivy_garden/markdownlabel/tests/test_utils.py) provides [`find_labels_recursive()`](kivy_garden/markdownlabel/tests/test_utils.py:134) which finds Label widgets specifically, this test needs a generic widget finder. The guideline states:

> **Section "Helper Functions" - "Using Shared Helpers":**
> "Always use helper functions from test_utils.py instead of duplicating code"

> **Section "Helper Functions" - "Adding New Helpers":**
> "When adding new helper functions:
> 1. **Add to test_utils.py** - Never duplicate in individual test files"

**What Should Be Done Instead:**
Either:
1. Add a generic `find_widgets_recursive()` helper to [`test_utils.py`](kivy_garden/markdownlabel/tests/test_utils.py) that works with any widget type, or
2. Modify the existing [`find_labels_recursive()`](kivy_garden/markdownlabel/tests/test_utils.py:134) to be more generic, or
3. Use the existing helper if the test only needs to verify Label widgets (the test appears to check for Label widgets in some cases)

**Additional Issue:** The comment on line 56 (`# Complex strategy: 20 examples (adequate coverage)`) is misplaced - this is a regular method, not a property-based test with Hypothesis.

---

### Aspects That Are Compliant

| Aspect | Status | Details |
|--------|--------|---------|
| **Test file structure** | ✅ Compliant | Follows standard template with module docstring, imports, and organized test classes |
| **Test naming conventions** | ✅ Compliant | File name follows `test_<feature>.py` pattern; method names follow `test_<scenario>` pattern |
| **Pytest markers** | ✅ Compliant | Uses `@pytest.mark.test_tests` for meta-tests (lines 35, 393) |
| **Property-based testing** | ✅ Compliant | Proper use of `@given`, `@settings`, and `assume()` decorators |
| **Strategy classifications** | ✅ Compliant | Correct classifications: "Complex strategy", "Small finite strategy", "Combination strategy" |
| **max_examples settings** | ✅ Compliant | Appropriate values: 2 for booleans, 5-6 for small finite, 20 for complex strategies |
| **Comment formats** | ✅ Compliant | All Hypothesis strategy comments follow standard format: `# [Type] strategy: [N] examples ([Rationale])` |
| **Helper function imports** | ✅ Compliant | Imports [`simple_markdown_document`](kivy_garden/markdownlabel/tests/test_utils.py:100), [`markdown_heading`](kivy_garden/markdownlabel/tests/test_utils.py:41), [`markdown_paragraph`](kivy_garden/markdownlabel/tests/test_utils.py:52), [`find_labels_recursive`](kivy_garden/markdownlabel/tests/test_utils.py:134) from test_utils |

---

### Examples of Good Practices Found

1. **Standardized Hypothesis comments** (lines 62-63, 76-77, 99-100, 115-116, 205-206, 249-250, 300-301, 347-348):
   ```python
   @given(simple_markdown_document())
   # Complex strategy: 20 examples (adequate coverage)
   @settings(max_examples=20, deadline=None)
   ```

2. **Small finite strategy correctly sized** (lines 204-206):
   ```python
   @given(st.integers(min_value=1, max_value=5))
   # Small finite strategy: 5 examples (input space size: 5)
   @settings(max_examples=5, deadline=None)
   ```

3. **Combination strategy correctly sized** (lines 299-301):
   ```python
   @given(simple_markdown_document(), simple_markdown_document())
   # Combination strategy: 20 examples (combination coverage)
   @settings(max_examples=20, deadline=None)
   ```

4. **Proper use of `assume()` to filter invalid inputs** (lines 119, 253, 304-305)

5. **Descriptive test class and method names** (e.g., `TestComprehensiveTextureSizeCalculation`, `test_texture_size_returns_tuple`)

6. **Meta-tests properly marked** (lines 35, 393) with `@pytest.mark.test_tests`

---

## Tool Result 32


Subtask e15050a0-a153-4e60-abbb-39111550c412 completed.

Result:
## Analysis Report: test_utils.py vs TESTING.md Guidelines

### Executive Summary

**No deviations found.** The file [`test_utils.py`](kivy_garden/markdownlabel/tests/test_utils.py) is a **utility module** (not a test file), and most of the testing guidelines in [`TESTING.md`](kivy_garden/markdownlabel/tests/TESTING.md) apply to actual test files. The utility module correctly implements the helper functions and Hypothesis strategies described in the guidelines.

---

### Detailed Analysis by Category

#### 1. Test File Structure and Organization
**Status: Not Applicable** - [`test_utils.py`](kivy_garden/markdownlabel/tests/test_utils.py) is a utility module, not a test file. The guidelines in "Test File Structure" (lines 461-512) apply to actual test files like `test_font_properties.py`, not to utility modules.

#### 2. Test Naming Conventions
**Status: Not Applicable** - The naming conventions `test_<feature>[_<subfeature>].py` for files and `test_<scenario>` for methods (lines 96-147) apply to test files and test methods. [`test_utils.py`](kivy_garden/markdownlabel/tests/test_utils.py) correctly follows the naming convention for utility modules as specified in the file organization section (line 40).

#### 3. Use of Pytest Markers
**Status: Not Applicable** - Pytest markers like `@pytest.mark.unit`, `@pytest.mark.integration`, `@pytest.mark.property`, and `@pytest.mark.slow` (lines 148-172) are used on test functions. [`test_utils.py`](kivy_garden/markdownlabel/tests/test_utils.py) contains no test functions, only helper functions and strategy definitions.

#### 4. Property-Based Testing Practices
**Status: Compliant** - The file contains Hypothesis strategies but no property tests. Property tests with `@given` and `@settings(max_examples=N)` decorators belong in test files, not in utility modules.

The strategies defined in [`test_utils.py`](kivy_garden/markdownlabel/tests/test_utils.py) are correctly implemented:
- [`markdown_heading()`](kivy_garden/markdownlabel/tests/test_utils.py:40-48) - Lines 40-48
- [`markdown_paragraph()`](kivy_garden/markdownlabel/tests/test_utils.py:51-65) - Lines 51-65
- [`markdown_bold()`](kivy_garden/markdownlabel/tests/test_utils.py:68-75) - Lines 68-75
- [`markdown_italic()`](kivy_garden/markdownlabel/tests/test_utils.py:78-85) - Lines 78-85
- [`markdown_link()`](kivy_garden/markdownlabel/tests/test_utils.py:88-96) - Lines 88-96
- [`simple_markdown_document()`](kivy_garden/markdownlabel/tests/test_utils.py:99-116) - Lines 99-116
- [`color_strategy`](kivy_garden/markdownlabel/tests/test_utils.py:120-123) - Lines 120-123
- [`text_padding_strategy`](kivy_garden/markdownlabel/tests/test_utils.py:126-129) - Lines 126-129

All strategies are properly documented with docstrings and follow Hypothesis best practices.

#### 5. Use of Helper Functions from test_utils.py
**Status: Not Applicable** - This IS [`test_utils.py`](kivy_garden/markdownlabel/tests/test_utils.py), so the guideline "Always use helper functions from test_utils.py instead of duplicating code" (line 416) applies to OTHER test files, not to this file itself.

The helper functions provided in [`test_utils.py`](kivy_garden/markdownlabel/tests/test_utils.py) match those listed in the guidelines (lines 434-442):

| Guideline Reference | Function in test_utils.py | Lines |
|---------------------|---------------------------|-------|
| `find_labels_recursive(widget)` | [`find_labels_recursive()`](kivy_garden/markdownlabel/tests/test_utils.py:134-154) | 134-154 |
| `collect_widget_ids(widget)` | [`collect_widget_ids()`](kivy_garden/markdownlabel/tests/test_utils.py:205-224) | 205-224 |
| `colors_equal(color1, color2)` | [`colors_equal()`](kivy_garden/markdownlabel/tests/test_utils.py:157-170) | 157-170 |
| `padding_equal(pad1, pad2)` | [`padding_equal()`](kivy_garden/markdownlabel/tests/test_utils.py:173-186) | 173-186 |
| `floats_equal(f1, f2)` | [`floats_equal()`](kivy_garden/markdownlabel/tests/test_utils.py:189-200) | 189-200 |

Additional rebuild testing helpers not explicitly listed in guidelines but logically consistent:
- [`assert_rebuild_occurred()`](kivy_garden/markdownlabel/tests/test_utils.py:227-245) - Lines 227-245
- [`assert_no_rebuild()`](kivy_garden/markdownlabel/tests/test_utils.py:248-266) - Lines 248-266

#### 6. Standard Comment Formats for Hypothesis Strategies
**Status: Not Applicable** - The standardized comment format requirement (lines 312-411) applies to `@settings(max_examples=N)` decorators in property test functions. The strategies in [`test_utils.py`](kivy_garden/markdownlabel/tests/test_utils.py) are strategy definitions, not test functions, and therefore do not use `@settings` decorators or require these comments.

The guideline specifically states (lines 314-321):
```python
# [Strategy Type] strategy: [N] examples ([Rationale])
@settings(max_examples=N, deadline=None)
def test_example(value):
    pass
```

This format is for test functions, not for strategy definitions.

#### 7. Any Deviations from Best Practices
**Status: None Found**

The file follows all applicable best practices:

✅ **Module Documentation** - Lines 1-6 provide clear module-level documentation  
✅ **Strategy Documentation** - All strategies have descriptive docstrings (e.g., [`markdown_heading()`](kivy_garden/markdownlabel/tests/test_utils.py:41-42), [`markdown_paragraph()`](kivy_garden/markdownlabel/tests/test_utils.py:52))  
✅ **Helper Function Documentation** - All helpers have detailed docstrings with Args and Returns sections  
✅ **Type Hints** - Functions use type annotations for better code clarity (e.g., [`find_labels_recursive()`](kivy_garden/markdownlabel/tests/test_utils.py:134))  
✅ **Logical Organization** - Code is organized into clear sections: Touch Simulation, Constants, Hypothesis Strategies, Helper Functions, Rebuild Detection Helpers  
✅ **Consistent Naming** - Function names follow Python conventions and clearly describe their purpose  

---

### Conclusion

**No deviations found.** The file [`test_utils.py`](kivy_garden/markdownlabel/tests/test_utils.py) is a utility module that correctly implements the helper functions and Hypothesis strategies described in the testing guidelines. Since it is not a test file, most of the testing guidelines (naming conventions, pytest markers, property test structure, comment formats for settings) do not apply to it directly. The file is well-structured, documented, and provides exactly what the guidelines specify for a shared test utilities module.

---

## Tool Result 33


Subtask 09e55358-8e73-4590-8d46-4bcf2e60bed8 completed.

Result:
I have completed the analysis of [`test_assertion_analyzer.py`](kivy_garden/markdownlabel/tests/tools/test_analysis/test_assertion_analyzer.py) against the testing guidelines from [`TESTING.md`](kivy_garden/markdownlabel/tests/TESTING.md).

## Summary of Findings

**5 deviations identified:**

1. **Missing `@pytest.mark.test_tests` marker** (Entire file) - This file contains meta-tests for the test suite infrastructure but lacks the required marker specified in lines 160-172 of TESTING.md.

2. **Property-based tests not organized in classes** (Lines 94-177) - The functions `test_value_change_test_naming_property` and `test_assertion_classification_consistency` should be organized within a test class per guidelines lines 46-94.

3. **Integration test not in a class** (Lines 180-232) - The `test_file_analysis_integration` function should be organized within a test class.

4. **Missing standardized comment for Hypothesis strategy** (Line 97) - The `@settings(max_examples=100)` decorator lacks the required comment format: `# [Strategy Type] strategy: [N] examples ([Rationale])` as specified in lines 312-322.

5. **Missing standardized comment for Hypothesis strategy** (Line 145) - Same issue as #4 for the second `@settings` decorator.

The report includes specific line numbers, the nature of each deviation, what the guidelines require, and expected implementation examples for each fix.

---

## Tool Result 34


Subtask 2c8b7465-a254-49c4-b773-b9fab830fa5f completed.

Result:
I have completed the analysis of [`test_code_duplication_minimization.py`](kivy_garden/markdownlabel/tests/tools/test_analysis/test_code_duplication_minimization.py) against [`TESTING.md`](kivy_garden/markdownlabel/tests/TESTING.md). The file generally follows most testing guidelines but contains **4 deviations**:

## Deviations Found

### 1. Missing `@pytest.mark.test_tests` marker (Line 133)
The `TestCodeDuplicationMinimization` class contains meta-tests that validate the test suite itself. According to lines 162-171 of [`TESTING.md`](kivy_garden/markdownlabel/tests/TESTING.md:162-171), meta-tests must be marked with `@pytest.mark.test_tests`.

**Fix:** Add `@pytest.mark.test_tests` decorator to the class.

### 2. Non-standard strategy type classification (Line 392)
The comment uses "Simple strategy" for `st.floats()`, but according to lines 383-395 of [`TESTING.md`](kivy_garden/markdownlabel/tests/TESTING.md:383-395), `st.floats()` is classified as a **Complex/Infinite Strategy**.

**Fix:** Change comment to `# Complex strategy: 8 examples (adequate coverage)`

### 3. Non-standard strategy type classification and incorrect max_examples (Line 192)
The comment uses "Simple strategy" for `st.integers(min_value=2, max_value=6)`, but this is a **Small Finite Strategy** with an input space of 5 values. According to lines 339-351 of [`TESTING.md`](kivy_garden/markdownlabel/tests/TESTING.md:339-351), it should use `max_examples` equal to the input space size.

**Fix:** Change comment to `# Small finite strategy: 5 examples (input space size: 5)` and set `max_examples=5`

### 4. Missing `@pytest.mark.test_tests` marker on test_duplication_threshold_realistic (Line 291)
This test validates test suite structure and should be marked as a meta-test.

**Fix:** Add `@pytest.mark.test_tests` decorator to the method (or apply at class level as per Deviation 1)

## Compliant Aspects
- ✅ Test file structure and organization
- ✅ Test naming conventions follow `test_<feature>[_<subfeature>].py` and `test_<scenario>` patterns
- ✅ Property-based testing practices (custom strategy properly defined)
- ✅ Helper functions usage (appropriate for meta-test context)
- ✅ Comments exist for all custom max_examples values

---

## Tool Result 35


Subtask ff6c74ac-830a-450f-ba4f-35820c3d531c completed.

Result:
I have completed the analysis of all 4 test files in `kivy_garden/markdownlabel/tests/tools/test_analysis/` against the testing guidelines from `TESTING.md`. 

**Summary of Deviations Found:**

### **File 1: test_coverage_preservation.py**
- 5 missing `@pytest.mark.test_tests` markers (lines 187, 193, 318, 399, 496)
- 2 incorrect strategy classifications (lines 316, 494)

### **File 2: test_duplicate_detector.py**
- 6 missing `@pytest.mark.test_tests` markers (lines 97, 103, 155, 198, 269, 323)
- 2 incorrect strategy classifications (lines 101, 153)

### **File 3: test_naming_convention_validator.py**
- 5 missing `@pytest.mark.test_tests` markers (lines 28, 118, 177, 228, 285)
- 2 missing strategy comments for custom max_examples (lines 118, 177)
- 2 incorrect strategy classifications (lines 118, 177)

### **File 4: test_test_file_parser.py**
- 6 missing `@pytest.mark.test_tests` markers (lines 87, 93, 133, 162, 202, 243)
- 2 incorrect strategy classifications (lines 91, 131)

**Total: 23 missing pytest markers, 8 incorrect strategy classifications, 2 missing strategy comments**

All files have correct test file structure and test naming conventions. The primary deviations are:
1. Missing `@pytest.mark.test_tests` markers for meta-tests (required per TESTING.md:162-171)
2. Incorrect strategy type classifications in comments (should use: Boolean, Small finite, Medium finite, Combination, or Complex as defined in TESTING.md:323-395)
3. Missing standardized comments for custom max_examples values (format: `# [Strategy Type] strategy: [N] examples ([Rationale])` per TESTING.md:312-322)

---

