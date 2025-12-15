"""
Tests for round-trip serialization functionality.

This module contains tests that verify the MarkdownLabel can correctly
serialize and deserialize Markdown content, maintaining semantic equivalence
through parse-serialize-parse cycles.
"""

import os
# Set environment variable to use headless mode for Kivy
os.environ['KIVY_NO_ARGS'] = '1'
os.environ['KIVY_NO_CONSOLELOG'] = '1'

from hypothesis import given, settings, assume

from kivy_garden.markdownlabel import MarkdownLabel
from .test_utils import (
    markdown_heading,
    markdown_paragraph,
    markdown_bold,
    markdown_italic,
    markdown_link,
    simple_markdown_document
)


class TestRoundTripSerialization:
    """Property tests for round-trip serialization (Property 17)."""
    
    def _normalize_ast(self, tokens):
        """Normalize AST for comparison by removing non-semantic fields.
        
        Args:
            tokens: List of AST tokens
            
        Returns:
            Normalized token list for comparison
        """
        if not isinstance(tokens, list):
            return tokens
        
        normalized = []
        for token in tokens:
            if not isinstance(token, dict):
                normalized.append(token)
                continue
            
            # Skip blank_line tokens as they're formatting artifacts
            if token.get('type') == 'blank_line':
                continue
            
            # Create normalized copy without style/formatting metadata
            norm_token = {}
            for key, value in token.items():
                # Skip non-semantic fields
                if key in ('style',):
                    continue
                elif key == 'children':
                    norm_token[key] = self._normalize_ast(value)
                elif key == 'attrs':
                    # Keep attrs but normalize them
                    norm_token[key] = dict(value) if value else {}
                elif key == 'bullet':
                    # Normalize bullet character - all unordered list bullets
                    # are semantically equivalent (-, +, *)
                    norm_token[key] = '-'
                else:
                    norm_token[key] = value
            
            normalized.append(norm_token)
        
        # Merge adjacent text tokens for semantic comparison
        normalized = self._merge_adjacent_text(normalized)
        
        return normalized
    
    def _merge_adjacent_text(self, tokens):
        """Merge adjacent text tokens into single tokens.
        
        This handles cases where the same text content is tokenized
        differently (e.g., '0:' vs '0' + ':').
        
        Args:
            tokens: List of normalized tokens
            
        Returns:
            Tokens with adjacent text merged
        """
        if not tokens:
            return tokens
        
        merged = []
        i = 0
        while i < len(tokens):
            token = tokens[i]
            
            if isinstance(token, dict) and token.get('type') == 'text':
                # Collect consecutive text tokens
                text_parts = [token.get('raw', '')]
                j = i + 1
                while j < len(tokens):
                    next_token = tokens[j]
                    if isinstance(next_token, dict) and next_token.get('type') == 'text':
                        text_parts.append(next_token.get('raw', ''))
                        j += 1
                    else:
                        break
                
                # Create merged text token
                merged.append({'type': 'text', 'raw': ''.join(text_parts)})
                i = j
            else:
                merged.append(token)
                i += 1
        
        return merged
    
    @given(markdown_heading())
    @settings(max_examples=100, deadline=None)
    def test_heading_round_trip(self, heading):
        """Heading round-trips through parse-serialize-parse."""
        label = MarkdownLabel(text=heading)
        ast1 = self._normalize_ast(label.get_ast())
        
        # Serialize back to markdown
        serialized = label.to_markdown()
        
        # Parse again
        label2 = MarkdownLabel(text=serialized)
        ast2 = self._normalize_ast(label2.get_ast())
        
        # ASTs should be equivalent
        assert ast1 == ast2, \
            f"AST mismatch after round-trip:\nOriginal: {ast1}\nAfter: {ast2}\nSerialized: {serialized!r}"
    
    @given(markdown_paragraph())
    @settings(max_examples=100, deadline=None)
    def test_paragraph_round_trip(self, paragraph):
        """Paragraph round-trips through parse-serialize-parse."""
        assume(paragraph.strip())
        
        label = MarkdownLabel(text=paragraph)
        ast1 = self._normalize_ast(label.get_ast())
        
        # Skip if the paragraph was parsed as something other than a paragraph
        # (e.g., "0)" gets parsed as an ordered list)
        if ast1 and ast1[0].get('type') != 'paragraph':
            assume(False)
        
        serialized = label.to_markdown()
        
        label2 = MarkdownLabel(text=serialized)
        ast2 = self._normalize_ast(label2.get_ast())
        
        assert ast1 == ast2, \
            f"AST mismatch after round-trip:\nOriginal: {ast1}\nAfter: {ast2}"
    
    @given(markdown_bold())
    @settings(max_examples=100, deadline=None)
    def test_bold_round_trip(self, bold_text):
        """Bold text round-trips through parse-serialize-parse."""
        label = MarkdownLabel(text=bold_text)
        ast1 = self._normalize_ast(label.get_ast())
        
        serialized = label.to_markdown()
        
        label2 = MarkdownLabel(text=serialized)
        ast2 = self._normalize_ast(label2.get_ast())
        
        assert ast1 == ast2, \
            f"AST mismatch after round-trip:\nOriginal: {ast1}\nAfter: {ast2}"
    
    @given(markdown_italic())
    @settings(max_examples=100, deadline=None)
    def test_italic_round_trip(self, italic_text):
        """Italic text round-trips through parse-serialize-parse."""
        label = MarkdownLabel(text=italic_text)
        ast1 = self._normalize_ast(label.get_ast())
        
        serialized = label.to_markdown()
        
        label2 = MarkdownLabel(text=serialized)
        ast2 = self._normalize_ast(label2.get_ast())
        
        assert ast1 == ast2, \
            f"AST mismatch after round-trip:\nOriginal: {ast1}\nAfter: {ast2}"
    
    @given(markdown_link())
    @settings(max_examples=100, deadline=None)
    def test_link_round_trip(self, link_text):
        """Link round-trips through parse-serialize-parse."""
        label = MarkdownLabel(text=link_text)
        ast1 = self._normalize_ast(label.get_ast())
        
        serialized = label.to_markdown()
        
        label2 = MarkdownLabel(text=serialized)
        ast2 = self._normalize_ast(label2.get_ast())
        
        assert ast1 == ast2, \
            f"AST mismatch after round-trip:\nOriginal: {ast1}\nAfter: {ast2}"
    
    @given(simple_markdown_document())
    @settings(max_examples=100, deadline=None)
    def test_document_round_trip(self, markdown_text):
        """Full document round-trips through parse-serialize-parse."""
        assume(markdown_text.strip())
        # Skip texts with escape sequences that change meaning when unescaped
        assume('\\' not in markdown_text)
        
        label = MarkdownLabel(text=markdown_text)
        ast1 = self._normalize_ast(label.get_ast())
        
        serialized = label.to_markdown()
        
        label2 = MarkdownLabel(text=serialized)
        ast2 = self._normalize_ast(label2.get_ast())
        
        assert ast1 == ast2, \
            f"AST mismatch after round-trip:\nOriginal: {ast1}\nAfter: {ast2}\nSerialized: {serialized!r}"
    
    def test_code_block_round_trip(self):
        """Code block round-trips correctly."""
        markdown = '```python\nprint("hello")\n```'
        
        label = MarkdownLabel(text=markdown)
        ast1 = self._normalize_ast(label.get_ast())
        
        serialized = label.to_markdown()
        
        label2 = MarkdownLabel(text=serialized)
        ast2 = self._normalize_ast(label2.get_ast())
        
        assert ast1 == ast2, \
            f"AST mismatch after round-trip:\nOriginal: {ast1}\nAfter: {ast2}"
    
    def test_list_round_trip(self):
        """List round-trips correctly."""
        markdown = '- Item 1\n- Item 2\n- Item 3'
        
        label = MarkdownLabel(text=markdown)
        ast1 = self._normalize_ast(label.get_ast())
        
        serialized = label.to_markdown()
        
        label2 = MarkdownLabel(text=serialized)
        ast2 = self._normalize_ast(label2.get_ast())
        
        assert ast1 == ast2, \
            f"AST mismatch after round-trip:\nOriginal: {ast1}\nAfter: {ast2}"
    
    def test_ordered_list_round_trip(self):
        """Ordered list round-trips correctly."""
        markdown = '1. First\n2. Second\n3. Third'
        
        label = MarkdownLabel(text=markdown)
        ast1 = self._normalize_ast(label.get_ast())
        
        serialized = label.to_markdown()
        
        label2 = MarkdownLabel(text=serialized)
        ast2 = self._normalize_ast(label2.get_ast())
        
        assert ast1 == ast2, \
            f"AST mismatch after round-trip:\nOriginal: {ast1}\nAfter: {ast2}"
    
    def test_block_quote_round_trip(self):
        """Block quote round-trips correctly."""
        markdown = '> This is a quote'
        
        label = MarkdownLabel(text=markdown)
        ast1 = self._normalize_ast(label.get_ast())
        
        serialized = label.to_markdown()
        
        label2 = MarkdownLabel(text=serialized)
        ast2 = self._normalize_ast(label2.get_ast())
        
        assert ast1 == ast2, \
            f"AST mismatch after round-trip:\nOriginal: {ast1}\nAfter: {ast2}"
    
    def test_thematic_break_round_trip(self):
        """Thematic break round-trips correctly."""
        markdown = 'Before\n\n---\n\nAfter'
        
        label = MarkdownLabel(text=markdown)
        ast1 = self._normalize_ast(label.get_ast())
        
        serialized = label.to_markdown()
        
        label2 = MarkdownLabel(text=serialized)
        ast2 = self._normalize_ast(label2.get_ast())
        
        assert ast1 == ast2, \
            f"AST mismatch after round-trip:\nOriginal: {ast1}\nAfter: {ast2}"
    
    def test_table_round_trip(self):
        """Table round-trips correctly."""
        markdown = '| A | B |\n| --- | --- |\n| 1 | 2 |'
        
        label = MarkdownLabel(text=markdown)
        ast1 = self._normalize_ast(label.get_ast())
        
        serialized = label.to_markdown()
        
        label2 = MarkdownLabel(text=serialized)
        ast2 = self._normalize_ast(label2.get_ast())
        
        assert ast1 == ast2, \
            f"AST mismatch after round-trip:\nOriginal: {ast1}\nAfter: {ast2}"