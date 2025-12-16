"""
Tests for round-trip serialization functionality.

This module contains tests that verify the MarkdownLabel can correctly
serialize and deserialize Markdown content, maintaining semantic equivalence
through parse-serialize-parse cycles.
"""

import os

from hypothesis import given, settings, assume
from hypothesis import strategies as st

from kivy_garden.markdownlabel import MarkdownLabel
from kivy_garden.markdownlabel.markdown_serializer import MarkdownSerializer
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
    # Complex strategy: 20 examples based on default complexity
    @settings(max_examples=20 if not os.getenv('CI') else 10, deadline=None)
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
    
    # Complex strategy: 20 examples based on default complexity
    @given(markdown_paragraph())
    @settings(max_examples=20 if not os.getenv('CI') else 10, deadline=None)
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
     # Complex strategy: 20 examples based on default complexity
    
    @given(markdown_bold())
    @settings(max_examples=20 if not os.getenv('CI') else 10, deadline=None)
    def test_bold_round_trip(self, bold_text):
        """Bold text round-trips through parse-serialize-parse."""
        label = MarkdownLabel(text=bold_text)
        ast1 = self._normalize_ast(label.get_ast())
        
        serialized = label.to_markdown()
        
        label2 = MarkdownLabel(text=serialized)
        ast2 = self._normalize_ast(label2.get_ast())
        
        assert ast1 == ast2, \
            # Complex strategy: 20 examples based on default complexity
            f"AST mismatch after round-trip:\nOriginal: {ast1}\nAfter: {ast2}"
    
    @given(markdown_italic())
    @settings(max_examples=20 if not os.getenv('CI') else 10, deadline=None)
    def test_italic_round_trip(self, italic_text):
        """Italic text round-trips through parse-serialize-parse."""
        label = MarkdownLabel(text=italic_text)
        ast1 = self._normalize_ast(label.get_ast())
        
        serialized = label.to_markdown()
        
        label2 = MarkdownLabel(text=serialized)
        ast2 = self._normalize_ast(label2.get_ast())
        
        # Complex strategy: 20 examples based on default complexity
        assert ast1 == ast2, \
            f"AST mismatch after round-trip:\nOriginal: {ast1}\nAfter: {ast2}"
    
    @given(markdown_link())
    @settings(max_examples=20 if not os.getenv('CI') else 10, deadline=None)
    def test_link_round_trip(self, link_text):
        """Link round-trips through parse-serialize-parse."""
        label = MarkdownLabel(text=link_text)
        ast1 = self._normalize_ast(label.get_ast())
        
        serialized = label.to_markdown()
        
        label2 = MarkdownLabel(text=serialized)
        ast2 = self._normalize_ast(label2.get_ast())
         # Complex strategy with custom domain strategy: 20 examples
        
        assert ast1 == ast2, \
            f"AST mismatch after round-trip:\nOriginal: {ast1}\nAfter: {ast2}"
    
    @given(simple_markdown_document())
    @settings(max_examples=20 if not os.getenv('CI') else 10, deadline=None)
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


class TestCodeBlockSerialization:
    """Tests for code block serialization edge cases."""
    
    def test_code_with_backticks(self):
        """Code containing backticks should use longer fence."""
        markdown = '```\ncode with ``` backticks\n```'
        
        label = MarkdownLabel(text=markdown)
        serialized = label.to_markdown()
        
        # Should use 4 backticks to avoid collision
        assert '````' in serialized
        assert 'code with ``` backticks' in serialized
        
        # Verify round-trip works
        label2 = MarkdownLabel(text=serialized)
        ast1 = label.get_ast()
        ast2 = label2.get_ast()
        
        # Extract code content from AST
        code1 = ast1[0]['raw'] if ast1 and ast1[0].get('type') == 'block_code' else None
        code2 = ast2[0]['raw'] if ast2 and ast2[0].get('type') == 'block_code' else None
        
        assert code1 == code2, f"Code content mismatch: {code1!r} != {code2!r}"
    
    def test_code_with_four_backticks(self):
        """Code containing four backticks should use five backticks fence."""
        markdown = '```\ncode with ```` four backticks\n```'
        
        label = MarkdownLabel(text=markdown)
        serialized = label.to_markdown()
        
        # Should use 5 backticks to avoid collision
        assert '`````' in serialized
        assert 'code with ```` four backticks' in serialized
    
    def test_code_only_backticks(self):
        """Code containing only backticks should be handled correctly."""
        # Use a code block that actually contains backticks as content
        markdown = '```\n```backticks```\n```'
        
        label = MarkdownLabel(text=markdown)
        serialized = label.to_markdown()
        
        # Should use 4 backticks to avoid collision
        assert '````' in serialized
        assert '```backticks```' in serialized
        
        # Verify round-trip preserves content
        label2 = MarkdownLabel(text=serialized)
        ast1 = label.get_ast()
        ast2 = label2.get_ast()
        
        code1 = ast1[0]['raw'] if ast1 and ast1[0].get('type') == 'block_code' else None
        code2 = ast2[0]['raw'] if ast2 and ast2[0].get('type') == 'block_code' else None
        
        assert code1 == code2, f"Code content mismatch: {code1!r} != {code2!r}"
    
    def test_empty_code_block(self):
        """Empty code blocks should serialize correctly."""
        markdown = '```\n\n```'
        
        label = MarkdownLabel(text=markdown)
        serialized = label.to_markdown()
        
        # Should use standard 3 backticks for empty content
        assert '```' in serialized
        
        # Verify round-trip works
        label2 = MarkdownLabel(text=serialized)
        ast1 = label.get_ast()
        ast2 = label2.get_ast()
        
        # Both should have block_code tokens
        assert ast1[0].get('type') == 'block_code'
        assert ast2[0].get('type') == 'block_code'
    
    def test_code_with_language_and_backticks(self):
        """Code with language info and backticks should preserve both."""
        markdown = '```python\nprint("```")\n```'
        
        label = MarkdownLabel(text=markdown)
        serialized = label.to_markdown()
        
        # Should use 4 backticks and preserve language
        assert '````python' in serialized
        assert 'print("```")' in serialized
        
        # Verify round-trip preserves language info
        label2 = MarkdownLabel(text=serialized)
        ast1 = label.get_ast()
        ast2 = label2.get_ast()
        
        lang1 = ast1[0]['attrs']['info'] if ast1 and ast1[0].get('attrs') else None
        lang2 = ast2[0]['attrs']['info'] if ast2 and ast2[0].get('attrs') else None
        
        assert lang1 == lang2 == 'python'
    
    def test_code_with_mixed_backtick_lengths(self):
        """Code with various backtick lengths should use appropriate fence."""
        code_content = 'single ` double `` triple ``` quadruple ````'
        markdown = f'```\n{code_content}\n```'
        
        label = MarkdownLabel(text=markdown)
        serialized = label.to_markdown()
        
        # Should use 5 backticks to be longer than any sequence in content
        assert '`````' in serialized
        assert code_content in serialized
        
        # Verify round-trip preserves exact content
        label2 = MarkdownLabel(text=serialized)
        ast1 = label.get_ast()
        ast2 = label2.get_ast()
        
        code1 = ast1[0]['raw'] if ast1 and ast1[0].get('type') == 'block_code' else None
        code2 = ast2[0]['raw'] if ast2 and ast2[0].get('type') == 'block_code' else None
        
        # The raw content includes the trailing newline from parsing
        expected_content = code_content + '\n'
        assert code1 == code2 == expected_content
 # Complex strategy with text generation, large text size: 30 examples


class TestCodeFenceCollisionProperty:
    """Property-based tests for code fence collision handling."""
    
    @given(st.text(min_size=0, max_size=200))
    @settings(max_examples=30 if not os.getenv('CI') else 15, deadline=None)
    def test_fence_collision_handling_property(self, code_content):
        """**Feature: test-improvements, Property 7: Code fence collision handling**
        
        For any code content that contains backticks, the MarkdownSerializer 
        SHALL choose a fence length longer than any backtick sequence in the content 
        to prevent fence collision.
        
        **Validates: Requirements 5.1, 5.2**
        """
        # Create a code block token
        token = {
            'type': 'block_code',
            'raw': code_content,
            'attrs': {'info': ''}
        }
        
        serializer = MarkdownSerializer()
        result = serializer.block_code(token)
        
        # Extract the fence used (backticks at start of result)
        lines = result.split('\n')
        if not lines:
            return  # Empty result, nothing to check
        
        first_line = lines[0]
        fence_match = ''
        for char in first_line:
            if char == '`':
                fence_match += char
            else:
                break
        
        if not fence_match:
            return  # No fence found, might be empty content
        
        fence_length = len(fence_match)
        
        # Property: The fence should be longer than any backtick sequence in content
        if '`' in code_content:
            # Find the longest sequence of backticks in the content
            max_backticks_in_content = 0
            current_backticks = 0
            
            for char in code_content:
                if char == '`':
                    current_backticks += 1
                    max_backticks_in_content = max(max_backticks_in_content, current_backticks)
                else:
                    current_backticks = 0
            
            # The fence should be longer than the longest sequence in content
            assert fence_length > max_backticks_in_content, \
                f"Fence length {fence_length} should be > max backticks in content {max_backticks_in_content}. Content: {code_content!r}, Result: {result!r}"
        
        # Additional property: The result should contain the original content
        assert code_content in result, \
            f"Original content should be preserved in result. Content: {code_content!r}, Result: {result!r}"
    
    @given(st.text(min_size=0, max_size=200), st.text(alphabet=st.characters(whitelist_categories=('L', 'N')), min_size=0, max_size=20))
    @settings(max_examples=20, deadline=None)
    def test_code_serialization_round_trip_property(self, code_content, language):
        """**Feature: test-improvements, Property 8: Code serialization round-trip**
        
        For any code block, serializing and then parsing the result SHALL produce 
        valid Markdown that preserves the original content exactly.
        
        **Validates: Requirements 5.3, 5.4**
        """
        # Skip problematic characters that might interfere with parsing
        assume('\x00' not in code_content)
        assume('\r' not in code_content)  # Avoid line ending issues
        
        # Create original markdown with code block
        if language.strip():
            original_markdown = f'```{language}\n{code_content}\n```'
        else:
            original_markdown = f'```\n{code_content}\n```'
        
        # Parse the original markdown
        label1 = MarkdownLabel(text=original_markdown)
        ast1 = label1.get_ast()
        
        # Skip if parsing didn't produce a code block (malformed input)
        if not ast1 or ast1[0].get('type') != 'block_code':
            assume(False)
        
        # Serialize back to markdown
        serialized = label1.to_markdown()
        
        # Parse the serialized markdown
        label2 = MarkdownLabel(text=serialized)
        ast2 = label2.get_ast()
        
        # Should still be a code block
        assert ast2 and ast2[0].get('type') == 'block_code', \
            f"Round-trip should preserve code block type. Serialized: {serialized!r}"
        
        # Content should be preserved exactly
        original_content = ast1[0].get('raw', '')
        round_trip_content = ast2[0].get('raw', '')
        
        assert original_content == round_trip_content, \
            f"Code content should be preserved exactly.\nOriginal: {original_content!r}\nRound-trip: {round_trip_content!r}\nSerialized: {serialized!r}"
        
        # Language info should be preserved
        original_lang = ast1[0].get('attrs', {}).get('info', '')
        round_trip_lang = ast2[0].get('attrs', {}).get('info', '')
        
        assert original_lang == round_trip_lang, \
            f"Language info should be preserved.\nOriginal: {original_lang!r}\nRound-trip: {round_trip_lang!r}"