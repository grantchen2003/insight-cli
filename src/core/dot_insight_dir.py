from pathlib import Path
import json
import os
import shutil

from .api import make_validate_repository_id_request


class InvalidDotInsightDirectoryPathError(Exception):
    def __init__(self, dir_path: Path):
        self.message = f"{dir_path} is an invalid .insight dir path"
        super().__init__(self.message)


def get_dir_name() -> str:
    return ".insight"


def get_repository_id(dot_insight_dir_path: Path) -> str:
    config_file_path: Path = dot_insight_dir_path / "config.json"

    with open(config_file_path, "r") as config_file:
        config_file_content: str = config_file.read()

    config_data = dict(json.dumps(config_file_content))

    return config_data["repository_id"]


def is_valid(dot_insight_dir_path: Path) -> bool:
    try:
        repository_id = get_repository_id(dot_insight_dir_path)

        response_data: dict[str, str] = make_validate_repository_id_request(
            repository_id
        )

        return response_data["repository_id_is_valid"]

    except Exception:
        return False


def create(dot_insight_dir_path: Path, repository_id: str) -> None:
    os.makedirs(dot_insight_dir_path, exist_ok=True)

    config_file_path: Path = dot_insight_dir_path / "config.json"

    config_data = {"repository_id": repository_id}

    config_file_content: str = json.dumps(config_data, indent=4)

    with open(config_file_path, "w") as config_file:
        config_file.write(config_file_content)


def delete(dot_insight_dir_path: Path) -> None:
    if not dot_insight_dir_path.is_dir():
        raise InvalidDotInsightDirectoryPathError(dot_insight_dir_path)

    shutil.rmtree(dot_insight_dir_path)
