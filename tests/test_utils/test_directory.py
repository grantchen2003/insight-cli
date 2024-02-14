from datetime import datetime
from pathlib import Path
import os, tempfile, unittest

from insight_cli.utils.directory import Directory, File


class TestDirectory(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_dir_path = Path(self.temp_dir.name)

        files = [
            ("file1.py", "content1"),
            ("file2.py", "content2"),
            ("subdir/file3.py", "content3"),
            ("subdir/file4.py", "content4"),
            ("subdir/file5.py", "content5"),
            ("subdir1/file3.py", "content6"),
        ]

        for file_path, file_content in files:
            (self.temp_dir_path / file_path).parent.mkdir(parents=True, exist_ok=True)
            with open(self.temp_dir_path / file_path, "w") as f:
                f.write(file_content)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_files(self) -> None:
        self.assertEqual(
            Directory(
                self.temp_dir_path,
                {"directory": {"subdir1"}, "file": {"file2"}},
                {".py"},
            ).files,
            [
                File(self.temp_dir_path / "file1.py"),
                File(self.temp_dir_path / "subdir/file3.py"),
                File(self.temp_dir_path / "subdir/file4.py"),
                File(self.temp_dir_path / "subdir/file5.py"),
            ],
        )

    def test_file_paths(self) -> None:
        self.assertEqual(
            Directory(
                self.temp_dir_path,
                {"directory": {"subdir1"}, "file": {"file2"}},
                {".py"},
            ).file_paths,
            [
                self.temp_dir_path / "file1.py",
                self.temp_dir_path / "subdir/file3.py",
                self.temp_dir_path / "subdir/file4.py",
                self.temp_dir_path / "subdir/file5.py",
            ],
        )

    def test_file_modification_times(self) -> None:
        expected_file_modification_times = {
            file_path: datetime.fromtimestamp(os.path.getmtime(file_path))
            for file_path in [
                self.temp_dir_path / "file1.py",
                self.temp_dir_path / "subdir/file3.py",
                self.temp_dir_path / "subdir/file4.py",
                self.temp_dir_path / "subdir/file5.py",
            ]
        }

        self.assertEqual(
            Directory(
                self.temp_dir_path,
                {"directory": {"subdir1"}, "file": {"file2.py"}},
                {".py"},
            ).file_modified_times,
            expected_file_modification_times,
        )

    def test_file_paths_to_content(self) -> None:
        self.assertEqual(
            Directory(
                self.temp_dir_path,
                {"directory": {"subdir1"}, "file": {"file2.py"}},
                {".py"},
            ).file_paths_to_content,
            {
                str(self.temp_dir_path / "file1.py"): b"content1",
                str(self.temp_dir_path / "subdir/file3.py"): b"content3",
                str(self.temp_dir_path / "subdir/file4.py"): b"content4",
                str(self.temp_dir_path / "subdir/file5.py"): b"content5",
            },
        )
