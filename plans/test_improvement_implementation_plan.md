# Test Suite Improvement Implementation Plan

This document outlines the implementation plan to address all deviations documented in `kivy_garden/markdownlabel/tests/DEVIATIONS.md` based on the testing guidelines in `TESTING.md`.

## Overview

The plan is organized into 12 phases covering 74 individual tasks across 24 test files. Each phase focuses on a specific category of improvements to ensure systematic and manageable implementation.

## Phase 1a: Comment Fixes - test_comment_standardizer.py

### Tasks

1. **Fix line 42-43**: Change boolean strategy comment from "Combination strategy: 20 examples (adequate coverage)" to "Boolean strategy: 2 examples (True/False coverage)" and update max_examples from 20 to 2
   - **Issue**: Boolean strategy incorrectly classified as combination strategy with excessive examples
   - **Guideline**: TESTING.md lines 321-333 - Boolean strategies should use exactly 2 examples with format "Boolean strategy: 2 examples (True/False coverage)"

2. **Fix line 591-592**: Change comment from "Combination strategy: 3 examples (performance optimized)" to correct strategy type for integers (small finite or complex based on range)
   - **Issue**: First @given parameter is `st.integers(min_value=1, max_value=5)`, not booleans. Copy-paste error from boolean strategy template
   - **Guideline**: TESTING.md lines 335-347 - Small integer ranges should use input space size (5 values)

## Phase 1b: Comment Fixes - test_comment_format.py

### Tasks

1. **Fix line 538**: Change "Complex strategy: 30 examples (adequate coverage)" to "Combination strategy: 30 examples (performance optimized)" for multiple sampled_from strategies
   - **Issue**: Test uses `st.sampled_from()` to sample from 3 independent domains (strategy_type, max_examples, rationale_base), creating a combination
   - **Guideline**: TESTING.md lines 363-377 - Multiple strategies combined should be classified as "Combination strategy"

## Phase 1c: Comment Fixes - test_text_properties.py

### Tasks

1. **Fix line 162-164**: Change "Small finite strategy: 3 examples (input space size: 3)" to "Combination strategy" for floats + sampled_from combination
   - **Issue**: Test `test_valign_forwarded_with_height` uses combination of `st.floats()` and `st.sampled_from()` strategies
   - **Guideline**: TESTING.md lines 363-377 - Combination strategies are for multiple strategies combined

## Phase 1d: Comment Fixes - test_helper_availability.py

### Tasks

1. **Fix line 59**: Change "Combination strategy: 10 examples (combination coverage)" to "Complex strategy: 10 examples (adequate coverage)" for color_strategy
   - **Issue**: `color_strategy` is a complex/infinite strategy, not a finite combination strategy
   - **Guideline**: TESTING.md lines 379-391 - Complex strategies use 10-50 examples

2. **Fix line 75**: Change "Combination strategy: 10 examples (combination coverage)" to "Complex strategy: 10 examples (adequate coverage)" for text_padding_strategy
   - **Issue**: `text_padding_strategy` is a complex/infinite strategy
   - **Guideline**: TESTING.md lines 379-391

3. **Fix line 91**: Change "Combination strategy: 10 examples (combination coverage)" to "Complex strategy: 10 examples (adequate coverage)" for floats strategy
   - **Issue**: `st.floats(min_value=-1000, max_value=1000, allow_nan=False, allow_infinity=False)` is complex (2000+ possible values)
   - **Guideline**: TESTING.md lines 379-391

4. **Fix line 146**: Update rationale from "adequate coverage" to more specific justification for max_examples=1
   - **Issue**: Using `max_examples=1` for a complex strategy with vague rationale
   - **Guideline**: TESTING.md lines 379-391 - Complex strategies should use 10-50 examples

5. **Fix line 159**: Update rationale from "adequate coverage" to more specific justification for max_examples=1
   - **Issue**: Same as line 146
   - **Guideline**: TESTING.md lines 379-391

6. **Fix line 172**: Update rationale from "adequate coverage" to more specific justification for max_examples=1
   - **Issue**: Same as line 146
   - **Guideline**: TESTING.md lines 379-391

## Phase 1e: Comment Fixes - test_clipping_behavior.py

### Tasks

1. **Fix line 77-78**: Reduce max_examples from 50 to 10-20 for single floats strategy
   - **Issue**: `test_clipping_container_height_matches_text_size` uses `max_examples=50` for single `st.floats()` strategy
   - **Guideline**: TESTING.md lines 379-391 - Complex strategies like `st.floats()` should typically use 10-20 examples

2. **Fix line 244-245**: Reduce max_examples from 50 to 10-20 for single floats strategy
   - **Issue**: `test_text_size_width_only_no_clipping` uses `max_examples=50` for single `st.floats()` strategy
   - **Guideline**: TESTING.md lines 379-391

## Phase 1f: Comment Fixes - test_strategy_classification.py

### Tasks

1. **Fix line 24-26**: Change from "Small finite strategy: 1 examples (input space size: 1)" to "Boolean strategy: 2 examples (True/False coverage)" and update max_examples to 2
   - **Issue**: Test uses `st.just('st.booleans()')` which generates only 1 example, but comment format is incorrect
   - **Guideline**: TESTING.md lines 321-333 - Boolean strategies should use exactly 2 examples

2. **Fix line 53-55**: Change "Medium finite strategy: 10 examples (adequate finite coverage)" to "Complex strategy: 10 examples (adequate coverage)" for lists with text
   - **Issue**: Test uses `st.lists(st.text(min_size=1, max_size=3, alphabet='abc'), min_size=1, max_size=10)` which generates potentially infinite combinations
   - **Guideline**: TESTING.md lines 379-391 - `st.lists()` with `st.text()` is a complex/infinite strategy

## Phase 1g: Comment Fixes - test_kivy_renderer.py

### Tasks

1. **Fix line 88**: Update max_examples from 5 to 6 for integers 1-6 (input space size)
   - **Issue**: Test uses `st.integers(min_value=1, max_value=6)` with `max_examples=5`, but input space is 6 values
   - **Guideline**: TESTING.md lines 335-347 - Small finite strategies should use input space size

2. **Fix line 89-90**: Change "Complex strategy: 10 examples (adequate coverage)" to "Combination strategy: 10 examples (performance optimized)"
   - **Issue**: Strategy is combination of `st.integers(min_value=1, max_value=6)` (6 values) and `st.floats(min_value=10, max_value=30)` (21 values), total input space 126
   - **Guideline**: TESTING.md lines 363-377 - Combination strategies with performance optimization

## Phase 1h: Comment Fixes - test_inline_renderer.py

### Tasks

1. **Fix lines 61-74**: Change "Complex strategy: 20 examples (adequate coverage)" to "Combination strategy: 20 examples (combination coverage)" for sampled_from + text
   - **Issue**: `link_token()` strategy uses `st.sampled_from()` with 69 URL-safe characters combined with `st.text()` for URL generation
   - **Guideline**: TESTING.md lines 363-377 - Multiple strategies combined should be "Combination strategy"

2. **Fix lines 408-420**: Change "Complex strategy: 20 examples (adequate coverage)" to "Combination strategy: 20 examples (combination coverage)" for one_of with 5 strategies
   - **Issue**: Test `test_urls_with_brackets_are_safe` uses `st.one_of()` with 5 different mapped text strategies
   - **Guideline**: TESTING.md lines 363-377

3. **Fix lines 658-677**: Change "Complex strategy: 20 examples (adequate coverage)" to "Combination strategy: 20 examples (combination coverage)" for one_of with 8 strategies
   - **Issue**: Test `test_html_content_is_escaped` uses `st.one_of()` with 8 different mapped text strategies
   - **Guideline**: TESTING.md lines 363-377

## Phase 1i: Comment Fixes - test_performance.py

### Tasks

1. **Fix line 216**: Change "Combination strategy: 20 examples (adequate coverage)" to "Complex strategy: 20 examples (adequate coverage)" for single floats
   - **Issue**: Test uses a single `st.floats()` strategy
   - **Guideline**: TESTING.md lines 379-391 - Single `st.floats()` is a complex/infinite strategy

2. **Fix line 241**: Change "Combination strategy: 20 examples (adequate coverage)" to "Complex strategy: 20 examples (adequate coverage)" for single floats
   - **Issue**: Same as line 216
   - **Guideline**: TESTING.md lines 379-391

3. **Fix line 396**: Change "Combination strategy: 20 examples (adequate coverage)" to "Complex strategy: 20 examples (adequate coverage)" for tuples with floats
   - **Issue**: Test uses two `st.tuples()` arguments, each containing 4 floats with range [0, 1] (effectively infinite strategies)
   - **Guideline**: TESTING.md lines 379-391

## Phase 1j: Comment Fixes - test_texture_sizing.py

### Tasks

1. **Fix line 276-278**: Increase max_examples from 20 to 50 (capped) for combination of two complex strategies
   - **Issue**: Test uses two `simple_markdown_document()` parameters (combination strategy) with only `max_examples=20`
   - **Guideline**: TESTING.md lines 363-377 - Combination strategies should use product of individual strategy sizes, capped at 50

## Phase 1k: Comment Fixes - test_rebuild_semantics.py

### Tasks

1. **Fix line 775**: Change "Complex strategy: 50 examples (adequate coverage)" to "Combination strategy: 50 examples (performance optimized)"
   - **Issue**: Test uses two `simple_markdown_document()` parameters which is a combination of two complex strategies
   - **Guideline**: TESTING.md lines 363-377

2. **Fix line 822**: Change "Complex strategy: 50 examples (adequate coverage)" to "Small finite strategy: 3 examples (input space size: 3)" and update max_examples to 3
   - **Issue**: Test uses `st.sampled_from(['Roboto', 'RobotoMono-Regular', 'Roboto-Bold'])` which is a small finite strategy (3 values)
   - **Guideline**: TESTING.md lines 335-347

3. **Fix line 869**: Change "Complex strategy: 50 examples (adequate coverage)" to "Small finite strategy: 2 examples (input space size: 2)" and update max_examples to 2
   - **Issue**: Test uses `st.sampled_from(['unstyled', 'styled'])` which is a small finite strategy (2 values)
   - **Guideline**: TESTING.md lines 335-347

## Phase 1l: Comment Fixes - test_shortening_and_coordinate.py

### Tasks

1. **Fix line 134-136**: Change "Combination strategy: 30 examples (adequate coverage)" to "Complex strategy: 30 examples (adequate coverage)" for single text
   - **Issue**: Test uses `st.text(min_size=0, max_size=5, alphabet='abc ')` which is a single text strategy
   - **Guideline**: TESTING.md lines 379-391

2. **Fix line 148-150**: Change "Combination strategy: 30 examples (adequate coverage)" to "Complex strategy: 30 examples (adequate coverage)" for single text
   - **Issue**: Same as line 134-136
   - **Guideline**: TESTING.md lines 379-391

3. **Fix line 325-327**: Change "Combination strategy: 2 examples (combination coverage)" to "Boolean strategy: 2 examples (True/False coverage)" for two booleans
   - **Issue**: Test uses `st.booleans(), st.booleans()` which are two boolean strategies
   - **Guideline**: TESTING.md lines 321-333

4. **Fix line 406-407**: Change "Combination strategy: 20 examples (adequate coverage)" to "Complex strategy: 20 examples (adequate coverage)" for lists with text
   - **Issue**: Test uses `st.lists(st.text(...), min_size=2, max_size=4)` which is a complex/infinite strategy
   - **Guideline**: TESTING.md lines 379-391

5. **Fix line 577-578**: Change "Combination strategy: 20 examples (adequate coverage)" to "Complex strategy: 20 examples (adequate coverage)" for two text parameters
   - **Issue**: Test uses two `st.text()` parameters creating a complex strategy with multiple text inputs
   - **Guideline**: TESTING.md lines 379-391

6. **Fix line 615-616**: Change "Combination strategy: 20 examples (adequate coverage)" to "Complex strategy: 20 examples (adequate coverage)" for four floats
   - **Issue**: Test uses four `st.floats()` parameters
   - **Guideline**: TESTING.md lines 379-391

7. **Fix line 645-646**: Change "Combination strategy: 20 examples (adequate coverage)" to "Complex strategy: 20 examples (adequate coverage)" for two floats
   - **Issue**: Test uses two `st.floats()` parameters
   - **Guideline**: TESTING.md lines 379-391

8. **Fix line 957-959**: Standardize comment format from "Complex strategy with 12 float parameters: 100 examples for adequate coverage" to "Complex strategy: 100 examples (adequate coverage for 12-parameter float strategy)"
   - **Issue**: Comment does not follow standardized format
   - **Guideline**: TESTING.md lines 308-317 - Comments must follow format: `# [Strategy Type] strategy: [N] examples ([Rationale])`

## Phase 1m: Comment Fixes - test_label_compatibility.py

### Tasks

1. **Fix lines 137-139**: Change "Combination strategy: 2 examples (combination coverage)" to "Small finite strategy: 32 examples (input space size: 32)" and update max_examples to 32
   - **Issue**: Test uses 5 booleans with `max_examples=2`, creating a finite input space of 32 combinations (2^5)
   - **Guideline**: TESTING.md lines 335-347

2. **Fix lines 156-159**: Increase max_examples from 2 to 50 (capped) for 5 booleans + markdown document combination
   - **Issue**: Test uses 5 booleans + simple_markdown_document with `max_examples=2`, but 5 booleans alone create 32 combinations
   - **Guideline**: TESTING.md lines 363-377 - Combination strategies should use product of individual strategy sizes, capped at 50

## Phase 2: Test Naming Convention Fixes

### Tasks

1. **Fix line 877** (test_advanced_compatibility.py): Rename `test_disabled_color_updates_value` to `test_disabled_change_triggers_rebuild` to match rebuild behavior
   - **Issue**: Method name suggests value update test, but implementation verifies rebuild behavior (calls `force_rebuild()`)
   - **Guideline**: TESTING.md lines 102-107 - Tests verifying rebuilds should use naming convention `test_*_triggers_rebuild_*`

2. **Fix line 238** (test_padding_properties.py): Rename `test_padding_change_updates_value` to `test_padding_change_triggers_rebuild` and add rebuild verification
   - **Issue**: Method name suggests value update test, but implementation calls `label.force_rebuild()` indicating rebuild behavior
   - **Guideline**: TESTING.md lines 102-107

3. **Fix line 283** (test_padding_properties.py): Rename `test_padding_update_paragraph` to `test_padding_update_triggers_rebuild` and add rebuild verification
   - **Issue**: Method name suggests value update test, but implementation calls `label.force_rebuild()` without verifying rebuild behavior
   - **Guideline**: TESTING.md lines 102-107

4. **Fix line 308** (test_padding_properties.py): Rename `test_padding_update_complex_content` to `test_padding_update_triggers_rebuild` and add rebuild verification
   - **Issue**: Same as line 283
   - **Guideline**: TESTING.md lines 102-107

5. **Rename all "preserves_widget_ids" tests** (test_rebuild_semantics.py, lines 91-267) to "preserves_widget_tree" pattern
   - **Issue**: Tests use "preserves_widget_ids" naming pattern instead of guideline pattern `test_*_preserves_widget_tree_*`
   - **Guideline**: TESTING.md lines 102-107 - Tests verifying NO rebuild occurred should use `test_*_preserves_widget_tree_*`

6. **Rename property test** "test_style_property_changes_preserve_widget_identities" (test_rebuild_semantics.py, lines 313-358) to "preserves_widget_tree" pattern
   - **Issue**: Uses "preserve_widget_identities" naming instead of `test_*_preserves_widget_tree_*`
   - **Guideline**: TESTING.md lines 102-107

7. **Rename all "rebuilds_widget_tree" tests** (test_rebuild_semantics.py, lines 601-758) to "triggers_rebuild" pattern
   - **Issue**: Tests use "rebuilds_widget_tree" naming pattern instead of guideline pattern `test_*_triggers_rebuild_*`
   - **Guideline**: TESTING.md lines 102-107 - Tests verifying a rebuild occurred should use `test_*_triggers_rebuild_*`

8. **Rename property test** "test_text_change_rebuilds_widget_tree_pbt" (test_rebuild_semantics.py, lines 777-816) to "triggers_rebuild" pattern
   - **Issue**: Uses "rebuilds_widget_tree_pbt" naming instead of `test_*_triggers_rebuild_*`
   - **Guideline**: TESTING.md lines 102-107

## Phase 3: Docstring Improvements

### Tasks

1. **Fix line 123-137** (test_documentation_compliance.py): Improve docstring for `test_custom_value_detection_property` to describe specific property and expected behavior
   - **Issue**: Docstring "Property test for custom value detection logic." is generic and does not describe what specific property is being tested
   - **Guideline**: TESTING.md lines 45-74 - Test docstrings should clearly describe what is being tested, including what property or behavior is being verified

2. **Fix line 138-164** (test_documentation_compliance.py): Improve docstring for `test_comment_detection_property` to describe specific property and expected behavior
   - **Issue**: Docstring "Property test for explanatory comment detection." is generic
   - **Guideline**: TESTING.md lines 45-74

3. **Fix line 22** (test_assertion_analyzer.py): Update class docstring from "Unit tests for AssertionAnalyzer." to "Tests for assertion pattern detection and naming mismatch analysis."
   - **Issue**: Generic class docstring
   - **Guideline**: TESTING.md lines 45-74 - Class docstrings should clearly indicate what is being tested

4. **Fix line 37-41** (test_shared_infrastructure.py): Simplify docstring for `test_markdown_heading_strategy_generates_valid_headings` to remove markdown formatting
   - **Issue**: Overly verbose docstring with markdown formatting (Feature/Property/Rationale sections)
   - **Guideline**: TESTING.md lines 286-300, 456-490 - Test docstrings should be concise and descriptive

5. **Fix line 160-165** (test_shared_infrastructure.py): Simplify docstring for `test_find_labels_recursive_function_available` to remove markdown formatting
   - **Issue**: Same as line 37-41
   - **Guideline**: TESTING.md lines 286-300, 456-490

6. **Fix line 116-122** (test_naming_convention_validator.py): Simplify docstring for `test_naming_pattern_consistency_property` to remove markdown formatting
   - **Issue**: Docstring uses markdown formatting with "**Property 6: Naming Pattern Consistency**" and "**Validates: Requirements 1.4, 5.2**" headers
   - **Guideline**: TESTING.md lines 286-300, 456-490

## Phase 4: Unused Import Removal

### Tasks

1. **Remove unused imports** (test_padding_properties.py, lines 11-14): BoxLayout, Label, Widget, GridLayout from kivy.uix modules
   - **Issue**: Imports declared but never used in the test file
   - **Guideline**: TESTING.md line 628 - Unused imports should be removed to keep code clean

2. **Remove unused import** (test_rtl_alignment.py, line 8): `import os`
   - **Issue**: Import declared but never used
   - **Guideline**: TESTING.md line 628

3. **Remove unused import** (test_font_properties.py, line 9): `import os`
   - **Issue**: Import declared but never used
   - **Guideline**: TESTING.md line 628

4. **Remove unused imports** (test_sizing_behavior.py, lines 11-12): BoxLayout and Label from kivy.uix
   - **Issue**: Imports declared but never used
   - **Guideline**: TESTING.md line 628

## Phase 5: Test Organization Fixes

### Tasks

1. **Move property test** `test_value_change_test_naming_property` (test_assertion_analyzer.py, lines 89-128) into TestAssertionAnalyzer class
   - **Issue**: Property-based test is at module level rather than within a class
   - **Guideline**: TESTING.md lines 43-74 - Tests should be organized into logical classes with descriptive names

2. **Move property test** `test_assertion_classification_consistency` (test_assertion_analyzer.py, lines 131-174) into TestAssertionAnalyzer class
   - **Issue**: Property-based test is at module level rather than within a class
   - **Guideline**: TESTING.md lines 43-74

3. **Move integration test** `test_file_analysis_integration()` (test_assertion_analyzer.py, lines 177-229) into a new TestAssertionAnalyzerIntegration class
   - **Issue**: Integration test is a module-level function instead of being in a class
   - **Guideline**: TESTING.md lines 43-74 - Tests should be organized into logical classes

## Phase 6: Rebuild Testing Improvements

### Tasks

1. **Fix line 251** (test_padding_properties.py): Replace `label.force_rebuild()` call with rebuild detection helpers in `test_padding_change_updates_value`
   - **Issue**: Test calls `label.force_rebuild()` after changing padding property
   - **Guideline**: TESTING.md lines 186-258 - Tests should verify rebuild behavior using helper functions like `assert_rebuild_occurred()` or `assert_no_rebuild()` instead of manually calling `force_rebuild()`

2. **Fix line 297** (test_padding_properties.py): Replace `label.force_rebuild()` call with rebuild detection helpers in `test_padding_update_paragraph`
   - **Issue**: Same as line 251
   - **Guideline**: TESTING.md lines 186-258

3. **Fix line 335** (test_padding_properties.py): Replace `label.force_rebuild()` call with rebuild detection helpers in `test_padding_update_complex_content`
   - **Issue**: Same as line 251
   - **Guideline**: TESTING.md lines 186-258

4. **Fix line 353** (test_padding_properties.py): Replace `label.force_rebuild()` call with rebuild detection helpers in `test_multiple_padding_updates`
   - **Issue**: Same as line 251
   - **Guideline**: TESTING.md lines 186-258

## Phase 7: Pytest Marker Fixes

### Tasks

1. **Remove or document all `@pytest.mark.property` markers** (test_sizing_behavior.py, lines 29, 47, 69, 94, 105, 132, 162, 176, 195, 222, 244, 266, 301, 338, 352, 371, 398, 407, 417, 440, 463, 491, 507, 525, 544)
   - **Issue**: Marker is NOT documented in TESTING.md. Guidelines only document `@pytest.mark.slow`, `@pytest.mark.needs_window`, and `@pytest.mark.test_tests` markers
   - **Guideline**: TESTING.md lines 150-158 - Only documented markers should be used

2. **Remove or document undocumented markers** (test_file_analyzer.py): @pytest.mark.unit (lines 83, 224, 322), @pytest.mark.property (lines 286, 459), @pytest.mark.integration (line 393)
   - **Issue**: Undocumented pytest markers used throughout the file
   - **Guideline**: TESTING.md lines 150-158

3. **Remove or document undocumented marker** (test_import.py, lines 14, 21): @pytest.mark.unit
   - **Issue**: Undocumented pytest marker
   - **Guideline**: TESTING.md lines 150-158

## Phase 8: Property-Based Test Usage Fixes

### Tasks

1. **Fix line 119-121** (test_padding_properties.py): Remove @given decorator from `test_default_padding_is_zero` and convert to regular unit test
   - **Issue**: Test uses `@given(st.data())` but the `data` parameter is never used. Test simply verifies default padding is zero, which is a concrete assertion
   - **Guideline**: TESTING.md lines 276-300 - Property-based tests should be used for universal properties, not for testing specific default values

## Phase 9: Window Marker Fixes

### Tasks

1. **Add @pytest.mark.needs_window marker** (test_core_functionality.py, lines 33, 46, 63, 108, 127, 154, 171, 203, 227, 248, 279, 297, 314) to tests creating MarkdownLabel widgets
   - **Issue**: Tests that create MarkdownLabel widgets require a Kivy window but are missing the marker
   - **Guideline**: TESTING.md lines 150-158 - Tests requiring Kivy window should be marked with `@pytest.mark.needs_window`

## Phase 10: Code Cleanup

### Tasks

1. **Remove redundant local `import os`** (test_refactoring_properties.py, line 89) in method `test_fast_test_discovery_baseline`
   - **Issue**: Redundant local import when `os` is already imported at module level (line 9)
   - **Guideline**: TESTING.md line 628 - Unused/duplicate code should be removed

2. **Remove redundant local `import os`** (test_refactoring_properties.py, line 137) in method `test_individual_module_discovery_functionality`
   - **Issue**: Same as line 89
   - **Guideline**: TESTING.md line 628

3. **Remove redundant local `import os`** (test_refactoring_properties.py, line 173) in method `test_discovery_startup_functionality`
   - **Issue**: Same as line 89
   - **Guideline**: TESTING.md line 628

4. **Remove orphaned comment** (test_serialization.py, line 156)
   - **Issue**: Orphaned comment `# Complex strategy: 20 examples (adequate coverage)` not associated with any `@given` decorator or test method
   - **Guideline**: Code cleanliness

## Phase 11: Import Path Fixes

### Tasks

1. **Fix line 15** (test_code_duplication_minimization.py): Change import from `from test_analysis.duplicate_detector import...` to `from tools.test_analysis.duplicate_detector import...`
   - **Issue**: Import statement imports from wrong location. Test file is at `kivy_garden/markdownlabel/tests/tools/test_analysis/test_code_duplication_minimization.py` and uses relative import `test_analysis.duplicate_detector`, but `duplicate_detector.py` is at `tools/test_analysis/duplicate_detector.py`
   - **Guideline**: Correct import paths for module resolution

## Phase 12: Validation & Testing

### Tasks

1. **Run all tests** to ensure fixes don't break functionality
   - Execute full test suite to verify no regressions

2. **Run comment validation tool** to verify all comment format issues are resolved
   - Use `tools/validate_comments.py` to validate comment compliance

3. **Update DEVIATIONS.md** to mark completed items
   - Document which deviations have been addressed

## Summary

- **Total Phases**: 12
- **Total Tasks**: 74
- **Files Affected**: 24 test files
- **Primary Categories**:
  - Comment format and strategy classification (36 tasks)
  - Test naming conventions (8 tasks)
  - Docstring improvements (6 tasks)
  - Code cleanup and organization (24 tasks)

## Implementation Notes

1. Each task should be completed independently where possible
2. After each phase, run tests to ensure no regressions
3. Use the comment validation tool to verify comment format compliance
4. Update the todo list as tasks are completed
5. Document any unexpected issues or deviations from the plan

## References

- Testing Guidelines: `kivy_garden/markdownlabel/tests/TESTING.md`
- Deviations Document: `kivy_garden/markdownlabel/tests/DEVIATIONS.md`
- Comment Validation Tool: `tools/validate_comments.py`
