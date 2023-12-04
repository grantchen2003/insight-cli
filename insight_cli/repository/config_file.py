from pathlib import Path
from typing import TypedDict
import json


class ConfigFileData(TypedDict):
    repository_id: str


class ConfigFile:
    _NAME = "config.json"

    def __init__(self, parent_dir_path: Path):
        self._path = parent_dir_path / ConfigFile._NAME

    def create(self, data: ConfigFileData) -> None:
        with open(self._path, "w") as file:
            content = json.dumps(data, indent=4)
            file.write(content)

    @property
    def data(self) -> ConfigFileData:
        with open(self._path, "r") as file:
            return json.load(file)

    @property
    def is_valid(self) -> bool:
        return self._path.is_file() and isinstance(self.data, ConfigFileData)
