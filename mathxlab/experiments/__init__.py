"""Experiment package.

Experiments are organized as importable modules, e.g.:

    uv run python -m mathxlab.experiments.e001

This package also exposes a small, stable registry so other tooling (CLI / docs
builders) can enumerate available experiments without importing every module.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ExperimentSpec:
    """Lightweight metadata about an experiment.

    Args:
        experiment_id: The experiment id, e.g. "e001".
        title: Human-readable title (used in listings).
        module: Import path of the experiment entry point module.
    """

    experiment_id: str
    title: str
    module: str


# Keep this list in sync with files under `mathxlab/experiments/`.
_EXPERIMENTS: tuple[ExperimentSpec, ...] = (
    ExperimentSpec(
        experiment_id="e001",
        title="Taylor Error Landscapes",
        module="mathxlab.experiments.e001",
    ),
    ExperimentSpec(
        experiment_id="e002",
        title="Even Perfect Numbers — Generator and Growth",
        module="mathxlab.experiments.e002",
    ),
    ExperimentSpec(
        experiment_id="e003",
        title="Abundancy Index Landscape",
        module="mathxlab.experiments.e003",
    ),
    ExperimentSpec(
        experiment_id="e004",
        title="Computing σ(n) at Scale — Sieve vs. Factorization",
        module="mathxlab.experiments.e004",
    ),
    ExperimentSpec(
        experiment_id="e005",
        title="Odd Perfect Numbers — Constraint Filter Pipeline",
        module="mathxlab.experiments.e005",
    ),
    ExperimentSpec(
        experiment_id="e006",
        title="Near Misses to Perfection",
        module="mathxlab.experiments.e006",
    ),
)


def iter_experiments() -> Iterable[ExperimentSpec]:
    """Iterate over known experiments.

    Returns:
        An iterable of ExperimentSpec items in ascending experiment id order.
    """
    return _EXPERIMENTS


def list_experiment_ids() -> tuple[str, ...]:
    """Return all known experiment ids.

    Returns:
        Tuple of ids like ("e001", "e002", ...).
    """
    return tuple(e.experiment_id for e in _EXPERIMENTS)


def get_experiment_module(experiment_id: str) -> str:
    """Return the module import path for a given experiment id.

    Args:
        experiment_id: The experiment id, e.g. "e003".

    Returns:
        The module import path, e.g. "mathxlab.experiments.e003".

    Raises:
        KeyError: If the experiment id is unknown.
    """
    for e in _EXPERIMENTS:
        if e.experiment_id == experiment_id:
            return e.module
    raise KeyError(f"Unknown experiment id: {experiment_id!r}")


__all__ = [
    "ExperimentSpec",
    "get_experiment_module",
    "iter_experiments",
    "list_experiment_ids",
]
