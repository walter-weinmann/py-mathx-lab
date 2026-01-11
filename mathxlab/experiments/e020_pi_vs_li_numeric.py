"""E020: Compare pi(x) to li(x) numerically.

This is a thin wrapper that follows the standard experiment template and delegates
the actual computation to :mod:`mathxlab.experiments.prime_suite`.

Usage:
    make run EXP=e020

Artifacts:
    - figures/fig_*.png
    - params.json
    - report.md
"""

from __future__ import annotations

from pathlib import Path

from mathxlab.exp.cli import parse_experiment_args_with_n_max
from mathxlab.exp.io import prepare_out_dir
from mathxlab.exp.logging import LoggingConfig, get_logger, setup_logging
from mathxlab.exp.random import set_global_seed
from mathxlab.exp.run_logging import infer_run_log_file
from mathxlab.experiments.prime_suite import run_e020

# ------------------------------------------------------------------------------
logger = get_logger(__name__)


# ------------------------------------------------------------------------------
def main() -> int:
    """Run the experiment.

    Returns:
        Process exit code (0 for success).
    """
    args = parse_experiment_args_with_n_max(
        experiment_id="e020",
        description="Compare pi(x) to li(x) numerically",
        n_max_default=3_000_000,
        n_max_help="Inclusive upper bound N for computations (>= 2).",
    )
    run_log = infer_run_log_file(out_dir=args.out_dir, experiment_slug="e020")
    setup_logging(config=LoggingConfig(verbose=args.verbose, log_file=run_log.log_file))
    set_global_seed(args.seed)

    out_paths = prepare_out_dir(out_dir=args.out_dir)

    logger.info("Starting experiment E020")
    run_e020(
        out_dir=Path(args.out_dir),
        seed=args.seed,
        figures_dir=out_paths.figures_dir,
        report_path=out_paths.report_path,
        params_path=out_paths.params_path,
        n_max=args.n_max,
    )
    logger.info("Experiment E020 completed successfully. Artifacts saved to: %s", args.out_dir)
    return 0


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
