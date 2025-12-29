"""Command-line helpers for experiments.

This module provides a small, stable set of CLI arguments shared by all
experiments (output directory, seed, verbosity).

Compatibility note:
Some experiments call ``parse_experiment_args(argv)`` positionally, where
``argv`` may be ``None``. The preferred style is ``parse_experiment_args(argv=argv)``.
Both are supported.
"""

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
    *args: object,
    experiment_id: str | None = None,
    description: str | None = None,
    argv: list[str] | None = None,
) -> ExperimentArgs:
    """Parse standard experiment CLI arguments.

    Args:
        experiment_id: Optional program name for help.
        description: Optional description for help.
        argv: Optional argv list (without a program name). If None, argparse reads
            from sys.argv.

    Returns:
        Parsed ExperimentArgs.
    """
    # Backward/forward compatibility:
    # Some experiments may call this as parse_experiment_args(argv)
    # while the preferred style is parse_experiment_args(argv=argv).
    if args:
        if len(args) != 1:
            raise TypeError("parse_experiment_args() accepts at most one positional argument: argv")
        if argv is not None:
            raise TypeError("parse_experiment_args(): argv given both positionally and as a keyword")

        pos_argv = args[0]
        if pos_argv is None:
            argv = None
        elif isinstance(pos_argv, (list, tuple)):
            argv = list(pos_argv)
        else:
            raise TypeError(
                "parse_experiment_args(): positional argv must be None, list[str], or tuple[str, ...]"
            )

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
