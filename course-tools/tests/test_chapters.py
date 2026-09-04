import unittest

from course_tools.chapters import course_chapter_lookup


class ChapterLookupTests(unittest.TestCase):
    def test_exact_title_lookup(self):
        result = course_chapter_lookup(query="Observer")
        self.assertTrue(result["ok"])
        self.assertEqual(result["count"], 1)
        self.assertEqual(result["results"][0]["id"], "lab-05-observer")
        self.assertEqual(result["results"][0]["lab_no"], 5)
        self.assertEqual(result["results"][0]["category"], "behavioral")
        self.assertEqual(result["results"][0]["pattern_kind"], "gof")
        self.assertIn("labs/behavioral_observer.md", result["results"][0]["sources"])

    def test_category_filter(self):
        result = course_chapter_lookup(category="creational", limit=20)
        self.assertTrue(result["ok"])
        self.assertEqual(result["count"], 8)
        lab_numbers = [item["lab_no"] for item in result["results"]]
        self.assertEqual(lab_numbers, list(range(11, 19)))

    def test_lab_no_filter(self):
        result = course_chapter_lookup(lab_no=28)
        self.assertTrue(result["ok"])
        self.assertEqual(result["results"][0]["id"], "lab-28-three-tier")
        self.assertEqual(result["results"][0]["pattern_kind"], "architecture")

    def test_pattern_kind_filter(self):
        result = course_chapter_lookup(pattern_kind="python_idiom", limit=20)
        self.assertTrue(result["ok"])
        self.assertEqual(result["count"], 6)
        for item in result["results"]:
            self.assertEqual(item["pattern_kind"], "python_idiom")

    def test_no_match_returns_suggestions(self):
        result = course_chapter_lookup(query="zzz-not-a-pattern")
        self.assertTrue(result["ok"])
        self.assertEqual(result["count"], 0)
        self.assertTrue(result["suggestions"])

    def test_invalid_category(self):
        result = course_chapter_lookup(category="bogus")
        self.assertFalse(result["ok"])
        self.assertEqual(result["error"]["code"], "INVALID_INPUT")

    def test_invalid_limit(self):
        result = course_chapter_lookup(query="Observer", limit=0)
        self.assertFalse(result["ok"])
        self.assertEqual(result["error"]["code"], "INVALID_INPUT")

    def test_knowledge_points_included(self):
        result = course_chapter_lookup(query="Observer", include_knowledge_points=True)
        self.assertTrue(result["ok"])
        self.assertTrue(result["results"][0]["knowledge_points"])

    def test_no_question_bank_fields(self):
        result = course_chapter_lookup(query="Observer", include_knowledge_points=True)
        payload = result["results"][0]
        self.assertNotIn("options", payload)
        self.assertNotIn("correct_answer", payload)
        self.assertNotIn("score", payload)


if __name__ == "__main__":
    unittest.main()

