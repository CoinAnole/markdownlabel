#!/usr/bin/env python3
"""
Generate comprehensive optimization report with detailed analysis and prioritization.

This script creates a detailed report showing current vs recommended max_examples,
calculates potential time savings, and prioritizes optimizations by impact and safety.
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Add the package to Python path
sys.path.insert(0, str(Path(__file__).parent))

from kivy_garden.markdownlabel.test_file_analyzer import FileAnalyzer


def generate_detailed_report():
    """Generate comprehensive optimization report."""
    analyzer = FileAnalyzer()
    test_directory = "kivy_garden/markdownlabel/tests"
    
    print("Generating comprehensive optimization report...")
    print("=" * 80)
    
    # Generate validation report
    report = analyzer.validate_test_suite(test_directory)
    
    # Create report data structure
    report_data = {
        'metadata': {
            'generated_at': datetime.now().isoformat(),
            'test_directory': test_directory,
            'total_files_analyzed': len(report.file_analyses)
        },
        'summary': {
            'total_tests': report.total_tests,
            'over_tested_count': report.total_over_tested,
            'over_testing_percentage': (report.total_over_tested / report.total_tests * 100) if report.total_tests > 0 else 0,
            'average_time_savings_percent': report.potential_time_savings_percent,
            'estimated_time_reduction_seconds': report.estimated_time_reduction_seconds,
            'estimated_time_reduction_minutes': report.estimated_time_reduction_seconds / 60
        },
        'strategy_analysis': {},
        'priority_recommendations': [],
        'file_details': []
    }
    
    # Analyze by strategy type
    strategy_stats = {}
    all_recommendations = []
    
    for file_analysis in report.file_analyses:
        for rec in file_analysis.recommendations:
            all_recommendations.append(rec)
            strategy_type = rec.strategy_type
            
            if strategy_type not in strategy_stats:
                strategy_stats[strategy_type] = {
                    'count': 0,
                    'total_current': 0,
                    'total_recommended': 0,
                    'total_savings_percent': 0.0,
                    'total_time_saved': 0.0,
                    'examples': []
                }
            
            stats = strategy_stats[strategy_type]
            stats['count'] += 1
            stats['total_current'] += rec.current_examples
            stats['total_recommended'] += rec.recommended_examples
            stats['total_savings_percent'] += rec.time_savings_percent
            stats['total_time_saved'] += (rec.current_examples - rec.recommended_examples) * 0.1  # 0.1s per example
            stats['examples'].append({
                'test_name': rec.test_name,
                'file': rec.file_path,
                'current': rec.current_examples,
                'recommended': rec.recommended_examples,
                'savings_percent': rec.time_savings_percent
            })
    
    # Calculate strategy statistics
    for strategy_type, stats in strategy_stats.items():
        report_data['strategy_analysis'][strategy_type] = {
            'tests_affected': stats['count'],
            'average_current_examples': stats['total_current'] / stats['count'],
            'average_recommended_examples': stats['total_recommended'] / stats['count'],
            'average_time_savings_percent': stats['total_savings_percent'] / stats['count'],
            'total_time_saved_seconds': stats['total_time_saved'],
            'total_time_saved_minutes': stats['total_time_saved'] / 60,
            'impact_level': _calculate_impact_level(stats),
            'safety_level': _calculate_safety_level(strategy_type),
            'priority_score': _calculate_priority_score(stats, strategy_type)
        }
    
    # Sort recommendations by priority (highest impact, safest first)
    prioritized_recommendations = sorted(
        all_recommendations,
        key=lambda r: (
            r.time_savings_percent,  # Higher savings first
            _get_safety_score(r.strategy_type),  # Safer changes first
            -r.current_examples  # Larger current values first (more impact)
        ),
        reverse=True
    )
    
    # Top 20 priority recommendations
    report_data['priority_recommendations'] = [
        {
            'rank': i + 1,
            'test_name': rec.test_name,
            'file_path': rec.file_path,
            'line_number': rec.line_number,
            'strategy_type': rec.strategy_type,
            'current_examples': rec.current_examples,
            'recommended_examples': rec.recommended_examples,
            'time_savings_percent': rec.time_savings_percent,
            'estimated_time_saved_seconds': (rec.current_examples - rec.recommended_examples) * 0.1,
            'rationale': rec.rationale,
            'safety_level': _get_safety_level_name(rec.strategy_type),
            'impact_level': _get_impact_level_name(rec.time_savings_percent)
        }
        for i, rec in enumerate(prioritized_recommendations[:20])
    ]
    
    # File-level details
    for file_analysis in report.file_analyses:
        if file_analysis.over_tested_count > 0:
            report_data['file_details'].append({
                'file_path': file_analysis.file_path,
                'total_tests': file_analysis.total_tests,
                'over_tested_count': file_analysis.over_tested_count,
                'over_testing_percentage': (file_analysis.over_tested_count / file_analysis.total_tests * 100) if file_analysis.total_tests > 0 else 0,
                'potential_time_savings_percent': file_analysis.potential_time_savings_percent,
                'estimated_time_saved_seconds': sum(
                    (r.current_examples - r.recommended_examples) * 0.1 
                    for r in file_analysis.recommendations
                ),
                'recommendations_count': len(file_analysis.recommendations)
            })
    
    # Sort files by impact
    report_data['file_details'].sort(
        key=lambda f: f['estimated_time_saved_seconds'], 
        reverse=True
    )
    
    return report_data


def _calculate_impact_level(stats):
    """Calculate impact level based on time savings."""
    total_time_saved = stats['total_time_saved']
    if total_time_saved > 60:  # More than 1 minute
        return 'HIGH'
    elif total_time_saved > 20:  # More than 20 seconds
        return 'MEDIUM'
    else:
        return 'LOW'


def _calculate_safety_level(strategy_type):
    """Calculate safety level for strategy type changes."""
    safety_levels = {
        'boolean': 'VERY_HIGH',  # Boolean tests are very safe to optimize
        'small_finite': 'HIGH',   # Small finite are safe
        'medium_finite': 'MEDIUM', # Medium finite are moderately safe
        'combination': 'MEDIUM',   # Combinations need more care
        'complex': 'LOW'          # Complex strategies need careful review
    }
    return safety_levels.get(strategy_type, 'LOW')


def _calculate_priority_score(stats, strategy_type):
    """Calculate priority score combining impact and safety."""
    impact_scores = {'HIGH': 3, 'MEDIUM': 2, 'LOW': 1}
    safety_scores = {'VERY_HIGH': 4, 'HIGH': 3, 'MEDIUM': 2, 'LOW': 1}
    
    impact = _calculate_impact_level(stats)
    safety = _calculate_safety_level(strategy_type)
    
    return impact_scores[impact] * safety_scores[safety]


def _get_safety_score(strategy_type):
    """Get numeric safety score for sorting."""
    scores = {
        'boolean': 4,
        'small_finite': 3,
        'medium_finite': 2,
        'combination': 2,
        'complex': 1
    }
    return scores.get(strategy_type, 1)


def _get_safety_level_name(strategy_type):
    """Get safety level name for display."""
    return _calculate_safety_level(strategy_type).replace('_', ' ').title()


def _get_impact_level_name(time_savings_percent):
    """Get impact level name based on time savings percentage."""
    if time_savings_percent >= 90:
        return 'Very High'
    elif time_savings_percent >= 75:
        return 'High'
    elif time_savings_percent >= 50:
        return 'Medium'
    else:
        return 'Low'


def print_executive_summary(report_data):
    """Print executive summary of the optimization report."""
    summary = report_data['summary']
    
    print("\nEXECUTIVE SUMMARY")
    print("=" * 80)
    print(f"Total tests analyzed: {summary['total_tests']}")
    print(f"Tests requiring optimization: {summary['over_tested_count']} ({summary['over_testing_percentage']:.1f}%)")
    print(f"Estimated time savings: {summary['estimated_time_reduction_minutes']:.1f} minutes ({summary['estimated_time_reduction_seconds']:.1f} seconds)")
    print(f"Average optimization potential: {summary['average_time_savings_percent']:.1f}%")
    
    print(f"\nSTRATEGY TYPE BREAKDOWN")
    print("-" * 40)
    
    # Sort strategies by priority score
    strategies = sorted(
        report_data['strategy_analysis'].items(),
        key=lambda x: x[1]['priority_score'],
        reverse=True
    )
    
    for strategy_type, analysis in strategies:
        print(f"\n{strategy_type.upper().replace('_', ' ')}:")
        print(f"  Tests affected: {analysis['tests_affected']}")
        print(f"  Average savings: {analysis['average_time_savings_percent']:.1f}%")
        print(f"  Time saved: {analysis['total_time_saved_minutes']:.1f} minutes")
        print(f"  Impact: {analysis['impact_level']}")
        print(f"  Safety: {analysis['safety_level'].replace('_', ' ').title()}")
        print(f"  Priority Score: {analysis['priority_score']}")


def print_top_recommendations(report_data):
    """Print top priority recommendations."""
    print(f"\nTOP 10 PRIORITY OPTIMIZATIONS")
    print("=" * 80)
    
    for rec in report_data['priority_recommendations'][:10]:
        print(f"\n{rec['rank']}. {rec['test_name']}")
        print(f"   File: {rec['file_path']} (line {rec['line_number']})")
        print(f"   Change: {rec['current_examples']} → {rec['recommended_examples']} examples")
        print(f"   Savings: {rec['time_savings_percent']:.1f}% ({rec['estimated_time_saved_seconds']:.1f}s)")
        print(f"   Strategy: {rec['strategy_type'].replace('_', ' ').title()}")
        print(f"   Safety: {rec['safety_level']} | Impact: {rec['impact_level']}")
        print(f"   Rationale: {rec['rationale']}")


def print_file_impact_analysis(report_data):
    """Print file-by-file impact analysis."""
    print(f"\nFILE IMPACT ANALYSIS (Top 10)")
    print("=" * 80)
    
    for i, file_detail in enumerate(report_data['file_details'][:10], 1):
        print(f"\n{i}. {file_detail['file_path']}")
        print(f"   Tests: {file_detail['over_tested_count']}/{file_detail['total_tests']} over-tested ({file_detail['over_testing_percentage']:.1f}%)")
        print(f"   Time savings: {file_detail['estimated_time_saved_seconds']:.1f} seconds")
        print(f"   Average optimization: {file_detail['potential_time_savings_percent']:.1f}%")
        print(f"   Recommendations: {file_detail['recommendations_count']}")


def save_json_report(report_data, filename="optimization_report.json"):
    """Save detailed report as JSON."""
    with open(filename, 'w') as f:
        json.dump(report_data, f, indent=2)
    print(f"\nDetailed JSON report saved to: {filename}")


def main():
    """Generate and display optimization report."""
    report_data = generate_detailed_report()
    
    print_executive_summary(report_data)
    print_top_recommendations(report_data)
    print_file_impact_analysis(report_data)
    
    # Save detailed JSON report
    save_json_report(report_data)
    
    print(f"\n" + "=" * 80)
    print("RECOMMENDATIONS:")
    print("1. Start with Boolean and Small Finite strategies (highest safety, highest impact)")
    print("2. Focus on files with highest time savings potential first")
    print("3. Test each batch of changes to ensure functionality is preserved")
    print("4. Consider implementing CI-aware optimizations for complex strategies")
    print("=" * 80)


if __name__ == "__main__":
    main()