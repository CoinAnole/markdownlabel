import pytest


def test_markdown_label_import():
    """Test that MarkdownLabel can be imported."""
    from kivy_garden.markdown_label import MarkdownLabel
    label = MarkdownLabel()
    assert hasattr(label, 'text')


def test_markdown_label_text_property():
    """Test that MarkdownLabel has a text property."""
    from kivy_garden.markdown_label import MarkdownLabel
    label = MarkdownLabel(text='# Hello')
    assert label.text == '# Hello'
