from pathlib import Path
from typing import TypedDict
import json

from insight_cli.api import ValidateRepositoryIdAPI


class InvalidConfigFileDataError(Exception):
    def __init__(self, data) -> None:
        self.message = f"{data} is not valid config file data."
        super().__init__(self.message)


class ConfigFileData(TypedDict):
    repository_id: str


class ConfigFile:
    _NAME = "config.json"

    @staticmethod
    def _is_config_file_data_instance(data):
        return (
            isinstance(data, dict)
            and len(data) == len(ConfigFileData.__annotations__)
            and all(
                key in data and isinstance(data[key], val)
                for key, val in ConfigFileData.__annotations__.items()
            )
        )

    def __init__(self, parent_dir_path: Path):
        self._path = parent_dir_path / ConfigFile._NAME

    def create(self, data: ConfigFileData) -> None:
        if not ConfigFile._is_config_file_data_instance(data):
            raise InvalidConfigFileDataError(data)

        with open(self._path, "w") as file:
            content = json.dumps(data, indent=4)
            file.write(content)

    @property
    def data(self) -> ConfigFileData:
        if not self._path.is_file():
            raise FileNotFoundError()

        with open(self._path, "r") as file:
            data = json.load(file)

        if not ConfigFile._is_config_file_data_instance(data):
            raise InvalidConfigFileDataError(data)

        return data

    @property
    def is_valid(self) -> bool:
        try:
            response_data: dict[str, bool] = ValidateRepositoryIdAPI.make_request(
                self.data["repository_id"]
            )

            return response_data["repository_id_is_valid"]

        except FileNotFoundError:
            return False
