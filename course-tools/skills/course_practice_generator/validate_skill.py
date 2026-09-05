"""Build a course-grounded context packet for the practice-generator Skill.

This helper deliberately stops before question generation.  It reads the same
local chapter index used by the course tools and exposes only verified fields,
so the Open WebUI Skill can be tested without turning the curriculum index into
an answer bank.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable


MAX_COUNT = 20

DIFFICULTY_ALIASES = {
    "基础": "基础",
    "基础难度": "基础",
    "basic": "基础",
    "easy": "基础",
    "入门": "基础",
    "中等": "中等",
    "中等难度": "中等",
    "中级": "中等",
    "medium": "中等",
    "intermediate": "中等",
    "进阶": "进阶",
    "进阶难度": "进阶",
    "高级": "进阶",
    "advanced": "进阶",
    "hard": "进阶",
}

QUESTION_TYPE_ALIASES = {
    "选择": "choice",
    "选择题": "choice",
    "单选": "choice",
    "单选题": "choice",
    "choice": "choice",
    "single": "choice",
    "single choice": "choice",
    "single_choice": "choice",
    "判断": "true_false",
    "判断题": "true_false",
    "true false": "true_false",
    "true_false": "true_false",
    "true-false": "true_false",
    "tf": "true_false",
    "简答": "short_answer",
    "简答题": "short_answer",
    "short answer": "short_answer",
    "short_answer": "short_answer",
    "代码阅读": "code_reading",
    "代码阅读题": "code_reading",
    "code reading": "code_reading",
    "code_reading": "code_reading",
    "综合": "comprehensive",
    "综合题": "comprehensive",
    "综合题型": "comprehensive",
    "comprehensive": "comprehensive",
}

DEFAULT_QUESTION_TYPES = [
    "choice",
    "true_false",
    "short_answer",
    "code_reading",
    "comprehensive",
]


def _normalise_key(value: str) -> str:
    return " ".join(value.strip().lower().replace("-", " ").split())


def canonicalize_difficulty(value: str) -> str | None:
    if not isinstance(value, str):
        return None
    return DIFFICULTY_ALIASES.get(_normalise_key(value))


def canonicalize_question_type(value: str) -> str | None:
    if not isinstance(value, str):
        return None
    key = _normalise_key(value)
    return QUESTION_TYPE_ALIASES.get(key) or QUESTION_TYPE_ALIASES.get(value.strip().lower())


def _error(code: str, message: str, **extra: Any) -> dict[str, Any]:
    result: dict[str, Any] = {
        "ok": False,
        "error": {"code": code, "message": message},
    }
    result.update(extra)
    return result


def _load_chapters(course_tools_dir: Path) -> tuple[list[dict[str, Any]] | None, dict[str, Any] | None]:
    data_path = course_tools_dir / "data" / "chapters.json"
    if not data_path.exists():
        return None, _error("DATA_FILE_NOT_FOUND", f"未找到课程章节索引：{data_path}")
    try:
        with data_path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        return None, _error("DATA_LOAD_ERROR", f"读取课程章节索引失败：{exc}")
    chapters = data.get("chapters") if isinstance(data, dict) else None
    if not isinstance(chapters, list):
        return None, _error("DATA_SCHEMA_ERROR", "chapters.json 缺少 chapters 数组。")
    valid = [item for item in chapters if isinstance(item, dict)]
    if len(valid) != len(chapters):
        return None, _error("DATA_SCHEMA_ERROR", "chapters.json 中存在非对象章节记录。")
    return valid, None


def _text_values(chapter: dict[str, Any]) -> Iterable[str]:
    yield str(chapter.get("id", ""))
    title = chapter.get("title", {})
    if isinstance(title, dict):
        yield str(title.get("en", ""))
        yield str(title.get("zh", ""))
    for key in ("aliases", "keywords"):
        values = chapter.get(key, [])
        if isinstance(values, list):
            for value in values:
                yield str(value)
    yield str(chapter.get("summary", ""))


def _matches(chapter: dict[str, Any], query: str | None, lab_no: int | None) -> bool:
    if lab_no is not None and chapter.get("lab_no") != lab_no:
        return False
    if not query:
        return True
    needle = _normalise_key(query)
    values = [_normalise_key(value) for value in _text_values(chapter) if value]
    return any(needle in value or value in needle for value in values)


def _source_paths(chapter: dict[str, Any]) -> list[str]:
    paths: list[str] = []
    for source in chapter.get("sources", []) or []:
        path = source.get("path") if isinstance(source, dict) else source
        if path and str(path) not in paths:
            paths.append(str(path))
    for point in chapter.get("knowledge_points", []) or []:
        if not isinstance(point, dict):
            continue
        for path in point.get("source_files", []) or []:
            if path and str(path) not in paths:
                paths.append(str(path))
    return paths


def _source_checks(course_tools_dir: Path, paths: list[str]) -> list[dict[str, Any]]:
    roots = [
        course_tools_dir.parent / "python-design-pattern-rag",
        course_tools_dir.parent / "python-design-pattern-rag-main",
    ]
    checks: list[dict[str, Any]] = []
    for path in paths:
        matching_root = next((root for root in roots if (root / path).exists()), None)
        checks.append(
            {
                "path": path,
                "exists": matching_root is not None,
                "checked_root": str(matching_root) if matching_root else None,
            }
        )
    return checks


def _chapter_view(chapter: dict[str, Any]) -> dict[str, Any]:
    title = chapter.get("title", {})
    return {
        "id": chapter.get("id"),
        "lab_no": chapter.get("lab_no"),
        "title": title if isinstance(title, dict) else {},
        "aliases": chapter.get("aliases", []),
        "category": chapter.get("category"),
        "pattern_kind": chapter.get("pattern_kind"),
        "summary": chapter.get("summary"),
        "keywords": chapter.get("keywords", []),
        "knowledge_points": chapter.get("knowledge_points", []),
        "sources": _source_paths(chapter),
    }


def build_verified_practice_context(
    *,
    course_tools_dir: str | Path | None = None,
    query: str | None = None,
    lab_no: int | None = None,
    difficulty: str = "中等",
    question_types: Iterable[str] | None = None,
    count: int = 5,
) -> dict[str, Any]:
    """Return a verified chapter context or a structured error.

    No question or answer is generated here.  The separation is intentional:
    this helper verifies the course facts, while the Open WebUI Skill formats
    questions only after the existing lookup Tool has returned those facts.
    """

    base_dir = Path(course_tools_dir) if course_tools_dir else Path(__file__).resolve().parents[2]
    base_dir = base_dir.expanduser().resolve()

    if query is not None and not isinstance(query, str):
        return _error("INVALID_INPUT", "query 必须是字符串。")
    if lab_no is not None and (isinstance(lab_no, bool) or not isinstance(lab_no, int)):
        return _error("INVALID_INPUT", "lab_no 必须是整数。")
    if lab_no is None and (query is None or not query.strip()):
        return _error("INVALID_INPUT", "必须提供 query 或 lab_no，才能确认课程章节。")
    if isinstance(count, bool) or not isinstance(count, int) or count < 1 or count > MAX_COUNT:
        return _error("INVALID_INPUT", f"count 必须是 1 到 {MAX_COUNT} 之间的整数。")

    canonical_difficulty = canonicalize_difficulty(difficulty)
    if canonical_difficulty is None:
        return _error("INVALID_INPUT", "difficulty 必须是 基础、中等 或 进阶。")

    if question_types is None:
        requested_types = list(DEFAULT_QUESTION_TYPES)
    elif isinstance(question_types, str):
        requested_types = [question_types]
    else:
        try:
            requested_types = list(question_types)
        except TypeError:
            return _error("INVALID_INPUT", "question_types 必须是题型字符串列表。")
    canonical_types: list[str] = []
    for item in requested_types:
        canonical = canonicalize_question_type(item)
        if canonical is None:
            return _error("INVALID_INPUT", f"不支持的题型：{item}。")
        if canonical not in canonical_types:
            canonical_types.append(canonical)
    if not canonical_types:
        return _error("INVALID_INPUT", "question_types 不能为空。")

    chapters, load_error = _load_chapters(base_dir)
    if load_error:
        return load_error
    assert chapters is not None

    effective_query = query.strip() if isinstance(query, str) else None
    if lab_no is None and effective_query:
        lab_match = re.fullmatch(r"lab\s*[-_#:]?\s*(\d+)", effective_query, flags=re.IGNORECASE)
        if lab_match:
            lab_no = int(lab_match.group(1))
            effective_query = None

    matches = [chapter for chapter in chapters if _matches(chapter, effective_query, lab_no)]
    request = {
        "query": query,
        "lab_no": lab_no,
        "difficulty": canonical_difficulty,
        "question_types": canonical_types,
        "count": count,
    }

    if not matches:
        suggestions = [
            chapter.get("title", {}).get("en", chapter.get("id"))
            for chapter in chapters[:8]
            if isinstance(chapter.get("title"), dict)
        ]
        return _error(
            "ENTITY_NOT_FOUND",
            "课程资料中未找到/无法确认符合条件的章节。",
            request=request,
            suggestions=suggestions,
        )

    if len(matches) > 1:
        return _error(
            "AMBIGUOUS_QUERY",
            "查询匹配多个课程章节，请补充 Lab 编号或完整主题。",
            request=request,
            candidates=[_chapter_view(chapter) for chapter in matches[:8]],
        )

    chapter = matches[0]
    view = _chapter_view(chapter)
    source_paths = view["sources"]
    source_checks = _source_checks(base_dir, source_paths)
    missing_sources = [item["path"] for item in source_checks if not item["exists"]]

    grounded_context: list[dict[str, Any]] = []
    if view.get("summary"):
        grounded_context.append(
            {
                "kind": "summary",
                "text": view["summary"],
                "source": ["data/chapters.json"],
                "confidence": "confirmed",
            }
        )
    for point in view.get("knowledge_points", []) or []:
        if not isinstance(point, dict):
            continue
        grounded_context.append(
            {
                "kind": "knowledge_point",
                "id": point.get("id"),
                "text": point.get("text"),
                "evidence": point.get("evidence"),
                "source": point.get("source_files", []),
                "confidence": point.get("confidence"),
            }
        )

    warnings = []
    if missing_sources:
        warnings.append(
            "索引登记了来源文件，但当前工作区未找到正文；只能依据已返回的课程索引，不能补全正文事实。"
        )

    return {
        "ok": True,
        "request": request,
        "chapter": view,
        "grounded_context": grounded_context,
        "sources": ["data/chapters.json", *source_paths],
        "source_checks": source_checks,
        "warnings": warnings,
        "generation_policy": [
            "只使用 grounded_context 和实际 RAG 返回的课程正文。",
            "课程资料中未找到/无法确认的内容不得由模型常识补全。",
            "隐藏答案时不得通过解释、选项顺序或提示泄露答案。",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build verified context for course_practice_generator.")
    parser.add_argument("--course-tools-dir", default=str(Path(__file__).resolve().parents[2]))
    parser.add_argument("--query")
    parser.add_argument("--lab-no", type=int)
    parser.add_argument("--difficulty", default="中等")
    parser.add_argument("--question-type", dest="question_types", action="append")
    parser.add_argument("--count", type=int, default=5)
    args = parser.parse_args(argv)

    result = build_verified_practice_context(
        course_tools_dir=args.course_tools_dir,
        query=args.query,
        lab_no=args.lab_no,
        difficulty=args.difficulty,
        question_types=args.question_types,
        count=args.count,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
