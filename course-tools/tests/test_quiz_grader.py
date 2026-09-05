import importlib.util
import unittest
from pathlib import Path


GRADER_PATH = (
    Path(__file__).resolve().parents[1]
    / "mcp"
    / "course_quiz_grader"
    / "grader.py"
)
SPEC = importlib.util.spec_from_file_location("course_quiz_grader", GRADER_PATH)
assert SPEC and SPEC.loader
grader = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(grader)


class QuizGraderTests(unittest.TestCase):
    def test_single_choice_case_and_punctuation_normalization(self):
        result = grader.grade_quiz_answer("题目", "choice", "B", " b. ")
        self.assertTrue(result["ok"])
        self.assertTrue(result["correct"])
        self.assertEqual(result["score"], 1)

    def test_wrong_single_choice_is_not_correct(self):
        result = grader.grade_quiz_answer("题目", "单选题", "B", "A")
        self.assertTrue(result["ok"])
        self.assertFalse(result["correct"])
        self.assertEqual(result["score"], 0)

    def test_true_false_chinese_and_english(self):
        result = grader.grade_quiz_answer("题目", "判断题", "对", "True")
        self.assertTrue(result["correct"])
        result = grader.grade_quiz_answer("题目", "true_false", "False", "错")
        self.assertTrue(result["correct"])

    def test_multiple_choice_is_order_independent(self):
        result = grader.grade_quiz_answer("题目", "多选题", "A,C", "c、a")
        self.assertTrue(result["ok"])
        self.assertTrue(result["correct"])
        self.assertEqual(result["normalized_student_answer"], ["A", "C"])

    def test_empty_student_answer_is_a_zero_score(self):
        result = grader.grade_quiz_answer("题目", "choice", "B", "   ")
        self.assertTrue(result["ok"])
        self.assertFalse(result["correct"])
        self.assertEqual(result["score"], 0)
        self.assertIn("未作答", result["feedback"])

    def test_invalid_student_answer_returns_error(self):
        result = grader.grade_quiz_answer("题目", "choice", "B", "hello!")
        self.assertFalse(result["ok"])
        self.assertEqual(result["error"]["code"], "INVALID_STUDENT_ANSWER")

    def test_missing_standard_answer_returns_error(self):
        result = grader.grade_quiz_answer("题目", "choice", "", "A")
        self.assertFalse(result["ok"])
        self.assertEqual(result["error"]["code"], "MISSING_STANDARD_ANSWER")

    def test_unsupported_question_type_returns_error(self):
        result = grader.grade_quiz_answer("题目", "代码阅读", "B", "B")
        self.assertFalse(result["ok"])
        self.assertEqual(result["error"]["code"], "UNSUPPORTED_QUESTION_TYPE")

    def test_invalid_question_and_standard_formats(self):
        result = grader.grade_quiz_answer("", "choice", "B", "B")
        self.assertFalse(result["ok"])
        self.assertEqual(result["error"]["code"], "INVALID_INPUT")

        result = grader.grade_quiz_answer("题目", "choice", "A,C", "A")
        self.assertFalse(result["ok"])
        self.assertEqual(result["error"]["code"], "INVALID_STANDARD_ANSWER")

    def test_explanation_and_source_are_preserved(self):
        result = grader.grade_quiz_answer(
            "题目",
            "choice",
            "B",
            "B",
            explanation="课程索引中的说明。",
            source="data/chapters.json",
        )
        self.assertEqual(result["explanation"], "课程索引中的说明。")
        self.assertEqual(result["source"], "data/chapters.json")
        self.assertIn("课程索引中的说明", result["feedback"])


if __name__ == "__main__":
    unittest.main()

