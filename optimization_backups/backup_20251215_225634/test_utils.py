"""
Shared test utilities and Hypothesis strategies for MarkdownLabel tests.

This module provides common test utilities, Hypothesis strategies, and helper
functions used across multiple test modules in the MarkdownLabel test suite.
"""

from hypothesis import strategies as st
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from typing import List, Optional


# Constants
KIVY_FONTS = ['Roboto', 'Roboto-Bold', 'Roboto-Italic', 'RobotoMono-Regular']


# Hypothesis Strategies

@st.composite
def markdown_heading(draw):
    """Generate a Markdown heading."""
    level = draw(st.integers(min_value=1, max_value=6))
    text = draw(st.text(min_size=1, max_size=50, alphabet=st.characters(
        whitelist_categories=['L', 'N', 'P', 'S'],
        blacklist_characters='#[]&\n\r'
    )))
    return '#' * level + ' ' + text


@st.composite
def markdown_paragraph(draw):
    """Generate a Markdown paragraph."""
    # Exclude backslash as it's an escape character in Markdown
    # that gets consumed during parsing (e.g., \: becomes :)
    # Also exclude < and > to avoid HTML-like tags that might not parse as paragraphs
    text = draw(st.text(min_size=1, max_size=100, alphabet=st.characters(
        whitelist_categories=['L', 'N', 'P', 'S', 'Z'],
        blacklist_characters='#[]&\n\r*_`~\\<>'
    )))
    text = text.strip()
    # Ensure we have some actual content that will render as a paragraph
    if not text or len(text.strip()) == 0:
        text = "sample text"
    return text


@st.composite
def markdown_bold(draw):
    """Generate bold Markdown text."""
    text = draw(st.text(min_size=1, max_size=30, alphabet=st.characters(
        whitelist_categories=['L', 'N'],
        blacklist_characters='*_[]&\n\r'
    )))
    return f'**{text}**'


@st.composite
def markdown_italic(draw):
    """Generate italic Markdown text."""
    text = draw(st.text(min_size=1, max_size=30, alphabet=st.characters(
        whitelist_categories=['L', 'N'],
        blacklist_characters='*_[]&\n\r'
    )))
    return f'*{text}*'


@st.composite
def markdown_link(draw):
    """Generate a Markdown link."""
    text = draw(st.text(min_size=1, max_size=30, alphabet=st.characters(
        whitelist_categories=['L', 'N'],
        blacklist_characters='[]()&\n\r'
    )))
    url = draw(st.from_regex(r'https?://[a-z]+\.[a-z]+/[a-z]+', fullmatch=True))
    return f'[{text}]({url})'


@st.composite
def simple_markdown_document(draw):
    """Generate a simple Markdown document with various block elements."""
    elements = []
    num_elements = draw(st.integers(min_value=1, max_value=5))
    
    for _ in range(num_elements):
        element_type = draw(st.sampled_from(['heading', 'paragraph']))
        if element_type == 'heading':
            elements.append(draw(markdown_heading()))
        else:
            para = draw(markdown_paragraph())
            if para:  # Only add non-empty paragraphs
                elements.append(para)
    
    # Filter out empty elements and join with double newlines
    elements = [e for e in elements if e.strip()]
    return '\n\n'.join(elements) if elements else 'Default text'


# Strategy for generating valid RGBA colors
color_strategy = st.lists(
    st.floats(min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False),
    min_size=4, max_size=4
)

# Strategy for generating valid padding values
text_padding_strategy = st.lists(
    st.floats(min_value=0.0, max_value=50.0, allow_nan=False, allow_infinity=False),
    min_size=4, max_size=4
)


# Helper Functions

def find_labels_recursive(widget: Widget, labels: Optional[List[Label]] = None) -> List[Label]:
    """Recursively find all Label widgets in a widget tree.
    
    Args:
        widget: The root widget to search from
        labels: Optional list to accumulate results (used for recursion)
        
    Returns:
        List of all Label widgets found in the widget tree
    """
    if labels is None:
        labels = []
    
    if isinstance(widget, Label):
        labels.append(widget)
    
    if hasattr(widget, 'children'):
        for child in widget.children:
            find_labels_recursive(child, labels)
    
    return labels


def colors_equal(c1: List[float], c2: List[float], tolerance: float = 0.001) -> bool:
    """Compare two colors with tolerance for floating point differences.
    
    Args:
        c1: First color as [r, g, b, a] list
        c2: Second color as [r, g, b, a] list
        tolerance: Maximum allowed difference between components
        
    Returns:
        True if colors are equal within tolerance, False otherwise
    """
    if len(c1) != len(c2):
        return False
    return all(abs(a - b) < tolerance for a, b in zip(c1, c2))


def padding_equal(p1: List[float], p2: List[float], tolerance: float = 0.001) -> bool:
    """Compare two padding values with tolerance for floating point differences.
    
    Args:
        p1: First padding as [left, top, right, bottom] list
        p2: Second padding as [left, top, right, bottom] list
        tolerance: Maximum allowed difference between components
        
    Returns:
        True if padding values are equal within tolerance, False otherwise
    """
    if len(p1) != len(p2):
        return False
    return all(abs(a - b) < tolerance for a, b in zip(p1, p2))


def floats_equal(f1: float, f2: float, tolerance: float = 0.001) -> bool:
    """Compare two float values with tolerance.
    
    Args:
        f1: First float value
        f2: Second float value
        tolerance: Maximum allowed difference
        
    Returns:
        True if values are equal within tolerance, False otherwise
    """
    return abs(f1 - f2) < tolerance