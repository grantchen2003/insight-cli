from pathlib import Path
from typing import TypedDict

from .file import File, FileDict


class DirectoryDict(TypedDict):
    name: str
    files: list[FileDict]
    directories: list["DirectoryDict"]


class Directory:
    def __init__(self, name: str):
        self._name: str = name
        self._files: list[File] = []
        self._subdirectories: list[Directory] = []

    @classmethod
    def create_from_path(
        cls, dir_path: Path, ignorable_names: set[str] = None
    ) -> "Directory":
        directory = Directory(name=dir_path.name)

        if ignorable_names is None:
            ignorable_names = set()

        for path in dir_path.iterdir():
            if path.name in ignorable_names:
                continue

            if path.is_dir():
                subdirectory: Directory = cls.create_from_path(path)
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
