"""
Shared pytest fixtures and configuration for MarkdownLabel tests.

This module provides common pytest fixtures and configuration used across
all test modules in the MarkdownLabel test suite.

Additionally, it provides reusable Hypothesis strategies for property-based
testing. These strategies encapsulate common test data generation patterns
to reduce duplication and ensure consistency across test files.
"""

import os
import sys
import pytest
from hypothesis import strategies as st

# Set environment variables for headless Kivy testing
os.environ['KIVY_NO_ARGS'] = '1'
os.environ['KIVY_NO_CONSOLELOG'] = '1'

# Add parent directory of tools to path for absolute imports
repo_root = os.path.join(os.path.dirname(__file__), '..', '..', '..')
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)


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


# =============================================================================
# SHARED HYPOTHESIS STRATEGIES
# =============================================================================


def st_alphanumeric_text(min_size=1, max_size=30):
    """Strategy for generating alphanumeric text without markdown characters.

    Args:
        min_size: Minimum text length (default: 1)
        max_size: Maximum text length (default: 30)

    Returns:
        Strategy that generates text with only letters and numbers,
        excluding markdown special characters (#[]&\n\r).
    """
    return st.text(
        min_size=min_size,
        max_size=max_size,
        alphabet=st.characters(
            whitelist_categories=['L', 'N'],
            blacklist_characters='#[]&\n\r'
        )
    )


def st_font_size(min_value=8, max_value=48):
    """Strategy for generating font size floats.

    Args:
        min_value: Minimum font size (default: 8)
        max_value: Maximum font size (default: 48)

    Returns:
        Strategy that generates floats in the specified range.
    """
    return st.floats(min_value=min_value, max_value=max_value,
                     allow_nan=False, allow_infinity=False)


def st_font_name(fonts=None):
    """Strategy for generating font names.

    Args:
        fonts: List of font names to sample from. If None, uses default fonts.

    Returns:
        Strategy that samples from font names.
    """
    if fonts is None:
        fonts = ['Roboto', 'RobotoMono-Regular', 'Roboto-Bold']
    return st.sampled_from(fonts)


def st_rgba_color():
    """Strategy for generating RGBA color tuples.

    Returns:
        Strategy that generates 4-tuples of floats in the range [0, 1],
        representing red, green, blue, and alpha channels.
    """
    return st.tuples(
        st.floats(min_value=0, max_value=1, allow_nan=False, allow_infinity=False),
        st.floats(min_value=0, max_value=1, allow_nan=False, allow_infinity=False),
        st.floats(min_value=0, max_value=1, allow_nan=False, allow_infinity=False),
        st.floats(min_value=0, max_value=1, allow_nan=False, allow_infinity=False)
    )
