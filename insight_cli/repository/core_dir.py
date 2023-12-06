from pathlib import Path
import os
import shutil

from insight_cli.api import API
from .config_file import ConfigFile, ConfigFileData


class CoreDir:
    _NAME = ".insight"

    def __init__(self, parent_dir_path: Path):
        self._path = parent_dir_path / CoreDir._NAME
        self._config_file = ConfigFile(self._path)

    def create(self, repository_id: str) -> None:
        os.makedirs(self._path, exist_ok=True)
        config_file_data: ConfigFileData = {"repository_id": repository_id}
        self._config_file.create(config_file_data)

    def delete(self) -> None:
        shutil.rmtree(self._path)

    @property
    def is_valid(self) -> bool:
        return self._config_file.is_valid

    @property
    def repository_id(self) -> str:
        return self._config_file.data["repository_id"]
