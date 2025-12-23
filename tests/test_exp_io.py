import json
from pathlib import Path

import matplotlib.figure

from mathxlab.exp.io import RunPaths, prepare_out_dir, save_figure, write_json


def test_prepare_out_dir(tmp_path: Path) -> None:
    out_dir = tmp_path / "out"
    paths = prepare_out_dir(out_dir=out_dir)

    assert isinstance(paths, RunPaths)
    assert paths.root == out_dir
    assert paths.figures_dir == out_dir / "figures"
    assert paths.report_path == out_dir / "report.md"
    assert paths.params_path == out_dir / "params.json"
    assert paths.figures_dir.exists()


def test_save_figure(tmp_path: Path) -> None:
    out_dir = tmp_path / "figs"
    fig = matplotlib.figure.Figure()

    saved_path = save_figure(out_dir=out_dir, name="test_plot", fig=fig)

    assert saved_path == out_dir / "test_plot.png"
    assert saved_path.exists()


def test_write_json(tmp_path: Path) -> None:
    json_path = tmp_path / "data.json"
    data = {"z": 10, "a": 5}

    write_json(json_path, data)

    assert json_path.exists()
    content = json_path.read_text(encoding="utf-8")
    expected_content = json.dumps(data, indent=2, sort_keys=True) + "\n"
    assert content == expected_content
