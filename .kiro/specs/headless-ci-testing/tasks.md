# Implementation Plan: Headless CI Testing

## Overview

This implementation plan adds deterministic, headless-safe tests for MarkdownLabel's texture mode hit-testing, coordinate translation, widget identity preservation, and untested renderer branches. The implementation follows an incremental approach, starting with pytest configuration, then adding test utilities, and finally implementing the test cases.

## Tasks

- [x] 1. Configure pytest marker for window-dependent tests
  - Add `needs_window` marker to pytest.ini
  - Update addopts to exclude `needs_window` tests by default
  - _Requirements: 1.1, 1.2, 1.4_

- [x] 2. Add FakeTouch utility class
  - [x] 2.1 Create FakeTouch class in test_utils.py
    - Add minimal touch simulation class with x, y, pos attributes
    - _Requirements: 2.6_

- [x] 3. Implement deterministic texture mode hit-testing tests
  - [x] 3.1 Add inside-zone dispatch test
    - Create MarkdownLabel with render_mode='texture'
    - Manually set _aggregated_refs with known zones
    - Bind on_ref_press to capture dispatched ref
    - Call on_touch_down with FakeTouch inside zone
    - Assert handler called with correct ref and returns True
    - _Requirements: 2.1, 2.2_

  - [x] 3.2 Write property test for inside-zone dispatch
    - **Property 1: Touch Inside Ref Zone Dispatches Event**
    - **Validates: Requirements 2.1, 2.2**

  - [x] 3.3 Add outside-zone no-dispatch test
    - Same setup as 3.1 but touch at coordinates outside all zones
    - Assert no dispatch and method returns False
    - _Requirements: 2.3, 2.4_

  - [x] 3.4 Write property test for outside-zone behavior
    - **Property 2: Touch Outside Ref Zones Does Not Dispatch**
    - **Validates: Requirements 2.3, 2.4**

  - [x] 3.5 Add multiple zones test
    - Set up multiple overlapping ref zones
    - Verify first matching zone triggers dispatch
    - _Requirements: 2.5_

- [x] 4. Implement deterministic refs/anchors translation tests
  - [x] 4.1 Add refs translation test with injected geometry
    - Build minimal widget tree: MarkdownLabel > BoxLayout > Label
    - Set deterministic pos, size, texture_size on all widgets
    - Inject refs onto child Label
    - Assert aggregated refs match expected translated coordinates
    - _Requirements: 3.1, 3.3, 3.4_

  - [x] 4.2 Write property test for refs translation math
    - **Property 3: Refs Coordinate Translation Math**
    - **Validates: Requirements 3.1, 3.3, 3.4**

  - [x] 4.3 Add anchors translation test with injected geometry
    - Same setup as 4.1 but inject anchors instead of refs
    - Assert aggregated anchors match expected translated coordinates
    - _Requirements: 3.2, 3.3, 3.4_

  - [x] 4.4 Write property test for anchors translation math
    - **Property 4: Anchors Coordinate Translation Math**
    - **Validates: Requirements 3.2, 3.3, 3.4**

  - [x] 4.5 Mark existing window-dependent tests with needs_window
    - Review existing coordinate translation tests
    - Add @pytest.mark.needs_window to tests requiring Label.refs population
    - _Requirements: 3.6_

- [x] 5. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 6. Implement widget identity preservation tests
  - [x] 6.1 Create test_rebuild_semantics.py module
    - Add collect_widget_ids helper function
    - _Requirements: 4.2, 5.2_

  - [x] 6.2 Add style property identity preservation tests
    - Test base_font_size, color, halign, valign, disabled, disabled_color, base_direction, line_height
    - Capture widget IDs before change
    - Apply property change
    - Assert widget IDs unchanged
    - _Requirements: 4.1_

  - [x] 6.3 Write property test for style property identity preservation
    - **Property 5: Style Property Changes Preserve Widget Identities**
    - **Validates: Requirements 4.1**

  - [x] 6.4 Add style property propagation tests
    - Verify property values propagate to all descendant Labels
    - _Requirements: 4.4_

  - [x] 6.5 Write property test for style property propagation
    - **Property 6: Style Property Values Propagate to Descendants**
    - **Validates: Requirements 4.4**

  - [x] 6.6 Add structure property rebuild tests
    - Test text, font_name, text_size, link_style, strict_label_mode, render_mode
    - Capture children widget IDs before change
    - Apply property change and force_rebuild()
    - Assert children widget IDs differ
    - Assert root MarkdownLabel ID unchanged
    - _Requirements: 5.1, 5.4_

  - [x] 6.7 Write property test for structure property rebuild
    - **Property 7: Structure Property Changes Rebuild Widget Tree**
    - **Validates: Requirements 5.1**

  - [x] 6.8 Write property test for root ID preservation
    - **Property 8: Root Widget ID Preserved Across Property Changes**
    - **Validates: Requirements 5.4**

- [x] 7. Implement texture fallback branch test
  - [x] 7.1 Add texture fallback test to test_texture_render_mode.py
    - Monkeypatch _render_as_texture to return None
    - Create MarkdownLabel with render_mode='texture' and non-empty text
    - Call force_rebuild()
    - Assert no Image widget in tree
    - Assert at least one Label widget exists (widgets-mode fallback)
    - _Requirements: 6.1, 6.2_

- [x] 8. Implement deep nesting truncation placeholder test
  - [x] 8.1 Add truncation placeholder test to test_kivy_renderer.py
    - Construct AST token with nesting depth > _max_nesting_depth
    - Render via KivyRenderer
    - Assert Label exists with text containing "content truncated"
    - _Requirements: 7.1, 7.2_

- [x] 9. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties
- Unit tests validate specific examples and edge cases

