# Test Suite Improvement Guidelines for AI Agents

## Objective

The goal is to manually repair the test suite's comment standardization and hypothesis optimization settings. Previous attempts to use automated scripts (`fix_comment_format.py`) resulted in errors, so we represent a "human-in-the-loop" approach where an AI agent (you) iteratively fixes files one by one, applying judgment to avoid edge cases.

## Workflow

For the named test file in `kivy_garden/markdownlabel/tests/`:

1.  **Analyze**: Run `python tools/validate_comments.py validate <path_to_file> --verbose` to see reported issues.
2.  **Inspect**: Read the file code. *Do not blindly trust the tool's report*, especially regarding line numbers or content inside string literals.
3.  **Edit**: Apply fixes manually to the file.
4.  **Verify**:
    *   Run `python tools/validate_comments.py validate <path_to_file>` to ensure compliance.
    *   Run `pytest <path_to_file>` to ensure no syntax errors or logic breaks were introduced.

## Standards and Guidelines

### 1. Comment Placement and Format
*   **Location**: The comment **MUST** be placed *immediately* before the `@settings` decorator.
*   **Format**: `# [Strategy Type] strategy: [N] examples ([Rationale])`
*   **Removal**: Remove any duplicate strategy comments found:
    *   Inside the function body.
    *   Before `@given`.
    *   Detached from the decorators.

### 2. Strategy Types and Max Examples

| Strategy Type | Definition | Max Examples | Rationale Text |
| :--- | :--- | :--- | :--- |
| **Boolean** | `st.booleans()` | **2** | `True/False coverage` |
| **Small finite** | Range size ≤ 10 | **Size of space** | `input space size: N` |
| **Medium finite** | Range size 11-50 | **Size of space** | `adequate finite coverage` |
| **Combination** | Tuples/Multiple args | **Product (cap 50)** | `combination coverage` |
| **Complex** | Text, Floats, Recursive | **10-50** | `adequate coverage` or `performance optimized` |

**Critical Rule for Booleans**:
*   **Incorrect**: `max_examples=2 if os.getenv('CI') else 100` (for `st.booleans()`).
*   **Correct**: `max_examples=2` (always). Testing `True` and `False` 50 times each adds no value.

### 3. Edge Cases and Pitfalls (CRITICAL)

*   **Test Data vs. Code**:
    *   **Do NOT** modify strings that contain Python code or comments (e.g., in `test_comment_format.py` or `test_file_analyzer.py`). These are tests *checking* the validator. Modifying them will break the tests.
    *   *Example*: If you see `code_str = "# Boolean strategy..."`, **LEAVE IT ALONE**.
*   **Indentation**: Ensure the comment matches the indentation of the decorator it precedes (usually 4 spaces inside a class).
*   **Imports**: If you change `max_examples` to a fixed number, you might generate unused imports (e.g., `os` if you remove `os.getenv('CI')`). Clean them up if obvious, but primarily focus on the tests.

## Step-by-Step Fix Example

**Input (Broken):**

```python
    # Complex strategy: 20 examples (adequate coverage)  <-- WRONG TYPE, WRONG PLACE
    @given(st.booleans())
    # Complex strategy: 20 examples (adequate coverage)  <-- DUPLICATE
    @settings(max_examples=2 if os.getenv('CI') else 100, deadline=None) <-- OVERKILL
    def test_something(self, value):
```

**Action:**
1.  Identify strategy is `st.booleans()`, so type is **Boolean**.
2.  Max examples for Boolean is **2**.
3.  Remove `os.getenv` logic.
4.  Remove duplicate/misplaced comments.
5.  Add correct comment before `@settings`.

**Output (Fixed):**

```python
    @given(st.booleans())
    # Boolean strategy: 2 examples (True/False coverage)
    @settings(max_examples=2, deadline=None)
    def test_something(self, value):
```