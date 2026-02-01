# MarkdownLabel Rebuild Contract

This document defines the rebuild contract for MarkdownLabel - which property changes trigger widget tree rebuilds versus style-only updates.

## Overview

MarkdownLabel optimizes performance by distinguishing between two types of property changes:

1. **Style-only changes** - Update existing widgets in place without rebuilding the widget tree
2. **Structure changes** - Rebuild the entire widget tree from scratch

### Degenerate Markdown normalization

When the parsed Markdown is a single structural token with no meaningful content
(e.g., a lone list marker `-`/`*`/`+`, `1.`/`1)`, or a bare `>` blockquote
marker), MarkdownLabel normalizes it to a paragraph `Label` showing the literal
input for Label-like UX. Inputs with actual content continue to render with
strict Markdown semantics.

Understanding this contract is crucial for:
- **Performance optimization** - Avoiding unnecessary rebuilds
- **Test writing** - Knowing when to test for rebuilds vs. value updates
- **API design** - Ensuring consistent behavior across properties

## Style-Only Properties

These properties update existing widgets **without rebuilding** the widget tree:

### Font Properties
- `base_font_size` / `font_size` - Updates `Label.font_size` on all existing Labels
- `font_name` - Updates `Label.font_name` on all existing Labels (respects code block font settings)
- `code_font_name` - Updates `Label.font_name` on code block Labels only
- `line_height` - Updates `Label.line_height` on all existing Labels

### Color Properties
- `color` - Updates `Label.color` on all existing Labels (except code blocks)
- `disabled` - Updates disabled state, switching between `color` and `disabled_color`
- `disabled_color` - Updates `Label.disabled_color` when widget is disabled
- `outline_color` - Updates `Label.outline_color` on all existing Labels
- `disabled_outline_color` - Updates `Label.disabled_outline_color` when widget is disabled

### Text Layout Properties
- `halign` - Updates `Label.halign` on all existing Labels
- `valign` - Updates `Label.valign` on all existing Labels
- `base_direction` - Updates `Label.base_direction` on all existing Labels

### Outline Properties
- `outline_width` - Updates `Label.outline_width` on all existing Labels

### Container Properties
- `padding` - Updates BoxLayout container padding without rebuilding child widgets
- `text_padding` - Updates `Label.padding` on all existing Labels

### Advanced Label Properties
- `mipmap` - Updates `Label.mipmap` on all existing Labels
- `text_language` - Updates `Label.text_language` on all existing Labels
- `limit_render_to_text_bbox` - Updates `Label.limit_render_to_text_bbox` on all existing Labels

### Advanced Font Properties
- `font_family` - Updates `Label.font_family` on non-code Labels (code blocks preserve monospace font)
- `font_context` - Updates `Label.font_context` on all existing Labels
- `font_features` - Updates `Label.font_features` on all existing Labels
- `font_hinting` - Updates `Label.font_hinting` on all existing Labels
- `font_kerning` - Updates `Label.font_kerning` on all existing Labels
- `font_blended` - Updates `Label.font_blended` on all existing Labels

### Text Processing Properties
- `unicode_errors` - Updates `Label.unicode_errors` on all existing Labels
- `strip` - Updates `Label.strip` on all existing Labels

### Truncation Properties
- `shorten` - Updates `Label.shorten` on all existing Labels
- `max_lines` - Updates `Label.max_lines` on all existing Labels (only if > 0)
- `shorten_from` - Updates `Label.shorten_from` on all existing Labels
- `split_str` - Updates `Label.split_str` on all existing Labels
- `ellipsis_options` - Updates `Label.ellipsis_options` on all existing Labels (as dict copy)

### Layout Properties
- `text_size` - Updates `Label.text_size` on all existing Labels with binding management

## Structure Properties

These properties trigger a **complete widget tree rebuild**:

### Content Properties
- `text` - Changes the markdown content, requiring new parsing and widget creation

### Rendering Properties
- `render_mode` - Changes between 'widgets', 'texture', and 'auto' rendering modes
- `strict_label_mode` - Changes layout behavior, affecting widget hierarchy

### Parser Configuration
- `link_style` - Changes link rendering behavior, requires rebuild to regenerate markup

### Color Properties
- `link_color` - Changes link color, requires rebuild to regenerate markup with new color
- `code_bg_color` - Changes code block background color, requires rebuild to regenerate markup with new background

### Font Fallback Properties
- `fallback_enabled` - Enables/disables font fallback system, requires rebuild to regenerate markup
- `fallback_fonts` - List of fallback fonts for Unicode coverage, requires rebuild to regenerate markup
- `fallback_font_scales` - Per-font size scaling factors, requires rebuild to regenerate markup

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

`MarkdownLabel.update_style(**kwargs)` batches multiple assignments. Style-only
changes apply immediately in-place once, while any structure property in the
kwargs schedules a single rebuild after all assignments complete.

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

Use these helpers from `kivy_garden.markdownlabel.utils`:

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
- **Behavior**: Updates `Label.font_name` on all existing Labels in place
- **Exception**: Code blocks preserve their `code_font_name` setting (checked via `_is_code` marker)
- **Fallback**: Uses system default if font not found
- **Performance**: Fast O(n) update where n = number of Labels

#### `code_font_name`
- **Type**: Style-only
- **Behavior**: Updates `Label.font_name` on code block Labels only (identified by `_is_code` marker)
- **Scope**: Only affects Labels inside code block containers
- **Performance**: Fast O(n) update where n = number of code Labels

### Color Properties

#### `color`
- **Type**: Style-only
- **Behavior**: Updates `Label.color` on all Labels
- **Exception**: Code blocks preserve their light color `[0.9, 0.9, 0.9, 1]`
- **Format**: RGBA list `[r, g, b, a]` with values 0.0-1.0

#### `outline_width`
- **Type**: Style-only
- **Behavior**: Updates `Label.outline_width` on all existing Labels in place
- **Format**: Float value (typically 0-10)
- **Performance**: Fast O(n) update where n = number of Labels

### Text Properties

#### `text`
- **Type**: Structure (requires rebuild)
- **Reason**: Changes markdown content, requiring new parsing
- **Behavior**: Complete widget tree recreation
- **Performance**: May be deferred for rapid changes

#### `padding`
- **Type**: Style-only
- **Behavior**: Updates container padding without rebuilding the widget tree
- **Scope**: Affects the BoxLayout container only (child Labels use `text_padding`)
- **Performance**: Fast O(1) update (no traversal needed)

#### `text_size`
- **Type**: Style-only
- **Behavior**: Updates `Label.text_size` on all existing Labels with binding management
- **Layout impact**: Affects how text wraps and flows
- **None handling**: `(None, None)` allows unlimited size, respects `strict_label_mode`
- **Binding management**: Handles transitions between constrained and unconstrained states and
  rebinds/unbinds width/texture callbacks to avoid stale captured widths
- **Performance**: Fast O(n) update where n = number of Labels

#### `text_padding`
- **Type**: Style-only
- **Behavior**: Updates `Label.padding` on all existing Labels
- **Purpose**: Controls padding within individual Label widgets, not container padding
- **Format**: List `[left, top, right, bottom]` with float values
- **Difference from `padding`**: `padding` affects the MarkdownLabel container, `text_padding` affects child Labels

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

### Performance Benefits of Property Reclassification

The optimization of reclassifying 14 properties from "structure" to "style-only" provides significant performance benefits:

| Property Category | Properties Reclassified | Benefit |
|-------------------|------------------------|---------|
| Advanced Font | `font_family`, `font_context`, `font_features`, `font_hinting`, `font_kerning`, `font_blended` | Dynamic font adjustments without rebuild |
| Text Processing | `unicode_errors`, `strip` | Text handling changes without rebuild |
| Truncation | `shorten`, `max_lines`, `shorten_from`, `split_str`, `ellipsis_options` | Responsive text displays without rebuild |
| Layout | `text_size` | Container size changes without rebuild |

**Key insight**: Kivy's Label internally handles these properties via texture refresh, which regenerates the text texture without destroying the Label widget. MarkdownLabel exploits this by updating properties on existing child Labels rather than rebuilding the entire widget tree.

**Typical performance improvement**:
- Style-only update: ~1-5ms for typical documents
- Full rebuild: ~10-50ms for typical documents
- Improvement factor: 5-10x faster for property changes

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
    
def update_formatting(label, font_size, font_name, color):
    """Update label formatting without rebuild."""
    label.base_font_size = font_size  # Style-only
    label.font_name = font_name       # Style-only
    label.color = color               # Style-only

def update_advanced_font_settings(label, font_family, font_hinting, font_kerning):
    """Update advanced font settings without rebuild."""
    label.font_family = font_family   # Style-only (reclassified)
    label.font_hinting = font_hinting # Style-only (reclassified)
    label.font_kerning = font_kerning # Style-only (reclassified)

def update_truncation_settings(label, shorten, max_lines, shorten_from):
    """Update truncation settings without rebuild."""
    label.shorten = shorten           # Style-only (reclassified)
    label.max_lines = max_lines       # Style-only (reclassified)
    label.shorten_from = shorten_from # Style-only (reclassified)
```

### Performance-Critical Updates

```python
def animate_font_size(label, target_size, duration=1.0):
    """Animate font size change smoothly."""
    # Style-only changes are fast enough for animation
    from kivy.animation import Animation
    Animation(base_font_size=target_size, duration=duration).start(label)

def animate_outline(label, target_width, duration=0.5):
    """Animate outline width change smoothly."""
    # Style-only changes are fast enough for animation
    from kivy.animation import Animation
    Animation(outline_width=target_width, duration=duration).start(label)
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