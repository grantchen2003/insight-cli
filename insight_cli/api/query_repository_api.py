import requests

from .base.api import API
from insight_cli import config


class QueryRepositoryAPI(API):
    @staticmethod
    def make_request(repository_id: str, query_string: str) -> list[dict]:
        response = requests.get(
            url=f"{config.INSIGHT_API_BASE_URL}/query?repository-id={repository_id}&query-string={query_string}"
        )

        response.raise_for_status()

        return response.json()
