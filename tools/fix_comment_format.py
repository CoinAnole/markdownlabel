#!/usr/bin/env python3
"""
Conservative comment format fixer for property-based tests.

This script only fixes comments that are very close to the standard format,
specifically targeting the rationale part that doesn't match expected patterns.
"""

import re
import sys
import os
from pathlib import Path


# Standard format: # [Strategy Type] strategy: [N] examples ([Rationale])
# The issue is comments have things like "based on default complexity" instead of "(adequate coverage)"

# Pattern to match existing comments that are close to standard format
CLOSE_TO_STANDARD_PATTERN = re.compile(
    r'^(\s*)#\s*(Boolean|Small finite|Medium finite|Complex|Combination|Custom)\s+strategy:\s*(\d+)\s+examples\s*(.*)$',
    re.IGNORECASE
)

# Valid rationale patterns (these should NOT be changed)
VALID_RATIONALE_PATTERNS = [
    r'\(True/False coverage\)',
    r'\(boolean coverage\)',
    r'\(input space size:?\s*\d*\)',
    r'\(finite coverage\)',
    r'\(adequate finite coverage\)',
    r'\(adequate coverage\)',
    r'\(performance optimized\)',
    r'\(complexity coverage\)',
    r'\(combination coverage\)',
    r'\(product coverage\)',
]

# Mapping of strategy types to their standard rationale
STANDARD_RATIONALES = {
    'boolean': '(True/False coverage)',
    'small finite': '(finite coverage)',
    'medium finite': '(adequate finite coverage)',
    'complex': '(adequate coverage)',
    'combination': '(combination coverage)',
    'custom': '(adequate coverage)',  # Treat custom as complex
}


def is_valid_rationale(rationale: str) -> bool:
    """Check if a rationale matches one of the valid patterns."""
    for pattern in VALID_RATIONALE_PATTERNS:
        if re.match(pattern, rationale, re.IGNORECASE):
            return True
    return False


def fix_comment_line(line: str) -> tuple[str, bool]:
    """
    Fix a single comment line if it's close to standard format.
    
    Returns:
        Tuple of (fixed_line, was_changed)
    """
    match = CLOSE_TO_STANDARD_PATTERN.match(line)
    if not match:
        return line, False
    
    indent = match.group(1)
    strategy_type = match.group(2)
    max_examples = match.group(3)
    current_rationale = match.group(4).strip()
    
    # Check if already has a valid rationale - don't change it
    if is_valid_rationale(current_rationale):
        # Only change if strategy type needs normalization (Custom -> Complex)
        if strategy_type.lower() == 'custom':
            fixed_line = f"{indent}# Complex strategy: {max_examples} examples {current_rationale}"
            return fixed_line, True
        return line, False
    
    # Normalize strategy type
    strategy_key = strategy_type.lower()
    if strategy_key == 'custom':
        strategy_type = 'Complex'  # Normalize "Custom" to "Complex"
        strategy_key = 'complex'
    
    # Get standard rationale
    standard_rationale = STANDARD_RATIONALES.get(strategy_key, '(adequate coverage)')
    
    # Build the fixed line
    fixed_line = f"{indent}# {strategy_type} strategy: {max_examples} examples {standard_rationale}"
    return fixed_line, True


def process_file(filepath: str, dry_run: bool = True) -> dict:
    """
    Process a single file and fix comment formats.
    
    Returns:
        Dict with statistics about changes made
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    changes = []
    new_lines = []
    
    for i, line in enumerate(lines):
        fixed_line, was_changed = fix_comment_line(line.rstrip('\n'))
        new_lines.append(fixed_line + '\n')
        
        if was_changed:
            changes.append({
                'line_number': i + 1,
                'original': line.rstrip('\n'),
                'fixed': fixed_line
            })
    
    if not dry_run and changes:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
    
    return {
        'filepath': filepath,
        'total_lines': len(lines),
        'changes': changes,
        'num_changes': len(changes)
    }


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Fix comment formats in test files')
    parser.add_argument('path', help='File or directory to process')
    parser.add_argument('--apply', action='store_true', help='Apply changes (default is dry-run)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed changes')
    
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
    
    total_changes = 0
    files_changed = 0
    
    for filepath in sorted(files):
        result = process_file(str(filepath), dry_run=dry_run)
        
        if result['num_changes'] > 0:
            files_changed += 1
            total_changes += result['num_changes']
            
            print(f"\n{filepath}: {result['num_changes']} changes")
            
            if args.verbose:
                for change in result['changes']:
                    print(f"  Line {change['line_number']}:")
                    print(f"    - {change['original']}")
                    print(f"    + {change['fixed']}")
    
    print(f"\n=== SUMMARY ===")
    print(f"Files processed: {len(files)}")
    print(f"Files with changes: {files_changed}")
    print(f"Total changes: {total_changes}")
    
    if dry_run and total_changes > 0:
        print(f"\nRun with --apply to make these changes")


if __name__ == '__main__':
    main()
