# kivy_garden/markdownlabel/tests/meta_tests Deviations from TESTING.md Guidelines

## test_comment_standardizer_finite.py
- Line 37: Property-based test comment incorrectly classifies combination of finite integer strategies (`min_value`, `max_value`, `max_examples`) as "Mixed finite/complex strategy: 50 examples (adequate coverage)"; should be "Combination strategy: 50 examples (combination coverage)" per TESTING.md line 133.
- Line 111: Property-based test comment incorrectly classifies mixed finite (`max_examples`) and complex (`items` lists of text) strategies as "Complex strategy: 30 examples (adequate coverage)"; should be "Mixed finite/complex strategy: 30 examples (X finite × Y complex samples)" per TESTING.md line 140.

## test_comment_standardizer_performance.py
- Line 123: Inaccurate rationale in property-based testing comment; "Mixed finite/complex strategy: 25 examples (5 finite × 5 complex samples)" misrepresents strategy composition with sampled_from(5 finite values), integers(1-20) (20 finite values, product 100 finite coverage), and text (complex).

## test_file_analyzer.py
- Line 309: Accesses undocumented private method `_generate_rationale`; not a documented exception in TESTING.md "Testing Exceptions" section and `TestRationaleGeneration` class does not qualify as an edge case class.

## test_helper_availability.py
- Line 28: Class `TestHelperFunctionAvailability` containing property-based tests lacks `@pytest.mark.property` marker; only `@pytest.mark.test_tests` is present.
- Lines 32, 54, 66, 79, 91, 122, 131, 140: Hypothesis strategy comments placed before `@given` decorator instead of between `@given` and `@settings` decorators as per standardized comment format.

## test_refactoring_properties.py
- Lines 16-17: Uses `sys.path.insert` hack to import from parent `conftest.py`; violates import best practices and can cause side effects.
- Line 24: Class docstring "Property tests for test discovery performance" but no performance measurements (e.g., timing); only verifies basic functionality.
- Line 27: Method name `test_fast_test_discovery_baseline` implies speed/performance testing but asserts only discovery success and test count, no timing.
- Line 50: Hardcoded `assert len(test_lines) >= 50`; brittle threshold, should be dynamic or configurable.
- Line 59: `@pytest.mark.parametrize` over `TEST_MODULES` (likely >10 modules); guidelines recommend Hypothesis `st.sampled_from` for single enums >10 values.
- Line 98: Hardcodes specific module `'test_rebuild_scheduling.py'` for "minimal" test; creates brittle dependency, prefer dynamic selection of simple module.
- Line 23: Class `TestDiscoveryPerformance` runs multiple `subprocess` pytest invocations (parametrized); missing `@pytest.mark.slow` for performance-intensive tests.

## test_shared_infrastructure.py
- Line 168: `from kivy.uix.label import Label` import statement inside `for` loop; imports should be at module top following Python best practices.
- Lines 174-184: `test_colors_equal_function_available` does not assert `colors_equal` returns `False` for unequal colors (only asserts identical colors are equal and return type is `bool` for different colors), violating best practice to test both positive and negative cases.
- Lines 188-197: `test_padding_equal_function_available` does not assert `padding_equal` returns `False` for unequal padding (only asserts identical padding are equal and return type is `bool` for different padding), violating best practice to test both positive and negative cases.

## test_strategy_classification.py
- Lines 16, 123: Missing `@pytest.mark.meta` markers directly on test functions; marker is only on the class, violating requirement for markers on every test function.
- Line 16: Function name `test_classify_strategies` does not follow `test_<subject>_<verb>_<object>()` naming convention (lacks explicit subject).
- Line 123: Function name `test_strategy_descriptors_keys` does not follow naming convention (`keys` is not a verb or descriptive object).
- Lines 24-31, 39-52, 60-68, 76, 84-104: Hardcoded lists of specific test names for each strategy category in a meta test, violating guideline to avoid hardcoded test names where possible and dynamic adaptation.
- Lines 16-122: `test_classify_strategies` fails to use `@pytest.mark.parametrize` for data-driven testing of multiple test classifications, mandatory for similar cases.
- Lines 32-36, 53-56, 69-72, 77-80, 106-109: Multiple assert statements in loops within a single test, violating single logical assertion principle (prefer parametrization).

## test_test_file_parser.py
- Line 25: Class docstring "Property tests for test name consistency." inaccurately describes the class contents, which include unit tests for test class extraction, helper function extraction, and rebuild assertion detection beyond just property tests and name consistency.
- Line 24: Class name `TestTestNameConsistency` is overly specific and does not reflect the broader FileParser testing (e.g., extraction of classes, helpers, rebuild assertions).
- Lines 36-66, 96-108, 134-148, 171-189, 212-233: Duplicated boilerplate for temporary file creation, writing test code, parsing, and cleanup across multiple tests; violates best practices by not using a shared local helper function for reusable code.
- Lines 57-64: `test_rebuild_test_names_match_assertions` fails to assert that the parser correctly detects absence of rebuild assertions when `has_rebuild_assertion` is `False`, providing incomplete property-based coverage.
- Lines 223-230: `test_parser_detects_rebuild_assertions` asserts detection of rebuild assertions but does not verify non-detection in the method without widget ID checks, making the test incomplete.
- Line 32: Docstring for `test_rebuild_test_names_match_assertions` misleadingly implies enforcement of rebuild assertions based on test names rather than validation of the parser's detection logic.

