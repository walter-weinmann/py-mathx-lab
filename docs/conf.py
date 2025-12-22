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
author = "Walter Weinmann"
copyright = "2025, Walter Weinmann"

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
    "sphinx.ext.mathjax",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# Prefer Markdown as the primary source format.
source_suffix = {
    ".md": "markdown",
    ".rst": "restructuredtext",
}

# Autosummary (optional but useful once you add API pages)
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
    "dollarmath",
    "amsmath",
]
myst_heading_anchors = 3

# BibTeX settings
bibtex_bibfiles = ["refs.bib"]

# -- Options for HTML output -------------------------------------------------

html_theme = "furo"
html_static_path = ["_static"]

# Optional: nicer browser title
html_title = "py-mathx-lab documentation"

# Optional: Edit-on-GitHub links (recommended for contributors)
html_context = {
    "display_github": True,
    "github_user": "walter-weinmann",
    "github_repo": "py-mathx-lab",
    "github_version": "main",
    "conf_py_path": "/docs/",
}

html_theme_options = {
    "sidebar_hide_name": False,
}

# MyST math configuration
myst_dmath_double_inline = True

# -- Options for LaTeX / PDF output -----------------------------------------

# Produce a stable PDF filename when running the LaTeX builder.
latex_engine = "pdflatex"

latex_documents = [
    (
        "index",  # start doc
        "py-mathx-lab.tex",  # target .tex name
        "py-mathx-lab Documentation",
        author,
        "manual",
    ),
]

# Keep the PDF readable and avoid excessive wide tables.
latex_elements = {
    "papersize": "a4paper",
    "pointsize": "10pt",
    "fontpkg": r"\usepackage{lmodern}",
}
