# Design Document: Rebuild Test Refactoring

## Overview

This design describes the refactoring of `test_rebuild_scheduling.py` to reduce coupling to internal implementation details. The refactoring transforms tests from verifying internal mechanisms (like `_pending_rebuild` flags and `_schedule_rebuild()` calls) to verifying observable outcomes (widget identity changes via `collect_widget_ids()`).

The key insight is that the rebuild contract guarantees two observable behaviors:
1. **Deferral**: Property changes don't immediately recreate widgets
2. **Batching**: Multiple changes result in a single rebuild when `force_rebuild()` is called

Both can be verified by comparing widget identities before and after operations, without accessing internal state.

## Architecture

### Current Test Structure (Before Refactoring)

```
test_rebuild_scheduling.py
├── TestBatchedRebuilds
│   ├── test_multiple_text_changes_batch_to_single_rebuild  [REWRITE - patches _rebuild_widgets]
│   ├── test_mixed_property_changes_batch_rebuilds          [REWRITE - patches _rebuild_widgets]
│   └── test_pending_rebuild_flag_prevents_duplicate_scheduling [REMOVE - tests internal flag]
│
└── TestDeferredRebuildScheduling
    ├── test_text_change_schedules_deferred_rebuild         [REWRITE - checks _pending_rebuild]
    ├── test_font_name_change_schedules_deferred_rebuild    [REWRITE - manipulates _pending_rebuild]
    ├── test_rebuild_trigger_is_clock_trigger               [KEEP - architectural documentation]
    ├── test_schedule_rebuild_sets_pending_flag             [REMOVE - tests internal method]
    ├── test_do_rebuild_clears_pending_flag                 [REMOVE - tests internal method]
    ├── test_do_rebuild_skips_when_not_pending              [REMOVE - tests internal optimization]
    └── test_multiple_changes_all_deferred                  [REWRITE - patches + checks flag]
```

### Target Test Structure (After Refactoring)

```
test_rebuild_scheduling.py
├── TestBatchedRebuilds
│   ├── test_multiple_text_changes_batch_to_single_rebuild  [Uses collect_widget_ids]
│   └── test_mixed_property_changes_batch_rebuilds          [Uses collect_widget_ids]
│
└── TestDeferredRebuildScheduling
    ├── test_text_change_schedules_deferred_rebuild         [Checks children unchanged]
    ├── test_font_name_change_schedules_deferred_rebuild    [Checks children unchanged]
    ├── test_rebuild_trigger_is_clock_trigger               [Architectural documentation]
    └── test_multiple_changes_all_deferred                  [Uses collect_widget_ids]
```

## Components and Interfaces

### Test Helper Functions (from test_utils.py)

The refactored tests rely on existing public helper functions:

```python
def collect_widget_ids(widget, exclude_root=False):
    """Collect Python object IDs of all widgets in the tree.
    
    Args:
        widget: Root widget to collect IDs from
        exclude_root: If True, excludes the root widget's ID
        
    Returns:
        Set of widget object IDs for identity comparison
    """
```

### Test Pattern: Observable Deferral Verification

```python
def test_property_change_defers_rebuild(self):
    """Verify property change doesn't immediately rebuild."""
    label = MarkdownLabel(text="Initial")
    label.force_rebuild()  # Ensure stable initial state
    
    ids_before = collect_widget_ids(label, exclude_root=True)
    
    # Change property (should defer rebuild)
    label.text = "New text"
    
    # Verify: widgets unchanged immediately after property change
    ids_during = collect_widget_ids(label, exclude_root=True)
    assert ids_before == ids_during, "Rebuild should be deferred"
    
    # Verify: widgets changed after force_rebuild
    label.force_rebuild()
    ids_after = collect_widget_ids(label, exclude_root=True)
    assert ids_before != ids_after, "Rebuild should have occurred"
```

### Test Pattern: Observable Batching Verification

```python
def test_multiple_changes_batch_to_single_rebuild(self):
    """Verify multiple changes don't cause multiple rebuilds."""
    label = MarkdownLabel(text="Initial")
    label.force_rebuild()
    
    ids_before = collect_widget_ids(label, exclude_root=True)
    
    # Make multiple changes (all should be batched)
    label.text = "Change 1"
    label.text = "Change 2"
    label.text = "Change 3"
    
    # Verify: still unchanged (all deferred)
    ids_during = collect_widget_ids(label, exclude_root=True)
    assert ids_before == ids_during, "All changes should be deferred"
    
    # Verify: single rebuild produces final state
    label.force_rebuild()
    ids_after = collect_widget_ids(label, exclude_root=True)
    assert ids_before != ids_after, "Rebuild should have occurred"
```

## Data Models

No new data models are required. The refactoring uses existing:
- `MarkdownLabel` widget class
- `collect_widget_ids()` helper function
- Python `set` for widget ID comparison

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

Since this is a test refactoring spec (modifying test code, not production code), the correctness properties describe what the refactored tests must verify, not properties to test with PBT.

### Property 1: Deferral Observable via Widget Identity

*For any* MarkdownLabel and *for any* structure property change, the widget identities (excluding root) SHALL remain unchanged immediately after the property assignment and before `force_rebuild()` is called.

**Validates: Requirements 3.1, 3.2, 3.4**

### Property 2: Batching Observable via Single Identity Change

*For any* sequence of structure property changes on a MarkdownLabel, the widget identities SHALL change exactly once when `force_rebuild()` is called, regardless of how many property changes preceded it.

**Validates: Requirements 2.1, 2.2, 2.4**

### Property 3: No Internal State Access in Behavioral Tests

*For any* test verifying deferral or batching behavior, the test SHALL NOT access attributes prefixed with `_` (except `_rebuild_trigger` in the architectural documentation test).

**Validates: Requirements 1.1, 1.2, 1.3, 2.3, 3.3**

## Error Handling

Not applicable - this is a test refactoring spec. Error handling in tests follows standard pytest patterns (assertions, clear failure messages).

## Testing Strategy

### Verification Approach

Since this spec modifies test code, verification is through:

1. **Code Review**: Verify refactored tests don't access internal state (except architectural test)
2. **Test Execution**: Run refactored tests to ensure they pass
3. **Coverage Check**: Verify the rebuild contract behaviors are still tested

### Tests to Remove (4 tests)

| Test | Reason for Removal |
|------|-------------------|
| `test_pending_rebuild_flag_prevents_duplicate_scheduling` | Only tests internal flag, behavior covered by batching tests |
| `test_schedule_rebuild_sets_pending_flag` | Tests internal method directly |
| `test_do_rebuild_clears_pending_flag` | Tests internal method directly |
| `test_do_rebuild_skips_when_not_pending` | Tests internal optimization, not observable behavior |

### Tests to Rewrite (4 tests)

| Test | Current Approach | New Approach |
|------|------------------|--------------|
| `test_multiple_text_changes_batch_to_single_rebuild` | Patches `_rebuild_widgets`, counts calls | Use `collect_widget_ids()`, verify unchanged then changed |
| `test_mixed_property_changes_batch_rebuilds` | Patches `_rebuild_widgets`, counts calls | Use `collect_widget_ids()`, verify unchanged then changed |
| `test_text_change_schedules_deferred_rebuild` | Checks `_pending_rebuild` flag | Verify children unchanged after property set |
| `test_multiple_changes_all_deferred` | Patches + checks `_pending_rebuild` | Use `collect_widget_ids()`, verify unchanged then changed |

### Tests to Keep (1 test)

| Test | Reason to Keep |
|------|----------------|
| `test_rebuild_trigger_is_clock_trigger` | Documents architectural decision; add explanatory docstring |

### Test to Modify (1 test)

| Test | Modification |
|------|--------------|
| `test_font_name_change_schedules_deferred_rebuild` | Remove `_pending_rebuild = False` manipulation, use widget identity check instead |

### Validation Commands

```bash
# Run refactored tests
pytest kivy_garden/markdownlabel/tests/test_rebuild_scheduling.py -v

# Verify no regressions in rebuild semantics tests
pytest kivy_garden/markdownlabel/tests/test_rebuild_semantics.py -v

# Check for internal state access (manual grep)
grep -n "_pending_rebuild\|_schedule_rebuild\|_do_rebuild\|_rebuild_widgets" \
    kivy_garden/markdownlabel/tests/test_rebuild_scheduling.py
```

### Expected Outcome

After refactoring:
- **10 tests → 6 tests** (4 removed, 4 rewritten, 1 kept, 1 modified)
- All remaining tests verify observable behavior
- Only `test_rebuild_trigger_is_clock_trigger` accesses internal state (with documented justification)
- Full coverage of rebuild contract guarantees maintained
