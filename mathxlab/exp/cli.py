from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


# ------------------------------------------------------------------------------
@dataclass(frozen=True)
class ExperimentArgs:
    """Parsed command-line arguments for an experiment run.

    Attributes:
        out_dir: Output directory where all artifacts will be written.
        seed: Deterministic seed for randomness.
        verbose: Enable verbose logging.
    """

    out_dir: Path
    seed: int
    verbose: bool


# ------------------------------------------------------------------------------
def parse_experiment_args(
    *,
    experiment_id: str | None = None,
    description: str | None = None,
    argv: list[str] | None = None,
) -> ExperimentArgs:
    """Parse standard experiment CLI arguments.

    Args:
        experiment_id: Optional program name for help.
        description: Optional description for help.
        argv: Optional argv list (without a program name). If None, argparse
            reads from sys.argv.

    Returns:
        Parsed ExperimentArgs.
    """
    parser = argparse.ArgumentParser(
        prog=experiment_id,
        description=description,
        add_help=True,
    )
    parser.add_argument(
        "--out",
        dest="out_dir",
        type=Path,
        required=True,
        help="Output directory (e.g., out/e001).",
    )
    parser.add_argument(
        "--seed",
        dest="seed",
        type=int,
        default=1,
        help="Deterministic seed for reproducibility.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose logging.",
    )
    ns = parser.parse_args(argv)
    return ExperimentArgs(out_dir=ns.out_dir, seed=ns.seed, verbose=ns.verbose)
