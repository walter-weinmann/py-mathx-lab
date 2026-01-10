"""Filesystem and serialization helpers for experiment runs.

This module standardizes where experiments write their artifacts:

- figures/            (PNG images)
- report.md           (human-readable summary)
- params.json         (machine-readable parameters)

It is intentionally small and dependency-light so experiments can import it
without pulling in heavy tooling.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import matplotlib.figure
import numpy as np

from mathxlab.plots.helpers import finalize_figure

__all__ = [
    "RunPaths",
    "json_default",
    "prepare_out_dir",
    "save_figure",
    "write_json",
    "write_text",
]

# ------------------------------------------------------------------------------
logger = logging.getLogger(__name__)


type JsonDict = dict[str, Any]


# ------------------------------------------------------------------------------
@dataclass(frozen=True)
class RunPaths:
    """
    Standard output paths for an experiment run.

    Examples:
        >>> from mathxlab.exp.io import RunPaths
        >>> RunPaths  # doctest: +SKIP
    """

    root: Path
    figures_dir: Path
    report_path: Path
    params_path: Path


# ------------------------------------------------------------------------------
def prepare_out_dir(*, out_dir: Path) -> RunPaths:
    """
    Prepare the output directory structure.

    Args:
        out_dir: The root output directory for the experiment.

    Returns:
        A RunPaths object containing the paths to standard artifacts.

    Examples:
        >>> from pathlib import Path
        >>> from mathxlab.exp.io import prepare_out_dir
        >>> paths = prepare_out_dir(out_dir=Path("out/e001"))
    """
    logger.info("Preparing output directory: %s", out_dir)
    figures_dir = out_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    return RunPaths(
        root=out_dir,
        figures_dir=figures_dir,
        report_path=out_dir / "report.md",
        params_path=out_dir / "params.json",
    )


# ------------------------------------------------------------------------------
def save_figure(
    *,
    out_dir: Path,
    name: str,
    fig: matplotlib.figure.Figure,
    dpi: int = 160,
    finalize: bool = True,
) -> Path:
    """
    Save a Matplotlib figure to disk.

    Args:
        out_dir: Directory to save the figure in.
        name: Filename (without extension).
        fig: The figure object to save.
        dpi: Dots per inch for the output image.
        finalize: If True, apply standard formatting via :func:`finalize_figure`
            before saving.

    Returns:
        The path where the figure was saved.

    Notes:
        When `finalize=True`, the function applies shared layout and math-text configuration before saving.

    Examples:
        >>> import matplotlib.pyplot as plt
        >>> from mathxlab.exp.io import save_figure
        >>> fig = plt.figure(); _ = save_figure(out_dir=Path("out/e001/figures"), name="demo", fig=fig)
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{name}.png"
    if finalize:
        finalize_figure(fig)
    logger.info("Saving figure to: %s", path)
    fig.savefig(path, dpi=dpi, bbox_inches="tight", pad_inches=0.10)
    return path


# ------------------------------------------------------------------------------
def json_default(obj: Any) -> Any:
    """
    Default JSON encoder for math objects.

    Args:
        obj: Object to encode.

    Returns:
        A JSON-serializable representation of the object.

    Raises:
        TypeError: If the object type is not supported.

    Examples:
        >>> from mathxlab.exp.io import json_default
        >>> json_default  # doctest: +SKIP
    """
    if isinstance(obj, complex):
        return {"real": obj.real, "imag": obj.imag}
    if isinstance(obj, (np.integer, np.floating)):
        return obj.item()
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, Path):
        return str(obj)
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")


# ------------------------------------------------------------------------------
def write_json(path: Path, data: JsonDict) -> None:
    """
    Write a dictionary to a JSON file with stable formatting.

    Args:
        path: Path to the JSON file.
        data: Dictionary to write.

    Notes:
        The parent directory is not created automatically. Use `prepare_out_dir()` first, or create the directory yourself.

    Examples:
        >>> from pathlib import Path
        >>> from mathxlab.exp.io import write_json
        >>> write_json(Path("out/e001/params.json"), {"seed": 1, "n": 100})
    """
    logger.info("Writing JSON to: %s", path)
    path.write_text(
        json.dumps(data, indent=2, sort_keys=True, default=json_default) + "\n", encoding="utf-8"
    )


# ------------------------------------------------------------------------------
def write_text(path: Path, text: str, encoding: str = "utf-8") -> None:
    """
    Write text to a file.

    Args:
        path: Path to the file.
        text: Text to write.
        encoding: Text encoding.

    Examples:
        >>> from pathlib import Path
        >>> from mathxlab.exp.io import write_text
        >>> write_text(Path("out/e001/report.md"), "# Report\n")
    """
    logger.info("Writing text to: %s", path)
    path.write_text(text, encoding=encoding)
