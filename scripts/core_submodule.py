"""Fetch and verify the ``greekromannumerical-core`` submodule by version tag.

The pinned tag is stored as ``submodule.greekromannumerical-core.tag`` in ``.gitmodules``.

Usage:
    python scripts/core_submodule.py check [--require-latest]
    python scripts/core_submodule.py sync [--tag vX.Y.Z | --latest]
    python scripts/core_submodule.py latest
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SUBMODULE = "greekromannumerical-core"
SUBMODULE_PATH = ROOT / SUBMODULE
TAG_KEY = f"submodule.{SUBMODULE}.tag"
VERSION_TAG = re.compile(r"^v(\d+)\.(\d+)\.(\d+)$")


def git(*args: str, cwd: Path = ROOT) -> str:
    result = subprocess.run(
        ["git", *args], cwd=cwd, check=True, capture_output=True, text=True
    )
    return result.stdout.strip()


def annotate(level: str, message: str) -> None:
    if os.getenv("GITHUB_ACTIONS") == "true":
        print(f"::{level}::{message}")
    else:
        print(f"{level}: {message}", file=sys.stderr if level == "error" else sys.stdout)


def version_key(tag: str) -> tuple[int, ...]:
    match = VERSION_TAG.match(tag)
    if match is None:
        raise SystemExit(f"Tag must look like vX.Y.Z, got {tag!r}")
    return tuple(int(part) for part in match.groups())


def pinned_tag() -> str:
    tag = git("config", "-f", ".gitmodules", "--get", TAG_KEY)
    version_key(tag)
    return tag


def latest_tag() -> str:
    output = git("ls-remote", "--tags", "--refs", "origin", "v*", cwd=SUBMODULE_PATH)
    tags = [line.rsplit("refs/tags/", 1)[1] for line in output.splitlines()]
    tags = [tag for tag in tags if VERSION_TAG.match(tag)]
    if not tags:
        raise SystemExit(f"No vX.Y.Z tags found in the {SUBMODULE} remote")
    return max(tags, key=version_key)


def ensure_initialized() -> None:
    if not (SUBMODULE_PATH / ".git").exists():
        git("submodule", "update", "--init", SUBMODULE)


def fetch_tag(tag: str) -> str:
    git(
        "fetch", "--force", "--no-tags", "origin",
        f"+refs/tags/{tag}:refs/tags/{tag}",
        cwd=SUBMODULE_PATH,
    )
    return git("rev-parse", f"{tag}^{{commit}}", cwd=SUBMODULE_PATH)


def check(require_latest: bool) -> int:
    ensure_initialized()
    tag = pinned_tag()
    expected = fetch_tag(tag)
    actual = git("rev-parse", "HEAD", cwd=SUBMODULE_PATH)
    if actual != expected:
        annotate(
            "error",
            f"{SUBMODULE} is checked out at {actual[:12]}, but .gitmodules pins {tag} "
            f"({expected[:12]}). Run: python scripts/core_submodule.py sync --tag {tag}",
        )
        return 1
    print(f"{SUBMODULE} matches pinned tag {tag} ({expected[:12]})")

    latest = latest_tag()
    if latest != tag:
        annotate(
            "error" if require_latest else "warning",
            f"{SUBMODULE} {latest} is available (pinned {tag}). "
            "Run: python scripts/core_submodule.py sync --latest",
        )
        return 1 if require_latest else 0
    print(f"{tag} is the latest {SUBMODULE} release")
    return 0


def sync(tag: str | None, latest: bool) -> int:
    ensure_initialized()
    tag = latest_tag() if latest else tag or pinned_tag()
    version_key(tag)
    commit = fetch_tag(tag)
    git("checkout", "--quiet", "--detach", commit, cwd=SUBMODULE_PATH)
    git("config", "-f", ".gitmodules", TAG_KEY, tag)
    print(f"{SUBMODULE} checked out at {tag} ({commit[:12]})")
    if os.getenv("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as output:
            output.write(f"tag={tag}\n")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Manage the core submodule version tag.")
    commands = parser.add_subparsers(dest="command", required=True)

    check_parser = commands.add_parser("check", help="verify the checkout matches the pinned tag")
    check_parser.add_argument(
        "--require-latest",
        action="store_true",
        help="fail instead of warning when a newer core tag exists",
    )

    sync_parser = commands.add_parser("sync", help="check out a core tag and pin it")
    target = sync_parser.add_mutually_exclusive_group()
    target.add_argument("--tag", help="tag to check out (default: the pinned tag)")
    target.add_argument("--latest", action="store_true", help="use the newest vX.Y.Z tag")

    commands.add_parser("latest", help="print the newest vX.Y.Z tag of the core remote")

    args = parser.parse_args()
    try:
        if args.command == "check":
            return check(args.require_latest)
        if args.command == "sync":
            return sync(args.tag, args.latest)
        ensure_initialized()
        print(latest_tag())
        return 0
    except subprocess.CalledProcessError as error:
        annotate("error", f"git {' '.join(error.cmd[1:])} failed: {error.stderr.strip()}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
