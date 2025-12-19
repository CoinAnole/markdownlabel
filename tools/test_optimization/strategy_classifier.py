"""Strategy classification system for Hypothesis test optimization.

This module provides tools to analyze Hypothesis strategies and classify them
by input space size and complexity for optimal max_examples calculation.
"""

import re
from enum import Enum
from dataclasses import dataclass
from typing import Optional, List, Dict, Any


class StrategyType(Enum):
    """Classification of Hypothesis strategies by input space characteristics."""
    BOOLEAN = "boolean"
    SMALL_FINITE = "small_finite"  # ≤10 values
    MEDIUM_FINITE = "medium_finite"  # 11-50 values
    COMBINATION = "combination"  # Multiple strategies
    COMPLEX = "complex"  # Infinite or large spaces


@dataclass
class StrategyAnalysis:
    """Analysis result for a Hypothesis strategy."""
    strategy_type: StrategyType
    input_space_size: Optional[int] = None
    complexity_level: int = 1
    components: List[str] = None
    
    def __post_init__(self):
        if self.components is None:
            self.components = []


class StrategyClassifier:
    """Classifies Hypothesis strategies by input space size and complexity."""
    
    def __init__(self):
        # Regex patterns for strategy detection
        self.boolean_pattern = re.compile(r'st\.booleans\(\)')
        self.integer_pattern = re.compile(r'st\.integers\(\s*min_value\s*=\s*(-?\d+)\s*,\s*max_value\s*=\s*(-?\d+)\s*\)')
        self.sampled_from_pattern = re.compile(r'st\.sampled_from\(\s*\[([^\]]*)\]\s*\)')
        self.text_pattern = re.compile(r'st\.text\(')
        self.floats_pattern = re.compile(r'st\.floats\(')
        self.tuples_pattern = re.compile(r'st\.tuples\(')
        
    def classify_strategy(self, strategy_code: str) -> StrategyAnalysis:
        """Analyze strategy code and return classification.

        Args:
            strategy_code: String containing Hypothesis strategy definition

        Returns:
            StrategyAnalysis with type, size, and complexity information
        """
        strategy_code = strategy_code.strip()

        # Check for combination strategies FIRST (multiple @given arguments)
        # This must come before individual strategy checks to avoid false positives
        if self._is_combination_strategy(strategy_code):
            components = self._extract_strategy_components(strategy_code)
            total_size = self._calculate_combination_size(components)

            return StrategyAnalysis(
                strategy_type=StrategyType.COMBINATION,
                input_space_size=total_size,
                components=components
            )

        # Check for tuple combinations
        if self.tuples_pattern.search(strategy_code):
            components = self._extract_tuple_components(strategy_code)
            if len(components) > 1:  # Only treat as combination if multiple components
                total_size = self._calculate_combination_size(components)

                return StrategyAnalysis(
                    strategy_type=StrategyType.COMBINATION,
                    input_space_size=total_size,
                    components=components
                )

        # Check for boolean strategies
        if self.boolean_pattern.search(strategy_code):
            return StrategyAnalysis(
                strategy_type=StrategyType.BOOLEAN,
                input_space_size=2,
                components=['st.booleans()']
            )

        # Check for integer range strategies
        integer_match = self.integer_pattern.search(strategy_code)
        if integer_match:
            min_val = int(integer_match.group(1))
            max_val = int(integer_match.group(2))
            size = max_val - min_val + 1

            # Treat 51-value ranges as finite (medium) instead of complex.
            if size <= 10:
                strategy_type = StrategyType.SMALL_FINITE
            elif size <= 51:
                strategy_type = StrategyType.MEDIUM_FINITE
            else:
                strategy_type = StrategyType.COMPLEX
                size = None  # Large ranges are effectively infinite

            return StrategyAnalysis(
                strategy_type=strategy_type,
                input_space_size=size,
                components=[f'st.integers(min_value={min_val}, max_value={max_val})']
            )

        # Check for sampled_from strategies
        sampled_match = self.sampled_from_pattern.search(strategy_code)
        if sampled_match:
            items_str = sampled_match.group(1)
            # Count items by splitting on commas (simple heuristic)
            items = [item.strip() for item in items_str.split(',') if item.strip()]
            size = len(items)

            if size <= 10:
                strategy_type = StrategyType.SMALL_FINITE
            elif size <= 50:
                strategy_type = StrategyType.MEDIUM_FINITE
            else:
                strategy_type = StrategyType.COMPLEX
                size = None

            return StrategyAnalysis(
                strategy_type=strategy_type,
                input_space_size=size,
                components=[f'st.sampled_from([{items_str}])']
            )

        # Default to complex for text, floats, and other infinite strategies
        complexity = self._assess_complexity(strategy_code)
        return StrategyAnalysis(
            strategy_type=StrategyType.COMPLEX,
            input_space_size=None,
            complexity_level=complexity,
            components=[strategy_code]
        )
    
    def calculate_input_space_size(self, strategy_code: str) -> Optional[int]:
        """Calculate the total number of possible values for a strategy.
        
        Args:
            strategy_code: String containing Hypothesis strategy definition
            
        Returns:
            Integer size for finite strategies, None for infinite strategies
        """
        analysis = self.classify_strategy(strategy_code)
        return analysis.input_space_size
    
    def _is_combination_strategy(self, strategy_code: str) -> bool:
        """Check if strategy code represents multiple combined strategies."""
        # Look for multiple strategy calls or tuple/composite patterns
        strategy_calls = len(re.findall(r'st\.\w+\(', strategy_code))
        return strategy_calls > 1
    
    def _extract_strategy_components(self, strategy_code: str) -> List[str]:
        """Extract individual strategy components from combination."""
        # Find all st.* calls
        components = re.findall(r'st\.\w+\([^)]*\)', strategy_code)
        return components
    
    def _calculate_combination_size(self, components: List[str]) -> Optional[int]:
        """Calculate product of component strategy sizes."""
        total_size = 1
        
        for component in components:
            # Use direct analysis to avoid recursion
            component_size = self._get_component_size(component)
            if component_size is None:
                return None  # If any component is infinite, combination is infinite
            total_size *= component_size
            
            # Cap at reasonable limit to prevent overflow
            if total_size > 1000:
                return None
        
        return total_size
    
    def _get_component_size(self, component: str) -> Optional[int]:
        """Get size of a single component without full classification."""
        component = component.strip()
        
        # Check for boolean
        if self.boolean_pattern.search(component):
            return 2
        
        # Check for integer range
        integer_match = self.integer_pattern.search(component)
        if integer_match:
            min_val = int(integer_match.group(1))
            max_val = int(integer_match.group(2))
            size = max_val - min_val + 1
            return size if size <= 50 else None
        
        # Check for sampled_from
        sampled_match = self.sampled_from_pattern.search(component)
        if sampled_match:
            items_str = sampled_match.group(1)
            items = [item.strip() for item in items_str.split(',') if item.strip()]
            size = len(items)
            return size if size <= 50 else None
        
        # For other strategies, assume infinite
        return None
    
    def _assess_complexity(self, strategy_code: str) -> int:
        """Assess complexity level for infinite/complex strategies."""
        complexity = 1
        
        # Text strategies are more complex
        if self.text_pattern.search(strategy_code):
            complexity += 1
            
        # Float strategies with constraints are moderately complex
        if self.floats_pattern.search(strategy_code):
            complexity += 1
            
        # Additional complexity indicators
        if 'allow_nan=False' in strategy_code:
            complexity += 1
        if 'allow_infinity=False' in strategy_code:
            complexity += 1
            
        return min(complexity, 4)  # Cap at level 4
    
    def _extract_tuple_components(self, strategy_code: str) -> List[str]:
        """Extract components from st.tuples() strategy."""
        # Find the content inside st.tuples(...) with proper parentheses matching
        start_idx = strategy_code.find('st.tuples(')
        if start_idx == -1:
            return []
        
        # Find the matching closing parenthesis
        start_paren = start_idx + len('st.tuples(')
        paren_count = 1
        end_idx = start_paren
        
        while end_idx < len(strategy_code) and paren_count > 0:
            if strategy_code[end_idx] == '(':
                paren_count += 1
            elif strategy_code[end_idx] == ')':
                paren_count -= 1
            end_idx += 1
        
        if paren_count != 0:
            return []  # Unmatched parentheses
        
        content = strategy_code[start_paren:end_idx-1]
        
        # Split by commas, but be careful about nested parentheses
        components = []
        paren_depth = 0
        current_component = ""
        
        for char in content:
            if char == '(':
                paren_depth += 1
            elif char == ')':
                paren_depth -= 1
            elif char == ',' and paren_depth == 0:
                if current_component.strip():
                    components.append(current_component.strip())
                current_component = ""
                continue
            
            current_component += char
        
        # Add the last component
        if current_component.strip():
            components.append(current_component.strip())
        
        return components