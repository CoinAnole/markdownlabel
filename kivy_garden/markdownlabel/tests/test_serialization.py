"""
Tests for round-trip serialization functionality.

This module contains tests that verify the MarkdownLabel can correctly
serialize and deserialize Markdown content, maintaining semantic equivalence
through parse-serialize-parse cycles.
"""

import pytest
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


class TestMarkdownRoundTripSerialization:
    """Property tests for round-trip serialization."""

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

            # Convert softbreak to space for round-trip comparison
            if token.get('type') == 'softbreak':
                normalized.append({'type': 'text', 'raw': ' '})
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

    @pytest.mark.property
    @given(markdown_heading())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
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

    @pytest.mark.property
    @given(markdown_paragraph())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
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

    @pytest.mark.property
    @given(markdown_bold())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_bold_round_trip(self, bold_text):
        """Bold text round-trips through parse-serialize-parse."""
        label = MarkdownLabel(text=bold_text)
        ast1 = self._normalize_ast(label.get_ast())

        serialized = label.to_markdown()

        label2 = MarkdownLabel(text=serialized)
        ast2 = self._normalize_ast(label2.get_ast())

        assert ast1 == ast2, \
            f"AST mismatch after round-trip:\nOriginal: {ast1}\nAfter: {ast2}"

    @pytest.mark.property
    @given(markdown_italic())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_italic_round_trip(self, italic_text):
        """Italic text round-trips through parse-serialize-parse."""
        label = MarkdownLabel(text=italic_text)
        ast1 = self._normalize_ast(label.get_ast())

        serialized = label.to_markdown()

        label2 = MarkdownLabel(text=serialized)
        ast2 = self._normalize_ast(label2.get_ast())

        assert ast1 == ast2, \
            f"AST mismatch after round-trip:\nOriginal: {ast1}\nAfter: {ast2}"

    @pytest.mark.property
    @given(markdown_link())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_link_round_trip(self, link_text):
        """Link round-trips through parse-serialize-parse."""
        label = MarkdownLabel(text=link_text)
        ast1 = self._normalize_ast(label.get_ast())

        serialized = label.to_markdown()

        label2 = MarkdownLabel(text=serialized)
        ast2 = self._normalize_ast(label2.get_ast())

        assert ast1 == ast2, \
            f"AST mismatch after round-trip:\nOriginal: {ast1}\nAfter: {ast2}"

    @pytest.mark.property
    @given(simple_markdown_document())
    # Mixed finite/complex strategy: 20 examples (10 finite × 2 complex samples)
    @settings(max_examples=20, deadline=None)
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

    @pytest.mark.unit
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

    @pytest.mark.unit
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

    @pytest.mark.unit
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

    @pytest.mark.unit
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

    @pytest.mark.unit
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

    @pytest.mark.unit
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

    @pytest.mark.unit
    def test_table_alignment_round_trip(self):
        """Table with alignment round-trips correctly."""
        markdown = '| Left | Center | Right |\n| :--- | :---: | ---: |\n| 1 | 2 | 3 |'

        label = MarkdownLabel(text=markdown)
        ast1 = self._normalize_ast(label.get_ast())

        serialized = label.to_markdown()

        # Verify markers are present in serialized output
        assert ':---' in serialized
        assert ':---:' in serialized
        assert '---:' in serialized

        label2 = MarkdownLabel(text=serialized)
        ast2 = self._normalize_ast(label2.get_ast())

        assert ast1 == ast2, \
            f"AST mismatch after round-trip:\nOriginal: {ast1}\nAfter: {ast2}"

    @pytest.mark.unit
    def test_inline_code_serialization(self):
        """Inline code serialization."""
        markdown = 'Text with `code` included.'

        label = MarkdownLabel(text=markdown)
        ast1 = self._normalize_ast(label.get_ast())

        serialized = label.to_markdown()
        assert '`code`' in serialized

        label2 = MarkdownLabel(text=serialized)
        ast2 = self._normalize_ast(label2.get_ast())

        assert ast1 == ast2

    @pytest.mark.unit
    def test_strikethrough_serialization(self):
        """Strikethrough serialization."""
        markdown = 'Text with ~~strikethrough~~ included.'

        label = MarkdownLabel(text=markdown)
        ast1 = self._normalize_ast(label.get_ast())

        serialized = label.to_markdown()
        assert '~~strikethrough~~' in serialized

        label2 = MarkdownLabel(text=serialized)
        ast2 = self._normalize_ast(label2.get_ast())

        assert ast1 == ast2

    @pytest.mark.unit
    def test_image_serialization(self):
        """Image serialization."""
        markdown = '![Alt text](http://example.com/image.png)'

        label = MarkdownLabel(text=markdown)
        ast1 = self._normalize_ast(label.get_ast())

        serialized = label.to_markdown()
        assert '![Alt text](http://example.com/image.png)' in serialized

        label2 = MarkdownLabel(text=serialized)
        ast2 = self._normalize_ast(label2.get_ast())

        assert ast1 == ast2

    @pytest.mark.unit
    def test_softbreak_serialization(self):
        """Softbreak serialization."""
        # A parseable softbreak usually requires a newline in the input that doesn't trigger a paragraph break
        markdown = 'Line 1\nLine 2'

        label = MarkdownLabel(text=markdown)
        ast1 = self._normalize_ast(label.get_ast())

        serialized = label.to_markdown()

        # Softbreak is typically serialized as a space or newline depending on implementation;
        # serializer implementation shows it returns ' '
        # Original input 'Line 1\nLine 2' parses to text 'Line 1', softbreak, text 'Line 2'

        label2 = MarkdownLabel(text=serialized)
        ast2 = self._normalize_ast(label2.get_ast())

        # Note: mistune might normalize softbreaks, so exact round trip of whitespace
        # isn't always guaranteed, but semantic content should match.
        # Check if ASTs are equivalent structure-wise
        assert ast1 == ast2

    @pytest.mark.unit
    def test_hard_linebreak_serialization(self):
        """Hard linebreak serialization."""
        # Hard linebreak is two spaces at end of line
        markdown = 'Line 1  \nLine 2'

        label = MarkdownLabel(text=markdown)
        ast1 = self._normalize_ast(label.get_ast())

        serialized = label.to_markdown()
        assert '  \n' in serialized or '\\\n' in serialized  # Check for standard hard break indicators

        label2 = MarkdownLabel(text=serialized)
        ast2 = self._normalize_ast(label2.get_ast())

        assert ast1 == ast2


class TestCodeBlockSerialization:
    """Tests for code block serialization edge cases."""

    @pytest.mark.unit
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

    @pytest.mark.unit
    def test_code_with_four_backticks(self):
        """Code containing four backticks should use five backticks fence."""
        markdown = '```\ncode with ```` four backticks\n```'

        label = MarkdownLabel(text=markdown)
        serialized = label.to_markdown()

        # Should use 5 backticks to avoid collision
        assert '`````' in serialized
        assert 'code with ```` four backticks' in serialized

    @pytest.mark.unit
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

    @pytest.mark.unit
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

    @pytest.mark.unit
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

    @pytest.mark.unit
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


class TestCodeFenceCollisionProperty:
    """Property-based tests for code fence collision handling."""

    @pytest.mark.property
    @given(st.text(min_size=0, max_size=200))
    # Complex strategy: 30 examples (adequate coverage)
    @settings(max_examples=30, deadline=None)
    def test_fence_collision_handling_property(self, code_content):
        """**Feature: test-improvements, Code fence collision handling**

        For any code content that contains backticks, the MarkdownSerializer
        SHALL choose a fence length longer than any backtick sequence in the content
        to prevent fence collision.

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
            assert fence_length > max_backticks_in_content, (
                f"Fence length {fence_length} should be > max backticks in "
                f"content {max_backticks_in_content}. Content: {code_content!r}, "
                f"Result: {result!r}"
            )

        # Additional property: The result should contain the original content
        assert code_content in result, \
            f"Original content should be preserved in result. Content: {code_content!r}, Result: {result!r}"

    @pytest.mark.property
    @given(
        st.text(min_size=0, max_size=200),
        st.text(
            alphabet=st.characters(whitelist_categories=('L', 'N')),
            min_size=0,
            max_size=20
        )
    )
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_code_serialization_round_trip_property(self, code_content, language):
        """**Feature: test-improvements, Code serialization round-trip**

        For any code block, serializing and then parsing the result SHALL produce
        valid Markdown that preserves the original content exactly.

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

        assert original_content == round_trip_content, (
            f"Code content should be preserved exactly.\n"
            f"Original: {original_content!r}\n"
            f"Round-trip: {round_trip_content!r}\n"
            f"Serialized: {serialized!r}"
        )

        # Language info should be preserved
        original_lang = ast1[0].get('attrs', {}).get('info', '')
        round_trip_lang = ast2[0].get('attrs', {}).get('info', '')

        assert original_lang == round_trip_lang, (
            f"Language info should be preserved.\n"
            f"Original: {original_lang!r}\n"
            f"Round-trip: {round_trip_lang!r}"
        )


class TestMarkdownSerializerEdgeCases:
    """Tests for MarkdownSerializer edge cases and coverage."""

    @pytest.mark.unit
    def test_serialize_unknown_token(self):
        """Test that unknown token types return empty string."""
        serializer = MarkdownSerializer()
        # Token with unknown type
        token = {'type': 'unknown_thing', 'raw': 'content'}
        # Edge case: Testing unknown token handling requires direct call since
        # mistune parser never produces unknown token types
        assert serializer._serialize_token(token) == ''

    @pytest.mark.unit
    def test_serialize_inline_unknown(self):
        """Test that unknown inline tokens fall back to raw content."""
        serializer = MarkdownSerializer()
        # Inline token with unknown type
        token = {'type': 'weird_inline', 'raw': 'content'}
        # serialize_inline falls back to raw
        assert serializer.serialize_inline([token]) == 'content'

    @pytest.mark.unit
    def test_blank_line(self):
        """Test that blank_line tokens return None."""
        serializer = MarkdownSerializer()
        token = {'type': 'blank_line'}
        assert serializer.blank_line(token) is None

    @pytest.mark.unit
    def test_table_edge_cases(self):
        """Test table serialization with empty children."""
        serializer = MarkdownSerializer()
        # Table with empty children
        token = {'type': 'table', 'children': []}
        assert serializer.table(token) == ''

    @pytest.mark.unit
    def test_serialize_list_item_unknown_child(self):
        """Test list item serialization with unknown child type."""
        serializer = MarkdownSerializer()
        # List item with unknown child type
        item_token = {
            'type': 'list_item',
            'children': [{'type': 'unknown_block', 'raw': 'ignore me'}]
        }
        # Edge case: Testing list item with unknown children requires direct call
        # because such tokens are not naturally produced by the parser
        assert serializer._serialize_list_item(item_token) == ''

    @pytest.mark.unit
    def test_serialize_list_item_known_child_returns_empty(self):
        """Test list item serialization with child that serializes to empty."""
        serializer = MarkdownSerializer()
        # List item with a child that serializes to empty (e.g. blank_line)
        item_token = {
            'type': 'list_item',
            'children': [{'type': 'blank_line'}]
        }
        # Edge case: Testing list item empty serialization requires direct call
        # since blank_line inner tokens are typically handled at block level
        assert serializer._serialize_list_item(item_token) == ''

    @pytest.mark.unit
    def test_block_code_no_newline(self):
        """Test block code serialization without trailing newline."""
        serializer = MarkdownSerializer()
        token = {'type': 'block_code', 'raw': 'code without newline'}
        result = serializer.block_code(token)
        assert result == '```\ncode without newline\n```'

    @pytest.mark.unit
    def test_block_code_with_newline(self):
        """Test block code serialization with trailing newline."""
        serializer = MarkdownSerializer()
        token = {'type': 'block_code', 'raw': 'code with newline\n'}
        result = serializer.block_code(token)
        assert result == '```\ncode with newline\n```'


class TestReferenceStyleLinkSerialization:
    """Tests for reference-style link serialization."""

    @pytest.mark.unit
    def test_basic_reference_style_link_serialization(self):
        """Basic reference-style link serializes to [text][label] format with definition."""
        markdown = '''Click [here][1] for info.

[1]: http://example.com/'''

        label = MarkdownLabel(text=markdown)
        serialized = label.to_markdown()

        # Should contain reference-style link format
        assert '[here][1]' in serialized
        # Should contain definition at end
        assert '[1]: http://example.com/' in serialized

    @pytest.mark.unit
    def test_implicit_reference_style_link_serialization(self):
        """Implicit reference-style link ([Google][]) serializes correctly."""
        markdown = '''Visit [Google][] for search.

[Google]: http://google.com/'''

        label = MarkdownLabel(text=markdown)
        serialized = label.to_markdown()

        # Should contain reference-style link format with label
        assert '[Google][Google]' in serialized
        # Should contain definition at end
        assert '[Google]: http://google.com/' in serialized

    @pytest.mark.unit
    def test_reference_style_link_with_title_serialization(self):
        """Reference-style link with title includes title in definition."""
        markdown = '''Visit [Google][] for search.

[Google]: http://google.com/ "Search Engine"'''

        label = MarkdownLabel(text=markdown)
        serialized = label.to_markdown()

        # Should contain reference-style link format
        assert '[Google][Google]' in serialized
        # Should contain definition with title
        assert '[Google]: http://google.com/ "Search Engine"' in serialized

    @pytest.mark.unit
    def test_mixed_inline_and_reference_style_links(self):
        """Mixed inline and reference-style links serialize correctly."""
        markdown = '''Click [here][1] or [inline](http://inline.com/).

[1]: http://example.com/'''

        label = MarkdownLabel(text=markdown)
        serialized = label.to_markdown()

        # Should contain reference-style link
        assert '[here][1]' in serialized
        # Should contain inline link
        assert '[inline](http://inline.com/)' in serialized
        # Should contain definition
        assert '[1]: http://example.com/' in serialized

    @pytest.mark.unit
    def test_multiple_reference_style_links_same_label(self):
        """Multiple links with same label produce single definition."""
        markdown = '''Click [here][1] and [there][1] for info.

[1]: http://example.com/'''

        label = MarkdownLabel(text=markdown)
        serialized = label.to_markdown()

        # Should contain both links
        assert '[here][1]' in serialized
        assert '[there][1]' in serialized
        # Should contain only one definition
        assert serialized.count('[1]: http://example.com/') == 1

    @pytest.mark.unit
    def test_reference_style_link_round_trip(self):
        """Reference-style link round-trips correctly."""
        markdown = '''Click [here][1] for info.

[1]: http://example.com/'''

        label = MarkdownLabel(text=markdown)
        ast1 = label.get_ast()

        serialized = label.to_markdown()

        label2 = MarkdownLabel(text=serialized)
        ast2 = label2.get_ast()

        # Both should have link tokens with same URL
        link1 = ast1[0]['children'][1]
        link2 = ast2[0]['children'][1]

        assert link1['attrs']['url'] == link2['attrs']['url']
        assert link1['children'][0]['raw'] == link2['children'][0]['raw']

    @pytest.mark.property
    @given(
        label=st.text(min_size=1, max_size=10, alphabet=st.characters(
            whitelist_categories=['L', 'N'],
            blacklist_characters='[]()&\n\r'
        )),
        link_text1=st.text(min_size=1, max_size=20, alphabet=st.characters(
            whitelist_categories=['L', 'N'],
            blacklist_characters='[]()&\n\r'
        )),
        link_text2=st.text(min_size=1, max_size=20, alphabet=st.characters(
            whitelist_categories=['L', 'N'],
            blacklist_characters='[]()&\n\r'
        )),
        num_links=st.integers(min_value=2, max_value=5)
    )
    # Complex strategy: 50 examples (adequate coverage for property test)
    @settings(max_examples=50, deadline=None)
    def test_property_duplicate_labels_single_definition(
        self, label, link_text1, link_text2, num_links
    ):
        """**Property 4: Duplicate Labels Produce Single Definition**

        *For any* document with multiple links sharing the same label,
        serialization SHALL output exactly one definition for that label.

        **Validates: Requirements 3.2**
        """
        assume(len(label.strip()) > 0)
        assume(len(link_text1.strip()) > 0)
        assume(len(link_text2.strip()) > 0)

        # Build markdown with multiple links using the same label
        link_texts = [link_text1, link_text2]
        for i in range(num_links - 2):
            link_texts.append(f"link{i}")

        links = ' and '.join(f'[{text}][{label}]' for text in link_texts)
        markdown = f'''{links}

[{label}]: http://example.com/'''

        md_label = MarkdownLabel(text=markdown)
        serialized = md_label.to_markdown()

        # Property: Only one definition should exist for the label
        definition_pattern = f'[{label}]: http://example.com/'
        definition_count = serialized.count(definition_pattern)

        assert definition_count == 1, (
            f"Expected exactly 1 definition for label '{label}', "
            f"but found {definition_count}.\n"
            f"Input markdown:\n{markdown}\n"
            f"Serialized output:\n{serialized}"
        )

        # Additional verification: all link references should be preserved
        for text in link_texts:
            assert f'[{text}][{label}]' in serialized, (
                f"Link reference '[{text}][{label}]' not found in serialized output.\n"
                f"Serialized output:\n{serialized}"
            )
