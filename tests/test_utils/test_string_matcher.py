from unittest.mock import patch
import functools, re, unittest

from insight_cli.utils.string_matcher import StringMatcher


class TestStringMatcher(unittest.TestCase):
    def setUp(self):
        self._original_func = StringMatcher._raise_for_invalid_regex_patterns
        StringMatcher._raise_for_invalid_regex_patterns = (
            StringMatcher._convert_list_args_to_tuple(
                functools.lru_cache(maxsize=None)(self._original_func)
            )
        )
        self._mock_re_compile = patch("re.compile")

    def tearDown(self):
        StringMatcher._raise_for_invalid_regex_patterns = self._original_func
        self._mock_re_compile.stop()

    def test_convert_list_args_to_tuple_with_no_list_args(self) -> None:
        def func(*args):
            return args

        func = StringMatcher._convert_list_args_to_tuple(func)

        self.assertEqual(func(13, "name"), (13, "name"))

    def test_convert_list_args_to_tuple_with_list_args(self) -> None:
        def func(*args):
            return args

        func = StringMatcher._convert_list_args_to_tuple(func)

        self.assertEqual(func(13, "name", [1, 2]), (13, "name", (1, 2)))

    def test_raise_for_invalid_regex_patterns_with_invalid_regex_patterns(self) -> None:
        invalid_patterns = ["*.", ".git"]
        with self.assertRaises(ValueError):
            StringMatcher._raise_for_invalid_regex_patterns(invalid_patterns)

    def test_raise_for_invalid_regex_patterns_with_valid_regex_patterns(self) -> None:
        patterns = ["a*.", ".git"]
        StringMatcher._raise_for_invalid_regex_patterns(patterns)

    @patch("re.compile")
    def test_raise_for_invalid_regex_patterns_with_no_cache_usage_with_valid_patterns(
        self, mock_re_compile
    ) -> None:
        patterns = ["a*.", ".git"]
        StringMatcher._raise_for_invalid_regex_patterns(patterns)
        self.assertEqual(mock_re_compile.call_count, len(patterns))

    @patch("re.compile")
    def test_raise_for_invalid_regex_patterns_with_no_cache_usage_with_invalid_patterns(
        self, mock_re_compile
    ) -> None:
        invalid_patterns = ["*.", "[0-9]++"]
        mock_re_compile.side_effect = re.error("error message")
        with self.assertRaises(ValueError):
            StringMatcher._raise_for_invalid_regex_patterns(invalid_patterns)
        self.assertEqual(mock_re_compile.call_count, 1)

    @patch("re.compile")
    def test_raise_for_invalid_regex_patterns_with_cache_usage_with_invalid_and_valid_patterns(
        self, mock_re_compile
    ) -> None:
        valid_patterns = [".git", "lol"]
        StringMatcher._raise_for_invalid_regex_patterns(valid_patterns)
        self.assertEqual(mock_re_compile.call_count, 2)
        
        invalid_patterns = ["*.", "[0-9]++"]
        mock_re_compile.side_effect = re.error("error message")
        with self.assertRaises(ValueError):
            StringMatcher._raise_for_invalid_regex_patterns(invalid_patterns)
        self.assertEqual(mock_re_compile.call_count, 3)
        
    @patch("re.compile")
    def test_raise_for_invalid_regex_patterns_with_cache_usage_with_valid_patterns(
        self, mock_re_compile
    ) -> None:
        valid_patterns = [".git", "lol"]
        StringMatcher._raise_for_invalid_regex_patterns(valid_patterns)
        self.assertEqual(mock_re_compile.call_count, 2)
        # StringMatcher._raise_for_invalid_regex_patterns(valid_patterns)
        # self.assertEqual(mock_re_compile.call_count, 2)

    # def test_raise_for_invalid_regex_patterns_with_cache_usage_with_invalid_patterns(
    #     self,
    # ) -> None:
    #     pass

    # def test_matches_any_regex_pattern_with_no_patterns(self) -> None:
    #     pass

    # def test_matches_any_regex_pattern_with_no_matching_patterns(self) -> None:
    #     pass

    # def test_matches_any_regex_pattern_with_matching_patterns(self) -> None:
    #     pass


if __name__ == "__main__":
    unittest.main()
