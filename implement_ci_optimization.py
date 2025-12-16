#!/usr/bin/env python3
"""
Implement CI environment optimization for property-based tests.

This script adds CI detection and reduced max_examples for appropriate tests,
ensuring finite strategies maintain full coverage while allowing complex strategies
to use reduced examples in CI environments.
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


def find_ci_optimizable_tests(test_dir):
    """Find tests that can benefit from CI optimization."""
    classifier = StrategyClassifier()
    calculator = MaxExamplesCalculator(classifier)
    ci_tests = []
    
    for test_file in Path(test_dir).glob('test_*.py'):
        with open(test_file, 'r') as f:
            content = f.read()
        
        lines = content.split('\n')
        
        # Find @given decorators
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
                
                # Check strategy type
                strategy_match = re.search(r'@given\((.*)\)', given_decorator, re.DOTALL)
                if strategy_match:
                    strategy_code = strategy_match.group(1).strip()
                    
                    # Classify the strategy
                    analysis = classifier.classify_strategy(strategy_code)
                    
                    # Only complex and large combination strategies benefit from CI optimization
                    if (analysis.strategy_type == StrategyType.COMPLEX or 
                        (analysis.strategy_type == StrategyType.COMBINATION and 
                         analysis.input_space_size and analysis.input_space_size > 20)):
                        
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
                            # Calculate CI-optimized examples
                            base_examples = calculator.calculate_from_analysis(analysis)
                            
                            # Simulate CI environment for calculation
                            os.environ['CI'] = '1'
                            ci_examples = calculator.calculate_from_analysis(analysis)
                            if 'CI' in os.environ:
                                del os.environ['CI']
                            
                            if ci_examples < base_examples:
                                ci_tests.append({
                                    'file': str(test_file),
                                    'function': func_name,
                                    'line_num': settings_line_num + 1,  # 1-based
                                    'strategy_code': strategy_code,
                                    'strategy_type': analysis.strategy_type,
                                    'current_examples': current_max_examples,
                                    'base_examples': base_examples,
                                    'ci_examples': ci_examples,
                                    'settings_line': lines[settings_line_num]
                                })
                
                i = j + 1
            else:
                i += 1
    
    return ci_tests


def add_ci_optimization(test_info):
    """Add CI optimization to a test."""
    file_path = test_info['file']
    line_num = test_info['line_num'] - 1  # Convert to 0-based
    base_examples = test_info['base_examples']
    ci_examples = test_info['ci_examples']
    strategy_type = test_info['strategy_type']
    
    # Read the file
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    # Check if CI optimization is already present
    settings_line = lines[line_num]
    if 'os.getenv(' in settings_line or 'CI' in settings_line:
        print(f"⚠️  {test_info['function']}: CI optimization already present")
        return 0
    
    # Generate CI-aware max_examples expression
    if strategy_type == StrategyType.COMPLEX:
        ci_expression = f"max_examples={base_examples} if not os.getenv('CI') else {ci_examples}"
    else:  # Large combination
        ci_expression = f"max_examples={base_examples} if not os.getenv('CI') else {ci_examples}"
    
    # Update the @settings line
    new_line = re.sub(
        r'max_examples\s*=\s*\d+',
        ci_expression,
        settings_line
    )
    
    lines[line_num] = new_line
    
    # Add import for os at the top of the file if not present
    has_os_import = any('import os' in line for line in lines[:20])
    if not has_os_import:
        # Find the first import line and add os import after it
        for i, line in enumerate(lines):
            if line.strip().startswith('import ') or line.strip().startswith('from '):
                lines.insert(i + 1, 'import os\n')
                break
        else:
            # No imports found, add at the beginning
            lines.insert(0, 'import os\n')
    
    # Write back to file
    with open(file_path, 'w') as f:
        f.writelines(lines)
    
    print(f"✓ {test_info['function']}: Added CI optimization ({base_examples} → {ci_examples} in CI)")
    
    # Calculate potential CI time savings
    ci_time_savings = (base_examples - ci_examples) / base_examples * 100
    return ci_time_savings


def main():
    """Main CI optimization function."""
    test_dir = 'kivy_garden/markdownlabel/tests'
    
    print("=== CI ENVIRONMENT OPTIMIZATION ===")
    print()
    
    # Create backup
    backup_dir = backup_files(test_dir)
    
    # Find CI-optimizable tests
    print("Scanning for CI-optimizable tests...")
    ci_tests = find_ci_optimizable_tests(test_dir)
    
    if not ci_tests:
        print("No tests found that would benefit from CI optimization.")
        return
    
    print(f"Found {len(ci_tests)} tests that can benefit from CI optimization:")
    print()
    
    total_ci_savings = 0
    total_base_examples = 0
    total_ci_examples = 0
    
    for test in ci_tests:
        print(f"📁 {test['file']}")
        print(f"   Function: {test['function']}")
        print(f"   Strategy type: {test['strategy_type'].value}")
        print(f"   Current max_examples: {test['current_examples']}")
        print(f"   Base max_examples: {test['base_examples']}")
        print(f"   CI max_examples: {test['ci_examples']}")
        
        ci_savings = add_ci_optimization(test)
        total_ci_savings += ci_savings
        total_base_examples += test['base_examples']
        total_ci_examples += test['ci_examples']
        
        print(f"   CI time savings: {ci_savings:.1f}%")
        print()
    
    # Summary
    print("=== CI OPTIMIZATION SUMMARY ===")
    print(f"Added CI optimization to {len(ci_tests)} tests")
    print(f"Base examples (local): {total_base_examples}")
    print(f"CI examples: {total_ci_examples}")
    print(f"CI examples reduction: {total_base_examples - total_ci_examples}")
    print(f"Average CI time savings: {total_ci_savings / len(ci_tests):.1f}%")
    print()
    print("CI Optimization Rules:")
    print("- Finite strategies (boolean, small ranges) maintain full coverage in CI")
    print("- Complex strategies use reduced examples in CI for faster feedback")
    print("- Large combination strategies (>20 examples) are reduced in CI")
    print(f"Backup created in: {backup_dir}")


if __name__ == '__main__':
    main()