# Copyright (c) 2022-2025 IO-Swiss Aero GmbH. All rights reserved.
# Use of this source code is governed by the IO-Swiss Aero GmbH
# License, that can be found in the LICENSE.md file.

"""Verify GitHub Wiki markdown content stored under a repo folder.

This module is intentionally dependency-free so it can run in CI and locally via:

    uv run --extra dev python -m mathxlab.tools.verify_wiki --wiki-dir wiki

What it checks (default):
- The wiki directory exists.
- `Home.md` exists (GitHub Wiki front page).
- Each `*.md` page contains an H1 heading (`# ...`).
- Internal links and image links point to existing local files.
  - Wiki page links may be written as `(Page-Name)` or `(Page-Name.md)`.
  - Links may include anchors like `(Page-Name#section)`; anchors are ignored by default.

It does *not* attempt to render markdown. The goal is to catch obvious structural issues
(broken links, missing pages) early, before publishing the wiki.

Exit codes:
- 0: OK (or only warnings when --fail-on-warnings is not set)
- 2: Errors found
- 3: Warnings found and --fail-on-warnings is set
"""

from __future__ import annotations

import argparse
import re
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote

_MD_LINK_RE = re.compile(r"""(?<!\!)\[[^\]]*\]\(([^)]+)\)""")
_MD_IMAGE_RE = re.compile(r"""!\[[^\]]*\]\(([^)]+)\)""")


@dataclass(frozen=True)
class LinkIssue:
    """A single verification finding."""

    severity: str  # "ERROR" or "WARN"
    page: Path
    target: str
    message: str


def _iter_markdown_pages(wiki_dir: Path) -> Iterator[Path]:
    """Yield markdown pages under the wiki directory.

    Args:
        wiki_dir: Root directory of wiki pages.

    Yields:
        Paths to markdown files.
    """
    yield from sorted(wiki_dir.rglob("*.md"))


def _has_h1_heading(md_text: str) -> bool:
    """Return True if the markdown text contains a level-1 heading.

    Args:
        md_text: Markdown file content.

    Returns:
        True if a line starts with '# ' (ignoring leading whitespace).
    """
    return any(line.lstrip().startswith("# ") for line in md_text.splitlines())


def _split_target(raw_target: str) -> tuple[str, str]:
    """Split a markdown link target into (path_part, anchor_part).

    Args:
        raw_target: The raw string inside parentheses of a markdown link.

    Returns:
        Tuple of (path_part, anchor_part). Anchor part includes the leading '#'
        when present, otherwise ''.
    """
    target = raw_target.strip()
    if "#" in target:
        path_part, anchor_part = target.split("#", 1)
        return path_part, "#" + anchor_part
    return target, ""


def _is_external_link(target: str) -> bool:
    """Return True if the link is external and should not be checked.

    Args:
        target: Link target string.

    Returns:
        True for http(s), mailto, or other non-file links.
    """
    lower = target.lower()
    return (
        lower.startswith("http://")
        or lower.startswith("https://")
        or lower.startswith("mailto:")
        or lower.startswith("tel:")
    )


def _normalize_target_path(path_part: str) -> str:
    """Normalize a link target path for filesystem checking.

    Args:
        path_part: Link target without anchor.

    Returns:
        Decoded, trimmed path string.
    """
    # GitHub links often include %20 etc.
    path = unquote(path_part.strip())
    # Ignore empty or anchor-only links.
    return path


def _candidate_paths(wiki_dir: Path, page_path: Path, target_path: str) -> list[Path]:
    """Return candidate filesystem paths for a target.

    Args:
        wiki_dir: Wiki root.
        page_path: The page where the link appears.
        target_path: Normalized target path without anchor.

    Returns:
        A list of candidate Paths that should be considered for existence checks.
    """
    # Absolute-like paths are treated as relative to wiki root.
    target = target_path.lstrip("/")
    rel = Path(target)

    # Prefer relative-to-page first (handles subfolders if you use them).
    candidates: list[Path] = []
    candidates.append((page_path.parent / rel).resolve())

    # Also allow wiki-root-relative.
    candidates.append((wiki_dir / rel).resolve())

    return candidates


def _looks_like_wiki_page(target_path: str) -> bool:
    """Return True if the target should be treated as a wiki page link.

    Args:
        target_path: Normalized target path without anchor.

    Returns:
        True for links without an extension or with '.md'.
    """
    if not target_path:
        return False
    suffix = Path(target_path).suffix.lower()
    return suffix in ("", ".md")


def _looks_like_image(target_path: str) -> bool:
    """Return True if the target looks like an image/asset link.

    Args:
        target_path: Normalized target path without anchor.

    Returns:
        True if the path ends with a common image extension.
    """
    suffix = Path(target_path).suffix.lower()
    return suffix in (".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp")


def _extract_link_targets(md_text: str) -> Iterator[str]:
    """Extract inline markdown link targets (excluding images).

    Args:
        md_text: Markdown file content.

    Yields:
        Targets (the raw text inside parentheses).
    """
    for m in _MD_LINK_RE.finditer(md_text):
        yield m.group(1)


def _extract_image_targets(md_text: str) -> Iterator[str]:
    """Extract inline markdown image targets.

    Args:
        md_text: Markdown file content.

    Yields:
        Targets (the raw text inside parentheses).
    """
    for m in _MD_IMAGE_RE.finditer(md_text):
        yield m.group(1)


def verify_wiki(wiki_dir: Path) -> list[LinkIssue]:
    """Verify the wiki directory content.

    Args:
        wiki_dir: Wiki root directory, typically 'wiki/'.

    Returns:
        A list of issues (errors and warnings).
    """
    issues: list[LinkIssue] = []

    if not wiki_dir.exists():
        issues.append(
            LinkIssue(
                severity="ERROR",
                page=wiki_dir,
                target=str(wiki_dir),
                message="Wiki directory does not exist.",
            )
        )
        return issues

    home = wiki_dir / "Home.md"
    if not home.exists():
        issues.append(
            LinkIssue(
                severity="ERROR",
                page=wiki_dir,
                target="Home.md",
                message="Missing Home.md (GitHub Wiki front page).",
            )
        )

    pages = list(_iter_markdown_pages(wiki_dir))
    if not pages:
        issues.append(
            LinkIssue(
                severity="WARN",
                page=wiki_dir,
                target=str(wiki_dir),
                message="No markdown pages found under wiki directory.",
            )
        )
        return issues

    for page in pages:
        try:
            text = page.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            issues.append(
                LinkIssue(
                    severity="ERROR",
                    page=page,
                    target=str(page),
                    message="File is not valid UTF-8.",
                )
            )
            continue

        if not _has_h1_heading(text):
            issues.append(
                LinkIssue(
                    severity="WARN",
                    page=page,
                    target=str(page.name),
                    message="No H1 heading found (expected '# ...').",
                )
            )

        # Regular links
        for raw in _extract_link_targets(text):
            path_part, _anchor = _split_target(raw)
            if not path_part.strip():
                continue
            if _is_external_link(path_part):
                continue

            norm = _normalize_target_path(path_part)
            if not norm:
                continue

            if _looks_like_image(norm):
                # treat image link like asset
                if not _path_exists(wiki_dir, page, norm):
                    issues.append(
                        LinkIssue(
                            severity="ERROR",
                            page=page,
                            target=raw,
                            message="Broken asset link.",
                        )
                    )
                continue

            if _looks_like_wiki_page(norm):
                if not _wiki_page_exists(wiki_dir, page, norm):
                    issues.append(
                        LinkIssue(
                            severity="ERROR",
                            page=page,
                            target=raw,
                            message="Broken wiki page link.",
                        )
                    )
                continue

            # Other relative files (e.g. .pdf) are checked as assets.
            if not _path_exists(wiki_dir, page, norm):
                issues.append(
                    LinkIssue(
                        severity="ERROR",
                        page=page,
                        target=raw,
                        message="Broken relative link.",
                    )
                )

        # Image links
        for raw in _extract_image_targets(text):
            path_part, _anchor = _split_target(raw)
            if not path_part.strip():
                continue
            if _is_external_link(path_part):
                continue

            norm = _normalize_target_path(path_part)
            if not norm:
                continue

            if not _path_exists(wiki_dir, page, norm):
                issues.append(
                    LinkIssue(
                        severity="ERROR",
                        page=page,
                        target=raw,
                        message="Broken image link.",
                    )
                )

    return issues


def _path_exists(wiki_dir: Path, page_path: Path, target_path: str) -> bool:
    """Return True if the target file exists (relative to page or wiki root)."""
    return any(cand.exists() for cand in _candidate_paths(wiki_dir, page_path, target_path))


def _wiki_page_exists(wiki_dir: Path, page_path: Path, target_path: str) -> bool:
    """Return True if a wiki page exists for the given target.

    Accepts links written as '(Page-Name)' or '(Page-Name.md)'.
    """
    p = Path(target_path)
    candidates: list[str] = []
    if p.suffix.lower() == ".md":
        candidates.append(target_path)
    else:
        candidates.append(target_path + ".md")

    # Some people use spaces; others use dashes. We do not rewrite: we check
    # exactly as written, plus the '.md' normalization above.
    return any(_path_exists(wiki_dir, page_path, cand_rel) for cand_rel in candidates)


def _format_issues(issues: Iterable[LinkIssue]) -> str:
    """Format issues for console output."""
    lines: list[str] = []
    for iss in issues:
        rel_page = iss.page.as_posix()
        lines.append(f"[{iss.severity}] {rel_page}: {iss.message} -> {iss.target}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    """CLI entry point.

    Args:
        argv: Optional argv list (without program name). If None, uses sys.argv[1:].

    Returns:
        Process exit code.
    """
    parser = argparse.ArgumentParser(description="Verify wiki markdown and internal links.")
    parser.add_argument(
        "--wiki-dir",
        type=Path,
        default=Path("wiki"),
        help="Wiki directory (default: wiki)",
    )
    parser.add_argument(
        "--fail-on-warnings",
        action="store_true",
        help="Return a non-zero exit code if warnings exist.",
    )
    args = parser.parse_args(argv)

    issues = verify_wiki(args.wiki_dir)
    errors = [i for i in issues if i.severity == "ERROR"]
    warnings = [i for i in issues if i.severity == "WARN"]

    if issues:
        print(_format_issues(issues))

    if errors:
        return 2
    if warnings and args.fail_on_warnings:
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
