from pathlib import Path
import os, tempfile, unittest

from insight_cli.utils.file import File


class TestFile(unittest.TestCase):
    def setUp(self) -> None:
        self._temp_dir = tempfile.TemporaryDirectory()
        self._temp_dir_path: Path = Path(self._temp_dir.name)

    def tearDown(self):
        self._temp_dir.cleanup()

    def test_create_in_file_system_with_empty_file(self) -> None:
        file_dict: FileDict = {"path": self._temp_dir_path / "example.txt", "lines": []}

        File.create_in_file_system(file_dict)

        self.assertEqual(
            File.create_from_path(file_dict["path"]).to_file_dict(), file_dict
        )

    def test_create_in_file_system_with_non_empty_file(self) -> None:
        file_dict: FileDict = {
            "path": self._temp_dir_path / "example.txt",
            "lines": ["line1", "line2", "line3"],
        }

        File.create_in_file_system(file_dict)

        self.assertEqual(
            File.create_from_path(file_dict["path"]).to_file_dict(), file_dict
        )

    def test_create_from_path_with_empty_path(self) -> None:
        empty_path = Path()

        with self.assertRaises(Exception):
            File.create_from_path(empty_path)

    def test_create_from_path_with_invalid_path(self) -> None:
        invalid_path = Path("./invalid_path.py")

        with self.assertRaises(Exception):
            File.create_from_path(invalid_path)

    def test_create_from_path_with_valid_path(self) -> None:
        current_file_path = Path(os.path.abspath(__file__))

        self.assertIsInstance(File.create_from_path(current_file_path), File)

    def test_to_dict_with_empty_file(self) -> None:
        empty_file = File(
            path=self._temp_dir_path / "empty_file_name.txt",
            lines=[],
        )

        self.assertEqual(
            empty_file.to_file_dict(),
            {
                "path": self._temp_dir_path / "empty_file_name.txt",
                "lines": [],
            },
        )

    def test_to_dict_with_non_empty_file(self) -> None:
        non_empty_file = File(
            path=self._temp_dir_path / "non_empty_file_name.txt",
            lines=["line 1\nline2"],
        )

        self.assertEqual(
            non_empty_file.to_file_dict(),
            {
                "path": self._temp_dir_path / "non_empty_file_name.txt",
                "lines": ["line 1\nline2"],
            },
        )


if __name__ == "__main__":
    unittest.main()
