# Implementation Plan: Reference-Style Links

## Overview

This implementation adds proper reference-style link support to MarkdownLabel. The main work is in the MarkdownSerializer to preserve reference-style format during serialization. The InlineRenderer already handles rendering correctly since mistune resolves reference-style links to standard link tokens.

## Tasks

- [x] 1. Enhance MarkdownSerializer for reference-style links
  - [x] 1.1 Add link definition tracking to MarkdownSerializer
    - Add `_link_definitions` dictionary to track label → (url, title) mappings
    - Reset the dictionary at the start of each `serialize()` call
    - _Requirements: 2.1, 2.2_
  
  - [x] 1.2 Update `inline_link` method to detect reference-style links
    - Check for `ref` and `label` fields in link tokens
    - If present, serialize as `[text][label]` format and collect definition
    - If absent, continue using existing `[text](url)` format
    - _Requirements: 2.1, 2.4_
  
  - [x] 1.3 Append link definitions at document end
    - After serializing all tokens, append collected definitions
    - Format: `[label]: url` or `[label]: url "title"` if title exists
    - Add blank line separator before definitions
    - _Requirements: 2.2, 2.3_
  
  - [x] 1.4 Write unit tests for reference-style link serialization
    - Test basic reference-style link serialization
    - Test implicit reference-style link (`[Google][]`)
    - Test link with title in definition
    - Test mixed inline and reference-style links
    - _Requirements: 2.1, 2.2, 2.3, 2.4_

- [x] 2. Implement definition deduplication
  - [x] 2.1 Handle multiple links with same label
    - When collecting definitions, use label as key (natural deduplication)
    - Verify only one definition is output per label
    - _Requirements: 3.2_
  
  - [x] 2.2 Write property test for duplicate label handling
    - **Property 4: Duplicate Labels Produce Single Definition**
    - **Validates: Requirements 3.2**

- [x] 3. Checkpoint - Verify serialization works
  - Ensure all tests pass, ask the user if questions arise.

- [x] 4. Add rendering verification tests
  - [x] 4.1 Write property test for rendering equivalence
    - **Property 1: Reference-Style Links Render Identically to Inline Links**
    - Verify reference-style links produce same BBCode as inline links
    - **Validates: Requirements 1.1, 1.2, 1.4**
  
  - [x] 4.2 Write unit test for on_ref_press event dispatch
    - Create MarkdownLabel with reference-style link
    - Verify on_ref_press event contains resolved URL
    - _Requirements: 1.3_

- [ ] 5. Add round-trip serialization tests
  - [ ] 5.1 Write property test for round-trip serialization
    - **Property 3: Reference-Style Link Round-Trip Serialization**
    - Parse reference-style markdown, serialize, parse again
    - Compare normalized ASTs for semantic equivalence
    - **Validates: Requirements 2.1, 2.2, 2.3, 2.4, 2.5**
  
  - [ ] 5.2 Write unit tests for round-trip edge cases
    - Test round-trip with titles containing special characters
    - Test round-trip with multiple definitions
    - _Requirements: 2.5, 3.4_

- [ ] 6. Add Hypothesis strategy for reference-style links
  - [ ] 6.1 Create `markdown_reference_link` strategy in test_utils.py
    - Generate valid reference-style link markdown
    - Include variations: explicit label, implicit label, with title
    - _Requirements: 2.5_

- [ ] 7. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- All tasks including tests are required for comprehensive coverage
- The InlineRenderer does not need modification - mistune already resolves reference-style links
- Property tests should use minimum 100 iterations per Hypothesis guidelines
- Tests should be added to existing test files (test_serialization.py, test_core_functionality.py)
