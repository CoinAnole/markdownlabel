"""
Property-based tests for font-related properties in MarkdownLabel widget.

Tests verify that font properties (font_name, line_height, font_size, etc.)
are correctly forwarded to child Label widgets and that font scaling
behavior works correctly for headings.
"""

import pytest
from hypothesis import given, strategies as st, settings, assume

from kivy.uix.label import Label

from kivy_garden.markdownlabel import MarkdownLabel
from .test_utils import (
    KIVY_FONTS,
    simple_markdown_document,
    find_labels_recursive,
    floats_equal,
    collect_widget_ids,
    st_alphanumeric_text,
    st_font_size
)


# Strategy for generating valid line_height values
line_height_strategy = st.floats(min_value=0.5, max_value=3.0, allow_nan=False, allow_infinity=False)


# *For any* Markdown text and any font_name value, all internal Labels SHALL have
# `font_name` set to the specified value, except code blocks which preserve their
# code_font_name setting.

class TestFontNamePropertyForwarding:
    """Property tests for font_name forwarding."""

    @pytest.mark.parametrize('font_name', KIVY_FONTS)
    def test_font_name_applied_to_paragraph(self, font_name):
        """font_name is applied to paragraph Labels."""
        label = MarkdownLabel(text='Hello World', font_name=font_name)

        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"

        # All labels should have the specified font_name
        for lbl in labels:
            assert lbl.font_name == font_name, \
                f"Expected font_name={font_name}, got {lbl.font_name}"

    @pytest.mark.parametrize('font_name', KIVY_FONTS)
    def test_font_name_applied_to_heading(self, font_name):
        """font_name is applied to heading Labels."""
        label = MarkdownLabel(text='# Heading', font_name=font_name)

        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"

        # All labels should have the specified font_name
        for lbl in labels:
            assert lbl.font_name == font_name, \
                f"Expected font_name={font_name}, got {lbl.font_name}"

    @pytest.mark.parametrize('font_name', KIVY_FONTS)
    def test_code_block_preserves_code_font_name(self, font_name):
        """Code blocks preserve code_font_name regardless of font_name setting."""
        code_font = 'RobotoMono-Regular'
        markdown = '```python\nprint("hello")\n```'

        label = MarkdownLabel(
            text=markdown,
            font_name=font_name,
            code_font_name=code_font
        )

        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label for code block"

        # Code block labels should use code_font_name, not font_name
        for lbl in labels:
            assert lbl.font_name == code_font, \
                f"Code label should use code_font_name={code_font}, got {lbl.font_name}"

    @pytest.mark.parametrize('font_name', ['Roboto', 'Roboto-Bold', 'Roboto-Italic'])
    def test_mixed_content_font_separation(self, font_name):
        """Mixed content correctly separates font_name and code_font_name."""
        code_font = 'RobotoMono-Regular'
        markdown = 'Regular text\n\n```\ncode\n```\n\nMore text'

        label = MarkdownLabel(
            text=markdown,
            font_name=font_name,
            code_font_name=code_font
        )

        labels = find_labels_recursive(label)
        assert len(labels) >= 2, "Expected at least 2 Labels (text + code)"

        # Separate labels by font
        body_labels = [l for l in labels if l.font_name == font_name]
        code_labels = [l for l in labels if l.font_name == code_font]

        # Should have both body and code labels
        assert len(body_labels) >= 1, "Expected at least one body text label"
        assert len(code_labels) >= 1, "Expected at least one code label"

    @pytest.mark.parametrize('font1,font2', [
        ('Roboto', 'Roboto-Bold'), ('Roboto', 'Roboto-Italic'),
        ('Roboto-Bold', 'Roboto'), ('Roboto-Bold', 'Roboto-Italic'),
        ('Roboto-Italic', 'Roboto'), ('Roboto-Italic', 'Roboto-Bold')
    ])
    def test_font_name_property_forwarding_triggers_rebuild(self, font1, font2):
        """Changing font_name triggers widget rebuild with new font."""
        label = MarkdownLabel(text='Hello World', font_name=font1)

        # Collect widget IDs before change
        ids_before = collect_widget_ids(label)

        # Verify initial font
        labels = find_labels_recursive(label)
        for lbl in labels:
            assert lbl.font_name == font1

        # Change font_name
        label.font_name = font2
        label.force_rebuild()  # Force immediate rebuild for test

        # Verify rebuild occurred
        ids_after = collect_widget_ids(label)
        assert ids_before != ids_after, "Widget tree should rebuild for font_name changes"

        # Verify new font
        labels = find_labels_recursive(label)
        for lbl in labels:
            assert lbl.font_name == font2, \
                f"After change, expected font_name={font2}, got {lbl.font_name}"

    @pytest.mark.parametrize('font_name', KIVY_FONTS)
    def test_font_name_applied_to_list_items(self, font_name):
        """font_name is applied to list item Labels."""
        markdown = '- Item 1\n- Item 2'
        label = MarkdownLabel(text=markdown, font_name=font_name)

        labels = find_labels_recursive(label)
        assert len(labels) >= 2, "Expected at least 2 Labels for list items"

        # All labels should have the specified font_name
        for lbl in labels:
            assert lbl.font_name == font_name, \
                f"Expected font_name={font_name}, got {lbl.font_name}"

    @pytest.mark.parametrize('font_name', KIVY_FONTS)
    def test_font_name_applied_to_table_cells(self, font_name):
        """font_name is applied to table cell Labels."""
        markdown = '| A | B |\n| --- | --- |\n| 1 | 2 |'
        label = MarkdownLabel(text=markdown, font_name=font_name)

        labels = find_labels_recursive(label)
        assert len(labels) >= 4, "Expected at least 4 Labels for table cells"

        # All labels should have the specified font_name
        for lbl in labels:
            assert lbl.font_name == font_name, \
                f"Expected font_name={font_name}, got {lbl.font_name}"


# *For any* Markdown text and any line_height value, all internal Labels SHALL have
# `line_height` set to the specified value.

class TestLineHeightPropertyForwarding:
    """Property tests for line_height forwarding."""

    @pytest.mark.property
    @given(line_height_strategy)
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_line_height_applied_to_paragraph(self, line_height):
        """line_height is applied to paragraph Labels."""
        label = MarkdownLabel(text='Hello World', line_height=line_height)

        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"

        # All labels should have the specified line_height
        for lbl in labels:
            assert floats_equal(lbl.line_height, line_height), \
                f"Expected line_height={line_height}, got {lbl.line_height}"

    @pytest.mark.property
    @given(line_height_strategy)
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_line_height_applied_to_heading(self, line_height):
        """line_height is applied to heading Labels."""
        label = MarkdownLabel(text='# Heading', line_height=line_height)

        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label"

        # All labels should have the specified line_height
        for lbl in labels:
            assert floats_equal(lbl.line_height, line_height), \
                f"Expected line_height={line_height}, got {lbl.line_height}"

    @pytest.mark.property
    @given(line_height_strategy)
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_line_height_applied_to_code_block(self, line_height):
        """line_height is applied to code block Labels."""
        markdown = '```python\nprint("hello")\n```'

        label = MarkdownLabel(text=markdown, line_height=line_height)

        labels = find_labels_recursive(label)
        assert len(labels) >= 1, "Expected at least one Label for code block"

        # Code block labels should also have the specified line_height
        for lbl in labels:
            assert floats_equal(lbl.line_height, line_height), \
                f"Expected line_height={line_height}, got {lbl.line_height}"

    @pytest.mark.property
    @given(line_height_strategy, line_height_strategy)
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_line_height_change_triggers_rebuild(self, lh1, lh2):
        """Changing line_height triggers widget rebuild with new value."""
        assume(not floats_equal(lh1, lh2))

        label = MarkdownLabel(text='Hello World', line_height=lh1)

        # Collect widget IDs before change
        ids_before = collect_widget_ids(label)

        # Verify initial line_height
        labels = find_labels_recursive(label)
        for lbl in labels:
            assert floats_equal(lbl.line_height, lh1)

        # Change line_height
        label.line_height = lh2
        label.force_rebuild()  # Force immediate rebuild for test

        # Verify rebuild occurred
        ids_after = collect_widget_ids(label)
        assert ids_before != ids_after, "Widget tree should rebuild for line_height changes"

        # Verify new line_height
        labels = find_labels_recursive(label)
        for lbl in labels:
            assert floats_equal(lbl.line_height, lh2), \
                f"After change, expected line_height={lh2}, got {lbl.line_height}"

    @pytest.mark.property
    @given(line_height_strategy)
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_line_height_applied_to_list_items(self, line_height):
        """line_height is applied to list item Labels."""
        markdown = '- Item 1\n- Item 2'
        label = MarkdownLabel(text=markdown, line_height=line_height)

        labels = find_labels_recursive(label)
        assert len(labels) >= 2, "Expected at least 2 Labels for list items"

        # All labels should have the specified line_height
        for lbl in labels:
            assert floats_equal(lbl.line_height, line_height), \
                f"Expected line_height={line_height}, got {lbl.line_height}"

    @pytest.mark.property
    @given(line_height_strategy)
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_line_height_applied_to_table_cells(self, line_height):
        """line_height is applied to table cell Labels."""
        markdown = '| A | B |\n| --- | --- |\n| 1 | 2 |'
        label = MarkdownLabel(text=markdown, line_height=line_height)

        labels = find_labels_recursive(label)
        assert len(labels) >= 4, "Expected at least 4 Labels for table cells"

        # All labels should have the specified line_height
        for lbl in labels:
            assert floats_equal(lbl.line_height, line_height), \
                f"Expected line_height={line_height}, got {lbl.line_height}"

    @pytest.mark.property
    @given(line_height_strategy)
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_line_height_applied_to_all_content_types(self, line_height):
        """line_height is applied to all content types including code."""
        markdown = 'Regular text\n\n```\ncode\n```\n\n# Heading\n\n- List item'

        label = MarkdownLabel(text=markdown, line_height=line_height)

        labels = find_labels_recursive(label)
        assert len(labels) >= 3, "Expected at least 3 Labels"

        # All labels should have the specified line_height
        for lbl in labels:
            assert floats_equal(lbl.line_height, line_height), \
                f"Expected line_height={line_height}, got {lbl.line_height}"


# *For any* font advanced properties (font_family, font_context, font_features,
# font_hinting, font_kerning), all Labels SHALL receive these properties EXCEPT
# font_family which is excluded from code blocks to preserve monospace appearance.

class TestAdvancedFontPropertyForwarding:
    """Property tests for font advanced property forwarding.

    This test class verifies that font advanced properties are correctly
    forwarded to child Labels, with the special case that font_family
    is excluded from code blocks to preserve monospace appearance.
    """

    def _find_code_block_labels(self, widget):
        """Find Labels that are inside code block containers.

        Code block containers have a 'language_info' attribute.
        """
        code_labels = []

        def find_in_container(container):
            if hasattr(container, 'language_info'):
                # This is a code block container
                for child in container.children:
                    if isinstance(child, Label):
                        code_labels.append(child)
            if hasattr(container, 'children'):
                for child in container.children:
                    find_in_container(child)

        find_in_container(widget)
        return code_labels

    def _find_non_code_labels(self, widget):
        """Find Labels that are NOT inside code block containers."""
        all_labels = find_labels_recursive(widget)
        code_labels = self._find_code_block_labels(widget)
        return [lbl for lbl in all_labels if lbl not in code_labels]

    @pytest.mark.property
    @given(st_alphanumeric_text(min_size=1, max_size=30))
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_font_family_excluded_from_code_blocks(self, font_family_value):
        """font_family is NOT forwarded to code block Labels."""
        # Create markdown with both regular text and code block
        markdown = 'Regular paragraph\n\n```python\ncode here\n```'
        label = MarkdownLabel(text=markdown, font_family=font_family_value)

        # Find code block labels
        code_labels = self._find_code_block_labels(label)

        # Code block labels should NOT have font_family set
        for lbl in code_labels:
            assert lbl.font_family is None, \
                f"Code block should not have font_family, got {lbl.font_family!r}"

    @pytest.mark.property
    @given(st_alphanumeric_text(min_size=1, max_size=30))
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_font_family_forwarded_to_non_code_labels(self, font_family_value):
        """font_family IS forwarded to non-code block Labels."""
        # Create markdown with both regular text and code block
        markdown = 'Regular paragraph\n\n```python\ncode here\n```'
        label = MarkdownLabel(text=markdown, font_family=font_family_value)

        # Find non-code labels
        non_code_labels = self._find_non_code_labels(label)
        assert len(non_code_labels) >= 1, "Expected at least 1 non-code Label"

        # Non-code labels should have font_family set
        for lbl in non_code_labels:
            assert lbl.font_family == font_family_value, \
                f"Expected font_family={font_family_value!r}, got {lbl.font_family!r}"

    @pytest.mark.property
    @given(st_alphanumeric_text(min_size=1, max_size=30))
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_font_context_forwarded_to_all_labels_including_code(self, font_context_value):
        """font_context IS forwarded to ALL Labels including code blocks."""
        # Create markdown with both regular text and code block
        markdown = 'Regular paragraph\n\n```python\ncode here\n```'
        label = MarkdownLabel(text=markdown, font_context=font_context_value)

        # Find all labels
        all_labels = find_labels_recursive(label)
        assert len(all_labels) >= 2, "Expected at least 2 Labels (paragraph + code)"

        # All labels should have font_context set
        for lbl in all_labels:
            assert lbl.font_context == font_context_value, \
                f"Expected font_context={font_context_value!r}, got {lbl.font_context!r}"

    @pytest.mark.property
    @given(st_alphanumeric_text(min_size=0, max_size=50))
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_font_features_forwarded_to_all_labels_including_code(self, font_features_value):
        """font_features IS forwarded to ALL Labels including code blocks."""
        # Create markdown with both regular text and code block
        markdown = 'Regular paragraph\n\n```python\ncode here\n```'
        label = MarkdownLabel(text=markdown, font_features=font_features_value)

        # Find all labels
        all_labels = find_labels_recursive(label)
        assert len(all_labels) >= 2, "Expected at least 2 Labels (paragraph + code)"

        # All labels should have font_features set
        for lbl in all_labels:
            assert lbl.font_features == font_features_value, \
                f"Expected font_features={font_features_value!r}, got {lbl.font_features!r}"

    @pytest.mark.parametrize('font_hinting_value', [None, 'normal', 'light', 'mono'])
    def test_font_hinting_forwarded_to_all_labels_including_code(self, font_hinting_value):
        """font_hinting IS forwarded to ALL Labels including code blocks."""
        # Create markdown with both regular text and code block
        markdown = 'Regular paragraph\n\n```python\ncode here\n```'
        label = MarkdownLabel(text=markdown, font_hinting=font_hinting_value)

        # Find all labels
        all_labels = find_labels_recursive(label)
        assert len(all_labels) >= 2, "Expected at least 2 Labels (paragraph + code)"

        # All labels should have font_hinting set (when not None)
        for lbl in all_labels:
            if font_hinting_value is not None:
                assert lbl.font_hinting == font_hinting_value, \
                    f"Expected font_hinting={font_hinting_value!r}, got {lbl.font_hinting!r}"

    @pytest.mark.property
    @given(st.booleans())
    # Boolean strategy: 2 examples (True/False coverage)
    @settings(max_examples=2, deadline=None)
    def test_font_kerning_forwarded_to_all_labels_including_code(self, font_kerning_value):
        """font_kerning IS forwarded to ALL Labels including code blocks."""
        # Create markdown with both regular text and code block
        markdown = 'Regular paragraph\n\n```python\ncode here\n```'
        label = MarkdownLabel(text=markdown, font_kerning=font_kerning_value)

        # Find all labels
        all_labels = find_labels_recursive(label)
        assert len(all_labels) >= 2, "Expected at least 2 Labels (paragraph + code)"

        # All labels should have font_kerning set
        for lbl in all_labels:
            assert lbl.font_kerning == font_kerning_value, \
                f"Expected font_kerning={font_kerning_value}, got {lbl.font_kerning}"

    @pytest.mark.property
    @given(st_alphanumeric_text(min_size=1, max_size=20),
        st_alphanumeric_text(min_size=1, max_size=20),
        st.sampled_from([None, 'normal', 'light', 'mono']),
        st.booleans())
    # Mixed finite/complex strategy: 20 examples (8 finite × 2.5 complex samples)
    @settings(max_examples=20, deadline=None)
    def test_combined_font_properties_with_code_block(self, font_family, font_context,
                                                       font_hinting, font_kerning):
        """Combined font properties are correctly forwarded with code block exclusion."""
        # Create markdown with both regular text and code block
        markdown = '# Heading\n\nParagraph\n\n```python\ncode\n```'
        label = MarkdownLabel(
            text=markdown,
            font_family=font_family,
            font_context=font_context,
            font_hinting=font_hinting,
            font_kerning=font_kerning
        )

        # Find code and non-code labels
        code_labels = self._find_code_block_labels(label)
        non_code_labels = self._find_non_code_labels(label)

        # Verify non-code labels have all properties
        for lbl in non_code_labels:
            assert lbl.font_family == font_family, \
                f"Non-code label: Expected font_family={font_family!r}, got {lbl.font_family!r}"
            assert lbl.font_context == font_context, \
                f"Non-code label: Expected font_context={font_context!r}, got {lbl.font_context!r}"
            if font_hinting is not None:
                assert lbl.font_hinting == font_hinting, \
                    f"Non-code label: Expected font_hinting={font_hinting!r}, got {lbl.font_hinting!r}"
            assert lbl.font_kerning == font_kerning, \
                f"Non-code label: Expected font_kerning={font_kerning}, got {lbl.font_kerning}"

        # Verify code labels have all properties EXCEPT font_family
        for lbl in code_labels:
            assert lbl.font_family is None, \
                f"Code label: font_family should be None, got {lbl.font_family!r}"
            assert lbl.font_context == font_context, \
                f"Code label: Expected font_context={font_context!r}, got {lbl.font_context!r}"
            if font_hinting is not None:
                assert lbl.font_hinting == font_hinting, \
                    f"Code label: Expected font_hinting={font_hinting!r}, got {lbl.font_hinting!r}"
            assert lbl.font_kerning == font_kerning, \
                f"Code label: Expected font_kerning={font_kerning}, got {lbl.font_kerning}"


# *For any* MarkdownLabel with rendered content, when base_font_size is modified,
# all child Label font_size properties SHALL be updated immediately to reflect
# the new base size multiplied by their respective scale factors.

class TestFontSizeImmediateUpdates:
    """Property tests for font size immediate update."""

    @pytest.mark.property
    @given(
        simple_markdown_document(),
        st_font_size(min_value=8, max_value=50),
        st_font_size(min_value=8, max_value=50)
    )
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_base_font_size_updates_all_labels_immediately(self, markdown_text, initial_size, new_size):
        """Changing base_font_size immediately updates all child Label font_size properties."""
        assume(markdown_text.strip())
        assume(abs(initial_size - new_size) > 1.0)  # Ensure meaningful change

        # Create label with initial font size
        label = MarkdownLabel(text=markdown_text, base_font_size=initial_size)

        # Collect all Label widgets and their expected font sizes
        def collect_labels_and_scales(widget, labels_info=None):
            if labels_info is None:
                labels_info = []

            if isinstance(widget, Label):
                # Get the font scale factor (default to 1.0 if not set)
                scale = getattr(widget, '_font_scale', 1.0)
                labels_info.append((widget, scale))

            if hasattr(widget, 'children'):
                for child in widget.children:
                    collect_labels_and_scales(child, labels_info)

            return labels_info

        labels_before = collect_labels_and_scales(label)
        assume(len(labels_before) > 0)  # Need at least one Label to test

        # Change base_font_size
        label.base_font_size = new_size

        # Collect labels after change
        labels_after = collect_labels_and_scales(label)

        # Verify all Labels have updated font_size
        for label_widget, scale in labels_after:
            expected_font_size = new_size * scale
            actual_font_size = label_widget.font_size

            assert abs(actual_font_size - expected_font_size) < 0.1, \
                f"Label font_size not updated: expected {expected_font_size}, " \
                f"got {actual_font_size} (scale={scale})"

    @pytest.mark.property
    @given(
        st.integers(min_value=1, max_value=6),  # Heading levels
        st_font_size(min_value=10, max_value=30),
        st_font_size(min_value=10, max_value=30)
    )
    # Mixed finite/complex strategy: 20 examples (6 finite × ~3 complex samples)
    @settings(max_examples=20, deadline=None)
    def test_heading_font_size_updates_with_scale(self, heading_level, initial_size, new_size):
        """Heading font sizes update immediately with correct scale factors."""
        assume(abs(initial_size - new_size) > 1.0)

        # Create heading markdown
        heading_text = '#' * heading_level + ' Test Heading'
        label = MarkdownLabel(text=heading_text, base_font_size=initial_size)

        # Find the heading Label
        heading_label = None
        for child in label.children:
            if isinstance(child, Label) and hasattr(child, '_font_scale'):
                heading_label = child
                break

        assume(heading_label is not None)

        # Get expected scale from KivyRenderer.HEADING_SIZES
        from kivy_garden.markdownlabel.kivy_renderer import KivyRenderer
        expected_scale = KivyRenderer.HEADING_SIZES.get(heading_level, 1.0)

        # Verify initial font size
        initial_expected = initial_size * expected_scale
        assert abs(heading_label.font_size - initial_expected) < 0.1, \
            f"Initial heading font_size incorrect: expected {initial_expected}, got {heading_label.font_size}"

        # Change base_font_size
        label.base_font_size = new_size

        # Verify updated font size
        new_expected = new_size * expected_scale
        assert abs(heading_label.font_size - new_expected) < 0.1, \
            f"Updated heading font_size incorrect: expected {new_expected}, got {heading_label.font_size}"

    @pytest.mark.property
    @given(
        st_font_size(min_value=10, max_value=30)
    )
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_paragraph_font_size_updates_immediately(self, new_size):
        """Paragraph font sizes update immediately when base_font_size changes."""
        # Create simple paragraph
        label = MarkdownLabel(text='This is a test paragraph.')

        # Find the paragraph Label
        paragraph_label = None
        for child in label.children:
            if isinstance(child, Label):
                paragraph_label = child
                break

        assume(paragraph_label is not None)

        # Change base_font_size
        label.base_font_size = new_size

        # Verify font_size updated (paragraphs have scale factor 1.0)
        assert abs(paragraph_label.font_size - new_size) < 0.1, \
            f"Paragraph font_size not updated: expected {new_size}, got {paragraph_label.font_size}"


# *For any* MarkdownLabel with headings (h1-h6) and any base_font_size value,
# each heading Label's font_size SHALL equal `base_font_size * HEADING_SIZES[level]`
# where HEADING_SIZES is {1: 2.5, 2: 2.0, 3: 1.75, 4: 1.5, 5: 1.25, 6: 1.0}.

class TestHeadingScalePreservation:
    """Property tests for heading scale preservation."""

    @pytest.mark.property
    @given(
        st.integers(min_value=1, max_value=6),  # Heading levels
        st_font_size(min_value=8, max_value=50)
    )
    # Mixed finite/complex strategy: 20 examples (6 finite × ~3 complex samples)
    @settings(max_examples=20, deadline=None)
    def test_heading_scale_factors_preserved(self, heading_level, base_size):
        """Heading scale factors are preserved according to HEADING_SIZES."""
        # Create heading markdown
        heading_text = '#' * heading_level + ' Test Heading'
        label = MarkdownLabel(text=heading_text, base_font_size=base_size)

        # Find the heading Label
        heading_label = None
        for child in label.children:
            if isinstance(child, Label) and hasattr(child, '_font_scale'):
                heading_label = child
                break

        assume(heading_label is not None)

        # Get expected scale from KivyRenderer.HEADING_SIZES
        from kivy_garden.markdownlabel.kivy_renderer import KivyRenderer
        expected_scale = KivyRenderer.HEADING_SIZES.get(heading_level, 1.0)

        # Verify the scale factor is stored correctly
        actual_scale = getattr(heading_label, '_font_scale', 1.0)
        assert abs(actual_scale - expected_scale) < 0.01, \
            f"Heading scale factor incorrect: expected {expected_scale}, got {actual_scale}"

        # Verify the computed font_size matches base_font_size * scale
        expected_font_size = base_size * expected_scale
        actual_font_size = heading_label.font_size
        assert abs(actual_font_size - expected_font_size) < 0.1, \
            f"Heading font_size incorrect: expected {expected_font_size}, got {actual_font_size}"

    @pytest.mark.property
    @given(
        st.lists(
            st.integers(min_value=1, max_value=6),
            min_size=2,
            max_size=6,
            unique=True
        ),
        st_font_size(min_value=12, max_value=24)
    )
    # Mixed finite/complex strategy: 20 examples (large finite lists × complex)
    @settings(max_examples=20, deadline=None)
    def test_multiple_headings_preserve_relative_scales(self, heading_levels, base_size):
        """Multiple headings preserve correct relative scale factors."""
        # Create markdown with multiple headings
        headings = [f"{'#' * level} Heading {level}" for level in heading_levels]
        markdown_text = '\n\n'.join(headings)

        label = MarkdownLabel(text=markdown_text, base_font_size=base_size)

        # Collect all heading Labels with their levels
        heading_labels = []
        for child in label.children:
            if isinstance(child, Label) and hasattr(child, '_font_scale'):
                # Try to determine heading level from font scale
                scale = getattr(child, '_font_scale', 1.0)
                heading_labels.append((child, scale))

        assume(len(heading_labels) >= 2)  # Need multiple headings to test relative scales

        # Get expected scales from KivyRenderer.HEADING_SIZES
        from kivy_garden.markdownlabel.kivy_renderer import KivyRenderer

        # Verify each heading has correct scale and font size
        for heading_label, actual_scale in heading_labels:
            # Find which heading level this corresponds to
            expected_level = None
            for level, expected_scale in KivyRenderer.HEADING_SIZES.items():
                if abs(actual_scale - expected_scale) < 0.01:
                    expected_level = level
                    break

            assert expected_level is not None, \
                f"Could not match scale {actual_scale} to any heading level"

            # Verify font_size matches base_size * scale
            expected_font_size = base_size * actual_scale
            actual_font_size = heading_label.font_size
            assert abs(actual_font_size - expected_font_size) < 0.1, \
                f"Heading level {expected_level} font_size incorrect: " \
                f"expected {expected_font_size}, got {actual_font_size}"

    @pytest.mark.property
    @given(
        st.integers(min_value=1, max_value=6),
        st_font_size(min_value=10, max_value=20),
        st_font_size(min_value=20, max_value=40)
    )
    # Mixed finite/complex strategy: 20 examples (6 finite × ~3 complex samples)
    @settings(max_examples=20, deadline=None)
    def test_heading_scale_preserved_after_base_font_size_change(self, heading_level, initial_size, new_size):
        """Heading scale factors are preserved when base_font_size changes."""
        # Create heading
        heading_text = '#' * heading_level + ' Test Heading'
        label = MarkdownLabel(text=heading_text, base_font_size=initial_size)

        # Find heading Label
        heading_label = None
        for child in label.children:
            if isinstance(child, Label) and hasattr(child, '_font_scale'):
                heading_label = child
                break

        assume(heading_label is not None)

        # Get expected scale
        from kivy_garden.markdownlabel.kivy_renderer import KivyRenderer
        expected_scale = KivyRenderer.HEADING_SIZES.get(heading_level, 1.0)

        # Verify initial state
        initial_expected_font_size = initial_size * expected_scale
        assert abs(heading_label.font_size - initial_expected_font_size) < 0.1

        # Change base_font_size
        label.base_font_size = new_size

        # Verify scale factor is still preserved
        actual_scale = getattr(heading_label, '_font_scale', 1.0)
        assert abs(actual_scale - expected_scale) < 0.01, \
            f"Scale factor changed after base_font_size update: expected {expected_scale}, got {actual_scale}"

        # Verify new font_size uses preserved scale
        new_expected_font_size = new_size * expected_scale
        assert abs(heading_label.font_size - new_expected_font_size) < 0.1, \
            f"Font size not updated with preserved scale: " \
            f"expected {new_expected_font_size}, got {heading_label.font_size}"


# *For any* MarkdownLabel with rendered content, when base_font_size is modified,
# the child widget object identities SHALL remain unchanged (same Python object ids),
# indicating no rebuild occurred.

class TestNoRebuildOnFontSizeChange:
    """Property tests for no rebuild on font size change."""

    @pytest.mark.property
    @given(
        simple_markdown_document(),
        st_font_size(min_value=10, max_value=20),
        st_font_size(min_value=20, max_value=40)
    )
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_widget_identities_preserved_on_font_size_change(self, markdown_text, initial_size, new_size):
        """Widget object identities are preserved when base_font_size changes."""
        assume(markdown_text.strip())
        assume(abs(initial_size - new_size) > 2.0)  # Ensure meaningful change

        # Create label with content
        label = MarkdownLabel(text=markdown_text, base_font_size=initial_size)

        # Collect widget IDs before change
        ids_before = collect_widget_ids(label)
        assume(len(ids_before) > 1)  # Need at least the label itself + children

        # Change base_font_size
        label.base_font_size = new_size

        # Collect widget IDs after change
        ids_after = collect_widget_ids(label)

        # Widget identities should be exactly the same (no rebuild occurred)
        assert ids_before == ids_after, \
            f"Widget identities changed after font_size update: " \
            f"{len(ids_before)} before, {len(ids_after)} after"

    @pytest.mark.property
    @given(
        st.integers(min_value=1, max_value=6),
        st_font_size(min_value=12, max_value=18),
        st_font_size(min_value=20, max_value=30)
    )
    # Mixed finite/complex strategy: 30 examples (6 finite × 5 complex samples)
    @settings(max_examples=30, deadline=None)
    def test_heading_widget_identity_preserved(self, heading_level, initial_size, new_size):
        """Heading Label widget identity is preserved when base_font_size changes."""
        # Create heading
        heading_text = '#' * heading_level + ' Test Heading'
        label = MarkdownLabel(text=heading_text, base_font_size=initial_size)

        # Find the heading Label
        heading_label = None
        for child in label.children:
            if isinstance(child, Label):
                heading_label = child
                break

        assume(heading_label is not None)

        # Store the widget ID
        heading_id_before = id(heading_label)

        # Change base_font_size
        label.base_font_size = new_size

        # Find the heading Label again
        heading_label_after = None
        for child in label.children:
            if isinstance(child, Label):
                heading_label_after = child
                break

        assert heading_label_after is not None
        heading_id_after = id(heading_label_after)

        # Should be the same object
        assert heading_id_before == heading_id_after, \
            f"Heading Label widget was recreated (IDs: {heading_id_before} -> {heading_id_after})"

    @pytest.mark.property
    @given(
        st_font_size(min_value=10, max_value=15),
        st_font_size(min_value=20, max_value=25),
        st_font_size(min_value=30, max_value=35)
    )
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_multiple_font_size_changes_preserve_identities(self, size1, size2, size3):
        """Multiple font size changes preserve widget identities."""
        # Create content with multiple elements
        markdown_text = '# Heading\n\nParagraph text\n\n## Subheading'
        label = MarkdownLabel(text=markdown_text, base_font_size=size1)

        # Collect initial widget IDs
        initial_ids = collect_widget_ids(label)
        assume(len(initial_ids) > 2)  # Need multiple widgets

        # Make multiple font size changes
        label.base_font_size = size2
        ids_after_first = collect_widget_ids(label)

        label.base_font_size = size3
        ids_after_second = collect_widget_ids(label)

        # All widget identities should be preserved through all changes
        assert initial_ids == ids_after_first == ids_after_second, \
            f"Widget identities changed: initial={len(initial_ids)}, " \
            f"after_first={len(ids_after_first)}, after_second={len(ids_after_second)}"

    @pytest.mark.property
    @given(
        st_font_size(min_value=12, max_value=24)
    )
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_rebuild_counter_not_incremented_on_font_size_change(self, new_size):
        """Rebuild operations are not triggered by font size changes."""
        # Create label with content
        label = MarkdownLabel(text='# Test\n\nParagraph')

        # Track rebuild calls
        rebuild_count = [0]
        original_rebuild = label._rebuild_widgets

        def counting_rebuild():
            rebuild_count[0] += 1
            original_rebuild()

        label._rebuild_widgets = counting_rebuild

        # Change font size
        label.base_font_size = new_size

        # No rebuild should have been triggered
        assert rebuild_count[0] == 0, \
            f"Expected 0 rebuilds for font_size change, got {rebuild_count[0]}"

        # Verify the change was applied (font sizes should be updated)
        found_label = False
        for child in label.children:
            if isinstance(child, Label):
                found_label = True
                # Font size should reflect the change
                assert abs(child.font_size - new_size) < 0.1, \
                    f"Expected font_size={new_size}, got {child.font_size}"
                break

        assert found_label, "Should have found at least one Label widget"
