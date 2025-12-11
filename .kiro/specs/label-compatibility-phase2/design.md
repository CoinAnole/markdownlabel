# Design Document: Label Compatibility Phase 2

## Overview

This design addresses Phase 2 of Label API compatibility improvements for MarkdownLabel, building on Phase 1 (text_size height, padding forwarding, auto_size_height). The goal is comprehensive drop-in compatibility with Kivy's standard Label widget.

Key improvements:
1. **No-op property acceptance** - Accept all common Label properties without crashing
2. **Strict Label mode** - Optional mode matching Label's exact sizing semantics
3. **Accurate texture_size** - Include all widget types in calculation
4. **Shortening property forwarding** - Forward shorten/max_lines/ellipsis_options to all child Labels
5. **Coordinate translation** - Translate refs/anchors to MarkdownLabel's coordinate space
6. **Font advanced property forwarding** - Forward font_family, font_context, etc.
7. **Efficient style updates** - Update styles in-place without full rebuild

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           MarkdownLabel                                  │
│  (__init__.py)                                                          │
│                                                                          │
│  New Properties:                                                         │
│  - strict_label_mode: BooleanProperty(False)                            │
│  - mipmap, outline_width, outline_color (no-op)                         │
│  - text_language, base_direction (no-op)                                │
│  - ellipsis_options: DictProperty({})                                   │
│                                                                          │
│  Modified:                                                               │
│  - texture_size: Include all widget types                               │
│  - refs/anchors: Coordinate translation                                 │
│  - _rebuild_widgets: Conditional rebuild for style-only changes         │
│  - __init__: Handle strict_label_mode                                   │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           KivyRenderer                                   │
│  (kivy_renderer.py)                                                     │
│                                                                          │
│  New Parameters:                                                         │
│  - strict_label_mode: bool                                              │
│  - ellipsis_options: dict                                               │
│                                                                          │
│  Modified:                                                               │
│  - Label creation: Conditional text_size binding based on mode          │
│  - ellipsis_options forwarding to child Labels                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## Components and Interfaces

### 1. MarkdownLabel - New No-op Properties

```python
# No-op properties for Label API compatibility
# These are accepted but have no effect on rendering

mipmap = BooleanProperty(False)
"""No-op property for Label API compatibility.

This property is accepted but has no effect on rendering.
MarkdownLabel does not use texture mipmapping.

:attr:`mipmap` is a :class:`~kivy.properties.BooleanProperty`
and defaults to False.
"""

outline_width = NumericProperty(0)
"""No-op property for Label API compatibility.

This property is accepted but has no effect on rendering.
Text outline is not supported in MarkdownLabel.

:attr:`outline_width` is a :class:`~kivy.properties.NumericProperty`
and defaults to 0.
"""

outline_color = ColorProperty([0, 0, 0, 1])
"""No-op property for Label API compatibility.

This property is accepted but has no effect on rendering.
Text outline is not supported in MarkdownLabel.

:attr:`outline_color` is a :class:`~kivy.properties.ColorProperty`
and defaults to [0, 0, 0, 1].
"""

text_language = StringProperty(None, allownone=True)
"""No-op property for Label API compatibility.

This property is accepted but has no effect on rendering.

:attr:`text_language` is a :class:`~kivy.properties.StringProperty`
and defaults to None.
"""

base_direction = OptionProperty(None, options=[None, 'ltr', 'rtl', 'weak_ltr', 'weak_rtl'], allownone=True)
"""No-op property for Label API compatibility.

This property is accepted but has no effect on rendering.

:attr:`base_direction` is an :class:`~kivy.properties.OptionProperty`
and defaults to None.
"""

ellipsis_options = DictProperty({})
"""Ellipsis options for text shortening.

This dictionary is forwarded to all child Labels that support it.
See Kivy Label documentation for available options.

:attr:`ellipsis_options` is a :class:`~kivy.properties.DictProperty`
and defaults to {}.
"""
```

### 2. MarkdownLabel - Strict Label Mode

```python
strict_label_mode = BooleanProperty(False)
"""Enable strict Label API compatibility mode.

When True:
- auto_size_height behavior is disabled (size_hint_y preserved)
- text_size bindings only apply when text_size is explicitly set
- Widget follows Label's sizing semantics exactly

When False (default):
- Markdown-friendly auto-wrap and auto-size behavior
- Internal Labels bind width to parent for text wrapping
- Widget auto-sizes to content height

:attr:`strict_label_mode` is a :class:`~kivy.properties.BooleanProperty`
and defaults to False.
"""

def __init__(self, **kwargs):
    # ... existing code ...
    
    # Handle strict_label_mode
    if self.strict_label_mode:
        # Override auto_size_height behavior
        self._user_size_hint_y = kwargs.get('size_hint_y', 1)
        self.size_hint_y = self._user_size_hint_y
        # Don't bind height to minimum_height
    
    self.bind(strict_label_mode=self._on_strict_label_mode_changed)

def _on_strict_label_mode_changed(self, instance, value):
    """Handle strict_label_mode property changes."""
    if value:
        # Disable auto-sizing
        self.unbind(minimum_height=self.setter('height'))
        self.size_hint_y = self._user_size_hint_y
    else:
        # Enable auto-sizing (if auto_size_height is True)
        if self.auto_size_height:
            self.size_hint_y = None
            self.bind(minimum_height=self.setter('height'))
    self._rebuild_widgets()
```

### 3. MarkdownLabel - Improved texture_size

```python
def _get_texture_size(self):
    """Compute aggregate texture_size from all descendant widgets.
    
    Returns the bounding box size that encompasses all content:
    - Width: maximum width of any descendant
    - Height: sum of all descendant heights
    
    Includes: Labels, AsyncImages, GridLayouts (tables), 
    BoxLayouts (code blocks, quotes), and Widgets (spacers, rules).
    """
    if not self.children:
        return [0, 0]
    
    max_width = 0
    total_height = 0
    
    def collect_sizes(widget):
        nonlocal max_width, total_height
        
        # For Labels, use texture_size
        if isinstance(widget, Label) and hasattr(widget, 'texture_size'):
            ts = widget.texture_size
            if ts[0] > max_width:
                max_width = ts[0]
            total_height += ts[1]
        # For AsyncImage, use actual size
        elif isinstance(widget, AsyncImage):
            if widget.width > max_width:
                max_width = widget.width
            total_height += widget.height
        # For GridLayout (tables), use minimum_size
        elif isinstance(widget, GridLayout):
            if hasattr(widget, 'minimum_width'):
                if widget.minimum_width > max_width:
                    max_width = widget.minimum_width
            if hasattr(widget, 'minimum_height'):
                total_height += widget.minimum_height
        # For BoxLayout containers (code blocks, quotes), recurse
        elif isinstance(widget, BoxLayout):
            for child in widget.children:
                collect_sizes(child)
        # For plain Widgets (spacers, rules), use height
        elif isinstance(widget, Widget):
            total_height += widget.height
        
        # Recurse into children for container widgets
        if hasattr(widget, 'children') and not isinstance(widget, (Label, AsyncImage)):
            for child in widget.children:
                collect_sizes(child)
    
    for child in self.children:
        collect_sizes(child)
    
    return [max_width, total_height]
```

### 4. MarkdownLabel - Coordinate Translation for refs/anchors

```python
def _get_refs(self):
    """Aggregate refs from all child Labels with coordinate translation.
    
    Returns a dictionary mapping ref names to bounding boxes in
    MarkdownLabel's local coordinate space.
    """
    refs = {}
    
    def collect_refs(widget, parent_offset_x=0, parent_offset_y=0):
        if isinstance(widget, Label) and hasattr(widget, 'refs'):
            # Calculate widget's position relative to MarkdownLabel
            offset_x = parent_offset_x + widget.x
            offset_y = parent_offset_y + widget.y
            
            for ref_name, ref_boxes in widget.refs.items():
                if ref_name not in refs:
                    refs[ref_name] = []
                # Translate each bounding box
                for box in ref_boxes:
                    # box is [x1, y1, x2, y2] relative to Label
                    translated_box = [
                        box[0] + offset_x,
                        box[1] + offset_y,
                        box[2] + offset_x,
                        box[3] + offset_y
                    ]
                    refs[ref_name].append(translated_box)
        
        if hasattr(widget, 'children'):
            for child in widget.children:
                collect_refs(child, 
                           parent_offset_x + widget.x,
                           parent_offset_y + widget.y)
    
    for child in self.children:
        collect_refs(child)
    
    return refs

def _get_anchors(self):
    """Aggregate anchors from all child Labels with coordinate translation.
    
    Returns a dictionary mapping anchor names to positions in
    MarkdownLabel's local coordinate space.
    """
    anchors = {}
    
    def collect_anchors(widget, parent_offset_x=0, parent_offset_y=0):
        if isinstance(widget, Label) and hasattr(widget, 'anchors'):
            offset_x = parent_offset_x + widget.x
            offset_y = parent_offset_y + widget.y
            
            for anchor_name, pos in widget.anchors.items():
                # pos is (x, y) relative to Label
                anchors[anchor_name] = (
                    pos[0] + offset_x,
                    pos[1] + offset_y
                )
        
        if hasattr(widget, 'children'):
            for child in widget.children:
                collect_anchors(child,
                              parent_offset_x + widget.x,
                              parent_offset_y + widget.y)
    
    for child in self.children:
        collect_anchors(child)
    
    return anchors
```

### 5. MarkdownLabel - Efficient Style Updates

```python
# Track which properties require full rebuild vs in-place update
_STYLE_ONLY_PROPERTIES = {
    'font_size', 'base_font_size', 'color', 'halign', 'valign',
    'line_height', 'disabled', 'disabled_color'
}

_STRUCTURE_PROPERTIES = {
    'text', 'font_name', 'code_font_name', 'text_size',
    'strict_label_mode', 'padding'
}

def _on_style_changed(self, instance, value):
    """Callback when a styling property changes.
    
    For style-only properties, update descendants in place.
    For structure properties, rebuild the widget tree.
    """
    prop_name = self._get_changed_property_name(instance, value)
    
    if prop_name in self._STYLE_ONLY_PROPERTIES:
        self._update_styles_in_place()
    else:
        self._rebuild_widgets()

def _update_styles_in_place(self):
    """Update style properties on existing child widgets without rebuild."""
    effective_color = self.disabled_color if self.disabled else self.color
    
    def update_widget(widget):
        if isinstance(widget, Label):
            widget.font_size = self.base_font_size
            widget.color = effective_color
            widget.halign = 'left' if self.halign == 'auto' else self.halign
            widget.valign = self.valign
            widget.line_height = self.line_height
        
        if hasattr(widget, 'children'):
            for child in widget.children:
                update_widget(child)
    
    for child in self.children:
        update_widget(child)
```

### 6. KivyRenderer - Strict Mode and ellipsis_options

```python
def __init__(self,
             # ... existing parameters ...
             strict_label_mode: bool = False,
             ellipsis_options: Optional[Dict] = None):
    # ... existing initialization ...
    self.strict_label_mode = strict_label_mode
    self.ellipsis_options = ellipsis_options or {}

def paragraph(self, token: Dict[str, Any], state: Any = None) -> Label:
    # ... existing code ...
    
    # Add ellipsis_options if set
    if self.ellipsis_options:
        label_kwargs['ellipsis_options'] = self.ellipsis_options
    
    label = Label(**label_kwargs)
    
    # Handle text_size based on mode
    if self.strict_label_mode:
        # Strict mode: only set text_size if explicitly provided
        if self.text_size[0] is not None or self.text_size[1] is not None:
            label.text_size = tuple(self.text_size)
        # Otherwise, don't bind width - let Label handle naturally
    else:
        # Markdown-friendly mode: existing behavior
        # ... existing text_size binding code ...
```

## Data Models

No new data models required. Changes extend existing property handling.

### Property Categories

| Category | Properties | Behavior |
|----------|-----------|----------|
| No-op | mipmap, outline_width, outline_color, text_language, base_direction | Accepted, stored, no effect |
| Forwarded | ellipsis_options, font_family, font_context, font_features, font_hinting, font_kerning | Passed to child Labels |
| Mode | strict_label_mode | Changes sizing/binding behavior |
| Computed | texture_size, refs, anchors | Aggregated from children |

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: No-op Property Acceptance and Storage

*For any* no-op property (mipmap, outline_width, outline_color, text_language, base_direction), when set to any valid value, the MarkdownLabel SHALL accept the value without raising an exception AND return the same value when accessed.

**Validates: Requirements 1.1, 1.2, 1.3**

### Property 2: Strict Label Mode Sizing Behavior

*For any* MarkdownLabel with `strict_label_mode=True`, the widget SHALL have `size_hint_y` preserved (not set to None) AND height SHALL NOT be bound to `minimum_height` AND internal Labels SHALL NOT have automatic text_size width bindings when `text_size=[None, None]`.

**Validates: Requirements 2.1, 2.2, 2.3, 2.4**

### Property 3: Comprehensive texture_size Calculation

*For any* MarkdownLabel containing mixed content (Labels, Images, Tables, Code blocks), the `texture_size` property SHALL return a tuple where width is the maximum width of any descendant widget AND height is the sum of all descendant heights.

**Validates: Requirements 3.1, 3.2, 3.3**

### Property 4: Shortening Property Forwarding

*For any* shortening-related property (shorten, shorten_from, split_str, max_lines, ellipsis_options), when set on MarkdownLabel, all child Labels (paragraphs, headings, list items, table cells, quote text) SHALL have the same property value.

**Validates: Requirements 4.1, 4.2, 4.3, 4.4, 4.5**

### Property 5: Coordinate Translation for refs and anchors

*For any* MarkdownLabel containing links (refs) or anchors, the `refs` and `anchors` properties SHALL return coordinates translated to MarkdownLabel's local coordinate space (not child Label's coordinate space).

**Validates: Requirements 5.1, 5.2, 5.3**

### Property 6: Font Advanced Property Forwarding

*For any* font advanced property (font_family, font_context, font_features, font_hinting, font_kerning), when set on MarkdownLabel, all applicable child Labels SHALL have the same property value (font_family excluded from code blocks).

**Validates: Requirements 6.1, 6.2, 6.3, 6.4, 6.5**

### Property 7: Efficient Style Updates

*For any* style-only property change (font_size, color, halign, valign, line_height), the MarkdownLabel SHALL update descendant properties in place AND the widget tree structure (widget identities) SHALL remain unchanged.

**Validates: Requirements 7.1, 7.2, 7.3**

## Error Handling

### Invalid Property Values

- **No-op properties**: Kivy's property system handles validation. Invalid values raise appropriate exceptions.
- **strict_label_mode**: BooleanProperty only accepts boolean values.
- **ellipsis_options**: DictProperty accepts any dictionary.

### Edge Cases

1. **Empty MarkdownLabel**: texture_size returns [0, 0], refs/anchors return empty dicts.
2. **No links**: refs returns empty dict, anchors returns empty dict.
3. **Mode switching**: Changing strict_label_mode triggers rebuild with new behavior.
4. **Nested content**: Coordinate translation handles arbitrary nesting depth.

## Testing Strategy

### Property-Based Testing

The project uses **Hypothesis** for property-based testing. Each correctness property will be implemented as a property-based test.

**Test Configuration:**
- Minimum 100 iterations per property test
- Tests tagged with format: `**Feature: label-compatibility-phase2, Property {N}: {description}**`

### Unit Tests

Unit tests will cover:
- Default property values for new no-op properties
- Mode switching behavior
- Edge cases (empty content, no links)
- Integration with existing Phase 1 functionality

### Test File Location

Tests will be added to `kivy_garden/markdownlabel/tests/test_markdown_label.py` following existing patterns.

### Test Annotations

Each property-based test MUST include:
```python
# **Feature: label-compatibility-phase2, Property N: Property Name**
# **Validates: Requirements X.Y**
```
