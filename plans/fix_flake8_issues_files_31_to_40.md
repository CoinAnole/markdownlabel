# Plan: Fix Flake8 Issues - Files 31 to 40

## Overview
This plan addresses fixing flake8 linting issues in files 31-40 from the 53 split files. Each file will be addressed in a separate subtask to avoid context bloat and agent confusion.

## Issue Types Summary

The flake8 issues fall into these categories:

- **W293**: Blank line contains whitespace (most common)
- **F401**: Imported but unused
- **W291**: Trailing whitespace
- **E501**: Line too long (>110 characters)
- **W292**: No newline at end of file
- **W391**: Blank line at end of file
- **F541**: f-string is missing placeholders
- **E302**: Expected 2 blank lines
- **E303**: Too many blank lines
- **E122**: Continuation line missing indentation or outdented

## File-by-File Plan

### File 31: kivy_garden/markdownlabel/tests/test_clipping_behavior.py (1 issue)

**Issues breakdown:**
- 1 W391 (blank line at end of file at line 258)

**Fix approach:**
1. Remove the trailing blank line at the end of the file (line 258)

**Verification:**
- Run `flake8 kivy_garden/markdownlabel/tests/test_clipping_behavior.py` to confirm all issues resolved

---

### File 32: kivy_garden/markdownlabel/tests/test_color_properties.py (34 issues)

**Issues breakdown:**
- ~30 W293 (blank lines with whitespace)
- 3 F401 (unused imports: `pytest`, `hypothesis.strategies as st`, `kivy.uix.label.Label`)
- 1 W391 (blank line at end of file at line 178)

**Fix approach:**
1. Remove unused imports:
   - Line 9: Remove `pytest`
   - Line 10: Remove `hypothesis.strategies as st`
   - Line 12: Remove `kivy.uix.label.Label`
2. Fix W391 at end of file: Remove trailing blank line at line 178
3. Remove all W293 whitespace from blank lines throughout the file

**Verification:**
- Run `flake8 kivy_garden/markdownlabel/tests/test_color_properties.py` to confirm all issues resolved

---

### File 33: kivy_garden/markdownlabel/tests/test_core_functionality_properties.py (176 issues)

**Issues breakdown:**
- ~165 W293 (blank lines with whitespace)
- 1 F401 (unused import: `os` at line 8)
- 6 E501 (lines too long at lines 17, 83, 171, 305, 308, 532, 551)
- 10 W291 (trailing whitespace at lines 57, 96, 180, 181, 253, 254, 345, 346, 416, 488, 612, 664, 788, 789)
- 1 F541 (f-string missing placeholders at line 654)
- 1 W292 (no newline at end of file at line 895)

**Fix approach:**
1. Remove unused import at line 8: `os`
2. Break all long lines (>110 chars) at lines 17, 83, 171, 305, 308, 532, 551
3. Remove trailing whitespace at all W291 locations (lines 57, 96, 180, 181, 253, 254, 345, 346, 416, 488, 612, 664, 788, 789)
4. Fix F541 at line 654: Convert f-string without placeholders to regular string
5. Add newline at end of file (line 895)
6. Remove all W293 whitespace from blank lines throughout the file

**Verification:**
- Run `flake8 kivy_garden/markdownlabel/tests/test_core_functionality_properties.py` to confirm all issues resolved

---

### File 34: kivy_garden/markdownlabel/tests/test_core_functionality.py (59 issues)

**Issues breakdown:**
- 58 W293 (blank lines with whitespace)
- 1 F401 (unused import: `kivy.uix.widget.Widget` at line 13)

**Fix approach:**
1. Remove unused import at line 13: `kivy.uix.widget.Widget`
2. Remove all W293 whitespace from blank lines throughout the file

**Verification:**
- Run `flake8 kivy_garden/markdownlabel/tests/test_core_functionality.py` to confirm all issues resolved

---

### File 35: kivy_garden/markdownlabel/tests/test_font_properties.py (180 issues)

**Issues breakdown:**
- ~165 W293 (blank lines with whitespace)
- 1 F401 (unused import: `.test_utils.is_code_label` at line 15)
- 2 W291 (trailing whitespace at lines 312, 505)
- 6 F541 (f-string missing placeholders at lines 364, 388, 413, 438, 458, 481, 513)
- 3 E122 (continuation line missing indentation at lines 498, 499, 500)
- 5 E501 (lines too long at lines 606, 769, 812, 851, 921)

**Fix approach:**
1. Remove unused import at line 15: `.test_utils.is_code_label`
2. Remove trailing whitespace at lines 312 and 505
3. Fix F541 at lines 364, 388, 413, 438, 458, 481, 513: Convert f-strings without placeholders to regular strings
4. Fix E122 at lines 498, 499, 500: Adjust continuation line indentation to match PEP 8 standards
5. Break all long lines (>110 chars) at lines 606, 769, 812, 851, 921
6. Remove all W293 whitespace from blank lines throughout the file

**Verification:**
- Run `flake8 kivy_garden/markdownlabel/tests/test_font_properties.py` to confirm all issues resolved

---

### File 36: kivy_garden/markdownlabel/tests/test_import.py (3 issues)

**Issues breakdown:**
- 2 W293 (blank lines with whitespace at lines 13 and 19)
- 1 F401 (unused import: `pytest` at line 8)

**Fix approach:**
1. Remove unused import at line 8: `pytest`
2. Remove all W293 whitespace from blank lines at lines 13 and 19

**Verification:**
- Run `flake8 kivy_garden/markdownlabel/tests/test_import.py` to confirm all issues resolved

---

### File 37: kivy_garden/markdownlabel/tests/test_inline_renderer.py (128 issues)

**Issues breakdown:**
- ~115 W293 (blank lines with whitespace)
- 1 F401 (unused import: `os` at line 9)
- ~15 E501 (lines too long at lines 438, 439, 451, 452, 575, 603, 689, 690, 694, 696, 710, 714, 729, 733, 734, 735, 736, 763, 764, 767, 768)

**Fix approach:**
1. Remove unused import at line 9: `os`
2. Break all long lines (>110 chars) at lines 438, 439, 451, 452, 575, 603, 689, 690, 694, 696, 710, 714, 729, 733, 734, 735, 736, 763, 764, 767, 768
3. Remove all W293 whitespace from blank lines throughout the file

**Verification:**
- Run `flake8 kivy_garden/markdownlabel/tests/test_inline_renderer.py` to confirm all issues resolved

---

### File 38: kivy_garden/markdownlabel/tests/test_kivy_renderer.py (95 issues)

**Issues breakdown:**
- ~85 W293 (blank lines with whitespace)
- 4 F401 (unused imports: `os` at line 8, `.test_utils.list_item_token`, `.test_utils.table_cell_token`, `.test_utils.table_row_token` at line 20)
- 4 E303 (too many blank lines at lines 111, 141, 269, 707)
- 4 E302 (expected 2 blank lines at lines 115, 147, 274, 711)
- 5 F541 (f-string missing placeholders at lines 184, 188, 204, 207, 296)
- 1 W291 (trailing whitespace at line 504)

**Fix approach:**
1. Remove unused imports:
   - Line 8: Remove `os`
   - Line 20: Remove `.test_utils.list_item_token`, `.test_utils.table_cell_token`, and `.test_utils.table_row_token`
2. Fix E303 at lines 111, 141, 269, 707: Remove one blank line at each location (3 → 2 blank lines)
3. Fix E302 at lines 115, 147, 274, 711: Add 1 blank line before the function/class definition (1 → 2 blank lines)
4. Fix F541 at lines 184, 188, 204, 207, 296: Convert f-strings without placeholders to regular strings
5. Remove trailing whitespace at line 504
6. Remove all W293 whitespace from blank lines throughout the file

**Verification:**
- Run `flake8 kivy_garden/markdownlabel/tests/test_kivy_renderer.py` to confirm all issues resolved

---

### File 39: kivy_garden/markdownlabel/tests/test_label_compatibility.py (73 issues)

**Issues breakdown:**
- ~60 W293 (blank lines with whitespace)
- 10 F401 (unused imports: `importlib`, `os`, `sys` at lines 8-10, `kivy_garden.markdownlabel.tests.test_label_compatibility` at line 437, and 6 test_utils imports at line 465)
- 2 E501 (lines too long at lines 231, 501)
- 4 W291 (trailing whitespace at lines 231, 232, 425)
- 1 W292 (no newline at end of file at line 514)

**Fix approach:**
1. Remove unused imports:
   - Lines 8-10: Remove `importlib`, `os`, and `sys`
   - Line 437: Remove `kivy_garden.markdownlabel.tests.test_label_compatibility`
   - Line 465: Remove `.test_utils.markdown_bold`, `.test_utils.markdown_italic`, `.test_utils.markdown_link`, `.test_utils.padding_equal`, `.test_utils.floats_equal`, `.test_utils.color_strategy`, `.test_utils.text_padding_strategy`
2. Break long lines (>110 chars) at lines 231 and 501
3. Remove trailing whitespace at lines 231, 232, and 425
4. Add newline at end of file (line 514)
5. Remove all W293 whitespace from blank lines throughout the file

**Verification:**
- Run `flake8 kivy_garden/markdownlabel/tests/test_label_compatibility.py` to confirm all issues resolved

---

### File 40: kivy_garden/markdownlabel/tests/test_padding_properties.py (120 issues)

**Issues breakdown:**
- ~115 W293 (blank lines with whitespace)
- 1 F401 (unused import: `pytest` at line 8)
- 3 W291 (trailing whitespace at lines 129, 636, 637)
- 1 E501 (line too long at line 374)

**Fix approach:**
1. Remove unused import at line 8: `pytest`
2. Remove trailing whitespace at lines 129, 636, and 637
3. Break long line (>110 chars) at line 374
4. Remove all W293 whitespace from blank lines throughout the file

**Verification:**
- Run `flake8 kivy_garden/markdownlabel/tests/test_padding_properties.py` to confirm all issues resolved

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

### For F541 (f-string is missing placeholders)
- Convert f-strings without placeholders to regular strings
- Use `str()` instead of `f"{}"`

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
| test_clipping_behavior.py | 1 | W391 |
| test_color_properties.py | 34 | F401, W293, W391 |
| test_core_functionality_properties.py | 176 | F401, E501, W293, W291, F541, W292 |
| test_core_functionality.py | 59 | F401, W293 |
| test_font_properties.py | 180 | F401, W293, W291, F541, E122, E501 |
| test_import.py | 3 | F401, W293 |
| test_inline_renderer.py | 128 | F401, W293, E501 |
| test_kivy_renderer.py | 95 | F401, W293, E303, E302, F541, W291 |
| test_label_compatibility.py | 73 | F401, W293, E501, W291, W292 |
| test_padding_properties.py | 120 | F401, W293, W291, E501 |
| **Total** | **869** | |

## Notes

- The flake8 configuration appears to use a line length of 110 characters (default is 79)
- W293 issues are the most common and can be fixed with automated tools
- F401 issues require careful review to ensure imports aren't actually needed
- E501 issues may require code restructuring in some cases
- File 35 (test_font_properties.py) has the highest number of issues (180) and will require careful attention
- F541 issues indicate f-strings that don't use placeholders and should be converted to regular strings
- E122 issues in test_font_properties.py indicate continuation line indentation problems that need to be fixed
- E303 and E302 issues in test_kivy_renderer.py indicate blank line spacing problems around function/class definitions
