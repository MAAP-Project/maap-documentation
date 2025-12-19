# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))

def setup(app):
    app.add_css_file('custom.css')
    # Add Leaflet CSS and JS for R htmlwidgets
    app.add_css_file('https://unpkg.com/leaflet@1.9.4/dist/leaflet.css',
                     integrity='sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=',
                     crossorigin='anonymous')
    app.add_js_file('https://unpkg.com/leaflet@1.9.4/dist/leaflet.js',
                    integrity='sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=',
                    crossorigin='anonymous')
    # Add Proj4js and Leaflet.Proj for coordinate transformations
    app.add_js_file('https://cdnjs.cloudflare.com/ajax/libs/proj4js/2.9.0/proj4.js',
                    crossorigin='anonymous')
    app.add_js_file('https://cdn.jsdelivr.net/npm/proj4leaflet@1.0.2/src/proj4leaflet.js',
                    crossorigin='anonymous')
    # Add Leaflet providers for base maps
    app.add_js_file('https://unpkg.com/leaflet-providers@1.13.0/leaflet-providers.js',
                    crossorigin='anonymous')


# -- Project information -----------------------------------------------------

project = 'maap-docs'
copyright = '2020-2023, NASA MAAP Team'
author = 'NASA MAAP Team'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'nbsphinx',
    'IPython.sphinxext.ipython_console_highlighting',
    'sphinx_copybutton'
]

nbsphinx_execute = 'never'

# Enable RequireJS for HTML widgets (needed for R leaflet maps)
nbsphinx_requirejs_path = 'https://cdnjs.cloudflare.com/ajax/libs/require.js/2.3.6/require.min.js'
nbsphinx_requirejs_options = {
    'crossorigin': 'anonymous',
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# Explicitly assigning the master document
master_doc = 'index'


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'
html_logo = "_static/nasamaap_logo.png"
html_favicon = "_static/maapsheep-80x80.png"
html_theme_options = {
    'logo_only': True,
	'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Read The Docs Configuration
# https://about.readthedocs.com/blog/2024/07/addons-by-default/
html_baseurl = os.environ.get("READTHEDOCS_CANONICAL_URL", "")

if os.environ.get("READTHEDOCS", "") == "True":
	if "html_context" not in globals():
        	html_context = {}
	html_context["READTHEDOCS"] = True
