#!/usr/bin/env python3
"""
Script to analyze the test suite for over-testing patterns.

This script uses the TestFileAnalyzer to scan all test files and generate
a comprehensive report of optimization opportunities.
"""

import sys
from pathlib import Path

# Add the package to Python path
sys.path.insert(0, str(Path(__file__).parent))

from kivy_garden.markdownlabel.test_file_analyzer import TestFileAnalyzer


def main():
    """Run analysis on the test suite and generate report."""
    analyzer = TestFileAnalyzer()
    test_directory = "kivy_garden/markdownlabel/tests"
    
    print("Analyzing test suite for over-testing patterns...")
    print("=" * 60)
    
    # Generate validation report
    report = analyzer.validate_test_suite(test_directory)
    
    # Print summary statistics
    print(f"\nSUMMARY STATISTICS")
    print(f"Total tests analyzed: {report.total_tests}")
    print(f"Tests with over-testing: {report.total_over_tested}")
    print(f"Average potential time savings: {report.potential_time_savings_percent:.1f}%")
    print(f"Estimated time reduction: {report.estimated_time_reduction_seconds:.1f} seconds")
    
    if report.total_over_tested == 0:
        print("\nNo over-testing patterns found!")
        return
    
    # Print detailed file analysis
    print(f"\nDETAILED ANALYSIS")
    print("=" * 60)
    
    for file_analysis in report.file_analyses:
        if file_analysis.over_tested_count > 0:
            print(f"\nFile: {file_analysis.file_path}")
            print(f"  Total tests: {file_analysis.total_tests}")
            print(f"  Over-tested: {file_analysis.over_tested_count}")
            print(f"  Potential savings: {file_analysis.potential_time_savings_percent:.1f}%")
            
            # Show top recommendations for this file
            for rec in file_analysis.recommendations[:5]:  # Show first 5
                print(f"    {rec.test_name} (line {rec.line_number}): "
                      f"{rec.current_examples} → {rec.recommended_examples} "
                      f"({rec.time_savings_percent:.1f}% savings)")
                print(f"      Rationale: {rec.rationale}")
            
            if len(file_analysis.recommendations) > 5:
                print(f"    ... and {len(file_analysis.recommendations) - 5} more")
    
    # Print optimization opportunities by strategy type
    print(f"\nOPTIMIZATION OPPORTUNITIES BY STRATEGY TYPE")
    print("=" * 60)
    
    strategy_stats = {}
    for file_analysis in report.file_analyses:
        for rec in file_analysis.recommendations:
            strategy_type = rec.strategy_type
            if strategy_type not in strategy_stats:
                strategy_stats[strategy_type] = {
                    'count': 0,
                    'total_current': 0,
                    'total_recommended': 0,
                    'total_savings': 0.0
                }
            
            stats = strategy_stats[strategy_type]
            stats['count'] += 1
            stats['total_current'] += rec.current_examples
            stats['total_recommended'] += rec.recommended_examples
            stats['total_savings'] += rec.time_savings_percent
    
    for strategy_type, stats in sorted(strategy_stats.items()):
        avg_current = stats['total_current'] / stats['count']
        avg_recommended = stats['total_recommended'] / stats['count']
        avg_savings = stats['total_savings'] / stats['count']
        
        print(f"\n{strategy_type.upper()}:")
        print(f"  Tests affected: {stats['count']}")
        print(f"  Average current max_examples: {avg_current:.1f}")
        print(f"  Average recommended max_examples: {avg_recommended:.1f}")
        print(f"  Average time savings: {avg_savings:.1f}%")
    
    print(f"\nAnalysis complete. Found {report.total_over_tested} over-tested cases.")


if __name__ == "__main__":
    main()