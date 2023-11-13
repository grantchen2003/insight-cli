from pathlib import Path
from utils.directory import Directory
from . import insight_dir
from . import insightignore_file

import json
import os
import requests
import utils


@utils.requests.handle_make_request_exceptions
def _make_initialize_repository_request(repository_dir: Directory) -> dict[str, str]:
    request_url = f"{os.environ.get('API_BASE_URL')}/initialize_repository"

    request_json_body = json.dumps(
        {"repository": repository_dir.to_dict()},
        default=str,
    )

    response = requests.post(url=request_url, json=request_json_body)

    response.raise_for_status()

    return response.json()


@utils.requests.handle_make_request_exceptions
def _make_reinitialize_repository_request(
    repository_dir: Directory, repository_id: str
) -> None:
    request_url = f"{os.environ.get('API_BASE_URL')}/reinitialize_repository"

    request_json_body = json.dumps(
        {
            "repository": repository_dir.to_dict(),
            "repository_id": repository_id,
        },
        default=str,
    )

    response = requests.post(url=request_url, json=request_json_body)

    response.raise_for_status()

    return response.json()


def initialize(repository_dir_path: Path) -> None:
    insight_dir_path: Path = repository_dir_path / ".insight"

    if insight_dir.is_valid(insight_dir_path):
        reinitialize(repository_dir_path)
        return

    insightignore_file_path: Path = repository_dir_path / ".insightignore"
    ignorable_names: list[str] = insightignore_file.get_ignorable_names(
        insightignore_file_path
    )

    repository: Directory = utils.Directory.create_from_path(
        dir_path=repository_dir_path, ignorable_names=ignorable_names
    )

    response_data: dict[str, str] = _make_initialize_repository_request(repository)
    repository_id: str = response_data["repository_id"]

    insight_dir.create(insight_dir_path, repository_id)


def reinitialize(repository_dir_path: Path) -> None:
    insight_dir_path: Path = repository_dir_path / ".insight"

    if not insight_dir.is_valid(insight_dir_path):
        raise insight_dir.InvalidInsightDirectoryPathError(insight_dir_path)

    insightignore_file_path: Path = repository_dir_path / ".insightignore"
    ignorable_names: list[str] = insightignore_file.get_ignorable_names(
        insightignore_file_path
    )

    repository_dir: Directory = utils.Directory.create_from_path(
        dir_path=repository_dir_path, ignorable_names=ignorable_names
    )

    repository_id: str = insight_dir.get_repository_id(insight_dir_path)

    _make_reinitialize_repository_request(repository_dir, repository_id)


def uninitialize(repository_dir_path: Path) -> None:
    insight_dir.delete(repository_dir_path)
