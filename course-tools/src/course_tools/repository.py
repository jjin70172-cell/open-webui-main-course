"""Read and validate the local curriculum JSON files."""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from .errors import DataFileNotFoundError, DataSchemaError, EntityNotFoundError
from .paths import CHAPTERS_PATH, PREREQUISITES_PATH, resolve_repo_root


VALID_CATEGORIES = {"behavioral", "creational", "structural"}
VALID_PATTERN_KINDS = {"gof", "python_idiom", "architecture"}
VALID_KNOWLEDGE_POINT_TYPES = {
    "pattern_role",
    "python_technique",
    "lab_task",
    "pitfall",
    "comparison",
}


def _load_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise DataFileNotFoundError(str(path))
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except json.JSONDecodeError as exc:
        raise DataSchemaError(f"JSON 解析失败: {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise DataSchemaError(f"JSON 根节点必须是对象: {path}")
    return data


class CurriculumRepository:
    """Cached access to chapters and prerequisite data."""

    def __init__(self, repo_root=None, chapters_path: Optional[Path] = None, prerequisites_path: Optional[Path] = None):
        self.repo_root = resolve_repo_root(repo_root)
        self.chapters_path = chapters_path or CHAPTERS_PATH
        self.prerequisites_path = prerequisites_path or PREREQUISITES_PATH
        self._chapters: Optional[List[Dict[str, Any]]] = None
        self._prerequisites: Optional[Dict[str, Any]] = None
        self._chapter_by_id: Optional[Dict[str, Dict[str, Any]]] = None

    @property
    def chapters(self) -> List[Dict[str, Any]]:
        if self._chapters is None:
            data = _load_json(self.chapters_path)
            chapters = data.get("chapters")
            if not isinstance(chapters, list):
                raise DataSchemaError("chapters.json 中缺少 chapters 数组")
            self._chapters = chapters
            self._chapter_by_id = {}
            for chapter in chapters:
                if not isinstance(chapter, dict) or not chapter.get("id"):
                    raise DataSchemaError("章节对象缺少 id")
                self._chapter_by_id[chapter["id"]] = chapter
        return self._chapters

    @property
    def prerequisites(self) -> Dict[str, Any]:
        if self._prerequisites is None:
            data = _load_json(self.prerequisites_path)
            for key in ("confirmed_prerequisites", "related", "unconfirmed", "foundations", "unmapped_references"):
                if key not in data:
                    raise DataSchemaError(f"prerequisites.json 缺少字段: {key}")
            self._prerequisites = data
        return self._prerequisites

    def chapter_ids(self) -> List[str]:
        return [chapter["id"] for chapter in self.chapters]

    def get_chapter(self, chapter_id: str) -> Dict[str, Any]:
        self.chapters
        chapter = self._chapter_by_id.get(chapter_id)
        if chapter is None:
            raise EntityNotFoundError(chapter_id)
        return chapter

    def source_paths(self, paths) -> List[Path]:
        return [self.repo_root / str(path) for path in paths]

    def missing_source_paths(self, paths) -> List[str]:
        missing = []
        for path in paths:
            full_path = self.repo_root / str(path)
            if not full_path.exists():
                missing.append(str(path))
        return missing

    def check_source_paths(self, chapter: Dict[str, Any]) -> List[str]:
        paths = [source["path"] for source in chapter.get("sources", [])]
        return self.missing_source_paths(paths)


def build_chapter_search_index(chapters: List[Dict[str, Any]]) -> Dict[str, str]:
    """Map a normalized search token to a chapter id."""
    index: Dict[str, str] = {}

    def add(key: str, chapter_id: str):
        normalized = " ".join(key.lower().split())
        if normalized and normalized not in index:
            index[normalized] = chapter_id

    for chapter in chapters:
        add(chapter.get("id", ""), chapter["id"])
        add(str(chapter.get("lab_no", "")), chapter["id"])
        add(chapter.get("title", {}).get("en", ""), chapter["id"])
        add(chapter.get("title", {}).get("zh", ""), chapter["id"])
        for alias in chapter.get("aliases", []):
            add(str(alias), chapter["id"])
    return index

