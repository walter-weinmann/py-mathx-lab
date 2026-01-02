"""Sync experiment run snapshots into the documentation tree.

This repository generates per-run artifacts under ``out/e###/`` (figures, params,
report, logs). For a clean VCS history, it is often preferable to *publish* the
stable textual artifacts (``params.json`` and ``report.md``) inside ``docs/``
instead of committing the entire ``out/`` tree.

This tool copies (in a deterministic, idempotent way):

- ``out/e###/params.json`` -> ``docs/params/e###.json``
- ``out/e###/report.md``  -> ``docs/reports/e###.md``

Idempotency goals:

- Re-running the tool with the same source inputs causes no filesystem changes.
- JSON is normalized for stable diffs (sorted keys, consistent indentation).
- Text files are normalized to LF newlines and end with a trailing newline.

Typical usage:

    uv run --extra dev python -m mathxlab.tools.sync_docs_snapshots --overwrite

"""

from __future__ import annotations

import argparse
import json
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class SyncResult:
    """Result of syncing one experiment."""

    experiment_slug: str
    copied_params: bool
    copied_report: bool


def _iter_experiment_slugs(out_root: Path) -> list[str]:
    """Discover experiment slugs under an ``out`` directory.

    Args:
        out_root: Root output directory (usually ``out``).

    Returns:
        Sorted list of experiment slugs like ``["e001", "e002", ...]``.
    """
    if not out_root.exists():
        return []

    slugs: list[str] = []
    for p in out_root.iterdir():
        if not p.is_dir():
            continue
        name = p.name.lower()
        if len(name) == 4 and name[0] == "e" and name[1:].isdigit():
            slugs.append(name)
    return sorted(slugs)


def _normalize_newlines(text: str) -> str:
    """Normalize newlines to LF and ensure a trailing newline.

    Args:
        text: Input text.

    Returns:
        Normalized text.
    """
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    if not normalized.endswith("\n"):
        normalized += "\n"
    return normalized


def _write_text_if_changed(path: Path, text: str, *, overwrite: bool) -> bool:
    """Write text to a file only if the content differs.

    Args:
        path: Destination file path.
        text: Text content to write.
        overwrite: Whether to overwrite an existing destination file.

    Returns:
        True if the file was created/updated, otherwise False.
    """
    if path.exists() and not overwrite:
        return False

    path.parent.mkdir(parents=True, exist_ok=True)
    new_bytes = text.encode("utf-8")

    if path.exists():
        old_bytes = path.read_bytes()
        if old_bytes == new_bytes:
            return False

    path.write_bytes(new_bytes)
    return True


def _render_params_json(src: Path) -> str:
    """Render ``params.json`` deterministically.

    The function attempts to parse JSON and re-dump it in a canonical form.
    If parsing fails, it falls back to raw file content (newline-normalized).

    Args:
        src: Source ``params.json`` path.

    Returns:
        Canonical JSON text.
    """
    raw = src.read_text(encoding="utf-8")
    try:
        obj = json.loads(raw)
    except json.JSONDecodeError:
        return _normalize_newlines(raw)

    rendered = json.dumps(
        obj,
        ensure_ascii=False,
        sort_keys=True,
        indent=2,
    )
    return _normalize_newlines(rendered)


def _render_report_md(src: Path) -> str:
    """Render ``report.md`` deterministically.

    Args:
        src: Source ``report.md`` path.

    Returns:
        Normalized markdown text.
    """
    return _normalize_newlines(src.read_text(encoding="utf-8"))


def sync_one(
    *,
    out_root: Path,
    docs_root: Path,
    experiment_slug: str,
    overwrite: bool,
) -> SyncResult:
    """Sync snapshots for a single experiment.

    Args:
        out_root: Root output directory (usually ``out``).
        docs_root: Documentation root directory (usually ``docs``).
        experiment_slug: Experiment slug like ``e013``.
        overwrite: Whether to overwrite existing snapshot files.

    Returns:
        A ``SyncResult`` describing what was copied.
    """
    out_dir = out_root / experiment_slug
    src_params = out_dir / "params.json"
    src_report = out_dir / "report.md"

    dst_params = docs_root / "params" / f"{experiment_slug}.json"
    dst_report = docs_root / "reports" / f"{experiment_slug}.md"

    copied_params = False
    if src_params.exists():
        params_text = _render_params_json(src_params)
        copied_params = _write_text_if_changed(dst_params, params_text, overwrite=overwrite)

    copied_report = False
    if src_report.exists():
        report_text = _render_report_md(src_report)
        copied_report = _write_text_if_changed(dst_report, report_text, overwrite=overwrite)

    return SyncResult(
        experiment_slug=experiment_slug,
        copied_params=copied_params,
        copied_report=copied_report,
    )


def sync_many(
    *,
    out_root: Path,
    docs_root: Path,
    experiment_slugs: Iterable[str],
    overwrite: bool,
) -> list[SyncResult]:
    """Sync snapshots for multiple experiments.

    Args:
        out_root: Root output directory (usually ``out``).
        docs_root: Documentation root directory (usually ``docs``).
        experiment_slugs: Iterable of experiment slugs like ``["e001", ...]``.
        overwrite: Whether to overwrite existing snapshot files.

    Returns:
        List of results in the input order.
    """
    return [
        sync_one(out_root=out_root, docs_root=docs_root, experiment_slug=slug, overwrite=overwrite)
        for slug in experiment_slugs
    ]


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    """Parse CLI arguments.

    Args:
        argv: Optional argv list, excluding the program name.

    Returns:
        Parsed argument namespace.
    """
    parser = argparse.ArgumentParser(
        prog="sync_docs_snapshots",
        description="Sync out/e### snapshots (params.json + report.md) into docs/.",
    )
    parser.add_argument(
        "--out-root",
        type=Path,
        default=Path("out"),
        help="Root output directory (default: out).",
    )
    parser.add_argument(
        "--docs-root",
        type=Path,
        default=Path("docs"),
        help="Documentation root directory (default: docs).",
    )
    parser.add_argument(
        "--ids",
        type=str,
        default="",
        help=(
            "Comma-separated experiment ids to sync (e.g. e013,e024). "
            "If empty, auto-discover under out-root."
        ),
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing snapshot files in docs/.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """CLI entry point.

    Args:
        argv: Optional argv list, excluding the program name.

    Returns:
        Process exit code (0 for success).
    """
    ns = _parse_args(argv)
    out_root: Path = ns.out_root
    docs_root: Path = ns.docs_root
    overwrite: bool = bool(ns.overwrite)

    if ns.ids:
        slugs = [s.strip().lower() for s in str(ns.ids).split(",") if s.strip()]
    else:
        slugs = _iter_experiment_slugs(out_root)

    if not slugs:
        print(f"No experiments found under: {out_root}")
        return 0

    results = sync_many(
        out_root=out_root,
        docs_root=docs_root,
        experiment_slugs=slugs,
        overwrite=overwrite,
    )

    copied_any = False
    for r in results:
        if r.copied_params or r.copied_report:
            copied_any = True
        status = []
        status.append("params" if r.copied_params else "-")
        status.append("report" if r.copied_report else "-")
        print(f"{r.experiment_slug}: {', '.join(status)}")

    if not copied_any:
        print("Nothing changed (already up to date, files missing, or overwrite disabled).")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
