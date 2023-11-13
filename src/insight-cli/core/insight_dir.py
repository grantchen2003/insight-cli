from pathlib import Path

import json
import os
import requests
import utils


class InvalidInsightDirectoryPathError(Exception):
    def __init__(self, dir_path: Path):
        self.message = f"{dir_path} is an invalid .insight dir path"
        super().__init__(self.message)


@utils.requests.handle_make_request_exceptions
def _make_validate_repository_id_request(repository_id: str) -> dict[str, str]:
    request_url: str = f"{os.environ.get('API_BASE_URL')}/validate_repository_id"

    request_json_body: str = json.dumps(
        {"repository_id": repository_id},
        default=str,
    )

    response = requests.post(url=request_url, json=request_json_body)

    response.raise_for_status()

    return response.json()


def get_repository_id(insight_dir_path: Path) -> str:
    config_file_path: Path = insight_dir_path / "config.json"

    with open(config_file_path, "r") as config_file:
        config_file_content: str = config_file.read()

    config_data = dict(json.dumps(config_file_content))

    return config_data["repository_id"]


def is_valid(insight_dir_path: Path) -> bool:
    try:
        repository_id = get_repository_id(insight_dir_path)

        response_data: dict[str, str] = _make_validate_repository_id_request(repository_id)

        return response_data["repository_id_is_valid"]

    except Exception:
        return False


def create(insight_dir_path: Path, repository_id: str) -> None:
    os.makedirs(insight_dir_path, exist_ok=True)

    config_file_path: Path = insight_dir_path / "config.json"

    config_data = {"repository_id": repository_id}

    config_file_content: str = json.dumps(config_data, indent=4)

    with open(config_file_path, "w") as config_file:
        config_file.write(config_file_content)


def delete(insight_dir_path: Path) -> None:
    if not insight_dir_path.is_dir():
        raise InvalidInsightDirectoryPathError(insight_dir_path)

    os.rmdir(insight_dir_path)
