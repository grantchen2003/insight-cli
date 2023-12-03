import json

import requests

from insight_cli.utils.directory import Directory
from insight_cli.config import config


class API:
    @staticmethod
    def make_initialize_repository_request(repository_dir: Directory) -> dict[str, str]:
        request_url = f"{config.INSIGHT_API_BASE_URL}/initialize_repository"

        request_json_body = json.dumps(
            {"repository": repository_dir.to_dict()}, default=str
        )

        response = requests.post(url=request_url, json=request_json_body)

        response.raise_for_status()

        return response.json()

    @staticmethod
    def make_reinitialize_repository_request(
        repository_dir: Directory, repository_id: str
    ) -> None:
        request_url = f"{config.INSIGHT_API_BASE_URL}/reinitialize_repository"

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

    @staticmethod
    def make_validate_repository_id_request(repository_id: str) -> dict[str, str]:
        request_url = f"{config.INSIGHT_API_BASE_URL}/validate_repository_id"

        request_json_body = json.dumps(
            {"repository_id": repository_id},
            default=str,
        )

        response = requests.post(url=request_url, json=request_json_body)

        response.raise_for_status()

        return response.json()

    @staticmethod
    def make_query_repository_request(
        repository_id: str, query_string: str
    ) -> list | dict:
        request_url = f"{config.INSIGHT_API_BASE_URL}/query?repository-id={repository_id}&query-string={query_string}"

        response = requests.get(url=request_url)

        response.raise_for_status()

        return response.json()
