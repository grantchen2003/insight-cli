from pathlib import Path
from utils.directory import Directory
from . import insight_dir
from . import insightignore_file

import json
import os
import requests
import utils


@utils.requests.handle_make_request_exceptions
def _make_initialize_codebase_request(codebase_dir: Directory) -> dict[str, str]:
    request_url = f"{os.environ.get('API_BASE_URL')}/initialize_codebase"

    request_json_body = json.dumps(
        {"codebase": codebase_dir.to_dict()},
        default=str,
    )

    response = requests.post(url=request_url, json=request_json_body)

    response.raise_for_status()

    return response.json()


@utils.requests.handle_make_request_exceptions
def _make_reinitialize_codebase_request(
    codebase_dir: Directory, codebase_id: str
) -> None:
    request_url = f"{os.environ.get('API_BASE_URL')}/reinitialize_codebase"

    request_json_body = json.dumps(
        {
            "codebase": codebase_dir.to_dict(),
            "codebase_id": codebase_id,
        },
        default=str,
    )

    response = requests.post(url=request_url, json=request_json_body)

    response.raise_for_status()

    return response.json()


def initialize(codebase_dir_path: Path) -> None:
    insight_dir_path: Path = codebase_dir_path / ".insight"

    if insight_dir.is_valid(insight_dir_path):
        reinitialize(codebase_dir_path)
        return

    insightignore_file_path: Path = codebase_dir_path / ".insightignore"
    ignorable_names: list[str] = insightignore_file.get_ignorable_names(
        insightignore_file_path
    )

    codebase: Directory = utils.Directory.create_from_path(
        dir_path=codebase_dir_path, ignorable_names=ignorable_names
    )

    response_data: dict[str, str] = _make_initialize_codebase_request(codebase)
    codebase_id: str = response_data["codebase_id"]

    insight_dir.create(insight_dir_path, codebase_id)


def reinitialize(codebase_dir_path: Path) -> None:
    insight_dir_path: Path = codebase_dir_path / ".insight"

    if not insight_dir.is_valid(insight_dir_path):
        raise insight_dir.InvalidInsightDirectoryPathError(insight_dir_path)

    insightignore_file_path: Path = codebase_dir_path / ".insightignore"
    ignorable_names: list[str] = insightignore_file.get_ignorable_names(
        insightignore_file_path
    )

    codebase_dir: Directory = utils.Directory.create_from_path(
        dir_path=codebase_dir_path, ignorable_names=ignorable_names
    )

    codebase_id: str = insight_dir.get_codebase_id(insight_dir_path)

    _make_reinitialize_codebase_request(codebase_dir, codebase_id)


def uninitialize(codebase_dir_path: Path) -> None:
    insight_dir.delete(codebase_dir_path)
