"""Update the experiment status Markdown page by appending missing experiments.

The status page is expected at `docs/experiment_status.md` and contains a
Markdown table with columns:

| Experiment | Generated | Last edited | Notes |

This script:
- Scans `mathxlab/experiments` for implementation modules `e###_*.py`.
- Parses ALL matching status tables in the document (robust to different
  separator styles like |---| or |-----|).
- Merges rows into a single table (first occurrence wins, preserving manual edits).
- Removes redundant duplicate tables from the document.
- Appends rows for newly discovered experiments not yet present in the merged table.
- Does NOT remove rows that no longer exist on disk (to preserve manual history).
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

_RE_EXPERIMENT_IMPL = re.compile(r"^e\d{3}_.+\.py$")
_RE_ROW = re.compile(
    r"^\|\s*(?P<c1>[^|]+?)\s*\|\s*(?P<c2>[^|]*)\|\s*(?P<c3>[^|]*)\|\s*(?P<c4>[^|]*)\|\s*$"
)
_RE_HEADER = re.compile(
    r"^\|\s*Experiment\s*\|\s*Generated\s*\|\s*Last edited\s*\|\s*Notes\s*\|\s*$",
    re.IGNORECASE,
)
_RE_SEPARATOR = re.compile(r"^\|\s*:?-+:?\s*\|\s*:?-+:?\s*\|\s*:?-+:?\s*\|\s*:?-+:?\s*\|\s*$")


@dataclass(frozen=True, slots=True)
class StatusRow:
    """A single row in the experiment status table."""

    experiment: str
    generated: str
    last_edited: str
    notes: str

    def to_markdown_row(self) -> str:
        """Render as a Markdown table row."""
        return f"| {self.experiment} | {self.generated} | {self.last_edited} | {self.notes} |"


def _collect_experiment_names(experiments_dir: Path) -> list[str]:
    """Collect experiment implementation module stems from a directory."""
    if not experiments_dir.is_dir():
        raise FileNotFoundError(f"Experiments directory not found: {experiments_dir}")

    names: list[str] = []
    for path in experiments_dir.iterdir():
        if not path.is_file():
            continue
        if path.suffix != ".py":
            continue
        if not _RE_EXPERIMENT_IMPL.match(path.name):
            continue
        names.append(path.stem)

    names.sort()
    return names


def _find_all_status_tables(lines: list[str]) -> list[tuple[int, int]]:
    """Find all status tables in the document.

    A status table is recognized by:
    - a header row containing the 4 expected column titles
    - a separator row (any dash length, optional colons)
    - followed by one or more `| ... | ... | ... | ... |` rows (possibly zero rows)

    Returns:
        List of (start_index, end_index) tuples (end exclusive) for each table.
    """
    tables: list[tuple[int, int]] = []
    i = 0
    while i < len(lines) - 1:
        if _RE_HEADER.match(lines[i].strip()) and _RE_SEPARATOR.match(lines[i + 1].strip()):
            start = i
            j = i + 2
            while j < len(lines) and lines[j].lstrip().startswith("|"):
                j += 1
            tables.append((start, j))
            i = j
            continue
        i += 1
    return tables


def _parse_rows(table_lines: list[str]) -> dict[str, StatusRow]:
    """Parse status rows from a table block (including header + separator)."""
    rows: dict[str, StatusRow] = {}
    for line in table_lines[2:]:
        m = _RE_ROW.match(line.strip())
        if not m:
            continue
        exp = m.group("c1").strip()
        if not exp or exp.lower() == "experiment":
            continue
        rows[exp] = StatusRow(
            experiment=exp,
            generated=m.group("c2").strip(),
            last_edited=m.group("c3").strip(),
            notes=m.group("c4").strip(),
        )
    return rows


def _ensure_doc_exists(text: str) -> list[str]:
    """Ensure we have a document skeleton if file is missing/empty."""
    if text.strip():
        return text.splitlines()
    return [
        "# Experiment Status",
        "",
        "This page tracks the generation and manual editing status of experiment pages.",
        "",
        "| Experiment | Generated | Last edited | Notes |",
        "|---|---|---|---|",
        "",
    ]


def main() -> None:
    """Update `docs/experiment_status.md` by merging tables and appending new experiments."""
    repo_root = Path(__file__).resolve().parents[2]
    experiments_dir = repo_root / "mathxlab" / "experiments"
    doc_path = repo_root / "docs" / "experiment_status.md"

    generated_date = "31.12.2025"

    existing_text = doc_path.read_text(encoding="utf-8") if doc_path.exists() else ""
    lines = _ensure_doc_exists(existing_text)

    tables = _find_all_status_tables(lines)

    if not tables:
        # Insert a table at the end if none exists.
        if lines and lines[-1].strip() != "":
            lines.append("")
        lines.extend(
            [
                "| Experiment | Generated | Last edited | Notes |",
                "|:---|:---|:---|:---|",
            ]
        )
        tables = _find_all_status_tables(lines)

    if not tables:
        raise RuntimeError("Failed to locate or insert a status table.")

    # Merge all parsed rows: first occurrence wins (preserve manual edits).
    merged_rows: dict[str, StatusRow] = {}
    header_line = lines[tables[0][0]]
    sep_line = lines[tables[0][0] + 1]

    for start, end in tables:
        rows = _parse_rows(lines[start:end])
        for exp, row in rows.items():
            if exp not in merged_rows:
                merged_rows[exp] = row

    # Discover experiments and add missing ones.
    discovered = _collect_experiment_names(experiments_dir)
    for exp in discovered:
        if exp not in merged_rows:
            merged_rows[exp] = StatusRow(exp, generated_date, "", "")

    # Keep stable ordering.
    ordered = sorted(merged_rows.values(), key=lambda r: r.experiment)

    # Rebuild a SINGLE table where the first table was, remove the others.
    first_start, _first_end = tables[0]
    new_table_lines = [header_line.strip(), sep_line.strip()]
    new_table_lines.extend([r.to_markdown_row() for r in ordered])

    # Delete all table blocks (from back to front), then insert the rebuilt one.
    for start, end in reversed(tables):
        del lines[start:end]

    # Insert rebuilt table at original location of first table.
    lines[first_start:first_start] = new_table_lines

    out_text = "\n".join(lines).rstrip() + "\n"
    doc_path.parent.mkdir(parents=True, exist_ok=True)
    doc_path.write_text(out_text, encoding="utf-8")


if __name__ == "__main__":
    main()
