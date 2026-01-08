# Implementation Plan: Optimize Rebuild Contract

## Overview

This implementation plan reclassifies 14 properties from "structure" to "style-only" in MarkdownLabel's rebuild contract. The changes are organized to minimize risk: first update the property sets, then extend the style update method, then add tests to verify correctness.

## Tasks

- [x] 1. Update property classification sets
  - [x] 1.1 Add reclassified properties to STYLE_ONLY_PROPERTIES
    - Add `font_family`, `font_context`, `font_features`, `font_hinting`, `font_kerning`, `font_blended` to the set
    - Add `unicode_errors`, `strip` to the set
    - Add `shorten`, `max_lines`, `shorten_from`, `split_str`, `ellipsis_options` to the set
    - Add `text_size` to the set
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

  - [x] 1.2 Remove reclassified properties from STRUCTURE_PROPERTIES
    - Remove all 14 reclassified properties from STRUCTURE_PROPERTIES
    - Verify only `text`, `link_style`, `render_mode`, `strict_label_mode` remain
    - _Requirements: 5.5, 5.6_

- [x] 2. Extend _update_styles_in_place method
  - [x] 2.1 Add advanced font property updates
    - Update `font_family` on non-code Labels (check `_is_code` marker)
    - Update `font_context` on all Labels (with None check)
    - Update `font_features` on all Labels
    - Update `font_hinting` on all Labels (with None check)
    - Update `font_kerning` on all Labels
    - Update `font_blended` on all Labels
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 6.2, 6.3_

  - [x] 2.2 Add text processing property updates
    - Update `unicode_errors` on all Labels
    - Update `strip` on all Labels
    - _Requirements: 2.1, 2.2, 6.4_

  - [x] 2.3 Add truncation property updates
    - Update `shorten` on all Labels
    - Update `max_lines` on all Labels (only if > 0)
    - Update `shorten_from` on all Labels
    - Update `split_str` on all Labels
    - Update `ellipsis_options` on all Labels (as dict copy)
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 6.5_

  - [x] 2.4 Add text_size update logic
    - Update `text_size` on all Labels based on current value
    - Handle `[None, None]`, `[width, None]`, `[None, height]`, `[width, height]` cases
    - Respect `strict_label_mode` for binding behavior
    - _Requirements: 4.1, 4.2, 4.3, 6.6_

- [x] 3. Checkpoint - Verify basic functionality
  - Ensure all tests pass, ask the user if questions arise.

- [x] 4. Write property-based tests for widget identity preservation
  - [x] 4.1 Write property test for advanced font properties preserving widget identity
    - **Property 1: Style-only property updates preserve widget identity**
    - Test `font_family`, `font_context`, `font_features`, `font_hinting`, `font_kerning`, `font_blended`
    - Verify widget IDs unchanged after property change
    - **Validates: Requirements 1.1-1.7**

  - [x] 4.2 Write property test for text processing properties preserving widget identity
    - **Property 1: Style-only property updates preserve widget identity**
    - Test `unicode_errors`, `strip`
    - Verify widget IDs unchanged after property change
    - **Validates: Requirements 2.1-2.3**

  - [x] 4.3 Write property test for truncation properties preserving widget identity
    - **Property 1: Style-only property updates preserve widget identity**
    - Test `shorten`, `max_lines`, `shorten_from`, `split_str`, `ellipsis_options`
    - Verify widget IDs unchanged after property change
    - **Validates: Requirements 3.1-3.6**

  - [x] 4.4 Write property test for text_size preserving widget identity
    - **Property 3: text_size updates preserve widget identity**
    - Test various text_size transitions
    - Verify widget IDs unchanged after property change
    - **Validates: Requirements 4.1, 4.4**

- [x] 5. Write property-based tests for value application
  - [x] 5.1 Write property test for advanced font properties applied to children
    - **Property 2: Style-only property updates apply values to all child Labels**
    - Verify all child Labels have the new property value
    - **Validates: Requirements 1.1-1.6**

  - [x] 5.2 Write property test for text processing properties applied to children
    - **Property 2: Style-only property updates apply values to all child Labels**
    - Verify all child Labels have the new property value
    - **Validates: Requirements 2.1-2.2**

  - [x] 5.3 Write property test for truncation properties applied to children
    - **Property 2: Style-only property updates apply values to all child Labels**
    - Verify all child Labels have the new property value
    - **Validates: Requirements 3.1-3.5**

- [x] 6. Write tests for special cases
  - [x] 6.1 Write property test for code block font preservation
    - **Property 4: Code blocks preserve monospace font when font_family changes**
    - Create markdown with code blocks
    - Change font_family
    - Verify code blocks keep code_font_name
    - **Validates: Requirements 6.2**

  - [x] 6.2 Write unit tests for property classification sets
    - **Property 5: Property classification sets are mutually exclusive and complete**
    - Verify reclassified properties in STYLE_ONLY_PROPERTIES
    - Verify STRUCTURE_PROPERTIES contains only expected properties
    - Verify sets are mutually exclusive
    - **Validates: Requirements 5.1-5.6**

  - [x] 6.3 Write unit tests for text_size binding transitions
    - Test transition from [None, None] to constrained value
    - Test transition from constrained value to [None, None]
    - Verify bindings work correctly after transition
    - **Validates: Requirements 4.2, 4.3**

- [x] 7. Checkpoint - Verify all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 8. Update documentation
  - [ ] 8.1 Update REBUILD_CONTRACT.md
    - Move reclassified properties from Structure to Style-Only section
    - Update property tables
    - Document performance benefits
    - _Requirements: 7.1, 7.3_

  - [ ] 8.2 Update TESTING.md
    - Update Style-Only Properties list
    - Update Structure Properties list
    - _Requirements: 7.2_

  - [ ] 8.3 Update docstrings in __init__.py
    - Update STYLE_ONLY_PROPERTIES docstring
    - Update STRUCTURE_PROPERTIES docstring
    - _Requirements: 7.4_

- [ ] 9. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- All tasks are required for comprehensive coverage
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties
- Unit tests validate specific examples and edge cases
