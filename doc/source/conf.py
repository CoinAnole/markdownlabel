# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('../../src'))

import sphinx_rtd_theme


# -- Project information -----------------------------------------------------

project = 'MarkdownLabel'
copyright = '2026, Kivy Garden'
author = 'Kivy Garden'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.intersphinx',
    "sphinx_rtd_theme",
]

intersphinx_mapping = {
    'kivy': ('https://kivy.org/docs/', None),
}
intersphinx_disabled_domains = []

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for autodoc -----------------------------------------------------

# Hide version annotations from inherited Kivy docstrings
autodoc_member_order = 'bysource'
autodoc_typehints = 'description'
autosummary_generate = True
nitpick_ignore_regex = [
    # In offline/restricted environments we intentionally allow unresolved
    # cross-references to external Kivy classes.
    (r'py:class', r'kivy\..*'),
    (r'py:class', r'kivy_garden\.markdownlabel\.properties\.MarkdownLabelProperties'),
]


def _normalize_disabled_domains(value):
    """Normalize intersphinx-disabled domain names from config/CLI."""
    if value is None:
        return []
    if isinstance(value, str):
        return [item.strip() for item in value.split(',') if item.strip()]
    return [str(item).strip() for item in value if str(item).strip()]


def _apply_intersphinx_domain_filter(app, config):
    """Drop selected intersphinx mappings after CLI overrides are applied."""
    disabled_domains = _normalize_disabled_domains(config.intersphinx_disabled_domains)
    for domain in disabled_domains:
        config.intersphinx_mapping.pop(domain, None)


def setup(app):
    """Sphinx extension hook for doc build customizations."""
    app.add_config_value('intersphinx_disabled_domains', [], 'env')
    app.connect('config-inited', _apply_intersphinx_domain_filter)

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Custom CSS to hide Kivy version annotations
html_css_files = [
    'custom.css',
]
