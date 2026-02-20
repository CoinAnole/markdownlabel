"""See README.md for package documentation."""

from setuptools import setup, find_namespace_packages

from io import open
from os import path

here = path.abspath(path.dirname(__file__))

filename = path.join(here, 'src', 'kivy_garden', 'markdownlabel', '_version.py')
locals = {}
with open(filename, "rb") as fh:
    exec(compile(fh.read(), filename, 'exec'), globals(), locals)
__version__ = locals['__version__']

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

URL = 'https://github.com/kivy-garden/markdownlabel'

# exposing the params so it can be imported
setup_params = dict(
    name='kivy_garden.markdownlabel',
    version=__version__,
    description='A Kivy widget that renders Markdown as interactive UI elements.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=URL,
    author='Kivy',
    author_email='kivy@kivy.org',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
    ],
    keywords='Kivy kivy-garden markdown',

    packages=find_namespace_packages(where='src', include=['kivy_garden.*']),
    package_dir={'': 'src'},
    python_requires='>=3.8',
    install_requires=[
        'kivy>=2.0.0',
        'mistune>=3.0.0',
        'fonttools>=4.0.0',
    ],
    extras_require={
        # pytest-asyncio>=0.21.0 required to prevent PytestConfigWarning
        # about asyncio_default_fixture_loop_scope in pytest.ini
        # asyncio_default_fixture_loop_scope was added to pytest.ini
        # to prevent a warning with python 3.8
        'dev': ['pytest>=3.6', 'pytest-cov', 'pytest-asyncio>=0.21.0',
                'sphinx_rtd_theme', 'hypothesis>=6.0.0'],
        'ci': ['coveralls', 'pycodestyle'],
        'test': ['pytest>=3.6', 'hypothesis>=6.0.0'],
    },
    entry_points={},
    project_urls={
        'Bug Reports': URL + '/issues',
        'Source': URL,
    },
)


def run_setup():
    setup(**setup_params)


# makes sure the setup doesn't run at import time
if __name__ == '__main__':
    run_setup()
