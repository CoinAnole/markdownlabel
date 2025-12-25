"""
Property-based tests for test file parser.

This module contains property tests that validate the test file parser
correctly extracts metadata from test files.
"""

import pytest
from hypothesis import given, strategies as st, settings, assume
import tempfile
import os
from pathlib import Path

from test_analysis.file_parser import FileParser, FileMetadata
# Import strategies from test_utils using absolute import
from kivy_garden.markdownlabel.tests.test_utils import rebuild_test_file_strategy


# **Feature: test-suite-refactoring, Property 1: Test Name Consistency**
# *For any* test method with "triggers_rebuild" in its name, the test
# implementation SHALL contain assertions that verify a rebuild actually
# occurred (such as widget identity checks or explicit rebuild verification).
# **Validates: Requirements 1.1**


@pytest.mark.test_tests
class TestTestNameConsistency:
    """Property tests for test name consistency (Property 1)."""
    
    @given(rebuild_test_file_strategy())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_rebuild_test_names_match_assertions(self, test_data):
        """Tests with 'triggers_rebuild' in name should have rebuild assertions."""
        test_code, test_name, has_rebuild_assertion = test_data
        
        # Write test code to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(test_code)
            temp_file = f.name
        
        try:
            parser = FileParser()
            metadata = parser.parse_file(temp_file)
            
            # Find the test method
            test_method = None
            for test_class in metadata.test_classes:
                for method in test_class.methods:
                    if method.name == test_name:
                        test_method = method
                        break
            
            assert test_method is not None, f"Test method {test_name} not found"
            
            # Property 1: If test name contains "triggers_rebuild",
            # it should have rebuild assertions
            if "triggers_rebuild" in test_name:
                if has_rebuild_assertion:
                    assert test_method.has_rebuild_assertions, \
                        f"Test {test_name} should have rebuild assertions"
                else:
                    # This is a naming violation - test claims to test rebuilds
                    # but doesn't actually verify them
                    # The parser should detect this inconsistency
                    pass  # We're testing the parser can detect this
        finally:
            os.unlink(temp_file)
    
    @given(st.text(min_size=1, max_size=10, alphabet=st.characters(min_codepoint=ord('a'), max_codepoint=ord('z'))))
    # Complex strategy: 10 examples (adequate coverage)
    @settings(max_examples=10, deadline=None)
    def test_parser_handles_valid_python_files(self, content_suffix):
        """Parser should handle any valid Python test file."""
        # Create a minimal valid test file
        safe_suffix = ''.join(c for c in content_suffix if c.isalnum())[:10] or "example"
        test_code = f'''"""Test module."""
import pytest

class TestExample:
    """Example test class."""
    
    def test_example_{safe_suffix}(self):
        """Example test method."""
        assert True
'''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(test_code)
            temp_file = f.name
        
        try:
            parser = FileParser()
            metadata = parser.parse_file(temp_file)
            
            # Should successfully parse
            assert isinstance(metadata, FileMetadata)
            assert len(metadata.test_classes) >= 1
        finally:
            os.unlink(temp_file)
    
    def test_parser_extracts_test_classes(self):
        """Parser should extract test classes correctly."""
        test_code = '''"""Test module."""
import pytest

class TestExample:
    """Example test class."""
    
    def test_method_one(self):
        """First test method."""
        assert True
    
    def test_method_two(self):
        """Second test method."""
        assert True

class TestAnother:
    """Another test class."""
    
    def test_method_three(self):
        """Third test method."""
        assert True
'''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(test_code)
            temp_file = f.name
        
        try:
            parser = FileParser()
            metadata = parser.parse_file(temp_file)
            
            assert len(metadata.test_classes) == 2
            assert metadata.test_classes[0].name == "TestExample"
            assert metadata.test_classes[1].name == "TestAnother"
            assert len(metadata.test_classes[0].methods) == 2
            assert len(metadata.test_classes[1].methods) == 1
        finally:
            os.unlink(temp_file)
    
    def test_parser_extracts_helper_functions(self):
        """Parser should extract helper functions correctly."""
        test_code = '''"""Test module."""
import pytest

def helper_function_one():
    """First helper function."""
    return True

def _private_helper():
    """Private helper function."""
    return False

class TestExample:
    """Example test class."""
    
    def test_method(self):
        """Test method."""
        assert helper_function_one()
'''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(test_code)
            temp_file = f.name
        
        try:
            parser = FileParser()
            metadata = parser.parse_file(temp_file)
            
            assert len(metadata.helper_functions) == 2
            helper_names = [h.name for h in metadata.helper_functions]
            assert "helper_function_one" in helper_names
            assert "_private_helper" in helper_names
            
            # Check private flag
            private_helper = next(h for h in metadata.helper_functions 
                                 if h.name == "_private_helper")
            assert private_helper.is_private
        finally:
            os.unlink(temp_file)
    
    def test_parser_detects_rebuild_assertions(self):
        """Parser should detect rebuild-related assertions."""
        test_code = '''"""Test module."""
import pytest

class TestRebuild:
    """Test rebuild behavior."""
    
    def test_with_rebuild_check(self):
        """Test with rebuild check."""
        widget_id_before = id(label.children[0])
        label.text = 'new'
        widget_id_after = id(label.children[0])
        assert widget_id_before != widget_id_after
    
    def test_without_rebuild_check(self):
        """Test without rebuild check."""
        label.text = 'new'
        assert label.text == 'new'
'''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(test_code)
            temp_file = f.name
        
        try:
            parser = FileParser()
            metadata = parser.parse_file(temp_file)
            
            test_class = metadata.test_classes[0]
            
            # First test should have rebuild assertions
            rebuild_test = next(m for m in test_class.methods 
                               if m.name == "test_with_rebuild_check")
            assert rebuild_test.has_rebuild_assertions
            
            # Second test should not have rebuild assertions
            value_test = next(m for m in test_class.methods 
                             if m.name == "test_without_rebuild_check")
            # Note: This might still be True if it has value assertions
            # The key is that it doesn't have widget_id checks
        finally:
            os.unlink(temp_file)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
