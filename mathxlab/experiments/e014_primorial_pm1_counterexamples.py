"""E014 — Primorial ± 1 counterexamples.

This is a thin wrapper that follows the standard experiment template and delegates
the actual computation to :mod:`mathxlab.experiments.prime_suite`.

Usage:
    make run EXP=e014

Artifacts:
    - figures/fig_*.png
    - params.json
    - report.md
"""

from __future__ import annotations

from pathlib import Path

from mathxlab.exp.cli import parse_experiment_args
from mathxlab.exp.io import prepare_out_dir
from mathxlab.exp.logging import LoggingConfig, get_logger, setup_logging
from mathxlab.exp.random import set_global_seed
from mathxlab.experiments.prime_suite import run_e014

# ------------------------------------------------------------------------------
logger = get_logger(__name__)


# ------------------------------------------------------------------------------
def main() -> int:
    """Run the experiment.

    Returns:
        Process exit code (0 for success).
    """
    args = parse_experiment_args(
        experiment_id="e014",
        description="Primorial ± 1 counterexamples",
    )
    setup_logging(config=LoggingConfig(verbose=args.verbose))
    set_global_seed(args.seed)

    out_paths = prepare_out_dir(out_dir=args.out_dir)

    logger.info("Starting experiment E014")
    run_e014(
        out_dir=Path(args.out_dir),
        seed=args.seed,
        figures_dir=out_paths.figures_dir,
        report_path=out_paths.report_path,
        params_path=out_paths.params_path,
    )
    logger.info("Experiment E014 completed successfully. Artifacts saved to: %s", args.out_dir)
    return 0


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
