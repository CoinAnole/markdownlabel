# Technology Stack

## Core Technologies

- **Python**: 3.8+ (supports 3.8, 3.9, 3.10, 3.11, 3.12)
- **Kivy**: 2.0.0+ (UI framework)
- **mistune**: 3.0.0+ (Markdown parser)

## Build System

- **setuptools**: Standard Python packaging
- **namespace packages**: Uses `find_namespace_packages` for `kivy_garden.*` structure
- **Virtual environment**: `.venv/` directory (use `source .venv/bin/activate`)

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

## Common Commands

### Setup
```bash
# Activate virtual environment
source .venv/bin/activate

# Install package in development mode
python3 -m pip install -e .

# Install with dev dependencies
python3 -m pip install -e ".[dev]"
```

### Testing
```bash
# Run all tests
python3 -m pytest tests/

# Run with coverage
python3 -m pytest --cov=kivy_garden.markdownlabel tests/

# Run specific test file
python3 -m pytest tests/test_markdown_label.py
```

### Code Quality
```bash
# Check code style (flake8)
flake8 kivy_garden/

# Run pre-commit hook manually
./tools/hooks/pre-commit
```

### Documentation
```bash
# Build documentation
cd doc
make html

# View docs
# Open doc/build/html/index.html in browser
```

### Building Distribution
```bash
# Build wheel and source distribution
python3 setup.py bdist_wheel --universal
python3 setup.py sdist

# Check distribution
twine check dist/*

# Upload to PyPI (maintainers only)
twine upload dist/*
```

## Code Style

- **PEP8 compliance** with exceptions defined in `setup.cfg`
- **Max line length**: 80 characters
- **Flake8 configuration**: See `setup.cfg` for ignored rules
- Pre-commit hook available in `tools/hooks/pre-commit`

## CI/CD

- **GitHub Actions**: Automated testing on push/PR
- **Platforms tested**: Multiple OS environments
- **Coverage**: Tracked via coveralls
- **Artifacts**: Wheels generated for releases
