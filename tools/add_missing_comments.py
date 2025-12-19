#!/usr/bin/env python3
"""
Add missing comments to tests that have no documentation at all.
"""

import os
import re
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.test_optimization.comment_analyzer import CommentAnalyzer


_always_document = os.getenv("ALWAYS_DOCUMENT_MAX_EXAMPLES", "").lower() in {"1", "true", "yes", "on"}
# Standard values that historically were exempt; honor env to force documentation
STANDARD_VALUES = set() if _always_document else {2, 3, 4, 5, 6, 7, 8, 9, 10, 100}

# Files to skip (test fixtures)
SKIP_FILES = {
    'test_comment_format.py',
    'test_file_analyzer.py', 
    'test_comment_standardizer.py',
    'test_documentation_compliance.py',
}


def get_strategy_type_and_rationale(max_examples):
    """Determine strategy type and rationale based on max_examples value."""
    if max_examples == 2:
        return "Boolean", "True/False coverage"
    if max_examples <= 10:
        return "Small finite", f"input space size: {max_examples}"
    if max_examples <= 50:
        return "Medium finite", "adequate finite coverage"
    return "Complex", "adequate coverage"


def add_comment_to_file(filepath, line_num, max_examples):
    """Add a standardized comment before the @settings line."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Find the @settings line (line_num is 1-based)
    settings_line_idx = line_num - 1
    
    # Look backwards to find where to insert the comment
    # We want to insert before @settings but after @given
    insert_idx = settings_line_idx
    
    # Check if there's already a comment
    for i in range(max(0, settings_line_idx - 3), settings_line_idx):
        line = lines[i].strip()
        if line.startswith('#') and ('strategy' in line.lower() or 'examples' in line.lower()):
            # Already has a comment
            return False
    
    # Get indentation from the @settings line
    settings_line = lines[settings_line_idx]
    indent = len(settings_line) - len(settings_line.lstrip())
    indent_str = ' ' * indent
    
    # Generate comment
    strategy_type, rationale = get_strategy_type_and_rationale(max_examples)
    comment = f"{indent_str}# {strategy_type} strategy: {max_examples} examples ({rationale})\n"
    
    # Insert the comment
    lines.insert(insert_idx, comment)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    return True


def main():
    default_dir = Path(__file__).parent.parent / 'kivy_garden' / 'markdownlabel' / 'tests'
    test_dir = os.getenv("TEST_DIR", str(default_dir.resolve()))

    analyzer = CommentAnalyzer()
    analysis = analyzer.analyze_directory(test_dir)
    
    total_added = 0
    
    for file_analysis in analysis.file_analyses:
        filename = file_analysis.file_path.split('/')[-1]
        if filename in SKIP_FILES:
            continue
        
        if not file_analysis.missing_documentation:
            continue
        
        # Sort by line number in reverse order so we don't mess up line numbers
        missing_docs = sorted(file_analysis.missing_documentation, 
                             key=lambda x: x[1], reverse=True)
        
        for func_name, line_num, max_examples in missing_docs:
            # Skip standard values
            if max_examples in STANDARD_VALUES:
                continue
            
            if add_comment_to_file(file_analysis.file_path, line_num, max_examples):
                print(f"Added comment to {file_analysis.file_path}:{line_num} ({func_name})")
                total_added += 1
    
    print(f"\nTotal comments added: {total_added}")


if __name__ == '__main__':
    main()
