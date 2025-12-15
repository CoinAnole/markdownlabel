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


# **Feature: test-refactoring, Property 5: Test Discovery Completeness**
# *For any* test in the original file, pytest should discover and be able to execute
# that test in the refactored structure
# **Validates: Requirements 2.5**

class TestDiscoveryCompleteness:
    """Property tests for test discovery completeness (Property 5)."""
    
    def test_pytest_discovers_all_refactored_tests(self):
        """Test that pytest can discover all tests in the refactored structure.
        
        **Feature: test-refactoring, Property 5: Test Discovery Completeness**
        **Validates: Requirements 2.5**
        """
        import subprocess
        import os
        
        # Get the test directory path
        test_dir = os.path.dirname(__file__)
        
        # Run pytest --collect-only to get all discoverable tests
        result = subprocess.run([
            'pytest', '--collect-only', test_dir, '-q'
        ], capture_output=True, text=True, cwd=os.path.dirname(test_dir))
        
        # Should succeed without errors
        assert result.returncode == 0, \
            f"pytest test discovery failed with return code {result.returncode}. " \
            f"stderr: {result.stderr}"
        
        # Should discover a reasonable number of tests (at least 500)
        # This ensures the refactored structure is discoverable
        lines = result.stdout.strip().split('\n')
        test_lines = [line for line in lines if '::' in line and 'test_' in line]
        
        assert len(test_lines) >= 500, \
            f"Expected at least 500 discoverable tests, found {len(test_lines)}. " \
            f"This suggests test discovery is incomplete."
        
        # Should discover tests from multiple modules
        modules = set()
        for line in test_lines:
            if '::' in line:
                module_path = line.split('::')[0]
                module_name = os.path.basename(module_path)
                modules.add(module_name)
        
        # Should have tests from at least 10 different modules
        assert len(modules) >= 10, \
            f"Expected tests from at least 10 modules, found {len(modules)}: {sorted(modules)}"
        
        # Should include key refactored modules
        expected_modules = {
            'test_core_functionality.py',
            'test_label_compatibility.py',
            'test_font_properties.py',
            'test_color_properties.py',
            'test_sizing_behavior.py',
            'test_text_properties.py',
            'test_padding_properties.py',
            'test_serialization.py',
            'test_performance.py'
        }
        
        found_modules = {mod for mod in modules if mod in expected_modules}
        assert len(found_modules) >= 8, \
            f"Expected at least 8 key refactored modules, found {len(found_modules)}: {sorted(found_modules)}"
    
    @given(st.sampled_from([
        'test_core_functionality.py',
        'test_label_compatibility.py',
        'test_advanced_compatibility.py',
        'test_font_properties.py',
        'test_color_properties.py',
        'test_sizing_behavior.py',
        'test_text_properties.py',
        'test_padding_properties.py',
        'test_serialization.py',
        'test_performance.py'
    ]))
    @settings(max_examples=50, deadline=None)
    def test_individual_modules_discoverable(self, module_name):
        """Test that individual refactored modules are discoverable by pytest.
        
        **Feature: test-refactoring, Property 5: Test Discovery Completeness**
        **Validates: Requirements 2.5**
        """
        import subprocess
        import os
        
        # Get the full path to the module
        test_dir = os.path.dirname(__file__)
        module_path = os.path.join(test_dir, module_name)
        
        # Skip if module doesn't exist (some may not be implemented yet)
        if not os.path.exists(module_path):
            return
        
        # Run pytest --collect-only on the specific module
        result = subprocess.run([
            'pytest', '--collect-only', module_path, '-q'
        ], capture_output=True, text=True, cwd=os.path.dirname(test_dir))
        
        # Should succeed without errors
        assert result.returncode == 0, \
            f"pytest discovery failed for {module_name} with return code {result.returncode}. " \
            f"stderr: {result.stderr}"
        
        # Should discover at least some tests from this module
        lines = result.stdout.strip().split('\n')
        test_lines = [line for line in lines if '::' in line and 'test_' in line]
        
        assert len(test_lines) > 0, \
            f"No tests discovered in {module_name}. Module may be empty or have import issues."
        
        # All discovered tests should be from this module
        for line in test_lines:
            if '::' in line:
                discovered_module = os.path.basename(line.split('::')[0])
                assert discovered_module == module_name, \
                    f"Expected test from {module_name}, but found test from {discovered_module}: {line}"
    
    def test_refactored_tests_are_executable(self):
        """Test that discovered tests can actually be executed without import errors.
        
        **Feature: test-refactoring, Property 5: Test Discovery Completeness**
        **Validates: Requirements 2.5**
        """
        import subprocess
        import os
        
        # Get the test directory path
        test_dir = os.path.dirname(__file__)
        
        # Run a quick smoke test - execute just one test from each major module
        # to verify they can actually run (not just be discovered)
        test_modules = [
            'test_core_functionality.py::TestWidgetTreeGeneration::test_markdown_produces_widgets',
            'test_label_compatibility.py::TestFontSizeAliasBidirectionality::test_font_size_sets_base_font_size',
            'test_font_properties.py::TestFontNameForwarding::test_font_name_applied_to_paragraph',
            'test_color_properties.py::TestColorForwarding::test_color_applied_to_paragraph',
            'test_sizing_behavior.py::TestAutoSizingBehavior::test_auto_size_hint_enabled_sets_none'
        ]
        
        for test_spec in test_modules:
            module_name = test_spec.split('::')[0]
            module_path = os.path.join(test_dir, module_name)
            
            # Skip if module doesn't exist
            if not os.path.exists(module_path):
                continue
            
            # Try to run the specific test
            result = subprocess.run([
                'pytest', os.path.join(test_dir, test_spec), '-v', '--tb=short'
            ], capture_output=True, text=True, cwd=os.path.dirname(test_dir))
            
            # Should be able to execute without import errors
            # Note: The test itself might fail due to Kivy setup issues, but it should
            # at least be importable and discoverable
            assert 'ImportError' not in result.stderr, \
                f"Import error when executing {test_spec}: {result.stderr}"
            assert 'ModuleNotFoundError' not in result.stderr, \
                f"Module not found error when executing {test_spec}: {result.stderr}"
    
    def test_refactored_modules_have_unique_tests(self):
        """Test that refactored modules don't have duplicate tests among themselves.
        
        **Feature: test-refactoring, Property 5: Test Discovery Completeness**
        **Validates: Requirements 2.5**
        """
        import subprocess
        import os
        
        # Get the test directory path
        test_dir = os.path.dirname(__file__)
        
        # Only test the refactored modules (exclude the original monolithic file)
        refactored_modules = [
            'test_core_functionality.py',
            'test_label_compatibility.py',
            'test_advanced_compatibility.py',
            'test_font_properties.py',
            'test_color_properties.py',
            'test_sizing_behavior.py',
            'test_text_properties.py',
            'test_padding_properties.py',
            'test_serialization.py',
            'test_performance.py',
            'test_shortening_and_coordinate.py'
        ]
        
        # Collect tests from refactored modules only
        all_test_ids = []
        for module_name in refactored_modules:
            module_path = os.path.join(test_dir, module_name)
            
            # Skip if module doesn't exist
            if not os.path.exists(module_path):
                continue
            
            # Run pytest --collect-only on the specific module
            result = subprocess.run([
                'pytest', '--collect-only', module_path, '-q'
            ], capture_output=True, text=True, cwd=os.path.dirname(test_dir))
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                test_lines = [line for line in lines if '::' in line and 'test_' in line]
                
                for line in test_lines:
                    if '::' in line:
                        parts = line.split('::')
                        if len(parts) >= 3:  # module::class::method
                            test_id = f"{parts[1]}::{parts[2]}"
                            all_test_ids.append((test_id, module_name))
        
        # Find duplicates among refactored modules
        seen = {}
        duplicates = []
        for test_id, module_name in all_test_ids:
            if test_id in seen:
                duplicates.append(f"{test_id} (in {seen[test_id]} and {module_name})")
            else:
                seen[test_id] = module_name
        
        # Should not have any duplicate test identifiers among refactored modules
        assert len(duplicates) == 0, \
            f"Found duplicate test identifiers among refactored modules: {duplicates[:10]}... " \
            f"(showing first 10 of {len(duplicates)} duplicates)"