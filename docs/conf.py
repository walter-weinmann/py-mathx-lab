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
copyright = "2025-2026, Walter Weinmann"

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
    # Snapshots are included into experiment pages; they must not be treated as
    # standalone documents (otherwise Sphinx emits toc.not_included warnings).
    "reports/**",
    "params/**",
]

# Prefer Markdown as the primary source format.
source_suffix = {
    ".md": "markdown",
    ".rst": "restructuredtext",
}

# Autosummary (optional but useful once you add API pages)
autosummary_generate = True

# BibTeX settings
bibtex_bibfiles = ["refs.bib"]

# Make bibliography labels non-cryptic (numeric) and make inline cites readable (author-year)
bibtex_default_style = "plain"          # numeric labels like [1], [2], ...
bibtex_reference_style = "author_year"  # inline cites like "Titchmarsh (1986)"
bibtex_tooltips = True                 # hover shows a short preview
bibtex_tooltips_style = "plain"

# Suppress known sphinx-design warnings that don't affect rendering
suppress_warnings = ["design.grid"]

# -- Options for HTML output -------------------------------------------------

html_css_files = [
    "gallery.css",
]


html_js_files = [
    "gallery.js",
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
    # Hide the project name text in the sidebar header.
    # With a logo configured, this effectively replaces "py-mathx-lab" with the image.
    "sidebar_hide_name": True,
    # Furo expects these filenames to be relative to html_static_path (docs/_static).
    "light_logo": "social-preview.png",
    "dark_logo": "social-preview.png",
}

# -- Options for LaTeX / PDF output -----------------------------------------

latex_documents = [
    (
        "index",  # start doc
        "py-mathx-lab.tex",  # target .tex name
        "py-mathx-lab Documentation",
        author,
        "manual",
    ),
]

# Produce a stable PDF filename when running the LaTeX builder.
latex_engine = "xelatex"

# Keep the PDF readable and avoid excessive wide tables.
latex_elements = {
    "fontpkg": r"""
    \usepackage{fontspec}
    \setmainfont{Latin Modern Roman}
    \setsansfont{Latin Modern Sans}
    \setmonofont{Latin Modern Mono}
    """,
    "papersize": "a4paper",
    "pointsize": "10pt",
    "preamble": r"\usepackage{xurl}",
}

# LaTeX/PDF logo (shown on the PDF title page)
latex_logo = "_static/social-preview.png"


# Make the PDF title-page logo smaller
latex_elements = latex_elements if "latex_elements" in globals() else {}
latex_elements.setdefault("preamble", "")
latex_elements["preamble"] += r"""
\AtBeginDocument{%
  \providecommand{\sphinxlogo}{}%
  \renewcommand{\sphinxlogo}{%
    \includegraphics[height=2.0cm]{social-preview.png}\par
  }%
}
"""

mathjax3_config = {
    "tex": {
        "inlineMath": [["$", "$"], ["\\(", "\\)"]],
        "displayMath": [["$$", "$$"], ["\\[", "\\]"]],
    }
}

# MyST math configuration
myst_dmath_double_inline = True

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

# Napoleon for Google-style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = False
