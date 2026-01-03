
from kivy_garden.markdownlabel.inline_renderer import InlineRenderer
from kivy_garden.markdownlabel.markdown_serializer import MarkdownSerializer
from kivy_garden.markdownlabel.kivy_renderer import KivyRenderer
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget


class TestInlineRendererCoverage:
    def test_unknown_token_type(self):
        renderer = InlineRenderer()
        # Mock token with unknown type
        token = {'type': 'unknown_weird_type', 'raw': 'some text [b]'}
        # Should fallback to _unknown which escapes raw text
        result = renderer.render([token])
        assert result == 'some text &bl;b&br;'

        # Test direct _unknown call
        assert renderer._unknown(token) == 'some text &bl;b&br;'

    def test_image_rendering(self):
        renderer = InlineRenderer()
        # Image in inline context renders children (alt text)
        token = {
            'type': 'image',
            'children': [{'type': 'text', 'raw': 'alt text'}],
            'attrs': {'url': 'http://example.com/img.png'}
        }
        result = renderer.image(token)
        # Should render alt text
        assert result == 'alt text'

    def test_escape_markup_edge_cases(self):
        renderer = InlineRenderer()
        # Test basic escaping
        assert renderer._escape_markup('[b]') == '&bl;b&br;'
        # Test nothing to escape
        assert renderer._escape_markup('plain') == 'plain'


class TestMarkdownSerializerCoverage:
    def test_serialize_unknown_token(self):
        serializer = MarkdownSerializer()
        # Token with unknown type
        token = {'type': 'unknown_thing', 'raw': 'content'}
        # _serialize_token returns '' for unknown
        assert serializer._serialize_token(token) == ''

    def test_serialize_inline_unknown(self):
        serializer = MarkdownSerializer()
        # Inline token with unknown type
        token = {'type': 'weird_inline', 'raw': 'content'}
        # serialize_inline falls back to raw
        assert serializer.serialize_inline([token]) == 'content'

    def test_blank_line(self):
        serializer = MarkdownSerializer()
        token = {'type': 'blank_line'}
        assert serializer.blank_line(token) is None

    def test_table_edge_cases(self):
        serializer = MarkdownSerializer()
        # Table with empty children
        token = {'type': 'table', 'children': []}
        assert serializer.table(token) == ''

    def test_serialize_list_item_unknown_child(self):
        serializer = MarkdownSerializer()
        # List item with unknown child type
        item_token = {
            'type': 'list_item',
            'children': [{'type': 'unknown_block', 'raw': 'ignore me'}]
        }
        # It calls _serialize_token which returns '' so result is empty string
        assert serializer._serialize_list_item(item_token) == ''

    def test_serialize_list_item_known_child_returns_empty(self):
        serializer = MarkdownSerializer()
        # List item with a child that serializes to empty (e.g. blank_line)
        item_token = {
            'type': 'list_item',
            'children': [{'type': 'blank_line'}]
        }
        assert serializer._serialize_list_item(item_token) == ''

    def test_block_code_no_newline(self):
        serializer = MarkdownSerializer()
        token = {'type': 'block_code', 'raw': 'code without newline'}
        result = serializer.block_code(token)
        assert result == '```\ncode without newline\n```'

    def test_block_code_with_newline(self):
        serializer = MarkdownSerializer()
        token = {'type': 'block_code', 'raw': 'code with newline\n'}
        result = serializer.block_code(token)
        assert result == '```\ncode with newline\n```'


class TestKivyRendererCoverage:
    def test_deep_nesting_truncation(self):
        renderer = KivyRenderer()
        # Mock a token structure that exceeds max depth (10)
        # We can just manually set the depth to simulate deep recursion
        renderer._nesting_depth = 11

        # Try to render something
        token = {'type': 'paragraph', 'children': []}
        result = renderer._render_token(token)

        # Should return placeholder
        assert result is not None
        assert isinstance(result, Label)
        assert result.text == '[...content truncated due to deep nesting...]'

    def test_unknown_token_render(self):
        renderer = KivyRenderer()
        token = {'type': 'unknown_thing'}
        # Should result in None
        assert renderer._render_token(token) is None

    def test_list_item_direct_call(self):
        renderer = KivyRenderer()
        # Wrap in paragraph for this test to be sure we get content
        token_para = {
            'type': 'list_item',
            'children': [{
                'type': 'paragraph',
                'children': [{'type': 'text', 'raw': 'item'}]
            }]
        }
        widget = renderer.list_item(token_para)
        assert isinstance(widget, BoxLayout)
        assert len(widget.children) > 0

    def test_list_item_text_token(self):
        # If we just have text, it might be skipped if no method handles 'text'
        # KivyRenderer has 'paragraph', 'block_text', etc.
        # Let's check 'block_text'
        renderer = KivyRenderer()
        token = {'type': 'block_text', 'children': [{'type': 'text', 'raw': 'item'}]}
        widget = renderer.block_text(token)
        assert isinstance(widget, Label)
        assert widget.text == 'item'

    def test_text_size_binding_strict_mode(self):
        # strict_label_mode=True
        renderer = KivyRenderer(strict_label_mode=True, text_size=[None, None])
        label = Label()
        renderer._apply_text_size_binding(label)
        # No binding should be properly applied
        assert label.text_size == [None, None] or label.text_size == (None, None)

    def test_text_size_binding_height_only(self):
        renderer = KivyRenderer(text_size=[None, 100])
        label = Label(width=200)
        renderer._apply_text_size_binding(label)
        # Should bind width to label width, height to 100
        # Trigger width change to see effect if needed, but initial assignment happens
        assert label.text_size[1] == 100

    def test_blank_line(self):
        renderer = KivyRenderer()
        token = {'type': 'blank_line'}
        widget = renderer.blank_line(token)
        assert isinstance(widget, Widget)
        assert widget.height == renderer.base_font_size
