# Copyright (c) 2022-2026 IO-Swiss Aero GmbH. All rights reserved.
# Use of this source code is governed by the IO-Swiss Aero GmbH
# License, that can be found in the LICENSE.md file.

"""Publish repo-managed wiki pages to the GitHub Wiki repository.

GitHub Wikis are stored in a separate git repository: `<OWNER>/<REPO>.wiki.git`.
This script supports a repo-first workflow:

- Source of truth lives in the main repo under `wiki/`.
- Changes go through normal PR review and CI checks.
- On merge to `main`, CI publishes `wiki/` to the GitHub Wiki repo.

Usage:
    python tools/sync_wiki.py --repo walter-weinmann/py-mathx-lab

Environment variables:
    WIKI_TOKEN: GitHub token with write access to the repository. A fine-grained
        PAT is recommended (Contents: read/write for this repo).
    WIKI_AUTHOR_NAME: Optional commit author name (default: wiki-sync-bot).
    WIKI_AUTHOR_EMAIL: Optional commit author email
        (default: wiki-sync-bot@users.noreply.github.com).

Notes:
    - The sync is one-way (repo -> wiki). The wiki git repo is treated as a
      publish target and will be overwritten with the contents of `wiki/`.
    - Keep math-heavy MyST/Sphinx pages in `docs/` since GitHub Wiki does not
      render MyST roles like `{doc}` or `{cite:p}`.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import tempfile
from pathlib import Path


def _run(cmd: list[str], cwd: Path | None = None) -> None:
    """Run a command and raise a helpful error if it fails.

    Args:
        cmd: Command and arguments.
        cwd: Optional working directory.

    Raises:
        RuntimeError: If the command fails.
    """
    try:
        subprocess.run(cmd, cwd=str(cwd) if cwd else None, check=True)
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}") from exc


def _git_output(cmd: list[str], cwd: Path) -> str:
    """Run a git command and return stdout.

    Args:
        cmd: Git command and arguments (without the leading 'git').
        cwd: Working directory.

    Returns:
        Command stdout.

    Raises:
        RuntimeError: If the git command fails.
    """
    try:
        proc = subprocess.run(
            ["git", *cmd],
            cwd=str(cwd),
            check=True,
            capture_output=True,
            text=True,
        )
        return proc.stdout
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(f"Git command failed: git {' '.join(cmd)}") from exc


def _copy_tree(src: Path, dst: Path) -> None:
    """Copy a directory tree into an existing destination folder.

    Args:
        src: Source directory.
        dst: Destination directory.
    """
    for path in src.rglob("*"):
        rel = path.relative_to(src)
        target = dst / rel

        if path.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue

        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)


def _clear_publish_target(target_dir: Path) -> None:
    """Remove all files/folders in publish target except .git.

    Args:
        target_dir: Directory that contains a `.git` folder.
    """
    for item in target_dir.iterdir():
        if item.name == ".git":
            continue
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()


def sync_wiki(repo: str, wiki_dir: Path) -> None:
    """Sync `wiki_dir` into the GitHub Wiki git repository.

    Args:
        repo: Repository in the form "owner/name", e.g. "walter-weinmann/py-mathx-lab".
        wiki_dir: Path to the wiki source directory in the main repo.

    Raises:
        FileNotFoundError: If wiki_dir does not exist.
        RuntimeError: If cloning/pushing fails.
    """
    if not wiki_dir.exists():
        raise FileNotFoundError(f"Wiki source folder not found: {wiki_dir}")

    token = os.environ.get("WIKI_TOKEN", "").strip()
    author_name = os.environ.get("WIKI_AUTHOR_NAME", "wiki-sync-bot").strip()
    author_email = os.environ.get(
        "WIKI_AUTHOR_EMAIL", "wiki-sync-bot@users.noreply.github.com"
    ).strip()

    wiki_url = f"https://github.com/{repo}.wiki.git"
    if token:
        # Token auth for CI (fine-grained PAT recommended).
        wiki_url = f"https://x-access-token:{token}@github.com/{repo}.wiki.git"

    with tempfile.TemporaryDirectory(prefix="wiki_sync_") as tmp:
        checkout = Path(tmp) / "wiki_repo"

        _run(["git", "clone", "--depth", "1", wiki_url, str(checkout)])

        _run(["git", "config", "user.name", author_name], cwd=checkout)
        _run(["git", "config", "user.email", author_email], cwd=checkout)

        _clear_publish_target(checkout)
        _copy_tree(wiki_dir, checkout)

        status = _git_output(["status", "--porcelain"], cwd=checkout).strip()
        if not status:
            print("No wiki changes to publish.")
            return

        _run(["git", "add", "-A"], cwd=checkout)
        _run(["git", "commit", "-m", "Sync wiki from main repo"], cwd=checkout)
        _run(["git", "push"], cwd=checkout)
        print("Wiki published successfully.")


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Sync repo wiki/ folder to GitHub Wiki.")
    parser.add_argument(
        "--repo", required=True, help="owner/repo, e.g. walter-weinmann/py-mathx-lab"
    )
    parser.add_argument(
        "--wiki-dir", default="wiki", help="Path to wiki source folder (default: wiki)"
    )
    args = parser.parse_args()

    sync_wiki(repo=args.repo, wiki_dir=Path(args.wiki_dir).resolve())


if __name__ == "__main__":
    main()
