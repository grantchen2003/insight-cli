from datetime import datetime
from pathlib import Path
import os, shutil

from .authenticator import Authenticator
from .file_tracker import FileTracker


class Manager:
    _DIR_NAME = ".insight"

    @classmethod
    @property
    def name(cls) -> str:
        return cls._DIR_NAME

    def __init__(self, parent_dir_path: Path):
        self._path = parent_dir_path / Manager._DIR_NAME
        self._authenticator = Authenticator(self._path)
        self._file_tracker = FileTracker(self._path)

    def create(
        self, repository_id: str, nested_repository_file_paths: list[Path]
    ) -> None:
        os.makedirs(self._path, exist_ok=True)
        self._authenticator.create({"repository_id": repository_id})
        self._file_tracker.create(nested_repository_file_paths)

    def update(
        self, repository_file_changes: dict[str, list[tuple[str, bytes]]]
    ) -> None:
        self._file_tracker.change_file_paths(
            paths_to_add=[Path(path) for path in repository_file_changes["add"]],
            paths_to_update=[Path(path) for path in repository_file_changes["update"]],
            paths_to_delete=[Path(path) for path in repository_file_changes["delete"]],
        )

    def delete(self) -> None:
        shutil.rmtree(self._path)

    @property
    def is_valid(self) -> bool:
        return self._authenticator.is_valid

    @property
    def repository_id(self) -> str:
        return self._authenticator.data["repository_id"]

    @property
    def tracked_file_modified_times(self) -> dict[Path, datetime]:
        return self._file_tracker.tracked_file_modified_times
