from pathlib import Path
from typing import TypedDict


class FileDict(TypedDict):
    name: str
    lines: list[str]


class File:
    def __init__(self, name: str, lines: list[str]):
        self._name: str = name
        self._lines: list[str] = lines

    @staticmethod
    def create_in_file_system(parent_dir_path: Path, file_dict: FileDict) -> None:
        file_path: Path = parent_dir_path / file_dict["name"]

        with open(file_path, "w") as file:
            file.write("\n".join(file_dict["lines"]))

    @staticmethod
    def create_from_path(file_path: Path) -> "File":
        with open(file_path, "rb") as file:
            lines = file.read().decode("utf-8", errors="ignore").splitlines()
        return File(name=file_path.name, lines=lines)

    def to_dict(self) -> FileDict:
        return {"name": self._name, "lines": self._lines}
