"""Sync experiment snapshots from out/ into docs/params and docs/reports.

This tool copies (or updates) per-experiment snapshot files produced under `out/<slug>/`:

- `params.json`  -> `docs/params/<slug>.json`
- `report.md`    -> `docs/reports/<slug>.md`

It is designed to be **idempotent**:
running it repeatedly should not change files if the inputs have not changed.

In addition to regular experiment slugs like `e001`, this script also syncs a small
set of special slugs (e.g. `experiments_gallery`) if present in `out/`.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

_EXPERIMENT_DIR_RE = re.compile(r"^e\d{3}$")
_SPECIAL_SLUGS: set[str] = {"experiments_gallery"}


@dataclass(frozen=True)
class SyncResult:
    """Result summary for one run."""

    changed: int
    skipped: int
    missing: int


def _parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out-root",
        type=Path,
        default=Path("out"),
        help="Root directory that contains per-experiment output folders (default: out/).",
    )
    parser.add_argument(
        "--docs-root",
        type=Path,
        default=Path("docs"),
        help="Docs root directory containing params/ and reports/ (default: docs/).",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress non-error output.",
    )
    return parser.parse_args()


def _is_valid_slug(name: str) -> bool:
    """Return True if the directory name is an experiment slug we should sync."""
    return bool(_EXPERIMENT_DIR_RE.match(name)) or name in _SPECIAL_SLUGS


def _find_slug_dirs(out_root: Path) -> list[Path]:
    """Find all slug directories under out_root that should be synced.

    Args:
        out_root: Root directory containing per-experiment output subfolders.

    Returns:
        List of directories (paths) sorted by slug name.
    """
    if not out_root.exists():
        return []

    dirs: list[Path] = []
    for p in out_root.iterdir():
        if p.is_dir() and _is_valid_slug(p.name):
            dirs.append(p)

    return sorted(dirs, key=lambda x: x.name)


def _read_text(path: Path) -> str:
    """Read UTF-8 text, replacing invalid bytes."""
    return path.read_text(encoding="utf-8", errors="replace")


def _write_text_if_changed(path: Path, content: str) -> bool:
    """Write text only if content differs.

    Args:
        path: Destination file path.
        content: Text to write.

    Returns:
        True if a write occurred, otherwise False.
    """
    if path.exists():
        existing = _read_text(path)
        if existing == content:
            return False

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    return True


def _read_bytes(path: Path) -> bytes:
    """Read bytes."""
    return path.read_bytes()


def _write_bytes_if_changed(path: Path, data: bytes) -> bool:
    """Write bytes only if data differs."""
    if path.exists():
        existing = _read_bytes(path)
        if existing == data:
            return False

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return True


def _wrap_report(slug: str, report_md: str) -> str:
    """Ensure the report file has a top-level heading.

    This prevents Sphinx/MyST warnings when reports are built as standalone pages.

    Args:
        slug: Experiment slug (e.g. "e001").
        report_md: Raw report markdown from out/<slug>/report.md.

    Returns:
        Markdown content with a leading H1 title.
    """
    stripped = report_md.lstrip()
    if stripped.startswith("# "):
        return report_md

    title = f"# {slug}\n\n"
    auto = f"<!-- AUTO-GENERATED: do not edit manually. Source: out/{slug}/report.md -->\n\n"
    return title + auto + report_md.lstrip("\n")


def _cleanup_legacy_filenames(docs_root: Path, slug: str) -> None:
    """Remove legacy double-extension snapshot files if they exist.

    Older versions of the sync script could produce files like `e001.md.md`.
    Those trigger Sphinx warnings and should not be kept.

    Args:
        docs_root: Docs root directory.
        slug: Experiment slug.
    """
    legacy_report = docs_root / "reports" / f"{slug}.md.md"
    if legacy_report.exists():
        legacy_report.unlink()

    legacy_params = docs_root / "params" / f"{slug}.json.json"
    if legacy_params.exists():
        legacy_params.unlink()


def sync_docs_snapshots(out_root: Path, docs_root: Path, quiet: bool) -> SyncResult:
    """Sync snapshots for all discovered experiment slugs.

    Args:
        out_root: Root directory that contains per-experiment output folders.
        docs_root: Docs root containing params/ and reports/ directories.
        quiet: If True, suppress informational output.

    Returns:
        Summary counters for the run.
    """
    slug_dirs = _find_slug_dirs(out_root)
    if not slug_dirs:
        if not quiet:
            print("No experiment output folders found under:", out_root)
        return SyncResult(changed=0, skipped=0, missing=0)

    changed = 0
    skipped = 0
    missing = 0

    for slug_dir in slug_dirs:
        slug = slug_dir.name
        _cleanup_legacy_filenames(docs_root, slug)

        src_params = slug_dir / "params.json"
        src_report = slug_dir / "report.md"

        if not src_params.exists() or not src_report.exists():
            missing += 1
            if not quiet:
                missing_parts = []
                if not src_params.exists():
                    missing_parts.append("params.json")
                if not src_report.exists():
                    missing_parts.append("report.md")
                print(f"Skipping {slug}: missing {', '.join(missing_parts)} in {slug_dir}")
            continue

        # params.json -> docs/params/<slug>.json
        dst_params = docs_root / "params" / f"{slug}.json"
        did_params = _write_bytes_if_changed(dst_params, _read_bytes(src_params))

        # report.md -> docs/reports/<slug>.md (with H1 wrapper)
        dst_report = docs_root / "reports" / f"{slug}.md"
        wrapped_report = _wrap_report(slug, _read_text(src_report))
        did_report = _write_text_if_changed(dst_report, wrapped_report)

        if did_params or did_report:
            changed += 1
        else:
            skipped += 1

    if not quiet:
        if changed == 0 and missing == 0:
            print("Nothing changed.")
        else:
            print(f"Synced snapshots: changed={changed}, skipped={skipped}, missing={missing}")

    return SyncResult(changed=changed, skipped=skipped, missing=missing)


def main() -> int:
    """CLI entrypoint."""
    args = _parse_args()
    result = sync_docs_snapshots(
        out_root=args.out_root,
        docs_root=args.docs_root,
        quiet=args.quiet,
    )
    # Non-zero exit on missing inputs is usually too strict for local dev.
    # Sphinx will still fail later if required includes are missing.
    return 0 if (result.changed >= 0) else 1


if __name__ == "__main__":
    raise SystemExit(main())
