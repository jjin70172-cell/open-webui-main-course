"""
title: Course Knowledge Relation Lookup
description: 查询 Python 设计模式课程的先修关系、相关关系和基础知识。
author: course-tools
version: 1.0.0
license: MIT
"""

import json
import os
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

            if (path / "data" / "prerequisites.json").exists():
                return str(path)

        return ""

    def course_knowledge_relation_lookup(
        self,
        target: str,
        direction: str = "both",
        max_depth: int = 1,
        include_related: bool = True,
        include_unconfirmed: bool = True,
        include_foundations: bool = True,
    ) -> str:
        """
        查询课程知识点的先修关系、相关关系和基础知识。

        :param target: 要查询的知识点，例如“抽象工厂模式”或“Abstract Factory”
        :param direction: 查询方向，可选 prerequisites、dependents、both
        :param max_depth: 递归查询深度
        :param include_related: 是否返回相关知识点
        :param include_unconfirmed: 是否返回未确认关系
        :param include_foundations: 是否返回基础知识
        """

        if not target or not target.strip():
            return json.dumps(
                {
                    "ok": False,
                    "error": {
                        "code": "INVALID_INPUT",
                        "message": "target 不能为空。",
                    },
                },
                ensure_ascii=False,
                indent=2,
            )

        if direction not in {
            "prerequisites",
            "dependents",
            "both",
        }:
            return json.dumps(
                {
                    "ok": False,
                    "error": {
                        "code": "INVALID_INPUT",
                        "message": (
                            "direction 必须是 prerequisites、dependents 或 both。"
                        ),
                    },
                },
                ensure_ascii=False,
                indent=2,
            )

        course_tools_dir = self._resolve_course_tools_dir()

        if not course_tools_dir:
            return json.dumps(
                {
                    "ok": False,
                    "error": {
                        "code": "DATA_FILE_NOT_FOUND",
                        "message": (
                            "未找到 course-tools/data/prerequisites.json。"
                        ),
                    },
                },
                ensure_ascii=False,
                indent=2,
            )

        data_file = (
            Path(course_tools_dir)
            / "data"
            / "prerequisites.json"
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
                        "message": f"读取知识关系数据失败：{e}",
                    },
                },
                ensure_ascii=False,
                indent=2,
            )

        target_lower = target.strip().lower()

        def contains_target(value):
            if isinstance(value, str):
                return target_lower in value.lower()

            if isinstance(value, list):
                return any(
                    target_lower in str(item).lower()
                    for item in value
                )

            return False

        def match_item(item):
            if not isinstance(item, dict):
                return False

            searchable_fields = [
                "target",
                "source",
                "from",
                "to",
                "knowledge_point",
                "name",
                "title",
                "pattern",
                "related",
                "prerequisite",
            ]

            for field in searchable_fields:
                if field in item and contains_target(item[field]):
                    return True

            return False

        result = {
            "ok": True,
            "target": target,
            "confirmed_prerequisites": [],
            "recommended_prerequisites": [],
            "unconfirmed_prerequisites": [],
            "related": [],
            "foundations": [],
            "dependents": [],
            "warnings": [],
            "source": "data/prerequisites.json",
        }

        # 兼容不同的 JSON 字段命名
        relationships = data.get("relationships", [])

        if isinstance(relationships, list):
            for item in relationships:
                if not isinstance(item, dict):
                    continue

                relation_type = str(
                    item.get("type", item.get("relation", ""))
                ).lower()

                if not match_item(item):
                    continue

                if relation_type in {
                    "confirmed",
                    "confirmed_prerequisite",
                    "required",
                }:
                    result["confirmed_prerequisites"].append(item)

                elif relation_type in {
                    "recommended",
                    "recommended_prerequisite",
                }:
                    result["recommended_prerequisites"].append(item)

                elif relation_type in {
                    "unconfirmed",
                    "candidate",
                }:
                    if include_unconfirmed:
                        result["unconfirmed_prerequisites"].append(item)

                elif relation_type in {
                    "related",
                    "comparison",
                    "similar",
                }:
                    if include_related:
                        result["related"].append(item)

                else:
                    if include_unconfirmed:
                        result["unconfirmed_prerequisites"].append(item)

        # foundations 可能是列表，也可能是字典
        foundations = data.get("foundations", [])

        if include_foundations:
            if isinstance(foundations, list):
                for item in foundations:
                    if match_item(item):
                        result["foundations"].append(item)

            elif isinstance(foundations, dict):
                for key, value in foundations.items():
                    item = {
                        "name": key,
                        "value": value,
                    }

                    if match_item(item):
                        result["foundations"].append(item)

        # 当前课程资料没有正式确认的先修关系
        if not result["confirmed_prerequisites"]:
            result["warnings"].append(
                "课程资料未确认该知识点存在正式先修关系，"
                "不能将相关关系或推测性顺序视为强制先修要求。"
            )

        if not any(
            [
                result["confirmed_prerequisites"],
                result["recommended_prerequisites"],
                result["unconfirmed_prerequisites"],
                result["related"],
                result["foundations"],
            ]
        ):
            result["warnings"].append(
                "本地课程索引未找到与该知识点匹配的关系记录。"
            )

        return json.dumps(
            result,
            ensure_ascii=False,
            indent=2,
        )
