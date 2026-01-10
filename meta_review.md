## Review of DEVIATIONS.md

I've examined each deviation against the actual test code. Here's my assessment:

### test_comment_standardizer_finite.py

**Line 37 deviation:** ❌ **Not legitimate**
- The comment says "Mixed finite/complex strategy: 50 examples (adequate coverage)"
- The strategies are `st.integers(min_value=0, max_value=10)`, `st.integers(min_value=11, max_value=50)`, and `st.integers(min_value=1, max_value=100).filter(...)` 
- These are all bounded integers, but the `.filter()` makes the third one complex (non-deterministic size). The "Mixed finite/complex" classification is actually reasonable here.
- The DEVIATIONS.md claims it should be "Combination strategy" but that's for multiple finite strategies combined. The filter makes this mixed.

**Line 111 deviation:** ✅ **Legitimate but minor**
- Uses `st.lists(st.text(...), ...)` which is complex, and `st.integers(...)` which is finite
- Comment says "Complex strategy: 30 examples" but should be "Mixed finite/complex strategy"
- Worth fixing for consistency.

### test_comment_standardizer_performance.py

**Line 123 deviation:** ✅ **Legitimate**
- The comment claims "5 finite × 5 complex samples" but `sampled_from` has 5 values, `integers(1-20)` has 20 values, and `text` is complex
- The math doesn't add up. Worth fixing.

### test_file_analyzer.py

**Line 309 deviation:** ⚠️ **Partially legitimate**
- The code accesses `_generate_rationale` which is private
- However, there's a comment: "Access private method to test rationale generation logic directly. Reference: TESTING.md Section 'Testing Exceptions'"
- TESTING.md does allow documented exceptions for private methods when no public API exists
- The deviation is technically correct but the code already documents the exception. **Low priority.**

### test_helper_availability.py

**Line 28 deviation:** ✅ **Legitimate**
- Class has `@pytest.mark.test_tests` but property-based tests inside should also have `@pytest.mark.property`
- Worth fixing.

**Lines 32, 54, 66, 79, 91, 122, 131, 140 deviation:** ❌ **Not legitimate**
- TESTING.md shows the comment format as being between `@given` and `@settings`, but the actual examples in TESTING.md show comments BEFORE `@given`:
  ```python
  @given(st.booleans())
  # Boolean strategy: 2 examples (True/False coverage)
  @settings(max_examples=2, deadline=None)
  ```
- The test file follows this exact pattern. The deviation is incorrect.

### test_refactoring_properties.py

**Lines 16-17 deviation:** ✅ **Legitimate**
- Uses `sys.path.insert(0, ...)` which is a code smell
- Should use proper relative imports or pytest's conftest mechanism
- Worth fixing.

**Line 24 deviation:** ⚠️ **Minor**
- Docstring says "performance" but doesn't measure timing
- The class tests discovery *functionality*, not performance metrics
- Could rename to `TestDiscoveryFunctionality` for clarity. **Low priority.**

**Line 27 deviation:** Same as above - name implies performance but tests functionality.

**Line 50 deviation:** ✅ **Legitimate**
- Hardcoded `assert len(test_lines) >= 50` is brittle
- Should be configurable or dynamic.

**Line 59 deviation:** ⚠️ **Debatable**
- Uses `@pytest.mark.parametrize` over TEST_MODULES (26 modules)
- TESTING.md says >10 values should use Hypothesis `sampled_from`
- However, for test discovery validation, you actually want to test ALL modules, not a sample
- **Not worth changing** - the parametrize is intentional here.

**Line 98 deviation:** ✅ **Legitimate**
- Hardcodes `'test_rebuild_scheduling.py'` as the "minimal" module
- Creates brittle dependency. Should be dynamic.

**Line 23 deviation:** ✅ **Legitimate**
- Multiple subprocess calls without `@pytest.mark.slow` marker
- Worth adding.

### test_shared_infrastructure.py

**Line 168 deviation:** ✅ **Legitimate**
- Import inside a loop is inefficient
- Should be at module top.

**Lines 174-184, 188-197 deviations:** ✅ **Legitimate**
- Tests only check that identical values are equal and that the return type is bool
- Don't verify that unequal values return False
- Worth fixing for completeness.

### test_strategy_classification.py

**Lines 16, 123 deviation:** ❌ **Not legitimate**
- The class has `@pytest.mark.property` which applies to all methods
- Individual methods don't need the marker when the class has it.

**Line 16 deviation (naming):** ⚠️ **Minor**
- `test_classify_strategies` could be more descriptive
- **Low priority.**

**Lines 24-31, 39-52, etc. deviation:** ⚠️ **Debatable**
- Hardcoded test names in meta-tests
- For meta-tests validating test infrastructure, some hardcoding is acceptable
- **Low priority.**

**Lines 16-122 deviation:** ⚠️ **Debatable**
- Could use parametrize for data-driven testing
- But the current structure is readable and maintainable
- **Low priority.**

**Lines 32-36, etc. deviation:** ⚠️ **Minor**
- Multiple asserts in loops
- For meta-tests, this is often acceptable for comprehensive validation
- **Low priority.**

### test_test_file_parser.py

**Line 25 deviation:** ⚠️ **Minor**
- Class docstring is slightly narrow but not inaccurate
- **Low priority.**

**Line 24 deviation:** Same - class name could be broader.

**Lines 36-66, etc. deviation:** ✅ **Legitimate**
- Duplicated boilerplate for temp file creation
- Should use a shared fixture or helper.

**Lines 57-64 deviation:** ✅ **Legitimate**
- Doesn't test the negative case (absence of rebuild assertions)
- Worth fixing.

**Lines 223-230 deviation:** ✅ **Legitimate**
- Same issue - incomplete coverage.

**Line 32 deviation:** ⚠️ **Minor**
- Docstring could be clearer
- **Low priority.**

---

## Summary: Worth Fixing

**High Priority (clear violations):**
1. `test_comment_standardizer_finite.py` line 111 - wrong strategy classification
2. `test_comment_standardizer_performance.py` line 123 - incorrect rationale math
3. `test_helper_availability.py` line 28 - missing `@pytest.mark.property`
4. `test_refactoring_properties.py` lines 16-17 - `sys.path.insert` hack
5. `test_refactoring_properties.py` line 50 - hardcoded threshold
6. `test_refactoring_properties.py` line 98 - hardcoded module name
7. `test_shared_infrastructure.py` line 168 - import inside loop
8. `test_shared_infrastructure.py` lines 174-197 - incomplete negative case testing
9. `test_test_file_parser.py` - duplicated boilerplate and incomplete coverage

**Low Priority (minor or debatable):**
- Performance class naming
- Missing `@pytest.mark.slow`
- Hardcoded test names in meta-tests
- Minor docstring improvements

**Not Legitimate:**
- Comment placement (lines 32, 54, etc. in test_helper_availability.py) - follows TESTING.md examples
- Missing markers on individual methods when class has marker
- Line 37 in test_comment_standardizer_finite.py - classification is reasonable