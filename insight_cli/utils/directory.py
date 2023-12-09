from pathlib import Path
from typing import TypedDict

from .file import File, FileDict
from .string_matcher import StringMatcher


class DirectoryDict(TypedDict):
    path: Path
    files: list[FileDict]
    subdirectories: list["DirectoryDict"]


class Directory:
    def __init__(self, path: Path):
        self._path: Path = path
        self._files: list[File] = []
        self._subdirectories: list[Directory] = []

    @staticmethod
    def create_in_file_system(dir_dict: DirectoryDict) -> None:
        dir_dict["path"].mkdir()

        for file_dict in dir_dict["files"]:
            File.create_in_file_system(file_dict)

        for subdir_dict in dir_dict["subdirectories"]:
            Directory.create_in_file_system(subdir_dict)

    @staticmethod
    def create_from_path(
        dir_path: Path, ignorable_regex_patterns: list[str] = None
    ) -> "Directory":
        if ignorable_regex_patterns is None:
            ignorable_regex_patterns = []

        directory = Directory(dir_path)

        for path in dir_path.iterdir():
            if StringMatcher.matches_any_regex_pattern(
                str(path), ignorable_regex_patterns
            ):
                continue

            if path.is_dir():
                subdirectory: Directory = Directory.create_from_path(
                    path, ignorable_regex_patterns
                )
                directory.add_subdirectory(subdirectory)

            if path.is_file():
                file: File = File.create_from_path(path)
                directory.add_file(file)

        return directory

    def add_file(self, file: File) -> None:
        self._files.append(file)

    def add_subdirectory(self, subdirectory: "Directory") -> None:
        self._subdirectories.append(subdirectory)

    def to_directory_dict(self) -> DirectoryDict:
        return {
            "path": self._path,
            "files": [file.to_file_dict() for file in self._files],
            "subdirectories": [
                subdirectory.to_directory_dict()
                for subdirectory in self._subdirectories
            ],
        }

    def to_json_dict(self) -> DirectoryDict:
        return {
            "path": str(self._path),
            "files": [file.to_json_dict() for file in self._files],
            "subdirectories": [
                subdirectory.to_json_dict() for subdirectory in self._subdirectories
            ],
        }
