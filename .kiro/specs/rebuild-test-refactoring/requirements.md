# Requirements Document

## Introduction

This specification defines the refactoring of `test_rebuild_scheduling.py` to reduce coupling to internal implementation details while maintaining test coverage of the documented rebuild contract. The goal is to make tests more resilient to internal refactoring while still verifying the observable behavior guarantees defined in `REBUILD_CONTRACT.md`.

## Glossary

- **MarkdownLabel**: The main widget class that renders Markdown as Kivy UI elements
- **Rebuild_Contract**: The documented public API behavior defining which property changes trigger widget tree rebuilds versus style-only updates
- **Observable_Outcome**: Behavior that can be verified through public API without accessing internal state
- **Internal_Mechanism**: Private methods, attributes, or implementation details (prefixed with `_`)
- **Widget_Identity**: The Python object ID of a widget, used to detect whether widgets were recreated
- **Deferred_Rebuild**: A rebuild that is scheduled for the next frame rather than executed synchronously
- **Batched_Rebuild**: Multiple property changes resulting in a single rebuild operation

## Requirements

### Requirement 1: Remove Tests That Only Verify Internal Mechanisms

**User Story:** As a maintainer, I want tests that verify observable behavior rather than internal implementation, so that I can refactor internals without breaking tests.

#### Acceptance Criteria

1. WHEN the test suite is reviewed THEN the Test_Suite SHALL NOT contain tests that directly call `_schedule_rebuild()` as the primary action under test
2. WHEN the test suite is reviewed THEN the Test_Suite SHALL NOT contain tests that directly call `_do_rebuild()` as the primary action under test
3. WHEN the test suite is reviewed THEN the Test_Suite SHALL NOT contain tests that only verify the `_pending_rebuild` flag state without testing observable outcomes
4. WHEN tests are removed THEN the Test_Suite SHALL maintain equivalent coverage of the documented rebuild contract behavior

### Requirement 2: Rewrite Batching Tests to Use Observable Outcomes

**User Story:** As a maintainer, I want batching tests to verify behavior through widget identity changes rather than internal method patching, so that tests remain valid if the batching mechanism is reimplemented.

#### Acceptance Criteria

1. WHEN testing that multiple text changes batch to a single rebuild THEN the Test SHALL verify widget identities are unchanged before `force_rebuild()` and changed after
2. WHEN testing that mixed property changes batch rebuilds THEN the Test SHALL verify widget identities using `collect_widget_ids()` rather than patching `_rebuild_widgets`
3. WHEN testing batching behavior THEN the Test SHALL use only public API methods (`force_rebuild()`, property setters) and public helper functions (`collect_widget_ids()`)
4. WHEN a batching test passes THEN the Test SHALL have verified that deferred changes do not immediately alter the widget tree

### Requirement 3: Rewrite Deferral Tests to Use Observable Outcomes

**User Story:** As a maintainer, I want deferral tests to verify that rebuilds don't happen synchronously by checking widget state rather than internal flags, so that tests verify the user-visible guarantee.

#### Acceptance Criteria

1. WHEN testing that text changes schedule deferred rebuilds THEN the Test SHALL verify children are unchanged immediately after property assignment
2. WHEN testing that multiple changes are all deferred THEN the Test SHALL verify widget identities remain stable until `force_rebuild()` is called
3. WHEN testing deferral behavior THEN the Test SHALL NOT directly read or write the `_pending_rebuild` attribute as the primary assertion
4. WHEN a deferral test passes THEN the Test SHALL have verified the observable guarantee that property changes don't cause immediate widget recreation

### Requirement 4: Preserve Architectural Documentation Test

**User Story:** As a maintainer, I want to retain the test that documents the Clock trigger architecture, so that significant architectural changes are flagged during refactoring.

#### Acceptance Criteria

1. WHEN the test suite is reviewed THEN the Test_Suite SHALL contain a test verifying `_rebuild_trigger` is a `ClockEvent` instance
2. WHEN the architectural test exists THEN the Test SHALL include a docstring explaining why this implementation detail is intentionally tested
3. IF the Clock trigger architecture changes THEN the Test SHALL fail to alert maintainers of the architectural change

### Requirement 5: Maintain Test Coverage of Rebuild Contract

**User Story:** As a maintainer, I want the refactored tests to fully cover the rebuild contract guarantees, so that no behavioral regressions can occur undetected.

#### Acceptance Criteria

1. WHEN all refactoring is complete THEN the Test_Suite SHALL verify that multiple property changes within the same frame result in at most one rebuild
2. WHEN all refactoring is complete THEN the Test_Suite SHALL verify that property changes trigger deferred rebuilds rather than synchronous rebuilds
3. WHEN all refactoring is complete THEN the Test_Suite SHALL verify that `force_rebuild()` executes pending rebuilds
4. WHEN running the refactored tests THEN all Tests SHALL pass without accessing internal state except for the architectural documentation test
