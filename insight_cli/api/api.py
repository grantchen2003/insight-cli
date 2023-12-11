import requests
from concurrent.futures import ThreadPoolExecutor

from insight_cli import config


class API:
    @staticmethod
    def make_initialize_repository_request(
        repository_files: dict[str:bytes],
    ) -> dict[str, str]:
        response = requests.post(
            url=f"{config.INSIGHT_API_BASE_URL}/initialize_repository",
            files=repository_files,
        )

        response.raise_for_status()

        return response.json()

    @staticmethod
    def make_query_repository_request(
        repository_id: str, query_string: str
    ) -> list[dict]:
        response = requests.get(
            url=f"{config.INSIGHT_API_BASE_URL}/query?repository-id={repository_id}&query-string={query_string}"
        )

        response.raise_for_status()

        return response.json()

    @staticmethod
    def make_reinitialize_repository_request(
        repository_files: dict[str:bytes], repository_id: str
    ) -> None:
        # TODO need to implement
        return
        def make_batch_request(batch_files):
            response = requests.post(
                url=f"{config.INSIGHT_API_BASE_URL}/reinitialize_repository",
                files=batch_files,
                json={"repository_id": repository_id},
            )
            response.raise_for_status()

        BYTES_PER_BATCH = 10 * 1024 * 1024

        with ThreadPoolExecutor(max_workers=10) as executor:
            batch_files = {}
            batch_size = 0
            futures = []
            for file_path, file_data in repository_files.items():
                file_size = len(file_data)

                if batch_size + file_size > BYTES_PER_BATCH and batch_files:
                    futures.append(executor.submit(make_batch_request, batch_files))
                    batch_files = {}
                    batch_size = 0

                batch_files[file_path] = file_data
                batch_size += file_size

            if batch_files:
                futures.append(executor.submit(make_batch_request, batch_files))

            for future in futures:
                future.result()

    @staticmethod
    def make_validate_repository_id_request(repository_id: str) -> dict[str, bool]:
        response = requests.post(
            headers={"Content-Type": "application/json"},
            url=f"{config.INSIGHT_API_BASE_URL}/validate_repository_id",
            json={"repository_id": repository_id},
        )

        response.raise_for_status()

        return response.json()
