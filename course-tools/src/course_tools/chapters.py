"""Course chapter lookup backed by chapters.json."""

from typing import Any, Dict, List, Optional, Tuple

from .errors import InvalidInputError, UnknownError
from .repository import CurriculumRepository, VALID_CATEGORIES, VALID_PATTERN_KINDS, build_chapter_search_index


def _normalize(value: str) -> str:
    return " ".join(value.lower().split())


def _validate_lookup_inputs(query, category, lab_no, pattern_kind, limit) -> None:
    if query is not None and not isinstance(query, str):
        raise InvalidInputError("query 必须是字符串。")
    if category is not None and category not in VALID_CATEGORIES:
        raise InvalidInputError(f"category 必须是 {sorted(VALID_CATEGORIES)} 之一。")
    if pattern_kind is not None and pattern_kind not in VALID_PATTERN_KINDS:
        raise InvalidInputError(f"pattern_kind 必须是 {sorted(VALID_PATTERN_KINDS)} 之一。")
    if lab_no is not None:
        if isinstance(lab_no, bool) or not isinstance(lab_no, int):
            raise InvalidInputError("lab_no 必须是整数。")
    if limit is not None:
        if isinstance(limit, bool) or not isinstance(limit, int) or limit < 1:
            raise InvalidInputError("limit 必须是正整数。")


def _filter_chapters(chapters: List[Dict[str, Any]], category, lab_no, pattern_kind) -> List[Dict[str, Any]]:
    result = chapters
    if category is not None:
        result = [c for c in result if c.get("category") == category]
    if lab_no is not None:
        result = [c for c in result if c.get("lab_no") == lab_no]
    if pattern_kind is not None:
        result = [c for c in result if c.get("pattern_kind") == pattern_kind]
    return result


def _score_chapter(chapter: Dict[str, Any], query: str) -> Tuple[int, List[str]]:
    q = _normalize(query)
    if not q:
        return 0, []

    chapter_id = _normalize(str(chapter.get("id", "")))
    lab_no = _normalize(str(chapter.get("lab_no", "")))
    title_en = _normalize(str(chapter.get("title", {}).get("en", "")))
    title_zh = _normalize(str(chapter.get("title", {}).get("zh", "")))
    aliases = [_normalize(str(alias)) for alias in chapter.get("aliases", [])]
    keywords = [_normalize(str(keyword)) for keyword in chapter.get("keywords", [])]
    summary = _normalize(str(chapter.get("summary", "")))

    score = 0
    matched_by: List[str] = []

    if q == chapter_id:
        return 100, ["id"]
    if q == lab_no:
        return 100, ["lab_no"]
    if q == title_en:
        return 95, ["title.en"]
    if q == title_zh:
        return 95, ["title.zh"]

    if q in aliases:
        return 90, ["alias"]
    if q in keywords:
        return 80, ["keyword"]

    if q in title_en or q in title_zh:
        score = 85
        matched_by.append("title")
    for alias in aliases:
        if q in alias:
            score = max(score, 75)
            matched_by.append("alias")
    for keyword in keywords:
        if q in keyword or keyword in q:
            score = max(score, 70)
            matched_by.append("keyword")
    if q in summary:
        score = max(score, 30)
        matched_by.append("summary")
    return score, list(dict.fromkeys(matched_by))


def _format_knowledge_point(kp: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": kp.get("id"),
        "type": kp.get("type"),
        "text": kp.get("text"),
        "source_files": kp.get("source_files", []),
        "confidence": kp.get("confidence"),
    }


def _format_chapter(chapter: Dict[str, Any], include_knowledge_points: bool, include_sources: bool) -> Dict[str, Any]:
    item = {
        "id": chapter.get("id"),
        "lab_no": chapter.get("lab_no"),
        "title": chapter.get("title"),
        "category": chapter.get("category"),
        "pattern_kind": chapter.get("pattern_kind"),
        "aliases": chapter.get("aliases", []),
        "summary": chapter.get("summary"),
    }
    if include_sources:
        item["sources"] = [source.get("path") for source in chapter.get("sources", [])]
    if include_knowledge_points:
        item["knowledge_points"] = [
            _format_knowledge_point(kp) for kp in chapter.get("knowledge_points", [])
        ]
    return item


def _source_warning(chapters: List[Dict[str, Any]], repository: CurriculumRepository) -> List[Dict[str, Any]]:
    missing: Dict[str, List[str]] = {}
    for chapter in chapters:
        for path in repository.check_source_paths(chapter):
            missing.setdefault(path, []).append(chapter["id"])
    return [
        {
            "code": "SOURCE_FILE_MISSING",
            "message": "结果引用的来源文件不存在，已保留结果但请核对来源。",
            "path": path,
            "chapter_ids": ids,
        }
        for path, ids in missing.items()
    ]


def course_chapter_lookup(
    query: Optional[str] = None,
    category: Optional[str] = None,
    lab_no: Optional[int] = None,
    pattern_kind: Optional[str] = None,
    limit: int = 5,
    include_knowledge_points: bool = False,
    include_sources: bool = True,
    repo_root=None,
) -> Dict[str, Any]:
    """Query chapters from chapters.json.

    The function never generates course content from the model. It reads the
    local JSON index and returns the matching chapter records.
    """
    try:
        _validate_lookup_inputs(query, category, lab_no, pattern_kind, limit)
        repository = CurriculumRepository(repo_root=repo_root)
        chapters = _filter_chapters(repository.chapters, category, lab_no, pattern_kind)

        has_query = query is not None and _normalize(query) != ""
        filters = {
            "category": category,
            "lab_no": lab_no,
            "pattern_kind": pattern_kind,
        }
        active_filters = [key for key, value in filters.items() if value is not None]

        if has_query:
            scored = []
            for chapter in chapters:
                score, matched_by = _score_chapter(chapter, query)
                if score > 0:
                    scored.append((score, chapter, matched_by))
            scored.sort(key=lambda entry: (-entry[0], entry[1].get("lab_no", 0)))
            selected = [entry for entry in scored[:limit]]
            match_type = "exact" if selected and selected[0][0] >= 90 else "fuzzy"
            matched_by = selected[0][2] if selected else []
        else:
            chapters_sorted = sorted(chapters, key=lambda c: c.get("lab_no", 0))
            selected = [(0, chapter, []) for chapter in chapters_sorted[:limit]]
            match_type = "filter" if active_filters else "all"
            matched_by = active_filters

        results = [
            _format_chapter(chapter, include_knowledge_points, include_sources)
            for _, chapter, _ in selected
        ]
        warnings = _source_warning([chapter for _, chapter, _ in selected], repository)

        if not results:
            suggestions = [chapter.get("title", {}).get("en", chapter["id"]) for chapter in repository.chapters[:10]]
        else:
            suggestions = []

        return {
            "ok": True,
            "query": query,
            "filters": filters,
            "match_type": match_type,
            "matched_by": matched_by,
            "count": len(results),
            "limit": limit,
            "results": results,
            "warnings": warnings,
            "suggestions": suggestions,
        }
    except InvalidInputError as exc:
        return {"ok": False, "error": exc.to_dict()}
    except Exception as exc:  # pragma: no cover - defensive boundary
        if hasattr(exc, "code") and hasattr(exc, "to_dict"):
            return {"ok": False, "error": exc.to_dict()}
        return {"ok": False, "error": UnknownError(str(exc)).to_dict()}

