# Test Suite Review: Optimization & Documentation Guidelines

This document details the findings from a review of the `kivy_garden/markdownlabel/tests` directory against the standards defined in `HYPOTHESIS_OPTIMIZATION_GUIDELINES.md` and related requirement documents.

## Executive Summary

The test suite has partially adopted the new optimization guidelines. Most property-based tests correctly implement CI-aware `max_examples` settings (e.g., reducing examples in CI). However, the **documentation standards are consistently violated** across the codebase.

**Key Issues:**
1.  **Duplicate Comments:** Almost every file contains redundant strategy comments (appearing before `@given`, before `@settings`, and inside function bodies).
2.  **Misplaced Comments:** Comments often appear in the wrong location (must be immediately before `@settings`).
3.  **Strategy Misclassification:** Boolean strategies are frequently mislabeled as "Complex" or "Combination" with incorrect example counts.
4.  **Optimization Logic Errors:** Some boolean tests use excessive example counts (e.g., 100) instead of the mathematically sufficient 2.

## Detailed Findings

### 1. `tests/test_performance.py`

*   **Logic Error:** `test_disabled_change_preserves_widget_tree` uses `st.booleans()` but sets `max_examples=2 if os.getenv('CI') else 100`.
    *   **Recommendation:** Change to `max_examples=2` (constant). Boolean space size is 2. Testing 100 times is wasteful.
    *   **Correction:** Change comment to `# Boolean strategy: 2 examples (True/False coverage)`.
*   **Misclassification:** The above test is labeled "Complex strategy".

### 2. `tests/test_color_properties.py`

*   **Duplicate Comments:**
    *   `test_color_applied_to_heading`: Comment appears twice (before `@given` and before `@settings`).
    *   `test_color_change_triggers_rebuild`: Comment appears inside the function body.
*   **Misplaced Comments:**
    *   `test_code_block_preserves_light_color`: Comment appears after the function body logic.

### 3. `tests/test_text_properties.py`

*   **Missing Documentation:**
    *   `test_strip_stored_correctly`: Uses `@settings(max_examples=2)` but has **NO** explanatory comment.
*   **Duplicate/Misplaced Comments:**
    *   `test_text_size_height_forwarded_to_paragraph`: Comment appears before `@given`.
    *   `test_default_text_size_is_none_none`: Comment appears inside the function body.

### 4. `tests/test_font_properties.py`

*   **Duplicate Comments:**
    *   `test_line_height_applied_to_code_block`: Comment appears before `@given` and inside function body.
*   **Misclassification:**
    *   `test_font_kerning_forwarded_to_all_labels_including_code`: Uses `st.booleans()` but is likely labeled generically or duplicated.

### 5. `tests/test_advanced_compatibility.py`

*   **Misclassification:**
    *   `test_font_kerning_change_triggers_rebuild`: Uses `st.booleans()` (two of them) but label says `# Complex strategy: 20 examples`. Should be `# Combination strategy: 4 examples`.
    *   `test_disabled_change_rebuilds_widgets`: Same issue. Two booleans = 4 combinations, not "Complex".

## Recommendations

1.  **Run the `CommentStandardizer` tool:** The codebase clearly needs an automated cleanup pass to remove duplicate and misplaced comments. The current state suggests comments were maybe added via a script that didn't check for existing ones, or were copy-pasted incorrectly.
2.  **Enforce Comment Placement:** Ensure strict adherence to placing comments **only** immediately before `@settings`.
3.  **Fix Boolean Strategies:** Grep for `st.booleans()` and ensure `max_examples` is set to 2 (or 4 for two booleans, etc.) and labeled as "Boolean strategy" or "Combination strategy", never "Complex".
4.  **Remove In-Function Comments:** Remove all strategy comments that have leaked into the function bodies.

## Example of Correct vs. Current State

**Current (Incorrect):**
```python
    # Complex strategy: 20 examples (adequate coverage)  <-- Duplicate/Wrong Type
    @given(st.booleans())
    # Complex strategy: 20 examples (adequate coverage)  <-- Wrong Type
    @settings(max_examples=2 if os.getenv('CI') else 100, deadline=None) <-- Wasteful
    def test_something(self, value):
```

**Correct:**
```python
    @given(st.booleans())
    # Boolean strategy: 2 examples (True/False coverage)
    @settings(max_examples=2, deadline=None)
    def test_something(self, value):
```
