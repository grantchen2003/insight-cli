from concurrent.futures import ThreadPoolExecutor
import requests

from .base.api import API
from insight_cli import config


class ReinitializeRepositoryAPI(API):
    _MAX_BATCH_SIZE = 10 * 1024 ** 2  # 1 MB
    _MAX_THREADS = 80

    @classmethod
    def _get_batched_repository_file_changes(cls, repository_id, repository_file_changes):
        batches: list[dict] = []
        current_batch = {
            "files": {},
            "changes": {},
            "repository_id": repository_id
        }
        current_batch_size = 0

        for change, files in repository_file_changes.items():
            for file_path, file_content in files:
                file_size = len(file_content)

                if current_batch_size + file_size > cls._MAX_BATCH_SIZE:
                    batches.append(current_batch)
                    current_batch = {
                        "files": {},
                        "changes": {},
                        "repository_id": repository_id
                    }
                    current_batch_size = 0

                current_batch["files"][file_path] = file_content
                current_batch["changes"][file_path] = change
                current_batch_size += file_size

        batches.append(current_batch)

        return batches

    @staticmethod
    def _make_batch_request(payload) -> None:
        response = requests.post(
            url=f"{config.INSIGHT_API_BASE_URL}/reinitialize_repository",
            files=payload["files"],
            data={
                "repository_id": payload["repository_id"],
                "changes": payload["changes"]
            },
        )

        response.raise_for_status()

    @classmethod
    def make_request(
            cls,
            repository_id: str,
            repository_file_changes: list[tuple[str, bytes, str]]
    ) -> None:
        with ThreadPoolExecutor(max_workers=cls._MAX_THREADS) as executor:
            batched_changed_repository_files = cls._get_batched_repository_file_changes(
                repository_id,
                repository_file_changes
            )

            executor.map(cls._make_batch_request, batched_changed_repository_files)
