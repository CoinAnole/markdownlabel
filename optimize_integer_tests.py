#!/usr/bin/env python3
"""
Script to optimize small integer range tests by setting max_examples to the range size.
"""

import re
import os
from pathlib import Path

def calculate_range_size(strategy_code):
    """Calculate the size of an integer range from strategy code."""
    # Look for patterns like st.integers(min_value=X, max_value=Y)
    match = re.search(r'st\.integers\(.*?min_value\s*=\s*(\d+).*?max_value\s*=\s*(\d+)', strategy_code)
    if match:
        min_val = int(match.group(1))
        max_val = int(match.group(2))
        return max_val - min_val + 1
    return None

def optimize_integer_tests_in_file(file_path):
    """Optimize integer range tests in a single file."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    lines = content.split('\n')
    changes_made = 0
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Check if this line contains @given with st.integers() with small ranges
        if '@given(' in line and 'st.integers(' in line:
            # Extract the strategy code from this line and potentially next lines
            strategy_lines = [line]
            j = i + 1
            # Collect multi-line @given statements
            while j < len(lines) and (lines[j].strip().startswith('st.') or 
                                     lines[j].strip().endswith(',') or
                                     ')' not in lines[j]):
                strategy_lines.append(lines[j].strip())
                j += 1
                if j < len(lines) and ')' in lines[j]:
                    strategy_lines.append(lines[j].strip())
                    break
            
            strategy_code = ' '.join(strategy_lines)
            
            # Calculate range size for simple integer strategies
            range_size = calculate_range_size(strategy_code)
            
            # Only optimize small ranges (≤10 values)
            if range_size and range_size <= 10:
                # Look for @settings in the next few lines
                for k in range(i + 1, min(i + 8, len(lines))):
                    settings_line = lines[k].strip()
                    if '@settings(' in settings_line and 'max_examples=' in settings_line:
                        # Check if it's max_examples=100 or other high values
                        if re.search(r'max_examples\s*=\s*([5-9]\d|\d{3,})', settings_line):
                            # Replace with the range size
                            new_line = re.sub(r'max_examples\s*=\s*\d+', f'max_examples={range_size}', settings_line)
                            if new_line != settings_line:
                                lines[k] = lines[k].replace(settings_line, new_line)
                                changes_made += 1
                                print(f"  Changed line {k+1}: max_examples -> {range_size} (range size)")
                        break
        
        i += 1
    
    # Write back if changes were made
    if changes_made > 0:
        new_content = '\n'.join(lines)
        with open(file_path, 'w') as f:
            f.write(new_content)
        print(f"Made {changes_made} changes to {file_path}")
        return changes_made
    else:
        print(f"No changes needed in {file_path}")
        return 0

def main():
    """Main function to optimize all integer range tests."""
    test_files = [
        "kivy_garden/markdownlabel/tests/test_clipping_behavior.py",
        "kivy_garden/markdownlabel/tests/test_padding_properties.py",
        "kivy_garden/markdownlabel/tests/test_strategy_classification.py",
        "kivy_garden/markdownlabel/tests/test_rebuild_scheduling.py",
        "kivy_garden/markdownlabel/tests/test_core_functionality.py",
        "kivy_garden/markdownlabel/tests/test_shortening_and_coordinate.py"
    ]
    
    total_changes = 0
    
    for file_path in test_files:
        if os.path.exists(file_path):
            print(f"\nProcessing {file_path}...")
            changes = optimize_integer_tests_in_file(file_path)
            total_changes += changes
        else:
            print(f"File not found: {file_path}")
    
    print(f"\nTotal changes made: {total_changes}")

if __name__ == "__main__":
    main()