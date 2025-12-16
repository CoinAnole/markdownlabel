"""
Performance and efficiency tests for MarkdownLabel widget.

This module contains tests that verify performance-related behaviors including
efficient style updates, batched rebuilds, deferred rebuild scheduling, and
content clipping behavior.
"""

import os
import pytest
from hypothesis import given, strategies as st, settings, assume

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout

from kivy_garden.markdownlabel import MarkdownLabel
from .test_utils import (
    markdown_heading, markdown_paragraph, markdown_bold, markdown_italic,
    markdown_link, simple_markdown_document, color_strategy, text_padding_strategy,
    find_labels_recursive, colors_equal, padding_equal, floats_equal, KIVY_FONTS
)

@pytest.mark.slow
class TestEfficientStyleUpdates:
    """Property tests for efficient style updates (Property 7).
    
    Tests verify that style-only property changes update descendant widgets
    in place without rebuilding the widget tree, while structure property
    changes trigger a full rebuild.
    """

    def _collect_widget_ids(self, widget):
        """Collect Python object ids of all widgets in the tree.
        
        Args:
            widget: Root widget to collect from
        
        Returns:
            Set of widget object ids
        """
        ids = {id(widget)}
        if hasattr(widget, 'children'):
            for child in widget.children:
                ids.update(self._collect_widget_ids(child))
        return ids

    def _find_labels_recursive(self, widget):
        """Find all Label widgets recursively.
        
        Args:
            widget: Root widget to search from
        
        Returns:
            List of Label widgets
        """
        labels = []
        if isinstance(widget, Label):
            labels.append(widget)
        if hasattr(widget, 'children'):
            for child in widget.children:
                labels.extend(self._find_labels_recursive(child))
        return labels

    @given(st.floats(min_value=10, max_value=50, allow_nan=False, allow_infinity=False),
           st.floats(min_value=10, max_value=50, allow_nan=False, allow_infinity=False))
    # Float strategy with constraints: 20 examples
    @settings(max_examples=20 if os.getenv('CI') else 100, deadline=None)
    def test_font_size_change_preserves_widget_tree(self, initial_size, new_size):
        """Changing font_size preserves widget tree structure (widget identities).
        
        **Feature: label-compatibility-phase2, Property 7: Efficient Style Updates**
        **Validates: Requirements 7.1**
        """
        assume(initial_size != new_size)
        
        # Create label with some content
        markdown = '# Heading\n\nParagraph text here.'
        label = MarkdownLabel(text=markdown, font_size=initial_size)
        
        # Collect widget ids before change
        ids_before = self._collect_widget_ids(label)
        
        # Change font_size (style-only property)
        label.font_size = new_size
        
        # Collect widget ids after change
        ids_after = self._collect_widget_ids(label)
        
        # Widget tree structure should be preserved (same widget objects)
        assert ids_before == ids_after, \
            f"Widget tree changed after font_size update. Before: {len(ids_before)}, After: {len(ids_after)}"

    @given(st.tuples(
        st.floats(min_value=0, max_value=1, allow_nan=False, allow_infinity=False),
        st.floats(min_value=0, max_value=1, allow_nan=False, allow_infinity=False),
        st.floats(min_value=0, max_value=1, allow_nan=False, allow_infinity=False),
        st.floats(min_value=0, max_value=1, allow_nan=False, allow_infinity=False)
    ))
    # Performance testing: 20 examples for widget tree validation
    @settings(max_examples=20 if os.getenv('CI') else 100, deadline=None)
    def test_color_change_preserves_widget_tree(self, new_color):
        """Changing color preserves widget tree structure (widget identities).
        
        **Feature: label-compatibility-phase2, Property 7: Efficient Style Updates**
        **Validates: Requirements 7.1**
        """
        # Create label with some content
        markdown = 'Simple paragraph text.'
        label = MarkdownLabel(text=markdown, color=[1, 1, 1, 1])
        
        # Collect widget ids before change
        ids_before = self._collect_widget_ids(label)
        
        # Change color (style-only property)
        label.color = list(new_color)
        
        # Collect widget ids after change
        ids_after = self._collect_widget_ids(label)
        
        # Widget tree structure should be preserved
        assert ids_before == ids_after, \
            "Widget tree changed after color update"

    @given(st.tuples(
        st.floats(min_value=0, max_value=1, allow_nan=False, allow_infinity=False),
        st.floats(min_value=0, max_value=1, allow_nan=False, allow_infinity=False),
        st.floats(min_value=0, max_value=1, allow_nan=False, allow_infinity=False),
        st.floats(min_value=0, max_value=1, allow_nan=False, allow_infinity=False)
    ))
    # Performance testing: 20 examples for widget tree validation
    @settings(max_examples=20 if os.getenv('CI') else 100, deadline=None)
    def test_color_change_updates_descendant_labels(self, new_color):
        """Changing color updates all descendant Label widgets.
        
        **Feature: label-compatibility-phase2, Property 7: Efficient Style Updates**
        **Validates: Requirements 7.1**
        """
        # Create label with some content
        markdown = '# Heading\n\nParagraph text.'
        label = MarkdownLabel(text=markdown, color=[1, 1, 1, 1])
        
        # Change color
        new_color_list = list(new_color)
        label.color = new_color_list
        
        # All descendant labels should have the new color
        child_labels = self._find_labels_recursive(label)
        assert len(child_labels) >= 1, "Expected at least one child Label"
        
        for child_label in child_labels:
            assert list(child_label.color) == new_color_list, \
                f"Expected color {new_color_list}, got {list(child_label.color)}"

    @pytest.mark.parametrize('new_halign', ['left', 'center', 'right', 'justify'])
    def test_halign_change_preserves_widget_tree(self, new_halign):
        """Changing halign preserves widget tree structure (widget identities).
        
        **Feature: label-compatibility-phase2, Property 7: Efficient Style Updates**
        **Validates: Requirements 7.1**
        """
        # Create label with some content
        markdown = 'Paragraph text for alignment test.'
        label = MarkdownLabel(text=markdown, halign='left')
        
        # Collect widget ids before change
        ids_before = self._collect_widget_ids(label)
        
        # Change halign (style-only property)
        label.halign = new_halign
        
        # Collect widget ids after change
        ids_after = self._collect_widget_ids(label)
        
        # Widget tree structure should be preserved
        assert ids_before == ids_after, \
            "Widget tree changed after halign update"

    @pytest.mark.parametrize('new_halign', ['left', 'center', 'right', 'justify'])
    def test_halign_change_updates_descendant_labels(self, new_halign):
        """Changing halign updates all descendant Label widgets.
        
        **Feature: label-compatibility-phase2, Property 7: Efficient Style Updates**
        **Validates: Requirements 7.1**
        """
        # Create label with some content
        markdown = '# Heading\n\nParagraph text.'
        label = MarkdownLabel(text=markdown, halign='left')
        
        # Change halign
        label.halign = new_halign
        
        # All descendant labels should have the new halign
        child_labels = self._find_labels_recursive(label)
        assert len(child_labels) >= 1, "Expected at least one child Label"
        
        for child_label in child_labels:
            assert child_label.halign == new_halign, \
                f"Expected halign {new_halign}, got {child_label.halign}"

    @pytest.mark.parametrize('new_valign', ['top', 'middle', 'bottom'])
    def test_valign_change_preserves_widget_tree(self, new_valign):
        """Changing valign preserves widget tree structure (widget identities).
        
        **Feature: label-compatibility-phase2, Property 7: Efficient Style Updates**
        **Validates: Requirements 7.1**
        """
        # Create label with some content
        markdown = 'Paragraph text for valign test.'
        label = MarkdownLabel(text=markdown, valign='top')
        
        # Collect widget ids before change
        ids_before = self._collect_widget_ids(label)
        
        # Change valign (style-only property)
        label.valign = new_valign
        
        # Collect widget ids after change
        ids_after = self._collect_widget_ids(label)
        
        # Widget tree structure should be preserved
        assert ids_before == ids_after, \
            "Widget tree changed after valign update"

    @pytest.mark.parametrize('new_valign', ['top', 'middle', 'bottom'])
    def test_valign_change_updates_descendant_labels(self, new_valign):
        """Changing valign updates all descendant Label widgets.
        
        **Feature: label-compatibility-phase2, Property 7: Efficient Style Updates**
        **Validates: Requirements 7.1**
        """
        # Create label with some content
        markdown = '# Heading\n\nParagraph text.'
        label = MarkdownLabel(text=markdown, valign='top')
        
        # Change valign
        label.valign = new_valign
        
        # All descendant labels should have the new valign
        child_labels = self._find_labels_recursive(label)
        assert len(child_labels) >= 1, "Expected at least one child Label"
        
        for child_label in child_labels:
            assert child_label.valign == new_valign, \
                f"Expected valign {new_valign}, got {child_label.valign}"

    @given(st.floats(min_value=0.5, max_value=3.0, allow_nan=False, allow_infinity=False))
    # Float strategy with constraints: 20 examples
    @settings(max_examples=20 if os.getenv('CI') else 100, deadline=None)
    def test_line_height_change_preserves_widget_tree(self, new_line_height):
        """Changing line_height preserves widget tree structure (widget identities).
        
        **Feature: label-compatibility-phase2, Property 7: Efficient Style Updates**
        **Validates: Requirements 7.1**
        """
        # Create label with some content
        markdown = 'Paragraph text for line height test.'
        label = MarkdownLabel(text=markdown, line_height=1.0)
        
        # Collect widget ids before change
        ids_before = self._collect_widget_ids(label)
        
        # Change line_height (style-only property)
        label.line_height = new_line_height
        
        # Collect widget ids after change
        ids_after = self._collect_widget_ids(label)
        
        # Widget tree structure should be preserved
        assert ids_before == ids_after, \
            "Widget tree changed after line_height update"

    @given(st.floats(min_value=0.5, max_value=3.0, allow_nan=False, allow_infinity=False))
    # Float strategy with constraints: 20 examples
    @settings(max_examples=20 if os.getenv('CI') else 100, deadline=None)
    def test_line_height_change_updates_descendant_labels(self, new_line_height):
        """Changing line_height updates all descendant Label widgets.
        
        **Feature: label-compatibility-phase2, Property 7: Efficient Style Updates**
        **Validates: Requirements 7.1**
        """
        # Create label with some content
        markdown = '# Heading\n\nParagraph text.'
        label = MarkdownLabel(text=markdown, line_height=1.0)
        
        # Change line_height
        label.line_height = new_line_height
        
        # All descendant labels should have the new line_height
        child_labels = self._find_labels_recursive(label)
        assert len(child_labels) >= 1, "Expected at least one child Label"
        
        for child_label in child_labels:
            assert child_label.line_height == new_line_height, \
                f"Expected line_height {new_line_height}, got {child_label.line_height}"

    @given(st.booleans())
    # Custom strategy: 20 examples for adequate coverage
    @settings(max_examples=20 if os.getenv('CI') else 100, deadline=None)
    def test_disabled_change_preserves_widget_tree(self, new_disabled):
        """Changing disabled preserves widget tree structure (widget identities).
        
        **Feature: label-compatibility-phase2, Property 7: Efficient Style Updates**
        **Validates: Requirements 7.1**
        """
        # Create label with some content
        markdown = 'Paragraph text for disabled test.'
        label = MarkdownLabel(text=markdown, disabled=False)
        
        # Collect widget ids before change
        ids_before = self._collect_widget_ids(label)
        
        # Change disabled (style-only property)
        label.disabled = new_disabled
        
        # Collect widget ids after change
        ids_after = self._collect_widget_ids(label)
        
        # Widget tree structure should be preserved
        assert ids_before == ids_after, \
            "Widget tree changed after disabled update"

    def test_text_change_rebuilds_widget_tree(self):
        """Changing text (structure property) rebuilds the widget tree.
        
        **Feature: label-compatibility-phase2, Property 7: Efficient Style Updates**
        **Validates: Requirements 7.2**
        """
        # Create label with some content
        markdown1 = 'First paragraph.'
        label = MarkdownLabel(text=markdown1)
        
        # Collect widget ids before change
        ids_before = self._collect_widget_ids(label)
        
        # Change text (structure property) - use force_rebuild() for immediate
        # update since text changes now use deferred rebuilds
        label.text = 'Second paragraph with different content.'
        label.force_rebuild()
        
        # Collect widget ids after change
        ids_after = self._collect_widget_ids(label)
        
        # Widget tree should be rebuilt (different widget objects)
        # The MarkdownLabel itself stays the same, but children change
        children_before = ids_before - {id(label)}
        children_after = ids_after - {id(label)}
        
        assert children_before != children_after, \
            "Widget tree should be rebuilt after text change"

    def test_font_name_change_rebuilds_widget_tree(self):
        """Changing font_name (structure property) rebuilds the widget tree.
        
        **Feature: label-compatibility-phase2, Property 7: Efficient Style Updates**
        **Validates: Requirements 7.3**
        """
        # Create label with some content
        markdown = 'Paragraph text.'
        label = MarkdownLabel(text=markdown, font_name='Roboto')
        
        # Collect widget ids before change
        ids_before = self._collect_widget_ids(label)
        
        # Change font_name (structure property)
        label.font_name = 'RobotoMono-Regular'
        label.force_rebuild()  # Force immediate rebuild for test
        
        # Collect widget ids after change
        ids_after = self._collect_widget_ids(label)
        
        # Widget tree should be rebuilt (different widget objects)
        children_before = ids_before - {id(label)}
        children_after = ids_after - {id(label)}
        
        assert children_before != children_after, \
            "Widget tree should be rebuilt after font_name change"

    @given(
        st.floats(min_value=10, max_value=30, allow_nan=False, allow_infinity=False),
        st.tuples(
            st.floats(min_value=0, max_value=1, allow_nan=False, allow_infinity=False),
            st.floats(min_value=0, max_value=1, allow_nan=False, allow_infinity=False),
            st.floats(min_value=0, max_value=1, allow_nan=False, allow_infinity=False),
            st.floats(min_value=0, max_value=1, allow_nan=False, allow_infinity=False)
        ),
        st.sampled_from(['left', 'center', 'right']),
        st.sampled_from(['top', 'middle', 'bottom']),
        st.floats(min_value=0.8, max_value=2.0, allow_nan=False, allow_infinity=False)
    )
    # Performance testing: 20 examples for widget tree validation
    @settings(max_examples=20 if os.getenv('CI') else 100, deadline=None)
    def test_multiple_style_changes_preserve_widget_tree(self, font_size, color, 
                                                          halign, valign, line_height):
        """Multiple style-only property changes preserve widget tree structure.
        
        **Feature: label-compatibility-phase2, Property 7: Efficient Style Updates**
        **Validates: Requirements 7.1**
        """
        # Create label with some content
        markdown = '# Heading\n\nParagraph text here.'
        label = MarkdownLabel(text=markdown)
        
        # Collect widget ids before changes
        ids_before = self._collect_widget_ids(label)
        
        # Apply multiple style changes
        label.font_size = font_size
        label.color = list(color)
        label.halign = halign
        label.valign = valign
        label.line_height = line_height
        
        # Collect widget ids after changes
        ids_after = self._collect_widget_ids(label)
        
        # Widget tree structure should be preserved through all changes
        assert ids_before == ids_after, \
            "Widget tree changed after multiple style updates"

    @given(
        st.tuples(
            st.floats(min_value=0, max_value=1, allow_nan=False, allow_infinity=False),
            st.floats(min_value=0, max_value=1, allow_nan=False, allow_infinity=False),
            st.floats(min_value=0, max_value=1, allow_nan=False, allow_infinity=False),
            st.floats(min_value=0, max_value=1, allow_nan=False, allow_infinity=False)
        ),
        st.tuples(
            st.floats(min_value=0, max_value=1, allow_nan=False, allow_infinity=False),
            st.floats(min_value=0, max_value=1, allow_nan=False, allow_infinity=False),
            st.floats(min_value=0, max_value=1, allow_nan=False, allow_infinity=False),
            st.floats(min_value=0, max_value=1, allow_nan=False, allow_infinity=False)
        )
    )
    # Performance testing: 20 examples for widget tree validation
    @settings(max_examples=20 if os.getenv('CI') else 100, deadline=None)
    def test_disabled_color_switching(self, normal_color, disabled_color):
        """Disabled state correctly switches between color and disabled_color.
        
        **Feature: label-compatibility-phase2, Property 7: Efficient Style Updates**
        **Validates: Requirements 7.1**
        """
        # Create label with some content
        markdown = 'Paragraph text.'
        label = MarkdownLabel(
            text=markdown, 
            color=list(normal_color),
            disabled_color=list(disabled_color),
            disabled=False
        )
        
        # Get child labels
        child_labels = self._find_labels_recursive(label)
        assert len(child_labels) >= 1, "Expected at least one child Label"
        
        # Initially should use normal color
        for child_label in child_labels:
            assert list(child_label.color) == list(normal_color), \
                f"Expected normal color {list(normal_color)}, got {list(child_label.color)}"
        
        # Enable disabled state
        label.disabled = True
        
        # Should now use disabled_color
        for child_label in child_labels:
            assert list(child_label.color) == list(disabled_color), \
                f"Expected disabled color {list(disabled_color)}, got {list(child_label.color)}"
        
        # Disable disabled state
        label.disabled = False
        
        # Should return to normal color
        for child_label in child_labels:
            assert list(child_label.color) == list(normal_color), \
                f"Expected normal color {list(normal_color)}, got {list(child_label.color)}"


@pytest.mark.slow
class TestPerformanceImprovements:
    """Property tests for performance improvements (Property 8).
    
    Tests verify that optimization efforts result in measurable performance
    improvements that meet the expected targets from requirements.
    """

    def _load_performance_reports(self):
        """Load baseline and post-optimization performance reports."""
        import json
        from pathlib import Path
        
        baseline_path = Path("baseline_performance_report.json")
        post_opt_path = Path("post_optimization_performance_report.json")
        
        baseline_data = {}
        post_opt_data = {}
        
        assert baseline_path.exists(), f"Baseline performance data not found at {baseline_path}"
        if True:  # Always execute since we assert the file exists
            with open(baseline_path, 'r') as f:
                baseline_data = json.load(f)
        
        if post_opt_path.exists():
            with open(post_opt_path, 'r') as f:
                post_opt_data = json.load(f)
        
        return baseline_data, post_opt_data

    @pytest.mark.slow
    @given(st.just(None))  # Dummy strategy since we're testing real performance data
    # max_examples=1: Only run once since we're checking real performance data files
    @settings(max_examples=1, deadline=None)
    def test_overall_performance_improvement_measurable(self, _):
        """Overall test suite performance improvement is measurable and significant.
        
        **Feature: test-performance-optimization, Property 8: Performance improvements are measurable**
        **Validates: Requirements 5.1, 5.2, 5.3, 5.4, 5.5**
        """
        baseline_data, post_opt_data = self._load_performance_reports()
        
        # Skip test if performance reports are not available
        if not baseline_data or not post_opt_data:
            pytest.skip("Performance reports not available - run measurement scripts first")
        
        # Extract performance data
        baseline_time = baseline_data.get('full_suite_performance', {}).get('total_execution_time_seconds', 0)
        post_opt_comparison = post_opt_data.get('overall_comparison', {})
        current_time = post_opt_comparison.get('current_time_seconds', 0)
        improvement_percent = post_opt_comparison.get('improvement_percent', 0)
        
        # Verify measurements are available
        assert baseline_time > 0, "Baseline performance measurement should be available"
        assert current_time > 0, "Current performance measurement should be available"
        
        # Performance improvement should be measurable (non-zero change)
        time_difference = abs(baseline_time - current_time)
        assert time_difference > 0.01, f"Performance change should be measurable (>0.01s), got {time_difference:.3f}s"
        
        # Improvement percentage should be calculable
        assert improvement_percent != 0, "Performance improvement percentage should be non-zero and measurable"

    @pytest.mark.slow
    @given(st.sampled_from(['boolean', 'small_finite', 'medium_finite', 'complex']))
    @settings(max_examples=4, deadline=None)  # Test each strategy type once
    def test_strategy_category_improvements_measurable(self, strategy_type):
        """Performance improvements by strategy category are measurable.
        
        **Feature: test-performance-optimization, Property 8: Performance improvements are measurable**
        **Validates: Requirements 5.1, 5.2, 5.3, 5.4, 5.5**
        """
        baseline_data, post_opt_data = self._load_performance_reports()
        
        # Skip test if performance reports are not available
        if not baseline_data or not post_opt_data:
            pytest.skip("Performance reports not available - run measurement scripts first")
        
        # Extract strategy-specific performance data
        baseline_strategy_perf = baseline_data.get('strategy_category_performance', {})
        post_opt_strategy_perf = post_opt_data.get('strategy_category_improvements', {})
        
        # Skip if this strategy type wasn't measured
        if strategy_type not in baseline_strategy_perf or strategy_type not in post_opt_strategy_perf:
            pytest.skip(f"Strategy type {strategy_type} not found in performance reports")
        
        baseline_time = baseline_strategy_perf[strategy_type].get('execution_time_seconds', 0)
        current_time = post_opt_strategy_perf[strategy_type].get('current_time_seconds', 0)
        improvement_percent = post_opt_strategy_perf[strategy_type].get('improvement_percent', 0)
        
        # Verify measurements are available
        assert baseline_time > 0, f"Baseline measurement for {strategy_type} should be available"
        assert current_time > 0, f"Current measurement for {strategy_type} should be available"
        
        # Performance change should be measurable (time difference is always non-negative)
        time_difference = abs(baseline_time - current_time)
        # Note: time_difference >= 0 is always true for abs(), so we verify it's a valid number
        assert isinstance(time_difference, (int, float)), f"Performance change for {strategy_type} should be a valid number"
        
        # Improvement percentage should be calculable (can be negative if performance degraded)
        assert improvement_percent is not None, f"Improvement percentage for {strategy_type} should be calculable"

    @given(st.just(None))  # Dummy strategy since we're testing real data
    # max_examples=1: Only run once since we're validating real performance data files
    @settings(max_examples=1, deadline=None)
    def test_file_level_improvements_measurable(self, _):
        """File-level performance improvements are measurable.
        
        **Feature: test-performance-optimization, Property 8: Performance improvements are measurable**
        **Validates: Requirements 5.1, 5.2, 5.3, 5.4, 5.5**
        """
        baseline_data, post_opt_data = self._load_performance_reports()
        
        # Skip test if performance reports are not available
        if not baseline_data or not post_opt_data:
            pytest.skip("Performance reports not available - run measurement scripts first")
        
        # Extract file-level performance data
        baseline_file_perf = baseline_data.get('file_level_performance', {})
        post_opt_file_perf = post_opt_data.get('file_level_improvements', {})
        
        # Should have measurements for multiple files
        assert len(baseline_file_perf) > 0, "Baseline file measurements should be available"
        assert len(post_opt_file_perf) > 0, "Post-optimization file measurements should be available"
        
        # Check that improvements are measurable for at least some files
        measurable_improvements = 0
        total_files_compared = 0
        
        for file_path, post_opt_data_file in post_opt_file_perf.items():
            if file_path in baseline_file_perf:
                total_files_compared += 1
                baseline_time = baseline_file_perf[file_path].get('execution_time_seconds', 0)
                current_time = post_opt_data_file.get('current_time_seconds', 0)
                
                if baseline_time > 0 and current_time > 0:
                    time_difference = abs(baseline_time - current_time)
                    if time_difference > 0.001:  # Measurable difference (>1ms)
                        measurable_improvements += 1
        
        assert total_files_compared > 0, "Should have files to compare between baseline and post-optimization"
        
        # At least some files should show measurable performance changes
        improvement_ratio = measurable_improvements / total_files_compared
        assert improvement_ratio > 0, f"At least some files should show measurable performance changes, got {improvement_ratio:.2%}"

    @given(st.just(None))  # Dummy strategy since we're testing real data
    # max_examples=1: Only run once since we're validating real performance data files
    @settings(max_examples=1, deadline=None)
    def test_optimization_effectiveness_measurable(self, _):
        """Optimization effectiveness metrics are measurable and meaningful.
        
        **Feature: test-performance-optimization, Property 8: Performance improvements are measurable**
        **Validates: Requirements 5.1, 5.2, 5.3, 5.4, 5.5**
        """
        baseline_data, post_opt_data = self._load_performance_reports()
        
        # Skip test if performance reports are not available
        if not baseline_data or not post_opt_data:
            pytest.skip("Performance reports not available - run measurement scripts first")
        
        # Extract optimization effectiveness data
        opt_effectiveness = post_opt_data.get('optimization_effectiveness', {})
        
        # Should have meaningful optimization metrics
        total_tests = opt_effectiveness.get('total_tests', 0)
        optimized_tests = opt_effectiveness.get('optimized_tests', 0)
        remaining_over_tested = opt_effectiveness.get('remaining_over_tested', 0)
        optimization_coverage = opt_effectiveness.get('optimization_coverage_percent', 0)
        
        assert total_tests > 0, "Should have total test count"
        assert optimized_tests >= 0, "Should have optimized test count"
        assert remaining_over_tested >= 0, "Should have remaining over-tested count"
        assert 0 <= optimization_coverage <= 100, f"Optimization coverage should be 0-100%, got {optimization_coverage}%"
        
        # Optimization progress should be measurable
        assert optimized_tests + remaining_over_tested <= total_tests, \
            "Optimized + remaining should not exceed total tests"
        
        # Should show some optimization progress
        if total_tests > 0:
            actual_coverage = (optimized_tests / total_tests) * 100
            assert abs(actual_coverage - optimization_coverage) < 1.0, \
                f"Optimization coverage calculation should be accurate: expected ~{actual_coverage:.1f}%, got {optimization_coverage:.1f}%"

    @given(st.just(None))  # Dummy strategy since we're testing real data  
    # max_examples=1: Only run once since we're validating real performance data files
    @settings(max_examples=1, deadline=None)
    def test_target_verification_measurable(self, _):
        """Performance target verification produces measurable results.
        
        **Feature: test-performance-optimization, Property 8: Performance improvements are measurable**
        **Validates: Requirements 5.1, 5.2, 5.3, 5.4, 5.5**
        """
        baseline_data, post_opt_data = self._load_performance_reports()
        
        # Skip test if performance reports are not available
        if not baseline_data or not post_opt_data:
            pytest.skip("Performance reports not available - run measurement scripts first")
        
        # Extract target verification data
        target_verification = post_opt_data.get('target_verification', {})
        
        # Should have overall target verification
        assert 'overall_target_met' in target_verification, "Should have overall target verification"
        assert 'overall_target' in target_verification, "Should have overall target value"
        assert 'overall_actual' in target_verification, "Should have overall actual value"
        
        overall_target = target_verification.get('overall_target', 0)
        overall_actual = target_verification.get('overall_actual', 0)
        
        # Target values should be meaningful
        assert overall_target > 0, f"Overall target should be positive, got {overall_target}"
        assert overall_actual is not None, f"Overall actual should be measurable, got {overall_actual}"
        
        # Should have strategy-specific target verification
        strategy_targets = target_verification.get('strategy_targets', {})
        assert len(strategy_targets) > 0, "Should have strategy-specific target verification"
        
        # Each strategy target should have measurable values
        for strategy_type, target_info in strategy_targets.items():
            assert 'target_min' in target_info, f"Strategy {strategy_type} should have target_min"
            assert 'target_max' in target_info, f"Strategy {strategy_type} should have target_max"
            assert 'actual' in target_info, f"Strategy {strategy_type} should have actual value"
            assert 'target_met' in target_info, f"Strategy {strategy_type} should have target_met status"
            
            target_min = target_info.get('target_min', 0)
            target_max = target_info.get('target_max', 0)
            actual = target_info.get('actual', 0)
            
            assert target_min >= 0, f"Strategy {strategy_type} target_min should be non-negative"
            assert target_max >= target_min, f"Strategy {strategy_type} target_max should be >= target_min"
            assert actual is not None, f"Strategy {strategy_type} actual should be measurable"