#!/usr/bin/env python3
"""
Measure post-optimization performance and compare against baseline.

This script records execution times after optimization phases, calculates actual
time savings by test category, and verifies improvements meet expected targets.
"""

import sys
import time
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Any

# Add the package to Python path
sys.path.insert(0, str(Path(__file__).parent))

from kivy_garden.markdownlabel.test_file_analyzer import TestFileAnalyzer


class PostOptimizationPerformanceMeasurer:
    """Measures post-optimization performance and compares against baseline."""
    
    def __init__(self, baseline_report_path: str = "baseline_performance_report.json"):
        self.analyzer = TestFileAnalyzer()
        self.test_directory = "kivy_garden/markdownlabel/tests"
        self.baseline_report = self._load_baseline_report(baseline_report_path)
        
    def _load_baseline_report(self, baseline_path: str) -> Dict[str, Any]:
        """Load baseline performance report."""
        try:
            with open(baseline_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️  Baseline report not found at {baseline_path}")
            print("Please run measure_baseline_performance.py first")
            return {}
    
    def measure_current_performance(self) -> Dict[str, Any]:
        """Measure current performance after optimizations."""
        print("🔍 Measuring current (post-optimization) performance...")
        
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
            'measurement_timestamp': datetime.now().isoformat()
        }
    
    def measure_file_level_improvements(self) -> Dict[str, Dict[str, Any]]:
        """Measure file-level performance improvements."""
        print("📁 Measuring file-level performance improvements...")
        
        test_files = list(Path(self.test_directory).glob('test_*.py'))
        file_improvements = {}
        
        baseline_file_perf = self.baseline_report.get('file_level_performance', {})
        
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
            current_time = end_time - start_time
            
            # Get baseline time for comparison
            baseline_time = 0
            if str(test_file) in baseline_file_perf:
                baseline_time = baseline_file_perf[str(test_file)]['execution_time_seconds']
            
            # Calculate improvement
            time_saved = baseline_time - current_time
            improvement_percent = (time_saved / baseline_time * 100) if baseline_time > 0 else 0
            
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
            
            file_improvements[str(test_file)] = {
                'current_time_seconds': current_time,
                'baseline_time_seconds': baseline_time,
                'time_saved_seconds': time_saved,
                'improvement_percent': improvement_percent,
                'test_count': test_count,
                'passed_tests': passed_count,
                'failed_tests': failed_count,
                'return_code': result.returncode
            }
        
        return file_improvements
    
    def measure_strategy_category_improvements(self) -> Dict[str, Dict[str, Any]]:
        """Measure performance improvements by strategy category."""
        print("🎯 Measuring strategy category improvements...")
        
        # Get current strategy analysis
        report = self.analyzer.validate_test_suite(self.test_directory)
        
        # Group tests by strategy type
        strategy_files = {}
        for file_analysis in report.file_analyses:
            for rec in file_analysis.recommendations:
                strategy_type = rec.strategy_type
                if strategy_type not in strategy_files:
                    strategy_files[strategy_type] = set()
                strategy_files[strategy_type].add(rec.file_path)
        
        # Get baseline strategy performance
        baseline_strategy_perf = self.baseline_report.get('strategy_category_performance', {})
        
        # Measure current performance for each strategy category
        strategy_improvements = {}
        
        for strategy_type, files in strategy_files.items():
            print(f"  Measuring {strategy_type} strategy improvements...")
            
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
            current_time = end_time - start_time
            
            # Get baseline time
            baseline_time = 0
            if strategy_type in baseline_strategy_perf:
                baseline_time = baseline_strategy_perf[strategy_type]['execution_time_seconds']
            
            # Calculate improvement
            time_saved = baseline_time - current_time
            improvement_percent = (time_saved / baseline_time * 100) if baseline_time > 0 else 0
            
            # Count tests of this strategy type
            strategy_test_count = sum(
                1 for file_analysis in report.file_analyses
                for rec in file_analysis.recommendations
                if rec.strategy_type == strategy_type
            )
            
            strategy_improvements[strategy_type] = {
                'current_time_seconds': current_time,
                'baseline_time_seconds': baseline_time,
                'time_saved_seconds': time_saved,
                'improvement_percent': improvement_percent,
                'test_count': strategy_test_count,
                'files_involved': len(file_list),
                'return_code': result.returncode
            }
        
        return strategy_improvements
    
    def analyze_optimization_effectiveness(self) -> Dict[str, Any]:
        """Analyze how effective the optimizations were."""
        print("📊 Analyzing optimization effectiveness...")
        
        # Get current max_examples analysis
        current_report = self.analyzer.validate_test_suite(self.test_directory)
        
        # Compare with baseline
        baseline_max_examples = self.baseline_report.get('max_examples_analysis', {})
        
        # Count optimized tests
        optimized_tests = 0
        total_tests = 0
        
        for file_analysis in current_report.file_analyses:
            total_tests += file_analysis.total_tests
            # Tests that still need optimization
            optimized_tests += file_analysis.total_tests - file_analysis.over_tested_count
        
        optimization_coverage = (optimized_tests / total_tests * 100) if total_tests > 0 else 0
        
        return {
            'total_tests': total_tests,
            'optimized_tests': optimized_tests,
            'remaining_over_tested': current_report.total_over_tested,
            'optimization_coverage_percent': optimization_coverage,
            'baseline_over_tested': len([
                rec for file_analysis in self.baseline_report.get('file_analyses', [])
                for rec in file_analysis.get('recommendations', [])
            ]) if 'file_analyses' in self.baseline_report else 0
        }
    
    def generate_comparison_report(self) -> Dict[str, Any]:
        """Generate comprehensive comparison report."""
        print("📋 Generating performance comparison report...")
        print("=" * 80)
        
        if not self.baseline_report:
            print("❌ Cannot generate comparison without baseline report")
            return {}
        
        # Collect all measurements
        current_perf = self.measure_current_performance()
        file_improvements = self.measure_file_level_improvements()
        strategy_improvements = self.measure_strategy_category_improvements()
        optimization_analysis = self.analyze_optimization_effectiveness()
        
        # Get baseline data
        baseline_perf = self.baseline_report.get('full_suite_performance', {})
        
        # Calculate overall improvements
        baseline_time = baseline_perf.get('total_execution_time_seconds', 0)
        current_time = current_perf['total_execution_time_seconds']
        total_time_saved = baseline_time - current_time
        overall_improvement = (total_time_saved / baseline_time * 100) if baseline_time > 0 else 0
        
        # Create comprehensive comparison report
        comparison_report = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'test_directory': self.test_directory,
                'measurement_type': 'post_optimization_comparison',
                'baseline_report_used': bool(self.baseline_report)
            },
            'overall_comparison': {
                'baseline_time_seconds': baseline_time,
                'current_time_seconds': current_time,
                'time_saved_seconds': total_time_saved,
                'improvement_percent': overall_improvement,
                'baseline_tests': baseline_perf.get('total_tests', 0),
                'current_tests': current_perf['total_tests'],
                'tests_still_passing': current_perf['passed_tests'],
                'tests_failed': current_perf['failed_tests']
            },
            'file_level_improvements': file_improvements,
            'strategy_category_improvements': strategy_improvements,
            'optimization_effectiveness': optimization_analysis,
            'target_verification': self._verify_improvement_targets(
                overall_improvement, strategy_improvements
            )
        }
        
        return comparison_report
    
    def _verify_improvement_targets(self, overall_improvement: float, 
                                  strategy_improvements: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Verify if improvements meet expected targets from requirements."""
        
        # Expected targets from requirements:
        # - Overall: 50% reduction
        # - Boolean: 98% reduction  
        # - Small finite: 80-95% reduction
        # - Complex: 50-80% reduction
        
        target_verification = {
            'overall_target_met': overall_improvement >= 50.0,
            'overall_target': 50.0,
            'overall_actual': overall_improvement,
            'strategy_targets': {}
        }
        
        # Define expected targets by strategy
        strategy_targets = {
            'boolean': {'min': 95.0, 'max': 100.0},
            'small_finite': {'min': 80.0, 'max': 95.0},
            'medium_finite': {'min': 50.0, 'max': 80.0},
            'combination': {'min': 50.0, 'max': 80.0},
            'complex': {'min': 50.0, 'max': 80.0}
        }
        
        for strategy_type, targets in strategy_targets.items():
            if strategy_type in strategy_improvements:
                actual = strategy_improvements[strategy_type]['improvement_percent']
                target_verification['strategy_targets'][strategy_type] = {
                    'target_min': targets['min'],
                    'target_max': targets['max'],
                    'actual': actual,
                    'target_met': targets['min'] <= actual <= targets['max'] or actual >= targets['min']
                }
        
        return target_verification
    
    def print_comparison_summary(self, report: Dict[str, Any]):
        """Print summary of performance comparison."""
        if not report:
            return
            
        overall = report['overall_comparison']
        targets = report['target_verification']
        
        print(f"\nPERFORMANCE COMPARISON SUMMARY")
        print("=" * 80)
        print(f"Baseline time: {overall['baseline_time_seconds']:.2f} seconds")
        print(f"Current time: {overall['current_time_seconds']:.2f} seconds")
        print(f"Time saved: {overall['time_saved_seconds']:.2f} seconds")
        print(f"Overall improvement: {overall['improvement_percent']:.1f}%")
        
        # Target verification
        overall_target_status = "✅ MET" if targets['overall_target_met'] else "❌ NOT MET"
        print(f"Overall target (≥50%): {overall_target_status}")
        
        print(f"\nSTRATEGY CATEGORY IMPROVEMENTS")
        print("-" * 40)
        for strategy_type, improvements in report['strategy_category_improvements'].items():
            print(f"{strategy_type.replace('_', ' ').title()}:")
            print(f"  Time saved: {improvements['time_saved_seconds']:.2f}s")
            print(f"  Improvement: {improvements['improvement_percent']:.1f}%")
            
            # Check target
            if strategy_type in targets['strategy_targets']:
                target_info = targets['strategy_targets'][strategy_type]
                target_status = "✅ MET" if target_info['target_met'] else "❌ NOT MET"
                print(f"  Target ({target_info['target_min']:.0f}-{target_info['target_max']:.0f}%): {target_status}")
        
        print(f"\nOPTIMIZATION EFFECTIVENESS")
        print("-" * 40)
        opt_analysis = report['optimization_effectiveness']
        print(f"Total tests: {opt_analysis['total_tests']}")
        print(f"Optimized tests: {opt_analysis['optimized_tests']}")
        print(f"Still over-tested: {opt_analysis['remaining_over_tested']}")
        print(f"Optimization coverage: {opt_analysis['optimization_coverage_percent']:.1f}%")
        
        print(f"\nTOP 5 FILE IMPROVEMENTS")
        print("-" * 40)
        file_improvements_sorted = sorted(
            report['file_level_improvements'].items(),
            key=lambda x: x[1]['time_saved_seconds'],
            reverse=True
        )
        
        for file_path, improvements in file_improvements_sorted[:5]:
            file_name = Path(file_path).name
            print(f"{file_name}: {improvements['time_saved_seconds']:.2f}s saved ({improvements['improvement_percent']:.1f}%)")


def save_comparison_report(report: Dict[str, Any], filename: str = "post_optimization_performance_report.json"):
    """Save comparison report to JSON file."""
    with open(filename, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"\n📄 Performance comparison report saved to: {filename}")


def main():
    """Main function to measure post-optimization performance."""
    measurer = PostOptimizationPerformanceMeasurer()
    
    print("🚀 Starting post-optimization performance measurement...")
    print("This will compare current performance against the baseline.")
    print("=" * 80)
    
    # Generate comprehensive comparison report
    comparison_report = measurer.generate_comparison_report()
    
    if comparison_report:
        # Print summary
        measurer.print_comparison_summary(comparison_report)
        
        # Save detailed report
        save_comparison_report(comparison_report)
        
        print(f"\n" + "=" * 80)
        print("✅ Post-optimization performance measurement complete!")
        
        # Check if targets were met
        targets = comparison_report.get('target_verification', {})
        if targets.get('overall_target_met', False):
            print("🎯 Overall performance target achieved!")
        else:
            print("⚠️  Overall performance target not yet achieved.")
            
        print("=" * 80)
    else:
        print("❌ Could not complete comparison - baseline report missing")


if __name__ == "__main__":
    main()