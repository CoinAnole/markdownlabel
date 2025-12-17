#!/usr/bin/env python3
"""
Add missing documentation comments to property-based tests.

This script adds standardized documentation comments to tests that have
max_examples values but no documentation comment.
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple, Optional


# Files to skip - these contain intentional test fixtures
SKIP_FILES = {
    'test_documentation_compliance.py',
    'test_comment_format.py',
    'test_file_analyzer.py',
    'test_comment_standardizer.py',
}

# Standard values that don't need documentation
# These match the values in comment_analyzer.py
STANDARD_VALUES = {2, 5, 10, 20, 50, 100}


def get_strategy_type_from_context(lines: List[str], settings_idx: int) -> str:
    """Determine strategy type from surrounding code context."""
    # Look at the @given decorator and surrounding code
    search_start = max(0, settings_idx - 10)
    search_end = min(len(lines), settings_idx + 5)
    context = '\n'.join(lines[search_start:search_end]).lower()
    
    # Check for boolean strategies
    if 'st.booleans()' in context or 'booleans()' in context:
        return 'Boolean'
    
    # Check for small finite strategies
    if 'st.sampled_from' in context or 'sampled_from' in context:
        return 'Small finite'
    
    # Check for combination strategies
    if 'st.tuples' in context or 'st.one_of' in context:
        return 'Combination'
    
    # Default to Complex for most strategies
    return 'Complex'


def get_rationale(strategy_type: str, max_examples: int) -> str:
    """Get the appropriate rationale for a strategy type."""
    if strategy_type == 'Boolean':
        return 'True/False coverage'
    elif strategy_type == 'Small finite':
        return f'input space size: {max_examples}'
    elif strategy_type == 'Combination':
        return 'combination coverage'
    else:
        return 'adequate coverage'


def find_undocumented_tests(file_path: Path) -> List[Tuple[int, int, str]]:
    """Find tests with max_examples but no documentation comment.
    
    Returns:
        List of (line_number, max_examples, strategy_type) tuples
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    undocumented = []
    
    for i, line in enumerate(lines):
        # Look for @settings with max_examples
        settings_match = re.search(r'@settings\([^)]*max_examples\s*=\s*(\d+)', line)
        if settings_match:
            max_examples = int(settings_match.group(1))
            
            # Skip standard values
            if max_examples in STANDARD_VALUES:
                continue
            
            # Check if there's already a documentation comment
            has_comment = False
            for j in range(max(0, i - 3), i):
                prev_line = lines[j].strip()
                if prev_line.startswith('#') and 'strategy' in prev_line.lower():
                    has_comment = True
                    break
            
            if not has_comment:
                strategy_type = get_strategy_type_from_context(lines, i)
                undocumented.append((i, max_examples, strategy_type))
    
    return undocumented


def add_documentation_comments(file_path: Path, dry_run: bool = True) -> int:
    """Add documentation comments to undocumented tests.
    
    Returns:
        Number of comments added
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    undocumented = find_undocumented_tests(file_path)
    
    if not undocumented:
        return 0
    
    # Sort by line number in reverse order so we can insert without affecting indices
    undocumented.sort(key=lambda x: x[0], reverse=True)
    
    for line_idx, max_examples, strategy_type in undocumented:
        rationale = get_rationale(strategy_type, max_examples)
        comment = f"    # {strategy_type} strategy: {max_examples} examples ({rationale})\n"
        
        # Insert the comment before the @settings line
        lines.insert(line_idx, comment)
    
    if not dry_run:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
    
    return len(undocumented)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Add missing documentation comments to property-based tests'
    )
    parser.add_argument('path', help='File or directory to process')
    parser.add_argument('--apply', action='store_true',
                        help='Apply changes (default is dry-run)')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Show detailed changes')
    
    args = parser.parse_args()
    
    dry_run = not args.apply
    
    if dry_run:
        print("=== DRY RUN MODE (use --apply to make changes) ===\n")
    else:
        print("=== APPLYING CHANGES ===\n")
    
    path = Path(args.path)
    
    if path.is_file():
        files = [path]
    else:
        files = list(path.glob('**/test_*.py'))
    
    total_added = 0
    files_changed = 0
    
    for filepath in sorted(files):
        if filepath.name in SKIP_FILES:
            continue
        
        undocumented = find_undocumented_tests(filepath)
        
        if undocumented:
            files_changed += 1
            count = add_documentation_comments(filepath, dry_run=dry_run)
            total_added += count
            
            print(f"\n{filepath}: {count} comments to add")
            
            if args.verbose:
                for line_idx, max_examples, strategy_type in undocumented:
                    rationale = get_rationale(strategy_type, max_examples)
                    print(f"  Line {line_idx + 1}: # {strategy_type} strategy: {max_examples} examples ({rationale})")
    
    print(f"\n=== SUMMARY ===")
    print(f"Files processed: {len(files)}")
    print(f"Files with changes: {files_changed}")
    print(f"Total comments to add: {total_added}")
    
    if dry_run and total_added > 0:
        print(f"\nRun with --apply to make these changes")


if __name__ == '__main__':
    main()
