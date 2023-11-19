from datetime import datetime, timedelta
from pathlib import Path
from src.utils.file import File
from typing import Any

import unittest


class TestFile(unittest.TestCase):
    def is_file_dict_instance(self, variable: Any) -> bool:
        return (
            isinstance(variable, dict)
            and len(variable) == 3
            and "name" in variable
            and "last_updated" in variable
            and "content" in variable
            and isinstance(variable["name"], str)
            and len(variable["name"]) > 0
            and isinstance(variable["last_updated"], datetime)
            and variable["last_updated"] <= datetime.now()
            and isinstance(variable["content"], list)
            and all(isinstance(val, str) for val in variable["content"])
        )

    def test_create_from_path(self) -> None:
        self.assertIsInstance(
            File.create_from_path(Path("./tests/test_utils/test_file.py")), File
        )

        with self.assertRaises(Exception):
            File.create_from_path(Path())
            File.create_from_path(Path("./x.py"))

    def test_to_dict(self) -> None:
        test_cases = [
            {
                "input": 3,
                "output": False,
            },
            {
                "input": File(
                    name="",
                    last_updated=datetime.now(),
                    content=[],
                ),
                "output": False,
            },
            {
                "input": File(
                    name="",
                    last_updated=datetime.now(),
                    content=[],
                ).to_dict(),
                "output": False,
            },
            {
                "input": File(
                    name="water",
                    last_updated=datetime.now() + timedelta(days=1),
                    content=[],
                ).to_dict(),
                "output": False,
            },
            {
                "input": File(
                    name="water",
                    last_updated=datetime.now(),
                    content=[3],
                ).to_dict(),
                "output": False,
            },
            {
                "input": File(
                    name="water",
                    last_updated=datetime.now(),
                    content=[3, "3"],
                ).to_dict(),
                "output": False,
            },
            {
                "input": File(
                    name="water",
                    last_updated=datetime.now(),
                    content=[],
                ).to_dict(),
                "output": True,
            },
            {
                "input": File(
                    name="water",
                    last_updated=datetime.now(),
                    content=["green"],
                ).to_dict(),
                "output": True,
            },
            {
                "input": File(
                    name="water",
                    last_updated=datetime.now(),
                    content=["\n"],
                ).to_dict(),
                "output": True,
            },
        ]

        for test_case in test_cases:
            self.assertEqual(
                self.is_file_dict_instance(test_case["input"]), test_case["output"]
            )


if __name__ == "__main__":
    unittest.main()
