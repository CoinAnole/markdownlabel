"""Strategy type classification mapper for comment standardization.

This module provides mapping between the existing strategy classification system
and the standardized comment format terminology, along with enhanced classification
for edge cases and complex strategy combinations.
"""

import ast
import re
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass

from .strategy_classifier import StrategyClassifier, StrategyType as ExistingStrategyType
from .comment_format import StrategyType as CommentStrategyType


@dataclass
class StrategyTypeMapping:
    """Mapping between existing and comment format strategy types."""
    comment_type: CommentStrategyType
    rationale_template: str
    input_space_size: Optional[int] = None


class StrategyTypeMapper:
    """Maps existing strategy classifications to comment format terminology."""
    
    def __init__(self):
        """Initialize mapper with existing classifier and mapping rules."""
        self.existing_classifier = StrategyClassifier()
        
        # Mapping from existing strategy types to comment format types
        self.type_mapping = {
            ExistingStrategyType.BOOLEAN: StrategyTypeMapping(
                comment_type=CommentStrategyType.BOOLEAN,
                rationale_template="True/False coverage"
            ),
            ExistingStrategyType.SMALL_FINITE: StrategyTypeMapping(
                comment_type=CommentStrategyType.SMALL_FINITE,
                rationale_template="input space size: {input_space_size}"
            ),
            ExistingStrategyType.MEDIUM_FINITE: StrategyTypeMapping(
                comment_type=CommentStrategyType.MEDIUM_FINITE,
                rationale_template="adequate finite coverage"
            ),
            ExistingStrategyType.COMBINATION: StrategyTypeMapping(
                comment_type=CommentStrategyType.COMBINATION,
                rationale_template="combination coverage"
            ),
            ExistingStrategyType.COMPLEX: StrategyTypeMapping(
                comment_type=CommentStrategyType.COMPLEX,
                rationale_template="adequate coverage"
            )
        }
    
    def classify_strategy_for_comments(self, strategy_code: str) -> 'CommentStrategyClassification':
        """Classify strategy and return comment-format classification.
        
        Args:
            strategy_code: String containing Hypothesis strategy definition
            
        Returns:
            CommentStrategyClassification with type and rationale information
        """
        # Use existing classifier to get base analysis
        existing_analysis = self.existing_classifier.classify_strategy(strategy_code)
        
        # Map to comment format terminology
        mapping = self.type_mapping[existing_analysis.strategy_type]
        
        # Generate appropriate rationale
        if existing_analysis.strategy_type == ExistingStrategyType.SMALL_FINITE:
            if existing_analysis.input_space_size is not None:
                rationale = f"input space size: {existing_analysis.input_space_size}"
            else:
                rationale = "finite coverage"
        elif existing_analysis.strategy_type == ExistingStrategyType.COMPLEX:
            # Check if this is a performance-optimized case
            if self._is_performance_optimized(strategy_code):
                rationale = "performance optimized"
            else:
                rationale = mapping.rationale_template
        else:
            rationale = mapping.rationale_template
        
        return CommentStrategyClassification(
            strategy_type=mapping.comment_type,
            rationale=rationale,
            input_space_size=existing_analysis.input_space_size,
            complexity_level=existing_analysis.complexity_level,
            components=existing_analysis.components or []
        )
    
    def detect_strategy_from_test_code(self, test_code: str) -> Optional['CommentStrategyClassification']:
        """Detect strategy type from complete test function code.
        
        Args:
            test_code: Complete test function source code
            
        Returns:
            CommentStrategyClassification if strategy detected, None otherwise
        """
        # Extract @given decorator and its strategy
        strategy_code = self._extract_given_strategy(test_code)
        if not strategy_code:
            return None
        
        return self.classify_strategy_for_comments(strategy_code)
    
    def handle_edge_cases(self, strategy_code: str) -> Optional['CommentStrategyClassification']:
        """Handle edge cases and complex strategy combinations.
        
        Args:
            strategy_code: Strategy code that may contain edge cases
            
        Returns:
            CommentStrategyClassification for edge cases, None if standard classification applies
        """
        # Check for CI-specific optimizations
        if self._is_ci_optimized(strategy_code):
            base_classification = self.classify_strategy_for_comments(strategy_code)
            base_classification.rationale = f"CI optimized: {base_classification.rationale}"
            return base_classification
        
        # Check for custom domain strategies
        if self._is_custom_domain_strategy(strategy_code):
            return CommentStrategyClassification(
                strategy_type=CommentStrategyType.COMPLEX,
                rationale="custom domain strategy",
                input_space_size=None,
                complexity_level=2,
                components=[strategy_code]
            )
        
        # Check for nested tuple combinations
        if self._is_nested_combination(strategy_code):
            return CommentStrategyClassification(
                strategy_type=CommentStrategyType.COMBINATION,
                rationale="nested combination coverage",
                input_space_size=None,
                complexity_level=3,
                components=self._extract_nested_components(strategy_code)
            )
        
        return None  # Use standard classification
    
    def _extract_given_strategy(self, test_code: str) -> Optional[str]:
        """Extract strategy code from @given decorator in test function."""
        # Look for @given decorator with proper parentheses matching
        start_idx = test_code.find('@given(')
        if start_idx == -1:
            return None
        
        # Find the matching closing parenthesis
        start_paren = start_idx + len('@given(')
        paren_count = 1
        end_idx = start_paren
        
        while end_idx < len(test_code) and paren_count > 0:
            if test_code[end_idx] == '(':
                paren_count += 1
            elif test_code[end_idx] == ')':
                paren_count -= 1
            end_idx += 1
        
        if paren_count != 0:
            return None  # Unmatched parentheses
        
        strategy_code = test_code[start_paren:end_idx-1]
        return strategy_code.strip()
    
    def _is_performance_optimized(self, strategy_code: str) -> bool:
        """Check if strategy appears to be performance-optimized."""
        # Look for indicators of performance optimization
        performance_indicators = [
            'deadline=None',
            'max_examples=2',
            'max_examples=5',
            'max_examples=10'
        ]
        
        return any(indicator in strategy_code for indicator in performance_indicators)
    
    def _is_ci_optimized(self, strategy_code: str) -> bool:
        """Check if strategy uses CI-specific optimizations."""
        # Look for CI environment checks
        ci_patterns = [
            r"os\.getenv\(['\"]CI['\"]\)",
            r"if.*CI.*else",
            r"CI.*\?.*:"
        ]
        
        return any(re.search(pattern, strategy_code) for pattern in ci_patterns)
    
    def _is_custom_domain_strategy(self, strategy_code: str) -> bool:
        """Check if strategy uses custom domain-specific generators."""
        custom_indicators = [
            'markdown_',
            'html_',
            'css_',
            'custom_',
            'domain_'
        ]
        
        return any(indicator in strategy_code.lower() for indicator in custom_indicators)
    
    def _is_nested_combination(self, strategy_code: str) -> bool:
        """Check if strategy contains nested tuple or composite combinations."""
        # Look for nested st.tuples or multiple levels of composition
        nested_patterns = [
            r'st\.tuples\([^)]*st\.tuples',
            r'st\.composite\([^)]*st\.composite',
            r'st\.one_of\([^)]*st\.one_of'
        ]
        
        return any(re.search(pattern, strategy_code) for pattern in nested_patterns)
    
    def _extract_nested_components(self, strategy_code: str) -> List[str]:
        """Extract components from nested strategy combinations."""
        # Simple extraction of top-level strategy calls
        components = re.findall(r'st\.\w+\([^)]*\)', strategy_code)
        return components[:5]  # Limit to avoid excessive detail


@dataclass
class CommentStrategyClassification:
    """Classification result for comment format generation."""
    strategy_type: CommentStrategyType
    rationale: str
    input_space_size: Optional[int] = None
    complexity_level: int = 1
    components: List[str] = None
    
    def __post_init__(self):
        if self.components is None:
            self.components = []


class TestCodeAnalyzer:
    """Analyzes test code to extract strategy information for comment generation."""
    
    def __init__(self):
        """Initialize analyzer with strategy mapper."""
        self.mapper = StrategyTypeMapper()
    
    def analyze_test_function(self, test_code: str) -> Optional[CommentStrategyClassification]:
        """Analyze complete test function and return strategy classification.
        
        Args:
            test_code: Complete test function source code
            
        Returns:
            CommentStrategyClassification if analysis successful, None otherwise
        """
        # First check for edge cases
        edge_case_result = self.mapper.handle_edge_cases(test_code)
        if edge_case_result:
            return edge_case_result
        
        # Use standard classification
        return self.mapper.detect_strategy_from_test_code(test_code)
    
    def extract_max_examples_from_settings(self, test_code: str) -> Optional[int]:
        """Extract max_examples value from @settings decorator.
        
        Args:
            test_code: Test function source code
            
        Returns:
            max_examples value if found, None otherwise
        """
        settings_pattern = re.compile(r'@settings\([^)]*max_examples\s*=\s*(\d+)', re.DOTALL)
        match = settings_pattern.search(test_code)
        
        if match:
            return int(match.group(1))
        
        return None
    
    def extract_function_name(self, test_code: str) -> Optional[str]:
        """Extract test function name from code.
        
        Args:
            test_code: Test function source code
            
        Returns:
            Function name if found, None otherwise
        """
        func_pattern = re.compile(r'def\s+(test_\w+)\s*\(')
        match = func_pattern.search(test_code)
        
        if match:
            return match.group(1)
        
        return None