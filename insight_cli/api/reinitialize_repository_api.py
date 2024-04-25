from concurrent.futures import ThreadPoolExecutor
import copy, requests

from insight_cli.utils import FileChunkifier, ChunkedFileEncoder
from .base.api import API
from insight_cli import config


class ReinitializeRepositoryAPI(API):
    @staticmethod
    def _add_metadata_to_batches(
        batched_repository_file_changes: list[dict], repository_id: str
    ) -> list[dict]:
        for i, batch in enumerate(batched_repository_file_changes):
            del batch["size_bytes"]
            batch.update(
                {
                    "batch_index": i,
                    "num_total_batches": len(batched_repository_file_changes),
                    "repository_id": repository_id,
                }
            )

        return batched_repository_file_changes

    @staticmethod
    def _batch_repository_file_changes(
        repository_file_changes: dict[str, list[tuple[str, bytes]]],
        max_batch_size_bytes: int = 10 * 1024**2,
    ) -> list[dict]:
        batched_repository_file_changes = []
        empty_batch = {"files": {}, "changes": {}, "size_bytes": 0}
        current_batch = copy.deepcopy(empty_batch)

        for change, files in repository_file_changes.items():
            for file_path, file_content in files:
                if change == "delete":
                    current_batch["changes"][file_path] = change
                    continue

                file_content_chunks = FileChunkifier.chunkify_file_content(
                    file_content,
                    max_batch_size_bytes,
                    max_batch_size_bytes - current_batch["size_bytes"],
                )

                encoded_file_content_chunks_with_metadata = (
                    ChunkedFileEncoder.encode_with_metadata(file_content_chunks)
                )

                for file_content_chunk in encoded_file_content_chunks_with_metadata:
                    if (
                        current_batch["size_bytes"] + file_content_chunk["size_bytes"]
                        > max_batch_size_bytes
                    ):
                        batched_repository_file_changes.append(current_batch)
                        current_batch = copy.deepcopy(empty_batch)

                    current_batch["files"][file_path] = file_content_chunk
                    current_batch["changes"][file_path] = change
                    current_batch["size_bytes"] += file_content_chunk["size_bytes"]

        if current_batch != empty_batch:
            batched_repository_file_changes.append(current_batch)

        return batched_repository_file_changes

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
        repository_file_changes_batches = cls._batch_repository_file_changes(
            repository_file_changes
        )

        request_batches = cls._add_metadata_to_batches(
            repository_file_changes_batches, repository_id
        )

        with ThreadPoolExecutor(max_workers=len(request_batches)) as executor:
            executor.map(cls._make_batch_request, request_batches)
