# Deviations

## test_assertion_analyzer.py

No deviations found

## test_code_duplication_minimization.py

No deviations found

## test_comment_format.py

No deviations found

## test_comment_standardizer.py

- Line 391: Missing strategy type in standardized comment for property-based test - `test_sampled_from_finite_strategy_documentation` uses `@settings(max_examples=30, deadline=None)` but the comment `# Complex strategy: 30 examples (adequate coverage)` does not follow the required format `# [Strategy Type] strategy: [N] examples ([Rationale])`. The comment must specify the strategy type before the word "strategy" (e.g., "Finite strategy: 30 examples (adequate coverage)" or "Mixed finite/complex strategy: 30 examples (adequate coverage)"). Per TESTING.md section "Property-Based Testing Optimization", the format requires the strategy type to be explicitly stated. The test uses `st.lists(st.text(...))` and `st.sampled_from()` which involves finite elements sampled from a list, requiring an explicit strategy type classification.

## test_core_functionality_properties.py

- Line 72: Silent-pass file existence check - `test_no_timing_assertions_in_test_files` uses `if not module_path.exists(): return` which silently skips the test when the file doesn't exist. Per TESTING.md section "Test Naming Conventions" under "Rebuild Testing Names" and "Best Practices", tests should use `assert Path(...).exists()` to fail loudly instead of conditional logic that can silently pass. The pattern appears in multiple test methods (lines 72, 162, 227, 289, 413, 545, 575, 654) and should be replaced with `assert module_path.exists()` to ensure test failures are visible.

## test_documentation_compliance.py

No deviations found

## test_coverage_preservation.py

No deviations found

## test_duplicate_detector.py

No deviations found

## test_file_analyzer.py

No deviations found

## test_helper_availability.py

No deviations found

## test_naming_convention_validator.py

No deviations found

## test_refactoring_properties.py

- Line 76: Silent-pass file existence check - `test_individual_module_discovery_functionality` uses `if not os.path.exists(module_path): return` which silently skips the test when the file doesn't exist. Per TESTING.md section "Test Naming Conventions" under "Rebuild Testing Names" and "Best Practices", tests should use `assert os.path.exists(module_path)` to fail loudly instead of conditional logic that can silently pass. The pattern appears again at line 110 and should be replaced with assertions to ensure test failures are visible.

- Line 110: Silent-pass file existence check - `test_discovery_startup_functionality` uses `if not os.path.exists(module_path): pytest.skip(...)` which skips the test with a pytest.skip call. While this is better than a silent return, per TESTING.md best practices, tests should fail loudly with assertions rather than skip when checking for expected file existence. The pattern should be replaced with `assert os.path.exists(module_path)` to ensure test failures are visible when expected files are missing.

## test_shared_infrastructure.py

No deviations found

## test_sizing_behavior_grouping.py

No deviations found

## test_strategy_classification.py

- Line 50: Incorrect strategy type in comment - `test_small_sampled_from_classification` uses `@given(st.lists(st.text(...), min_size=1, max_size=10))` with comment `# Complex strategy: 10 examples (adequate coverage)` but the strategy is actually generating sampled_from lists (finite). Per TESTING.md section "Property-Based Testing Optimization", the comment format requires correct strategy type classification. The strategy uses `st.lists()` with `st.text()` which creates a finite list of text items, making it a "Small finite strategy" with comment format `# Small finite strategy: [N] examples (input space size: [N])` where N is the list length.

- Line 78: Incorrect strategy type in comment - `test_complex_strategy_classification` uses `@given(st.sampled_from([...]))` with comment `# Small finite strategy: 3 examples (input space size: 3)` but the test asserts `analysis.strategy_type == StrategyType.COMPLEX`. Per TESTING.md section "Property-Based Testing Optimization", the comment must accurately reflect the strategy type being tested. The test is verifying that the classifier identifies this as COMPLEX (not SMALL_FINITE), so the comment should reflect what the strategy actually is (a finite sampled_from) rather than what it's being classified as.

- Line 157: Incorrect strategy type in comment - `test_complex_strategy_uses_complexity_based_examples` uses `@given(st.integers(min_value=1, max_value=4))` with comment `# Small finite strategy: 4 examples (input space size: 4)` but the test simulates a complex strategy using `StrategyAnalysis(strategy_type=StrategyType.COMPLEX, ...)`. Per TESTING.md section "Property-Based Testing Optimization", the comment must accurately reflect the strategy type being tested. The @given decorator generates complexity levels (1-4) for simulating complex strategies, not a small finite strategy itself.

- Line 233: Incorrect strategy type in comment - `test_large_combination_capped_at_fifty` uses `@given(st.integers(min_value=6, max_value=10))` with comment `# Small finite strategy: 5 examples (input space size: 5)` but the test creates a combination strategy with `st.tuples(st.integers(...), st.integers(...))` which is a combination strategy. Per TESTING.md section "Property-Based Testing Optimization", the comment format requires correct strategy type classification. The @given generates the size for each integer range (6-10), then creates a combination strategy, so the comment should reflect that it's a combination strategy, not a small finite strategy.

## test_test_file_parser.py

No deviations found

## test_texture_sizing_grouping.py

No deviations found
