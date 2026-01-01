from __future__ import annotations

from typing import Any, Literal

import matplotlib
import matplotlib.axes
import matplotlib.figure
import numpy as np


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
        title: Figure title.
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


# ------------------------------------------------------------------------------
def imshow_centered(
    ax: matplotlib.axes.Axes,
    img: np.ndarray,
    *,
    size: int,
    origin: Literal["lower", "upper"] = "lower",
    interpolation: str = "nearest",
    **imshow_kwargs: Any,
) -> None:
    """Show an image with axes centered at (0, 0) and integer grid coordinates.

    This maps the *center pixel* to coordinate (0, 0) and labels axes in
    "grid offsets from center", i.e. approximately [-k..k] where k=(size-1)//2.

    Notes:
        For imshow, `extent` refers to pixel *edges*. Using ±0.5 ensures pixel
        centers align with integer coordinates.

    Args:
        ax: Matplotlib axes to draw on.
        img: 2D image array.
        size: Image width/height (must match img.shape).
        origin: "lower" for y increasing upward, "upper" for image-style.
        interpolation: Pixel interpolation mode.
        **imshow_kwargs: Forwarded to `ax.imshow`.
    """
    if img.shape[0] != size or img.shape[1] != size:
        raise ValueError(f"img shape {img.shape} does not match size={size}")

    if size <= 0 or size % 2 == 0:
        raise ValueError("size must be positive and odd")

    k = (size - 1) // 2
    ax.imshow(
        img,
        origin=origin,
        extent=(-k - 0.5, k + 0.5, -k - 0.5, k + 0.5),
        interpolation=interpolation,
        **imshow_kwargs,
    )
