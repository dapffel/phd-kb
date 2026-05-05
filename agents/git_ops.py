import subprocess
from pathlib import Path

from agents.config import settings


def run_git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=settings.vault_root,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def commit(message: str):
    run_git("add", "wiki/", "raw/_catalog.json", "raw/_catalog.md", "outputs/")
    run_git("commit", "-m", message)


def has_changes(paths: list[str] | None = None) -> bool:
    args = ["status", "--porcelain"]
    if paths:
        args.append("--")
        args.extend(paths)
    status = run_git(*args)
    return bool(status)
