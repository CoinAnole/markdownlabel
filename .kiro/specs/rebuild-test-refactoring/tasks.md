# Implementation Plan: Rebuild Test Refactoring

## Overview

This plan refactors `test_rebuild_scheduling.py` to test observable outcomes rather than internal implementation details. The refactoring removes 4 tests, rewrites 4 tests, and modifies 1 test while preserving 1 architectural documentation test.

## Tasks

- [x] 1. Remove tests that only verify internal mechanisms
  - [x] 1.1 Remove `test_pending_rebuild_flag_prevents_duplicate_scheduling` from `TestBatchedRebuilds`
    - This test only verifies the `_pending_rebuild` flag behavior
    - The batching behavior it intends to test is covered by other tests
    - _Requirements: 1.1, 1.3, 1.4_
  - [x] 1.2 Remove `test_schedule_rebuild_sets_pending_flag` from `TestDeferredRebuildScheduling`
    - This test directly calls `_schedule_rebuild()` which is an internal method
    - _Requirements: 1.1, 1.4_
  - [x] 1.3 Remove `test_do_rebuild_clears_pending_flag` from `TestDeferredRebuildScheduling`
    - This test directly calls `_do_rebuild()` which is an internal method
    - _Requirements: 1.2, 1.4_
  - [x] 1.4 Remove `test_do_rebuild_skips_when_not_pending` from `TestDeferredRebuildScheduling`
    - This test verifies an internal optimization, not observable behavior
    - _Requirements: 1.2, 1.3, 1.4_

- [ ] 2. Rewrite batching tests to use observable outcomes
  - [ ] 2.1 Rewrite `test_multiple_text_changes_batch_to_single_rebuild`
    - Replace `_rebuild_widgets` patching with `collect_widget_ids()` comparison
    - Verify widget IDs unchanged after multiple text changes
    - Verify widget IDs changed after `force_rebuild()`
    - _Requirements: 2.1, 2.3, 2.4_
  - [ ] 2.2 Rewrite `test_mixed_property_changes_batch_rebuilds`
    - Replace `_rebuild_widgets` patching with `collect_widget_ids()` comparison
    - Verify widget IDs unchanged after mixed property changes
    - Verify widget IDs changed after `force_rebuild()`
    - _Requirements: 2.2, 2.3, 2.4_

- [ ] 3. Rewrite deferral tests to use observable outcomes
  - [ ] 3.1 Rewrite `test_text_change_schedules_deferred_rebuild`
    - Replace `_pending_rebuild` check with widget identity verification
    - Verify children unchanged immediately after `text` property change
    - _Requirements: 3.1, 3.3, 3.4_
  - [ ] 3.2 Modify `test_font_name_change_schedules_deferred_rebuild`
    - Remove `_pending_rebuild = False` manipulation
    - Use widget identity check to verify deferral
    - _Requirements: 3.1, 3.3, 3.4_
  - [ ] 3.3 Rewrite `test_multiple_changes_all_deferred`
    - Replace `_rebuild_widgets` patching and `_pending_rebuild` check
    - Use `collect_widget_ids()` to verify all changes are deferred
    - _Requirements: 3.2, 3.3, 3.4_

- [ ] 4. Update architectural documentation test
  - [ ] 4.1 Add explanatory docstring to `test_rebuild_trigger_is_clock_trigger`
    - Explain why this test intentionally accesses internal state
    - Document that this test serves as architectural documentation
    - Note that test failure indicates significant architectural change
    - _Requirements: 4.1, 4.2_

- [ ] 5. Checkpoint - Verify refactoring completeness
  - Run all tests in `test_rebuild_scheduling.py` to ensure they pass
  - Verify no internal state access except in architectural test
  - Ensure all tests pass, ask the user if questions arise
  - _Requirements: 5.1, 5.2, 5.3, 5.4_

- [ ] 6. Final validation
  - [ ] 6.1 Run full rebuild-related test suite
    - Execute `pytest kivy_garden/markdownlabel/tests/test_rebuild_scheduling.py -v`
    - Execute `pytest kivy_garden/markdownlabel/tests/test_rebuild_semantics.py -v`
    - Verify no regressions
    - _Requirements: 5.1, 5.2, 5.3, 5.4_
  - [ ] 6.2 Verify internal state access is eliminated
    - Grep for `_pending_rebuild`, `_schedule_rebuild`, `_do_rebuild`, `_rebuild_widgets`
    - Only `_rebuild_trigger` should appear (in architectural test)
    - _Requirements: 1.1, 1.2, 1.3, 2.3, 3.3_

## Notes

- The `collect_widget_ids()` helper is already available in `test_utils.py`
- Tests use `force_rebuild()` which is a public API method
- Property-based tests retain their `@given` decorators and `@settings` configurations
- The architectural test (`test_rebuild_trigger_is_clock_trigger`) is the only test allowed to access internal state
