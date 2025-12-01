# Design Document: Label Compatibility Improvements

## Overview

This design addresses three Label API compatibility improvements for the MarkdownLabel widget:

1. **text_size height support** - Forward `text_size[1]` to child Labels for vertical alignment
2. **Padding forwarding** - Forward padding to child Labels so text isn't flush to edges
3. **Configurable auto-sizing** - Add `auto_size_height` property to control size_hint behavior

These changes make MarkdownLabel behave more consistently with Kivy's standard Label widget while maintaining backward compatibility.

## Architecture

The changes affect two main components:

```
┌─────────────────────────────────────────────────────────────┐
│                      MarkdownLabel                          │
│  (__init__.py)                                              │
│  - New: auto_size_height property                           │
│  - Modified: padding forwarding to renderer                 │
│  - Modified: text_size forwarding (already exists)          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      KivyRenderer                           │
│  (kivy_renderer.py)                                         │
│  - Modified: text_size[1] handling in Label creation        │
│  - New: padding parameter forwarding to Labels              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Child Label Widgets                      │
│  - Receive text_size with height constraint                 │
│  - Receive padding values                                   │
│  - valign works when text_size[1] is set                    │
└─────────────────────────────────────────────────────────────┘
```

## Components and Interfaces

### 1. MarkdownLabel (`__init__.py`)

#### New Property: `auto_size_height`

```python
auto_size_height = BooleanProperty(True)
"""Control automatic height sizing behavior.

When True (default):
- size_hint_y is set to None
- height is bound to minimum_height
- Widget auto-sizes to fit content

When False:
- size_hint_y is preserved (user-specified or default)
- height is NOT bound to minimum_height
- Widget participates in normal size hint layout

:attr:`auto_size_height` is a :class:`~kivy.properties.BooleanProperty`
and defaults to True.
"""
```

#### Modified: `__init__` method

```python
def __init__(self, **kwargs):
    super(MarkdownLabel, self).__init__(**kwargs)
    self.orientation = 'vertical'
    
    # Store user's size_hint_y before we potentially override it
    self._user_size_hint_y = kwargs.get('size_hint_y', 1)
    
    # Apply auto-sizing based on auto_size_height property
    if self.auto_size_height:
        self.size_hint_y = None
        self.bind(minimum_height=self.setter('height'))
    
    # Bind auto_size_height changes
    self.bind(auto_size_height=self._on_auto_size_height_changed)
    
    # ... rest of existing init code
```

#### New Method: `_on_auto_size_height_changed`

```python
def _on_auto_size_height_changed(self, instance, value):
    """Handle auto_size_height property changes."""
    if value:
        # Enable auto-sizing
        self.size_hint_y = None
        self.bind(minimum_height=self.setter('height'))
    else:
        # Disable auto-sizing
        self.unbind(minimum_height=self.setter('height'))
        self.size_hint_y = self._user_size_hint_y
```

#### Modified: `_rebuild_widgets` method

Pass padding to KivyRenderer:

```python
renderer = KivyRenderer(
    # ... existing parameters ...
    padding=list(self.padding),  # NEW: forward padding
)
```

### 2. KivyRenderer (`kivy_renderer.py`)

#### Modified: `__init__` method

Add padding parameter:

```python
def __init__(self,
             # ... existing parameters ...
             padding: Optional[List[float]] = None):  # NEW
    # ... existing initialization ...
    self.padding = padding or [0, 0, 0, 0]
```

#### Modified: Label creation methods

Update `paragraph()`, `heading()`, `block_text()`, and `_render_table_cell()` to:

1. Use `text_size[1]` when specified (not always None)
2. Apply padding to Labels

Example for `paragraph()`:

```python
def paragraph(self, token: Dict[str, Any], state: Any = None) -> Label:
    # ... existing code to build label_kwargs ...
    
    # Add padding to label
    label_kwargs['padding'] = self.padding
    
    label = Label(**label_kwargs)
    
    # Handle text_size - respect both width AND height
    text_width = self.text_size[0]
    text_height = self.text_size[1]
    
    if text_width is not None:
        if text_height is not None:
            # Both width and height specified
            label.text_size = (text_width, text_height)
        else:
            # Only width specified - bind to maintain width
            label.bind(width=lambda inst, val: setattr(
                inst, 'text_size', (text_width, None)))
    else:
        if text_height is not None:
            # Only height specified - bind width to label width
            label.bind(width=lambda inst, val: setattr(
                inst, 'text_size', (val, text_height)))
        else:
            # Neither specified - current behavior
            label.bind(width=lambda inst, val: setattr(
                inst, 'text_size', (val, None)))
    
    # ... rest of existing code ...
```

## Data Models

No new data models are required. The changes extend existing property handling.

### Property Flow

```
User sets property on MarkdownLabel
         │
         ▼
MarkdownLabel stores value
         │
         ▼
_rebuild_widgets() called
         │
         ▼
KivyRenderer created with property values
         │
         ▼
Child Labels created with forwarded properties
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: text_size Height Forwarding

*For any* MarkdownLabel with `text_size[1]` set to a non-None numeric value H, all child Labels SHALL have their `text_size[1]` equal to H, and their `valign` property SHALL match the MarkdownLabel's `valign` value.

**Validates: Requirements 1.1, 1.2**

### Property 2: text_size Height None Backward Compatibility

*For any* MarkdownLabel with `text_size[1]` set to None, all child Labels SHALL have their `text_size[1]` equal to None, maintaining the existing auto-sizing behavior.

**Validates: Requirements 1.3**

### Property 3: text_size Dynamic Updates

*For any* MarkdownLabel, when `text_size` is changed from value A to value B, all child Labels SHALL be updated to reflect the new `text_size` value B.

**Validates: Requirements 1.4**

### Property 4: Padding Forwarding to Child Labels

*For any* MarkdownLabel with `padding` set to value P, all child Labels that display text content SHALL have their `padding` property equal to P.

**Validates: Requirements 2.1, 2.2**

### Property 5: Padding Dynamic Updates

*For any* MarkdownLabel, when `padding` is changed from value A to value B, all child Labels SHALL be updated to reflect the new `padding` value B.

**Validates: Requirements 2.3**

### Property 6: Padding with Nested Structures

*For any* MarkdownLabel containing nested structures (lists, tables, block quotes), all text-containing Labels within those structures SHALL have the `padding` property applied without breaking the layout structure.

**Validates: Requirements 2.4**

### Property 7: auto_size_height True Behavior

*For any* MarkdownLabel with `auto_size_height=True`, the widget SHALL have `size_hint_y=None` AND its height SHALL be bound to `minimum_height`.

**Validates: Requirements 3.1, 3.3**

### Property 8: auto_size_height False Behavior

*For any* MarkdownLabel with `auto_size_height=False`, the widget SHALL preserve the user-specified `size_hint_y` value (or default to 1) AND its height SHALL NOT be bound to `minimum_height`.

**Validates: Requirements 3.2**

### Property 9: auto_size_height Dynamic Toggling

*For any* MarkdownLabel, when `auto_size_height` is toggled from True to False, the height binding SHALL be removed and `size_hint_y` SHALL be restored. When toggled from False to True, the height binding SHALL be added and `size_hint_y` SHALL be set to None.

**Validates: Requirements 3.4, 3.5**

## Error Handling

### Invalid Property Values

- **text_size**: If `text_size[1]` is set to a negative value, Kivy's Label will handle it (typically treating it as no constraint). No additional validation needed.
- **padding**: Kivy's VariableListProperty handles validation. Invalid values raise ValueError.
- **auto_size_height**: BooleanProperty only accepts boolean values.

### Edge Cases

1. **Empty MarkdownLabel**: When text is empty, no child Labels exist. Properties are stored but not applied until content is added.
2. **Dynamic text changes**: When text changes, widgets are rebuilt with current property values.
3. **Nested content**: Lists, tables, and block quotes contain nested Labels that must all receive forwarded properties.

## Testing Strategy

### Property-Based Testing

The project uses **Hypothesis** for property-based testing. Each correctness property will be implemented as a property-based test.

**Test Configuration:**
- Minimum 100 iterations per property test
- Tests tagged with format: `**Feature: label-compatibility, Property {N}: {description}**`

### Unit Tests

Unit tests will cover:
- Default property values
- Property initialization via kwargs
- Edge cases (empty text, None values)
- Integration with existing functionality

### Test File Location

Tests will be added to `kivy_garden/markdownlabel/tests/test_markdown_label.py` following the existing test patterns.

### Test Annotations

Each property-based test MUST include:
```python
# **Feature: label-compatibility, Property N: Property Name**
# **Validates: Requirements X.Y**
```
