# Design Document: Test Suite Improvements

## Overview

This design addresses critical flakiness, maintainability risks, and coverage gaps in the MarkdownLabel test suite. The improvements focus on eliminating timing-based assertions, strengthening meta-test reliability, converting inappropriate property tests to parametrized tests, adding missing security-focused test coverage, and cleaning up test configuration.

The key improvements are:
1. Remove timing-based assertions that cause CI flakiness
2. Replace silent-pass meta-tests with loud-fail assertions
3. Convert fixed-list property tests to parametrized tests
4. Add comprehensive URL markup safety testing
5. Implement robust code block serialization testing
6. Add explicit inline HTML security testing
7. Mark performance tests appropriately for CI
8. Centralize test configuration to eliminate duplication

## Architecture

### Current Test Structure Issues

```
test_refactoring_properties.py
├── Timing assertions (>= 0.5s, <= 15s) → Flaky on different machines
├── Subprocess pytest calls → Heavy, plugin conflicts
└── Property tests on fixed lists → Unnecessary complexity

test_core_functionality_properties.py
├── if os.path.exists(...): ... → Silent passes
├── except Exception: pass → Silent failures
└── Broad exception handling → Masks real issues

Multiple test files
├── Duplicate KIVY_NO_ARGS setup → Maintenance burden
├── Repeated environment configuration → Inconsistency
└── Missing security test coverage → Vulnerabilities
```

### Proposed Test Architecture

```
Improved Test Suite
├── Non-timing functional tests
│   ├── Return code verification
│   ├── Test collection count checks
│   └── PYTEST_DISABLE_PLUGIN_AUTOLOAD env var
├── Loud-fail assertions
│   ├── assert Path(...).exists()
│   ├── Specific exception handling
│   └── No broad except clauses
├── Appropriate test types
│   ├── Parametrized tests for fixed lists
│   ├── Property tests for random generation
│   └── Clear parameter naming
├── Security-focused coverage
│   ├── URL markup safety tests
│   ├── Code fence collision handling
│   └── HTML escaping verification
├── Performance test marking
│   ├── @pytest.mark.slow for heavy tests
│   ├── Reduced Hypothesis examples in CI
│   └── CI skip configuration
└── Centralized configuration
    ├── conftest.py environment setup
    ├── Shared fixtures
    └── No duplicate configuration
```

## Components and Interfaces

### 1. Timing-Free Test Verification

Replace timing assertions with functional checks:

```python
# OLD: Flaky timing assertion
assert discovery_time >= 0.5, "Suspiciously fast"
assert discovery_time <= 15.0, "Too slow"

# NEW: Functional verification
result = subprocess.run([
    sys.executable, '-m', 'pytest', '--collect-only', test_dir, '-q'
], env={**os.environ, 'PYTEST_DISABLE_PLUGIN_AUTOLOAD': '1'})

assert result.returncode == 0, f"Discovery failed: {result.stderr}"
assert "collected" in result.stdout, "No tests collected"
```

### 2. Loud-Fail Meta-Tests

Replace silent-pass patterns with explicit assertions:

```python
# OLD: Silent pass
if os.path.exists(core_module_path):
    try:
        test_names = self._extract_test_names_from_file(core_module_path)
    except Exception:
        pass

# NEW: Loud fail
core_module_path = Path('kivy_garden/markdownlabel/tests/test_core_functionality.py')
assert core_module_path.exists(), f"Core module not found: {core_module_path}"
test_names = self._extract_test_names_from_file(str(core_module_path))
```

### 3. Parametrized Test Conversion

Convert fixed-list property tests to parametrized tests:

```python
# OLD: Property test with fixed list
@given(st.sampled_from(['test_core.py', 'test_label.py']))
def test_module_names(self, module_name):
    # test logic

# NEW: Parametrized test
@pytest.mark.parametrize('module_name', [
    'test_core_functionality.py',
    'test_label_compatibility.py',
    'test_font_properties.py',
])
def test_module_names(self, module_name):
    # same test logic
```

### 4. URL Markup Safety

Add comprehensive URL safety testing:

```python
class TestURLMarkupSafety:
    """Test URL handling for markup injection prevention."""
    
    @pytest.mark.parametrize('unsafe_url', [
        'http://example.com]malicious[/ref][b]bold',
        'https://test.com[color=ff0000]red[/color]',
        'ftp://site.com]]][[[ref=evil]click[/ref]',
    ])
    def test_url_markup_escaping(self, unsafe_url):
        """URLs with markup characters should be escaped."""
        renderer = InlineRenderer()
        token = {
            'children': [{'type': 'text', 'raw': 'link'}],
            'attrs': {'url': unsafe_url}
        }
        result = renderer.link(token)
        
        # Should not contain unescaped markup-breaking characters
        assert ']' not in result or result.count('[ref=') == 1
        assert '[/ref]' in result  # Should still be a valid link
```

### 5. Code Fence Collision Handling

Implement robust fence selection:

```python
class MarkdownSerializer:
    def block_code(self, token: Dict[str, Any]) -> str:
        """Serialize code block with appropriate fence length."""
        raw = token.get('raw', '')
        attrs = token.get('attrs', {})
        language = attrs.get('info', '')
        
        # Find appropriate fence length
        fence_length = 3
        while '`' * fence_length in raw:
            fence_length += 1
        
        fence = '`' * fence_length
        return f'{fence}{language}\n{raw}\n{fence}'
```

### 6. HTML Security Testing

Add explicit HTML escaping tests:

```python
class TestHTMLSecurity:
    """Test HTML content security and escaping."""
    
    @pytest.mark.parametrize('html_content', [
        '<script>alert("xss")</script>',
        '<b>bold</b>',
        '<img src="x" onerror="alert(1)">',
        '&lt;escaped&gt;',
    ])
    def test_html_escaping(self, html_content):
        """HTML content should be escaped, not interpreted."""
        renderer = InlineRenderer()
        token = {'type': 'inline_html', 'raw': html_content}
        result = renderer.inline_html(token)
        
        # Should not contain unescaped HTML
        assert '<' not in result or result.startswith('[')
        assert '>' not in result or result.endswith(']')
```

### 7. Performance Test Marking

Mark heavy tests appropriately:

```python
@pytest.mark.slow
@settings(max_examples=10 if os.getenv('CI') else 100)
class TestPerformanceHeavy:
    """Heavy performance tests marked for CI control."""
    
    def test_large_document_rendering(self):
        """Test rendering of very large documents."""
        # Heavy test logic
```

### 8. Centralized Configuration

Clean up test configuration:

```python
# conftest.py - Single source of truth
@pytest.fixture(scope="session", autouse=True)
def setup_kivy_environment():
    """Configure Kivy for headless testing."""
    os.environ['KIVY_NO_ARGS'] = '1'
    os.environ['KIVY_NO_CONSOLELOG'] = '1'

# Individual test files - No duplicate setup
# Remove all individual os.environ settings
```

## Data Models

### Test Metadata

```python
# Test classification for CI control
TestMetadata = {
    'slow_tests': Set[str],  # Tests marked with @pytest.mark.slow
    'security_tests': Set[str],  # Tests covering security aspects
    'property_tests': Set[str],  # Remaining property-based tests
    'parametrized_tests': Set[str],  # Converted parametrized tests
}
```

### URL Safety Patterns

```python
# URL patterns that need escaping
UNSAFE_URL_PATTERNS = [
    r'\]',  # Closing bracket
    r'\[',  # Opening bracket  
    r'\[/?\w+[=\]]',  # Kivy markup patterns
]
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: No timing assertions in tests

*For any* test file in the test suite, the file SHALL NOT contain timing assertions with lower bounds (>= X seconds) or upper bounds (<= Y seconds) that can cause flakiness across different machine speeds.

**Validates: Requirements 1.1, 1.2**

### Property 2: Subprocess pytest uses stable configuration

*For any* test that calls pytest as a subprocess, the call SHALL include PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 in the environment and SHALL verify return codes and collection counts instead of execution timing.

**Validates: Requirements 1.3, 1.4**

### Property 3: No silent-pass file existence checks

*For any* test that checks file existence, the test SHALL use assert statements that fail loudly (assert Path(...).exists()) instead of conditional logic that can silently pass.

**Validates: Requirements 2.1**

### Property 4: No broad exception handling

*For any* test file, the file SHALL NOT contain broad exception handling patterns (except Exception: pass or except:) that can mask real failures.

**Validates: Requirements 2.2, 2.4**

### Property 5: Fixed-list property tests converted

*For any* property-based test that uses st.sampled_from with a fixed list of values, the test SHALL be converted to pytest.mark.parametrize with descriptive parameter names.

**Validates: Requirements 3.1, 3.4**

### Property 6: URL markup safety

*For any* URL containing Kivy markup characters (], [, or markup patterns), the InlineRenderer SHALL escape or quote the URL to prevent markup injection while preserving link functionality.

**Validates: Requirements 4.1, 4.2, 4.4**

### Property 7: Code fence collision handling

*For any* code content that contains backticks, the MarkdownSerializer SHALL choose a fence length longer than any backtick sequence in the content to prevent fence collision.

**Validates: Requirements 5.1, 5.2**

### Property 8: Code serialization round-trip

*For any* code block, serializing and then parsing the result SHALL produce valid Markdown that preserves the original content exactly.

**Validates: Requirements 5.3, 5.4**

### Property 9: HTML content escaping

*For any* inline HTML content, the InlineRenderer SHALL escape HTML tags to render them as plain text without introducing exploitable Kivy markup.

**Validates: Requirements 6.1, 6.2, 6.4**

### Property 10: Performance tests marked

*For any* genuinely performance-intensive test, the test SHALL be marked with @pytest.mark.slow and SHALL use reduced Hypothesis max_examples in CI environments.

**Validates: Requirements 7.1, 7.3**

### Property 11: No duplicate environment setup

*For any* test file (except conftest.py), the file SHALL NOT contain KIVY_NO_ARGS or KIVY_NO_CONSOLELOG environment variable setup, relying instead on centralized conftest.py configuration.

**Validates: Requirements 8.1, 8.4**

## Error Handling

### Test Conversion Failures

- Property test conversion errors: Preserve original test logic while changing test structure
- Parametrization errors: Ensure parameter names are descriptive and cover all original cases

### Security Test Edge Cases

- URL escaping failures: Fall back to safe rendering without links if escaping fails
- HTML content edge cases: Default to plain text rendering for any ambiguous content

### CI Configuration Issues

- Slow test marking: Default to running all tests if marker configuration fails
- Environment setup: Fail loudly if Kivy environment cannot be configured

## Testing Strategy

### Property-Based Testing Framework

Continue using **Hypothesis** for appropriate property-based tests (truly random inputs).

### Test Configuration

- Minimum 100 iterations for remaining property tests
- Reduced iterations (10-20) for slow tests in CI
- Use `@pytest.mark.slow` for performance-intensive tests

### Test Annotation Format

Each property-based test MUST be annotated with:
```python
# **Feature: test-improvements, Property {N}: {property_text}**
```

### Unit Tests

Unit tests cover specific examples and edge cases:
- Specific unsafe URLs with known markup patterns
- Specific HTML content with security implications
- Specific code blocks with fence collision scenarios
- CI configuration verification

### Property-Based Tests

Remaining property-based tests for truly random inputs:

1. **URL safety tests**: Generate random URLs with markup characters, verify safe handling
2. **Code fence tests**: Generate random code content, verify appropriate fence selection
3. **HTML escaping tests**: Generate random HTML content, verify safe escaping
4. **Configuration tests**: Verify no duplicate environment setup across test files

### Test Generators

```python
from hypothesis import strategies as st

# URL generator with markup characters
unsafe_urls = st.text(
    alphabet=st.characters(whitelist_categories=('L', 'N', 'P')),
    min_size=10, max_size=100
).map(lambda s: f"http://example.com/{s}]malicious[/ref]")

# Code content with backticks
code_with_backticks = st.text(
    alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S')),
    min_size=1, max_size=200
).filter(lambda s: '`' in s)

# HTML content generator
html_content = st.sampled_from([
    '<script>alert("xss")</script>',
    '<b>bold</b>',
    '<img src="x" onerror="alert(1)">',
    '&lt;escaped&gt;',
]).map(lambda s: f"<p>{s}</p>")
```

### Conversion Guidelines

1. **Timing to Functional**: Replace all timing assertions with return code and output verification
2. **Silent to Loud**: Replace conditional existence checks with explicit assertions
3. **Property to Parametrized**: Convert fixed-list property tests to parametrized tests
4. **Add Security Coverage**: Implement comprehensive security-focused test cases
5. **Centralize Configuration**: Move all environment setup to conftest.py