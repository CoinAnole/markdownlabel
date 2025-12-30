"""Unified optimization detection module.

This module consolidates performance rationale and CI optimization detection
into a single, unified module, eliminating duplicate code and providing a
consistent API for detecting and documenting test optimizations.

Key consolidations:
- Unified CI detection patterns (eliminated ~50 lines of duplicate patterns)
- Single _extract_ci_values() method (eliminated ~30 lines)
- Uses find_property_tests() from test_discovery.py (eliminated ~60 lines)
- Unified OptimizationInfo class combining PerformanceRationale and CIOptimizationInfo
"""

import os
import re
from dataclasses import dataclass
from typing import Optional, Dict, List, Tuple
from enum import Enum

from .comment_manager import CommentPattern, StrategyType, CommentStrategyClassification
from .strategy_analyzer import StrategyTypeMapper

# Import the unified test discovery function from modules package
from kivy_garden.markdownlabel.tests.modules.test_discovery import find_property_tests, PropertyTest


class OptimizationType(Enum):
    """Types of test optimizations."""
    CI_OPTIMIZATION = "CI optimization"
    EXECUTION_TIME = "execution time optimization"
    MEMORY_OPTIMIZATION = "memory optimization"
    COMPLEXITY_REDUCTION = "complexity reduction"
    DEADLINE_CONSTRAINT = "deadline constraint"


class CIOptimizationPattern(Enum):
    """Types of CI optimization patterns."""
    CONDITIONAL_EXPRESSION = "conditional_expression"  # max_examples=20 if not CI else 5
    ENVIRONMENT_VARIABLE = "environment_variable"     # os.getenv('CI')
    CI_FLAG_CHECK = "ci_flag_check"                   # if CI: reduce examples
    AUTOMATED_OPTIMIZATION = "automated_optimization"  # Applied by optimization tools


@dataclass
class OptimizationInfo:
    """Unified optimization information for max_examples reduction.
    
    This dataclass combines information from both PerformanceRationale
    and CIOptimizationInfo into a single, comprehensive structure.
    
    Attributes:
        optimization_type: The type of optimization (CI, performance, etc.)
        ci_pattern_type: The specific CI pattern type (if applicable)
        base_examples: The base max_examples value (for local execution)
        reduced_examples: The reduced max_examples value (for CI or performance)
        optimization_pattern: The pattern string that was detected
        performance_impact: Optional description of performance impact
        ci_specific: Whether this is a CI-specific optimization
        rationale: Optional custom rationale text
        line_number: Optional line number where optimization was detected
    """
    optimization_type: OptimizationType
    ci_pattern_type: Optional[CIOptimizationPattern] = None
    base_examples: Optional[int] = None
    reduced_examples: Optional[int] = None
    optimization_pattern: Optional[str] = None
    performance_impact: Optional[str] = None
    ci_specific: bool = False
    rationale: Optional[str] = None
    line_number: Optional[int] = None
    
    # Backward compatibility: alias for old attribute name
    @property
    def reason(self) -> OptimizationType:
        """Backward compatibility property for 'reason' attribute.
        
        This property provides backward compatibility with the old PerformanceRationale
        class that used 'reason' instead of 'optimization_type'.
        """
        return self.optimization_type
    
    def to_comment_rationale(self) -> str:
        """Convert to comment rationale text.
        
        Returns:
            Formatted rationale text for comment
        """
        if self.rationale:
            if self.ci_specific:
                return f"CI optimized: {self.rationale}"
            return self.rationale
        
        if self.ci_specific and self.base_examples and self.reduced_examples:
            return f"CI optimized: {self.base_examples} examples locally, {self.reduced_examples} in CI"
        elif self.ci_specific and self.reduced_examples:
            return f"CI optimized: {self.reduced_examples} examples in CI"
        elif self.optimization_type in (OptimizationType.EXECUTION_TIME, 
                                          OptimizationType.MEMORY_OPTIMIZATION,
                                          OptimizationType.COMPLEXITY_REDUCTION,
                                          OptimizationType.DEADLINE_CONSTRAINT):
            return "performance optimized"
        else:
            return "optimized"


class OptimizationDetector:
    """Detects all types of optimizations in test code."""
    
    def __init__(self):
        """Initialize detector with pattern matching rules."""
        self.mapper = StrategyTypeMapper()
        
        # Backward compatibility: alias for old attribute name
        self.performance_standardizer = None  # Will be set by OptimizationAwareCommentStandardizer
        
        # Consolidated CI detection patterns (merged from both modules)
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
            re.compile(r"getenv\s*\(\s*['\"]CI['\"]\s*\)", re.IGNORECASE),
            re.compile(r"if.*CI.*else", re.IGNORECASE),
            re.compile(r"CI.*\?.*:", re.IGNORECASE),
            re.compile(r"max_examples\s*=\s*\d+\s+if.*CI", re.IGNORECASE)
        ]
        
        # Patterns for detecting performance comments
        self.performance_comment_patterns = [
            re.compile(r"performance.*optimized?", re.IGNORECASE),
            re.compile(r"execution.*time", re.IGNORECASE),
            re.compile(r"memory.*optimization", re.IGNORECASE),
            re.compile(r"deadline.*constraint", re.IGNORECASE),
            re.compile(r"complexity.*reduction", re.IGNORECASE),
            re.compile(r"CI.*optimization", re.IGNORECASE)
        ]
        
        # Patterns for CI optimization comments
        self.ci_comment_patterns = [
            re.compile(r"CI.*optimiz", re.IGNORECASE),
            re.compile(r"continuous.*integration", re.IGNORECASE),
            re.compile(r"CI.*environment", re.IGNORECASE),
            re.compile(r"CI.*performance", re.IGNORECASE),
            re.compile(r"automated.*optimization", re.IGNORECASE)
        ]
        
        # Standard max_examples values that typically don't indicate performance optimization
        self.standard_values = {2, 5, 10, 20, 50, 100}
        
        # Low values that typically indicate performance optimization
        self.performance_values = {1, 2, 3, 4, 5}
    
    def detect_optimization(self, test_code: str, max_examples: int) -> Optional[OptimizationInfo]:
        """Detect any type of optimization in test code.
        
        Args:
            test_code: Complete test function source code
            max_examples: The max_examples value being used
            
        Returns:
            OptimizationInfo if optimization detected, None otherwise
        """
        # Check for CI-specific optimizations first
        ci_info = self._detect_ci_optimization(test_code, max_examples)
        if ci_info:
            return ci_info
        
        # Check for explicit performance comments
        comment_info = self._detect_performance_comments(test_code, max_examples)
        if comment_info:
            return comment_info
        
        # Check for implicit performance indicators
        implicit_info = self._detect_implicit_performance(test_code, max_examples)
        if implicit_info:
            return implicit_info
        
        return None
    
    def _detect_ci_optimization(self, test_code: str, max_examples: int) -> Optional[OptimizationInfo]:
        """Detect CI-specific optimizations in test code."""
        # Check for conditional expressions first
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
                
                return OptimizationInfo(
                    optimization_type=OptimizationType.CI_OPTIMIZATION,
                    ci_pattern_type=CIOptimizationPattern.CONDITIONAL_EXPRESSION,
                    base_examples=base_examples,
                    reduced_examples=ci_examples,
                    optimization_pattern=match.group(0),
                    ci_specific=True,
                    rationale=f"{base_examples} examples locally, {ci_examples} in CI"
                )
        
        # Check for environment variable patterns
        for pattern in self.ci_env_patterns:
            if pattern.search(test_code):
                # Try to extract max_examples values from the context
                base_examples, ci_examples = self._extract_ci_values(test_code)
                
                if base_examples and ci_examples:
                    return OptimizationInfo(
                        optimization_type=OptimizationType.CI_OPTIMIZATION,
                        ci_pattern_type=CIOptimizationPattern.ENVIRONMENT_VARIABLE,
                        base_examples=base_examples,
                        reduced_examples=ci_examples,
                        optimization_pattern=pattern.pattern,
                        ci_specific=True,
                        rationale=f"{base_examples} examples locally, {ci_examples} in CI"
                    )
                elif ci_examples:
                    return OptimizationInfo(
                        optimization_type=OptimizationType.CI_OPTIMIZATION,
                        ci_pattern_type=CIOptimizationPattern.ENVIRONMENT_VARIABLE,
                        base_examples=None,
                        reduced_examples=ci_examples,
                        optimization_pattern=pattern.pattern,
                        ci_specific=True
                    )
        
        # Check for CI optimization comments
        lines = test_code.split('\n')
        for line_num, line in enumerate(lines):
            if line.strip().startswith('#'):
                comment_text = line.strip()
                
                for pattern in self.ci_comment_patterns:
                    if pattern.search(comment_text):
                        # Try to extract max_examples from nearby @settings
                        extracted_max = self._extract_max_examples_near_line(lines, line_num)
                        
                        if extracted_max and extracted_max not in self.standard_values:
                            return OptimizationInfo(
                                optimization_type=OptimizationType.CI_OPTIMIZATION,
                                ci_pattern_type=CIOptimizationPattern.AUTOMATED_OPTIMIZATION,
                                base_examples=extracted_max * 2,  # Estimate base value
                                reduced_examples=extracted_max,
                                optimization_pattern=comment_text,
                                line_number=line_num + 1,
                                ci_specific=True,
                                rationale="automated CI optimization"
                            )
        
        return None
    
    def _detect_performance_comments(self, test_code: str, max_examples: int) -> Optional[OptimizationInfo]:
        """Detect performance rationale from existing comments."""
        lines = test_code.split('\n')
        
        for line in lines:
            if line.strip().startswith('#'):
                comment_text = line.strip()
                
                for pattern in self.performance_comment_patterns:
                    if pattern.search(comment_text):
                        # Determine specific performance reason
                        if "execution" in comment_text.lower() or "time" in comment_text.lower():
                            opt_type = OptimizationType.EXECUTION_TIME
                        elif "memory" in comment_text.lower():
                            opt_type = OptimizationType.MEMORY_OPTIMIZATION
                        elif "complexity" in comment_text.lower():
                            opt_type = OptimizationType.COMPLEXITY_REDUCTION
                        elif "deadline" in comment_text.lower():
                            opt_type = OptimizationType.DEADLINE_CONSTRAINT
                        elif "CI" in comment_text:
                            opt_type = OptimizationType.CI_OPTIMIZATION
                        else:
                            opt_type = OptimizationType.EXECUTION_TIME
                        
                        return OptimizationInfo(
                            optimization_type=opt_type,
                            base_examples=None,
                            reduced_examples=max_examples,
                            performance_impact=comment_text
                        )
        
        return None
    
    def _detect_implicit_performance(self, test_code: str, max_examples: int) -> Optional[OptimizationInfo]:
        """Detect implicit performance optimization indicators."""
        # Check for explicit complex strategy patterns first (st.composite, st.text, st.floats)
        # These are always complex regardless of classification
        complex_patterns = ['st.composite(', 'st.text(', 'st.floats(']
        is_complex_strategy = any(pattern in test_code for pattern in complex_patterns)
        
        # For complex strategies with low max_examples, detect performance optimization
        if is_complex_strategy and max_examples in self.performance_values:
            # Check for deadline=None which often accompanies performance optimization
            if "deadline=None" in test_code:
                return OptimizationInfo(
                    optimization_type=OptimizationType.DEADLINE_CONSTRAINT,
                    base_examples=None,
                    reduced_examples=max_examples
                )
            
            return OptimizationInfo(
                optimization_type=OptimizationType.EXECUTION_TIME,
                base_examples=None,
                reduced_examples=max_examples
            )
        
        # Fall back to strategy classification check
        strategy_classification = self.mapper.detect_strategy_from_test_code(test_code)
        if not strategy_classification:
            return None
        
        # For complex strategies, low max_examples values often indicate performance optimization
        if (strategy_classification.strategy_type == StrategyType.COMPLEX and 
            max_examples in self.performance_values):
            
            # Check for deadline=None which often accompanies performance optimization
            if "deadline=None" in test_code:
                return OptimizationInfo(
                    optimization_type=OptimizationType.DEADLINE_CONSTRAINT,
                    base_examples=None,
                    reduced_examples=max_examples
                )
            
            return OptimizationInfo(
                optimization_type=OptimizationType.EXECUTION_TIME,
                base_examples=None,
                reduced_examples=max_examples
            )
        
        # For combination strategies, check if examples are much lower than expected
        if (strategy_classification.strategy_type == StrategyType.COMBINATION and
            strategy_classification.input_space_size and
            max_examples < strategy_classification.input_space_size // 4):
            
            return OptimizationInfo(
                optimization_type=OptimizationType.COMPLEXITY_REDUCTION,
                base_examples=strategy_classification.input_space_size,
                reduced_examples=max_examples
            )
        
        return None
    
    def _extract_ci_values(self, test_code: str) -> Tuple[Optional[int], Optional[int]]:
        """Extract base and CI max_examples values from CI optimization code.
        
        This is the unified implementation that consolidates the duplicate
        methods from both performance_rationale_handler.py and ci_optimization_handler.py.
        
        Returns:
            Tuple of (base_examples, ci_examples)
        """
        # Look for patterns like: max_examples=20 if not os.getenv('CI') else 5
        ci_ternary_pattern = re.compile(
            r"max_examples\s*=\s*(\d+)\s+if\s+not.*CI.*else\s+(\d+)", 
            re.IGNORECASE
        )
        match = ci_ternary_pattern.search(test_code)
        if match:
            base_examples = int(match.group(1))
            ci_examples = int(match.group(2))
            return base_examples, ci_examples
        
        # Look for reverse pattern: max_examples=5 if os.getenv('CI') else 20
        ci_reverse_pattern = re.compile(
            r"max_examples\s*=\s*(\d+)\s+if.*CI.*else\s+(\d+)", 
            re.IGNORECASE
        )
        match = ci_reverse_pattern.search(test_code)
        if match:
            ci_examples = int(match.group(1))
            base_examples = int(match.group(2))
            return base_examples, ci_examples
        
        # Fallback: Look for numeric values in conditional expressions
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
    
    # Backward compatibility: alias for old method name
    def detect_performance_rationale(self, test_code: str, max_examples: int) -> Optional[OptimizationInfo]:
        """Backward compatibility alias for detect_optimization.
        
        This method is kept for backward compatibility with existing tests.
        Use detect_optimization() instead.
        """
        return self.detect_optimization(test_code, max_examples)
    
    def is_optimized(self, test_code: str, max_examples: int) -> bool:
        """Check if a test appears to be optimized.
        
        Args:
            test_code: Complete test function source code
            max_examples: The max_examples value being used
            
        Returns:
            True if test appears to be optimized
        """
        return self.detect_optimization(test_code, max_examples) is not None
    
    def is_ci_optimized(self, test_code: str) -> bool:
        """Check if test code contains CI optimization.
        
        Args:
            test_code: Complete test function source code
            
        Returns:
            True if CI optimization detected
        """
        return self._detect_ci_optimization(test_code, 0) is not None
    
    def get_optimization_summary(self, test_code: str, max_examples: int) -> Dict[str, any]:
        """Get summary of optimization in test code.
        
        Args:
            test_code: Complete test function source code
            max_examples: The max_examples value being used
            
        Returns:
            Dictionary with optimization summary
        """
        opt_info = self.detect_optimization(test_code, max_examples)
        
        if not opt_info:
            return {
                'has_optimization': False,
                'optimization_type': None,
                'base_examples': None,
                'reduced_examples': None,
                'performance_improvement': None,
                'ci_specific': False
            }
        
        # Calculate performance improvement
        if opt_info.base_examples and opt_info.reduced_examples:
            improvement = ((opt_info.base_examples - opt_info.reduced_examples) / opt_info.base_examples) * 100
        else:
            improvement = None
        
        return {
            'has_optimization': True,
            'optimization_type': opt_info.optimization_type.value,
            'ci_pattern_type': opt_info.ci_pattern_type.value if opt_info.ci_pattern_type else None,
            'base_examples': opt_info.base_examples,
            'reduced_examples': opt_info.reduced_examples,
            'performance_improvement': f"{improvement:.1f}%" if improvement else None,
            'optimization_pattern': opt_info.optimization_pattern,
            'rationale': opt_info.rationale,
            'ci_specific': opt_info.ci_specific
        }


class OptimizationCommentGenerator:
    """Generates optimization-aware comments for max_examples documentation."""
    
    def __init__(self):
        """Initialize generator with detector and mapper."""
        self.detector = OptimizationDetector()
        self.mapper = StrategyTypeMapper()
        
        # Backward compatibility: set detector's performance_standardizer reference
        self.detector.performance_standardizer = self
    
    # Backward compatibility: alias for old method name
    def generate_performance_comment(self, test_code: str, max_examples: int) -> Optional[str]:
        """Backward compatibility alias for generate_optimization_comment.
        
        This method is kept for backward compatibility with existing tests.
        Use generate_optimization_comment() instead.
        """
        return self.generate_optimization_comment(test_code, max_examples)
    
    def generate_optimization_comment(self, test_code: str, max_examples: int) -> Optional[str]:
        """Generate an optimization-aware comment for the given test.
        
        Args:
            test_code: Complete test function source code
            max_examples: The max_examples value being used
            
        Returns:
            Formatted comment string if optimization-related, None otherwise
        """
        # Detect optimization
        opt_info = self.detector.detect_optimization(test_code, max_examples)
        if not opt_info:
            return None
        
        # Get base strategy classification
        strategy_classification = self.mapper.detect_strategy_from_test_code(test_code)
        if not strategy_classification:
            # Default to complex if we can't classify
            strategy_type = StrategyType.COMPLEX
        else:
            strategy_type = strategy_classification.strategy_type
        
        # Generate comment with optimization rationale
        rationale_text = opt_info.to_comment_rationale()
        
        return f"# {strategy_type.value} strategy: {max_examples} examples ({rationale_text})"
    
    def enhance_existing_comment(self, existing_comment: str, test_code: str, max_examples: int) -> Optional[str]:
        """Enhance an existing comment with optimization rationale if applicable.
        
        Args:
            existing_comment: Existing comment text
            test_code: Complete test function source code
            max_examples: The max_examples value being used
            
        Returns:
            Enhanced comment string if optimization-related, None if no enhancement needed
        """
        # Check if comment already mentions optimization keywords
        if any(keyword in existing_comment.lower() for keyword in 
               ["performance", "optimized", "CI", "execution", "memory", "deadline"]):
            return None  # Already has optimization information
        
        # Detect optimization
        opt_info = self.detector.detect_optimization(test_code, max_examples)
        if not opt_info:
            return None
        
        # Parse existing comment to extract strategy type and basic rationale
        comment_pattern = re.match(
            r'^#\s*(\w+(?:\s+\w+)*)\s+strategy:\s*(\d+)\s+examples\s*\(([^)]+)\)\s*$',
            existing_comment.strip(),
            re.IGNORECASE
        )
        
        if not comment_pattern:
            return None  # Can't parse existing comment
        
        strategy_type, examples_str, basic_rationale = comment_pattern.groups()
        
        # Enhance with optimization rationale
        opt_text = opt_info.to_comment_rationale()
        enhanced_rationale = f"{basic_rationale}, {opt_text}"
        
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


class OptimizationAwareCommentStandardizer:
    """Comment standardizer with optimization rationale awareness."""
    
    def __init__(self):
        """Initialize with optimization-aware components."""
        self.detector = OptimizationDetector()
        self.generator = OptimizationCommentGenerator()
        self.mapper = StrategyTypeMapper()
        
        # Backward compatibility: set detector's performance_standardizer reference
        self.detector.performance_standardizer = self.generator
        self.generator.detector.performance_standardizer = self.generator
    
    def generate_comment_with_optimization_awareness(self, test_code: str, max_examples: int) -> str:
        """Generate a comment with optimization awareness.
        
        Args:
            test_code: Complete test function source code
            max_examples: The max_examples value being used
            
        Returns:
            Standardized comment string with optimization rationale if applicable
        """
        # Try optimization-aware generation first
        opt_comment = self.generator.generate_optimization_comment(test_code, max_examples)
        if opt_comment:
            return opt_comment
        
        # Fall back to standard comment generation
        strategy_classification = self.mapper.detect_strategy_from_test_code(test_code)
        if not strategy_classification:
            return f"# Complex strategy: {max_examples} examples (adequate coverage)"
        
        return f"# {strategy_classification.strategy_type.value} strategy: {max_examples} examples ({strategy_classification.rationale})"
    
    def should_document_optimization(self, test_code: str, max_examples: int) -> bool:
        """Check if a test should be documented with optimization rationale.
        
        Args:
            test_code: Complete test function source code
            max_examples: The max_examples value being used
            
        Returns:
            True if optimization documentation is recommended
        """
        return self.detector.is_optimized(test_code, max_examples)
    
    # Backward compatibility: alias for old method name
    def analyze_performance_patterns(self, test_files: List[str]) -> Dict[str, List[Dict]]:
        """Backward compatibility alias for analyze_optimization_patterns.
        
        This method is kept for backward compatibility with existing tests.
        Use analyze_optimization_patterns() instead.
        """
        return self.analyze_optimization_patterns(test_files)
    
    def analyze_optimization_patterns(self, test_files: List[str]) -> Dict[str, List[Dict]]:
        """Analyze optimization patterns across multiple test files.
        
        This method uses the unified find_property_tests() function from
        test_discovery.py, eliminating the duplicate _find_property_tests()
        implementations that existed in both source modules.
        
        Args:
            test_files: List of test file paths to analyze
            
        Returns:
            Dictionary with optimization pattern analysis results
        """
        results = {
            'ci_optimized_tests': [],
            'performance_optimized_tests': [],
            'potential_optimizations': [],
            'optimization_comments': [],
            'optimization_patterns': {},
            'performance_improvements': []
        }
        
        for file_path in test_files:
            if not os.path.exists(file_path):
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Use the unified find_property_tests function from test_discovery.py
                property_tests = find_property_tests(content)
                
                for test in property_tests:
                    if not test.max_examples:
                        continue
                    
                    # Extract test function code
                    test_code = self._extract_test_code_for_test(content, test)
                    
                    # Analyze optimization
                    opt_info = self.detector.detect_optimization(test_code, test.max_examples)
                    
                    test_entry = {
                        'file': file_path,
                        'function': test.name,
                        'line': test.start_line,
                        'max_examples': test.max_examples
                    }
                    
                    if opt_info:
                        if opt_info.ci_specific:
                            results['ci_optimized_tests'].append({
                                **test_entry,
                                'optimization_type': opt_info.ci_pattern_type.value if opt_info.ci_pattern_type else None,
                                'base_examples': opt_info.base_examples,
                                'ci_examples': opt_info.reduced_examples,
                                'rationale': opt_info.rationale
                            })
                            
                            # Track optimization patterns
                            if opt_info.ci_pattern_type:
                                pattern_type = opt_info.ci_pattern_type.value
                                if pattern_type not in results['optimization_patterns']:
                                    results['optimization_patterns'][pattern_type] = 0
                                results['optimization_patterns'][pattern_type] += 1
                            
                            # Calculate performance improvement
                            if opt_info.base_examples and opt_info.reduced_examples:
                                improvement = ((opt_info.base_examples - opt_info.reduced_examples) / opt_info.base_examples) * 100
                                results['performance_improvements'].append({
                                    **test_entry,
                                    'improvement_percentage': improvement
                                })
                        else:
                            results['performance_optimized_tests'].append({
                                **test_entry,
                                'optimization_type': opt_info.optimization_type.value
                            })
                    
                    # Check if optimization comment exists
                    if self._has_optimization_comment(test_code):
                        results['optimization_comments'].append(test_entry)
                    
                    # Check for optimization opportunities
                    elif self._could_benefit_from_optimization(test_code, test.max_examples):
                        results['potential_optimizations'].append({
                            **test_entry,
                            'suggested_examples': max(1, test.max_examples // 4),
                            'potential_improvement': 75.0
                        })
            
            except Exception as e:
                # Skip files that can't be processed
                continue
        
        return results
    
    def _extract_test_code_for_test(self, content: str, test: PropertyTest) -> str:
        """Extract the complete source code for a property test.
        
        Args:
            content: The full file content as a string
            test: The PropertyTest object describing the test
            
        Returns:
            The test source code including decorators
        """
        lines = content.split('\n')
        start_idx = max(0, test.decorator_start_line)
        end_idx = min(len(lines), test.end_line)
        return '\n'.join(lines[start_idx:end_idx])
    
    def _has_optimization_comment(self, test_code: str) -> bool:
        """Check if test code has optimization-related comments."""
        lines = test_code.split('\n')
        
        for line in lines:
            if line.strip().startswith('#'):
                comment_text = line.strip().lower()
                if any(keyword in comment_text for keyword in 
                       ["performance", "optimized", "CI", "execution", "memory", "deadline"]):
                    return True
        
        return False
    
    def _could_benefit_from_optimization(self, test_code: str, max_examples: int) -> bool:
        """Check if test could benefit from optimization.
        
        Args:
            test_code: Complete test function source code
            max_examples: Current max_examples value
            
        Returns:
            True if test could benefit from optimization
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
    
    def analyze_optimization_coverage(self, test_files: List[str]) -> Dict[str, any]:
        """Analyze optimization coverage across test files.
        
        Args:
            test_files: List of test file paths to analyze
            
        Returns:
            Dictionary with optimization coverage analysis
        """
        total_tests = 0
        optimized_tests = 0
        optimization_opportunities = 0
        
        optimization_types = {}
        performance_improvements = []
        
        for file_path in test_files:
            if not os.path.exists(file_path):
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Use the unified find_property_tests function from test_discovery.py
                property_tests = find_property_tests(content)
                total_tests += len(property_tests)
                
                for test in property_tests:
                    if not test.max_examples:
                        continue
                    
                    # Extract test function code
                    test_code = self._extract_test_code_for_test(content, test)
                    
                    opt_info = self.detector.detect_optimization(test_code, test.max_examples)
                    
                    if opt_info:
                        optimized_tests += 1
                        
                        # Track optimization type
                        opt_type = opt_info.optimization_type.value
                        optimization_types[opt_type] = optimization_types.get(opt_type, 0) + 1
                        
                        # Calculate improvement
                        if opt_info.base_examples and opt_info.reduced_examples:
                            improvement = ((opt_info.base_examples - opt_info.reduced_examples) / opt_info.base_examples) * 100
                            performance_improvements.append(improvement)
                    
                    elif self._could_benefit_from_optimization(test_code, test.max_examples):
                        optimization_opportunities += 1
            
            except Exception:
                continue
        
        # Calculate statistics
        coverage = (optimized_tests / total_tests * 100) if total_tests > 0 else 0
        avg_improvement = sum(performance_improvements) / len(performance_improvements) if performance_improvements else 0
        
        return {
            'total_tests': total_tests,
            'optimized_tests': optimized_tests,
            'coverage_percentage': coverage,
            'optimization_opportunities': optimization_opportunities,
            'optimization_types': optimization_types,
            'average_performance_improvement': avg_improvement,
            'performance_improvements': performance_improvements
        }


# Backward compatibility aliases - these allow existing code to continue working
# while using the new unified module
PerformanceRationale = OptimizationInfo
PerformanceReason = OptimizationType
CIOptimizationInfo = OptimizationInfo
CIOptimizationType = CIOptimizationPattern

PerformanceRationaleDetector = OptimizationDetector
CIOptimizationDetector = OptimizationDetector

PerformanceCommentGenerator = OptimizationCommentGenerator
CIOptimizationCommentGenerator = OptimizationCommentGenerator

PerformanceAwareCommentStandardizer = OptimizationAwareCommentStandardizer
CIOptimizationIntegrator = OptimizationAwareCommentStandardizer
