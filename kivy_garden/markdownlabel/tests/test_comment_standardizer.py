"""Property-based tests for comment standardization functionality.

Tests the CommentStandardizer's ability to generate and apply standardized
comments for property-based tests with proper strategy documentation.
"""

import pytest
import os
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