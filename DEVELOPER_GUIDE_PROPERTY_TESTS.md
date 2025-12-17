# Developer Guide: Writing Properly Documented Property-Based Tests

This guide provides comprehensive instructions for writing well-documented property-based tests using Hypothesis in the MarkdownLabel project. It covers comment standardization, tool usage, and troubleshooting common issues.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Comment Format Requirements](#comment-format-requirements)
3. [Strategy Type Classification](#strategy-type-classification)
4. [Writing Documented Tests](#writing-documented-tests)
5. [Standardization Tools](#standardization-tools)
6. [Validation and CI Integration](#validation-and-ci-integration)
7. [Troubleshooting Guide](#troubleshooting-guide)
8. [Best Practices](#best-practices)

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

### Invalid Examples

```python
# ❌ Wrong format - missing strategy type
# 2 examples (True/False coverage)

# ❌ Wrong format - incorrect terminology
# Bool strategy: 2 examples (True/False coverage)

# ❌ Wrong format - missing parentheses
# Boolean strategy: 2 examples True/False coverage

# ❌ Wrong format - extra text
# Boolean strategy: 2 examples (True/False coverage) - optimized

# ❌ Wrong format - incorrect spacing
#Boolean strategy:2 examples(True/False coverage)
```

## Strategy Type Classification

### Boolean Strategies

**When to use:** Tests using `st.booleans()`

**Format:** `Boolean strategy: 2 examples (True/False coverage)`

**Example:**
```python
@given(st.booleans())
# Boolean strategy: 2 examples (True/False coverage)
@settings(max_examples=2, deadline=None)
def test_boolean_flag(enabled):
    result = process_with_flag(enabled)
    assert result.success == enabled
```

### Small Finite Strategies

**When to use:** Finite input spaces with ≤10 possible values

**Format:** `Small finite strategy: [N] examples (input space size: [N])`

**Examples:**
```python
@given(st.integers(min_value=1, max_value=6))
# Small finite strategy: 6 examples (input space size: 6)
@settings(max_examples=6, deadline=None)
def test_dice_roll(value):
    assert 1 <= value <= 6

@given(st.sampled_from(['red', 'green', 'blue']))
# Small finite strategy: 3 examples (input space size: 3)
@settings(max_examples=3, deadline=None)
def test_color_validation(color):
    assert color in VALID_COLORS
```

### Medium Finite Strategies

**When to use:** Finite input spaces with 11-50 possible values

**Format:** `Medium finite strategy: [N] examples (adequate finite coverage)`

**Example:**
```python
@given(st.integers(min_value=1, max_value=20))
# Medium finite strategy: 20 examples (adequate finite coverage)
@settings(max_examples=20, deadline=None)
def test_medium_range(value):
    assert validate_range(value)
```

### Complex Strategies

**When to use:** Infinite or very large input spaces (text, floats, large ranges)

**Format:** `Complex strategy: [N] examples (adequate coverage)` or `Complex strategy: [N] examples (performance optimized)`

**Examples:**
```python
@given(st.text())
# Complex strategy: 30 examples (adequate coverage)
@settings(max_examples=30, deadline=None)
def test_text_processing(text):
    result = process_text(text)
    assert result is not None

@given(st.text())
# Complex strategy: 15 examples (performance optimized)
@settings(max_examples=15, deadline=None)
def test_expensive_text_analysis(text):
    result = expensive_analysis(text)  # Slow operation
    assert result.is_valid()
```

### Combination Strategies

**When to use:** Multiple strategies combined (tuples, multiple @given arguments)

**Format:** `Combination strategy: [N] examples (combination coverage)`

**Examples:**
```python
@given(st.tuples(st.booleans(), st.sampled_from(['a', 'b', 'c'])))
# Combination strategy: 6 examples (combination coverage)
@settings(max_examples=6, deadline=None)
def test_boolean_enum_combination(value):
    bool_val, enum_val = value
    assert process_combination(bool_val, enum_val)

@given(flag=st.booleans(), mode=st.booleans())
# Combination strategy: 4 examples (combination coverage)
@settings(max_examples=4, deadline=None)
def test_two_flags(flag, mode):
    result = process_flags(flag, mode)
    assert result.is_configured()
```

## Writing Documented Tests

### Step-by-Step Process

1. **Write the test function with @given decorator**
2. **Analyze the strategy type** (see classification above)
3. **Calculate appropriate max_examples** (see HYPOTHESIS_OPTIMIZATION_GUIDELINES.md)
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

#### Issue: "Inconsistent spacing"

**Symptoms:**
```
ValidationError: Invalid format - spacing issues detected
```

**Solution:**
Follow exact spacing requirements:
```python
# ❌ Incorrect spacing
#Boolean strategy:2 examples(True/False coverage)

# ✅ Correct spacing
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

#### Issue: "Undocumented custom max_examples"

**Symptoms:**
```
Error: Test 'test_example' uses custom max_examples=25 but has no documentation comment
```

**Solution:**
Add a standardized comment above the @settings decorator:
```python
@given(st.text())
# Complex strategy: 25 examples (performance optimized)
@settings(max_examples=25, deadline=None)
def test_example(text):
    pass
```

#### Issue: "Tool integration failures"

**Symptoms:**
```
ImportError: cannot import name 'CommentAnalyzer' from 'tools.test_optimization'
```

**Solution:**
Ensure you're importing from the correct module:
```python
# ❌ Incorrect import
from tools.test_optimization import CommentAnalyzer

# ✅ Correct import
from tools.test_optimization.comment_analyzer import CommentAnalyzer
```

#### Issue: "Backup file conflicts"

**Symptoms:**
```
Error: Backup file already exists: test_example.py.backup.20231216_143022
```

**Solution:**
Either remove old backups or specify a different backup directory:
```bash
# Remove old backups
rm *.backup.*

# Or use different backup directory
python tools/validate_comments.py standardize tests/ --backup-dir ./new_backups
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

4. **Verify tool installation:**
   ```bash
   python -c "from tools.test_optimization.comment_analyzer import CommentAnalyzer; print('Tools installed correctly')"
   ```

### Getting Help

If you encounter issues not covered in this guide:

1. **Check existing issues:** Look for similar problems in project documentation
2. **Run diagnostic commands:**
   ```bash
   python tools/validate_comments.py validate --verbose kivy_garden/markdownlabel/tests/
   ```
3. **Generate detailed report:**
   ```bash
   python tools/validate_comments.py report kivy_garden/markdownlabel/tests/ --output debug_report.json
   ```
4. **Test with minimal example:** Create a simple test to isolate the issue

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

3. **Use performance rationale appropriately:**
   ```python
   # ✅ Good - explains performance consideration
   # Complex strategy: 15 examples (performance optimized)
   
   # ✅ Good - explains adequate coverage
   # Complex strategy: 30 examples (adequate coverage)
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

3. **Document complex strategies:**
   ```python
   @given(st.recursive(
       st.integers(min_value=0, max_value=10),
       lambda x: st.lists(x, min_size=0, max_size=3)
   ))
   # Complex strategy: 25 examples (adequate coverage)
   @settings(max_examples=25, deadline=None)
   def test_recursive_data_structure(self, data):
       """Test recursive data structure validation.
       
       Uses recursive strategy to generate nested lists of integers.
       Requires adequate examples to cover various nesting levels.
       """
       pass
   ```

### Maintenance

1. **Regular validation:**
   ```bash
   # Run weekly validation
   python tools/validate_comments.py validate kivy_garden/markdownlabel/tests/
   ```

2. **Update comments when changing strategies:**
   ```python
   # When changing from:
   @given(st.integers(min_value=1, max_value=5))
   # Small finite strategy: 5 examples (input space size: 5)
   
   # To:
   @given(st.integers(min_value=1, max_value=50))
   # Medium finite strategy: 50 examples (adequate finite coverage)
   ```

3. **Review generated comments:**
   Always review auto-generated comments for accuracy and clarity before committing.

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

3. **Monitor test suite performance:**
   ```bash
   # Track performance over time
   python tools/analyze_tests.py --performance-report
   ```

By following this guide, you'll write well-documented, efficient property-based tests that integrate seamlessly with the project's optimization and validation infrastructure.