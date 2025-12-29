"""Tests for experiment CLI helpers."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from mathxlab.exp.cli import parse_experiment_args


def test_parse_experiment_args_accepts_keyword_argv(tmp_path: Path) -> None:
    """Parse args via keyword argv."""
    args = parse_experiment_args(argv=["--out", str(tmp_path)])
    assert args.out_dir == tmp_path
    assert args.seed == 1
    assert args.verbose is False


def test_parse_experiment_args_accepts_positional_list_argv(tmp_path: Path) -> None:
    """Parse args via positional argv list."""
    args = parse_experiment_args(["--out", str(tmp_path), "--seed", "7", "--verbose"])
    assert args.out_dir == tmp_path
    assert args.seed == 7
    assert args.verbose is True


def test_parse_experiment_args_accepts_positional_none(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Positional ``None`` should be accepted (argv taken from ``sys.argv``).

    This function is intentionally flexible: some experiments call
    ``parse_experiment_args(argv)``, others call ``parse_experiment_args(argv=...)``.
    Passing ``None`` positionally should behave like omitting ``argv`` entirely.

    Args:
        tmp_path: Temporary directory provided by pytest.
        monkeypatch: Pytest fixture to patch globals safely.
    """
    monkeypatch.setattr(sys, "argv", ["prog", "--out", str(tmp_path)])
    args = parse_experiment_args(None)
    assert args.out_dir == tmp_path


def test_parse_experiment_args_rejects_argv_given_twice(tmp_path: Path) -> None:
    """Passing argv both positionally and via keyword should raise TypeError."""
    with pytest.raises(TypeError, match="both positionally and as a keyword"):
        _ = parse_experiment_args(None, argv=["--out", str(tmp_path)])


def test_parse_experiment_args_rejects_multiple_positional_args() -> None:
    """More than one positional argument should raise TypeError."""
    with pytest.raises(TypeError, match="at most one positional"):
        _ = parse_experiment_args([], [])


def test_parse_experiment_args_rejects_bad_positional_type() -> None:
    """A non-list/tuple positional argv should raise TypeError."""
    with pytest.raises(TypeError, match="positional argv must be"):
        _ = parse_experiment_args(123)
