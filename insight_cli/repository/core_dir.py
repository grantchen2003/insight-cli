from datetime import datetime
from pathlib import Path
import os, shutil

from .config_file import ConfigFile, ConfigFileData
from .tracker_file import TrackerFile


class CoreDir:
    _NAME = ".insight"

    @classmethod
    @property
    def name(cls) -> str:
        return cls._NAME

    def __init__(self, parent_dir_path: Path):
        self._path = parent_dir_path / CoreDir._NAME
        self._config_file = ConfigFile(self._path)
        self._tracker_file = TrackerFile(self._path)

    def create(
        self, repository_id: str, nested_repository_file_paths: list[Path]
    ) -> None:
        os.makedirs(self._path, exist_ok=True)
        config_file_data: ConfigFileData = {"repository_id": repository_id}
        self._config_file.create(config_file_data)
        self._tracker_file.create(nested_repository_file_paths)

    def update(
        self, repository_file_changes: dict[str, list[tuple[str, bytes]]]
    ) -> None:
        self._tracker_file.change_paths(
            paths_to_add=[Path(path) for path in repository_file_changes["add"]],
            paths_to_update=[Path(path) for path in repository_file_changes["update"]],
            paths_to_delete=[Path(path) for path in repository_file_changes["delete"]],
        )

    def delete(self) -> None:
        shutil.rmtree(self._path)

    @property
    def is_valid(self) -> bool:
        return self._config_file.is_valid

    @property
    def repository_id(self) -> str:
        return self._config_file.data["repository_id"]

    @property
    def tracked_file_modified_times(self) -> dict[Path, datetime]:
        return self._tracker_file.tracked_file_modified_times
