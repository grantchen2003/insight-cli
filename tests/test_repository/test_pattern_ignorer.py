from pathlib import Path
import re, tempfile, unittest

from insight_cli.repository.pattern_ignorer import PatternIgnorer, Manager


class TestPatternIgnorer(unittest.TestCase):
    def setUp(self):
        self._temp_dir = tempfile.TemporaryDirectory()
        self._temp_dir_path = Path(self._temp_dir.name)

    def tearDown(self):
        self._temp_dir.cleanup()

    def test_regex_patterns_with_invalid_path(self) -> None:
        pattern_ignorer = PatternIgnorer(self._temp_dir_path)
        self.assertDictEqual(
            pattern_ignorer.regex_patterns,
            {
                "directory": {re.compile(re.escape(Manager.name)).pattern},
                "file": {re.compile(re.escape(PatternIgnorer._FILE_NAME)).pattern},
            },
        )

    def test_regex_patterns_with_path_to_empty_file(self) -> None:
        pattern_ignorer = PatternIgnorer(self._temp_dir_path)
        pattern_ignorer._path.touch()
        self.assertDictEqual(
            pattern_ignorer.regex_patterns,
            {
                "directory": {re.compile(re.escape(Manager.name)).pattern},
                "file": {re.compile(re.escape(PatternIgnorer._FILE_NAME)).pattern},
            },
        )

    def test_regex_patterns_with_path_to_non_empty_file(self) -> None:
        pattern_ignorer = PatternIgnorer(self._temp_dir_path)
        with open(pattern_ignorer._path, "w") as file:
            file.write("hello\nworld")
        self.assertSetEqual(
            pattern_ignorer.regex_patterns["directory"],
            {re.compile(re.escape(Manager.name)).pattern, "hello", "world"},
        )
        self.assertSetEqual(
            pattern_ignorer.regex_patterns["file"],
            {
                re.compile(re.escape(PatternIgnorer._FILE_NAME)).pattern,
                "hello",
                "world",
            },
        )

    def test_regex_patterns_with_path_to_file_with_comments(self) -> None:
        pattern_ignorer = PatternIgnorer(self._temp_dir_path)

        with open(pattern_ignorer._path, "w") as file:
            file.write(
                "\n".join(
                    [
                        "#",
                        "# comment",
                        "#",
                        r"\#",
                        ".venv",
                        ".git # a",
                        r"\# a # is",
                    ]
                )
            )

        self.assertSetEqual(
            pattern_ignorer.regex_patterns["directory"],
            {
                re.compile(re.escape(Manager.name)).pattern,
                ".venv",
                ".git # a",
                "# a # is",
                "#",
            },
        )
        self.assertSetEqual(
            pattern_ignorer.regex_patterns["file"],
            {
                re.compile(re.escape(PatternIgnorer._FILE_NAME)).pattern,
                ".venv",
                ".git # a",
                "# a # is",
                "#",
            },
        )

    def test_regex_patterns_with_path_to_file_with_scope(self) -> None:
        pattern_ignorer = PatternIgnorer(self._temp_dir_path)
        with open(pattern_ignorer._path, "w") as file:
            file.write(
                "\n".join(
                    [
                        "pattern1",
                        "pattern2",
                        "#",
                        "",
                        "# comment",
                        "## _directory_",
                        "dir_pattern1",
                        "## comment",
                        "dir_pattern2",
                        "## _file_",
                        "file_pattern1",
                        "##",
                        "## _directory_",
                        "dir_pattern3",
                        "## _file_",
                        "file_pattern2",
                    ]
                )
            )

        self.assertSetEqual(
            pattern_ignorer.regex_patterns["directory"],
            {
                re.compile(re.escape(Manager.name)).pattern,
                "pattern1",
                "pattern2",
                "dir_pattern1",
                "dir_pattern2",
                "dir_pattern3",
            },
        )
        self.assertSetEqual(
            pattern_ignorer.regex_patterns["file"],
            {
                re.compile(re.escape(PatternIgnorer._FILE_NAME)).pattern,
                "pattern1",
                "pattern2",
                "file_pattern1",
                "file_pattern2",
            },
        )


if __name__ == "__main__":
    unittest.main()
