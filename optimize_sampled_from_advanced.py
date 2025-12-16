#!/usr/bin/env python3
"""
Advanced script to optimize sampled_from tests, including those in fixed_dictionaries.
"""

import re
import os
from pathlib import Path

def find_sampled_from_in_line(line):
    """Find sampled_from patterns in a line and return their sizes."""
    # Pattern for st.sampled_from([...])
    pattern = r'st\.sampled_from\(\[(.*?)\]\)'
    matches = re.findall(pattern, line)
    
    sizes = []
    for match in matches:
        if match.strip():
            # Count items by splitting on comma and filtering non-empty
            items = [item.strip() for item in match.split(',') if item.strip()]
            sizes.append(len(items))
    
    return sizes

def optimize_sampled_from_tests_in_file(file_path):
    """Optimize sampled_from tests in a single file."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    lines = content.split('\n')
    changes_made = 0
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Check if this line contains @given with st.sampled_from()
        if '@given(' in line and 'st.sampled_from(' in line:
            # Look for sampled_from patterns in this line and next few lines
            strategy_lines = [line]
            j = i + 1
            
            # Collect the full @given statement (may span multiple lines)
            paren_count = line.count('(') - line.count(')')
            while j < len(lines) and paren_count > 0:
                strategy_lines.append(lines[j])
                paren_count += lines[j].count('(') - lines[j].count(')')
                j += 1
            
            # Analyze all sampled_from patterns in the strategy
            all_sizes = []
            for strategy_line in strategy_lines:
                sizes = find_sampled_from_in_line(strategy_line)
                all_sizes.extend(sizes)
            
            # If we found small sampled_from lists (≤10 items each)
            if all_sizes and all(size <= 10 for size in all_sizes):
                # Calculate optimal max_examples
                if len(all_sizes) == 1:
                    # Single sampled_from: use list size
                    optimal_examples = all_sizes[0]
                else:
                    # Multiple sampled_from: use product (capped at 50)
                    optimal_examples = 1
                    for size in all_sizes:
                        optimal_examples *= size
                    optimal_examples = min(optimal_examples, 50)
                
                # Look for @settings in the next few lines
                for k in range(j, min(j + 5, len(lines))):
                    settings_line = lines[k].strip()
                    if '@settings(' in settings_line and 'max_examples=' in settings_line:
                        # Check if it's max_examples=100 or other high values
                        current_match = re.search(r'max_examples\s*=\s*(\d+)', settings_line)
                        if current_match:
                            current_examples = int(current_match.group(1))
                            if current_examples > optimal_examples:
                                # Replace with the optimal value
                                new_line = re.sub(r'max_examples\s*=\s*\d+', f'max_examples={optimal_examples}', settings_line)
                                if new_line != settings_line:
                                    lines[k] = lines[k].replace(settings_line, new_line)
                                    changes_made += 1
                                    print(f"  Changed line {k+1}: max_examples {current_examples} -> {optimal_examples} (sampled_from optimization)")
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
    """Main function to optimize all sampled_from tests."""
    test_files = [
        "kivy_garden/markdownlabel/tests/test_shortening_and_coordinate.py",
        "kivy_garden/markdownlabel/tests/test_rtl_alignment.py",
        "kivy_garden/markdownlabel/tests/test_text_properties.py"
    ]
    
    total_changes = 0
    
    for file_path in test_files:
        if os.path.exists(file_path):
            print(f"\nProcessing {file_path}...")
            changes = optimize_sampled_from_tests_in_file(file_path)
            total_changes += changes
        else:
            print(f"File not found: {file_path}")
    
    print(f"\nTotal changes made: {total_changes}")

if __name__ == "__main__":
    main()