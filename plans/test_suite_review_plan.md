# Test Suite Review Plan

## Overview

This plan outlines a systematic review of the MarkdownLabel test suite to ensure compliance with the guidelines documented in [`kivy_garden/markdownlabel/tests/TESTING.md`](../kivy_garden/markdownlabel/tests/TESTING.md). The review will be conducted in chunks of no more than 5 files at a time to prevent context window overflow.

## Review Methodology

### Review Approach

Each chunk will be reviewed systematically using the following methodology:

1. **File-by-File Analysis**: Examine each test file individually against the guidelines
2. **Guideline Verification**: Check compliance with each relevant section of TESTING.md
3. **Issue Documentation**: Record all violations, missing elements, or areas for improvement
4. **Pattern Recognition**: Identify recurring issues across files within the chunk
5. **Recommendation Generation**: Provide specific, actionable recommendations for each issue

### Review Checklist

Based on TESTING.md, each test file will be evaluated against the following criteria:

#### 1. File Organization
- [ ] File name follows `test_[functionality_area].py` pattern
- [ ] File is organized by functionality, not implementation file
- [ ] Module docstring describes what the file covers
- [ ] Module docstring lists key areas tested

#### 2. Class Organization
- [ ] Tests organized into logical classes
- [ ] One class per property or behavior being tested
- [ ] Descriptive class names that clearly indicate what is being tested
- [ ] Related test methods grouped within the same class
- [ ] No mixing of unrelated functionality in a single class
- [ ] No vague class names (e.g., `TestBasicStuff`, `TestMisc`)

#### 3. Test Naming Conventions
- [ ] Test method names accurately reflect what they assert
- [ ] Rebuild testing names follow patterns:
  - `test_*_triggers_rebuild_*` - ONLY for tests verifying rebuild occurred
  - `test_*_preserves_widget_tree_*` - For tests verifying NO rebuild occurred
  - `test_*_rebuilds_*` - For tests verifying rebuild behavior
- [ ] Value/property testing names follow patterns:
  - `test_*_updates_value_*` - For tests verifying value changes
  - `test_*_changes_property_*` - For tests verifying property changes
  - `test_*_forwards_to_*` - For tests verifying property forwarding
  - `test_*_applied_to_*` - For tests verifying property application
- [ ] Test names match actual assertions (not misleading)

#### 4. Test Types and Markers
- [ ] Appropriate pytest markers used:
  - `@pytest.mark.slow` for performance-intensive tests
  - `@pytest.mark.needs_window` for tests requiring Kivy window
  - `@pytest.mark.test_tests` for meta-tests
- [ ] Meta-tests properly marked with `@pytest.mark.test_tests`

#### 5. Rebuild Contract Testing
- [ ] Style-only properties tested for NO rebuild:
  - color, font_size, base_font_size, font_name, line_height
  - halign, valign, text_size, padding
- [ ] Structure properties tested for rebuild:
  - text, render_mode, properties affecting parsing/hierarchy
- [ ] Rebuild tests use helper functions from test_utils.py:
  - `collect_widget_ids(widget)`
  - `assert_rebuild_occurred(widget, change_func)`
  - `assert_no_rebuild(widget, change_func)`
- [ ] Tests verify both rebuild behavior AND value changes

#### 6. Property-Based Testing
- [ ] Property-based tests use Hypothesis appropriately
- [ ] Tests verify universal properties, invariants, or round-trip properties
- [ ] No property-based tests for simple examples (use unit tests instead)
- [ ] Appropriate choice between Hypothesis and `@pytest.mark.parametrize`:
  - Single dimension, ≤10 values: Use `@pytest.mark.parametrize`
  - Multiple dimensions, product >20: Use Hypothesis
  - Infinite/broad spaces: Always use Hypothesis

#### 7. Property-Based Testing Optimization
- [ ] Custom `max_examples` values include standardized comments
- [ ] Comment format: `# [Strategy Type] strategy: [N] examples ([Rationale])`
- [ ] Strategy type classifications use standardized terminology:
  - Boolean strategy: 2 examples (True/False coverage)
  - Small finite strategy: [N] examples (input space size: [N])
  - Medium finite strategy: [N] examples (adequate finite coverage)
  - Combination strategy: [N] examples (combination coverage)
  - Complex strategy: [N] examples (adequate coverage or performance optimized)
- [ ] max_examples values are right-sized:
  - Boolean strategies: 2
  - Small finite (≤10 values): Input space size
  - Medium finite (11-50 values): Input space size, capped at 20-50
  - Combination strategies: Product of individual sizes, capped at 50
  - Complex/infinite: 10-50 based on complexity

#### 8. Helper Functions
- [ ] Helper functions imported from test_utils.py (not duplicated)
- [ ] Widget traversal helpers used:
  - `find_labels_recursive(widget)`
  - `collect_widget_ids(widget)`
- [ ] Comparison utilities used:
  - `colors_equal(color1, color2)`
  - `padding_equal(pad1, pad2)`
  - `floats_equal(f1, f2, tolerance=1e-6)`
- [ ] Hypothesis strategies from test_utils.py used where appropriate:
  - `markdown_heading()`, `markdown_paragraph()`, etc.

#### 9. Test File Structure
- [ ] Standard imports at top (pytest, hypothesis, MarkdownLabel, test_utils)
- [ ] Clear separation between test classes
- [ ] Docstrings for test classes and methods
- [ ] Consistent formatting and indentation

#### 10. Best Practices
- [ ] Descriptive test and class names
- [ ] Related tests grouped in same class
- [ ] Both positive and negative cases tested
- [ ] Complex test logic documented
- [ ] No testing of implementation details (test behavior instead)
- [ ] No test failures ignored or skipped without good reason
- [ ] Performance considerations addressed (slow tests marked)

### Issue Classification

Issues found during review will be classified as:

1. **Critical**: Violations that break testing guidelines or could lead to incorrect test behavior
2. **Major**: Significant deviations from guidelines that impact maintainability
3. **Minor**: Style or documentation improvements
4. **Suggestion**: Optional improvements or best practices

### Reporting Format

For each chunk, the review will produce:

1. **Chunk Summary**: Overview of files reviewed
2. **Per-File Analysis**: Detailed findings for each file
3. **Cross-File Patterns**: Recurring issues across the chunk
4. **Recommendations**: Specific, actionable recommendations
5. **Priority Matrix**: Issues ranked by severity and impact

## Test File Chunks

### Chunk 1: Core Functionality Tests
Files:
1. [`test_import.py`](../kivy_garden/markdownlabel/tests/test_import.py)
2. [`test_inline_renderer.py`](../kivy_garden/markdownlabel/tests/test_inline_renderer.py)
3. [`test_kivy_renderer.py`](../kivy_garden/markdownlabel/tests/test_kivy_renderer.py)
4. [`test_core_functionality.py`](../kivy_garden/markdownlabel/tests/test_core_functionality.py)
5. [`test_label_compatibility.py`](../kivy_garden/markdownlabel/tests/test_label_compatibility.py)

### Chunk 2: Property Tests - Font & Color
Files:
1. [`test_font_properties.py`](../kivy_garden/markdownlabel/tests/test_font_properties.py)
2. [`test_color_properties.py`](../kivy_garden/markdownlabel/tests/test_color_properties.py)
3. [`test_text_properties.py`](../kivy_garden/markdownlabel/tests/test_text_properties.py)
4. [`test_padding_properties.py`](../kivy_garden/markdownlabel/tests/test_padding_properties.py)
5. [`test_sizing_behavior.py`](../kivy_garden/markdownlabel/tests/test_sizing_behavior.py)

### Chunk 3: Advanced Features & Compatibility
Files:
1. [`test_advanced_compatibility.py`](../kivy_garden/markdownlabel/tests/test_advanced_compatibility.py)
2. [`test_serialization.py`](../kivy_garden/markdownlabel/tests/test_serialization.py)
3. [`test_performance.py`](../kivy_garden/markdownlabel/tests/test_performance.py)
4. [`test_rebuild_scheduling.py`](../kivy_garden/markdownlabel/tests/test_rebuild_scheduling.py)
5. [`test_rebuild_semantics.py`](../kivy_garden/markdownlabel/tests/test_rebuild_semantics.py)

### Chunk 4: Behavior Tests
Files:
1. [`test_clipping_behavior.py`](../kivy_garden/markdownlabel/tests/test_clipping_behavior.py)
2. [`test_texture_render_mode.py`](../kivy_garden/markdownlabel/tests/test_texture_render_mode.py)
3. [`test_texture_sizing.py`](../kivy_garden/markdownlabel/tests/test_texture_sizing.py)
4. [`test_rtl_alignment.py`](../kivy_garden/markdownlabel/tests/test_rtl_alignment.py)
5. [`test_shortening_and_coordinate.py`](../kivy_garden/markdownlabel/tests/test_shortening_and_coordinate.py)

### Chunk 5: Test Utilities & Meta-Tests (Part 1)
Files:
1. [`test_utils.py`](../kivy_garden/markdownlabel/tests/test_utils.py)
2. [`meta_tests/test_assertion_analyzer.py`](../kivy_garden/markdownlabel/tests/meta_tests/test_assertion_analyzer.py)
3. [`meta_tests/test_code_duplication_minimization.py`](../kivy_garden/markdownlabel/tests/meta_tests/test_code_duplication_minimization.py)
4. [`meta_tests/test_comment_format.py`](../kivy_garden/markdownlabel/tests/meta_tests/test_comment_format.py)
5. [`meta_tests/test_comment_standardizer.py`](../kivy_garden/markdownlabel/tests/meta_tests/test_comment_standardizer.py)

### Chunk 6: Meta-Tests (Part 2)
Files:
1. [`meta_tests/test_core_functionality_properties.py`](../kivy_garden/markdownlabel/tests/meta_tests/test_core_functionality_properties.py)
2. [`meta_tests/test_coverage_preservation.py`](../kivy_garden/markdownlabel/tests/meta_tests/test_coverage_preservation.py)
3. [`meta_tests/test_documentation_compliance.py`](../kivy_garden/markdownlabel/tests/meta_tests/test_documentation_compliance.py)
4. [`meta_tests/test_duplicate_detector.py`](../kivy_garden/markdownlabel/tests/meta_tests/test_duplicate_detector.py)
5. [`meta_tests/test_file_analyzer.py`](../kivy_garden/markdownlabel/tests/meta_tests/test_file_analyzer.py)

### Chunk 7: Meta-Tests (Part 3)
Files:
1. [`meta_tests/test_helper_availability.py`](../kivy_garden/markdownlabel/tests/meta_tests/test_helper_availability.py)
2. [`meta_tests/test_naming_convention_validator.py`](../kivy_garden/markdownlabel/tests/meta_tests/test_naming_convention_validator.py)
3. [`meta_tests/test_refactoring_properties.py`](../kivy_garden/markdownlabel/tests/meta_tests/test_refactoring_properties.py)
4. [`meta_tests/test_shared_infrastructure.py`](../kivy_garden/markdownlabel/tests/meta_tests/test_shared_infrastructure.py)
5. [`meta_tests/test_sizing_behavior_grouping.py`](../kivy_garden/markdownlabel/tests/meta_tests/test_sizing_behavior_grouping.py)

### Chunk 8: Meta-Tests (Part 4)
Files:
1. [`meta_tests/test_strategy_classification.py`](../kivy_garden/markdownlabel/tests/meta_tests/test_strategy_classification.py)
2. [`meta_tests/test_test_file_parser.py`](../kivy_garden/markdownlabel/tests/meta_tests/test_test_file_parser.py)
3. [`meta_tests/test_texture_sizing_grouping.py`](../kivy_garden/markdownlabel/tests/meta_tests/test_texture_sizing_grouping.py)

**Total**: 8 chunks covering 38 test files

## Review Workflow

### For Each Chunk:

1. **Read Files**: Read all 5 files in the chunk
2. **Apply Checklist**: Systematically evaluate each file against the review checklist
3. **Document Findings**: Record all issues with:
   - File name and line number
   - Guideline section violated
   - Issue classification (Critical/Major/Minor/Suggestion)
   - Specific recommendation
4. **Identify Patterns**: Look for recurring issues across the chunk
5. **Generate Report**: Create a structured report for the chunk

### Chunk Report Template:

```markdown
# Test Suite Review: Chunk [N] - [Chunk Name]

## Files Reviewed
- [File 1]
- [File 2]
- [File 3]
- [File 4]
- [File 5]

## Per-File Analysis

### [File 1]
**Overall Status**: [Pass/Fail/Needs Improvement]

**Findings**:
- [ ] [Issue 1] - [Classification]
  - Location: Line [X]
  - Guideline: [Section from TESTING.md]
  - Recommendation: [Specific action]

[... additional findings ...]

### [File 2]
[... same structure ...]

## Cross-File Patterns
1. [Pattern 1]: [Description]
   - Affected files: [List]
   - Recommendation: [Unified approach]

## Priority Matrix

| Priority | Issue | File | Impact |
|----------|-------|------|--------|
| Critical | [Issue] | [File] | [Impact description] |
| Major | [Issue] | [File] | [Impact description] |
| Minor | [Issue] | [File] | [Impact description] |

## Summary Statistics
- Total files reviewed: 5
- Files with critical issues: [N]
- Files with major issues: [N]
- Files with minor issues: [N]
- Total issues found: [N]
- Critical: [N], Major: [N], Minor: [N], Suggestions: [N]
```

### Final Summary Report

After all chunks are reviewed, a final summary report will be generated:

1. **Overall Compliance Score**: Percentage of guidelines met across all files
2. **Most Common Violations**: Top 5 recurring issues
3. **Critical Issues Summary**: All critical issues requiring immediate attention
4. **Recommendations by Category**: Organized by guideline section
5. **Action Plan**: Prioritized list of improvements

## Success Criteria

The review will be considered successful when:

1. All 8 chunks have been reviewed
2. Each file has been evaluated against all applicable guidelines
3. All issues have been documented with specific recommendations
4. Patterns across files have been identified
5. A comprehensive final summary report has been generated

## Next Steps

Once this plan is approved:

1. Begin with Chunk 1 (Core Functionality Tests)
2. Complete review for each chunk before moving to the next
3. Generate chunk reports as each chunk is completed
4. Compile final summary report after all chunks are reviewed
5. Present findings and recommendations to the team

## Notes

- This review focuses on compliance with TESTING.md guidelines
- Test functionality is NOT being evaluated (only test structure and organization)
- The review is descriptive, not prescriptive - it documents what exists vs. what guidelines require
- Meta-tests may have different requirements than regular tests (this will be noted in the review)
