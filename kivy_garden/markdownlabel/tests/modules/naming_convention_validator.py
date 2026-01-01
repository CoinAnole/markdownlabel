"""
Naming convention validator for test methods.

This module implements rules for consistent test naming patterns and generates
suggested renames for non-compliant tests based on their assertion patterns.
"""

import re
from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum
from pathlib import Path

try:
    from .assertion_analyzer import AssertionAnalyzer, AssertionType, AssertionAnalysis
except ImportError:
    # Handle running as script
    import sys
    sys.path.append(str(Path(__file__).parent))
    from assertion_analyzer import AssertionAnalyzer, AssertionType, AssertionAnalysis


class NamingViolationType(Enum):
    """Types of naming convention violations."""
    REBUILD_MISMATCH = "rebuild_mismatch"  # Name suggests rebuild but no rebuild assertions
    VALUE_MISMATCH = "value_mismatch"      # Name suggests value change but has rebuild assertions
    INCONSISTENT_PATTERN = "inconsistent_pattern"  # Doesn't follow standard patterns
    UNCLEAR_PURPOSE = "unclear_purpose"    # Name doesn't clearly indicate test purpose


@dataclass
class NamingViolation:
    """Represents a naming convention violation."""
    test_name: str
    file_path: str
    line_number: int
    violation_type: NamingViolationType
    current_name: str
    suggested_name: str
    rationale: str
    confidence: float  # 0.0 to 1.0, confidence in the suggestion


@dataclass
class NamingConventionReport:
    """Report of naming convention analysis for a file or directory."""
    violations: List[NamingViolation]
    total_tests: int
    compliant_tests: int
    violation_count: int
    compliance_percentage: float
    patterns_summary: Dict[str, int]  # Pattern -> count


class NamingConventionValidator:
    """Validates and suggests improvements for test naming conventions."""

    def __init__(self):
        """Initialize the validator with naming rules and patterns."""
        self.assertion_analyzer = AssertionAnalyzer()

        # Standard naming patterns we expect
        self.standard_patterns = {
            'triggers_rebuild': r'.*_triggers_rebuild$',
            'updates_value': r'.*_updates_value$',
            'changes_property': r'.*_changes_property$',
            'sets_property': r'.*_sets_\w+$',
            'modifies_property': r'.*_modifies_\w+$',
            'exists': r'.*_exists$',
            'raises_exception': r'.*_raises_\w+$',
            'validates': r'.*_validates_\w+$',
            'handles': r'.*_handles_\w+$',
        }

        # Compile patterns for efficiency
        self.compiled_patterns = {
            name: re.compile(pattern, re.IGNORECASE)
            for name, pattern in self.standard_patterns.items()
        }

        # Words that suggest different test purposes
        self.rebuild_indicators = {'trigger', 'rebuild', 'recreate', 'regenerate'}
        self.value_indicators = {'update', 'change', 'set', 'modify', 'assign'}
        self.existence_indicators = {'exist', 'present', 'available', 'create'}
        self.validation_indicators = {'validate', 'check', 'verify', 'ensure'}
        self.exception_indicators = {'raise', 'throw', 'error', 'fail', 'invalid'}

    def validate_test_method(self, analysis: AssertionAnalysis) -> List[NamingViolation]:
        """Validate a single test method's naming convention.

        Args:
            analysis: AssertionAnalysis from assertion analyzer

        Returns:
            List of NamingViolation objects (empty if compliant)
        """
        violations = []
        test_name = analysis.test_name

        # Check for rebuild naming mismatches
        rebuild_violation = self._check_rebuild_naming(analysis)
        if rebuild_violation:
            violations.append(rebuild_violation)

        # Check for value change naming mismatches
        value_violation = self._check_value_naming(analysis)
        if value_violation:
            violations.append(value_violation)

        # Check for pattern consistency
        pattern_violation = self._check_pattern_consistency(analysis)
        if pattern_violation:
            violations.append(pattern_violation)

        # Check for unclear purpose
        clarity_violation = self._check_naming_clarity(analysis)
        if clarity_violation:
            violations.append(clarity_violation)

        return violations

    def _check_rebuild_naming(self, analysis: AssertionAnalysis) -> Optional[NamingViolation]:
        """Check for rebuild-related naming violations."""
        test_name = analysis.test_name.lower()

        # If name suggests rebuild testing but no rebuild assertions found
        if any(indicator in test_name for indicator in self.rebuild_indicators):
            if not analysis.has_rebuild_assertions:
                suggested_name = self._generate_value_name(
                    analysis.test_name, analysis.primary_assertion_type
                )
                return NamingViolation(
                    test_name=analysis.test_name,
                    file_path=analysis.file_path,
                    line_number=analysis.line_number,
                    violation_type=NamingViolationType.REBUILD_MISMATCH,
                    current_name=analysis.test_name,
                    suggested_name=suggested_name,
                    rationale="Test name suggests rebuild testing but only contains value assertions",
                    confidence=0.8
                )

        return None

    def _check_value_naming(self, analysis: AssertionAnalysis) -> Optional[NamingViolation]:
        """Check for value change naming violations."""
        test_name = analysis.test_name.lower()

        # If name suggests value changes but has rebuild assertions
        if any(indicator in test_name for indicator in self.value_indicators):
            if analysis.has_rebuild_assertions and analysis.primary_assertion_type == AssertionType.REBUILD:
                suggested_name = self._generate_rebuild_name(analysis.test_name)
                return NamingViolation(
                    test_name=analysis.test_name,
                    file_path=analysis.file_path,
                    line_number=analysis.line_number,
                    violation_type=NamingViolationType.VALUE_MISMATCH,
                    current_name=analysis.test_name,
                    suggested_name=suggested_name,
                    rationale="Test name suggests value changes but contains rebuild assertions",
                    confidence=0.8
                )

        return None

    def _check_pattern_consistency(self, analysis: AssertionAnalysis) -> Optional[NamingViolation]:
        """Check if test follows standard naming patterns."""
        test_name = analysis.test_name

        # Check if it matches any standard pattern
        matches_pattern = any(
            pattern.match(test_name) for pattern in self.compiled_patterns.values()
        )

        if not matches_pattern:
            # Generate a suggested name based on assertion type
            suggested_name = self._generate_standard_name(analysis)

            if suggested_name and suggested_name != test_name:
                return NamingViolation(
                    test_name=analysis.test_name,
                    file_path=analysis.file_path,
                    line_number=analysis.line_number,
                    violation_type=NamingViolationType.INCONSISTENT_PATTERN,
                    current_name=analysis.test_name,
                    suggested_name=suggested_name,
                    rationale="Test name doesn't follow standard naming patterns",
                    confidence=0.6
                )

        return None

    def _check_naming_clarity(self, analysis: AssertionAnalysis) -> Optional[NamingViolation]:
        """Check if test name clearly indicates its purpose."""
        test_name = analysis.test_name.lower()

        # Very generic names that don't indicate purpose
        generic_patterns = [
            r'^test_\w+$',  # Just test_something
            r'^test_\w+_\w+$',  # test_something_else (too generic)
        ]

        is_generic = any(re.match(pattern, test_name) for pattern in generic_patterns)

        if is_generic and len(analysis.assertions) > 0:
            suggested_name = self._generate_descriptive_name(analysis)

            if suggested_name and suggested_name != analysis.test_name:
                return NamingViolation(
                    test_name=analysis.test_name,
                    file_path=analysis.file_path,
                    line_number=analysis.line_number,
                    violation_type=NamingViolationType.UNCLEAR_PURPOSE,
                    current_name=analysis.test_name,
                    suggested_name=suggested_name,
                    rationale="Test name is too generic and doesn't clearly indicate purpose",
                    confidence=0.5
                )

        return None

    def _generate_rebuild_name(self, current_name: str) -> str:
        """Generate a rebuild-focused name."""
        base_name = self._extract_base_name(current_name)
        return f"test_{base_name}_triggers_rebuild"

    def _generate_value_name(self, current_name: str, assertion_type: AssertionType) -> str:
        """Generate a value-focused name."""
        base_name = self._extract_base_name(current_name)

        if assertion_type == AssertionType.VALUE_CHANGE:
            return f"test_{base_name}_updates_value"
        elif assertion_type == AssertionType.EXISTENCE:
            return f"test_{base_name}_exists"
        elif assertion_type == AssertionType.EXCEPTION:
            return f"test_{base_name}_raises_exception"
        else:
            return f"test_{base_name}_changes_property"

    def _generate_standard_name(self, analysis: AssertionAnalysis) -> str:
        """Generate a name following standard patterns."""
        base_name = self._extract_base_name(analysis.test_name)

        if analysis.has_rebuild_assertions:
            return f"test_{base_name}_triggers_rebuild"
        elif analysis.primary_assertion_type == AssertionType.VALUE_CHANGE:
            return f"test_{base_name}_updates_value"
        elif analysis.primary_assertion_type == AssertionType.EXISTENCE:
            return f"test_{base_name}_exists"
        elif analysis.primary_assertion_type == AssertionType.EXCEPTION:
            return f"test_{base_name}_raises_exception"
        elif analysis.primary_assertion_type == AssertionType.BOOLEAN:
            return f"test_{base_name}_validates"
        else:
            return f"test_{base_name}_behaves_correctly"

    def _generate_descriptive_name(self, analysis: AssertionAnalysis) -> str:
        """Generate a more descriptive name based on assertions."""
        # Try to infer what the test is doing from its assertions
        assertion_codes = [a.code.lower() for a in analysis.assertions]

        # Look for property names in assertions
        property_names = set()
        for code in assertion_codes:
            # Extract property names like .text, .color, .font_size
            matches = re.findall(r'\.(\w+)', code)
            property_names.update(matches)

        if property_names:
            # Use the first property found
            prop_name = sorted(property_names)[0]
            if analysis.has_rebuild_assertions:
                return f"test_{prop_name}_change_triggers_rebuild"
            else:
                return f"test_{prop_name}_updates_value"

        # Fallback to generic descriptive name
        return self._generate_standard_name(analysis)

    def _extract_base_name(self, test_name: str) -> str:
        """Extract the base name from a test method name."""
        # Remove test_ prefix
        base = test_name.replace('test_', '', 1)

        # Remove common suffixes
        suffixes_to_remove = [
            '_triggers_rebuild', '_updates_value', '_changes_property',
            '_sets_property', '_modifies_property', '_exists',
            '_raises_exception', '_validates', '_handles'
        ]

        for suffix in suffixes_to_remove:
            if base.endswith(suffix):
                base = base[:-len(suffix)]
                break

        return base or 'property'

    def validate_file(self, file_path: str) -> NamingConventionReport:
        """Validate naming conventions for all tests in a file.

        Args:
            file_path: Path to the Python test file

        Returns:
            NamingConventionReport with violations and statistics
        """
        # Get assertion analyses for all test methods
        analyses = self.assertion_analyzer.analyze_file(file_path)

        all_violations = []
        patterns_count = {}

        for analysis in analyses:
            violations = self.validate_test_method(analysis)
            all_violations.extend(violations)

            # Count patterns used
            for pattern_name, pattern in self.compiled_patterns.items():
                if pattern.match(analysis.test_name):
                    patterns_count[pattern_name] = patterns_count.get(pattern_name, 0) + 1
                    break
            else:
                patterns_count['non_standard'] = patterns_count.get('non_standard', 0) + 1

        total_tests = len(analyses)
        violation_count = len(all_violations)
        compliant_tests = total_tests - violation_count
        compliance_percentage = (compliant_tests / total_tests * 100) if total_tests > 0 else 100.0

        return NamingConventionReport(
            violations=all_violations,
            total_tests=total_tests,
            compliant_tests=compliant_tests,
            violation_count=violation_count,
            compliance_percentage=compliance_percentage,
            patterns_summary=patterns_count
        )

    def validate_directory(self, directory_path: str) -> NamingConventionReport:
        """Validate naming conventions for all test files in a directory.

        Args:
            directory_path: Path to directory containing test files

        Returns:
            Aggregated NamingConventionReport for all files
        """
        test_dir = Path(directory_path)
        all_violations = []
        total_tests = 0
        patterns_count = {}

        for test_file in test_dir.glob('test_*.py'):
            if test_file.is_file():
                try:
                    file_report = self.validate_file(str(test_file))
                    all_violations.extend(file_report.violations)
                    total_tests += file_report.total_tests

                    # Merge pattern counts
                    for pattern, count in file_report.patterns_summary.items():
                        patterns_count[pattern] = patterns_count.get(pattern, 0) + count

                except Exception as e:
                    print(f"Warning: Failed to validate {test_file}: {e}")

        violation_count = len(all_violations)
        compliant_tests = total_tests - violation_count
        compliance_percentage = (compliant_tests / total_tests * 100) if total_tests > 0 else 100.0

        return NamingConventionReport(
            violations=all_violations,
            total_tests=total_tests,
            compliant_tests=compliant_tests,
            violation_count=violation_count,
            compliance_percentage=compliance_percentage,
            patterns_summary=patterns_count
        )

    def generate_rename_script(self, report: NamingConventionReport, output_file: str = None) -> str:
        """Generate a script to automatically rename tests based on violations.

        Args:
            report: NamingConventionReport with violations
            output_file: Optional file to write the script to

        Returns:
            String containing the rename script
        """
        script_lines = [
            "#!/usr/bin/env python3",
            '"""',
            "Automated test renaming script generated by NamingConventionValidator.",
            "This script renames test methods to follow naming conventions.",
            '"""',
            "",
            "import re",
            "from pathlib import Path",
            "",
            "def rename_tests():",
            '    """Apply all the suggested test renames."""',
            "    renames = ["
        ]

        # Group violations by file
        violations_by_file = {}
        for violation in report.violations:
            if violation.file_path not in violations_by_file:
                violations_by_file[violation.file_path] = []
            violations_by_file[violation.file_path].append(violation)

        # Generate rename operations
        for file_path, violations in violations_by_file.items():
            script_lines.append(f'        # Renames for {file_path}')
            for violation in violations:
                script_lines.append(
                    f'        ("{file_path}", "{violation.current_name}", "{violation.suggested_name}"),'
                )
            script_lines.append("")

        script_lines.extend([
            "    ]",
            "",
            "    for file_path, old_name, new_name in renames:",
            "        try:",
            "            with open(file_path, 'r', encoding='utf-8') as f:",
            "                content = f.read()",
            "",
            "            # Replace function definition",
            "            pattern = rf'def\\s+{re.escape(old_name)}\\s*\\('",
            "            replacement = f'def {new_name}('",
            "            new_content = re.sub(pattern, replacement, content)",
            "",
            "            if new_content != content:",
            "                with open(file_path, 'w', encoding='utf-8') as f:",
            "                    f.write(new_content)",
            "                print(f'Renamed {old_name} -> {new_name} in {file_path}')",
            "            else:",
            "                print(f'Warning: Could not find {old_name} in {file_path}')",
            "",
            "        except Exception as e:",
            "            print(f'Error processing {file_path}: {e}')",
            "",
            "",
            "if __name__ == '__main__':",
            "    rename_tests()"
        ])

        script_content = "\n".join(script_lines)

        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(script_content)

        return script_content


def main():
    """Command-line interface for the naming convention validator."""
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="Validate test naming conventions")
    parser.add_argument("path", help="Test file or directory to validate")
    parser.add_argument("--generate-script", help="Generate rename script file")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    validator = NamingConventionValidator()
    path = Path(args.path)

    if path.is_file():
        report = validator.validate_file(str(path))
        print(f"Validated {report.total_tests} tests in {path}")
    elif path.is_dir():
        report = validator.validate_directory(str(path))
        print(f"Validated {report.total_tests} tests in {len(list(path.glob('test_*.py')))} files")
    else:
        print(f"Error: {path} is not a valid file or directory")
        sys.exit(1)

    print(f"Compliance: {report.compliance_percentage:.1f}% ({report.compliant_tests}/{report.total_tests})")
    print(f"Violations: {report.violation_count}")

    if args.verbose and report.violations:
        print("\nViolations:")
        for violation in report.violations:
            print(f"  {violation.file_path}:{violation.line_number}")
            print(f"    {violation.current_name} -> {violation.suggested_name}")
            print(f"    {violation.rationale}")
            print()

    if args.generate_script:
        script_content = validator.generate_rename_script(report, args.generate_script)
        print(f"Generated rename script: {args.generate_script}")

    print("\nPattern usage:")
    for pattern, count in sorted(report.patterns_summary.items()):
        print(f"  {pattern}: {count}")


if __name__ == "__main__":
    main()
