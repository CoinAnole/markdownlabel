# Fixed-List Property Tests Analysis

## Tests to Convert from Property-Based to Parametrized

Based on scanning the test suite, the following tests use `@given(st.sampled_from([...]))` with fixed lists and should be converted to `@pytest.mark.parametrize`:

### 1. test_refactoring_properties.py

**TestModuleNamingConsistency.test_module_names_follow_pattern**
- Current: `@given(st.sampled_from(['test_core_functionality.py', 'test_label_compatibility.py', ...]))`
- Fixed list of 12 module names
- Should be parametrized

**TestDiscoveryPerformance.test_individual_module_discovery_functionality**
- Current: `@given(st.sampled_from(['test_core_functionality.py', 'test_label_compatibility.py', ...]))`
- Fixed list of 10 module names
- Should be parametrized

### 2. test_core_functionality_properties.py

**TestCoreTestClassExistence.test_specific_class_exists_in_core_module**
- Current: `@given(st.sampled_from(['TestWidgetTreeGeneration', 'TestReactiveTextUpdates', ...]))`
- Fixed list of 4 class names
- Should be parametrized

**TestModuleLineCountConstraint (multiple methods)**
- Current: `@given(st.sampled_from(['test_core_functionality.py', 'test_label_compatibility.py', ...]))`
- Fixed list of module names
- Should be parametrized

**TestTimingAssertionRemoval (multiple methods)**
- Current: `@given(st.sampled_from(['test_core_functionality.py', 'test_label_compatibility.py', ...]))`
- Fixed list of module names
- Should be parametrized

**TestSilentPassPatternRemoval (multiple methods)**
- Current: `@given(st.sampled_from(['test_core_functionality.py', 'test_label_compatibility.py', ...]))`
- Fixed list of module names
- Should be parametrized

**TestBroadExceptionHandlingRemoval (multiple methods)**
- Current: `@given(st.sampled_from(['test_core_functionality.py', 'test_label_compatibility.py', ...]))`
- Fixed list of module names
- Should be parametrized

### 3. test_rebuild_scheduling.py

**test_font_name_change_schedules_deferred_rebuild**
- Current: `@given(st.sampled_from(["Roboto", "RobotoMono-Regular", "Arial"]))`
- Fixed list of 3 font names
- Should be parametrized

### 4. test_advanced_compatibility.py

**test_font_hinting_forwarded_to_labels**
- Current: `@given(st.sampled_from([None, 'normal', 'light', 'mono']))`
- Fixed list of 4 font hinting values
- Should be parametrized

**test_halign_change_rebuilds_widgets**
- Current: `@given(st.sampled_from(['left', 'center', 'right', 'justify']), st.sampled_from(['left', 'center', 'right', 'justify']))`
- Fixed list of alignment values (used twice)
- Should be parametrized with combinations

**test_valign_change_rebuilds_widgets**
- Current: `@given(st.sampled_from(['bottom', 'middle', 'center', 'top']), st.sampled_from(['bottom', 'middle', 'center', 'top']))`
- Fixed list of alignment values (used twice)
- Should be parametrized with combinations

**test_unicode_errors_change_rebuilds_widgets**
- Current: `@given(st.sampled_from(['strict', 'replace', 'ignore']), st.sampled_from(['strict', 'replace', 'ignore']))`
- Fixed list of unicode error values (used twice)
- Should be parametrized with combinations

### 5. test_performance.py

**test_halign_change_preserves_widget_tree**
- Current: `@given(st.sampled_from(['left', 'center', 'right', 'justify']))`
- Fixed list of 4 alignment values
- Should be parametrized

**test_halign_change_updates_descendant_labels**
- Current: `@given(st.sampled_from(['left', 'center', 'right', 'justify']))`
- Fixed list of 4 alignment values
- Should be parametrized

**test_valign_change_preserves_widget_tree**
- Current: `@given(st.sampled_from(['top', 'middle', 'bottom']))`
- Fixed list of 3 alignment values
- Should be parametrized

**test_valign_change_updates_descendant_labels**
- Current: `@given(st.sampled_from(['top', 'middle', 'bottom']))`
- Fixed list of 3 alignment values
- Should be parametrized

### 6. test_shortening_and_coordinate.py

**test_shorten_from_forwarded_to_paragraph**
- Current: `@given(st.sampled_from(['left', 'center', 'right']))`
- Fixed list of 3 values
- Should be parametrized

**test_shorten_from_forwarded_to_heading**
- Current: `@given(st.sampled_from(['left', 'center', 'right']))`
- Fixed list of 3 values
- Should be parametrized

**test_shorten_from_forwarded_to_list_items**
- Current: `@given(st.sampled_from(['left', 'center', 'right']))`
- Fixed list of 3 values
- Should be parametrized

### 7. test_text_properties.py

**test_unicode_errors_change_triggers_rebuild**
- Current: `@given(st.sampled_from(['strict', 'replace']), st.sampled_from(['replace', 'ignore']))`
- Fixed lists of unicode error values
- Should be parametrized with combinations

### 8. test_rtl_alignment.py

**test_auto_alignment_rtl_directions_use_right**
- Current: `@given(st.sampled_from(['rtl', 'weak_rtl']))`
- Fixed list of 2 values
- Should be parametrized

**test_auto_alignment_ltr_directions_use_left**
- Current: `@given(st.sampled_from(['ltr', 'weak_ltr', None]))`
- Fixed list of 3 values
- Should be parametrized

**test_auto_alignment_rtl_applies_to_mixed_content**
- Current: `@given(st.sampled_from(['rtl', 'weak_rtl']))`
- Fixed list of 2 values
- Should be parametrized

**test_auto_alignment_ltr_applies_to_mixed_content**
- Current: `@given(st.sampled_from(['ltr', 'weak_ltr', None]))`
- Fixed list of 3 values
- Should be parametrized

### 9. test_label_compatibility.py

**test_base_direction_property_accepted_and_stored**
- Current: `@given(st.sampled_from([None, 'ltr', 'rtl', 'weak_ltr', 'weak_rtl']))`
- Fixed list of 5 values
- Should be parametrized

**test_base_direction_property_change_after_creation**
- Current: `@given(st.sampled_from([None, 'ltr', 'rtl', 'weak_ltr', 'weak_rtl']))`
- Fixed list of 5 values
- Should be parametrized

### 10. test_font_properties.py

**Multiple font-related tests**
- Various tests using `st.sampled_from(KIVY_FONTS)` or fixed font lists
- Should be parametrized

## Tests to Keep as Property-Based

The following tests use `st.sampled_from` but should remain as property-based tests because they're part of larger composite strategies or used with truly random generation:

1. Tests that combine `st.sampled_from` with other random strategies (like `st.floats`, `st.text`)
2. Tests where the sampled values are part of a larger random data structure
3. Tests using `st.fixed_dictionaries` with sampled values as part of complex object generation

## Conversion Strategy

For each test to convert:
1. Replace `@given(st.sampled_from([...]))` with `@pytest.mark.parametrize('param_name', [...])`
2. Update function signature to accept the parameter
3. Ensure parameter names are descriptive
4. Maintain the same test logic
5. Keep the same test coverage and edge cases