import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load_validator():
    spec = importlib.util.spec_from_file_location(
        "validate_curriculum", ROOT / "scripts" / "validate_curriculum.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ValidationScriptTests(unittest.TestCase):
    def test_validation_passes(self):
        validator = _load_validator()
        self.assertEqual(validator.main([]), 0)


if __name__ == "__main__":
    unittest.main()

