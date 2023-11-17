from pathlib import Path

import sys
import unittest

NUM_PARENT_DIRECTORIES_TO_PROJECT_ROOT = 2
project_root_path = (
    Path(__file__).resolve().parents[NUM_PARENT_DIRECTORIES_TO_PROJECT_ROOT]
)

sys.path.append(str(project_root_path))

from src.utils.directory import Directory

class TestDirectory(unittest. TestCase):
    def test_create_from_path(self):
        pass
    

if __name__ == "__main__":
    unittest.main()
