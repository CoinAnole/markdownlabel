.. _installation:

Installation
============

Supported Versions
------------------

- **Python**: 3.8, 3.9, 3.10, 3.11, 3.12, 3.13
- **Kivy**: 2.0.0+
- **mistune**: 3.0.0+

Dependencies
------------

MarkdownLabel requires the following packages:

1. `Kivy <https://kivy.org/#download>`_ - The UI framework (2.0.0 or higher)
2. `mistune <https://mistune.lepture.com/>`_ - Markdown parser (3.0.0 or higher)
3. `fonttools <https://fonttools.readthedocs.io/>`_ - Font fallback support (4.0.0 or higher)

Installation Methods
--------------------

From PyPI (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~

If the package is published to PyPI, you can install it directly::

    pip install kivy_garden.markdownlabel

From GitHub
~~~~~~~~~~~~

Install the latest development version directly from GitHub::

    python -m pip install https://github.com/kivy-garden/markdownlabel/archive/master.zip

To install a specific release, use the release URL::

    python -m pip install https://github.com/kivy-garden/markdownlabel/archive/v1.0.1.zip

Using Kivy Garden Index
~~~~~~~~~~~~~~~~~~~~~~~

You can install using the Kivy Garden package index::

    python -m pip install kivy_garden.markdownlabel --extra-index-url https://kivy-garden.github.io/simple/

To permanently add the garden server to your pip configuration, add the following to your `pip.conf <https://pip.pypa.io/en/stable/user_guide/#config-file>`_::

    [global]
    timeout = 60
    index-url = https://kivy-garden.github.io/simple/

Development Installation
~~~~~~~~~~~~~~~~~~~~~~~~

If you want to contribute or modify the code, install in development mode::

    git clone https://github.com/kivy-garden/markdownlabel.git
    cd markdownlabel
    pip install -e .

The ``-e`` flag installs the package in "editable" mode, so changes to the source code are immediately available without reinstallation.

Verify Installation
-------------------

Test that the installation worked::

    python -c "from kivy_garden.markdownlabel import MarkdownLabel; print('Success!')"

Troubleshooting
---------------

**ImportError: No module named 'kivy'**
    Install Kivy first::

        pip install kivy

**ImportError: No module named 'mistune'**
    The mistune dependency should be installed automatically, but if not::

        pip install mistune>=3.0.0

**SDL2 Library Errors (Linux)**
    Install required system libraries::

        sudo apt-get install -y libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev

See Also
--------

- :doc:`getting_started` - Get started using MarkdownLabel
- `Kivy Installation Guide <https://kivy.org/doc/stable/gettingstarted/installation.html>`_
