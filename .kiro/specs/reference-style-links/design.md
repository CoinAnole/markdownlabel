# Design Document: Reference-Style Links

## Overview

This design adds proper support for reference-style links in MarkdownLabel. Reference-style links use the syntax `[text][label]` with definitions `[label]: url` elsewhere in the document, enabling cleaner citation-style Markdown.

The key insight is that mistune (v3.0+) already parses reference-style links and resolves them to standard `link` tokens with the URL populated. The AST tokens include additional `ref` and `label` fields that indicate the original reference-style format. This means:

1. **Rendering already works** - The existing `InlineRenderer.link()` method handles these tokens correctly
2. **Serialization needs enhancement** - The `MarkdownSerializer` must be updated to preserve reference-style format

## Architecture

The implementation follows the existing three-layer rendering pipeline:

```
┌─────────────────────────────────────────────────────────────────┐
│                        Markdown Input                            │
│  "Click [here][1] for info.\n\n[1]: http://example.com/"        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     mistune Parser                               │
│  Resolves [here][1] → link token with url="http://example.com/" │
│  Adds ref="1", label="1" to indicate reference-style origin     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    AST Token (link)                              │
│  {                                                               │
│    "type": "link",                                               │
│    "children": [{"type": "text", "raw": "here"}],               │
│    "attrs": {"url": "http://example.com/", "title": null},      │
│    "ref": "1",        ← indicates reference-style               │
│    "label": "1"       ← the label used                          │
│  }                                                               │
└─────────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
┌─────────────────────────┐     ┌─────────────────────────┐
│    InlineRenderer       │     │   MarkdownSerializer    │
│  (No changes needed)    │     │  (Needs enhancement)    │
│                         │     │                         │
│  Produces:              │     │  Produces:              │
│  [ref=url]here[/ref]    │     │  [here][1]              │
│                         │     │  ...                    │
│                         │     │  [1]: http://example.com│
└─────────────────────────┘     └─────────────────────────┘
```

## Components and Interfaces

### InlineRenderer (No Changes Required)

The existing `InlineRenderer.link()` method already handles reference-style links correctly because mistune resolves them to standard link tokens:

```python
def link(self, token: Dict[str, Any]) -> str:
    """Render link as [ref=url]...[/ref] with color and underline."""
    children = token.get('children', [])
    attrs = token.get('attrs', {})
    url = attrs.get('url', '')  # Already resolved by mistune
    # ... rest of implementation unchanged
```

### MarkdownSerializer (Requires Enhancement)

The serializer needs to:
1. Detect reference-style links via `ref`/`label` fields
2. Track link definitions during serialization
3. Append definitions at document end

```python
class MarkdownSerializer:
    def __init__(self):
        self._link_definitions = {}  # label -> (url, title)
    
    def serialize(self, tokens: List[Dict[str, Any]]) -> str:
        """Convert AST tokens to Markdown string."""
        self._link_definitions = {}  # Reset for each serialization
        
        result = []
        for token in tokens:
            serialized = self._serialize_token(token)
            if serialized is not None:
                result.append(serialized)
        
        # Append link definitions at end
        if self._link_definitions:
            result.append('')  # Blank line before definitions
            for label, (url, title) in self._link_definitions.items():
                if title:
                    result.append(f'[{label}]: {url} "{title}"')
                else:
                    result.append(f'[{label}]: {url}')
        
        return '\n\n'.join(result)
    
    def inline_link(self, token: Dict[str, Any]) -> str:
        """Serialize link token, preserving reference-style format."""
        children = token.get('children', [])
        attrs = token.get('attrs', {})
        url = attrs.get('url', '')
        title = attrs.get('title')
        
        text = self.serialize_inline(children)
        
        # Check for reference-style indicators
        ref = token.get('ref')
        label = token.get('label')
        
        if ref is not None and label is not None:
            # Reference-style link - collect definition
            self._link_definitions[label] = (url, title)
            return f'[{text}][{label}]'
        else:
            # Inline link - existing behavior
            return f'[{text}]({url})'
```

## Data Models

### Link Token Structure (from mistune)

Reference-style links produce tokens with additional fields:

```python
# Inline link token
{
    "type": "link",
    "children": [{"type": "text", "raw": "click here"}],
    "attrs": {"url": "http://example.com/", "title": None}
}

# Reference-style link token (after mistune resolution)
{
    "type": "link",
    "children": [{"type": "text", "raw": "click here"}],
    "attrs": {"url": "http://example.com/", "title": "Optional Title"},
    "ref": "ID",      # Uppercase version of label (mistune internal)
    "label": "id"     # Original label as written
}
```

### Link Definition Tracking

During serialization, definitions are tracked in a dictionary:

```python
_link_definitions: Dict[str, Tuple[str, Optional[str]]]
# Maps label -> (url, title)
# Example: {"1": ("http://example.com/", None), "wiki": ("http://wiki.org/", "Wiki")}
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Reference-Style Links Render Identically to Inline Links

*For any* reference-style link `[text][label]` with definition `[label]: url`, the InlineRenderer SHALL produce the same BBCode markup as an equivalent inline link `[text](url)`.

**Validates: Requirements 1.1, 1.2, 1.4**

### Property 2: Reference-Style Link Click Dispatches Event

*For any* MarkdownLabel containing reference-style links, clicking a link SHALL dispatch the `on_ref_press` event with the resolved URL from the definition.

**Validates: Requirements 1.3**

### Property 3: Reference-Style Link Round-Trip Serialization

*For any* valid Markdown document containing reference-style links, parsing then serializing then parsing SHALL produce an equivalent AST (semantic equivalence after normalization).

**Validates: Requirements 2.1, 2.2, 2.3, 2.4, 2.5**

### Property 4: Duplicate Labels Produce Single Definition

*For any* document with multiple links sharing the same label, serialization SHALL output exactly one definition for that label.

**Validates: Requirements 3.2**

### Property 5: Special Characters Are Escaped

*For any* reference-style link containing special characters (brackets, ampersands) in text or URLs, the InlineRenderer SHALL escape them to prevent markup injection.

**Validates: Requirements 3.3, 3.4**

## Error Handling

### Undefined Reference Labels

When a reference-style link references an undefined label (e.g., `[text][undefined]` with no `[undefined]: url` definition), mistune does not resolve it to a link token. Instead, it remains as literal text. No special handling is needed in MarkdownLabel.

### Malformed Definitions

Mistune handles malformed link definitions during parsing. Invalid definitions are ignored, and the reference remains unresolved.

### Title Escaping

When serializing link definitions with titles containing quotes, the serializer uses double quotes and relies on the title not containing unescaped double quotes (mistune's parsing behavior).

## Testing Strategy

### Dual Testing Approach

- **Unit tests**: Verify specific examples and edge cases
- **Property tests**: Verify universal properties across generated inputs

### Property-Based Testing Configuration

- **Library**: Hypothesis (already used in project)
- **Minimum iterations**: 100 per property test
- **Tag format**: `**Feature: reference-style-links, Property N: description**`

### Test Organization

Tests will be added to `kivy_garden/markdownlabel/tests/test_serialization.py` for serialization properties and `kivy_garden/markdownlabel/tests/test_core_functionality.py` for rendering properties.

### Unit Test Cases

1. Basic reference-style link rendering
2. Implicit reference-style link (`[Google][]`)
3. Reference-style link with title
4. Multiple links with same label
5. Mixed inline and reference-style links in same document
6. Reference-style link round-trip serialization
7. Undefined reference label (literal text output)

### Property Test Cases

1. Reference-style links produce same BBCode as inline links
2. Round-trip serialization preserves semantic equivalence
3. Duplicate labels produce single definition
4. Special character escaping prevents markup injection
