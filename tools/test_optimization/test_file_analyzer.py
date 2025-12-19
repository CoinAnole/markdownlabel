"""Test file analyzer for Hypothesis test optimization.

This module analyzes test files to identify property-based tests and their
current max_examples usage, generating optimization recommendations.
"""

import re
import ast
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional, Dict, Tuple

from .strategy_classifier import StrategyClassifier
from .max_examples_calculator import MaxExamplesCalculator
from .comment_analyzer import CommentAnalyzer
from .comment_format import CommentFormatValidator, ValidationResult


@dataclass
class PropertyTest:
    """Information about a property-based test."""
    name: str
    file_path: str
    line_number: int
    strategy_code: str
    current_max_examples: int
    decorator_line: str
    comment_info: Optional['CommentInfo'] = None


@dataclass
class CommentInfo:
    """Information about standardized comments for a test."""
    has_standardized_comment: bool
    comment_text: Optional[str] = None
    comment_line: Optional[int] = None
    validation_result: Optional[ValidationResult] = None
    is_documented: bool = False
    
    
@dataclass
class OptimizationRecommendation:
    """Recommendation for optimizing a property test."""
    test_name: str
    file_path: str
    line_number: int
    current_examples: int
    recommended_examples: int
    time_savings_percent: float
    rationale: str
    strategy_type: str
    comment_info: Optional[CommentInfo] = None
    needs_comment_update: bool = False


@dataclass
class FileAnalysis:
    """Analysis results for a single test file."""
    file_path: str
    recommendations: List[OptimizationRecommendation]
    total_tests: int
    over_tested_count: int
    potential_time_savings_percent: float
    comment_compliance_stats: Optional['CommentComplianceStats'] = None


@dataclass
class CommentComplianceStats:
    """Statistics about comment compliance in a file."""
    total_property_tests: int
    documented_tests: int
    undocumented_tests: int
    format_violations: int
    compliance_percentage: float


@dataclass
class ValidationReport:
    """Complete validation report for test suite."""
    file_analyses: List[FileAnalysis]
    total_tests: int
    total_over_tested: int
    potential_time_savings_percent: float
    estimated_time_reduction_seconds: float
    overall_comment_compliance: Optional[CommentComplianceStats] = None


class FileAnalyzer:
    """Analyzes test files for max_examples optimization opportunities."""
    
    def __init__(self):
        """Initialize analyzer with classifier and calculator."""
        self.classifier = StrategyClassifier()
        self.calculator = MaxExamplesCalculator(self.classifier)
        self.comment_analyzer = CommentAnalyzer()
        self.comment_validator = CommentFormatValidator()
        
        # Regex patterns for finding property tests
        self.given_pattern = re.compile(r'@given\((.*?)\)', re.DOTALL)
        self.settings_pattern = re.compile(r'@settings\(.*?max_examples\s*=\s*(\d+).*?\)', re.DOTALL)
        self.function_pattern = re.compile(r'def\s+(test_\w+)\s*\(')

        # Keep optimization reports aligned with comment validation reports by
        # excluding meta-validator tests (these often contain intentionally
        # malformed examples and/or different semantics).
        #
        # This mirrors the exclusions in tools/test_optimization/comment_analyzer.py.
        self.excluded_test_files = {
            'test_comment_format.py',
            'test_comment_standardizer.py',
            'test_file_analyzer.py',
        }
    
    def analyze_file(self, file_path: str) -> FileAnalysis:
        """Analyze a test file and return optimization recommendations.
        
        Args:
            file_path: Path to the test file to analyze
            
        Returns:
            FileAnalysis with recommendations and statistics
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except (IOError, UnicodeDecodeError) as e:
            # Return empty analysis for files we can't read
            return FileAnalysis(
                file_path=file_path,
                recommendations=[],
                total_tests=0,
                over_tested_count=0,
                potential_time_savings_percent=0.0
            )
        
        # Analyze comments using the comment analyzer
        comment_analysis = self.comment_analyzer.analyze_file(file_path)
        
        tests = self._extract_property_tests(content)
        recommendations = []
        
        for test in tests:
            # Add comment information to the test
            test.comment_info = self._get_comment_info_for_test(test, comment_analysis)
            
            optimal_examples = self.calculator.calculate_optimal_examples(test.strategy_code)
            
            if test.current_max_examples > optimal_examples:
                time_savings = self.calculator.get_optimization_ratio(
                    test.current_max_examples, optimal_examples
                )
                
                analysis = self.classifier.classify_strategy(test.strategy_code)
                
                # Check if comment needs updating after optimization
                needs_comment_update = self._check_if_comment_needs_update(
                    test.comment_info, optimal_examples
                )
                
                recommendations.append(OptimizationRecommendation(
                    test_name=test.name,
                    file_path=test.file_path,
                    line_number=test.line_number,
                    current_examples=test.current_max_examples,
                    recommended_examples=optimal_examples,
                    time_savings_percent=time_savings * 100,
                    rationale=self._generate_rationale(analysis, optimal_examples),
                    strategy_type=analysis.strategy_type.value,
                    comment_info=test.comment_info,
                    needs_comment_update=needs_comment_update
                ))
        
        # Calculate file-level statistics
        total_tests = len(tests)
        over_tested_count = len(recommendations)
        
        if total_tests > 0:
            avg_time_savings = sum(r.time_savings_percent for r in recommendations) / total_tests
        else:
            avg_time_savings = 0.0
        
        # Create comment compliance statistics
        comment_compliance = CommentComplianceStats(
            total_property_tests=comment_analysis.total_property_tests,
            documented_tests=comment_analysis.documented_tests,
            undocumented_tests=comment_analysis.undocumented_tests,
            format_violations=len(comment_analysis.format_violations),
            compliance_percentage=(
                (comment_analysis.documented_tests / comment_analysis.total_property_tests * 100)
                if comment_analysis.total_property_tests > 0 else 100.0
            )
        )
        
        return FileAnalysis(
            file_path=file_path,
            recommendations=recommendations,
            total_tests=total_tests,
            over_tested_count=over_tested_count,
            potential_time_savings_percent=avg_time_savings,
            comment_compliance_stats=comment_compliance
        )
    
    def _extract_property_tests(self, content: str) -> List[PropertyTest]:
        """Extract property-based tests from file content."""
        tests = []
        lines = content.split('\n')
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Look for @given decorator
            if line.startswith('@given('):
                given_match = self._extract_given_decorator(lines, i)
                if given_match:
                    strategy_code, given_end_line = given_match
                    
                    # Look for @settings decorator after @given
                    settings_match = self._extract_settings_decorator(lines, given_end_line + 1)
                    if settings_match:
                        max_examples, settings_line = settings_match
                        
                        # Look for function definition
                        func_match = self._extract_function_name(lines, settings_line + 1)
                        if func_match:
                            func_name, func_line = func_match
                            
                            tests.append(PropertyTest(
                                name=func_name,
                                file_path="",  # Will be set by caller
                                line_number=i + 1,  # 1-based line numbers
                                strategy_code=strategy_code,
                                current_max_examples=max_examples,
                                decorator_line=lines[settings_line]
                            ))
                            
                            i = func_line
                        else:
                            i = settings_line + 1
                    else:
                        i = given_end_line + 1
                else:
                    i += 1
            else:
                i += 1
        
        return tests
    
    def _extract_given_decorator(self, lines: List[str], start_line: int) -> Optional[Tuple[str, int]]:
        """Extract @given decorator and its strategy code."""
        if start_line >= len(lines):
            return None
            
        # Handle multi-line @given decorators
        decorator_lines = []
        i = start_line
        paren_count = 0
        started = False
        
        while i < len(lines):
            line = lines[i].strip()
            
            if not started and line.startswith('@given('):
                started = True
                
            if started:
                decorator_lines.append(line)
                paren_count += line.count('(') - line.count(')')
                
                if paren_count == 0:
                    break
                    
            i += 1
        
        if not decorator_lines:
            return None
            
        # Extract strategy code from @given(...)
        full_decorator = ' '.join(decorator_lines)
        match = re.search(r'@given\((.*)\)', full_decorator, re.DOTALL)
        if match:
            strategy_code = match.group(1).strip()
            return strategy_code, i
            
        return None
    
    def _extract_settings_decorator(self, lines: List[str], start_line: int) -> Optional[Tuple[int, int]]:
        """Extract max_examples from @settings decorator."""
        # Look for @settings in the next few lines
        for i in range(start_line, min(start_line + 3, len(lines))):
            line = lines[i].strip()
            if line.startswith('@settings('):
                match = re.search(r'max_examples\s*=\s*(\d+)', line)
                if match:
                    return int(match.group(1)), i
        
        return None
    
    def _extract_function_name(self, lines: List[str], start_line: int) -> Optional[Tuple[str, int]]:
        """Extract function name from def statement."""
        # Look for function definition in the next few lines
        for i in range(start_line, min(start_line + 3, len(lines))):
            line = lines[i].strip()
            if line.startswith('def '):
                match = re.search(r'def\s+(test_\w+)\s*\(', line)
                if match:
                    return match.group(1), i
        
        return None
    
    def _generate_rationale(self, analysis, optimal_examples: int) -> str:
        """Generate human-readable rationale for optimization."""
        strategy_type = analysis.strategy_type.value
        
        if strategy_type == 'boolean':
            return f"Boolean strategy only needs {optimal_examples} examples (True/False)"
        elif strategy_type == 'small_finite':
            return f"Small finite strategy needs {optimal_examples} examples (input space size)"
        elif strategy_type == 'medium_finite':
            return f"Medium finite strategy capped at {optimal_examples} examples"
        elif strategy_type == 'combination':
            return f"Combination strategy uses {optimal_examples} examples (product formula, capped at 50)"
        else:
            return f"Complex strategy uses {optimal_examples} examples based on complexity"
    
    def _get_comment_info_for_test(self, test: PropertyTest, comment_analysis) -> CommentInfo:
        """Get comment information for a specific test.
        
        Args:
            test: PropertyTest instance
            comment_analysis: FileAnalysis from CommentAnalyzer
            
        Returns:
            CommentInfo with standardized comment details
        """
        # Look for valid comments that might correspond to this test
        for comment_pattern in comment_analysis.valid_comments:
            # Check if comment is near the test (within reasonable range)
            if (comment_pattern.line_number and 
                abs(comment_pattern.line_number - test.line_number) <= 5):
                
                return CommentInfo(
                    has_standardized_comment=True,
                    comment_text=comment_pattern.to_standardized_format(),
                    comment_line=comment_pattern.line_number,
                    validation_result=None,  # Already validated
                    is_documented=True
                )
        
        # Check if test is in missing documentation list
        for func_name, line_num, max_examples in comment_analysis.missing_documentation:
            if func_name == test.name and line_num == test.line_number:
                return CommentInfo(
                    has_standardized_comment=False,
                    comment_text=None,
                    comment_line=None,
                    validation_result=None,
                    is_documented=False
                )
        
        # Default case - assume documented if not in missing list
        return CommentInfo(
            has_standardized_comment=False,
            comment_text=None,
            comment_line=None,
            validation_result=None,
            is_documented=True  # Assume documented if not explicitly missing
        )
    
    def _check_if_comment_needs_update(self, comment_info: Optional[CommentInfo], 
                                     new_max_examples: int) -> bool:
        """Check if comment needs updating after optimization.
        
        Args:
            comment_info: Current comment information
            new_max_examples: New max_examples value after optimization
            
        Returns:
            True if comment needs updating, False otherwise
        """
        if not comment_info or not comment_info.has_standardized_comment:
            # No standardized comment exists, will need one after optimization
            return True
        
        if comment_info.comment_text:
            # Parse current comment to check max_examples value
            validation_result = self.comment_validator.validate_comment_format(comment_info.comment_text)
            if (validation_result.is_valid and 
                validation_result.parsed_pattern and
                validation_result.parsed_pattern.max_examples != new_max_examples):
                return True
        
        return False
    
    def validate_test_suite(self, test_directory: str) -> ValidationReport:
        """Validate entire test suite and generate optimization report."""
        test_dir = Path(test_directory)
        file_analyses = []
        
        # Find all Python test files
        for test_file in test_dir.glob('test_*.py'):
            if test_file.name in self.excluded_test_files:
                continue
            analysis = self.analyze_file(str(test_file))
            analysis.file_path = str(test_file)  # Set the correct path
            
            # Update test file paths in recommendations
            for rec in analysis.recommendations:
                rec.file_path = str(test_file)
                
            file_analyses.append(analysis)
        
        # Calculate aggregate statistics
        total_tests = sum(a.total_tests for a in file_analyses)
        total_over_tested = sum(a.over_tested_count for a in file_analyses)
        
        if total_tests > 0:
            avg_time_savings = sum(
                a.potential_time_savings_percent * a.total_tests 
                for a in file_analyses
            ) / total_tests
        else:
            avg_time_savings = 0.0
        
        # Rough estimate: assume each test takes 0.1 seconds per example on average
        estimated_time_reduction = sum(
            (r.current_examples - r.recommended_examples) * 0.1
            for a in file_analyses
            for r in a.recommendations
        )
        
        # Calculate overall comment compliance statistics
        overall_comment_compliance = self._calculate_overall_comment_compliance(file_analyses)
        
        return ValidationReport(
            file_analyses=file_analyses,
            total_tests=total_tests,
            total_over_tested=total_over_tested,
            potential_time_savings_percent=avg_time_savings,
            estimated_time_reduction_seconds=estimated_time_reduction,
            overall_comment_compliance=overall_comment_compliance
        )
    
    def _calculate_overall_comment_compliance(self, file_analyses: List[FileAnalysis]) -> CommentComplianceStats:
        """Calculate overall comment compliance across all files.
        
        Args:
            file_analyses: List of file analysis results
            
        Returns:
            CommentComplianceStats for the entire test suite
        """
        total_property_tests = 0
        total_documented_tests = 0
        total_undocumented_tests = 0
        total_format_violations = 0
        
        for analysis in file_analyses:
            if analysis.comment_compliance_stats:
                stats = analysis.comment_compliance_stats
                total_property_tests += stats.total_property_tests
                total_documented_tests += stats.documented_tests
                total_undocumented_tests += stats.undocumented_tests
                total_format_violations += stats.format_violations
        
        compliance_percentage = (
            (total_documented_tests / total_property_tests * 100)
            if total_property_tests > 0 else 100.0
        )
        
        return CommentComplianceStats(
            total_property_tests=total_property_tests,
            documented_tests=total_documented_tests,
            undocumented_tests=total_undocumented_tests,
            format_violations=total_format_violations,
            compliance_percentage=compliance_percentage
        )