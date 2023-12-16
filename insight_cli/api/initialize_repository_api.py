from concurrent.futures import ThreadPoolExecutor
from typing import Union
import grpc, requests, secrets, time

from .base.api import API
from .proto import repository_pb2_grpc, repository_pb2
from insight_cli import config


class InitializeRepositoryAPI(API):
    @staticmethod
    def _generate_request_session_id(length: int = 16) -> str:
        return secrets.token_hex(length)

    @staticmethod
    def _get_batched_repository_files(
        repository_files: dict[str, bytes]
    ) -> list[dict[str, bytes]]:
        MAX_BATCH_SIZE_BYTES = 4 * 1024**2

        batches = []
        current_batch = {"files": {}}
        current_batch_size_bytes = 0

        for file_path, file_content in repository_files.items():
            file_size_bytes = len(file_content)

            if current_batch_size_bytes + file_size_bytes > MAX_BATCH_SIZE_BYTES:
                batches.append(current_batch)
                current_batch = {"files": {}}
                current_batch_size_bytes = 0

            current_batch["files"][file_path] = file_content
            current_batch_size_bytes += file_size_bytes

        batches.append(current_batch)

        return batches

    @classmethod
    def _add_batches_request_metadata(
        cls, batches: list[dict[str, bytes]]
    ) -> list[dict[str, Union[bytes, int, str]]]:
        session_id = cls._generate_request_session_id()
        num_total_batches = len(batches)

        for i, batch in enumerate(batches):
            batch.update(
                {
                    "batch_number": i + 1,
                    "num_total_batches": num_total_batches,
                    "session_id": session_id,
                }
            )

        return batches

    @staticmethod
    def _make_batch_request_grpc(payload: dict[str, dict[str, bytes]]) -> str:
        with grpc.insecure_channel(f"127.0.0.1:50051") as channel:
            stub = repository_pb2_grpc.RepositoryStub(channel)

            request = repository_pb2.InitializeRepositoryRequest(
                files=payload["files"],
                session_id=payload["session_id"],
                batch_number=payload["batch_number"],
                num_total_batches=payload["num_total_batches"],
            )

            response = stub.InitializeRepository(request)

            return response.repository_id
        
    @staticmethod
    def _make_batch_request_rest(payload: dict[str, dict[str, bytes]]) -> dict[str, str]:
        response = requests.post(
            url=f"http://127.0.0.1:5000/initialize_repository",
            files=payload["files"],
            data={
                "session_id": payload["session_id"],
                "batch_num": payload["batch_number"],
                "num_total_batches": payload["num_total_batches"],
            },
        )

        response.raise_for_status()

        return response.json()

    @classmethod
    def make_request(cls, repository_files: dict[str, bytes]) -> dict[str, str]:
        request_batches = cls._add_batches_request_metadata(
            cls._get_batched_repository_files(repository_files)
        )

        with ThreadPoolExecutor(max_workers=len(request_batches)) as executor:
            start = time.perf_counter()
            results = list(executor.map(cls._make_batch_request_grpc, request_batches))
            print(f"time: {time.perf_counter() - start}")
            return {"repository_id": repository_id for repository_id in results}
