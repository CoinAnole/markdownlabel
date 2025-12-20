# Testing Guidelines for MarkdownLabel

This document provides comprehensive guidelines for writing, organizing, and maintaining tests in the MarkdownLabel project.

## Table of Contents

- [Test Organization](#test-organization)
- [Test Naming Conventions](#test-naming-conventions)
- [Test Types and Markers](#test-types-and-markers)
- [Rebuild Contract Testing](#rebuild-contract-testing)
- [Property-Based Testing](#property-based-testing)
- [Helper Functions](#helper-functions)
- [Test File Structure](#test-file-structure)

## Test Organization

### File Organization

Tests are organized by **functionality**, not by implementation file:

```
tests/
├── test_core_functionality.py      # Core parsing and rendering
├── test_label_compatibility.py     # Basic label property forwarding
├── test_font_properties.py         # Font-related property forwarding
├── test_color_properties.py        # Color and styling properties
├── test_text_properties.py         # Text-related property forwarding
├── test_padding_properties.py      # Padding and spacing properties
├── test_sizing_behavior.py         # Auto-sizing and layout behavior
├── test_advanced_compatibility.py  # Advanced label features
├── test_serialization.py           # Round-trip serialization
├── test_performance.py             # Performance and stability tests
└── test_utils.py                   # Shared test utilities
```

### Class Organization

Within each test file, organize tests into logical classes:

- **One class per property or behavior being tested**
- **Descriptive class names** that clearly indicate what is being tested
- **Related test methods** grouped within the same class

#### Good Class Organization Examples:

```python
class TestFontNamePropertyForwarding:
    """Tests for font_name property forwarding to child Labels."""
    
    def test_font_name_applied_to_paragraph(self):
        # Test font_name forwarding to paragraph labels
        
    def test_font_name_applied_to_heading(self):
        # Test font_name forwarding to heading labels
        
    def test_font_name_preserves_code_font(self):
        # Test that code blocks preserve their special font

class TestColorPropertyForwarding:
    """Tests for color property forwarding to child Labels."""
    
    def test_color_applied_to_paragraph(self):
        # Test color forwarding to paragraph labels
        
    def test_color_applied_to_heading(self):
        # Test color forwarding to heading labels
```

#### Poor Class Organization Examples:

```python
# DON'T: Mix unrelated functionality
class TestMixedFunctionality:
    def test_font_size_forwarding(self):
        pass
    def test_serialization_roundtrip(self):
        pass
    def test_performance_benchmark(self):
        pass

# DON'T: Vague class names
class TestBasicStuff:
    pass

class TestMisc:
    pass
```

## Test Naming Conventions

### Test Method Names

Test method names should **accurately reflect what they assert**:

#### Rebuild Testing Names

- `test_*_triggers_rebuild_*` - ONLY for tests that verify a rebuild occurred
- `test_*_preserves_widget_tree_*` - For tests that verify NO rebuild occurred
- `test_*_rebuilds_*` - For tests that verify rebuild behavior

#### Value/Property Testing Names

- `test_*_updates_value_*` - For tests that verify value changes without rebuild verification
- `test_*_changes_property_*` - For tests that verify property changes
- `test_*_forwards_to_*` - For tests that verify property forwarding
- `test_*_applied_to_*` - For tests that verify property application

#### Examples:

```python
# GOOD: Name matches assertion
def test_font_size_change_triggers_rebuild(self):
    """Test that changing font_size rebuilds the widget tree."""
    ids_before = collect_widget_ids(label)
    label.font_size = 20
    ids_after = collect_widget_ids(label)
    assert ids_before != ids_after  # Verifies rebuild occurred

def test_color_updates_value_immediately(self):
    """Test that color changes update Label.color immediately."""
    label.color = [1, 0, 0, 1]
    labels = find_labels_recursive(label)
    assert all(l.color == [1, 0, 0, 1] for l in labels)  # Verifies value change

# BAD: Name doesn't match assertion
def test_font_size_triggers_rebuild(self):
    """Test font size changes."""
    label.font_size = 20
    labels = find_labels_recursive(label)
    assert labels[0].font_size == 20  # Only tests value, not rebuild!
```

### Test Class Names

Use descriptive, specific class names:

- `Test[Property][Behavior]` - e.g., `TestFontSizeImmediateUpdates`
- `Test[Component][Functionality]` - e.g., `TestMarkdownLinkRendering`
- `Test[Feature][Aspect]` - e.g., `TestRebuildContractEnforcement`

## Test Types and Markers

### Pytest Markers

Use appropriate pytest markers to categorize tests:

```python
@pytest.mark.slow           # Performance-intensive tests
@pytest.mark.needs_window   # Tests requiring Kivy window
@pytest.mark.test_tests     # Meta-tests (tests about test suite structure)
```

#### Meta-Test Marking

Tests that validate the test suite itself must be marked with `@pytest.mark.test_tests`:

```python
@pytest.mark.test_tests
class TestHelperFunctionAvailability:
    """Tests that verify helper functions are available and consolidated."""
    
    def test_widget_traversal_helpers_available(self):
        # Test that helper functions exist in test_utils
```

### Test Categories

#### Unit Tests
- Test specific examples and edge cases
- Verify concrete behavior with known inputs
- Fast execution, deterministic results

#### Property-Based Tests
- Test universal properties across many inputs
- Use Hypothesis for input generation
- Verify behavior holds for all valid inputs
- Minimum 100 iterations per property test

## Rebuild Contract Testing

### Understanding the Rebuild Contract

MarkdownLabel distinguishes between two types of property changes:

1. **Style-only changes** - Update existing widgets in place (no rebuild)
2. **Structure changes** - Rebuild the entire widget tree

### Style-Only Properties

These properties update existing widgets without rebuilding:

- `color` - Updates Label.color on existing Labels
- `font_size` / `base_font_size` - Updates Label.font_size on existing Labels  
- `font_name` - Updates Label.font_name on existing Labels
- `line_height` - Updates Label.line_height on existing Labels
- `halign`, `valign` - Updates alignment on existing Labels
- `text_size` - Updates Label.text_size on existing Labels
- `padding` - Updates container padding

### Structure Properties

These properties trigger a complete widget tree rebuild:

- `text` - Changes the markdown content structure
- `render_mode` - Changes between widgets/texture rendering
- Properties that affect parsing or widget hierarchy

### Testing Rebuild Behavior

#### Testing Style-Only Changes (No Rebuild)

```python
def test_color_change_preserves_widget_tree(self):
    """Test that color changes preserve widget identities (no rebuild)."""
    label = MarkdownLabel(text="Hello World")
    
    # Collect widget IDs before change
    ids_before = collect_widget_ids(label)
    
    # Change style-only property
    label.color = [1, 0, 0, 1]
    
    # Verify widget tree structure is preserved
    ids_after = collect_widget_ids(label)
    assert ids_before == ids_after, "Widget tree should not rebuild for style changes"
    
    # Verify the style change was applied
    labels = find_labels_recursive(label)
    assert all(l.color == [1, 0, 0, 1] for l in labels)
```

#### Testing Structure Changes (Rebuild Required)

```python
def test_text_change_triggers_rebuild(self):
    """Test that text changes rebuild the widget tree."""
    label = MarkdownLabel(text="Original text")
    
    # Collect widget IDs before change
    ids_before = collect_widget_ids(label)
    
    # Change structure property
    label.text = "New text with different structure"
    
    # Verify widget tree was rebuilt
    ids_after = collect_widget_ids(label)
    assert ids_before != ids_after, "Widget tree should rebuild for structure changes"
    
    # Verify the content change was applied
    assert label.text == "New text with different structure"
```

### Rebuild Testing Helpers

Use these helper functions from `test_utils.py`:

```python
def collect_widget_ids(widget):
    """Collect Python object IDs of all widgets in the tree."""
    
def assert_rebuild_occurred(widget, change_func):
    """Assert that a change function triggers a rebuild."""
    
def assert_no_rebuild(widget, change_func):
    """Assert that a change function does NOT trigger a rebuild."""
```

## Property-Based Testing

### When to Use Property-Based Tests

Use property-based tests for:

- **Universal properties** that should hold for all inputs
- **Invariants** that must be preserved across operations
- **Round-trip properties** (serialize → deserialize → compare)
- **Metamorphic properties** (relationships between inputs/outputs)

### Property Test Structure

```python
from hypothesis import given, strategies as st, settings

class TestPropertyName:
    """Property tests for [specific behavior] (Property N)."""
    
    @given(st.text(min_size=1, max_size=100))
    @settings(max_examples=20, deadline=None)  # Adjust based on complexity
    def test_property_description(self, input_value):
        """Test that [property] holds for all valid inputs.
        
        **Feature: feature-name, Property N: Property Description**
        **Validates: Requirements X.Y**
        """
        # Test implementation
        assert property_holds(input_value)
```

### Strategy Selection and max_examples

Choose `max_examples` based on strategy complexity:

- **Simple strategies** (booleans, small integers): 2-10 examples
- **Medium strategies** (text, floats): 20-50 examples  
- **Complex strategies** (nested structures): 50-100 examples
- **Combination strategies**: Based on input space size

## Helper Functions

### Using Shared Helpers

Always use helper functions from `test_utils.py` instead of duplicating code:

```python
from .test_utils import (
    find_labels_recursive,
    collect_widget_ids,
    colors_equal,
    padding_equal,
    floats_equal
)

def test_example(self):
    label = MarkdownLabel(text="Test")
    labels = find_labels_recursive(label)  # Use shared helper
    assert len(labels) > 0
```

### Available Helper Functions

#### Widget Traversal
- `find_labels_recursive(widget)` - Find all Label widgets in tree
- `collect_widget_ids(widget)` - Collect widget object IDs for rebuild testing

#### Comparison Utilities
- `colors_equal(color1, color2)` - Compare color values with tolerance
- `padding_equal(pad1, pad2)` - Compare padding values with tolerance
- `floats_equal(f1, f2, tolerance=1e-6)` - Compare floats with tolerance

#### Test Data Generation (Hypothesis Strategies)
- `markdown_heading()` - Generate valid markdown headings
- `markdown_paragraph()` - Generate valid markdown paragraphs
- `markdown_bold()` - Generate bold text markdown
- `simple_markdown_document()` - Generate simple markdown documents
- `color_strategy` - Generate valid RGBA color values

### Adding New Helpers

When adding new helper functions:

1. **Add to `test_utils.py`** - Never duplicate in individual test files
2. **Use descriptive names** - Make the purpose clear
3. **Add docstrings** - Document parameters and return values
4. **Write tests** - Add tests for complex helper functions

## Test File Structure

### Standard Test File Template

```python
"""
Brief description of what this test file covers.

This module contains tests for [specific functionality area],
including [list key areas tested].
"""

import pytest
from hypothesis import given, strategies as st, settings

from kivy_garden.markdownlabel import MarkdownLabel
from .test_utils import (
    # Import needed helpers
)


# **Feature: feature-name, Property N: Property Description**
# *For any* [universal quantification], the system SHALL [behavior].
# **Validates: Requirements X.Y**

class TestDescriptiveClassName:
    """Property tests for [specific behavior] (Property N)."""
    
    def test_specific_example(self):
        """Test [specific behavior] with concrete example."""
        # Unit test implementation
        
    @given(st.text())
    @settings(max_examples=20, deadline=None)
    def test_property_holds_universally(self, input_text):
        """Test that [property] holds for all valid inputs.
        
        **Feature: feature-name, Property N: Property Description**
        **Validates: Requirements X.Y**
        """
        # Property test implementation
```

### File Naming

- `test_[functionality_area].py` - e.g., `test_font_properties.py`
- Use underscores for word separation
- Be descriptive about the functionality area
- Group related functionality in the same file

## Best Practices

### Do's

✅ **Use descriptive test and class names**
✅ **Group related tests in the same class**
✅ **Use shared helper functions from test_utils.py**
✅ **Test both positive and negative cases**
✅ **Use appropriate pytest markers**
✅ **Write property tests for universal behaviors**
✅ **Test rebuild contracts explicitly**
✅ **Document complex test logic**

### Don'ts

❌ **Don't duplicate helper function implementations**
❌ **Don't mix unrelated functionality in the same class**
❌ **Don't use vague test names like `test_basic` or `test_misc`**
❌ **Don't claim to test rebuilds without verifying them**
❌ **Don't write property tests for simple examples**
❌ **Don't ignore test failures or skip tests without good reason**
❌ **Don't test implementation details instead of behavior**

### Performance Considerations

- **Mark slow tests** with `@pytest.mark.slow`
- **Use appropriate max_examples** for property tests
- **Avoid unnecessary widget creation** in test setup
- **Use `assume()` to filter invalid inputs** in property tests

### Debugging Tests

- **Use descriptive assertion messages** with context
- **Print intermediate values** when debugging complex failures
- **Use `pytest -v`** for verbose output
- **Use `pytest -x`** to stop on first failure
- **Use `pytest --tb=short`** for concise tracebacks

## Examples

### Complete Test Class Example

```python
class TestFontSizeImmediateUpdates:
    """Property tests for font size immediate updates (Property 3)."""
    
    def test_font_size_updates_single_label(self):
        """Test font_size updates immediately for single label."""
        label = MarkdownLabel(text="Hello", base_font_size=16)
        
        # Change font size
        label.base_font_size = 24
        
        # Verify immediate update
        labels = find_labels_recursive(label)
        assert labels[0].font_size == 24
    
    @given(
        st.floats(min_value=8.0, max_value=50.0, allow_nan=False),
        st.floats(min_value=8.0, max_value=50.0, allow_nan=False)
    )
    @settings(max_examples=20, deadline=None)
    def test_font_size_updates_preserve_scale_factors(self, initial_size, new_size):
        """Test that font size updates preserve heading scale factors.
        
        **Feature: label-compatibility, Property 3: Font size immediate update**
        **Validates: Requirements 2.1**
        """
        assume(abs(initial_size - new_size) > 1.0)
        
        label = MarkdownLabel(text="# Heading", base_font_size=initial_size)
        
        # Get heading scale factor
        heading_label = find_labels_recursive(label)[0]
        scale_factor = heading_label.font_size / initial_size
        
        # Change base font size
        label.base_font_size = new_size
        
        # Verify scale factor preserved
        expected_size = new_size * scale_factor
        assert abs(heading_label.font_size - expected_size) < 0.1
```

This testing guide ensures consistent, maintainable, and comprehensive test coverage for the MarkdownLabel project.