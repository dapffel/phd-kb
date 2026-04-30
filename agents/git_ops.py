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


def has_changes() -> bool:
    status = run_git("status", "--porcelain")
    return bool(status)
