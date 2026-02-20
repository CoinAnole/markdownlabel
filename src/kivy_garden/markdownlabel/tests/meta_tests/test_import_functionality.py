"""
Meta-tests for import functionality across test modules.

This module contains tests that verify imports resolve successfully
and tests can execute without import errors.
"""

import pytest


@pytest.mark.test_tests
class TestImportFunctionality:
    """Meta-tests for import functionality."""

    def test_label_compatibility_imports_resolve(self):
        """Label compatibility module imports resolve successfully."""
        try:
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
                simple_markdown_document,
                find_labels_recursive,
                colors_equal,
                KIVY_FONTS,
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
            from kivy_garden.markdownlabel.tests.test_label_compatibility import (
                TestFontSizeAliasBidirectionality,
            )

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
