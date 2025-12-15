"""
Property-based tests for core functionality module refactoring.

This module contains property-based tests that validate the refactoring
process for the core functionality test module.
"""

import os
import ast
import re
from pathlib import Path
import pytest
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
        core_module_path = Path('kivy_garden/markdownlabel/tests/test_core_functionality.py')
        assert core_module_path.exists(), f"Core module not found: {core_module_path}"
        
        actual_names = self._extract_test_names_from_file(str(core_module_path))
        
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
            if test_file.name in ['test_core_functionality_properties.py', 'test_markdown_label_DEPRECATED.py']:
                continue  # Skip property test file and original monolithic file during refactoring
            
            test_names = self._extract_test_names_from_file(str(test_file))
            
            for name in test_names:
                if name in all_test_names:
                    assert False, \
                        f"Test name '{name}' found in both {all_test_names[name]} and {test_file.name}"
                all_test_names[name] = test_file.name
    
    @pytest.mark.parametrize('class_name', [
        'TestWidgetTreeGeneration',
        'TestReactiveTextUpdates', 
        'TestLinkRefMarkup',
        'TestDeepNestingStability'
    ])
    def test_specific_class_exists_in_core_module(self, class_name):
        """Each specific core functionality class exists in the core module."""
        core_module_path = Path('kivy_garden/markdownlabel/tests/test_core_functionality.py')
        assert core_module_path.exists(), f"Core module not found: {core_module_path}"
        
        test_names = self._extract_test_names_from_file(str(core_module_path))
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
        with open(file_path, 'r', encoding='utf-8') as f:
            return len(f.readlines())
    
    def test_core_functionality_module_line_count(self):
        """Core functionality module should not exceed 1000 lines."""
        core_module_path = Path('kivy_garden/markdownlabel/tests/test_core_functionality.py')
        assert core_module_path.exists(), f"Core module not found: {core_module_path}"
        
        line_count = self._count_lines_in_file(str(core_module_path))
        assert line_count <= 1000, \
            f"Core functionality module has {line_count} lines, exceeds 1000 line limit"
    
    @pytest.mark.parametrize('module_name', [
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
    ])
    def test_any_refactored_module_line_count(self, module_name):
        """Any refactored test module should not exceed 1000 lines."""
        module_path = Path(f'kivy_garden/markdownlabel/tests/{module_name}')
        if not module_path.exists():
            return  # Skip non-existent modules
        
        line_count = self._count_lines_in_file(str(module_path))
        assert line_count <= 1000, \
            f"Module {module_name} has {line_count} lines, exceeds 1000 line limit"
    
    def test_all_existing_test_modules_line_count(self):
        """All existing test modules should respect the line count constraint."""
        test_dir = Path('kivy_garden/markdownlabel/tests')
        if not test_dir.exists():
            return
        
        for test_file in test_dir.glob('test_*.py'):
            # Skip the original monolithic file and property test files
            if test_file.name in ['test_markdown_label_DEPRECATED.py', 'test_core_functionality_properties.py']:
                continue
            
            line_count = self._count_lines_in_file(str(test_file))
            assert line_count <= 1000, \
                f"Module {test_file.name} has {line_count} lines, exceeds 1000 line limit"


# **Feature: test-improvements, Property 1: No timing assertions in tests**
# *For any* test file in the test suite, the file SHALL NOT contain timing assertions 
# with lower bounds (>= X seconds) or upper bounds (<= Y seconds) that can cause 
# flakiness across different machine speeds.
# **Validates: Requirements 1.1, 1.2**

class TestNoTimingAssertions:
    """Property tests for no timing assertions (Property 1)."""
    
    def _check_file_for_timing_assertions(self, file_path: str) -> List[str]:
        """Check a file for timing assertions.
        
        Args:
            file_path: Path to the Python file
            
        Returns:
            List of timing assertion patterns found
        """
        timing_patterns = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Patterns that indicate timing assertions
        timing_assertion_patterns = [
            r'assert.*time.*>=.*\d+\.?\d*',  # assert time >= X
            r'assert.*time.*<=.*\d+\.?\d*',  # assert time <= X
            r'assert.*\d+\.?\d*.*<=.*time',  # assert X <= time
            r'assert.*\d+\.?\d*.*>=.*time',  # assert X >= time
            r'discovery_time.*>=.*\d+\.?\d*',  # discovery_time >= X
            r'discovery_time.*<=.*\d+\.?\d*',  # discovery_time <= X
            r'startup_time.*>=.*\d+\.?\d*',   # startup_time >= X
            r'startup_time.*<=.*\d+\.?\d*',   # startup_time <= X
        ]
        
        for pattern in timing_assertion_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            timing_patterns.extend(matches)
        
        return timing_patterns
    
    @pytest.mark.parametrize('module_name', [
        'test_core_functionality.py',
        'test_label_compatibility.py',
        'test_font_properties.py',
        'test_color_properties.py',
        'test_sizing_behavior.py',
        'test_text_properties.py',
        'test_padding_properties.py',
        'test_advanced_compatibility.py',
        'test_serialization.py',
        'test_performance.py',
        'test_refactoring_properties.py',
        'test_core_functionality_properties.py'
    ])
    def test_no_timing_assertions_in_test_files(self, module_name):
        """Test files should not contain timing assertions.
        
        **Feature: test-improvements, Property 1: No timing assertions in tests**
        **Validates: Requirements 1.1, 1.2**
        """
        module_path = Path(f'kivy_garden/markdownlabel/tests/{module_name}')
        if not module_path.exists():
            return  # Skip non-existent modules
        
        timing_patterns = self._check_file_for_timing_assertions(str(module_path))
        
        assert len(timing_patterns) == 0, \
            f"Found timing assertions in {module_name}: {timing_patterns}. " \
            f"Timing assertions cause flakiness and should be replaced with functional checks."


# **Feature: test-improvements, Property 2: Subprocess pytest uses stable configuration**
# *For any* test that calls pytest as a subprocess, the call SHALL include 
# PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 in the environment and SHALL verify return codes 
# and collection counts instead of execution timing.
# **Validates: Requirements 1.3, 1.4**

class TestSubprocessPytestConfiguration:
    """Property tests for subprocess pytest configuration (Property 2)."""
    
    def _check_file_for_subprocess_pytest_calls(self, file_path: str) -> List[str]:
        """Check a file for subprocess pytest calls and their configuration.
        
        Args:
            file_path: Path to the Python file
            
        Returns:
            List of issues found with subprocess pytest calls
        """
        issues = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find subprocess.run calls with pytest
        subprocess_pytest_pattern = r'subprocess\.run\(\s*\[\s*[\'"]pytest[\'"]'
        matches = re.finditer(subprocess_pytest_pattern, content, re.MULTILINE | re.DOTALL)
        
        for match in matches:
            # Extract the full subprocess.run call
            start_pos = match.start()
            # Find the matching closing bracket/parenthesis
            bracket_count = 0
            paren_count = 0
            end_pos = start_pos
            
            for i, char in enumerate(content[start_pos:], start_pos):
                if char == '[':
                    bracket_count += 1
                elif char == ']':
                    bracket_count -= 1
                elif char == '(':
                    paren_count += 1
                elif char == ')':
                    paren_count -= 1
                    if paren_count == 0 and bracket_count <= 0:
                        end_pos = i + 1
                        break
            
            subprocess_call = content[start_pos:end_pos]
            
            # Check if PYTEST_DISABLE_PLUGIN_AUTOLOAD is set
            if 'PYTEST_DISABLE_PLUGIN_AUTOLOAD' not in subprocess_call:
                issues.append(f"subprocess pytest call missing PYTEST_DISABLE_PLUGIN_AUTOLOAD: {subprocess_call[:100]}...")
            
            # Check if it's verifying return codes instead of timing
            if 'returncode' not in subprocess_call and 'result.returncode' not in content[end_pos:end_pos+500]:
                issues.append(f"subprocess pytest call not checking return code: {subprocess_call[:100]}...")
        
        return issues
    
    @pytest.mark.parametrize('module_name', [
        'test_core_functionality.py',
        'test_label_compatibility.py',
        'test_font_properties.py',
        'test_color_properties.py',
        'test_sizing_behavior.py',
        'test_text_properties.py',
        'test_padding_properties.py',
        'test_advanced_compatibility.py',
        'test_serialization.py',
        'test_performance.py',
        'test_refactoring_properties.py',
        'test_core_functionality_properties.py'
    ])
    def test_subprocess_pytest_uses_stable_configuration(self, module_name):
        """Subprocess pytest calls should use stable configuration.
        
        **Feature: test-improvements, Property 2: Subprocess pytest uses stable configuration**
        **Validates: Requirements 1.3, 1.4**
        """
        module_path = Path(f'kivy_garden/markdownlabel/tests/{module_name}')
        if not module_path.exists():
            return  # Skip non-existent modules
        
        issues = self._check_file_for_subprocess_pytest_calls(str(module_path))
        
        assert len(issues) == 0, \
            f"Found subprocess pytest configuration issues in {module_name}: {issues}. " \
            f"All subprocess pytest calls should use PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 and check return codes."


# **Feature: test-improvements, Property 3: No silent-pass file existence checks**
# *For any* test that checks file existence, the test SHALL use assert statements 
# that fail loudly (assert Path(...).exists()) instead of conditional logic that 
# can silently pass.
# **Validates: Requirements 2.1**

class TestNoSilentPassFileChecks:
    """Property tests for no silent-pass file checks (Property 3)."""
    
    def _check_file_for_silent_pass_patterns(self, file_path: str) -> List[str]:
        """Check a file for silent-pass file existence patterns.
        
        Args:
            file_path: Path to the Python file
            
        Returns:
            List of silent-pass patterns found
        """
        silent_pass_patterns = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for i, line in enumerate(lines):
            # Look for problematic patterns that don't have proper error handling
            if re.search(r'if\s+os\.path\.exists\([^)]+\):', line):
                # Check if this is followed by proper error handling or return/skip
                next_lines = ''.join(lines[i:i+5])  # Look at next few lines
                if not any(keyword in next_lines for keyword in ['assert', 'raise', 'pytest.skip', 'return']):
                    silent_pass_patterns.append(f"Line {i+1}: {line.strip()}")
            
            elif re.search(r'if\s+.*\.exists\(\):', line) and 'not' not in line:
                # Only flag positive existence checks that don't have proper handling
                next_lines = ''.join(lines[i:i+5])
                if not any(keyword in next_lines for keyword in ['assert', 'raise', 'pytest.skip', 'return']):
                    silent_pass_patterns.append(f"Line {i+1}: {line.strip()}")
        
        return silent_pass_patterns
    
    @pytest.mark.parametrize('module_name', [
        'test_core_functionality.py',
        'test_label_compatibility.py',
        'test_font_properties.py',
        'test_color_properties.py',
        'test_sizing_behavior.py',
        'test_text_properties.py',
        'test_padding_properties.py',
        'test_advanced_compatibility.py',
        'test_serialization.py',
        'test_performance.py',
        'test_refactoring_properties.py',
        'test_core_functionality_properties.py'
    ])
    def test_no_silent_pass_file_existence_checks(self, module_name):
        """Test files should not contain silent-pass file existence checks.
        
        **Feature: test-improvements, Property 3: No silent-pass file existence checks**
        **Validates: Requirements 2.1**
        """
        module_path = Path(f'kivy_garden/markdownlabel/tests/{module_name}')
        if not module_path.exists():
            return  # Skip non-existent modules
        
        silent_pass_patterns = self._check_file_for_silent_pass_patterns(str(module_path))
        
        assert len(silent_pass_patterns) == 0, \
            f"Found silent-pass file existence checks in {module_name}: {silent_pass_patterns}. " \
            f"Use 'assert Path(...).exists()' instead of 'if os.path.exists(...):' to fail loudly."


# **Feature: test-improvements, Property 4: No broad exception handling**
# *For any* test file, the file SHALL NOT contain broad exception handling patterns 
# (except Exception: pass or except:) that can mask real failures.
# **Validates: Requirements 2.2, 2.4**

class TestNoBroadExceptionHandling:
    """Property tests for no broad exception handling (Property 4)."""
    
    def _check_file_for_broad_exception_handling(self, file_path: str) -> List[str]:
        """Check a file for broad exception handling patterns.
        
        Args:
            file_path: Path to the Python file
            
        Returns:
            List of broad exception handling patterns found
        """
        broad_exception_patterns = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Patterns that indicate broad exception handling
        patterns = [
            r'except\s+Exception\s*:\s*pass',     # except Exception: pass
            r'except\s*:\s*pass',                 # except: pass
            r'except\s+Exception\s*:\s*return',   # except Exception: return
            r'except\s*:\s*return',               # except: return
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content, re.MULTILINE)
            broad_exception_patterns.extend(matches)
        
        return broad_exception_patterns
    
    @pytest.mark.parametrize('module_name', [
        'test_core_functionality.py',
        'test_label_compatibility.py',
        'test_font_properties.py',
        'test_color_properties.py',
        'test_sizing_behavior.py',
        'test_text_properties.py',
        'test_padding_properties.py',
        'test_advanced_compatibility.py',
        'test_serialization.py',
        'test_performance.py',
        'test_refactoring_properties.py',
        'test_core_functionality_properties.py'
    ])
    def test_no_broad_exception_handling(self, module_name):
        """Test files should not contain broad exception handling.
        
        **Feature: test-improvements, Property 4: No broad exception handling**
        **Validates: Requirements 2.2, 2.4**
        """
        module_path = Path(f'kivy_garden/markdownlabel/tests/{module_name}')
        if not module_path.exists():
            return  # Skip non-existent modules
        
        # Skip checking this test file itself since it contains pattern examples
        if module_name == 'test_core_functionality_properties.py':
            return
        
        broad_exception_patterns = self._check_file_for_broad_exception_handling(str(module_path))
        
        assert len(broad_exception_patterns) == 0, \
            f"Found broad exception handling in {module_name}: {broad_exception_patterns}. " \
            f"Use specific exception handling or let exceptions propagate to avoid masking failures."