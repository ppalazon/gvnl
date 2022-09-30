"""Sphinx configuration."""
project = "Grammar-Vocabulary Notebook Log"
author = "Pablo Palazon"
copyright = "2022, Pablo Palazon"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
