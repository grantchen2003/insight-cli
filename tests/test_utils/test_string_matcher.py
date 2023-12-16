import unittest

from insight_cli.utils.string_matcher import StringMatcher


class TestStringMatcher(unittest.TestCase):
    def test_matches_any_regex_pattern_with_only_invalid_regex_patterns(
        self,
    ) -> None:
        string = ""
        regex_pattern = {"*abc", "abc|"}

        with self.assertRaises(ValueError) as context_manager:
            StringMatcher.matches_any_regex_pattern(string, regex_pattern)

        self.assertEqual(
            str(context_manager.exception),
            "*abc is an invalid regex pattern. nothing to repeat at position 0",
        )

    def test_matches_any_regex_pattern_with_empty_string_and_no_regex_patterns(
        self,
    ) -> None:
        string = ""
        regex_pattern = set()

        self.assertFalse(StringMatcher.matches_any_regex_pattern(string, regex_pattern))

    def test_matches_any_regex_pattern_with_no_matches(
        self,
    ) -> None:
        string = ".git"
        regex_pattern = {"xgit"}

        self.assertFalse(StringMatcher.matches_any_regex_pattern(string, regex_pattern))

    def test_matches_any_regex_pattern_with_matches(
        self,
    ) -> None:
        string = ".git"
        regex_pattern = {"yo", r"\.git"}

        self.assertTrue(StringMatcher.matches_any_regex_pattern(string, regex_pattern))


if __name__ == "__main__":
    unittest.main()
