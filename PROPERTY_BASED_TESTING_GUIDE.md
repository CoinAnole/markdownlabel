# Property-Based Testing Guide

This guide provides comprehensive instructions for writing optimized and well-documented property-based tests using Hypothesis in the MarkdownLabel project.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Optimization Guidelines](#optimization-guidelines)
3. [Comment Format Requirements](#comment-format-requirements)
4. [Strategy Classifications](#strategy-classifications)
5. [Writing Documented Tests](#writing-documented-tests)
6. [Standardization Tools](#standardization-tools)
7. [Validation and CI Integration](#validation-and-ci-integration)
8. [Troubleshooting Guide](#troubleshooting-guide)
9. [Best Practices](#best-practices)

## Quick Start

### Basic Requirements

Every property-based test with a custom `max_examples` value MUST include a standardized comment:

```python
# [Strategy Type] strategy: [N] examples ([Rationale])
@settings(max_examples=N, deadline=None)
def test_example(value):
    pass
```

### Example

```python
@given(st.booleans())
# Boolean strategy: 2 examples (True/False coverage)
@settings(max_examples=2, deadline=None)
def test_boolean_property(value):
    assert isinstance(value, bool)
```

## Optimization Guidelines

### Overview

Property-based testing with Hypothesis generates random inputs to verify that properties hold across many examples. However, using excessive `max_examples` values can lead to unnecessary test execution time without proportional coverage benefits.

### Right-Sizing Principles

- **Finite strategies:** Use input space size (test each value once)
- **Infinite strategies:** Use moderate counts based on property complexity
- **Combination strategies:** Calculate combinations, cap at reasonable limits

### Performance Impact

Following these guidelines typically results in:

- **Boolean tests:** 98% time reduction (100 → 2 examples)
- **Small finite tests:** 80-95% time reduction
- **Medium finite tests:** 50-80% time reduction  
- **Complex tests:** 0-50% time reduction (may already be appropriate)

## Comment Format Requirements

### Mandatory Format Structure

All comments documenting `max_examples` values MUST follow this exact format:

```
# [Strategy Type] strategy: [N] examples ([Rationale])
```

**Components:**
- `#` - Comment marker (single space after hash)
- `[Strategy Type]` - One of: Boolean, Small finite, Medium finite, Complex, Combination
- ` strategy: ` - Literal text with spaces
- `[N]` - The actual max_examples number
- ` examples ` - Literal text with spaces
- `([Rationale])` - Explanation in parentheses

### Valid Examples

```python
# Boolean strategy: 2 examples (True/False coverage)
# Small finite strategy: 6 examples (input space size: 6)
# Medium finite strategy: 20 examples (adequate finite coverage)
# Complex strategy: 25 examples (performance optimized)
# Combination strategy: 6 examples (combination coverage)
```

## Strategy Classifications

### 1. Boolean Strategies

**Pattern:** `st.booleans()`
**Recommended max_examples:** `2`
**Rationale:** Boolean strategies have exactly 2 possible values (True/False). Testing with more than 2 examples provides no additional coverage.

**Format:** `Boolean strategy: 2 examples (True/False coverage)`

```python
# ✅ Optimal
@given(st.booleans())
# Boolean strategy: 2 examples (True/False coverage)
@settings(max_examples=2, deadline=None)
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

**Format:** `Small finite strategy: [N] examples (input space size: [N])`

```python
# ✅ Optimal - 6 possible values
@given(st.integers(min_value=1, max_value=6))
# Small finite strategy: 6 examples (input space size: 6)
@settings(max_examples=6, deadline=None)
def test_dice_roll(value):
    assert 1 <= value <= 6

# ✅ Optimal - 3 possible values
@given(st.sampled_from(['red', 'green', 'blue']))
# Small finite strategy: 3 examples (input space size: 3)
@settings(max_examples=3, deadline=None)
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

**Format:** `Medium finite strategy: [N] examples (adequate finite coverage)`

```python
# ✅ Optimal - 20 possible values
@given(st.integers(min_value=1, max_value=20))
# Medium finite strategy: 20 examples (adequate finite coverage)
@settings(max_examples=20, deadline=None)
def test_medium_range(value):
    assert 1 <= value <= 20

# ✅ Acceptable - Large range capped at 50
@given(st.integers(min_value=1, max_value=100))
# Medium finite strategy: 50 examples (adequate finite coverage)
@settings(max_examples=50, deadline=None)
def test_large_range(value):
    assert 1 <= value <= 100
```

### 4. Combination Strategies

**Pattern:** Multiple strategies combined (tuples, multiple @given arguments)
**Recommended max_examples:** Product of individual strategy sizes, capped at 50
**Rationale:** Combination strategies create cartesian products. Calculate the total combinations and cap at reasonable limits.

**Format:** `Combination strategy: [N] examples (combination coverage)`

```python
# ✅ Optimal - 2 × 3 = 6 combinations
@given(st.tuples(st.booleans(), st.sampled_from(['a', 'b', 'c'])))
# Combination strategy: 6 examples (combination coverage)
@settings(max_examples=6, deadline=None)
def test_boolean_enum_combination(value):
    bool_val, enum_val = value
    assert isinstance(bool_val, bool)
    assert enum_val in ['a', 'b', 'c']

# ✅ Optimal - 2 × 2 = 4 combinations
@given(flag=st.booleans(), mode=st.booleans())
# Combination strategy: 4 examples (combination coverage)
@settings(max_examples=4, deadline=None)
def test_two_booleans(flag, mode):
    assert isinstance(flag, bool)
    assert isinstance(mode, bool)

# ✅ Capped - Large combination space
@given(st.tuples(st.integers(1, 20), st.integers(1, 20)))
# Combination strategy: 50 examples (combination coverage)
@settings(max_examples=50, deadline=None)  # 400 combinations capped at 50
def test_large_combination(value):
    x, y = value
    assert x * y > 0
```

### 5. Complex/Infinite Strategies

**Pattern:** `st.text()`, `st.floats()`, large ranges, recursive strategies
**Recommended max_examples:** 10-50 based on complexity
**Rationale:** For infinite or very large input spaces, use moderate example counts based on the complexity of the property being tested.

**Format:** `Complex strategy: [N] examples (adequate coverage)` or `Complex strategy: [N] examples (performance optimized)`

```python
# ✅ Simple property - lower examples
@given(st.text())
# Complex strategy: 10 examples (adequate coverage)
@settings(max_examples=10, deadline=None)
def test_text_length_property(text):
    assert len(text) >= 0

# ✅ Complex property - higher examples
@given(st.text(min_size=1), st.floats(allow_nan=False))
# Complex strategy: 30 examples (adequate coverage)
@settings(max_examples=30, deadline=None)
def test_complex_text_float_interaction(text, number):
    result = complex_processing(text, number)
    assert validate_complex_result(result)

# ✅ Performance-sensitive property
@given(st.text())
# Complex strategy: 15 examples (performance optimized)
@settings(max_examples=15, deadline=None)
def test_expensive_text_analysis(text):
    result = expensive_analysis(text)  # Slow operation
    assert result.is_valid()
```

## Writing Documented Tests

### Step-by-Step Process

1. **Write the test function with @given decorator**
2. **Analyze the strategy type** (see classification above)
3. **Calculate appropriate max_examples** based on strategy type
4. **Add standardized comment** using the correct format
5. **Add @settings decorator** with max_examples and deadline=None

### Template

```python
@given([your_strategy])
# [Strategy Type] strategy: [N] examples ([Rationale])
@settings(max_examples=[N], deadline=None)
def test_[descriptive_name]([parameters]):
    # Test implementation
    assert [your_assertion]
```

### Complete Example

```python
from hypothesis import given, settings
from hypothesis import strategies as st

@given(st.integers(min_value=0, max_value=255))
# Small finite strategy: 256 examples (input space size: 256)
@settings(max_examples=256, deadline=None)
def test_rgb_color_component(value):
    """Test RGB color component validation."""
    color = RGBColor(value, 128, 64)
    assert color.red == value
    assert 0 <= color.red <= 255
```

### CI Optimization

For complex strategies that may be slow in CI environments:

```python
import os

# Calculate CI-optimized examples
CI_EXAMPLES = 15 if os.getenv('CI') else 30

@given(st.text())
# Complex strategy: 15 examples (CI performance optimized)
@settings(max_examples=CI_EXAMPLES, deadline=None)
def test_text_processing_ci_optimized(text):
    result = process_text(text)
    assert result is not None
```

## Standardization Tools

### CommentAnalyzer

Analyzes existing test files for comment compliance:

```python
from tools.test_optimization.comment_analyzer import CommentAnalyzer

analyzer = CommentAnalyzer()

# Analyze single file
analysis = analyzer.analyze_file('kivy_garden/markdownlabel/tests/test_example.py')
print(f"Documented tests: {analysis.documented_tests}")
print(f"Undocumented tests: {analysis.undocumented_tests}")

# Analyze entire directory
dir_analysis = analyzer.analyze_directory('kivy_garden/markdownlabel/tests/')
for file_analysis in dir_analysis.file_analyses:
    if file_analysis.format_violations:
        print(f"Format violations in {file_analysis.file_path}:")
        for violation in file_analysis.format_violations:
            print(f"  Line {violation.line_number}: {violation.description}")
```

### CommentStandardizer

Automatically applies standardized comments:

```python
from tools.test_optimization.comment_standardizer import CommentStandardizer

standardizer = CommentStandardizer()

# Dry run (preview changes)
result = standardizer.standardize_file('test_example.py', dry_run=True)
print(f"Would make {len(result.changes)} changes:")
for change in result.changes:
    print(f"  Line {change.line_number}: {change.description}")

# Apply changes (creates backup)
if input("Apply changes? (y/n): ").lower() == 'y':
    result = standardizer.standardize_file('test_example.py', dry_run=False)
    print(f"Applied {len(result.changes)} changes")
    print(f"Backup created: {result.backup_path}")
```

### Command-Line Tools

#### validate_comments.py

Primary CLI tool for comment validation and standardization:

```bash
# Validate all test files
python tools/validate_comments.py validate kivy_garden/markdownlabel/tests/

# Generate detailed report
python tools/validate_comments.py report kivy_garden/markdownlabel/tests/ --output report.json

# Standardize comments (dry run)
python tools/validate_comments.py standardize kivy_garden/markdownlabel/tests/ --dry-run

# Apply standardization with backup
python tools/validate_comments.py standardize kivy_garden/markdownlabel/tests/ --backup-dir ./backups

# Optimize max_examples and add comments
python tools/validate_comments.py optimize kivy_garden/markdownlabel/tests/ --include-comments
```

#### analyze_tests.py

Analyzes test performance and comment compliance:

```bash
# Full analysis with comment validation
python tools/analyze_tests.py --include-comments

# Generate optimization report
python tools/analyze_tests.py --report-format json --output analysis.json
```

### Integration with Existing Tools

The standardization tools integrate with existing optimization infrastructure:

```python
from tools.test_optimization import FileAnalyzer, CommentAnalyzer

# Combined analysis
file_analyzer = FileAnalyzer()
comment_analyzer = CommentAnalyzer()

# Get optimization recommendations
optimization_report = file_analyzer.validate_test_suite('tests/')

# Get comment compliance report
comment_report = comment_analyzer.analyze_directory('tests/')

# Cross-reference findings
for file_analysis in optimization_report.file_analyses:
    comment_analysis = next(
        (ca for ca in comment_report.file_analyses 
         if ca.file_path == file_analysis.file_path), 
        None
    )
    
    if comment_analysis and comment_analysis.undocumented_tests > 0:
        print(f"{file_analysis.file_path}: needs both optimization and documentation")
```

## Validation and CI Integration

### Pre-commit Hook

Add comment validation to your pre-commit hook:

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Validating test comments..."
python tools/validate_comments.py validate kivy_garden/markdownlabel/tests/

if [ $? -ne 0 ]; then
    echo "❌ Comment format violations detected."
    echo "Run: python tools/validate_comments.py standardize kivy_garden/markdownlabel/tests/ --dry-run"
    echo "to see suggested fixes."
    exit 1
fi

echo "✅ All comments properly formatted."
```

### GitHub Actions Integration

Add to your CI workflow:

```yaml
name: Test Quality Validation

on: [push, pull_request]

jobs:
  validate-comments:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install -e .
        pip install -e ".[dev]"
    
    - name: Validate comment format
      run: python tools/validate_comments.py validate kivy_garden/markdownlabel/tests/
    
    - name: Check for over-testing
      run: python tools/analyze_tests.py --include-comments
```

### Local Development Workflow

1. **Write your test** following the documentation format
2. **Validate locally:**
   ```bash
   python tools/validate_comments.py validate kivy_garden/markdownlabel/tests/test_your_file.py
   ```
3. **Fix any issues:**
   ```bash
   python tools/validate_comments.py standardize kivy_garden/markdownlabel/tests/test_your_file.py --dry-run
   ```
4. **Apply fixes if needed:**
   ```bash
   python tools/validate_comments.py standardize kivy_garden/markdownlabel/tests/test_your_file.py
   ```
5. **Run tests to ensure functionality:**
   ```bash
   pytest kivy_garden/markdownlabel/tests/test_your_file.py
   ```

## Troubleshooting Guide

### Common Issues and Solutions

#### Issue: "Comment format validation failed"

**Symptoms:**
```
ValidationError: Comment format validation failed: Expected format '# [Strategy Type] strategy: [N] examples ([Rationale])'
Found: '# Boolean: 2 examples (True/False)'
```

**Solution:**
The comment is missing the word "strategy". Fix:
```python
# ❌ Incorrect
# Boolean: 2 examples (True/False)

# ✅ Correct  
# Boolean strategy: 2 examples (True/False coverage)
```

#### Issue: "Unknown strategy type"

**Symptoms:**
```
ValidationError: Unknown strategy type 'Bool'. Valid types: Boolean, Small finite, Medium finite, Complex, Combination
```

**Solution:**
Use the exact standardized terminology:
```python
# ❌ Incorrect
# Bool strategy: 2 examples (True/False coverage)

# ✅ Correct
# Boolean strategy: 2 examples (True/False coverage)
```

#### Issue: "Missing rationale parentheses"

**Symptoms:**
```
ValidationError: Rationale must be enclosed in parentheses
Found: 'True/False coverage'
```

**Solution:**
Ensure rationale is in parentheses:
```python
# ❌ Incorrect
# Boolean strategy: 2 examples True/False coverage

# ✅ Correct
# Boolean strategy: 2 examples (True/False coverage)
```

#### Issue: "Strategy type mismatch"

**Symptoms:**
```
Warning: Strategy type 'Complex' doesn't match detected strategy 'Boolean'
```

**Solution:**
Analyze your strategy and use the correct classification:
```python
# ❌ Misclassified
@given(st.booleans())
# Complex strategy: 2 examples (adequate coverage)

# ✅ Correctly classified
@given(st.booleans())
# Boolean strategy: 2 examples (True/False coverage)
```

### Debugging Steps

1. **Check file syntax:**
   ```bash
   python -m py_compile kivy_garden/markdownlabel/tests/test_your_file.py
   ```

2. **Validate individual comments:**
   ```python
   from tools.test_optimization.comment_format import CommentFormatValidator
   
   validator = CommentFormatValidator()
   result = validator.validate_comment_format("# Boolean strategy: 2 examples (True/False coverage)")
   print(f"Valid: {result.is_valid}")
   if not result.is_valid:
       print(f"Error: {result.message}")
   ```

3. **Check strategy detection:**
   ```python
   from tools.test_optimization.strategy_type_mapper import TestCodeAnalyzer
   
   analyzer = TestCodeAnalyzer()
   strategy_info = analyzer.analyze_test_function(test_function_code)
   print(f"Detected strategy: {strategy_info.strategy_type}")
   print(f"Recommended examples: {strategy_info.recommended_examples}")
   ```

## Best Practices

### Writing Quality Comments

1. **Be specific in rationales:**
   ```python
   # ✅ Good - specific rationale
   # Small finite strategy: 6 examples (input space size: 6)
   
   # ❌ Vague - unclear rationale  
   # Small finite strategy: 6 examples (enough coverage)
   ```

2. **Match strategy to actual code:**
   ```python
   # ✅ Correct match
   @given(st.booleans())
   # Boolean strategy: 2 examples (True/False coverage)
   
   # ❌ Incorrect match
   @given(st.text())
   # Boolean strategy: 2 examples (True/False coverage)
   ```

### Code Organization

1. **Group related tests:**
   ```python
   class TestBooleanProperties:
       """Tests for boolean property handling."""
       
       @given(st.booleans())
       # Boolean strategy: 2 examples (True/False coverage)
       @settings(max_examples=2, deadline=None)
       def test_boolean_flag_processing(self, flag):
           pass
   ```

2. **Use consistent naming:**
   ```python
   # ✅ Descriptive test names
   def test_boolean_flag_enables_feature(self, flag):
   def test_finite_color_validation(self, color):
   def test_complex_text_processing(self, text):
   ```

### Performance Considerations

1. **Profile before optimizing:**
   ```bash
   # Measure test execution time
   pytest --durations=10 kivy_garden/markdownlabel/tests/
   ```

2. **Use CI optimization judiciously:**
   ```python
   # Only for genuinely slow tests
   CI_EXAMPLES = 10 if os.getenv('CI') else 25
   
   @given(st.text())
   # Complex strategy: 10 examples (CI performance optimized)
   @settings(max_examples=CI_EXAMPLES, deadline=None)
   def test_expensive_operation(self, text):
       pass
   ```

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
- **Validate format:** Ensure comments follow standardized pattern
- **Use tools:** Leverage automated analysis and standardization tools
- **Measure impact:** Verify that optimizations maintain coverage while improving performance

By following this guide, you can achieve significant test performance improvements while maintaining consistent, well-documented, and high-quality test coverage.