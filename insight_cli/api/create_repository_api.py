import requests

from .base.api import API
from insight_cli import config


class CreateRepositoryAPI(API):
    @staticmethod
    def make_request() -> dict:
        response = requests.post(url=f"{config.INSIGHT_API_BASE_URL}/create_repository")

        response.raise_for_status()

        return response.json()
