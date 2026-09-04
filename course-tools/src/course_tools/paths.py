"""Filesystem locations used by the curriculum tools."""

from pathlib import Path


PACKAGE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = PACKAGE_DIR.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
CHAPTERS_PATH = DATA_DIR / "chapters.json"
PREREQUISITES_PATH = DATA_DIR / "prerequisites.json"
DEFAULT_REPO_ROOT = PROJECT_ROOT.parent / "python-design-pattern-rag"


def resolve_repo_root(repo_root) -> Path:
    """Return an absolute repository path, falling back to the cloned knowledge base."""
    if repo_root:
        return Path(repo_root).expanduser().resolve()
    return DEFAULT_REPO_ROOT

