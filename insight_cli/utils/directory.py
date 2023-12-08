from pathlib import Path
from typing import TypedDict

from .file import File, FileDict
from .string_matcher import StringMatcher


class DirectoryDict(TypedDict):
    name: str
    files: list[FileDict]
    subdirectories: list["DirectoryDict"]


class Directory:
    def __init__(self, name: str):
        self._name: str = name
        self._files: list[File] = []
        self._subdirectories: list[Directory] = []

    @staticmethod
    def create_in_file_system(parent_dir_path: Path, dir_dict: DirectoryDict) -> None:
        dir_path: Path = parent_dir_path / dir_dict["name"]
        dir_path.mkdir()

        for file_dict in dir_dict["files"]:
            File.create_in_file_system(dir_path, file_dict)

        for subdir_dict in dir_dict["subdirectories"]:
            Directory.create_in_file_system(dir_path, subdir_dict)

    @staticmethod
    def create_from_path(dir_path: Path, ignorable_regex_patterns: list[str] = None) -> "Directory":
        if ignorable_regex_patterns is None:
            ignorable_regex_patterns = []

        directory = Directory(name=dir_path.name)

        for path in dir_path.iterdir():
            if StringMatcher.matches_any_regex_pattern(path.name, ignorable_regex_patterns):
                continue

            if path.is_dir():
                subdirectory: Directory = Directory.create_from_path(path, ignorable_regex_patterns)
                directory.add_subdirectory(subdirectory)

            if path.is_file():
                file: File = File.create_from_path(path)
                directory.add_file(file)

        return directory

    def add_file(self, file: File) -> None:
        self._files.append(file)

    def add_subdirectory(self, subdirectory: "Directory") -> None:
        self._subdirectories.append(subdirectory)

    def to_dict(self) -> DirectoryDict:
        return {
            "name": self._name,
            "files": [file.to_dict() for file in self._files],
            "subdirectories": [
                subdirectory.to_dict() for subdirectory in self._subdirectories
            ],
        }
