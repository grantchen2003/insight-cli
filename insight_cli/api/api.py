import requests

from insight_cli import config


class API:
    @staticmethod
    def make_initialize_repository_request(
        repository_files: dict[str:bytes],
    ) -> dict[str, str]:
        response = requests.post(
            url=f"{config.INSIGHT_API_BASE_URL}/initialize_repository",
            files=repository_files,
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
        repository_files: dict[str:bytes], repository_id: str
    ) -> None:
        response = requests.post(
            url=f"{config.INSIGHT_API_BASE_URL}/reinitialize_repository",
            files=repository_files,
            json={"repository_id": repository_id},
        )

        response.raise_for_status()

    @staticmethod
    def make_validate_repository_id_request(repository_id: str) -> dict[str, bool]:
        response = requests.post(
            headers={"Content-Type": "application/json"},
            url=f"{config.INSIGHT_API_BASE_URL}/validate_repository_id",
            json={"repository_id": repository_id},
        )

        response.raise_for_status()

        return response.json()
