These are the findings from a review of the `kivy_garden/markdownlabel/tests` directory against the standards defined in `.kiro/specs/test-comment-standardization/design.md`,`.kiro/specs/test-comment-standardization/requirements.md`,`DEVELOPER_GUIDE_PROPERTY_TESTS.md`, and `HYPOTHESIS_OPTIMIZATION_GUIDELINES.md`.

## Summary

The test suite has partially adopted the new optimization guidelines. Most property-based tests correctly implement CI-aware `max_examples` settings (e.g., reducing examples in CI). However, the **documentation standards are consistently violated** across the codebase.

**Key Issues:**

1. **Duplicate Comments:** Almost every file contains redundant strategy comments (appearing before `@given`, before `@settings`, and inside function bodies).
2. **Misplaced Comments:** Comments often appear in the wrong location (must be immediately before `@settings`).
3. **Strategy Misclassification:** Boolean strategies are frequently mislabeled as "Complex" or "Combination" with incorrect example counts.
4. **Optimization Logic Errors:** Some boolean tests use excessive example counts (e.g., 100) instead of the mathematically sufficient 2.

## Recommendations

1. **Enforce Comment Placement:** Ensure strict adherence to placing comments **only** immediately before `@settings`.
2. **Fix Boolean Strategies:** Grep for `st.booleans()` and ensure `max_examples` is set to 2 (or 4 for two booleans, etc.) and labeled as "Boolean strategy" or "Combination strategy", never "Complex".
3. **Remove In-Function Comments:** Remove all strategy comments that have leaked into the function bodies.

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