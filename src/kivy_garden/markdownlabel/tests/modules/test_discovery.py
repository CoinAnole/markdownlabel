"""
Test discovery utility for finding property-based test functions.

This module provides a unified implementation for discovering property-based
test functions in Python test files, extracting metadata about test functions
including their location, decorators, and max_examples configuration.

This consolidates duplicate test discovery logic from multiple modules:
- modules/file_parser.py
- modules/comment_manager.py
- modules/optimization_detector.py
"""

import re
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class PropertyTest:
    """Represents a property-based test function with its metadata.

    This dataclass captures all information needed by the various test
    analysis and optimization modules that use test discovery.

    Attributes:
        name: The name of the test function (e.g., "test_example")
        start_line: The line number (1-based) where the function definition starts
        end_line: The line number (1-based) where the function ends
        max_examples: The max_examples value from @settings decorator, if present
        decorator_start_line: The line number (0-based) where the @given decorator starts
        has_ci_optimization: Whether the test uses CI-optimized max_examples
    """
    name: str
    start_line: int
    end_line: int
    max_examples: Optional[int]
    decorator_start_line: int
    has_ci_optimization: bool = False


def find_property_tests(content: str) -> List[PropertyTest]:
    """Find all property-based test functions in the content.

    This function uses a regex-based approach to reliably detect property-based
    test functions that use the @given decorator from Hypothesis. It handles:
    - Multi-line @given decorators
    - @settings decorators with max_examples
    - Conditional max_examples expressions for CI optimization
    - Proper function end detection based on indentation

    Args:
        content: The content of a Python test file as a string

    Returns:
        List of PropertyTest objects containing test metadata

    Example:
        >>> content = '''
        ... @given(st.integers())
        ... @settings(max_examples=100)
        ... def test_example(x):
        ...     assert x > 0
        ... '''
        >>> tests = find_property_tests(content)
        >>> len(tests)
        1
        >>> tests[0].name
        'test_example'
        >>> tests[0].max_examples
        100
    """
    property_tests = []
    lines = content.split('\n')

    # Pattern to match @settings decorator with max_examples
    settings_pattern = re.compile(r'@settings\([^)]*max_examples\s*=\s*(\d+)', re.DOTALL)

    # Pattern for detecting CI optimization in max_examples
    ci_pattern = re.compile(r'max_examples\s*=\s*\d+\s+if.*CI.*else', re.IGNORECASE)

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Look for @given decorator
        if line.startswith('@given'):
            # Find the function definition that follows
            j = i + 1
            max_examples = None
            has_ci_optimization = False

            # Look for @settings decorator between @given and function def
            while j < len(lines):
                next_line = lines[j].strip()

                if next_line.startswith('@settings'):
                    # Check for CI optimization pattern
                    has_ci_optimization = ci_pattern.search(next_line) is not None

                    # Try to extract max_examples from more complex expressions first
                    max_examples = _extract_max_examples_from_settings_line(next_line)

                    # If that didn't work, try the simple pattern
                    if max_examples is None:
                        settings_match = settings_pattern.search(next_line)
                        if settings_match:
                            max_examples = int(settings_match.group(1))

                elif next_line.startswith('def test_'):
                    # Found the function definition
                    # Get indentation level from the raw line
                    raw_line = lines[j]
                    indentation = len(raw_line) - len(raw_line.lstrip())

                    # Allow broader function names, including unicode and dashes generated
                    # by Hypothesis, by accepting any non-whitespace characters up to '('.
                    func_match = re.match(r'def\s+(test_[^\s(]+)\s*\(', next_line)
                    if func_match:
                        func_name = func_match.group(1)

                        # Find the end of the function
                        # Stop at next line with same or lower indentation (that isn't a comment/empty)
                        end_line = j + 1
                        while end_line < len(lines):
                            line_content = lines[end_line]
                            stripped = line_content.strip()

                            # Skip empty lines and comments
                            if not stripped or stripped.startswith('#'):
                                end_line += 1
                                continue

                            # Check indentation
                            current_indent = len(line_content) - len(line_content.lstrip())
                            if current_indent <= indentation:
                                # Found start of next block (could be decorator or def)
                                # But wait, decorators for next function might be at same indentation
                                # If it's a decorator, it belongs to the NEXT function, so we stop here.
                                break

                            end_line += 1

                        property_tests.append(PropertyTest(
                            name=func_name,
                            start_line=j + 1,  # Line numbers are 1-based (function definition line)
                            end_line=end_line,
                            max_examples=max_examples,
                            decorator_start_line=i,  # Decorator start line (0-based index)
                            has_ci_optimization=has_ci_optimization
                        ))
                    break

                elif next_line.startswith('def ') or next_line.startswith('class '):
                    # Hit another definition without finding test function
                    break

                j += 1

        i += 1

    return property_tests


def _extract_max_examples_from_settings_line(settings_line: str) -> Optional[int]:
    """Extract max_examples value from @settings line with complex expressions.

    This function handles complex max_examples expressions like:
    - max_examples=20 if not os.getenv('CI') else 5
    - max_examples=5 if os.getenv('CI') else 20

    For CI optimizations, this returns the CI (reduced) value since that's
    what typically needs documentation.

    Args:
        settings_line: The @settings decorator line

    Returns:
        Integer value to use for documentation purposes, or None if can't parse

    Example:
        >>> _extract_max_examples_from_settings_line(
        ...     '@settings(max_examples=20 if not os.getenv("CI") else 5)')
        5
    """
    # Find max_examples= and extract the balanced expression
    start_match = re.search(r'max_examples\s*=\s*', settings_line)
    if not start_match:
        return None

    start_pos = start_match.end()

    # Extract the expression by finding the next comma at the same nesting level
    # or the closing parenthesis of the @settings decorator
    paren_count = 0
    quote_char = None
    i = start_pos

    while i < len(settings_line):
        char = settings_line[i]

        # Handle quotes
        if char in ('"', "'") and (i == 0 or settings_line[i-1] != '\\'):
            if quote_char is None:
                quote_char = char
            elif quote_char == char:
                quote_char = None
        elif quote_char is None:  # Only process structure when not in quotes
            if char == '(':
                paren_count += 1
            elif char == ')':
                if paren_count == 0:
                    # This is the closing paren of @settings
                    break
                paren_count -= 1
            elif char == ',' and paren_count == 0:
                # This is a comma at the top level
                break

        i += 1

    max_examples_expr = settings_line[start_pos:i].strip()
    return _extract_max_examples_from_conditional(max_examples_expr)


def _extract_max_examples_from_conditional(max_examples_expr: str) -> Optional[int]:
    """Extract max_examples value from conditional expression.

    For CI optimizations, we want to document the CI (reduced) value
    since that's what needs performance rationale.

    Args:
        max_examples_expr: Expression like "20 if not os.getenv('CI') else 5"

    Returns:
        Integer value to use for documentation purposes, or None if can't parse

    Example:
        >>> _extract_max_examples_from_conditional('20 if not os.getenv("CI") else 5')
        5
    """
    # Pattern: "base_value if not CI_condition else ci_value"
    ci_pattern = re.search(r'(\d+)\s+if\s+not.*CI.*else\s+(\d+)', max_examples_expr, re.IGNORECASE)
    if ci_pattern:
        base_value = int(ci_pattern.group(1))
        ci_value = int(ci_pattern.group(2))
        return ci_value  # Return CI value for documentation

    # Pattern: "ci_value if CI_condition else base_value"
    ci_reverse_pattern = re.search(r'(\d+)\s+if.*CI.*else\s+(\d+)', max_examples_expr, re.IGNORECASE)
    if ci_reverse_pattern:
        ci_value = int(ci_reverse_pattern.group(1))
        base_value = int(ci_reverse_pattern.group(2))
        return ci_value  # Return CI value for documentation

    # Try to extract any integer from the expression
    numbers = re.findall(r'\d+', max_examples_expr)
    if numbers:
        # Return the smallest value (likely the performance-optimized one)
        return min(int(n) for n in numbers)

    return None


def has_ci_optimization_pattern(test_code: str) -> bool:
    """Check if function code contains CI optimization patterns.

    This function detects various CI optimization patterns used in
    property-based tests to reduce max_examples in CI environments.

    Args:
        test_code: The function source code

    Returns:
        True if CI optimization pattern is detected

    Example:
        >>> has_ci_optimization_pattern('max_examples=20 if not os.getenv("CI") else 5')
        True
        >>> has_ci_optimization_pattern('max_examples=100')
        False
    """
    # Patterns that indicate CI optimization
    ci_patterns = [
        r"os\.getenv\s*\(\s*['\"]CI['\"]\s*\)",
        r"os\.environ\.get\s*\(\s*['\"]CI['\"]\s*\)",
        r"if\s+not.*CI.*else",
        r"if.*CI.*else",
        r"max_examples\s*=\s*\d+\s+if.*CI",
    ]

    for pattern in ci_patterns:
        if re.search(pattern, test_code, re.IGNORECASE):
            return True

    return False


def extract_test_code(content: str, test: PropertyTest) -> str:
    """Extract the complete source code for a property test.

    This function extracts the full test code including decorators,
    which is useful for further analysis of strategy types and
    optimization patterns.

    Args:
        content: The full file content as a string
        test: The PropertyTest object describing the test

    Returns:
        The test source code including decorators
    """
    lines = content.split('\n')
    start_idx = max(0, test.decorator_start_line)
    end_idx = min(len(lines), test.end_line)
    return '\n'.join(lines[start_idx:end_idx])
