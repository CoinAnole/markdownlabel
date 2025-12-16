"""
Property-based tests for shared test infrastructure.

These tests validate that the shared test utilities and strategies work correctly
and are available for use across all test modules.
"""

import pytest
import os
from hypothesis import given, strategies as st, settings

from kivy_garden.markdownlabel import MarkdownLabel
from kivy_garden.markdownlabel.tests.test_utils import (
    markdown_heading,
    markdown_paragraph,
    markdown_bold,
    markdown_italic,
    markdown_link,
    simple_markdown_document,
    color_strategy,
    text_padding_strategy,
    find_labels_recursive,
    colors_equal,
    padding_equal,
    floats_equal,
    KIVY_FONTS
)


class TestSharedStrategyAvailability:
    """Property tests for shared strategy availability (Property 6)."""
    
    @given(markdown_heading())
    # Complex strategy: 20 examples based on default complexity
    @settings(max_examples=20 if not os.getenv('CI') else 10, deadline=None)
    def test_markdown_heading_strategy_generates_valid_headings(self, heading):
        """**Feature: test-refactoring, Property 6: Shared Strategy Availability**
        *For any* Hypothesis strategy used in multiple modules, that strategy should be 
        importable from the shared utilities module and generate valid test data.
        **Validates: Requirements 3.2**
        """
        # Verify heading format
        assert heading.startswith('#'), f"Heading should start with #: {heading}"
        assert ' ' in heading, f"Heading should have space after #: {heading}"
        
        # Verify it can be used with MarkdownLabel
        label = MarkdownLabel(text=heading)
        assert len(label.children) >= 1, "Heading should produce at least one widget"
    
    # Complex strategy: 20 examples based on default complexity
    @given(markdown_paragraph())
    # Custom strategy: 50 examples for adequate coverage
    @settings(max_examples=50, deadline=None)
    def test_markdown_paragraph_strategy_generates_valid_paragraphs(self, paragraph):
        """Paragraph strategy generates valid paragraph text."""
        assert isinstance(paragraph, str), "Paragraph should be a string"
        assert len(paragraph.strip()) > 0, "Paragraph should not be empty"
        
        # Verify it can be used with MarkdownLabel
        label = MarkdownLabel(text=paragraph)
        assert len(label.children) >= 1, "Paragraph should produce at least one widget"
     # Complex strategy: 20 examples based on default complexity
    
    @given(markdown_bold())
    # Custom strategy: 50 examples for adequate coverage
    @settings(max_examples=50, deadline=None)
    def test_markdown_bold_strategy_generates_valid_bold_text(self, bold_text):
        """Bold text strategy generates valid bold markdown."""
        assert bold_text.startswith('**'), f"Bold text should start with **: {bold_text}"
        assert bold_text.endswith('**'), f"Bold text should end with **: {bold_text}"
        # Complex strategy: 20 examples based on default complexity
        assert len(bold_text) > 4, "Bold text should have content between markers"
    
    @given(markdown_italic())
    # Custom strategy: 50 examples for adequate coverage
    @settings(max_examples=50, deadline=None)
    def test_markdown_italic_strategy_generates_valid_italic_text(self, italic_text):
        """Italic text strategy generates valid italic markdown."""
        assert italic_text.startswith('*'), f"Italic text should start with *: {italic_text}"
        assert italic_text.endswith('*'), f"Italic text should end with *: {italic_text}"
        assert len(italic_text) > 2, "Italic text should have content between markers"
        # Complex strategy: 20 examples based on default complexity
        # Ensure it's not bold (which would start/end with **)
        assert not italic_text.startswith('**'), "Should be italic, not bold"
    
    @given(markdown_link())
    # Custom strategy: 50 examples for adequate coverage
    @settings(max_examples=50, deadline=None)
    def test_markdown_link_strategy_generates_valid_links(self, link):
        """Link strategy generates valid markdown links."""
        assert '[' in link and ']' in link, f"Link should contain brackets: {link}"
        assert '(' in link and ')' in link, f"Link should contain parentheses: {link}"
        assert link.startswith('['), f"Link should start with [: {link}"
        
        # Complex strategy with custom domain strategy: 20 examples
        # Verify it can be used with MarkdownLabel
        label = MarkdownLabel(text=link)
        assert len(label.children) >= 1, "Link should produce at least one widget"
    
    @given(simple_markdown_document())
    # Custom strategy: 50 examples for adequate coverage
    @settings(max_examples=50, deadline=None)
    def test_simple_markdown_document_strategy_generates_valid_documents(self, document):
        """Document strategy generates valid markdown documents."""
        assert isinstance(document, str), "Document should be a string"
        assert len(document.strip()) > 0, "Document should not be empty"
         # Complex strategy: 20 examples based on default complexity
        
        # Verify it can be used with MarkdownLabel
        label = MarkdownLabel(text=document)
        assert len(label.children) >= 1, "Document should produce at least one widget"
    
    @given(color_strategy)
    # Custom strategy: 50 examples for adequate coverage
    @settings(max_examples=50, deadline=None)
    def test_color_strategy_generates_valid_colors(self, color):
        """Color strategy generates valid RGBA color values."""
        assert len(color) == 4, f"Color should have 4 components: {color}"
        for component in color:
            assert 0.0 <= component <= 1.0, f"Color component should be 0-1: {component}"
        
        # Complex strategy: 20 examples based on default complexity
        # Verify it can be used with MarkdownLabel
        label = MarkdownLabel(text="Test", color=color)
        labels = find_labels_recursive(label)
        if labels:  # If there are labels, they should have the color applied
            assert colors_equal(list(labels[0].color), color), "Color should be applied to labels"
    
    @given(text_padding_strategy)
    # Custom strategy: 50 examples for adequate coverage
    @settings(max_examples=50, deadline=None)
    def test_text_padding_strategy_generates_valid_padding(self, padding):
        """Text padding strategy generates valid padding values."""
        assert len(padding) == 4, f"Padding should have 4 components: {padding}"
        for component in padding:
            assert component >= 0.0, f"Padding component should be non-negative: {component}"
        
        # Verify it can be used with MarkdownLabel
        label = MarkdownLabel(text="Test", text_padding=padding)
        labels = find_labels_recursive(label)
        if labels:  # If there are labels, they should have the padding applied
            assert padding_equal(list(labels[0].padding), padding), "Padding should be applied to labels"
    
    def test_kivy_fonts_constant_available(self):
        """KIVY_FONTS constant is available and contains valid font names."""
        assert isinstance(KIVY_FONTS, list), "KIVY_FONTS should be a list"
        assert len(KIVY_FONTS) > 0, "KIVY_FONTS should not be empty"
        
        for font in KIVY_FONTS:
            assert isinstance(font, str), f"Font name should be string: {font}"
            assert len(font) > 0, f"Font name should not be empty: {font}"
        
        # Verify fonts can be used with MarkdownLabel
        label = MarkdownLabel(text="Test", font_name=KIVY_FONTS[0])
        labels = find_labels_recursive(label)
        # Complex strategy with text generation: 30 examples
        if labels:
            assert labels[0].font_name == KIVY_FONTS[0], "Font should be applied to labels"


class TestHelperFunctionConsolidation:
    """Property tests for helper function consolidation (Property 7)."""
    
    @given(st.text(min_size=1, max_size=50))
    # Complex text strategy with constraints: 50 examples
    @settings(max_examples=50, deadline=None)
    def test_find_labels_recursive_function_available(self, text):
        """**Feature: test-refactoring, Property 7: Helper Function Consolidation**
        *For any* helper function, it should appear in exactly one location 
        (either in a specific module or in shared utilities) and be functional.
        **Validates: Requirements 3.3**
        """
        label = MarkdownLabel(text=text)
        
        # Test that find_labels_recursive is available and works
        labels = find_labels_recursive(label)
        assert isinstance(labels, list), "find_labels_recursive should return a list"
        
        # All items in the list should be Label instances
        for lbl in labels:
            from kivy.uix.label import Label
            assert isinstance(lbl, Label), f"Should find only Labels, got {type(lbl)}"
    
    @given(color_strategy, color_strategy)
    # Combination strategy: 50 examples (capped for performance)
    @settings(max_examples=50, deadline=None)
    def test_colors_equal_function_available(self, color1, color2):
        """colors_equal helper function is available and works correctly."""
        # Test with identical colors
        assert colors_equal(color1, color1), "Identical colors should be equal"
        
        # Test with different colors (if they're actually different)
        if color1 != color2:
            # Most of the time they should be different
            result = colors_equal(color1, color2)
            assert isinstance(result, bool), "colors_equal should return boolean"
    
    @given(text_padding_strategy, text_padding_strategy)
    # Combination strategy: 50 examples (capped for performance)
    @settings(max_examples=50, deadline=None)
    def test_padding_equal_function_available(self, padding1, padding2):
        """padding_equal helper function is available and works correctly."""
        # Test with identical padding
        assert padding_equal(padding1, padding1), "Identical padding should be equal"
        
        # Test with different padding (if they're actually different)
        if padding1 != padding2:
            result = padding_equal(padding1, padding2)
            assert isinstance(result, bool), "padding_equal should return boolean"
    
    @given(st.floats(min_value=0.0, max_value=100.0, allow_nan=False, allow_infinity=False),
           st.floats(min_value=0.0, max_value=100.0, allow_nan=False, allow_infinity=False))
    # Float strategy with constraints: 20 examples
    @settings(max_examples=20, deadline=None)
    def test_floats_equal_function_available(self, float1, float2):
        """floats_equal helper function is available and works correctly."""
        # Test with identical floats
        assert floats_equal(float1, float1), "Identical floats should be equal"
        
        # Test with different floats (if they're actually different)
        if abs(float1 - float2) > 0.001:  # Only test if they're meaningfully different
            result = floats_equal(float1, float2)
            assert isinstance(result, bool), "floats_equal should return boolean"
            # They should not be equal if they differ by more than tolerance
            assert not result, f"Floats {float1} and {float2} should not be equal"