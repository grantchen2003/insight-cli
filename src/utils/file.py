from datetime import datetime
from pathlib import Path
from typing import TypedDict


class FileDict(TypedDict):
    name: str
    last_updated: datetime
    content: list[str]


class File:
    def __init__(self, name: str, last_updated: datetime, content: list[str]):
        self._name: str = name
        self._last_updated: datetime = last_updated
        self._content: list[str] = content

    def to_dict(self) -> FileDict:
        return {
            "name": self._name,
            "last_updated": self._last_updated,
            "content": self._content,
        }


def create_file_from_path(file_path: Path) -> File:
    with open(file_path) as file:
        content = file.read().splitlines()

    return File(
        name=file_path.name,
        last_updated=datetime.fromtimestamp(file_path.stat().st_mtime),
        content=content,
    )
