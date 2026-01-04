"""
Meta tests for sizing behavior test grouping validation.

These tests validate that sizing behavior tests are properly organized and grouped.
"""

import pytest


# *For any* two test classes that test the same feature area, they should be located in the same module

@pytest.mark.test_tests
class TestLogicalTestGrouping:
    """Property tests for logical test grouping."""

    def test_sizing_behavior_classes_grouped_together(self):
        """All sizing behavior test classes are grouped in the same module."""
        import inspect
        import kivy_garden.markdownlabel.tests.test_sizing_behavior as sizing_module

        # Get all test classes in this module
        test_classes = []
        for name, obj in inspect.getmembers(sizing_module):
            if (inspect.isclass(obj) and
                name.startswith('Test') and
                    obj.__module__ == sizing_module.__name__):
                test_classes.append(name)

        # Expected sizing behavior test classes (texture sizing moved to separate module)
        expected_classes = {
            'TestAutoSizingBehavior',
            'TestAutoSizeHeightTrueBehavior',
            'TestAutoSizeHeightFalseBehavior',
            'TestAutoSizeHeightDynamicToggling',
            'TestStrictLabelModeSizingBehavior'
        }

        # Verify all expected classes are present
        actual_classes = set(test_classes)
        assert expected_classes.issubset(actual_classes), \
            f"Missing expected classes: {expected_classes - actual_classes}"

        # Verify no unexpected classes (all classes should be sizing-related)
        sizing_related_keywords = {
            'auto', 'size', 'sizing', 'height', 'strict'
        }

        for class_name in test_classes:
            class_name_lower = class_name.lower()
            has_sizing_keyword = any(keyword in class_name_lower for keyword in sizing_related_keywords)
            assert has_sizing_keyword, \
                f"Test class {class_name} doesn't appear to be sizing-related"

    def test_module_focuses_on_sizing_behavior(self):
        """This module focuses specifically on sizing behavior functionality."""
        import kivy_garden.markdownlabel.tests.test_sizing_behavior as sizing_module

        # Check module docstring mentions sizing
        module_doc = sizing_module.__doc__ or ""
        sizing_keywords = ['sizing', 'size', 'auto-sizing']

        has_sizing_focus = any(keyword in module_doc.lower() for keyword in sizing_keywords)
        assert has_sizing_focus, \
            f"Module docstring should mention sizing behavior: {module_doc}"
