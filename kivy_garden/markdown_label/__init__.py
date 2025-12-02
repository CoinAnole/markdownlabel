"""
MarkdownLabel
=============

A Kivy widget that parses and renders Markdown documents as structured,
interactive Kivy UI elements. It serves as a drop-in replacement for Kivy's
standard Label widget but supports full Markdown syntax.

Example usage::

    from kivy_garden.markdown_label import MarkdownLabel
    
    label = MarkdownLabel(text='# Hello World\\n\\nThis is **bold** text.')
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import (
    StringProperty, 
    NumericProperty, 
    ColorProperty
)

import mistune
from mistune.plugins.table import table
from mistune.plugins.formatting import strikethrough

from .inline_renderer import InlineRenderer
from .kivy_renderer import KivyRenderer
from .markdown_serializer import MarkdownSerializer

__all__ = ('MarkdownLabel', 'InlineRenderer', 'KivyRenderer', 'MarkdownSerializer')

from ._version import __version__


class MarkdownLabel(BoxLayout):
    """A :class:`~kivy.uix.boxlayout.BoxLayout` based widget that renders
    Markdown text as a Kivy widget tree.
    
    The MarkdownLabel parses Markdown text using mistune and renders it as
    a hierarchy of Kivy widgets. It supports headings, paragraphs, lists,
    tables, code blocks, block quotes, images, and inline formatting.
    
    Events:
        on_ref_press: Dispatched when a link is clicked. The event data
            contains the URL of the clicked link.
    
    Example::
    
        label = MarkdownLabel(text='# Hello\\n\\nThis is **bold** text.')
        label.bind(on_ref_press=lambda instance, ref: print(f'Clicked: {ref}'))
    """
    
    text = StringProperty('')
    """Markdown text to render.
    
    :attr:`text` is a :class:`~kivy.properties.StringProperty` and defaults
    to an empty string.
    """
    
    base_font_size = NumericProperty(15)
    """Base font size in sp for body text.
    
    Heading sizes are calculated as multiples of this value:
    - h1: 2.5x
    - h2: 2.0x
    - h3: 1.75x
    - h4: 1.5x
    - h5: 1.25x
    - h6: 1.0x
    
    :attr:`base_font_size` is a :class:`~kivy.properties.NumericProperty`
    and defaults to 15.
    """
    
    code_font_name = StringProperty('RobotoMono-Regular')
    """Font name for code blocks and inline code.
    
    :attr:`code_font_name` is a :class:`~kivy.properties.StringProperty`
    and defaults to 'RobotoMono-Regular'.
    """
    
    link_color = ColorProperty([0, 0.5, 1, 1])
    """RGBA color for link text.
    
    :attr:`link_color` is a :class:`~kivy.properties.ColorProperty`
    and defaults to [0, 0.5, 1, 1] (blue).
    """
    
    code_bg_color = ColorProperty([0.15, 0.15, 0.15, 1])
    """RGBA background color for code blocks.
    
    :attr:`code_bg_color` is a :class:`~kivy.properties.ColorProperty`
    and defaults to [0.15, 0.15, 0.15, 1] (dark gray).
    """
    
    __events__ = ('on_ref_press',)
    
    def __init__(self, **kwargs):
        super(MarkdownLabel, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        
        # Bind height to minimum_height for auto-sizing
        self.bind(minimum_height=self.setter('height'))
        
        # Store the parsed AST tokens
        self._ast_tokens = []
        
        # Create mistune parser with plugins
        self._parser = mistune.create_markdown(renderer=None)
        # Enable table and strikethrough plugins
        table(self._parser)
        strikethrough(self._parser)
        
        # Bind text property to rebuild widgets
        self.bind(text=self._on_text_changed)
        
        # Initial build if text is provided
        if self.text:
            self._rebuild_widgets()
    
    def _on_text_changed(self, instance, value):
        """Callback when text property changes."""
        self._rebuild_widgets()
    
    def _rebuild_widgets(self):
        """Parse the Markdown text and rebuild the widget tree."""
        # Clear existing children
        self.clear_widgets()
        
        # Handle empty text
        if not self.text:
            self._ast_tokens = []
            return
        
        # Parse Markdown to AST
        # mistune.parse() returns a tuple of (tokens, state)
        result = self._parser.parse(self.text)
        self._ast_tokens = result[0] if isinstance(result, tuple) else result
        
        # Create renderer with current styling properties
        renderer = KivyRenderer(
            base_font_size=self.base_font_size,
            code_font_name=self.code_font_name,
            link_color=list(self.link_color),
            code_bg_color=list(self.code_bg_color)
        )
        
        # Render AST to widget tree
        content = renderer(self._ast_tokens, None)
        
        # Bind ref_press events from child Labels to bubble up
        self._bind_ref_press_events(content)
        
        # Add rendered content
        # Note: content.children is in reverse order, so we reverse it to maintain document order
        for child in reversed(list(content.children)):
            content.remove_widget(child)
            self.add_widget(child)
    
    def _bind_ref_press_events(self, widget):
        """Recursively bind on_ref_press events from child Labels.
        
        Args:
            widget: Widget to search for Labels with ref markup
        """
        if isinstance(widget, Label) and widget.markup:
            widget.bind(on_ref_press=self._on_child_ref_press)
        
        # Recursively bind for container widgets
        if hasattr(widget, 'children'):
            for child in widget.children:
                self._bind_ref_press_events(child)
    
    def _on_child_ref_press(self, instance, ref):
        """Handle ref_press from child Label and bubble up.
        
        Args:
            instance: The Label that was clicked
            ref: The URL/reference string
        """
        self.dispatch('on_ref_press', ref)
    
    def on_ref_press(self, ref):
        """Event handler for link clicks.
        
        Override this method or bind to the event to handle link clicks.
        
        Args:
            ref: The URL of the clicked link
        """
        pass
    
    def get_ast(self):
        """Return the parsed AST tokens.
        
        Returns:
            List of AST token dictionaries from mistune
        """
        return self._ast_tokens
    
    def to_markdown(self):
        """Serialize the current AST back to Markdown text.
        
        Returns:
            Markdown string representation of the current AST
        """
        serializer = MarkdownSerializer()
        return serializer.serialize(self._ast_tokens)
