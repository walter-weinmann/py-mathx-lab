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

__all__ = [
    "ExperimentArgs",
    "ExperimentArgsWithNMax",
    "ExperimentArgsWithSize",
    "parse_experiment_args",
    "parse_experiment_args_with_n_max",
    "parse_experiment_args_with_size",
]


# ------------------------------------------------------------------------------
@dataclass(frozen=True)
class ExperimentArgs:
    """
    Parsed command-line arguments for an experiment run.

    Attributes:
        out_dir: Output directory where all artifacts will be written.
        seed: Deterministic seed for randomness.
        verbose: Enable verbose logging.

    Examples:
        >>> from mathxlab.exp.cli import ExperimentArgs
        >>> ExperimentArgs  # doctest: +SKIP
    """

    out_dir: Path
    seed: int
    verbose: bool


# ------------------------------------------------------------------------------
@dataclass(frozen=True)
class ExperimentArgsWithSize:
    """
    Parsed command-line arguments for an experiment run with a `size` parameter.

    Attributes:
        out_dir: Output directory where all artifacts will be written.
        seed: Deterministic seed for reproducibility.
        verbose: Enable verbose logging.
        size: Grid size parameter (meaning depends on experiment).

    Examples:
        >>> from mathxlab.exp.cli import ExperimentArgsWithSize
        >>> ExperimentArgsWithSize  # doctest: +SKIP
    """

    out_dir: Path
    seed: int
    verbose: bool
    size: int


# ------------------------------------------------------------------------------
@dataclass(frozen=True)
class ExperimentArgsWithNMax:
    """
    Parsed command-line arguments for an experiment run with an `n_max` parameter.

    Attributes:
        out_dir: Output directory where all artifacts will be written.
        seed: Deterministic seed for reproducibility.
        verbose: Enable verbose logging.
        n_max: Inclusive upper bound for computations (must be >= 2).

    Examples:
        >>> from mathxlab.exp.cli import ExperimentArgsWithNMax
        >>> ExperimentArgsWithNMax  # doctest: +SKIP
    """

    out_dir: Path
    seed: int
    verbose: bool
    n_max: int


# ------------------------------------------------------------------------------
def parse_experiment_args_with_size(
    *args: object,
    experiment_id: str | None = None,
    description: str | None = None,
    argv: list[str] | None = None,
    size_default: int = 301,
    size_help: str = "Grid size parameter (must be positive and odd).",
) -> ExperimentArgsWithSize:
    """
    Parse standard experiment CLI arguments plus a `--size` option.

    This helper keeps new experiments consistent with the standard template while
    allowing a common `--size` knob for grid-based visualizations.

    Args:
        experiment_id: Optional program name for help.
        description: Optional description for help.
        argv: Optional argv list (without a program name). If None, argparse reads
            from sys.argv.
        size_default: Default `size` value.
        size_help: Help text for the `--size` option.

    Returns:
        Parsed ExperimentArgsWithSize.

    Raises:
        TypeError: If argv is passed both positionally and as a keyword, or if the
            positional argv is invalid.
        SystemExit: If size is non-positive or even.

    Examples:
        >>> from mathxlab.exp.cli import parse_experiment_args_with_size
        >>> args = parse_experiment_args_with_size(argv=["--out", "out/e124", "--size", "401"])
        >>> args.size
        401
    """
    # Backward/forward compatibility (match parse_experiment_args):
    if args:
        if len(args) != 1:
            raise TypeError(
                "parse_experiment_args_with_size() accepts at most one positional argument: argv"
            )

        pos_argv = args[0]
        if pos_argv is not None and argv is not None:
            raise TypeError(
                "parse_experiment_args_with_size(): argv given both positionally and as a keyword"
            )

        if pos_argv is None:
            pass
        elif isinstance(pos_argv, (list, tuple)):
            argv = list(pos_argv)
        else:
            raise TypeError(
                "parse_experiment_args_with_size(): positional argv must be None, list[str], or tuple[str, ...]"
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
        help="Output directory (e.g., out/e124).",
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
    parser.add_argument(
        "--size",
        dest="size",
        type=int,
        default=size_default,
        help=size_help,
    )

    ns = parser.parse_args(argv)

    if ns.size <= 0:
        raise SystemExit("--size must be positive")
    if ns.size % 2 == 0:
        raise SystemExit("--size must be odd")

    return ExperimentArgsWithSize(
        out_dir=ns.out_dir, seed=ns.seed, verbose=ns.verbose, size=ns.size
    )


# ------------------------------------------------------------------------------
def parse_experiment_args_with_n_max(
    *args: object,
    experiment_id: str | None = None,
    description: str | None = None,
    argv: list[str] | None = None,
    n_max_default: int = 2_000_000,
    n_max_help: str = "Inclusive upper bound N for computations (>= 2).",
) -> ExperimentArgsWithNMax:
    """
    Parse standard experiment CLI arguments plus a `--n-max` option.

    Compatibility note:
    Some experiments call ``parse_experiment_args_with_n_max(argv)`` positionally,
    where ``argv`` may be ``None``. The preferred style is
    ``parse_experiment_args_with_n_max(argv=argv)``. Both are supported.

    Args:
        experiment_id: Optional program name for help.
        description: Optional description for help.
        argv: Optional argv list (without a program name). If None, argparse reads
            from sys.argv.
        n_max_default: Default `n_max` value.
        n_max_help: Help text for the `--n-max` option.

    Returns:
        Parsed ExperimentArgsWithNMax.

    Raises:
        TypeError: If argv is passed both positionally and as a keyword, or if the
            positional argv is invalid.
        SystemExit: If n_max is < 2.
    """
    # Backward/forward compatibility (match parse_experiment_args):
    if args:
        if len(args) != 1:
            raise TypeError(
                "parse_experiment_args_with_n_max() accepts at most one positional argument: argv"
            )

        pos_argv = args[0]
        if pos_argv is not None and argv is not None:
            raise TypeError(
                "parse_experiment_args_with_n_max(): argv given both positionally and as a keyword"
            )

        if pos_argv is None:
            # argv remains as passed via keyword (which might be None)
            pass
        elif isinstance(pos_argv, (list, tuple)):
            argv = list(pos_argv)
        else:
            raise TypeError(
                "parse_experiment_args_with_n_max(): positional argv must be None, list[str], or tuple[str, ...]"
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
    parser.add_argument(
        "--n-max",
        dest="n_max",
        type=int,
        default=n_max_default,
        help=n_max_help,
    )

    ns = parser.parse_args(argv)
    if ns.n_max < 2:
        raise SystemExit("--n-max must be >= 2")

    return ExperimentArgsWithNMax(
        out_dir=ns.out_dir, seed=ns.seed, verbose=ns.verbose, n_max=ns.n_max
    )


# ------------------------------------------------------------------------------
def parse_experiment_args(
    *args: object,
    experiment_id: str | None = None,
    description: str | None = None,
    argv: list[str] | None = None,
) -> ExperimentArgs:
    """
    Parse standard experiment CLI arguments.

    Args:
        experiment_id: Optional program name for help.
        description: Optional description for help.
        argv: Optional argv list (without a program name). If None, argparse reads
            from sys.argv.

    Returns:
        Parsed ExperimentArgs.

    Examples:
        >>> from mathxlab.exp.cli import parse_experiment_args
        >>> args = parse_experiment_args(argv=["--out", "out/e001", "--seed", "7"])
        >>> args.out_dir.name
        'e001'
    """
    # Backward/forward compatibility:
    # Some experiments may call this as parse_experiment_args(argv)
    # while the preferred style is parse_experiment_args(argv=argv).
    if args:
        if len(args) != 1:
            raise TypeError("parse_experiment_args() accepts at most one positional argument: argv")

        pos_argv = args[0]
        if pos_argv is not None and argv is not None:
            raise TypeError(
                "parse_experiment_args(): argv given both positionally and as a keyword"
            )

        if pos_argv is None:
            # argv remains as passed via keyword (which might be None)
            pass
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
