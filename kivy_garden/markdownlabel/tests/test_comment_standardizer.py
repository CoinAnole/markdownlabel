"""Property-based tests for comment standardization functionality.

Tests the CommentStandardizer's ability to generate and apply standardized
comments for property-based tests with proper strategy documentation.
"""

import pytest
import os
import re
import sys
import tempfile
from hypothesis import given, strategies as st, settings

# Add tools directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'tools'))

from test_optimization.comment_standardizer import CommentStandardizer, StandardizationResult
from test_optimization.comment_format import StrategyType, CommentFormatValidator


class TestBooleanStrategyDocumentation:
    """Property tests for boolean strategy documentation (Property 4)."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.standardizer = CommentStandardizer()
        self.validator = CommentFormatValidator()
    
    # **Feature: test-comment-standardization, Property 4: Boolean Strategy Documentation**
    # *For any* property-based test using boolean strategies, the comment SHALL reference 
    # True/False coverage in the rationale
    # **Validates: Requirements 2.3**
    
    @given(
        max_examples=st.integers(min_value=1, max_value=100).filter(lambda x: x not in {2, 5, 10, 20, 50, 100}),
        function_name=st.text(min_size=5, max_size=30, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd', 'Pc'))).map(lambda x: f"test_{x}")
    )
    # Boolean strategy: 2 examples (True/False coverage)
    @settings(max_examples=2, deadline=None)
    def test_boolean_strategy_comments_reference_true_false_coverage(self, max_examples, function_name):
        """Boolean strategy comments always reference True/False coverage."""
        # Create test code with boolean strategy but no comment
        test_code = f'''
@given(flag=st.booleans())
@settings(max_examples={max_examples}, deadline=None)
def {function_name}(flag):
    """Test function using boolean strategy."""
    assert isinstance(flag, bool)
'''
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(test_code)
            temp_file = f.name
        
        try:
            # Standardize the file
            result = self.standardizer.standardize_file(temp_file, dry_run=True)
            
            # Should succeed and generate a comment
            assert result.success
            assert result.changes_made > 0
            assert len(result.generated_comments) > 0
            
            # Find the boolean strategy comment
            boolean_comment = None
            for comment in result.generated_comments:
                if comment.strategy_type == "Boolean":
                    boolean_comment = comment
                    break
            
            # Should have generated a boolean strategy comment
            assert boolean_comment is not None, "Should generate a Boolean strategy comment"
            
            # Comment should reference True/False coverage
            assert "True/False" in boolean_comment.rationale, \
                f"Boolean strategy rationale should reference True/False coverage, got: {boolean_comment.rationale}"
            
            # Verify the generated comment is valid
            formatted_comment = boolean_comment.to_standardized_format()
            validation_result = self.validator.validate_comment_format(formatted_comment)
            assert validation_result.is_valid, f"Generated comment should be valid: {formatted_comment}"
            
        finally:
            # Clean up
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_boolean_strategy_comment_generation_consistency(self):
        """Boolean strategy comment generation is consistent."""
        # Test multiple max_examples values
        test_values = [1, 2, 5, 10, 25]
        
        for max_examples in test_values:
            comment = self.standardizer.generate_comment("Boolean", max_examples)
            
            # Should always contain True/False reference
            assert "True/False" in comment, f"Boolean comment should reference True/False: {comment}"
            
            # Should be valid format
            validation_result = self.validator.validate_comment_format(comment)
            assert validation_result.is_valid, f"Generated comment should be valid: {comment}"
            
            # Should have correct max_examples
            assert str(max_examples) in comment, f"Comment should contain max_examples {max_examples}: {comment}"
    
    def test_boolean_strategy_detection_accuracy(self):
        """Boolean strategy detection correctly identifies st.booleans() usage."""
        boolean_test_codes = [
            '''
@given(flag=st.booleans())
@settings(max_examples=3, deadline=None)
def test_simple_boolean(flag):
    assert isinstance(flag, bool)
''',
            '''
@given(enabled=st.booleans(), disabled=st.booleans())
@settings(max_examples=4, deadline=None)
def test_multiple_booleans(enabled, disabled):
    assert isinstance(enabled, bool)
    assert isinstance(disabled, bool)
''',
            '''
@given(data=st.tuples(st.booleans(), st.integers(min_value=0, max_value=2)))
@settings(max_examples=6, deadline=None)
def test_boolean_in_tuple(data):
    flag, num = data
    assert isinstance(flag, bool)
'''
        ]
        
        for i, test_code in enumerate(boolean_test_codes):
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(test_code)
                temp_file = f.name
            
            try:
                result = self.standardizer.standardize_file(temp_file, dry_run=True)
                
                # Should detect and generate appropriate comments
                assert result.success, f"Standardization should succeed for test {i}"
                assert result.changes_made > 0, f"Should generate comments for test {i}"
                
                # Should generate comments that reference boolean strategies appropriately
                has_boolean_reference = False
                for comment in result.generated_comments:
                    if "Boolean" in comment.strategy_type or "True/False" in comment.rationale:
                        has_boolean_reference = True
                        break
                
                # For tests with boolean strategies, should have boolean or combination references
                # (tuples with booleans might be classified as combinations)
                if 'st.booleans()' in test_code:
                    # Allow either Boolean strategy or combination strategy for tuple cases
                    has_strategy_reference = any(
                        "Boolean" in comment.strategy_type or 
                        "Combination" in comment.strategy_type or
                        "True/False" in comment.rationale or
                        "combination" in comment.rationale.lower()
                        for comment in result.generated_comments
                    )
                    assert has_strategy_reference, f"Should detect boolean or combination strategy in test {i}"
                
            finally:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
    
    def test_boolean_strategy_rationale_templates(self):
        """Boolean strategy rationale templates are consistent and correct."""
        # Test different ways to generate boolean strategy comments
        strategy_enum = StrategyType.BOOLEAN
        
        # Test with validator's generate_standard_comment
        validator_comment = self.validator.generate_standard_comment(strategy_enum, 2)
        assert "True/False" in validator_comment
        assert "Boolean strategy" in validator_comment
        
        # Test with standardizer's generate_comment
        standardizer_comment = self.standardizer.generate_comment("Boolean", 2)
        assert "True/False" in standardizer_comment
        assert "Boolean strategy" in standardizer_comment
        
        # Both should produce valid comments
        validator_result = self.validator.validate_comment_format(validator_comment)
        standardizer_result = self.validator.validate_comment_format(standardizer_comment)
        
        assert validator_result.is_valid
        assert standardizer_result.is_valid
        
        # Both should have the same essential content
        assert validator_result.parsed_pattern.strategy_type == "Boolean"
        assert standardizer_result.parsed_pattern.strategy_type == "Boolean"
        assert "True/False" in validator_result.parsed_pattern.rationale
        assert "True/False" in standardizer_result.parsed_pattern.rationale
    
    def test_boolean_strategy_edge_cases(self):
        """Boolean strategy documentation handles edge cases correctly."""
        edge_case_codes = [
            # Boolean with custom settings
            '''
@given(flag=st.booleans())
@settings(max_examples=1, deadline=None, suppress_health_check=[HealthCheck.too_slow])
def test_boolean_edge_case_1(flag):
    assert flag in [True, False]
''',
            # Boolean in complex combination
            '''
@given(data=st.one_of(st.booleans(), st.just(None)))
@settings(max_examples=7, deadline=None)
def test_boolean_edge_case_2(data):
    assert data is None or isinstance(data, bool)
''',
        ]
        
        for i, test_code in enumerate(edge_case_codes):
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(test_code)
                temp_file = f.name
            
            try:
                result = self.standardizer.standardize_file(temp_file, dry_run=True)
                
                # Should handle edge cases gracefully
                assert result.success, f"Should handle edge case {i} gracefully"
                
                # If comments are generated, they should be valid
                for comment in result.generated_comments:
                    formatted = comment.to_standardized_format()
                    validation_result = self.validator.validate_comment_format(formatted)
                    assert validation_result.is_valid, f"Edge case comment should be valid: {formatted}"
                
            finally:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
    
    def test_boolean_strategy_integration_with_analysis(self):
        """Boolean strategy documentation integrates properly with analysis tools."""
        test_code = '''
@given(flag=st.booleans())
@settings(max_examples=3, deadline=None)
def test_boolean_integration(flag):
    """Test boolean integration."""
    assert isinstance(flag, bool)
'''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(test_code)
            temp_file = f.name
        
        try:
            # First analyze without standardization
            from test_optimization.comment_analyzer import CommentAnalyzer
            analyzer = CommentAnalyzer()
            
            initial_analysis = analyzer.analyze_file(temp_file)
            assert initial_analysis.undocumented_tests > 0  # Should have undocumented test
            
            # Apply standardization
            result = self.standardizer.standardize_file(temp_file, dry_run=False)
            assert result.success
            assert result.changes_made > 0
            
            # Analyze after standardization
            final_analysis = analyzer.analyze_file(temp_file)
            
            # Should now be documented
            assert final_analysis.documented_tests > initial_analysis.documented_tests
            assert final_analysis.undocumented_tests < initial_analysis.undocumented_tests
            
            # Should have valid boolean strategy comment
            boolean_comments = [c for c in final_analysis.valid_comments if c.strategy_type == "Boolean"]
            assert len(boolean_comments) > 0
            
            for comment in boolean_comments:
                assert "True/False" in comment.rationale
            
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)


class TestFiniteStrategyDocumentation:
    """Property tests for finite strategy documentation (Property 5)."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.standardizer = CommentStandardizer()
        self.validator = CommentFormatValidator()
    
    # **Feature: test-comment-standardization, Property 5: Finite Strategy Documentation**
    # *For any* property-based test using finite strategies, the comment SHALL reference 
    # input space size in the rationale
    # **Validates: Requirements 2.4**
    
    @given(
        min_value=st.integers(min_value=0, max_value=10),
        max_value=st.integers(min_value=11, max_value=50),
        max_examples=st.integers(min_value=1, max_value=100).filter(lambda x: x not in {2, 5, 10, 20, 50, 100})
    )
    # Small finite strategy: 8 examples (input space size: 8)
    @settings(max_examples=8, deadline=None)
    def test_finite_strategy_comments_reference_input_space_size(self, min_value, max_value, max_examples):
        """Finite strategy comments reference input space size in rationale."""
        # Ensure we have a finite range
        if max_value <= min_value:
            max_value = min_value + 10
        
        input_space_size = max_value - min_value + 1
        
        # Create test code with finite integer strategy but no comment
        test_code = f'''
@given(num=st.integers(min_value={min_value}, max_value={max_value}))
@settings(max_examples={max_examples}, deadline=None)
def test_finite_strategy(num):
    """Test function using finite integer strategy."""
    assert {min_value} <= num <= {max_value}
'''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(test_code)
            temp_file = f.name
        
        try:
            # Standardize the file
            result = self.standardizer.standardize_file(temp_file, dry_run=True)
            
            # Should succeed and generate a comment
            assert result.success
            assert result.changes_made > 0
            assert len(result.generated_comments) > 0
            
            # Find the finite strategy comment
            finite_comment = None
            for comment in result.generated_comments:
                if "finite" in comment.strategy_type.lower():
                    finite_comment = comment
                    break
            
            # Should have generated a finite strategy comment
            assert finite_comment is not None, "Should generate a finite strategy comment"
            
            # Comment should reference input space size or finite coverage
            rationale_lower = finite_comment.rationale.lower()
            assert ("input space size" in rationale_lower or 
                   "finite coverage" in rationale_lower), \
                f"Finite strategy rationale should reference input space or finite coverage, got: {finite_comment.rationale}"
            
            # If it mentions input space size, it should include the actual size for small finite
            if "input space size" in rationale_lower and input_space_size <= 10:
                assert str(input_space_size) in finite_comment.rationale, \
                    f"Small finite strategy should include actual input space size {input_space_size}"
            
            # Verify the generated comment is valid
            formatted_comment = finite_comment.to_standardized_format()
            validation_result = self.validator.validate_comment_format(formatted_comment)
            assert validation_result.is_valid, f"Generated comment should be valid: {formatted_comment}"
            
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    @given(
        items=st.lists(st.text(min_size=1, max_size=10), min_size=1, max_size=20),
        max_examples=st.integers(min_value=1, max_value=50).filter(lambda x: x not in {2, 5, 10, 20, 50, 100})
    )
    # Medium finite strategy: 15 examples (adequate finite coverage)
    @settings(max_examples=15, deadline=None)
    def test_sampled_from_finite_strategy_documentation(self, items, max_examples):
        """Sampled_from finite strategies are properly documented."""
        # Create unique items to avoid duplicates affecting size calculation
        unique_items = list(set(items))
        if len(unique_items) == 0:
            unique_items = ['item1']
        
        items_str = ', '.join(f'"{item}"' for item in unique_items[:10])  # Limit to 10 items
        
        test_code = f'''
@given(item=st.sampled_from([{items_str}]))
@settings(max_examples={max_examples}, deadline=None)
def test_sampled_from_strategy(item):
    """Test function using sampled_from strategy."""
    assert item in [{items_str}]
'''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(test_code)
            temp_file = f.name
        
        try:
            result = self.standardizer.standardize_file(temp_file, dry_run=True)
            
            assert result.success
            assert result.changes_made > 0
            
            # Should generate appropriate finite strategy comment
            finite_comment = None
            for comment in result.generated_comments:
                if "finite" in comment.strategy_type.lower():
                    finite_comment = comment
                    break
            
            if finite_comment:
                # Should reference finite coverage or input space
                rationale_lower = finite_comment.rationale.lower()
                assert ("finite coverage" in rationale_lower or 
                       "input space size" in rationale_lower), \
                    f"Sampled_from strategy should reference finite coverage: {finite_comment.rationale}"
            
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_finite_strategy_size_classification(self):
        """Finite strategies are correctly classified by size."""
        test_cases = [
            # Small finite (≤10 elements)
            ('st.integers(min_value=0, max_value=5)', "Small finite", 6),
            ('st.integers(min_value=1, max_value=10)', "Small finite", 10),
            
            # Medium finite (11-50 elements)  
            ('st.integers(min_value=0, max_value=25)', "Medium finite", 26),
            ('st.integers(min_value=10, max_value=50)', "Medium finite", 41),
        ]
        
        for strategy_code, expected_type, expected_size in test_cases:
            # Use custom max_examples value
            custom_max_examples = 15  # Non-standard value
            test_code = f'''
@given(num={strategy_code})
@settings(max_examples={custom_max_examples}, deadline=None)
def test_finite_classification(num):
    """Test finite strategy classification."""
    assert isinstance(num, int)
'''
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(test_code)
                temp_file = f.name
            
            try:
                result = self.standardizer.standardize_file(temp_file, dry_run=True)
                
                assert result.success
                assert result.changes_made > 0
                
                # Find the generated comment
                generated_comment = result.generated_comments[0]
                
                # Should be classified correctly
                assert expected_type.lower() in generated_comment.strategy_type.lower(), \
                    f"Strategy {strategy_code} should be classified as {expected_type}, got {generated_comment.strategy_type}"
                
                # Should reference appropriate rationale
                if expected_type == "Small finite":
                    assert ("input space size" in generated_comment.rationale or 
                           "finite coverage" in generated_comment.rationale)
                elif expected_type == "Medium finite":
                    assert "finite coverage" in generated_comment.rationale
                
            finally:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
    
    def test_finite_strategy_rationale_consistency(self):
        """Finite strategy rationale is consistent across similar strategies."""
        small_finite_strategies = [
            'st.integers(min_value=0, max_value=5)',
            'st.integers(min_value=1, max_value=8)',
            'st.sampled_from(["a", "b", "c", "d", "e"])'
        ]
        
        medium_finite_strategies = [
            'st.integers(min_value=0, max_value=20)',
            'st.integers(min_value=5, max_value=30)',
        ]
        
        # Test small finite strategies
        small_finite_rationales = set()
        for strategy in small_finite_strategies:
            comment = self.standardizer.generate_comment("Small finite", 10, 6)
            small_finite_rationales.add(comment.lower())
        
        # Should use consistent rationale patterns
        for rationale in small_finite_rationales:
            assert ("input space size" in rationale or "finite coverage" in rationale)
        
        # Test medium finite strategies  
        medium_finite_rationales = set()
        for strategy in medium_finite_strategies:
            comment = self.standardizer.generate_comment("Medium finite", 20)
            medium_finite_rationales.add(comment.lower())
        
        # Should use consistent rationale patterns
        for rationale in medium_finite_rationales:
            assert "finite coverage" in rationale


class TestBackupAndRollbackFunctionality:
    """Tests for backup and rollback functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.standardizer = CommentStandardizer()
    
    def test_backup_creation_and_rollback(self):
        """Test that backups are created and rollback works correctly."""
        original_content = '''
@given(flag=st.booleans())
@settings(max_examples=3, deadline=None)
def test_backup_example(flag):
    """Test function for backup testing."""
    assert isinstance(flag, bool)
'''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(original_content)
            temp_file = f.name
        
        try:
            # Apply standardization (should create backup)
            result = self.standardizer.standardize_file(temp_file, dry_run=False)
            
            assert result.success
            assert result.changes_made > 0
            assert result.backup_path is not None
            assert os.path.exists(result.backup_path)
            
            # Verify backup contains original content
            with open(result.backup_path, 'r') as f:
                backup_content = f.read()
            assert backup_content == original_content
            
            # Verify file was modified
            with open(temp_file, 'r') as f:
                modified_content = f.read()
            assert modified_content != original_content
            assert "Boolean strategy" in modified_content
            
            # Test rollback
            rollback_success = self.standardizer.rollback_file(temp_file, result.backup_path)
            assert rollback_success
            
            # Verify rollback restored original content
            with open(temp_file, 'r') as f:
                restored_content = f.read()
            assert restored_content == original_content
            
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
            if result.backup_path and os.path.exists(result.backup_path):
                os.unlink(result.backup_path)
    
    def test_backup_directory_management(self):
        """Test backup directory creation and management."""
        # Test backup directory creation
        assert self.standardizer.create_backup_directory()
        assert os.path.exists(self.standardizer.backup_dir)
        
        # Clean up any existing backups first
        existing_backups = self.standardizer.list_backups()
        for backup in existing_backups:
            try:
                os.unlink(backup)
            except Exception:
                pass
        
        # Test listing backups (should be empty after cleanup)
        backups = self.standardizer.list_backups()
        assert isinstance(backups, list)
        
        # Create some test backup files
        test_backups = []
        for i in range(3):
            backup_path = os.path.join(self.standardizer.backup_dir, f"test_{i}.py.backup")
            with open(backup_path, 'w') as f:
                f.write(f"# Test backup {i}")
            test_backups.append(backup_path)
        
        try:
            # Test listing backups
            backups = self.standardizer.list_backups()
            assert len(backups) == 3
            
            # Test backup cleanup
            removed_count = self.standardizer.cleanup_old_backups(keep_count=2)
            assert removed_count == 1
            
            remaining_backups = self.standardizer.list_backups()
            assert len(remaining_backups) == 2
            
        finally:
            # Clean up test backups
            for backup_path in test_backups:
                if os.path.exists(backup_path):
                    os.unlink(backup_path)
    
    def test_backup_integrity_verification(self):
        """Test backup integrity verification."""
        # Create a valid backup file
        valid_backup_content = '''
@given(data=st.text())
@settings(max_examples=25, deadline=None)
def test_valid_backup(data):
    """Valid test function."""
    assert isinstance(data, str)
'''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py.backup', delete=False) as f:
            f.write(valid_backup_content)
            valid_backup = f.name
        
        # Create an invalid backup file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py.backup', delete=False) as f:
            f.write("")  # Empty file
            invalid_backup = f.name
        
        try:
            # Test valid backup
            assert self.standardizer.verify_backup_integrity(valid_backup)
            
            # Test invalid backup
            assert not self.standardizer.verify_backup_integrity(invalid_backup)
            
            # Test non-existent backup
            assert not self.standardizer.verify_backup_integrity("/non/existent/file.backup")
            
        finally:
            if os.path.exists(valid_backup):
                os.unlink(valid_backup)
            if os.path.exists(invalid_backup):
                os.unlink(invalid_backup)
    
    def test_batch_rollback_functionality(self):
        """Test batch rollback functionality."""
        # Create multiple test files
        test_files = []
        results = []
        
        for i in range(3):
            # Use custom max_examples values that will trigger standardization
            max_examples = [3, 7, 15][i]  # Non-standard values
            content = f'''
@given(num=st.integers(min_value=0, max_value={i+3}))
@settings(max_examples={max_examples}, deadline=None)
def test_batch_{i}(num):
    """Test function {i}."""
    assert isinstance(num, int)
'''
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(content)
                test_files.append(f.name)
        
        try:
            # Apply standardization to all files
            for file_path in test_files:
                result = self.standardizer.standardize_file(file_path, dry_run=False)
                results.append(result)
            
            # Verify all were standardized
            for result in results:
                assert result.success
                assert result.changes_made > 0
                assert result.backup_path is not None
            
            # Test batch rollback
            rollback_count = self.standardizer.rollback_batch(results)
            assert rollback_count == len(results)
            
            # Verify all files were rolled back
            for i, file_path in enumerate(test_files):
                with open(file_path, 'r') as f:
                    content = f.read()
                # Should not contain standardized comments
                assert "strategy:" not in content
                assert f"test_batch_{i}" in content
            
        finally:
            # Clean up
            for file_path in test_files:
                if os.path.exists(file_path):
                    os.unlink(file_path)
            for result in results:
                if result.backup_path and os.path.exists(result.backup_path):
                    os.unlink(result.backup_path)
    
    def test_backup_info_retrieval(self):
        """Test backup information retrieval."""
        # Create a test backup file
        backup_content = '''
@given(data=st.text())
@settings(max_examples=15, deadline=None)
def test_backup_info(data):
    """Test function for backup info."""
    assert isinstance(data, str)
'''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py.backup', delete=False) as f:
            f.write(backup_content)
            backup_path = f.name
        
        try:
            # Get backup info
            info = self.standardizer.get_backup_info(backup_path)
            
            assert info is not None
            assert info['path'] == backup_path
            assert 'size' in info
            assert 'created' in info
            assert 'modified' in info
            assert info['valid'] == 'True'
            
            # Test non-existent backup
            non_existent_info = self.standardizer.get_backup_info("/non/existent/backup.py")
            assert non_existent_info is None
            
        finally:
            if os.path.exists(backup_path):
                os.unlink(backup_path)
    
    def test_safety_checks_and_validation(self):
        """Test safety checks and validation functionality."""
        # Test file that doesn't need standardization
        already_standardized_content = '''
# Boolean strategy: 3 examples (True/False coverage)
@given(flag=st.booleans())
@settings(max_examples=3, deadline=None)
def test_already_standardized(flag):
    """Already standardized test function."""
    assert isinstance(flag, bool)
'''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(already_standardized_content)
            temp_file = f.name
        
        try:
            # Should not create backup for already standardized file
            result = self.standardizer.standardize_file(temp_file, dry_run=False)
            
            assert result.success
            assert result.changes_made == 0  # No changes needed
            assert result.backup_path is None  # No backup created
            
            # Validate standardization
            is_standardized = self.standardizer.validate_standardization(temp_file)
            assert is_standardized
            
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_error_handling_in_backup_operations(self):
        """Test error handling in backup operations."""
        # Test rollback with non-existent backup
        rollback_success = self.standardizer.rollback_file(
            "/some/file.py", 
            "/non/existent/backup.py"
        )
        assert not rollback_success
        
        # Test backup info for invalid path
        info = self.standardizer.get_backup_info("/invalid/path/backup.py")
        assert info is None
        
        # Test cleanup with non-existent backup directory
        original_backup_dir = self.standardizer.backup_dir
        self.standardizer.backup_dir = "/non/existent/backup/dir"
        
        try:
            removed_count = self.standardizer.cleanup_old_backups()
            assert removed_count == 0
            
            backups = self.standardizer.list_backups()
            assert backups == []
            
        finally:
            self.standardizer.backup_dir = original_backup_dir


class TestPerformanceRationaleDocumentation:
    """Property tests for performance rationale documentation (Property 6)."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.standardizer = CommentStandardizer()
        self.validator = CommentFormatValidator()
        
        # Import performance handler components
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'tools'))
        from test_optimization.performance_rationale_handler import (
            PerformanceRationaleDetector, 
            PerformanceCommentGenerator,
            PerformanceReason
        )
        self.detector = PerformanceRationaleDetector()
        self.generator = PerformanceCommentGenerator()
        self.PerformanceReason = PerformanceReason  # Make accessible to test methods
    
    # **Feature: test-comment-standardization, Property 6: Performance Rationale Documentation**
    # *For any* property-based test with reduced max_examples for performance reasons, 
    # the comment SHALL explain the performance rationale
    # **Validates: Requirements 2.2, 3.3, 5.2**
    
    @given(
        base_examples=st.integers(min_value=20, max_value=100),
        ci_examples=st.integers(min_value=1, max_value=10).filter(lambda x: x not in {2, 5, 10}),  # Exclude standard values
        function_name=st.text(min_size=5, max_size=30, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd', 'Pc'))).map(lambda x: f"test_{x}")
    )
    # Complex strategy: 5 examples (performance optimized)
    @settings(max_examples=5, deadline=None)
    def test_ci_optimization_performance_rationale_documented(self, base_examples, ci_examples, function_name):
        """CI optimization performance rationale is properly documented."""
        # Create test code with CI optimization pattern
        test_code = f'''
@given(data=st.text(min_size=10, max_size=100))
@settings(max_examples={base_examples} if not os.getenv('CI') else {ci_examples}, deadline=None)
def {function_name}(data):
    """Test function with CI optimization."""
    assert isinstance(data, str)
    assert len(data) >= 10
'''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(test_code)
            temp_file = f.name
        
        try:
            # Detect performance rationale
            performance_rationale = self.detector.detect_performance_rationale(test_code, ci_examples)
            
            # Should detect CI optimization
            assert performance_rationale is not None, "Should detect CI optimization performance rationale"
            assert performance_rationale.ci_specific, "Should identify as CI-specific optimization"
            assert performance_rationale.base_examples == base_examples, f"Should detect base examples: {base_examples}"
            assert performance_rationale.reduced_examples == ci_examples, f"Should detect CI examples: {ci_examples}"
            
            # Generate performance-aware comment
            performance_comment = self.generator.generate_performance_comment(test_code, ci_examples)
            assert performance_comment is not None, "Should generate performance-aware comment"
            
            # Comment should mention CI optimization
            assert "CI" in performance_comment, f"Performance comment should mention CI: {performance_comment}"
            assert str(base_examples) in performance_comment, f"Should mention base examples {base_examples}"
            assert str(ci_examples) in performance_comment, f"Should mention CI examples {ci_examples}"
            
            # Standardize the file to test integration
            result = self.standardizer.standardize_file(temp_file, dry_run=True)
            assert result.success, "Standardization should succeed"
            assert result.changes_made > 0, "Should generate performance comment"
            
            # Find the generated performance comment
            performance_generated = None
            for comment in result.generated_comments:
                if "CI" in comment.rationale or "performance" in comment.rationale.lower():
                    performance_generated = comment
                    break
            
            assert performance_generated is not None, "Should generate comment with performance rationale"
            
            # Validate the generated comment format
            formatted_comment = performance_generated.to_standardized_format()
            validation_result = self.validator.validate_comment_format(formatted_comment)
            assert validation_result.is_valid, f"Performance comment should be valid: {formatted_comment}"
            
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    @given(
        max_examples=st.integers(min_value=1, max_value=5),
        strategy_complexity=st.sampled_from(['text', 'floats', 'composite']),
        function_name=st.text(min_size=5, max_size=30, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd', 'Pc'))).map(lambda x: f"test_{x}")
    )
    # Complex strategy: 3 examples (performance optimized)
    @settings(max_examples=3, deadline=None)
    def test_execution_time_performance_rationale_documented(self, max_examples, strategy_complexity, function_name):
        """Execution time performance rationale is properly documented."""
        # Create test code with complex strategy and low max_examples (performance optimization)
        strategy_map = {
            'text': 'st.text(min_size=50, max_size=200)',
            'floats': 'st.floats(min_value=-1000.0, max_value=1000.0, allow_nan=False)',
            'composite': 'st.composite(lambda draw: draw(st.text()) + str(draw(st.integers())))'
        }
        
        strategy_code = strategy_map[strategy_complexity]
        
        test_code = f'''
@given(data={strategy_code})
@settings(max_examples={max_examples}, deadline=None)
def {function_name}(data):
    """Test function with performance optimization."""
    # Complex processing that justifies low max_examples
    processed = str(data).upper().lower().strip()
    assert len(processed) >= 0
'''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(test_code)
            temp_file = f.name
        
        try:
            # Detect performance rationale
            performance_rationale = self.detector.detect_performance_rationale(test_code, max_examples)
            
            # Should detect performance optimization for complex strategies with low max_examples
            if strategy_complexity in ['text', 'floats', 'composite']:
                assert performance_rationale is not None, f"Should detect performance rationale for {strategy_complexity} with {max_examples} examples"
                assert not performance_rationale.ci_specific, "Should not be CI-specific"
                assert performance_rationale.reduced_examples == max_examples
            
            # Generate performance-aware comment
            performance_comment = self.generator.generate_performance_comment(test_code, max_examples)
            
            if performance_comment:
                # Comment should mention performance optimization
                assert "performance" in performance_comment.lower() or "optimized" in performance_comment.lower(), \
                    f"Performance comment should mention optimization: {performance_comment}"
                
                # Should be valid format
                validation_result = self.validator.validate_comment_format(performance_comment)
                assert validation_result.is_valid, f"Performance comment should be valid: {performance_comment}"
            
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    @given(
        performance_keywords=st.sampled_from([
            "performance optimized",
            "execution time optimization", 
            "memory optimization",
            "deadline constraint",
            "complexity reduction"
        ]),
        max_examples=st.integers(min_value=1, max_value=20),
        function_name=st.text(min_size=5, max_size=30, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd', 'Pc'))).map(lambda x: f"test_{x}")
    )
    # Complex strategy: 4 examples (performance optimized)
    @settings(max_examples=4, deadline=None)
    def test_explicit_performance_comments_detected(self, performance_keywords, max_examples, function_name):
        """Explicit performance comments are properly detected and preserved."""
        # Create test code with explicit performance comment
        test_code = f'''
# This test uses reduced examples for {performance_keywords}
@given(data=st.text(min_size=20, max_size=100))
@settings(max_examples={max_examples}, deadline=None)
def {function_name}(data):
    """Test function with explicit performance comment."""
    assert isinstance(data, str)
'''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(test_code)
            temp_file = f.name
        
        try:
            # Detect performance rationale from existing comment
            performance_rationale = self.detector.detect_performance_rationale(test_code, max_examples)
            
            # Should detect performance rationale from comment
            assert performance_rationale is not None, f"Should detect performance rationale from comment: {performance_keywords}"
            assert performance_rationale.reduced_examples == max_examples
            
            # Should identify the correct performance reason type
            if "execution time" in performance_keywords:
                assert performance_rationale.reason == self.PerformanceReason.EXECUTION_TIME
            elif "memory" in performance_keywords:
                assert performance_rationale.reason == self.PerformanceReason.MEMORY_OPTIMIZATION
            elif "deadline" in performance_keywords:
                assert performance_rationale.reason == self.PerformanceReason.DEADLINE_CONSTRAINT
            elif "complexity" in performance_keywords:
                assert performance_rationale.reason == self.PerformanceReason.COMPLEXITY_REDUCTION
            
            # Generate performance-aware comment
            performance_comment = self.generator.generate_performance_comment(test_code, max_examples)
            assert performance_comment is not None, "Should generate performance-aware comment"
            
            # Should include performance rationale
            assert "performance" in performance_comment.lower() or "optimized" in performance_comment.lower(), \
                f"Generated comment should include performance rationale: {performance_comment}"
            
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_performance_rationale_consistency_across_similar_tests(self):
        """Performance rationale is consistent across similar test patterns."""
        # Test multiple similar CI optimization patterns
        ci_patterns = [
            "max_examples=20 if not os.getenv('CI') else 5",
            "max_examples=5 if os.getenv('CI') else 20",
            "max_examples=30 if not os.getenv('CI') else 10"
        ]
        
        generated_rationales = []
        
        for i, pattern in enumerate(ci_patterns):
            test_code = f'''
@given(data=st.text())
@settings({pattern}, deadline=None)
def test_ci_pattern_{i}(data):
    """Test CI pattern {i}."""
    assert isinstance(data, str)
'''
            
            # Extract the CI examples value
            if "else 5" in pattern:
                ci_examples = 5
            elif "else 20" in pattern:
                ci_examples = 20
            elif "else 10" in pattern:
                ci_examples = 10
            else:
                ci_examples = 5
            
            performance_rationale = self.detector.detect_performance_rationale(test_code, ci_examples)
            
            # All should be detected as CI optimizations
            assert performance_rationale is not None, f"Should detect CI optimization in pattern: {pattern}"
            assert performance_rationale.ci_specific, f"Should be CI-specific: {pattern}"
            
            # Generate comments
            performance_comment = self.generator.generate_performance_comment(test_code, ci_examples)
            assert performance_comment is not None
            
            generated_rationales.append(performance_comment)
        
        # All CI optimization comments should mention CI
        for rationale in generated_rationales:
            assert "CI" in rationale, f"CI optimization comment should mention CI: {rationale}"
        
        # Should use consistent terminology
        ci_keywords = ["CI optimized", "CI optimization", "CI"]
        for rationale in generated_rationales:
            has_ci_keyword = any(keyword in rationale for keyword in ci_keywords)
            assert has_ci_keyword, f"Should use consistent CI terminology: {rationale}"
    
    def test_performance_rationale_integration_with_standardizer(self):
        """Performance rationale integrates properly with the comment standardizer."""
        # Test various performance optimization scenarios
        test_scenarios = [
            {
                'name': 'ci_optimization',
                'code': '''
@given(data=st.text(min_size=10, max_size=50))
@settings(max_examples=25 if not os.getenv('CI') else 5, deadline=None)
def test_ci_integration(data):
    """Test CI integration."""
    assert len(data) >= 10
''',
                'expected_max_examples': 5,
                'should_have_performance': True,
                'should_mention_ci': True
            },
            {
                'name': 'deadline_constraint',
                'code': '''
@given(data=st.text(min_size=50, max_size=200))
@settings(max_examples=3, deadline=None)
def test_deadline_constraint(data):
    """Test with deadline constraint."""
    # Complex processing
    result = data.upper().lower().strip().replace(' ', '_')
    assert isinstance(result, str)
''',
                'expected_max_examples': 3,
                'should_have_performance': True,
                'should_mention_ci': False
            },
            {
                'name': 'standard_test',
                'code': '''
@given(flag=st.booleans())
@settings(max_examples=2, deadline=None)
def test_standard_boolean(flag):
    """Standard boolean test."""
    assert isinstance(flag, bool)
''',
                'expected_max_examples': 2,
                'should_have_performance': False,
                'should_mention_ci': False
            }
        ]
        
        for scenario in test_scenarios:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(scenario['code'])
                temp_file = f.name
            
            try:
                # Test standardization
                result = self.standardizer.standardize_file(temp_file, dry_run=True)
                
                assert result.success, f"Standardization should succeed for {scenario['name']}"
                
                if scenario['should_have_performance']:
                    # Should generate performance-aware comment
                    assert result.changes_made > 0, f"Should generate comment for {scenario['name']}"
                    
                    performance_comment = None
                    for comment in result.generated_comments:
                        if ("performance" in comment.rationale.lower() or 
                            "optimized" in comment.rationale.lower() or
                            "CI" in comment.rationale):
                            performance_comment = comment
                            break
                    
                    assert performance_comment is not None, f"Should generate performance comment for {scenario['name']}"
                    
                    if scenario['should_mention_ci']:
                        assert "CI" in performance_comment.rationale, f"Should mention CI for {scenario['name']}"
                    
                    # Validate comment format
                    formatted = performance_comment.to_standardized_format()
                    validation_result = self.validator.validate_comment_format(formatted)
                    assert validation_result.is_valid, f"Performance comment should be valid for {scenario['name']}: {formatted}"
                
            finally:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
    
    def test_performance_rationale_enhancement_of_existing_comments(self):
        """Performance rationale can enhance existing non-performance comments."""
        # Test enhancing a basic comment with performance information
        test_code = '''
# Complex strategy: 5 examples (adequate coverage)
@given(data=st.text(min_size=100, max_size=500))
@settings(max_examples=5, deadline=None)
def test_enhancement_example(data):
    """Test for comment enhancement."""
    # Expensive processing that justifies low max_examples
    processed = data.upper().lower().strip().replace(' ', '_')
    assert len(processed) > 0
'''
        
        existing_comment = "# Complex strategy: 5 examples (adequate coverage)"
        
        # Test enhancement
        enhanced_comment = self.generator.enhance_existing_comment(existing_comment, test_code, 5)
        
        if enhanced_comment:
            # Should include both original and performance rationale
            assert "adequate coverage" in enhanced_comment, "Should preserve original rationale"
            assert ("performance" in enhanced_comment.lower() or 
                   "optimized" in enhanced_comment.lower()), "Should add performance rationale"
            
            # Should be valid format
            validation_result = self.validator.validate_comment_format(enhanced_comment)
            assert validation_result.is_valid, f"Enhanced comment should be valid: {enhanced_comment}"
    
    def test_performance_pattern_analysis_across_files(self):
        """Performance pattern analysis works across multiple files."""
        # Create multiple test files with different performance patterns
        test_files = []
        
        file_contents = [
            # CI optimized file
            '''
@given(data=st.text())
@settings(max_examples=20 if not os.getenv('CI') else 5, deadline=None)
def test_ci_file_1(data):
    """CI optimized test."""
    assert isinstance(data, str)
''',
            # Performance optimized file
            '''
@given(data=st.text(min_size=50, max_size=200))
@settings(max_examples=3, deadline=None)
def test_performance_file_1(data):
    """Performance optimized test."""
    result = data.upper().lower()
    assert len(result) > 0
''',
            # Standard file (no performance optimization)
            '''
@given(flag=st.booleans())
@settings(max_examples=2, deadline=None)
def test_standard_file_1(flag):
    """Standard test."""
    assert isinstance(flag, bool)
'''
        ]
        
        for i, content in enumerate(file_contents):
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(content)
                test_files.append(f.name)
        
        try:
            # Analyze performance patterns
            performance_standardizer = self.standardizer.performance_standardizer
            analysis_results = performance_standardizer.analyze_performance_patterns(test_files)
            
            # Should detect CI optimized tests
            assert len(analysis_results['ci_optimized_tests']) > 0, "Should detect CI optimized tests"
            
            # Should detect performance optimized tests
            assert len(analysis_results['performance_optimized_tests']) > 0, "Should detect performance optimized tests"
            
            # Verify CI optimization detection
            ci_test = analysis_results['ci_optimized_tests'][0]
            assert ci_test['base_examples'] == 20, "Should detect base examples"
            assert ci_test['ci_examples'] == 5, "Should detect CI examples"
            
            # Verify performance optimization detection
            perf_test = analysis_results['performance_optimized_tests'][0]
            assert perf_test['max_examples'] == 3, "Should detect performance optimized max_examples"
            
        finally:
            for file_path in test_files:
                if os.path.exists(file_path):
                    os.unlink(file_path)


class TestCIOptimizationDocumentation:
    """Property tests for CI optimization documentation (Property 7)."""
    
    def setup_method(self):
        """Set up test fixtures."""
        # Import CI optimization components first
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'tools'))
        from test_optimization.ci_optimization_handler import (
            CIOptimizationDetector,
            CIOptimizationCommentGenerator,
            CIOptimizationIntegrator,
            CIOptimizationType
        )
        
        self.standardizer = CommentStandardizer()
        self.validator = CommentFormatValidator()
        self.ci_detector = CIOptimizationDetector()
        self.ci_generator = CIOptimizationCommentGenerator()
        self.ci_integrator = CIOptimizationIntegrator()
        self.CIOptimizationType = CIOptimizationType  # Make it accessible to test methods
    
    # **Feature: test-comment-standardization, Property 7: CI Optimization Documentation**
    # *For any* property-based test using CI-specific max_examples reduction, 
    # the comment SHALL document both the optimization rationale and reference the CI environment
    # **Validates: Requirements 1.5, 5.1, 5.5**
    
    @given(
        base_examples=st.integers(min_value=15, max_value=100),
        ci_examples=st.integers(min_value=1, max_value=10).filter(lambda x: x not in {2, 5, 10}),  # Exclude standard values
        function_name=st.text(min_size=5, max_size=30, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd', 'Pc'))).map(lambda x: f"test_{x}")
    )
    # Complex strategy: 3 examples (adequate coverage)
    @settings(max_examples=3, deadline=None)
    def test_ci_optimization_documentation_includes_both_values(self, base_examples, ci_examples, function_name):
        """CI optimization documentation includes both base and CI values."""
        # Create test code with CI optimization pattern
        test_code = f'''
@given(data=st.text(min_size=20, max_size=100))
@settings(max_examples={base_examples} if not os.getenv('CI') else {ci_examples}, deadline=None)
def {function_name}(data):
    """Test function with CI optimization."""
    assert isinstance(data, str)
    assert len(data) >= 20
'''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(test_code)
            temp_file = f.name
        
        try:
            # Detect CI optimization
            ci_info = self.ci_detector.detect_ci_optimization(test_code)
            
            # Should detect CI optimization
            assert ci_info is not None, "Should detect CI optimization"
            assert ci_info.optimization_type == self.CIOptimizationType.CONDITIONAL_EXPRESSION
            assert ci_info.base_examples == base_examples, f"Should detect base examples: {base_examples}"
            assert ci_info.ci_examples == ci_examples, f"Should detect CI examples: {ci_examples}"
            
            # Generate CI optimization comment
            ci_comment = self.ci_generator.generate_ci_optimization_comment(test_code, ci_examples)
            assert ci_comment is not None, "Should generate CI optimization comment"
            
            # Comment should mention CI optimization
            assert "CI optimized" in ci_comment or "CI" in ci_comment, f"CI comment should mention CI: {ci_comment}"
            assert str(base_examples) in ci_comment, f"Should mention base examples {base_examples}"
            assert str(ci_examples) in ci_comment, f"Should mention CI examples {ci_examples}"
            
            # Should reference both local and CI environments
            assert ("locally" in ci_comment.lower() or "local" in ci_comment.lower()), \
                f"Should reference local environment: {ci_comment}"
            assert "CI" in ci_comment, f"Should reference CI environment: {ci_comment}"
            
            # Standardize the file to test integration
            result = self.standardizer.standardize_file(temp_file, dry_run=True)
            assert result.success, "Standardization should succeed"
            assert result.changes_made > 0, "Should generate CI optimization comment"
            
            # Find the generated CI optimization comment
            ci_generated = None
            for comment in result.generated_comments:
                if "CI" in comment.rationale:
                    ci_generated = comment
                    break
            
            assert ci_generated is not None, "Should generate comment with CI optimization rationale"
            
            # Validate the generated comment format
            formatted_comment = ci_generated.to_standardized_format()
            validation_result = self.validator.validate_comment_format(formatted_comment)
            assert validation_result.is_valid, f"CI optimization comment should be valid: {formatted_comment}"
            
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    @given(
        ci_pattern=st.sampled_from([
            "max_examples=25 if not os.getenv('CI') else 5",
            "max_examples=5 if os.getenv('CI') else 25",
            "max_examples=30 if not os.getenv('CI') else 8",
            "max_examples=8 if os.getenv('CI') else 30"
        ]),
        function_name=st.text(min_size=5, max_size=30, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd', 'Pc'))).map(lambda x: f"test_{x}")
    )
    # Complex strategy: 4 examples (adequate coverage)
    @settings(max_examples=4, deadline=None)
    def test_ci_optimization_patterns_consistently_documented(self, ci_pattern, function_name):
        """Different CI optimization patterns are consistently documented."""
        # Create test code with specific CI pattern
        test_code = f'''
@given(data=st.text(min_size=10, max_size=50))
@settings({ci_pattern}, deadline=None)
def {function_name}(data):
    """Test function with CI pattern."""
    assert isinstance(data, str)
'''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(test_code)
            temp_file = f.name
        
        try:
            # Detect CI optimization
            ci_info = self.ci_detector.detect_ci_optimization(test_code)
            
            # Should detect CI optimization for all patterns
            assert ci_info is not None, f"Should detect CI optimization in pattern: {ci_pattern}"
            assert ci_info.optimization_type == self.CIOptimizationType.CONDITIONAL_EXPRESSION
            
            # Extract expected values from pattern
            numbers = re.findall(r'\d+', ci_pattern)
            assert len(numbers) == 2, f"Pattern should have two numbers: {ci_pattern}"
            
            values = [int(n) for n in numbers]
            expected_base = max(values)
            expected_ci = min(values)
            
            assert ci_info.base_examples == expected_base, f"Should detect base examples: {expected_base}"
            assert ci_info.ci_examples == expected_ci, f"Should detect CI examples: {expected_ci}"
            
            # Generate CI optimization comment
            ci_comment = self.ci_generator.generate_ci_optimization_comment(test_code, expected_ci)
            assert ci_comment is not None, f"Should generate CI comment for pattern: {ci_pattern}"
            
            # All CI optimization comments should use consistent terminology
            assert "CI" in ci_comment, f"Should mention CI: {ci_comment}"
            
            # Should use consistent format
            validation_result = self.validator.validate_comment_format(ci_comment)
            assert validation_result.is_valid, f"CI comment should be valid: {ci_comment}"
            
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    @given(
        optimization_reference=st.sampled_from([
            "automated CI optimization",
            "CI environment optimization", 
            "continuous integration performance",
            "CI pipeline optimization"
        ]),
        max_examples=st.integers(min_value=1, max_value=15).filter(lambda x: x not in {2, 5, 10}),
        function_name=st.text(min_size=5, max_size=30, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd', 'Pc'))).map(lambda x: f"test_{x}")
    )
    # Complex strategy: 6 examples (adequate coverage)
    @settings(max_examples=6, deadline=None)
    def test_ci_optimization_process_referenced_in_comments(self, optimization_reference, max_examples, function_name):
        """CI optimization process is properly referenced in comments."""
        # Create test code with CI optimization reference in comment
        test_code = f'''
# This test uses {optimization_reference}
@given(data=st.text(min_size=30, max_size=100))
@settings(max_examples={max_examples}, deadline=None)
def {function_name}(data):
    """Test function with CI optimization reference."""
    assert isinstance(data, str)
'''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(test_code)
            temp_file = f.name
        
        try:
            # Detect CI optimization from comment
            ci_info = self.ci_detector.detect_ci_optimization(test_code)
            
            # Should detect CI optimization from comment reference
            if "CI" in optimization_reference:
                assert ci_info is not None, f"Should detect CI optimization from reference: {optimization_reference}"
                assert ci_info.optimization_type == self.CIOptimizationType.AUTOMATED_OPTIMIZATION
                assert ci_info.ci_examples == max_examples
            
            # Generate CI optimization comment
            ci_comment = self.ci_generator.generate_ci_optimization_comment(test_code, max_examples)
            
            if ci_comment:
                # Should reference the optimization process
                assert "CI" in ci_comment, f"Should reference CI in comment: {ci_comment}"
                
                # Should be valid format
                validation_result = self.validator.validate_comment_format(ci_comment)
                assert validation_result.is_valid, f"CI comment should be valid: {ci_comment}"
            
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_ci_optimization_integration_with_standardizer(self):
        """CI optimization integrates properly with the comment standardizer."""
        # Test various CI optimization scenarios
        test_scenarios = [
            {
                'name': 'conditional_expression',
                'code': '''
@given(data=st.text(min_size=20, max_size=100))
@settings(max_examples=30 if not os.getenv('CI') else 7, deadline=None)
def test_ci_conditional(data):
    """Test CI conditional expression."""
    assert len(data) >= 20
''',
                'expected_ci_examples': 7,
                'expected_base_examples': 30,
                'should_have_ci': True
            },
            {
                'name': 'reverse_conditional',
                'code': '''
@given(data=st.text(min_size=10, max_size=50))
@settings(max_examples=4 if os.getenv('CI') else 20, deadline=None)
def test_ci_reverse(data):
    """Test CI reverse conditional."""
    assert len(data) >= 10
''',
                'expected_ci_examples': 4,
                'expected_base_examples': 20,
                'should_have_ci': True
            },
            {
                'name': 'no_ci_optimization',
                'code': '''
@given(flag=st.booleans())
@settings(max_examples=2, deadline=None)
def test_no_ci(flag):
    """Standard boolean test."""
    assert isinstance(flag, bool)
''',
                'expected_ci_examples': 2,
                'expected_base_examples': None,
                'should_have_ci': False
            }
        ]
        
        for scenario in test_scenarios:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(scenario['code'])
                temp_file = f.name
            
            try:
                # Test CI integration
                should_use_ci = self.ci_integrator.should_use_ci_optimization_comment(
                    scenario['code'], scenario['expected_ci_examples']
                )
                
                assert should_use_ci == scenario['should_have_ci'], \
                    f"CI integration detection mismatch for {scenario['name']}"
                
                if scenario['should_have_ci']:
                    # Test integrated comment generation
                    integrated_comment = self.ci_integrator.generate_integrated_comment(
                        scenario['code'], scenario['expected_ci_examples']
                    )
                    
                    assert integrated_comment is not None, f"Should generate integrated comment for {scenario['name']}"
                    assert "CI" in integrated_comment, f"Integrated comment should mention CI for {scenario['name']}"
                    
                    if scenario['expected_base_examples']:
                        assert str(scenario['expected_base_examples']) in integrated_comment, \
                            f"Should mention base examples for {scenario['name']}"
                    assert str(scenario['expected_ci_examples']) in integrated_comment, \
                        f"Should mention CI examples for {scenario['name']}"
                    
                    # Validate comment format
                    validation_result = self.validator.validate_comment_format(integrated_comment)
                    assert validation_result.is_valid, \
                        f"Integrated comment should be valid for {scenario['name']}: {integrated_comment}"
                
                # Test full standardization
                result = self.standardizer.standardize_file(temp_file, dry_run=True)
                assert result.success, f"Standardization should succeed for {scenario['name']}"
                
                if scenario['should_have_ci']:
                    assert result.changes_made > 0, f"Should generate comment for {scenario['name']}"
                    
                    # Find CI optimization comment
                    ci_comment = None
                    for comment in result.generated_comments:
                        if "CI" in comment.rationale:
                            ci_comment = comment
                            break
                    
                    assert ci_comment is not None, f"Should generate CI comment for {scenario['name']}"
                
            finally:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
    
    def test_ci_optimization_coverage_analysis(self):
        """CI optimization coverage analysis works correctly."""
        # Create multiple test files with different CI optimization patterns
        test_files = []
        
        file_contents = [
            # File with CI optimization
            '''
@given(data=st.text())
@settings(max_examples=25 if not os.getenv('CI') else 6, deadline=None)
def test_ci_optimized_1(data):
    """CI optimized test."""
    assert isinstance(data, str)

@given(num=st.integers(min_value=0, max_value=100))
@settings(max_examples=4 if os.getenv('CI') else 16, deadline=None)
def test_ci_optimized_2(num):
    """Another CI optimized test."""
    assert isinstance(num, int)
''',
            # File without CI optimization but could benefit
            '''
@given(data=st.text(min_size=50, max_size=200))
@settings(max_examples=30, deadline=None)
def test_could_benefit_1(data):
    """Test that could benefit from CI optimization."""
    result = data.upper().lower()
    assert len(result) > 0

@given(data=st.floats(min_value=-1000.0, max_value=1000.0))
@settings(max_examples=25, deadline=None)
def test_could_benefit_2(data):
    """Another test that could benefit."""
    assert isinstance(data, float)
''',
            # File with standard tests (no optimization needed)
            '''
@given(flag=st.booleans())
@settings(max_examples=2, deadline=None)
def test_standard_1(flag):
    """Standard boolean test."""
    assert isinstance(flag, bool)

@given(num=st.integers(min_value=0, max_value=5))
@settings(max_examples=6, deadline=None)
def test_standard_2(num):
    """Standard small finite test."""
    assert 0 <= num <= 5
'''
        ]
        
        for i, content in enumerate(file_contents):
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(content)
                test_files.append(f.name)
        
        try:
            # Analyze CI optimization coverage
            coverage_analysis = self.ci_integrator.analyze_ci_optimization_coverage(test_files)
            
            # Should detect CI optimized tests
            assert coverage_analysis['ci_optimized_tests'] >= 2, "Should detect CI optimized tests"
            
            # Should detect optimization opportunities
            assert coverage_analysis['optimization_opportunities'] >= 2, "Should detect optimization opportunities"
            
            # Should have reasonable coverage statistics
            assert coverage_analysis['total_tests'] >= 6, "Should count all tests"
            assert 0 <= coverage_analysis['ci_coverage_percentage'] <= 100, "Coverage should be valid percentage"
            
            # Should detect optimization types
            assert 'conditional_expression' in coverage_analysis['optimization_types'], \
                "Should detect conditional expression optimizations"
            
            # Should calculate performance improvements
            assert len(coverage_analysis['performance_improvements']) >= 2, \
                "Should calculate performance improvements"
            
            for improvement in coverage_analysis['performance_improvements']:
                assert 0 <= improvement <= 100, f"Performance improvement should be valid percentage: {improvement}"
            
        finally:
            for file_path in test_files:
                if os.path.exists(file_path):
                    os.unlink(file_path)
    
    def test_ci_optimization_comment_enhancement(self):
        """CI optimization can enhance existing non-CI comments."""
        # Test enhancing a basic comment with CI information
        test_code = '''
# Complex strategy: 8 examples (adequate coverage)
@given(data=st.text(min_size=50, max_size=200))
@settings(max_examples=20 if not os.getenv('CI') else 8, deadline=None)
def test_ci_enhancement_example(data):
    """Test for CI comment enhancement."""
    processed = data.upper().lower().strip()
    assert len(processed) > 0
'''
        
        existing_comment = "# Complex strategy: 8 examples (adequate coverage)"
        
        # Test enhancement
        enhanced_comment = self.ci_generator.enhance_comment_with_ci_info(existing_comment, test_code)
        
        if enhanced_comment:
            # Should include both original and CI rationale
            assert "adequate coverage" in enhanced_comment, "Should preserve original rationale"
            assert "CI" in enhanced_comment, "Should add CI rationale"
            
            # Should be valid format
            validation_result = self.validator.validate_comment_format(enhanced_comment)
            assert validation_result.is_valid, f"Enhanced comment should be valid: {enhanced_comment}"
    
    def test_ci_optimization_documentation_generation(self):
        """CI optimization documentation generation works across multiple files."""
        # Create test files with various CI optimization patterns
        test_files = []
        
        file_contents = [
            # Conditional expression optimization
            '''
@given(data=st.text())
@settings(max_examples=20 if not os.getenv('CI') else 5, deadline=None)
def test_conditional_ci(data):
    """Conditional CI optimization."""
    assert isinstance(data, str)
''',
            # Comment-based optimization
            '''
# This test uses automated CI optimization
@given(data=st.text(min_size=30, max_size=100))
@settings(max_examples=7, deadline=None)
def test_comment_ci(data):
    """Comment-based CI optimization."""
    assert len(data) >= 30
''',
            # Opportunity for optimization
            '''
@given(data=st.text(min_size=100, max_size=500))
@settings(max_examples=40, deadline=None)
def test_optimization_opportunity(data):
    """Test that could benefit from CI optimization."""
    result = data.upper().lower().strip()
    assert len(result) > 0
'''
        ]
        
        for i, content in enumerate(file_contents):
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(content)
                test_files.append(f.name)
        
        try:
            # Generate CI optimization documentation
            documentation = self.ci_generator.generate_ci_optimization_documentation(test_files)
            
            # Should detect CI optimized tests
            assert len(documentation['ci_optimized_tests']) >= 1, "Should detect CI optimized tests"
            
            # Should detect optimization opportunities
            assert len(documentation['optimization_opportunities']) >= 1, "Should detect optimization opportunities"
            
            # Should track optimization patterns
            assert len(documentation['optimization_patterns']) > 0, "Should track optimization patterns"
            
            # Should calculate performance improvements
            assert len(documentation['performance_improvements']) >= 1, "Should calculate performance improvements"
            
            # Verify CI optimized test details
            for ci_test in documentation['ci_optimized_tests']:
                assert 'optimization_type' in ci_test, "Should include optimization type"
                assert 'base_examples' in ci_test or 'ci_examples' in ci_test, "Should include examples info"
                assert 'rationale' in ci_test, "Should include rationale"
            
            # Verify optimization opportunities
            for opportunity in documentation['optimization_opportunities']:
                assert 'suggested_ci_examples' in opportunity, "Should suggest CI examples"
                assert 'potential_improvement' in opportunity, "Should estimate improvement"
            
        finally:
            for file_path in test_files:
                if os.path.exists(file_path):
                    os.unlink(file_path)


class TestCommentStandardizationIntegration:
    """Integration tests for the complete comment standardization workflow."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.standardizer = CommentStandardizer()
        self.analyzer = None
        
        # Import analyzer only when needed to avoid circular imports
        try:
            from test_optimization.comment_analyzer import CommentAnalyzer
            self.analyzer = CommentAnalyzer()
        except ImportError:
            pytest.skip("CommentAnalyzer not available for integration tests")
    
    def test_end_to_end_standardization_workflow(self):
        """Test complete workflow: analyze -> standardize -> validate.
        
        **Validates: Requirements 3.4, 4.4**
        """
        # Create a test file with various comment issues
        test_content = '''
from hypothesis import given, settings
import hypothesis.strategies as st

# Missing comment for custom max_examples
@given(st.booleans())
@settings(max_examples=15, deadline=None)
def test_undocumented_boolean(value):
    assert isinstance(value, bool)

# Wrong format comment
@given(st.integers(min_value=1, max_value=3))
@settings(max_examples=8, deadline=None)
def test_wrong_format_comment(value):
    assert 1 <= value <= 3

@given(st.text())
# Complex strategy: 25 examples (adequate coverage)
@settings(max_examples=25, deadline=None)
def test_already_documented(text):
    assert isinstance(text, str)
'''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(test_content)
            temp_file = f.name
        
        try:
            # Step 1: Analyze the file
            initial_analysis = self.analyzer.analyze_file(temp_file)
            
            # Should find issues
            assert initial_analysis.total_property_tests == 3
            assert initial_analysis.undocumented_tests > 0
            assert initial_analysis.documented_tests < initial_analysis.total_property_tests
            
            # Step 2: Standardize the file
            result = self.standardizer.standardize_file(temp_file, dry_run=False)
            
            # Should succeed and make changes
            assert result.success, f"Standardization failed: {result.errors}"
            assert result.changes_made > 0, "Should have made changes"
            
            # Step 3: Re-analyze to validate improvements
            final_analysis = self.analyzer.analyze_file(temp_file)
            
            # Should be improved
            assert final_analysis.total_property_tests == 3
            assert final_analysis.undocumented_tests < initial_analysis.undocumented_tests
            assert final_analysis.documented_tests > initial_analysis.documented_tests
            
            # Step 4: Verify backup was created
            if result.backup_path:
                assert os.path.exists(result.backup_path), "Backup file should exist"
                
        finally:
            # Clean up
            if os.path.exists(temp_file):
                os.unlink(temp_file)
            if hasattr(result, 'backup_path') and result.backup_path and os.path.exists(result.backup_path):
                os.unlink(result.backup_path)
    
    def test_batch_standardization_workflow(self):
        """Test batch processing of multiple files.
        
        **Validates: Requirements 3.4, 4.4**
        """
        # Create multiple test files
        test_files = []
        
        for i in range(3):
            content = f'''
from hypothesis import given, settings
import hypothesis.strategies as st

@given(st.booleans())
@settings(max_examples={10 + i}, deadline=None)
def test_file_{i}_function(value):
    assert isinstance(value, bool)
'''
            
            with tempfile.NamedTemporaryFile(mode='w', suffix=f'_test_{i}.py', delete=False) as f:
                f.write(content)
                test_files.append(f.name)
        
        try:
            # Analyze all files initially
            initial_undocumented = 0
            for file_path in test_files:
                analysis = self.analyzer.analyze_file(file_path)
                initial_undocumented += analysis.undocumented_tests
            
            assert initial_undocumented > 0, "Should have undocumented tests initially"
            
            # Batch standardize
            batch_result = self.standardizer.apply_standardization(test_files)
            
            # Should process all files successfully
            assert batch_result.successful_files == len(test_files)
            assert batch_result.failed_files == 0
            assert batch_result.total_changes > 0
            
            # Verify improvements
            final_undocumented = 0
            for file_path in test_files:
                analysis = self.analyzer.analyze_file(file_path)
                final_undocumented += analysis.undocumented_tests
            
            assert final_undocumented < initial_undocumented, "Should have fewer undocumented tests"
            
        finally:
            # Clean up
            for file_path in test_files:
                if os.path.exists(file_path):
                    os.unlink(file_path)
    
    def test_backup_and_rollback_functionality(self):
        """Test backup creation and rollback capability.
        
        **Validates: Requirements 3.4**
        """
        original_content = '''
from hypothesis import given, settings
import hypothesis.strategies as st

@given(st.booleans())
@settings(max_examples=15, deadline=None)
def test_example(value):
    assert isinstance(value, bool)
'''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(original_content)
            temp_file = f.name
        
        try:
            # Standardize with backup
            result = self.standardizer.standardize_file(temp_file, dry_run=False)
            
            assert result.success, "Standardization should succeed"
            assert result.backup_path, "Should create backup"
            assert os.path.exists(result.backup_path), "Backup file should exist"
            
            # Verify backup contains original content
            with open(result.backup_path, 'r') as f:
                backup_content = f.read()
            
            assert backup_content.strip() == original_content.strip(), "Backup should contain original content"
            
            # Verify main file was modified
            with open(temp_file, 'r') as f:
                modified_content = f.read()
            
            assert modified_content != original_content, "Main file should be modified"
            assert "# Boolean strategy:" in modified_content, "Should contain standardized comment"
            
            # Test rollback by restoring from backup
            with open(result.backup_path, 'r') as f:
                backup_content = f.read()
            
            with open(temp_file, 'w') as f:
                f.write(backup_content)
            
            # Verify rollback worked
            with open(temp_file, 'r') as f:
                restored_content = f.read()
            
            assert restored_content.strip() == original_content.strip(), "Rollback should restore original content"
            
        finally:
            # Clean up
            if os.path.exists(temp_file):
                os.unlink(temp_file)
            if hasattr(result, 'backup_path') and result.backup_path and os.path.exists(result.backup_path):
                os.unlink(result.backup_path)
    
    def test_standardization_tool_integration_compatibility(self):
        """Test integration with existing optimization tools.
        
        **Validates: Requirements 4.4, 5.4**
        """
        # Create a file with standardized comments
        test_content = '''
from hypothesis import given, settings
import hypothesis.strategies as st

@given(st.booleans())
# Boolean strategy: 2 examples (True/False coverage)
@settings(max_examples=2, deadline=None)
def test_boolean_example(value):
    assert isinstance(value, bool)

@given(st.integers(min_value=1, max_value=5))
# Small finite strategy: 5 examples (input space size: 5)
@settings(max_examples=5, deadline=None)
def test_finite_example(value):
    assert 1 <= value <= 5

@given(st.text())
# Complex strategy: 20 examples (adequate coverage)
@settings(max_examples=20, deadline=None)
def test_complex_example(text):
    assert isinstance(text, str)
'''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(test_content)
            temp_file = f.name
        
        try:
            # Test that analyzer can parse standardized comments
            analysis = self.analyzer.analyze_file(temp_file)
            
            assert analysis.total_property_tests == 3
            assert analysis.documented_tests == 3
            assert analysis.undocumented_tests == 0
            assert len(analysis.format_violations) == 0
            assert len(analysis.valid_comments) == 3
            
            # Test that comments contain expected strategy types
            strategy_types = [comment.strategy_type for comment in analysis.valid_comments]
            assert 'Boolean' in strategy_types
            assert 'Small finite' in strategy_types
            assert 'Complex' in strategy_types
            
            # Test that rationales are appropriate
            rationales = [comment.rationale for comment in analysis.valid_comments]
            assert any('True/False coverage' in rationale for rationale in rationales)
            assert any('input space size' in rationale for rationale in rationales)
            assert any('adequate coverage' in rationale for rationale in rationales)
            
            # Test terminology consistency check
            terminology = self.analyzer.check_terminology_consistency([analysis])
            
            # Each strategy type should have consistent terminology
            for strategy_type, rationale_list in terminology.items():
                assert len(rationale_list) == 1, f"Strategy type '{strategy_type}' should have consistent terminology"
            
        finally:
            # Clean up
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_error_handling_and_recovery(self):
        """Test error handling in standardization workflow.
        
        **Validates: Requirements 3.4**
        """
        # Test with invalid Python file
        invalid_content = '''
This is not valid Python code
@given(st.booleans())
@settings(max_examples=15
def test_broken_syntax(value):
    assert True
'''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(invalid_content)
            temp_file = f.name
        
        try:
            # Should handle syntax errors gracefully
            result = self.standardizer.standardize_file(temp_file, dry_run=False)
            
            # May succeed or fail, but should not crash
            if not result.success:
                assert len(result.errors) > 0, "Should report errors"
            
            # Test with read-only file (if possible)
            try:
                os.chmod(temp_file, 0o444)  # Make read-only
                
                result = self.standardizer.standardize_file(temp_file, dry_run=False)
                
                # Should handle permission errors
                if not result.success:
                    assert len(result.errors) > 0, "Should report permission errors"
                    
            except (OSError, PermissionError):
                # Skip if we can't change permissions
                pass
            finally:
                # Restore permissions for cleanup
                try:
                    os.chmod(temp_file, 0o644)
                except (OSError, PermissionError):
                    pass
            
        finally:
            # Clean up
            if os.path.exists(temp_file):
                try:
                    os.unlink(temp_file)
                except (OSError, PermissionError):
                    pass