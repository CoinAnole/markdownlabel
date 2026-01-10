# kivy_garden/markdownlabel/tests/meta_tests Deviations from TESTING.md Guidelines

## test_comment_standardizer_finite.py
- Line 111: Property-based test comment incorrectly classifies mixed finite (`max_examples`) and complex (`items` lists of text) strategies as "Complex strategy: 30 examples (adequate coverage)"; should be "Mixed finite/complex strategy: 30 examples (X finite × Y complex samples)" per TESTING.md line 140.

## test_comment_standardizer_performance.py
- Line 123: Inaccurate rationale in property-based testing comment; "Mixed finite/complex strategy: 25 examples (5 finite × 5 complex samples)" misrepresents strategy composition with sampled_from(5 finite values), integers(1-20) (20 finite values, product 100 finite coverage), and text (complex).

## test_file_analyzer.py
- No legitimate deviations found.

## test_helper_availability.py
- Line 28: Class `TestHelperFunctionAvailability` containing property-based tests lacks `@pytest.mark.property` marker; only `@pytest.mark.test_tests` is present.

## test_refactoring_properties.py
- Lines 16-17: Uses `sys.path.insert` hack to import from parent `conftest.py`; violates import best practices and can cause side effects.
- Line 24: Class docstring "Property tests for test discovery performance" but no performance measurements (e.g., timing); only verifies basic functionality.
- Line 27: Method name `test_fast_test_discovery_baseline` implies speed/performance testing but asserts only discovery success and test count, no timing.
- Line 50: Hardcoded `assert len(test_lines) >= 50`; brittle threshold, should be dynamic or configurable.
- Line 98: Hardcodes specific module `'test_rebuild_scheduling.py'` for "minimal" test; creates brittle dependency, prefer dynamic selection of simple module.

## test_shared_infrastructure.py
- Line 168: `from kivy.uix.label import Label` import statement inside `for` loop; imports should be at module top following Python best practices.
- Lines 174-184: `test_colors_equal_function_available` does not assert `colors_equal` returns `False` for unequal colors (only asserts identical colors are equal and return type is `bool` for different colors), violating best practice to test both positive and negative cases.
- Lines 188-197: `test_padding_equal_function_available` does not assert `padding_equal` returns `False` for unequal padding (only asserts identical padding are equal and return type is `bool` for different padding), violating best practice to test both positive and negative cases.

## test_strategy_classification.py
- No legitimate deviations found.

## test_test_file_parser.py
- Lines 36-66, 96-108, 134-148, 171-189, 212-233: Duplicated boilerplate for temporary file creation, writing test code, parsing, and cleanup across multiple tests; violates best practices by not using a shared local helper function for reusable code.
- Lines 57-64: `test_rebuild_test_names_match_assertions` fails to assert that the parser correctly detects absence of rebuild assertions when `has_rebuild_assertion` is `False`, providing incomplete property-based coverage.
- Lines 223-230: `test_parser_detects_rebuild_assertions` asserts detection of rebuild assertions but does not verify non-detection in the method without widget ID checks, making the test incomplete.

