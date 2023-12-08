import unittest

from insight_cli.utils.string_matcher import StringMatcher


class TestStringMatcher(unittest.TestCase):
    def setUp(self):
        StringMatcher._cache["_raise_for_invalid_regex_patterns"] = {}

    def test_raise_for_invalid_regex_patterns_with_no_cache_usage_and_invalid_patterns(self) -> None:
        invalid_patterns = ["*.", ".venv"]
        with self.assertRaises(ValueError) as context_manager:
            StringMatcher._raise_for_invalid_regex_patterns(invalid_patterns)
            self.assertTrue(str(context_manager.exception).startswith(f"*. is an invalid regex pattern."))
        self.assertEqual(len(StringMatcher._cache["_raise_for_invalid_regex_patterns"]), 1)
        self.assertIsNotNone(StringMatcher._cache["_raise_for_invalid_regex_patterns"][tuple(invalid_patterns)])

    def test_raise_for_invalid_regex_patterns_with_no_cache_usage_and_valid_regex_patterns(self) -> None:
        valid_patterns = [".git", ".venv"]
        StringMatcher._raise_for_invalid_regex_patterns(valid_patterns)
        self.assertEqual(len(StringMatcher._cache["_raise_for_invalid_regex_patterns"]), 1)
        self.assertIsNone(StringMatcher._cache["_raise_for_invalid_regex_patterns"][tuple(valid_patterns)])

    def test_raise_for_invalid_regex_patterns_with_cache_usage_and_invalid_patterns(self) -> None:
        invalid_patterns = ["*.", ".venv"]
        with self.assertRaises(ValueError) as context_manager:
            for _ in range(3):
                StringMatcher._raise_for_invalid_regex_patterns(invalid_patterns)
                self.assertTrue(str(context_manager.exception).startswith(f"*. is an invalid regex pattern."))

        self.assertEqual(len(StringMatcher._cache["_raise_for_invalid_regex_patterns"]), 1)
        self.assertIsNotNone(StringMatcher._cache["_raise_for_invalid_regex_patterns"][tuple(invalid_patterns)])

    def test_raise_for_invalid_regex_patterns_with_cache_usage_and_valid_patterns(self) -> None:
        valid_patterns = [".git", ".venv"]
        for _ in range(3):
            StringMatcher._raise_for_invalid_regex_patterns(valid_patterns)
        self.assertEqual(len(StringMatcher._cache["_raise_for_invalid_regex_patterns"]), 1)
        self.assertIsNone(StringMatcher._cache["_raise_for_invalid_regex_patterns"][tuple(valid_patterns)])

    def test_raise_for_invalid_regex_patterns_with_cache_usage_and_invalid_and_valid_patterns(
        self
    ) -> None:
        invalid_patterns = ["*.", ".venv"]
        with self.assertRaises(ValueError) as context_manager:
            for _ in range(3):
                StringMatcher._raise_for_invalid_regex_patterns(invalid_patterns)
                self.assertTrue(str(context_manager.exception).startswith(f"*. is an invalid regex pattern."))

        self.assertEqual(len(StringMatcher._cache["_raise_for_invalid_regex_patterns"]), 1)
        self.assertIsNotNone(StringMatcher._cache["_raise_for_invalid_regex_patterns"][tuple(invalid_patterns)])

        valid_patterns = [".git", ".venv"]
        for _ in range(3):
            StringMatcher._raise_for_invalid_regex_patterns(valid_patterns)
        self.assertEqual(len(StringMatcher._cache["_raise_for_invalid_regex_patterns"]), 2)
        self.assertIsNone(StringMatcher._cache["_raise_for_invalid_regex_patterns"][tuple(valid_patterns)])

    def test_matches_any_regex_pattern_with_no_patterns(self) -> None:
        string = ''
        patterns = []
        self.assertFalse(StringMatcher.matches_any_regex_pattern(string, patterns))

    def test_matches_any_regex_pattern_with_invalid_patterns(self) -> None:
        string = ''
        invalid_patterns = ["*.", ".venv"]
        with self.assertRaises(ValueError) as context_manager:
            StringMatcher.matches_any_regex_pattern(string, invalid_patterns)
            self.assertTrue(str(context_manager.exception).startswith(f"*. is an invalid regex pattern."))
        self.assertEqual(len(StringMatcher._cache["_raise_for_invalid_regex_patterns"]), 1)
        self.assertIsNotNone(StringMatcher._cache["_raise_for_invalid_regex_patterns"][tuple(invalid_patterns)])

    def test_matches_any_regex_pattern_with_no_matching_patterns(self) -> None:
        string = 'water'
        patterns = [".*water_"]
        self.assertFalse(StringMatcher.matches_any_regex_pattern(string, patterns))
        self.assertEqual(len(StringMatcher._cache["_raise_for_invalid_regex_patterns"]), 1)
        self.assertIsNone(StringMatcher._cache["_raise_for_invalid_regex_patterns"][tuple(patterns)])

    def test_matches_any_regex_pattern_with_matching_patterns(self) -> None:
        string = '__init__.cpython-39'
        patterns = [".git", ".*cpython.*"]
        self.assertTrue(StringMatcher.matches_any_regex_pattern(string, patterns))
        self.assertEqual(len(StringMatcher._cache["_raise_for_invalid_regex_patterns"]), 1)
        self.assertIsNone(StringMatcher._cache["_raise_for_invalid_regex_patterns"][tuple(patterns)])


if __name__ == "__main__":
    unittest.main()
