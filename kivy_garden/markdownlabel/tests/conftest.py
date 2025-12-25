"""
Shared pytest fixtures and configuration for MarkdownLabel tests.

This module provides common pytest fixtures and configuration used across
all test modules in the MarkdownLabel test suite.
"""

import os
import sys
import pytest

# Set environment variables for headless Kivy testing
os.environ['KIVY_NO_ARGS'] = '1'
os.environ['KIVY_NO_CONSOLELOG'] = '1'

# Add tools directory to path for test optimization utilities
tools_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'tools')
if tools_path not in sys.path:
    sys.path.insert(0, tools_path)


@pytest.fixture(scope="session", autouse=True)
def setup_kivy_environment():
    """Set up Kivy environment for testing."""
    # Environment variables are already set above
    # This fixture ensures they're applied before any tests run
    pass


@pytest.fixture
def sample_markdown_texts():
    """Provide sample markdown texts for testing."""
    return {
        'simple_paragraph': 'Hello World',
        'heading': '# Test Heading',
        'bold_text': '**Bold Text**',
        'italic_text': '*Italic Text*',
        'link': '[Link Text](https://example.com)',
        'list': '- Item 1\n- Item 2\n- Item 3',
        'table': '| A | B |\n| --- | --- |\n| 1 | 2 |',
        'code_block': '```python\nprint("hello")\n```',
        'mixed_content': '''# Heading

This is a paragraph with **bold** and *italic* text.

- List item 1
- List item 2

| Column 1 | Column 2 |
| -------- | -------- |
| Cell 1   | Cell 2   |

```python
def hello():
    print("Hello, World!")
```''',
    }


@pytest.fixture
def default_colors():
    """Provide default color values for testing."""
    return {
        'white': [1.0, 1.0, 1.0, 1.0],
        'black': [0.0, 0.0, 0.0, 1.0],
        'red': [1.0, 0.0, 0.0, 1.0],
        'green': [0.0, 1.0, 0.0, 1.0],
        'blue': [0.0, 0.0, 1.0, 1.0],
        'code_light': [0.8, 0.8, 0.8, 1.0],  # Light color used for code blocks
    }


@pytest.fixture
def default_padding_values():
    """Provide default padding values for testing."""
    return {
        'zero': [0.0, 0.0, 0.0, 0.0],
        'uniform_small': [5.0, 5.0, 5.0, 5.0],
        'uniform_large': [20.0, 20.0, 20.0, 20.0],
        'horizontal_vertical': [10.0, 5.0, 10.0, 5.0],  # [left, top, right, bottom]
        'asymmetric': [5.0, 10.0, 15.0, 20.0],
    }


@pytest.fixture
def kivy_fonts():
    """Provide list of available Kivy fonts for testing."""
    return ['Roboto', 'Roboto-Bold', 'Roboto-Italic', 'RobotoMono-Regular']