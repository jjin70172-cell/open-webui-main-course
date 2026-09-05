import importlib.util
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1] / "skills" / "course_practice_generator"
SPEC = importlib.util.spec_from_file_location("course_practice_skill_validator", SKILL_DIR / "validate_skill.py")
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class PracticeSkillContextTests(unittest.TestCase):
    def test_lab_context_is_grounded_in_index(self):
        result = validator.build_verified_practice_context(
            lab_no=11,
            difficulty="medium",
            question_types=["选择题", "代码阅读"],
            count=5,
        )
        self.assertTrue(result["ok"])
        self.assertEqual(result["chapter"]["lab_no"], 11)
        self.assertEqual(result["request"]["difficulty"], "中等")
        self.assertEqual(result["request"]["question_types"], ["choice", "code_reading"])
        self.assertIn("labs/creational_abstract_factory.md", result["sources"])
        self.assertTrue(any(item["kind"] == "knowledge_point" for item in result["grounded_context"]))

    def test_query_can_resolve_chinese_alias(self):
        result = validator.build_verified_practice_context(query="抽象工厂", difficulty="进阶")
        self.assertTrue(result["ok"])
        self.assertEqual(result["chapter"]["title"]["en"], "Abstract Factory")
        self.assertEqual(result["request"]["difficulty"], "进阶")

    def test_all_supported_difficulties_are_normalized(self):
        for value in ("基础", "medium", "进阶"):
            with self.subTest(value=value):
                result = validator.build_verified_practice_context(lab_no=11, difficulty=value)
                self.assertTrue(result["ok"])
        self.assertEqual(
            validator.build_verified_practice_context(lab_no=11, difficulty="基础")["request"]["difficulty"],
            "基础",
        )

    def test_missing_chapter_is_explicit(self):
        result = validator.build_verified_practice_context(query="不存在的课程章节")
        self.assertFalse(result["ok"])
        self.assertEqual(result["error"]["code"], "ENTITY_NOT_FOUND")
        self.assertIn("课程资料中未找到/无法确认", result["error"]["message"])

    def test_ambiguous_query_does_not_generate(self):
        result = validator.build_verified_practice_context(query="factory")
        self.assertFalse(result["ok"])
        self.assertEqual(result["error"]["code"], "AMBIGUOUS_QUERY")

    def test_invalid_request_is_explicit(self):
        result = validator.build_verified_practice_context(lab_no=11, difficulty="专家")
        self.assertFalse(result["ok"])
        self.assertEqual(result["error"]["code"], "INVALID_INPUT")

    def test_skill_requires_real_lookup_tool(self):
        content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("course_chapter_lookup", content)
        self.assertIn("knowledge_points", content)
        self.assertIn("课程资料中未找到/无法确认", content)
        self.assertIn("grade_quiz_answer", content)


if __name__ == "__main__":
    unittest.main()
