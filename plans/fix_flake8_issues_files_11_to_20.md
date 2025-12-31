# Plan: Fix Flake8 Issues - Files 11 to 20

## Overview
This plan addresses fixing flake8 linting issues in files 11-20 from the 53 split files. Each file will be addressed in a separate subtask to avoid context bloat and agent confusion.

## Issue Types Summary

The flake8 issues fall into these categories:

- **W293**: Blank line contains whitespace (most common)
- **F401**: Imported but unused
- **W291**: Trailing whitespace
- **E501**: Line too long (>110 characters)
- **W292**: No newline at end of file
- **E303**: Too many blank lines
- **E302**: Expected 2 blank lines
- **E129**: Visually indented line with same indent as next logical line
- **F811**: Redefinition of unused import
- **W391**: Blank line at end of file

## File-by-File Plan

### File 11: kivy_garden/markdownlabel/tests/meta_tests/test_documentation_compliance.py (35 issues)

**Issues breakdown:**
- ~30 W293 (blank lines with whitespace)
- 3 E501 (lines too long at lines 135, 150, 172)
- 1 W291 (trailing whitespace at line 21)
- 1 W292 (no newline at end of file)

**Fix approach:**
1. Break long lines (>110 chars) at lines 135, 150, 172
2. Remove trailing whitespace at line 21
3. Add newline at end of file
4. Remove all W293 whitespace from blank lines throughout the file

**Verification:**
- Run `flake8 kivy_garden/markdownlabel/tests/meta_tests/test_documentation_compliance.py` to confirm all issues resolved

---

### File 12: kivy_garden/markdownlabel/tests/meta_tests/test_duplicate_detector.py (53 issues)

**Issues breakdown:**
- ~47 W293 (blank lines with whitespace)
- 4 F401 (unused imports: `hypothesis.assume`, `pathlib.Path`, `DuplicateGroup`, `ConsolidationReport`)
- 2 E501 (lines too long at lines 14, 73)
- 1 W292 (no newline at end of file)

**Fix approach:**
1. Remove unused imports:
   - Line 9: Remove `hypothesis.assume`
   - Line 12: Remove `pathlib.Path`
   - Line 14: Remove `DuplicateGroup` and `ConsolidationReport` from the import statement
2. Break long lines (>110 chars) at lines 14 and 73
3. Add newline at end of file
4. Remove all W293 whitespace from blank lines

**Verification:**
- Run `flake8 kivy_garden/markdownlabel/tests/meta_tests/test_duplicate_detector.py` to confirm all issues resolved

---

### File 13: kivy_garden/markdownlabel/tests/meta_tests/test_file_analyzer.py (85 issues)

**Issues breakdown:**
- ~80 W293 (blank lines with whitespace)
- 2 F401 (unused imports: `PropertyTest`, `OptimizationRecommendation`)
- 1 E501 (line too long at line 462)
- 2 W291 (trailing whitespace at lines 369, 471)
- 1 W292 (no newline at end of file)

**Fix approach:**
1. Remove unused imports at line 14: `PropertyTest` and `OptimizationRecommendation`
2. Break long line (>110 chars) at line 462
3. Remove trailing whitespace at lines 369 and 471
4. Add newline at end of file
5. Remove all W293 whitespace from blank lines

**Verification:**
- Run `flake8 kivy_garden/markdownlabel/tests/meta_tests/test_file_analyzer.py` to confirm all issues resolved

---

### File 14: kivy_garden/markdownlabel/tests/meta_tests/test_helper_availability.py (45 issues)

**Issues breakdown:**
- ~39 W293 (blank lines with whitespace)
- 4 F401 (unused imports: `BoxLayout` at line 11, `os` at lines 195 and 229, `ast` at line 263)
- 1 W292 (no newline at end of file)

**Fix approach:**
1. Remove unused imports:
   - Line 11: Remove `kivy.uix.boxlayout.BoxLayout`
   - Line 195: Remove `os` import
   - Line 229: Remove `os` import
   - Line 263: Remove `ast` import
2. Add newline at end of file
3. Remove all W293 whitespace from blank lines

**Verification:**
- Run `flake8 kivy_garden/markdownlabel/tests/meta_tests/test_helper_availability.py` to confirm all issues resolved

---

### File 15: kivy_garden/markdownlabel/tests/meta_tests/test_naming_convention_validator.py (63 issues)

**Issues breakdown:**
- ~53 W293 (blank lines with whitespace)
- 4 F401 (unused imports: `pathlib.Path`, `NamingViolation`, `AssertionType`, `AssertionAnalysis`)
- 6 E501 (lines too long at lines 19, 78, 97, 107, 116, 142, 160)
- 1 W291 (trailing whitespace at line 263)
- 1 W292 (no newline at end of file)

**Fix approach:**
1. Remove unused imports:
   - Line 14: Remove `pathlib.Path`
   - Line 16: Remove `NamingViolation`
   - Line 19: Remove `AssertionType` and `AssertionAnalysis`
2. Break long lines (>110 chars) at lines 19, 78, 97, 107, 116, 142, 160
3. Remove trailing whitespace at line 263
4. Add newline at end of file
5. Remove all W293 whitespace from blank lines

**Verification:**
- Run `flake8 kivy_garden/markdownlabel/tests/meta_tests/test_naming_convention_validator.py` to confirm all issues resolved

---

### File 16: kivy_garden/markdownlabel/tests/meta_tests/test_strategy_classification.py (87 issues)

**Issues breakdown:**
- ~70 W293 (blank lines with whitespace)
- 1 F401 (unused import: `StrategyAnalysis` at line 10)
- 1 F811 (redefinition of unused `StrategyAnalysis` at line 168)
- 10 E501 (lines too long at lines 124, 137, 181, 202, 212, 238, 247, 257, 322, 335, 373, 378, 382)
- 2 E302 (expected 2 blank lines at lines 183, 283)
- 1 W292 (no newline at end of file)

**Fix approach:**
1. Remove unused import at line 10: `StrategyAnalysis`
2. Remove redefinition at line 168: Remove the duplicate `StrategyAnalysis` import
3. Break all long lines (>110 chars) at lines 124, 137, 181, 202, 212, 238, 247, 257, 322, 335, 373, 378, 382
4. Fix E302 at line 183: Add 1 blank line before the function/class definition
5. Fix E302 at line 283: Add 1 blank line before the function/class definition
6. Add newline at end of file
7. Remove all W293 whitespace from blank lines

**Verification:**
- Run `flake8 kivy_garden/markdownlabel/tests/meta_tests/test_strategy_classification.py` to confirm all issues resolved

---

### File 17: kivy_garden/markdownlabel/tests/meta_tests/test_test_file_parser.py (38 issues)

**Issues breakdown:**
- ~32 W293 (blank lines with whitespace)
- 2 F401 (unused imports: `hypothesis.assume`, `pathlib.Path`)
- 1 E501 (line too long at line 70)
- 3 W291 (trailing whitespace at lines 177, 215, 220)

**Fix approach:**
1. Remove unused imports:
   - Line 9: Remove `hypothesis.assume`
   - Line 12: Remove `pathlib.Path`
2. Break long line (>110 chars) at line 70
3. Remove trailing whitespace at lines 177, 215, 220
4. Remove all W293 whitespace from blank lines

**Verification:**
- Run `flake8 kivy_garden/markdownlabel/tests/meta_tests/test_test_file_parser.py` to confirm all issues resolved

---

### File 18: kivy_garden/markdownlabel/tests/modules/__init__.py (10 issues)

**Issues breakdown:**
- 10 W293 (blank lines with whitespace at lines 146, 163, 168, 177, 184, 187, 193, 201, 206, 212)

**Fix approach:**
1. Remove all W293 whitespace from blank lines at the specified line numbers

**Verification:**
- Run `flake8 kivy_garden/markdownlabel/tests/modules/__init__.py` to confirm all issues resolved

---

### File 19: kivy_garden/markdownlabel/tests/modules/assertion_analyzer.py (64 issues)

**Issues breakdown:**
- ~60 W293 (blank lines with whitespace)
- 1 F401 (unused import: `typing.Set`)
- 2 E501 (lines too long at lines 200, 293)
- 1 W292 (no newline at end of file)

**Fix approach:**
1. Remove unused import at line 11: `typing.Set`
2. Break long lines (>110 chars) at lines 200 and 293
3. Add newline at end of file
4. Remove all W293 whitespace from blank lines

**Verification:**
- Run `flake8 kivy_garden/markdownlabel/tests/modules/assertion_analyzer.py` to confirm all issues resolved

---

### File 20: kivy_garden/markdownlabel/tests/modules/comment_manager.py (336 issues)

**Issues breakdown:**
- ~310 W293 (blank lines with whitespace)
- 2 F401 (unused imports: `pathlib.Path`, `typing.Set`)
- ~20 E501 (lines too long at multiple locations)
- ~7 W291 (trailing whitespace at lines 208, 312, 564, 640, 667, 779, 780, 1209, 1404, 1635)
- 1 E303 (too many blank lines at line 869)
- 1 E129 (visual indentation issue at line 1637)
- 1 W292 (no newline at end of file)
- 1 W391 (blank line at end of file at line 1918)

**Fix approach:**
1. Remove unused imports:
   - Line 21: Remove `pathlib.Path`
   - Line 22: Remove `typing.Set`
2. Break all long lines (>110 chars) throughout the file
3. Remove trailing whitespace at all W291 locations
4. Fix E303 at line 869: Remove one blank line
5. Fix E129 at line 1637: Adjust indentation
6. Fix W292 and W391 at end of file: Ensure single newline at end, remove extra blank lines
7. Remove all W293 whitespace from blank lines

**Verification:**
- Run `flake8 kivy_garden/markdownlabel/tests/modules/comment_manager.py` to confirm all issues resolved

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

### For W391 (Blank line at end of file)
- Remove trailing blank lines at the end of the file
- Ensure the file ends with a single newline character

### For E302 (Expected 2 blank lines)
- Add blank lines before top-level class/function definitions
- Ensure there are exactly 2 blank lines before top-level definitions

### For E303 (Too many blank lines)
- Remove extra blank lines (keep to 2 maximum)

### For E129 (Visual indentation)
- Adjust indentation to match PEP 8 standards
- Use consistent indentation for continued lines

### For F811 (Redefinition of unused import)
- Remove the duplicate import statement
- Keep only one instance of the import

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
|------|---------|---------------|
| test_documentation_compliance.py | 35 | W293, E501, W291, W292 |
| test_duplicate_detector.py | 53 | F401, W293, E501, W292 |
| test_file_analyzer.py | 85 | F401, W293, E501, W291, W292 |
| test_helper_availability.py | 45 | F401, W293, W292 |
| test_naming_convention_validator.py | 63 | F401, W293, E501, W291, W292 |
| test_strategy_classification.py | 87 | F401, F811, W293, E501, E302, W292 |
| test_test_file_parser.py | 38 | F401, W293, E501, W291 |
| __init__.py (modules) | 10 | W293 |
| assertion_analyzer.py | 64 | F401, W293, E501, W292 |
| comment_manager.py | 336 | F401, W293, E501, W291, E303, E129, W292, W391 |
| **Total** | **816** | |

## Notes

- The flake8 configuration appears to use a line length of 110 characters (default is 79)
- W293 issues are the most common and can be fixed with automated tools
- F401 issues require careful review to ensure imports aren't actually needed
- E501 issues may require code restructuring in some cases
- File 20 (comment_manager.py) has the highest number of issues (336) and will require careful attention
- F811 issue in test_strategy_classification.py indicates a duplicate import that needs to be resolved
