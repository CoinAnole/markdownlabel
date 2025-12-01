# Requirements Document

## Introduction

This specification addresses Phase 2 of Label API compatibility improvements for the MarkdownLabel widget, building on the Phase 1 work (text_size height, padding forwarding, auto-sizing). The goal is to achieve comprehensive drop-in compatibility with Kivy's standard Label widget, covering property surface area, sizing semantics, shortening/overflow, interactivity parity, and rendering knobs. These improvements will enable developers to replace Label with MarkdownLabel in existing applications with minimal code changes.

## Glossary

- **MarkdownLabel**: A Kivy Garden widget that renders Markdown documents as interactive Kivy UI elements, extending BoxLayout
- **Label**: Kivy's standard text display widget
- **Drop-in Compatibility**: The ability to replace one widget with another without changing application code
- **Property Surface Area**: The complete set of properties a widget exposes
- **No-op Property**: A property that is accepted but has no effect on widget behavior
- **Strict Label Mode**: A compatibility mode where MarkdownLabel behaves exactly like Label for sizing and text_size semantics
- **refs**: Dictionary mapping reference names to their bounding box coordinates in Label
- **anchors**: Dictionary mapping anchor names to their positions in Label
- **texture_size**: The size of the rendered text texture in Label
- **shorten**: Label property that truncates text with ellipsis when it exceeds text_size
- **Child Label**: Internal Label widgets created by KivyRenderer to display Markdown content

## Requirements

### Requirement 1: Property Surface Area Acceptance

**User Story:** As a Kivy developer, I want MarkdownLabel to accept all common Label properties without crashing, so that I can use it as a drop-in replacement in existing kv files and application code.

#### Acceptance Criteria

1. WHEN a user passes any of the following properties to MarkdownLabel THEN the MarkdownLabel SHALL accept them without raising an exception: `mipmap`, `outline_width`, `outline_color`, `text_language`, `base_direction`, `ellipsis_options`
2. WHEN a user accesses a no-op property THEN the MarkdownLabel SHALL return the stored value
3. WHEN a user sets the `markup` property THEN the MarkdownLabel SHALL store the value and document that Markdown rendering always uses markup internally

### Requirement 2: Strict Label Sizing Mode

**User Story:** As a Kivy developer, I want a strict compatibility mode where MarkdownLabel follows Label's sizing rules exactly, so that I can use it in layouts designed for Label without unexpected behavior.

#### Acceptance Criteria

1. WHEN `strict_label_mode` is True THEN the MarkdownLabel SHALL NOT auto-size its height by default
2. WHEN `strict_label_mode` is True and `text_size` is `[None, None]` THEN the MarkdownLabel SHALL NOT bind internal Label widths to the widget width
3. WHEN `strict_label_mode` is True THEN the MarkdownLabel SHALL only constrain text when `text_size` is explicitly set
4. WHEN `strict_label_mode` is False (default) THEN the MarkdownLabel SHALL use the current Markdown-friendly auto-wrap and auto-size behavior

### Requirement 3: Accurate texture_size Calculation

**User Story:** As a Kivy developer, I want `texture_size` to accurately reflect the minimum content size including all child widgets, so that I can use it for layout calculations.

#### Acceptance Criteria

1. WHEN calculating `texture_size` THEN the MarkdownLabel SHALL include the dimensions of all descendant widgets including Labels, Images, Tables, and Code containers
2. WHEN `texture_size` is queried THEN the MarkdownLabel SHALL return a tuple representing the minimum width and total height needed to display all content
3. WHEN child widget sizes change THEN the MarkdownLabel SHALL update `texture_size` to reflect the new dimensions

### Requirement 4: Shortening and Overflow Support

**User Story:** As a Kivy developer, I want text shortening properties to work consistently across all text content in MarkdownLabel, so that I can control text overflow behavior.

#### Acceptance Criteria

1. WHEN `shorten` is True THEN the MarkdownLabel SHALL forward the shorten property to all child Labels including paragraphs, headings, list items, table cells, and quote text
2. WHEN `shorten_from` is set THEN the MarkdownLabel SHALL forward the value to all child Labels
3. WHEN `split_str` is set THEN the MarkdownLabel SHALL forward the value to all child Labels
4. WHEN `max_lines` is set THEN the MarkdownLabel SHALL forward the value to all child Labels
5. WHEN `ellipsis_options` is set THEN the MarkdownLabel SHALL forward the value to all child Labels that support it

### Requirement 5: Interactivity Coordinate Translation

**User Story:** As a Kivy developer, I want `refs` and `anchors` to provide coordinates in MarkdownLabel's local coordinate space, so that I can use them for overlays and hit testing.

#### Acceptance Criteria

1. WHEN accessing `refs` THEN the MarkdownLabel SHALL return a dictionary with reference bounding boxes translated to MarkdownLabel's local coordinate space
2. WHEN accessing `anchors` THEN the MarkdownLabel SHALL return a dictionary with anchor positions translated to MarkdownLabel's local coordinate space
3. WHEN child Labels move or resize THEN the MarkdownLabel SHALL update the translated `refs` and `anchors` coordinates
4. WHEN `on_ref_press` is dispatched THEN the event SHALL include the reference name consistent with Label's behavior

### Requirement 6: Font Advanced Options Forwarding

**User Story:** As a Kivy developer, I want advanced font properties to be forwarded to all text-rendering Labels, so that I can customize text appearance consistently.

#### Acceptance Criteria

1. WHEN `font_family` is set THEN the MarkdownLabel SHALL forward it to all child Labels except code blocks
2. WHEN `font_context` is set THEN the MarkdownLabel SHALL forward it to all child Labels
3. WHEN `font_features` is set THEN the MarkdownLabel SHALL forward it to all child Labels
4. WHEN `font_hinting` is set THEN the MarkdownLabel SHALL forward it to all child Labels
5. WHEN `font_kerning` is set THEN the MarkdownLabel SHALL forward it to all child Labels

### Requirement 7: Efficient Property Updates

**User Story:** As a Kivy developer, I want style property changes to update rendering without full widget reconstruction, so that the widget performs efficiently.

#### Acceptance Criteria

1. WHEN a purely stylistic property changes (font_size, color, halign, valign) THEN the MarkdownLabel SHALL update descendant properties in place without rebuilding the widget tree
2. WHEN the markdown text or AST changes THEN the MarkdownLabel SHALL rebuild the widget structure
3. WHEN a property affecting block structure changes THEN the MarkdownLabel SHALL rebuild the widget structure

### Requirement 8: Documentation and Compatibility Matrix

**User Story:** As a Kivy developer, I want clear documentation of which Label properties are supported, partially supported, no-op, or unsupported, so that I can understand the compatibility level.

#### Acceptance Criteria

1. WHEN a developer reads the documentation THEN the documentation SHALL include a Label compatibility matrix showing property support levels
2. WHEN a property is a no-op THEN the documentation SHALL clearly state this
3. WHEN two modes exist (strict vs markdown-friendly) THEN the documentation SHALL explain the differences and when to use each

