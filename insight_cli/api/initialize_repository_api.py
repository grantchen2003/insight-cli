from concurrent.futures import ThreadPoolExecutor
import copy, requests, secrets

from .base.api import API
from insight_cli import config


class InitializeRepositoryAPI(API):
    @staticmethod
    def _generate_request_session_id() -> str:
        return secrets.token_hex()

    @staticmethod
    def _chunkify_file_content(
        file_content: bytes, chunk_size_bytes: int, first_chunk_size_bytes: int = 0
    ) -> list[bytes]:
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
                "content": file_content_chunk,
                "chunk_index": i,
                "num_total_chunks": len(file_content_chunks),
            }
            for i, file_content_chunk in enumerate(file_content_chunks)
        ]

    @classmethod
    def _get_batched_repository_files(
        cls, repository_files: dict[str, bytes]
    ) -> list[dict]:
        MAX_BATCH_SIZE_BYTES = 10 * 1024**2

        batches = []
        empty_batch = {"files": {}, "size_bytes": 0}

        current_batch = copy.deepcopy(empty_batch)

        for file_path, file_content in repository_files.items():
            file_content_chunks = cls._chunkify_file_content(
                file_content,
                MAX_BATCH_SIZE_BYTES,
                MAX_BATCH_SIZE_BYTES - current_batch["size_bytes"],
            )

            for file_content_chunk in file_content_chunks:
                file_content_chunk_size_bytes = len(file_content_chunk["content"])

                if (
                    current_batch["size_bytes"] + file_content_chunk_size_bytes
                    > MAX_BATCH_SIZE_BYTES
                ):
                    batches.append(current_batch)
                    current_batch = copy.deepcopy(empty_batch)

                current_batch["files"][file_path] = file_content_chunk
                current_batch["size_bytes"] += file_content_chunk_size_bytes

        if current_batch != empty_batch:
            batches.append(current_batch)

        session_id = cls._generate_request_session_id()

        for i, batch in enumerate(batches):
            del batch["size_bytes"]
            batch.update(
                {
                    "batch_index": i,
                    "num_total_batches": len(batches),
                    "session_id": session_id,
                }
            )

        return batches

    @staticmethod
    def _make_batch_request(payload: dict) -> dict[str, str]:
        response = requests.post(
            url=f"{config.INSIGHT_API_BASE_URL}/initialize_repository",
            cookies={"session_id": payload["session_id"]},
            data={
                "files": payload["files"],
                "batch_index": payload["batch_index"],
                "num_total_batches": payload["num_total_batches"],
            },
        )

        response.raise_for_status()

        return response.json()

    @classmethod
    def make_request(cls, repository_files: dict[str, bytes]) -> dict[str, str]:
        request_batches = cls._get_batched_repository_files(repository_files)

        with ThreadPoolExecutor(max_workers=len(request_batches)) as executor:
            results = executor.map(cls._make_batch_request, request_batches)
            return {"repository_id": result["repository_id"] for result in results}
