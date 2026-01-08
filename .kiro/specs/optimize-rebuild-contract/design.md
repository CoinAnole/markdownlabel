# Design Document: Optimize Rebuild Contract

## Overview

This design optimizes MarkdownLabel's rebuild contract by reclassifying 14 properties from "structure" (requiring full widget tree rebuild) to "style-only" (updating existing widgets in-place). The optimization leverages Kivy's Label internal texture refresh mechanism, which regenerates text textures when properties change without destroying the Label widget object.

The key insight is that Kivy's `Label._font_properties` tuple lists all properties that trigger texture regeneration, but this happens within the existing Label widget - the widget identity is preserved. MarkdownLabel can exploit this by updating properties on existing child Labels rather than rebuilding the entire widget tree.

## Architecture

### Current Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      MarkdownLabel                          │
├─────────────────────────────────────────────────────────────┤
│  Property Change                                            │
│       │                                                     │
│       ▼                                                     │
│  ┌─────────────────┐    ┌─────────────────┐                │
│  │ STYLE_ONLY_PROP │    │ STRUCTURE_PROP  │                │
│  │ (10 properties) │    │ (18 properties) │                │
│  └────────┬────────┘    └────────┬────────┘                │
│           │                      │                          │
│           ▼                      ▼                          │
│  _update_styles_in_place()  _schedule_rebuild()            │
│  (preserves widgets)        (destroys & recreates)         │
└─────────────────────────────────────────────────────────────┘
```

### Optimized Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      MarkdownLabel                          │
├─────────────────────────────────────────────────────────────┤
│  Property Change                                            │
│       │                                                     │
│       ▼                                                     │
│  ┌─────────────────┐    ┌─────────────────┐                │
│  │ STYLE_ONLY_PROP │    │ STRUCTURE_PROP  │                │
│  │ (24 properties) │    │ (4 properties)  │                │
│  └────────┬────────┘    └────────┬────────┘                │
│           │                      │                          │
│           ▼                      ▼                          │
│  _update_styles_in_place()  _schedule_rebuild()            │
│  (preserves widgets)        (destroys & recreates)         │
└─────────────────────────────────────────────────────────────┘
```

### Property Reclassification

| Property | Old Classification | New Classification | Reason |
|----------|-------------------|-------------------|--------|
| `font_family` | Structure | Style-Only | Kivy Label handles via texture refresh |
| `font_context` | Structure | Style-Only | Kivy Label handles via texture refresh |
| `font_features` | Structure | Style-Only | Kivy Label handles via texture refresh |
| `font_hinting` | Structure | Style-Only | Kivy Label handles via texture refresh |
| `font_kerning` | Structure | Style-Only | Kivy Label handles via texture refresh |
| `font_blended` | Structure | Style-Only | Kivy Label handles via texture refresh |
| `unicode_errors` | Structure | Style-Only | Kivy Label handles via texture refresh |
| `strip` | Structure | Style-Only | Kivy Label handles via texture refresh |
| `shorten` | Structure | Style-Only | Kivy Label handles via texture refresh |
| `max_lines` | Structure | Style-Only | Kivy Label handles via texture refresh |
| `shorten_from` | Structure | Style-Only | Kivy Label handles via texture refresh |
| `split_str` | Structure | Style-Only | Kivy Label handles via texture refresh |
| `ellipsis_options` | Structure | Style-Only | Kivy Label handles via texture refresh |
| `text_size` | Structure | Style-Only | Kivy Label handles via texture refresh (with binding management) |

## Components and Interfaces

### Modified Components

#### 1. MarkdownLabel Class (`__init__.py`)

**STYLE_ONLY_PROPERTIES Update:**
```python
STYLE_ONLY_PROPERTIES = frozenset({
    # Existing style-only properties
    'color',
    'halign',
    'valign',
    'line_height',
    'disabled',
    'disabled_color',
    'base_direction',
    'text_padding',
    'outline_color',
    'disabled_outline_color',
    'outline_width',
    'mipmap',
    'text_language',
    'limit_render_to_text_bbox',
    'font_name',
    'code_font_name',
    # Newly reclassified properties
    'font_family',
    'font_context',
    'font_features',
    'font_hinting',
    'font_kerning',
    'font_blended',
    'unicode_errors',
    'strip',
    'shorten',
    'max_lines',
    'shorten_from',
    'split_str',
    'ellipsis_options',
    'text_size',
})
```

**STRUCTURE_PROPERTIES Update:**
```python
STRUCTURE_PROPERTIES = frozenset({
    'text',
    'link_style',
    'render_mode',
    'strict_label_mode',
})
```

#### 2. Extended `_update_styles_in_place()` Method

The method will be extended to handle all newly reclassified properties:

```python
def _update_styles_in_place(self):
    """Update style properties on existing child widgets without rebuild."""
    
    def update_widget(widget):
        if isinstance(widget, Label):
            # Existing style updates
            widget.color = effective_color
            widget.halign = effective_halign
            widget.valign = self.valign
            widget.line_height = self.line_height
            widget.padding = effective_text_padding
            
            # Font name (respecting code blocks)
            if hasattr(widget, '_is_code') and widget._is_code:
                widget.font_name = self.code_font_name
            else:
                widget.font_name = self.font_name
                # font_family only applies to non-code Labels
                if self.font_family is not None:
                    widget.font_family = self.font_family
            
            # Advanced font properties (all Labels)
            if self.font_context is not None:
                widget.font_context = self.font_context
            widget.font_features = self.font_features
            if self.font_hinting is not None:
                widget.font_hinting = self.font_hinting
            widget.font_kerning = self.font_kerning
            widget.font_blended = self.font_blended
            
            # Text processing properties
            widget.unicode_errors = self.unicode_errors
            widget.strip = self.strip
            
            # Truncation properties
            widget.shorten = self.shorten
            if self.max_lines > 0:
                widget.max_lines = self.max_lines
            widget.shorten_from = self.shorten_from
            widget.split_str = self.split_str
            widget.ellipsis_options = dict(self.ellipsis_options)
            
            # Existing outline/mipmap/direction properties
            widget.outline_width = self.outline_width
            widget.outline_color = effective_outline_color
            widget.disabled_outline_color = list(self.disabled_outline_color)
            widget.mipmap = self.mipmap
            widget.base_direction = self.base_direction
            widget.text_language = self.text_language
            widget.limit_render_to_text_bbox = self.limit_render_to_text_bbox
        
        # Recurse into children
        if hasattr(widget, 'children'):
            for child in widget.children:
                update_widget(child)
    
    for child in self.children:
        update_widget(child)
```

#### 3. New `_update_text_size_in_place()` Method

A dedicated method for text_size updates with binding management:

```python
def _update_text_size_in_place(self):
    """Update text_size on existing child widgets with binding management."""
    text_width = self.text_size[0]
    text_height = self.text_size[1]
    
    def update_widget(widget):
        if isinstance(widget, Label):
            # Update text_size directly
            if text_width is not None and text_height is not None:
                widget.text_size = (text_width, text_height)
            elif text_width is not None:
                widget.text_size = (text_width, None)
            elif text_height is not None:
                widget.text_size = (widget.width, text_height)
            else:
                # [None, None] - let width binding handle it if not strict mode
                if not self.strict_label_mode:
                    widget.text_size = (widget.width, None)
                else:
                    widget.text_size = (None, None)
        
        if hasattr(widget, 'children'):
            for child in widget.children:
                update_widget(child)
    
    for child in self.children:
        update_widget(child)
```

## Data Models

No new data models are required. The existing property classification sets (`STYLE_ONLY_PROPERTIES`, `STRUCTURE_PROPERTIES`) are updated with new members.

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system - essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Style-only property updates preserve widget identity

*For any* MarkdownLabel with rendered content and *for any* style-only property from the newly reclassified set (`font_family`, `font_context`, `font_features`, `font_hinting`, `font_kerning`, `font_blended`, `unicode_errors`, `strip`, `shorten`, `max_lines`, `shorten_from`, `split_str`, `ellipsis_options`), changing that property should preserve all widget object identities (same Python `id()` values before and after the change).

**Validates: Requirements 1.1-1.7, 2.1-2.3, 3.1-3.6**

### Property 2: Style-only property updates apply values to all child Labels

*For any* MarkdownLabel with rendered content and *for any* style-only property from the newly reclassified set, changing that property should result in all child Label widgets having the new property value.

**Validates: Requirements 1.1-1.6, 2.1-2.2, 3.1-3.5**

### Property 3: text_size updates preserve widget identity

*For any* MarkdownLabel with rendered content and *for any* valid text_size value (including `[None, None]`, `[width, None]`, `[None, height]`, `[width, height]`), changing text_size should preserve all widget object identities.

**Validates: Requirements 4.1, 4.4**

### Property 4: Code blocks preserve monospace font when font_family changes

*For any* MarkdownLabel containing code blocks and *for any* font_family value, changing font_family should update non-code Labels but preserve the `code_font_name` on code block Labels.

**Validates: Requirements 6.2**

### Property 5: Property classification sets are mutually exclusive and complete

*For all* properties in STYLE_ONLY_PROPERTIES and STRUCTURE_PROPERTIES, no property should appear in both sets, and the union should cover all properties that affect rendering.

**Validates: Requirements 5.1-5.6**

## Error Handling

### Invalid Property Values

When invalid property values are provided:
- Kivy's property system will raise appropriate exceptions (e.g., `ValueError` for invalid `font_hinting` options)
- No special error handling is needed in the style update methods

### Missing Widget Attributes

When updating properties on widgets that may not have certain attributes:
- Use `hasattr()` checks before setting properties
- This handles edge cases like custom widgets in the tree

```python
if hasattr(widget, 'font_hinting'):
    widget.font_hinting = self.font_hinting
```

## Testing Strategy

### Dual Testing Approach

Testing will use both unit tests and property-based tests:

- **Unit tests**: Verify specific examples, edge cases, and property classification correctness
- **Property tests**: Verify universal properties across many generated inputs

### Property-Based Testing Configuration

- **Library**: Hypothesis
- **Minimum iterations**: 100 per property test
- **Tag format**: `Feature: optimize-rebuild-contract, Property N: [property_text]`

### Test Categories

#### 1. Widget Identity Preservation Tests

Property-based tests verifying that style-only property changes preserve widget identities:

```python
@given(
    property_name=st.sampled_from([
        'font_family', 'font_context', 'font_features', 'font_hinting',
        'font_kerning', 'font_blended', 'unicode_errors', 'strip',
        'shorten', 'max_lines', 'shorten_from', 'split_str', 'ellipsis_options'
    ]),
    # Property value generators based on property type
)
def test_style_property_preserves_widget_identity(property_name, value):
    """Property 1: Style-only updates preserve widget identity."""
    label = MarkdownLabel(text='# Heading\n\nParagraph')
    ids_before = collect_widget_ids(label)
    setattr(label, property_name, value)
    ids_after = collect_widget_ids(label)
    assert ids_before == ids_after
```

#### 2. Property Value Application Tests

Property-based tests verifying that property values are correctly applied to child Labels:

```python
@given(font_hinting=st.sampled_from([None, 'normal', 'light', 'mono']))
def test_font_hinting_applied_to_children(font_hinting):
    """Property 2: Style-only updates apply values to children."""
    label = MarkdownLabel(text='Hello World')
    label.font_hinting = font_hinting
    labels = find_labels_recursive(label)
    assert all(l.font_hinting == font_hinting for l in labels)
```

#### 3. text_size Specific Tests

Tests for text_size binding management:

```python
def test_text_size_transition_none_to_constrained():
    """Requirement 4.2: text_size [None, None] to constrained."""
    label = MarkdownLabel(text='Hello', text_size=[None, None])
    ids_before = collect_widget_ids(label)
    label.text_size = [100, None]
    ids_after = collect_widget_ids(label)
    assert ids_before == ids_after
    labels = find_labels_recursive(label)
    assert all(l.text_size[0] == 100 for l in labels)
```

#### 4. Code Block Font Preservation Tests

```python
@given(font_family=st.text(min_size=1, max_size=20))
def test_code_blocks_preserve_monospace_font(font_family):
    """Property 4: Code blocks preserve monospace font."""
    label = MarkdownLabel(text='```\ncode\n```\n\ntext')
    label.font_family = font_family
    for lbl in find_labels_recursive(label):
        if hasattr(lbl, '_is_code') and lbl._is_code:
            assert lbl.font_name == label.code_font_name
        else:
            # Non-code labels may have font_family set
            pass
```

#### 5. Property Classification Tests

Unit tests verifying set membership:

```python
def test_reclassified_properties_in_style_only():
    """Requirement 5.1-5.4: Properties in STYLE_ONLY_PROPERTIES."""
    reclassified = {
        'font_family', 'font_context', 'font_features', 'font_hinting',
        'font_kerning', 'font_blended', 'unicode_errors', 'strip',
        'shorten', 'max_lines', 'shorten_from', 'split_str',
        'ellipsis_options', 'text_size'
    }
    assert reclassified.issubset(MarkdownLabel.STYLE_ONLY_PROPERTIES)

def test_structure_properties_unchanged():
    """Requirement 5.6: Structure properties retained."""
    expected = {'text', 'link_style', 'render_mode', 'strict_label_mode'}
    assert expected == MarkdownLabel.STRUCTURE_PROPERTIES
```

### Performance Validation

Benchmark tests comparing rebuild time vs style-only update time:

```python
def test_style_update_faster_than_rebuild():
    """Verify style-only updates are faster than rebuilds."""
    label = MarkdownLabel(text='# Heading\n\n' + 'Paragraph\n\n' * 10)
    
    # Time style-only update
    start = time.perf_counter()
    label.font_hinting = 'light'
    style_time = time.perf_counter() - start
    
    # Time rebuild
    start = time.perf_counter()
    label.text = label.text + ' '  # Force rebuild
    rebuild_time = time.perf_counter() - start
    
    assert style_time < rebuild_time
```
