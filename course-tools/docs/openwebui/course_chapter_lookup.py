"""
title: Course Chapter Lookup
description: 查询 Python 设计模式课程的章节、Lab、知识点和来源文件。
author: course-tools
version: 1.0.0
license: MIT
"""

import json
import os
import sys
from pathlib import Path

from pydantic import BaseModel, Field


class Tools:
    class Valves(BaseModel):
        COURSE_TOOLS_DIR: str = Field(
            default=r"D:\Focusly\course-tools",
            description="course-tools 项目目录的绝对路径",
        )

    def __init__(self):
        self.valves = self.Valves()

    def _resolve_course_tools_dir(self) -> str:
        candidates = []

        if self.valves.COURSE_TOOLS_DIR:
            candidates.append(self.valves.COURSE_TOOLS_DIR)

        env_value = os.environ.get("COURSE_TOOLS_DIR", "")
        if env_value:
            candidates.append(env_value)

        for candidate in candidates:
            path = Path(candidate)
            if (path / "data" / "chapters.json").exists():
                return str(path)

        return ""

    def course_chapter_lookup(
        self,
        query: str = "",
        lab_no: int = 0,
        category: str = "",
        pattern_kind: str = "",
        limit: int = 10,
    ) -> str:
        """
        查询课程章节信息。

        :param query: 章节名称、英文名称、中文名称或关键词，例如 Abstract Factory、抽象工厂
        :param lab_no: Lab 编号，例如 11
        :param category: 分类，可选
        :param pattern_kind: 模式类型，可选
        :param limit: 最多返回多少条结果
        """

        course_tools_dir = self._resolve_course_tools_dir()

        if not course_tools_dir:
            return json.dumps(
                {
                    "ok": False,
                    "error": {
                        "code": "DATA_FILE_NOT_FOUND",
                        "message": "未找到 course-tools/data/chapters.json。",
                    },
                },
                ensure_ascii=False,
                indent=2,
            )

        data_file = (
            Path(course_tools_dir)
            / "data"
            / "chapters.json"
        )

        try:
            with open(data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            return json.dumps(
                {
                    "ok": False,
                    "error": {
                        "code": "DATA_LOAD_ERROR",
                        "message": f"读取课程章节数据失败：{e}",
                    },
                },
                ensure_ascii=False,
                indent=2,
            )

        chapters = data.get("chapters", [])

        results = []

        query_lower = query.strip().lower()

        for chapter in chapters:
            matched = False

            # Lab 编号匹配
            if lab_no:
                chapter_lab_no = chapter.get("lab_no")

                try:
                    if int(chapter_lab_no) == int(lab_no):
                        matched = True
                except (TypeError, ValueError):
                    pass

            # 关键词匹配
            if query_lower:
                searchable = []

                for key in [
                    "id",
                    "title",
                    "title_en",
                    "title_zh",
                    "name",
                    "description",
                    "category",
                    "pattern_kind",
                ]:
                    value = chapter.get(key)
                    if value:
                        searchable.append(str(value).lower())

                aliases = chapter.get("aliases", [])
                if isinstance(aliases, list):
                    searchable.extend(
                        str(x).lower() for x in aliases
                    )

                knowledge_points = chapter.get(
                    "knowledge_points", []
                )
                if isinstance(knowledge_points, list):
                    searchable.extend(
                        str(x).lower()
                        for x in knowledge_points
                    )

                if any(query_lower in text for text in searchable):
                    matched = True

            # 分类过滤
            if category:
                if str(chapter.get("category", "")).lower() != category.lower():
                    matched = False

            # 模式类型过滤
            if pattern_kind:
                if (
                    str(chapter.get("pattern_kind", "")).lower()
                    != pattern_kind.lower()
                ):
                    matched = False

            if matched:
                results.append(chapter)

        if not results:
            return json.dumps(
                {
                    "ok": False,
                    "error": {
                        "code": "ENTITY_NOT_FOUND",
                        "message": "本地课程索引未找到符合条件的章节。",
                    },
                    "query": {
                        "query": query,
                        "lab_no": lab_no,
                    },
                },
                ensure_ascii=False,
                indent=2,
            )

        results = results[:max(1, min(limit, 50))]

        return json.dumps(
            {
                "ok": True,
                "count": len(results),
                "results": results,
                "source": "data/chapters.json",
            },
            ensure_ascii=False,
            indent=2,
        )
