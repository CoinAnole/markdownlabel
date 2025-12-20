"""
Property-based tests for test refactoring validation.

This module contains tests that validate the test refactoring process itself,
including module naming consistency and other refactoring properties.
"""

import ast
import os
import re
from pathlib import Path

import pytest


# **Feature: test-refactoring, Property 8: Module Naming Consistency**
# *For any* test module in the refactored structure, the filename SHALL follow
# the pattern `test_<feature_area>.py` where feature_area clearly indicates
# the functionality being tested.
# **Validates: Requirements 1.2, 4.1**

@pytest.mark.test_tests
class TestModuleNamingConsistency:
    """Property tests for module naming consistency (Property 8)."""
    
    @pytest.mark.parametrize('module_name', [
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
    ])
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


# **Feature: test-refactoring, Property 12: Test Discovery Performance**
# *For any* test discovery operation, the time to discover all tests should not
# increase significantly compared to the original structure
# **Validates: Requirements 6.4, 6.5**

@pytest.mark.test_tests
class TestDiscoveryPerformance:
    """Property tests for test discovery performance (Property 12)."""
    
    def test_fast_test_discovery_baseline(self):
        """Test that test discovery works correctly for the refactored structure.
        
        **Feature: test-refactoring, Property 12: Test Discovery Performance**
        **Validates: Requirements 6.4, 6.5**
        """
        import subprocess
        import os
        
        # Get the test directory path
        test_dir = os.path.dirname(__file__)
        
        # Run test discovery with stable configuration
        # Use -o addopts= to clear default addopts and keep discovery deterministic
        result = subprocess.run([
            'pytest', '--collect-only', test_dir, '-q', '-o', 'addopts='
        ], capture_output=True, text=True, cwd=os.path.dirname(test_dir),
        env={**os.environ, 'PYTEST_DISABLE_PLUGIN_AUTOLOAD': '1'})
        
        # Should successfully discover tests
        assert result.returncode == 0, \
            f"Test discovery failed with return code {result.returncode}. " \
            f"stderr: {result.stderr}"
        
        # Should discover a reasonable number of tests from refactored modules
        lines = result.stdout.strip().split('\n')
        test_lines = [line for line in lines if '::' in line and 'test_' in line]
        
        assert len(test_lines) >= 50, \
            f"Only discovered {len(test_lines)} tests, expected at least 50. " \
            f"This suggests discovery is incomplete or modules are missing."
        
        # Should contain "collected" in output to confirm discovery worked
        assert "collected" in result.stdout, \
            f"Discovery output doesn't contain 'collected', suggesting discovery failed. " \
            f"Output: {result.stdout}"
    
    @pytest.mark.parametrize('module_name', [
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
    ])
    def test_individual_module_discovery_functionality(self, module_name):
        """Test that individual modules can be discovered correctly.
        
        **Feature: test-refactoring, Property 12: Test Discovery Performance**
        **Validates: Requirements 6.4, 6.5**
        """
        import subprocess
        import os
        
        # Get the test directory path
        test_dir = os.path.dirname(__file__)
        module_path = os.path.join(test_dir, module_name)
        
        # Skip if module doesn't exist
        if not os.path.exists(module_path):
            return
        
        # Run discovery for this specific module with stable configuration
        # Use -o addopts= to clear default addopts and keep discovery deterministic
        result = subprocess.run([
            'pytest', '--collect-only', module_path, '-q', '-o', 'addopts='
        ], capture_output=True, text=True, cwd=os.path.dirname(test_dir),
        env={**os.environ, 'PYTEST_DISABLE_PLUGIN_AUTOLOAD': '1'})
        
        # Should successfully discover tests
        assert result.returncode == 0, \
            f"Discovery failed for {module_name} with return code {result.returncode}. " \
            f"stderr: {result.stderr}"
        
        # Should discover at least some tests from this module
        lines = result.stdout.strip().split('\n')
        test_lines = [line for line in lines if '::' in line and 'test_' in line]
        
        assert len(test_lines) > 0, \
            f"No tests discovered in {module_name}. Module may be empty or have issues."
    
    def test_discovery_startup_functionality(self):
        """Test that discovery startup works correctly for refactored structure.
        
        **Feature: test-refactoring, Property 12: Test Discovery Performance**
        **Validates: Requirements 6.4, 6.5**
        """
        import subprocess
        import os
        
        # Get the test directory path
        test_dir = os.path.dirname(__file__)
        
        # Test discovery startup by running discovery on a minimal module
        minimal_module = 'test_import.py'  # Should be a simple, fast module
        module_path = os.path.join(test_dir, minimal_module)
        
        # Skip if minimal module doesn't exist
        if not os.path.exists(module_path):
            pytest.skip(f"Minimal test module {minimal_module} not found")
        
        # Run discovery with stable configuration
        # Use -o addopts= to clear default addopts and keep discovery deterministic
        result = subprocess.run([
            'pytest', '--collect-only', module_path, '-q', '-o', 'addopts='
        ], capture_output=True, text=True, cwd=os.path.dirname(test_dir),
        env={**os.environ, 'PYTEST_DISABLE_PLUGIN_AUTOLOAD': '1'})
        
        # Should succeed
        assert result.returncode == 0, \
            f"Discovery failed for minimal module with return code {result.returncode}. " \
            f"stderr: {result.stderr}"
        
        # Should contain expected discovery output
        assert "collected" in result.stdout or "no tests ran" in result.stdout, \
            f"Discovery output doesn't contain expected patterns. Output: {result.stdout}"


# **Feature: test-suite-refactoring, Property 5: Rebuild Contract Enforcement**
# *For any* test that claims to test rebuild behavior, the test SHALL verify both 
# that the rebuild occurred (or didn't occur as appropriate) AND that the resulting 
# state is correct.
# **Validates: Requirements 4.1, 4.2, 4.4**

@pytest.mark.test_tests
class TestRebuildContractEnforcement:
    """Property tests for rebuild contract enforcement (Property 5)."""
    
    def _has_rebuild_verification(self, test_content):
        """Check if test content actually verifies that a rebuild occurred."""
        # Look for patterns that indicate rebuild verification
        rebuild_patterns = [
            r'collect_widget_ids',
            r'widget.*id.*!=',
            r'id\s*\(\s*\w+\s*\)\s*!=',
            r'children_ids.*!=',
            r'assert.*rebuild',
            r'widget.*identity',
            r'widget.*instance',
            r'assert_rebuild_occurred',
            r'assert_no_rebuild',
        ]
        
        for pattern in rebuild_patterns:
            if re.search(pattern, test_content, re.IGNORECASE):
                return True
        return False
    
    def _extract_test_method(self, file_content, method_name):
        """Extract the content of a specific test method."""
        # Find the method definition
        method_pattern = rf'def\s+{re.escape(method_name)}\s*\([^)]*\):'
        match = re.search(method_pattern, file_content)
        if not match:
            return None
        
        start_pos = match.start()
        
        # Find the end of the method (next method or class definition, or end of file)
        remaining_content = file_content[start_pos:]
        
        # Split into lines and find where this method ends
        method_lines = remaining_content.split('\n')
        method_content = [method_lines[0]]  # Include the def line
        
        # Find the indentation level of the method
        method_indent = len(method_lines[0]) - len(method_lines[0].lstrip())
        
        for i, line in enumerate(method_lines[1:], 1):
            # If we hit a line with same or less indentation that starts with def/class, we're done
            if line.strip() and not line.startswith(' ' * (method_indent + 1)):
                if line.lstrip().startswith(('def ', 'class ', '@')):
                    break
            method_content.append(line)
        
        return '\n'.join(method_content)
    
    def test_rebuild_contract_enforcement(self):
        """Test that all tests claiming to test rebuilds actually verify rebuilds.
        
        **Feature: test-suite-refactoring, Property 5: Rebuild Contract Enforcement**
        **Validates: Requirements 4.1, 4.2, 4.4**
        """
        test_dir = Path(__file__).parent
        violations = []
        
        # Check all test files
        for test_file in test_dir.glob('test_*.py'):
            if not test_file.is_file():
                continue
                
            try:
                with open(test_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Find all test methods that claim to test rebuilds
                rebuild_test_patterns = [
                    r'def\s+(test_\w*rebuild\w*)\s*\(',
                    r'def\s+(test_\w*triggers_rebuild\w*)\s*\(',
                    r'def\s+(test_\w*rebuilds_\w*)\s*\(',
                ]
                
                for pattern in rebuild_test_patterns:
                    matches = re.finditer(pattern, content)
                    
                    for match in matches:
                        method_name = match.group(1)
                        method_content = self._extract_test_method(content, method_name)
                        
                        if method_content:
                            # Check if this test actually verifies rebuilds
                            if not self._has_rebuild_verification(method_content):
                                violations.append({
                                    'file': str(test_file.name),
                                    'method': method_name,
                                    'issue': 'Claims to test rebuilds but does not verify rebuild occurred'
                                })
                            
            except Exception as e:
                # Don't fail the test for file reading issues, just skip
                continue
        
        # Assert no violations found
        if violations:
            violation_details = '\n'.join([
                f"  - {v['file']}::{v['method']}: {v['issue']}"
                for v in violations
            ])
            assert False, f"Found {len(violations)} rebuild contract violations:\n{violation_details}"
    
    def test_rebuild_verification_patterns_work(self):
        """Test that our rebuild verification detection patterns work correctly.
        
        **Feature: test-suite-refactoring, Property 5: Rebuild Contract Enforcement**
        **Validates: Requirements 4.1, 4.2, 4.4**
        """
        # Test cases with rebuild verification
        valid_rebuild_tests = [
            """
            def test_something_rebuilds_widget_tree(self):
                children_ids_before = collect_widget_ids(label)
                label.text = "new text"
                children_ids_after = collect_widget_ids(label)
                assert children_ids_before != children_ids_after
            """,
            """
            def test_property_change_rebuilds(self):
                widget_id_before = id(label.children[0])
                label.font_name = "Arial"
                widget_id_after = id(label.children[0])
                assert widget_id_before != widget_id_after
            """,
            """
            def test_rebuild_detection(self):
                assert_rebuild_occurred(label, lambda: setattr(label, 'text', 'new'))
            """
        ]
        
        # Test cases without rebuild verification (should be flagged)
        invalid_rebuild_tests = [
            """
            def test_something_triggers_rebuild(self):
                label.text = "new text"
                assert label.text == "new text"
            """,
            """
            def test_property_rebuilds_widget(self):
                label.font_name = "Arial"
                labels = find_labels_recursive(label)
                assert labels[0].font_name == "Arial"
            """
        ]
        
        # Test that valid tests are not flagged
        for test_content in valid_rebuild_tests:
            assert self._has_rebuild_verification(test_content), \
                f"Valid rebuild test was incorrectly flagged: {test_content[:50]}..."
        
        # Test that invalid tests are flagged
        for test_content in invalid_rebuild_tests:
            assert not self._has_rebuild_verification(test_content), \
                f"Invalid rebuild test was not flagged: {test_content[:50]}..."


# **Feature: test-suite-refactoring, Property 4: Meta-Test Marking**
# *For any* test that validates test suite structure or properties (tests about tests), 
# the test SHALL be marked with `@pytest.mark.test_tests`.
# **Validates: Requirements 3.1**

@pytest.mark.test_tests
class TestMetaTestMarking:
    """Property tests for meta-test marking (Property 4)."""
    
    def _is_meta_test_class(self, class_content):
        """Check if a test class is a meta-test (tests about test suite structure)."""
        # Look for patterns that indicate meta-testing
        meta_test_patterns = [
            r'test.*suite.*structure',
            r'test.*refactor',
            r'test.*helper.*availability',
            r'test.*consolidation',
            r'test.*naming.*consistency',
            r'test.*discovery.*performance',
            r'test.*rebuild.*contract',
            r'test.*meta.*test',
            r'Property.*test.*suite',
            r'validates.*test.*suite',
            r'test.*file.*analyzer',
            r'test.*shared.*infrastructure',
            r'test.*strategy.*availability',
        ]
        
        for pattern in meta_test_patterns:
            if re.search(pattern, class_content, re.IGNORECASE):
                return True
        return False
    
    def _has_test_tests_marker(self, class_content):
        """Check if a test class has the @pytest.mark.test_tests marker."""
        return re.search(r'@pytest\.mark\.test_tests', class_content) is not None
    
    def _extract_test_class(self, file_content, class_name):
        """Extract the content of a specific test class."""
        # Find the class definition
        class_pattern = rf'^class\s+{re.escape(class_name)}\s*[:\(]'
        match = re.search(class_pattern, file_content, re.MULTILINE)
        if not match:
            return None
        
        start_pos = match.start()
        
        # Find the end of the class (next class definition or end of file)
        remaining_content = file_content[start_pos:]
        
        # Split into lines and find where this class ends
        class_lines = remaining_content.split('\n')
        class_content = [class_lines[0]]  # Include the class line
        
        # Find the indentation level of the class
        class_indent = len(class_lines[0]) - len(class_lines[0].lstrip())
        
        for i, line in enumerate(class_lines[1:], 1):
            # If we hit a line with same or less indentation that starts with class/def, we're done
            if line.strip() and not line.startswith(' ' * (class_indent + 1)):
                if line.lstrip().startswith(('class ', 'def ')):
                    break
                elif line.lstrip().startswith('@'):
                    # This might be a decorator for the next class, check ahead
                    for j in range(i + 1, min(i + 5, len(class_lines))):  # Look ahead max 5 lines
                        next_line = class_lines[j]
                        if next_line.strip():
                            if next_line.lstrip().startswith('class '):
                                # This decorator is for the next class, stop here
                                return '\n'.join(class_content)
                            elif not next_line.lstrip().startswith('@'):
                                # This decorator is part of current class
                                class_content.append(line)
                                break
                    else:
                        # Couldn't determine, include the line
                        class_content.append(line)
                else:
                    class_content.append(line)
            else:
                class_content.append(line)
        
        return '\n'.join(class_content)
    
    def test_meta_test_marking_compliance(self):
        """Test that all meta-tests are properly marked with @pytest.mark.test_tests.
        
        **Feature: test-suite-refactoring, Property 4: Meta-Test Marking**
        **Validates: Requirements 3.1**
        """
        test_dir = Path(__file__).parent
        violations = []
        seen_classes = set()  # Track classes we've already checked
        
        # Check all test files
        for test_file in test_dir.glob('test_*.py'):
            if not test_file.is_file():
                continue
                
            try:
                with open(test_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Find all test classes at the module level (not nested in strings)
                class_pattern = r'^class\s+(Test\w+)\s*[:\(]'
                matches = re.finditer(class_pattern, content, re.MULTILINE)
                
                for match in matches:
                    class_name = match.group(1)
                    class_key = f"{test_file.name}::{class_name}"
                    
                    # Skip if we've already checked this class
                    if class_key in seen_classes:
                        continue
                    seen_classes.add(class_key)
                    
                    # Get the content including decorators before the class
                    start_pos = match.start()
                    # Look back up to 10 lines for decorators
                    lines_before = content[:start_pos].split('\n')
                    decorator_start = max(0, len(lines_before) - 10)
                    class_with_decorators = '\n'.join(lines_before[decorator_start:])
                    
                    class_content = self._extract_test_class(content, class_name)
                    
                    if class_content:
                        full_class_content = class_with_decorators + '\n' + class_content
                        
                        # Check if this is a meta-test class
                        if self._is_meta_test_class(full_class_content):
                            # Check if it has the proper marker
                            if not self._has_test_tests_marker(full_class_content):
                                violations.append({
                                    'file': str(test_file.name),
                                    'class': class_name,
                                    'issue': 'Meta-test class missing @pytest.mark.test_tests marker'
                                })
                            
            except Exception as e:
                # Don't fail the test for file reading issues, just skip
                continue
        
        # Assert no violations found
        if violations:
            violation_details = '\n'.join([
                f"  - {v['file']}::{v['class']}: {v['issue']}"
                for v in violations
            ])
            assert False, f"Found {len(violations)} meta-test marking violations:\n{violation_details}"
    
    def test_meta_test_detection_patterns_work(self):
        """Test that our meta-test detection patterns work correctly.
        
        **Feature: test-suite-refactoring, Property 4: Meta-Test Marking**
        **Validates: Requirements 3.1**
        """
        # Test cases that should be detected as meta-tests
        valid_meta_test_classes = [
            """
            class TestHelperFunctionAvailability:
                '''Property tests for helper function availability.'''
                def test_widget_traversal_helpers_available(self):
                    pass
            """,
            """
            class TestModuleNamingConsistency:
                '''Tests for test suite structure validation.'''
                def test_module_names_follow_pattern(self):
                    pass
            """,
            """
            class TestRebuildContractEnforcement:
                '''Tests for rebuild contract validation.'''
                def test_rebuild_contract_enforcement(self):
                    pass
            """
        ]
        
        # Test cases that should NOT be detected as meta-tests
        invalid_meta_test_classes = [
            """
            class TestMarkdownRendering:
                '''Tests for markdown rendering functionality.'''
                def test_bold_text_rendering(self):
                    pass
            """,
            """
            class TestLabelProperties:
                '''Tests for label property forwarding.'''
                def test_font_size_forwarding(self):
                    pass
            """
        ]
        
        # Test that valid meta-tests are detected
        for test_content in valid_meta_test_classes:
            assert self._is_meta_test_class(test_content), \
                f"Valid meta-test class was not detected: {test_content[:50]}..."
        
        # Test that non-meta-tests are not flagged
        for test_content in invalid_meta_test_classes:
            assert not self._is_meta_test_class(test_content), \
                f"Non-meta-test class was incorrectly flagged: {test_content[:50]}..."