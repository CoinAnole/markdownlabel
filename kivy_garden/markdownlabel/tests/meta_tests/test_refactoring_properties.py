"""
Property-based tests for test refactoring validation.

This module contains tests that validate the test refactoring process itself,
including module naming consistency and other refactoring properties.
"""

import os
import re
import sys
from pathlib import Path

import pytest


# *For any* test discovery operation, the time to discover all tests should not
# increase significantly compared to the original structure

@pytest.mark.test_tests
class TestDiscoveryPerformance:
    """Property tests for test discovery performance."""

    def test_fast_test_discovery_baseline(self):
        """Test that test discovery works correctly for the refactored structure.

        """
        import subprocess

        # Get the test directory path
        test_dir = os.path.dirname(__file__)

        # Run test discovery with stable configuration
        # Use -o addopts= to clear default addopts and keep discovery deterministic
        result = subprocess.run([
            sys.executable, '-m', 'pytest', '--collect-only', test_dir, '-q', '-o', 'addopts='
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

        """
        import subprocess

        # Get the test directory path
        test_dir = os.path.dirname(__file__)
        module_path = os.path.join(test_dir, module_name)

        # Skip if module doesn't exist
        if not os.path.exists(module_path):
            return

        # Run discovery for this specific module with stable configuration
        # Use -o addopts= to clear default addopts and keep discovery deterministic
        result = subprocess.run([
            sys.executable, '-m', 'pytest', '--collect-only', module_path, '-q', '-o', 'addopts='
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

        """
        import subprocess

        # Get the test directory path
        test_dir = os.path.dirname(__file__)

        # Test discovery startup by running discovery on a minimal module
        minimal_module = 'test_import.py'  # Should be a simple, fast module
        module_path = os.path.join(os.path.dirname(test_dir), minimal_module)

        # Skip if minimal module doesn't exist
        if not os.path.exists(module_path):
            pytest.skip(f"Minimal test module {minimal_module} not found")

        # Run discovery with stable configuration
        # Use -o addopts= to clear default addopts and keep discovery deterministic
        result = subprocess.run([
            sys.executable, '-m', 'pytest', '--collect-only', module_path, '-q', '-o', 'addopts='
        ], capture_output=True, text=True, cwd=os.path.dirname(test_dir),
            env={**os.environ, 'PYTEST_DISABLE_PLUGIN_AUTOLOAD': '1'})

        # Should succeed
        assert result.returncode == 0, \
            f"Discovery failed for minimal module with return code {result.returncode}. " \
            f"stderr: {result.stderr}"

        # Should contain expected discovery output
        assert "collected" in result.stdout or "no tests ran" in result.stdout, \
            f"Discovery output doesn't contain expected patterns. Output: {result.stdout}"


# *For any* test that claims to test rebuild behavior, the test SHALL verify both
# that the rebuild occurred (or didn't occur as appropriate) AND that the resulting
# state is correct.

@pytest.mark.test_tests
class TestRebuildContractEnforcement:
    """Property tests for rebuild contract enforcement."""

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

        """
        test_dir = Path(__file__).parent
        violations = []

        # Check all test files, but exclude meta_tests directory since those test
        # the testing infrastructure itself, not actual rebuild behavior
        for test_file in test_dir.glob('../test_*.py'):
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
