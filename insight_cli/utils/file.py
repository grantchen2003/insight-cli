from pathlib import Path
from typing import TypedDict


class FileDict(TypedDict):
    name: str
    content: list[str]


class File:
    def __init__(self, name: str, content: list[str]):
        self._name: str = name
        self._content: list[str] = content

    @classmethod
    def create_from_path(cls, file_path: Path) -> "File":
        with open(file_path, "rb") as file:
            content = file.read().decode("utf-8", errors="ignore").splitlines()

        return File(name=file_path.name, content=content)

    def to_dict(self) -> FileDict:
        return {"name": self._name, "content": self._content}
