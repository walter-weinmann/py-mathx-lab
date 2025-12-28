"""CI smoke test for documentation tags.

This test fails if any experiment page or the gallery uses tags that are not
declared in docs/tags.md.
"""

from __future__ import annotations

from pathlib import Path

from mathxlab.tools.validate_doc_tags import validate_doc_tags


# ------------------------------------------------------------------------------
def test_docs_tags_are_valid() -> None:
    """Ensure documentation tags are restricted to docs/tags.md."""
    repo_root = Path(__file__).resolve().parents[1]
    result = validate_doc_tags(repo_root)

    missing = result.missing_tags_line
    unknown_pages = result.unknown_tags
    unknown_gallery = result.gallery_unknown_tags
    invalid_gallery = result.gallery_invalid_format

    if not missing and not unknown_pages and not unknown_gallery and not invalid_gallery:
        return

    lines: list[str] = []
    if missing:
        lines.append("Missing '**Tags:**' line:")
        for p in sorted(missing, key=lambda x: x.as_posix()):
            lines.append(f"  - {p.as_posix()}")

    if unknown_pages:
        lines.append("Unknown tags in experiment pages:")
        for p, tags in sorted(unknown_pages.items(), key=lambda x: x[0].as_posix()):
            lines.append(f"  - {p.as_posix()}: {', '.join(tags)}")

    if unknown_gallery:
        lines.append("Unknown tags in gallery:")
        lines.append(f"  - {', '.join(unknown_gallery)}")

    if invalid_gallery:
        lines.append("Invalid tag format in gallery (expected lowercase [a-z0-9-]):")
        lines.append(f"  - {', '.join(invalid_gallery)}")

    raise AssertionError("\n".join(lines))
