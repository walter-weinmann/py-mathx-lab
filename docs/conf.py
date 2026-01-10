"""
Sphinx configuration for py-mathx-lab.

This configuration is intentionally minimal and cross-platform.
It supports Markdown sources via MyST, citations via sphinxcontrib-bibtex,
and uses the Furo theme.
"""

from __future__ import annotations

import sys
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as get_version
from pathlib import Path

# ------------------------------------------------------------------------------
# Make the repository importable for autodoc without requiring an installed wheel.
DOCS_DIR = Path(__file__).resolve().parent
REPO_ROOT = DOCS_DIR.parent
sys.path.insert(0, str(REPO_ROOT))


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

# Autosummary
autosummary_generate = True

# Autodoc settings (API docs)
autodoc_typehints = "signature"
autodoc_member_order = "bysource"
autodoc_default_options = {
    "members": True,
    "show-inheritance": True,
}

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
    "api.css",
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
        "index_latex",          # start doc (your LaTeX root)
        "py-mathx-lab.tex",     # target filename (MUST end with .tex)
        "py-mathx-lab Documentation",
        "Walter Weinmann",      # author (4th!)
        "manual",               # documentclass (5th!) -> must be 'manual' or 'howto'
    ),
]

# Produce a stable PDF filename when running the LaTeX builder.
latex_engine = "xelatex"

# Keep the PDF readable and avoid excessive wide tables.
latex_elements = {
    "classoptions": ",oneside,openany",
    "papersize": "a4paper",
    "pointsize": "10pt",
    "preamble": r"""
\usepackage{fontspec}
\setmainfont{Latin Modern Roman}

% --- Increase nesting limits for lists ----------------------------------------
\usepackage{enumitem}
\setlistdepth{20}
\renewlist{description}{description}{20}
\setlist[description]{style=unboxed,leftmargin=\leftmargin,labelindent=\labelindent}

% --- Better Unicode handling in text sources (MyST/Markdown) ------------------
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{newunicodechar}

% Blackboard bold (very common in number theory)
\newunicodechar{ℕ}{\ensuremath{\mathbb{N}}}
\newunicodechar{ℤ}{\ensuremath{\mathbb{Z}}}
\newunicodechar{ℚ}{\ensuremath{\mathbb{Q}}}
\newunicodechar{ℝ}{\ensuremath{\mathbb{R}}}
\newunicodechar{ℂ}{\ensuremath{\mathbb{C}}}
\newunicodechar{ℙ}{\ensuremath{\mathbb{P}}}

% Common relations/operators that often appear as Unicode in Markdown
\newunicodechar{≤}{\ensuremath{\le}}
\newunicodechar{≥}{\ensuremath{\ge}}
\newunicodechar{≠}{\ensuremath{\neq}}
\newunicodechar{≈}{\ensuremath{\approx}}
\newunicodechar{≡}{\ensuremath{\equiv}}
\newunicodechar{∈}{\ensuremath{\in}}
\newunicodechar{∉}{\ensuremath{\notin}}
\newunicodechar{→}{\ensuremath{\to}}
\newunicodechar{↦}{\ensuremath{\mapsto}}
\newunicodechar{×}{\ensuremath{\times}}

% Unicode minus (U+2212) shows up a lot when copy/pasting formulas
\newunicodechar{−}{\ensuremath{-}}
""",
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

# Keep Google-style docstrings readable (avoid deep field-list indentation).
napoleon_use_param = False
napoleon_use_rtype = False
