# Documentation Implementation Plan for MarkdownLabel

## Overview

The `doc/` directory currently contains template files with "Flower" placeholder text. This plan outlines how to populate it with comprehensive Sphinx documentation for the MarkdownLabel widget.

---

## Proposed Documentation Structure

```
doc/source/
├── conf.py                          # [UPDATE] Fix project metadata
├── index.rst                        # [UPDATE] Main entry point
├── getting_started.rst              # [UPDATE] Navigation + overview
├── installation.rst                 # [UPDATE] Installation instructions
├── api.rst                          # [UPDATE] API index
├── examples.rst                     # [UPDATE] Usage examples
├── usage_guide.rst                  # [NEW] Comprehensive usage guide
├── styling_guide.rst                # [NEW] Customization guide
├── label_compatibility.rst          # [NEW] Label API compatibility
├── events.rst                       # [NEW] Event handling
└── modules/                         # [NEW] Module documentation
    ├── markdownlabel.rst            # Main MarkdownLabel class
    ├── properties.rst               # Property system
    ├── rendering.rst                # Rendering pipeline
    ├── inline_renderer.rst          # Inline markup rendering
    ├── kivy_renderer.rst            # Block rendering
    └── markdown_serializer.rst      # Markdown serialization
```

---

## Detailed Tasks

### 1. Update `conf.py`

**Changes needed:**
- Change `project = 'Flower'` to `project = 'MarkdownLabel'`
- Update `copyright` year to current
- Ensure paths are correct for `src/` layout

**Code snippet:**
```python
import os
import sys
sys.path.insert(0, os.path.abspath('../../src'))

project = 'MarkdownLabel'
copyright = '2024, Kivy Garden'
author = 'Kivy Garden'
```

---

### 2. Update `index.rst`

**Structure:**
```rst
Welcome to MarkdownLabel's documentation!
=========================================

A Kivy widget that parses and renders Markdown documents as structured,
interactive Kivy UI elements.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   getting_started
   installation
   usage_guide
   styling_guide
   label_compatibility
   examples
   api

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
```

---

### 3. Rewrite `installation.rst`

**Content to include:**
- Python version requirements (3.8+)
- Dependencies: Kivy 2.0.0+, mistune 3.0.0+
- Installation methods:
  - From PyPI: `pip install kivy_garden.markdownlabel`
  - From GitHub: `pip install https://github.com/kivy-garden/markdownlabel/archive/master.zip`
  - With garden index: `pip install kivy_garden.markdownlabel --extra-index-url https://kivy-garden.github.io/simple/`
- Development installation: `pip install -e .`

---

### 4. Rewrite `getting_started.rst`

**Sections:**
1. **Introduction** - What is MarkdownLabel?
2. **Quick Start** - Minimal working example
3. **Key Features** - Bullet list from README
4. **Navigation** - Link to other sections

**Quick start example:**
```rst
Quick Start
-----------

Basic usage is simple::

    from kivy_garden.markdownlabel import MarkdownLabel

    label = MarkdownLabel(text='# Hello\\n\\nThis is **bold**.')
```

---

### 5. Rewrite `api.rst`

**Structure:**
```rst
API Reference
=============

.. toctree::
   :maxdepth: 1

   modules/markdownlabel
   modules/properties
   modules/rendering
   modules/inline_renderer
   modules/kivy_renderer
   modules/markdown_serializer
```

---

### 6. Create `modules/markdownlabel.rst`

**Content:**
```rst
MarkdownLabel Widget
====================

.. automodule:: kivy_garden.markdownlabel
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__

Class Documentation
-------------------

.. autoclass:: kivy_garden.markdownlabel.MarkdownLabel
   :members:
   :undoc-members:
   :show-inheritance:
```

---

### 7. Create `modules/properties.rst`

**Content:**
- Document `MarkdownLabelProperties` mixin
- List STYLE_ONLY_PROPERTIES vs STRUCTURE_PROPERTIES
- Explain the rebuild contract
- Property classification reference

---

### 8. Create `modules/rendering.rst`

**Content:**
- `MarkdownLabelRendering` mixin
- Render modes: 'widget' vs 'texture'
- The three-layer rendering pipeline
- Clipping behavior

---

### 9. Create `events.rst`

**Content:**
```rst
Event Handling
==============

on_ref_press Event
------------------

Dispatched when a user clicks on a link in the Markdown content.

Example::

    def on_link_click(instance, url):
        print(f'Clicked: {url}')

    label.bind(on_ref_press=on_link_click)
```

---

### 10. Rewrite `examples.rst`

**Content:**
1. **Simple Demo** - Explain `simple_demo.py` with code and screenshot
2. **Full-Featured Demo** - Explain `full_featured_demo.py`
3. **Sample Markdown** - Show what's in `sample_markdown.md`
4. **Running Examples** - Command line instructions

---

### 11. Create `usage_guide.rst`

**Sections:**
1. **Basic Usage** - Setting text, handling links
2. **Label Compatibility** - Using familiar Label properties
3. **Auto-sizing** - Height/width behavior
4. **Text Wrapping** - Using text_size
5. **Rendering Modes** - Widget vs texture mode
6. **Performance Tips** - When to use each mode

---

### 12. Create `styling_guide.rst`

**Sections:**
1. **Font Customization** - font_name, code_font_name
2. **Colors** - color, link_color, code_bg_color
3. **Alignment** - halign, valign
4. **Spacing** - line_height, padding, text_padding
5. **Advanced** - outline, mipmap, text_language

---

### 13. Create `label_compatibility.rst`

**Content:**
- List of fully supported Label properties
- List of no-op properties (accepted but ignored)
- Migration guide from Label to MarkdownLabel
- Differences and limitations

**Table format:**
```rst
Supported Properties
--------------------

======================== ============================================
Property                 Notes
======================== ============================================
font_name                Applied to all text except code blocks
font_size                Alias for base_font_size
color                    Text color (preserves link_color)
halign                   'left', 'center', 'right', 'justify', 'auto'
...                      ...
======================== ============================================
```

---

### 14. Add Screenshots

**Screenshots to include:**
- Simple demo rendering
- Full-featured demo with different styles
- Table rendering example
- Code block with syntax highlighting

Place in `doc/source/_static/` and reference with:
```rst
.. image:: _static/simple_demo.png
   :alt: Simple MarkdownLabel Demo
```

---

### 15. Test Documentation Build

**Commands:**
```bash
cd doc
make html
# Or on Windows:
make.bat html
```

**Verify:**
- No Sphinx warnings
- All autodoc imports work
- Images display correctly
- Links are functional

---

## Implementation Priority

### Phase 1: Core Documentation (Must Have)
1. Update conf.py
2. Update index.rst
3. Rewrite installation.rst
4. Rewrite getting_started.rst
5. Create markdownlabel.rst (main API)
6. Rewrite examples.rst

### Phase 2: Advanced Documentation (Should Have)
7. Create usage_guide.rst
8. Create styling_guide.rst
9. Create label_compatibility.rst
10. Create events.rst

### Phase 3: Complete API (Nice to Have)
11. Create properties.rst
12. Create rendering.rst
13. Create inline_renderer.rst
14. Create kivy_renderer.rst
15. Create markdown_serializer.rst

---

## Notes

- The existing `README.md` has excellent content that can be adapted
- The examples in `examples/` directory are well-documented
- The code has good docstrings that autodoc will pick up
- Consider adding intersphinx links to Kivy docs for Label references
