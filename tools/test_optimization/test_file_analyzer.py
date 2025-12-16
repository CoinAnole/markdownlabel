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


@dataclass
class PropertyTest:
    """Information about a property-based test."""
    name: str
    file_path: str
    line_number: int
    strategy_code: str
    current_max_examples: int
    decorator_line: str
    
    
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


@dataclass
class FileAnalysis:
    """Analysis results for a single test file."""
    file_path: str
    recommendations: List[OptimizationRecommendation]
    total_tests: int
    over_tested_count: int
    potential_time_savings_percent: float


@dataclass
class ValidationReport:
    """Complete validation report for test suite."""
    file_analyses: List[FileAnalysis]
    total_tests: int
    total_over_tested: int
    potential_time_savings_percent: float
    estimated_time_reduction_seconds: float


class FileAnalyzer:
    """Analyzes test files for max_examples optimization opportunities."""
    
    def __init__(self):
        """Initialize analyzer with classifier and calculator."""
        self.classifier = StrategyClassifier()
        self.calculator = MaxExamplesCalculator(self.classifier)
        
        # Regex patterns for finding property tests
        self.given_pattern = re.compile(r'@given\((.*?)\)', re.DOTALL)
        self.settings_pattern = re.compile(r'@settings\(.*?max_examples\s*=\s*(\d+).*?\)', re.DOTALL)
        self.function_pattern = re.compile(r'def\s+(test_\w+)\s*\(')
    
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
        
        tests = self._extract_property_tests(content)
        recommendations = []
        
        for test in tests:
            optimal_examples = self.calculator.calculate_optimal_examples(test.strategy_code)
            
            if test.current_max_examples > optimal_examples:
                time_savings = self.calculator.get_optimization_ratio(
                    test.current_max_examples, optimal_examples
                )
                
                analysis = self.classifier.classify_strategy(test.strategy_code)
                
                recommendations.append(OptimizationRecommendation(
                    test_name=test.name,
                    file_path=test.file_path,
                    line_number=test.line_number,
                    current_examples=test.current_max_examples,
                    recommended_examples=optimal_examples,
                    time_savings_percent=time_savings * 100,
                    rationale=self._generate_rationale(analysis, optimal_examples),
                    strategy_type=analysis.strategy_type.value
                ))
        
        # Calculate file-level statistics
        total_tests = len(tests)
        over_tested_count = len(recommendations)
        
        if total_tests > 0:
            avg_time_savings = sum(r.time_savings_percent for r in recommendations) / total_tests
        else:
            avg_time_savings = 0.0
        
        return FileAnalysis(
            file_path=file_path,
            recommendations=recommendations,
            total_tests=total_tests,
            over_tested_count=over_tested_count,
            potential_time_savings_percent=avg_time_savings
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
    
    def validate_test_suite(self, test_directory: str) -> ValidationReport:
        """Validate entire test suite and generate optimization report."""
        test_dir = Path(test_directory)
        file_analyses = []
        
        # Find all Python test files
        for test_file in test_dir.glob('test_*.py'):
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
        
        return ValidationReport(
            file_analyses=file_analyses,
            total_tests=total_tests,
            total_over_tested=total_over_tested,
            potential_time_savings_percent=avg_time_savings,
            estimated_time_reduction_seconds=estimated_time_reduction
        )