"""Prime-visualization spiral suite (E124–E126).

This module groups prime-visualization experiments that arrange the natural
numbers in alternative geometric layouts and highlight the primes:

- E124: Klauber triangle (rows between consecutive squares)
- E125: Sacks spiral (polar coordinates r=sqrt(n), theta=2π sqrt(n))
- E126: Hexagonal number spiral (centered hex-grid spiral)

Each `run_e###` function writes:
- one or more figures under `figures_dir`
- `params.json`
- `report.md`

Notes:
- The `seed` argument is accepted for consistency with the experiment interface,
  but these experiments are deterministic (unless you later add randomized
  rendering options).
"""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from pathlib import Path
from time import perf_counter

import matplotlib.pyplot as plt
import numpy as np

from mathxlab.exp.io import save_figure, write_json
from mathxlab.plots.helpers import apply_axis_style, finalize_figure

from ._prime_utils import prime_mask_up_to


# ------------------------------------------------------------------------------
def _axial_to_xy(q: np.ndarray, r: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Convert axial hex coordinates to 2D Cartesian coordinates.

    Uses a pointy-top axial layout.

    Args:
        q: Axial q coordinates.
        r: Axial r coordinates.

    Returns:
        (x, y) Cartesian coordinates.
    """
    x = math.sqrt(3.0) * (q.astype(float) + 0.5 * r.astype(float))
    y = 1.5 * r.astype(float)
    return x, y


# ------------------------------------------------------------------------------
def _basic_report_header(eid: str, title: str, reproduce_exp: str) -> list[str]:
    """Return standard report header lines.

    Args:
        eid: Experiment id like "E124".
        title: Human-readable title.
        reproduce_exp: Experiment module name like "e124".

    Returns:
        Lines for the top of report.md.
    """
    return [
        f"# {eid.upper()} — {title}",
        "",
        "**Reproduce:**",
        "",
        "```bash",
        f"make run EXP={reproduce_exp}",
        "```",
        "",
    ]


# ------------------------------------------------------------------------------
def _hex_spiral_axial_coords(rings: int) -> tuple[np.ndarray, np.ndarray]:
    """Generate axial (q, r) coordinates for a centered hex spiral.

    The sequence starts at (0, 0) for n=1 and then enumerates rings 1..rings
    around the origin on an axial hex grid (pointy-top layout).

    Implementation notes:
    - For ring k, we start at the axial corner (-k, k) and walk k steps in each
      of the 6 axial directions.
    - The construction is deterministic and produces exactly
      1 + 3*rings*(rings + 1) coordinates.

    Args:
        rings: Number of rings (>= 0).

    Returns:
        Two arrays (q, r) of equal length, one coordinate per integer.
    """
    if rings < 0:
        raise ValueError("rings must be >= 0")

    coords_q: list[int] = [0]
    coords_r: list[int] = [0]

    # Axial directions for a pointy-top layout.
    directions: list[tuple[int, int]] = [
        (1, 0),
        (1, -1),
        (0, -1),
        (-1, 0),
        (-1, 1),
        (0, 1),
    ]

    for k in range(1, rings + 1):
        q, r = -k, k  # start at a corner of the k-th ring
        for dq, dr in directions:
            for _ in range(k):
                coords_q.append(q)
                coords_r.append(r)
                q += dq
                r += dr

    return np.asarray(coords_q, dtype=np.int64), np.asarray(coords_r, dtype=np.int64)


# ------------------------------------------------------------------------------
@dataclass(frozen=True, slots=True)
class ParamsE124:
    """Parameters for E124 (Klauber triangle).

    Attributes:
        rows: Number of rows in the triangle. Row m contains integers
            from (m-1)^2 + 1 to m^2 (inclusive), so total integers are rows^2.
    """

    rows: int = 301


# ------------------------------------------------------------------------------
@dataclass(frozen=True, slots=True)
class ParamsE125:
    """Parameters for E125 (Sacks spiral).

    Attributes:
        n_max: Largest integer to place on the spiral (inclusive). Integers 1..n_max
            are mapped to polar coordinates r=sqrt(n), theta=2π sqrt(n).
    """

    n_max: int = 250_000


# ------------------------------------------------------------------------------
@dataclass(frozen=True, slots=True)
class ParamsE126:
    """Parameters for E126 (hexagonal number spiral).

    Attributes:
        rings: Number of hexagonal rings around the center. The spiral contains
            1 + 3*rings*(rings+1) integers.
    """

    rings: int = 150


# ------------------------------------------------------------------------------
def run_e124(
    *,
    out_dir: Path,
    seed: int,
    figures_dir: Path,
    report_path: Path,
    params_path: Path,
    rows: int = 301,
) -> None:
    """E124: Klauber triangle: primes in a square-to-square triangle.

    In the Klauber triangle, row m contains the integers:

        (m-1)^2 + 1, (m-1)^2 + 2, ..., m^2

    i.e. between consecutive squares. Highlighting primes reveals striking vertical
    streaks for certain quadratic prime-rich sequences.

    Args:
        out_dir: Experiment output directory.
        seed: Deterministic seed for reproducibility (not used here).
        figures_dir: Directory for figure artifacts.
        report_path: Path to the Markdown report.
        params_path: Path to params.json.
        rows: Number of rows (must be positive).
    """
    if rows <= 0:
        raise ValueError("rows must be positive")

    params = ParamsE124(rows=rows)
    n_max = params.rows * params.rows

    t0 = perf_counter()
    is_prime = prime_mask_up_to(n_max)
    t_sieve = perf_counter() - t0

    width = 2 * params.rows - 1
    img = np.full((params.rows, width), np.nan, dtype=float)

    # Build rows bottom-up for a visually balanced triangle
    for m in range(1, params.rows + 1):
        start = (m - 1) * (m - 1) + 1
        end = m * m
        row_nums = np.arange(start, end + 1, dtype=np.int64)
        row_mask = is_prime[row_nums].astype(float)

        # center-align in a fixed-width canvas
        left = params.rows - m
        img[m - 1, left : left + row_nums.size] = row_mask

    fig_obj, ax = plt.subplots()
    ax.imshow(img, origin="lower", interpolation="nearest")
    ax.set_xticks([])
    ax.set_yticks([])
    apply_axis_style(
        ax,
        title="Klauber triangle (primes = 1)",
        xlab="",
        ylab="",
        equal=False,
    )
    finalize_figure(fig_obj)
    save_figure(out_dir=figures_dir, name="fig_01_klauber_triangle", fig=fig_obj)

    write_json(path=params_path, data=asdict(params))

    lines = _basic_report_header("E124", "Klauber triangle", "e124")
    lines += [
        "### Parameters",
        f"- rows: `{params.rows}`",
        f"- n_max: `{n_max}` (numbers 1..n_max)",
        "",
        "### Notes",
        "- Row m contains integers from (m-1)^2+1 to m^2 (inclusive).",
        "- The run is deterministic; `seed` is accepted for interface consistency.",
        "",
        "## Performance",
        f"- Prime sieve time: `{t_sieve:.3f}` s",
    ]
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ------------------------------------------------------------------------------
def run_e125(
    *,
    out_dir: Path,
    seed: int,
    figures_dir: Path,
    report_path: Path,
    params_path: Path,
    n_max: int = 250_000,
) -> None:
    """E125: Sacks spiral: primes on r=sqrt(n), θ=2π sqrt(n).

    Args:
        out_dir: Experiment output directory.
        seed: Deterministic seed for reproducibility (not used here).
        figures_dir: Directory for figure artifacts.
        report_path: Path to the Markdown report.
        params_path: Path to params.json.
        n_max: Largest integer to plot (inclusive).
    """
    if n_max <= 1:
        raise ValueError("n_max must be >= 2")

    params = ParamsE125(n_max=n_max)

    t0 = perf_counter()
    is_prime = prime_mask_up_to(params.n_max)
    t_sieve = perf_counter() - t0

    n = np.arange(1, params.n_max + 1, dtype=np.int64)
    prime_n = n[is_prime[n]]

    r = np.sqrt(prime_n.astype(float))
    theta = 2.0 * math.pi * r
    x = r * np.cos(theta)
    y = r * np.sin(theta)

    fig_obj, ax = plt.subplots()
    ax.scatter(x, y, s=3)
    apply_axis_style(
        ax,
        title="Sacks spiral (primes only)",
        xlab=r"$x$",
        ylab=r"$y$",
        equal=True,
    )
    finalize_figure(fig_obj)
    save_figure(out_dir=figures_dir, name="fig_01_sacks_spiral", fig=fig_obj)

    write_json(path=params_path, data=asdict(params))

    lines = _basic_report_header("E125", "Sacks spiral", "e125")
    lines += [
        "### Parameters",
        f"- n_max: `{params.n_max}` (numbers 1..n_max)",
        "",
        "### Notes",
        "- Coordinates: r=√n, θ=2π√n, plotted as (r cos θ, r sin θ).",
        "- This run plots primes only (composites omitted).",
        "- The run is deterministic; `seed` is accepted for interface consistency.",
        "",
        "## Performance",
        f"- Prime sieve time: `{t_sieve:.3f}` s",
    ]
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ------------------------------------------------------------------------------
def run_e126(
    *,
    out_dir: Path,
    seed: int,
    figures_dir: Path,
    report_path: Path,
    params_path: Path,
    rings: int = 150,
) -> None:
    """E126: Hexagonal number spiral: primes on a hex grid spiral.

    Args:
        out_dir: Experiment output directory.
        seed: Deterministic seed for reproducibility (not used here).
        figures_dir: Directory for figure artifacts.
        report_path: Path to the Markdown report.
        params_path: Path to params.json.
        rings: Number of rings around the origin (>=0).
    """
    if rings < 0:
        raise ValueError("rings must be >= 0")

    params = ParamsE126(rings=rings)
    total = 1 + 3 * params.rings * (params.rings + 1)

    t0 = perf_counter()
    is_prime = prime_mask_up_to(total)
    t_sieve = perf_counter() - t0

    q, r = _hex_spiral_axial_coords(params.rings)
    # Map n=1..total to coords; coordinate arrays already have length total
    n = np.arange(1, total + 1, dtype=np.int64)
    prime_mask = is_prime[n]

    x, y = _axial_to_xy(q, r)
    x_p = x[prime_mask]
    y_p = y[prime_mask]

    fig_obj, ax = plt.subplots()
    ax.scatter(x_p, y_p, s=5)
    apply_axis_style(
        ax,
        title="Hexagonal spiral (primes only)",
        xlab=r"$x$",
        ylab=r"$y$",
        equal=True,
    )
    finalize_figure(fig_obj)
    save_figure(out_dir=figures_dir, name="fig_01_hex_spiral", fig=fig_obj)

    write_json(path=params_path, data=asdict(params))

    lines = _basic_report_header("E126", "Hexagonal number spiral", "e126")
    lines += [
        "### Parameters",
        f"- rings: `{params.rings}`",
        f"- total: `{total}` (numbers 1..total)",
        "",
        "### Notes",
        "- The spiral enumerates hexagonal rings around the origin on an axial grid.",
        "- This run plots primes only (composites omitted).",
        "- The run is deterministic; `seed` is accepted for interface consistency.",
        "",
        "## Performance",
        f"- Prime sieve time: `{t_sieve:.3f}` s",
    ]
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
