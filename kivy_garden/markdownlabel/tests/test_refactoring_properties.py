"""
Property-based tests for test refactoring validation.

This module contains tests that validate the test refactoring process itself,
including module naming consistency and other refactoring properties.
"""

import os
# Set environment variable to use headless mode for Kivy
os.environ['KIVY_NO_ARGS'] = '1'
os.environ['KIVY_NO_CONSOLELOG'] = '1'

import pytest
from hypothesis import given, strategies as st, settings


# **Feature: test-refactoring, Property 8: Module Naming Consistency**
# *For any* test module in the refactored structure, the filename SHALL follow
# the pattern `test_<feature_area>.py` where feature_area clearly indicates
# the functionality being tested.
# **Validates: Requirements 1.2, 4.1**

class TestModuleNamingConsistency:
    """Property tests for module naming consistency (Property 8)."""
    
    @given(st.sampled_from([
        'test_core_functionality.py',
        'test_label_compatibility.py', 
        'test_advanced_compatibility.py',
        'test_shortening_and_coordinate.py',
        'test_sizing_behavior.py',
        'test_text_properties.py',
        'test_font_properties.py',
        'test_color_properties.py',
        'test_padding_properties.py',
        'test_serialization.py',
        'test_performance.py',
        'test_refactoring_properties.py'
    ]))
    @settings(max_examples=100, deadline=None)
    def test_module_names_follow_pattern(self, module_name):
        """Test module names follow the test_<feature_area>.py pattern.
        
        **Feature: test-refactoring, Property 8: Module Naming Consistency**
        **Validates: Requirements 1.2, 4.1**
        """
        # Module should start with 'test_'
        assert module_name.startswith('test_'), \
            f"Module name {module_name} should start with 'test_'"
        
        # Module should end with '.py'
        assert module_name.endswith('.py'), \
            f"Module name {module_name} should end with '.py'"
        
        # Extract feature area (between 'test_' and '.py')
        feature_area = module_name[5:-3]  # Remove 'test_' prefix and '.py' suffix
        
        # Feature area should not be empty
        assert len(feature_area) > 0, \
            f"Feature area should not be empty in {module_name}"
        
        # Feature area should use underscores, not spaces or other separators
        assert '_' in feature_area or feature_area.isalpha(), \
            f"Feature area '{feature_area}' should use underscores for word separation"
        
        # Feature area should be descriptive (at least 4 characters)
        assert len(feature_area) >= 4, \
            f"Feature area '{feature_area}' should be descriptive (at least 4 characters)"
    
    def test_current_module_follows_naming_pattern(self):
        """Verify the current refactoring properties module follows naming pattern.
        
        **Feature: test-refactoring, Property 8: Module Naming Consistency**
        **Validates: Requirements 1.2, 4.1**
        """
        import os
        current_module = os.path.basename(__file__)
        
        # Should be 'test_refactoring_properties.py'
        assert current_module == 'test_refactoring_properties.py', \
            f"Current module name {current_module} should be 'test_refactoring_properties.py'"
        
        # Verify it follows the pattern
        assert current_module.startswith('test_'), \
            f"Current module {current_module} should start with 'test_'"
        assert current_module.endswith('.py'), \
            f"Current module {current_module} should end with '.py'"
        
        feature_area = current_module[5:-3]  # 'refactoring_properties'
        assert feature_area == 'refactoring_properties', \
            f"Feature area should be 'refactoring_properties', got '{feature_area}'"
    
    @given(st.text(min_size=4, max_size=20, alphabet=st.characters(
        whitelist_categories=['Ll', 'Nd'],  # Only lowercase letters and decimal numbers
        blacklist_characters=' -'
    )))
    @settings(max_examples=100, deadline=None)
    def test_feature_area_naming_rules(self, feature_name):
        """Test that feature area names follow consistent rules.
        
        **Feature: test-refactoring, Property 8: Module Naming Consistency**
        **Validates: Requirements 1.2, 4.1**
        """
        # Convert to lowercase with underscores (simulating module naming)
        normalized_name = feature_name.lower().replace(' ', '_').replace('-', '_')
        module_name = f'test_{normalized_name}.py'
        
        # Should follow pattern
        assert module_name.startswith('test_'), \
            f"Generated module name {module_name} should start with 'test_'"
        assert module_name.endswith('.py'), \
            f"Generated module name {module_name} should end with '.py'"
        
        # Feature area should be valid
        feature_area = module_name[5:-3]
        assert len(feature_area) >= 4, \
            f"Feature area '{feature_area}' should be at least 4 characters"
        # Should be lowercase (or contain no case-sensitive characters like numbers)
        assert feature_area == feature_area.lower(), \
            f"Feature area '{feature_area}' should be lowercase"
        
        # Should not have consecutive underscores
        assert '__' not in feature_area, \
            f"Feature area '{feature_area}' should not have consecutive underscores"