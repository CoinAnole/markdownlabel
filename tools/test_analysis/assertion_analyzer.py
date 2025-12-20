"""
Test assertion analyzer for identifying assertion patterns in test methods.

This module analyzes test method bodies to identify different types of assertions,
particularly distinguishing between rebuild-related assertions and value-only assertions.
"""

import ast
import re
from dataclasses import dataclass
from typing import List, Set, Optional, Dict, Any
from enum import Enum


class AssertionType(Enum):
    """Types of assertions found in test methods."""
    REBUILD = "rebuild"
    VALUE_CHANGE = "value_change"
    EXISTENCE = "existence"
    EQUALITY = "equality"
    BOOLEAN = "boolean"
    EXCEPTION = "exception"
    UNKNOWN = "unknown"


@dataclass
class AssertionPattern:
    """Represents an assertion pattern found in a test method."""
    assertion_type: AssertionType
    line_number: int
    code: str
    confidence: float  # 0.0 to 1.0, how confident we are in the classification
    details: Dict[str, Any]  # Additional context about the assertion


@dataclass
class TestAssertionAnalysis:
    """Analysis results for a single test method."""
    test_name: str
    file_path: str
    line_number: int
    assertions: List[AssertionPattern]
    has_rebuild_assertions: bool
    has_value_assertions: bool
    primary_assertion_type: AssertionType
    naming_mismatch_detected: bool
    suggested_name_pattern: Optional[str]


class AssertionAnalyzer:
    """Analyzes test methods to identify assertion patterns."""
    
    def __init__(self):
        """Initialize the assertion analyzer with pattern definitions."""
        # Patterns that indicate rebuild testing
        self.rebuild_patterns = [
            r'widget_id\s*!=\s*widget\.id',
            r'widget\.id\s*!=\s*\w+',  # widget.id != old_id pattern
            r'\w+\s*!=\s*widget\.id',  # old_id != widget.id pattern
            r'id\s*\(\s*\w+\s*\)\s*!=\s*id\s*\(\s*\w+\s*\)',
            r'collect_widget_ids\s*\(',
            r'assert_rebuild\s*\(',
            r'assert_no_rebuild\s*\(',
            r'rebuild.*occurred',
            r'widget.*recreated',
            r'identity.*changed',
            r'is\s+not\s+',  # Identity comparison
        ]
        
        # Patterns that indicate value-only testing
        self.value_patterns = [
            r'\.text\s*==',
            r'\.color\s*==',
            r'\.font_size\s*==',
            r'\.font_name\s*==',
            r'\.padding\s*==',
            r'assertEqual\s*\(',
            r'assert\s+\w+\s*==',
            r'assert.*equal',
            r'\.markup\s*==',
            r'\.halign\s*==',
            r'\.valign\s*==',
        ]
        
        # Patterns that indicate existence testing
        self.existence_patterns = [
            r'assert\s+\w+\s+is\s+not\s+None',
            r'assert\s+\w+',
            r'assertTrue\s*\(',
            r'assertFalse\s*\(',
            r'assertIsNotNone\s*\(',
            r'assertIsNone\s*\(',
        ]
        
        # Patterns that indicate exception testing
        self.exception_patterns = [
            r'assertRaises\s*\(',
            r'pytest\.raises\s*\(',
            r'with\s+raises\s*\(',
            r'except\s+\w+',
        ]
        
        # Compile patterns for efficiency
        self.compiled_rebuild_patterns = [re.compile(p, re.IGNORECASE) for p in self.rebuild_patterns]
        self.compiled_value_patterns = [re.compile(p, re.IGNORECASE) for p in self.value_patterns]
        self.compiled_existence_patterns = [re.compile(p, re.IGNORECASE) for p in self.existence_patterns]
        self.compiled_exception_patterns = [re.compile(p, re.IGNORECASE) for p in self.exception_patterns]
    
    def analyze_test_method(self, test_method_node: ast.FunctionDef, file_path: str) -> TestAssertionAnalysis:
        """Analyze a single test method for assertion patterns.
        
        Args:
            test_method_node: AST node for the test method
            file_path: Path to the file containing the test
            
        Returns:
            TestAssertionAnalysis with detailed assertion information
        """
        assertions = self._extract_assertions(test_method_node)
        
        # Classify assertions
        has_rebuild = any(a.assertion_type == AssertionType.REBUILD for a in assertions)
        has_value = any(a.assertion_type == AssertionType.VALUE_CHANGE for a in assertions)
        
        # Determine primary assertion type
        primary_type = self._determine_primary_assertion_type(assertions)
        
        # Check for naming mismatches
        naming_mismatch = self._detect_naming_mismatch(test_method_node.name, primary_type, has_rebuild)
        suggested_name = self._suggest_name_pattern(test_method_node.name, primary_type, has_rebuild)
        
        return TestAssertionAnalysis(
            test_name=test_method_node.name,
            file_path=file_path,
            line_number=test_method_node.lineno,
            assertions=assertions,
            has_rebuild_assertions=has_rebuild,
            has_value_assertions=has_value,
            primary_assertion_type=primary_type,
            naming_mismatch_detected=naming_mismatch,
            suggested_name_pattern=suggested_name
        )
    
    def _extract_assertions(self, test_method_node: ast.FunctionDef) -> List[AssertionPattern]:
        """Extract all assertions from a test method."""
        assertions = []
        
        # Walk through all nodes in the test method
        for node in ast.walk(test_method_node):
            if isinstance(node, ast.Assert):
                assertion = self._analyze_assert_node(node)
                if assertion:
                    assertions.append(assertion)
            elif isinstance(node, ast.Call):
                assertion = self._analyze_call_node(node)
                if assertion:
                    assertions.append(assertion)
        
        return assertions
    
    def _analyze_assert_node(self, node: ast.Assert) -> Optional[AssertionPattern]:
        """Analyze an assert statement node."""
        try:
            # Convert the assertion to source code
            if hasattr(ast, 'unparse'):
                code = ast.unparse(node)
            else:
                # Fallback for older Python versions
                code = ast.dump(node)
            
            assertion_type, confidence, details = self._classify_assertion_code(code)
            
            return AssertionPattern(
                assertion_type=assertion_type,
                line_number=node.lineno,
                code=code,
                confidence=confidence,
                details=details
            )
        except Exception:
            # If we can't parse the assertion, return unknown type
            return AssertionPattern(
                assertion_type=AssertionType.UNKNOWN,
                line_number=node.lineno,
                code="<unparseable>",
                confidence=0.0,
                details={}
            )
    
    def _analyze_call_node(self, node: ast.Call) -> Optional[AssertionPattern]:
        """Analyze a function call that might be an assertion."""
        try:
            # Convert the call to source code
            if hasattr(ast, 'unparse'):
                code = ast.unparse(node)
            else:
                code = ast.dump(node)
            
            # Check if this looks like an assertion method call
            if any(pattern in code.lower() for pattern in ['assert', 'equal', 'true', 'false', 'none', 'raises']):
                assertion_type, confidence, details = self._classify_assertion_code(code)
                
                return AssertionPattern(
                    assertion_type=assertion_type,
                    line_number=node.lineno,
                    code=code,
                    confidence=confidence,
                    details=details
                )
        except Exception:
            pass
        
        return None
    
    def _classify_assertion_code(self, code: str) -> tuple[AssertionType, float, Dict[str, Any]]:
        """Classify assertion code into assertion types.
        
        Returns:
            Tuple of (assertion_type, confidence, details)
        """
        details = {"matched_patterns": []}
        
        # Check for rebuild patterns (highest priority)
        for pattern in self.compiled_rebuild_patterns:
            if pattern.search(code):
                details["matched_patterns"].append(pattern.pattern)
                return AssertionType.REBUILD, 0.9, details
        
        # Check for exception patterns
        for pattern in self.compiled_exception_patterns:
            if pattern.search(code):
                details["matched_patterns"].append(pattern.pattern)
                return AssertionType.EXCEPTION, 0.8, details
        
        # Check for value patterns
        for pattern in self.compiled_value_patterns:
            if pattern.search(code):
                details["matched_patterns"].append(pattern.pattern)
                return AssertionType.VALUE_CHANGE, 0.8, details
        
        # Check for existence patterns
        for pattern in self.compiled_existence_patterns:
            if pattern.search(code):
                details["matched_patterns"].append(pattern.pattern)
                return AssertionType.EXISTENCE, 0.7, details
        
        # Check for basic equality
        if '==' in code or '!=' in code:
            return AssertionType.EQUALITY, 0.6, details
        
        # Check for boolean assertions
        if any(word in code.lower() for word in ['true', 'false']):
            return AssertionType.BOOLEAN, 0.6, details
        
        return AssertionType.UNKNOWN, 0.0, details
    
    def _determine_primary_assertion_type(self, assertions: List[AssertionPattern]) -> AssertionType:
        """Determine the primary assertion type for a test method."""
        if not assertions:
            return AssertionType.UNKNOWN
        
        # Count assertion types by confidence-weighted score
        type_scores = {}
        for assertion in assertions:
            score = assertion.confidence
            if assertion.assertion_type in type_scores:
                type_scores[assertion.assertion_type] += score
            else:
                type_scores[assertion.assertion_type] = score
        
        # Return the type with the highest score
        if type_scores:
            return max(type_scores.items(), key=lambda x: x[1])[0]
        
        return AssertionType.UNKNOWN
    
    def _detect_naming_mismatch(self, test_name: str, primary_type: AssertionType, has_rebuild: bool) -> bool:
        """Detect if test name doesn't match its assertion patterns."""
        name_lower = test_name.lower()
        
        # Check for rebuild naming mismatches
        if 'rebuild' in name_lower or 'trigger' in name_lower:
            # Test name suggests rebuild testing, but no rebuild assertions found
            return not has_rebuild
        
        # Check for value change naming mismatches
        if any(word in name_lower for word in ['update', 'change', 'set', 'modify']):
            # Test name suggests value changes, but primary type is rebuild
            return primary_type == AssertionType.REBUILD
        
        return False
    
    def _suggest_name_pattern(self, current_name: str, primary_type: AssertionType, has_rebuild: bool) -> Optional[str]:
        """Suggest a better name pattern for the test."""
        base_name = current_name.replace('test_', '', 1)
        
        # Remove common suffixes to get the base name
        suffixes_to_remove = [
            '_triggers_rebuild', '_updates_value', '_changes_property',
            '_sets_property', '_modifies_property', '_exists',
            '_raises_exception', '_validates', '_handles'
        ]
        
        for suffix in suffixes_to_remove:
            if base_name.endswith(suffix):
                base_name = base_name[:-len(suffix)]
                break
        
        if primary_type == AssertionType.REBUILD or has_rebuild:
            return f"test_{base_name}_triggers_rebuild"
        elif primary_type == AssertionType.VALUE_CHANGE:
            return f"test_{base_name}_updates_value"
        elif primary_type == AssertionType.EXISTENCE:
            return f"test_{base_name}_exists"
        elif primary_type == AssertionType.EXCEPTION:
            return f"test_{base_name}_raises_exception"
        
        return None
    
    def analyze_file(self, file_path: str) -> List[TestAssertionAnalysis]:
        """Analyze all test methods in a file.
        
        Args:
            file_path: Path to the Python test file
            
        Returns:
            List of TestAssertionAnalysis for all test methods in the file
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
        except (IOError, SyntaxError) as e:
            print(f"Warning: Failed to parse {file_path}: {e}")
            return []
        
        analyses = []
        
        # Find all test methods (both in classes and at module level)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
                analysis = self.analyze_test_method(node, file_path)
                analyses.append(analysis)
        
        return analyses


def main():
    """Command-line interface for testing the assertion analyzer."""
    import sys
    from pathlib import Path
    
    if len(sys.argv) != 2:
        print("Usage: python assertion_analyzer.py <test_file_or_directory>")
        sys.exit(1)
    
    path = Path(sys.argv[1])
    analyzer = AssertionAnalyzer()
    
    if path.is_file():
        analyses = analyzer.analyze_file(str(path))
        print(f"Analyzed {len(analyses)} test methods in {path}")
        
        for analysis in analyses:
            print(f"\n{analysis.test_name}:")
            print(f"  Primary type: {analysis.primary_assertion_type.value}")
            print(f"  Has rebuild assertions: {analysis.has_rebuild_assertions}")
            print(f"  Has value assertions: {analysis.has_value_assertions}")
            print(f"  Naming mismatch: {analysis.naming_mismatch_detected}")
            if analysis.suggested_name_pattern:
                print(f"  Suggested name: {analysis.suggested_name_pattern}")
            print(f"  Assertions: {len(analysis.assertions)}")
            
    elif path.is_dir():
        total_analyses = 0
        mismatches = 0
        
        for test_file in path.glob('test_*.py'):
            analyses = analyzer.analyze_file(str(test_file))
            total_analyses += len(analyses)
            mismatches += sum(1 for a in analyses if a.naming_mismatch_detected)
            
            if analyses:
                print(f"\n{test_file.name}: {len(analyses)} tests")
                for analysis in analyses:
                    if analysis.naming_mismatch_detected:
                        print(f"  MISMATCH: {analysis.test_name} -> {analysis.suggested_name_pattern}")
        
        print(f"\nSummary: {total_analyses} tests analyzed, {mismatches} naming mismatches found")
    
    else:
        print(f"Error: {path} is not a valid file or directory")
        sys.exit(1)


if __name__ == "__main__":
    main()