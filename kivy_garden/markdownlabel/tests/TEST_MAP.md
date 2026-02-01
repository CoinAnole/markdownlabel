# Test Map: MarkdownLabel Test Suite

## 1. Quick Reference

**Counts & Categories**
- 26 main unit tests (13,332 lines total, avg 513/file)
- conftest.py (123 lines): fixtures & TEST_MODULES
- test_utils.py (918 lines): helpers, Hypothesis strategies
- modules/ (14 files): meta-analysis tools
- meta_tests/ (20 files): test suite validators

**Key Files by Purpose**

| Category | Files | Notes |
|----------|-------|-------|
| Rebuild | test_rebuild_*.py (7 files) | Identity, propagation, scheduling, structure, classification |
| Style Properties | test_font_properties.py, test_color_properties.py, test_padding_properties.py, test_text_properties.py, test_shortening_properties.py, test_rtl_alignment.py, test_clipping_behavior.py, test_performance.py, test_advanced_compatibility.py | Font, color, padding, text, RTL, clipping, perf |
| Structure Properties | test_sizing_behavior.py, test_texture_render_mode.py, test_core_functionality.py | strict_label_mode, render_mode, text |
| Rendering | test_inline_renderer.py, test_kivy_renderer_blocks.py, test_kivy_renderer_tables.py | Inline, blocks, tables |
| Core/Compat | test_core_functionality.py, test_label_compatibility.py, test_coordinate_translation.py | Parsing, aliases, refs/anchors |
| Other | test_serialization.py, test_texture_sizing.py | Serialization, texture math |

**Infrastructure Overview**
- conftest.py: setup_kivy_environment (autouse), sample_markdown_texts, default_colors/padding, kivy_fonts; TEST_MODULES lists 27 main tests for meta
- test_utils.py: find_labels_recursive/collect_widget_ids/assert_no_rebuild/colors_equal; strategies: st_alphanumeric_text, markdown_heading, heading_token, etc.
- modules/: assertion_analyzer.py (patterns), duplicate_detector.py, file_analyzer.py (max_examples), strategy_analyzer.py, etc. (14 total)
- meta_tests/: test_assertion_analyzer.py, test_coverage_preservation.py, test_duplicate_detector.py, test_naming_convention_validator.py, etc. (20 total)

**Property → File Lookup** (key examples; full ref [`REBUILD_CONTRACT.md`](../REBUILD_CONTRACT.md))

| Property | Primary Files | Type |
|----------|---------------|------|
| font_name, code_font_name, line_height, font_family* | [`test_font_properties.py`](kivy_garden/markdownlabel/tests/test_font_properties.py) | Style |
| base_font_size/font_size | [`test_font_properties.py`](kivy_garden/markdownlabel/tests/test_font_properties.py) [`test_label_compatibility.py`](kivy_garden/markdownlabel/tests/test_label_compatibility.py) | Style |
| color, outline* | [`test_color_properties.py`](kivy_garden/markdownlabel/tests/test_color_properties.py) [`test_performance.py`](kivy_garden/markdownlabel/tests/test_performance.py) | Style |
| padding, text_padding | [`test_padding_properties.py`](kivy_garden/markdownlabel/tests/test_padding_properties.py) | Style |
| text_size | [`test_text_properties.py`](kivy_garden/markdownlabel/tests/test_text_properties.py) [`test_clipping_behavior.py`](kivy_garden/markdownlabel/tests/test_clipping_behavior.py) [`test_rebuild_text_size_and_code_blocks.py`](kivy_garden/markdownlabel/tests/test_rebuild_text_size_and_code_blocks.py) | Style |
| shorten*, max_lines, ellipsis_options | [`test_shortening_properties.py`](kivy_garden/markdownlabel/tests/test_shortening_properties.py) | Style |
| base_direction, halign | [`test_rtl_alignment.py`](kivy_garden/markdownlabel/tests/test_rtl_alignment.py) | Style |
| unicode_errors, strip | [`test_text_properties.py`](kivy_garden/markdownlabel/tests/test_text_properties.py) | Style |
| text | [`test_core_functionality.py`](kivy_garden/markdownlabel/tests/test_core_functionality.py) [`test_rebuild_scheduling.py`](kivy_garden/markdownlabel/tests/test_rebuild_scheduling.py) | Structure |
| render_mode | [`test_texture_render_mode.py`](kivy_garden/markdownlabel/tests/test_texture_render_mode.py) | Structure |
| strict_label_mode | [`test_sizing_behavior.py`](kivy_garden/markdownlabel/tests/test_sizing_behavior.py) | Structure |
| link_style | [`test_core_functionality.py`](kivy_garden/markdownlabel/tests/test_core_functionality.py) | Structure |
| link_color | [`test_color_properties.py`](kivy_garden/markdownlabel/tests/test_color_properties.py) | Structure |
| code_bg_color | [`test_color_properties.py`](kivy_garden/markdownlabel/tests/test_color_properties.py) | Structure |
| fallback_enabled, fallback_fonts, fallback_font_scales | [`test_rebuild_property_classification.py`](kivy_garden/markdownlabel/tests/test_rebuild_property_classification.py) | Structure |
| Property classification | [`test_rebuild_property_classification.py`](kivy_garden/markdownlabel/tests/test_rebuild_property_classification.py) | Meta |

(*advanced: font_features etc. [`test_advanced_compatibility.py`](kivy_garden/markdownlabel/tests/test_advanced_compatibility.py))

## 2. Main Test Files Catalog

### General Functionality Tests

#### [`test_advanced_compatibility.py`](kivy_garden/markdownlabel/tests/test_advanced_compatibility.py) (869 lines)
**Purpose**: Advanced compatibility: font forwarding, disabled color, reactive style updates.
**Key Classes**:
- TestAdvancedFontPropertiesForwarding - advanced font forwarding (~25 tests)
- TestDisabledColorApplication - disabled_color (~15 tests)
- TestStylePropertyReactiveUpdates - style changes preserve tree (~20 tests)
**Property Types**: Style-only
**Markers**: @pytest.mark.property
**Dependencies**: test_utils (find_labels_recursive, collect_widget_ids, assert_no_rebuild, colors_equal)
**Related**: test_font_properties.py, test_rebuild_style_propagation.py

#### [`test_clipping_behavior.py`](kivy_garden/markdownlabel/tests/test_clipping_behavior.py) (260 lines)
**Purpose**: Clipping with StencilView (height-constrained) vs expansion (unconstrained).
**Key Classes**:
- TestContentClippingWhenHeightConstrained - text_size/strict mode (~10 tests)
- TestNoClippingWhenUnconstrained - no constraints (~8 tests)
**Property Types**: Style-only (text_size, strict_label_mode)
**Markers**: @pytest.mark.property, @pytest.mark.unit
**Dependencies**: test_utils (has_clipping_container)
**Related**: test_sizing_behavior.py, test_text_properties.py

#### [`test_color_properties.py`](kivy_garden/markdownlabel/tests/test_color_properties.py) (193 lines)
**Purpose**: Color forwarding, code preservation, style no-rebuild.
**Key Classes**:
- TestColorPropertyForwarding - forwarding/updates (~8 tests)
- TestLinkStyling - links (2 tests)
**Property Types**: Style-only
**Markers**: @pytest.mark.property, @pytest.mark.unit
**Dependencies**: test_utils (color_strategy, find_labels_recursive)
**Related**: test_performance.py, test_rebuild_identity_preservation.py

#### [`test_coordinate_translation.py`](kivy_garden/markdownlabel/tests/test_coordinate_translation.py) (1031 lines)
**Purpose**: Refs/anchors coordinate translation from Labels to MarkdownLabel.
**Key Classes**:
- TestCoordinateTranslation - markup/translation (~15 tests)
- TestDeterministicRefsTranslation - ref math (5 tests)
- TestDeterministicAnchorsTranslation - anchor math (5 tests)
**Property Types**: N/A (math)
**Markers**: @pytest.mark.property, @pytest.mark.slow, @pytest.mark.needs_window
**Dependencies**: test_utils (find_labels_with_refs, get_widget_offset)
**Related**: test_core_functionality.py

#### [`test_core_functionality.py`](kivy_garden/markdownlabel/tests/test_core_functionality.py) (450 lines)
**Purpose**: Parsing, rendering, tree gen, text updates, links, nesting.
**Key Classes**:
- TestMarkdownToWidgetTreeGeneration - markdown to widgets (~10 tests)
- TestMarkdownTextPropertyUpdates - text triggers rebuild (~5 tests)
- TestMarkdownLinkRendering - links (~5 tests)
- TestMarkdownNestingStability - nesting (~15 tests)
**Property Types**: Both
**Markers**: @pytest.mark.property, @pytest.mark.needs_window
**Dependencies**: test_utils (markdown_heading, collect_widget_ids)
**Related**: test_rebuild_scheduling.py, test_inline_renderer.py

#### [`test_font_properties.py`](kivy_garden/markdownlabel/tests/test_font_properties.py) (890 lines)
**Purpose**: Font forwarding (name/size/line_height/advanced), heading scales, no-rebuild.
**Key Classes**:
- TestFontNamePropertyForwarding - font_name (~10 tests)
- TestLineHeightPropertyForwarding - line_height (~10 tests)
- TestAdvancedFontPropertyForwarding - advanced/code excl (20 tests)
- TestFontSizeImmediateUpdates - base_font_size (~5 tests)
- TestHeadingScalePreservation - headings (~5 tests)
**Property Types**: Style-only
**Markers**: @pytest.mark.property
**Dependencies**: test_utils (find_labels_recursive)
**Related**: test_advanced_compatibility.py, test_label_compatibility.py

#### [`test_inline_renderer.py`](kivy_garden/markdownlabel/tests/test_inline_renderer.py) (849 lines)
**Purpose**: InlineRenderer: formatting, escaping, URL/HTML security.
**Key Classes**:
- TestInlineFormattingConversion - tags (~8 tests)
- TestSpecialCharacterEscaping - markup (~5 tests)
- TestURLMarkupSafety - URLs (~10 tests)
- TestHTMLSecurity - XSS (~15 tests)
**Property Types**: N/A (unit)
**Markers**: @pytest.mark.property, @pytest.mark.unit
**Dependencies**: None
**Related**: test_core_functionality.py

#### [`test_kivy_renderer_blocks.py`](kivy_garden/markdownlabel/tests/test_kivy_renderer_blocks.py) (768 lines)
**Purpose**: Blocks: headings, paras, lists, code, quotes.
**Key Classes**:
- TestHeadingFontHierarchy - headings (~5 tests)
- TestParagraphMarkupEnabled - paras (2 tests)
- TestListStructurePreservation - lists (~5 tests)
- TestNestedListIndentation - nested (~4 tests)
- TestCodeBlockStyling - code (3 tests)
**Property Types**: N/A
**Markers**: @pytest.mark.property
**Dependencies**: test_utils (heading_token)
**Related**: test_kivy_renderer_tables.py

#### [`test_kivy_renderer_tables.py`](kivy_garden/markdownlabel/tests/test_kivy_renderer_tables.py) (338 lines)
**Purpose**: Tables: grid, cell alignment.
**Key Classes**:
- TestTableGridStructure - cols/cells (~5 tests)
- TestTableAlignmentApplication - alignment (~5 tests)
**Property Types**: N/A
**Markers**: @pytest.mark.property
**Dependencies**: test_utils (table_token)
**Related**: test_kivy_renderer_blocks.py

#### [`test_label_compatibility.py`](kivy_garden/markdownlabel/tests/test_label_compatibility.py) (430 lines)
**Purpose**: Label API compat: font_size alias, no-op props.
**Key Classes**:
- TestFontSizeAliasBidirectionality - alias sync (~5 tests)
- TestNoOpPropertiesAcceptance - bool props (~10 tests)
- TestNoOpPropertyAcceptanceAndStorage - advanced (~15 tests)
**Property Types**: Style-only
**Markers**: @pytest.mark.property
**Dependencies**: test_utils (st_rgba_color)
**Related**: test_font_properties.py

#### [`test_padding_properties.py`](kivy_garden/markdownlabel/tests/test_padding_properties.py) (714 lines)
**Purpose**: Padding/text_padding/label_padding norm/forward/updates.
**Key Classes**:
- TestPaddingApplication - norm (~5 tests)
- TestTextPaddingForwarding - to labels (~15 tests)
- TestTextPaddingDynamicUpdates - updates (~5 tests)
**Property Types**: Style-only
**Markers**: @pytest.mark.property
**Dependencies**: test_utils (text_padding_strategy, padding_equal)
**Related**: test_text_properties.py

#### [`test_performance.py`](kivy_garden/markdownlabel/tests/test_performance.py) (377 lines)
**Purpose**: Style updates no rebuild, disabled switching.
**Key Classes**:
- TestStyleOnlyPropertyUpdates - preserve tree (~20 tests)
**Property Types**: Style-only
**Markers**: @pytest.mark.slow, @pytest.mark.property
**Dependencies**: test_utils (find_labels_recursive)
**Related**: test_color_properties.py, test_rebuild_identity_preservation.py

#### [`test_rtl_alignment.py`](kivy_garden/markdownlabel/tests/test_rtl_alignment.py) (493 lines)
**Purpose**: RTL halign auto/override, direction changes.
**Key Classes**:
- TestAutoAlignmentRespectsDirection - auto (~15 tests)
- TestDirectionChangeUpdatesAlignment - changes (~10 tests)
- TestExplicitAlignmentOverridesAuto - overrides (~20 tests)
**Property Types**: Style-only
**Markers**: @pytest.mark.property, @pytest.mark.needs_window
**Dependencies**: test_utils (find_labels_recursive)
**Related**: test_core_functionality.py

#### [`test_serialization.py`](kivy_garden/markdownlabel/tests/test_serialization.py) (785 lines)
**Purpose**: Round-trip serialization, code fences.
**Key Classes**:
- TestMarkdownRoundTripSerialization - elements (~15 tests)
- TestCodeBlockSerialization - backticks (~10 tests)
**Property Types**: N/A
**Markers**: @pytest.mark.property
**Dependencies**: test_utils (markdown_heading)
**Related**: test_inline_renderer.py

#### [`test_shortening_properties.py`](kivy_garden/markdownlabel/tests/test_shortening_properties.py) (360 lines)
**Purpose**: Shortening props forwarding.
**Key Classes**:
- TestShorteningPropertyForwarding - to elements (~25 tests)
**Property Types**: Style-only
**Markers**: @pytest.mark.property
**Dependencies**: test_utils (collect_widget_ids)
**Related**: test_text_properties.py

#### [`test_sizing_behavior.py`](kivy_garden/markdownlabel/tests/test_sizing_behavior.py) (587 lines)
**Purpose**: auto_size_height, strict_label_mode sizing.
**Key Classes**:
- TestAutoSizingBehavior - auto (~10 tests)
- TestStrictLabelModeSizingBehavior - strict (~20 tests)
**Property Types**: Structure
**Markers**: @pytest.mark.property
**Dependencies**: None
**Related**: test_clipping_behavior.py

#### [`test_text_properties.py`](kivy_garden/markdownlabel/tests/test_text_properties.py) (590 lines)
**Purpose**: text_size forward/storage, unicode_errors/strip.
**Key Classes**:
- TestTextSizeForwarding - storage (~10 tests)
- TestUnicodeErrorsForwarding - errors (~15 tests)
- TestStripForwarding - strip (~15 tests)
**Property Types**: Style-only
**Markers**: @pytest.mark.property
**Dependencies**: test_utils (find_labels_recursive)
**Related**: test_padding_properties.py, test_shortening_properties.py

#### [`test_texture_render_mode.py`](kivy_garden/markdownlabel/tests/test_texture_render_mode.py) (689 lines)
**Purpose**: texture mode structure, links, hit-test, fallback.
**Key Classes**:
- TestTextureRenderModeStructure - images (~5 tests)
- TestTextureModeLinksHandling - refs (~5 tests)
- TestDeterministicTextureHitTesting - hit (~10 tests)
**Property Types**: Structure
**Markers**: @pytest.mark.slow
**Dependencies**: test_utils (find_images)
**Related**: test_texture_sizing.py

#### [`test_texture_sizing.py`](kivy_garden/markdownlabel/tests/test_texture_sizing.py) (394 lines)
**Purpose**: texture_size calc across widgets.
**Key Classes**:
- TestComprehensiveTextureSizeCalculation - validity (~20 tests)
**Property Types**: N/A
**Markers**: @pytest.mark.property
**Dependencies**: test_utils (simple_markdown_document)
**Related**: test_texture_render_mode.py

### Rebuild Behavior Tests

#### [`test_rebuild_advanced_properties.py`](kivy_garden/markdownlabel/tests/test_rebuild_advanced_properties.py) (531 lines)
**Purpose**: Advanced props (fonts/text/trunc) identity no rebuild PBT.
**Key Classes**:
- TestAdvancedFontPropertyIdentityPreservationPBT - fonts (48 tests)
- TestTextProcessingPropertyIdentityPreservationPBT - text (30 tests)
**Property Types**: Style-only
**Markers**: @pytest.mark.property, @pytest.mark.slow
**Dependencies**: test_utils (assert_no_rebuild)
**Related**: test_rebuild_identity_preservation.py, other rebuild_*.py

#### [`test_rebuild_identity_preservation.py`](kivy_garden/markdownlabel/tests/test_rebuild_identity_preservation.py) (496 lines)
**Purpose**: Style changes preserve IDs (no rebuild) PBT.
**Key Classes**:
- TestStylePropertyIdentityPreservationPBT - style (50 tests)
- TestRootIDPreservationPBT - root (48 tests)
**Property Types**: Style-only
**Markers**: @pytest.mark.property, @pytest.mark.slow
**Dependencies**: test_utils (collect_widget_ids)
**Related**: test_rebuild_style_propagation.py, test_performance.py

#### [`test_rebuild_property_classification.py`](kivy_garden/markdownlabel/tests/test_rebuild_property_classification.py) (213 lines)
**Purpose**: STYLE_ONLY/STRUCTURE sets validation.
**Key Classes**:
- TestPropertyClassificationSets - validation (~15 tests)
**Property Types**: N/A
**Markers**: None
**Dependencies**: None
**Related**: All rebuild_*.py; [`REBUILD_CONTRACT.md`](../REBUILD_CONTRACT.md)

#### [`test_rebuild_scheduling.py`](kivy_garden/markdownlabel/tests/test_rebuild_scheduling.py) (253 lines)
**Purpose**: Rebuild batching/deferral via Clock.
**Key Classes**:
- TestBatchedRebuilds - batching (~5 tests)
- TestDeferredRebuildScheduling - defer (~20 tests)
**Property Types**: Structure
**Markers**: @pytest.mark.property
**Dependencies**: test_utils (collect_widget_ids)
**Related**: test_core_functionality.py

#### [`test_rebuild_structure_changes.py`](kivy_garden/markdownlabel/tests/test_rebuild_structure_changes.py) (216 lines)
**Purpose**: Structure props trigger rebuild (new IDs) PBT.
**Key Classes**:
- TestStructurePropertyRebuildPBT - PBT (50 tests)
**Property Types**: Structure
**Markers**: @pytest.mark.property, @pytest.mark.slow
**Dependencies**: test_utils (collect_widget_ids)
**Related**: test_sizing_behavior.py, test_texture_render_mode.py

#### [`test_rebuild_style_propagation.py`](kivy_garden/markdownlabel/tests/test_rebuild_style_propagation.py) (241 lines)
**Purpose**: Style props propagate to descendants no rebuild PBT.
**Key Classes**:
- TestStylePropertyPropagationPBT - PBT (50 tests)
**Property Types**: Style-only
**Markers**: @pytest.mark.property, @pytest.mark.slow
**Dependencies**: test_utils (find_labels_recursive, assert_no_rebuild)
**Related**: test_rebuild_identity_preservation.py

#### [`test_rebuild_text_size_and_code_blocks.py`](kivy_garden/markdownlabel/tests/test_rebuild_text_size_and_code_blocks.py) (315 lines)
**Purpose**: text_size preservation/bindings, code monospace on font change.
**Key Classes**:
- TestTextSizePropertyIdentityPreservationPBT - text_size (50 tests)
- TestCodeBlockFontPreservationPBT - code (30 tests)
**Property Types**: Style-only
**Markers**: @pytest.mark.property, @pytest.mark.slow
**Dependencies**: test_utils (find_labels_recursive)
**Related**: test_text_properties.py, test_font_properties.py

## 3. Infrastructure & Support Files

### conftest.py (123 lines)
- Fixtures: setup_kivy_environment (session autouse, KIVY_NO_ARGS=1), sample_markdown_texts, default_colors, default_padding_values, kivy_fonts
- TEST_MODULES (24-54): 27 main tests for meta
- Env: repo_root in sys.path

### test_utils.py (918 lines)
- Helpers: find_labels_recursive, collect_widget_ids, assert_no_rebuild/colors_equal/padding_equal/floats_equal; FakeTouch, simulate_coverage_measurement
- Strategies: st_alphanumeric_text/st_rgba_color; markdown_heading/table_token; duplicate_helper_functions etc.
- Constants: KIVY_FONTS

### modules/ (14 files)
- assertion_analyzer.py: assertion patterns/mismatches
- comment_analysis.py: compliance
- comment_manager.py: re-exports
- comment_standardization.py: auto comments
- comment_validation.py: formats
- duplicate_detector.py: dups
- file_analyzer.py: max_examples opt
- file_parser.py: AST parser
- max_examples_calculator.py: optimal N
- naming_convention_validator.py: naming
- optimization_detector.py: CI/perf
- over_testing_validator.py: excess examples
- strategy_analyzer.py: classify strategies
- test_discovery.py: @given discovery

### meta_tests/ (20 files)
- test_assertion_analyzer.py, test_code_duplication_minimization.py, test_comment_format.py
- test_comment_standardizer_boolean.py/finite/performance.py
- test_core_functionality_properties.py, test_coverage_preservation.py
- test_documentation_compliance.py, test_duplicate_detector.py
- test_file_analyzer.py, test_helper_availability.py
- test_import_functionality.py, test_naming_convention_validator.py
- test_refactoring_properties.py, test_shared_infrastructure.py
- test_sizing_behavior_grouping.py, test_strategy_classification.py
- test_test_file_parser.py, test_texture_sizing_grouping.py

## 4. Test Organization Patterns

**Functionality Groupings**
- Core/Rendering: test_core_functionality.py (parsing/tree), test_inline_renderer.py (inline), test_kivy_renderer_blocks.py (blocks/lists), test_kivy_renderer_tables.py (tables), test_texture_sizing.py (texture math)
- Style Properties: test_font_properties.py (fonts), test_color_properties.py (colors), test_padding_properties.py, test_text_properties.py (text proc), test_shortening_properties.py (trunc), test_rtl_alignment.py (dir/align), test_clipping_behavior.py (clip), test_performance.py (perf), test_advanced_compatibility.py (advanced)
- Rebuild (7 files): test_rebuild_identity_preservation.py/propagation/advanced_properties/text_size_code/structure_changes/scheduling + test_rebuild_property_classification.py (sets)
- Structure: test_sizing_behavior.py (strict), test_texture_render_mode.py (render_mode), test_core_functionality.py (text)
- Compat/Edge: test_label_compatibility.py (Label API), test_coordinate_translation.py (refs)
- Serialization: test_serialization.py

**Cross-Cutting**
- Rebuild Contracts: test_rebuild_*.py (no-rebuild verify via collect_widget_ids/assert_no_rebuild)
- Property-Heavy PBT: Most style files; heavy in rebuild PBT (@slow, max_examples=50)
- @needs_window: test_coordinate_translation.py, test_core_functionality.py, test_rtl_alignment.py
- @slow (perf/PBT): test_coordinate_translation.py, test_performance.py, test_texture_render_mode.py, rebuild PBT files
- @pytest.mark.property: Nearly all main tests (Hypothesis focus)

## 5. Navigation Guide

- **New Label property tests?** [`test_label_compatibility.py`](kivy_garden/markdownlabel/tests/test_label_compatibility.py) (no-op/alias) or prop-specific (e.g. font → test_font_properties.py)
- **Rebuild semantics?** test_rebuild_*.py (6 core + classification); verify no-rebuild w/ assert_no_rebuild
- **Inline markdown?** [`test_inline_renderer.py`](kivy_garden/markdownlabel/tests/test_inline_renderer.py) (formatting/escape)
- **Block elements?** [`test_kivy_renderer_blocks.py`](kivy_garden/markdownlabel/tests/test_kivy_renderer_blocks.py) (headings/lists/code)
- **Tables?** [`test_kivy_renderer_tables.py`](kivy_garden/markdownlabel/tests/test_kivy_renderer_tables.py)
- **Refs/anchors/coords?** [`test_coordinate_translation.py`](kivy_garden/markdownlabel/tests/test_coordinate_translation.py)
- **Style no-rebuild perf?** [`test_performance.py`](kivy_garden/markdownlabel/tests/test_performance.py), test_rebuild_identity_preservation.py
- **Structure rebuild?** test_rebuild_structure_changes.py, test_sizing_behavior.py (strict), test_texture_render_mode.py
- **Serialization round-trip?** [`test_serialization.py`](kivy_garden/markdownlabel/tests/test_serialization.py)
- **Helpers/fixtures?** [`test_utils.py`](kivy_garden/markdownlabel/tests/test_utils.py), conftest.py; meta-tests validate
- **Property classification gaps?** [`test_rebuild_property_classification.py`](kivy_garden/markdownlabel/tests/test_rebuild_property_classification.py), [`REBUILD_CONTRACT.md`](../REBUILD_CONTRACT.md)
