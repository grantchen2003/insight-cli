import json
import os

import requests

from insight_cli.utils.directory import Directory
from insight_cli import utils


def get_base_api_url() -> str:
    env = os.getenv("ENV", "prod")

    env_to_base_api_url = {
        "dev": "http://localhost:5000",
        "prod": "https://insight.api.com",
    }

    return env_to_base_api_url[env]


@utils.handle_make_request_exceptions
def make_initialize_repository_request(repository_dir: Directory) -> dict[str, str]:
    request_url = f"{get_base_api_url()}/initialize_repository"

    request_json_body = json.dumps(
        {
            "repository": repository_dir.to_dict(),
        },
        default=str,
    )

    response = requests.post(url=request_url, json=request_json_body)

    response.raise_for_status()

    return response.json()


@utils.handle_make_request_exceptions
def make_reinitialize_repository_request(
    repository_dir: Directory, repository_id: str
) -> None:
    request_url = f"{get_base_api_url()}/reinitialize_repository"

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


@utils.handle_make_request_exceptions
def make_validate_repository_id_request(repository_id: str) -> dict[str, str]:
    request_url = f"{get_base_api_url()}/validate_repository_id"

    request_json_body = json.dumps(
        {"repository_id": repository_id},
        default=str,
    )

    response = requests.post(url=request_url, json=request_json_body)

    response.raise_for_status()

    return response.json()


@utils.handle_make_request_exceptions
def make_query_repository_request(repository_id: str, query_string: str) -> list | dict:
    request_url = f"{get_base_api_url()}/query?repository-id={repository_id}&query-string={query_string}"

    response = requests.get(url=request_url)

    response.raise_for_status()

    return response.json()
