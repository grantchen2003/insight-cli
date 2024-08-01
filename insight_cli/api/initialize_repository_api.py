from concurrent.futures import ThreadPoolExecutor
import copy, requests

from insight_cli.utils import FileChunkifier, ChunkedFileEncoder
from .base.api import API
from insight_cli import config


class InitializeRepositoryAPI(API):
    @staticmethod
    def _add_metadata_to_batches(
        repository_id: str, batched_repository_files: list[dict]
    ) -> list[dict]:
        for i, batch in enumerate(batched_repository_files):
            del batch["size_bytes"]
            batch.update(
                {
                    "batch_index": i,
                    "num_total_batches": len(batched_repository_files),
                    "repository_id": repository_id,
                }
            )

        return batched_repository_files

    @staticmethod
    def _batch_repository_files(
        repository_files: dict[str, bytes], max_batch_size_bytes: int = 10 * 1024**2
    ) -> list[dict]:
        batched_repository_files = []
        empty_batch = {"files": {}, "size_bytes": 0}
        current_batch = copy.deepcopy(empty_batch)

        for file_path, file_content in repository_files.items():
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
                    batched_repository_files.append(current_batch)
                    current_batch = copy.deepcopy(empty_batch)

                current_batch["files"][file_path] = file_content_chunk
                current_batch["size_bytes"] += file_content_chunk["size_bytes"]

        if current_batch != empty_batch:
            batched_repository_files.append(current_batch)

        return batched_repository_files

    @staticmethod
    def _make_batch_request(payload: dict) -> None:
        response = requests.post(
            url=f"{config.INSIGHT_API_BASE_URL}/initialize_repository",
            cookies={"repository_id": payload["repository_id"]},
            json={
                "files": payload["files"],
                "batch_index": payload["batch_index"],
                "num_total_batches": payload["num_total_batches"],
            },
            timeout=None,
        )

        response.raise_for_status()

    @classmethod
    def make_request(
        cls, repository_id: str, repository_files: dict[str, bytes]
    ) -> None:
        repository_files_batches = cls._batch_repository_files(repository_files)
        request_batches = cls._add_metadata_to_batches(
            repository_id, repository_files_batches
        )

        with ThreadPoolExecutor(max_workers=len(request_batches)) as executor:
            executor.map(cls._make_batch_request, request_batches)
