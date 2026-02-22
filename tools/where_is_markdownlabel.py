#!/usr/bin/env python3
"""Show which MarkdownLabel installation Python is currently importing."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from importlib import metadata


def print_distributions() -> None:
    """Print installed distributions related to markdownlabel."""
    found = False
    for dist in metadata.distributions():
        name = (dist.metadata.get("Name") or "").strip()
        if "markdownlabel" not in name.lower():
            continue

        found = True
        print(f"- Distribution: {name}")
        try:
            print(f"  Version: {dist.version}")
        except Exception:
            print("  Version: <unknown>")

        try:
            print(f"  Location: {dist.locate_file('')}")
        except Exception:
            print("  Location: <unknown>")

        direct_url = dist.read_text("direct_url.json")
        if direct_url:
            try:
                parsed = json.loads(direct_url)
                print(f"  direct_url.json: {parsed}")
            except Exception:
                print(f"  direct_url.json: {direct_url}")
    if not found:
        print("- No installed distributions containing 'markdownlabel' were found.")


def main() -> int:
    print("Python executable:", sys.executable)
    print("Python version:", sys.version.split()[0])
    print("Current working directory:", Path.cwd())
    print("PYTHONPATH:", os.environ.get("PYTHONPATH", "<unset>"))
    print("sys.path[0]:", sys.path[0] if sys.path else "<empty>")
    print()

    # Keep Kivy import side effects minimal for this diagnostic command.
    os.environ.setdefault("KIVY_NO_ARGS", "1")
    os.environ.setdefault("KIVY_NO_CONSOLELOG", "1")

    try:
        import kivy_garden.markdownlabel as markdownlabel
    except Exception as exc:
        print("Import error: could not import kivy_garden.markdownlabel")
        print(f"Error detail: {exc!r}")
        print()
        print("Installed distributions:")
        print_distributions()
        return 1

    module_file = Path(markdownlabel.__file__).resolve()
    print("Imported module:", markdownlabel.__name__)
    print("Imported from:", module_file)
    print("Package directory:", module_file.parent)
    print("Module __version__:", getattr(markdownlabel, "__version__", "<missing>"))
    print()
    print("Installed distributions:")
    print_distributions()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
