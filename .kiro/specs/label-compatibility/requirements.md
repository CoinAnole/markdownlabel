# Requirements Document

## Introduction

This feature addresses the behavioral gaps between `MarkdownLabel` and Kivy's native `Label` widget. While `MarkdownLabel` extends `BoxLayout` (necessary for multi-widget Markdown rendering), it should provide predictable, Label-like behavior for sizing, clipping, property updates, and performance. The goal is to make `MarkdownLabel` a true drop-in replacement for `Label` in scenarios where rich text formatting is needed, without surprising developers with divergent behavior.

## Glossary

- **MarkdownLabel**: The Kivy Garden widget that renders Markdown as interactive Kivy UI elements
- **Label**: Kivy's native text display widget with texture-based rendering
- **text_size**: A tuple (width, height) that constrains text layout and enables clipping in Label
- **strict_label_mode**: A MarkdownLabel property intended to enable Label-compatible sizing semantics
- **StencilView**: A Kivy widget that clips child content to its bounds using stencil buffer
- **texture**: The rendered bitmap representation of text content
- **base_font_size**: The base font size property in MarkdownLabel from which heading sizes are scaled
- **rebuild**: The process of recreating the widget tree when Markdown content or structural properties change

## Requirements

### Requirement 1

**User Story:** As a Kivy developer, I want `MarkdownLabel` to clip overflowing content when `text_size` height is constrained, so that the widget behaves like a native `Label` in fixed-height layouts.

#### Acceptance Criteria

1. WHEN `text_size[1]` is set to a non-None value THEN the MarkdownLabel SHALL clip rendered content that exceeds the specified height
2. WHEN `strict_label_mode` is True THEN the MarkdownLabel SHALL clip content to its bounds regardless of `text_size` settings
3. WHEN clipping is active THEN the MarkdownLabel SHALL use a StencilView or equivalent mechanism to prevent content from drawing outside widget bounds
4. WHEN `text_size[1]` is None and `strict_label_mode` is False THEN the MarkdownLabel SHALL allow content to expand vertically without clipping

### Requirement 2

**User Story:** As a Kivy developer, I want `base_font_size` changes to immediately update all rendered text, so that font size behaves consistently with Kivy Label's `font_size` property.

#### Acceptance Criteria

1. WHEN `base_font_size` is modified THEN the MarkdownLabel SHALL update all child Label widgets' font sizes immediately
2. WHEN `base_font_size` is modified THEN the MarkdownLabel SHALL preserve the relative scale factors for headings (h1, h2, etc.)
3. WHEN `base_font_size` is modified THEN the MarkdownLabel SHALL update font sizes without triggering a full widget tree rebuild
4. WHEN a child Label has a heading scale factor THEN the MarkdownLabel SHALL compute its font_size as `base_font_size * scale_factor`

### Requirement 3

**User Story:** As a Kivy developer, I want property changes to be batched and deferred like Kivy Label, so that multiple rapid property updates perform efficiently.

#### Acceptance Criteria

1. WHEN multiple properties are changed in the same frame THEN the MarkdownLabel SHALL batch the updates into a single rebuild operation
2. WHEN a property change triggers a rebuild THEN the MarkdownLabel SHALL schedule the rebuild using Clock.create_trigger for the next frame
3. WHEN the scheduled rebuild executes THEN the MarkdownLabel SHALL process all pending property changes in one operation
4. WHEN an immediate rebuild is required THEN the MarkdownLabel SHALL provide a method to force synchronous rebuilding

### Requirement 4

**User Story:** As a Kivy developer, I want clear documentation and aliasing for padding properties, so that I understand the difference between container padding and text padding.

#### Acceptance Criteria

1. WHEN a developer accesses `text_padding` THEN the MarkdownLabel SHALL apply padding inside individual Label widgets (like Label.padding)
2. WHEN a developer accesses `padding` THEN the MarkdownLabel SHALL apply padding to the outer BoxLayout container
3. WHEN the MarkdownLabel is initialized THEN the MarkdownLabel SHALL provide a `label_padding` alias that maps to `text_padding`
4. WHEN `label_padding` is modified THEN the MarkdownLabel SHALL update `text_padding` with the same value

### Requirement 5

**User Story:** As a Kivy developer, I want `halign='auto'` to respect text direction, so that right-to-left content aligns correctly by default.

#### Acceptance Criteria

1. WHEN `halign` is 'auto' and `base_direction` is 'rtl' or 'weak_rtl' THEN the MarkdownLabel SHALL use 'right' alignment
2. WHEN `halign` is 'auto' and `base_direction` is 'ltr', 'weak_ltr', or None THEN the MarkdownLabel SHALL use 'left' alignment
3. WHEN `base_direction` changes THEN the MarkdownLabel SHALL re-evaluate auto alignment for all child Labels
4. WHEN `halign` is explicitly set to 'left', 'center', 'right', or 'justify' THEN the MarkdownLabel SHALL use that alignment regardless of `base_direction`

### Requirement 6

**User Story:** As a Kivy developer, I want an optional single-texture render mode for maximum Label compatibility, so that I can use MarkdownLabel in complex layouts where widget-tree rendering causes issues.

#### Acceptance Criteria

1. WHEN `render_mode` is set to 'texture' THEN the MarkdownLabel SHALL render all content to a single texture and display it via an Image widget
2. WHEN `render_mode` is 'texture' and a link is clicked THEN the MarkdownLabel SHALL dispatch `on_ref_press` events using aggregated reference zones
3. WHEN `render_mode` is 'widgets' THEN the MarkdownLabel SHALL use the current widget-tree rendering approach
4. WHEN `render_mode` is 'auto' THEN the MarkdownLabel SHALL select the appropriate mode based on content complexity and layout constraints
5. WHEN switching between render modes THEN the MarkdownLabel SHALL preserve the visual appearance of the rendered Markdown
