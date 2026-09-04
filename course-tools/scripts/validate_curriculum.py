"""Validate chapters.json and prerequisites.json against the knowledge base.

The script checks structural constraints, cross references, forbidden
question-bank fields, and optionally verifies that every source path exists in
the cloned ``python-design-pattern-rag`` repository.
"""

import argparse
import json
import sys
from pathlib import Path


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from course_tools.repository import (  # noqa: E402
    VALID_CATEGORIES,
    VALID_KNOWLEDGE_POINT_TYPES,
    VALID_PATTERN_KINDS,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
CHAPTERS_PATH = DATA_DIR / "chapters.json"
PREREQUISITES_PATH = DATA_DIR / "prerequisites.json"
DEFAULT_REPO_ROOT = PROJECT_ROOT.parent / "python-design-pattern-rag"

FORBIDDEN_FIELDS = {
    "options",
    "correct_answer",
    "score",
    "answer",
    "answers",
    "difficulty",
    "question_type",
}


def _load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _add(errors, message):
    errors.append(message)


def _check_forbidden(errors, obj, context):
    for field in FORBIDDEN_FIELDS:
        if field in obj:
            _add(errors, f"{context} 包含题库字段 {field!r}")


def _validate_chapters(chapters, errors):
    if not isinstance(chapters, list):
        _add(errors, "chapters.json 根节点的 chapters 必须是数组")
        return []

    if len(chapters) != 28:
        _add(errors, f"chapters.json 应包含 28 个 Lab，实际为 {len(chapters)}")

    ids = set()
    lab_numbers = []
    for chapter in chapters:
        chapter_id = chapter.get("id")
        if not chapter_id:
            _add(errors, "存在缺少 id 的章节对象")
            continue
        if chapter_id in ids:
            _add(errors, f"章节 id 重复: {chapter_id}")
        ids.add(chapter_id)

        lab_no = chapter.get("lab_no")
        if not isinstance(lab_no, int) or isinstance(lab_no, bool):
            _add(errors, f"{chapter_id}: lab_no 必须是整数")
        else:
            lab_numbers.append(lab_no)

        title = chapter.get("title") or {}
        if not title.get("en") or not title.get("zh"):
            _add(errors, f"{chapter_id}: title 必须同时包含 en 和 zh")

        if chapter.get("category") not in VALID_CATEGORIES:
            _add(errors, f"{chapter_id}: 无效 category {chapter.get('category')!r}")
        if chapter.get("pattern_kind") not in VALID_PATTERN_KINDS:
            _add(errors, f"{chapter_id}: 无效 pattern_kind {chapter.get('pattern_kind')!r}")

        sources = chapter.get("sources", [])
        if not sources:
            _add(errors, f"{chapter_id}: sources 不能为空")
        for source in sources:
            if not isinstance(source, dict) or not source.get("path"):
                _add(errors, f"{chapter_id}: source 必须包含 path")

        _check_forbidden(errors, chapter, chapter_id)

        for kp in chapter.get("knowledge_points", []):
            kp_id = kp.get("id", "<missing>")
            if kp.get("type") not in VALID_KNOWLEDGE_POINT_TYPES:
                _add(errors, f"{chapter_id}/{kp_id}: 无效知识点类型 {kp.get('type')!r}")
            if not kp.get("text"):
                _add(errors, f"{chapter_id}/{kp_id}: 知识点缺少 text")
            if not kp.get("source_files"):
                _add(errors, f"{chapter_id}/{kp_id}: 知识点缺少 source_files")
            _check_forbidden(errors, kp, f"{chapter_id}/{kp_id}")

    expected = list(range(1, 29))
    if sorted(lab_numbers) != expected:
        _add(errors, f"lab_no 应连续覆盖 1..28，实际为 {sorted(lab_numbers)}")

    return sorted(ids)


def _validate_prerequisites(data, chapter_ids, errors):
    confirmed = data.get("confirmed_prerequisites")
    if confirmed != []:
        _add(errors, "prerequisites.json 的 confirmed_prerequisites 必须为空数组")

    for section in ("related", "unconfirmed"):
        for relation in data.get(section, []):
            relation_id = relation.get("id", "<missing>")
            for endpoint in ("target", "prerequisite"):
                value = relation.get(endpoint)
                if value not in chapter_ids:
                    _add(errors, f"{section}/{relation_id}: {endpoint} 指向不存在的章节 {value!r}")
            if not relation.get("source_files"):
                _add(errors, f"{section}/{relation_id}: 缺少 source_files")
            if not relation.get("evidence"):
                _add(errors, f"{section}/{relation_id}: 缺少 evidence")
            if relation.get("is_confirmed_prerequisite") is not False:
                _add(errors, f"{section}/{relation_id}: is_confirmed_prerequisite 必须为 false")
            _check_forbidden(errors, relation, f"{section}/{relation_id}")

    for item in data.get("foundations", []):
        if not item.get("source_files"):
            _add(errors, f"foundations/{item.get('id', '<missing>')}: 缺少 source_files")
        _check_forbidden(errors, item, f"foundations/{item.get('id', '<missing>')}")

    for item in data.get("unmapped_references", []):
        mentioned = item.get("mentioned_in", [])
        if not mentioned:
            _add(errors, f"unmapped_references/{item.get('id', '<missing>')}: 缺少 mentioned_in")
        _check_forbidden(errors, item, f"unmapped_references/{item.get('id', '<missing>')}")


def _collect_source_paths(chapters, prerequisites):
    paths = []
    for chapter in chapters:
        for source in chapter.get("sources", []):
            paths.append(source.get("path"))
        for kp in chapter.get("knowledge_points", []):
            paths.extend(kp.get("source_files", []))

    for key in ("foundations", "related", "unconfirmed"):
        for item in prerequisites.get(key, []):
            paths.extend(item.get("source_files", []))
    for item in prerequisites.get("unmapped_references", []):
        paths.extend(item.get("mentioned_in", []))
    return paths


def _check_sources(paths, repo_root, errors):
    missing = sorted({path for path in paths if path and not (repo_root / str(path)).exists()})
    for path in missing:
        _add(errors, f"来源文件不存在: {path}")
    return missing


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skip-sources",
        action="store_true",
        help="Skip existence checks for referenced source files.",
    )
    parser.add_argument(
        "--repo-root",
        default=str(DEFAULT_REPO_ROOT),
        help="Path to the python-design-pattern-rag checkout.",
    )
    args = parser.parse_args(argv)

    errors = []
    chapters_data = _load_json(CHAPTERS_PATH)
    prerequisites_data = _load_json(PREREQUISITES_PATH)

    chapters = chapters_data.get("chapters", [])
    chapter_ids = _validate_chapters(chapters, errors)
    _validate_prerequisites(prerequisites_data, chapter_ids, errors)

    if not args.skip_sources:
        paths = _collect_source_paths(chapters, prerequisites_data)
        _check_sources(paths, Path(args.repo_root), errors)

    if errors:
        print(f"校验失败：发现 {len(errors)} 个问题")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(
        f"校验通过：{len(chapters)} 个章节，"
        f"confirmed_prerequisites={len(prerequisites_data.get('confirmed_prerequisites', []))}，"
        f"related={len(prerequisites_data.get('related', []))}，"
        f"unconfirmed={len(prerequisites_data.get('unconfirmed', []))}。"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

