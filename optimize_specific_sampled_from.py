#!/usr/bin/env python3
"""
Targeted script to optimize specific sampled_from tests.
"""

import re
import os

def optimize_file(file_path):
    """Optimize sampled_from tests in a specific file."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Pattern 1: st.sampled_from([[1, 0, 0, 1], [0, 1, 0, 1], [0, 0, 1, 1]]) - 3 items
    # This appears in fixed_dictionaries with max_examples=100
    pattern1 = r"(st\.sampled_from\(\[\[1, 0, 0, 1\], \[0, 1, 0, 1\], \[0, 0, 1, 1\]\]\).*?@settings\(max_examples=)100"
    content = re.sub(pattern1, r"\g<1>3", content, flags=re.DOTALL)
    
    # Pattern 2: st.sampled_from(['left', 'center', 'right']) - 3 items
    pattern2 = r"(st\.sampled_from\(\['left', 'center', 'right'\].*?@settings\(max_examples=)100"
    content = re.sub(pattern2, r"\g<1>3", content, flags=re.DOTALL)
    
    # Pattern 3: st.sampled_from(['top', 'middle', 'bottom']) - 3 items  
    pattern3 = r"(st\.sampled_from\(\['top', 'middle', 'bottom'\].*?@settings\(max_examples=)100"
    content = re.sub(pattern3, r"\g<1>3", content, flags=re.DOTALL)
    
    # Pattern 4: st.sampled_from([None, 'ltr', 'rtl', 'weak_ltr', 'weak_rtl']) - 5 items
    pattern4 = r"(st\.sampled_from\(\[None, 'ltr', 'rtl', 'weak_ltr', 'weak_rtl'\].*?@settings\(max_examples=)100"
    content = re.sub(pattern4, r"\g<1>5", content, flags=re.DOTALL)
    
    # Pattern 5: st.sampled_from(['rtl', 'weak_rtl']) - 2 items
    pattern5 = r"(st\.sampled_from\(\['rtl', 'weak_rtl'\].*?@settings\(max_examples=)100"
    content = re.sub(pattern5, r"\g<1>2", content, flags=re.DOTALL)
    
    # Pattern 6: st.sampled_from(['ltr', 'weak_ltr', None]) - 3 items
    pattern6 = r"(st\.sampled_from\(\['ltr', 'weak_ltr', None\].*?@settings\(max_examples=)100"
    content = re.sub(pattern6, r"\g<1>3", content, flags=re.DOTALL)
    
    with open(file_path, 'w') as f:
        f.write(content)
    
    print(f"Processed {file_path}")

def main():
    """Main function."""
    files_to_process = [
        "kivy_garden/markdownlabel/tests/test_shortening_and_coordinate.py",
        "kivy_garden/markdownlabel/tests/test_rtl_alignment.py", 
        "kivy_garden/markdownlabel/tests/test_text_properties.py"
    ]
    
    for file_path in files_to_process:
        if os.path.exists(file_path):
            optimize_file(file_path)
        else:
            print(f"File not found: {file_path}")

if __name__ == "__main__":
    main()