# Changelog

## [v1.0.1] - 2026-02-21

### Fixed
- Fixed texture sizing semantics in auto/texture render mode when width/height constraints change.
- Fixed clipping behavior and property-binding lifecycle across rebuilds so style updates stay applied.
- Fixed fallback font cache/reference handling to avoid stale refs during dynamic updates.
- Fixed Markdown serialization for inline code spans that contain backticks.
- Fixed Markdown serialization to preserve inline link titles.

### Documentation
- Updated release install example to `v1.0.1`.
- Refreshed test documentation links and command paths for the `src/` layout.

## [v1.0.0] - 2026-02-20

### Added
- Initial release of MarkdownLabel
- Full Markdown syntax support (headings, paragraphs, lists, tables, code blocks, block quotes, images)
- Inline formatting (bold, italic, strikethrough, inline code, links)
- Interactive links with `on_ref_press` event handling
- Label-compatible API with support for `font_name`, `color`, `halign`, `valign`, `padding`, `text_size`
- Advanced font properties support (`font_family`, `font_kerning`, `font_hinting`, `font_blended`)
- Text processing options (`unicode_errors`, `strip`, `shorten`)
- Auto-sizing widget that adapts to content
- Built on mistune parser (v3.2.0) with plugin support
- Comprehensive test suite with pytest and Hypothesis property-based testing
- Texture render mode support for optimized rendering
- RTL (Right-to-Left) alignment support
- Code block syntax highlighting with customizable fonts and colors
- Table rendering with alignment support
- Reference-style links support
- Font fallback mechanism for missing glyphs
- Rebuild optimization system (STYLE_ONLY vs STRUCTURE property classification)
- Extensive documentation and examples
