"""
Duplicate helper function detector for test suite analysis.

This module provides functionality to detect duplicate helper function
implementations across test files and generate consolidation reports.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict
import difflib
import ast

from test_file_parser import TestFileParser, HelperFunction, TestFileMetadata


@dataclass
class DuplicateGroup:
    """Represents a group of duplicate helper functions."""
    function_name: str
    body_hash: str
    functions: List[HelperFunction] = field(default_factory=list)
    similarity_score: float = 1.0  # 1.0 = identical, lower = similar
    consolidation_priority: int = 0  # Higher = more important to consolidate


@dataclass
class ConsolidationReport:
    """Report of duplicate functions and consolidation opportunities."""
    duplicate_groups: List[DuplicateGroup] = field(default_factory=list)
    total_duplicates: int = 0
    total_files_affected: int = 0
    consolidation_savings: int = 0  # Lines of code that could be saved
    
    def add_duplicate_group(self, group: DuplicateGroup):
        """Add a duplicate group to the report."""
        self.duplicate_groups.append(group)
        self.total_duplicates += len(group.functions)
        files = set(func.file_path for func in group.functions)
        self.total_files_affected += len(files)
        # Estimate savings: (number of duplicates - 1) * average function size
        if group.functions:
            avg_lines = 10  # Rough estimate for helper function size
            self.consolidation_savings += (len(group.functions) - 1) * avg_lines


class DuplicateDetector:
    """Detector for duplicate helper functions across test files."""
    
    def __init__(self, similarity_threshold: float = 0.8):
        """Initialize the duplicate detector.
        
        Args:
            similarity_threshold: Minimum similarity score to consider functions
                                as duplicates (0.0 to 1.0)
        """
        self.similarity_threshold = similarity_threshold
        self.parser = TestFileParser()
    
    def analyze_directory(self, directory_path: str) -> ConsolidationReport:
        """Analyze all test files in a directory for duplicate helpers.
        
        Args:
            directory_path: Path to directory containing test files
            
        Returns:
            ConsolidationReport with all detected duplicates
        """
        # Parse all test files
        file_metadata = self.parser.parse_directory(directory_path)
        
        # Extract all helper functions
        all_helpers = []
        for metadata in file_metadata.values():
            all_helpers.extend(metadata.helper_functions)
        
        # Group functions by name and detect duplicates
        report = ConsolidationReport()
        name_groups = self._group_by_name(all_helpers)
        
        for name, functions in name_groups.items():
            if len(functions) > 1:
                duplicate_groups = self._detect_duplicates_in_group(functions)
                for group in duplicate_groups:
                    group.consolidation_priority = self._calculate_priority(group)
                    report.add_duplicate_group(group)
        
        # Sort by priority (highest first)
        report.duplicate_groups.sort(key=lambda g: g.consolidation_priority, reverse=True)
        
        return report
    
    def _group_by_name(self, functions: List[HelperFunction]) -> Dict[str, List[HelperFunction]]:
        """Group helper functions by name."""
        groups = defaultdict(list)
        for func in functions:
            # Normalize names to catch variations like _find_labels_recursive vs find_labels_recursive
            normalized_name = func.name.lstrip('_')
            groups[normalized_name].append(func)
        return dict(groups)
    
    def _detect_duplicates_in_group(self, functions: List[HelperFunction]) -> List[DuplicateGroup]:
        """Detect duplicates within a group of same-named functions."""
        duplicate_groups = []
        processed = set()
        
        for i, func1 in enumerate(functions):
            if i in processed:
                continue
            
            # Start a new duplicate group
            group = DuplicateGroup(
                function_name=func1.name,
                body_hash=func1.body_hash,
                functions=[func1]
            )
            
            # Find all similar functions
            for j, func2 in enumerate(functions[i+1:], i+1):
                if j in processed:
                    continue
                
                similarity = self._calculate_similarity(func1, func2)
                if similarity >= self.similarity_threshold:
                    group.functions.append(func2)
                    processed.add(j)
            
            # Only add groups with actual duplicates
            if len(group.functions) > 1:
                group.similarity_score = self._calculate_group_similarity(group.functions)
                duplicate_groups.append(group)
            
            processed.add(i)
        
        return duplicate_groups
    
    def _calculate_similarity(self, func1: HelperFunction, func2: HelperFunction) -> float:
        """Calculate similarity between two helper functions."""
        # If body hashes are identical, they're the same
        if func1.body_hash == func2.body_hash:
            return 1.0
        
        # Check parameter similarity
        param_similarity = self._parameter_similarity(func1.parameters, func2.parameters)
        
        # For now, use a simple heuristic based on parameters and names
        # In a more sophisticated implementation, we could compare AST structures
        name_similarity = self._name_similarity(func1.name, func2.name)
        
        # Weighted average
        return (param_similarity * 0.6 + name_similarity * 0.4)
    
    def _parameter_similarity(self, params1: List[str], params2: List[str]) -> float:
        """Calculate similarity between parameter lists."""
        if not params1 and not params2:
            return 1.0
        
        if not params1 or not params2:
            return 0.0
        
        # Use sequence matching
        matcher = difflib.SequenceMatcher(None, params1, params2)
        return matcher.ratio()
    
    def _name_similarity(self, name1: str, name2: str) -> float:
        """Calculate similarity between function names."""
        # Normalize names (remove leading underscores)
        norm1 = name1.lstrip('_')
        norm2 = name2.lstrip('_')
        
        if norm1 == norm2:
            return 1.0
        
        # Use string similarity
        matcher = difflib.SequenceMatcher(None, norm1, norm2)
        return matcher.ratio()
    
    def _calculate_group_similarity(self, functions: List[HelperFunction]) -> float:
        """Calculate average similarity within a group of functions."""
        if len(functions) < 2:
            return 1.0
        
        total_similarity = 0.0
        comparisons = 0
        
        for i in range(len(functions)):
            for j in range(i + 1, len(functions)):
                total_similarity += self._calculate_similarity(functions[i], functions[j])
                comparisons += 1
        
        return total_similarity / comparisons if comparisons > 0 else 0.0
    
    def _calculate_priority(self, group: DuplicateGroup) -> int:
        """Calculate consolidation priority for a duplicate group."""
        # Higher priority for:
        # - More duplicates
        # - Higher similarity
        # - Functions used across more files
        
        num_duplicates = len(group.functions)
        similarity_bonus = int(group.similarity_score * 10)
        
        # Count unique files
        unique_files = len(set(func.file_path for func in group.functions))
        file_spread_bonus = unique_files * 2
        
        # Bonus for common helper patterns
        name_bonus = 0
        if any(pattern in group.function_name.lower() for pattern in 
               ['find_labels', 'recursive', 'collect', 'assert']):
            name_bonus = 5
        
        return num_duplicates * 10 + similarity_bonus + file_spread_bonus + name_bonus
    
    def generate_consolidation_suggestions(self, report: ConsolidationReport) -> List[str]:
        """Generate human-readable consolidation suggestions."""
        suggestions = []
        
        for group in report.duplicate_groups:
            files = [func.file_path for func in group.functions]
            unique_files = list(set(files))
            
            suggestion = f"""
Duplicate Function: {group.function_name}
- Found in {len(group.functions)} locations across {len(unique_files)} files
- Similarity Score: {group.similarity_score:.2f}
- Priority: {group.consolidation_priority}
- Files: {', '.join(unique_files)}
- Suggestion: Move to test_utils.py and update imports
"""
            suggestions.append(suggestion.strip())
        
        return suggestions
    
    def find_specific_duplicates(self, directory_path: str, function_name: str) -> List[HelperFunction]:
        """Find all instances of a specific helper function name.
        
        Args:
            directory_path: Path to directory containing test files
            function_name: Name of function to search for
            
        Returns:
            List of all helper functions with that name
        """
        file_metadata = self.parser.parse_directory(directory_path)
        
        matches = []
        for metadata in file_metadata.values():
            for helper in metadata.helper_functions:
                if (helper.name == function_name or 
                    helper.name.lstrip('_') == function_name.lstrip('_')):
                    matches.append(helper)
        
        return matches


def main():
    """Command-line interface for testing the duplicate detector."""
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python duplicate_detector.py <test_directory>")
        sys.exit(1)
    
    directory = sys.argv[1]
    detector = DuplicateDetector()
    
    print(f"Analyzing test files in {directory}...")
    report = detector.analyze_directory(directory)
    
    print(f"\nDuplicate Detection Report:")
    print(f"Total duplicate groups: {len(report.duplicate_groups)}")
    print(f"Total duplicate functions: {report.total_duplicates}")
    print(f"Files affected: {report.total_files_affected}")
    print(f"Estimated consolidation savings: {report.consolidation_savings} lines")
    
    print(f"\nConsolidation Suggestions:")
    suggestions = detector.generate_consolidation_suggestions(report)
    for suggestion in suggestions[:5]:  # Show top 5
        print(suggestion)
        print("-" * 50)


if __name__ == "__main__":
    main()