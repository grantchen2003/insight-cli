from pathlib import Path
from typing import TypedDict
import json

from insight_cli.api import ValidateRepositoryIdAPI


class AuthenticatorData(TypedDict):
    repository_id: str


class Authenticator:
    _FILE_NAME = "authenticator.json"

    @staticmethod
    def _is_authenticator_data_instance(data):
        return (
            isinstance(data, dict)
            and len(data) == len(AuthenticatorData.__annotations__)
            and all(
                key in data and isinstance(data[key], val)
                for key, val in AuthenticatorData.__annotations__.items()
            )
        )

    def __init__(self, parent_dir_path: Path):
        self._path = parent_dir_path / Authenticator._FILE_NAME

    def create_file(self, data: AuthenticatorData) -> None:
        if not Authenticator._is_authenticator_data_instance(data):
            raise ValueError(f"{data} is not valid authenticator data.")

        with open(self._path, "w") as file:
            content = json.dumps(data, indent=4)
            file.write(content)

    @property
    def data(self) -> AuthenticatorData:
        if not self._path.is_file():
            raise FileNotFoundError(f"No file found at {self._path}.")

        with open(self._path, "r") as file:
            data = json.load(file)

        if not Authenticator._is_authenticator_data_instance(data):
            raise ValueError(f"{data} is not valid authenticator data.")

        return data

    @property
    def is_valid(self) -> bool:
        try:
            response_data: dict[str, bool] = ValidateRepositoryIdAPI.make_request(
                self.data["repository_id"]
            )

            return response_data["repository_id_is_valid"]

        except ValueError:
            return False

        except FileNotFoundError:
            return False
