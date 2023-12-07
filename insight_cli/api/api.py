import requests

from insight_cli import config
from insight_cli.utils.directory import Directory


class API:
    @staticmethod
    def make_initialize_repository_request(repository_dir: Directory) -> dict[str, str]:
        response = requests.post(
            headers={"Content-Type": "application/json"},
            url=f"{config.INSIGHT_API_BASE_URL}/initialize_repository",
            json={"repository_dir": repository_dir.to_dict()},
        )

        response.raise_for_status()

        return response.json()

    @staticmethod
    def make_query_repository_request(
        repository_id: str, query_string: str
    ) -> list[dict]:
        response = requests.get(
            url=f"{config.INSIGHT_API_BASE_URL}/query?repository-id={repository_id}&query-string={query_string}"
        )

        response.raise_for_status()

        return response.json()

    @staticmethod
    def make_reinitialize_repository_request(
        repository_dir: Directory, repository_id: str
    ) -> None:
        response = requests.post(
            headers={"Content-Type": "application/json"},
            url=f"{config.INSIGHT_API_BASE_URL}/reinitialize_repository",
            json={
                "repository_dir": repository_dir.to_dict(),
                "repository_id": repository_id,
            },
        )

        response.raise_for_status()

        return response.json()

    @staticmethod
    def make_validate_repository_id_request(repository_id: str) -> dict[str, bool]:
        response = requests.post(
            headers={"Content-Type": "application/json"},
            url=f"{config.INSIGHT_API_BASE_URL}/validate_repository_id",
            json={"repository_id": repository_id},
        )

        response.raise_for_status()

        return response.json()
