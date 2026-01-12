import sys
from pathlib import Path
import argparse

# Ensure repo root (and local markdownlabel package) is importable when run directly.
REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

def _parse_args(argv):
    """Parse repro-specific args without breaking Kivy's own CLI parsing."""
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument(
        '--render-mode',
        dest='render_mode',
        default='widgets',
        choices=('widgets', 'texture', 'auto'),
        help="MarkdownLabel render_mode to use (default: widgets).",
    )
    args, unknown = parser.parse_known_args(argv[1:])
    # Preserve any unknown args for Kivy (and remove ours).
    remaining_argv = [argv[0], *unknown]
    return args, remaining_argv


def main():
    args, remaining_argv = _parse_args(sys.argv)
    sys.argv = remaining_argv

    # Delay Kivy imports until after we've stripped repro-only args.
    from kivy.app import App
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.scrollview import ScrollView
    from kivy.clock import Clock

    from kivy_garden.markdownlabel import MarkdownLabel

    class ReproductionApp(App):
        def __init__(self, render_mode='widgets', **kwargs):
            super().__init__(**kwargs)
            self._render_mode = render_mode

        def build(self):
            root = BoxLayout(orientation='vertical')
            scroll = ScrollView(size_hint=(1, 1), bar_width=0, do_scroll_x=False)
            self.feed_layout = BoxLayout(orientation='vertical', size_hint_y=None)
            self.feed_layout.bind(minimum_height=self.feed_layout.setter('height'))

            scroll.add_widget(self.feed_layout)
            root.add_widget(scroll)

            # Complex markdown content from the Fulcrum session.
            self.complex_content = """
# Markdown Rendering Stress Test

## Overview
This document tests **medium complexity** Markdown rendering. It includes nested elements, tables, code blocks, and more to stress the parser without overwhelming it.

### Key Features Tested
- ~~Strikethrough~~ text for *emphasis* and **bold**.
- [External link](https://example.com)
- Inline `code` like `print("Hello")`.
- Nested lists and tables.

## Nested Lists
- **Unordered List (UL)**
  - Level 1: Item A
    - Level 2: Subitem A1
      - Level 3: Deep subitem
    - Level 2: Subitem A2
  - Level 1: Item B
    - With a [link](https://x.ai) and `inline code`.

1. **Ordered List (OL)**
   2. Second item (note: intentional misnumbering for rendering test)
      1. Nested OL
         - Mixed with UL
      2. Another nested
   3. Third item

- [ ] Task list: unchecked
- [x] Task list: checked
  - [ ] Nested unchecked
  - [x] Nested checked

## Tables
Simple table:

| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Row 1A   | Row 1B   | Row 1C   |
| Row 2A   | Row 2B   | Row 2C   |

Advanced table with alignment:

| Left     | Center | Right   |
|:---------|:------:|--------:|
| Left     | Center |   Right |
| Longer left text | Short | 12345   |

## Code Blocks
### Inline Syntax Highlighting
```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(10))  # Output: 55
```
"""

            Clock.schedule_once(self.add_content, 0.5)
            return root

        def add_content(self, dt):
            print("Adding content...")
            label = MarkdownLabel(
                text=self.complex_content,
                render_mode=self._render_mode,
                size_hint_y=None,
                halign='left',
                valign='top',
                auto_size_height=True,
            )

            # Simulate a ChatScreen-style "bubble height" observer (no-op).
            label.bind(height=lambda instance, value: None)

            self.feed_layout.add_widget(label)
            print("Content added.")

            Clock.schedule_once(lambda dt: self.stop(), 5)

    ReproductionApp(render_mode=args.render_mode).run()

if __name__ == '__main__':
    main()

