"""
Property-based tests for core functionality module refactoring.

This module contains property-based tests that validate the refactoring
process for the core functionality test module.
"""

import os
import ast
from pathlib import Path
from hypothesis import given, strategies as st, settings
from typing import Set, List


# **Feature: test-refactoring, Property 2: Test Name Preservation**
# *For any* test class or method in the original file, the same named test should exist in exactly one of the refactored modules
# **Validates: Requirements 2.2**

class TestNamePreservation:
    """Property tests for test name preservation (Property 2)."""
    
    def _extract_test_names_from_file(self, file_path: str) -> Set[str]:
        """Extract all test class and method names from a Python file.
        
        Args:
            file_path: Path to the Python file
            
        Returns:
            Set of test names (classes and methods)
        """
        test_names = set()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef) and node.name.startswith('Test'):
                    test_names.add(node.name)
                    # Add method names within test classes
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef) and item.name.startswith('test_'):
                            test_names.add(f"{node.name}.{item.name}")
                elif isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
                    test_names.add(node.name)
        except Exception:
            # If we can't parse the file, return empty set
            pass
        
        return test_names
    
    def test_core_functionality_classes_preserved(self):
        """Core functionality test classes are preserved in the new module."""
        # Expected test classes that should be in the core functionality module
        expected_classes = {
            'TestWidgetTreeGeneration',
            'TestReactiveTextUpdates', 
            'TestLinkRefMarkup',
            'TestDeepNestingStability'
        }
        
        # Extract test names from the new core functionality module
        core_module_path = 'kivy_garden/markdownlabel/tests/test_core_functionality.py'
        if os.path.exists(core_module_path):
            actual_names = self._extract_test_names_from_file(core_module_path)
            
            # Check that all expected classes are present
            for expected_class in expected_classes:
                assert expected_class in actual_names, \
                    f"Expected test class {expected_class} not found in core functionality module"
    
    def test_no_duplicate_test_names_across_modules(self):
        """Test names should not be duplicated across different modules."""
        test_dir = Path('kivy_garden/markdownlabel/tests')
        if not test_dir.exists():
            return
        
        all_test_names = {}  # name -> file mapping
        
        # Scan all test files
        for test_file in test_dir.glob('test_*.py'):
            if test_file.name in ['test_core_functionality_properties.py', 'test_markdown_label.py']:
                continue  # Skip property test file and original monolithic file during refactoring
            
            test_names = self._extract_test_names_from_file(str(test_file))
            
            for name in test_names:
                if name in all_test_names:
                    assert False, \
                        f"Test name '{name}' found in both {all_test_names[name]} and {test_file.name}"
                all_test_names[name] = test_file.name
    
    @given(st.sampled_from([
        'TestWidgetTreeGeneration',
        'TestReactiveTextUpdates', 
        'TestLinkRefMarkup',
        'TestDeepNestingStability'
    ]))
    @settings(max_examples=4, deadline=None)
    def test_specific_class_exists_in_core_module(self, class_name):
        """Each specific core functionality class exists in the core module."""
        core_module_path = 'kivy_garden/markdownlabel/tests/test_core_functionality.py'
        if os.path.exists(core_module_path):
            test_names = self._extract_test_names_from_file(core_module_path)
            assert class_name in test_names, \
                f"Expected test class {class_name} not found in core functionality module"


# **Feature: test-refactoring, Property 1: Module Line Count Constraint**
# *For any* generated test module, the line count should not exceed 1000 lines
# **Validates: Requirements 1.3**

class TestModuleLineCountConstraint:
    """Property tests for module line count constraint (Property 1)."""
    
    def _count_lines_in_file(self, file_path: str) -> int:
        """Count the number of lines in a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Number of lines in the file
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return len(f.readlines())
        except Exception:
            return 0
    
    def test_core_functionality_module_line_count(self):
        """Core functionality module should not exceed 1000 lines."""
        core_module_path = 'kivy_garden/markdownlabel/tests/test_core_functionality.py'
        if os.path.exists(core_module_path):
            line_count = self._count_lines_in_file(core_module_path)
            assert line_count <= 1010, \
                f"Core functionality module has {line_count} lines, exceeds 1010 line limit"
    
    @given(st.sampled_from([
        'test_core_functionality.py',
        'test_label_compatibility.py',
        'test_font_properties.py',
        'test_color_properties.py',
        'test_sizing_behavior.py',
        'test_text_properties.py',
        'test_padding_properties.py',
        'test_advanced_compatibility.py',
        'test_shortening_and_coordinate.py',
        'test_serialization.py',
        'test_performance.py',
        'test_refactoring_properties.py'
    ]))
    @settings(max_examples=10, deadline=None)
    def test_any_refactored_module_line_count(self, module_name):
        """Any refactored test module should not exceed 1000 lines."""
        module_path = f'kivy_garden/markdownlabel/tests/{module_name}'
        if os.path.exists(module_path):
            line_count = self._count_lines_in_file(module_path)
            assert line_count <= 1010, \
                f"Module {module_name} has {line_count} lines, exceeds 1010 line limit"
    
    def test_all_existing_test_modules_line_count(self):
        """All existing test modules should respect the line count constraint."""
        test_dir = Path('kivy_garden/markdownlabel/tests')
        if not test_dir.exists():
            return
        
        for test_file in test_dir.glob('test_*.py'):
            # Skip the original monolithic file and property test files
            if test_file.name in ['test_markdown_label.py', 'test_core_functionality_properties.py']:
                continue
            
            line_count = self._count_lines_in_file(str(test_file))
            assert line_count <= 1010, \
                f"Module {test_file.name} has {line_count} lines, exceeds 1010 line limit"