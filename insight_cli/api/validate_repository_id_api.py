import requests

from .base.api import API
from insight_cli import config


class ValidateRepositoryIdAPI(API):
    @staticmethod
    def make_request(repository_id: str) -> dict[str, bool]:
        response = requests.post(
            url=f"{config.INSIGHT_API_BASE_URL}/validate_repository_id",
            json={"repository_id": repository_id},
        )

        response.raise_for_status()

        return response.json()
