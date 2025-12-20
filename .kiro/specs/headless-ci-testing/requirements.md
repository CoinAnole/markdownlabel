# Requirements Document

## Introduction

This feature enhances the MarkdownLabel test suite to make key behaviors deterministically testable in headless CI environments without relying on Kivy's text/GL pipeline to populate `Label.refs`. It introduces a `needs_window` pytest marker to separate tests that require a window from those that can run headlessly, strengthens assertions around widget identity preservation vs rebuild, and covers important untested branches (texture fallback, deep-nesting truncation placeholder).

## Glossary

- **MarkdownLabel**: The main widget class that renders Markdown text as Kivy widgets
- **Headless_CI**: Continuous integration environment without display/window capabilities
- **Texture_Mode**: Render mode where content is rendered to a single texture via Image widget
- **Widgets_Mode**: Render mode where content is rendered as a tree of Kivy widgets
- **Aggregated_Refs**: Dictionary mapping ref names to bounding box zones for hit-testing in texture mode
- **Refs**: Dictionary on Label widgets mapping reference names to bounding box coordinates
- **Anchors**: Dictionary on Label widgets mapping anchor names to coordinate positions
- **Nesting_Depth**: Counter tracking how deeply nested the current rendering context is
- **Truncation_Placeholder**: Widget displayed when content exceeds maximum nesting depth
- **FakeTouch**: Test utility class simulating touch events without requiring a window
- **Widget_Identity**: Python object id of a widget, used to verify same vs different widget instances

## Requirements

### Requirement 1: Pytest Marker for Window-Dependent Tests

**User Story:** As a CI maintainer, I want to separate tests that require a Kivy window from headless-safe tests, so that CI runs remain stable without display dependencies.

#### Acceptance Criteria

1. THE pytest.ini SHALL define a `needs_window` marker with description "marks tests that require a Kivy window/text provider"
2. THE pytest.ini addopts SHALL include `-m "not needs_window"` to exclude window-dependent tests by default
3. WHEN a test requires Kivy to populate `Label.refs` or render textures, THE Test_Suite SHALL mark it with `@pytest.mark.needs_window`
4. WHEN running `pytest` without marker flags, THE Test_Suite SHALL execute only headless-safe tests

### Requirement 2: Deterministic Texture Mode Hit-Testing Tests

**User Story:** As a developer, I want to test texture mode link hit-testing without relying on actual texture rendering, so that tests are deterministic in headless CI.

#### Acceptance Criteria

1. WHEN `_aggregated_refs` is manually set on a MarkdownLabel with `render_mode='texture'`, THE on_touch_down method SHALL dispatch `on_ref_press` for touches inside a ref zone
2. WHEN a touch occurs inside a ref zone, THE on_touch_down method SHALL return True
3. WHEN a touch occurs outside all ref zones, THE on_touch_down method SHALL NOT dispatch `on_ref_press`
4. WHEN a touch occurs outside all ref zones, THE on_touch_down method SHALL return the result of `super().on_touch_down(touch)`
5. WHEN multiple ref zones exist, THE on_touch_down method SHALL dispatch for the first matching zone
6. THE Test_Suite SHALL use a FakeTouch class with `x`, `y`, and `pos` attributes to simulate touches without a window

### Requirement 3: Deterministic Refs/Anchors Coordinate Translation Tests

**User Story:** As a developer, I want to verify the coordinate translation math for refs and anchors without relying on Kivy's text rendering, so that tests are deterministic in headless CI.

#### Acceptance Criteria

1. WHEN a child Label has `refs` set with known coordinates, THE MarkdownLabel._get_refs() method SHALL return translated coordinates in MarkdownLabel's local coordinate space
2. WHEN a child Label has `anchors` set with known coordinates, THE MarkdownLabel._get_anchors() method SHALL return translated coordinates in MarkdownLabel's local coordinate space
3. THE coordinate translation SHALL account for parent widget offsets (container.pos, label.pos)
4. THE coordinate translation SHALL account for texture centering within the Label widget
5. THE Test_Suite SHALL set deterministic geometry (pos, size, texture_size) on test widgets to verify translation math
6. WHEN existing tests depend on Kivy populating `Label.refs`, THE Test_Suite SHALL mark them with `@pytest.mark.needs_window`

### Requirement 4: Widget Identity Preservation Tests for Style Properties

**User Story:** As a developer, I want to verify that style-only property changes preserve widget identities, so that the performance optimization contract is proven by tests.

#### Acceptance Criteria

1. WHEN a style-only property (base_font_size, color, halign, valign, disabled, disabled_color, base_direction) is changed, THE MarkdownLabel SHALL preserve all widget object identities in the subtree
2. THE Test_Suite SHALL capture widget IDs of the entire subtree before property changes
3. THE Test_Suite SHALL verify the set of widget IDs is unchanged after style-only property changes
4. THE Test_Suite SHALL verify that style property values are propagated to all descendant Labels

### Requirement 5: Widget Identity Change Tests for Structure Properties

**User Story:** As a developer, I want to verify that structure property changes rebuild the widget tree, so that the rebuild contract is proven by tests.

#### Acceptance Criteria

1. WHEN a structure property (text, font_name, text_size, link_style, strict_label_mode, render_mode) is changed, THE MarkdownLabel SHALL rebuild the widget tree with new widget instances
2. THE Test_Suite SHALL capture widget IDs of children/subtree (excluding root MarkdownLabel) before property changes
3. THE Test_Suite SHALL verify that children widget IDs differ after structure property changes
4. THE Test_Suite SHALL verify that the root MarkdownLabel ID remains the same after structure property changes

### Requirement 6: Texture Fallback Branch Test

**User Story:** As a developer, I want to verify that texture mode falls back to widgets mode when texture rendering fails, so that the fallback behavior is covered by tests.

#### Acceptance Criteria

1. WHEN `_render_as_texture` returns None, THE MarkdownLabel SHALL fall back to widgets-mode rendering
2. WHEN texture rendering fails, THE widget tree SHALL contain Label widgets instead of an Image widget
3. THE Test_Suite SHALL monkeypatch `_render_as_texture` to return None to test the fallback branch

### Requirement 7: Deep Nesting Truncation Placeholder Test

**User Story:** As a developer, I want to verify that deeply nested content is truncated with a placeholder, so that the nesting protection behavior is covered by tests.

#### Acceptance Criteria

1. WHEN rendering content that exceeds `_max_nesting_depth`, THE KivyRenderer SHALL return a truncation placeholder widget
2. THE truncation placeholder SHALL be a Label widget with text containing "content truncated"
3. THE Test_Suite SHALL construct AST tokens that force nesting depth beyond `_max_nesting_depth`
4. THE Test_Suite SHALL verify the placeholder Label exists in the rendered output

