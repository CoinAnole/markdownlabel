# MarkdownLabel Rebuild Contract

This document defines the rebuild contract for MarkdownLabel - which property changes trigger widget tree rebuilds versus style-only updates.

## Overview

MarkdownLabel optimizes performance by distinguishing between two types of property changes:

1. **Style-only changes** - Update existing widgets in place without rebuilding the widget tree
2. **Structure changes** - Rebuild the entire widget tree from scratch

Understanding this contract is crucial for:
- **Performance optimization** - Avoiding unnecessary rebuilds
- **Test writing** - Knowing when to test for rebuilds vs. value updates
- **API design** - Ensuring consistent behavior across properties

## Style-Only Properties

These properties update existing widgets **without rebuilding** the widget tree:

### Font Properties
- `base_font_size` / `font_size` - Updates `Label.font_size` on all existing Labels
- `font_name` - Updates `Label.font_name` on all existing Labels (except code blocks)
- `line_height` - Updates `Label.line_height` on all existing Labels
- `font_family` - Updates `Label.font_family` on non-code Labels
- `font_context` - Updates `Label.font_context` on all Labels
- `font_features` - Updates `Label.font_features` on all Labels
- `font_hinting` - Updates `Label.font_hinting` on all Labels
- `font_kerning` - Updates `Label.font_kerning` on all Labels

### Color Properties
- `color` - Updates `Label.color` on all existing Labels (except code blocks)
- `disabled_color` - Updates `Label.disabled_color` when widget is disabled

### Text Layout Properties
- `halign` - Updates `Label.halign` on all existing Labels
- `valign` - Updates `Label.valign` on all existing Labels
- `text_size` - Updates `Label.text_size` on all existing Labels

### Container Properties
- `padding` - Updates container padding without rebuilding child widgets
- `spacing` - Updates container spacing without rebuilding child widgets

## Structure Properties

These properties trigger a **complete widget tree rebuild**:

### Content Properties
- `text` - Changes the markdown content, requiring new parsing and widget creation
- `markup` - Changes how text is interpreted (markdown vs. plain text)

### Rendering Properties
- `render_mode` - Changes between 'widgets', 'texture', and 'auto' rendering modes
- `strict_label_mode` - Changes layout behavior, affecting widget hierarchy

### Parser Configuration
- `code_font_name` - Affects code block rendering, requires rebuild to apply
- `link_style` - Changes link rendering behavior, requires rebuild

## Implementation Details

### Style-Only Update Mechanism

When a style-only property changes:

1. **Property setter** is called on MarkdownLabel
2. **Value is stored** in the MarkdownLabel instance
3. **Existing widgets are traversed** using `find_labels_recursive()`
4. **Property is applied** to each relevant widget
5. **Widget tree structure remains unchanged** (same object identities)

```python
def _update_font_size(self, new_size):
    """Update font_size on all existing Labels without rebuilding."""
    self._base_font_size = new_size
    
    # Update existing Labels in place
    for label in find_labels_recursive(self):
        scale = getattr(label, '_font_scale', 1.0)
        label.font_size = new_size * scale
```

### Structure Rebuild Mechanism

When a structure property changes:

1. **Property setter** is called on MarkdownLabel
2. **Value is stored** in the MarkdownLabel instance
3. **Rebuild is scheduled** (may be deferred for performance)
4. **Old widget tree is cleared** (`self.clear_widgets()`)
5. **New widget tree is created** from updated property values
6. **Widget object identities change** (new objects created)

```python
def _rebuild_widget_tree(self):
    """Rebuild the entire widget tree from current properties."""
    # Clear existing widgets
    self.clear_widgets()
    
    # Parse markdown with current text
    tokens = self._parse_markdown(self.text)
    
    # Create new widget tree
    for token in tokens:
        widget = self._render_token(token)
        self.add_widget(widget)
```

## Testing the Rebuild Contract

### Testing Style-Only Changes

Use `collect_widget_ids()` to verify widget identities are preserved:

```python
def test_font_size_preserves_widget_tree(self):
    """Test that font_size changes preserve widget identities."""
    label = MarkdownLabel(text="# Heading\n\nParagraph")
    
    # Collect widget IDs before change
    ids_before = collect_widget_ids(label)
    
    # Change style-only property
    label.base_font_size = 20
    
    # Verify widget tree structure preserved
    ids_after = collect_widget_ids(label)
    assert ids_before == ids_after, "Widget identities should be preserved"
    
    # Verify style change applied
    labels = find_labels_recursive(label)
    for lbl in labels:
        expected_size = 20 * getattr(lbl, '_font_scale', 1.0)
        assert abs(lbl.font_size - expected_size) < 0.1
```

### Testing Structure Changes

Use `collect_widget_ids()` to verify widget identities change:

```python
def test_text_change_rebuilds_widget_tree(self):
    """Test that text changes rebuild the widget tree."""
    label = MarkdownLabel(text="Original text")
    
    # Collect widget IDs before change
    ids_before = collect_widget_ids(label)
    
    # Change structure property
    label.text = "New text with different structure"
    
    # Verify widget tree was rebuilt
    ids_after = collect_widget_ids(label)
    assert ids_before != ids_after, "Widget identities should change"
    
    # Verify content change applied
    assert label.text == "New text with different structure"
```

### Helper Functions

Use these helpers from `test_utils.py`:

```python
def collect_widget_ids(widget):
    """Collect Python object IDs of all widgets in the tree.
    
    Returns:
        Set of widget object IDs for identity comparison
    """
    
def assert_rebuild_occurred(widget, change_func):
    """Assert that a change function triggers a rebuild.
    
    Args:
        widget: MarkdownLabel instance
        change_func: Function that makes the change
    """
    
def assert_no_rebuild(widget, change_func):
    """Assert that a change function does NOT trigger a rebuild.
    
    Args:
        widget: MarkdownLabel instance  
        change_func: Function that makes the change
    """
```

## Property-Specific Behavior

### Font Properties

#### `base_font_size` / `font_size`
- **Type**: Style-only
- **Behavior**: Updates `Label.font_size` on all Labels, preserving scale factors
- **Scale factors**: Headings use `HEADING_SIZES` multipliers (h1=2.0, h2=1.5, etc.)
- **Code blocks**: Use same font_size as other content

#### `font_name`
- **Type**: Style-only
- **Behavior**: Updates `Label.font_name` on all Labels
- **Exception**: Code blocks preserve their `code_font_name` setting
- **Fallback**: Uses system default if font not found

#### `code_font_name`
- **Type**: Structure (requires rebuild)
- **Reason**: Code blocks need to be re-rendered with new font
- **Behavior**: Only affects Labels inside code block containers

### Color Properties

#### `color`
- **Type**: Style-only
- **Behavior**: Updates `Label.color` on all Labels
- **Exception**: Code blocks preserve their light color `[0.9, 0.9, 0.9, 1]`
- **Format**: RGBA list `[r, g, b, a]` with values 0.0-1.0

### Text Properties

#### `text`
- **Type**: Structure (requires rebuild)
- **Reason**: Changes markdown content, requiring new parsing
- **Behavior**: Complete widget tree recreation
- **Performance**: May be deferred for rapid changes

#### `text_size`
- **Type**: Style-only
- **Behavior**: Updates `Label.text_size` on all Labels
- **Layout impact**: May trigger Kivy layout recalculation
- **None handling**: `(None, None)` allows unlimited size

### Rendering Properties

#### `render_mode`
- **Type**: Structure (requires rebuild)
- **Values**: `'widgets'`, `'texture'`, `'auto'`
- **Reason**: Fundamentally changes rendering approach
- **Widget mode**: Creates Label widgets for each text element
- **Texture mode**: Renders to single texture image

#### `strict_label_mode`
- **Type**: Structure (requires rebuild)
- **Reason**: Changes container layout behavior
- **True**: Behaves more like standard Kivy Label
- **False**: Uses flexible BoxLayout container

## Performance Implications

### Style-Only Changes
- **Fast**: O(n) where n = number of Labels
- **No parsing**: Reuses existing widget tree
- **No layout**: Minimal Kivy layout recalculation
- **Memory**: No additional allocation

### Structure Changes
- **Slower**: O(m) where m = markdown complexity
- **Full parsing**: Re-parses entire markdown content
- **Full layout**: Complete Kivy layout recalculation  
- **Memory**: Allocates new widget objects

### Optimization Strategies

1. **Batch style changes** when possible:
   ```python
   # Good: Single update
   label.update_style(font_size=16, color=[1,0,0,1])
   
   # Less efficient: Multiple updates
   label.font_size = 16
   label.color = [1, 0, 0, 1]
   ```

2. **Defer structure changes** during rapid updates:
   ```python
   # MarkdownLabel automatically defers rebuilds during rapid text changes
   label.text = "First change"
   label.text = "Second change"  # Only rebuilds once
   ```

3. **Use style properties** when possible instead of changing text:
   ```python
   # Good: Style-only change
   label.color = [1, 0, 0, 1]
   
   # Less efficient: Structure change
   label.text = f"[color=ff0000]{original_text}[/color]"
   ```

## Common Patterns

### Conditional Styling

```python
def update_theme(label, dark_mode=False):
    """Update label theme without rebuilding."""
    if dark_mode:
        label.color = [0.9, 0.9, 0.9, 1.0]  # Light text
    else:
        label.color = [0.1, 0.1, 0.1, 1.0]  # Dark text
    # No rebuild required - style-only change
```

### Dynamic Content

```python
def update_content(label, new_markdown):
    """Update label content (triggers rebuild)."""
    label.text = new_markdown  # Structure change - rebuild required
    
def update_formatting(label, font_size, color):
    """Update label formatting without rebuild."""
    label.base_font_size = font_size  # Style-only
    label.color = color               # Style-only
```

### Performance-Critical Updates

```python
def animate_font_size(label, target_size, duration=1.0):
    """Animate font size change smoothly."""
    # Style-only changes are fast enough for animation
    from kivy.animation import Animation
    Animation(base_font_size=target_size, duration=duration).start(label)
```

## Debugging Rebuild Issues

### Identifying Unexpected Rebuilds

```python
def debug_rebuild_behavior(label, change_func):
    """Debug whether a change triggers a rebuild."""
    ids_before = collect_widget_ids(label)
    change_func()
    ids_after = collect_widget_ids(label)
    
    if ids_before != ids_after:
        print("REBUILD OCCURRED - widget identities changed")
    else:
        print("NO REBUILD - widget identities preserved")
```

### Common Rebuild Issues

1. **Unexpected rebuilds**: Property marked as style-only but triggers rebuild
2. **Missing rebuilds**: Property marked as structure but doesn't rebuild
3. **Partial updates**: Some widgets updated, others not
4. **Performance issues**: Too many rebuilds during rapid changes

### Debugging Tools

- `collect_widget_ids()` - Check widget identity preservation
- `find_labels_recursive()` - Inspect widget tree structure
- `pytest -v` - Verbose test output for rebuild tests
- Kivy Inspector - Visual widget tree inspection

## Future Considerations

### Potential Optimizations

1. **Partial rebuilds** - Rebuild only affected subtrees
2. **Change batching** - Batch multiple property changes
3. **Lazy evaluation** - Defer rebuilds until widget is visible
4. **Caching** - Cache parsed AST for identical text

### API Stability

The rebuild contract is part of the public API. Changes to which properties trigger rebuilds should be:

1. **Documented** in changelog
2. **Tested** with explicit rebuild contract tests
3. **Backward compatible** when possible
4. **Performance justified** when breaking compatibility

This contract ensures predictable, performant behavior for MarkdownLabel users while maintaining clear testing guidelines for developers.