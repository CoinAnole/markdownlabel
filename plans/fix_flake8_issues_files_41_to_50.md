# Plan: Fix Flake8 Issues - Files 41 to 50

## Overview
This plan addresses fixing flake8 linting issues in files 41-50 from the 53 split files. Each file will be addressed in a separate subtask to avoid context bloat and agent confusion.

## Issue Types Summary

The flake8 issues fall into these categories:

- **W293**: Blank line contains whitespace (most common)
- **F401**: Imported but unused
- **W291**: Trailing whitespace
- **E501**: Line too long (>110 characters)
- **W292**: No newline at end of file
- **W391**: Blank line at end of file
- **E303**: Too many blank lines
- **E302**: Expected 2 blank lines
- **E122**: Continuation line missing indentation or outdented
- **F541**: f-string is missing placeholders
- **F402**: Import shadowed by loop variable
- **E129**: Visually indented line with same indent as next logical line

## File-by-File Plan

### File 41: kivy_garden/markdownlabel/tests/test_performance.py (89 issues)

**Issues breakdown:**
- 15 F401 (unused imports: `BoxLayout`, `Label`, `GridLayout`, and 12 test_utils imports)
- 1 E302 (expected 2 blank lines at line 24)
- 72 W293 (blank lines with whitespace)
- 2 W291 (trailing whitespace at lines 354 and 407)
- 1 W391 (blank line at end of file at line 437)

**Fix approach:**
1. Remove unused imports:
   - Lines 12-14: Remove `kivy.uix.boxlayout.BoxLayout`, `kivy.uix.label.Label`, `kivy.uix.gridlayout.GridLayout`
   - Line 17: Remove all `.test_utils` imports: `markdown_heading`, `markdown_paragraph`, `markdown_bold`, `markdown_italic`, `markdown_link`, `simple_markdown_document`, `color_strategy`, `text_padding_strategy`, `colors_equal`, `padding_equal`, `floats_equal`, `KIVY_FONTS`
2. Fix E302 at line 24: Add 1 blank line before the function/class definition
3. Remove trailing whitespace at lines 354 and 407
4. Fix W391 at end of file: Remove trailing blank line at line 437
5. Remove all W293 whitespace from blank lines throughout the file

**Verification:**
- Run `flake8 kivy_garden/markdownlabel/tests/test_performance.py` to confirm all issues resolved

---

### File 42: kivy_garden/markdownlabel/tests/test_rebuild_scheduling.py (2 issues)

**Issues breakdown:**
- 1 E501 (line too long at line 66)
- 1 W391 (blank line at end of file at line 338)

**Fix approach:**
1. Break long line (>110 chars) at line 66
2. Fix W391 at end of file: Remove trailing blank line at line 338

**Verification:**
- Run `flake8 kivy_garden/markdownlabel/tests/test_rebuild_scheduling.py` to confirm all issues resolved

---

### File 43: kivy_garden/markdownlabel/tests/test_rebuild_semantics.py (213 issues)

**Issues breakdown:**
- 3 F401 (unused imports: `Label`, `Widget`, `.test_utils.color_strategy`)
- 206 W293 (blank lines with whitespace)
- 4 E303 (too many blank lines at lines 80, 271, 362, 589, 762, 914)

**Fix approach:**
1. Remove unused imports:
   - Line 16: Remove `kivy.uix.label.Label`
   - Line 17: Remove `kivy.uix.widget.Widget`
   - Line 20: Remove `.test_utils.color_strategy`
2. Fix E303 at lines 80, 271, 362, 589, 762, 914: Remove one blank line at each location (3 → 2 blank lines)
3. Remove all W293 whitespace from blank lines throughout the file

**Verification:**
- Run `flake8 kivy_garden/markdownlabel/tests/test_rebuild_semantics.py` to confirm all issues resolved

---

### File 44: kivy_garden/markdownlabel/tests/test_refactoring_properties.py (179 issues)

**Issues breakdown:**
- 3 F401 (unused imports: `find_labels_recursive`, `collect_widget_ids`, `re`)
- 1 F402 (import 're' from line 10 shadowed by loop variable at line 586)
- 6 E501 (lines too long at lines 458, 474, 494, 498, 502, 546, 676)
- 3 E122 (continuation line missing indentation at lines 98, 151, 189)
- ~165 W293 (blank lines with whitespace)
- 6 W291 (trailing whitespace at lines 31, 202, 203, 368, 422, 461, 690, 729, 782)
- 1 W292 (no newline at end of file at line 983)

**Fix approach:**
1. Remove unused imports:
   - Line 10: Remove `re`
   - Line 16: Remove `.test_utils.find_labels_recursive` and `.test_utils.collect_widget_ids`
2. Fix F402 at line 586: Rename the loop variable to avoid shadowing the `re` import (or remove the `re` import if not needed)
3. Break all long lines (>110 chars) at lines 458, 474, 494, 498, 502, 546, 676
4. Fix E122 at lines 98, 151, 189: Adjust continuation line indentation to match PEP 8 standards
5. Remove trailing whitespace at all W291 locations
6. Add newline at end of file (line 983)
7. Remove all W293 whitespace from blank lines

**Verification:**
- Run `flake8 kivy_garden/markdownlabel/tests/test_refactoring_properties.py` to confirm all issues resolved

---

### File 45: kivy_garden/markdownlabel/tests/test_rtl_alignment.py (101 issues)

**Issues breakdown:**
- 2 F401 (unused imports: `hypothesis.assume`, `Label`)
- 11 E501 (lines too long at lines 155, 182, 278, 297, 306, 339, 371, 382, 420, 431, 450, 482, 493)
- 2 E303 (too many blank lines at lines 195, 394)
- ~96 W293 (blank lines with whitespace)
- 1 W292 (no newline at end of file at line 549)

**Fix approach:**
1. Remove unused imports:
   - Line 9: Remove `hypothesis.assume`
   - Line 11: Remove `kivy.uix.label.Label`
2. Break all long lines (>110 chars) at lines 155, 182, 278, 297, 306, 339, 371, 382, 420, 431, 450, 482, 493
3. Fix E303 at lines 195 and 394: Remove one blank line at each location (2 → 1 blank line)
4. Add newline at end of file (line 549)
5. Remove all W293 whitespace from blank lines

**Verification:**
- Run `flake8 kivy_garden/markdownlabel/tests/test_rtl_alignment.py` to confirm all issues resolved

---

### File 46: kivy_garden/markdownlabel/tests/test_serialization.py (129 issues)

**Issues breakdown:**
- 6 E501 (lines too long at lines 497, 503, 548, 555)
- 3 W291 (trailing whitespace at lines 448, 449, 509)
- ~120 W293 (blank lines with whitespace)

**Fix approach:**
1. Break all long lines (>110 chars) at lines 497, 503, 548, 555
2. Remove trailing whitespace at lines 448, 449, and 509
3. Remove all W293 whitespace from blank lines

**Verification:**
- Run `flake8 kivy_garden/markdownlabel/tests/test_serialization.py` to confirm all issues resolved

---

### File 47: kivy_garden/markdownlabel/tests/test_shared_infrastructure.py (24 issues)

**Issues breakdown:**
- 2 E501 (lines too long at lines 37 and 157)
- 22 W293 (blank lines with whitespace)

**Fix approach:**
1. Break long lines (>110 chars) at lines 37 and 157
2. Remove all W293 whitespace from blank lines

**Verification:**
- Run `flake8 kivy_garden/markdownlabel/tests/test_shared_infrastructure.py` to confirm all issues resolved

---

### File 48: kivy_garden/markdownlabel/tests/test_shortening_and_coordinate.py (245 issues)

**Issues breakdown:**
- 3 F401 (unused imports: `os`, `Widget`, `GridLayout`)
- 2 F541 (f-string missing placeholders at lines 1020 and 1357)
- 3 E303 (too many blank lines at lines 938, 1030, 1278)
- 1 E302 (expected 2 blank lines at line 1040)
- 2 W291 (trailing whitespace at lines 548 and 566)
- ~235 W293 (blank lines with whitespace)

**Fix approach:**
1. Remove unused imports:
   - Line 12: Remove `os`
   - Line 19: Remove `kivy.uix.widget.Widget`
   - Line 20: Remove `kivy.uix.gridlayout.GridLayout`
2. Fix F541 at lines 1020 and 1357: Convert f-strings without placeholders to regular strings
3. Fix E303 at lines 938, 1030, 1278: Remove one blank line at each location (2 → 1 blank line)
4. Fix E302 at line 1040: Add 1 blank line before the function/class definition (3 → 2 blank lines)
5. Remove trailing whitespace at lines 548 and 566
6. Remove all W293 whitespace from blank lines

**Verification:**
- Run `flake8 kivy_garden/markdownlabel/tests/test_shortening_and_coordinate.py` to confirm all issues resolved

---

### File 49: kivy_garden/markdownlabel/tests/test_sizing_behavior.py (131 issues)

**Issues breakdown:**
- 2 F401 (unused imports: `markdown_paragraph`, `find_labels_recursive`)
- 1 E501 (line too long at line 480)
- 2 E129 (visual indentation at lines 561 and 611)
- 22 W291 (trailing whitespace at multiple locations)
- ~106 W293 (blank lines with whitespace)

**Fix approach:**
1. Remove unused imports at line 12: `.test_utils.markdown_paragraph` and `.test_utils.find_labels_recursive`
2. Break long line (>110 chars) at line 480
3. Fix E129 at lines 561 and 611: Adjust indentation to match PEP 8 standards
4. Remove trailing whitespace at all W291 locations
5. Remove all W293 whitespace from blank lines

**Verification:**
- Run `flake8 kivy_garden/markdownlabel/tests/test_sizing_behavior.py` to confirm all issues resolved

---

### File 50: kivy_garden/markdownlabel/tests/test_text_properties.py (106 issues)

**Issues breakdown:**
- 1 F401 (unused import: `Label` at line 11)
- 5 W291 (trailing whitespace at lines 100, 101, 195, 254)
- ~100 W293 (blank lines with whitespace)

**Fix approach:**
1. Remove unused import at line 11: `kivy.uix.label.Label`
2. Remove trailing whitespace at lines 100, 101, 195, and 254
3. Remove all W293 whitespace from blank lines

**Verification:**
- Run `flake8 kivy_garden/markdownlabel/tests/test_text_properties.py` to confirm all issues resolved

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

### For E122 (Continuation line missing indentation)
- Adjust continuation line indentation to match PEP 8 standards
- Ensure continuation lines are properly indented

### For E129 (Visual indentation)
- Adjust indentation to match PEP 8 standards
- Use consistent indentation for continued lines

### For F541 (f-string is missing placeholders)
- Convert f-strings without placeholders to regular strings
- Use `str()` instead of `f"{}"`

### For F402 (Import shadowed by loop variable)
- Rename the loop variable to avoid shadowing the import
- Or remove the import if not needed

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
| test_performance.py | 89 | F401, W293, E302, W291, W391 |
| test_rebuild_scheduling.py | 2 | E501, W391 |
| test_rebuild_semantics.py | 213 | F401, W293, E303 |
| test_refactoring_properties.py | 179 | F401, F402, W293, E501, E122, W291, W292 |
| test_rtl_alignment.py | 101 | F401, W293, E501, E303, W292 |
| test_serialization.py | 129 | W293, E501, W291 |
| test_shared_infrastructure.py | 24 | W293, E501 |
| test_shortening_and_coordinate.py | 245 | F401, W293, F541, E303, E302, W291 |
| test_sizing_behavior.py | 131 | F401, W293, E501, E129, W291 |
| test_text_properties.py | 106 | F401, W293, W291 |
| **Total** | **1,219** | |

## Notes

- The flake8 configuration appears to use a line length of 110 characters (default is 79)
- W293 issues are the most common and can be fixed with automated tools
- F401 issues require careful review to ensure imports aren't actually needed
- E501 issues may require code restructuring in some cases
- File 48 (test_shortening_and_coordinate.py) has the highest number of issues (245) and will require careful attention
- F541 issues indicate f-strings that don't use placeholders and should be converted to regular strings
- F402 issue in test_refactoring_properties.py indicates a loop variable that shadows an import
- E122 and E129 issues indicate indentation problems that need to be fixed
- E303 and E302 issues indicate blank line spacing problems around function/class definitions
