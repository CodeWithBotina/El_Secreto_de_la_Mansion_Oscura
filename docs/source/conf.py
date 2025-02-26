import os
import sys

sys.path.insert(0, os.path.abspath('../../src'))

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'El Secreto de la Mansión Oscura'
copyright = '2025, CodeWithBotina'
author = 'CodeWithBotina'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
     
extensions = [
    'sphinx.ext.autodoc',  # Para generar documentación automáticamente
    'sphinx.ext.viewcode',  # Para agregar enlaces al código fuente
    'sphinx.ext.napoleon',  # Para soportar docstrings en formato Google o NumPy
]

templates_path = ['_templates']
exclude_patterns = []

language = 'es'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
