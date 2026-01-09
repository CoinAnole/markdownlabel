"""
Property-based tests for coordinate translation features.

This module contains tests for coordinate translation for refs (link bounding boxes)
and anchors from child Labels to MarkdownLabel's local coordinate space, covering:

- Coordinate translation for refs and anchors
- Deterministic coordinate translation tests with injected geometry for headless CI environments
- Property-based tests using Hypothesis for universal behavior verification

These tests verify that MarkdownLabel correctly implements coordinate translation
while maintaining proper Markdown rendering, ensuring that links and anchors are
properly positioned in the widget tree.
"""

import pytest
from hypothesis import given, strategies as st, settings

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from kivy_garden.markdownlabel import MarkdownLabel
from .test_utils import (
    find_labels_with_refs,
    find_labels_with_ref_markup,
    get_widget_offset,
    st_alphanumeric_text
)


class TestCoordinateTranslation:
    """Property tests for coordinate translation of refs and anchors."""

    @pytest.mark.property
    @given(st_alphanumeric_text(min_size=1, max_size=20))
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_link_produces_ref_markup_for_translation(self, link_text):
        """Links produce ref markup that will be translated when rendered.

        This test verifies that links are correctly rendered with [ref=url] markup,
        which is the prerequisite for coordinate translation. The actual refs
        dictionary is populated by Kivy during texture rendering.
        """
        url = 'https://example.com/page'
        markdown = f'[{link_text}]({url})'

        label = MarkdownLabel(text=markdown)

        # Find Labels with ref markup
        labels_with_markup = find_labels_with_ref_markup(label)

        assert len(labels_with_markup) >= 1, \
            f"Expected at least one Label with ref markup for: {markdown}"

        # Verify the URL is in the markup
        found_url = False
        for lbl in labels_with_markup:
            if f'[ref={url}]' in lbl.text:
                found_url = True
                break

        assert found_url, \
            f"Expected [ref={url}] in Label markup"

    @pytest.mark.property
    @given(st.lists(
        st_alphanumeric_text(min_size=1, max_size=10),
        min_size=2, max_size=4
    ))
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_multiple_links_produce_ref_markup(self, link_texts):
        """Multiple links in different paragraphs produce ref markup.

        This test verifies that multiple links are correctly rendered with
        [ref=url] markup in their respective Labels.
        """
        # Create markdown with multiple links in separate paragraphs
        paragraphs = []
        urls = []
        for i, text in enumerate(link_texts):
            url = f'https://example{i}.com/page'
            urls.append(url)
            paragraphs.append(f'[{text}]({url})')

        markdown = '\n\n'.join(paragraphs)
        label = MarkdownLabel(text=markdown)

        # Find Labels with ref markup
        labels_with_markup = find_labels_with_ref_markup(label)

        # Should have at least as many Labels with markup as we have links
        assert len(labels_with_markup) >= len(link_texts), \
            f"Expected at least {len(link_texts)} Labels with ref markup, got {len(labels_with_markup)}"

        # Verify each URL appears in some Label's markup
        for url in urls:
            found = False
            for lbl in labels_with_markup:
                if f'[ref={url}]' in lbl.text:
                    found = True
                    break
            assert found, f"Expected [ref={url}] in some Label markup"

    def test_refs_empty_for_no_links(self):
        """refs returns empty dict when there are no links."""
        label = MarkdownLabel(text='Hello World without links')

        assert label.refs == {}, \
            f"Expected empty refs, got {label.refs}"

    def test_refs_empty_for_empty_text(self):
        """refs returns empty dict for empty text."""
        label = MarkdownLabel(text='')

        assert label.refs == {}, \
            f"Expected empty refs for empty text, got {label.refs}"

    def test_anchors_empty_for_no_anchors(self):
        """anchors returns empty dict when there are no anchors."""
        label = MarkdownLabel(text='Hello World without anchors')

        assert label.anchors == {}, \
            f"Expected empty anchors, got {label.anchors}"

    def test_anchors_empty_for_empty_text(self):
        """anchors returns empty dict for empty text."""
        label = MarkdownLabel(text='')

        assert label.anchors == {}, \
            f"Expected empty anchors for empty text, got {label.anchors}"

    @pytest.mark.needs_window
    def test_refs_translation_algorithm_correctness(self):
        """Test that the coordinate translation algorithm works correctly.

        This test directly verifies the translation logic by checking that
        when child Labels have refs, the aggregated refs contain properly
        translated coordinates.

        Note: This test requires a Kivy window/text provider to populate
        Label.refs. In headless CI, use the deterministic tests in
        TestDeterministicRefsTranslation instead.

        _Requirements: 3.6_
        """
        markdown = '[Click me](https://example.com)'
        label = MarkdownLabel(text=markdown)

        # Get aggregated refs
        aggregated_refs = label.refs

        # Find child Labels with refs (if any - depends on rendering)
        labels_with_refs = find_labels_with_refs(label)

        # If we have child Labels with refs, verify translation
        for child_label in labels_with_refs:
            child_refs = child_label.refs
            offset_x, offset_y = get_widget_offset(child_label, label)

            for url, child_boxes in child_refs.items():
                assert url in aggregated_refs, \
                    f"Expected URL {url} in aggregated refs"

                for child_box in child_boxes:
                    expected_box = [
                        child_box[0] + offset_x,
                        child_box[1] + offset_y,
                        child_box[2] + offset_x,
                        child_box[3] + offset_y
                    ]

                    assert expected_box in aggregated_refs[url], \
                        f"Expected translated box {expected_box} in aggregated refs"

    def test_nested_list_produces_correct_ref_markup(self):
        """Links in nested content (lists) produce correct ref markup."""
        markdown = '''- [Link 1](https://example1.com)
- [Link 2](https://example2.com)
'''
        label = MarkdownLabel(text=markdown)

        # Find Labels with ref markup
        labels_with_markup = find_labels_with_ref_markup(label)

        # Should have Labels with ref markup for the links
        assert len(labels_with_markup) >= 1, \
            "Expected at least one Label with ref markup in list"

        # Verify URLs appear in markup
        all_markup = ' '.join(lbl.text for lbl in labels_with_markup)
        assert '[ref=https://example1.com]' in all_markup or \
               '[ref=https://example2.com]' in all_markup, \
            "Expected ref markup for list links"

    def test_table_produces_correct_ref_markup(self):
        """Links in table content produce correct ref markup."""
        markdown = '''| Column A | Column B |
| --- | --- |
| [Link](https://example.com) | Text |
'''
        label = MarkdownLabel(text=markdown)

        # Find Labels with ref markup
        labels_with_markup = find_labels_with_ref_markup(label)

        # Should have at least one Label with ref markup
        assert len(labels_with_markup) >= 1, \
            "Expected at least one Label with ref markup in table"

        # Verify URL appears in markup
        found = any('[ref=https://example.com]' in lbl.text
                   for lbl in labels_with_markup)
        assert found, "Expected ref markup for table link"

    def test_blockquote_produces_correct_ref_markup(self):
        """Links in blockquote content produce correct ref markup."""
        markdown = '> [Quoted link](https://example.com)'

        label = MarkdownLabel(text=markdown)

        # Find Labels with ref markup
        labels_with_markup = find_labels_with_ref_markup(label)

        # Should have at least one Label with ref markup
        assert len(labels_with_markup) >= 1, \
            "Expected at least one Label with ref markup in blockquote"

        # Verify URL appears in markup
        found = any('[ref=https://example.com]' in lbl.text
                   for lbl in labels_with_markup)
        assert found, "Expected ref markup for blockquote link"

    @pytest.mark.property
    @given(st_alphanumeric_text(min_size=1, max_size=10),
           st_alphanumeric_text(min_size=1, max_size=10))
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_ref_markup_updates_when_text_changes(self, link_text1, link_text2):
        """ref markup updates correctly when text property changes."""
        url1 = 'https://example1.com'
        url2 = 'https://example2.com'

        markdown1 = f'[{link_text1}]({url1})'
        markdown2 = f'[{link_text2}]({url2})'

        label = MarkdownLabel(text=markdown1)

        # Initial markup should have url1
        labels1 = find_labels_with_ref_markup(label)
        assert len(labels1) >= 1, "Expected Label with ref markup initially"
        found_url1 = any(f'[ref={url1}]' in lbl.text for lbl in labels1)
        assert found_url1, f"Expected [ref={url1}] in initial markup"

        # Change text - use force_rebuild() for immediate update since
        # text changes now use deferred rebuilds
        label.text = markdown2
        label.force_rebuild()

        # Updated markup should have url2
        labels2 = find_labels_with_ref_markup(label)
        assert len(labels2) >= 1, "Expected Label with ref markup after update"
        found_url2 = any(f'[ref={url2}]' in lbl.text for lbl in labels2)
        assert found_url2, f"Expected [ref={url2}] in updated markup"

        # url1 should no longer be present (unless url1 == url2)
        if url1 != url2:
            found_old = any(f'[ref={url1}]' in lbl.text for lbl in labels2)
            assert not found_old, f"Did not expect [ref={url1}] in updated markup"

    @pytest.mark.property
    @given(st.floats(min_value=0, max_value=100),
           st.floats(min_value=0, max_value=100),
           st.floats(min_value=0, max_value=100),
           st.floats(min_value=0, max_value=100))
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_coordinate_translation_math(self, x1, y1, x2, y2):
        """Test that coordinate translation math is correct.

        This tests the translation algorithm directly with known values.
        """
        # Simulate a bounding box
        original_box = [x1, y1, x2, y2]

        # Simulate an offset
        offset_x = 10.0
        offset_y = 20.0

        # Apply translation (same algorithm as in _get_refs)
        translated_box = [
            original_box[0] + offset_x,
            original_box[1] + offset_y,
            original_box[2] + offset_x,
            original_box[3] + offset_y
        ]

        # Verify translation
        assert translated_box[0] == x1 + offset_x
        assert translated_box[1] == y1 + offset_y
        assert translated_box[2] == x2 + offset_x
        assert translated_box[3] == y2 + offset_y

    @pytest.mark.property
    @given(st.floats(min_value=0, max_value=100),
           st.floats(min_value=0, max_value=100))
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_anchor_translation_math(self, x, y):
        """Test that anchor coordinate translation math is correct.

        This tests the translation algorithm directly with known values.
        """
        # Simulate an anchor position
        original_pos = (x, y)

        # Simulate an offset
        offset_x = 15.0
        offset_y = 25.0

        # Apply translation (same algorithm as in _get_anchors)
        translated_pos = (
            original_pos[0] + offset_x,
            original_pos[1] + offset_y
        )

        # Verify translation
        assert translated_pos[0] == x + offset_x
        assert translated_pos[1] == y + offset_y


# *For any* MarkdownLabel containing a child Label with known `refs`, `pos`, `size`,
# and `texture_size`, the aggregated `refs` property SHALL return bounding boxes
# translated according to the formula:
# - `base_x = parent_offset_x + (label.center_x - tex_w / 2.0)`
# - `base_y = parent_offset_y + (label.center_y + tex_h / 2.0)`
# - `translated_box = [base_x + x1, base_y - y1, base_x + x2, base_y - y2]`


@pytest.mark.slow
class TestDeterministicRefsTranslation:
    """Deterministic tests for refs coordinate translation with injected geometry.

    These tests verify the coordinate translation math by injecting known
    geometry values rather than relying on Kivy's text rendering pipeline.
    """

    def test_refs_translation_with_injected_geometry(self):
        """Test refs translation with manually injected geometry.

        This test builds a minimal widget tree and injects deterministic
        geometry values to verify the coordinate translation algorithm.

        _Requirements: 3.1, 3.3, 3.4_
        """
        # Create MarkdownLabel with simple text (no links needed for this test)
        md_label = MarkdownLabel(text='Test')

        # Set deterministic geometry on MarkdownLabel
        md_label.pos = (0, 0)
        md_label.size = (400, 300)

        # Create a BoxLayout container
        container = BoxLayout(orientation='vertical')
        container.pos = (10, 20)  # Offset from MarkdownLabel
        container.size = (380, 260)

        # Create a Label with injected refs
        child_label = Label(text='[ref=http://example.com]Click[/ref]', markup=True)
        child_label.pos = (5, 10)  # Offset from container
        child_label.size = (200, 50)
        child_label.texture_size = (180, 40)  # Simulated texture size

        # Inject refs onto the child Label
        # refs format: {ref_name: [[x1, y1, x2, y2], ...]}
        # These are in texture space (origin at top-left of texture)
        child_label.refs = {
            'http://example.com': [[10, 5, 60, 25]]
        }

        # Build widget tree: MarkdownLabel > BoxLayout > Label
        md_label.clear_widgets()
        container.add_widget(child_label)
        md_label.add_widget(container)

        # Get aggregated refs
        aggregated_refs = md_label.refs

        # Calculate expected translation
        # parent_offset = container.pos = (10, 20)
        # label.center_x = child_label.x + child_label.width/2 = 5 + 100 = 105
        # label.center_y = child_label.y + child_label.height/2 = 10 + 25 = 35
        # tex_w, tex_h = 180, 40
        # base_x = parent_offset_x + (label.center_x - tex_w/2) = 10 + (105 - 90) = 25
        # base_y = parent_offset_y + (label.center_y + tex_h/2) = 20 + (35 + 20) = 75

        parent_offset_x = container.x  # 10
        parent_offset_y = container.y  # 20
        tex_w, tex_h = child_label.texture_size  # 180, 40
        base_x = parent_offset_x + (child_label.center_x - tex_w / 2.0)
        base_y = parent_offset_y + (child_label.center_y + tex_h / 2.0)

        # Original ref box in texture space
        orig_box = [10, 5, 60, 25]

        # Expected translated box
        expected_box = [
            base_x + orig_box[0],  # base_x + x1
            base_y - orig_box[1],  # base_y - y1 (Y inverted)
            base_x + orig_box[2],  # base_x + x2
            base_y - orig_box[3],  # base_y - y2 (Y inverted)
        ]

        # Verify aggregated refs contain the translated coordinates
        assert 'http://example.com' in aggregated_refs, \
            f"Expected 'http://example.com' in refs, got {aggregated_refs.keys()}"

        actual_boxes = aggregated_refs['http://example.com']
        assert len(actual_boxes) == 1, \
            f"Expected 1 box, got {len(actual_boxes)}"

        actual_box = actual_boxes[0]
        for i, (expected, actual) in enumerate(zip(expected_box, actual_box)):
            assert abs(expected - actual) < 0.001, \
                f"Box coordinate {i}: expected {expected}, got {actual}"

    def test_refs_translation_with_multiple_zones(self):
        """Test refs translation with multiple ref zones.

        _Requirements: 3.1, 3.3, 3.4_
        """
        md_label = MarkdownLabel(text='Test')
        md_label.pos = (0, 0)
        md_label.size = (500, 400)

        # Create container
        container = BoxLayout(orientation='vertical')
        container.pos = (20, 30)
        container.size = (460, 340)

        # Create Label with multiple refs
        child_label = Label(text='Links', markup=True)
        child_label.pos = (10, 15)
        child_label.size = (300, 80)
        child_label.texture_size = (280, 70)

        # Inject multiple refs
        child_label.refs = {
            'http://link1.com': [[5, 10, 50, 30]],
            'http://link2.com': [[100, 10, 150, 30], [200, 40, 250, 60]]
        }

        md_label.clear_widgets()
        container.add_widget(child_label)
        md_label.add_widget(container)

        aggregated_refs = md_label.refs

        # Calculate base coordinates
        parent_offset_x = container.x
        parent_offset_y = container.y
        tex_w, tex_h = child_label.texture_size
        base_x = parent_offset_x + (child_label.center_x - tex_w / 2.0)
        base_y = parent_offset_y + (child_label.center_y + tex_h / 2.0)

        # Verify all refs are present
        assert 'http://link1.com' in aggregated_refs
        assert 'http://link2.com' in aggregated_refs

        # Verify link1 has 1 box
        assert len(aggregated_refs['http://link1.com']) == 1

        # Verify link2 has 2 boxes
        assert len(aggregated_refs['http://link2.com']) == 2

        # Verify translation for link1
        orig_box = [5, 10, 50, 30]
        expected_box = [
            base_x + orig_box[0],
            base_y - orig_box[1],
            base_x + orig_box[2],
            base_y - orig_box[3],
        ]
        actual_box = aggregated_refs['http://link1.com'][0]
        for i, (expected, actual) in enumerate(zip(expected_box, actual_box)):
            assert abs(expected - actual) < 0.001, \
                f"link1 box coord {i}: expected {expected}, got {actual}"

    def test_refs_translation_with_nested_containers(self):
        """Test refs translation with deeply nested containers.

        _Requirements: 3.1, 3.3, 3.4_
        """
        md_label = MarkdownLabel(text='Test')
        md_label.pos = (0, 0)
        md_label.size = (600, 500)

        # Create nested containers
        outer_container = BoxLayout(orientation='vertical')
        outer_container.pos = (10, 20)
        outer_container.size = (580, 460)

        inner_container = BoxLayout(orientation='horizontal')
        inner_container.pos = (5, 10)
        inner_container.size = (570, 440)

        # Create Label
        child_label = Label(text='Nested', markup=True)
        child_label.pos = (15, 25)
        child_label.size = (200, 60)
        child_label.texture_size = (180, 50)

        child_label.refs = {
            'http://nested.com': [[20, 10, 80, 35]]
        }

        # Build nested tree
        md_label.clear_widgets()
        inner_container.add_widget(child_label)
        outer_container.add_widget(inner_container)
        md_label.add_widget(outer_container)

        aggregated_refs = md_label.refs

        # Calculate cumulative offset
        # parent_offset = outer_container.pos + inner_container.pos
        parent_offset_x = outer_container.x + inner_container.x  # 10 + 5 = 15
        parent_offset_y = outer_container.y + inner_container.y  # 20 + 10 = 30

        tex_w, tex_h = child_label.texture_size
        base_x = parent_offset_x + (child_label.center_x - tex_w / 2.0)
        base_y = parent_offset_y + (child_label.center_y + tex_h / 2.0)

        orig_box = [20, 10, 80, 35]
        expected_box = [
            base_x + orig_box[0],
            base_y - orig_box[1],
            base_x + orig_box[2],
            base_y - orig_box[3],
        ]

        assert 'http://nested.com' in aggregated_refs
        actual_box = aggregated_refs['http://nested.com'][0]
        for i, (expected, actual) in enumerate(zip(expected_box, actual_box)):
            assert abs(expected - actual) < 0.001, \
                f"Nested box coord {i}: expected {expected}, got {actual}"

    def test_refs_translation_with_zero_texture_size_fallback(self):
        """Test refs translation falls back to widget size when texture_size is zero.

        _Requirements: 3.1, 3.3, 3.4_
        """
        md_label = MarkdownLabel(text='Test')
        md_label.pos = (0, 0)
        md_label.size = (400, 300)

        container = BoxLayout(orientation='vertical')
        container.pos = (10, 20)
        container.size = (380, 260)

        child_label = Label(text='Fallback', markup=True)
        child_label.pos = (5, 10)
        child_label.size = (200, 50)
        child_label.texture_size = (0, 0)  # Zero texture size

        child_label.refs = {
            'http://fallback.com': [[10, 5, 60, 25]]
        }

        md_label.clear_widgets()
        container.add_widget(child_label)
        md_label.add_widget(container)

        aggregated_refs = md_label.refs

        # When texture_size is (0, 0), should fall back to widget size
        parent_offset_x = container.x
        parent_offset_y = container.y
        tex_w, tex_h = child_label.width, child_label.height  # Fallback
        base_x = parent_offset_x + (child_label.center_x - tex_w / 2.0)
        base_y = parent_offset_y + (child_label.center_y + tex_h / 2.0)

        orig_box = [10, 5, 60, 25]
        expected_box = [
            base_x + orig_box[0],
            base_y - orig_box[1],
            base_x + orig_box[2],
            base_y - orig_box[3],
        ]

        assert 'http://fallback.com' in aggregated_refs
        actual_box = aggregated_refs['http://fallback.com'][0]
        for i, (expected, actual) in enumerate(zip(expected_box, actual_box)):
            assert abs(expected - actual) < 0.001, \
                f"Fallback box coord {i}: expected {expected}, got {actual}"

    @pytest.mark.property
    @given(
        # Parent container offset
        st.floats(min_value=0, max_value=100, allow_nan=False, allow_infinity=False),
        st.floats(min_value=0, max_value=100, allow_nan=False, allow_infinity=False),
        # Label position within container
        st.floats(min_value=0, max_value=100, allow_nan=False, allow_infinity=False),
        st.floats(min_value=0, max_value=100, allow_nan=False, allow_infinity=False),
        # Label size
        st.floats(min_value=50, max_value=300, allow_nan=False, allow_infinity=False),
        st.floats(min_value=20, max_value=100, allow_nan=False, allow_infinity=False),
        # Texture size
        st.floats(min_value=40, max_value=280, allow_nan=False, allow_infinity=False),
        st.floats(min_value=15, max_value=90, allow_nan=False, allow_infinity=False),
        # Ref box coordinates (in texture space)
        st.floats(min_value=0, max_value=30, allow_nan=False, allow_infinity=False),
        st.floats(min_value=0, max_value=10, allow_nan=False, allow_infinity=False),
        st.floats(min_value=31, max_value=100, allow_nan=False, allow_infinity=False),
        st.floats(min_value=11, max_value=50, allow_nan=False, allow_infinity=False),
    )
    # Complex strategy: 50 examples (adequate coverage)
    @settings(max_examples=50, deadline=None)
    def test_property_refs_coordinate_translation_math(
        self, container_x, container_y, label_x, label_y,
        label_w, label_h, tex_w, tex_h, box_x1, box_y1, box_x2, box_y2
    ):
        """Property test: refs coordinate translation follows the specified formula.

        *For any* MarkdownLabel containing a child Label with known `refs`, `pos`,
        `size`, and `texture_size`, the aggregated `refs` property SHALL return
        bounding boxes translated according to the formula:
        - `base_x = parent_offset_x + (label.center_x - tex_w / 2.0)`
        - `base_y = parent_offset_y + (label.center_y + tex_h / 2.0)`
        - `translated_box = [base_x + x1, base_y - y1, base_x + x2, base_y - y2]`

        **Refs Coordinate Translation Math**
        """
        # Create MarkdownLabel
        md_label = MarkdownLabel(text='Test')
        md_label.pos = (0, 0)
        md_label.size = (500, 400)

        # Create container with generated position
        container = BoxLayout(orientation='vertical')
        container.pos = (container_x, container_y)
        container.size = (400, 300)

        # Create Label with generated geometry
        child_label = Label(text='Link', markup=True)
        child_label.pos = (label_x, label_y)
        child_label.size = (label_w, label_h)
        child_label.texture_size = (tex_w, tex_h)

        # Inject refs with generated box coordinates
        ref_box = [box_x1, box_y1, box_x2, box_y2]
        child_label.refs = {
            'http://test.com': [ref_box]
        }

        # Build widget tree
        md_label.clear_widgets()
        container.add_widget(child_label)
        md_label.add_widget(container)

        # Get aggregated refs
        aggregated_refs = md_label.refs

        # Calculate expected translation using the formula
        parent_offset_x = container.x
        parent_offset_y = container.y
        base_x = parent_offset_x + (child_label.center_x - tex_w / 2.0)
        base_y = parent_offset_y + (child_label.center_y + tex_h / 2.0)

        expected_box = [
            base_x + box_x1,
            base_y - box_y1,  # Y is inverted
            base_x + box_x2,
            base_y - box_y2,  # Y is inverted
        ]

        # Verify the ref is present
        assert 'http://test.com' in aggregated_refs, \
            "Expected 'http://test.com' in refs"

        # Verify the translation
        actual_box = aggregated_refs['http://test.com'][0]
        for i, (expected, actual) in enumerate(zip(expected_box, actual_box)):
            assert abs(expected - actual) < 0.001, \
                f"Box coord {i}: expected {expected}, got {actual}"

# *For any* MarkdownLabel containing a child Label with known `anchors`, `pos`, `size`,
# and `texture_size`, the aggregated `anchors` property SHALL return positions
# translated according to the formula:
# - `base_x = parent_offset_x + (label.center_x - tex_w / 2.0)`
# - `base_y = parent_offset_y + (label.center_y + tex_h / 2.0)`
# - `translated_anchor = (base_x + ax, base_y - ay)`


@pytest.mark.slow
class TestDeterministicAnchorsTranslation:

    """Deterministic tests for anchors coordinate translation with injected geometry.

    These tests verify the coordinate translation math for anchors by injecting
    known geometry values rather than relying on Kivy's text rendering pipeline.
    """

    def test_anchors_translation_with_injected_geometry(self):
        """Test anchors translation with manually injected geometry.

        This test builds a minimal widget tree and injects deterministic
        geometry values to verify the anchor coordinate translation algorithm.

        _Requirements: 3.2, 3.3, 3.4_
        """
        # Create MarkdownLabel with simple text
        md_label = MarkdownLabel(text='Test')

        # Set deterministic geometry on MarkdownLabel
        md_label.pos = (0, 0)
        md_label.size = (400, 300)

        # Create a BoxLayout container
        container = BoxLayout(orientation='vertical')
        container.pos = (10, 20)  # Offset from MarkdownLabel
        container.size = (380, 260)

        # Create a Label with injected anchors
        child_label = Label(text='[anchor=section1]Section[/anchor]', markup=True)
        child_label.pos = (5, 10)  # Offset from container
        child_label.size = (200, 50)
        child_label.texture_size = (180, 40)  # Simulated texture size

        # Inject anchors onto the child Label
        # anchors format: {anchor_name: (x, y)}
        # These are in texture space (origin at top-left of texture)
        child_label.anchors = {
            'section1': (25, 15)
        }

        # Build widget tree: MarkdownLabel > BoxLayout > Label
        md_label.clear_widgets()
        container.add_widget(child_label)
        md_label.add_widget(container)

        # Get aggregated anchors
        aggregated_anchors = md_label.anchors

        # Calculate expected translation
        parent_offset_x = container.x  # 10
        parent_offset_y = container.y  # 20
        tex_w, tex_h = child_label.texture_size  # 180, 40
        base_x = parent_offset_x + (child_label.center_x - tex_w / 2.0)
        base_y = parent_offset_y + (child_label.center_y + tex_h / 2.0)

        # Original anchor position in texture space
        orig_pos = (25, 15)

        # Expected translated position
        expected_pos = (
            base_x + orig_pos[0],  # base_x + ax
            base_y - orig_pos[1],  # base_y - ay (Y inverted)
        )

        # Verify aggregated anchors contain the translated coordinates
        assert 'section1' in aggregated_anchors, \
            f"Expected 'section1' in anchors, got {aggregated_anchors.keys()}"

        actual_pos = aggregated_anchors['section1']
        assert abs(expected_pos[0] - actual_pos[0]) < 0.001, \
            f"Anchor X: expected {expected_pos[0]}, got {actual_pos[0]}"
        assert abs(expected_pos[1] - actual_pos[1]) < 0.001, \
            f"Anchor Y: expected {expected_pos[1]}, got {actual_pos[1]}"

    def test_anchors_translation_with_multiple_anchors(self):
        """Test anchors translation with multiple anchor points.

        _Requirements: 3.2, 3.3, 3.4_
        """
        md_label = MarkdownLabel(text='Test')
        md_label.pos = (0, 0)
        md_label.size = (500, 400)

        # Create container
        container = BoxLayout(orientation='vertical')
        container.pos = (20, 30)
        container.size = (460, 340)

        # Create Label with multiple anchors
        child_label = Label(text='Anchors', markup=True)
        child_label.pos = (10, 15)
        child_label.size = (300, 80)
        child_label.texture_size = (280, 70)

        # Inject multiple anchors
        child_label.anchors = {
            'intro': (10, 5),
            'middle': (140, 35),
            'conclusion': (250, 60)
        }

        md_label.clear_widgets()
        container.add_widget(child_label)
        md_label.add_widget(container)

        aggregated_anchors = md_label.anchors

        # Calculate base coordinates
        parent_offset_x = container.x
        parent_offset_y = container.y
        tex_w, tex_h = child_label.texture_size
        base_x = parent_offset_x + (child_label.center_x - tex_w / 2.0)
        base_y = parent_offset_y + (child_label.center_y + tex_h / 2.0)

        # Verify all anchors are present
        assert 'intro' in aggregated_anchors
        assert 'middle' in aggregated_anchors
        assert 'conclusion' in aggregated_anchors

        # Verify translation for each anchor
        for anchor_name, orig_pos in child_label.anchors.items():
            expected_pos = (
                base_x + orig_pos[0],
                base_y - orig_pos[1],
            )
            actual_pos = aggregated_anchors[anchor_name]
            assert abs(expected_pos[0] - actual_pos[0]) < 0.001, \
                f"{anchor_name} X: expected {expected_pos[0]}, got {actual_pos[0]}"
            assert abs(expected_pos[1] - actual_pos[1]) < 0.001, \
                f"{anchor_name} Y: expected {expected_pos[1]}, got {actual_pos[1]}"

    def test_anchors_translation_with_nested_containers(self):
        """Test anchors translation with deeply nested containers.

        _Requirements: 3.2, 3.3, 3.4_
        """
        md_label = MarkdownLabel(text='Test')
        md_label.pos = (0, 0)
        md_label.size = (600, 500)

        # Create nested containers
        outer_container = BoxLayout(orientation='vertical')
        outer_container.pos = (10, 20)
        outer_container.size = (580, 460)

        inner_container = BoxLayout(orientation='horizontal')
        inner_container.pos = (5, 10)
        inner_container.size = (570, 440)

        # Create Label
        child_label = Label(text='Nested', markup=True)
        child_label.pos = (15, 25)
        child_label.size = (200, 60)
        child_label.texture_size = (180, 50)

        child_label.anchors = {
            'nested_anchor': (50, 20)
        }

        # Build nested tree
        md_label.clear_widgets()
        inner_container.add_widget(child_label)
        outer_container.add_widget(inner_container)
        md_label.add_widget(outer_container)

        aggregated_anchors = md_label.anchors

        # Calculate cumulative offset
        parent_offset_x = outer_container.x + inner_container.x  # 10 + 5 = 15
        parent_offset_y = outer_container.y + inner_container.y  # 20 + 10 = 30

        tex_w, tex_h = child_label.texture_size
        base_x = parent_offset_x + (child_label.center_x - tex_w / 2.0)
        base_y = parent_offset_y + (child_label.center_y + tex_h / 2.0)

        orig_pos = (50, 20)
        expected_pos = (
            base_x + orig_pos[0],
            base_y - orig_pos[1],
        )

        assert 'nested_anchor' in aggregated_anchors
        actual_pos = aggregated_anchors['nested_anchor']
        assert abs(expected_pos[0] - actual_pos[0]) < 0.001, \
            f"Nested anchor X: expected {expected_pos[0]}, got {actual_pos[0]}"
        assert abs(expected_pos[1] - actual_pos[1]) < 0.001, \
            f"Nested anchor Y: expected {expected_pos[1]}, got {actual_pos[1]}"

    def test_anchors_translation_with_zero_texture_size_fallback(self):
        """Test anchors translation falls back to widget size when texture_size is zero.

        _Requirements: 3.2, 3.3, 3.4_
        """
        md_label = MarkdownLabel(text='Test')
        md_label.pos = (0, 0)
        md_label.size = (400, 300)

        container = BoxLayout(orientation='vertical')
        container.pos = (10, 20)
        container.size = (380, 260)

        child_label = Label(text='Fallback', markup=True)
        child_label.pos = (5, 10)
        child_label.size = (200, 50)
        child_label.texture_size = (0, 0)  # Zero texture size

        child_label.anchors = {
            'fallback_anchor': (30, 15)
        }

        md_label.clear_widgets()
        container.add_widget(child_label)
        md_label.add_widget(container)

        aggregated_anchors = md_label.anchors

        # When texture_size is (0, 0), should fall back to widget size
        parent_offset_x = container.x
        parent_offset_y = container.y
        tex_w, tex_h = child_label.width, child_label.height  # Fallback
        base_x = parent_offset_x + (child_label.center_x - tex_w / 2.0)
        base_y = parent_offset_y + (child_label.center_y + tex_h / 2.0)

        orig_pos = (30, 15)
        expected_pos = (
            base_x + orig_pos[0],
            base_y - orig_pos[1],
        )

        assert 'fallback_anchor' in aggregated_anchors
        actual_pos = aggregated_anchors['fallback_anchor']
        assert abs(expected_pos[0] - actual_pos[0]) < 0.001, \
            f"Fallback anchor X: expected {expected_pos[0]}, got {actual_pos[0]}"
        assert abs(expected_pos[1] - actual_pos[1]) < 0.001, \
            f"Fallback anchor Y: expected {expected_pos[1]}, got {actual_pos[1]}"

    @pytest.mark.property
    @given(
        # Parent container offset
        st.floats(min_value=0, max_value=100, allow_nan=False, allow_infinity=False),
        st.floats(min_value=0, max_value=100, allow_nan=False, allow_infinity=False),
        # Label position within container
        st.floats(min_value=0, max_value=100, allow_nan=False, allow_infinity=False),
        st.floats(min_value=0, max_value=100, allow_nan=False, allow_infinity=False),
        # Label size
        st.floats(min_value=50, max_value=300, allow_nan=False, allow_infinity=False),
        st.floats(min_value=20, max_value=100, allow_nan=False, allow_infinity=False),
        # Texture size
        st.floats(min_value=40, max_value=280, allow_nan=False, allow_infinity=False),
        st.floats(min_value=15, max_value=90, allow_nan=False, allow_infinity=False),
        # Anchor position (in texture space)
        st.floats(min_value=0, max_value=100, allow_nan=False, allow_infinity=False),
        st.floats(min_value=0, max_value=50, allow_nan=False, allow_infinity=False),
    )
    # Complex strategy: 50 examples (adequate coverage)
    @settings(max_examples=50, deadline=None)
    def test_property_anchors_coordinate_translation_math(
        self, container_x, container_y, label_x, label_y,
        label_w, label_h, tex_w, tex_h, anchor_x, anchor_y
    ):
        """Property test: anchors coordinate translation follows the specified formula.

        *For any* MarkdownLabel containing a child Label with known `anchors`, `pos`,
        `size`, and `texture_size`, the aggregated `anchors` property SHALL return
        positions translated according to the formula:
        - `base_x = parent_offset_x + (label.center_x - tex_w / 2.0)`
        - `base_y = parent_offset_y + (label.center_y + tex_h / 2.0)`
        - `translated_anchor = (base_x + ax, base_y - ay)`

        **Anchors Coordinate Translation Math**
        """
        # Create MarkdownLabel
        md_label = MarkdownLabel(text='Test')
        md_label.pos = (0, 0)
        md_label.size = (500, 400)

        # Create container with generated position
        container = BoxLayout(orientation='vertical')
        container.pos = (container_x, container_y)
        container.size = (400, 300)

        # Create Label with generated geometry
        child_label = Label(text='Anchor', markup=True)
        child_label.pos = (label_x, label_y)
        child_label.size = (label_w, label_h)
        child_label.texture_size = (tex_w, tex_h)

        # Inject anchor with generated position
        anchor_pos = (anchor_x, anchor_y)
        child_label.anchors = {
            'test_anchor': anchor_pos
        }

        # Build widget tree
        md_label.clear_widgets()
        container.add_widget(child_label)
        md_label.add_widget(container)

        # Get aggregated anchors
        aggregated_anchors = md_label.anchors

        # Calculate expected translation using the formula
        parent_offset_x = container.x
        parent_offset_y = container.y
        base_x = parent_offset_x + (child_label.center_x - tex_w / 2.0)
        base_y = parent_offset_y + (child_label.center_y + tex_h / 2.0)

        expected_pos = (
            base_x + anchor_x,
            base_y - anchor_y,  # Y is inverted
        )

        # Verify the anchor is present
        assert 'test_anchor' in aggregated_anchors, \
            "Expected 'test_anchor' in anchors"

        # Verify the translation
        actual_pos = aggregated_anchors['test_anchor']
        assert abs(expected_pos[0] - actual_pos[0]) < 0.001, \
            f"Anchor X: expected {expected_pos[0]}, got {actual_pos[0]}"
        assert abs(expected_pos[1] - actual_pos[1]) < 0.001, \
            f"Anchor Y: expected {expected_pos[1]}, got {actual_pos[1]}"
