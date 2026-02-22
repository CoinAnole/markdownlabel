#!/usr/bin/env python3
"""
Full-Featured MarkdownLabel Demo

A comprehensive demonstration of the MarkdownLabel widget showcasing
all Label-compatible properties and Markdown features.

Run with: python3 full_featured_demo.py
"""
from pathlib import Path

from kivy.config import Config

# Request window size before importing Window
Config.set("graphics", "width", "1400")
Config.set("graphics", "height", "900")

from kivy.app import App  # noqa: E402
from kivy.uix.scrollview import ScrollView  # noqa: E402
from kivy.uix.boxlayout import BoxLayout  # noqa: E402
from kivy.uix.label import Label  # noqa: E402
from kivy.core.window import Window  # noqa: E402
from kivy.graphics import Color, Rectangle  # noqa: E402
from kivy_garden.markdownlabel import MarkdownLabel  # noqa: E402


# Sample markdown content for property demonstrations
SAMPLE_MARKDOWN = """## Sample Heading

This is a paragraph with some text to demonstrate the property. \
It includes `inline code` for testing code font preservation.

Another paragraph to show line spacing effects. To make alignment \
differences clearer, this paragraph contains multiple sentences that \
should wrap across several lines when the text width is constrained. \
Notice how the right edge will appear ragged for left alignment but \
straight for justified alignment when enough wrapping occurs."""


class MarkdownDemoApp(App):
    """Demo app showcasing MarkdownLabel Label-compatible properties."""

    def __init__(self, **kwargs):
        """Initialize the app and set up caches."""
        super().__init__(**kwargs)
        self._full_sample_cache = None

    def build(self):
        """Build scrollable layout with property demonstration sections."""
        Window.size = (1400, 900)
        self.title = "MarkdownLabel Demo - Label Compatibility"

        # Create main vertical BoxLayout container
        main_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=20,
            padding=[10, 10, 10, 10]
        )
        main_layout.bind(minimum_height=main_layout.setter('height'))

        # Create ScrollView for vertical scrolling
        scroll_view = ScrollView(
            do_scroll_x=False,
            do_scroll_y=True
        )
        scroll_view.add_widget(main_layout)

        # Add font_name demonstration section
        font_name_variations = [
            ("font_name='Roboto' (default)", {"font_name": "Roboto"}),
            ("font_name='DejaVuSans'", {"font_name": "DejaVuSans"}),
        ]
        font_name_section = self.create_section("font_name", font_name_variations)
        main_layout.add_widget(font_name_section)

        # Add font_size demonstration section
        font_size_variations = [
            ("font_size=14", {"font_size": 14}),
            ("font_size=20", {"font_size": 20}),
            ("font_size=28", {"font_size": 28}),
        ]
        font_size_section = self.create_section("font_size", font_size_variations)
        main_layout.add_widget(font_size_section)

        # Add color demonstration section
        color_variations = [
            ("color=[1,1,1,1] (white)", {"color": [1, 1, 1, 1]}),
            ("color=[1,1,0,1] (yellow)", {"color": [1, 1, 0, 1]}),
            ("color=[0,1,1,1] (cyan)", {"color": [0, 1, 1, 1]}),
        ]
        color_section = self.create_section("color", color_variations)
        main_layout.add_widget(color_section)

        # Add line_height demonstration section
        line_height_variations = [
            ("line_height=1.0", {"line_height": 1.0}),
            ("line_height=1.5", {"line_height": 1.5}),
            ("line_height=2.0", {"line_height": 2.0}),
        ]
        line_height_section = self.create_section("line_height", line_height_variations)
        main_layout.add_widget(line_height_section)

        # Add halign demonstration section
        halign_variations = [
            ("halign='left'", {"halign": "left"}),
            ("halign='center'", {"halign": "center"}),
            ("halign='right'", {"halign": "right"}),
            ("halign='justify' (wrapped to show effect)", {
                "halign": "justify",
                "text_size": [600, None],
            }),
            ("halign='left' (wrapped, side-by-side comparison)", {
                "halign": "left",
                "text_size": [600, None],
            }),
        ]
        halign_section = self.create_section("halign", halign_variations)
        main_layout.add_widget(halign_section)

        # Add padding demonstration section
        padding_variations = [
            ("padding=[0,0,0,0]", {"padding": [0, 0, 0, 0]}),
            ("padding=[20,20,20,20]", {"padding": [20, 20, 20, 20]}),
            ("padding=[50,10,100,10]", {"padding": [50, 10, 100, 10]}),
        ]
        padding_section = self.create_section("padding", padding_variations, show_background=True)
        main_layout.add_widget(padding_section)

        # Add disabled demonstration section
        disabled_variations = [
            ("disabled=False (normal)", {"disabled": False}),
            ("disabled=True, disabled_color=[0.5,0.5,0.5,1]", {
                "disabled": True,
                "disabled_color": [0.5, 0.5, 0.5, 1]
            }),
        ]
        disabled_section = self.create_section("disabled", disabled_variations)
        main_layout.add_widget(disabled_section)

        # Add image rendering demonstration section
        image_section = self.create_image_display_section()
        main_layout.add_widget(image_section)

        # Add full sample_markdown.md display
        full_sample_section = self.create_full_sample_section()
        main_layout.add_widget(full_sample_section)

        return scroll_view

    def create_header(self, title):
        """Create a section header label."""
        header = Label(
            text=f"[b]{title}[/b]",
            markup=True,
            font_size='24sp',
            size_hint_y=None,
            height=50,
            color=[1, 0.8, 0, 1],
            halign='left',
            valign='middle'
        )
        header.bind(size=header.setter('text_size'))
        return header

    def create_variation(self, description, show_background=False, text=None, **properties):
        """Create a single MarkdownLabel variation with description."""
        variation_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=5,
            padding=[10, 5, 10, 5]
        )

        # Description label
        desc_label = Label(
            text=description,
            font_size='14sp',
            size_hint_y=None,
            height=30,
            color=[0.7, 0.7, 0.7, 1],
            halign='left',
            valign='middle'
        )
        desc_label.bind(size=desc_label.setter('text_size'))
        variation_layout.add_widget(desc_label)

        # MarkdownLabel with specified properties
        markdown_text = SAMPLE_MARKDOWN if text is None else text
        md_label = MarkdownLabel(
            text=markdown_text,
            size_hint_y=None,
            **properties
        )
        md_label.bind(minimum_height=md_label.setter('height'))
        md_label.bind(on_ref_press=self.on_ref_press)

        # Add background color if requested
        if show_background:
            with md_label.canvas.before:
                Color(0.2, 0.2, 0.3, 1)
                md_label.bg_rect = Rectangle(pos=md_label.pos, size=md_label.size)
            md_label.bind(pos=self._update_rect, size=self._update_rect)

        variation_layout.add_widget(md_label)

        # Calculate total height
        variation_layout.bind(
            minimum_height=variation_layout.setter('height')
        )

        return variation_layout

    def create_section(self, title, variations, show_background=False):
        """Create a section with header and variations."""
        section_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=10,
            padding=[0, 10, 0, 20]
        )
        section_layout.section_title = title

        # Add section header
        header = self.create_header(title)
        section_layout.add_widget(header)

        # Add each variation
        for description, props in variations:
            variation = self.create_variation(description, show_background=show_background, **props)
            section_layout.add_widget(variation)

        # Bind height to minimum_height
        section_layout.bind(minimum_height=section_layout.setter('height'))

        return section_layout

    def create_image_display_section(self):
        """Create a section demonstrating Markdown image rendering behavior."""
        image_path = Path(__file__).with_name("markdownlabel_test_pattern.png").resolve()

        image_markdown = (
            "Local image sizing comparison:\n\n"
            f"![Local pattern image]({image_path})\n\n"
            f"`{image_path}`"
        )

        image_variations = [
            ("render_mode='widgets', image_size_mode='contain_no_upscale' (default)", {
                "render_mode": "widgets",
                "text": image_markdown,
                "image_size_mode": "contain_no_upscale",
            }),
            ("render_mode='widgets', image_size_mode='fill_width'", {
                "render_mode": "widgets",
                "text": image_markdown,
                "image_size_mode": "fill_width",
            }),
        ]
        return self.create_section("image rendering", image_variations)

    def create_full_sample_section(self):
        """Create a section that displays the full sample_markdown.md content."""
        section_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=10,
            padding=[0, 10, 0, 20]
        )
        section_layout.section_title = "sample_markdown.md"

        header = self.create_header("sample_markdown.md (full content)")
        section_layout.add_widget(header)

        full_sample_text = self.load_full_sample_markdown()
        md_label = MarkdownLabel(
            text=full_sample_text,
            size_hint_y=None,
        )
        md_label.bind(minimum_height=md_label.setter('height'))
        md_label.bind(on_ref_press=self.on_ref_press)
        section_layout.add_widget(md_label)

        section_layout.bind(minimum_height=section_layout.setter('height'))
        return section_layout

    def load_full_sample_markdown(self):
        """Load and cache the contents of sample_markdown.md."""
        if self._full_sample_cache is None:
            sample_path = Path(__file__).with_name("sample_markdown.md")
            try:
                self._full_sample_cache = sample_path.read_text(encoding="utf-8")
            except Exception as exc:
                self._full_sample_cache = "Failed to load sample_markdown.md"
                print(f"Error loading sample_markdown.md: {exc}")
        return self._full_sample_cache

    def _update_rect(self, instance, value):
        """Update background rectangle position and size."""
        if hasattr(instance, 'bg_rect'):
            instance.bg_rect.pos = instance.pos
            instance.bg_rect.size = instance.size

    def on_ref_press(self, instance, ref):
        """Handle link click events from MarkdownLabel."""
        try:
            print(f"Link clicked: {ref}")
        except Exception as e:
            print(f"Error handling link click: {e}")


if __name__ == '__main__':
    MarkdownDemoApp().run()
