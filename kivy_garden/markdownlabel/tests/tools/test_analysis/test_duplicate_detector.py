"""
Property-based tests for duplicate helper function detector.

This module contains property tests that validate the duplicate detector
correctly identifies duplicate helper functions across test files.
"""

import pytest
from hypothesis import given, strategies as st, settings, assume
import tempfile
import os
from pathlib import Path

from test_analysis.duplicate_detector import DuplicateDetector, DuplicateGroup, ConsolidationReport
# Import strategies from test_utils using absolute import
from kivy_garden.markdownlabel.tests.test_utils import duplicate_helper_functions


# **Feature: test-suite-refactoring, Property 3: Helper Function Consolidation**
# *For any* helper function that appears in multiple test files with identical
# or similar implementations, the function SHALL be defined once in `test_utils.py`
# and imported by other files.
# **Validates: Requirements 2.1, 2.2, 2.3**


@pytest.mark.test_tests
class TestHelperFunctionConsolidation:
    """Property tests for helper function consolidation (Property 3)."""
    
    @given(duplicate_helper_functions())
    # Complex strategy: 20 examples (adequate coverage)
    @settings(max_examples=20, deadline=None)
    def test_duplicate_detection_finds_duplicates(self, test_data):
        """Duplicate detector should find helper functions that appear in multiple files."""
        function_name, file_contents, should_be_identical = test_data
        
        # Create temporary test files
        temp_files = []
        temp_dir = tempfile.mkdtemp()
        
        try:
            for i, content in enumerate(file_contents):
                file_path = os.path.join(temp_dir, f"test_example_{i}.py")
                with open(file_path, 'w') as f:
                    f.write(content)
                temp_files.append(file_path)
            
            # Run duplicate detection
            detector = DuplicateDetector(similarity_threshold=0.7)
            report = detector.analyze_directory(temp_dir)
            
            # Property 3: Should detect duplicates when functions appear in multiple files
            if len(file_contents) > 1:
                # Should find at least one duplicate group
                assert len(report.duplicate_groups) >= 1, \
                    f"Expected to find duplicates for {function_name} in {len(file_contents)} files"
                
                # Find the group for our function
                target_group = None
                for group in report.duplicate_groups:
                    if function_name in group.function_name or group.function_name in function_name:
                        target_group = group
                        break
                
                if target_group:
                    # Should have found multiple instances
                    assert len(target_group.functions) >= 2, \
                        f"Expected multiple instances of {function_name}"
                    
                    # If they should be identical, similarity should be high
                    if should_be_identical:
                        assert target_group.similarity_score >= 0.9, \
                            f"Expected high similarity for identical functions: {target_group.similarity_score}"
        
        finally:
            # Clean up temporary files
            for file_path in temp_files:
                if os.path.exists(file_path):
                    os.unlink(file_path)
            os.rmdir(temp_dir)
    
    @given(st.integers(min_value=1, max_value=5))
    # Small finite strategy: 5 examples (input space size: 5)
    @settings(max_examples=5, deadline=None)
    def test_detector_handles_no_duplicates(self, num_files):
        """Detector should handle files with no duplicate functions correctly."""
        temp_files = []
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Create files with unique helper functions
            for i in range(num_files):
                content = f'''"""Test module {i}."""
import pytest

class TestUnique{i}:
    """Test class {i}."""
    
    def unique_helper_{i}(self):
        """Unique helper function {i}."""
        return {i}
    
    def test_example_{i}(self):
        """Example test."""
        assert self.unique_helper_{i}() == {i}
'''
                file_path = os.path.join(temp_dir, f"test_unique_{i}.py")
                with open(file_path, 'w') as f:
                    f.write(content)
                temp_files.append(file_path)
            
            # Run duplicate detection
            detector = DuplicateDetector()
            report = detector.analyze_directory(temp_dir)
            
            # Should find no duplicates
            assert len(report.duplicate_groups) == 0, \
                f"Expected no duplicates, but found {len(report.duplicate_groups)}"
            assert report.total_duplicates == 0
        
        finally:
            # Clean up
            for file_path in temp_files:
                if os.path.exists(file_path):
                    os.unlink(file_path)
            os.rmdir(temp_dir)
    
    def test_detector_calculates_priority_correctly(self):
        """Detector should assign higher priority to more important duplicates."""
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Create high-priority duplicate (common name, many files)
            high_priority_files = []
            for i in range(4):
                content = f'''"""Test module {i}."""
import pytest

class TestCommon{i}:
    """Test class {i}."""
    
    def find_labels_recursive(self, widget, labels=None):
        """Common helper function."""
        if labels is None:
            labels = []
        return labels
    
    def test_example_{i}(self):
        """Example test."""
        assert True
'''
                file_path = os.path.join(temp_dir, f"test_common_{i}.py")
                with open(file_path, 'w') as f:
                    f.write(content)
                high_priority_files.append(file_path)
            
            # Create low-priority duplicate (uncommon name, fewer files)
            low_priority_files = []
            for i in range(2):
                content = f'''"""Test module {i}."""
import pytest

class TestRare{i}:
    """Test class {i}."""
    
    def obscure_helper_function(self):
        """Rare helper function."""
        return True
    
    def test_example_{i}(self):
        """Example test."""
        assert True
'''
                file_path = os.path.join(temp_dir, f"test_rare_{i}.py")
                with open(file_path, 'w') as f:
                    f.write(content)
                low_priority_files.append(file_path)
            
            # Run duplicate detection
            detector = DuplicateDetector()
            report = detector.analyze_directory(temp_dir)
            
            # Should find both groups
            assert len(report.duplicate_groups) >= 2
            
            # High-priority group should have higher priority than low-priority group
            priorities = [group.consolidation_priority for group in report.duplicate_groups]
            assert max(priorities) > min(priorities), \
                "Expected different priority levels for different duplicate groups"
        
        finally:
            # Clean up
            all_files = high_priority_files + low_priority_files
            for file_path in all_files:
                if os.path.exists(file_path):
                    os.unlink(file_path)
            os.rmdir(temp_dir)
    
    def test_detector_generates_consolidation_suggestions(self):
        """Detector should generate actionable consolidation suggestions."""
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Create duplicate functions
            for i in range(3):
                content = f'''"""Test module {i}."""
import pytest

class TestDuplicate{i}:
    """Test class {i}."""
    
    def _find_labels_recursive(self, widget, labels=None):
        """Duplicate helper function."""
        if labels is None:
            labels = []
        return labels
    
    def test_example_{i}(self):
        """Example test."""
        assert True
'''
                file_path = os.path.join(temp_dir, f"test_duplicate_{i}.py")
                with open(file_path, 'w') as f:
                    f.write(content)
            
            # Run duplicate detection
            detector = DuplicateDetector()
            report = detector.analyze_directory(temp_dir)
            
            # Generate suggestions
            suggestions = detector.generate_consolidation_suggestions(report)
            
            # Should have suggestions
            assert len(suggestions) > 0, "Expected consolidation suggestions"
            
            # Suggestions should mention test_utils.py
            suggestion_text = '\n'.join(suggestions)
            assert 'test_utils.py' in suggestion_text, \
                "Suggestions should mention test_utils.py"
            
            # Should mention the duplicate function name
            assert '_find_labels_recursive' in suggestion_text, \
                "Suggestions should mention the duplicate function name"
        
        finally:
            # Clean up
            for i in range(3):
                file_path = os.path.join(temp_dir, f"test_duplicate_{i}.py")
                if os.path.exists(file_path):
                    os.unlink(file_path)
            os.rmdir(temp_dir)
    
    def test_detector_finds_specific_duplicates(self):
        """Detector should be able to find all instances of a specific function."""
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Create files with the target function
            target_function = "_find_labels_recursive"
            for i in range(3):
                content = f'''"""Test module {i}."""
import pytest

class TestTarget{i}:
    """Test class {i}."""
    
    def {target_function}(self, widget, labels=None):
        """Target helper function."""
        return []
    
    def other_function_{i}(self):
        """Other function."""
        return True
    
    def test_example_{i}(self):
        """Example test."""
        assert True
'''
                file_path = os.path.join(temp_dir, f"test_target_{i}.py")
                with open(file_path, 'w') as f:
                    f.write(content)
            
            # Find specific duplicates
            detector = DuplicateDetector()
            matches = detector.find_specific_duplicates(temp_dir, target_function)
            
            # Should find all instances
            assert len(matches) == 3, \
                f"Expected 3 instances of {target_function}, found {len(matches)}"
            
            # All should have the correct name
            for match in matches:
                assert match.name == target_function, \
                    f"Expected name {target_function}, got {match.name}"
        
        finally:
            # Clean up
            for i in range(3):
                file_path = os.path.join(temp_dir, f"test_target_{i}.py")
                if os.path.exists(file_path):
                    os.unlink(file_path)
            os.rmdir(temp_dir)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])