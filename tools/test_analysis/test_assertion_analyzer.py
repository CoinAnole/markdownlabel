"""
Tests for the assertion analyzer module.

This module contains both unit tests and property-based tests for validating
the assertion analyzer's ability to correctly identify assertion patterns
and detect naming mismatches.
"""

import ast
import pytest
from hypothesis import given, strategies as st, settings
from pathlib import Path
import tempfile
import os

from .assertion_analyzer import AssertionAnalyzer, AssertionType, AssertionPattern, TestAssertionAnalysis


class TestAssertionAnalyzer:
    """Unit tests for AssertionAnalyzer."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.analyzer = AssertionAnalyzer()
    
    def test_rebuild_assertion_detection(self):
        """Test detection of rebuild-related assertions."""
        test_code = '''
def test_property_triggers_rebuild(self):
    old_id = widget.id
    widget.text = "new text"
    assert widget.id != old_id
'''
        tree = ast.parse(test_code)
        test_method = tree.body[0]
        
        analysis = self.analyzer.analyze_test_method(test_method, "test_file.py")
        
        assert analysis.has_rebuild_assertions
        assert analysis.primary_assertion_type == AssertionType.REBUILD
        assert not analysis.naming_mismatch_detected
    
    def test_value_assertion_detection(self):
        """Test detection of value-only assertions."""
        test_code = '''
def test_property_updates_value(self):
    widget.text = "new text"
    assert widget.text == "new text"
'''
        tree = ast.parse(test_code)
        test_method = tree.body[0]
        
        analysis = self.analyzer.analyze_test_method(test_method, "test_file.py")
        
        assert analysis.has_value_assertions
        assert analysis.primary_assertion_type == AssertionType.VALUE_CHANGE
        assert not analysis.naming_mismatch_detected
    
    def test_naming_mismatch_detection(self):
        """Test detection of naming/assertion mismatches."""
        test_code = '''
def test_property_triggers_rebuild(self):
    widget.text = "new text"
    assert widget.text == "new text"
'''
        tree = ast.parse(test_code)
        test_method = tree.body[0]
        
        analysis = self.analyzer.analyze_test_method(test_method, "test_file.py")
        
        assert analysis.naming_mismatch_detected
        assert analysis.suggested_name_pattern == "test_property_updates_value"
    
    def test_suggested_name_generation(self):
        """Test generation of suggested test names."""
        test_cases = [
            ("test_font_size_triggers_rebuild", AssertionType.VALUE_CHANGE, False, "test_font_size_updates_value"),
            ("test_text_changes_property", AssertionType.REBUILD, True, "test_text_triggers_rebuild"),
            ("test_widget_exists", AssertionType.EXISTENCE, False, "test_widget_exists"),
        ]
        
        for current_name, primary_type, has_rebuild, expected in test_cases:
            suggested = self.analyzer._suggest_name_pattern(current_name, primary_type, has_rebuild)
            assert suggested == expected


# Property-based tests

@given(st.text(min_size=1, max_size=50, alphabet=st.characters(whitelist_categories=['L', 'N']) | st.just('_')))
@settings(max_examples=100)
def test_value_change_test_naming_property(test_name_suffix):
    """
    **Property 2: Value Change Test Naming**
    **Validates: Requirements 1.2**
    
    For any test method that only asserts value changes without verifying rebuild behavior,
    the test name SHALL use patterns like "updates_value" or "changes_property" instead of "triggers_rebuild".
    """
    analyzer = AssertionAnalyzer()
    
    # Create a test method that only has value assertions (no rebuild)
    test_code = f'''
def test_{test_name_suffix}_triggers_rebuild(self):
    widget.text = "new text"
    assert widget.text == "new text"
    assert widget.color == [1, 1, 1, 1]
'''
    
    try:
        tree = ast.parse(test_code)
        test_method = tree.body[0]
        
        analysis = analyzer.analyze_test_method(test_method, "test_file.py")
        
        # If the test only has value assertions but name suggests rebuild,
        # it should be detected as a naming mismatch
        if analysis.has_value_assertions and not analysis.has_rebuild_assertions:
            if "triggers_rebuild" in test_method.name:
                assert analysis.naming_mismatch_detected, f"Test {test_method.name} should be flagged for naming mismatch"
                assert analysis.suggested_name_pattern is not None
                assert "updates_value" in analysis.suggested_name_pattern or "changes_property" in analysis.suggested_name_pattern
    
    except SyntaxError:
        # Skip invalid test names that don't parse
        pass


@given(
    assertion_type=st.sampled_from([
        ("rebuild", "widget.id != old_id"),
        ("value", "widget.text == 'test'"),
        ("existence", "assert widget is not None"),
        ("equality", "assert a == b"),
        ("boolean", "assert True")
    ]),
    test_name_base=st.text(min_size=1, max_size=30, alphabet=st.characters(whitelist_categories=['L', 'N']) | st.just('_'))
)
@settings(max_examples=100)
def test_assertion_classification_consistency(assertion_type, test_name_base):
    """Test that assertion classification is consistent across different test structures."""
    analyzer = AssertionAnalyzer()
    assertion_name, assertion_code = assertion_type
    
    # Create a test method with the given assertion
    test_code = f'''
def test_{test_name_base}(self):
    assert {assertion_code}
'''
    
    try:
        tree = ast.parse(test_code)
        test_method = tree.body[0]
        
        analysis = analyzer.analyze_test_method(test_method, "test_file.py")
        
        # Verify that the assertion was classified
        assert len(analysis.assertions) > 0, "Should detect at least one assertion"
        
        # Verify that the primary assertion type is reasonable
        assert analysis.primary_assertion_type != AssertionType.UNKNOWN or len(analysis.assertions) == 0
        
        # Verify that rebuild assertions are properly detected
        if assertion_name == "rebuild":
            assert analysis.has_rebuild_assertions, "Should detect rebuild assertions"
        elif assertion_name == "value":
            assert analysis.has_value_assertions, "Should detect value assertions"
    
    except SyntaxError:
        # Skip invalid test code that doesn't parse
        pass


def test_file_analysis_integration():
    """Integration test for analyzing a complete test file."""
    analyzer = AssertionAnalyzer()
    
    # Create a temporary test file
    test_content = '''
import pytest

class TestExample:
    def test_property_triggers_rebuild(self):
        """Test that should trigger rebuild but only checks value."""
        widget.text = "new text"
        assert widget.text == "new text"
    
    def test_property_updates_value(self):
        """Test that correctly checks value changes."""
        widget.color = [1, 0, 0, 1]
        assert widget.color == [1, 0, 0, 1]
    
    def test_widget_rebuild_detection(self):
        """Test that correctly checks for rebuild."""
        old_id = widget.id
        widget.text = "new text"
        assert widget.id != old_id

def test_module_level_function(self):
    """Module-level test function."""
    assert True
'''
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_content)
        temp_file = f.name
    
    try:
        analyses = analyzer.analyze_file(temp_file)
        
        # Should find 4 test methods
        assert len(analyses) == 4
        
        # Check for naming mismatch in first test
        first_test = next(a for a in analyses if a.test_name == "test_property_triggers_rebuild")
        assert first_test.naming_mismatch_detected
        
        # Check that correctly named tests don't have mismatches
        value_test = next(a for a in analyses if a.test_name == "test_property_updates_value")
        assert not value_test.naming_mismatch_detected
        
        rebuild_test = next(a for a in analyses if a.test_name == "test_widget_rebuild_detection")
        assert not rebuild_test.naming_mismatch_detected
        
    finally:
        os.unlink(temp_file)


if __name__ == "__main__":
    pytest.main([__file__])