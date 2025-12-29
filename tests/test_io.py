"""Tests for experiment output helpers."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

from mathxlab.exp.io import prepare_out_dir, save_figure, write_json, write_text


def test_prepare_out_dir_creates_structure(tmp_path: Path) -> None:
    """prepare_out_dir should create figures directory and return standard paths."""
    paths = prepare_out_dir(out_dir=tmp_path)
    assert paths.root == tmp_path
    assert paths.figures_dir.exists()
    assert paths.figures_dir.is_dir()
    assert paths.report_path.name == "report.md"
    assert paths.params_path.name == "params.json"


def test_save_figure_writes_png(tmp_path: Path) -> None:
    """save_figure should write a PNG file."""
    paths = prepare_out_dir(out_dir=tmp_path)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot([0, 1], [0, 1])
    ax.set_title("Smoke figure")

    out_path = save_figure(out_dir=paths.figures_dir, name="fig_test", fig=fig, finalize=True)
    assert out_path.exists()
    assert out_path.suffix == ".png"


def test_write_json_and_text(tmp_path: Path) -> None:
    """write_json and write_text should write UTF-8 files."""
    json_path = tmp_path / "x.json"
    txt_path = tmp_path / "x.md"

    write_json(json_path, {"b": 2, "a": 1})
    assert json_path.read_text(encoding="utf-8").strip().startswith("{")

    write_text(txt_path, "hello\n", encoding="utf-8")
    assert txt_path.read_text(encoding="utf-8") == "hello\n"
