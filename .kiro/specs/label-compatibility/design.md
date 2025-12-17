# Design Document: Label Compatibility Improvements

## Overview

This design addresses behavioral gaps between `MarkdownLabel` and Kivy's native `Label` widget. The goal is to make `MarkdownLabel` a true drop-in replacement for `Label` in scenarios requiring rich text formatting, while preserving all Markdown rendering capabilities.

The key improvements are:
1. Content clipping when `text_size` height is constrained
2. Immediate `base_font_size` updates with proper heading scale preservation
3. Deferred/batched property updates for performance
4. Clear padding property semantics with `label_padding` alias
5. RTL-aware `halign='auto'` behavior
6. Optional single-texture render mode for maximum compatibility

## Architecture

### Current Architecture

```
MarkdownLabel (BoxLayout)
├── Property bindings → _rebuild_widgets() (immediate)
├── KivyRenderer → Widget tree (Labels, BoxLayouts, GridLayouts, etc.)
└── Child Labels with individual texture_size bindings
```

### Proposed Architecture

```
MarkdownLabel (BoxLayout)
├── Property bindings → _schedule_rebuild() (deferred via Clock.create_trigger)
├── _ClippingContainer (StencilView, conditional)
│   └── Content widgets
├── KivyRenderer → Widget tree OR single texture
├── Font scale metadata on child Labels
└── Render mode selection (widgets/texture/auto)
```

## Components and Interfaces

### 1. ClippingContainer (Internal)

A conditional wrapper that clips content when height constraints are active.

```python
class _ClippingContainer(StencilView):
    """Internal container that clips content to bounds.
    
    Used when:
    - text_size[1] is not None, OR
    - strict_label_mode is True
    """
    pass
```

### 2. Enhanced MarkdownLabel Properties

```python
class MarkdownLabel(BoxLayout):
    # New properties
    render_mode = OptionProperty('widgets', options=['widgets', 'texture', 'auto'])
    """Rendering mode: 'widgets' (default), 'texture', or 'auto'."""
    
    label_padding = AliasProperty(
        _get_label_padding, _set_label_padding, bind=['text_padding']
    )
    """Alias for text_padding for Label API compatibility."""
    
    # Internal state
    _rebuild_trigger = ObjectProperty(None)
    """Clock trigger for deferred rebuilds."""
    
    _pending_rebuild = BooleanProperty(False)
    """Flag indicating a rebuild is pending."""
```

### 3. Font Scale Metadata

Store scale factors on child Labels for in-place font size updates:

```python
# In KivyRenderer, when creating Labels:
label._font_scale = 1.0  # Body text
label._font_scale = 2.5  # h1
label._font_scale = 2.0  # h2
# etc.
```

### 4. Deferred Rebuild System

```python
def __init__(self, **kwargs):
    # Create deferred rebuild trigger
    self._rebuild_trigger = Clock.create_trigger(
        self._do_rebuild, timeout=-1
    )
    
def _schedule_rebuild(self):
    """Schedule a rebuild for the next frame."""
    self._pending_rebuild = True
    self._rebuild_trigger()

def _do_rebuild(self, dt=None):
    """Execute the deferred rebuild."""
    if self._pending_rebuild:
        self._pending_rebuild = False
        self._rebuild_widgets()

def force_rebuild(self):
    """Force an immediate synchronous rebuild."""
    self._rebuild_trigger.cancel()
    self._pending_rebuild = False
    self._rebuild_widgets()
```

### 5. RTL-Aware Auto Alignment

```python
def _get_effective_halign(self):
    """Compute effective halign based on auto and base_direction."""
    if self.halign != 'auto':
        return self.halign
    
    if self.base_direction in ('rtl', 'weak_rtl'):
        return 'right'
    return 'left'
```

### 6. Texture Render Mode

```python
def _render_as_texture(self):
    """Render content to a single texture with hit-testing support."""
    # 1. Render widget tree off-screen
    # 2. Export to texture via export_as_image()
    # 3. Display via Image widget
    # 4. Store aggregated refs for hit-testing
    
def on_touch_down(self, touch):
    """Handle touch events for texture mode link clicking."""
    if self.render_mode == 'texture' and self.collide_point(*touch.pos):
        # Hit-test against aggregated refs
        for ref_name, zones in self._aggregated_refs.items():
            for zone in zones:
                if self._point_in_zone(touch.pos, zone):
                    self.dispatch('on_ref_press', ref_name)
                    return True
    return super().on_touch_down(touch)
```

## Data Models

### Font Scale Metadata

```python
# Stored on each Label widget as an attribute
label._font_scale: float  # Multiplier relative to base_font_size
label._is_code: bool      # True for code blocks (uses code_font_name)
```

### Aggregated Refs for Texture Mode

```python
# Stored on MarkdownLabel when render_mode='texture'
self._aggregated_refs: Dict[str, List[Tuple[float, float, float, float]]]
# Maps ref names to list of (x, y, width, height) zones in widget coordinates
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Content clipping when height-constrained

*For any* Markdown content and any positive height value h, when `text_size[1]` is set to h OR `strict_label_mode` is True with a fixed height, the MarkdownLabel SHALL contain a StencilView (or equivalent) that prevents content from rendering outside the widget bounds.

**Validates: Requirements 1.1, 1.2, 1.3**

### Property 2: No clipping when unconstrained

*For any* Markdown content, when `text_size[1]` is None AND `strict_label_mode` is False, the MarkdownLabel SHALL NOT contain a clipping container, and content SHALL expand to its natural height.

**Validates: Requirements 1.4**

### Property 3: Font size immediate update

*For any* MarkdownLabel with rendered content and any new base_font_size value, after setting base_font_size, all child Label widgets SHALL have their font_size property updated to reflect the new base_font_size (accounting for scale factors).

**Validates: Requirements 2.1**

### Property 4: Heading scale preservation

*For any* MarkdownLabel with headings (h1-h6) and any base_font_size value, each heading Label's font_size SHALL equal `base_font_size * HEADING_SIZES[level]` where HEADING_SIZES is {1: 2.5, 2: 2.0, 3: 1.75, 4: 1.5, 5: 1.25, 6: 1.0}.

**Validates: Requirements 2.2, 2.4**

### Property 5: No rebuild on font size change

*For any* MarkdownLabel with rendered content, when base_font_size is modified, the child widget object identities SHALL remain unchanged (same Python object ids), indicating no rebuild occurred.

**Validates: Requirements 2.3**

### Property 6: Batched rebuilds

*For any* sequence of N property changes (where N > 1) made within the same frame, the MarkdownLabel SHALL execute at most one rebuild operation.

**Validates: Requirements 3.1, 3.3**

### Property 7: Deferred rebuild scheduling

*For any* property change that triggers a rebuild, the rebuild SHALL NOT execute synchronously; instead, it SHALL be scheduled via Clock.create_trigger for the next frame.

**Validates: Requirements 3.2**

### Property 8: text_padding applies to child Labels

*For any* MarkdownLabel with text_padding set to value P, all child Label widgets SHALL have their padding property set to P.

**Validates: Requirements 4.1**

### Property 9: padding applies to container

*For any* MarkdownLabel with padding set to value P, the BoxLayout container (self) SHALL have padding P, and child Label widgets SHALL NOT have their padding affected by this property.

**Validates: Requirements 4.2**

### Property 10: label_padding alias synchronization

*For any* value V assigned to label_padding, text_padding SHALL equal V, and vice versa.

**Validates: Requirements 4.4**

### Property 11: Auto alignment respects direction

*For any* MarkdownLabel with halign='auto', when base_direction is 'rtl' or 'weak_rtl', all child Labels SHALL have halign='right'; when base_direction is 'ltr', 'weak_ltr', or None, all child Labels SHALL have halign='left'.

**Validates: Requirements 5.1, 5.2**

### Property 12: Direction change updates alignment

*For any* MarkdownLabel with halign='auto' and rendered content, when base_direction changes, all child Label widgets SHALL have their halign updated to reflect the new effective alignment.

**Validates: Requirements 5.3**

### Property 13: Explicit alignment overrides auto

*For any* MarkdownLabel with halign explicitly set to 'left', 'center', 'right', or 'justify', all child Labels SHALL use that alignment regardless of base_direction value.

**Validates: Requirements 5.4**

### Property 14: Texture render mode structure

*For any* MarkdownLabel with render_mode='texture' and non-empty text, the widget tree SHALL contain an Image widget displaying the rendered content as a texture.

**Validates: Requirements 6.1**

### Property 15: Texture mode link handling

*For any* MarkdownLabel with render_mode='texture' containing links, when a touch event occurs within a link's bounding zone, the on_ref_press event SHALL be dispatched with the correct ref value.

**Validates: Requirements 6.2**

### Property 16: Auto render mode selection

*For any* MarkdownLabel with render_mode='auto', the effective render mode SHALL be determined by content complexity and layout constraints (widgets for simple content, texture for complex layouts or when strict_label_mode is True with height constraints).

**Validates: Requirements 6.4**

## Error Handling

### Invalid Property Values

- `render_mode` with invalid value: Kivy's OptionProperty handles this automatically
- `text_size` with negative values: Treat as None (no constraint)
- `base_font_size` <= 0: Clamp to minimum of 1

### Clipping Edge Cases

- Empty content with clipping: No StencilView needed, return empty widget
- Content exactly fits bounds: No visual clipping, but StencilView still present for consistency

### Texture Mode Failures

- `export_as_image()` fails: Fall back to widget mode with warning
- Touch outside widget bounds: Ignore (standard Kivy behavior)

## Testing Strategy

### Testing Framework and Organization

Following the test-improvements design, use a combination of:
- **Hypothesis** for property-based testing (truly random inputs)
- **pytest.mark.parametrize** for fixed-list testing (specific edge cases)
- **Focused test files** for different aspects of functionality

### Test File Organization

Tests are organized into focused files following the test-improvements structure:
- `test_clipping_behavior.py` - Content clipping and StencilView tests
- `test_rebuild_scheduling.py` - Deferred rebuild and batching tests  
- `test_font_properties.py` - Font size and heading scale tests
- `test_padding_properties.py` - Padding property tests
- `test_rtl_alignment.py` - RTL-aware alignment tests
- `test_advanced_compatibility.py` - Texture render mode tests

### Test Configuration

- Centralized configuration in `conftest.py` (no duplicate environment setup)
- Property tests: 100 iterations for comprehensive coverage
- Parametrized tests: Specific edge cases with descriptive parameter names
- Performance tests: Marked with `@pytest.mark.slow`

### Test Annotation Format

Each property-based test MUST be annotated with:
```python
# **Feature: label-compatibility, Property {number}: {property_text}**
```

### Testing Approach Guidelines

**Use Property-Based Tests For:**
- Random Markdown content with varying structures
- Random font sizes and property combinations
- Random padding values and alignment combinations
- Truly variable inputs where edge cases emerge from randomness

**Use Parametrized Tests For:**
- Specific clipping scenarios (height-constrained vs unconstrained)
- Specific alignment combinations (halign + base_direction)
- Specific render modes ('widgets', 'texture', 'auto')
- Known edge cases and regression scenarios

### Unit Tests

Unit tests cover specific examples and edge cases:
- Empty text with clipping enabled
- Single character content  
- Very large content (marked as slow)
- Rapid property changes
- Mode switching scenarios
- Specific padding configurations

### Test Generators (for Property-Based Tests)

```python
from hypothesis import strategies as st

# Markdown content with structure
markdown_content = st.text(
    alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')),
    min_size=0, max_size=500  # Reduced for faster tests
).map(lambda s: f"# Heading\n\n{s}\n\n**bold** and *italic*")

# Font size generator
font_sizes = st.floats(min_value=1.0, max_value=100.0, allow_nan=False, allow_infinity=False)

# Padding generator  
padding_values = st.lists(
    st.floats(min_value=0.0, max_value=50.0, allow_nan=False, allow_infinity=False),
    min_size=4, max_size=4
)

# Direction generator (for parametrized tests)
DIRECTIONS = [None, 'ltr', 'rtl', 'weak_ltr', 'weak_rtl']
HALIGN_VALUES = ['auto', 'left', 'center', 'right', 'justify']
```
