---
inclusion: always
---

# Python Setup for This Project

**CRITICAL**: This project uses Python 3 with a virtual environment.

## Always use these commands:

- **Activate venv first**: `source .venv/bin/activate`
- **Run Python**: Use `python3` (NOT `python`)
- **Run pip**: Use `python3 -m pip` or activate venv first

## Correct workflow:

```bash
source .venv/bin/activate
python3 script.py
```

OR run directly with venv python:

```bash
.venv/bin/python3 script.py
```

**Never use `python` command directly** - it may not exist or point to the wrong version.
