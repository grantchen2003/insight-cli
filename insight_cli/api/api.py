from io import BufferedReader
import requests, threading, time

from insight_cli.utils import File
from insight_cli import config


class API:
    @staticmethod
    def make_initialize_repository_request(
        repository_nested_files: dict[str:BufferedReader],
    ) -> dict[str, str]:
        response = requests.post(
            url=f"{config.INSIGHT_API_BASE_URL}/initialize_repository",
            files=repository_nested_files,
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
    def make_reinitialize_repository_request_chunk(
        repository_nested_files: dict[str:BufferedReader], repository_id: str
    ) -> None:
        response = requests.post(
            url=f"{config.INSIGHT_API_BASE_URL}/reinitialize_repository",
            files=repository_nested_files,
            json={"repository_id": repository_id},
        )
        response.raise_for_status()

    @staticmethod
    def make_reinitialize_repository_request(
        repository_nested_files: list[File], repository_id: str
    ) -> None:
        # just used to artificially size up the size of the repo for testing 
        for _ in range(len(repository_nested_files) * 25):
            file = repository_nested_files[0]
            repository_nested_files.append(File(file.path, file.binary_data))
        
        
        """Non multithreading method"""
        start = time.perf_counter()
        files = {}
        for file in repository_nested_files:
            with open(file._path, "rb") as binary_data:
                files[str(file.path)] = binary_data.read()
        API.make_reinitialize_repository_request_chunk(files, repository_id)
        print(f"time 1: {time.perf_counter() - start}") 
        
        
        """Multithreading method, split into chunks, create thread for each chunk"""
        """
        this method is twice as slow as the non-multithreading method. 
        chunkify takes half the time and threaded api requests take half of the time
        """
        num_chunks = 50 # this number has to be just right
        print(f"num chunks: {num_chunks}")
        start = time.perf_counter()
        max_file_chunk_size_bytes = (
            sum(file.size_bytes for file in repository_nested_files) // num_chunks
        )
        file_chunks = []
        file_chunk = []
        file_chunk_size_bytes = 0
        for file in repository_nested_files:
            if file_chunk_size_bytes + file.size_bytes > max_file_chunk_size_bytes:
                file_chunks.append(file_chunk.copy())
                file_chunk = []
                file_chunk_size_bytes = 0
            file_chunk.append(file)
            file_chunk_size_bytes += file.size_bytes
        file_chunks.append(file_chunk)
        print(f"chunkify time: {time.perf_counter() - start}")

        start = time.perf_counter()
        threads = []
        for file_chunk in file_chunks:
            files = {}
            for file in file_chunk:                
                with open(file._path, "rb") as binary_data:
                    files[str(file.path)] = binary_data.read()
            thread = threading.Thread(target=API.make_reinitialize_repository_request_chunk, args=(files, repository_id))
            threads.append(thread)
            thread.start()
               
        for thread in threads:
            thread.join()
        print(f"time 2: {time.perf_counter() - start}")
        
    @staticmethod
    def make_validate_repository_id_request(repository_id: str) -> dict[str, bool]:
        response = requests.post(
            headers={"Content-Type": "application/json"},
            url=f"{config.INSIGHT_API_BASE_URL}/validate_repository_id",
            json={"repository_id": repository_id},
        )

        response.raise_for_status()

        return response.json()
