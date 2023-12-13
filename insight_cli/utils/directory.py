from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from datetime import datetime
import os

from .file import File
from .string_matcher import StringMatcher


class Directory:
    def __init__(self, path: Path):
        self._path: Path = path
        self._files: list[File] = []
        self._subdirectories: list[Directory] = []

    @staticmethod
    def get_nested_file_paths(
        dir_path: Path, ignorable_regex_patterns: dict[str, set] = None
    ) -> list[Path]:
        nested_file_paths = []

        for path in dir_path.iterdir():
            if path.is_dir() and not StringMatcher.matches_any_regex_pattern(
                str(path), ignorable_regex_patterns["file"]
            ):
                nested_file_paths.extend(
                    Directory.get_nested_file_paths(path, ignorable_regex_patterns)
                )

            if path.is_file() and not StringMatcher.matches_any_regex_pattern(
                str(path), ignorable_regex_patterns["file"]
            ):
                nested_file_paths.append(path)

        return nested_file_paths

    @staticmethod
    def compare_file_paths(
        previous_file_paths: dict[Path, datetime],
        current_dir_path: Path,
        ignorable_regex_patterns: dict[str, set] = None,
    ) -> dict[str, list[Path]]:
        file_paths_to_reinitialize = {"add": [], "update": [], "delete": []}

        nested_file_paths = Directory.get_nested_file_paths(
            current_dir_path, ignorable_regex_patterns
        )

        for file_path in nested_file_paths:
            if file_path not in previous_file_paths:
                file_paths_to_reinitialize["add"].append(file_path)
                continue

            if (
                datetime.fromtimestamp(os.path.getmtime(file_path))
                != previous_file_paths[file_path]
            ):
                file_paths_to_reinitialize["update"].append(file_path)

            del previous_file_paths[file_path]

        file_paths_to_reinitialize["delete"] = list(previous_file_paths.keys())

        return file_paths_to_reinitialize

    @staticmethod
    def create_from_path(
        dir_path: Path, ignorable_regex_patterns: dict[str, set] = None
    ) -> "Directory":
        if ignorable_regex_patterns is None:
            ignorable_regex_patterns = {"directory": set(), "file": set()}

        directory = Directory(dir_path)

        def add_directory_entry(entry_path: Path) -> None:
            if entry_path.is_dir() and not StringMatcher.matches_any_regex_pattern(
                str(entry_path), ignorable_regex_patterns["directory"]
            ):
                directory.add_subdirectory(
                    Directory.create_from_path(entry_path, ignorable_regex_patterns)
                )

            if entry_path.is_file() and not StringMatcher.matches_any_regex_pattern(
                str(entry_path), ignorable_regex_patterns["file"]
            ):
                directory.add_file(File(entry_path))

        with ThreadPoolExecutor() as executor:
            for entry_path in os.scandir(directory.path):
                executor.submit(add_directory_entry, Path(entry_path))

        return directory

    def add_file(self, file: File) -> None:
        self._files.append(file)

    def add_subdirectory(self, subdirectory: "Directory") -> None:
        self._subdirectories.append(subdirectory)

    @property
    def path(self) -> Path:
        return self._path

    @property
    def files(self) -> list[File]:
        return self._files

    @property
    def subdirectories(self) -> list["Directory"]:
        return self._subdirectories

    @property
    def nested_files(self) -> list[File]:
        nested_files = self._files

        for subdirectory in self._subdirectories:
            nested_files.extend(subdirectory.nested_files)

        return nested_files

    @property
    def nested_file_paths(self) -> list[Path]:
        nested_file_paths = [file.path for file in self._files]

        for subdirectory in self._subdirectories:
            nested_file_paths.extend(subdirectory.nested_file_paths)

        return nested_file_paths

    @property
    def nested_files_path_to_content(self) -> dict[str, bytes]:
        return {str(file.path): file.content for file in self.nested_files}
