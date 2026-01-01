"""Validate documentation tags against docs/tags.md.

This module provides a small, dependency-free validation helper that can be run
in CI and locally. It checks that:

1) Every experiment page in docs/experiments/e*.md has a '**Tags:**' line.
2) Every tag listed there is defined in docs/tags.md.
3) The gallery (docs/experiments/experiments_gallery.md) only uses allowed tags
   and only uses the allowed tag format.

Usage:
    python -m tools.validate_doc_tags

The exit code is non-zero if validation fails.
"""

from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

_TAG_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")


@dataclass(frozen=True)
class TagValidationResult:
    """Holds validation results for documentation tags.

    Attributes:
        missing_tags_line: Experiment pages missing a '**Tags:**' line.
        unknown_tags: Mapping of page -> list of tags not present in docs/tags.md.
        gallery_unknown_tags: Tags used in the gallery that are not allowed.
        gallery_invalid_format: Tags used in the gallery that do not match the tag format.
        allowed_tags: The allowed tag set parsed from docs/tags.md.
    """

    missing_tags_line: list[Path]
    unknown_tags: dict[Path, list[str]]
    gallery_unknown_tags: list[str]
    gallery_invalid_format: list[str]
    allowed_tags: set[str]


def _iter_markdown_table_rows(lines: Iterable[str]) -> Iterable[str]:
    """Yield raw Markdown table rows.

    Args:
        lines: Lines of a Markdown file.

    Yields:
        Lines that look like Markdown table rows (start with '|').
    """
    for line in lines:
        if line.lstrip().startswith("|"):
            yield line.rstrip("\n")


def _parse_allowed_tags_from_tags_md(tags_md_path: Path) -> set[str]:
    """Parse allowed tags from docs/tags.md.

    This function extracts the first column of Markdown tables and returns
    tokens that look like tags, i.e., match ``^[a-z0-9][a-z0-9-]*$``.

    Args:
        tags_md_path: Path to docs/tags.md.

    Returns:
        Set of allowed tag strings.
    """
    text = tags_md_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    allowed: set[str] = set()
    header_seen = False
    align_seen = False

    for row in _iter_markdown_table_rows(lines):
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue

        if not header_seen:
            header_seen = True
            align_seen = False
            continue

        if header_seen and not align_seen:
            # Alignment row: consists mainly of ':' and '-' in each cell.
            if all(set(c) <= set(":-") and c for c in cells):
                align_seen = True
            continue

        if header_seen and align_seen:
            first_col = cells[0]
            m = re.fullmatch(r"`([^`]+)`", first_col)
            candidate = (m.group(1) if m else first_col).strip()
            if _TAG_RE.fullmatch(candidate):
                allowed.add(candidate)

    return allowed


def _extract_tags_line(md_text: str) -> str | None:
    """Extract the raw '**Tags:**' line from an experiment page.

    Args:
        md_text: Markdown page content.

    Returns:
        The tags line (full line) if found, otherwise None.
    """
    for line in md_text.splitlines():
        if line.strip().startswith("**Tags:**"):
            return line.strip()
    return None


def _parse_tags_from_tags_line(tags_line: str) -> list[str]:
    """Parse tags from a '**Tags:**' line.

    The canonical format is:
        **Tags:** `tag-a`, `tag-b`, `tag-c`

    Args:
        tags_line: The line that starts with '**Tags:**'.

    Returns:
        List of parsed tag strings.
    """
    tags = re.findall(r"`([^`]+)`", tags_line)
    return [t.strip() for t in tags if t.strip()]


def _extract_gallery_tags(gallery_text: str) -> list[str]:
    """Extract tag tokens used in the experiments gallery.

    This scans several common patterns:
    - data-tags="tag1,tag2"
    - data-tag="tag"
    - visible tag pills like: <span class="... tag ...">tag</span>
    - backticked tokens: `tag`

    Args:
        gallery_text: Markdown/HTML content of experiments_gallery.md.

    Returns:
        List of raw tag strings found (not filtered by regex).
    """
    found: list[str] = []

    for m in re.finditer(r'data-tags\s*=\s*"([^"]+)"', gallery_text):
        raw = m.group(1)
        parts = re.split(r"[\s,]+", raw)
        found.extend([p.strip() for p in parts if p.strip()])

    for m in re.finditer(r'data-tag\s*=\s*"([^"]+)"', gallery_text):
        found.append(m.group(1).strip())

    for m in re.finditer(
        r'<[^>]*class="[^"]*\btag\b[^"]*"[^>]*>([^<]+)</',
        gallery_text,
        flags=re.IGNORECASE,
    ):
        found.append(m.group(1).strip())

    for m in re.finditer(r"`([^`]+)`", gallery_text):
        tag = m.group(1).strip()
        # Filter out experiment IDs like e106, e013, etc.
        if not re.fullmatch(r"e\d{3,4}", tag):
            found.append(tag)

    return [t for t in found if t]


def _format_failure(result: TagValidationResult) -> str:
    """Format validation failures as a readable multiline string."""
    lines: list[str] = []

    if result.missing_tags_line:
        lines.append("Experiment pages missing a '**Tags:**' line:")
        for p in result.missing_tags_line:
            lines.append(f"  - {p.as_posix()}")
        lines.append("")

    if result.unknown_tags:
        lines.append("Experiment pages using unknown tags:")
        for p, tags in sorted(result.unknown_tags.items(), key=lambda x: x[0].as_posix()):
            lines.append(f"  - {p.as_posix()}: {', '.join(tags)}")
        lines.append("")

    if result.gallery_unknown_tags:
        lines.append("Gallery uses unknown tags:")
        lines.append(f"  - {', '.join(result.gallery_unknown_tags)}")
        lines.append("")

    if result.gallery_invalid_format:
        lines.append("Gallery uses tags with invalid format (expected lowercase [a-z0-9-]):")
        lines.append(f"  - {', '.join(result.gallery_invalid_format)}")
        lines.append("")

    return "\n".join(lines).rstrip()


def validate_doc_tags(repo_root: Path) -> TagValidationResult:
    """Validate tags used in docs against docs/tags.md.

    Args:
        repo_root: Repository root directory (contains docs/).

    Returns:
        TagValidationResult with details.
    """
    docs_dir = repo_root / "docs"
    tags_md_path = docs_dir / "tags.md"
    experiments_dir = docs_dir / "experiments"
    gallery_path = experiments_dir / "experiments_gallery.md"

    allowed = _parse_allowed_tags_from_tags_md(tags_md_path)

    missing_tags_line: list[Path] = []
    unknown_tags: dict[Path, list[str]] = {}

    for md_path in sorted(experiments_dir.glob("e[0-9]*.md")):
        md_text = md_path.read_text(encoding="utf-8")
        tags_line = _extract_tags_line(md_text)
        if tags_line is None:
            missing_tags_line.append(md_path)
            continue

        page_tags = _parse_tags_from_tags_line(tags_line)
        page_unknown = sorted({t for t in page_tags if t not in allowed})
        if page_unknown:
            unknown_tags[md_path] = page_unknown

    gallery_unknown: list[str] = []
    gallery_invalid_format: list[str] = []

    if gallery_path.exists():
        gallery_text = gallery_path.read_text(encoding="utf-8")
        used_gallery_tags = sorted(set(_extract_gallery_tags(gallery_text)))
        gallery_invalid_format = sorted([t for t in used_gallery_tags if not _TAG_RE.fullmatch(t)])
        gallery_unknown = sorted(
            [t for t in used_gallery_tags if _TAG_RE.fullmatch(t) and t not in allowed]
        )

    return TagValidationResult(
        missing_tags_line=missing_tags_line,
        unknown_tags=unknown_tags,
        gallery_unknown_tags=gallery_unknown,
        gallery_invalid_format=gallery_invalid_format,
        allowed_tags=allowed,
    )


def main() -> int:
    """CLI entrypoint.

    Returns:
        Process exit code (0 on success, 1 on failure).
    """
    repo_root = Path(__file__).resolve().parents[2]
    result = validate_doc_tags(repo_root)

    ok = (
        not result.missing_tags_line
        and not result.unknown_tags
        and not result.gallery_unknown_tags
        and not result.gallery_invalid_format
    )
    if ok:
        print("OK: docs tags validated.")
        return 0

    print(_format_failure(result))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
