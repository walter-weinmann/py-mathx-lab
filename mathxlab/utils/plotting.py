"""Shared plotting utilities for py-mathx-lab.

This module centralizes Matplotlib configuration so experiments can remain
small and consistent.

A key feature is optional *true LaTeX* rendering in generated figures:

- Default: Matplotlib's built-in mathtext engine (portable; no TeX required)
  with a LaTeX-like global style (Computer Modern math + serif font stack).
- Optional: enable `text.usetex = True` if a LaTeX toolchain is available.

Recommended usage (early in an experiment's `run()`):

    from mathxlab.utils.plotting import configure_matplotlib

    configure_matplotlib()  # portable defaults
    # or: MATHXLAB_USETEX=1 make run EXP=e012

The environment variable `MATHXLAB_USETEX` controls LaTeX usage:
    - unset / "0"  -> mathtext
    - "1"          -> try LaTeX; fall back to mathtext if toolchain is missing

Notes:
    - Matplotlib's `usetex` path normally uses `latex` + `dvipng` (or `dvisvgm`)
      behind the scenes. This is independent from Sphinx `latexmk` runs.
"""

from __future__ import annotations

import os
import shutil
from collections.abc import Mapping, Sequence
from dataclasses import dataclass

import matplotlib as mpl

# ------------------------------------------------------------------------------
# A LaTeX-ish serif font preference stack.
# Matplotlib will pick the first installed font available at runtime.
_LATEXISH_SERIF_STACK: list[str] = [
    # Best if installed:
    "CMU Serif",  # Computer Modern Unicode
    "Computer Modern Roman",
    "Latin Modern Roman",
    # Good widely-available fallback with TeX-like proportions:
    "STIXGeneral",
    # Always available with Matplotlib:
    "DejaVu Serif",
]


# ------------------------------------------------------------------------------
@dataclass(frozen=True, slots=True)
class LatexToolchainStatus:
    """Represents the availability of an external LaTeX toolchain.

    Args:
        latex: True if `latex` (or an alternative TeX engine) is available.
        dvipng: True if `dvipng` is available.
        dvisvgm: True if `dvisvgm` is available.
    """

    latex: bool
    dvipng: bool
    dvisvgm: bool


# ------------------------------------------------------------------------------
def detect_latex_toolchain() -> LatexToolchainStatus:
    """Detect whether an external LaTeX toolchain is available.

    Matplotlib's `text.usetex = True` typically requires:
      - `latex`
      - and one of `dvipng` or `dvisvgm`

    Returns:
        A `LatexToolchainStatus` instance describing which tools were found.
    """
    latex = shutil.which("latex") is not None
    dvipng = shutil.which("dvipng") is not None
    dvisvgm = shutil.which("dvisvgm") is not None
    return LatexToolchainStatus(latex=latex, dvipng=dvipng, dvisvgm=dvisvgm)


# ------------------------------------------------------------------------------
def _env_flag(name: str, default: str = "0") -> bool:
    """Parse a boolean-like environment variable.

    Args:
        name: Environment variable name.
        default: Default value if the variable is not set.

    Returns:
        True if the variable is set to a truthy value ("1", "true", "yes", "on"),
        otherwise False.
    """
    raw = os.getenv(name, default).strip().lower()
    return raw in {"1", "true", "yes", "on"}


# ------------------------------------------------------------------------------
def configure_matplotlib(
    *,
    use_tex: bool | None = None,
    tex_preamble: Sequence[str] | None = None,
    font_family: str = "serif",
    rcparams: Mapping[str, object] | None = None,
) -> bool:
    """Configure Matplotlib defaults for experiments.

    This sets stable, portable defaults and optionally enables true LaTeX
    rendering for math labels.

    Selection logic:
      - If `use_tex` is given, it is respected.
      - Otherwise, `MATHXLAB_USETEX=1` triggers an attempt to enable `usetex`.
      - If LaTeX tools are missing, configuration falls back to mathtext.

    Global LaTeX-like look without TeX:
      - `mathtext.fontset = "cm"` uses Computer Modern for `$...$`.
      - `font.serif` prefers CMU/Computer Modern/Latin Modern (falls back cleanly).
      - `axes.formatter.use_mathtext = True` makes tick formatting use mathtext.

    Args:
        use_tex: Whether to enable Matplotlib's `text.usetex`. If None, uses
            `MATHXLAB_USETEX` env var.
        tex_preamble: Optional LaTeX preamble lines (e.g. packages). Only used
            when LaTeX is enabled.
        font_family: Matplotlib font family to prefer (defaults to serif).
        rcparams: Extra rcParams to apply after base configuration.

    Returns:
        True if LaTeX rendering was enabled; False if mathtext is used.
    """
    # Stable defaults that work well across platforms.
    #
    # Important: we configure a LaTeX-ish mathtext + font stack by default,
    # even when TeX is not installed, so `$...$` and surrounding text look consistent.
    base: dict[str, object] = {
        # Text (non-math) font configuration
        "font.family": font_family,
        "font.serif": list(_LATEXISH_SERIF_STACK),
        # MathText configuration (TeX-free, but LaTeX-like)
        "mathtext.fontset": "cm",  # Computer Modern math look
        "axes.formatter.use_mathtext": True,  # tick formatter uses mathtext too
        # General figure defaults
        "axes.grid": True,
        "figure.constrained_layout.use": True,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.05,
    }

    # Apply base first so later values can override.
    mpl.rcParams.update(base)

    if use_tex is None:
        use_tex = _env_flag("MATHXLAB_USETEX", default="0")

    latex_enabled = False
    if use_tex:
        status = detect_latex_toolchain()
        if status.latex and (status.dvipng or status.dvisvgm):
            mpl.rcParams.update({"text.usetex": True})
            latex_enabled = True

            if tex_preamble:
                # Matplotlib expects a single string or list depending on version;
                # keep it as a list to be explicit.
                mpl.rcParams.update({"text.latex.preamble": list(tex_preamble)})
        else:
            # Fall back cleanly.
            mpl.rcParams.update({"text.usetex": False})
            latex_enabled = False
    else:
        mpl.rcParams.update({"text.usetex": False})
        latex_enabled = False

    if rcparams:
        mpl.rcParams.update(dict(rcparams))

    return latex_enabled


# ------------------------------------------------------------------------------
def make_math_label(expr: str) -> str:
    """Wrap an expression in `$...$` for math rendering.

    Args:
        expr: A LaTeX/mathtext expression (without surrounding `$`).

    Returns:
        A string like `"$\\pi(x) \\sim x/\\log x$"`.

    Notes:
        Use raw strings in calling code where convenient:
            ax.set_title(rf"Prime counting: {make_math_label('\\pi(x)')}")

        This helper keeps figure code consistent and avoids duplicated `$`.
    """
    inner = expr.strip()
    if inner.startswith("$") and inner.endswith("$"):
        return inner
    return f"${inner}$"
