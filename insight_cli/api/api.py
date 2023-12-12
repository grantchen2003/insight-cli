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
        repository_files: dict[str:tuple[bytes, str]], repository_id: str
    ) -> None:
        def make_batch_request(payload):
            response = requests.post(
                url=f"{config.INSIGHT_API_BASE_URL}/reinitialize_repository",
                files=payload["files"],
                data={"repository_id": repository_id, **payload["actions"]}
            )
            response.raise_for_status()

        BYTES_PER_BATCH = 10 * 1024 * 1024

        with ThreadPoolExecutor(max_workers=10) as executor:
            batch_payload = {"files": {}, "actions": {}}
            batch_size = 0
            futures = []

            for file_path, file_data in repository_files.items():
                file_content, file_action = file_data
                file_size = len(file_content)

                if batch_size + file_size > BYTES_PER_BATCH and batch_payload:
                    futures.append(executor.submit(make_batch_request, batch_payload))
                    batch_payload = {"files": {}, "actions": {}}
                    batch_size = 0
                
                if file_action != "delete":
                    batch_payload["files"][file_path] = file_content
                batch_payload["actions"][file_path] = file_action
                batch_size += file_size

            if batch_payload:
                futures.append(executor.submit(make_batch_request, batch_payload))

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
