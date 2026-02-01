# Requirements Document

## Introduction

This feature adds proper support for reference-style links in MarkdownLabel. Reference-style links are a Markdown syntax that separates link text from URL definitions, making documents more readable and enabling citation-style references.

Mistune (the underlying parser) already parses reference-style links and resolves them to standard link tokens with the URL populated. However, the current implementation loses the reference-style metadata during serialization, converting all links to inline format. This feature ensures reference-style links are properly rendered as clickable links and can be serialized back to their original reference-style format.

## Glossary

- **Reference_Style_Link**: A Markdown link syntax where the URL is defined separately from the link text, using the format `[text][label]` with a definition `[label]: url` elsewhere in the document
- **Inline_Link**: A Markdown link where the URL is embedded directly: `[text](url)`
- **Link_Definition**: The line that defines a reference label's URL: `[label]: url "optional title"`
- **Implicit_Link**: A reference-style link where the label matches the text: `[Google][]` with `[Google]: url`
- **InlineRenderer**: The component that converts inline AST tokens to Kivy BBCode markup strings
- **MarkdownSerializer**: The component that converts AST tokens back to Markdown text
- **AST_Token**: Abstract Syntax Tree node produced by mistune parser

## Requirements

### Requirement 1: Reference-Style Link Rendering

**User Story:** As a developer, I want reference-style links to render as clickable links, so that I can use citation-style Markdown in my Kivy applications.

#### Acceptance Criteria

1. WHEN a reference-style link `[text][label]` with a valid definition `[label]: url` is parsed, THE InlineRenderer SHALL produce the same `[ref=url]text[/ref]` BBCode markup as inline links
2. WHEN an implicit reference-style link `[text][]` with definition `[text]: url` is parsed, THE InlineRenderer SHALL produce clickable `[ref=url]text[/ref]` markup
3. WHEN a reference-style link is clicked, THE MarkdownLabel SHALL dispatch the `on_ref_press` event with the resolved URL
4. WHEN link_style is 'styled', THE InlineRenderer SHALL apply color and underline formatting to reference-style links identically to inline links

### Requirement 2: Reference-Style Link Serialization

**User Story:** As a developer, I want reference-style links to serialize back to reference-style format, so that round-trip parsing preserves my document's citation structure.

#### Acceptance Criteria

1. WHEN a link token contains `ref` and `label` attributes (indicating reference-style origin), THE MarkdownSerializer SHALL serialize it as `[text][label]` format
2. WHEN serializing reference-style links, THE MarkdownSerializer SHALL collect and append all link definitions at the end of the document in the format `[label]: url`
3. WHEN a link token has a `title` attribute, THE MarkdownSerializer SHALL include it in the definition as `[label]: url "title"`
4. WHEN a link token lacks `ref`/`label` attributes (inline link), THE MarkdownSerializer SHALL continue to serialize it as `[text](url)` format
5. FOR ALL valid reference-style link Markdown, parsing then serializing then parsing SHALL produce an equivalent AST (round-trip property)

### Requirement 3: Edge Case Handling

**User Story:** As a developer, I want reference-style links to handle edge cases gracefully, so that malformed or unusual input doesn't break my application.

#### Acceptance Criteria

1. WHEN a reference-style link references an undefined label, THE MarkdownLabel SHALL render the raw text literally (mistune's default behavior)
2. WHEN multiple links share the same label, THE MarkdownSerializer SHALL output only one definition for that label
3. WHEN link text or URLs contain special characters requiring escaping, THE InlineRenderer SHALL escape them properly to prevent markup injection
4. WHEN a link definition contains a title with quotes, THE MarkdownSerializer SHALL properly escape or quote the title string
