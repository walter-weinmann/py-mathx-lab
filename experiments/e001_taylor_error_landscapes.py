from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from mathxlab.exp.cli import parse_experiment_args
from mathxlab.exp.reporting import prepare_out_dir, save_figure, write_json
from mathxlab.exp.seeding import set_global_seed
from mathxlab.num.series import taylor_sin
from mathxlab.viz.mpl import finalize_figure


# ------------------------------------------------------------------------------
@dataclass(frozen=True)
class Params:
    """Parameters for E001 Taylor error landscapes.

    Attributes:
        x_min: Minimum x for the grid.
        x_max: Maximum x for the grid.
        num_points: Number of grid points.
        degrees: Polynomial degrees to test.
        centers: Expansion centers to test.
    """

    x_min: float
    x_max: float
    num_points: int
    degrees: list[int]
    centers: list[float]


# ------------------------------------------------------------------------------
def _write_report(path: Path, params: Params, figures: list[str]) -> None:
    """Write a Markdown report for the experiment.

    Args:
        path: Output report path.
        params: Experiment parameters.
        figures: List of figure filenames produced.
    """
    lines: list[str] = []
    lines.append("# E001 — Taylor error landscapes (sin)\n")
    lines.append("## What this experiment does\n")
    lines.append(
        "We compare `sin(x)` to a simple Taylor-series-style polynomial approximation and "
        "measure absolute error across an interval. We vary polynomial degree and the "
        "chosen expansion center to visualize how 'local' approximations behave.\n"
    )
    lines.append("## Reproduce\n")
    lines.append(
        "```bash\npython -m experiments.e001_taylor_error_landscapes --out out/e001 --seed 1\n```\n"
    )
    lines.append("## Parameters\n")
    lines.append("```json\n")
    lines.append(f"{asdict(params)}\n")
    lines.append("```\n")
    lines.append("## Figures\n")
    for fig in figures:
        lines.append(f"- ![]({fig})\n")

    path.write_text("".join(lines), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    """Run experiment E001.

    Args:
        argv: Optional argv list (without program name).

    Returns:
        Process exit code (0 on success).
    """
    args = parse_experiment_args(argv)
    set_global_seed(args.seed)

    artifacts = prepare_out_dir(args.out_dir)

    params = Params(
        x_min=-6.0,
        x_max=6.0,
        num_points=4000,
        degrees=[1, 3, 5, 9, 15],
        centers=[0.0, 1.0, 2.0],
    )

    x = np.linspace(params.x_min, params.x_max, params.num_points)
    y_true = np.sin(x)

    produced_figures: list[str] = []

    # Figure 1: overlay approximations for a single center
    center = 0.0
    plt.figure()
    plt.plot(x, y_true, label="sin(x)")
    for d in params.degrees:
        y_approx = taylor_sin(x=x, x0=center, degree=d)
        plt.plot(x, y_approx, label=f"approx degree={d}")
    plt.legend()
    finalize_figure(
        title=f"sin(x) vs polynomial approximations (center={center})",
        xlabel="x",
        ylabel="y",
    )
    fig_name = "fig_01_overview_center_0.png"
    save_figure(artifacts.out_dir / fig_name)
    produced_figures.append(fig_name)

    # Figure set: error curves for each center and degree
    for c in params.centers:
        plt.figure()
        for d in params.degrees:
            y_approx = taylor_sin(x=x, x0=c, degree=d)
            err = np.abs(y_true - y_approx)
            plt.plot(x, err, label=f"deg={d}")
        plt.yscale("log")
        plt.legend()
        finalize_figure(
            title=f"Absolute error |sin(x) - approx(x)| (log-scale), center={c}",
            xlabel="x",
            ylabel="absolute error",
        )
        fig_name = f"fig_02_error_center_{str(c).replace('.', '_')}.png"
        save_figure(artifacts.out_dir / fig_name)
        produced_figures.append(fig_name)

    write_json(artifacts.params_json, {"seed": args.seed, "params": asdict(params)})
    _write_report(artifacts.report_md, params=params, figures=produced_figures)

    return 0


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
