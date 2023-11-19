from io import StringIO
from pathlib import Path
from unittest.mock import patch
import os
import shutil
import unittest

from src.core.dot_insightignore_file import get_file_name, get_ignorable_names


class TestDotInsightignoreFile(unittest.TestCase):
    def setUp(self) -> None:
        self.test_temp_folder_path = Path(
            "./tests/test_core/temp_test_dot_insightignore_file"
        )
        if not os.path.exists(self.test_temp_folder_path):
            os.makedirs(self.test_temp_folder_path)

    def tearDown(self):
        shutil.rmtree(self.test_temp_folder_path)

    def test_get_file_name(self) -> None:
        self.assertEqual(get_file_name(), ".insightignore")

    @patch("pathlib.Path.is_file")
    def test_get_ignorable_names(self, mock_is_file) -> None:
        mock_is_file.return_value = False
        dot_insightignore_file_path = Path("non_existent_dot_insightignore_file_path")
        self.assertEqual(get_ignorable_names(dot_insightignore_file_path), set())

        dot_insightignore_file_path: Path = (
            self.test_temp_folder_path / "test_dot_insightignore_file1.txt"
        )
        dot_insightignore_file_content: str = "name1\nname2"
        with open(dot_insightignore_file_path, "w") as dot_insightignore_file:
            dot_insightignore_file.write(dot_insightignore_file_content)
        mock_is_file.return_value = True
        dot_insightignore_file_path = Path(dot_insightignore_file_path)
        self.assertEqual(
            get_ignorable_names(dot_insightignore_file_path), {"name1", "name2"}
        )

        dot_insightignore_file_path: Path = (
            self.test_temp_folder_path / "test_dot_insightignore_file2.txt"
        )
        dot_insightignore_file_content: str = ""
        with open(dot_insightignore_file_path, "w") as dot_insightignore_file:
            dot_insightignore_file.write(dot_insightignore_file_content)
        mock_is_file.return_value = True
        dot_insightignore_file_path = Path(dot_insightignore_file_path)
        self.assertEqual(get_ignorable_names(dot_insightignore_file_path), set())


if __name__ == "__main__":
    unittest.main()
