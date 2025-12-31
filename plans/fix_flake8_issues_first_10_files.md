# Plan: Fix Flake8 Issues - First 10 Files

## Overview
This plan addresses fixing flake8 linting issues in the first 10 files from the 53 split files. Each file will be addressed in a separate subtask to avoid context bloat and agent confusion.

## Issue Types Summary

The flake8 issues fall into these categories:

- **W293**: Blank line contains whitespace (most common)
- **F401**: Imported but unused
- **W291**: Trailing whitespace
- **E305**: Expected 2 blank lines after class/function definition
- **E501**: Line too long (>110 characters)
- **W292**: No newline at end of file
- **E303**: Too many blank lines
- **E301**: Expected 1 blank line
- **E302**: Expected 2 blank lines
- **E129**: Visually indented line with same indent as next logical line

## File-by-File Plan

### File 1: kivy_garden/markdownlabel/__init__.py (330 issues)

**Issues breakdown:**
- ~325 W293 (blank lines with whitespace)
- 4 F401 (unused imports: `Color`, `Rectangle`, `ObjectProperty`, `__version__`)
- 2 W291 (trailing whitespace)
- 1 E305 (missing blank line after class definition)

**Fix approach:**
1. Remove unused imports:
   - Line 20: Remove `kivy.graphics.Color` and `kivy.graphics.Rectangle`
   - Line 21: Remove `kivy.properties.ObjectProperty`
   - Line 66: Remove `._version.__version__` (or move it to appropriate location)
2. Remove trailing whitespace from lines 22 and 23
3. Add 2 blank lines after class definition at line 66 (E305 fix)
4. Remove all W293 whitespace from blank lines throughout the file

**Verification:**
- Run `flake8 kivy_garden/markdownlabel/__init__.py` to confirm all issues resolved

---

### File 2: kivy_garden/markdownlabel/inline_renderer.py (54 issues)

**Issues breakdown:**
- 53 W293 (blank lines with whitespace)
- 1 W291 (trailing whitespace on line 19)

**Fix approach:**
1. Remove trailing whitespace from line 19
2. Remove all W293 whitespace from blank lines throughout the file

**Verification:**
- Run `flake8 kivy_garden/markdownlabel/inline_renderer.py` to confirm all issues resolved

---

### File 3: kivy_garden/markdownlabel/kivy_renderer.py (190 issues)

**Issues breakdown:**
- 188 W293 (blank lines with whitespace)
- 2 W291 (trailing whitespace on lines 580 and 996)

**Fix approach:**
1. Remove trailing whitespace from lines 580 and 996
2. Remove all W293 whitespace from blank lines throughout the file

**Verification:**
- Run `flake8 kivy_garden/markdownlabel/kivy_renderer.py` to confirm all issues resolved

---

### File 4: kivy_garden/markdownlabel/markdown_serializer.py (109 issues)

**Issues breakdown:**
- ~105 W293 (blank lines with whitespace)
- 2 E303 (too many blank lines at lines 78 and 250)
- 2 E301 (expected 1 blank line at line 80)

**Fix approach:**
1. Fix E303 at line 78: Remove one blank line (2 → 1 blank line)
2. Fix E301 at line 80: Add 1 blank line before the function/class definition
3. Fix E303 at line 250: Remove one blank line (3 → 2 blank lines)
4. Remove all W293 whitespace from blank lines throughout the file

**Verification:**
- Run `flake8 kivy_garden/markdownlabel/markdown_serializer.py` to confirm all issues resolved

---

### File 5: kivy_garden/markdownlabel/tests/conftest.py (1 issue)

**Issues breakdown:**
- 1 W292 (no newline at end of file, line 88)

**Fix approach:**
1. Add a newline character at the end of the file

**Verification:**
- Run `flake8 kivy_garden/markdownlabel/tests/conftest.py` to confirm all issues resolved

---

### File 6: kivy_garden/markdownlabel/tests/meta_tests/test_assertion_analyzer.py (49 issues)

**Issues breakdown:**
- ~40 W293 (blank lines with whitespace)
- 6 F401 (unused imports: `hypothesis.assume`, `pathlib.Path`, `typing.List`, `typing.Dict`, `AssertionPattern`, `AssertionAnalysis`)
- 5 E501 (lines too long at lines 17, 79, 88, 95, 117, 119, 133)
- 1 W292 (no newline at end of file)

**Fix approach:**
1. Remove unused imports:
   - Line 11: Remove `hypothesis.assume`
   - Line 14: Remove `pathlib.Path`
   - Line 15: Remove `typing.List` and `typing.Dict`
   - Line 17: Remove `AssertionPattern` and `AssertionAnalysis`
2. Break long lines (>110 chars) by:
   - Line 17: Split import statement across multiple lines
   - Lines 79, 88, 95, 117, 119, 133: Break long lines or use parentheses for continuation
3. Add newline at end of file
4. Remove all W293 whitespace from blank lines

**Verification:**
- Run `flake8 kivy_garden/markdownlabel/tests/meta_tests/test_assertion_analyzer.py` to confirm all issues resolved

---

### File 7: kivy_garden/markdownlabel/tests/meta_tests/test_code_duplication_minimization.py (69 issues)

**Issues breakdown:**
- ~60 W293 (blank lines with whitespace)
- 5 F401 (unused imports: `hypothesis.assume`, `pathlib.Path`, `typing.List`, `typing.Dict`, `ConsolidationReport`)
- 3 E501 (lines too long at lines 69, 73, 274, 277)
- 1 W292 (no newline at end of file)

**Fix approach:**
1. Remove unused imports:
   - Line 9: Remove `hypothesis.assume`
   - Line 12: Remove `pathlib.Path`
   - Line 13: Remove `typing.List` and `typing.Dict`
   - Line 15: Remove `ConsolidationReport`
2. Break long lines (>110 chars) at lines 69, 73, 274, 277
3. Add newline at end of file
4. Remove all W293 whitespace from blank lines

**Verification:**
- Run `flake8 kivy_garden/markdownlabel/tests/meta_tests/test_code_duplication_minimization.py` to confirm all issues resolved

---

### File 8: kivy_garden/markdownlabel/tests/meta_tests/test_comment_format.py (123 issues)

**Issues breakdown:**
- ~110 W293 (blank lines with whitespace)
- 1 F401 (unused import: `ValidationResult`)
- 5 E501 (lines too long at lines 33, 211, 217, 411, 463, 482, 535)
- 3 W291 (trailing whitespace at lines 25, 211, 367, 527)
- 1 W292 (no newline at end of file)

**Fix approach:**
1. Remove unused import at line 10: `ValidationResult`
2. Break long lines (>110 chars) at lines 33, 211, 217, 411, 463, 482, 535
3. Remove trailing whitespace at lines 25, 211, 367, 527
4. Add newline at end of file
5. Remove all W293 whitespace from blank lines

**Verification:**
- Run `flake8 kivy_garden/markdownlabel/tests/meta_tests/test_comment_format.py` to confirm all issues resolved

---

### File 9: kivy_garden/markdownlabel/tests/meta_tests/test_comment_standardizer.py (219 issues)

**Issues breakdown:**
- ~190 W293 (blank lines with whitespace)
- 2 F401 (unused imports: `re`, `StandardizationResult`)
- ~20 E501 (lines too long at multiple locations)
- 6 W291 (trailing whitespace at lines 33, 160, 296, 350, 412, 462, 494, 542, 581, 791)
- 1 E303 (too many blank lines at line 506)
- 1 E302 (expected 2 blank lines at line 845)
- 1 E129 (visual indentation issue at line 754)
- 1 W292 (no newline at end of file)

**Fix approach:**
1. Remove unused imports:
   - Line 9: Remove `re`
   - Line 13: Remove `StandardizationResult`
2. Break all long lines (>110 chars)
3. Remove trailing whitespace at all W291 locations
4. Fix E303 at line 506: Remove one blank line
5. Fix E302 at line 845: Add 1 blank line before class/function
6. Fix E129 at line 754: Adjust indentation
7. Add newline at end of file
8. Remove all W293 whitespace from blank lines

**Verification:**
- Run `flake8 kivy_garden/markdownlabel/tests/meta_tests/test_comment_standardizer.py` to confirm all issues resolved

---

### File 10: kivy_garden/markdownlabel/tests/meta_tests/test_coverage_preservation.py (67 issues)

**Issues breakdown:**
- ~60 W293 (blank lines with whitespace)
- 7 F401 (unused imports: `hypothesis.assume`, `subprocess`, `json`, `pathlib.Path`, `typing.List`, `typing.Dict`, `typing.Optional`)
- 1 W292 (no newline at end of file)

**Fix approach:**
1. Remove unused imports:
   - Line 9: Remove `hypothesis.assume`
   - Line 12: Remove `subprocess`
   - Line 13: Remove `json`
   - Line 14: Remove `pathlib.Path`
   - Line 15: Remove `typing.List`, `typing.Dict`, and `typing.Optional`
2. Add newline at end of file
3. Remove all W293 whitespace from blank lines

**Verification:**
- Run `flake8 kivy_garden/markdownlabel/tests/meta_tests/test_coverage_preservation.py` to confirm all issues resolved

---

## General Fixing Guidelines

### For W293 (Blank line contains whitespace)
- Use text editor's "remove trailing whitespace" feature
- Or manually replace blank lines with only spaces/tabs with completely empty lines

### For F401 (Imported but unused)
- Remove the unused import statement
- If the import is needed but marked as unused, add `# noqa: F401` comment

### For W291 (Trailing whitespace)
- Remove spaces/tabs at end of lines
- Use regex: ` +$` to find and replace with empty string

### For E501 (Line too long)
- Break long lines using parentheses for continuation
- Use string concatenation for long strings
- Use implicit line continuation for long expressions

### For W292 (No newline at end of file)
- Add a single newline character at the end of the file

### For E301/E302/E303 (Blank line issues)
- E301: Add 1 blank line before class/function definitions
- E302: Add 2 blank lines before top-level class/function definitions
- E303: Remove extra blank lines (keep to 2 maximum)

### For E129 (Visual indentation)
- Adjust indentation to match PEP 8 standards
- Use consistent indentation for continued lines

## Execution Strategy

1. **One file at a time**: Each subtask will handle exactly one file
2. **Verification after each fix**: Run flake8 to confirm all issues are resolved
3. **No context switching**: Complete one file completely before moving to the next
4. **Preserve functionality**: Only fix linting issues, do not change logic

## Success Criteria

For each file:
- ✅ All flake8 issues resolved (zero exit code)
- ✅ No new issues introduced
- ✅ Code functionality unchanged
- ✅ File passes flake8 linting

## Total Issues Summary

| File | Issues | Primary Types |
|-------|---------|---------------|
| __init__.py | 330 | W293, F401, W291, E305 |
| inline_renderer.py | 54 | W293, W291 |
| kivy_renderer.py | 190 | W293, W291 |
| markdown_serializer.py | 109 | W293, E303, E301 |
| conftest.py | 1 | W292 |
| test_assertion_analyzer.py | 49 | F401, W293, E501, W292 |
| test_code_duplication_minimization.py | 69 | F401, W293, E501, W292 |
| test_comment_format.py | 123 | F401, W293, E501, W291, W292 |
| test_comment_standardizer.py | 219 | F401, W293, E501, W291, E303, E302, E129, W292 |
| test_coverage_preservation.py | 67 | F401, W293, W292 |
| **Total** | **1,211** | |

## Notes

- The flake8 configuration appears to use a line length of 110 characters (default is 79)
- W293 issues are the most common and can be fixed with automated tools
- F401 issues require careful review to ensure imports aren't actually needed
- E501 issues may require code restructuring in some cases
