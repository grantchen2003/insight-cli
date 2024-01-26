from concurrent.futures import ThreadPoolExecutor
import base64, copy, requests

from .base.api import API
from insight_cli import config


class ReinitializeRepositoryAPI(API):
    @staticmethod
    def _chunkify_file_content(
        file_content: bytes, chunk_size_bytes: int, first_chunk_size_bytes: int = 0
    ) -> list[dict]:
        if first_chunk_size_bytes == 0:
            first_chunk_size_bytes = chunk_size_bytes

        file_size_bytes = len(file_content)

        file_content_chunks = []
        left, right = 0, first_chunk_size_bytes
        while left < file_size_bytes:
            right = min(right, file_size_bytes)
            file_content_chunks.append(file_content[left:right])
            left, right = right, right + chunk_size_bytes

        return [
            {
                "content": base64.b64encode(file_content_chunk).decode("utf-8"),
                "type": "base64",
                "size_bytes": len(file_content_chunk),
                "chunk_index": i,
                "num_total_chunks": len(file_content_chunks),
            }
            for i, file_content_chunk in enumerate(file_content_chunks)
        ]

    @classmethod
    def _get_batched_repository_file_changes(
        cls,
        repository_id: str,
        repository_file_changes: dict[str, list[tuple[str, bytes]]],
    ) -> list[dict]:
        MAX_BATCH_SIZE_BYTES = 10 * 1024**2

        batches = []
        empty_batch = {"files": {}, "changes": {}, "size_bytes": 0}

        current_batch = copy.deepcopy(empty_batch)

        for change, files in repository_file_changes.items():
            for file_path, file_content in files:
                if change == "delete":
                    current_batch["changes"][file_path] = change
                    continue

                file_content_chunks = cls._chunkify_file_content(
                    file_content,
                    MAX_BATCH_SIZE_BYTES,
                    MAX_BATCH_SIZE_BYTES - current_batch["size_bytes"],
                )

                for file_content_chunk in file_content_chunks:
                    if (
                        current_batch["size_bytes"] + file_content_chunk["size_bytes"]
                        > MAX_BATCH_SIZE_BYTES
                    ):
                        batches.append(current_batch)
                        current_batch = copy.deepcopy(empty_batch)

                    current_batch["files"][file_path] = file_content_chunk
                    current_batch["changes"][file_path] = change
                    current_batch["size_bytes"] += file_content_chunk["size_bytes"]

        if current_batch != empty_batch:
            batches.append(current_batch)

        for i, batch in enumerate(batches):
            del batch["size_bytes"]
            batch.update(
                {
                    "batch_index": i,
                    "num_total_batches": len(batches),
                    "repository_id": repository_id,
                }
            )

        return batches

    @staticmethod
    def _make_batch_request(
        payload: dict[str, dict[str, bytes] | dict[str, str] | str]
    ) -> None:
        response = requests.put(
            url=f"{config.INSIGHT_API_BASE_URL}/reinitialize_repository",
            json={
                "repository_id": payload["repository_id"],
                "files": payload["files"],
                "changes": payload["changes"],
                "batch_index": payload["batch_index"],
                "num_total_batches": payload["num_total_batches"],
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
