# Directory Renaming Plan

## Overview

This plan clarifies the test directory structure by renaming directories to better reflect their purpose:

- **`test_analysis/` → `modules/`** - Contains utility modules imported by tests
- **`tools/test_analysis/` → `meta_tests/`** - Contains meta-tests (tests that test the test infrastructure)

## Rationale

The current naming is confusing because:
1. `test_analysis/` sounds like it contains test files, but it actually contains utility modules
2. `tools/test_analysis/` is nested under `tools/` which is meant for CLI utilities, not test files

The new names make the purpose immediately clear:
- `modules/` - clearly indicates these are reusable modules
- `meta_tests/` - clearly indicates these are tests about tests

## Current Structure

```
kivy_garden/markdownlabel/tests/
├── test_analysis/                              # ❌ Confusing name
│   ├── __init__.py
│   ├── assertion_analyzer.py                  # Module imported by tests
│   ├── duplicate_detector.py                  # Module imported by tests
│   ├── file_parser.py                          # Module imported by tests
│   ├── naming_convention_validator.py          # Module imported by tests
│   └── test_discovery.py                       # Module imported by tests
├── tools/test_analysis/                        # ❌ Wrong location & confusing
│   ├── test_assertion_analyzer.py              # Meta-test
│   ├── test_code_duplication_minimization.py   # Meta-test
│   ├── test_coverage_preservation.py           # Meta-test
│   ├── test_duplicate_detector.py              # Meta-test
│   ├── test_naming_convention_validator.py     # Meta-test
│   └── test_test_file_parser.py                # Meta-test
└── test_optimization/                          # ✅ Already in correct location
    └── (imports from test_analysis)
```

## Target Structure

```
kivy_garden/markdownlabel/tests/
├── modules/                                    # ✅ Clear: utility modules
│   ├── __init__.py
│   ├── assertion_analyzer.py
│   ├── duplicate_detector.py
│   ├── file_parser.py
│   ├── naming_convention_validator.py
│   └── test_discovery.py
├── meta_tests/                                 # ✅ Clear: meta-tests
│   ├── test_assertion_analyzer.py
│   ├── test_code_duplication_minimization.py
│   ├── test_coverage_preservation.py
│   ├── test_duplicate_detector.py
│   ├── test_naming_convention_validator.py
│   └── test_test_file_parser.py
└── test_optimization/                          # ✅ Imports from modules
    └── (imports from modules)
```

## Phase 1: Rename Directories

### 1.1 Rename test_analysis/ to modules/

```bash
# Rename the directory
mv kivy_garden/markdownlabel/tests/test_analysis kivy_garden/markdownlabel/tests/modules
```

**Files moved:**
- `kivy_garden/markdownlabel/tests/test_analysis/__init__.py` → `modules/__init__.py`
- `kivy_garden/markdownlabel/tests/test_analysis/assertion_analyzer.py` → `modules/assertion_analyzer.py`
- `kivy_garden/markdownlabel/tests/test_analysis/duplicate_detector.py` → `modules/duplicate_detector.py`
- `kivy_garden/markdownlabel/tests/test_analysis/file_parser.py` → `modules/file_parser.py`
- `kivy_garden/markdownlabel/tests/test_analysis/naming_convention_validator.py` → `modules/naming_convention_validator.py`
- `kivy_garden/markdownlabel/tests/test_analysis/test_discovery.py` → `modules/test_discovery.py`

### 1.2 Rename tools/test_analysis/ to meta_tests/

```bash
# Rename the directory
mv kivy_garden/markdownlabel/tests/tools/test_analysis kivy_garden/markdownlabel/tests/meta_tests
```

**Files moved:**
- `kivy_garden/markdownlabel/tests/tools/test_analysis/test_assertion_analyzer.py` → `meta_tests/test_assertion_analyzer.py`
- `kivy_garden/markdownlabel/tests/tools/test_analysis/test_code_duplication_minimization.py` → `meta_tests/test_code_duplication_minimization.py`
- `kivy_garden/markdownlabel/tests/tools/test_analysis/test_coverage_preservation.py` → `meta_tests/test_coverage_preservation.py`
- `kivy_garden/markdownlabel/tests/tools/test_analysis/test_duplicate_detector.py` → `meta_tests/test_duplicate_detector.py`
- `kivy_garden/markdownlabel/tests/tools/test_analysis/test_naming_convention_validator.py` → `meta_tests/test_naming_convention_validator.py`
- `kivy_garden/markdownlabel/tests/tools/test_analysis/test_test_file_parser.py` → `meta_tests/test_test_file_parser.py`

### 1.3 Remove empty tools/ directory

```bash
# Check if tools/ directory is empty after move
ls kivy_garden/markdownlabel/tests/tools/

# If empty, remove it
rmdir kivy_garden/markdownlabel/tests/tools
```

## Phase 2: Update Import Statements

### 2.1 Update tools/validate_refactoring.py

**Current import (line 22):**
```python
from kivy_garden.markdownlabel.tests.test_analysis.duplicate_detector import DuplicateDetector, ConsolidationReport
```

**New import:**
```python
from kivy_garden.markdownlabel.tests.modules.duplicate_detector import DuplicateDetector, ConsolidationReport
```

### 2.2 Update meta_tests/test_assertion_analyzer.py

**Current import (line 17):**
```python
from kivy_garden.markdownlabel.tests.test_analysis.assertion_analyzer import AssertionAnalyzer, AssertionType, AssertionPattern, AssertionAnalysis
```

**New import:**
```python
from kivy_garden.markdownlabel.tests.modules.assertion_analyzer import AssertionAnalyzer, AssertionType, AssertionPattern, AssertionAnalysis
```

### 2.3 Update meta_tests/test_test_file_parser.py

**Current import (line 14):**
```python
from kivy_garden.markdownlabel.tests.test_analysis.file_parser import FileParser, FileMetadata
```

**New import:**
```python
from kivy_garden.markdownlabel.tests.modules.file_parser import FileParser, FileMetadata
```

### 2.4 Update meta_tests/test_code_duplication_minimization.py

**Current import (line 15):**
```python
from kivy_garden.markdownlabel.tests.test_analysis.duplicate_detector import DuplicateDetector, ConsolidationReport
```

**New import:**
```python
from kivy_garden.markdownlabel.tests.modules.duplicate_detector import DuplicateDetector, ConsolidationReport
```

### 2.5 Update meta_tests/test_duplicate_detector.py

**Current import (line 14):**
```python
from kivy_garden.markdownlabel.tests.test_analysis.duplicate_detector import DuplicateDetector, DuplicateGroup, ConsolidationReport
```

**New import:**
```python
from kivy_garden.markdownlabel.tests.modules.duplicate_detector import DuplicateDetector, DuplicateGroup, ConsolidationReport
```

### 2.6 Update meta_tests/test_naming_convention_validator.py

**Current imports (lines 16-19):**
```python
from kivy_garden.markdownlabel.tests.test_analysis.naming_convention_validator import (
    NamingConventionValidator, NamingViolationType, NamingViolation
)
from kivy_garden.markdownlabel.tests.test_analysis.assertion_analyzer import AssertionAnalyzer, AssertionType, AssertionAnalysis
```

**New imports:**
```python
from kivy_garden.markdownlabel.tests.modules.naming_convention_validator import (
    NamingConventionValidator, NamingViolationType, NamingViolation
)
from kivy_garden.markdownlabel.tests.modules.assertion_analyzer import AssertionAnalyzer, AssertionType, AssertionAnalysis
```

### 2.7 Update test_optimization/file_analyzer.py

**Current import (line 16):**
```python
from kivy_garden.markdownlabel.tests.test_analysis.test_discovery import find_property_tests as shared_find_property_tests
```

**New import:**
```python
from kivy_garden.markdownlabel.tests.modules.test_discovery import find_property_tests as shared_find_property_tests
```

### 2.8 Update test_optimization/optimization_detector.py

**Current import (line 28):**
```python
from kivy_garden.markdownlabel.tests.test_analysis.test_discovery import find_property_tests, PropertyTest
```

**New import:**
```python
from kivy_garden.markdownlabel.tests.modules.test_discovery import find_property_tests, PropertyTest
```

## Phase 3: Update Documentation

### 3.1 Update tools/README.md

**Remove or update references to `test_analysis/`:**

Current section (lines 63-67):
```markdown
- `test_analysis/` - Infrastructure for general test suite analysis
  - `file_parser.py` - AST-based parser for test metadata extraction
  - `duplicate_detector.py` - Identifies redundant helper functions
  - `assertion_analyzer.py` - Validates assertion patterns against test names
  - `naming_convention_validator.py` - Enforces consistent test naming
```

Replace with:
```markdown
- `modules/` - Infrastructure for test suite analysis
  - `file_parser.py` - AST-based parser for test metadata extraction
  - `duplicate_detector.py` - Identifies redundant helper functions
  - `assertion_analyzer.py` - Validates assertion patterns against test names
  - `naming_convention_validator.py` - Enforces consistent test naming
  - `test_discovery.py` - Discovers and analyzes test files
```

### 3.2 Update kivy_garden/markdownlabel/tests/TESTING.md

Search for any references to `test_analysis` or `tools/test_analysis` and update to `modules` and `meta_tests`.

### 3.3 Update plans/tools_restructuring_plan.md

Update all references to reflect the new directory names.

## Phase 4: Verify Tests Work

### 4.1 Run full test suite

```bash
pytest kivy_garden/markdownlabel/tests/ -v
```

### 4.2 Run meta-tests specifically

```bash
pytest kivy_garden/markdownlabel/tests/meta_tests/ -v
```

### 4.3 Test CLI tools still work

```bash
python tools/validate_refactoring.py
```

### 4.4 Check for import errors

```bash
python -c "from kivy_garden.markdownlabel.tests.modules.assertion_analyzer import AssertionAnalyzer"
python -c "from kivy_garden.markdownlabel.tests.modules.duplicate_detector import DuplicateDetector"
python -c "from kivy_garden.markdownlabel.tests.modules.file_parser import FileParser"
python -c "from kivy_garden.markdownlabel.tests.modules.naming_convention_validator import NamingConventionValidator"
python -c "from kivy_garden.markdownlabel.tests.modules.test_discovery import find_property_tests"
```

## Phase 5: Cleanup

### 5.1 Verify no empty directories remain

```bash
find kivy_garden/markdownlabel/tests/ -type d -empty
```

### 5.2 Verify no references to old paths remain

```bash
grep -r "test_analysis" kivy_garden/markdownlabel/tests/ --include="*.py"
grep -r "tools/test_analysis" . --include="*.py"
grep -r "from.*test_analysis" . --include="*.md"
```

## Rollback Plan

If any issues arise during restructuring:

```bash
# Rollback directory renames
mv kivy_garden/markdownlabel/tests/modules kivy_garden/markdownlabel/tests/test_analysis
mv kivy_garden/markdownlabel/tests/meta_tests kivy_garden/markdownlabel/tests/tools/test_analysis

# Revert import changes
git checkout -- kivy_garden/markdownlabel/tests/*.py
git checkout -- tools/*.py
git checkout -- kivy_garden/markdownlabel/tests/test_optimization/*.py

# Revert documentation changes
git checkout -- *.md
```

## Success Criteria

- [ ] Directories successfully renamed to `modules/` and `meta_tests/`
- [ ] All imports updated to use new paths
- [ ] All tests pass without errors
- [ ] CLI tools still function correctly
- [ ] No references to old `test_analysis` or `tools/test_analysis` paths remain
- [ ] Documentation reflects new structure
- [ ] No empty directories remain
- [ ] Meta-tests pass

## Files Summary

**Directories renamed:** 2
**Files moved:** 12
**Import statements updated:** 8 files
**Documentation files updated:** 3 (tools/README.md, TESTING.md, tools_restructuring_plan.md)

**Risk level:** Low (mechanical renames with clear import path updates)
**Testing required:** Standard (all test suites and CLI tools)

## Benefits

1. **Clarity:** New names immediately convey the purpose of each directory
2. **Maintainability:** Easier for new contributors to understand the structure
3. **Consistency:** Aligns with common Python project patterns
4. **Documentation:** Reduces confusion about what each directory contains
