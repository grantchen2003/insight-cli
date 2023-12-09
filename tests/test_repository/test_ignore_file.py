from pathlib import Path
import tempfile, unittest

from insight_cli.repository.ignore_file import IgnoreFile


class TestIgnoreFile(unittest.TestCase):
    def setUp(self):
        self._temp_dir = tempfile.TemporaryDirectory()
        self._temp_dir_path = Path(self._temp_dir.name)

    def tearDown(self):
        self._temp_dir.cleanup()

    def test_is_valid_with_invalid_path(self) -> None:
        ignore_file = IgnoreFile(self._temp_dir_path)
        self.assertFalse(ignore_file.is_valid)

    def test_is_valid_with_valid_path(self) -> None:
        ignore_file = IgnoreFile(self._temp_dir_path)
        ignore_file._path.touch()
        self.assertTrue(ignore_file.is_valid)

    def test_names_with_invalid_path(self) -> None:
        ignore_file = IgnoreFile(self._temp_dir_path)
        self.assertDictEqual(
            ignore_file.regex_patterns, {"directory": set(), "file": set()}
        )

    def test_names_with_path_to_empty_file(self) -> None:
        ignore_file = IgnoreFile(self._temp_dir_path)
        ignore_file._path.touch()
        self.assertDictEqual(
            ignore_file.regex_patterns, {"directory": set(), "file": set()}
        )

    def test_names_with_path_to_non_empty_file(self) -> None:
        ignore_file = IgnoreFile(self._temp_dir_path)
        with open(ignore_file._path, "w") as file:
            file.write("hello\nworld")
        self.assertSetEqual(ignore_file.regex_patterns["directory"], {"hello", "world"})
        self.assertSetEqual(ignore_file.regex_patterns["file"], {"hello", "world"})

    def test_names_with_path_to_file_with_comments(self) -> None:
        ignore_file = IgnoreFile(self._temp_dir_path)
        with open(ignore_file._path, "w") as file:
            file.write(
                "\n".join(
                    ["#", "# comment", "#", "\#", ".venv", ".git # a", "\# a # is"]
                )
            )
        self.assertSetEqual(
            ignore_file.regex_patterns["directory"],
            {"#", ".venv", ".git # a", "# a # is"},
        )
        self.assertSetEqual(
            ignore_file.regex_patterns["file"], {"#", ".venv", ".git # a", "# a # is"}
        )


if __name__ == "__main__":
    unittest.main()
