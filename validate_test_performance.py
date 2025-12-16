#!/usr/bin/env python3
"""CI script for validating test performance and preventing over-testing regression."""

import sys
from pathlib import Path

# Add the package to Python path
sys.path.insert(0, str(Path.cwd()))

from kivy_garden.markdownlabel.over_testing_validator import OverTestingValidator


def main():
    """Run over-testing validation for CI."""
    test_directory = 'kivy_garden/markdownlabel/tests'
    
    print("🔍 Running over-testing validation...")
    
    validator = OverTestingValidator()
    result = validator.validate_test_suite(test_directory, 'over_testing_report.json')
    
    print(f"\n📊 Validation Results:")
    print(f"  Total tests: {result.total_tests}")
    print(f"  Over-tested: {result.over_tested_count}")
    print(f"  Critical violations: {len(result.critical_violations)}")
    print(f"  Warnings: {len(result.warnings)}")
    print(f"  Estimated time waste: {result.estimated_time_waste_seconds:.1f} seconds")
    
    if result.critical_violations:
        print("\n❌ Critical violations found:")
        for violation in result.critical_violations:
            print(f"  - {Path(violation.file_path).name}:{violation.test_name}")
            print(f"    Current: {violation.current_examples} examples")
            print(f"    Recommended: {violation.recommended_examples} examples")
            print(f"    Time savings: {violation.time_savings_percent:.1f}%")
            print()
    
    if result.warnings:
        print("\n⚠️  Warnings:")
        for warning in result.warnings:
            print(f"  - {Path(warning.file_path).name}:{warning.test_name}")
            print(f"    Current: {warning.current_examples} → Recommended: {warning.recommended_examples}")
    
    if result.report_path:
        print(f"\n📄 Detailed report saved: {result.report_path}")
    
    if not result.passed:
        print("\n💥 Validation FAILED: Critical over-testing violations found")
        print("Please optimize the flagged tests to improve performance.")
        sys.exit(1)
    else:
        print("\n✅ Validation PASSED: No critical over-testing detected")


if __name__ == '__main__':
    main()