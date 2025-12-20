"""
Shared test utilities and Hypothesis strategies for MarkdownLabel tests.

This module provides common test utilities, Hypothesis strategies, and helper
functions used across multiple test modules in the MarkdownLabel test suite.
"""

from hypothesis import strategies as st
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from typing import List, Optional


# Touch Simulation Classes

class FakeTouch:
    """Minimal touch simulation for headless testing.
    
    Provides the essential attributes needed by on_touch_down
    without requiring a Kivy window.
    """
    def __init__(self, x: float, y: float):
        """Initialize a fake touch at the given coordinates.
        
        Args:
            x: X coordinate of the touch
            y: Y coordinate of the touch
        """
        self.x = x
        self.y = y
        self.pos = (x, y)


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


# Rebuild Detection Helpers

def collect_widget_ids(widget: Widget, exclude_root: bool = False) -> set:
    """Collect Python object ids of all widgets in the tree.
    
    This helper function traverses the widget tree and collects the Python
    object IDs of all widgets. It's used to verify widget identity preservation
    across property changes.
    
    Args:
        widget: Root widget to collect from
        exclude_root: If True, exclude the root widget's id from the result
    
    Returns:
        Set of widget object ids
    """
    ids = set() if exclude_root else {id(widget)}
    if hasattr(widget, 'children'):
        for child in widget.children:
            ids.update(collect_widget_ids(child, exclude_root=False))
    return ids


def assert_rebuild_occurred(widget: Widget, ids_before: set, exclude_root: bool = True) -> None:
    """Assert that a widget tree rebuild occurred.
    
    Verifies that the widget tree has been rebuilt by comparing widget IDs
    before and after a change. A rebuild means new widget instances were created.
    
    Args:
        widget: Root widget to check
        ids_before: Set of widget IDs before the change
        exclude_root: If True, exclude the root widget from comparison
        
    Raises:
        AssertionError: If no rebuild occurred (widget IDs are the same)
    """
    ids_after = collect_widget_ids(widget, exclude_root=exclude_root)
    
    if exclude_root:
        # Root should remain the same, but children should be different
        assert ids_before != ids_after, \
            f"Expected rebuild to occur (children should change), but widget IDs are identical"
    else:
        # All widgets should be different
        assert ids_before != ids_after, \
            f"Expected rebuild to occur, but widget IDs are identical"


def assert_no_rebuild(widget: Widget, ids_before: set, exclude_root: bool = True) -> None:
    """Assert that no widget tree rebuild occurred.
    
    Verifies that the widget tree was updated in-place without creating new
    widget instances. This is expected for style-only property changes.
    
    Args:
        widget: Root widget to check
        ids_before: Set of widget IDs before the change
        exclude_root: If True, exclude the root widget from comparison
        
    Raises:
        AssertionError: If a rebuild occurred (widget IDs changed)
    """
    ids_after = collect_widget_ids(widget, exclude_root=exclude_root)
    
    assert ids_before == ids_after, \
        f"Expected no rebuild (widget IDs should remain the same), but IDs changed: " \
        f"{len(ids_before)} before, {len(ids_after)} after"