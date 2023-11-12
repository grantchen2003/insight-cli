from datetime import datetime
from .file import File, FileDict, create_file_from_path
from pathlib import Path
from typing import TypedDict


class DirectoryDict(TypedDict):
    name: str
    last_updated: datetime
    files: list[FileDict]
    directories: list["DirectoryDict"]


class Directory:
    def __init__(self, name: str, last_updated: datetime):
        self._name: str = name
        self._last_updated: datetime = last_updated
        self._files: list[File] = []
        self._subdirectories: list[Directory] = []

    def add_file(self, file: File) -> None:
        self._files.append(file)

    def add_subdirectory(self, directory: "Directory") -> None:
        self._subdirectories.append(directory)

    def to_dict(self) -> DirectoryDict:
        return {
            "name": self._name,
            "last_updated": self._last_updated,
            "files": [file.to_dict() for file in self._files],
            "subdirectories": [
                subdirectory.to_dict() for subdirectory in self._subdirectories
            ],
        }


def create_directory_from_path(
    dir_path: Path, ignorable_names: set[str] = None
) -> Directory:
    directory = Directory(
        name=dir_path.name,
        last_updated=datetime.fromtimestamp(dir_path.stat().st_mtime),
    )

    if ignorable_names is None:
        ignorable_names = set()

    for path in dir_path.iterdir():
        if path.name in ignorable_names:
            continue

        if path.is_dir():
            subdirectory: Directory = create_directory_from_path(path)
            directory.add_subdirectory(subdirectory)

        if path.is_file():
            file: File = create_file_from_path(path)
            directory.add_file(file)

    return directory
