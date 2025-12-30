#!/usr/bin/env python3
"""
Measure baseline performance of the test suite before optimization.

This script records execution times for all test categories, documents current
max_examples usage patterns, and establishes performance benchmarks.
"""

import os
import sys
import time
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Any

from kivy_garden.markdownlabel.tests.test_optimization.file_analyzer import FileAnalyzer


class BaselinePerformanceMeasurer:
    """Measures baseline performance of the test suite."""
    
    def __init__(self):
        self.analyzer = FileAnalyzer()
        default_dir = Path(__file__).parent.parent / "kivy_garden" / "markdownlabel" / "tests"
        self.test_directory = os.getenv("TEST_DIR", str(default_dir.resolve()))
        
    def measure_full_suite_performance(self) -> Dict[str, Any]:
        """Measure performance of the entire test suite."""
        print("🔍 Measuring full test suite performance...")
        
        start_time = time.time()
        
        # Run the full test suite
        result = subprocess.run([
            'pytest', 
            self.test_directory,
            '-v',
            '--tb=short'
        ], capture_output=True, text=True)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Parse pytest output for test counts
        output_lines = result.stdout.split('\n')
        test_count = 0
        passed_count = 0
        failed_count = 0
        
        for line in output_lines:
            if ' passed' in line or ' failed' in line:
                # Look for summary line like "314 passed in 45.67s"
                parts = line.split()
                for i, part in enumerate(parts):
                    if part == 'passed' and i > 0:
                        try:
                            passed_count = int(parts[i-1])
                        except ValueError:
                            continue
                    elif part == 'failed' and i > 0:
                        try:
                            failed_count = int(parts[i-1])
                        except ValueError:
                            continue
        
        test_count = passed_count + failed_count
        
        return {
            'total_execution_time_seconds': total_time,
            'total_tests': test_count,
            'passed_tests': passed_count,
            'failed_tests': failed_count,
            'average_time_per_test': total_time / test_count if test_count > 0 else 0,
            'return_code': result.returncode,
            'stdout_sample': result.stdout[-1000:] if result.stdout else '',  # Last 1000 chars
            'stderr_sample': result.stderr[-500:] if result.stderr else ''    # Last 500 chars
        }
    
    def measure_file_level_performance(self) -> Dict[str, Dict[str, Any]]:
        """Measure performance of individual test files."""
        print("📁 Measuring individual file performance...")
        
        test_files = list(Path(self.test_directory).glob('test_*.py'))
        file_performance = {}
        
        for test_file in test_files:
            print(f"  Measuring {test_file.name}...")
            
            start_time = time.time()
            
            result = subprocess.run([
                'pytest', 
                str(test_file),
                '-v',
                '--tb=short'
            ], capture_output=True, text=True)
            
            end_time = time.time()
            execution_time = end_time - start_time
            
            # Parse test count from output
            test_count = 0
            passed_count = 0
            failed_count = 0
            
            output_lines = result.stdout.split('\n')
            for line in output_lines:
                if ' passed' in line or ' failed' in line:
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if part == 'passed' and i > 0:
                            try:
                                passed_count = int(parts[i-1])
                            except ValueError:
                                continue
                        elif part == 'failed' and i > 0:
                            try:
                                failed_count = int(parts[i-1])
                            except ValueError:
                                continue
            
            test_count = passed_count + failed_count
            
            file_performance[str(test_file)] = {
                'execution_time_seconds': execution_time,
                'test_count': test_count,
                'passed_tests': passed_count,
                'failed_tests': failed_count,
                'average_time_per_test': execution_time / test_count if test_count > 0 else 0,
                'return_code': result.returncode
            }
        
        return file_performance
    
    def analyze_max_examples_patterns(self) -> Dict[str, Any]:
        """Analyze current max_examples usage patterns."""
        print("📊 Analyzing max_examples usage patterns...")
        
        report = self.analyzer.validate_test_suite(self.test_directory)
        
        # Collect all current max_examples values
        max_examples_values = []
        strategy_distribution = {}
        
        for file_analysis in report.file_analyses:
            for rec in file_analysis.recommendations:
                max_examples_values.append(rec.current_examples)
                
                strategy_type = rec.strategy_type
                if strategy_type not in strategy_distribution:
                    strategy_distribution[strategy_type] = {
                        'count': 0,
                        'total_examples': 0,
                        'min_examples': float('inf'),
                        'max_examples': 0,
                        'values': []
                    }
                
                stats = strategy_distribution[strategy_type]
                stats['count'] += 1
                stats['total_examples'] += rec.current_examples
                stats['min_examples'] = min(stats['min_examples'], rec.current_examples)
                stats['max_examples'] = max(stats['max_examples'], rec.current_examples)
                stats['values'].append(rec.current_examples)
        
        # Calculate statistics
        for strategy_type, stats in strategy_distribution.items():
            stats['average_examples'] = stats['total_examples'] / stats['count']
            stats['values'].sort()
            # Calculate median
            values = stats['values']
            n = len(values)
            if n % 2 == 0:
                stats['median_examples'] = (values[n//2 - 1] + values[n//2]) / 2
            else:
                stats['median_examples'] = values[n//2]
        
        return {
            'total_tests_analyzed': len(max_examples_values),
            'overall_statistics': {
                'min_max_examples': min(max_examples_values) if max_examples_values else 0,
                'max_max_examples': max(max_examples_values) if max_examples_values else 0,
                'average_max_examples': sum(max_examples_values) / len(max_examples_values) if max_examples_values else 0,
                'median_max_examples': sorted(max_examples_values)[len(max_examples_values)//2] if max_examples_values else 0
            },
            'strategy_distribution': strategy_distribution,
            'value_frequency': {
                str(value): max_examples_values.count(value) 
                for value in sorted(set(max_examples_values))
            }
        }
    
    def measure_strategy_category_performance(self) -> Dict[str, Dict[str, Any]]:
        """Measure performance by strategy category."""
        print("🎯 Measuring performance by strategy category...")
        
        # Get strategy analysis
        report = self.analyzer.validate_test_suite(self.test_directory)
        
        # Group tests by strategy type
        strategy_files = {}
        for file_analysis in report.file_analyses:
            for rec in file_analysis.recommendations:
                strategy_type = rec.strategy_type
                if strategy_type not in strategy_files:
                    strategy_files[strategy_type] = set()
                strategy_files[strategy_type].add(rec.file_path)
        
        # Measure performance for each strategy category
        strategy_performance = {}
        
        for strategy_type, files in strategy_files.items():
            print(f"  Measuring {strategy_type} strategy tests...")
            
            # Run tests for files containing this strategy type
            file_list = list(files)
            if not file_list:
                continue
                
            start_time = time.time()
            
            result = subprocess.run([
                'pytest'] + file_list + [
                '-v',
                '--tb=short'
            ], capture_output=True, text=True)
            
            end_time = time.time()
            execution_time = end_time - start_time
            
            # Count tests of this strategy type
            strategy_test_count = sum(
                1 for file_analysis in report.file_analyses
                for rec in file_analysis.recommendations
                if rec.strategy_type == strategy_type
            )
            
            strategy_performance[strategy_type] = {
                'execution_time_seconds': execution_time,
                'test_count': strategy_test_count,
                'files_involved': len(file_list),
                'average_time_per_test': execution_time / strategy_test_count if strategy_test_count > 0 else 0,
                'return_code': result.returncode
            }
        
        return strategy_performance
    
    def generate_baseline_report(self) -> Dict[str, Any]:
        """Generate comprehensive baseline performance report."""
        print("📋 Generating comprehensive baseline performance report...")
        print("=" * 80)
        
        # Collect all measurements
        full_suite_perf = self.measure_full_suite_performance()
        file_level_perf = self.measure_file_level_performance()
        max_examples_analysis = self.analyze_max_examples_patterns()
        strategy_perf = self.measure_strategy_category_performance()
        
        # Create comprehensive report
        baseline_report = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'test_directory': self.test_directory,
                'measurement_type': 'baseline_performance'
            },
            'full_suite_performance': full_suite_perf,
            'file_level_performance': file_level_perf,
            'max_examples_analysis': max_examples_analysis,
            'strategy_category_performance': strategy_perf,
            'benchmarks': {
                'total_execution_time_baseline': full_suite_perf['total_execution_time_seconds'],
                'average_time_per_test_baseline': full_suite_perf['average_time_per_test'],
                'total_tests_baseline': full_suite_perf['total_tests']
            }
        }
        
        return baseline_report
    
    def print_baseline_summary(self, report: Dict[str, Any]):
        """Print summary of baseline measurements."""
        full_suite = report['full_suite_performance']
        max_examples = report['max_examples_analysis']
        
        print(f"\nBASELINE PERFORMANCE SUMMARY")
        print("=" * 80)
        print(f"Total execution time: {full_suite['total_execution_time_seconds']:.2f} seconds")
        print(f"Total tests: {full_suite['total_tests']}")
        print(f"Average time per test: {full_suite['average_time_per_test']:.3f} seconds")
        print(f"Tests passed: {full_suite['passed_tests']}")
        print(f"Tests failed: {full_suite['failed_tests']}")
        
        print(f"\nMAX_EXAMPLES USAGE PATTERNS")
        print("-" * 40)
        overall = max_examples['overall_statistics']
        print(f"Average max_examples: {overall['average_max_examples']:.1f}")
        print(f"Median max_examples: {overall['median_max_examples']}")
        print(f"Range: {overall['min_max_examples']} - {overall['max_max_examples']}")
        
        print(f"\nSTRATEGY CATEGORY PERFORMANCE")
        print("-" * 40)
        for strategy_type, perf in report['strategy_category_performance'].items():
            print(f"{strategy_type.replace('_', ' ').title()}:")
            print(f"  Tests: {perf['test_count']}")
            print(f"  Time: {perf['execution_time_seconds']:.2f}s")
            print(f"  Avg per test: {perf['average_time_per_test']:.3f}s")
        
        print(f"\nTOP 5 SLOWEST FILES")
        print("-" * 40)
        file_perf_sorted = sorted(
            report['file_level_performance'].items(),
            key=lambda x: x[1]['execution_time_seconds'],
            reverse=True
        )
        
        for file_path, perf in file_perf_sorted[:5]:
            file_name = Path(file_path).name
            print(f"{file_name}: {perf['execution_time_seconds']:.2f}s ({perf['test_count']} tests)")


def save_baseline_report(report: Dict[str, Any], filename: str = "baseline_performance_report.json"):
    """Save baseline report to JSON file."""
    with open(filename, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"\n📄 Baseline report saved to: {filename}")


def main():
    """Main function to measure baseline performance."""
    measurer = BaselinePerformanceMeasurer()
    
    print("🚀 Starting baseline performance measurement...")
    print("This may take several minutes as we run the full test suite multiple times.")
    print("=" * 80)
    
    # Generate comprehensive baseline report
    baseline_report = measurer.generate_baseline_report()
    
    # Print summary
    measurer.print_baseline_summary(baseline_report)
    
    # Save detailed report
    save_baseline_report(baseline_report)
    
    print(f"\n" + "=" * 80)
    print("✅ Baseline performance measurement complete!")
    print("This data will be used to measure optimization improvements.")
    print("=" * 80)


if __name__ == "__main__":
    main()