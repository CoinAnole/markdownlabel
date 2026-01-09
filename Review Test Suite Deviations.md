# Review of DEVIATIONS.md

I've examined each deviation identified in the [DEVIATIONS.md](cci:7://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/DEVIATIONS.md:0:0-0:0) file against the [TESTING.md](cci:7://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/TESTING.md:0:0-0:0) guidelines and the actual test code. Here's my assessment:

## Summary Table

| File | Line(s) | Deviation | Legitimate? | Worth Fixing? | Priority |
|------|---------|-----------|-------------|---------------|----------|
| test_kivy_renderer_blocks.py | 502-508 | Test naming doesn't match assertions | **Yes** | Yes | Low |
| test_kivy_renderer_tables.py | 140-155 | Private method `_render_table_cell` | **Partially** | Consider | Medium |
| test_kivy_renderer_tables.py | 211-225 | Private method `_render_table_cell` | **Partially** | Consider | Medium |
| test_kivy_renderer_tables.py | 254-297 | Test name doesn't match assertions | **Yes** | Yes | Low |
| test_rebuild_scheduling.py | 73 | Incorrect docstring (font_name as structure) | **Yes** | Yes | Medium |
| test_rebuild_scheduling.py | 85 | Incorrect comment (font_name as structure) | **Yes** | Yes | Medium |
| test_rebuild_scheduling.py | 182-211 | Private [_rebuild_trigger](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_rebuild_scheduling.py:180:4-209:9) attribute | **No** | No | N/A |
| test_serialization.py | 718 | Private `_serialize_token` method | **Partially** | Consider | Low |
| test_serialization.py | 754, 765 | Private [_serialize_list_item](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_serialization.py:743:4-753:64) method | **Partially** | Consider | Low |
| test_texture_render_mode.py | 513-517, 544-548 | Monkeypatching `_render_as_texture` | **Partially** | Consider | Low |

---

## Detailed Analysis

### 1. [test_kivy_renderer_blocks.py](cci:7://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_kivy_renderer_blocks.py:0:0-0:0) (Lines 502-508)

**Deviation:** Test naming that doesn't match assertions (claims stores alt text but doesn't verify content)

**Code Review:**
```python
def test_image_stores_alt_text(self, token):
    """Image widget stores alt text for fallback."""
    renderer = KivyRenderer()
    widget = renderer.image(token, None)
    assert hasattr(widget, 'alt_text'), "Image should have alt_text attribute"
```

**Verdict: LEGITIMATE** ✅

The test claims to verify that "Image widget stores alt text" but only asserts `hasattr(widget, 'alt_text')`. It doesn't verify:
- That [alt_text](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_kivy_renderer_blocks.py:497:4-506:82) contains the correct value from the token
- That the content matches what was provided

**Recommendation:** Add assertion to verify the actual content:
```python
expected_alt = token.get('children', [{}])[0].get('raw', '') if token.get('children') else ''
assert widget.alt_text == expected_alt
```

---

### 2. [test_kivy_renderer_tables.py](cci:7://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_kivy_renderer_tables.py:0:0-0:0) (Lines 140-155, 211-225)

**Deviation:** Testing private method `_render_table_cell` without documented exception

**Code Review:**
```python
def test_cell_alignment_applied(self, alignment):
    """Table cell alignment is applied to Label halign."""
    renderer = KivyRenderer()
    cell_token = {...}
    widget = renderer._render_table_cell(cell_token, None, is_head=False)  # Private method
```

**Verdict: PARTIALLY LEGITIMATE** ⚠️

Per [TESTING.md](cci:7://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/TESTING.md:0:0-0:0) lines 255-258, edge case classes **may** access private methods when:
1. Class name/docstring indicates coverage/edge cases
2. Behavior cannot be easily triggered through public API
3. Test documents why direct access is necessary

The class [TestTableAlignmentApplication](cci:2://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_kivy_renderer_tables.py:135:0-237:81) doesn't clearly indicate it's an edge case class, and the same behavior could be tested through the public [table()](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_serialization.py:316:4-330:78) method (as demonstrated in [test_table_preserves_column_alignments](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_kivy_renderer_tables.py:155:4-207:106)).

**Recommendation:** Either:
- Refactor to use public [table()](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_serialization.py:316:4-330:78) API, or
- Add a comment explaining why direct `_render_table_cell` access is necessary (e.g., isolation testing for specific alignment values)

---

### 3. [test_kivy_renderer_tables.py](cci:7://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_kivy_renderer_tables.py:0:0-0:0) (Lines 254-297)

**Deviation:** Test naming does not match assertions

**Code Review:**
```python
def test_table_internals_coverage(self, renderer):
    """Test table internal methods directly to ensure coverage.

    Verifies that table rendering properly handles table_head and
    table_body structures with various alignments.
    """
    # ...
    table_widget = renderer.table(token)
    assert table_widget is not None
    assert isinstance(table_widget, GridLayout)
```

**Verdict: LEGITIMATE** ✅

The docstring claims it "Verifies that table rendering properly handles table_head and table_body structures with various alignments" but the assertions only check:
- `table_widget is not None`
- `isinstance(table_widget, GridLayout)`

There's **no verification of alignments** as the docstring claims.

**Recommendation:** Either:
- Update assertions to verify alignments match expectations, or
- Update docstring to accurately describe what's being tested

---

### 4. [test_rebuild_scheduling.py](cci:7://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_rebuild_scheduling.py:0:0-0:0) (Lines 73, 85)

**Deviation:** Docstring/comment incorrectly classifies [font_name](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_rebuild_scheduling.py:150:4-178:74) as a "structure property"

**Code Review:**
```python
def test_mixed_property_changes_batch_rebuilds(self, text, font_name):
    """Mixed structure property changes batch into single rebuild.
    ...
    """
    # ...
    # Make multiple structure property changes (should be batched/deferred)
    label.text = text
    label.font_name = font_name  # font_name is STYLE-ONLY, not structure!
```

**Verdict: LEGITIMATE** ✅

Per [TESTING.md](cci:7://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/TESTING.md:0:0-0:0) lines 81-84 and `REBUILD_CONTRACT.md`, [font_name](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_rebuild_scheduling.py:150:4-178:74) is explicitly a **style-only property** that updates in place without triggering rebuilds. The docstring and comment incorrectly label this as a structure property change.

However, reviewing the test logic, it's actually testing that [text](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_serialization.py:79:4-118:21) (a structure property) triggers a rebuild. The [font_name](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_rebuild_scheduling.py:150:4-178:74) change is coincidental and doesn't affect the test's validity—but the documentation is misleading.

**Recommendation:** 
- Update docstring to clarify that it tests batching of a structure property ([text](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_serialization.py:79:4-118:21)) change
- Update comment to note that [font_name](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_rebuild_scheduling.py:150:4-178:74) is style-only and updates immediately (or remove it from the test entirely for clarity)

---

### 5. [test_rebuild_scheduling.py](cci:7://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_rebuild_scheduling.py:0:0-0:0) (Lines 182-211)

**Deviation:** Testing private [_rebuild_trigger](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_rebuild_scheduling.py:180:4-209:9) attribute without documented exception

**Code Review:**
```python
def test_rebuild_trigger_is_clock_trigger(self):
    """_rebuild_trigger is a Clock.create_trigger instance.

    **ARCHITECTURAL DOCUMENTATION TEST**

    This test intentionally accesses internal state (_rebuild_trigger) to document
    and verify a critical architectural decision: MarkdownLabel uses Kivy's Clock
    system for deferred rebuilds rather than synchronous rebuilds.
    ...
    """
```

**Verdict: NOT LEGITIMATE** ❌

The test **already includes a documented exception** explaining why it accesses [_rebuild_trigger](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_rebuild_scheduling.py:180:4-209:9). The docstring clearly states:
- It's an "ARCHITECTURAL DOCUMENTATION TEST"
- It "intentionally accesses internal state"
- Why this access is necessary (documenting Clock usage for deferral)

This follows the [TESTING.md](cci:7://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/TESTING.md:0:0-0:0) guidelines at lines 255-258, which allow private method access when the test "documents why direct access is necessary."

**Recommendation:** **No fix needed.** This deviation entry in [DEVIATIONS.md](cci:7://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/DEVIATIONS.md:0:0-0:0) is incorrect—the test is properly documented.

---

### 6. [test_serialization.py](cci:7://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_serialization.py:0:0-0:0) (Lines 718, 754, 765)

**Deviation:** Testing private methods `_serialize_token` and [_serialize_list_item](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_serialization.py:743:4-753:64) without documented exception

**Code Review:**
```python
def test_serialize_unknown_token(self):
    """Test that unknown token types return empty string."""
    serializer = MarkdownSerializer()
    token = {'type': 'unknown_thing', 'raw': 'content'}
    assert serializer._serialize_token(token) == ''  # Private method

def test_serialize_list_item_unknown_child(self):
    """Test list item serialization with unknown child type."""
    # ...
    assert serializer._serialize_list_item(item_token) == ''  # Private method
```

**Verdict: PARTIALLY LEGITIMATE** ⚠️

These tests are in [TestMarkdownSerializerEdgeCases](cci:2://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_serialization.py:707:0-780:54) class, which follows the edge case pattern. However, per [TESTING.md](cci:7://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/TESTING.md:0:0-0:0):
- The class name indicates edge cases ✅
- But tests don't document **why** direct access is necessary

The behavior (unknown token handling) could potentially be tested through the public API by creating markdown that produces an unknown token after parsing. However, this is likely impractical since mistune won't produce unknown token types.

**Recommendation:** Add brief inline comments explaining why direct access is necessary:
```python
# Edge case: Testing unknown token handling requires direct call since
# mistune parser never produces unknown token types
assert serializer._serialize_token(token) == ''
```

---

### 7. [test_texture_render_mode.py](cci:7://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_texture_render_mode.py:0:0-0:0) (Lines 513-517, 544-548)

**Deviation:** Monkeypatching private `_render_as_texture` without documented exception

**Code Review:**
```python
def test_texture_fallback_to_widgets_mode(self, monkeypatch):
    """When _render_as_texture returns None, fallback to widgets mode.

    This test verifies that when texture rendering fails (returns None),
    the MarkdownLabel falls back to widgets-mode rendering...
    """
    # Monkeypatch _render_as_texture to return None (simulate failure)
    monkeypatch.setattr(
        MarkdownLabel,
        '_render_as_texture',
        lambda self, content: None
    )
```

**Verdict: PARTIALLY LEGITIMATE** ⚠️

The docstring does explain the test's purpose, but it doesn't explicitly acknowledge the private method access exception. The class [TestTextureFallbackBranch](cci:2://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_texture_render_mode.py:498:0-567:56) tests fallback behavior that cannot easily be triggered through public API (it requires simulating texture rendering failure).

**Recommendation:** Add a brief comment acknowledging the exception:
```python
# Monkeypatch _render_as_texture to return None (simulate failure)
# Testing Exception: Fallback behavior requires simulating texture failure
# which cannot be triggered through public API
monkeypatch.setattr(...)
```

---

## Summary: What Should Be Fixed?

### High Priority (Incorrect Information)
1. **test_rebuild_scheduling.py lines 73, 85** — Incorrect classification of [font_name](cci:1://file:///home/coinanole/repos/markdownlabel/kivy_garden/markdownlabel/tests/test_rebuild_scheduling.py:150:4-178:74) as a structure property is misleading and could confuse future maintainers

### Medium Priority (Missing Documentation)
2. **test_kivy_renderer_tables.py lines 140-155, 211-225** — Add comments explaining why `_render_table_cell` is accessed directly
3. **test_serialization.py lines 718, 754, 765** — Add comments explaining why private methods are tested directly
4. **test_texture_render_mode.py lines 513-517, 544-548** — Add exception acknowledgment comments

### Low Priority (Test Quality)
5. **test_kivy_renderer_blocks.py lines 502-508** — Strengthen assertions to actually verify alt text content
6. **test_kivy_renderer_tables.py lines 254-297** — Fix docstring/assertions mismatch

### Should Be Removed from DEVIATIONS.md
7. **test_rebuild_scheduling.py lines 182-211** — This is NOT a deviation; the test already properly documents its exception