#!/usr/bin/env python3
"""
Split flake8 output into separate files, one for each source file.

This script reads flake8_output.txt and creates individual files containing
only the issues for each specific Python file.
"""

import os
from collections import defaultdict
from pathlib import Path


def parse_flake8_line(line):
    """
    Parse a flake8 output line and extract the filename.
    
    Args:
        line: A line from flake8 output
        
    Returns:
        tuple: (filename, full_line) or (None, None) if parsing fails
    """
    if not line.strip() or ':' not in line:
        return None, None
    
    # Split on the first colon to get the filename
    parts = line.split(':', 1)
    if len(parts) < 2:
        return None, None
    
    filename = parts[0]
    return filename, line


def split_flake8_output(input_file, output_dir='flake8_split'):
    """
    Split flake8 output into separate files.
    
    Args:
        input_file: Path to the flake8 output file
        output_dir: Directory to save the split files (default: flake8_split)
    """
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Dictionary to store lines by filename
    files_issues = defaultdict(list)
    
    # Read and parse the input file
    print(f"Reading {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            filename, full_line = parse_flake8_line(line)
            if filename:
                files_issues[filename].append(full_line)
    
    # Write each file's issues to a separate file
    print(f"Writing {len(files_issues)} files...")
    for filename, issues in sorted(files_issues.items()):
        # Create a safe filename by replacing path separators
        safe_filename = filename.replace('/', '_').replace('\\', '_')
        output_file = output_path / f"{safe_filename}.txt"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(issues)
        
        print(f"  {safe_filename}.txt: {len(issues)} issues")
    
    print(f"\nDone! Files saved to {output_dir}/")
    print(f"Total files with issues: {len(files_issues)}")
    total_issues = sum(len(issues) for issues in files_issues.values())
    print(f"Total issues: {total_issues}")


if __name__ == '__main__':
    input_file = 'flake8_output.txt'
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found!")
        exit(1)
    
    split_flake8_output(input_file)
