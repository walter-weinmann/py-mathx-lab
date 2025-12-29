from __future__ import annotations

import matplotlib
import matplotlib.figure


# ------------------------------------------------------------------------------
def configure_mathtext() -> None:
    r"""Configure Matplotlib mathtext for consistent, TeX-like rendering.

    Notes:
        This uses Matplotlib's built-in *mathtext* engine (not LaTeX) so figures
        render without requiring a TeX installation.

        Mathtext does **not** support every LaTeX macro. In particular, prefer:

            r"$a \equiv b\ (\mathrm{mod}\ n)$"

        over:

            r"$a \equiv b \pmod{n}$"

        because ``\pmod`` is not supported by mathtext.
    """
    matplotlib.rcParams["mathtext.fontset"] = "stix"
    matplotlib.rcParams["font.family"] = "STIXGeneral"
    matplotlib.rcParams["axes.unicode_minus"] = False


# ------------------------------------------------------------------------------
def finalize_figure(fig: matplotlib.figure.Figure) -> None:
    """Apply standard styling and layout to a figure.

    Args:
        fig: The figure to finalize.
    """
    configure_mathtext()
    try:
        fig.tight_layout()
    except ValueError as exc:
        # Matplotlib mathtext can fail on unknown symbols (e.g. \le vs \leq).
        # Do not fail the experiment run for a layout issue.
        import logging

        logging.getLogger(__name__).warning("tight_layout() failed: %s", exc)
