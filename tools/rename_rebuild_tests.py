#!/usr/bin/env python3
"""
Script to rename tests that claim to test rebuilds but only test value changes.

This script identifies tests with "triggers_rebuild" in their name but that don't
actually verify rebuilds occurred, and renames them to use "updates_value" instead.
"""

import re
import os
from pathlib import Path


def has_rebuild_verification(test_content):
    """Check if test content actually verifies that a rebuild occurred."""
    # Look for patterns that indicate rebuild verification
    rebuild_patterns = [
        r'collect_widget_ids',
        r'widget.*id.*!=',
        r'id\s*\(\s*\w+\s*\)\s*!=',
        r'children_ids.*!=',
        r'assert.*rebuild',
        r'widget.*identity',
        r'widget.*instance',
    ]
    
    for pattern in rebuild_patterns:
        if re.search(pattern, test_content, re.IGNORECASE):
            return True
    return False


def extract_test_method(file_content, method_name):
    """Extract the content of a specific test method."""
    # Find the method definition
    method_pattern = rf'def\s+{re.escape(method_name)}\s*\([^)]*\):'
    match = re.search(method_pattern, file_content)
    if not match:
        return None
    
    start_pos = match.start()
    lines = file_content[:start_pos].count('\n')
    
    # Find the end of the method (next method or class definition, or end of file)
    remaining_content = file_content[start_pos:]
    
    # Split into lines and find where this method ends
    method_lines = remaining_content.split('\n')
    method_content = [method_lines[0]]  # Include the def line
    
    # Find the indentation level of the method
    method_indent = len(method_lines[0]) - len(method_lines[0].lstrip())
    
    for i, line in enumerate(method_lines[1:], 1):
        # If we hit a line with same or less indentation that starts with def/class, we're done
        if line.strip() and not line.startswith(' ' * (method_indent + 1)):
            if line.lstrip().startswith(('def ', 'class ', '@')):
                break
        method_content.append(line)
    
    return '\n'.join(method_content)


def rename_test_in_file(file_path, old_name, new_name):
    """Rename a test method in a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace the method definition
        pattern = rf'def\s+{re.escape(old_name)}\s*\('
        replacement = f'def {new_name}('
        new_content = re.sub(pattern, replacement, content)
        
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Renamed {old_name} -> {new_name} in {file_path}")
            return True
        else:
            print(f"Warning: Could not find {old_name} in {file_path}")
            return False
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False


def find_rebuild_test_mismatches(test_dir):
    """Find tests that claim to test rebuilds but don't verify them."""
    mismatches = []
    test_dir = Path(test_dir)
    
    for test_file in test_dir.glob('test_*.py'):
        if not test_file.is_file():
            continue
            
        try:
            with open(test_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find all test methods with "triggers_rebuild" in the name
            rebuild_test_pattern = r'def\s+(test_\w*triggers_rebuild\w*)\s*\('
            matches = re.finditer(rebuild_test_pattern, content)
            
            for match in matches:
                method_name = match.group(1)
                method_content = extract_test_method(content, method_name)
                
                if method_content and not has_rebuild_verification(method_content):
                    # Generate new name by replacing "triggers_rebuild" with "updates_value"
                    new_name = method_name.replace('triggers_rebuild', 'updates_value')
                    new_name = new_name.replace('_rebuilds_', '_updates_')
                    
                    mismatches.append({
                        'file': str(test_file),
                        'old_name': method_name,
                        'new_name': new_name,
                        'method_content': method_content
                    })
                    
        except Exception as e:
            print(f"Warning: Failed to process {test_file}: {e}")
    
    return mismatches


def main():
    """Main function to find and rename mismatched rebuild tests."""
    test_dir = 'kivy_garden/markdownlabel/tests'
    
    print("Finding tests that claim to test rebuilds but don't verify them...")
    mismatches = find_rebuild_test_mismatches(test_dir)
    
    if not mismatches:
        print("No mismatched rebuild tests found.")
        return
    
    print(f"Found {len(mismatches)} tests that need renaming:")
    
    # Show a few examples
    for i, mismatch in enumerate(mismatches[:5]):
        print(f"  {i+1}. {mismatch['old_name']} -> {mismatch['new_name']} in {mismatch['file']}")
    
    if len(mismatches) > 5:
        print(f"  ... and {len(mismatches) - 5} more")
    
    # Ask for confirmation
    response = input(f"\nRename these {len(mismatches)} tests? (y/n): ")
    if response.lower() != 'y':
        print("Aborted.")
        return
    
    # Perform the renames
    success_count = 0
    for mismatch in mismatches:
        if rename_test_in_file(mismatch['file'], mismatch['old_name'], mismatch['new_name']):
            success_count += 1
    
    print(f"\nSuccessfully renamed {success_count} out of {len(mismatches)} tests.")


if __name__ == "__main__":
    main()