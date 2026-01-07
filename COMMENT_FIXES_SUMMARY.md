# Summary of Test Comment Fixes

## Problem
Test comments had nonsensical fractional complex samples like "120 finite × ~0.4 complex samples" which doesn't make sense (you can't have 0.4 samples).

## Solution
Fixed all problematic comments to use whole numbers and clearer descriptions. The fixes fall into three categories:

### 1. Mixed Finite/Complex Strategy Fixes
When there's a finite dimension and a complex dimension, we now express it as:
- `N finite × M complex samples` where both N and M are whole numbers
- Example: `30 examples (6 finite × 5 complex samples)` means each of the 6 finite values gets paired with ~5 samples from the complex space

**Files Fixed:**
- `test_shortening_and_coordinate.py`: 50 → 30 examples (30 finite combinations × 1 complex sample)
- `test_performance.py`: 20 → 27 examples (9 finite combinations × 3 complex samples)
- `test_advanced_compatibility.py`: 
  - 20 → 15 examples (3 finite × 5 complex samples)
  - 20 → 18 examples (9 finite combinations × 2 complex samples)
- `test_rebuild_semantics.py`:
  - 3 → 15 examples (3 finite × 5 complex samples)
  - 2 → 10 examples (2 finite × 5 complex samples)
  - 50 → 48 examples (24 finite combinations × 2 complex samples)
- `test_font_properties.py`: 20 → 30 examples (6 finite × 5 complex samples) - 3 instances
- `test_comment_format.py`: 
  - 50 → 30 examples (6 finite × 5 complex samples)
  - 25 → 30 examples (6 finite × 5 complex samples)

### 2. Complex Combination Strategy Fixes
When there are multiple complex strategies combined with finite strategies, we now use:
- `Complex combination strategy: N examples (X finite combinations with Y complex strategies)`

**Files Fixed:**
- `test_rebuild_semantics.py`:
  - 50 examples (120 finite combinations with 5 complex strategies)
  - 50 examples (60 finite combinations with 3 complex strategies)
  - 50 examples (24 finite combinations with 4 complex strategies)

### 3. Pure Complex Strategy Fixes
When there's only complex strategies (no finite dimension), we simplified to:
- `Complex strategy: N examples (adequate coverage)`

**Files Fixed:**
- `test_sizing_behavior.py`: Removed incorrect "6 finite" claim
- `test_serialization.py`: Removed incorrect "6 finite" claim
- `test_shared_infrastructure.py`: Removed incorrect "6 finite" claim

### 4. Combination Strategy Fixes
When all strategies are finite (no complex strategies), we use:
- `Combination strategy: N examples (combination coverage)`

**Files Fixed:**
- `test_test_file_parser.py`: 20 → 28 examples (combination coverage)
- `test_duplicate_detector.py`: 20 → 36 examples (combination coverage)
- `test_code_duplication_minimization.py`: 15 → 18 examples (combination coverage)

## Key Principles Applied

1. **Whole numbers only**: No fractional samples (0.4, 0.7, etc.)
2. **Clear formulas**: For mixed finite/complex, use `finite_size × samples_per_value`
3. **Appropriate classification**: 
   - Use "Mixed finite/complex" only when there's exactly 1 finite and 1+ complex
   - Use "Complex combination" when there are multiple complex strategies with finite
   - Use "Combination" when all strategies are finite
   - Use "Complex" when all strategies are complex/infinite

## Total Changes
- 23 test files updated
- All fractional sample comments eliminated
- max_examples values adjusted where needed to ensure adequate coverage of finite dimensions
