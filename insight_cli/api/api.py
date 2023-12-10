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
        NUM_FILES_PER_BATCH = 10  # Adjust this based on your needs

        def upload_batch(batch_files):
            response = requests.post(
                url=f"{config.INSIGHT_API_BASE_URL}/reinitialize_repository",
                files=batch_files,
                json={"repository_id": repository_id},
            )
            response.raise_for_status()

        with ThreadPoolExecutor() as executor:
            batch_files = {}
            futures = []
            for i, (file_path, file_data) in enumerate(repository_files.items()):
                batch_files[file_path] = file_data
                if (i + 1) % NUM_FILES_PER_BATCH == 0 or (i + 1) == len(
                    repository_files
                ):
                    # When the batch is full or it's the last file, submit the batch for upload
                    futures.append(executor.submit(upload_batch, batch_files))
                    batch_files = {}  # Start a new batch

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
