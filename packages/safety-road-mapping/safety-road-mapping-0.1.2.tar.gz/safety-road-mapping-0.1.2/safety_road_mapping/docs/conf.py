# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

from folium import Map
from folium.features import GeoJson, GeoJsonTooltip
from folium.map import Marker
import numpy as np
from openrouteservice import client
from pandas.core.frame import DataFrame, Series
from pandas import Interval
from typeguard import typechecked
from typing import Union
from dotenv import dotenv_values
import math
import pandas as pd
from geopy import distance
import unidecode
from colour import Color
import copy
import sys
import os
from mock import Mock as MagicMock


class Mock(MagicMock):
    @classmethod
    def __getattr__(cls, name):
        return MagicMock()


MOCK_MODULES = ['folium', 'folium.features', 'folium.map', 'numpy', 'openrouteservice', 'geopy',
                'pandas.core.frame', 'pandas', 'typeguard', 'typing', 'dotenv', 'math', 'pandas',
                'unidecode', 'colour', 'copy']
sys.modules.update((mod_name, Mock()) for mod_name in MOCK_MODULES)

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('../'))


# -- Project information -----------------------------------------------------

project = 'Safety Road Mapping'
copyright = '2021, Gabriel Aparecido Fonseca'
author = 'Gabriel Aparecido Fonseca'

# The full version, including alpha/beta/rc tags
release = '1'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.coverage', 'sphinx.ext.napoleon',
              'sphinx.ext.viewcode']

napoleon_google_docstring = False
napoleon_use_param = False
napoleon_use_ivar = True
add_module_names = False

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = 'alabaster'
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

autodoc_default_options = {"members": True, "undoc-members": True, "class-doc-from": True,
                           "special-members": "__init__", "private-members": True}
