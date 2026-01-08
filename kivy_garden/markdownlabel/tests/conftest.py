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

# Add parent directory of tools to path for absolute imports
repo_root = os.path.join(os.path.dirname(__file__), '..', '..', '..')
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)


# Centralized list of all test modules for meta-testing
# This list is used by meta-tests to validate all test files
TEST_MODULES = [
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
    'test_clipping_behavior.py',
    'test_rebuild_scheduling.py',
    # test_rebuild_semantics.py was split into 6 files for maintainability:
    'test_rebuild_identity_preservation.py',
    'test_rebuild_structure_changes.py',
    'test_rebuild_style_propagation.py',
    'test_rebuild_advanced_properties.py',
    'test_rebuild_text_size_and_code_blocks.py',
    'test_rebuild_property_classification.py',
    'test_rtl_alignment.py',
    # test_shortening_and_coordinate.py was split into 2 files:
    'test_shortening_properties.py',
    'test_coordinate_translation.py',
    'test_texture_render_mode.py',
    'test_texture_sizing.py',
    # test_kivy_renderer.py was split into 2 files:
    'test_kivy_renderer_blocks.py',
    'test_kivy_renderer_tables.py',
    'test_inline_renderer.py',
]


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
