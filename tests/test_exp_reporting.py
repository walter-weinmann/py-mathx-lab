import json

import matplotlib.pyplot as plt
import pytest

from mathxlab.exp.reporting import RunArtifacts, prepare_out_dir, save_figure, write_json


def test_prepare_out_dir(tmp_path_factory: pytest.TempPathFactory) -> None:
    out_dir = tmp_path_factory.mktemp("out")
    artifacts = prepare_out_dir(out_dir)

    assert isinstance(artifacts, RunArtifacts)
    assert artifacts.out_dir == out_dir
    assert artifacts.report_md == out_dir / "report.md"
    assert artifacts.params_json == out_dir / "params.json"
    assert out_dir.exists()


def test_save_figure(tmp_path_factory: pytest.TempPathFactory) -> None:
    out_dir = tmp_path_factory.mktemp("figures")
    fig_path = out_dir / "test_fig.png"
    plt.figure()
    plt.plot([0, 1], [0, 1])

    save_figure(fig_path)

    assert fig_path.exists()
    assert fig_path.is_file()


def test_write_json(tmp_path_factory: pytest.TempPathFactory) -> None:
    out_dir = tmp_path_factory.mktemp("data")
    json_path = out_dir / "test.json"
    data = {"b": 2, "a": 1}

    write_json(json_path, data)

    assert json_path.exists()
    content = json_path.read_text(encoding="utf-8")
    # Check for stable formatting (sorted keys, indent=2)
    expected_content = json.dumps(data, indent=2, sort_keys=True) + "\n"
    assert content == expected_content
