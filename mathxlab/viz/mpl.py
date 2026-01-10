"""Minimal Matplotlib styling helpers.

This module provides a very small convenience wrapper around Matplotlib's
stateful pyplot interface. It is primarily intended for simple experiments.
For richer figure finalization, prefer `mathxlab.plots.helpers.finalize_figure`.
"""

from __future__ import annotations

import matplotlib.pyplot as plt

__all__ = [
    "finalize_figure",
]


# ------------------------------------------------------------------------------
def finalize_figure(title: str, xlabel: str, ylabel: str, grid: bool = True) -> None:
    """
    Apply consistent Matplotlib styling to the current figure.

    Args:
        title: Figure title.
        xlabel: X-axis label.
        ylabel: Y-axis label.
        grid: Whether to enable a grid.

    See Also:
        - mathxlab.plots.helpers.finalize_figure: Figure-level finalization for object-oriented Matplotlib usage.

    Examples:
        >>> import matplotlib.pyplot as plt
        >>> from mathxlab.viz.mpl import finalize_figure
        >>> finalize_figure("Demo", "x", "y")
    """
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    if grid:
        plt.grid(True)

    plt.tight_layout()
