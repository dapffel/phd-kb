import logging
import subprocess
from pathlib import Path

from agents.config import settings

logger = logging.getLogger(__name__)


class GitError(Exception):
    pass


def run_git(*args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=settings.vault_root,
        capture_output=True,
        text=True,
    )
    if check and result.returncode != 0:
        stderr = result.stderr.strip()
        logger.error("git %s failed (rc=%d): %s", " ".join(args), result.returncode, stderr)
        raise GitError(f"git {args[0]} failed: {stderr}")
    return result.stdout.strip()


def commit(message: str) -> bool:
    run_git("add", "wiki/", "raw/_catalog.json", "raw/_catalog.md", "outputs/")
    try:
        run_git("commit", "-m", message)
        return True
    except GitError as e:
        if "nothing to commit" in str(e):
            return False
        raise


def has_changes(paths: list[str] | None = None) -> bool:
    args = ["status", "--porcelain"]
    if paths:
        args.append("--")
        args.extend(paths)
    status = run_git(*args, check=False)
    return bool(status)
