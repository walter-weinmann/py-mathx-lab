from __future__ import annotations

import matplotlib.pyplot as plt


# ------------------------------------------------------------------------------
def finalize_figure(title: str, xlabel: str, ylabel: str, grid: bool = True) -> None:
    """Apply consistent Matplotlib styling to the current figure.

    Args:
        title: Figure title.
        xlabel: X-axis label.
        ylabel: Y-axis label.
        grid: Whether to enable a grid.
    """
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    if grid:
        plt.grid(True)

    plt.tight_layout()
