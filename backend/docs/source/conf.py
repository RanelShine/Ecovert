# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Ecovert'
copyright = '2025, Ranelle'
author = 'Ranelle'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',  
    'sphinx.ext.viewcode',
    'sphinx.ext.coverage',
    'sphinx.ext.todo'
]

import os
import sys
import django


sys.path.insert(0, os.path.abspath('../..'))

# Charge le module de configuration Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'backend.settings'  

django.setup()


templates_path = ['_templates']
exclude_patterns = []

language = 'fr'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
