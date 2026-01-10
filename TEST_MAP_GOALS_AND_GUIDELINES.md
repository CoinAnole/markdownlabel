# Test Map Creation: Goals and Guidelines

## Document Purpose

Create a comprehensive test suite map document named `TEST_MAP.md` in `kivy_garden/markdownlabel/tests/` that helps AI agents quickly understand the test organization without needing multiple tool calls.

## Critical Constraints

- **Maximum 800 lines** - Must fit in a single file read tool call
- **High information density** - Every line should provide value
- **Quick navigation** - Agents should find what they need in seconds
- **Complement TESTING.md** - Don't duplicate testing philosophy/guidelines, focus on "what's where"

## Target Audience

AI agents (like Claude, Grok, GPT-5) who need to:
- Understand what functionality is tested where
- Find relevant tests when modifying code
- Identify gaps in test coverage
- Navigate the test suite efficiently
- Understand test dependencies and infrastructure

## Document Structure

### 1. Quick Reference Section (50-100 lines)
- **Test file count and categories** - High-level overview
- **Key test files by purpose** - Where to look for specific functionality
- **Infrastructure files** - conftest.py, test_utils.py, modules/, meta_tests/
- **Quick lookup table** - Property → Test file mapping

### 2. Main Test Files Catalog (400-500 lines)
For each of the ~27 test files in the main directory, provide:
- **File name** and line count (for context on size)
- **Primary purpose** (1-2 sentences max)
- **Key test classes** (list with brief descriptions)
- **Property types tested** (if applicable: style-only, structure, both)
- **Test markers used** (@pytest.mark.property, @pytest.mark.needs_window, etc.)
- **Dependencies** (what it imports from test_utils, what fixtures it uses)
- **Related files** (which other test files cover related functionality)

### 3. Infrastructure & Support Files (100-150 lines)

#### conftest.py
- Fixtures provided
- TEST_MODULES list purpose
- Environment setup

#### test_utils.py
- Helper functions available
- Hypothesis strategies provided
- Constants defined

#### modules/ directory
- Purpose of each analysis module
- Which tools/meta-tests use them
- Brief description of functionality

#### meta_tests/ directory
- Purpose of meta-testing
- What each meta-test validates
- How they ensure test suite quality

### 4. Test Organization Patterns (50-100 lines)
- **By functionality groupings**:
  - Core functionality & rendering
  - Property testing (font, color, text, padding, shortening)
  - Rebuild semantics (6 files covering different aspects)
  - Renderer components (blocks, tables, inline)
  - Compatibility & edge cases
  - Performance & sizing
  - Serialization
  
- **Cross-cutting concerns**:
  - Which files test rebuild contracts
  - Which files use property-based testing heavily
  - Which files need Kivy window (@needs_window)
  - Which files are performance-sensitive (@slow)

### 5. Navigation Guide (50-100 lines)
Quick answers to common questions:
- "Where do I add tests for a new Label property?" → test_label_compatibility.py or specific property file
- "Where are rebuild semantics tested?" → 6 test_rebuild_*.py files
- "Where is inline markdown tested?" → test_inline_renderer.py
- "Where are tables tested?" → test_kivy_renderer_tables.py
- "How do I test a new markdown feature?" → Depends on block vs inline
- "Where are edge cases tested?" → Multiple files have edge case classes
- "Where is serialization tested?" → test_serialization.py
- "Where are performance tests?" → test_performance.py

## Content Guidelines

### Do's
✅ Use tables for dense information (file listings, property mappings)
✅ Use bullet points for lists of classes/functions
✅ Include line counts to give size context
✅ Cross-reference related files
✅ Mention key imports/dependencies
✅ Note which files are property-based test heavy
✅ Highlight files that need special attention (window, slow, etc.)
✅ Group related test files together
✅ Use consistent formatting throughout
✅ Include the TEST_MODULES list from conftest.py
✅ Note historical context (e.g., "split from test_rebuild_semantics.py")

### Don'ts
❌ Don't duplicate TESTING.md content (testing philosophy, best practices)
❌ Don't include full test method signatures
❌ Don't list every single test method (focus on classes and key tests)
❌ Don't explain how to write tests (that's in TESTING.md)
❌ Don't include code examples
❌ Don't explain Hypothesis or pytest basics
❌ Don't duplicate property classification lists (reference REBUILD_CONTRACT.md)
❌ Don't explain the rebuild contract (reference existing docs)
❌ Don't include implementation details of test helpers

### Tone & Style
- **Concise and factual** - No fluff, just information
- **Scannable** - Use formatting to enable quick scanning
- **Reference-oriented** - Point to other docs when appropriate
- **Agent-friendly** - Write for AI consumption, not human prose
- **Consistent terminology** - Use same terms as TESTING.md and structure.md

## Information Gathering Strategy

### Phase 1: Inventory (Read all main test files)
For each test file, extract:
1. Module docstring (purpose)
2. All class names and their docstrings
3. Count of test methods per class
4. Pytest markers used
5. Imports from test_utils
6. Line count

### Phase 2: Categorization
Group files by:
- Functionality area (properties, rebuild, rendering, etc.)
- Test type (property-based, parametrized, unit)
- Special requirements (window, slow)

### Phase 3: Infrastructure Analysis
- Read conftest.py fully
- Read test_utils.py to catalog helpers/strategies
- List modules/ files with brief purposes
- List meta_tests/ files with brief purposes

### Phase 4: Synthesis
Create the document following the structure above, ensuring:
- Total lines < 800
- High information density
- Easy navigation
- Complementary to TESTING.md

## Quality Checks

Before finalizing, verify:
- [ ] Line count ≤ 800
- [ ] All 27 main test files documented
- [ ] conftest.py fixtures listed
- [ ] test_utils.py helpers cataloged
- [ ] modules/ directory explained
- [ ] meta_tests/ directory explained
- [ ] Navigation guide answers common questions
- [ ] No duplication with TESTING.md
- [ ] Consistent formatting throughout
- [ ] Cross-references are accurate
- [ ] Tables are well-formatted
- [ ] Information is scannable

## Example Entry Format

```markdown
### test_font_properties.py (450 lines)
**Purpose**: Tests font-related properties (font_name, font_size, code_font_name, advanced font properties)

**Key Classes**:
- TestFontNameProperty - font_name forwarding and updates
- TestFontSizeProperty - font_size/base_font_size rebuild semantics
- TestCodeFontName - code_font_name for code blocks
- TestAdvancedFontProperties - font_family, font_context, font_features, etc.

**Property Types**: Style-only (all font properties after optimization)
**Markers**: @pytest.mark.property (heavy use), @pytest.mark.needs_window
**Dependencies**: test_utils (find_labels_recursive, collect_widget_ids, assert_no_rebuild)
**Related Files**: test_rebuild_property_classification.py, test_rebuild_style_propagation.py
```

## Success Criteria

The document is successful if an AI agent can:
1. Find which file tests a specific property in < 10 seconds
2. Understand test file relationships without reading code
3. Identify all files related to a feature area (e.g., "rebuild semantics")
4. Know which infrastructure files provide which helpers
5. Navigate to the right test file for adding new tests
6. Understand the test suite organization at a glance

## Final Notes

- This is a **reference document**, not a tutorial
- Optimize for **quick lookup**, not comprehensive explanation
- **Complement existing docs**, don't replace them
- Focus on **"what's where"**, not "how to test"
- Keep it **under 800 lines** - be ruthless about density
