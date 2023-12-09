from pathlib import Path
from typing import TypedDict


class FileDict(TypedDict):
    path: Path
    lines: list[str]


class File:
    def __init__(self, path: Path, lines: list[str]):
        self._path: Path = path
        self._lines: list[str] = lines

    @staticmethod
    def create_in_file_system(file_dict: FileDict) -> None:
        with open(file_dict["path"], "w") as file:
            file.write("\n".join(file_dict["lines"]))

    @staticmethod
    def create_from_path(file_path: Path) -> "File":
        return File(path=file_path, lines=open(file_path, "rb"))

    def to_file_dict(self) -> FileDict:
        return {
            "path": self._path,
            "lines": self._lines,
        }

    def to_binary_dict(self) -> dict:
        return {str(self._path): self._lines}
