"""
Label compatibility tests for MarkdownLabel widget.

Tests verify that MarkdownLabel maintains compatibility with Kivy Label API
for basic properties like font_size aliases and no-op property acceptance.
"""

import importlib
import sys
import pytest
from hypothesis import given, strategies as st, settings, assume

from kivy_garden.markdownlabel import MarkdownLabel
from .test_utils import simple_markdown_document


# **Feature: label-compatibility, Property 1: font_size/base_font_size Alias Bidirectionality**
# *For any* numeric value V, setting `font_size` to V SHALL result in `base_font_size`
# equaling V, and setting `base_font_size` to V SHALL result in `font_size` returning V.
# **Validates: Requirements 2.1, 2.2**

class TestFontSizeAliasBidirectionality:
    """Property tests for font_size/base_font_size alias (Property 1)."""
    
    @given(st.floats(min_value=1, max_value=200, allow_nan=False, allow_infinity=False))
    @settings(max_examples=100, deadline=None)
    def test_font_size_sets_base_font_size(self, font_size_value):
        """Setting font_size updates base_font_size to the same value."""
        label = MarkdownLabel(font_size=font_size_value)
        
        assert label.base_font_size == font_size_value, \
            f"Expected base_font_size={font_size_value}, got {label.base_font_size}"
    
    @given(st.floats(min_value=1, max_value=200, allow_nan=False, allow_infinity=False))
    @settings(max_examples=100, deadline=None)
    def test_base_font_size_returns_via_font_size(self, base_font_size_value):
        """Setting base_font_size is returned when reading font_size."""
        label = MarkdownLabel(base_font_size=base_font_size_value)
        
        assert label.font_size == base_font_size_value, \
            f"Expected font_size={base_font_size_value}, got {label.font_size}"
    
    @given(st.floats(min_value=1, max_value=200, allow_nan=False, allow_infinity=False),
           st.floats(min_value=1, max_value=200, allow_nan=False, allow_infinity=False))
    @settings(max_examples=20, deadline=None)
    def test_font_size_change_updates_base_font_size(self, initial_value, new_value):
        """Changing font_size after creation updates base_font_size."""
        label = MarkdownLabel(font_size=initial_value)
        label.font_size = new_value
        
        assert label.base_font_size == new_value, \
            f"Expected base_font_size={new_value}, got {label.base_font_size}"
    
    @given(st.floats(min_value=1, max_value=200, allow_nan=False, allow_infinity=False),
           st.floats(min_value=1, max_value=200, allow_nan=False, allow_infinity=False))
    @settings(max_examples=20, deadline=None)
    def test_base_font_size_change_updates_font_size(self, initial_value, new_value):
        """Changing base_font_size after creation updates font_size."""
        label = MarkdownLabel(base_font_size=initial_value)
        label.base_font_size = new_value
        
        assert label.font_size == new_value, \
            f"Expected font_size={new_value}, got {label.font_size}"
    
    @given(st.floats(min_value=1, max_value=200, allow_nan=False, allow_infinity=False))
    @settings(max_examples=100, deadline=None)
    def test_bidirectional_equivalence(self, value):
        """font_size and base_font_size are always equivalent."""
        label = MarkdownLabel()
        
        # Set via font_size
        label.font_size = value
        assert label.font_size == label.base_font_size, \
            f"font_size ({label.font_size}) != base_font_size ({label.base_font_size})"
        
        # Set via base_font_size
        label.base_font_size = value + 1
        assert label.font_size == label.base_font_size, \
            f"font_size ({label.font_size}) != base_font_size ({label.base_font_size})"


# **Feature: markdown-label, Property 8: No-op Properties Acceptance**
# *For any* no-op property (bold, italic, underline, strikethrough, markup), when set to any
# valid value, the MarkdownLabel SHALL accept the value without raising an exception.
# **Validates: Requirements 8.1, 8.2, 8.3, 8.4, 8.5, 8.6**

class TestNoOpPropertiesAcceptance:
    """Property tests for no-op properties acceptance (Property 8)."""
    
    @given(st.booleans())
    @settings(max_examples=2, deadline=None)
    def test_bold_property_accepted(self, value):
        """Setting bold property does not raise an exception."""
        # Should not raise any exception
        label = MarkdownLabel(text='# Hello World', bold=value)
        assert label.bold == value
    
    @given(st.booleans())
    @settings(max_examples=2, deadline=None)
    def test_italic_property_accepted(self, value):
        """Setting italic property does not raise an exception."""
        label = MarkdownLabel(text='# Hello World', italic=value)
        assert label.italic == value
    
    @given(st.booleans())
    @settings(max_examples=2, deadline=None)
    def test_underline_property_accepted(self, value):
        """Setting underline property does not raise an exception."""
        label = MarkdownLabel(text='# Hello World', underline=value)
        assert label.underline == value
    
    @given(st.booleans())
    @settings(max_examples=2, deadline=None)
    def test_strikethrough_property_accepted(self, value):
        """Setting strikethrough property does not raise an exception."""
        label = MarkdownLabel(text='# Hello World', strikethrough=value)
        assert label.strikethrough == value
    
    @given(st.booleans())
    @settings(max_examples=2, deadline=None)
    def test_markup_property_accepted(self, value):
        """Setting markup property does not raise an exception."""
        label = MarkdownLabel(text='# Hello World', markup=value)
        assert label.markup == value
    
    @given(st.booleans(), st.booleans(), st.booleans(), st.booleans(), st.booleans())
    @settings(max_examples=2, deadline=None)
    def test_all_noop_properties_together(self, bold, italic, underline, strikethrough, markup):
        """Setting all no-op properties together does not raise an exception."""
        label = MarkdownLabel(
            text='# Hello World',
            bold=bold,
            italic=italic,
            underline=underline,
            strikethrough=strikethrough,
            markup=markup
        )
        assert label.bold == bold
        assert label.italic == italic
        assert label.underline == underline
        assert label.strikethrough == strikethrough
        assert label.markup == markup
    
    @given(st.booleans(), st.booleans(), st.booleans(), st.booleans(), st.booleans(),
           simple_markdown_document())
    @settings(max_examples=2, deadline=None)
    def test_noop_properties_do_not_affect_rendering(self, bold, italic, underline, 
                                                      strikethrough, markup, markdown_text):
        """No-op properties do not affect the rendered output."""
        assume(markdown_text.strip())
        
        # Create label with default no-op property values
        label_default = MarkdownLabel(text=markdown_text)
        default_child_count = len(label_default.children)
        
        # Create label with various no-op property values
        label_with_props = MarkdownLabel(
            text=markdown_text,
            bold=bold,
            italic=italic,
            underline=underline,
            strikethrough=strikethrough,
            markup=markup
        )
        props_child_count = len(label_with_props.children)
        
        # The number of children should be the same regardless of no-op properties
        assert default_child_count == props_child_count, \
            f"Expected {default_child_count} children, got {props_child_count} with no-op props"
    
    @given(st.booleans())
    @settings(max_examples=2, deadline=None)
    def test_bold_property_change_after_creation(self, value):
        """Changing bold property after creation does not raise an exception."""
        label = MarkdownLabel(text='# Hello')
        label.bold = value
        assert label.bold == value
    
    @given(st.booleans())
    @settings(max_examples=2, deadline=None)
    def test_italic_property_change_after_creation(self, value):
        """Changing italic property after creation does not raise an exception."""
        label = MarkdownLabel(text='# Hello')
        label.italic = value
        assert label.italic == value
    
    @given(st.booleans())
    @settings(max_examples=2, deadline=None)
    def test_underline_property_change_after_creation(self, value):
        """Changing underline property after creation does not raise an exception."""
        label = MarkdownLabel(text='# Hello')
        label.underline = value
        assert label.underline == value
    
    @given(st.booleans())
    @settings(max_examples=2, deadline=None)
    def test_strikethrough_property_change_after_creation(self, value):
        """Changing strikethrough property after creation does not raise an exception."""
        label = MarkdownLabel(text='# Hello')
        label.strikethrough = value
        assert label.strikethrough == value
    
    @given(st.booleans())
    @settings(max_examples=2, deadline=None)
    def test_markup_property_change_after_creation(self, value):
        """Changing markup property after creation does not raise an exception."""
        label = MarkdownLabel(text='# Hello')
        label.markup = value
        assert label.markup == value


# **Feature: label-compatibility-phase2, Property 1: No-op Property Acceptance and Storage**
# *For any* no-op property (mipmap, outline_width, outline_color, text_language, base_direction, ellipsis_options), 
# when set to any valid value, the MarkdownLabel SHALL accept the value without raising an exception 
# AND return the same value when accessed.
# **Validates: Requirements 1.1, 1.2, 1.3**

class TestNoOpPropertyAcceptanceAndStorage:
    """Property tests for no-op property acceptance and storage (Property 1)."""
    
    @given(st.booleans())
    @settings(max_examples=2, deadline=None)
    def test_mipmap_property_accepted_and_stored(self, value):
        """Setting mipmap property accepts and stores the value."""
        label = MarkdownLabel(text='# Hello World', mipmap=value)
        assert label.mipmap == value
    
    @given(st.floats(min_value=0, max_value=100, allow_nan=False, allow_infinity=False))
    @settings(max_examples=100, deadline=None)
    def test_outline_width_property_accepted_and_stored(self, value):
        """Setting outline_width property accepts and stores the value."""
        label = MarkdownLabel(text='# Hello World', outline_width=value)
        assert label.outline_width == value
    
    @given(st.lists(
        st.floats(min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False),
        min_size=4, max_size=4
    ))
    @settings(max_examples=20, deadline=None)
    def test_outline_color_property_accepted_and_stored(self, value):
        """Setting outline_color property accepts and stores the value."""
        label = MarkdownLabel(text='# Hello World', outline_color=value)
        # Compare colors with tolerance for floating point differences
        assert all(abs(a - b) < 0.001 for a, b in zip(label.outline_color, value))
    
    @given(st.one_of(st.none(), st.text(min_size=1, max_size=10, alphabet=st.characters(
        whitelist_categories=['L', 'N'],
        blacklist_characters='\n\r'
    ))))
    @settings(max_examples=20, deadline=None)
    def test_text_language_property_accepted_and_stored(self, value):
        """Setting text_language property accepts and stores the value."""
        label = MarkdownLabel(text='# Hello World', text_language=value)
        assert label.text_language == value
    
    @pytest.mark.parametrize('value', [None, 'ltr', 'rtl', 'weak_ltr', 'weak_rtl'])
    def test_base_direction_property_accepted_and_stored(self, value):
        """Setting base_direction property accepts and stores the value."""
        label = MarkdownLabel(text='# Hello World', base_direction=value)
        assert label.base_direction == value
    
    @given(st.dictionaries(
        st.text(min_size=1, max_size=10, alphabet=st.characters(
            whitelist_categories=['L', 'N']
        )),
        st.one_of(st.booleans(), st.integers(), st.text(max_size=20))
    ))
    @settings(max_examples=100, deadline=None)
    def test_ellipsis_options_property_accepted_and_stored(self, value):
        """Setting ellipsis_options property accepts and stores the value."""
        label = MarkdownLabel(text='# Hello World', ellipsis_options=value)
        assert label.ellipsis_options == value
    
    @given(st.booleans(), st.floats(min_value=0, max_value=10), 
           st.lists(st.floats(min_value=0.0, max_value=1.0), min_size=4, max_size=4),
           st.one_of(st.none(), st.text(min_size=1, max_size=5)),
           st.sampled_from([None, 'ltr', 'rtl', 'weak_ltr', 'weak_rtl']),
           st.dictionaries(st.text(min_size=1, max_size=5), st.booleans(), max_size=3))
    @settings(max_examples=100, deadline=None)
    def test_all_noop_properties_together_accepted_and_stored(self, mipmap, outline_width, 
                                                              outline_color, text_language, 
                                                              base_direction, ellipsis_options):
        """Setting all no-op properties together accepts and stores all values."""
        label = MarkdownLabel(
            text='# Hello World',
            mipmap=mipmap,
            outline_width=outline_width,
            outline_color=outline_color,
            text_language=text_language,
            base_direction=base_direction,
            ellipsis_options=ellipsis_options
        )
        
        assert label.mipmap == mipmap
        assert label.outline_width == outline_width
        assert all(abs(a - b) < 0.001 for a, b in zip(label.outline_color, outline_color))
        assert label.text_language == text_language
        assert label.base_direction == base_direction
        assert label.ellipsis_options == ellipsis_options
    
    @given(st.booleans())
    @settings(max_examples=2, deadline=None)
    def test_mipmap_property_change_after_creation(self, value):
        """Changing mipmap property after creation accepts and stores the value."""
        label = MarkdownLabel(text='# Hello')
        label.mipmap = value
        assert label.mipmap == value
    
    @given(st.floats(min_value=0, max_value=100, allow_nan=False, allow_infinity=False))
    @settings(max_examples=100, deadline=None)
    def test_outline_width_property_change_after_creation(self, value):
        """Changing outline_width property after creation accepts and stores the value."""
        label = MarkdownLabel(text='# Hello')
        label.outline_width = value
        assert label.outline_width == value
    
    @given(st.lists(
        st.floats(min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False),
        min_size=4, max_size=4
    ))
    @settings(max_examples=20, deadline=None)
    def test_outline_color_property_change_after_creation(self, value):
        """Changing outline_color property after creation accepts and stores the value."""
        label = MarkdownLabel(text='# Hello')
        label.outline_color = value
        assert all(abs(a - b) < 0.001 for a, b in zip(label.outline_color, value))
    
    @given(st.one_of(st.none(), st.text(min_size=1, max_size=10, alphabet=st.characters(
        whitelist_categories=['L', 'N'],
        blacklist_characters='\n\r'
    ))))
    @settings(max_examples=20, deadline=None)
    def test_text_language_property_change_after_creation(self, value):
        """Changing text_language property after creation accepts and stores the value."""
        label = MarkdownLabel(text='# Hello')
        label.text_language = value
        assert label.text_language == value
    
    @pytest.mark.parametrize('value', [None, 'ltr', 'rtl', 'weak_ltr', 'weak_rtl'])
    def test_base_direction_property_change_after_creation(self, value):
        """Changing base_direction property after creation accepts and stores the value."""
        label = MarkdownLabel(text='# Hello')
        label.base_direction = value
        assert label.base_direction == value
    
    @given(st.dictionaries(
        st.text(min_size=1, max_size=10, alphabet=st.characters(
            whitelist_categories=['L', 'N']
        )),
        st.one_of(st.booleans(), st.integers(), st.text(max_size=20))
    ))
    @settings(max_examples=100, deadline=None)
    def test_ellipsis_options_property_change_after_creation(self, value):
        """Changing ellipsis_options property after creation accepts and stores the value."""
        label = MarkdownLabel(text='# Hello')
        label.ellipsis_options = value
        assert label.ellipsis_options == value
    
    @given(st.booleans(), st.floats(min_value=0, max_value=10), 
           st.lists(st.floats(min_value=0.0, max_value=1.0), min_size=4, max_size=4),
           st.one_of(st.none(), st.text(min_size=1, max_size=5)),
           st.sampled_from([None, 'ltr', 'rtl', 'weak_ltr', 'weak_rtl']),
           st.dictionaries(st.text(min_size=1, max_size=5), st.booleans(), max_size=3),
           simple_markdown_document())
    @settings(max_examples=100, deadline=None)
    def test_noop_properties_do_not_affect_rendering(self, mipmap, outline_width, outline_color,
                                                     text_language, base_direction, ellipsis_options,
                                                     markdown_text):
        """No-op properties do not affect the rendered output."""
        assume(markdown_text.strip())
        
        # Create label with default no-op property values
        label_default = MarkdownLabel(text=markdown_text)
        default_child_count = len(label_default.children)
        
        # Create label with various no-op property values
        label_with_props = MarkdownLabel(
            text=markdown_text,
            mipmap=mipmap,
            outline_width=outline_width,
            outline_color=outline_color,
            text_language=text_language,
            base_direction=base_direction,
            ellipsis_options=ellipsis_options
        )
        props_child_count = len(label_with_props.children)
        
        # The number of children should be the same regardless of no-op properties
        assert default_child_count == props_child_count, \
            f"Expected {default_child_count} children, got {props_child_count} with no-op props"


# **Feature: test-refactoring, Property 4: Import Functionality**
# *For any* refactored test module, all imports should resolve successfully 
# and tests should execute without import errors
# **Validates: Requirements 2.4**

class TestImportFunctionality:
    """Property test for import functionality (Property 4)."""
    
    def test_label_compatibility_imports_resolve(self):
        """Label compatibility module imports resolve successfully."""
        try:
            # Test importing the module
            import kivy_garden.markdownlabel.tests.test_label_compatibility
            
            # Test that key classes are accessible
            from kivy_garden.markdownlabel.tests.test_label_compatibility import (
                TestFontSizeAliasBidirectionality,
                TestNoOpPropertiesAcceptance,
                TestNoOpPropertyAcceptanceAndStorage
            )
            
            # Verify classes exist and are classes
            assert TestFontSizeAliasBidirectionality is not None
            assert TestNoOpPropertiesAcceptance is not None
            assert TestNoOpPropertyAcceptanceAndStorage is not None
            
            # Verify they are actually classes
            assert isinstance(TestFontSizeAliasBidirectionality, type)
            assert isinstance(TestNoOpPropertiesAcceptance, type)
            assert isinstance(TestNoOpPropertyAcceptanceAndStorage, type)
            
        except ImportError as e:
            pytest.fail(f"Import failed for test_label_compatibility: {e}")
        except Exception as e:
            pytest.fail(f"Unexpected error importing test_label_compatibility: {e}")
    
    def test_shared_utilities_imports_resolve(self):
        """Shared test utilities imports resolve successfully."""
        try:
            # Test importing the utilities module
            from kivy_garden.markdownlabel.tests.test_utils import (
                markdown_heading,
                markdown_paragraph,
                markdown_bold,
                markdown_italic,
                markdown_link,
                simple_markdown_document,
                find_labels_recursive,
                colors_equal,
                padding_equal,
                floats_equal,
                KIVY_FONTS,
                color_strategy,
                text_padding_strategy
            )
            
            # Verify key functions exist
            assert callable(markdown_heading)
            assert callable(markdown_paragraph)
            assert callable(simple_markdown_document)
            assert callable(find_labels_recursive)
            assert callable(colors_equal)
            
            # Verify constants exist
            assert KIVY_FONTS is not None
            assert isinstance(KIVY_FONTS, list)
            
        except ImportError as e:
            pytest.fail(f"Import failed for test_utils: {e}")
        except Exception as e:
            pytest.fail(f"Unexpected error importing test_utils: {e}")
    
    def test_cross_module_imports_work(self):
        """Test modules can import from shared utilities."""
        try:
            # Import the label compatibility module which uses test_utils
            from kivy_garden.markdownlabel.tests.test_label_compatibility import TestFontSizeAliasBidirectionality
            
            # Verify that the class can be instantiated (imports worked)
            test_instance = TestFontSizeAliasBidirectionality()
            assert test_instance is not None
            
            # Verify that test methods exist (they use imported strategies)
            assert hasattr(test_instance, 'test_font_size_sets_base_font_size')
            assert callable(test_instance.test_font_size_sets_base_font_size)
            
        except ImportError as e:
            pytest.fail(f"Cross-module import failed: {e}")
        except Exception as e:
            pytest.fail(f"Unexpected error in cross-module import: {e}")