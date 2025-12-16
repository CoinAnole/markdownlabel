#!/usr/bin/env python3
"""
Simple script to optimize boolean tests by changing max_examples=100 to max_examples=2
for tests that use st.booleans() strategy.
"""

import re
import os
from pathlib import Path

def optimize_boolean_tests_in_file(file_path):
    """Optimize boolean tests in a single file."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    original_content = content
    lines = content.split('\n')
    
    # Track changes
    changes_made = 0
    
    # Look for patterns where we have @given(st.booleans()) followed by @settings(max_examples=100)
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Check if this line contains @given with st.booleans()
        if '@given(' in line and 'st.booleans()' in line:
            # Look for @settings in the next few lines
            for j in range(i + 1, min(i + 5, len(lines))):
                settings_line = lines[j].strip()
                if '@settings(' in settings_line and 'max_examples=' in settings_line:
                    # Check if it's max_examples=100 (or other high values)
                    if re.search(r'max_examples\s*=\s*(100|[5-9]\d)', settings_line):
                        # Replace with max_examples=2
                        new_line = re.sub(r'max_examples\s*=\s*\d+', 'max_examples=2', settings_line)
                        if new_line != settings_line:
                            lines[j] = lines[j].replace(settings_line, new_line)
                            changes_made += 1
                            print(f"  Changed line {j+1}: {settings_line} -> {new_line}")
                    break
        
        # Also handle cases with multiple booleans like @given(st.booleans(), st.booleans())
        elif '@given(' in line and 'st.booleans()' in line and line.count('st.booleans()') >= 2:
            # Look for @settings in the next few lines
            for j in range(i + 1, min(i + 5, len(lines))):
                settings_line = lines[j].strip()
                if '@settings(' in settings_line and 'max_examples=' in settings_line:
                    # For two booleans, we want max_examples=4 (2*2)
                    bool_count = line.count('st.booleans()')
                    optimal_examples = 2 ** bool_count
                    
                    if re.search(r'max_examples\s*=\s*(100|[1-9]\d)', settings_line):
                        new_line = re.sub(r'max_examples\s*=\s*\d+', f'max_examples={optimal_examples}', settings_line)
                        if new_line != settings_line:
                            lines[j] = lines[j].replace(settings_line, new_line)
                            changes_made += 1
                            print(f"  Changed line {j+1}: {settings_line} -> {new_line}")
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
    """Main function to optimize all boolean tests."""
    test_files = [
        "kivy_garden/markdownlabel/tests/test_kivy_renderer.py",
        "kivy_garden/markdownlabel/tests/test_label_compatibility.py", 
        "kivy_garden/markdownlabel/tests/test_font_properties.py",
        "kivy_garden/markdownlabel/tests/test_sizing_behavior.py",
        "kivy_garden/markdownlabel/tests/test_text_properties.py",
        "kivy_garden/markdownlabel/tests/test_performance.py",
        "kivy_garden/markdownlabel/tests/test_shortening_and_coordinate.py",
        "kivy_garden/markdownlabel/tests/test_advanced_compatibility.py",
        "kivy_garden/markdownlabel/tests/test_strategy_classification.py"
    ]
    
    total_changes = 0
    
    for file_path in test_files:
        if os.path.exists(file_path):
            print(f"\nProcessing {file_path}...")
            changes = optimize_boolean_tests_in_file(file_path)
            total_changes += changes
        else:
            print(f"File not found: {file_path}")
    
    print(f"\nTotal changes made: {total_changes}")

if __name__ == "__main__":
    main()