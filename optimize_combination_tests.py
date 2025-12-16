#!/usr/bin/env python3
"""
Optimize combination strategy tests by applying product formula.

This script identifies tests using multiple strategies (tuples or multiple @given arguments)
and updates their max_examples to use the combination formula (product of individual sizes, capped at 50).
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
from kivy_garden.markdownlabel.strategy_classifier import StrategyClassifier
from kivy_garden.markdownlabel.max_examples_calculator import MaxExamplesCalculator


def backup_files(test_dir):
    """Create backup of test files before modification."""
    backup_dir = f"optimization_backups/backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(backup_dir, exist_ok=True)
    
    for test_file in Path(test_dir).glob('test_*.py'):
        shutil.copy2(test_file, backup_dir)
    
    print(f"Created backup in {backup_dir}")
    return backup_dir


def find_combination_tests(test_dir):
    """Find all tests using combination strategies."""
    classifier = StrategyClassifier()
    calculator = MaxExamplesCalculator(classifier)
    combination_tests = []
    
    for test_file in Path(test_dir).glob('test_*.py'):
        with open(test_file, 'r') as f:
            content = f.read()
        
        lines = content.split('\n')
        
        # Find @given decorators with combination patterns
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
                
                # Check if this is a combination strategy
                strategy_match = re.search(r'@given\((.*)\)', given_decorator, re.DOTALL)
                if strategy_match:
                    strategy_code = strategy_match.group(1).strip()
                    
                    # Classify the strategy
                    analysis = classifier.classify_strategy(strategy_code)
                    
                    if analysis.strategy_type.value == 'combination':
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
                                combination_tests.append({
                                    'file': str(test_file),
                                    'function': func_name,
                                    'line_num': settings_line_num + 1,  # 1-based
                                    'strategy_code': strategy_code,
                                    'current_examples': current_max_examples,
                                    'optimal_examples': optimal_examples,
                                    'input_space_size': analysis.input_space_size,
                                    'components': analysis.components,
                                    'settings_line': lines[settings_line_num]
                                })
                
                i = j + 1
            else:
                i += 1
    
    return combination_tests


def optimize_combination_test(test_info):
    """Optimize a single combination test."""
    file_path = test_info['file']
    line_num = test_info['line_num'] - 1  # Convert to 0-based
    current_examples = test_info['current_examples']
    optimal_examples = test_info['optimal_examples']
    
    # Read the file
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    # Update the @settings line
    old_line = lines[line_num]
    new_line = re.sub(
        r'max_examples\s*=\s*\d+',
        f'max_examples={optimal_examples}',
        old_line
    )
    
    lines[line_num] = new_line
    
    # Write back to file
    with open(file_path, 'w') as f:
        f.writelines(lines)
    
    print(f"✓ {test_info['function']}: {current_examples} → {optimal_examples} examples")
    
    # Calculate time savings
    time_savings = (current_examples - optimal_examples) / current_examples * 100
    return time_savings


def main():
    """Main optimization function."""
    test_dir = 'kivy_garden/markdownlabel/tests'
    
    print("=== COMBINATION STRATEGY OPTIMIZATION ===")
    print()
    
    # Create backup
    backup_dir = backup_files(test_dir)
    
    # Find combination tests
    print("Scanning for combination strategy tests...")
    combination_tests = find_combination_tests(test_dir)
    
    if not combination_tests:
        print("No combination strategy tests found that need optimization.")
        return
    
    print(f"Found {len(combination_tests)} combination tests to optimize:")
    print()
    
    total_time_savings = 0
    total_examples_before = 0
    total_examples_after = 0
    
    for test in combination_tests:
        print(f"📁 {test['file']}")
        print(f"   Function: {test['function']}")
        print(f"   Strategy: {test['strategy_code'][:80]}{'...' if len(test['strategy_code']) > 80 else ''}")
        print(f"   Components: {len(test['components'])} strategies")
        if test['input_space_size']:
            print(f"   Input space size: {test['input_space_size']}")
        print(f"   Current max_examples: {test['current_examples']}")
        print(f"   Optimal max_examples: {test['optimal_examples']}")
        
        time_savings = optimize_combination_test(test)
        total_time_savings += time_savings
        total_examples_before += test['current_examples']
        total_examples_after += test['optimal_examples']
        
        print(f"   Time savings: {time_savings:.1f}%")
        print()
    
    # Summary
    print("=== OPTIMIZATION SUMMARY ===")
    print(f"Optimized {len(combination_tests)} combination strategy tests")
    print(f"Total examples before: {total_examples_before}")
    print(f"Total examples after: {total_examples_after}")
    print(f"Examples reduced by: {total_examples_before - total_examples_after}")
    print(f"Average time savings: {total_time_savings / len(combination_tests):.1f}%")
    print(f"Backup created in: {backup_dir}")


if __name__ == '__main__':
    main()