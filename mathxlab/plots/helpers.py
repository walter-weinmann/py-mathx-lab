from __future__ import annotations

import matplotlib
import matplotlib.axes
import matplotlib.figure


# ------------------------------------------------------------------------------
def apply_axis_style(
    ax: matplotlib.axes.Axes,
    *,
    title: str,
    xlab: str,
    ylab: str,
    equal: bool = False,
) -> None:
    """Apply common axis styling.

    Args:
        ax: Matplotlib axes to style.
        title: Plot title.
        xlab: X-axis label.
        ylab: Y-axis label.
        equal: If True, enforce equal scaling (useful for geometry-like plots).
    """
    ax.set_title(title)
    ax.set_xlabel(xlab)
    ax.set_ylabel(ylab)
    if equal:
        ax.set_aspect("equal")


# ------------------------------------------------------------------------------
def configure_mathtext() -> None:
    """Configure Matplotlib MathText to look more LaTeX-like.

    This repository uses MathText (not a full TeX installation) for portability.
    The settings here make $...$ labels and titles render closer to LaTeX.

    Notes:
        These settings are global (rcParams).
    """
    matplotlib.rcParams["mathtext.fontset"] = "cm"
    matplotlib.rcParams["axes.formatter.use_mathtext"] = True


# ------------------------------------------------------------------------------
def finalize_figure(fig: matplotlib.figure.Figure) -> None:
    """Finalize a Matplotlib figure (layout + MathText config).

    Args:
        fig: The figure to finalize.
    """
    configure_mathtext()
    try:
        fig.tight_layout()
    except ValueError as exc:
        # MathText can fail on unknown symbols; do not fail the experiment.
        import logging

        logging.getLogger(__name__).warning("tight_layout() failed: %s", exc)
