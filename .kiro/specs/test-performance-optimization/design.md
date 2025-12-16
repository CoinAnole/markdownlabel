# Design Document: Test Performance Optimization

## Overview

This design addresses the systematic over-use of `max_examples=100` in property-based tests throughout the MarkdownLabel test suite. Currently, 283 tests use this value regardless of input complexity, resulting in massive over-testing of finite input spaces and unnecessarily long test execution times.

The optimization focuses on right-sizing `max_examples` based on actual input space complexity:
- Boolean tests: 2 examples (test True and False once each)
- Small finite ranges: examples = input space size
- Complex infinite strategies: 10-50 examples based on complexity
- Combination strategies: product of individual spaces (capped at 50)

Expected outcomes:
- 50-95% reduction in test execution time
- Maintained or improved coverage quality
- Consistent patterns for future test development
- Automated validation to prevent regression

## Architecture

### Current Over-Testing Issues

```
Current State (283 tests)
├── Boolean tests: max_examples=100 → Testing True/False 50x each
├── Small integers (1-6): max_examples=100 → Testing 6 values ~17x each  
├── Small enums (3 items): max_examples=100 → Testing 3 values ~33x each
├── Two booleans: max_examples=100 → Testing 4 combinations 25x each
└── Complex strategies: max_examples=100 → May be appropriate or excessive

Time Impact
├── Boolean tests: 98% wasted time (2 examples needed, 100 used)
├── Small finite: 80-95% wasted time  
├── Medium finite: 50-80% wasted time
└── Complex strategies: 0-50% wasted time
```

### Optimized Architecture

```
Optimized Test Suite
├── Strategy Analysis Engine
│   ├── Input space size calculation
│   ├── Strategy type classification
│   └── Complexity assessment
├── max_examples Calculator
│   ├── Finite strategy: size = input space
│   ├── Boolean: size = 2
│   ├── Combination: size = product (capped at 50)
│   └── Complex: size = 10-50 based on complexity
├── Validation System
│   ├── Over-testing detection
│   ├── Pattern compliance checking
│   └── Performance impact analysis
└── CI Optimization
    ├── Environment-aware reduction
    ├── Critical path prioritization
    └── Time budget management
```

## Components and Interfaces

### 1. Strategy Classification System

Categorize Hypothesis strategies by input space complexity:

```python
class StrategyClassifier:
    """Classifies Hypothesis strategies by input space size and complexity."""
    
    def classify_strategy(self, strategy_code: str) -> StrategyType:
        """Analyze strategy code and return classification."""
        if 'st.booleans()' in strategy_code:
            return StrategyType.BOOLEAN
        elif 'st.integers(min_value=' in strategy_code:
            return self._classify_integer_range(strategy_code)
        elif 'st.sampled_from(' in strategy_code:
            return self._classify_sampled_from(strategy_code)
        elif multiple_strategies(strategy_code):
            return StrategyType.COMBINATION
        else:
            return StrategyType.COMPLEX
    
    def calculate_input_space_size(self, strategy_code: str) -> int:
        """Calculate the total number of possible values."""
        # Implementation details for each strategy type
```

### 2. max_examples Calculator

Calculate optimal `max_examples` based on strategy classification:

```python
class MaxExamplesCalculator:
    """Calculates optimal max_examples based on input space analysis."""
    
    COMPLEXITY_LIMITS = {
        StrategyType.BOOLEAN: 2,
        StrategyType.SMALL_FINITE: lambda size: size,
        StrategyType.MEDIUM_FINITE: lambda size: min(size, 20),
        StrategyType.COMBINATION: lambda size: min(size, 50),
        StrategyType.COMPLEX: lambda complexity: 10 + (complexity * 10)
    }
    
    def calculate_optimal_examples(self, strategy_type: StrategyType, 
                                 input_space_size: int = None,
                                 complexity_level: int = 1) -> int:
        """Calculate optimal max_examples for given strategy."""
        if strategy_type == StrategyType.BOOLEAN:
            return 2
        elif strategy_type in [StrategyType.SMALL_FINITE, StrategyType.MEDIUM_FINITE]:
            return min(input_space_size, 50)
        elif strategy_type == StrategyType.COMBINATION:
            return min(input_space_size, 50)
        else:  # COMPLEX
            return min(10 + (complexity_level * 10), 50)
```

### 3. Test File Analyzer

Scan test files and identify optimization opportunities:

```python
class TestFileAnalyzer:
    """Analyzes test files for max_examples optimization opportunities."""
    
    def analyze_file(self, file_path: str) -> FileAnalysis:
        """Analyze a test file and return optimization recommendations."""
        with open(file_path, 'r') as f:
            content = f.read()
        
        tests = self._extract_property_tests(content)
        recommendations = []
        
        for test in tests:
            current_max_examples = self._extract_max_examples(test)
            strategy_type = self.classifier.classify_strategy(test.strategy_code)
            optimal_examples = self.calculator.calculate_optimal_examples(strategy_type)
            
            if current_max_examples > optimal_examples:
                recommendations.append(OptimizationRecommendation(
                    test_name=test.name,
                    current_examples=current_max_examples,
                    recommended_examples=optimal_examples,
                    time_savings_percent=(current_max_examples - optimal_examples) / current_max_examples * 100
                ))
        
        return FileAnalysis(file_path, recommendations)
```

### 4. CI Environment Optimization

Support environment-aware `max_examples` reduction:

```python
def get_ci_optimized_examples(base_examples: int, strategy_type: StrategyType) -> int:
    """Get CI-optimized max_examples while maintaining coverage."""
    if not os.getenv('CI'):
        return base_examples
    
    # CI optimization rules
    if strategy_type == StrategyType.BOOLEAN:
        return 2  # Never reduce below minimum
    elif strategy_type in [StrategyType.SMALL_FINITE, StrategyType.MEDIUM_FINITE]:
        return base_examples  # Don't reduce finite strategies
    else:  # COMPLEX strategies can be reduced in CI
        return max(base_examples // 2, 5)  # Reduce by half, minimum 5
```

### 5. Validation and Reporting System

Automated detection of over-testing patterns:

```python
class OverTestingValidator:
    """Validates max_examples appropriateness and generates reports."""
    
    def validate_test_suite(self, test_directory: str) -> ValidationReport:
        """Validate entire test suite and generate optimization report."""
        report = ValidationReport()
        
        for test_file in self._find_test_files(test_directory):
            analysis = self.analyzer.analyze_file(test_file)
            report.add_file_analysis(analysis)
        
        # Calculate aggregate statistics
        report.total_over_tested = sum(len(a.recommendations) for a in report.file_analyses)
        report.potential_time_savings = self._calculate_time_savings(report)
        
        return report
    
    def generate_optimization_script(self, report: ValidationReport) -> str:
        """Generate script to apply all recommended optimizations."""
        # Generate sed/awk commands or Python script to update files
```

## Data Models

### Strategy Classification

```python
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional

class StrategyType(Enum):
    BOOLEAN = "boolean"
    SMALL_FINITE = "small_finite"  # ≤10 values
    MEDIUM_FINITE = "medium_finite"  # 11-50 values
    COMBINATION = "combination"  # Multiple strategies
    COMPLEX = "complex"  # Infinite or large spaces

@dataclass
class PropertyTest:
    name: str
    file_path: str
    line_number: int
    strategy_code: str
    current_max_examples: int
    strategy_type: StrategyType
    input_space_size: Optional[int] = None

@dataclass
class OptimizationRecommendation:
    test_name: str
    current_examples: int
    recommended_examples: int
    time_savings_percent: float
    rationale: str
```

### Validation Results

```python
@dataclass
class FileAnalysis:
    file_path: str
    recommendations: List[OptimizationRecommendation]
    total_tests: int
    over_tested_count: int
    potential_time_savings_percent: float

@dataclass
class ValidationReport:
    file_analyses: List[FileAnalysis]
    total_tests: int
    total_over_tested: int
    potential_time_savings_percent: float
    estimated_time_reduction_seconds: float
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Boolean tests use exactly 2 examples

*For any* property test using `st.booleans()` strategy, the test SHALL use `max_examples=2` to test both True and False exactly once.

**Validates: Requirements 1.1, 2.1**

### Property 2: Small finite strategies use input space size

*For any* property test using small finite strategies (≤10 possible values), the test SHALL use `max_examples` equal to the input space size to test each value exactly once.

**Validates: Requirements 1.2, 1.3, 2.2**

### Property 3: Combination strategies use product formula

*For any* property test using multiple finite strategies, the test SHALL use `max_examples` equal to the product of individual strategy sizes, capped at 50.

**Validates: Requirements 1.4, 2.4**

### Property 4: Complex strategies use appropriate ranges

*For any* property test using infinite or large strategies, the test SHALL use `max_examples` between 10-50 based on documented complexity levels.

**Validates: Requirements 1.5, 2.3**

### Property 5: CI environment reduces examples appropriately

*For any* property test in CI environment, the test MAY use reduced `max_examples` while maintaining minimum coverage requirements.

**Validates: Requirements 2.5, 3.5**

### Property 6: Custom values are documented

*For any* property test using custom `max_examples` values that deviate from standard patterns, the rationale SHALL be documented in test comments.

**Validates: Requirements 3.3**

### Property 7: Over-testing detection works correctly

*For any* property test with `max_examples` exceeding input space size, the validation system SHALL flag it as over-testing.

**Validates: Requirements 4.1, 4.2, 4.3**

### Property 8: Performance improvements are measurable

*For any* optimized test category, the execution time reduction SHALL be measurable and fall within expected ranges (50-98% depending on test type).

**Validates: Requirements 5.1, 5.2, 5.3, 5.4, 5.5**

## Error Handling

### Strategy Classification Failures

- Unknown strategy patterns: Default to conservative `max_examples=20`
- Parsing errors: Log warning and skip optimization for that test
- Complex nested strategies: Use heuristic-based classification

### File Modification Errors

- Backup original files before applying changes
- Validate syntax after modifications
- Rollback capability for failed optimizations
- Preserve existing comments and formatting

### CI Integration Issues

- Graceful fallback to original values if CI detection fails
- Environment variable validation
- Performance monitoring to detect regressions

## Testing Strategy

### Property-Based Testing Framework

Continue using **Hypothesis** for validation tests with appropriately sized `max_examples`.

### Test Configuration

- Validation tests: `max_examples=10` (testing the optimization system itself)
- Boolean validation: `max_examples=2` (testing boolean detection)
- Performance tests: `max_examples=5` (measuring time improvements)

### Test Annotation Format

Each property-based test MUST be annotated with:
```python
# **Feature: test-performance-optimization, Property {N}: {property_text}**
```

### Unit Tests

Unit tests cover specific examples and edge cases:
- Specific strategy patterns and their classifications
- Known over-testing cases and their corrections
- Performance measurement accuracy
- File modification safety

### Property-Based Tests

Property-based tests for the optimization system itself:

1. **Strategy classification accuracy**: Generate random strategy code, verify correct classification
2. **max_examples calculation**: Generate random input spaces, verify correct calculations
3. **File analysis correctness**: Generate test files, verify accurate analysis
4. **Optimization safety**: Verify optimizations don't break test functionality

### Performance Validation

Before and after performance measurements:
- Baseline test execution times
- Post-optimization execution times
- Verification of maintained test coverage
- Regression detection for edge cases

### Conversion Guidelines

1. **Analyze First**: Use validation system to identify all over-testing cases
2. **Batch Process**: Apply optimizations in groups by strategy type
3. **Verify Safety**: Run tests after each batch to ensure functionality preserved
4. **Measure Impact**: Document time savings and coverage maintenance
5. **Monitor Regression**: Set up CI checks to prevent future over-testing