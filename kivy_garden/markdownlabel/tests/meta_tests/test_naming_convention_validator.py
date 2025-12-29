"""
Tests for the naming convention validator module.

This module contains both unit tests and property-based tests for validating
the naming convention validator's ability to detect violations and suggest
appropriate renames.
"""

import ast
import pytest
import tempfile
import os
from hypothesis import given, strategies as st, settings
from pathlib import Path

from kivy_garden.markdownlabel.tests.modules.naming_convention_validator import (
    NamingConventionValidator, NamingViolationType, NamingViolation
)
from kivy_garden.markdownlabel.tests.modules.assertion_analyzer import AssertionAnalyzer, AssertionType, AssertionAnalysis


@pytest.mark.test_tests
class TestNamingConventionValidator:
    """Unit tests for NamingConventionValidator."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.validator = NamingConventionValidator()
        self.assertion_analyzer = AssertionAnalyzer()
    
    def test_rebuild_mismatch_detection(self):
        """Test detection of rebuild naming mismatches."""
        test_code = '''
def test_property_triggers_rebuild(self):
    widget.text = "new text"
    assert widget.text == "new text"
'''
        tree = ast.parse(test_code)
        test_method = tree.body[0]
        
        analysis = self.assertion_analyzer.analyze_test_method(test_method, "test_file.py")
        violations = self.validator.validate_test_method(analysis)
        
        assert len(violations) > 0
        assert any(v.violation_type == NamingViolationType.REBUILD_MISMATCH for v in violations)
    
    def test_value_mismatch_detection(self):
        """Test detection of value naming mismatches."""
        test_code = '''
def test_property_updates_value(self):
    old_id = widget.id
    widget.text = "new text"
    assert widget.id != old_id
'''
        tree = ast.parse(test_code)
        test_method = tree.body[0]
        
        analysis = self.assertion_analyzer.analyze_test_method(test_method, "test_file.py")
        violations = self.validator.validate_test_method(analysis)
        
        assert len(violations) > 0
        assert any(v.violation_type == NamingViolationType.VALUE_MISMATCH for v in violations)
    
    def test_compliant_test_no_violations(self):
        """Test that compliant tests have no violations."""
        test_code = '''
def test_property_updates_value(self):
    widget.text = "new text"
    assert widget.text == "new text"
'''
        tree = ast.parse(test_code)
        test_method = tree.body[0]
        
        analysis = self.assertion_analyzer.analyze_test_method(test_method, "test_file.py")
        violations = self.validator.validate_test_method(analysis)
        
        # Should have minimal or no violations for a properly named test
        rebuild_violations = [v for v in violations if v.violation_type == NamingViolationType.REBUILD_MISMATCH]
        value_violations = [v for v in violations if v.violation_type == NamingViolationType.VALUE_MISMATCH]
        
        assert len(rebuild_violations) == 0
        assert len(value_violations) == 0
    
    def test_suggested_rename_generation(self):
        """Test generation of suggested renames."""
        test_code = '''
def test_font_size_triggers_rebuild(self):
    widget.font_size = 20
    assert widget.font_size == 20
'''
        tree = ast.parse(test_code)
        test_method = tree.body[0]
        
        analysis = self.assertion_analyzer.analyze_test_method(test_method, "test_file.py")
        violations = self.validator.validate_test_method(analysis)
        
        rebuild_violations = [v for v in violations if v.violation_type == NamingViolationType.REBUILD_MISMATCH]
        assert len(rebuild_violations) > 0
        
        violation = rebuild_violations[0]
        assert "updates_value" in violation.suggested_name or "changes_property" in violation.suggested_name


# Property-based tests

@given(
    test_name_base=st.text(min_size=1, max_size=30, alphabet=st.characters(whitelist_categories=['L', 'N']) | st.just('_')),
    assertion_type=st.sampled_from([
        ("rebuild", "widget.id != old_id", True),
        ("value", "widget.text == 'test'", False),
    ])
)
# Combination strategy: 50 examples (combination coverage)
@settings(max_examples=50, deadline=None)
def test_naming_pattern_consistency_property(test_name_base, assertion_type):
    """Test that test methods with consistent naming patterns (matching their assertion types) do not generate rebuild or value naming violations."""
    validator = NamingConventionValidator()
    assertion_analyzer = AssertionAnalyzer()
    
    assertion_name, assertion_code, has_rebuild = assertion_type
    
    # Create test with appropriate naming
    if has_rebuild:
        test_name = f"test_{test_name_base}_triggers_rebuild"
    else:
        test_name = f"test_{test_name_base}_updates_value"
    
    test_code = f'''
def {test_name}(self):
    assert {assertion_code}
'''
    
    try:
        tree = ast.parse(test_code)
        test_method = tree.body[0]
        
        analysis = assertion_analyzer.analyze_test_method(test_method, "test_file.py")
        violations = validator.validate_test_method(analysis)
        
        # Tests with consistent naming should have fewer violations
        # (may still have pattern consistency violations, but not rebuild/value mismatches)
        rebuild_violations = [v for v in violations if v.violation_type == NamingViolationType.REBUILD_MISMATCH]
        value_violations = [v for v in violations if v.violation_type == NamingViolationType.VALUE_MISMATCH]
        
        # If test has rebuild assertions and name says "triggers_rebuild", no rebuild mismatch
        if has_rebuild and "triggers_rebuild" in test_name:
            assert len(rebuild_violations) == 0, f"Should not have rebuild violations for {test_name}"
        
        # If test has value assertions and name says "updates_value", no value mismatch
        if not has_rebuild and "updates_value" in test_name:
            assert len(value_violations) == 0, f"Should not have value violations for {test_name}"
    
    except SyntaxError:
        # Skip invalid test code that doesn't parse
        pass


@given(
    test_names=st.lists(
        st.text(min_size=1, max_size=20, alphabet=st.characters(whitelist_categories=['L', 'N']) | st.just('_')).filter(
            lambda x: x.isidentifier() and not x.startswith('_')
        ),
        min_size=2,
        max_size=5
    )
)
# Complex strategy: 30 examples (adequate coverage)
@settings(max_examples=30, deadline=None)
def test_file_level_consistency(test_names):
    """Test that naming consistency is checked at the file level."""
    validator = NamingConventionValidator()
    
    # Create a temporary test file with multiple tests
    test_content = "import pytest\n\n"
    
    for i, name_base in enumerate(test_names):
        # Alternate between rebuild and value tests
        if i % 2 == 0:
            test_content += f'''
def test_{name_base}_triggers_rebuild(self):
    old_id = widget.id
    widget.text = "new"
    assert widget.id != old_id

'''
        else:
            test_content += f'''
def test_{name_base}_updates_value(self):
    widget.text = "new"
    assert widget.text == "new"

'''
    
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(test_content)
            temp_file = f.name
        
        try:
            report = validator.validate_file(temp_file)
            
            # Should analyze all tests
            assert report.total_tests == len(test_names)
            
            # Compliance percentage should be between 0 and 100
            assert 0 <= report.compliance_percentage <= 100
            
            # Violations + compliant should equal total
            assert report.violation_count + report.compliant_tests == report.total_tests
        
        finally:
            os.unlink(temp_file)
    
    except SyntaxError:
        # Skip if generated code doesn't parse
        pass


def test_file_validation_integration():
    """Integration test for validating a complete test file."""
    validator = NamingConventionValidator()
    
    test_content = '''
import pytest

class TestExample:
    def test_property_triggers_rebuild(self):
        """Test with naming mismatch - says rebuild but only checks value."""
        widget.text = "new text"
        assert widget.text == "new text"
    
    def test_property_updates_value(self):
        """Test with correct naming."""
        widget.color = [1, 0, 0, 1]
        assert widget.color == [1, 0, 0, 1]
    
    def test_widget_rebuild_detection(self):
        """Test with correct rebuild naming."""
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
        report = validator.validate_file(temp_file)
        
        # Should find 4 test methods
        assert report.total_tests == 4
        
        # Should find at least one violation (the first test)
        assert report.violation_count > 0
        
        # Check that the first test has a rebuild mismatch
        first_test_violations = [
            v for v in report.violations 
            if v.test_name == "test_property_triggers_rebuild"
        ]
        assert len(first_test_violations) > 0
        
        # Compliance percentage should be calculated correctly
        expected_compliance = (report.compliant_tests / report.total_tests * 100)
        assert abs(report.compliance_percentage - expected_compliance) < 0.01
    
    finally:
        os.unlink(temp_file)


def test_rename_script_generation():
    """Test generation of rename scripts."""
    validator = NamingConventionValidator()
    
    test_content = '''
def test_property_triggers_rebuild(self):
    widget.text = "new text"
    assert widget.text == "new text"
'''
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_content)
        temp_file = f.name
    
    try:
        report = validator.validate_file(temp_file)
        
        if report.violations:
            script = validator.generate_rename_script(report)
            
            # Script should contain rename operations
            assert "def rename_tests():" in script
            assert "test_property_triggers_rebuild" in script
            
            # Should suggest a better name
            assert any(v.suggested_name in script for v in report.violations)
    
    finally:
        os.unlink(temp_file)


if __name__ == "__main__":
    pytest.main([__file__])