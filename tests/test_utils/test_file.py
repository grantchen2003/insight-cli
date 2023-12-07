from pathlib import Path
import os
import unittest

from insight_cli.utils.file import File


class TestFile(unittest.TestCase):
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
            name="empty_file_name.txt",
            content=[],
        )

        self.assertEqual(
            empty_file.to_dict(),
            {
                "name": "empty_file_name.txt",
                "content": [],
            },
        )

    def test_to_dict_with_non_empty_file(self) -> None:
        non_empty_file = File(
            name="non_empty_file_name.txt",
            content=["line 1\nline2"],
        )

        self.assertEqual(
            non_empty_file.to_dict(),
            {
                "name": "non_empty_file_name.txt",
                "content": ["line 1\nline2"],
            },
        )


if __name__ == "__main__":
    unittest.main()
