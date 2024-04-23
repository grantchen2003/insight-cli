from concurrent.futures import ThreadPoolExecutor
import copy, requests, secrets

from insight_cli.utils import FileChunkifier, FileChucksEncoder
from .base.api import API
from insight_cli import config


class InitializeRepositoryAPI(API):
    @staticmethod
    def _add_metadata_to_batches(batched_repository_files: list[dict]) -> list[dict]:
        session_id = secrets.token_hex()

        for i, batch in enumerate(batched_repository_files):
            del batch["size_bytes"]
            batch.update(
                {
                    "batch_index": i,
                    "num_total_batches": len(batched_repository_files),
                    "session_id": session_id,
                }
            )

        return batched_repository_files

    @classmethod
    def _batch_repository_files(
        cls, repository_files: dict[str, bytes], max_batch_size_bytes=10 * 1024**2
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

            utf8_encoded_file_content_chunks = FileChucksEncoder.utf8_encode(
                file_content_chunks
            )

            for file_content_chunk in utf8_encoded_file_content_chunks:
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
    def _make_batch_request(payload: dict) -> dict[str, str]:
        response = requests.post(
            url=f"{config.INSIGHT_API_BASE_URL}/initialize_repository",
            cookies={"session_id": payload["session_id"]},
            json={
                "files": payload["files"],
                "batch_index": payload["batch_index"],
                "num_total_batches": payload["num_total_batches"],
            },
        )

        response.raise_for_status()

        return response.json()

    @classmethod
    def make_request(cls, repository_files: dict[str, bytes]) -> dict[str, str]:
        repository_files_batches = cls._batch_repository_files(repository_files)
        request_batches = cls._add_metadata_to_batches(repository_files_batches)

        with ThreadPoolExecutor(max_workers=len(request_batches)) as executor:
            results = executor.map(cls._make_batch_request, request_batches)
            return {"repository_id": result["repository_id"] for result in results}
