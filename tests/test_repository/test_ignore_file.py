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
        self.assertEqual(ignore_file.names, set())

    def test_names_with_path_to_empty_file(self) -> None:
        ignore_file = IgnoreFile(self._temp_dir_path)
        ignore_file._path.touch()
        self.assertEqual(ignore_file.names, set())

    def test_names_with_path_to_non_empty_file(self) -> None:
        ignore_file = IgnoreFile(self._temp_dir_path)
        with open(ignore_file._path, "w") as file:
            file.write("hello\nworld")
        self.assertEqual(ignore_file.names, {"hello", "world"})


if __name__ == "__main__":
    unittest.main()
