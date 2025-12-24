from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import matplotlib.figure

logger = logging.getLogger(__name__)


type JsonDict = dict[str, Any]


@dataclass(frozen=True)
class RunPaths:
    """Standard output paths for an experiment run."""

    root: Path
    figures_dir: Path
    report_path: Path
    params_path: Path


def prepare_out_dir(*, out_dir: Path) -> RunPaths:
    """Prepare the output directory structure.

    Args:
        out_dir: The root output directory for the experiment.

    Returns:
        A RunPaths object containing the paths to standard artifacts.
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


def save_figure(*, out_dir: Path, name: str, fig: matplotlib.figure.Figure, dpi: int = 160) -> Path:
    """Save a Matplotlib figure to disk.

    Args:
        out_dir: Directory to save the figure in.
        name: Filename (without extension).
        fig: The figure object to save.
        dpi: Dots per inch for the output image.

    Returns:
        The path where the figure was saved.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{name}.png"
    logger.info("Saving figure to: %s", path)
    fig.savefig(path, dpi=dpi, bbox_inches="tight")
    return path


def write_json(path: Path, data: JsonDict) -> None:
    """Write a dictionary to a JSON file with stable formatting.

    Args:
        path: Path to the JSON file.
        data: Dictionary to write.
    """
    logger.info("Writing JSON to: %s", path)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
