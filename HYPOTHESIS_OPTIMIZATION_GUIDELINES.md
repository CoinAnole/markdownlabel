# Hypothesis Test Optimization Guidelines

This document provides guidelines for selecting appropriate `max_examples` values in property-based tests to optimize test execution time while maintaining coverage quality.

## Overview

Property-based testing with Hypothesis generates random inputs to verify that properties hold across many examples. However, using excessive `max_examples` values can lead to unnecessary test execution time without proportional coverage benefits.

## Strategy-Based Guidelines

### 1. Boolean Strategies

**Pattern:** `st.booleans()`
**Recommended max_examples:** `2`
**Rationale:** Boolean strategies have exactly 2 possible values (True/False). Testing with more than 2 examples provides no additional coverage.

```python
# ✅ Optimal
@given(st.booleans())
@settings(max_examples=2)
def test_boolean_property(value):
    assert isinstance(value, bool)

# ❌ Over-testing
@given(st.booleans())
@settings(max_examples=100)  # Tests True/False 50x each
def test_boolean_property(value):
    assert isinstance(value, bool)
```

### 2. Small Finite Strategies

**Pattern:** Small integer ranges (≤10 values), small `sampled_from` lists
**Recommended max_examples:** Equal to input space size
**Rationale:** For finite strategies with small input spaces, use exactly the number of possible values to test each value once.

```python
# ✅ Optimal - 6 possible values
@given(st.integers(min_value=1, max_value=6))
@settings(max_examples=6)
def test_dice_roll(value):
    assert 1 <= value <= 6

# ✅ Optimal - 3 possible values
@given(st.sampled_from(['red', 'green', 'blue']))
@settings(max_examples=3)
def test_color_property(color):
    assert color in ['red', 'green', 'blue']

# ❌ Over-testing
@given(st.integers(min_value=1, max_value=6))
@settings(max_examples=100)  # Tests 6 values ~17x each
def test_dice_roll(value):
    assert 1 <= value <= 6
```

### 3. Medium Finite Strategies

**Pattern:** Integer ranges or lists with 11-50 values
**Recommended max_examples:** Input space size, capped at 20-50
**Rationale:** For medium-sized finite strategies, test all values when practical, but cap to prevent excessive execution time.

```python
# ✅ Optimal - 20 possible values
@given(st.integers(min_value=1, max_value=20))
@settings(max_examples=20)
def test_medium_range(value):
    assert 1 <= value <= 20

# ✅ Acceptable - Large range capped at 50
@given(st.integers(min_value=1, max_value=100))
@settings(max_examples=50)
def test_large_range(value):
    assert 1 <= value <= 100
```

### 4. Combination Strategies

**Pattern:** Multiple strategies combined (tuples, multiple @given arguments)
**Recommended max_examples:** Product of individual strategy sizes, capped at 50
**Rationale:** Combination strategies create cartesian products. Calculate the total combinations and cap at reasonable limits.

```python
# ✅ Optimal - 2 × 3 = 6 combinations
@given(st.tuples(st.booleans(), st.sampled_from(['a', 'b', 'c'])))
@settings(max_examples=6)
def test_boolean_enum_combination(value):
    bool_val, enum_val = value
    assert isinstance(bool_val, bool)
    assert enum_val in ['a', 'b', 'c']

# ✅ Optimal - 2 × 2 = 4 combinations
@given(flag=st.booleans(), mode=st.booleans())
@settings(max_examples=4)
def test_two_booleans(flag, mode):
    assert isinstance(flag, bool)
    assert isinstance(mode, bool)

# ✅ Capped - Large combination space
@given(st.tuples(st.integers(1, 20), st.integers(1, 20)))
@settings(max_examples=50)  # 400 combinations capped at 50
def test_large_combination(value):
    x, y = value
    assert x * y > 0
```

### 5. Complex/Infinite Strategies

**Pattern:** `st.text()`, `st.floats()`, large ranges, recursive strategies
**Recommended max_examples:** 10-50 based on complexity
**Rationale:** For infinite or very large input spaces, use moderate example counts based on the complexity of the property being tested.

```python
# ✅ Simple property - lower examples
@given(st.text())
@settings(max_examples=10)
def test_text_length_property(text):
    assert len(text) >= 0

# ✅ Complex property - higher examples
@given(st.text(min_size=1), st.floats(allow_nan=False))
@settings(max_examples=30)
def test_complex_text_float_interaction(text, number):
    result = complex_processing(text, number)
    assert validate_complex_result(result)

# ✅ Very complex property - maximum examples
@given(st.text(), st.lists(st.integers()), st.dictionaries(st.text(), st.floats()))
@settings(max_examples=50)
def test_very_complex_property(text, numbers, mapping):
    # Complex property with multiple interactions
    pass
```

## Environment-Specific Optimizations

### CI Environment

In CI environments, you may further reduce `max_examples` for complex strategies while maintaining full coverage for finite strategies:

```python
import os

def get_max_examples_for_ci(base_examples, strategy_type):
    """Get CI-optimized max_examples."""
    if not os.getenv('CI'):
        return base_examples
    
    # Never reduce finite strategies - they need full coverage
    if strategy_type in ['boolean', 'small_finite', 'medium_finite']:
        return base_examples
    
    # Reduce complex strategies in CI
    return max(base_examples // 2, 5)

# Usage example
CI_EXAMPLES = get_max_examples_for_ci(30, 'complex')

@given(st.text())
@settings(max_examples=CI_EXAMPLES)
def test_text_property(text):
    assert process_text(text) is not None
```

## Documentation Requirements

### Comment Format Specification

All property-based tests with custom `max_examples` values MUST include standardized comments that follow this format:

```
# [Strategy Type] strategy: [N] examples ([Rationale])
@settings(max_examples=N, deadline=None)
```

### Strategy Type Classifications

Use these standardized strategy type classifications in comments:

- **Boolean** - For `st.booleans()` strategies
- **Small finite** - For finite ranges ≤10 elements  
- **Medium finite** - For finite ranges 11-50 elements
- **Complex** - For complex strategies requiring many examples
- **Combination** - For multiple combined strategies

### Rationale Templates

Use these standardized rationale templates:

- **Boolean:** `(True/False coverage)`
- **Small finite:** `(input space size: N)` where N is the actual input space size
- **Medium finite:** `(adequate finite coverage)`
- **Complex:** `(adequate coverage)` or `(performance optimized)` 
- **Combination:** `(combination coverage)`
- **CI optimized:** `(CI performance optimized)`

### Comment Format Examples

```python
# ✅ Boolean strategy documentation
@given(st.booleans())
# Boolean strategy: 2 examples (True/False coverage)
@settings(max_examples=2, deadline=None)
def test_boolean_property(value):
    assert isinstance(value, bool)

# ✅ Small finite strategy documentation  
@given(st.integers(min_value=1, max_value=6))
# Small finite strategy: 6 examples (input space size: 6)
@settings(max_examples=6, deadline=None)
def test_dice_roll(value):
    assert 1 <= value <= 6

# ✅ Medium finite strategy documentation
@given(st.integers(min_value=1, max_value=20))
# Medium finite strategy: 20 examples (adequate finite coverage)
@settings(max_examples=20, deadline=None)
def test_medium_range(value):
    assert 1 <= value <= 20

# ✅ Complex strategy documentation
@given(st.text())
# Complex strategy: 25 examples (performance optimized)
@settings(max_examples=25, deadline=None)
def test_text_processing(text):
    result = expensive_text_analysis(text)
    assert result.is_valid()

# ✅ Combination strategy documentation
@given(st.tuples(st.booleans(), st.sampled_from(['a', 'b', 'c'])))
# Combination strategy: 6 examples (combination coverage)
@settings(max_examples=6, deadline=None)
def test_boolean_enum_combination(value):
    bool_val, enum_val = value
    assert isinstance(bool_val, bool)
    assert enum_val in ['a', 'b', 'c']

# ✅ CI-optimized complex strategy documentation
@given(st.recursive(st.integers(), lambda x: st.lists(x)))
# Complex strategy: 15 examples (CI performance optimized)
@settings(max_examples=15, deadline=None)
def test_recursive_structure(data):
    assert validate_recursive_data(data)
```

### Legacy Documentation (Deprecated)

The following comment styles are deprecated and should be updated to use the standardized format:

```python
# ❌ Deprecated - Inconsistent format
@given(st.text())
@settings(max_examples=25)  # Reduced due to expensive processing
def test_old_style(text):
    pass

# ❌ Deprecated - Missing strategy type
@given(st.booleans())
@settings(max_examples=2)  # Only need True/False
def test_missing_strategy_type(value):
    pass

# ❌ Deprecated - Non-standard terminology
@given(st.integers(1, 5))
@settings(max_examples=5)  # Test all possible integers
def test_non_standard_terminology(value):
    pass
```

## Validation Checklist

Before committing property-based tests, verify:

1. **Boolean strategies use max_examples=2**
2. **Small finite strategies use input space size**
3. **Combination strategies use product formula (capped at 50)**
4. **Complex strategies use 10-50 examples based on complexity**
5. **All custom values include standardized comments**
6. **Comments follow the format: `# [Strategy Type] strategy: [N] examples ([Rationale])`**
7. **Strategy type classifications use standardized terminology**
8. **Rationale templates match the strategy type**
9. **CI optimization is considered for complex strategies**

## Common Anti-Patterns

### ❌ Default max_examples=100 for everything
```python
# Don't use the same value for all tests
@given(st.booleans())
@settings(max_examples=100)  # 98% wasted time

@given(st.integers(1, 3))
@settings(max_examples=100)  # 97% wasted time

@given(st.text())
@settings(max_examples=100)  # May be appropriate, but should be justified
```

### ❌ Ignoring input space size
```python
# Don't ignore finite input spaces
@given(st.sampled_from(['A', 'B']))
@settings(max_examples=50)  # Only 2 possible values!
```

### ❌ Undocumented custom values
```python
# Don't use custom values without explanation
@given(st.text())
@settings(max_examples=73)  # Why 73? Document the reasoning!
```

### ❌ Inconsistent comment formats
```python
# Don't use inconsistent comment formats
@given(st.booleans())
@settings(max_examples=2)  # Only need True/False  # Missing strategy type

@given(st.integers(1, 5))
@settings(max_examples=5)  # Test all integers  # Non-standard terminology

@given(st.text())
# Random comment format without standardization
@settings(max_examples=25)
def test_inconsistent_format(text):
    pass
```

### ❌ Wrong strategy type classifications
```python
# Don't misclassify strategy types
@given(st.booleans())
# Complex strategy: 2 examples (True/False coverage)  # Wrong: should be "Boolean"
@settings(max_examples=2)

@given(st.integers(1, 3))
# Boolean strategy: 3 examples (input space size: 3)  # Wrong: should be "Small finite"
@settings(max_examples=3)
```

## Performance Impact

Following these guidelines typically results in:

- **Boolean tests:** 98% time reduction (100 → 2 examples)
- **Small finite tests:** 80-95% time reduction
- **Medium finite tests:** 50-80% time reduction  
- **Complex tests:** 0-50% time reduction (may already be appropriate)

## Tools and Automation

### Test Optimization Analysis

Use the provided optimization tools to identify over-testing:

```python
from kivy_garden.markdownlabel.test_file_analyzer import FileAnalyzer

# Analyze test files for optimization opportunities
analyzer = FileAnalyzer()
report = analyzer.validate_test_suite('tests/')

# Generate optimization recommendations
for file_analysis in report.file_analyses:
    for recommendation in file_analysis.recommendations:
        print(f"{recommendation.test_name}: {recommendation.current_examples} → {recommendation.recommended_examples}")
```

### Comment Standardization Tools

Use the comment standardization tools to ensure consistent documentation:

```python
from tools.test_optimization.comment_analyzer import CommentAnalyzer
from tools.test_optimization.comment_standardizer import CommentStandardizer

# Analyze comment consistency
analyzer = CommentAnalyzer()
analysis = analyzer.analyze_directory('kivy_garden/markdownlabel/tests/')

# Report missing or inconsistent comments
for file_analysis in analysis.file_analyses:
    if file_analysis.undocumented_tests > 0:
        print(f"{file_analysis.file_path}: {file_analysis.undocumented_tests} undocumented tests")
    
    for violation in file_analysis.format_violations:
        print(f"Format violation: {violation.description}")

# Apply standardized comments (with dry-run)
standardizer = CommentStandardizer()
result = standardizer.standardize_file('test_example.py', dry_run=True)
print(f"Would update {len(result.changes)} comments")

# Apply changes (removes dry_run)
if input("Apply changes? (y/n): ").lower() == 'y':
    result = standardizer.standardize_file('test_example.py', dry_run=False)
    print(f"Updated {len(result.changes)} comments")
```

### Command-Line Validation

Use the command-line tools for batch operations:

```bash
# Analyze all test files for comment compliance
python tools/validate_comments.py kivy_garden/markdownlabel/tests/

# Generate standardization report
python tools/validate_comments.py --report kivy_garden/markdownlabel/tests/

# Apply standardization (with confirmation)
python tools/validate_comments.py --fix kivy_garden/markdownlabel/tests/
```

## Summary

The key principles for optimized property-based testing are:

### Right-Sizing Examples
- **Finite strategies:** Use input space size (test each value once)
- **Infinite strategies:** Use moderate counts based on property complexity
- **Combination strategies:** Calculate combinations, cap at reasonable limits

### Standardized Documentation
- **Always document:** Use standardized comment format for all custom values
- **Consistent terminology:** Use standardized strategy type classifications
- **Clear rationale:** Follow rationale templates for each strategy type
- **Machine-readable:** Enable automated analysis and validation

### Quality Assurance
- **Validate format:** Ensure comments follow `# [Strategy Type] strategy: [N] examples ([Rationale])` pattern
- **Use tools:** Leverage automated analysis and standardization tools
- **Measure impact:** Verify that optimizations maintain coverage while improving performance

By following these guidelines, you can achieve significant test performance improvements while maintaining consistent, well-documented, and high-quality test coverage.