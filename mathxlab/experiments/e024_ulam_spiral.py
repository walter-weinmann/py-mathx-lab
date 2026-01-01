"""E024 — Ulam spiral structure.

This is a thin wrapper that follows the standard experiment template and delegates
the actual computation to :mod:`mathxlab.experiments.prime_suite`.

Usage:
    make run EXP=e024
    # optional: override the default size (must be odd)
    make run EXP=e024 ARGS="--size 501"

Artifacts:
    - figures/fig_*.png
    - params.json
    - report.md
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

from mathxlab.exp.io import prepare_out_dir
from mathxlab.exp.logging import LoggingConfig, get_logger, setup_logging
from mathxlab.exp.random import set_global_seed
from mathxlab.experiments.prime_suite import run_e024

# ------------------------------------------------------------------------------
logger = get_logger(__name__)


# ------------------------------------------------------------------------------
@dataclass(frozen=True, slots=True)
class E024Args:
    """Parsed command-line arguments for E024.

    Attributes:
        out_dir: Output directory where all artifacts will be written.
        seed: Deterministic seed for reproducibility.
        verbose: Enable verbose logging.
        size: Odd grid size (size x size).
    """

    out_dir: Path
    seed: int
    verbose: bool
    size: int


# ------------------------------------------------------------------------------
def _parse_e024_args(argv: list[str] | None = None) -> E024Args:
    """Parse command-line arguments for E024.

    Args:
        argv: Optional argv list (without a program name). If None, argparse reads
            from sys.argv.

    Returns:
        Parsed E024Args.
    """
    parser = argparse.ArgumentParser(
        prog="e024",
        description="Ulam spiral structure",
        add_help=True,
    )
    parser.add_argument(
        "--out",
        dest="out_dir",
        type=Path,
        required=True,
        help="Output directory (e.g., out/e024).",
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
        default=301,
        help="Odd grid size (size x size).",
    )

    ns = parser.parse_args(argv)
    if ns.size <= 0:
        raise SystemExit("--size must be positive")
    if ns.size % 2 == 0:
        raise SystemExit("--size must be odd")

    return E024Args(out_dir=ns.out_dir, seed=ns.seed, verbose=ns.verbose, size=ns.size)


# ------------------------------------------------------------------------------
def main() -> int:
    """Run the experiment.

    Returns:
        Process exit code (0 for success).
    """
    args = _parse_e024_args()
    setup_logging(config=LoggingConfig(verbose=args.verbose))
    set_global_seed(args.seed)

    out_paths = prepare_out_dir(out_dir=args.out_dir)

    logger.info("Starting experiment E024")
    run_e024(
        out_dir=Path(args.out_dir),
        seed=args.seed,
        figures_dir=out_paths.figures_dir,
        report_path=out_paths.report_path,
        params_path=out_paths.params_path,
        size=args.size,
    )
    logger.info("Experiment E024 completed successfully. Artifacts saved to: %s", args.out_dir)
    return 0


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
