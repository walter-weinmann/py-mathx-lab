from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt


# ------------------------------------------------------------------------------
@dataclass(frozen=True)
class RunArtifacts:
    """Paths to standard artifacts produced by an experiment run.

    Attributes:
        out_dir: Output directory.
        report_md: Path to the Markdown report.
        params_json: Path to parameters JSON file.
    """

    out_dir: Path
    report_md: Path
    params_json: Path


# ------------------------------------------------------------------------------
def prepare_out_dir(out_dir: Path) -> RunArtifacts:
    """Create the output directory and return standard artifact paths.

    Args:
        out_dir: Output directory.

    Returns:
        RunArtifacts with paths for a report and params.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    return RunArtifacts(
        out_dir=out_dir,
        report_md=out_dir / "report.md",
        params_json=out_dir / "params.json",
    )


# ------------------------------------------------------------------------------
def save_figure(path: Path) -> None:
    """Save the current Matplotlib figure to disk.

    Args:
        path: Output image path.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(path, dpi=160, bbox_inches="tight")
    plt.close()


# ------------------------------------------------------------------------------
def write_json(path: Path, payload: dict[str, Any]) -> None:
    """Write a JSON file with stable formatting.

    Args:
        path: Output path.
        payload: JSON-serializable payload.
    """
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
