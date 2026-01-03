"""
Unit tests for the DuplicateDetector tool to improve coverage.

This module validates specific methods of the DuplicateDetector tool
that may not be fully covered by the updated property-based tests.
"""

import pytest
import os
import tempfile
import shutil
from unittest.mock import MagicMock
from kivy_garden.markdownlabel.tests.modules.duplicate_detector import DuplicateDetector


class TestDuplicateDetectorCoverage:
    """Tests for the DuplicateDetector class coverage."""

    @pytest.fixture
    def sample_dir(self):
        """Create a temporary directory with sample python files."""
        temp_dir = tempfile.mkdtemp()

        # Create file with duplicates
        with open(os.path.join(temp_dir, 'test_file1.py'), 'w') as f:
            f.write("def duplicate_func():\n    print('duplicate')\n    return True\n")

        with open(os.path.join(temp_dir, 'test_file2.py'), 'w') as f:
            f.write(
                "def duplicate_func():\n    print('duplicate')\n    return True\n\n"
                "def unique_func():\n    pass\n"
            )

        yield temp_dir
        shutil.rmtree(temp_dir)

    def test_initialization(self):
        """Test DuplicateDetector initialization."""
        detector = DuplicateDetector()
        assert detector.similarity_threshold > 0

        detector_custom = DuplicateDetector(similarity_threshold=0.9)
        assert detector_custom.similarity_threshold == 0.9

    def test_similarity_calculation_direct(self):
        """Test similarity calculation logic directly."""
        detector = DuplicateDetector()

        # Helper to create mock functions
        def create_mock_func(name, body_hash, params=None):
            func = MagicMock()
            func.name = name
            func.body_hash = body_hash
            func.parameters = params or []
            return func

        # Identical code (same body hash)
        func1 = create_mock_func("foo", "hash123")
        func2 = create_mock_func("foo", "hash123")

        score = detector._calculate_similarity(func1, func2)
        assert score == 1.0

        # Different code
        func3 = create_mock_func("foo", "hash_one", ["a"])
        func4 = create_mock_func("bar", "hash_two", ["b"])

        score = detector._calculate_similarity(func3, func4)
        assert score < 1.0

    def test_find_specific_duplicates_direct(self, sample_dir):
        """Test find_specific_duplicates method."""
        detector = DuplicateDetector()
        matches = detector.find_specific_duplicates(sample_dir, 'duplicate_func')
        assert len(matches) >= 2

        names = [m.name for m in matches]
        assert 'duplicate_func' in names
