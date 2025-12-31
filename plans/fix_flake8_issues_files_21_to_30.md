# Plan: Fix Flake8 Issues - Files 21 to 30

## Overview
This plan addresses fixing flake8 linting issues in files 21-30 from the 53 split files. Each file will be addressed in a separate subtask to avoid context bloat and agent confusion.

## Issue Types Summary

The flake8 issues fall into these categories:

- **W293**: Blank line contains whitespace (most common)
- **F401**: Imported but unused
- **W291**: Trailing whitespace
- **E501**: Line too long (>110 characters)
- **W292**: No newline at end of file
- **E129**: Visually indented line with same indent as next logical line
- **F541**: f-string is missing placeholders
- **F811**: Redefinition of unused import
- **E301**: Expected 1 blank line
- **E303**: Too many blank lines
- **W391**: Blank line at end of file

## File-by-File Plan

### File 21: kivy_garden/markdownlabel/tests/modules/duplicate_detector.py (65 issues)

**Issues breakdown:**
- ~56 W293 (blank lines with whitespace)
- 4 F401 (unused imports: `typing.Set`, `typing.Tuple`, `typing.Optional`, `ast`, `.file_parser.FileMetadata`)
- 2 W291 (trailing whitespace at lines 209 and 250)
- 1 E129 (visual indentation at line 251)
- 2 F541 (f-string missing placeholders at lines 271 and 277)
- 1 W292 (no newline at end of file)

**Fix approach:**
1. Remove unused imports:
   - Line 9: Remove `typing.Set`, `typing.Tuple`, and `typing.Optional`
   - Line 12: Remove `ast`
   - Line 14: Remove `.file_parser.FileMetadata`
2. Remove trailing whitespace at lines 209 and 250
3. Fix E129 at line 251: Adjust indentation to match PEP 8 standards
4. Fix F541 at lines 271 and 277: Convert f-strings without placeholders to regular strings
5. Add newline at end of file
6. Remove all W293 whitespace from blank lines throughout the file

**Verification:**
- Run `flake8 kivy_garden/markdownlabel/tests/modules/duplicate_detector.py` to confirm all issues resolved

---

### File 22: kivy_garden/markdownlabel/tests/modules/file_analyzer.py (81 issues)

**Issues breakdown:**
- ~75 W293 (blank lines with whitespace)
- 2 F401 (unused imports: `ast`, `typing.Dict`)
- 2 E501 (lines too long at lines 16 and 456)
- 4 W291 (trailing whitespace at lines 351, 382, 400, 431)
- 3 E129 (visual indentation at lines 352, 402)
- 1 W292 (no newline at end of file)

**Fix approach:**
1. Remove unused imports:
   - Line 8: Remove `ast`
   - Line 11: Remove `typing.Dict`
2. Break long lines (>110 chars) at lines 16 and 456
3. Remove trailing whitespace at lines 351, 382, 400, 431
4. Fix E129 at lines 352 and 402: Adjust indentation to match PEP 8 standards
5. Add newline at end of file
6. Remove all W293 whitespace from blank lines

**Verification:**
- Run `flake8 kivy_garden/markdownlabel/tests/modules/file_analyzer.py` to confirm all issues resolved

---

### File 23: kivy_garden/markdownlabel/tests/modules/file_parser.py (57 issues)

**Issues breakdown:**
- ~53 W293 (blank lines with whitespace)
- 1 F401 (unused import: `typing.Any`)
- 1 E129 (visual indentation at line 175)
- 3 W291 (trailing whitespace at lines 271, 282, 292)
- 1 W292 (no newline at end of file)

**Fix approach:**
1. Remove unused import at line 11: `typing.Any`
2. Fix E129 at line 175: Adjust indentation to match PEP 8 standards
3. Remove trailing whitespace at lines 271, 282, 292
4. Add newline at end of file
5. Remove all W293 whitespace from blank lines

**Verification:**
- Run `flake8 kivy_garden/markdownlabel/tests/modules/file_parser.py` to confirm all issues resolved

---

### File 24: kivy_garden/markdownlabel/tests/modules/max_examples_calculator.py (37 issues)

**Issues breakdown:**
- ~34 W293 (blank lines with whitespace)
- 2 W291 (trailing whitespace at lines 33 and 103)
- 1 W292 (no newline at end of file)

**Fix approach:**
1. Remove trailing whitespace at lines 33 and 103
2. Add newline at end of file
3. Remove all W293 whitespace from blank lines

**Verification:**
- Run `flake8 kivy_garden/markdownlabel/tests/modules/max_examples_calculator.py` to confirm all issues resolved

---

### File 25: kivy_garden/markdownlabel/tests/modules/naming_convention_validator.py (81 issues)

**Issues breakdown:**
- ~77 W293 (blank lines with whitespace)
- 2 F401 (unused imports: `typing.Set`, `typing.Tuple`)
- 1 F811 (redefinition of unused `Path` from line 12 at line 19)
- 1 E501 (line too long at line 130)
- 1 W291 (trailing whitespace at line 78)
- 1 W292 (no newline at end of file)

**Fix approach:**
1. Remove unused imports:
   - Line 10: Remove `typing.Set` and `typing.Tuple`
2. Remove redefinition at line 19: Remove the duplicate `Path` import
3. Break long line (>110 chars) at line 130
4. Remove trailing whitespace at line 78
5. Add newline at end of file
6. Remove all W293 whitespace from blank lines

**Verification:**
- Run `flake8 kivy_garden/markdownlabel/tests/modules/naming_convention_validator.py` to confirm all issues resolved

---

### File 26: kivy_garden/markdownlabel/tests/modules/optimization_detector.py (183 issues)

**Issues breakdown:**
- ~172 W293 (blank lines with whitespace)
- 2 F401 (unused imports: `.comment_manager.CommentPattern`, `.comment_manager.CommentStrategyClassification`)
- 5 E501 (lines too long at lines 485, 550, 654, 731, 746, 871, 882)
- 5 W291 (trailing whitespace at lines 97, 342, 383, 394, 562, 797)
- 2 E129 (visual indentation at lines 343, 362)

**Fix approach:**
1. Remove unused imports at line 20: `.comment_manager.CommentPattern` and `.comment_manager.CommentStrategyClassification`
2. Break all long lines (>110 chars) at lines 485, 550, 654, 731, 746, 871, 882
3. Remove trailing whitespace at lines 97, 342, 383, 394, 562, 797
4. Fix E129 at lines 343 and 362: Adjust indentation to match PEP 8 standards
5. Remove all W293 whitespace from blank lines

**Verification:**
- Run `flake8 kivy_garden/markdownlabel/tests/modules/optimization_detector.py` to confirm all issues resolved

---

### File 27: kivy_garden/markdownlabel/tests/modules/over_testing_validator.py (68 issues)

**Issues breakdown:**
- ~60 W293 (blank lines with whitespace)
- 4 F401 (unused imports: `os`, `pathlib.Path`, `typing.Dict`, `typing.Tuple`)
- 4 E501 (lines too long at lines 198, 203, 277, 279)
- 4 W291 (trailing whitespace at lines 59, 116, 130, 159, 294)
- 1 E129 (visual indentation at line 117)
- 1 F541 (f-string missing placeholders at line 320)
- 1 W292 (no newline at end of file)

**Fix approach:**
1. Remove unused imports:
   - Line 9: Remove `os`
   - Line 11: Remove `pathlib.Path`
   - Line 12: Remove `typing.Dict` and `typing.Tuple`
2. Break long lines (>110 chars) at lines 198, 203, 277, 279
3. Remove trailing whitespace at lines 59, 116, 130, 159, 294
4. Fix E129 at line 117: Adjust indentation to match PEP 8 standards
5. Fix F541 at line 320: Convert f-string without placeholders to regular string
6. Add newline at end of file
7. Remove all W293 whitespace from blank lines

**Verification:**
- Run `flake8 kivy_garden/markdownlabel/tests/modules/over_testing_validator.py` to confirm all issues resolved

---

### File 28: kivy_garden/markdownlabel/tests/modules/strategy_analyzer.py (82 issues)

**Issues breakdown:**
- ~80 W293 (blank lines with whitespace)
- 2 F401 (unused imports: `typing.Dict`, `typing.Any`)
- 1 E501 (line too long at line 40)

**Fix approach:**
1. Remove unused imports at line 11: `typing.Dict` and `typing.Any`
2. Break long line (>110 chars) at line 40
3. Remove all W293 whitespace from blank lines

**Verification:**
- Run `flake8 kivy_garden/markdownlabel/tests/modules/strategy_analyzer.py` to confirm all issues resolved

---

### File 29: kivy_garden/markdownlabel/tests/modules/test_discovery.py (54 issues)

**Issues breakdown:**
- ~53 W293 (blank lines with whitespace)
- 1 F401 (unused import: `typing.Tuple`)
- 1 E501 (line too long at line 182)

**Fix approach:**
1. Remove unused import at line 16: `typing.Tuple`
2. Break long line (>110 chars) at line 182
3. Remove all W293 whitespace from blank lines

**Verification:**
- Run `flake8 kivy_garden/markdownlabel/tests/modules/test_discovery.py` to confirm all issues resolved

---

### File 30: kivy_garden/markdownlabel/tests/test_advanced_compatibility.py (207 issues)

**Issues breakdown:**
- ~200 W293 (blank lines with whitespace)
- 10 F401 (unused imports: `kivy.uix.label.Label`, `.test_utils.markdown_heading`, `.test_utils.markdown_paragraph`, `.test_utils.markdown_bold`, `.test_utils.markdown_italic`, `.test_utils.markdown_link`, `.test_utils.color_strategy`, `.test_utils.text_padding_strategy`, `.test_utils.padding_equal`, `.test_utils.KIVY_FONTS`)
- 1 E301 (expected 1 blank line at line 636)
- 3 E303 (too many blank lines at lines 762, 794, 825)
- 1 W391 (blank line at end of file at line 1002)

**Fix approach:**
1. Remove unused imports:
   - Line 16: Remove `kivy.uix.label.Label`
   - Line 19: Remove all `.test_utils` imports: `markdown_heading`, `markdown_paragraph`, `markdown_bold`, `markdown_italic`, `markdown_link`, `color_strategy`, `text_padding_strategy`, `padding_equal`, `KIVY_FONTS`
2. Fix E301 at line 636: Add 1 blank line before the function/class definition
3. Fix E303 at lines 762, 794, 825: Remove one blank line at each location
4. Fix W391 at end of file: Remove trailing blank line at line 1002
5. Remove all W293 whitespace from blank lines

**Verification:**
- Run `flake8 kivy_garden/markdownlabel/tests/test_advanced_compatibility.py` to confirm all issues resolved

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

### For E301 (Expected 1 blank line)
- Add 1 blank line before class/function definitions

### For E303 (Too many blank lines)
- Remove extra blank lines (keep to 2 maximum)

### For E129 (Visual indentation)
- Adjust indentation to match PEP 8 standards
- Use consistent indentation for continued lines

### For F811 (Redefinition of unused import)
- Remove the duplicate import statement
- Keep only one instance of the import

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
| duplicate_detector.py | 65 | F401, W293, W291, E129, F541, W292 |
| file_analyzer.py | 81 | F401, W293, E501, W291, E129, W292 |
| file_parser.py | 57 | F401, W293, E129, W291, W292 |
| max_examples_calculator.py | 37 | W293, W291, W292 |
| naming_convention_validator.py | 81 | F401, F811, W293, E501, W291, W292 |
| optimization_detector.py | 183 | F401, W293, E501, W291, E129 |
| over_testing_validator.py | 68 | F401, W293, E501, W291, E129, F541, W292 |
| strategy_analyzer.py | 82 | F401, W293, E501 |
| test_discovery.py | 54 | F401, W293, E501 |
| test_advanced_compatibility.py | 207 | F401, W293, E301, E303, W391 |
| **Total** | **915** | |

## Notes

- The flake8 configuration appears to use a line length of 110 characters (default is 79)
- W293 issues are the most common and can be fixed with automated tools
- F401 issues require careful review to ensure imports aren't actually needed
- E501 issues may require code restructuring in some cases
- File 30 (test_advanced_compatibility.py) has the highest number of issues (207) and will require careful attention
- F541 issues indicate f-strings that don't use placeholders and should be converted to regular strings
- F811 issues indicate duplicate imports that need to be resolved
