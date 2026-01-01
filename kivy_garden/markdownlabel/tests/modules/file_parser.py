"""
AST-based test file parser for analyzing test methods, classes, and helper functions.

This module provides functionality to parse Python test files and extract
metadata about test methods, test classes, and helper functions for analysis.
"""

import ast
import os
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set
from pathlib import Path


@dataclass
class ParsedMethod:
    """Represents a test method with its metadata."""
    name: str
    class_name: Optional[str]
    docstring: Optional[str]
    line_number: int
    decorators: List[str]
    assertions: List[str]  # Types of assertions found
    has_rebuild_assertions: bool
    has_value_assertions: bool
    file_path: str


@dataclass
class ParsedClass:
    """Represents a test class with its metadata."""
    name: str
    docstring: Optional[str]
    line_number: int
    methods: List[ParsedMethod]
    helper_methods: List[str]  # Non-test methods in the class
    file_path: str


@dataclass
class HelperFunction:
    """Represents a helper function with its metadata."""
    name: str
    line_number: int
    docstring: Optional[str]
    parameters: List[str]
    body_hash: str  # Hash of function body for duplicate detection
    file_path: str
    is_private: bool  # Starts with underscore


@dataclass
class FileMetadata:
    """Complete metadata for a test file."""
    file_path: str
    test_classes: List[ParsedClass] = field(default_factory=list)
    test_methods: List[ParsedMethod] = field(default_factory=list)  # Module-level test functions
    helper_functions: List[HelperFunction] = field(default_factory=list)
    imports: List[str] = field(default_factory=list)
    pytest_markers: Set[str] = field(default_factory=set)


class FileParser:
    """AST-based parser for extracting test file metadata."""

    def __init__(self):
        self.current_file_path = ""

    def parse_file(self, file_path: str) -> FileMetadata:
        """Parse a Python test file and extract metadata.

        Args:
            file_path: Path to the Python test file

        Returns:
            FileMetadata containing all extracted information
        """
        self.current_file_path = file_path

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            raise ValueError(f"Failed to parse {file_path}: {e}")

        metadata = FileMetadata(file_path=file_path)

        # Extract imports
        metadata.imports = self._extract_imports(tree)

        # Extract pytest markers used in the file
        metadata.pytest_markers = self._extract_pytest_markers(tree)

        # Process top-level nodes
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                if self._is_test_class(node):
                    test_class = self._parse_test_class(node)
                    metadata.test_classes.append(test_class)

                    # Also extract helper methods from test classes
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            if not self._is_test_function(item) and not item.name.startswith("__"):
                                helper_func = self._parse_helper_function(item)
                                metadata.helper_functions.append(helper_func)
            elif isinstance(node, ast.FunctionDef):
                if self._is_test_function(node):
                    test_method = self._parse_test_method(node, None)
                    metadata.test_methods.append(test_method)
                elif self._is_helper_function(node):
                    helper_func = self._parse_helper_function(node)
                    metadata.helper_functions.append(helper_func)

        return metadata

    def parse_directory(self, directory_path: str) -> Dict[str, FileMetadata]:
        """Parse all Python test files in a directory.

        Args:
            directory_path: Path to directory containing test files

        Returns:
            Dictionary mapping file paths to their metadata
        """
        results = {}
        test_dir = Path(directory_path)

        for file_path in test_dir.glob("test_*.py"):
            if file_path.is_file():
                try:
                    metadata = self.parse_file(str(file_path))
                    results[str(file_path)] = metadata
                except Exception as e:
                    print(f"Warning: Failed to parse {file_path}: {e}")

        return results

    def _extract_imports(self, tree: ast.AST) -> List[str]:
        """Extract import statements from the AST."""
        imports = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    imports.append(f"{module}.{alias.name}")

        return imports

    def _extract_pytest_markers(self, tree: ast.AST) -> Set[str]:
        """Extract pytest markers used in the file."""
        markers = set()

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                for decorator in node.decorator_list:
                    marker = self._extract_pytest_marker(decorator)
                    if marker:
                        markers.add(marker)

        return markers

    def _extract_pytest_marker(self, decorator: ast.expr) -> Optional[str]:
        """Extract pytest marker name from a decorator."""
        if isinstance(decorator, ast.Attribute):
            if (isinstance(decorator.value, ast.Attribute) and
                    isinstance(decorator.value.value, ast.Name) and
                    decorator.value.value.id == "pytest" and
                    decorator.value.attr == "mark"):
                return decorator.attr
        elif isinstance(decorator, ast.Call):
            return self._extract_pytest_marker(decorator.func)

        return None

    def _is_test_class(self, node: ast.ClassDef) -> bool:
        """Check if a class is a test class."""
        return node.name.startswith("Test")

    def _is_test_function(self, node: ast.FunctionDef) -> bool:
        """Check if a function is a test function."""
        return node.name.startswith("test_")

    def _is_helper_function(self, node: ast.FunctionDef) -> bool:
        """Check if a function is a helper function (not a test)."""
        return not node.name.startswith("test_") and not node.name.startswith("__")

    def _parse_test_class(self, node: ast.ClassDef) -> ParsedClass:
        """Parse a test class and extract its metadata."""
        test_class = ParsedClass(
            name=node.name,
            docstring=ast.get_docstring(node),
            line_number=node.lineno,
            methods=[],
            helper_methods=[],
            file_path=self.current_file_path
        )

        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                if self._is_test_function(item):
                    test_method = self._parse_test_method(item, node.name)
                    test_class.methods.append(test_method)
                elif not item.name.startswith("__"):
                    test_class.helper_methods.append(item.name)

        return test_class

    def _parse_test_method(self, node: ast.FunctionDef, class_name: Optional[str]) -> ParsedMethod:
        """Parse a test method and extract its metadata."""
        decorators = []
        for decorator in node.decorator_list:
            decorators.append(self._decorator_to_string(decorator))

        assertions = self._extract_assertions(node)

        return ParsedMethod(
            name=node.name,
            class_name=class_name,
            docstring=ast.get_docstring(node),
            line_number=node.lineno,
            decorators=decorators,
            assertions=assertions,
            has_rebuild_assertions=self._has_rebuild_assertions(node),
            has_value_assertions=self._has_value_assertions(node),
            file_path=self.current_file_path
        )

    def _parse_helper_function(self, node: ast.FunctionDef) -> HelperFunction:
        """Parse a helper function and extract its metadata."""
        parameters = [arg.arg for arg in node.args.args]
        body_hash = self._compute_body_hash(node)

        return HelperFunction(
            name=node.name,
            line_number=node.lineno,
            docstring=ast.get_docstring(node),
            parameters=parameters,
            body_hash=body_hash,
            file_path=self.current_file_path,
            is_private=node.name.startswith("_")
        )

    def _decorator_to_string(self, decorator: ast.expr) -> str:
        """Convert a decorator AST node to string representation."""
        if isinstance(decorator, ast.Name):
            return decorator.id
        elif isinstance(decorator, ast.Attribute):
            return f"{self._decorator_to_string(decorator.value)}.{decorator.attr}"
        elif isinstance(decorator, ast.Call):
            func_name = self._decorator_to_string(decorator.func)
            return f"{func_name}(...)"
        else:
            return str(decorator)

    def _extract_assertions(self, node: ast.FunctionDef) -> List[str]:
        """Extract types of assertions used in a test method."""
        assertions = []

        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                if isinstance(child.func, ast.Name) and child.func.id == "assert":
                    assertions.append("assert")
                elif (isinstance(child.func, ast.Attribute) and
                      child.func.attr in ["assertEqual", "assertTrue", "assertFalse",
                                          "assertIn", "assertNotIn", "assertRaises"]):
                    assertions.append(child.func.attr)
            elif isinstance(child, ast.Assert):
                assertions.append("assert")

        return list(set(assertions))  # Remove duplicates

    def _has_rebuild_assertions(self, node: ast.FunctionDef) -> bool:
        """Check if the test method has assertions related to rebuild behavior."""
        rebuild_indicators = [
            "widget_id", "id(", "collect_widget_ids", "rebuild",
            "assert_rebuild", "assert_no_rebuild"
        ]

        source = ast.unparse(node) if hasattr(ast, 'unparse') else ""
        return any(indicator in source for indicator in rebuild_indicators)

    def _has_value_assertions(self, node: ast.FunctionDef) -> bool:
        """Check if the test method has assertions related to value changes."""
        value_indicators = [
            "assert", "assertEqual", "==", "!=", ".text", ".color",
            ".font_size", ".font_name"
        ]

        source = ast.unparse(node) if hasattr(ast, 'unparse') else ""
        return any(indicator in source for indicator in value_indicators)

    def _compute_body_hash(self, node: ast.FunctionDef) -> str:
        """Compute a hash of the function body for duplicate detection."""
        import hashlib

        # Get the function body without the signature
        body_nodes = node.body

        # Convert body to string representation
        if hasattr(ast, 'unparse'):
            body_str = "\n".join(ast.unparse(stmt) for stmt in body_nodes)
        else:
            # Fallback for older Python versions
            body_str = str([ast.dump(stmt) for stmt in body_nodes])

        # Normalize whitespace and compute hash
        normalized = " ".join(body_str.split())
        return hashlib.md5(normalized.encode()).hexdigest()


def main():
    """Command-line interface for testing the parser."""
    import sys

    if len(sys.argv) != 2:
        print("Usage: python test_file_parser.py <test_file_or_directory>")
        sys.exit(1)

    path = sys.argv[1]
    parser = FileParser()

    if os.path.isfile(path):
        metadata = parser.parse_file(path)
        print(f"File: {metadata.file_path}")
        print(f"Test classes: {len(metadata.test_classes)}")
        print(f"Test methods: {len(metadata.test_methods)}")
        print(f"Helper functions: {len(metadata.helper_functions)}")
        print(f"Pytest markers: {metadata.pytest_markers}")
    elif os.path.isdir(path):
        results = parser.parse_directory(path)
        print(f"Parsed {len(results)} test files")
        for file_path, metadata in results.items():
            print(f"\n{file_path}:")
            print(f"  Test classes: {len(metadata.test_classes)}")
            print(f"  Test methods: {len(metadata.test_methods)}")
            print(f"  Helper functions: {len(metadata.helper_functions)}")
    else:
        print(f"Error: {path} is not a valid file or directory")
        sys.exit(1)


if __name__ == "__main__":
    main()
