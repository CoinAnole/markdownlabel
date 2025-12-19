#!/usr/bin/env python3
"""
Enhanced comment format fixer for property-based tests.

This script handles a wider variety of non-standard comment formats and
converts them to the standard format:
    # [Strategy Type] strategy: [N] examples ([Rationale])

Patterns handled:
1. "# Complex strategy with X: N examples" -> "# Complex strategy: N examples (adequate coverage)"
2. "# Float strategy with constraints: N examples" -> "# Complex strategy: N examples (adequate coverage)"
3. "# List strategy: N examples for X" -> "# Complex strategy: N examples (adequate coverage)"
4. "# X testing: N examples for Y" -> "# Complex strategy: N examples (adequate coverage)"
5. "# Complex strategy with custom domain strategy: N examples" -> "# Complex strategy: N examples (adequate coverage)"
"""

import re
import sys
from pathlib import Path
from typing import Tuple, Optional


# Standard format: # [Strategy Type] strategy: [N] examples ([Rationale])

# Valid strategy types (case-insensitive)
VALID_STRATEGY_TYPES = {'boolean', 'small finite', 'medium finite', 'complex', 'combination'}

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
    r'\(CI optimized\)',
]

# Mapping of strategy types to their standard rationale
STANDARD_RATIONALES = {
    'boolean': '(True/False coverage)',
    'small finite': '(finite coverage)',
    'medium finite': '(adequate finite coverage)',
    'complex': '(adequate coverage)',
    'combination': '(combination coverage)',
}

# Pattern 1: Already close to standard format but with wrong rationale
# e.g., "# Complex strategy: 50 examples based on default complexity"
CLOSE_TO_STANDARD = re.compile(
    r'^(\s*)#\s*(Boolean|Small finite|Medium finite|Complex|Combination|Custom)\s+strategy:\s*(\d+)\s+examples\s*(.*)$',
    re.IGNORECASE
)

# Pattern 2: Strategy type with extra description before colon
# e.g., "# Complex strategy with float generation, NaN exclusion: 50 examples"
STRATEGY_WITH_DESCRIPTION = re.compile(
    r'^(\s*)#\s*(Boolean|Complex|Combination|Float|List|Text|Integer|String)\s+(?:strategy\s+)?(?:with\s+[^:]+)?:\s*(\d+)\s+examples\s*(.*)$',
    re.IGNORECASE
)

# Pattern 3: Non-standard strategy type with examples
# e.g., "# Float strategy with constraints: 20 examples"
# e.g., "# List strategy: 20 examples for varied list sizes"
NONSTANDARD_STRATEGY = re.compile(
    r'^(\s*)#\s*(\w+(?:\s+\w+)*)\s+strategy(?:\s+with\s+[^:]+)?:\s*(\d+)\s+examples\s*(.*)$',
    re.IGNORECASE
)

# Pattern 4: Testing description with examples
# e.g., "# Clipping behavior testing: 20 examples for layout validation"
TESTING_DESCRIPTION = re.compile(
    r'^(\s*)#\s*[\w\s]+testing:\s*(\d+)\s+examples\s*(.*)$',
    re.IGNORECASE
)

# Pattern 5: Complex strategy with custom domain
# e.g., "# Complex strategy with custom domain strategy: 20 examples"
CUSTOM_DOMAIN = re.compile(
    r'^(\s*)#\s*Complex\s+strategy\s+with\s+custom\s+domain\s+strategy:\s*(\d+)\s+examples\s*(.*)$',
    re.IGNORECASE
)


def is_valid_rationale(rationale: str) -> bool:
    """Check if a rationale matches one of the valid patterns."""
    rationale = rationale.strip()
    for pattern in VALID_RATIONALE_PATTERNS:
        if re.match(pattern, rationale, re.IGNORECASE):
            return True
    return False


def map_to_standard_strategy(strategy_type: str) -> str:
    """Map non-standard strategy types to standard ones."""
    strategy_lower = strategy_type.lower().strip()
    
    # Direct mappings
    if strategy_lower in VALID_STRATEGY_TYPES:
        # Capitalize properly
        if strategy_lower == 'boolean':
            return 'Boolean'
        elif strategy_lower == 'small finite':
            return 'Small finite'
        elif strategy_lower == 'medium finite':
            return 'Medium finite'
        elif strategy_lower == 'complex':
            return 'Complex'
        elif strategy_lower == 'combination':
            return 'Combination'
    
    # Map non-standard types to Complex
    if strategy_lower in {'float', 'list', 'text', 'integer', 'string', 'custom'}:
        return 'Complex'
    
    # Default to Complex for unknown types
    return 'Complex'


def get_standard_rationale(strategy_type: str) -> str:
    """Get the standard rationale for a strategy type."""
    strategy_lower = strategy_type.lower().strip()
    return STANDARD_RATIONALES.get(strategy_lower, '(adequate coverage)')


def fix_comment_line(line: str) -> Tuple[str, bool]:
    """
    Fix a single comment line if it matches any non-standard pattern.
    
    Returns:
        Tuple of (fixed_line, was_changed)
    """
    original_line = line
    line_stripped = line.rstrip('\n')
    
    # Skip lines that don't look like strategy comments
    if '#' not in line or 'strategy' not in line.lower() and 'examples' not in line.lower():
        return original_line, False
    
    # Skip lines that are already in standard format with valid rationale
    match = CLOSE_TO_STANDARD.match(line_stripped)
    if match:
        indent, strategy_type, max_examples, rationale = match.groups()
        rationale = rationale.strip()
        
        # If already valid, don't change
        if is_valid_rationale(rationale):
            # Only normalize Custom -> Complex
            if strategy_type.lower() == 'custom':
                fixed = f"{indent}# Complex strategy: {max_examples} examples {rationale}"
                return fixed + '\n', True
            return original_line, False
        
        # Fix the rationale
        std_strategy = map_to_standard_strategy(strategy_type)
        std_rationale = get_standard_rationale(std_strategy)
        fixed = f"{indent}# {std_strategy} strategy: {max_examples} examples {std_rationale}"
        return fixed + '\n', True
    
    # Pattern 5: Custom domain strategy
    match = CUSTOM_DOMAIN.match(line_stripped)
    if match:
        indent, max_examples, _ = match.groups()
        fixed = f"{indent}# Complex strategy: {max_examples} examples (adequate coverage)"
        return fixed + '\n', True
    
    # Pattern 2: Strategy with description
    match = STRATEGY_WITH_DESCRIPTION.match(line_stripped)
    if match:
        indent, strategy_type, max_examples, rationale = match.groups()
        rationale = rationale.strip()
        
        if is_valid_rationale(rationale):
            std_strategy = map_to_standard_strategy(strategy_type)
            fixed = f"{indent}# {std_strategy} strategy: {max_examples} examples {rationale}"
            return fixed + '\n', True
        
        std_strategy = map_to_standard_strategy(strategy_type)
        std_rationale = get_standard_rationale(std_strategy)
        fixed = f"{indent}# {std_strategy} strategy: {max_examples} examples {std_rationale}"
        return fixed + '\n', True
    
    # Pattern 3: Non-standard strategy type
    match = NONSTANDARD_STRATEGY.match(line_stripped)
    if match:
        indent, strategy_type, max_examples, rationale = match.groups()
        rationale = rationale.strip()
        
        # Skip if it's a comment about strategy definition, not a test comment
        if 'for generating' in line.lower():
            return original_line, False
        
        std_strategy = map_to_standard_strategy(strategy_type)
        
        if is_valid_rationale(rationale):
            fixed = f"{indent}# {std_strategy} strategy: {max_examples} examples {rationale}"
            return fixed + '\n', True
        
        std_rationale = get_standard_rationale(std_strategy)
        fixed = f"{indent}# {std_strategy} strategy: {max_examples} examples {std_rationale}"
        return fixed + '\n', True
    
    # Pattern 4: Testing description
    match = TESTING_DESCRIPTION.match(line_stripped)
    if match:
        indent, max_examples, _ = match.groups()
        fixed = f"{indent}# Complex strategy: {max_examples} examples (adequate coverage)"
        return fixed + '\n', True
    
    return original_line, False


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
        fixed_line, was_changed = fix_comment_line(line)
        new_lines.append(fixed_line)
        
        if was_changed:
            changes.append({
                'line_number': i + 1,
                'original': line.rstrip('\n'),
                'fixed': fixed_line.rstrip('\n')
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
    
    parser = argparse.ArgumentParser(
        description='Enhanced comment format fixer for property-based tests'
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
