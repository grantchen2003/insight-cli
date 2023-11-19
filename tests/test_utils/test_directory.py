from datetime import datetime
from pathlib import Path

import sys
import unittest


NUM_PARENT_DIRECTORIES_TO_PROJECT_ROOT = 2
project_root_path = (
    Path(__file__).resolve().parents[NUM_PARENT_DIRECTORIES_TO_PROJECT_ROOT]
)

sys.path.append(str(project_root_path))

from src.utils.directory import Directory, File


class TestDirectory(unittest.TestCase):
    def test_add_file(self) -> None:
        directory = Directory("example_directory", datetime.now())
        file = File("example_file", datetime.now(), ["example_content"])
        directory.add_file(file)
        self.assertIn(file, directory._files)

        directory = Directory("example_directory", datetime.now())
        file1 = File("example_file1", datetime.now(), ["example_content"])
        file2 = File("example_file2", datetime.now(), ["example_content"])
        directory.add_file(file1)
        directory.add_file(file2)
        self.assertIn(file1, directory._files)
        self.assertIn(file2, directory._files)

    def test_add_subdirectory(self) -> None:
        directory = Directory("example_directory", datetime.now())
        subdirectory = Directory("example_subdirectory", datetime.now())
        directory.add_subdirectory(subdirectory)
        self.assertIn(subdirectory, directory._subdirectories)

        directory = Directory("example_directory", datetime.now())
        subdirectory1 = Directory("example_subdirectory1", datetime.now())
        subdirectory2 = Directory("example_subdirectory2", datetime.now())
        directory.add_subdirectory(subdirectory1)
        directory.add_subdirectory(subdirectory2)
        self.assertIn(subdirectory1, directory._subdirectories)
        self.assertIn(subdirectory2, directory._subdirectories)

    def test_to_dict(self) -> None:
        directory = Directory("example_directory", datetime.now())
        file = File("test_file.txt", datetime.now(), [])
        subdirectory = Directory("example_subdirectory", datetime.now())
        directory.add_file(file)
        directory.add_subdirectory(subdirectory)
        expected_dict = {
            "name": "example_directory",
            "last_updated": datetime.now(),
            "files": [
                {
                    "name": "test_file.txt",
                    "last_updated": datetime.now(),
                    "content": [],
                }
            ],
            "subdirectories": [
                {
                    "name": "example_subdirectory",
                    "last_updated": datetime.now(),
                    "files": [],
                    "subdirectories": [],
                }
            ],
        }
        self.assertEqual(directory.to_dict(), expected_dict)


if __name__ == "__main__":
    unittest.main()
