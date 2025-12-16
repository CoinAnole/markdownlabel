# Test Optimization Tools

This directory contains tools for analyzing and optimizing Hypothesis property-based tests in the MarkdownLabel test suite.

## Overview

The test-performance-optimization spec identified that many tests were using `max_examples=100` regardless of input complexity, leading to unnecessary test execution time. These tools help identify and fix over-testing patterns.

## Tools

### `test_optimization/` Package

Core optimization infrastructure:

- **`strategy_classifier.py`** - Classifies Hypothesis strategies by input space size and complexity
- **`max_examples_calculator.py`** - Calculates optimal max_examples values based on strategy analysis  
- **`test_file_analyzer.py`** - Analyzes test files to identify optimization opportunities
- **`over_testing_validator.py`** - Validates test suite for over-testing patterns with CI integration

### `analyze_tests.py` Script

Command-line tool to analyze the entire test suite:

```bash
python3 tools/analyze_tests.py
```

This script:
- Scans all test files for property-based tests
- Identifies over-testing cases where `max_examples` exceeds optimal values
- Generates detailed recommendations with time savings estimates
- Provides actionable optimization suggestions

## Usage Examples

### Analyze Test Suite

```bash
# Run full analysis
python3 tools/analyze_tests.py

# Example output:
# 📊 ANALYSIS SUMMARY
# Total property tests found: 331
# Over-tested cases: 57
# Potential time savings: 14.0%
# Estimated time reduction: 416.5 seconds
```

### Use in Python Code

```python
from tools.test_optimization import FileAnalyzer, OverTestingValidator

# Basic analysis
analyzer = FileAnalyzer()
report = analyzer.validate_test_suite('kivy_garden/markdownlabel/tests/')

for file_analysis in report.file_analyses:
    for rec in file_analysis.recommendations:
        print(f"{rec.test_name}: {rec.current_examples} → {rec.recommended_examples}")

# CI validation with pass/fail
validator = OverTestingValidator()
result = validator.validate_test_suite('kivy_garden/markdownlabel/tests/')
if not result.passed:
    print(f"FAIL: {len(result.critical_violations)} critical violations found")
    exit(1)
```

## Optimization Guidelines

### Strategy Types and Recommended max_examples

1. **Boolean strategies** (`st.booleans()`) → `max_examples=2`
   - Only 2 possible values (True/False)
   
2. **Small finite strategies** (≤10 values) → `max_examples=input_space_size`
   - `st.integers(min_value=0, max_value=4)` → `max_examples=5`
   - `st.sampled_from(['a', 'b', 'c'])` → `max_examples=3`

3. **Medium finite strategies** (11-50 values) → `max_examples=min(input_space_size, 20)`
   - Capped to prevent excessive execution time

4. **Combination strategies** → `max_examples=product_of_components` (capped at 50)
   - `st.tuples(st.booleans(), st.booleans())` → `max_examples=4` (2×2)

5. **Complex/infinite strategies** → `max_examples=10-50` based on complexity
   - `st.text()`, `st.floats()`, large ranges

### CI Optimization

Tests support CI-aware optimization:

```python
@settings(max_examples=20 if not os.getenv('CI') else 10, deadline=None)
```

- Finite strategies maintain full coverage in CI
- Complex strategies can be reduced for faster CI runs

## Integration

### Pre-commit Hook

Add to `.git/hooks/pre-commit`:

```bash
#!/bin/bash
python3 tools/analyze_tests.py
if [ $? -ne 0 ]; then
    echo "❌ Over-testing detected. Please optimize max_examples values."
    exit 1
fi
```

### CI Integration

Add to GitHub Actions workflow:

```yaml
- name: Check for over-testing
  run: python3 tools/analyze_tests.py
```

## Related Documentation

- `HYPOTHESIS_OPTIMIZATION_GUIDELINES.md` - Detailed optimization guidelines
- `kivy_garden/markdownlabel/tests/test_strategy_classification.py` - Tests for the optimization system
- `kivy_garden/markdownlabel/tests/test_file_analyzer.py` - Tests for the file analyzer