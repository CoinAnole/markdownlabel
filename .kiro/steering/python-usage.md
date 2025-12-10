---
inclusion: always
---

# Python Setup for This Project

**CRITICAL**: This project uses Python 3 with a virtual environment.

## Python Version Support

- **Python**: 3.8+ (supports 3.8, 3.9, 3.10, 3.11, 3.12)

## Build System

- **setuptools**: Standard Python packaging
- **namespace packages**: Uses `find_namespace_packages` for `kivy_garden.*` structure
- **Virtual environment**: `.venv/` directory

## Development Dependencies

```
pytest>=3.6          # Testing framework
pytest-cov           # Coverage reporting
pytest-asyncio       # Async test support
hypothesis>=6.0.0    # Property-based testing
sphinx_rtd_theme     # Documentation theme
pycodestyle          # Code style checking
coveralls            # CI coverage integration
```

## Always use direct venv paths (RECOMMENDED):

- **Run Python**: `.venv/bin/python3 script.py`
- **Run pip**: `.venv/bin/pip install package`
- **Run pytest**: `.venv/bin/pytest tests/`
- **Run any Python tool**: `.venv/bin/tool_name`

## Common Commands

### Setup
```bash
# Install package in development mode
.venv/bin/pip install -e .

# Install with dev dependencies
.venv/bin/pip install -e ".[dev]"
```

### Testing
```bash
# Run all tests
.venv/bin/pytest tests/

# Run with coverage
.venv/bin/pytest --cov=kivy_garden.markdownlabel tests/

# Run specific test file
.venv/bin/pytest tests/test_markdown_label.py
```

### Code Quality
```bash
# Check code style (flake8)
.venv/bin/python3 -m flake8 kivy_garden/

# Run pre-commit hook manually
./tools/hooks/pre-commit
```

### Building Distribution
```bash
# Build wheel and source distribution
.venv/bin/python3 setup.py bdist_wheel --universal
.venv/bin/python3 setup.py sdist

# Check distribution
.venv/bin/twine check dist/*

# Upload to PyPI (maintainers only)
.venv/bin/twine upload dist/*
```

## Code Style

- **PEP8 compliance** with exceptions defined in `setup.cfg`
- **Max line length**: 80 characters
- **Flake8 configuration**: See `setup.cfg` for ignored rules
- Pre-commit hook available in `tools/hooks/pre-commit`

**Why direct paths?** The `source .venv/bin/activate && python3` pattern can be unreliable in automated contexts. Direct venv paths are more explicit and error-proof.

**Never use `python` command directly** - it may not exist or point to the wrong version.
