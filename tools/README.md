# MarkdownLabel Test Tools

This directory contains CLI tools for analyzing, validating, and optimizing the MarkdownLabel test suite.

## Core Tools

### 1. Comment Validation & Optimization (`tools/validate_comments.py`)
The primary CLI for property-based test maintenance.

```bash
# Analyze test suite for optimization opportunities
python3 tools/validate_comments.py optimize kivy_garden/markdownlabel/tests/

# Validate comment format compliance
python3 tools/validate_comments.py validate kivy_garden/markdownlabel/tests/

# Standardize comment formats (dry run)
python3 tools/validate_comments.py standardize kivy_garden/markdownlabel/tests/ --dry-run
```

### 2. Refactoring Validation (`tools/validate_refactoring.py`)
Measures code quality metrics to validate the success of refactoring efforts.

```bash
python3 tools/validate_refactoring.py
```

### 3. Performance Baselining (`tools/measure_baseline_performance.py`)
Establishes performance baselines for property-based tests.

```bash
python3 tools/measure_baseline_performance.py
```

### 4. Environment Diagnostic (`tools/where_is_markdownlabel.py`)
Shows which `kivy_garden.markdownlabel` module/distribution your Python is importing.

```bash
python3 tools/where_is_markdownlabel.py
```



## Related Documentation

- `TESTING.md` - General testing documentation
