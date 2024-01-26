from unittest.mock import patch, MagicMock
import base64, unittest

from insight_cli.api import InitializeRepositoryAPI
from insight_cli.config import config


class TestInitializeRepositoryAPI(unittest.TestCase):
    def test_chunkify_file_content(self) -> None:
        self.assertEqual(
            InitializeRepositoryAPI._chunkify_file_content(bytes(), 0),
            [],
        )

        size = 1200
        file_content = bytes(range(256)) * (size // 256) + bytes(range(size % 256))
        self.assertEqual(
            InitializeRepositoryAPI._chunkify_file_content(file_content, 500, 100),
            [
                {
                    "content": base64.b64encode(file_content[:100]).decode("utf-8"),
                    "size_bytes": 100,
                    "type": "base64",
                    "chunk_index": 0,
                    "num_total_chunks": 4,
                },
                {
                    "content": base64.b64encode(file_content[100:600]).decode("utf-8"),
                    "type": "base64",
                    "chunk_index": 1,
                    "size_bytes": 500,
                    "num_total_chunks": 4,
                },
                {
                    "content": base64.b64encode(file_content[600:1100]).decode("utf-8"),
                    "chunk_index": 2,
                    "type": "base64",
                    "size_bytes": 500,
                    "num_total_chunks": 4,
                },
                {
                    "content": base64.b64encode(file_content[1100:1200]).decode(
                        "utf-8"
                    ),
                    "size_bytes": 100,
                    "type": "base64",
                    "chunk_index": 3,
                    "num_total_chunks": 4,
                },
            ],
        )

    def test_get_batched_repository_files(self) -> None:
        repository_files = {
            "file1": bytes(10 * 1024**2),
            "file2": bytes(5 * 1024**2),
            "file3": bytes(5 * 1024**2),
            "file4": bytes(4 * 1024**2),
            "file5": bytes(4 * 1024**2),
            "file6": bytes(4 * 1024**2),
        }

        batched_repository_files = (
            InitializeRepositoryAPI._get_batched_repository_files(repository_files)
        )

        # self.assertEqual(len(batched_repository_files), 4)
        self.assertEqual(
            [sorted(batch["files"].keys()) for batch in batched_repository_files],
            [["file1"], ["file2", "file3"], ["file4", "file5", "file6"], ["file6"]],
        )

    @patch("requests.post")
    def test_make_batch_request(self, mock_request_post) -> None:
        expected_response = {"repository_id": "1234123"}
        mock_request_post.return_value = MagicMock(
            json=lambda: expected_response,
            raise_for_status=lambda: None,
        )

        payload = {
            "files": {
                "file2": {
                    "content": bytes(5 * 1024**2),
                    "chunk_index": 1,
                    "num_total_chunks": 1,
                },
                "file3": {
                    "content": bytes(5 * 1024**2),
                    "chunk_index": 1,
                    "num_total_chunks": 1,
                },
            },
            "session_id": "1234asdfdasfas",
            "batch_index": "2",
            "num_total_batches": "4",
        }

        result = InitializeRepositoryAPI._make_batch_request(payload)

        mock_request_post.assert_called_once_with(
            url=f"{config.INSIGHT_API_BASE_URL}/initialize_repository",
            cookies={"session_id": payload["session_id"]},
            json={
                "files": payload["files"],
                "batch_index": payload["batch_index"],
                "num_total_batches": payload["num_total_batches"],
            },
        )

        self.assertEqual(result, expected_response)

    @patch("requests.post")
    def test_make_request(self, mock_post):
        mock_response_data = {"repository_id": "mock_repository_id"}
        mock_post.return_value = MagicMock(
            json=lambda: mock_response_data,
            raise_for_status=lambda: None,
        )

        repository_files = {
            "file1.txt": b"File content 1",
            "file2.txt": b"File content 2",
        }

        self.assertEqual(
            InitializeRepositoryAPI().make_request(repository_files), mock_response_data
        )
        mock_post.assert_called_once()


if __name__ == "__main__":
    unittest.main()
