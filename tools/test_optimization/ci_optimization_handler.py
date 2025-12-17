"""CI optimization documentation handler.

This module provides specialized handling for detecting and documenting
CI-specific max_examples reductions with appropriate rationale comments
that reference the optimization process.
"""

import os
import re
from dataclasses import dataclass
from typing import Optional, Dict, List, Tuple, Set
from enum import Enum

from .performance_rationale_handler import (
    PerformanceRationaleDetector, 
    PerformanceRationale, 
    PerformanceReason
)
from .comment_format import CommentPattern, StrategyType


class CIOptimizationType(Enum):
    """Types of CI optimization patterns."""
    CONDITIONAL_EXPRESSION = "conditional_expression"  # max_examples=20 if not CI else 5
    ENVIRONMENT_VARIABLE = "environment_variable"     # os.getenv('CI')
    CI_FLAG_CHECK = "ci_flag_check"                   # if CI: reduce examples
    AUTOMATED_OPTIMIZATION = "automated_optimization"  # Applied by optimization tools


@dataclass
class CIOptimizationInfo:
    """Information about CI optimization in a test."""
    optimization_type: CIOptimizationType
    base_examples: int
    ci_examples: int
    optimization_pattern: str
    line_number: Optional[int] = None
    rationale: Optional[str] = None
    
    def to_comment_rationale(self) -> str:
        """Convert to comment rationale text.
        
        Returns:
            Formatted rationale text for CI optimization comment
        """
        if self.rationale:
            return f"CI optimized: {self.rationale}"
        else:
            return f"CI optimized: {self.base_examples} examples locally, {self.ci_examples} in CI"


class CIOptimizationDetector:
    """Detects CI-specific optimizations in test code."""
    
    def __init__(self):
        """Initialize detector with CI optimization patterns."""
        # Patterns for different CI optimization types
        self.ci_conditional_patterns = [
            # Pattern: max_examples=base if not os.getenv('CI') else ci
            re.compile(
                r'max_examples\s*=\s*(\d+)\s+if\s+not\s+os\.getenv\s*\(\s*[\'"]CI[\'"]\s*\)\s+else\s+(\d+)',
                re.IGNORECASE
            ),
            # Pattern: max_examples=ci if os.getenv('CI') else base
            re.compile(
                r'max_examples\s*=\s*(\d+)\s+if\s+os\.getenv\s*\(\s*[\'"]CI[\'"]\s*\)\s+else\s+(\d+)',
                re.IGNORECASE
            ),
            # Pattern: max_examples=base if not CI else ci (with various CI checks)
            re.compile(
                r'max_examples\s*=\s*(\d+)\s+if\s+not\s+.*CI.*\s+else\s+(\d+)',
                re.IGNORECASE
            ),
            # Pattern: max_examples=ci if CI else base
            re.compile(
                r'max_examples\s*=\s*(\d+)\s+if\s+.*CI.*\s+else\s+(\d+)',
                re.IGNORECASE
            )
        ]
        
        # Patterns for CI environment variable checks
        self.ci_env_patterns = [
            re.compile(r"os\.getenv\s*\(\s*['\"]CI['\"]\s*\)", re.IGNORECASE),
            re.compile(r"os\.environ\.get\s*\(\s*['\"]CI['\"]\s*\)", re.IGNORECASE),
            re.compile(r"CI\s*in\s+os\.environ", re.IGNORECASE),
            re.compile(r"getenv\s*\(\s*['\"]CI['\"]\s*\)", re.IGNORECASE)
        ]
        
        # Patterns for CI optimization comments
        self.ci_comment_patterns = [
            re.compile(r"CI.*optimiz", re.IGNORECASE),
            re.compile(r"continuous.*integration", re.IGNORECASE),
            re.compile(r"CI.*environment", re.IGNORECASE),
            re.compile(r"CI.*performance", re.IGNORECASE),
            re.compile(r"automated.*optimization", re.IGNORECASE)
        ]
        
        # Standard max_examples values
        self.standard_values = {2, 5, 10, 20, 50, 100}
    
    def detect_ci_optimization(self, test_code: str) -> Optional[CIOptimizationInfo]:
        """Detect CI optimization in test code.
        
        Args:
            test_code: Complete test function source code
            
        Returns:
            CIOptimizationInfo if CI optimization detected, None otherwise
        """
        # Check for conditional expressions first
        conditional_info = self._detect_conditional_ci_optimization(test_code)
        if conditional_info:
            return conditional_info
        
        # Check for environment variable patterns
        env_info = self._detect_environment_ci_optimization(test_code)
        if env_info:
            return env_info
        
        # Check for CI optimization comments
        comment_info = self._detect_comment_ci_optimization(test_code)
        if comment_info:
            return comment_info
        
        return None
    
    def _detect_conditional_ci_optimization(self, test_code: str) -> Optional[CIOptimizationInfo]:
        """Detect conditional CI optimization patterns."""
        for pattern in self.ci_conditional_patterns:
            match = pattern.search(test_code)
            if match:
                # Determine which group is base vs CI based on pattern
                if "if not" in match.group(0).lower():
                    # Pattern: base if not CI else ci
                    base_examples = int(match.group(1))
                    ci_examples = int(match.group(2))
                else:
                    # Pattern: ci if CI else base
                    ci_examples = int(match.group(1))
                    base_examples = int(match.group(2))
                
                return CIOptimizationInfo(
                    optimization_type=CIOptimizationType.CONDITIONAL_EXPRESSION,
                    base_examples=base_examples,
                    ci_examples=ci_examples,
                    optimization_pattern=match.group(0),
                    rationale=f"{base_examples} examples locally, {ci_examples} in CI"
                )
        
        return None
    
    def _detect_environment_ci_optimization(self, test_code: str) -> Optional[CIOptimizationInfo]:
        """Detect environment variable CI optimization patterns."""
        # Look for CI environment checks
        for pattern in self.ci_env_patterns:
            if pattern.search(test_code):
                # Try to extract max_examples values from the context
                base_examples, ci_examples = self._extract_ci_values_from_context(test_code)
                
                if base_examples and ci_examples:
                    return CIOptimizationInfo(
                        optimization_type=CIOptimizationType.ENVIRONMENT_VARIABLE,
                        base_examples=base_examples,
                        ci_examples=ci_examples,
                        optimization_pattern=pattern.pattern,
                        rationale=f"{base_examples} examples locally, {ci_examples} in CI"
                    )
        
        return None
    
    def _detect_comment_ci_optimization(self, test_code: str) -> Optional[CIOptimizationInfo]:
        """Detect CI optimization from comments."""
        lines = test_code.split('\n')
        
        for line_num, line in enumerate(lines):
            if line.strip().startswith('#'):
                comment_text = line.strip()
                
                for pattern in self.ci_comment_patterns:
                    if pattern.search(comment_text):
                        # Try to extract max_examples from nearby @settings
                        max_examples = self._extract_max_examples_near_line(lines, line_num)
                        
                        if max_examples and max_examples not in self.standard_values:
                            return CIOptimizationInfo(
                                optimization_type=CIOptimizationType.AUTOMATED_OPTIMIZATION,
                                base_examples=max_examples * 2,  # Estimate base value
                                ci_examples=max_examples,
                                optimization_pattern=comment_text,
                                line_number=line_num + 1,
                                rationale="automated CI optimization"
                            )
        
        return None
    
    def _extract_ci_values_from_context(self, test_code: str) -> Tuple[Optional[int], Optional[int]]:
        """Extract base and CI max_examples values from test context."""
        # Look for numeric values in conditional expressions
        numbers = re.findall(r'\d+', test_code)
        if len(numbers) >= 2:
            # Assume larger value is base, smaller is CI
            values = [int(n) for n in numbers if int(n) > 0]
            if len(values) >= 2:
                values.sort()
                return values[-1], values[0]  # largest, smallest
        
        return None, None
    
    def _extract_max_examples_near_line(self, lines: List[str], line_num: int) -> Optional[int]:
        """Extract max_examples value from lines near the given line number."""
        # Search a few lines around the comment
        search_range = range(max(0, line_num - 3), min(len(lines), line_num + 4))
        
        for i in search_range:
            line = lines[i]
            if '@settings' in line:
                # Extract max_examples from settings line
                match = re.search(r'max_examples\s*=\s*(\d+)', line)
                if match:
                    return int(match.group(1))
        
        return None
    
    def is_ci_optimized(self, test_code: str) -> bool:
        """Check if test code contains CI optimization.
        
        Args:
            test_code: Complete test function source code
            
        Returns:
            True if CI optimization detected
        """
        return self.detect_ci_optimization(test_code) is not None
    
    def get_ci_optimization_summary(self, test_code: str) -> Dict[str, any]:
        """Get summary of CI optimization in test code.
        
        Args:
            test_code: Complete test function source code
            
        Returns:
            Dictionary with CI optimization summary
        """
        ci_info = self.detect_ci_optimization(test_code)
        
        if not ci_info:
            return {
                'has_ci_optimization': False,
                'optimization_type': None,
                'base_examples': None,
                'ci_examples': None,
                'performance_improvement': None
            }
        
        # Calculate performance improvement
        if ci_info.base_examples and ci_info.ci_examples:
            improvement = ((ci_info.base_examples - ci_info.ci_examples) / ci_info.base_examples) * 100
        else:
            improvement = None
        
        return {
            'has_ci_optimization': True,
            'optimization_type': ci_info.optimization_type.value,
            'base_examples': ci_info.base_examples,
            'ci_examples': ci_info.ci_examples,
            'performance_improvement': f"{improvement:.1f}%" if improvement else None,
            'optimization_pattern': ci_info.optimization_pattern,
            'rationale': ci_info.rationale
        }


class CIOptimizationCommentGenerator:
    """Generates CI optimization-specific comments."""
    
    def __init__(self):
        """Initialize generator with CI detector."""
        self.detector = CIOptimizationDetector()
        self.performance_detector = PerformanceRationaleDetector()
    
    def generate_ci_optimization_comment(self, test_code: str, max_examples: int) -> Optional[str]:
        """Generate CI optimization comment for test code.
        
        Args:
            test_code: Complete test function source code
            max_examples: The max_examples value being used
            
        Returns:
            Formatted CI optimization comment string if applicable, None otherwise
        """
        # Detect CI optimization
        ci_info = self.detector.detect_ci_optimization(test_code)
        if not ci_info:
            return None
        
        # Determine strategy type from test code
        strategy_type = self._determine_strategy_type(test_code)
        
        # Generate CI optimization rationale
        rationale = ci_info.to_comment_rationale()
        
        return f"# {strategy_type.value} strategy: {max_examples} examples ({rationale})"
    
    def enhance_comment_with_ci_info(self, existing_comment: str, test_code: str) -> Optional[str]:
        """Enhance existing comment with CI optimization information.
        
        Args:
            existing_comment: Existing comment text
            test_code: Complete test function source code
            
        Returns:
            Enhanced comment string if CI optimization detected, None otherwise
        """
        # Check if comment already mentions CI
        if "CI" in existing_comment:
            return None  # Already has CI information
        
        # Detect CI optimization
        ci_info = self.detector.detect_ci_optimization(test_code)
        if not ci_info:
            return None
        
        # Parse existing comment
        comment_pattern = re.match(
            r'^#\s*(\w+(?:\s+\w+)*)\s+strategy:\s*(\d+)\s+examples\s*\(([^)]+)\)\s*$',
            existing_comment.strip(),
            re.IGNORECASE
        )
        
        if not comment_pattern:
            return None
        
        strategy_type, examples_str, basic_rationale = comment_pattern.groups()
        
        # Enhance with CI optimization rationale
        ci_rationale = ci_info.to_comment_rationale()
        enhanced_rationale = f"{basic_rationale}, {ci_rationale}"
        
        return f"# {strategy_type} strategy: {examples_str} examples ({enhanced_rationale})"
    
    def _determine_strategy_type(self, test_code: str) -> StrategyType:
        """Determine strategy type from test code.
        
        Args:
            test_code: Complete test function source code
            
        Returns:
            StrategyType enum value
        """
        # Simple heuristics to determine strategy type
        if 'st.booleans()' in test_code:
            return StrategyType.BOOLEAN
        elif 'st.integers(' in test_code and 'min_value' in test_code and 'max_value' in test_code:
            # Try to determine if it's small or medium finite
            min_match = re.search(r'min_value\s*=\s*(\d+)', test_code)
            max_match = re.search(r'max_value\s*=\s*(\d+)', test_code)
            
            if min_match and max_match:
                range_size = int(max_match.group(1)) - int(min_match.group(1)) + 1
                if range_size <= 10:
                    return StrategyType.SMALL_FINITE
                elif range_size <= 50:
                    return StrategyType.MEDIUM_FINITE
        elif 'st.sampled_from(' in test_code:
            return StrategyType.SMALL_FINITE  # Assume small finite for sampled_from
        elif 'st.tuples(' in test_code or len(re.findall(r'st\.\w+\(', test_code)) > 1:
            return StrategyType.COMBINATION
        
        # Default to complex for text, floats, and other strategies
        return StrategyType.COMPLEX
    
    def generate_ci_optimization_documentation(self, test_files: List[str]) -> Dict[str, List[Dict]]:
        """Generate CI optimization documentation for multiple test files.
        
        Args:
            test_files: List of test file paths to analyze
            
        Returns:
            Dictionary with CI optimization documentation results
        """
        results = {
            'ci_optimized_tests': [],
            'optimization_opportunities': [],
            'optimization_patterns': {},
            'performance_improvements': []
        }
        
        for file_path in test_files:
            if not os.path.exists(file_path):
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Find all property-based tests
                property_tests = self._find_property_tests(content)
                
                for test_info in property_tests:
                    func_name, start_line, end_line, max_examples = test_info
                    if not max_examples:
                        continue
                    
                    # Extract test function code
                    lines = content.split('\n')
                    test_code = '\n'.join(lines[max(0, start_line-5):end_line])
                    
                    # Analyze CI optimization
                    ci_info = self.detector.detect_ci_optimization(test_code)
                    
                    test_entry = {
                        'file': file_path,
                        'function': func_name,
                        'line': start_line,
                        'max_examples': max_examples
                    }
                    
                    if ci_info:
                        # Add to CI optimized tests
                        results['ci_optimized_tests'].append({
                            **test_entry,
                            'optimization_type': ci_info.optimization_type.value,
                            'base_examples': ci_info.base_examples,
                            'ci_examples': ci_info.ci_examples,
                            'rationale': ci_info.rationale
                        })
                        
                        # Track optimization patterns
                        pattern_type = ci_info.optimization_type.value
                        if pattern_type not in results['optimization_patterns']:
                            results['optimization_patterns'][pattern_type] = 0
                        results['optimization_patterns'][pattern_type] += 1
                        
                        # Calculate performance improvement
                        if ci_info.base_examples and ci_info.ci_examples:
                            improvement = ((ci_info.base_examples - ci_info.ci_examples) / ci_info.base_examples) * 100
                            results['performance_improvements'].append({
                                **test_entry,
                                'improvement_percentage': improvement
                            })
                    
                    else:
                        # Check if this could benefit from CI optimization
                        if self._could_benefit_from_ci_optimization(test_code, max_examples):
                            results['optimization_opportunities'].append({
                                **test_entry,
                                'suggested_ci_examples': max(1, max_examples // 4),
                                'potential_improvement': 75.0
                            })
            
            except Exception as e:
                # Skip files that can't be processed
                continue
        
        return results
    
    def _find_property_tests(self, content: str) -> List[Tuple[str, int, int, Optional[int]]]:
        """Find all property-based test functions in the content."""
        property_tests = []
        lines = content.split('\n')
        
        # Pattern to match @settings decorator with max_examples
        settings_pattern = re.compile(r'@settings\([^)]*max_examples\s*=\s*(\d+)', re.DOTALL)
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Look for @given decorator
            if line.startswith('@given'):
                # Find the function definition that follows
                j = i + 1
                max_examples = None
                
                # Look for @settings decorator between @given and function def
                while j < len(lines):
                    next_line = lines[j].strip()
                    
                    if next_line.startswith('@settings'):
                        # Extract max_examples from settings
                        settings_match = settings_pattern.search(next_line)
                        if settings_match:
                            max_examples = int(settings_match.group(1))
                    
                    elif next_line.startswith('def test_'):
                        # Found the function definition
                        func_match = re.match(r'def\s+(test_\w+)\s*\(', next_line)
                        if func_match:
                            func_name = func_match.group(1)
                            
                            # Find the end of the function
                            end_line = j + 1
                            while end_line < len(lines):
                                end_line_content = lines[end_line]
                                if (end_line_content.strip().startswith('def ') or 
                                    end_line_content.strip().startswith('class ') or
                                    (end_line_content and not end_line_content.startswith(' ') and not end_line_content.startswith('\t'))):
                                    break
                                end_line += 1
                            
                            property_tests.append((func_name, j + 1, end_line, max_examples))
                        break
                    
                    elif next_line.startswith('def ') or next_line.startswith('class '):
                        break
                    
                    j += 1
            
            i += 1
        
        return property_tests
    
    def _could_benefit_from_ci_optimization(self, test_code: str, max_examples: int) -> bool:
        """Check if test could benefit from CI optimization.
        
        Args:
            test_code: Complete test function source code
            max_examples: Current max_examples value
            
        Returns:
            True if test could benefit from CI optimization
        """
        # Tests with high max_examples values could benefit
        if max_examples >= 20:
            # Check if it's a complex strategy that would benefit
            if any(pattern in test_code for pattern in ['st.text(', 'st.floats(', 'st.composite(']):
                return True
            
            # Check if it's a large combination
            if 'st.tuples(' in test_code and max_examples >= 15:
                return True
        
        return False


class CIOptimizationIntegrator:
    """Integrates CI optimization with existing comment standardization tools."""
    
    def __init__(self):
        """Initialize integrator with CI components."""
        self.detector = CIOptimizationDetector()
        self.generator = CIOptimizationCommentGenerator()
        self.performance_detector = PerformanceRationaleDetector()
    
    def should_use_ci_optimization_comment(self, test_code: str, max_examples: int) -> bool:
        """Check if CI optimization comment should be used.
        
        Args:
            test_code: Complete test function source code
            max_examples: The max_examples value being used
            
        Returns:
            True if CI optimization comment is appropriate
        """
        return self.detector.is_ci_optimized(test_code)
    
    def generate_integrated_comment(self, test_code: str, max_examples: int) -> Optional[str]:
        """Generate integrated comment with CI optimization awareness.
        
        Args:
            test_code: Complete test function source code
            max_examples: The max_examples value being used
            
        Returns:
            Integrated comment string if applicable, None otherwise
        """
        # Check for CI optimization first
        ci_comment = self.generator.generate_ci_optimization_comment(test_code, max_examples)
        if ci_comment:
            return ci_comment
        
        # Fall back to general performance rationale
        performance_rationale = self.performance_detector.detect_performance_rationale(test_code, max_examples)
        if performance_rationale and performance_rationale.ci_specific:
            # This should have been caught by CI optimization, but handle as fallback
            strategy_type = self.generator._determine_strategy_type(test_code)
            rationale = performance_rationale.to_comment_rationale()
            return f"# {strategy_type.value} strategy: {max_examples} examples ({rationale})"
        
        return None
    
    def analyze_ci_optimization_coverage(self, test_files: List[str]) -> Dict[str, any]:
        """Analyze CI optimization coverage across test files.
        
        Args:
            test_files: List of test file paths to analyze
            
        Returns:
            Dictionary with CI optimization coverage analysis
        """
        total_tests = 0
        ci_optimized_tests = 0
        optimization_opportunities = 0
        
        optimization_types = {}
        performance_improvements = []
        
        for file_path in test_files:
            if not os.path.exists(file_path):
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                property_tests = self.generator._find_property_tests(content)
                total_tests += len(property_tests)
                
                for test_info in property_tests:
                    func_name, start_line, end_line, max_examples = test_info
                    if not max_examples:
                        continue
                    
                    lines = content.split('\n')
                    test_code = '\n'.join(lines[max(0, start_line-5):end_line])
                    
                    ci_info = self.detector.detect_ci_optimization(test_code)
                    
                    if ci_info:
                        ci_optimized_tests += 1
                        
                        # Track optimization type
                        opt_type = ci_info.optimization_type.value
                        optimization_types[opt_type] = optimization_types.get(opt_type, 0) + 1
                        
                        # Calculate improvement
                        if ci_info.base_examples and ci_info.ci_examples:
                            improvement = ((ci_info.base_examples - ci_info.ci_examples) / ci_info.base_examples) * 100
                            performance_improvements.append(improvement)
                    
                    elif self.generator._could_benefit_from_ci_optimization(test_code, max_examples):
                        optimization_opportunities += 1
            
            except Exception:
                continue
        
        # Calculate statistics
        ci_coverage = (ci_optimized_tests / total_tests * 100) if total_tests > 0 else 0
        avg_improvement = sum(performance_improvements) / len(performance_improvements) if performance_improvements else 0
        
        return {
            'total_tests': total_tests,
            'ci_optimized_tests': ci_optimized_tests,
            'ci_coverage_percentage': ci_coverage,
            'optimization_opportunities': optimization_opportunities,
            'optimization_types': optimization_types,
            'average_performance_improvement': avg_improvement,
            'performance_improvements': performance_improvements
        }