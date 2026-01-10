"""Internal helper utilities for MarkdownLabel.

These helpers mirror the rebuild contract documentation and are intended
for internal/testing use rather than public API export.
"""

from typing import Generator, Set

from kivy.uix.label import Label
from kivy.uix.widget import Widget


def find_labels_recursive(widget: Widget) -> Generator[Label, None, None]:
    """Yield all descendant Label widgets, depth-first, without revisiting nodes."""
    visited: Set[int] = set()

    def walk(node: Widget):
        node_id = id(node)
        if node_id in visited:
            return
        visited.add(node_id)

        if isinstance(node, Label):
            yield node

        for child in getattr(node, "children", []):
            yield from walk(child)

    yield from walk(widget)


def collect_widget_ids(widget: Widget, exclude_root: bool = False) -> Set[int]:
    """Collect Python object ids for a widget subtree.

    Args:
        widget: Root widget to traverse.
        exclude_root: If True, omit the root widget's id.

    Returns:
        Set of object ids for all visited widgets.
    """
    ids: Set[int] = set()

    def walk(node: Widget):
        node_id = id(node)
        if node_id in ids:
            return
        ids.add(node_id)

        for child in getattr(node, "children", []):
            walk(child)

    walk(widget)

    if exclude_root:
        ids.discard(id(widget))

    return ids
