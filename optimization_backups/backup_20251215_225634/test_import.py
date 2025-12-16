import pytest


def test_markdownlabel_import():
    """Test that MarkdownLabel can be imported."""
    from kivy_garden.markdownlabel import MarkdownLabel
    label = MarkdownLabel()
    assert hasattr(label, 'text')


def test_markdownlabel_text_property():
    """Test that MarkdownLabel has a text property."""
    from kivy_garden.markdownlabel import MarkdownLabel
    label = MarkdownLabel(text='# Hello')
    assert label.text == '# Hello'
