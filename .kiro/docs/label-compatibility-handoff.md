# Label Compatibility Improvements - Handoff Document

## Context

GPT 5.1 reviewed the MarkdownLabel project and identified several areas where the widget's Label-compatible API doesn't fully match Kivy's standard Label behavior. We've already addressed documentation clarity and added `texture_size`, `refs`, and `anchors` properties. Three issues remain.

## Remaining Issues

### Issue #2: `text_size` height is ignored (High Priority)

**Current behavior:** In `kivy_renderer.py`, the `text_size[1]` (height) value is always set to `None`, regardless of what the user specifies:

```python
# Current code in paragraph(), heading(), block_text(), etc.
if self.text_size[0] is not None:
    label.bind(width=lambda inst, val: setattr(inst, 'text_size', (self.text_size[0], None)))
else:
    label.bind(width=lambda inst, val: setattr(inst, 'text_size', (val, None)))
```

**Problem:** Users cannot constrain height or use `valign` for vertical positioning within a bounded area. In Kivy's Label, `text_size=(w, h)` enables clipping and vertical alignment behavior.

**Fix:** Respect `text_size[1]` when specified. Pass it through to child Labels so `valign` works correctly and text can be clipped/constrained vertically.

---

### Issue #3: `padding` not forwarded to child Labels (Medium Priority)

**Current behavior:** The `padding` property only affects the outer BoxLayout container, not the internal Labels:

```python
# In __init__.py
padding = VariableListProperty([0, 0, 0, 0])

def _on_padding_changed(self, instance, value):
    # BoxLayout handles padding directly, no rebuild needed
    pass
```

**Problem:** In Kivy's Label, `padding` affects the text inset within the label itself. In MarkdownLabel, text remains flush to the edge even when padding is set on the container.

**Fix options:**
1. Forward `padding` to all child Labels (may have side effects with nested layouts)
2. Add a separate `text_padding` property that gets forwarded to child Labels
3. Document the difference and recommend users wrap content if they need text inset

---

### Issue #5: Auto-sizing is always enabled (Medium Priority)

**Current behavior:** In `__init__.py`, `size_hint_y=None` is hardcoded and height is bound to `minimum_height`:

```python
def __init__(self, **kwargs):
    super(MarkdownLabel, self).__init__(**kwargs)
    self.orientation = 'vertical'
    self.size_hint_y = None
    self.bind(minimum_height=self.setter('height'))
```

**Problem:** This breaks layouts that expect the widget to participate in size hints. A standard Label defaults to `size_hint_y=1`, allowing it to expand/shrink with its parent. MarkdownLabel always sizes to its content, which can cause unexpected layout behavior.

**Fix:** Add an `auto_size_height` property (default `True` for backward compatibility) that controls whether:
- `size_hint_y` is set to `None` and height bound to `minimum_height` (current behavior)
- `size_hint_y` is left at its default/user-specified value (opt-out)

---

## Files to Modify

- `kivy_garden/markdownlabel/__init__.py` — Main widget class, properties
- `kivy_garden/markdownlabel/kivy_renderer.py` — Label creation, text_size handling
- `kivy_garden/markdownlabel/tests/test_markdown_label.py` — Add tests for new behavior

## Related Documentation

- Kivy Label docs: https://kivy.org/doc/stable/api-kivy.uix.label.html
- `text_size` behavior: https://kivy.org/doc/stable/api-kivy.uix.label.html#kivy.uix.label.Label.text_size
