from concurrent.futures import ThreadPoolExecutor
import requests

from .base.api import API
from insight_cli import config


class ReinitializeRepositoryAPI(API):
    @staticmethod
    def _get_batched_repository_file_changes(
        repository_id: str, repository_file_changes: dict[str, list[tuple[str, bytes]]]
    ) -> list[dict[str, dict[str, bytes] | dict[str, str] | str]]:
        MAX_BATCH_SIZE_BYTES = 10 * 1024**2

        batches = []
        current_batch = {"files": {}, "changes": {}, "repository_id": repository_id}
        current_batch_size_bytes = 0

        for change, files in repository_file_changes.items():
            for file_path, file_content in files:
                file_size_bytes = len(file_content)

                current_batch["files"][file_path] = file_content
                current_batch["changes"][file_path] = change
                current_batch_size_bytes += file_size_bytes

                if current_batch_size_bytes + file_size_bytes > MAX_BATCH_SIZE_BYTES:
                    batches.append(current_batch)
                    current_batch = {
                        "files": {},
                        "changes": {},
                        "repository_id": repository_id,
                    }
                    current_batch_size_bytes = 0

        batches.append(current_batch)

        return batches

    @staticmethod
    def _make_batch_request(
        payload: dict[str, dict[str, bytes] | dict[str, str] | str]
    ) -> None:
        response = requests.put(
            url=f"{config.INSIGHT_API_BASE_URL}/reinitialize_repository",
            files=payload["files"],
            data={
                "repository_id": payload["repository_id"],
                "changes": payload["changes"],
            },
        )

        response.raise_for_status()

    @classmethod
    def make_request(
        cls,
        repository_id: str,
        repository_file_changes: dict[str, list[tuple[str, bytes]]],
    ) -> None:
        request_batches = cls._get_batched_repository_file_changes(
            repository_id, repository_file_changes
        )

        with ThreadPoolExecutor(max_workers=len(request_batches)) as executor:
            executor.map(cls._make_batch_request, request_batches)
