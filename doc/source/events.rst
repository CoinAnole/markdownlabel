.. _events:

Event Handling
==============

MarkdownLabel provides event handling for interactive elements in Markdown content.

on_ref_press Event
------------------

The ``on_ref_press`` event is dispatched when a user clicks on a link (reference) in the Markdown content.

Event Signature
~~~~~~~~~~~~~~~

.. py:function:: on_ref_press(ref)

   :param str ref: The URL or reference identifier of the clicked link
   :return: None

Usage Example
~~~~~~~~~~~~~

.. code-block:: python

    from kivy_garden.markdownlabel import MarkdownLabel

    def on_link_click(instance, url):
        """Handle link clicks."""
        print(f'User clicked: {url}')

        # Open in browser
        import webbrowser
        webbrowser.open(url)

    label = MarkdownLabel(text='Visit [Kivy](https://kivy.org)')
    label.bind(on_ref_press=on_link_click)

Lambda Example
~~~~~~~~~~~~~~

For simple handlers, use a lambda:

.. code-block:: python

    label.bind(on_ref_press=lambda instance, ref: print(f'Clicked: {ref}'))

Link Detection
--------------

MarkdownLabel supports standard Markdown link syntax:

**Inline Links**
   ``[Link Text](https://example.com)``

**Reference Links**
   ``[Link Text][ref]`` with ``[ref]: https://example.com``

**Autolinks**
   ``<https://example.com>``

Link Styling
------------

Control link appearance with the ``link_style`` property:

.. code-block:: python

    # Styled links - blue and underlined
    label.link_style = 'styled'

    # Unstyled links (default) - no special styling
    label.link_style = 'unstyled'

Customize link color:

.. code-block:: python

    label.link_color = [0, 0.7, 1, 1]  # Light blue

Texture Mode Link Handling
--------------------------

When using ``render_mode='texture'``, links are handled differently:

- Click detection uses hit-testing on the aggregated texture
- The ``on_touch_down`` method checks ``_aggregated_refs`` for link zones
- Links still dispatch ``on_ref_press`` events normally

Example: Opening Links in Browser
---------------------------------

Complete example for web links:

.. code-block:: python

    from kivy.app import App
    from kivy.uix.boxlayout import BoxLayout
    from kivy_garden.markdownlabel import MarkdownLabel
    import webbrowser

    class LinkExample(App):
        def build(self):
            layout = BoxLayout(orientation='vertical')

            markdown_text = """
    # Link Examples

    - [Kivy Website](https://kivy.org)
    - [Python Documentation](https://docs.python.org)
    - [Markdown Guide](https://www.markdownguide.org)
    """

            label = MarkdownLabel(
                text=markdown_text,
                link_style='styled',
                link_color=[0.2, 0.6, 1, 1]
            )
            label.bind(on_ref_press=self.open_link)

            layout.add_widget(label)
            return layout

        def open_link(self, instance, url):
            print(f'Opening: {url}')
            webbrowser.open(url)

    if __name__ == '__main__':
        LinkExample().run()

Internal Links
--------------

You can use links for internal navigation by using custom URL schemes:

.. code-block:: python

    def handle_internal_link(instance, ref):
        if ref.startswith('app://'):
            page = ref[6:]  # Extract page name
            self.show_page(page)

    label = MarkdownLabel(text='[Go to Settings](app://settings)')
    label.bind(on_ref_press=handle_internal_link)

See Also
--------

- :doc:`usage_guide` - More usage patterns
- :doc:`examples` - Complete working examples
