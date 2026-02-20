# Documentation Maintainer Notes

## Build Commands

- Online (full intersphinx):
  - `/home/coinanole/.local/share/mise/installs/python/3.13.12/bin/sphinx-build -b html -n -W --keep-going doc/source /tmp/markdownlabel-docbuild`
- Offline-friendly (disable Kivy intersphinx domain):
  - `/home/coinanole/.local/share/mise/installs/python/3.13.12/bin/sphinx-build -b html -n -W --keep-going -D intersphinx_disabled_domains=kivy doc/source /tmp/markdownlabel-docbuild-offline`
