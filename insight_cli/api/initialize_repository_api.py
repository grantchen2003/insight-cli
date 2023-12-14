from concurrent.futures import ThreadPoolExecutor
import requests

from .base.api import API
from insight_cli import config


class InitializeRepositoryAPI(API):
    _MAX_BATCH_SIZE = 10 * 1024 ** 2  # 1 MB
    _MAX_THREADS = 80

    @staticmethod
    def _get_batched_repository_files(
            repository_files: dict[str, bytes]
    ) -> list[dict[str, dict[str, bytes]]]:
        batches = []
        current_batch = {"files": {}}
        current_batch_size = 0

        for file_path, file_content in repository_files.items():
            file_size = len(file_content)

            if current_batch_size + file_size > InitializeRepositoryAPI._MAX_BATCH_SIZE:
                batches.append(current_batch)
                current_batch = {"files": {}}
                current_batch_size = 0

            current_batch["files"][file_path] = file_content
            current_batch_size += file_size

        batches.append(current_batch)

        return batches

    @staticmethod
    def _make_batch_request(payload: list[dict[str, dict[str, bytes]]]) -> dict[str, str]:
        response = requests.post(
            url=f"{config.INSIGHT_API_BASE_URL}/initialize_repository",
            files=payload["files"],
        )

        response.raise_for_status()

        return response.json()

    @classmethod
    def make_request(cls, repository_files: dict[str, bytes]) -> dict[str, str]:
        with ThreadPoolExecutor(max_workers=cls._MAX_THREADS) as executor:
            results = executor.map(
                cls._make_batch_request,
                cls._get_batched_repository_files(repository_files)
            )

            return {"repository_id": result["repository_id"] for result in results}
