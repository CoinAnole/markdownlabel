"""
Meta tests for texture sizing test grouping validation.

These tests validate that texture sizing tests are properly organized and grouped.
"""

import pytest


# **Feature: test-refactoring, Property 9: Logical Test Grouping**
# *For any* two test classes that test the same feature area, they should be located in the same module
# **Validates: Requirements 1.4, 4.3, 4.4**

@pytest.mark.test_tests
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
            'TestComprehensiveTextureSizeCalculation'
        }

        # Verify all expected classes are present
        actual_classes = set(test_classes)
        assert expected_classes.issubset(actual_classes), \
            f"Missing expected classes: {expected_classes - actual_classes}"

        # Verify no unexpected classes (all classes should be texture-related)
        texture_related_keywords = {
            'texture', 'size', 'sizing', 'calculation'
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