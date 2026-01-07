"""
Tests for MarkdownLabel import functionality.

This module contains tests for verifying that MarkdownLabel can be imported
and has the expected basic properties available.
"""


import pytest


class TestMarkdownLabelImport:
    """Tests for MarkdownLabel import functionality."""

    @pytest.mark.unit
    def test_markdownlabel_import(self):
        """Test that MarkdownLabel can be imported."""
        from kivy_garden.markdownlabel import MarkdownLabel
        label = MarkdownLabel()
        assert hasattr(label, 'text')

    @pytest.mark.unit
    def test_markdownlabel_text_property(self):
        """Test that MarkdownLabel has a text property."""
        from kivy_garden.markdownlabel import MarkdownLabel
        label = MarkdownLabel(text='# Hello')
        assert label.text == '# Hello'
