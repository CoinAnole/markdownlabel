"""
Shared test utilities and Hypothesis strategies for MarkdownLabel tests.

This module provides common test utilities, Hypothesis strategies, and helper
functions used across multiple test modules in the MarkdownLabel test suite.
"""

from hypothesis import strategies as st
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.stencilview import StencilView
from typing import List, Optional, Dict


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
# Convert tuples to lists for backward compatibility
color_strategy = st_rgba_color().map(list)

# Strategy for generating valid padding values
text_padding_strategy = st.lists(
    st.floats(min_value=0.0, max_value=50.0, allow_nan=False, allow_infinity=False),
    min_size=4, max_size=4
)


# Strategies for padding application tests
padding_single = st.floats(min_value=0, max_value=100, allow_nan=False, allow_infinity=False)
padding_two = st.lists(
    st.floats(min_value=0, max_value=100, allow_nan=False, allow_infinity=False),
    min_size=2, max_size=2
)
padding_four = st.lists(
    st.floats(min_value=0, max_value=100, allow_nan=False, allow_infinity=False),
    min_size=4, max_size=4
)


# Strategy for unicode_errors values
unicode_errors_strategy = st.sampled_from(['strict', 'replace', 'ignore'])


# Strategies for KivyRenderer token generation
@st.composite
def heading_token(draw, level=None):
    """Generate a heading token with specified or random level.

    Args:
        level: Optional heading level (1-6). If None, a random level is generated.

    Returns:
        Dictionary representing a heading token with type 'heading'.
    """
    if level is None:
        level = draw(st.integers(min_value=1, max_value=6))
    text = draw(st.text(min_size=1, max_size=50, alphabet=st.characters(
        whitelist_categories=['L', 'N', 'P', 'S'],
        blacklist_characters='[]&'
    )))
    return {
        'type': 'heading',
        'children': [{'type': 'text', 'raw': text}],
        'attrs': {'level': level}
    }


@st.composite
def paragraph_token(draw):
    """Generate a paragraph token with text content.

    Returns:
        Dictionary representing a paragraph token with type 'paragraph'.
    """
    text = draw(st.text(min_size=1, max_size=100, alphabet=st.characters(
        whitelist_categories=['L', 'N', 'P', 'S'],
        blacklist_characters='[]&'
    )))
    return {
        'type': 'paragraph',
        'children': [{'type': 'text', 'raw': text}]
    }


@st.composite
def list_item_token(draw):
    """Generate a list item token.

    Returns:
        Dictionary representing a list item token with type 'list_item'.
    """
    text = draw(st.text(min_size=1, max_size=50, alphabet=st.characters(
        whitelist_categories=['L', 'N', 'P', 'S'],
        blacklist_characters='[]&'
    )))
    return {
        'type': 'list_item',
        'children': [{
            'type': 'paragraph',
            'children': [{'type': 'text', 'raw': text}]
        }]
    }


@st.composite
def list_token(draw, ordered=None):
    """Generate a list token (ordered or unordered).

    Args:
        ordered: Optional boolean specifying if list is ordered. If None, random.

    Returns:
        Dictionary representing a list token with type 'list'.
    """
    if ordered is None:
        ordered = draw(st.booleans())

    num_items = draw(st.integers(min_value=1, max_value=5))
    items = [draw(list_item_token()) for _ in range(num_items)]

    return {
        'type': 'list',
        'children': items,
        'attrs': {
            'ordered': ordered,
            'start': 1
        }
    }


@st.composite
def code_block_token(draw):
    """Generate a code block token.

    Returns:
        Dictionary representing a code block token with type 'block_code'.
    """
    code = draw(st.text(min_size=1, max_size=200, alphabet=st.characters(
        whitelist_categories=['L', 'N', 'P', 'S', 'Z'],
        blacklist_characters='[]&'
    )))
    language = draw(st.sampled_from(['', 'python', 'javascript', 'rust', 'go', 'java']))
    return {
        'type': 'block_code',
        'raw': code,
        'attrs': {'info': language}
    }


@st.composite
def block_quote_token(draw):
    """Generate a block quote token.

    Returns:
        Dictionary representing a block quote token with type 'block_quote'.
    """
    text = draw(st.text(min_size=1, max_size=100, alphabet=st.characters(
        whitelist_categories=['L', 'N', 'P', 'S'],
        blacklist_characters='[]&'
    )))
    return {
        'type': 'block_quote',
        'children': [{
            'type': 'paragraph',
            'children': [{'type': 'text', 'raw': text}]
        }]
    }


@st.composite
def image_token(draw):
    """Generate an image token.

    Returns:
        Dictionary representing an image token with type 'image'.
    """
    alt = draw(st.text(min_size=0, max_size=50, alphabet=st.characters(
        whitelist_categories=['L', 'N', 'P', 'S'],
        blacklist_characters='[]&'
    )))
    # Generate a simple URL-like string
    url = draw(st.from_regex(r'https?://[a-z]+\.[a-z]+/[a-z]+\.(png|jpg|gif)', fullmatch=True))
    return {
        'type': 'image',
        'children': [{'type': 'text', 'raw': alt}] if alt else [],
        'attrs': {'url': url}
    }


@st.composite
def table_cell_token(draw, align=None, is_head=False):
    """Generate a table cell token.

    Args:
        align: Optional alignment value ('left', 'center', 'right', or None).
        is_head: Boolean indicating if this is a header cell.

    Returns:
        Dictionary representing a table cell token with type 'table_cell'.
    """
    text = draw(st.text(min_size=0, max_size=30, alphabet=st.characters(
        whitelist_categories=['L', 'N', 'P', 'S'],
        blacklist_characters='[]&'
    )))
    if align is None:
        align = draw(st.sampled_from([None, 'left', 'center', 'right']))

    return {
        'type': 'table_cell',
        'children': [{'type': 'text', 'raw': text}] if text else [],
        'attrs': {'align': align, 'head': is_head}
    }


@st.composite
def table_row_token(draw, num_cols, alignments=None, is_head=False):
    """Generate a table row token with specified number of columns.

    Args:
        num_cols: Number of columns in the row.
        alignments: Optional list of alignment values for each column.
        is_head: Boolean indicating if this is a header row.

    Returns:
        Dictionary representing a table row token with type 'table_row'.
    """
    cells = []
    for i in range(num_cols):
        align = alignments[i] if alignments else None
        cell = draw(table_cell_token(align=align, is_head=is_head))
        cells.append(cell)

    return {
        'type': 'table_row',
        'children': cells
    }


@st.composite
def table_token(draw, num_rows=None, num_cols=None):
    """Generate a table token with specified dimensions.

    Args:
        num_rows: Optional number of rows (including header). If None, random (1-5).
        num_cols: Optional number of columns. If None, random (1-5).

    Returns:
        Dictionary representing a table token with type 'table'.
    """
    if num_rows is None:
        num_rows = draw(st.integers(min_value=1, max_value=5))
    if num_cols is None:
        num_cols = draw(st.integers(min_value=1, max_value=5))

    # Generate alignments for columns
    alignments = [draw(st.sampled_from([None, 'left', 'center', 'right']))
                  for _ in range(num_cols)]

    # Generate header row
    head_row = draw(table_row_token(num_cols, alignments, is_head=True))

    # Generate body rows
    body_rows = []
    for _ in range(num_rows - 1):  # -1 because header is one row
        body_row = draw(table_row_token(num_cols, alignments, is_head=False))
        body_rows.append(body_row)

    return {
        'type': 'table',
        'children': [
            {
                'type': 'table_head',
                'children': [head_row]
            },
            {
                'type': 'table_body',
                'children': body_rows
            }
        ]
    }


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

def collect_widget_ids(widget: Widget, exclude_root: bool = False) -> Dict[int, Widget]:
    """Collect Python object ids and references of all widgets in the tree.

    This helper function traverses the widget tree and collects a mapping of
    Python object IDs to the widgets themselves. Storing the widget references
    prevents their memory addresses (IDs) from being reused by Python's
    garbage collector during identity comparison tests.

    Args:
        widget: Root widget to collect from
        exclude_root: If True, exclude the root widget from the result

    Returns:
        Dictionary mapping widget object ids to widget instances
    """
    widgets = {} if exclude_root else {id(widget): widget}
    if hasattr(widget, 'children'):
        for child in widget.children:
            widgets.update(collect_widget_ids(child, exclude_root=False))
    return widgets


def assert_rebuild_occurred(widget: Widget, ids_before: Dict[int, Widget], exclude_root: bool = True) -> None:
    """Assert that a widget tree rebuild occurred.

    Verifies that the widget tree has been rebuilt by comparing widget mappings
    before and after a change. A rebuild means different widget instances.

    IMPORTANT: You must collect ids_before BEFORE making changes:
        ids_before = collect_widget_ids(widget)
        # ... make property changes ...
        # ... call force_rebuild() if needed ...
        assert_rebuild_occurred(widget, ids_before)

    Args:
        widget: Root widget to check
        ids_before: Dict mapping widget IDs to objects BEFORE the change
                    (from collect_widget_ids() called before changes)
        exclude_root: If True, exclude the root widget from comparison

    Raises:
        AssertionError: If no rebuild occurred (widget mappings are identical)
    """
    ids_after = collect_widget_ids(widget, exclude_root=exclude_root)

    # Compare dictionaries - will be unequal if instances differ even if IDs coincide
    assert ids_before != ids_after, \
        "Expected rebuild to occur, but widget instances are identical"


def assert_no_rebuild(widget: Widget, ids_before: Dict[int, Widget], exclude_root: bool = True) -> None:
    """Assert that no widget tree rebuild occurred.

    Verifies that the widget tree was updated in-place without creating new
    widget instances.

    IMPORTANT: You must collect ids_before BEFORE making changes:
        ids_before = collect_widget_ids(widget)
        # ... make property changes ...
        assert_no_rebuild(widget, ids_before)

    Args:
        widget: Root widget to check
        ids_before: Dict mapping widget IDs to objects BEFORE the change
                    (from collect_widget_ids() called before changes)
        exclude_root: If True, exclude the root widget from comparison

    Raises:
        AssertionError: If a rebuild occurred (widget mappings changed)
    """
    ids_after = collect_widget_ids(widget, exclude_root=exclude_root)

    assert ids_before == ids_after, \
        f"Expected no rebuild, but widget instances changed: " \
        f"{len(ids_before)} before, {len(ids_after)} after"


# Widget Search Helpers

def find_images(widget: Widget, images: Optional[List[Image]] = None) -> List[Image]:
    """Recursively find all Image widgets in a widget tree.

    Args:
        widget: The root widget to search from
        images: Optional list to accumulate results (used for recursion)

    Returns:
        List of all Image widgets found in the widget tree
    """
    if images is None:
        images = []

    if isinstance(widget, Image):
        images.append(widget)

    if hasattr(widget, 'children'):
        for child in widget.children:
            find_images(child, images)

    return images


def has_clipping_container(widget: Widget) -> bool:
    """Check if widget contains a clipping container (StencilView).

    This helper function searches through the widget tree to determine if
    a StencilView (used for clipping) is present.

    Args:
        widget: Widget to check

    Returns:
        True if a clipping container is found, False otherwise
    """
    for child in widget.children:
        if isinstance(child, StencilView):
            return True
    return False


def is_code_label(label: Label, code_font_name: str = 'RobotoMono-Regular') -> bool:
    """Check if a label is a code label based on its font.

    Code labels use a monospace font (typically RobotoMono-Regular) to
    distinguish them from regular text labels.

    Args:
        label: Label widget to check
        code_font_name: Expected code font name (default: 'RobotoMono-Regular')

    Returns:
        True if this appears to be a code label, False otherwise
    """
    return label.font_name == code_font_name


# Widget Search Helpers for Refs and Anchors

def find_labels_with_refs(widget: Widget, labels: Optional[List[Label]] = None) -> List[Label]:
    """Recursively find all Label widgets that have refs.

    Args:
        widget: The root widget to search from
        labels: Optional list to accumulate results (used for recursion)

    Returns:
        List of all Label widgets that have refs in the widget tree
    """
    if labels is None:
        labels = []

    if isinstance(widget, Label) and hasattr(widget, 'refs') and widget.refs:
        labels.append(widget)

    if hasattr(widget, 'children'):
        for child in widget.children:
            find_labels_with_refs(child, labels)

    return labels


def find_labels_with_ref_markup(widget: Widget, labels: Optional[List[Label]] = None) -> List[Label]:
    """Recursively find all Label widgets that have ref markup in their text.

    Args:
        widget: The root widget to search from
        labels: Optional list to accumulate results (used for recursion)

    Returns:
        List of all Label widgets with ref markup in the widget tree
    """
    if labels is None:
        labels = []

    if isinstance(widget, Label) and hasattr(widget, 'text'):
        if '[ref=' in widget.text and '[/ref]' in widget.text:
            labels.append(widget)

    if hasattr(widget, 'children'):
        for child in widget.children:
            find_labels_with_ref_markup(child, labels)

    return labels


def get_widget_offset(widget: Widget, root: Widget) -> tuple:
    """Calculate widget's position relative to root widget.

    Args:
        widget: Widget to calculate offset for
        root: Root widget to calculate offset relative to

    Returns:
        Tuple (offset_x, offset_y) relative to root
    """
    offset_x = 0
    offset_y = 0
    current = widget

    while current is not None and current is not root:
        offset_x += current.x
        offset_y += current.y
        current = current.parent

    return offset_x, offset_y


# Coverage Measurement Helper

def simulate_coverage_measurement(temp_dir: str, test_paths: List[str],
                                  source_paths: List[str], coverage_level: str) -> float:
    """Simulate coverage measurement for testing purposes.

    In a real implementation, this would run actual coverage measurement.
    For testing, we simulate based on coverage level and number of tests.

    Args:
        temp_dir: Temporary directory path
        test_paths: List of test file paths
        source_paths: List of source file paths
        coverage_level: Coverage level ('low', 'medium', 'high')

    Returns:
        Simulated coverage percentage (0.0 to 100.0)
    """
    import random

    num_tests = len(test_paths)
    num_sources = len(source_paths)

    # Base coverage based on level
    if coverage_level == 'low':
        base_coverage = 30.0
    elif coverage_level == 'medium':
        base_coverage = 60.0
    else:  # high
        base_coverage = 85.0

    # Adjust based on test/source ratio
    test_ratio = num_tests / max(num_sources, 1)
    coverage_adjustment = min(test_ratio * 10, 15)  # Max 15% boost

    # Add some variance
    variance = random.uniform(-5, 5)

    final_coverage = max(0, min(100, base_coverage + coverage_adjustment + variance))
    return final_coverage


# Test Analysis Strategies

@st.composite
def duplicate_helper_functions(draw):
    """Generate test files with duplicate helper functions.

    This strategy generates test files containing helper functions that appear
    in multiple files, either identically or with similar implementations. Used
    for testing duplicate detection and consolidation logic.

    Returns:
        Tuple containing:
            - function_name: Name of the duplicated helper function
            - files: List of test file contents as strings
            - make_identical: Boolean indicating if functions are identical
    """
    function_name = draw(st.sampled_from([
        "find_labels_recursive",
        "_find_labels_recursive",
        "collect_widget_ids",
        "_collect_widget_ids",
        "assert_colors_equal",
        "setup_test_widget"
    ]))

    # Generate function body variations
    body_templates = [
        """    if labels is None:
        labels = []
    for child in widget.children:
        if isinstance(child, Label):
            labels.append(child)
        labels = {func_name}(child, labels)
    return labels""",

        """    result = []
    if hasattr(widget, 'children'):
        for child in widget.children:
            if hasattr(child, 'text'):
                result.append(child)
            result.extend({func_name}(child))
    return result""",

        """    ids = set()
    ids.add(id(widget))
    for child in getattr(widget, 'children', []):
        ids.update({func_name}(child))
    return ids"""
    ]

    # Choose whether to make them identical or similar
    make_identical = draw(st.booleans())
    num_files = draw(st.integers(min_value=2, max_value=4))

    files = []
    for i in range(num_files):
        if make_identical:
            body = body_templates[0].format(func_name=function_name)
        else:
            body = draw(st.sampled_from(body_templates)).format(func_name=function_name)

        file_content = f'''"""Test module {i}."""
import pytest

class TestExample{i}:
    """Test class {i}."""

    def {function_name}(self, widget, labels=None):
        """Helper function for finding labels."""
{body}

    def test_example_{i}(self):
        """Example test."""
        assert True
'''
        files.append(file_content)

    return function_name, files, make_identical


@st.composite
def rebuild_test_file_strategy(draw):
    """Generate a Python test file with a rebuild test.

    This strategy generates test files containing tests with "triggers_rebuild"
    in their names, either with or without actual rebuild-related assertions.
    Used for testing test file parser and name consistency validation.

    Returns:
        Tuple containing:
            - test_code: Complete test file content as string
            - test_name: Name of the generated test method
            - has_rebuild_assertion: Boolean indicating if test has rebuild assertions
    """
    test_name = draw(st.sampled_from([
        "test_color_change_triggers_rebuild",
        "test_font_size_triggers_rebuild",
        "test_text_triggers_rebuild",
        "test_padding_triggers_rebuild"
    ]))

    has_rebuild_assertion = draw(st.booleans())

    if has_rebuild_assertion:
        # Include rebuild-related assertions
        assertion_code = draw(st.sampled_from([
            "    widget_id_before = id(label.children[0])\n"
            "    label.text = 'new text'\n"
            "    widget_id_after = id(label.children[0])\n"
            "    assert widget_id_before != widget_id_after",

            "    ids_before = collect_widget_ids(label)\n"
            "    label.color = [1, 0, 0, 1]\n"
            "    ids_after = collect_widget_ids(label)\n"
            "    assert ids_before != ids_after",

            "    assert_rebuild_occurred(label, lambda: setattr(label, 'font_size', 20))",

            "    assert_no_rebuild(label, lambda: setattr(label, 'color', [1, 0, 0, 1]))"
        ]))
    else:
        # Only value assertions, no rebuild checks
        assertion_code = draw(st.sampled_from([
            "    label.text = 'new text'\n"
            "    assert label.text == 'new text'",

            "    label.color = [1, 0, 0, 1]\n"
            "    assert label.color == [1, 0, 0, 1]",

            "    label.font_size = 20\n"
            "    assert label.font_size == 20"
        ]))

    test_code = f'''"""Test module."""
import pytest

class TestRebuildBehavior:
    """Test class for rebuild behavior."""

    def {test_name}(self):
        """Test that property change triggers rebuild."""
        label = create_label()
{assertion_code}
'''

    return test_code, test_name, has_rebuild_assertion
