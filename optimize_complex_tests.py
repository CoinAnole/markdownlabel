#!/usr/bin/env python3
"""
Optimize complex strategy tests by assessing complexity and setting appropriate max_examples.

This script identifies tests using infinite or large strategies (text, large floats, etc.)
and sets appropriate max_examples (10-50) based on complexity assessment.
"""

import re
import os
import shutil
from pathlib import Path
from datetime import datetime

# Add the package to path
import sys
sys.path.append('kivy_garden/markdownlabel')

# Import with absolute imports to avoid relative import issues
from kivy_garden.markdownlabel.strategy_classifier import StrategyClassifier, StrategyType
from kivy_garden.markdownlabel.max_examples_calculator import MaxExamplesCalculator


def backup_files(test_dir):
    """Create backup of test files before modification."""
    backup_dir = f"optimization_backups/backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(backup_dir, exist_ok=True)
    
    for test_file in Path(test_dir).glob('test_*.py'):
        shutil.copy2(test_file, backup_dir)
    
    print(f"Created backup in {backup_dir}")
    return backup_dir


def find_complex_tests(test_dir):
    """Find all tests using complex strategies."""
    classifier = StrategyClassifier()
    calculator = MaxExamplesCalculator(classifier)
    complex_tests = []
    
    for test_file in Path(test_dir).glob('test_*.py'):
        with open(test_file, 'r') as f:
            content = f.read()
        
        lines = content.split('\n')
        
        # Find @given decorators with complex patterns
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            if line.startswith('@given('):
                # Extract the full @given decorator (may span multiple lines)
                given_lines = []
                paren_count = 0
                j = i
                
                while j < len(lines):
                    current_line = lines[j].strip()
                    given_lines.append(current_line)
                    paren_count += current_line.count('(') - current_line.count(')')
                    
                    if paren_count == 0:
                        break
                    j += 1
                
                given_decorator = ' '.join(given_lines)
                
                # Check if this is a complex strategy
                strategy_match = re.search(r'@given\((.*)\)', given_decorator, re.DOTALL)
                if strategy_match:
                    strategy_code = strategy_match.group(1).strip()
                    
                    # Classify the strategy
                    analysis = classifier.classify_strategy(strategy_code)
                    
                    if analysis.strategy_type == StrategyType.COMPLEX:
                        # Look for @settings decorator
                        settings_line_num = None
                        current_max_examples = None
                        
                        for k in range(j + 1, min(j + 4, len(lines))):
                            settings_line = lines[k].strip()
                            if settings_line.startswith('@settings('):
                                settings_match = re.search(r'max_examples\s*=\s*(\d+)', settings_line)
                                if settings_match:
                                    current_max_examples = int(settings_match.group(1))
                                    settings_line_num = k
                                    break
                        
                        # Look for function name
                        func_name = None
                        for k in range(j + 1, min(j + 5, len(lines))):
                            func_line = lines[k].strip()
                            if func_line.startswith('def test_'):
                                func_match = re.search(r'def\s+(test_\w+)', func_line)
                                if func_match:
                                    func_name = func_match.group(1)
                                    break
                        
                        if current_max_examples and func_name:
                            optimal_examples = calculator.calculate_from_analysis(analysis)
                            
                            if current_max_examples > optimal_examples:
                                complexity_assessment = assess_strategy_complexity(strategy_code)
                                
                                complex_tests.append({
                                    'file': str(test_file),
                                    'function': func_name,
                                    'line_num': settings_line_num + 1,  # 1-based
                                    'strategy_code': strategy_code,
                                    'current_examples': current_max_examples,
                                    'optimal_examples': optimal_examples,
                                    'complexity_level': analysis.complexity_level,
                                    'complexity_assessment': complexity_assessment,
                                    'settings_line': lines[settings_line_num]
                                })
                
                i = j + 1
            else:
                i += 1
    
    return complex_tests


def assess_strategy_complexity(strategy_code):
    """Assess the complexity of a strategy and provide rationale."""
    complexity_factors = []
    
    # Text strategies
    if 'st.text(' in strategy_code:
        complexity_factors.append("text generation")
        if 'min_size=' in strategy_code and 'max_size=' in strategy_code:
            # Extract size limits
            min_match = re.search(r'min_size\s*=\s*(\d+)', strategy_code)
            max_match = re.search(r'max_size\s*=\s*(\d+)', strategy_code)
            if min_match and max_match:
                min_size = int(min_match.group(1))
                max_size = int(max_match.group(1))
                if max_size > 100:
                    complexity_factors.append("large text size")
        
        if 'alphabet=' in strategy_code:
            complexity_factors.append("custom alphabet")
    
    # Float strategies
    if 'st.floats(' in strategy_code:
        complexity_factors.append("float generation")
        if 'allow_nan=False' in strategy_code:
            complexity_factors.append("NaN exclusion")
        if 'allow_infinity=False' in strategy_code:
            complexity_factors.append("infinity exclusion")
    
    # List strategies
    if 'st.lists(' in strategy_code:
        complexity_factors.append("list generation")
        if 'min_size=' in strategy_code and 'max_size=' in strategy_code:
            complexity_factors.append("variable list size")
    
    # One_of strategies
    if 'st.one_of(' in strategy_code:
        complexity_factors.append("union of strategies")
    
    # Custom strategies
    if any(custom in strategy_code for custom in ['simple_markdown_document', 'markdown_with_']):
        complexity_factors.append("custom domain strategy")
    
    return complexity_factors


def generate_complexity_comment(complexity_assessment, optimal_examples):
    """Generate a comment explaining the complexity assessment."""
    if not complexity_assessment:
        return f"# Complex strategy: {optimal_examples} examples based on default complexity"
    
    factors_str = ", ".join(complexity_assessment)
    return f"# Complex strategy with {factors_str}: {optimal_examples} examples"


def optimize_complex_test(test_info):
    """Optimize a single complex test."""
    file_path = test_info['file']
    line_num = test_info['line_num'] - 1  # Convert to 0-based
    current_examples = test_info['current_examples']
    optimal_examples = test_info['optimal_examples']
    complexity_assessment = test_info['complexity_assessment']
    
    # Read the file
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    # Generate complexity comment
    complexity_comment = generate_complexity_comment(complexity_assessment, optimal_examples)
    
    # Update the @settings line
    old_line = lines[line_num]
    new_line = re.sub(
        r'max_examples\s*=\s*\d+',
        f'max_examples={optimal_examples}',
        old_line
    )
    
    # Add complexity comment above the @settings line if it doesn't already exist
    comment_line_num = line_num - 1
    if comment_line_num >= 0 and not lines[comment_line_num].strip().startswith('#'):
        # Insert comment line
        indent = len(old_line) - len(old_line.lstrip())
        comment_with_indent = ' ' * indent + complexity_comment + '\n'
        lines.insert(line_num, comment_with_indent)
        line_num += 1  # Adjust for inserted line
    
    lines[line_num] = new_line
    
    # Write back to file
    with open(file_path, 'w') as f:
        f.writelines(lines)
    
    print(f"✓ {test_info['function']}: {current_examples} → {optimal_examples} examples")
    print(f"  Complexity: {', '.join(complexity_assessment) if complexity_assessment else 'default'}")
    
    # Calculate time savings
    time_savings = (current_examples - optimal_examples) / current_examples * 100
    return time_savings


def main():
    """Main optimization function."""
    test_dir = 'kivy_garden/markdownlabel/tests'
    
    print("=== COMPLEX STRATEGY OPTIMIZATION ===")
    print()
    
    # Create backup
    backup_dir = backup_files(test_dir)
    
    # Find complex tests
    print("Scanning for complex strategy tests...")
    complex_tests = find_complex_tests(test_dir)
    
    if not complex_tests:
        print("No complex strategy tests found that need optimization.")
        return
    
    print(f"Found {len(complex_tests)} complex tests to optimize:")
    print()
    
    total_time_savings = 0
    total_examples_before = 0
    total_examples_after = 0
    
    for test in complex_tests:
        print(f"📁 {test['file']}")
        print(f"   Function: {test['function']}")
        print(f"   Strategy: {test['strategy_code'][:80]}{'...' if len(test['strategy_code']) > 80 else ''}")
        print(f"   Complexity level: {test['complexity_level']}")
        print(f"   Current max_examples: {test['current_examples']}")
        print(f"   Optimal max_examples: {test['optimal_examples']}")
        
        time_savings = optimize_complex_test(test)
        total_time_savings += time_savings
        total_examples_before += test['current_examples']
        total_examples_after += test['optimal_examples']
        
        print(f"   Time savings: {time_savings:.1f}%")
        print()
    
    # Summary
    print("=== OPTIMIZATION SUMMARY ===")
    print(f"Optimized {len(complex_tests)} complex strategy tests")
    print(f"Total examples before: {total_examples_before}")
    print(f"Total examples after: {total_examples_after}")
    print(f"Examples reduced by: {total_examples_before - total_examples_after}")
    print(f"Average time savings: {total_time_savings / len(complex_tests):.1f}%")
    print(f"Backup created in: {backup_dir}")


if __name__ == '__main__':
    main()