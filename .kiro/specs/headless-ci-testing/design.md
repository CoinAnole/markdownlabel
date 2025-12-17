# Design Document: Headless CI Testing

## Overview

This design document describes the implementation of deterministic, headless-safe tests for MarkdownLabel's texture mode hit-testing, coordinate translation, widget identity preservation, and untested renderer branches. The goal is to make the test suite reliable in CI environments without display capabilities while strengthening assertions around the widget's performance contracts.

## Architecture

The implementation follows a test-focused architecture with these key components:

1. **Pytest Marker Configuration**: A `needs_window` marker in pytest.ini to separate window-dependent tests
2. **FakeTouch Utility**: A lightweight touch simulation class for headless hit-testing
3. **Deterministic Test Fixtures**: Tests that inject known values rather than relying on Kivy rendering
4. **Widget Identity Tracking**: Helper methods to capture and compare widget object IDs

```
pytest.ini
├── markers: needs_window
└── addopts: -m "not needs_window"

tests/
├── test_texture_render_mode.py  (enhanced with deterministic hit-testing)
├── test_shortening_and_coordinate.py  (enhanced with deterministic translation tests)
├── test_kivy_renderer.py  (enhanced with truncation placeholder test)
├── test_performance.py  (enhanced with identity preservation tests)
└── test_rebuild_semantics.py  (new: focused identity change tests)
```

## Components and Interfaces

### FakeTouch Class

A minimal touch simulation class for headless testing:

```python
class FakeTouch:
    """Minimal touch simulation for headless testing.
    
    Provides the essential attributes needed by on_touch_down
    without requiring a Kivy window.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pos = (x, y)
```

### Widget Identity Helpers

Helper methods for tracking widget identities:

```python
def collect_widget_ids(widget, exclude_root=False):
    """Collect Python object ids of all widgets in the tree.
    
    Args:
        widget: Root widget to collect from
        exclude_root: If True, exclude the root widget's id
    
    Returns:
        Set of widget object ids
    """
    ids = set() if exclude_root else {id(widget)}
    if hasattr(widget, 'children'):
        for child in widget.children:
            ids.update(collect_widget_ids(child, exclude_root=False))
    return ids
```

### Test Categories

1. **Headless-Safe Tests** (default): Run without `needs_window` marker
   - Deterministic hit-testing with injected `_aggregated_refs`
   - Coordinate translation with injected `refs`/`anchors`
   - Widget identity preservation/change tests
   - Renderer branch coverage tests

2. **Window-Dependent Tests**: Marked with `@pytest.mark.needs_window`
   - Tests that require Kivy to populate `Label.refs`
   - Tests that require actual texture rendering

## Data Models

### Aggregated Refs Structure

```python
# _aggregated_refs format: {ref_name: [(x, y, width, height), ...]}
_aggregated_refs = {
    'http://example.com': [(10, 10, 50, 20)],
    'http://other.com': [(100, 50, 60, 25), (200, 100, 40, 15)]
}
```

### Coordinate Translation Math

For refs translation from Label texture space to MarkdownLabel local space:

```python
# Given:
# - label.pos = (label_x, label_y)
# - label.texture_size = (tex_w, tex_h)
# - parent_offset = cumulative offset from parent containers
# - ref_box = [x1, y1, x2, y2] in texture space

base_x = parent_offset_x + (label.center_x - tex_w / 2.0)
base_y = parent_offset_y + (label.center_y + tex_h / 2.0)

translated_box = [
    base_x + x1,
    base_y - y1,  # Y is inverted
    base_x + x2,
    base_y - y2,
]
```

For anchors translation:

```python
# Given anchor position (ax, ay) in texture space
translated_anchor = (
    base_x + ax,
    base_y - ay,  # Y is inverted
)
```



## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Touch Inside Ref Zone Dispatches Event

*For any* MarkdownLabel with `render_mode='texture'` and `_aggregated_refs` containing at least one zone, and *for any* touch point (x, y) that falls inside a ref zone, calling `on_touch_down` with that touch SHALL dispatch `on_ref_press` with the correct ref name AND return True.

**Validates: Requirements 2.1, 2.2**

### Property 2: Touch Outside Ref Zones Does Not Dispatch

*For any* MarkdownLabel with `render_mode='texture'` and `_aggregated_refs` containing zones, and *for any* touch point (x, y) that falls outside all ref zones, calling `on_touch_down` with that touch SHALL NOT dispatch `on_ref_press` AND SHALL return False (the default super behavior).

**Validates: Requirements 2.3, 2.4**

### Property 3: Refs Coordinate Translation Math

*For any* MarkdownLabel containing a child Label with known `refs`, `pos`, `size`, and `texture_size`, the aggregated `refs` property SHALL return bounding boxes translated according to the formula:
- `base_x = parent_offset_x + (label.center_x - tex_w / 2.0)`
- `base_y = parent_offset_y + (label.center_y + tex_h / 2.0)`
- `translated_box = [base_x + x1, base_y - y1, base_x + x2, base_y - y2]`

**Validates: Requirements 3.1, 3.3, 3.4**

### Property 4: Anchors Coordinate Translation Math

*For any* MarkdownLabel containing a child Label with known `anchors`, `pos`, `size`, and `texture_size`, the aggregated `anchors` property SHALL return positions translated according to the formula:
- `base_x = parent_offset_x + (label.center_x - tex_w / 2.0)`
- `base_y = parent_offset_y + (label.center_y + tex_h / 2.0)`
- `translated_anchor = (base_x + ax, base_y - ay)`

**Validates: Requirements 3.2, 3.3, 3.4**

### Property 5: Style Property Changes Preserve Widget Identities

*For any* MarkdownLabel with non-empty content, and *for any* style-only property (base_font_size, color, halign, valign, disabled, disabled_color, base_direction, line_height), changing that property SHALL preserve all widget object IDs in the subtree (the set of IDs before equals the set of IDs after).

**Validates: Requirements 4.1**

### Property 6: Style Property Values Propagate to Descendants

*For any* MarkdownLabel with non-empty content, and *for any* style-only property value, all descendant Label widgets SHALL have that property value after the change.

**Validates: Requirements 4.4**

### Property 7: Structure Property Changes Rebuild Widget Tree

*For any* MarkdownLabel with non-empty content, and *for any* structure property (text, font_name, text_size, link_style, strict_label_mode, render_mode), changing that property and calling `force_rebuild()` SHALL result in different widget object IDs for children (excluding the root MarkdownLabel).

**Validates: Requirements 5.1**

### Property 8: Root Widget ID Preserved Across Property Changes

*For any* MarkdownLabel, and *for any* property change (style or structure), the root MarkdownLabel's object ID SHALL remain unchanged.

**Validates: Requirements 5.4**

## Error Handling

### Texture Rendering Failure

When `_render_as_texture()` returns None (texture rendering fails), the system falls back to widgets-mode rendering. This ensures content is always displayed even when texture rendering is unavailable.

### Deep Nesting Protection

When content nesting exceeds `_max_nesting_depth` (default: 10), the KivyRenderer returns a truncation placeholder Label with text containing "content truncated" to prevent infinite recursion and stack overflow.

### Invalid Touch Coordinates

Touch coordinates outside the widget bounds are handled by the default `collide_point` check, which returns False and skips hit-testing.

## Testing Strategy

### Dual Testing Approach

This feature uses both unit tests and property-based tests:

- **Unit tests**: Verify specific examples (texture fallback, truncation placeholder, marker configuration)
- **Property tests**: Verify universal properties across generated inputs (hit-testing, coordinate translation, widget identity)

### Property-Based Testing Configuration

- **Library**: Hypothesis (already used in the project)
- **Minimum iterations**: 100 per property test
- **Tag format**: `**Feature: headless-ci-testing, Property N: {property_text}**`

### Test Organization

| Test File | Test Type | Properties/Examples |
|-----------|-----------|---------------------|
| `test_texture_render_mode.py` | Property + Unit | Properties 1, 2; Texture fallback example |
| `test_shortening_and_coordinate.py` | Property | Properties 3, 4 |
| `test_rebuild_semantics.py` (new) | Property | Properties 5, 6, 7, 8 |
| `test_kivy_renderer.py` | Unit | Deep nesting truncation example |
| `pytest.ini` | Config | Marker configuration |

### Headless vs Window-Dependent Tests

Tests are categorized by their runtime requirements:

**Headless-Safe (default)**:
- All property tests using injected values
- Texture fallback test (monkeypatched)
- Truncation placeholder test
- Widget identity tests

**Window-Dependent (`@pytest.mark.needs_window`)**:
- Tests that require Kivy to populate `Label.refs` from actual text rendering
- Tests that require actual texture creation

### FakeTouch Implementation

```python
class FakeTouch:
    """Minimal touch simulation for headless testing."""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pos = (x, y)
```

### Test Helpers

```python
def collect_widget_ids(widget, exclude_root=False):
    """Collect Python object ids of all widgets in the tree."""
    ids = set() if exclude_root else {id(widget)}
    if hasattr(widget, 'children'):
        for child in widget.children:
            ids.update(collect_widget_ids(child, exclude_root=False))
    return ids

def find_labels_recursive(widget):
    """Find all Label widgets recursively."""
    labels = []
    if isinstance(widget, Label):
        labels.append(widget)
    if hasattr(widget, 'children'):
        for child in widget.children:
            labels.extend(find_labels_recursive(child))
    return labels
```

