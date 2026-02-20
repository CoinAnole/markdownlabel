"""Over-testing validation system for preventing regression to excessive max_examples.

This module provides automated detection of excessive max_examples values and
generates reports for optimization opportunities. It can be used in CI to
prevent regression to over-testing patterns.
"""

import json
import sys
from typing import List, Optional
from dataclasses import dataclass, asdict

from .file_analyzer import FileAnalyzer, ValidationReport, OptimizationRecommendation


@dataclass
class ValidationThresholds:
    """Thresholds for detecting over-testing."""
    # Maximum allowed examples for different strategy types
    boolean_max: int = 2
    small_finite_max: int = 10
    medium_finite_max: int = 50
    combination_max: int = 50
    complex_max: int = 50

    # Minimum time savings percentage to report
    min_time_savings_percent: float = 20.0

    # Maximum allowed over-testing ratio (current/optimal)
    max_over_testing_ratio: float = 2.0


@dataclass
class ValidationResult:
    """Result of over-testing validation."""
    passed: bool
    total_tests: int
    over_tested_count: int
    critical_violations: List[OptimizationRecommendation]
    warnings: List[OptimizationRecommendation]
    estimated_time_waste_seconds: float
    report_path: Optional[str] = None


class OverTestingValidator:
    """Validates test suite for over-testing patterns and generates reports."""

    def __init__(self, thresholds: Optional[ValidationThresholds] = None):
        """Initialize validator with optional custom thresholds.

        Args:
            thresholds: Custom validation thresholds, uses defaults if None
        """
        self.thresholds = thresholds or ValidationThresholds()
        self.analyzer = FileAnalyzer()

    def validate_test_suite(self, test_directory: str,
                          output_file: Optional[str] = None) -> ValidationResult:
        """Validate entire test suite for over-testing patterns.

        Args:
            test_directory: Path to directory containing test files
            output_file: Optional path to write detailed report

        Returns:
            ValidationResult with pass/fail status and details
        """
        # Run full analysis
        report = self.analyzer.validate_test_suite(test_directory)

        # Classify violations by severity
        critical_violations = []
        warnings = []

        for file_analysis in report.file_analyses:
            for recommendation in file_analysis.recommendations:
                if self._is_critical_violation(recommendation):
                    critical_violations.append(recommendation)
                else:
                    warnings.append(recommendation)

        # Calculate estimated time waste
        time_waste = sum(
            (r.current_examples - r.recommended_examples) * 0.1  # 0.1 sec per example
            for r in critical_violations + warnings
        )

        # Determine pass/fail
        passed = len(critical_violations) == 0

        # Generate detailed report if requested
        report_path = None
        if output_file:
            report_path = self._generate_detailed_report(
                report, critical_violations, warnings, output_file
            )

        return ValidationResult(
            passed=passed,
            total_tests=report.total_tests,
            over_tested_count=report.total_over_tested,
            critical_violations=critical_violations,
            warnings=warnings,
            estimated_time_waste_seconds=time_waste,
            report_path=report_path
        )

    def _is_critical_violation(self, recommendation: OptimizationRecommendation) -> bool:
        """Determine if a recommendation represents a critical violation."""
        # Critical violations are cases with extreme over-testing
        over_testing_ratio = recommendation.current_examples / recommendation.recommended_examples

        # Boolean tests with more than 2 examples are always critical
        if (recommendation.strategy_type == 'boolean' and
                recommendation.current_examples > self.thresholds.boolean_max):
            return True

        # High time savings percentage indicates critical over-testing
        if recommendation.time_savings_percent >= 80.0:
            return True

        # Extreme over-testing ratios are critical
        if over_testing_ratio >= 5.0:
            return True

        return False

    def _generate_detailed_report(self,
                                report: ValidationReport,
                                critical_violations: List[OptimizationRecommendation],
                                warnings: List[OptimizationRecommendation],
                                output_file: str) -> str:
        """Generate detailed validation report."""
        report_data = {
            'validation_summary': {
                'passed': len(critical_violations) == 0,
                'total_tests': report.total_tests,
                'over_tested_count': report.total_over_tested,
                'critical_violations': len(critical_violations),
                'warnings': len(warnings),
                'estimated_time_waste_seconds': sum(
                    (r.current_examples - r.recommended_examples) * 0.1
                    for r in critical_violations + warnings
                )
            },
            'critical_violations': [asdict(v) for v in critical_violations],
            'warnings': [asdict(w) for w in warnings],
            'thresholds': asdict(self.thresholds),
            'file_analyses': [asdict(fa) for fa in report.file_analyses]
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2)

        return output_file

    def generate_ci_script(self, test_directory: str,
                          fail_on_violations: bool = True) -> str:
        """Generate CI script for automated validation.

        Args:
            test_directory: Path to test directory
            fail_on_violations: Whether to fail CI on critical violations

        Returns:
            Shell script content for CI integration
        """
        script_content = f"""#!/bin/bash
# Automated over-testing validation for CI

set -e

echo "Running over-testing validation..."

# Run validation
python3 -c "
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))

from kivy_garden.markdownlabel.tests.modules.over_testing_validator import OverTestingValidator

validator = OverTestingValidator()
result = validator.validate_test_suite('{test_directory}', 'over_testing_report.json')

print(f'Validation Results:')
print(f'  Total tests: {{result.total_tests}}')
print(f'  Over-tested: {{result.over_tested_count}}')
print(f'  Critical violations: {{len(result.critical_violations)}}')
print(f'  Warnings: {{len(result.warnings)}}')
print(f'  Estimated time waste: {{result.estimated_time_waste_seconds:.1f}} seconds')

if result.critical_violations:
    print('\\nCritical violations found:')
    for violation in result.critical_violations:
        print(f'  - {{violation.file_path}}:{{violation.test_name}} '
              f'({{violation.current_examples}} → {{violation.recommended_examples}})')

if result.warnings:
    print('\\nWarnings:')
    for warning in result.warnings:
        print(f'  - {{warning.file_path}}:{{warning.test_name}} '
              f'({{warning.current_examples}} → {{warning.recommended_examples}})')

if not result.passed and {str(fail_on_violations).lower()}:
    print('\\nValidation FAILED: Critical over-testing violations found')
    sys.exit(1)
else:
    print('\\nValidation PASSED')
"

echo "Over-testing validation complete"
"""
        return script_content

    def check_single_file(self, file_path: str) -> List[OptimizationRecommendation]:
        """Check a single test file for over-testing patterns.

        Args:
            file_path: Path to test file to check

        Returns:
            List of optimization recommendations for the file
        """
        analysis = self.analyzer.analyze_file(file_path)
        return analysis.recommendations

    def get_optimization_script(self, test_directory: str) -> str:
        """Generate script to automatically fix over-testing issues.

        Args:
            test_directory: Path to test directory

        Returns:
            Python script content for applying optimizations
        """
        script_content = f"""#!/usr/bin/env python3
# Auto-generated script to fix over-testing issues

import re
from pathlib import Path

def fix_over_testing():
    \"\"\"Apply recommended max_examples optimizations.\"\"\"

    # Get recommendations
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path.cwd()))

    from kivy_garden.markdownlabel.tests.modules.over_testing_validator import OverTestingValidator

    validator = OverTestingValidator()
    result = validator.validate_test_suite('{test_directory}')

    fixed_files = set()

    for recommendation in result.critical_violations + result.warnings:
        file_path = recommendation.file_path

        # Read file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Replace max_examples value
        old_pattern = f'max_examples={{recommendation.current_examples}}'
        new_pattern = f'max_examples={{recommendation.recommended_examples}}'

        if old_pattern in content:
            content = content.replace(old_pattern, new_pattern)

            # Write back
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            fixed_files.add(file_path)
            print(f'Fixed {{recommendation.test_name}} in {{file_path}}: '
                  f'{{recommendation.current_examples}} → '
                  f'{{recommendation.recommended_examples}}')

    print(f'\\nFixed {{len(result.critical_violations + result.warnings)}} tests '
          f'in {{len(fixed_files)}} files')

if __name__ == '__main__':
    fix_over_testing()
"""
        return script_content


def main():
    """Command-line interface for over-testing validation."""
    import argparse

    parser = argparse.ArgumentParser(description='Validate test suite for over-testing patterns')
    parser.add_argument('test_directory', help='Path to test directory')
    parser.add_argument('--output', '-o', help='Output file for detailed report')
    parser.add_argument('--fail-on-violations', action='store_true',
                       help='Exit with error code if critical violations found')
    parser.add_argument('--generate-ci-script', help='Generate CI script and save to file')
    parser.add_argument('--generate-fix-script', help='Generate fix script and save to file')

    args = parser.parse_args()

    validator = OverTestingValidator()

    if args.generate_ci_script:
        script_content = validator.generate_ci_script(args.test_directory, args.fail_on_violations)
        with open(args.generate_ci_script, 'w') as f:
            f.write(script_content)
        print(f"CI script generated: {args.generate_ci_script}")
        return

    if args.generate_fix_script:
        script_content = validator.get_optimization_script(args.test_directory)
        with open(args.generate_fix_script, 'w') as f:
            f.write(script_content)
        print(f"Fix script generated: {args.generate_fix_script}")
        return

    # Run validation
    result = validator.validate_test_suite(args.test_directory, args.output)

    print("Validation Results:")
    print(f"  Total tests: {result.total_tests}")
    print(f"  Over-tested: {result.over_tested_count}")
    print(f"  Critical violations: {len(result.critical_violations)}")
    print(f"  Warnings: {len(result.warnings)}")
    print(f"  Estimated time waste: {result.estimated_time_waste_seconds:.1f} seconds")

    if result.critical_violations:
        print("\nCritical violations:")
        for violation in result.critical_violations:
            print(f"  - {violation.file_path}:{violation.test_name} "
                  f"({violation.current_examples} → {violation.recommended_examples})")

    if result.warnings:
        print("\nWarnings:")
        for warning in result.warnings:
            print(f"  - {warning.file_path}:{warning.test_name} "
                  f"({warning.current_examples} → {warning.recommended_examples})")

    if result.report_path:
        print(f"\nDetailed report: {result.report_path}")

    if args.fail_on_violations and not result.passed:
        print("\nValidation FAILED")
        sys.exit(1)
    else:
        print("\nValidation PASSED")


if __name__ == '__main__':
    main()
