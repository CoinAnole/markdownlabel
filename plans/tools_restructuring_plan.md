# Tools Directory Restructuring Plan

## Overview

This plan reorganizes the tools directory to achieve clear separation between:
1. **Developer utilities** (CLI scripts for manual execution)
2. **Test infrastructure** (modules imported by tests)

## Current State

```
tools/
├── measure_baseline_performance.py      # CLI tool
├── validate_comments.py                 # CLI tool
├── validate_refactoring.py              # CLI tool
├── README.md                          # Documentation
├── hooks/pre-commit                   # Git hook
├── test_optimization/                 # ❌ Imported by tests (wrong location)
│   ├── __init__.py
│   ├── comment_manager.py
│   ├── file_analyzer.py
│   ├── max_examples_calculator.py
│   ├── optimization_detector.py
│   └── strategy_analyzer.py
└── modules/                         # ❌ Imported by tests (wrong location)
    ├── __init__.py
    ├── assertion_analyzer.py
    ├── duplicate_detector.py
    ├── file_parser.py
    ├── naming_convention_validator.py
    └── test_discovery.py

kivy_garden/markdownlabel/tests/
├── test_file_analyzer.py             # ❌ Imports from tools.test_optimization
├── test_strategy_classification.py      # ❌ Imports from tools.test_optimization
├── test_comment_format.py             # ❌ Imports from tools.test_optimization
├── test_comment_standardizer.py       # ❌ Imports from tools.test_optimization
└── meta_tests/                      # ✅ Meta-tests (correct location)
    ├── test_assertion_analyzer.py
    ├── test_code_duplication_minimization.py
    ├── test_coverage_preservation.py
    ├── test_duplicate_detector.py
    ├── test_naming_convention_validator.py
    └── test_test_file_parser.py
```

## Target State

```
tools/
├── measure_baseline_performance.py      # ✅ CLI tool (unchanged)
├── validate_comments.py                 # ✅ CLI tool (unchanged)
├── validate_refactoring.py              # ✅ CLI tool (unchanged)
├── README.md                          # ✅ Documentation (updated)
└── hooks/pre-commit                   # ✅ Git hook (unchanged)

kivy_garden/markdownlabel/tests/
├── test_optimization/                 # ✅ Test infrastructure (moved)
│   ├── __init__.py
│   ├── comment_manager.py
│   ├── file_analyzer.py
│   ├── max_examples_calculator.py
│   ├── optimization_detector.py
│   └── strategy_analyzer.py
├── modules/                         # ✅ Test infrastructure (moved)
│   ├── __init__.py
│   ├── assertion_analyzer.py
│   ├── duplicate_detector.py
│   ├── file_parser.py
│   ├── naming_convention_validator.py
│   └── test_discovery.py
├── test_file_analyzer.py             # ✅ Updated imports
├── test_strategy_classification.py      # ✅ Updated imports
├── test_comment_format.py             # ✅ Updated imports
├── test_comment_standardizer.py       # ✅ Updated imports
└── meta_tests/                      # ✅ Meta-tests (unchanged)
    ├── test_assertion_analyzer.py
    ├── test_code_duplication_minimization.py
    ├── test_coverage_preservation.py
    ├── test_duplicate_detector.py
    ├── test_naming_convention_validator.py
    └── test_test_file_parser.py
```

---

## Phase 1: Move test_optimization Package

**Objective**: Move test_optimization from tools/ to tests/ directory

### Steps

1.1 Create target directory
```bash
mkdir -p kivy_garden/markdownlabel/tests/test_optimization
```

1.2 Move all files from tools/test_optimization/
```bash
mv tools/test_optimization/__init__.py kivy_garden/markdownlabel/tests/test_optimization/
mv tools/test_optimization/comment_manager.py kivy_garden/markdownlabel/tests/test_optimization/
mv tools/test_optimization/file_analyzer.py kivy_garden/markdownlabel/tests/test_optimization/
mv tools/test_optimization/max_examples_calculator.py kivy_garden/markdownlabel/tests/test_optimization/
mv tools/test_optimization/optimization_detector.py kivy_garden/markdownlabel/tests/test_optimization/
mv tools/test_optimization/strategy_analyzer.py kivy_garden/markdownlabel/tests/test_optimization/
```

1.3 Remove empty tools/test_optimization directory
```bash
rmdir tools/test_optimization
```

### Files Affected
- `tools/test_optimization/__init__.py`
- `tools/test_optimization/comment_manager.py`
- `tools/test_optimization/file_analyzer.py`
- `tools/test_optimization/max_examples_calculator.py`
- `tools/test_optimization/optimization_detector.py`
- `tools/test_optimization/strategy_analyzer.py`

---

## Phase 2: Move test_analysis Package

**Objective**: Move test_analysis from tools/ to tests/ directory

### Steps

2.1 Create target directory
```bash
mkdir -p kivy_garden/markdownlabel/tests/modules
```

2.2 Move all files from tools/test_analysis/
```bash
mv tools/test_analysis/__init__.py kivy_garden/markdownlabel/tests/modules/
mv tools/test_analysis/assertion_analyzer.py kivy_garden/markdownlabel/tests/modules/
mv tools/test_analysis/duplicate_detector.py kivy_garden/markdownlabel/tests/modules/
mv tools/test_analysis/file_parser.py kivy_garden/markdownlabel/tests/modules/
mv tools/test_analysis/naming_convention_validator.py kivy_garden/markdownlabel/tests/modules/
mv tools/test_analysis/test_discovery.py kivy_garden/markdownlabel/tests/modules/
```

2.3 Remove empty tools/test_analysis directory
```bash
rmdir tools/test_analysis
```

### Files Affected
- `tools/test_analysis/__init__.py`
- `tools/test_analysis/assertion_analyzer.py`
- `tools/test_analysis/duplicate_detector.py`
- `tools/test_analysis/file_parser.py`
- `tools/test_analysis/naming_convention_validator.py`
- `tools/test_analysis/test_discovery.py`

---

## Phase 3: Update Import Statements

**Objective**: Update all import statements to use new paths

### Files to Update

#### 3.1 test_file_analyzer.py

**Current imports** (lines 14-18):
```python
from tools.test_optimization.file_analyzer import (
    FileAnalyzer, PropertyTest, OptimizationRecommendation,
)
from tools.test_optimization.strategy_analyzer import StrategyType, StrategyAnalysis
```

**New imports**:
```python
from kivy_garden.markdownlabel.tests.test_optimization.file_analyzer import (
    FileAnalyzer, PropertyTest, OptimizationRecommendation,
)
from kivy_garden.markdownlabel.tests.test_optimization.strategy_analyzer import StrategyType, StrategyAnalysis
```

#### 3.2 test_strategy_classification.py

**Current imports** (lines 10-12):
```python
from tools.test_optimization.strategy_analyzer import (
    StrategyClassifier, StrategyType, StrategyAnalysis
)
```

**New imports**:
```python
from kivy_garden.markdownlabel.tests.test_optimization.strategy_analyzer import (
    StrategyClassifier, StrategyType, StrategyAnalysis
)
```

#### 3.3 test_comment_format.py

**Current imports** (lines 10-13):
```python
from tools.test_optimization.comment_manager import (
    CommentFormatValidator, CommentPattern, StrategyType, ValidationResult, CommentAnalyzer
)
from tools.test_optimization.strategy_analyzer import StrategyTypeMapper, CodeAnalyzer
```

**New imports**:
```python
from kivy_garden.markdownlabel.tests.test_optimization.comment_manager import (
    CommentFormatValidator, CommentPattern, StrategyType, ValidationResult, CommentAnalyzer
)
from kivy_garden.markdownlabel.tests.test_optimization.strategy_analyzer import StrategyTypeMapper, CodeAnalyzer
```

#### 3.4 test_comment_standardizer.py

**Current imports** (lines 13-17):
```python
from tools.test_optimization.comment_manager import (
    CommentStandardizer, StandardizationResult, StrategyType, CommentFormatValidator, CommentAnalyzer
)
from tools.test_optimization.optimization_detector import (
    OptimizationDetector as PerformanceRationaleDetector,
)
```

**New imports**:
```python
from kivy_garden.markdownlabel.tests.test_optimization.comment_manager import (
    CommentStandardizer, StandardizationResult, StrategyType, CommentFormatValidator, CommentAnalyzer
)
from kivy_garden.markdownlabel.tests.test_optimization.optimization_detector import (
    OptimizationDetector as PerformanceRationaleDetector,
)
```

#### 3.5 Meta-tests in tests/meta_tests/

**Current imports** (all files):
```python
from tools.test_analysis.assertion_analyzer import AssertionAnalyzer, AssertionType, AssertionPattern, AssertionAnalysis
from tools.test_analysis.duplicate_detector import DuplicateDetector, DuplicateGroup, ConsolidationReport
from tools.test_analysis.file_parser import FileParser, FileMetadata
from tools.test_analysis.naming_convention_validator import NamingConventionValidator, NamingViolationType, NamingViolation
```

**New imports**:
```python
from kivy_garden.markdownlabel.tests.modules.assertion_analyzer import AssertionAnalyzer, AssertionType, AssertionPattern, AssertionAnalysis
from kivy_garden.markdownlabel.tests.modules.duplicate_detector import DuplicateDetector, DuplicateGroup, ConsolidationReport
from kivy_garden.markdownlabel.tests.modules.file_parser import FileParser, FileMetadata
from kivy_garden.markdownlabel.tests.modules.naming_convention_validator import NamingConventionValidator, NamingViolationType, NamingViolation
```

**Files affected**:
- `kivy_garden/markdownlabel/tests/meta_tests/test_assertion_analyzer.py`
- `kivy_garden/markdownlabel/tests/meta_tests/test_duplicate_detector.py`
- `kivy_garden/markdownlabel/tests/meta_tests/test_naming_convention_validator.py`
- `kivy_garden/markdownlabel/tests/meta_tests/test_test_file_parser.py`
- `kivy_garden/markdownlabel/tests/meta_tests/test_code_duplication_minimization.py`

#### 3.6 CLI tools that import from moved packages

**validate_comments.py** (line 19):
```python
from test_optimization.comment_manager import CommentAnalyzer, DirectoryAnalysis, CommentStandardizer, BatchResult
from test_optimization.file_analyzer import FileAnalyzer
```

**New imports**:
```python
from kivy_garden.markdownlabel.tests.test_optimization.comment_manager import CommentAnalyzer, DirectoryAnalysis, CommentStandardizer, BatchResult
from kivy_garden.markdownlabel.tests.test_optimization.file_analyzer import FileAnalyzer
```

**validate_refactoring.py** (line 22):
```python
from test_analysis.duplicate_detector import DuplicateDetector, ConsolidationReport
```

**New imports**:
```python
from kivy_garden.markdownlabel.tests.modules.duplicate_detector import DuplicateDetector, ConsolidationReport
```

**measure_baseline_performance.py** (line 22):
```python
from test_optimization.file_analyzer import FileAnalyzer
```

**New imports**:
```python
from kivy_garden.markdownlabel.tests.test_optimization.file_analyzer import FileAnalyzer
```

---

## Phase 4: Update Documentation

**Objective**: Update tools/README.md to reflect new structure

### Changes to tools/README.md

**Remove** sections referencing:
- `test_optimization/` package
- `modules/` package

**Update** to clarify that tools/ now contains only:
- CLI scripts for manual execution
- Developer utilities
- Pre-commit hooks

**Add** note that test infrastructure has been moved to `kivy_garden/markdownlabel/tests/`

---

## Phase 5: Verify Tests Work

**Objective**: Ensure all tests pass after restructuring

### Steps

5.1 Run full test suite
```bash
pytest kivy_garden/markdownlabel/tests/ -v
```

5.2 Run meta-tests specifically
```bash
pytest kivy_garden/markdownlabel/tests/meta_tests/ -v
```

5.3 Test CLI tools still work
```bash
python tools/validate_comments.py validate kivy_garden/markdownlabel/tests/
python tools/measure_baseline_performance.py
python tools/validate_refactoring.py
```

5.4 Check for import errors
```bash
python -c "from kivy_garden.markdownlabel.tests.test_optimization.file_analyzer import FileAnalyzer"
python -c "from kivy_garden.markdownlabel.tests.modules.assertion_analyzer import AssertionAnalyzer"
```

---

## Phase 6: Cleanup

**Objective**: Remove any empty directories or unused files

### Steps

6.1 Check for empty directories
```bash
find tools/ -type d -empty
find kivy_garden/markdownlabel/tests/ -type d -empty
```

6.2 Remove empty directories if any exist

6.3 Verify no leftover references to old paths
```bash
grep -r "from tools\.test_optimization" kivy_garden/markdownlabel/tests/
grep -r "from tools\.test_analysis" kivy_garden/markdownlabel/tests/
grep -r "from.*test_analysis" kivy_garden/markdownlabel/tests/
```

---

## Rollback Plan

If any issues arise during restructuring:

1. **Rollback Phase 3**: Revert import changes
2. **Rollback Phase 2**: Move modules back to test_analysis/
3. **Rollback Phase 1**: Move meta_tests back to tools/test_analysis/

```bash
# Rollback commands
mv kivy_garden/markdownlabel/tests/modules kivy_garden/markdownlabel/tests/test_analysis
mv kivy_garden/markdownlabel/tests/meta_tests kivy_garden/markdownlabel/tests/tools/test_analysis
git checkout -- kivy_garden/markdownlabel/tests/*.py
git checkout -- tools/*.py
```

---

## Success Criteria

- [ ] All test files can import from new locations
- [ ] All tests pass without errors
- [ ] CLI tools still function correctly
- [ ] No references to old `tools.test_*` imports remain
- [ ] Documentation reflects new structure
- [ ] No empty directories remain
- [ ] Meta-tests pass
- [ ] Pre-commit hook still works

---

## Estimated Impact

**Files moved**: 12
**Files modified**: 10
**Import statements updated**: 16
**Documentation updated**: 1

**Risk level**: Medium (mechanical changes, but extensive)
**Testing required**: Comprehensive (all test suites and CLI tools)
