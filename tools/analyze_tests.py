#!/usr/bin/env python3
"""
Test optimization analysis script.

This script analyzes the test suite for max_examples optimization opportunities
and generates a report showing potential improvements.
"""

import sys
import os
from pathlib import Path

# Add the tools directory to Python path
tools_dir = Path(__file__).parent
sys.path.insert(0, str(tools_dir))

from test_optimization import FileAnalyzer


def main():
    """Run test suite analysis and generate optimization report."""
    # Path to test directory
    test_dir = Path(__file__).parent.parent / 'kivy_garden' / 'markdownlabel' / 'tests'
    
    if not test_dir.exists():
        print(f"Error: Test directory not found: {test_dir}")
        return 1
    
    print("🔍 Analyzing test suite for max_examples optimization opportunities...")
    print(f"📁 Test directory: {test_dir}")
    print()
    
    # Create analyzer and run validation
    analyzer = FileAnalyzer()
    report = analyzer.validate_test_suite(str(test_dir))
    
    # Print summary
    print("📊 ANALYSIS SUMMARY")
    print("=" * 50)
    print(f"Total property tests found: {report.total_tests}")
    print(f"Over-tested cases: {report.total_over_tested}")
    print(f"Files analyzed: {len(report.file_analyses)}")
    print(f"Potential time savings: {report.potential_time_savings_percent:.1f}%")
    print(f"Estimated time reduction: {report.estimated_time_reduction_seconds:.1f} seconds")
    print()
    
    if report.total_over_tested == 0:
        print("✅ No over-testing detected! All tests use appropriate max_examples values.")
        return 0
    
    # Print detailed recommendations
    print("🚨 OVER-TESTING ISSUES FOUND")
    print("=" * 50)
    
    for file_analysis in report.file_analyses:
        if file_analysis.over_tested_count > 0:
            print(f"\n📄 {Path(file_analysis.file_path).name}")
            print(f"   Over-tested: {file_analysis.over_tested_count}/{file_analysis.total_tests} tests")
            
            for rec in file_analysis.recommendations:
                print(f"   ⚠️  {rec.test_name} (line {rec.line_number})")
                print(f"      Current: max_examples={rec.current_examples}")
                print(f"      Recommended: max_examples={rec.recommended_examples}")
                print(f"      Strategy: {rec.strategy_type}")
                print(f"      Time savings: {rec.time_savings_percent:.1f}%")
                print(f"      Rationale: {rec.rationale}")
                print()
    
    print("💡 RECOMMENDATIONS")
    print("=" * 50)
    print("1. Update the identified tests to use recommended max_examples values")
    print("2. Add explanatory comments for any custom values that deviate from guidelines")
    print("3. Consider adding a pre-commit hook to prevent future over-testing")
    print("4. Review the Hypothesis Optimization Guidelines for best practices")
    print()
    
    return 1 if report.total_over_tested > 0 else 0


if __name__ == '__main__':
    sys.exit(main())