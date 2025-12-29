"""Tests for experiment CLI helpers."""

from __future__ import annotations

from pathlib import Path

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


def test_parse_experiment_args_accepts_positional_none(tmp_path: Path) -> None:
    """Positional None should be accepted (argv taken from sys.argv).

    We can't reliably assert sys.argv contents here, but we *can* assert
    that passing None positionally does not raise TypeError.
    """
    # We pass a minimal argv via keyword to ensure parser doesn't exit;
    # the goal is to ensure positional None is accepted, not to parse from sys.argv.
    args = parse_experiment_args(None, argv=["--out", str(tmp_path)])
    assert args.out_dir == tmp_path
