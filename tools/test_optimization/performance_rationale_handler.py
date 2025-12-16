"""Performance rationale detection and documentation handler.

This module provides specialized handling for detecting performance-related
max_examples reductions and generating appropriate performance rationale comments.
"""

import os
import re
from dataclasses import dataclass
from typing import Optional, Dict, List, Tuple
from enum import Enum

from .comment_format import CommentPattern, StrategyType
from .strategy_type_mapper import StrategyTypeMapper, CommentStrategyClassification


class PerformanceReason(Enum):
    """Types of performance-related max_examples reductions."""
    CI_OPTIMIZATION = "CI optimization"
    EXECUTION_TIME = "execution time optimization"
    MEMORY_OPTIMIZATION = "memory optimization"
    COMPLEXITY_REDUCTION = "complexity reduction"
    DEADLINE_CONSTRAINT = "deadline constraint"


@dataclass
class PerformanceRationale:
    """Performance rationale information for max_examples reduction."""
    reason: PerformanceReason
    base_examples: Optional[int]
    reduced_examples: int
    performance_impact: Optional[str] = None
    ci_specific: bool = False
    
    def to_comment_rationale(self) -> str:
        """Convert to comment rationale text.
        
        Returns:
            Formatted rationale text for comment
        """
        if self.ci_specific and self.base_examples:
            return f"CI optimized: {self.base_examples} examples locally, {self.reduced_examples} in CI"
        elif self.reason == PerformanceReason.EXECUTION_TIME:
            return f"performance optimized (execution time)"
        elif self.reason == PerformanceReason.MEMORY_OPTIMIZATION:
            return f"performance optimized (memory)"
        elif self.reason == PerformanceReason.COMPLEXITY_REDUCTION:
            return f"performance optimized (complexity)"
        elif self.reason == PerformanceReason.DEADLINE_CONSTRAINT:
            return f"performance optimized (deadline constraint)"
        else:
            return f"performance optimized"


class PerformanceRationaleDetector:
    """Detects performance-related max_examples reductions in test code."""
    
    def __init__(self):
        """Initialize detector with pattern matching rules."""
        self.mapper = StrategyTypeMapper()
        
        # Patterns for detecting CI optimizations
        self.ci_patterns = [
            re.compile(r"os\.getenv\(['\"]CI['\"]\)", re.IGNORECASE),
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
        
        # Standard max_examples values that typically don't indicate performance optimization
        self.standard_values = {2, 5, 10, 20, 50, 100}
        
        # Low values that typically indicate performance optimization
        self.performance_values = {1, 2, 3, 4, 5}
    
    def detect_performance_rationale(self, test_code: str, max_examples: int) -> Optional[PerformanceRationale]:
        """Detect if max_examples value is performance-related.
        
        Args:
            test_code: Complete test function source code
            max_examples: The max_examples value being used
            
        Returns:
            PerformanceRationale if performance-related, None otherwise
        """
        # Check for CI-specific optimizations
        ci_rationale = self._detect_ci_optimization(test_code, max_examples)
        if ci_rationale:
            return ci_rationale
        
        # Check for explicit performance comments
        comment_rationale = self._detect_performance_comments(test_code, max_examples)
        if comment_rationale:
            return comment_rationale
        
        # Check for implicit performance indicators
        implicit_rationale = self._detect_implicit_performance(test_code, max_examples)
        if implicit_rationale:
            return implicit_rationale
        
        return None
    
    def _detect_ci_optimization(self, test_code: str, max_examples: int) -> Optional[PerformanceRationale]:
        """Detect CI-specific optimizations in test code."""
        for pattern in self.ci_patterns:
            if pattern.search(test_code):
                # Try to extract base and CI values
                base_examples, ci_examples = self._extract_ci_values(test_code)
                
                return PerformanceRationale(
                    reason=PerformanceReason.CI_OPTIMIZATION,
                    base_examples=base_examples,
                    reduced_examples=ci_examples or max_examples,
                    ci_specific=True
                )
        
        return None
    
    def _detect_performance_comments(self, test_code: str, max_examples: int) -> Optional[PerformanceRationale]:
        """Detect performance rationale from existing comments."""
        lines = test_code.split('\n')
        
        for line in lines:
            if line.strip().startswith('#'):
                comment_text = line.strip()
                
                for pattern in self.performance_comment_patterns:
                    if pattern.search(comment_text):
                        # Determine specific performance reason
                        if "execution" in comment_text.lower() or "time" in comment_text.lower():
                            reason = PerformanceReason.EXECUTION_TIME
                        elif "memory" in comment_text.lower():
                            reason = PerformanceReason.MEMORY_OPTIMIZATION
                        elif "complexity" in comment_text.lower():
                            reason = PerformanceReason.COMPLEXITY_REDUCTION
                        elif "deadline" in comment_text.lower():
                            reason = PerformanceReason.DEADLINE_CONSTRAINT
                        elif "CI" in comment_text:
                            reason = PerformanceReason.CI_OPTIMIZATION
                        else:
                            reason = PerformanceReason.EXECUTION_TIME
                        
                        return PerformanceRationale(
                            reason=reason,
                            base_examples=None,
                            reduced_examples=max_examples,
                            performance_impact=comment_text
                        )
        
        return None
    
    def _detect_implicit_performance(self, test_code: str, max_examples: int) -> Optional[PerformanceRationale]:
        """Detect implicit performance optimization indicators."""
        # Check if max_examples is unusually low for the strategy type
        strategy_classification = self.mapper.detect_strategy_from_test_code(test_code)
        if not strategy_classification:
            return None
        
        # For complex strategies, low max_examples values often indicate performance optimization
        if (strategy_classification.strategy_type == StrategyType.COMPLEX and 
            max_examples in self.performance_values):
            
            # Check for deadline=None which often accompanies performance optimization
            if "deadline=None" in test_code:
                return PerformanceRationale(
                    reason=PerformanceReason.DEADLINE_CONSTRAINT,
                    base_examples=None,
                    reduced_examples=max_examples
                )
            
            return PerformanceRationale(
                reason=PerformanceReason.EXECUTION_TIME,
                base_examples=None,
                reduced_examples=max_examples
            )
        
        # For combination strategies, check if examples are much lower than expected
        if (strategy_classification.strategy_type == StrategyType.COMBINATION and
            strategy_classification.input_space_size and
            max_examples < strategy_classification.input_space_size // 4):
            
            return PerformanceRationale(
                reason=PerformanceReason.COMPLEXITY_REDUCTION,
                base_examples=strategy_classification.input_space_size,
                reduced_examples=max_examples
            )
        
        return None
    
    def _extract_ci_values(self, test_code: str) -> Tuple[Optional[int], Optional[int]]:
        """Extract base and CI max_examples values from CI optimization code.
        
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
        
        return None, None
    
    def is_performance_optimized(self, test_code: str, max_examples: int) -> bool:
        """Check if a test appears to be performance-optimized.
        
        Args:
            test_code: Complete test function source code
            max_examples: The max_examples value being used
            
        Returns:
            True if test appears to be performance-optimized
        """
        return self.detect_performance_rationale(test_code, max_examples) is not None


class PerformanceCommentGenerator:
    """Generates performance-aware comments for max_examples documentation."""
    
    def __init__(self):
        """Initialize generator with detector and mapper."""
        self.detector = PerformanceRationaleDetector()
        self.mapper = StrategyTypeMapper()
    
    def generate_performance_comment(self, test_code: str, max_examples: int) -> Optional[str]:
        """Generate a performance-aware comment for the given test.
        
        Args:
            test_code: Complete test function source code
            max_examples: The max_examples value being used
            
        Returns:
            Formatted comment string if performance-related, None otherwise
        """
        # Detect performance rationale
        performance_rationale = self.detector.detect_performance_rationale(test_code, max_examples)
        if not performance_rationale:
            return None
        
        # Get base strategy classification
        strategy_classification = self.mapper.detect_strategy_from_test_code(test_code)
        if not strategy_classification:
            # Default to complex if we can't classify
            strategy_type = StrategyType.COMPLEX
        else:
            strategy_type = strategy_classification.strategy_type
        
        # Generate comment with performance rationale
        rationale_text = performance_rationale.to_comment_rationale()
        
        return f"# {strategy_type.value} strategy: {max_examples} examples ({rationale_text})"
    
    def enhance_existing_comment(self, existing_comment: str, test_code: str, max_examples: int) -> Optional[str]:
        """Enhance an existing comment with performance rationale if applicable.
        
        Args:
            existing_comment: Existing comment text
            test_code: Complete test function source code
            max_examples: The max_examples value being used
            
        Returns:
            Enhanced comment string if performance-related, None if no enhancement needed
        """
        # Check if comment already mentions performance
        if any(keyword in existing_comment.lower() for keyword in 
               ["performance", "optimized", "CI", "execution", "memory", "deadline"]):
            return None  # Already has performance information
        
        # Detect performance rationale
        performance_rationale = self.detector.detect_performance_rationale(test_code, max_examples)
        if not performance_rationale:
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
        
        # Enhance with performance rationale
        performance_text = performance_rationale.to_comment_rationale()
        enhanced_rationale = f"{basic_rationale}, {performance_text}"
        
        return f"# {strategy_type} strategy: {examples_str} examples ({enhanced_rationale})"


class PerformanceAwareCommentStandardizer:
    """Comment standardizer with performance rationale awareness."""
    
    def __init__(self):
        """Initialize with performance-aware components."""
        self.detector = PerformanceRationaleDetector()
        self.generator = PerformanceCommentGenerator()
        self.mapper = StrategyTypeMapper()
    
    def generate_comment_with_performance_awareness(self, test_code: str, max_examples: int) -> str:
        """Generate a comment with performance awareness.
        
        Args:
            test_code: Complete test function source code
            max_examples: The max_examples value being used
            
        Returns:
            Standardized comment string with performance rationale if applicable
        """
        # Try performance-aware generation first
        performance_comment = self.generator.generate_performance_comment(test_code, max_examples)
        if performance_comment:
            return performance_comment
        
        # Fall back to standard comment generation
        strategy_classification = self.mapper.detect_strategy_from_test_code(test_code)
        if not strategy_classification:
            return f"# Complex strategy: {max_examples} examples (adequate coverage)"
        
        return f"# {strategy_classification.strategy_type.value} strategy: {max_examples} examples ({strategy_classification.rationale})"
    
    def should_document_performance(self, test_code: str, max_examples: int) -> bool:
        """Check if a test should be documented with performance rationale.
        
        Args:
            test_code: Complete test function source code
            max_examples: The max_examples value being used
            
        Returns:
            True if performance documentation is recommended
        """
        return self.detector.is_performance_optimized(test_code, max_examples)
    
    def analyze_performance_patterns(self, test_files: List[str]) -> Dict[str, List[Dict]]:
        """Analyze performance patterns across multiple test files.
        
        Args:
            test_files: List of test file paths to analyze
            
        Returns:
            Dictionary with performance pattern analysis results
        """
        results = {
            'ci_optimized_tests': [],
            'performance_optimized_tests': [],
            'potential_optimizations': [],
            'performance_comments': []
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
                    
                    # Analyze performance rationale
                    performance_rationale = self.detector.detect_performance_rationale(test_code, max_examples)
                    
                    test_entry = {
                        'file': file_path,
                        'function': func_name,
                        'line': start_line,
                        'max_examples': max_examples
                    }
                    
                    if performance_rationale:
                        if performance_rationale.ci_specific:
                            results['ci_optimized_tests'].append({
                                **test_entry,
                                'base_examples': performance_rationale.base_examples,
                                'ci_examples': performance_rationale.reduced_examples
                            })
                        else:
                            results['performance_optimized_tests'].append({
                                **test_entry,
                                'reason': performance_rationale.reason.value
                            })
                    
                    # Check if performance comment exists
                    if self._has_performance_comment(test_code):
                        results['performance_comments'].append(test_entry)
            
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
    
    def _has_performance_comment(self, test_code: str) -> bool:
        """Check if test code has performance-related comments."""
        lines = test_code.split('\n')
        
        for line in lines:
            if line.strip().startswith('#'):
                comment_text = line.strip().lower()
                if any(keyword in comment_text for keyword in 
                       ["performance", "optimized", "CI", "execution", "memory", "deadline"]):
                    return True
        
        return False