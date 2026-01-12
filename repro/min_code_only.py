import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

from kivy_garden.markdownlabel import MarkdownLabel

CODE = """```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(10))
```"""


class AppMinCode(App):
    def build(self):
        root = BoxLayout(orientation='vertical')
        md = MarkdownLabel(text=CODE, size_hint_y=None, auto_size_height=True)
        root.add_widget(md)
        Clock.schedule_once(lambda dt: self.stop(), 2)
        return root


if __name__ == '__main__':
    AppMinCode().run()

