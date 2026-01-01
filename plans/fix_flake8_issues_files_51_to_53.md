# Plan: Fix Flake8 Issues - Files 51 to 53 (Final Batch)

## Overview
This plan addresses fixing flake8 linting issues in the final 3 files (51-53) from the 53 split files. Each file will be addressed in a separate subtask to avoid context bloat and agent confusion.

## Issue Types Summary

The flake8 issues fall into these categories:

- **W293**: Blank line contains whitespace (most common)
- **F401**: Imported but unused
- **F541**: f-string is missing placeholders
- **E501**: Line too long (>110 characters)
- **W291**: Trailing whitespace
- **E129**: Visually indented line with same indent as next logical line
- **W292**: No newline at end of file

## File-by-File Plan

### File 51: kivy_garden/markdownlabel/tests/test_texture_render_mode.py (124 issues)

**Issues breakdown:**
- 3 F401 (unused imports: `hypothesis.assume` at line 14, `kivy.uix.label.Label` at line 16, `kivy.uix.image.Image` at line 17)
- ~117 W293 (blank lines with whitespace at lines 31, 41, 52, 56, 59, 70, 74, 77, 88, 92, 96, 103, 106, 124, 127, 138, 144, 147, 158, 163, 170, 181, 200, 204, 207, 219, 225, 228, 231, 234, 238, 241, 247, 251, 272, 281, 290, 295, 298, 301, 303, 307, 310, 318, 321, 333, 338, 341, 344, 346, 350, 352, 356, 360, 378, 387, 396, 401, 404, 407, 409, 413, 416, 420, 424, 427, 439, 447, 450, 453, 455, 459, 463, 468, 471, 474, 486, 493, 496, 499, 501, 505, 530, 533, 536, 547, 555, 558, 563, 568, 571, 581, 589, 591, 596, 606, 609, 618, 622, 625, 636, 640, 643, 653, 657, 660, 670, 674, 683, 693, 697, 700, 711, 715, 718, 727)
- 4 F541 (f-string missing placeholders at lines 317, 423, 470, 512)
- 1 E501 (line too long at line 696: 117 > 110 characters)

**Fix approach:**
1. Remove unused imports:
   - Line 14: Remove `hypothesis.assume`
   - Line 16: Remove `kivy.uix.label.Label`
   - Line 17: Remove `kivy.uix.image.Image`
2. Fix F541 at lines 317, 423, 470, 512: Convert f-strings without placeholders to regular strings
3. Break long line (>110 chars) at line 696
4. Remove all W293 whitespace from blank lines throughout the file

**Verification:**
- Run `flake8 kivy_garden/markdownlabel/tests/test_texture_render_mode.py` to confirm all issues resolved

---

### File 52: kivy_garden/markdownlabel/tests/test_texture_sizing.py (86 issues)

**Issues breakdown:**
- 3 F401 (unused imports: `kivy.uix.boxlayout.BoxLayout` at line 11, `kivy.uix.label.Label` at line 12, `.test_utils.find_labels_recursive` at line 16)
- ~76 W293 (blank lines with whitespace at lines 37, 44, 46, 51, 58, 60, 65, 69, 74, 81, 85, 90, 97, 99, 103, 108, 113, 117, 122, 127, 131, 136, 141, 145, 149, 154, 159, 163, 168, 173, 175, 180, 189, 192, 197, 214, 216, 220, 224, 231, 233, 235, 239, 244, 252, 256, 261, 266, 270, 275, 283, 286, 301, 304, 311, 313, 318, 322, 330, 334, 339, 344, 347, 351, 354, 359, 373, 378, 386, 392, 397, 402, 408, 412, 416)
- 4 F541 (f-string missing placeholders at lines 196, 296, 298, 300)
- 2 W291 (trailing whitespace at lines 382, 383)
- 1 E129 (visual indentation at line 384)

**Fix approach:**
1. Remove unused imports:
   - Line 11: Remove `kivy.uix.boxlayout.BoxLayout`
   - Line 12: Remove `kivy.uix.label.Label`
   - Line 16: Remove `.test_utils.find_labels_recursive`
2. Fix F541 at lines 196, 296, 298, 300: Convert f-strings without placeholders to regular strings
3. Remove trailing whitespace at lines 382 and 383
4. Fix E129 at line 384: Adjust indentation to match PEP 8 standards
5. Remove all W293 whitespace from blank lines throughout the file

**Verification:**
- Run `flake8 kivy_garden/markdownlabel/tests/test_texture_sizing.py` to confirm all issues resolved

---

### File 53: kivy_garden/markdownlabel/tests/test_utils.py (109 issues)

**Issues breakdown:**
- 1 F401 (unused import: `typing.Set` at line 13)
- ~105 W293 (blank lines with whitespace at lines 20, 26, 106, 115, 154, 157, 177, 194, 214, 217, 223, 226, 240, 259, 279, 299, 303, 313, 324, 329, 338, 348, 352, 360, 364, 367, 373, 393, 397, 403, 406, 410, 416, 421, 432, 437, 448, 453, 464, 469, 473, 486, 489, 494, 499, 502, 507, 510, 515, 520, 530, 534, 540, 543, 547, 553, 556, 559, 571, 574, 578, 589, 593, 599, 602, 606, 612, 616, 622, 626, 630, 636, 640, 647, 652, 661, 664, 670, 675, 678, 686, 690, 693, 703, 707, 722, 732, 740, 747, 751, 758, 764, 768, 774, 781, 785, 798, 800, 808, 813, 815, 823, 826, 830, 836, 842)
- 1 F541 (f-string missing placeholders at line 502)
- 1 W291 (trailing whitespace at line 509)
- 1 W292 (no newline at end of file at line 843)

**Fix approach:**
1. Remove unused import at line 13: `typing.Set`
2. Fix F541 at line 502: Convert f-string without placeholders to regular string
3. Remove trailing whitespace at line 509
4. Add newline at end of file (line 843)
5. Remove all W293 whitespace from blank lines throughout the file

**Verification:**
- Run `flake8 kivy_garden/markdownlabel/tests/test_utils.py` to confirm all issues resolved

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

### For E129 (Visual indentation)
- Adjust indentation to match PEP 8 standards
- Use consistent indentation for continued lines

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
| test_texture_render_mode.py | 124 | F401, W293, F541, E501 |
| test_texture_sizing.py | 86 | F401, W293, F541, W291, E129 |
| test_utils.py | 109 | F401, W293, F541, W291, W292 |
| **Total** | **319** | |

## Notes

- The flake8 configuration appears to use a line length of 110 characters (default is 79)
- W293 issues are the most common and can be fixed with automated tools
- F401 issues require careful review to ensure imports aren't actually needed
- E501 issues may require code restructuring in some cases
- File 51 (test_texture_render_mode.py) has the highest number of issues (124) in this batch
- F541 issues indicate f-strings that don't use placeholders and should be converted to regular strings
- E129 issue in test_texture_sizing.py indicates a visual indentation problem that needs to be fixed
- This is the final batch of 3 files, completing the 53-file flake8 issue fixing project

## Project Completion Summary

After completing this final batch (files 51-53), the entire flake8 issue fixing project will be complete:

- **Total files processed**: 53 files
- **Total issues addressed**: 5,331 issues
- **Batches completed**: 6 batches
  - Batch 1 (files 1-10): 1,211 issues
  - Batch 2 (files 11-20): 816 issues
  - Batch 3 (files 21-30): 915 issues
  - Batch 4 (files 31-40): 869 issues
  - Batch 5 (files 41-50): 1,219 issues
  - Batch 6 (files 51-53): 319 issues (this batch)

All files will pass flake8 linting with zero issues upon completion of this final batch.
