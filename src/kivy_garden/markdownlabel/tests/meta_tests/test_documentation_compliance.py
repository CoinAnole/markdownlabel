"""Tests for documentation compliance of max_examples values.

This module tests that custom max_examples values are properly documented
according to the optimization guidelines.
"""

import re
from pathlib import Path
import pytest
from hypothesis import given, settings
import hypothesis.strategies as st


@pytest.mark.test_tests
class TestDocumentationCompliance:
    """Test documentation compliance for max_examples values."""

    def test_custom_values_are_documented(self):
        """**Feature: test-performance-optimization, Custom values are documented**

        For any property test using custom max_examples values that deviate from
        standard patterns, the rationale SHALL be documented in test comments.
        """
        test_dir = Path(__file__).parent.parent  # Go up from meta_tests to tests
        undocumented_tests = []

        # Files to skip - these contain intentional test fixtures for testing
        # the optimization tools themselves
        skip_files = {
            'test_documentation_compliance.py',  # This file (in meta_tests)
            'test_comment_format.py',  # Test fixtures for comment format validation (in meta_tests)
            'test_file_analyzer.py',  # Test fixtures for file analyzer (in meta_tests)
            'test_comment_standardizer.py',  # Test fixtures for comment standardizer (in meta_tests)
            'test_assertion_analyzer.py',  # Test fixtures for assertion analyzer (in meta_tests)
            'test_code_duplication_minimization.py',  # Test fixtures for code duplication (in meta_tests)
            'test_coverage_preservation.py',  # Test fixtures for coverage (in meta_tests)
            'test_duplicate_detector.py',  # Test fixtures for duplicate detector (in meta_tests)
            'test_helper_availability.py',  # Test fixtures for helper availability (in meta_tests)
            'test_naming_convention_validator.py',  # Test fixtures for naming validation (in meta_tests)
            'test_strategy_classification.py',  # Test fixtures for strategy classification (in meta_tests)
            'test_test_file_parser.py',  # Test fixtures for test file parser (in meta_tests)
        }

        for test_file in test_dir.glob('test_*.py'):
            if test_file.name in skip_files:
                continue

            undocumented = self._check_file_documentation(test_file)
            undocumented_tests.extend(undocumented)

        if undocumented_tests:
            error_msg = "Found tests with undocumented custom max_examples values:\n"
            for file_path, test_name, max_examples in undocumented_tests:
                error_msg += f"  - {file_path}:{test_name} (max_examples={max_examples})\n"
            error_msg += "\nAll custom max_examples values should have explanatory comments."

            assert False, error_msg

    def _check_file_documentation(self, file_path):
        """Check a single file for undocumented custom max_examples values."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except (IOError, UnicodeDecodeError):
            return []  # Skip files we can't read
        lines = content.split('\n')
        undocumented = []

        i = 0
        while i < len(lines):
            line = lines[i].strip()

            # Look for @settings with max_examples
            settings_match = re.search(r'@settings\(.*?max_examples\s*=\s*(\d+)', line)
            if settings_match:
                max_examples = int(settings_match.group(1))

                # Check if this is a custom value that needs documentation
                if self._is_custom_value(max_examples):
                    # Look for explanatory comment in previous lines
                    has_comment = self._has_explanatory_comment(lines, i)

                    if not has_comment:
                        # Find the test function name
                        test_name = self._find_test_name(lines, i)
                        undocumented.append((file_path, test_name, max_examples))

            i += 1

        return undocumented

    def _is_custom_value(self, max_examples):
        """Check if max_examples value is custom and needs documentation."""
        # Standard values that don't need documentation
        standard_values = {2, 3, 4, 5, 6, 7, 8, 9, 10, 100}

        # Values that are clearly custom and should be documented
        return max_examples not in standard_values

    def _has_explanatory_comment(self, lines, settings_line_idx):
        """Check if there's an explanatory comment before the @settings line."""
        # Look at the few lines before @settings
        for i in range(max(0, settings_line_idx - 3), settings_line_idx):
            line = lines[i].strip()
            if line.startswith('#'):
                # Check if comment explains max_examples rationale
                comment_text = line.lower()
                explanation_keywords = [
                    'examples', 'strategy', 'complex', 'finite', 'performance',
                    'coverage', 'constraint', 'generation', 'combination'
                ]

                if any(keyword in comment_text for keyword in explanation_keywords):
                    return True
        return False

    def _find_test_name(self, lines, settings_line_idx):
        """Find the test function name near the @settings line."""
        # Look for def test_* in the next few lines
        for i in range(settings_line_idx, min(len(lines), settings_line_idx + 5)):
            line = lines[i].strip()
            if line.startswith('def test_'):
                match = re.search(r'def\s+(test_\w+)', line)
                if match:
                    return match.group(1)

        return "unknown_test"

    @given(st.integers(min_value=11, max_value=200))
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_custom_value_detection_property(self, custom_value):
        """Test that _is_custom_value correctly identifies custom max_examples values
        outside the standard set."""
        # Test that our detection logic correctly identifies custom values
        is_custom = self._is_custom_value(custom_value)

        # Values outside standard range should be detected as custom
        standard_values = {2, 3, 4, 5, 6, 7, 8, 9, 10, 100}
        expected_custom = custom_value not in standard_values
        assert is_custom == expected_custom, \
            f"Custom value detection failed for {custom_value}: expected {expected_custom}, got {is_custom}"

    @given(st.text(min_size=1, max_size=100))
    # Complex strategy: 15 examples (adequate coverage)
    @settings(max_examples=15, deadline=None)
    def test_comment_detection_property(self, comment_text):
        """Test that _has_explanatory_comment correctly identifies comments containing
        explanation keywords."""
        # Create mock lines with comment
        lines = [
            "    @given(st.booleans())",
            f"    # {comment_text}",
            "    @settings(max_examples=25, deadline=None)",
            "    def test_example(self):",
            "        pass"
        ]

        # Test comment detection
        has_comment = self._has_explanatory_comment(lines, 2)  # @settings is at index 2

        # Check if comment contains explanation keywords
        explanation_keywords = [
            'examples', 'strategy', 'complex', 'finite', 'performance',
            'coverage', 'constraint', 'generation', 'combination'
        ]

        expected_has_comment = any(keyword in comment_text.lower() for keyword in explanation_keywords)

        assert has_comment == expected_has_comment, \
            f"Comment detection failed for '{comment_text}': expected " \
            f"{expected_has_comment}, got {has_comment}"
