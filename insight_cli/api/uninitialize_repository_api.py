import requests

from .base import API
from insight_cli import config


class UninitializeRepositoryAPI(API):
    @staticmethod
    def make_request(repository_id: str) -> None:
        response = requests.delete(
            url=f"{config.INSIGHT_API_BASE_URL}/uninitialize_repository",
            json={"repository_id": repository_id},
            timeout=None,
        )

        response.raise_for_status()
