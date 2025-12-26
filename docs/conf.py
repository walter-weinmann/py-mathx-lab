"""
Sphinx configuration for py-mathx-lab.

This configuration is intentionally minimal and cross-platform.
It supports Markdown sources via MyST, citations via sphinxcontrib-bibtex,
and uses the Furo theme.
"""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as get_version


# ------------------------------------------------------------------------------
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

raw_release = _get_package_version("mathxlab")

# Keep the base version (hide "+g<hash>" etc. on the title page)
release = raw_release.split("+", 1)[0]
version = release

# -- General configuration ---------------------------------------------------

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.mathjax",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_design",
    "sphinxcontrib.bibtex",
]

templates_path = ["_templates"]
exclude_patterns = [
    ".DS_Store",
    "Thumbs.db",
    "_build",
    "background/background_page_template.md",
    "experiments/experiment_page_template.md",
]

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
    "amsmath",
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "substitution",
]
myst_heading_anchors = 3

# BibTeX settings
bibtex_bibfiles = ["refs.bib"]

# -- Options for HTML output -------------------------------------------------

html_css_files = [
    "gallery.css",
]

html_static_path = ["_static"]

html_theme = "furo"

# Optional: nicer browser title
html_title = "py-mathx-lab documentation"

# Optional: Edit-on-GitHub links (recommended for contributors)
html_context = {
    "conf_py_path": "/docs/",
    "display_github": True,
    "github_repo": "py-mathx-lab",
    "github_user": "walter-weinmann",
    "github_version": "main",
}

html_theme_options = {
    "sidebar_hide_name": False,
}

# MyST math configuration
myst_dmath_double_inline = True

# -- Options for LaTeX / PDF output -----------------------------------------

# Produce a stable PDF filename when running the LaTeX builder.
latex_engine = "xelatex"

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
    "fontpkg": r"""
    \usepackage{fontspec}
    \setmainfont{Latin Modern Roman}
    \setsansfont{Latin Modern Sans}
    \setmonofont{Latin Modern Mono}
    """,
}
