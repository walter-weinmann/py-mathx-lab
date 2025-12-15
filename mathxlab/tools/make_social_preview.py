from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import textwrap


# ------------------------------------------------------------------------------
def make_social_preview(out_path: Path) -> Path:
    """Create a GitHub social preview PNG (1280x640) for the repository.

    The design is intentionally minimal, nerdy, and colorful:
    - subtle grid background
    - repo title + tagline
    - simple curve + points

    Args:
        out_path: Output path for the PNG file.

    Returns:
        The path to the written PNG file.
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # --- Figure: 1280x640 px ---
    dpi: int = 160
    width_px: int = 1280
    height_px: int = 640
    fig_w_in: float = width_px / dpi
    fig_h_in: float = height_px / dpi

    fig = plt.figure(figsize=(fig_w_in, fig_h_in), dpi=dpi)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_axis_off()

    # Background
    bg = "#0b1020"  # deep navy
    fig.patch.set_facecolor(bg)
    ax.set_facecolor(bg)

    # Subtle grid (single color, less noisy)
    grid_alpha: float = 0.08
    grid_color: str = "#ffffff"
    for x in np.linspace(0.05, 0.95, 16):
        ax.plot([x, x], [0.08, 0.92], lw=1.0, color=grid_color, alpha=grid_alpha, transform=ax.transAxes)
    for y in np.linspace(0.08, 0.92, 9):
        ax.plot([0.05, 0.95], [y, y], lw=1.0, color=grid_color, alpha=grid_alpha, transform=ax.transAxes)

    # Title / tagline (Fix 2: top-aligned + left-column width via wrapping)
    title = "py-mathx-lab"
    tagline = "Reproducible mathematical experiments in Python."
    tagline_wrapped = textwrap.fill(tagline, width=34)

    ax.text(
        0.08,
        0.92,
        title,
        transform=ax.transAxes,
        fontsize=42,
        fontweight="bold",
        color="white",
        va="top",
        ha="left",
    )
    ax.text(
        0.08,
        0.73,
        tagline_wrapped,
        transform=ax.transAxes,
        fontsize=18,
        color="#c7d2fe",
        va="top",
        ha="left",
        linespacing=1.15,
    )

    # Number theory motif (instead of the sum formula)
    ax.text(
        0.08,
        0.53,
        # Perfect numbers
        "6, 28, 496, 8128, 33550336, …",
        transform=ax.transAxes,
        fontsize=15,
        color="#a7f3d0",
        va="top",
        ha="left",
        fontfamily="monospace",
        alpha=0.95,
    )

    # Map into axes coordinates box on the right
    x0, x1 = 0.70, 0.94
    y0, y1 = 0.20, 0.80

    # Accent badge
    ax.text(
        0.08,
        0.30,
        "EXPERIMENTS",
        transform=ax.transAxes,
        fontsize=14,
        fontweight="bold",
        color=bg,
        bbox=dict(boxstyle="round,pad=0.35", facecolor="#fbbf24", edgecolor="none"),
        va="center",
        ha="left",
    )

    fig.savefig(out_path, dpi=dpi, facecolor=fig.get_facecolor(), bbox_inches=None, pad_inches=0.0)
    plt.close(fig)
    return out_path


# ------------------------------------------------------------------------------
def main() -> None:
    """CLI entry point."""
    out_path = Path("assets") / "social-preview.png"
    written = make_social_preview(out_path=out_path)
    print(f"Wrote: {written.as_posix()}")


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
