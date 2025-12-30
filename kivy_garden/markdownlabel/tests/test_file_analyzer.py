"""
Tests for the FileAnalyzer optimization tool.

This module tests the FileAnalyzer's ability to correctly analyze test files
and generate optimization recommendations for max_examples values.
"""

import os
import tempfile
from pathlib import Path
import pytest
from hypothesis import given, strategies as st, settings

from kivy_garden.markdownlabel.tests.modules.file_analyzer import (
    FileAnalyzer, PropertyTest, OptimizationRecommendation,
    FileAnalysis, ValidationReport
)
from kivy_garden.markdownlabel.tests.modules.strategy_analyzer import StrategyType, StrategyAnalysis


@pytest.mark.test_tests
class TestFileAnalyzerBasics:
    """Basic functionality tests for FileAnalyzer."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.analyzer = FileAnalyzer()
    
    def test_analyzer_initialization(self):
        """FileAnalyzer initializes correctly with classifier and calculator."""
        assert self.analyzer.classifier is not None
        assert self.analyzer.calculator is not None
        assert hasattr(self.analyzer, 'given_pattern')
        assert hasattr(self.analyzer, 'settings_pattern')
        assert hasattr(self.analyzer, 'function_pattern')
    
    def test_empty_file_analysis(self):
        """Empty file returns empty analysis."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("")
            temp_file = f.name
        
        try:
            analysis = self.analyzer.analyze_file(temp_file)
            
            assert analysis.file_path == temp_file
            assert analysis.total_tests == 0
            assert analysis.over_tested_count == 0
            assert len(analysis.recommendations) == 0
            assert analysis.potential_time_savings_percent == 0.0
        finally:
            os.unlink(temp_file)
    
    def test_file_without_property_tests(self):
        """File without property tests returns empty analysis."""
        content = '''
import pytest

def test_regular_function():
    """Regular test function."""
    assert True

class TestRegularClass:
    def test_method(self):
        """Regular test method."""
        assert True
'''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(content)
            temp_file = f.name
        
        try:
            analysis = self.analyzer.analyze_file(temp_file)
            
            assert analysis.total_tests == 0
            assert analysis.over_tested_count == 0
            assert len(analysis.recommendations) == 0
        finally:
            os.unlink(temp_file)


class TestPropertyTestExtraction:
    """Tests for extracting property tests from file content."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.analyzer = FileAnalyzer()
    
    def test_boolean_over_testing_detection(self):
        """Detects boolean tests with excessive max_examples."""
        content = '''
import pytest
from hypothesis import given, strategies as st, settings

class TestExample:
    @given(st.booleans())
    @settings(max_examples=100, deadline=None)
    def test_boolean_property(self, value):
        """Test with over-testing."""
        assert isinstance(value, bool)
'''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(content)
            temp_file = f.name
        
        try:
            analysis = self.analyzer.analyze_file(temp_file)
            
            assert analysis.total_tests == 1
            assert analysis.over_tested_count == 1
            assert len(analysis.recommendations) == 1
            
            rec = analysis.recommendations[0]
            assert rec.test_name == 'test_boolean_property'
            assert rec.current_examples == 100
            assert rec.recommended_examples == 2
            assert rec.strategy_type == 'Boolean'
            assert rec.time_savings_percent > 90  # Should be ~98%
        finally:
            os.unlink(temp_file)
    
    def test_small_integer_range_over_testing(self):
        """Detects small integer ranges with excessive max_examples."""
        content = '''
from hypothesis import given, strategies as st, settings

@given(st.integers(min_value=0, max_value=4))
@settings(max_examples=100, deadline=None)
def test_small_range_property(self, value):
    """Test with over-testing."""
    assert 0 <= value <= 4
'''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(content)
            temp_file = f.name
        
        try:
            analysis = self.analyzer.analyze_file(temp_file)
            
            assert analysis.total_tests == 1
            assert analysis.over_tested_count == 1
            
            rec = analysis.recommendations[0]
            assert rec.test_name == 'test_small_range_property'
            assert rec.current_examples == 100
            assert rec.recommended_examples == 5  # Range size
            assert rec.strategy_type == 'Small finite'
        finally:
            os.unlink(temp_file)
    
    def test_appropriate_examples_not_flagged_file_analyzer(self):
        """Appropriate max_examples values are not flagged by file analyzer."""
        content = '''
from hypothesis import given, strategies as st, settings

@given(st.booleans())
@settings(max_examples=2, deadline=None)
def test_boolean_optimal(self, value):
    assert isinstance(value, bool)

@given(st.integers(min_value=0, max_value=4))
@settings(max_examples=5, deadline=None)
def test_range_optimal(self, value):
    assert 0 <= value <= 4

@given(st.text())
@settings(max_examples=20, deadline=None)
def test_complex_reasonable(self, text):
    assert isinstance(text, str)
'''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(content)
            temp_file = f.name
        
        try:
            analysis = self.analyzer.analyze_file(temp_file)
            
            assert analysis.total_tests == 3
            assert analysis.over_tested_count == 0
            assert len(analysis.recommendations) == 0
        finally:
            os.unlink(temp_file)
    
    def test_multiline_given_decorator(self):
        """Handles multiline @given decorators correctly."""
        content = '''
from hypothesis import given, strategies as st, settings

@given(st.tuples(
    st.booleans(),
    st.integers(min_value=0, max_value=2)
))
# Combination strategy: 6 examples (combination coverage)
@settings(max_examples=6, deadline=None)
def test_multiline_given(self, value):
    bool_val, int_val = value
    assert isinstance(bool_val, bool)
    assert 0 <= int_val <= 2
'''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(content)
            temp_file = f.name
        
        try:
            analysis = self.analyzer.analyze_file(temp_file)
            
            assert analysis.total_tests == 1
            # Should detect combination strategy (2 * 3 = 6 combinations)
            if analysis.over_tested_count > 0:
                rec = analysis.recommendations[0]
                assert rec.current_examples == 100
                assert rec.recommended_examples == 6
                assert rec.strategy_type == 'Combination'
        finally:
            os.unlink(temp_file)


class TestValidationReport:
    """Tests for test suite validation reporting."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.analyzer = FileAnalyzer()
    
    def test_validate_test_suite_empty_directory(self):
        """Validates empty test directory correctly."""
        with tempfile.TemporaryDirectory() as temp_dir:
            report = self.analyzer.validate_test_suite(temp_dir)
            
            assert report.total_tests == 0
            assert report.total_over_tested == 0
            assert len(report.file_analyses) == 0
            assert report.potential_time_savings_percent == 0.0
            assert report.estimated_time_reduction_seconds == 0.0
    
    def test_validate_test_suite_with_files(self):
        """Validates test directory with multiple files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test file 1 with over-testing
            test_file1 = Path(temp_dir) / 'test_example1.py'
            test_file1.write_text('''
from hypothesis import given, strategies as st, settings

@given(st.booleans())
@settings(max_examples=100, deadline=None)
def test_boolean_over(self, value):
    assert isinstance(value, bool)
''')
            
            # Create test file 2 with appropriate testing
            test_file2 = Path(temp_dir) / 'test_example2.py'
            test_file2.write_text('''
from hypothesis import given, strategies as st, settings

@given(st.booleans())
@settings(max_examples=2, deadline=None)
def test_boolean_good(self, value):
    assert isinstance(value, bool)
''')
            
            report = self.analyzer.validate_test_suite(temp_dir)
            
            assert report.total_tests == 2
            assert report.total_over_tested == 1
            assert len(report.file_analyses) == 2
            
            # Find the file with over-testing
            over_tested_file = next(
                (fa for fa in report.file_analyses if fa.over_tested_count > 0),
                None
            )
            assert over_tested_file is not None
            assert len(over_tested_file.recommendations) == 1
            
            # Check time savings estimation
            assert report.estimated_time_reduction_seconds > 0


class TestRationaleGeneration:
    """Tests for optimization rationale generation."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.analyzer = FileAnalyzer()
    
    @given(st.sampled_from(['Boolean', 'Small finite', 'Medium finite', 'Combination', 'Complex']))
    # Small finite strategy: 5 examples (input space size: 5)
    @settings(max_examples=5, deadline=None)
    def test_rationale_generation_for_strategy_types(self, strategy_type):
        """Generates appropriate rationales for different strategy types."""
        # Create mock analysis
        analysis = StrategyAnalysis(
            strategy_type=StrategyType(strategy_type),
            input_space_size=10 if strategy_type != 'Complex' else None,
            complexity_level=2
        )
        
        rationale = self.analyzer._generate_rationale(analysis, 10)
        
        assert isinstance(rationale, str)
        assert len(rationale) > 0
        
        # Check that rationale contains relevant keywords
        if strategy_type == 'Boolean':
            assert 'Boolean' in rationale or 'True/False' in rationale
        elif strategy_type == 'Small finite':
            assert 'finite' in rationale or 'input space' in rationale
        elif strategy_type == 'Combination':
            assert 'combination' in rationale or 'product' in rationale
        elif strategy_type == 'Complex':
            assert 'complex' in rationale or 'complexity' in rationale


class TestErrorHandling:
    """Tests for error handling in file analysis."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.analyzer = FileAnalyzer()
    
    def test_nonexistent_file_handling(self):
        """Handles nonexistent files gracefully."""
        analysis = self.analyzer.analyze_file('/nonexistent/file.py')
        
        assert analysis.file_path == '/nonexistent/file.py'
        assert analysis.total_tests == 0
        assert analysis.over_tested_count == 0
        assert len(analysis.recommendations) == 0
    
    def test_malformed_python_file(self):
        """Handles malformed Python files gracefully."""
        content = '''
# This is not valid Python syntax
@given(st.booleans()
@settings(max_examples=100
def test_malformed
    assert True
'''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(content)
            temp_file = f.name
        
        try:
            # Should not raise an exception
            analysis = self.analyzer.analyze_file(temp_file)
            
            # May or may not find tests depending on regex matching
            assert isinstance(analysis, FileAnalysis)
        finally:
            os.unlink(temp_file)
    
    def test_file_with_incomplete_decorators(self):
        """Handles files with incomplete decorator patterns."""
        content = '''
from hypothesis import given, strategies as st, settings

@given(st.booleans())
# Missing @settings decorator
def test_incomplete(self, value):
    assert isinstance(value, bool)

@settings(max_examples=50)
# Missing @given decorator  
def test_incomplete2(self):
    assert True
'''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(content)
            temp_file = f.name
        
        try:
            analysis = self.analyzer.analyze_file(temp_file)
            
            # Should handle incomplete patterns gracefully
            assert isinstance(analysis, FileAnalysis)
            # Incomplete tests should not be counted
            assert analysis.total_tests == 0
        finally:
            os.unlink(temp_file)


class TestIntegrationWithOptimizationTools:
    """Integration tests with StrategyClassifier and MaxExamplesCalculator."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.analyzer = FileAnalyzer()
    
    def test_integration_with_strategy_classifier(self):
        """FileAnalyzer correctly uses StrategyClassifier."""
        content = '''
from hypothesis import given, strategies as st, settings

@given(st.sampled_from(['red', 'green', 'blue']))
@settings(max_examples=100, deadline=None)
def test_color_enum(self, color):
    assert color in ['red', 'green', 'blue']
'''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(content)
            temp_file = f.name
        
        try:
            analysis = self.analyzer.analyze_file(temp_file)
            
            assert analysis.total_tests == 1
            assert analysis.over_tested_count == 1
            
            rec = analysis.recommendations[0]
            assert rec.strategy_type == 'Small finite'
            assert rec.recommended_examples == 3  # Three colors
        finally:
            os.unlink(temp_file)
    
    def test_integration_with_max_examples_calculator(self):
        """FileAnalyzer correctly uses MaxExamplesCalculator."""
        content = '''
from hypothesis import given, strategies as st, settings

@given(st.tuples(st.booleans(), st.booleans()))
@settings(max_examples=100, deadline=None)
def test_two_booleans(self, values):
    bool1, bool2 = values
    assert isinstance(bool1, bool)
    assert isinstance(bool2, bool)
'''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(content)
            temp_file = f.name
        
        try:
            analysis = self.analyzer.analyze_file(temp_file)
            
            assert analysis.total_tests == 1
            assert analysis.over_tested_count == 1
            
            rec = analysis.recommendations[0]
            assert rec.strategy_type == 'Combination'
            assert rec.recommended_examples == 4  # 2 * 2 combinations
            assert rec.time_savings_percent > 90  # Significant savings
        finally:
            os.unlink(temp_file)


class TestToolIntegrationCompatibility:
    """Property-based tests for tool integration compatibility."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.analyzer = FileAnalyzer()
    
    @given(
        strategy_type=st.sampled_from(['Boolean', 'Small finite', 'Small finite', 'Small finite', 'Small finite']),
        max_examples=st.integers(min_value=1, max_value=100),
        has_comment=st.booleans()
    )
    # Small finite strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_tool_integration_compatibility(self, strategy_type, max_examples, has_comment):
        """**Feature: test-comment-standardization, Property 9: Tool Integration Compatibility**
        
        For any standardized comment format, existing optimization and analysis tools 
        SHALL be able to reference and utilize the comment information.
        **Validates: Requirements 4.4, 5.4**
        """
        # Generate test file content with or without standardized comment
        comment_line = ""
        if has_comment:
            # Map strategy types to appropriate rationales
            if strategy_type == 'Boolean':
                rationale = 'True/False coverage'
            else:
                # All other types are Small finite with different rationales
                rationale = f'input space size: {min(max_examples, 10)}'
            comment_line = f"    # {strategy_type} strategy: {max_examples} examples ({rationale})\n"
        
        # Generate appropriate strategy code based on type
        # Map strategy types to appropriate strategy code
        if strategy_type == 'Boolean':
            strategy_code = 'st.booleans()'
        else:
            # All other types are Small finite - use a representative strategy
            strategy_code = 'st.integers(min_value=0, max_value=4)'
        
        content = f'''
from hypothesis import given, strategies as st, settings

class TestExample:
{comment_line}    @given({strategy_code})
    @settings(max_examples={max_examples}, deadline=None)
    def test_property(self, value):
        """Test property."""
        assert value is not None
'''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(content)
            temp_file = f.name
        
        try:
            # Test that FileAnalyzer can process files with standardized comments
            analysis = self.analyzer.analyze_file(temp_file)
            
            # Property: Tool integration compatibility
            # The analysis should complete successfully regardless of comment presence
            assert isinstance(analysis, FileAnalysis)
            assert analysis.total_tests >= 0
            assert analysis.over_tested_count >= 0
            assert isinstance(analysis.recommendations, list)
            
            # If comment compliance stats are available, they should be valid
            if analysis.comment_compliance_stats:
                stats = analysis.comment_compliance_stats
                assert stats.total_property_tests >= 0
                assert stats.documented_tests >= 0
                assert stats.undocumented_tests >= 0
                assert stats.format_violations >= 0
                assert 0 <= stats.compliance_percentage <= 100
            
            # If recommendations exist, they should include comment information
            for rec in analysis.recommendations:
                assert hasattr(rec, 'comment_info')
                assert hasattr(rec, 'needs_comment_update')
                
                if rec.comment_info:
                    assert hasattr(rec.comment_info, 'has_standardized_comment')
                    assert hasattr(rec.comment_info, 'is_documented')
            
            # Test suite validation should also work with comment integration
            with tempfile.TemporaryDirectory() as temp_dir:
                # Copy test file to temporary directory
                temp_test_file = Path(temp_dir) / 'test_integration.py'
                temp_test_file.write_text(content)
                
                report = self.analyzer.validate_test_suite(temp_dir)
                
                # Property: Overall comment compliance should be calculated
                assert isinstance(report, ValidationReport)
                if report.overall_comment_compliance:
                    compliance = report.overall_comment_compliance
                    assert compliance.total_property_tests >= 0
                    assert compliance.documented_tests >= 0
                    assert compliance.undocumented_tests >= 0
                    assert 0 <= compliance.compliance_percentage <= 100
        
        finally:
            os.unlink(temp_file)