# Deviations from TESTING.md Guidelines

## test_advanced_compatibility.py
- Lines **173, 203, 382, 519, 557, 595, 629, 695, 729, 762, 794, 837, 869**: Manual `assert ids_before == ids_after` instead of using `assert_no_rebuild(widget, ids_before)` helper.
- Lines **296, 323, 349, 373, 388, 399**: Access to undocumented private attribute `lbl._is_code`.
- Lines **489-491**: Class `TestReactiveRebuildOnPropertyChange` name and docstring misleading, as tests verify no rebuild (preservation).

## test_coordinate_translation.py
- Lines **106, 113, 120, 127, 177, 198, 218**: Unit tests missing `@pytest.mark.unit` marker.
- Line **174**: Exact list containment check (expected_box in aggregated_refs[url]) for float coordinates without tolerance.
- Lines **300-303, 329-330**: Exact equality assertions (==) on float computations without tolerance or `floats_equal` helper.
- Lines **425-427, 486-488, 545-547, 594-596, 683-686, 766-769, 823-826, 880-883, 928-931, 1015-1018**: Manual float comparisons using `abs(diff) < 0.001` instead of `floats_equal` helper from test_utils.py.

## test_core_functionality.py
- Lines **327-329, 346-348, 365-367**: For medium finite strategy `st.integers(min_value=1, max_value=15)` (input space size: 15), `max_examples=20` used instead of 15, with comment reflecting incorrect example count.

## test_kivy_renderer_blocks.py
- Lines **527, 550, 570, 588**: Accesses private attribute `renderer._nesting_depth`.
- Lines **536, 557, 597**: Calls private method `renderer._render_token`.
- Line **591**: Accesses private attribute `renderer._max_nesting_depth`.
- Class `TestDeepNestingTruncation` (lines **515-607**): Accesses undocumented private attributes/methods without qualifying as edge case class or listed exception.

## test_kivy_renderer_tables.py
- Lines **152, 225**: Direct calls to private method `renderer._render_table_cell()` in `TestTableAlignmentApplication` class (not documented exception, not edge case class).

## test_padding_properties.py
- Lines **118, 265, 317, 362, 620**: Manual `assert ids_before == ids_after` instead of `assert_no_rebuild`.
- Lines **253, 264, 304, 316, 349, 361**: `collect_widget_ids(..., exclude_root=True)` uses undocumented parameter.
- Lines **40-46, 59-65, 74-80, 89-95, 109-112, 120-124, 131-137, 277-284, 709-715**: Manual `abs(actual - exp) < 0.001` instead of `padding_equal` helper.
- Lines **390-546** (class `TestPaddingWithNestedStructures`): Misleading class name (tests `text_padding`, suggests container `padding`).

## test_rebuild_advanced_properties.py
- Lines **101-104, 164-167, 244-247**: Manual widget ID equality instead of `assert_no_rebuild`.
- Lines **268-289**: Local helper accesses undocumented private `_is_code` (line 281).
- Lines **61, 207, 316, 495**: Inaccurate Hypothesis strategy comments.

## test_rebuild_identity_preservation.py
- Line **277**: Mixed strategy comment uses incorrect rationale "(sampling from 120 finite combinations)" instead of "(X finite × Y complex samples)".
- Line **339**: Mixed strategy comment inaccurately "24 finite × 2 complex"; 4 complex strategies.

## test_rebuild_scheduling.py
- Lines **206-208**: Access to undocumented private `label._rebuild_trigger`.
- Lines **105-250**: Class `TestDeferredRebuildScheduling` marked `@pytest.mark.property` but contains non-Hypothesis tests (parametrized line 151, unit line 180).

## test_sizing_behavior.py
- Lines **45, 110, 204, 381**: Tests assert preconditions/indicators, not actual height binding/absence.
- Lines **546, 553**: `collect_widget_ids(..., exclude_root=True)` undocumented parameter.
- Line **555**: Manual `assert ids_before != ids_after` instead of `assert_rebuild_occurred`.

## test_text_properties.py
- Lines **260-279, 284-304, 309-329**: Lack widget tree preservation assertions for style-only `text_size` changes.

