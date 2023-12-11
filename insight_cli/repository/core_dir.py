from datetime import datetime
from pathlib import Path
import os
import shutil

from .config_file import ConfigFile, ConfigFileData
from .updates_file import UpdatesFile


class CoreDir:
    _NAME = ".insight"

    def __init__(self, parent_dir_path: Path):
        self._path = parent_dir_path / CoreDir._NAME
        self._config_file = ConfigFile(self._path)
        self._updates_file = UpdatesFile(self._path)

    def create(
        self, repository_id: str, nested_repository_file_paths: list[Path]
    ) -> None:
        os.makedirs(self._path, exist_ok=True)
        config_file_data: ConfigFileData = {"repository_id": repository_id}
        self._config_file.create(config_file_data)
        self._updates_file.create(nested_repository_file_paths)

    def reinitialize(self, file_paths_to_reinitialize: dict[str, list[Path]]) -> None:
        self._updates_file.add(file_paths_to_reinitialize["add"])
        self._updates_file.update(file_paths_to_reinitialize["update"])
        self._updates_file.delete(file_paths_to_reinitialize["delete"])

    def delete(self) -> None:
        shutil.rmtree(self._path)

    @property
    def is_valid(self) -> bool:
        return self._config_file.is_valid

    @property
    def repository_id(self) -> str:
        return self._config_file.data["repository_id"]

    @property
    def files_path_to_last_updated(self) -> dict[Path, datetime]:
        return self._updates_file.data
