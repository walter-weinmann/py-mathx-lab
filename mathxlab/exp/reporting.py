"""Small helpers for writing experiment artifacts.

This module provides a minimal API for writing report files and figures.
For new experiments, `mathxlab.exp.io` is preferred because it offers a more
complete and consistent output layout.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt

from mathxlab.exp.io import json_default

__all__ = [
    "RunArtifacts",
    "prepare_out_dir",
    "save_figure",
    "write_json",
]

type JsonPayload = dict[str, Any]


# ------------------------------------------------------------------------------
@dataclass(frozen=True)
class RunArtifacts:
    """
    Paths to standard artifacts produced by an experiment run.

    Attributes:
        out_dir: Output directory.
        report_md: Path to the Markdown report.
        params_json: Path to parameters JSON file.

    Examples:
        >>> from mathxlab.exp.reporting import RunArtifacts
        >>> RunArtifacts  # doctest: +SKIP
    """

    out_dir: Path
    report_md: Path
    params_json: Path


# ------------------------------------------------------------------------------
def prepare_out_dir(out_dir: Path) -> RunArtifacts:
    """
    Create the output directory and return standard artifact paths.

    Args:
        out_dir: Output directory.

    Returns:
        RunArtifacts with paths for a report and params.

    See Also:
        - mathxlab.exp.io.prepare_out_dir: Preferred output layout helper for new experiments.

    Examples:
        >>> from pathlib import Path
        >>> from mathxlab.exp.reporting import prepare_out_dir
        >>> arts = prepare_out_dir(Path("out/e001"))
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    return RunArtifacts(
        out_dir=out_dir,
        report_md=out_dir / "report.md",
        params_json=out_dir / "params.json",
    )


# ------------------------------------------------------------------------------
def save_figure(path: Path) -> None:
    """
    Save the current Matplotlib figure to disk.

    Args:
        path: Output image path.

    See Also:
        - mathxlab.exp.io.save_figure: Figure saving with optional finalization.

    Examples:
        >>> from mathxlab.exp.reporting import save_figure
        >>> save_figure  # doctest: +SKIP
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(path, dpi=160, bbox_inches="tight")
    plt.close()


# ------------------------------------------------------------------------------
def write_json(path: Path, payload: JsonPayload) -> None:
    """
    Write a JSON file with stable formatting.

    Args:
        path: Output path.
        payload: JSON-serializable payload.

    See Also:
        - mathxlab.exp.io.write_json: JSON writer with NumPy/Path support via `json_default`.

    Examples:
        >>> from pathlib import Path
        >>> from mathxlab.exp.reporting import write_json
        >>> write_json(Path("out/e001/params.json"), {"seed": 1})
    """
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, default=json_default) + "\n", encoding="utf-8"
    )
