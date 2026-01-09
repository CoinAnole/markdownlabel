# Meta-Tests Deviations from TESTING.md Guidelines

## kivy_garden/markdownlabel/tests/meta_tests/test_comment_format.py
- Lines 249-250,285,352,582,683: Testing Exceptions (private methods only if documented/no public API): "self.analyzer._analyze_file_content"
- Line 402: Property-Based Testing (comment must match strategy table): "# Mixed finite/complex strategy: 2 examples (2 finite × 1 complex sample)" mismatches small finite input (sampled_from 2 finite strategies)

## kivy_garden/markdownlabel/tests/meta_tests/test_comment_standardizer_boolean.py
- Line 38: Hypothesis comment rationale "(low max=2 acceptable for meta-test)" does not match table-specified format for Complex strategy "(adequate coverage)"; violates "exact comment format ... matching table".  
- Lines 29-40: Property-based test marked @pytest.mark.property uses max_examples=2 for Complex strategies (filtered integers + text), but Best Practices require "right-size max_examples based on strategy type" (Complex/Infinite: 10-50).

## kivy_garden/markdownlabel/tests/meta_tests/test_comment_standardizer_finite.py
- Line 37: Property-Based Testing > Comment Format: incorrect strategy classification and rationale for all-finite combination strategy (should be "Combination strategy: 50 examples (combination coverage)"). "# Complex combination strategy: 50 examples (440 finite combinations with 1 complex strategy)"
- Lines 39-42, 82-86: Test Naming Conventions: method name and docstring "Finite strategy comments reference input space size in rationale" do not accurately reflect assertion which allows "finite coverage" without input space size reference.
- Lines 120-121: Best Practices: truncates unique_items to 10 for sampled_from without rationale or handling for larger sets, potentially affecting test validity. "unique_items[:10]  # Limit to 10 items"

## kivy_garden/markdownlabel/tests/meta_tests/test_comment_standardizer_performance.py
- Line(s) 47: Property-Based Testing comment format violated: "# Mixed finite/complex strategy: 15 examples (15 finite combinations × 1 complex sample)" uses "finite combinations" and singular "sample" instead of "(X finite × Y complex samples)"
- Line(s) 49-52: Test Naming Conventions violated: "def test_execution_time_performance_rationale_documented" and docstring claim execution_time specific but assertions only verify generic "performance_rationale is not None" without reason check
- Line(s) 456-459: Best Practices/Don'ts violated: "def test_backup_and_rollback_functionality(self): ... assert True" claims to test functionality without verification (analogous to rebuild tests without assert_rebuild_occurred)

## kivy_garden/markdownlabel/tests/meta_tests/test_coverage_preservation.py
- Line(s) 183-184: Property-Based Testing comment format violated, incorrect "[Strategy Type]" "Mixed finite/complex" for all-finite combination (st.integers × st.sampled_from); table requires "Combination strategy" for all finite; inaccurate rationale "12 finite ×1 complex (# Mixed finite/complex strategy: 12 examples (12 finite ×1 complex".

## kivy_garden/markdownlabel/tests/meta_tests/test_file_analyzer.py
- Lines 294-296: Property-based test `test_rationale_generation_for_strategy_types` lacks `@pytest.mark.property` (Test Types and Markers)
- Lines 466-475: Property-based test `test_tool_integration_compatibility` lacks `@pytest.mark.property` (Test Types and Markers)
- Line 305: Testing undocumented private method `_generate_rationale(analysis, 10)` (Testing Exceptions: private methods only if documented/no public API)
- Line 473: Inaccurate rationale in Hypothesis comment "# Mixed finite/complex strategy: 20 examples (4 finite × 5 complex samples)"; does not match strategies (Property-Based Testing: exact comment format matching table)

## kivy_garden/markdownlabel/tests/meta_tests/test_helper_availability.py
- Line(s) 210-255: Test Naming Conventions violated: method name/docstring "test_all_test_files_import_from_test_utils" claims checking imports for all helper functions, but code only checks for `find_labels_recursive` calls (`node.func.id == 'find_labels_recursive'` lines 237,242).
- Lines 152-179, 181-208, 210-255: Best Practices/Helper Functions violated: duplicated file globbing, opening, AST parsing logic across three methods instead of reusable helper function from test_utils.py.
- Line 150: Best Practices (descriptive classes) violated: class docstring claims "Property tests" but all methods are unit tests, no `@given`/`Hypothesis`.

## kivy_garden/markdownlabel/tests/meta_tests/test_test_file_parser.py
- Lines 24-25: Class name `TestTestNameConsistency` and docstring `"Property tests for test name consistency."` do not describe all tests (general parser extraction, helper functions, assertion detection). [Test Organization - Descriptive class names that indicate what's being tested]
- Lines 27-30: Property-based test missing `@pytest.mark.property` before `@given(...)`. [Test Types and Markers - @pytest.mark.property for property-based tests using Hypothesis]
- Lines 67-79: Property-based test missing `@pytest.mark.property` before `@given(...)`. [Test Types and Markers - @pytest.mark.property for property-based tests using Hypothesis]
- Lines 35-37, 94-96, 132-134, 169-171, 210-212: Duplicate `with tempfile.NamedTemporaryFile(...)` boilerplate. [Helper Functions - use test_utils.py where reusable, no duplicates; Best Practices]

