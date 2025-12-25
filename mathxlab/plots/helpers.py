from __future__ import annotations

import matplotlib.figure


# ------------------------------------------------------------------------------
def finalize_figure(fig: matplotlib.figure.Figure) -> None:
    """Apply standard styling and layout to a figure.

    Args:
        fig: The figure to finalize.
    """
    # For now, just apply tight_layout.
    # Can be extended with more styling.
    fig.tight_layout()
