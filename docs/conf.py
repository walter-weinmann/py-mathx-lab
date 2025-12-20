"""
Sphinx configuration for py-mathx-lab.

This configuration is intentionally minimal and cross-platform.
It supports Markdown sources via MyST, citations via sphinxcontrib-bibtex,
and uses the Furo theme.
"""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as get_version


def _get_package_version(dist_name: str) -> str:
    """Get the installed package version for the given distribution name.

    Args:
        dist_name: Distribution name as defined by packaging metadata.

    Returns:
        The version string if available, otherwise "0.0.0".
    """
    try:
        return get_version(dist_name)
    except PackageNotFoundError:
        return "0.0.0"


# -- Project information -----------------------------------------------------

project = "py-mathx-lab"
author = "io-swiss"
copyright = "2025, io-swiss"

# If your distribution name differs, adjust this.
# For many repos, it matches [project].name in pyproject.toml.
release = _get_package_version("py-mathx-lab")
version = release

# -- General configuration ---------------------------------------------------

extensions = [
    "myst_parser",
    "sphinxcontrib.bibtex",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# Prefer Markdown as the primary source format.
source_suffix = {
    ".md": "markdown",
    ".rst": "restructuredtext",
}

# Autosummary (optional, but useful once you add API pages)
autosummary_generate = True

# Napoleon for Google-style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = False

# MyST settings
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "fieldlist",
    "substitution",
]
myst_heading_anchors = 3

# BibTeX settings
bibtex_bibfiles = ["refs.bib"]

# -- Options for HTML output -------------------------------------------------

html_theme = "furo"
html_static_path = ["_static"]
