"""Knowledge point prerequisite and related relation lookup.

The module reads ``prerequisites.json`` and ``chapters.json`` and returns only
relationships that are actually recorded in the local index. It never invents a
formal prerequisite edge.
"""

from typing import Any, Dict, List, Optional

from .errors import (
    AmbiguousQueryError,
    EntityNotFoundError,
    InvalidInputError,
    UnknownError,
)
from .repository import CurriculumRepository, VALID_PATTERN_KINDS, VALID_CATEGORIES


VALID_DIRECTIONS = {"all", "incoming", "outgoing"}


def _normalize(value: str) -> str:
    return " ".join(value.lower().split())


def _validate_inputs(target, direction, max_depth) -> None:
    if target is None:
        raise InvalidInputError("target 不能为空。")
    if isinstance(target, str) and _normalize(target) == "":
        raise InvalidInputError("target 不能为空字符串。")
    if isinstance(target, bool) or (not isinstance(target, (str, int))):
        raise InvalidInputError("target 必须是字符串、Lab 编号或知识点 ID。")
    if direction is not None and direction not in VALID_DIRECTIONS:
        raise InvalidInputError(
            f"direction 必须是 {sorted(VALID_DIRECTIONS)} 之一，或省略以表示 all。"
        )
    if max_depth is not None:
        if isinstance(max_depth, bool) or not isinstance(max_depth, int) or max_depth < 1:
            raise InvalidInputError("max_depth 必须是正整数。")


def _chapter_title(chapter: Dict[str, Any]) -> Dict[str, str]:
    return {
        "en": chapter.get("title", {}).get("en", ""),
        "zh": chapter.get("title", {}).get("zh", ""),
    }


def _find_knowledge_point(repository: CurriculumRepository, value: str):
    """Return ``(chapter, knowledge_point)`` when ``value`` matches a KP."""
    normalized = _normalize(value)
    for chapter in repository.chapters:
        for kp in chapter.get("knowledge_points", []):
            if kp.get("id") == value or _normalize(str(kp.get("id", ""))) == normalized:
                return chapter, kp
    for chapter in repository.chapters:
        for kp in chapter.get("knowledge_points", []):
            if normalized == _normalize(str(kp.get("text", ""))):
                return chapter, kp
    return None, None


def _resolve_target(repository: CurriculumRepository, target):
    """Resolve a user supplied target into a chapter plus a resolution note."""
    if isinstance(target, int):
        for chapter in repository.chapters:
            if chapter.get("lab_no") == target:
                return chapter, {"resolved_via": "lab_no", "knowledge_point": None}
        raise EntityNotFoundError(str(target))

    value = str(target)
    normalized = _normalize(value)

    for chapter in repository.chapters:
        if chapter.get("id") == value:
            return chapter, {"resolved_via": "id", "knowledge_point": None}

    for chapter in repository.chapters:
        if str(chapter.get("lab_no")) == value:
            return chapter, {"resolved_via": "lab_no", "knowledge_point": None}

    kp_chapter, kp = _find_knowledge_point(repository, value)
    if kp_chapter is not None:
        return kp_chapter, {"resolved_via": "knowledge_point", "knowledge_point": kp}

    exact = []
    for chapter in repository.chapters:
        title = _chapter_title(chapter)
        if normalized in (_normalize(title["en"]), _normalize(title["zh"])):
            exact.append((chapter, "title"))
    if len(exact) == 1:
        return exact[0][0], {"resolved_via": exact[0][1], "knowledge_point": None}
    if len(exact) > 1:
        raise AmbiguousQueryError(
            f"target 匹配到多个章节: {value}",
            candidates=[chapter["id"] for chapter, _ in exact],
        )

    alias_matches = []
    for chapter in repository.chapters:
        for alias in chapter.get("aliases", []):
            if normalized == _normalize(str(alias)):
                alias_matches.append(chapter)
                break
    if len(alias_matches) == 1:
        return alias_matches[0], {"resolved_via": "alias", "knowledge_point": None}
    if len(alias_matches) > 1:
        raise AmbiguousQueryError(
            f"target 通过别名匹配到多个章节: {value}",
            candidates=[chapter["id"] for chapter in alias_matches],
        )

    fuzzy = []
    for chapter in repository.chapters:
        title = _chapter_title(chapter)
        haystacks = [title["en"], title["zh"], chapter.get("id", "")]
        haystacks += [str(alias) for alias in chapter.get("aliases", [])]
        haystacks += [str(keyword) for keyword in chapter.get("keywords", [])]
        if any(normalized and normalized in _normalize(str(hay)) for hay in haystacks):
            fuzzy.append(chapter)
    if len(fuzzy) == 1:
        return fuzzy[0], {"resolved_via": "fuzzy", "knowledge_point": None}
    if len(fuzzy) > 1:
        raise AmbiguousQueryError(
            f"target 模糊匹配到多个章节: {value}",
            candidates=[chapter["id"] for chapter in fuzzy],
        )

    suggestions = [chapter.get("id") for chapter in repository.chapters[:10]]
    raise EntityNotFoundError(value, candidates=suggestions)


def _format_chapter_ref(chapter: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": chapter.get("id"),
        "lab_no": chapter.get("lab_no"),
        "title": _chapter_title(chapter),
        "category": chapter.get("category"),
        "pattern_kind": chapter.get("pattern_kind"),
        "source_files": [source.get("path") for source in chapter.get("sources", [])],
    }


def _format_relation(relation: Dict[str, Any], role: str, other: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": relation.get("id"),
        "relation_type": relation.get("relation_type"),
        "confidence": relation.get("confidence"),
        "direction": relation.get("direction"),
        "is_confirmed_prerequisite": relation.get("is_confirmed_prerequisite", False),
        "teaching_order_status": relation.get("teaching_order_status"),
        "role": role,
        "related_chapter": _format_chapter_ref(other),
        "source_files": relation.get("source_files", []),
        "evidence": relation.get("evidence", ""),
    }


def _incoming_matches(relation: Dict[str, Any], chapter_id: str) -> bool:
    """The queried chapter is the dependent node (``target``)."""
    return relation.get("target") == chapter_id


def _outgoing_matches(relation: Dict[str, Any], chapter_id: str) -> bool:
    """The queried chapter is listed as the other node's candidate prerequisite."""
    return relation.get("prerequisite") == chapter_id


def _select_related(repository, chapter_id, include_related):
    if not include_related:
        return []
    selected = []
    for relation in repository.prerequisites.get("related", []):
        # related relations are undirected comparisons; direction does not
        # change whether they belong to the queried chapter.
        if relation.get("target") != chapter_id and relation.get("prerequisite") != chapter_id:
            continue
        role = "target" if relation.get("target") == chapter_id else "prerequisite"
        other_id = relation.get("prerequisite") if role == "target" else relation.get("target")
        other = repository.get_chapter(other_id)
        selected.append(_format_relation(relation, role, other))
    return selected


def _select_unconfirmed(repository, chapter_id, direction, include_unconfirmed):
    if not include_unconfirmed:
        return []
    selected = []
    for relation in repository.prerequisites.get("unconfirmed", []):
        if direction == "all":
            include = relation.get("target") == chapter_id or relation.get("prerequisite") == chapter_id
        elif direction == "incoming":
            include = _incoming_matches(relation, chapter_id)
        else:
            include = _outgoing_matches(relation, chapter_id)
        if not include:
            continue
        role = "target" if relation.get("target") == chapter_id else "prerequisite"
        other_id = relation.get("prerequisite") if role == "target" else relation.get("target")
        other = repository.get_chapter(other_id)
        selected.append(_format_relation(relation, role, other))
    return selected


def _format_foundation(item: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": item.get("id"),
        "text": item.get("text"),
        "source_files": item.get("source_files", []),
        "evidence": item.get("evidence", ""),
        "confidence": item.get("confidence"),
    }


def _source_warning(items, repository) -> List[Dict[str, Any]]:
    missing: Dict[str, List[str]] = {}
    for item in items:
        for path in item.get("source_files", []):
            if not (repository.repo_root / str(path)).exists():
                missing.setdefault(str(path), []).append(item.get("id", ""))
    return [
        {
            "code": "SOURCE_FILE_MISSING",
            "message": "结果引用的来源文件不存在，已保留结果但请核对来源。",
            "path": path,
            "relation_ids": ids,
        }
        for path, ids in missing.items()
    ]


def course_prerequisite_lookup(
    target,
    direction: Optional[str] = None,
    max_depth: Optional[int] = None,
    include_related: bool = True,
    include_unconfirmed: bool = True,
    include_foundations: bool = True,
    repo_root=None,
) -> Dict[str, Any]:
    """Return the recorded prerequisite and related relations for a chapter.

    ``confirmed_prerequisites`` is intentionally empty because the repository
    does not state a formal prerequisite edge anywhere. This function reports
    that fact instead of inventing one.
    """
    try:
        _validate_inputs(target, direction, max_depth)
        direction = direction or "all"

        repository = CurriculumRepository(repo_root=repo_root)
        chapter, resolution = _resolve_target(repository, target)
        chapter_id = chapter["id"]

        related = _select_related(repository, chapter_id, include_related)
        unconfirmed = _select_unconfirmed(
            repository, chapter_id, direction, include_unconfirmed
        )
        foundations = (
            [_format_foundation(item) for item in repository.prerequisites.get("foundations", [])]
            if include_foundations
            else []
        )

        referenced_items = related + unconfirmed + foundations
        warnings = _source_warning(referenced_items, repository)

        knowledge_point = resolution.get("knowledge_point")
        kp_block = None
        if knowledge_point:
            kp_block = {
                "id": knowledge_point.get("id"),
                "type": knowledge_point.get("type"),
                "text": knowledge_point.get("text"),
                "source_files": knowledge_point.get("source_files", []),
                "confidence": knowledge_point.get("confidence"),
            }

        confirmed = repository.prerequisites.get("confirmed_prerequisites", [])
        note = (
            "知识库未给出任何正式先修关系，confirmed_prerequisites 始终为空；"
            "related 表示资料明确表达的比较/替代/易混淆关系，"
            "unconfirmed 表示无法从资料确认、仅作为候选的先后关系。"
        )

        return {
            "ok": True,
            "target": _format_chapter_ref(chapter),
            "knowledge_point": kp_block,
            "resolved_via": resolution["resolved_via"],
            "direction": direction,
            "max_depth": max_depth,
            "confirmed_prerequisites": list(confirmed),
            "note": note,
            "foundations": foundations,
            "related": related,
            "unconfirmed": unconfirmed,
            "counts": {
                "confirmed_prerequisites": 0,
                "foundations": len(foundations),
                "related": len(related),
                "unconfirmed": len(unconfirmed),
            },
            "warnings": warnings,
        }
    except (InvalidInputError, EntityNotFoundError, AmbiguousQueryError) as exc:
        return {"ok": False, "error": exc.to_dict()}
    except Exception as exc:  # pragma: no cover - defensive boundary
        if hasattr(exc, "code") and hasattr(exc, "to_dict"):
            return {"ok": False, "error": exc.to_dict()}
        return {"ok": False, "error": UnknownError(str(exc)).to_dict()}
