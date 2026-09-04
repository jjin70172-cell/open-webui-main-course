import unittest

from course_tools.prerequisites import course_prerequisite_lookup


class PrerequisiteLookupTests(unittest.TestCase):
    def test_confirmed_prerequisites_is_empty(self):
        result = course_prerequisite_lookup(target="Factory Method")
        self.assertTrue(result["ok"])
        self.assertEqual(result["confirmed_prerequisites"], [])
        self.assertEqual(result["counts"]["confirmed_prerequisites"], 0)

    def test_related_and_unconfirmed_relations(self):
        result = course_prerequisite_lookup(target="Factory Method")
        self.assertTrue(result["ok"])
        related_ids = [item["id"] for item in result["related"]]
        unconfirmed_ids = [item["id"] for item in result["unconfirmed"]]
        self.assertIn("rel-factory-method-abstract-factory", related_ids)
        self.assertIn("unconfirmed-factory-method-before-abstract-factory", unconfirmed_ids)
        for item in result["related"]:
            self.assertEqual(item["relation_type"], "related")
            self.assertIn("confidence", item)
            self.assertIn("source_files", item)

    def test_singleton_relations(self):
        result = course_prerequisite_lookup(target="Singleton")
        self.assertTrue(result["ok"])
        related_ids = [item["id"] for item in result["related"]]
        self.assertIn("rel-borg-singleton", related_ids)
        self.assertIn("rel-global-object-singleton", related_ids)

    def test_knowledge_point_id_resolves_to_parent_chapter(self):
        result = course_prerequisite_lookup(target="lab-07-state-kp-comparison")
        self.assertTrue(result["ok"])
        self.assertEqual(result["target"]["id"], "lab-07-state")
        self.assertEqual(result["resolved_via"], "knowledge_point")
        self.assertIsNotNone(result["knowledge_point"])

    def test_missing_target(self):
        result = course_prerequisite_lookup(target="lab-999-missing")
        self.assertFalse(result["ok"])
        self.assertEqual(result["error"]["code"], "ENTITY_NOT_FOUND")

    def test_invalid_direction(self):
        result = course_prerequisite_lookup(target="Observer", direction="bogus")
        self.assertFalse(result["ok"])
        self.assertEqual(result["error"]["code"], "INVALID_INPUT")

    def test_outgoing_direction_limits_relations(self):
        result = course_prerequisite_lookup(target="Factory Method", direction="outgoing")
        self.assertTrue(result["ok"])
        self.assertEqual(result["direction"], "outgoing")

    def test_foundations_included_by_default(self):
        result = course_prerequisite_lookup(target="Observer")
        self.assertTrue(result["ok"])
        self.assertTrue(result["foundations"])
        self.assertEqual(result["foundations"][0]["id"], "foundation-python-familiarity")


if __name__ == "__main__":
    unittest.main()

