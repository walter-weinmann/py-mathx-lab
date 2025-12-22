from pathlib import Path

import pytest

from mathxlab.exp.cli import ExperimentArgs, parse_experiment_args


def test_parse_experiment_args_valid() -> None:
    argv = ["--out", "out/e001", "--seed", "42"]
    args = parse_experiment_args(argv=argv)
    assert isinstance(args, ExperimentArgs)
    assert args.out_dir == Path("out/e001")
    assert args.seed == 42


def test_parse_experiment_args_default_seed() -> None:
    argv = ["--out", "out/e001"]
    args = parse_experiment_args(argv=argv)
    assert args.seed == 1


def test_parse_experiment_args_missing_required() -> None:
    # argparse will call sys.exit() on error, which raises SystemExit
    with pytest.raises(SystemExit):
        parse_experiment_args(argv=[])


def test_parse_experiment_args_help() -> None:
    with pytest.raises(SystemExit):
        parse_experiment_args(argv=["--help"])
