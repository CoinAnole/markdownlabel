.. _examples:

Examples
========

This page summarizes the runnable examples in the repository.

Example Files
-------------

- ``examples/simple_demo.py`` - Minimal MarkdownLabel usage
- ``examples/full_featured_demo.py`` - Label-compatibility and styling showcase
- ``examples/sample_markdown.md`` - Source Markdown used by the full-featured demo

Run the demos from the repository root:

.. code-block:: bash

    python examples/simple_demo.py
    python examples/full_featured_demo.py

Quick Example
-------------

.. code-block:: python

    from kivy.base import runTouchApp
    from kivy_garden.markdownlabel import MarkdownLabel

    runTouchApp(MarkdownLabel(
        text='# Hello MarkdownLabel\n\nThis is **bold** text.',
        link_style='styled',
    ))

Auto-Sizing Example
-------------------

``auto_size_height`` defaults to ``False``. Enable it when you want the widget
to grow to content height:

.. code-block:: python

    from kivy.uix.boxlayout import BoxLayout
    from kivy_garden.markdownlabel import MarkdownLabel

    layout = BoxLayout(orientation='vertical')
    label = MarkdownLabel(
        text='# Auto-sized\n\nContent here',
        auto_size_height=True,
        size_hint_y=None,
    )
    layout.add_widget(label)

Link Handling Example
---------------------

.. code-block:: python

    import webbrowser
    from kivy_garden.markdownlabel import MarkdownLabel

    label = MarkdownLabel(text='Visit [Kivy](https://kivy.org)')
    label.bind(on_ref_press=lambda instance, ref: webbrowser.open(ref))

See Also
--------

- :doc:`usage_guide` - Comprehensive usage patterns
- :doc:`styling_guide` - Style customization guide
- :doc:`events` - Event handling details
- `examples/README.md <https://github.com/kivy-garden/markdownlabel/blob/master/examples/README.md>`_
