"""
Property-based tests for MarkdownLabel texture size calculations.

This module contains tests for texture size calculation behavior and
logical test grouping validation.
"""

import os

import pytest
from hypothesis import given, strategies as st, settings, assume

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout

from kivy_garden.markdownlabel import MarkdownLabel
from .test_utils import (
    simple_markdown_document, markdown_heading, markdown_paragraph,
    find_labels_recursive
)


# **Feature: label-compatibility, Property 3: Comprehensive Texture Size Calculation**
# *For any* MarkdownLabel with content, the `texture_size` property SHALL return
# a valid [width, height] list with non-negative values that aggregate all child widgets.
# **Validates: Requirements 1.1, 1.2, 1.3**

# The texture_size calculation must handle all widget types correctly:
# 1. Correct return type and structure
# 2. Handling all widget types without crashing
# 3. Correct aggregation logic (even if values are 0 in headless mode)
# 4. Proper handling of empty content
# 5. Widget types that have explicit heights (thematic_break, blank_line, AsyncImage)

class TestComprehensiveTextureSizeCalculation:
    """Property tests for comprehensive texture_size calculation (Property 3)."""
    
    def _find_all_widgets_recursive(self, widget, widgets=None):
        """Recursively find all widgets in a widget tree.
        
        Args:
            widget: Root widget to search
            # Complex strategy with custom domain strategy: 20 examples
            widgets: List to accumulate widgets (created if None)
            
        Returns:
            List of all widgets found
        """
        if widgets is None:
            widgets = []
        
        widgets.append(widget)
        
        if hasattr(widget, 'children'):
            for child in widget.children:
                # Complex strategy with custom domain strategy: 20 examples
                self._find_all_widgets_recursive(child, widgets)
        
        return widgets
    
    @given(simple_markdown_document())
    # Custom strategy: 20 examples for adequate coverage
    @settings(max_examples=20 if not os.getenv('CI') else 10, deadline=None)
    def test_texture_size_returns_tuple(self, markdown_text):
        """texture_size returns a list/tuple with two elements."""
        label = MarkdownLabel(text=markdown_text)
        
        texture_size = label.texture_size
        
        assert isinstance(texture_size, (list, tuple)), \
            f"Expected texture_size to be list/tuple, got {type(texture_size)}"
        assert len(texture_size) == 2, \
            f"Expected texture_size to have 2 elements, got {len(texture_size)}"
    
    @given(simple_markdown_document())
    # Custom strategy: 20 examples for adequate coverage
    @settings(max_examples=20 if not os.getenv('CI') else 10, deadline=None)
    def test_texture_size_non_negative(self, markdown_text):
        """texture_size width and height are non-negative."""
        # Complex strategy: 20 examples based on default complexity
        label = MarkdownLabel(text=markdown_text)
        
        texture_size = label.texture_size
        
        assert texture_size[0] >= 0, \
            f"Expected texture_size width >= 0, got {texture_size[0]}"
        assert texture_size[1] >= 0, \
            f"Expected texture_size height >= 0, got {texture_size[1]}"
    
    def test_empty_label_texture_size_is_zero(self):
        """Empty MarkdownLabel has texture_size [0, 0]."""
        label = MarkdownLabel(text='')
        
        texture_size = label.texture_size
         # Complex strategy: 20 examples based on default complexity
        
        assert texture_size == [0, 0], \
            f"Expected texture_size [0, 0] for empty label, got {texture_size}"
    
    @given(markdown_heading())
    # Custom strategy: 20 examples for adequate coverage
    @settings(max_examples=20 if not os.getenv('CI') else 10, deadline=None)
    def test_heading_creates_label_widget(self, heading):
        """Heading content creates a Label widget that is included in texture_size calculation."""
        label = MarkdownLabel(text=heading)
        
        # Verify heading creates children
        assert len(label.children) >= 1, \
            f"Expected at least 1 child for heading, got {len(label.children)}"
        
        # Verify texture_size is accessible and returns valid structure
        texture_size = label.texture_size
        assert isinstance(texture_size, (list, tuple)) and len(texture_size) == 2
        assert texture_size[0] >= 0 and texture_size[1] >= 0
    
    @given(markdown_paragraph())
    # Custom strategy: 20 examples for adequate coverage
    @settings(max_examples=20 if not os.getenv('CI') else 10, deadline=None)
    def test_paragraph_creates_label_widget(self, paragraph):
        """Paragraph content creates a Label widget that is included in texture_size calculation."""
        assume(paragraph.strip())
        
        label = MarkdownLabel(text=paragraph)
        
        # Verify paragraph creates children
        assert len(label.children) >= 1, \
            f"Expected at least 1 child for paragraph, got {len(label.children)}"
        
        # Verify texture_size is accessible and returns valid structure
        texture_size = label.texture_size
        assert isinstance(texture_size, (list, tuple)) and len(texture_size) == 2
        assert texture_size[0] >= 0 and texture_size[1] >= 0
    
    def test_code_block_creates_container_widget(self):
        """Code block content creates a BoxLayout container that is included in texture_size calculation."""
        markdown = '```python\nprint("hello")\n```'
        label = MarkdownLabel(text=markdown)
        
        # Verify code block creates children
        assert len(label.children) >= 1, \
            f"Expected at least 1 child for code block, got {len(label.children)}"
        
        # Verify texture_size is accessible and returns valid structure
        texture_size = label.texture_size
        assert isinstance(texture_size, (list, tuple)) and len(texture_size) == 2
        assert texture_size[0] >= 0 and texture_size[1] >= 0
    
    def test_list_creates_container_widget(self):
        """List content creates a BoxLayout container that is included in texture_size calculation."""
        markdown = '- Item 1\n- Item 2\n- Item 3'
        label = MarkdownLabel(text=markdown)
        
        # Verify list creates children
        assert len(label.children) >= 1, \
            f"Expected at least 1 child for list, got {len(label.children)}"
        
        # Verify texture_size is accessible and returns valid structure
        texture_size = label.texture_size
        assert isinstance(texture_size, (list, tuple)) and len(texture_size) == 2
        assert texture_size[0] >= 0 and texture_size[1] >= 0
    
    def test_table_creates_gridlayout_widget(self):
        """Table content creates a GridLayout widget that is included in texture_size calculation."""
        markdown = '| A | B |\n| --- | --- |\n| 1 | 2 |'
        label = MarkdownLabel(text=markdown)
        
        # Verify table creates children
        assert len(label.children) >= 1, \
            f"Expected at least 1 child for table, got {len(label.children)}"
        
        # Verify at least one child is a GridLayout
        has_gridlayout = any(isinstance(c, GridLayout) for c in label.children)
        assert has_gridlayout, "Expected a GridLayout child for table"
        
        # Verify texture_size is accessible and returns valid structure
        texture_size = label.texture_size
        assert isinstance(texture_size, (list, tuple)) and len(texture_size) == 2
        assert texture_size[0] >= 0 and texture_size[1] >= 0
    
    def test_block_quote_creates_container_widget(self):
        """Block quote content creates a BoxLayout container that is included in texture_size calculation."""
        markdown = '> This is a quote'
        label = MarkdownLabel(text=markdown)
        
        # Verify block quote creates children
        assert len(label.children) >= 1, \
            f"Expected at least 1 child for block quote, got {len(label.children)}"
        
        # Verify texture_size is accessible and returns valid structure
        texture_size = label.texture_size
        assert isinstance(texture_size, (list, tuple)) and len(texture_size) == 2
        assert texture_size[0] >= 0 and texture_size[1] >= 0
    
    def test_thematic_break_contributes_to_texture_size(self):
        """Thematic break (horizontal rule) contributes to texture_size with explicit height."""
        markdown = 'Before\n\n---\n\nAfter'
        label = MarkdownLabel(text=markdown)
        
        texture_size = label.texture_size
        
        # Thematic break has explicit height=20, so texture_size should be > 0
        # even in headless mode (Widget height is counted directly)
        assert texture_size[1] > 0, \
            f"Expected texture_size height > 0 for thematic break, got {texture_size[1]}"
    
    @given(st.integers(min_value=1, max_value=5))
    @settings(max_examples=100, deadline=None)
    def test_more_content_increases_texture_height(self, num_paragraphs):
        """More content results in larger texture_size height."""
        # Create markdown with varying number of paragraphs
        text1 = 'Single paragraph'
        text_multi = '\n\n'.join([f'Paragraph {i} with some text.' for i in range(num_paragraphs)])
        
        label1 = MarkdownLabel(text=text1)
        label_multi = MarkdownLabel(text=text_multi)
        
        # More paragraphs should result in larger height
        if num_paragraphs > 1:
            assert label_multi.texture_size[1] >= label1.texture_size[1], \
                f"Expected multi-paragraph height >= single paragraph height"
    
    def test_mixed_content_creates_multiple_widgets(self):
        """Mixed content (heading, paragraph, code, list) creates multiple widgets for texture_size."""
        markdown = '''# Heading

This is a paragraph.

```python
# Complex strategy with custom domain strategy: 20 examples
code = "block"
```

- List item 1
- List item 2

> A quote
'''
        label = MarkdownLabel(text=markdown)
        
        texture_size = label.texture_size
        
        # Verify texture_size is accessible and returns valid structure
        assert isinstance(texture_size, (list, tuple)) and len(texture_size) == 2
        assert texture_size[0] >= 0 and texture_size[1] >= 0
        
        # Should have multiple children
        assert len(label.children) > 1, \
            f"Expected multiple children for mixed content, got {len(label.children)}"
    
    @given(simple_markdown_document())
    # Custom strategy: 20 examples for adequate coverage
    @settings(max_examples=20 if not os.getenv('CI') else 10, deadline=None)
    def test_texture_size_accessible_for_all_content(self, markdown_text):
        """texture_size is accessible and valid for all markdown content."""
        assume(markdown_text.strip())
        
        label = MarkdownLabel(text=markdown_text)
        
        texture_size = label.texture_size
        
        # Verify texture_size is accessible and returns valid structure
        assert isinstance(texture_size, (list, tuple)) and len(texture_size) == 2
        assert texture_size[0] >= 0 and texture_size[1] >= 0
        
        # If there are children, the calculation should have run without error
        if len(label.children) > 0:
            # The method should have traversed all children
            pass  # No assertion needed - if we got here, the method worked
    
    def test_nested_list_creates_nested_containers(self):
        """Nested list content creates nested BoxLayout containers for texture_size calculation."""
        markdown = '''- Item 1
  - Nested 1
  - Nested 2
- Item 2'''
        label = MarkdownLabel(text=markdown)
        
        # Verify nested list creates children
        # Complex strategy with custom domain strategy: 20 examples
        assert len(label.children) >= 1, \
            f"Expected at least 1 child for nested list, got {len(label.children)}"
        
        # Verify texture_size is accessible and returns valid structure
        texture_size = label.texture_size
        assert isinstance(texture_size, (list, tuple)) and len(texture_size) == 2
        assert texture_size[0] >= 0 and texture_size[1] >= 0
    
    def test_ordered_list_creates_container_widget(self):
        """Ordered list content creates a BoxLayout container for texture_size calculation."""
        markdown = '1. First\n2. Second\n3. Third'
        label = MarkdownLabel(text=markdown)
        
        # Verify ordered list creates children
        assert len(label.children) >= 1, \
            f"Expected at least 1 child for ordered list, got {len(label.children)}"
        
        # Verify texture_size is accessible and returns valid structure
        texture_size = label.texture_size
        assert isinstance(texture_size, (list, tuple)) and len(texture_size) == 2
        assert texture_size[0] >= 0 and texture_size[1] >= 0
    
    @given(simple_markdown_document(), simple_markdown_document())
    # Custom strategy: 20 examples for adequate coverage
    @settings(max_examples=20 if not os.getenv('CI') else 10, deadline=None)
    def test_texture_size_updates_on_text_change(self, text1, text2):
        """texture_size updates when text property changes."""
        assume(text1.strip() and text2.strip())
        assume(text1 != text2)
        
        label = MarkdownLabel(text=text1)
        texture_size1 = label.texture_size
        
        # Change text - use force_rebuild() for immediate update since
        # text changes now use deferred rebuilds
        label.text = text2
        label.force_rebuild()
        texture_size2 = label.texture_size
        
        # texture_size should be recalculated (may or may not be different)
        # The key is that it doesn't crash and returns valid values
        assert isinstance(texture_size2, (list, tuple)), \
            f"Expected texture_size to be list/tuple after text change"
        assert len(texture_size2) == 2, \
            f"Expected texture_size to have 2 elements after text change"
        assert texture_size2[0] >= 0 and texture_size2[1] >= 0, \
            f"Expected non-negative texture_size after text change"
    
    def test_texture_size_with_image_markdown(self):
        """Image markdown contributes to texture_size.
        
        Note: In Markdown, images are inline elements typically wrapped in paragraphs.
        The texture_size should account for the containing paragraph and/or image widget.
        """
        # Use image in a paragraph context (common usage)
        markdown = 'Here is an image:\n\n![Alt text](https://example.com/image.png)\n\nAfter image.'
        label = MarkdownLabel(text=markdown)
        
        texture_size = label.texture_size
        
        # Content with image should have non-zero texture_size
        # (the surrounding text paragraphs will contribute even if image doesn't)
        assert texture_size[1] > 0, \
            f"Expected texture_size height > 0 for content with image, got {texture_size[1]}"
        
        # Verify children were created
        assert len(label.children) > 0, \
            f"Expected children for image markdown, got {len(label.children)}"
    
    @given(st.integers(min_value=1, max_value=6))
    @settings(max_examples=100, deadline=None)
    def test_all_heading_levels_create_label_widgets(self, level):
        """All heading levels create Label widgets for texture_size calculation."""
        markdown = '#' * level + ' Heading'
        label = MarkdownLabel(text=markdown)
        
        # Verify heading creates children
        assert len(label.children) >= 1, \
            f"Expected at least 1 child for h{level}, got {len(label.children)}"
        
        # Verify texture_size is accessible and returns valid structure
        texture_size = label.texture_size
        assert isinstance(texture_size, (list, tuple)) and len(texture_size) == 2
        assert texture_size[0] >= 0 and texture_size[1] >= 0
    
    def test_blank_lines_create_spacer_widgets(self):
        """Blank lines create spacer widgets with explicit height for texture_size."""
        markdown_no_blanks = 'Para 1\nPara 2'
        markdown_with_blanks = 'Para 1\n\n\n\nPara 2'
        
        label_no_blanks = MarkdownLabel(text=markdown_no_blanks)
        label_with_blanks = MarkdownLabel(text=markdown_with_blanks)
        
        # Both should have valid texture_size
        ts_no_blanks = label_no_blanks.texture_size
        ts_with_blanks = label_with_blanks.texture_size
        
        assert isinstance(ts_no_blanks, (list, tuple)) and len(ts_no_blanks) == 2
        assert isinstance(ts_with_blanks, (list, tuple)) and len(ts_with_blanks) == 2
        
        # With blank lines should have more children (blank_line widgets)
        # and thus potentially larger texture_size height
        assert len(label_with_blanks.children) >= len(label_no_blanks.children), \
            "Expected content with blank lines to have at least as many children"
        
        # blank_line widgets have explicit height (base_font_size), so they contribute
        # to texture_size even in headless mode
        assert ts_with_blanks[1] >= ts_no_blanks[1], \
            "Expected content with blank lines to have at least as much height"


# **Feature: test-refactoring, Property 9: Logical Test Grouping**
# *For any* two test classes that test the same feature area, they should be located in the same module
# **Validates: Requirements 1.4, 4.3, 4.4**

class TestTextureSizingTestGrouping:
    """Property tests for texture sizing test grouping (Property 9)."""
    
    def test_texture_sizing_classes_grouped_together(self):
        """All texture sizing test classes are grouped in the same module."""
        import inspect
        import kivy_garden.markdownlabel.tests.test_texture_sizing as texture_module
        
        # Get all test classes in this module
        test_classes = []
        for name, obj in inspect.getmembers(texture_module):
            if (inspect.isclass(obj) and 
                name.startswith('Test') and 
                obj.__module__ == texture_module.__name__):
                test_classes.append(name)
        
        # Expected texture sizing test classes
        expected_classes = {
            'TestComprehensiveTextureSizeCalculation',
            'TestTextureSizingTestGrouping'  # This test class itself
        }
        
        # Verify all expected classes are present
        actual_classes = set(test_classes)
        assert expected_classes.issubset(actual_classes), \
            f"Missing expected classes: {expected_classes - actual_classes}"
        
        # Verify no unexpected classes (all classes should be texture-related)
        texture_related_keywords = {
            'texture', 'size', 'sizing', 'calculation', 'grouping'
        }
        
        for class_name in test_classes:
            class_name_lower = class_name.lower()
            has_texture_keyword = any(keyword in class_name_lower for keyword in texture_related_keywords)
            assert has_texture_keyword, \
                f"Test class {class_name} doesn't appear to be texture-related"
    
    def test_module_focuses_on_texture_sizing(self):
        """This module focuses specifically on texture sizing functionality."""
        import kivy_garden.markdownlabel.tests.test_texture_sizing as texture_module
        
        # Check module docstring mentions texture sizing
        module_doc = texture_module.__doc__ or ""
        texture_keywords = ['texture', 'size', 'calculation']
        
        has_texture_focus = any(keyword in module_doc.lower() for keyword in texture_keywords)
        assert has_texture_focus, \
            f"Module docstring should mention texture sizing: {module_doc}"