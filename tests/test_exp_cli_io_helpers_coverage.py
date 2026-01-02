"""Coverage-focused tests for CLI/IO/helpers utilities.

These tests intentionally hit error/branch paths to keep coverage stable while
remaining fast (no full experiment runs).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from mathxlab.exp.cli import parse_experiment_args, parse_experiment_args_with_size
from mathxlab.exp.io import json_default
from mathxlab.plots.helpers import apply_axis_style, finalize_figure


def test_parse_experiment_args_rejects_multiple_positional_lists() -> None:
    """parse_experiment_args should reject multiple positional arg lists."""
    with pytest.raises(TypeError):
        parse_experiment_args(["--out", "out/e001"], ["--seed", "1"])


def test_parse_experiment_args_rejects_non_list_non_none() -> None:
    """parse_experiment_args should reject non-list positional args."""
    with pytest.raises(TypeError):
        parse_experiment_args(123)


def test_parse_experiment_args_accepts_list() -> None:
    """parse_experiment_args should accept a positional list."""
    args = parse_experiment_args(["--out", "out/e001", "--seed", "1"])
    assert args.out_dir.name == "e001"
    assert args.seed == 1


def test_parse_experiment_args_with_size_validates_odd_positive() -> None:
    """parse_experiment_args_with_size enforces odd positive size."""
    with pytest.raises(SystemExit):
        parse_experiment_args_with_size(["--out", "out/e001", "--size", "-1"])

    with pytest.raises(SystemExit):
        parse_experiment_args_with_size(["--out", "out/e001", "--size", "10"])

    args = parse_experiment_args_with_size(["--out", "out/e001", "--size", "11"])
    assert args.size == 11


def test_json_default_supported_types() -> None:
    """json_default should handle common numeric/path types."""
    assert json_default(complex(1.5, -2.25)) == {"real": 1.5, "imag": -2.25}
    assert json_default(np.int64(7)) == 7
    assert json_default(np.float64(1.25)) == 1.25
    assert json_default(np.array([1, 2, 3], dtype=np.int64)) == [1, 2, 3]

    p = Path("x/y/z")
    # json_default uses str(Path), which is OS-dependent (\ on Windows, / on POSIX).
    assert json_default(p) == str(p)


def test_json_default_rejects_unknown_type() -> None:
    """json_default should raise TypeError for unsupported types."""

    class _Nope:
        pass

    with pytest.raises(TypeError):
        json_default(_Nope())


def test_apply_axis_style_sets_equal_aspect() -> None:
    """apply_axis_style should be able to set equal aspect."""
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    apply_axis_style(ax=ax, title="T", xlab="X", ylab="Y", equal=True)
    assert ax.get_title() == "T"
    assert ax.get_xlabel() == "X"
    assert ax.get_ylabel() == "Y"
    # For 'equal', Matplotlib returns 1.0 for the aspect ratio.
    assert ax.get_aspect() == 1.0
    plt.close(fig)


def test_finalize_figure_handles_tight_layout_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    """finalize_figure should not crash if tight_layout fails."""
    import matplotlib.pyplot as plt

    fig, _ax = plt.subplots()

    def _boom(*_args: object, **_kwargs: object) -> None:
        raise ValueError("boom")

    monkeypatch.setattr(fig, "tight_layout", _boom)
    finalize_figure(fig=fig)
    plt.close(fig)
