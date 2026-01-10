## Review of DEVIATIONS.md

I've examined each deviation against the actual test code. Here's my assessment:

### test_comment_standardizer_finite.py

**Line 111 deviation:** ✅ **Legitimate but minor**
- Uses `st.lists(st.text(...), ...)` which is complex, and `st.integers(...)` which is finite
- Comment says "Complex strategy: 30 examples" but should be "Mixed finite/complex strategy"
- Worth fixing for consistency.

### test_comment_standardizer_performance.py

**Line 123 deviation:** ✅ **Legitimate**
- The comment claims "5 finite × 5 complex samples" but `sampled_from` has 5 values, `integers(1-20)` has 20 values, and `text` is complex
- The math doesn't add up. Worth fixing.

### test_file_analyzer.py

**No legitimate deviations found.**

### test_helper_availability.py

**Line 28 deviation:** ✅ **Legitimate**
- Class has `@pytest.mark.test_tests` but property-based tests inside should also have `@pytest.mark.property`
- Worth fixing.

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

**No legitimate deviations found.**

### test_test_file_parser.py

**Lines 36-66, etc. deviation:** ✅ **Legitimate**
- Duplicated boilerplate for temp file creation
- Should use a shared fixture or helper.

**Lines 57-64 deviation:** ✅ **Legitimate**
- Doesn't test the negative case (absence of rebuild assertions)
- Worth fixing.

**Lines 223-230 deviation:** ✅ **Legitimate**
- Same issue - incomplete coverage.

---

## Summary: Worth Fixing

**High Priority (clear violations):**
1. `test_comment_standardizer_finite.py` line 111 - wrong strategy classification
2. `test_comment_standardizer_performance.py` line 123 - incorrect rationale math
3. `test_helper_availability.py` line 28 - missing `@pytest.mark.property`
4. `test_refactoring_properties.py` lines 16-17 - `sys.path.insert` hack
5. `test_refactoring_properties.py` line 50 - hardcoded threshold
6. `test_refactoring_properties.py` line 98 - hardcoded module name
7. `test_refactoring_properties.py` line 23 - missing `@pytest.mark.slow`
8. `test_shared_infrastructure.py` line 168 - import inside loop
9. `test_shared_infrastructure.py` lines 174-197 - incomplete negative case testing
10. `test_test_file_parser.py` - duplicated boilerplate and incomplete coverage

**Low Priority (minor or debatable):**
- Performance class naming in test_refactoring_properties.py