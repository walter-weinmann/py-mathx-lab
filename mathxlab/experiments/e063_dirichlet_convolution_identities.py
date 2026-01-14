"""E063: Dirichlet convolution identities (computational checks).

Dirichlet convolution is defined by:
    (f*g)(n) = ∑_{d|n} f(d) g(n/d)

Classic identities:
- μ * 1 = ε (inverse of the constant-one function),
- φ = μ * id.

This experiment computes these convolutions on a finite prefix [1..N] and
verifies equality exactly, reporting the first mismatch if any.

Usage (repository convention):
    make run EXP=e063

Artifacts:
    - figures/fig_01_abs_error.png
"""

from __future__ import annotations

from dataclasses import asdict, dataclass

import matplotlib.figure as fig
import matplotlib.pyplot as plt

from mathxlab.exp.cli import parse_experiment_args
from mathxlab.exp.io import prepare_out_dir, save_figure, write_json, write_text
from mathxlab.exp.logging import LoggingConfig
from mathxlab.exp.logging_setup import setup_logging
from mathxlab.exp.run_logging import infer_run_log_file
from mathxlab.exp.seeding import set_global_seed
from mathxlab.nt.arithmetic import build_factor_sieve, compute_mobius, compute_phi
from mathxlab.nt.convolution import dirichlet_convolution, epsilon, identity, ones


# ------------------------------------------------------------------------------
@dataclass(frozen=True)
class Params:
    """Experiment parameters.

    Attributes:
        n_max: Maximum n for convolution.
    """

    n_max: int = 60_000


# ------------------------------------------------------------------------------
def _first_mismatch(a: list[int], b: list[int], n_max: int) -> int | None:
    """Return first index where a and b differ.

    Args:
        a: First list.
        b: Second list.
        n_max: Maximum index to check.

    Returns:
        Index of mismatch or None.
    """
    for n in range(1, n_max + 1):
        if a[n] != b[n]:
            return n
    return None


# ------------------------------------------------------------------------------
def _plot_abs_error(n_max: int, err: list[int]) -> fig.Figure:
    """Plot absolute error |err(n)|.

    Args:
        n_max: Maximum n.
        err: Error values.

    Returns:
        Figure.
    """
    xs = list(range(1, n_max + 1))
    ys = [abs(err[n]) for n in xs]

    f = plt.figure()
    ax = f.add_subplot(1, 1, 1)
    ax.plot(xs, ys, linewidth=0.8)
    ax.set_title("Dirichlet convolution identity check (absolute error)")
    ax.set_xlabel(r"$n$")
    ax.set_ylabel(r"$|\mathrm{error}(n)|$")
    ax.set_xlim(1, n_max)

    if any(y > 0 for y in ys):
        ax.set_yscale("log")
    return f


# ------------------------------------------------------------------------------
def main() -> int:
    """Run the experiment.

    Returns:
        Exit code.
    """
    args = parse_experiment_args(
        experiment_id="e063",
        description="Dirichlet convolution identities: μ*1=ε and φ=μ*id",
    )

    run_log = infer_run_log_file(out_dir=args.out_dir, experiment_slug="e063")
    setup_logging(config=LoggingConfig(verbose=args.verbose, log_file=run_log.log_file))
    set_global_seed(args.seed)

    params = Params()
    paths = prepare_out_dir(out_dir=args.out_dir)

    sieve = build_factor_sieve(params.n_max)
    mu = compute_mobius(params.n_max, sieve=sieve)
    phi = compute_phi(params.n_max, sieve=sieve)

    one = ones(params.n_max)
    eps = epsilon(params.n_max)
    idf = identity(params.n_max)

    conv_mu_one = dirichlet_convolution(mu, one, n_max=params.n_max).values
    conv_mu_id = dirichlet_convolution(mu, idf, n_max=params.n_max).values

    err1 = [0] * (params.n_max + 1)
    err2 = [0] * (params.n_max + 1)
    for n in range(1, params.n_max + 1):
        err1[n] = conv_mu_one[n] - eps[n]
        err2[n] = conv_mu_id[n] - phi[n]

    m1 = _first_mismatch(conv_mu_one, eps, params.n_max)
    m2 = _first_mismatch(conv_mu_id, phi, params.n_max)

    fig1 = _plot_abs_error(params.n_max, err1)
    save_figure(out_dir=paths.figures_dir, name="fig_01_abs_error", fig=fig1)

    lines: list[str] = []
    lines.append("# E063: Dirichlet convolution identities")
    lines.append("")
    lines.append(f"- n_max: {params.n_max}")
    lines.append("")
    lines.append("Checks:")
    lines.append(f"- μ * 1 = ε : {'OK' if m1 is None else f'FAIL at n={m1}'}")
    lines.append(f"- μ * id = φ : {'OK' if m2 is None else f'FAIL at n={m2}'}")
    lines.append("")
    lines.append("Figure:")
    lines.append("- fig_01_abs_error.png")
    lines.append("")

    write_json(paths.params_path, asdict(params))
    write_text(paths.report_path, "\n".join(lines), encoding="utf-8")
    return 0
