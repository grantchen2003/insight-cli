from unittest.mock import patch, MagicMock
import unittest

from insight_cli.api import InitializeRepositoryAPI
from insight_cli.config import config


class TestInitializeRepositoryAPI(unittest.TestCase):
    def test_batch_repository_files(self) -> None:
        repository_files = {
            "file1": bytes(10 * 1024**2),
            "file2": bytes(5 * 1024**2),
            "file3": bytes(5 * 1024**2),
            "file4": bytes(4 * 1024**2),
            "file5": bytes(4 * 1024**2),
            "file6": bytes(4 * 1024**2),
        }

        batched_repository_files = InitializeRepositoryAPI._batch_repository_files(
            repository_files
        )

        self.assertEqual(len(batched_repository_files), 4)
        self.assertEqual(
            [sorted(batch["files"].keys()) for batch in batched_repository_files],
            [["file1"], ["file2", "file3"], ["file4", "file5", "file6"], ["file6"]],
        )

    @patch("requests.post")
    def test_make_batch_request(self, mock_request_post) -> None:
        mock_request_post.return_value = MagicMock(
            json=lambda: None,
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
            "repository_id": "1234asdfdasfas",
            "batch_index": "2",
            "num_total_batches": "4",
        }

        result = InitializeRepositoryAPI._make_batch_request(payload)

        mock_request_post.assert_called_once_with(
            url=f"{config.INSIGHT_API_BASE_URL}/initialize_repository",
            cookies={"repository_id": payload["repository_id"]},
            json={
                "files": payload["files"],
                "batch_index": payload["batch_index"],
                "num_total_batches": payload["num_total_batches"],
            },
            timeout=None
        )

        self.assertIsNone(result)

    @patch("requests.post")
    def test_make_request(self, mock_post):
        mock_post.return_value = MagicMock(
            json=lambda: None,
            raise_for_status=lambda: None,
        )

        repository_id = "mock_repository_id"

        repository_files = {
            "file1.txt": b"File content 1",
            "file2.txt": b"File content 2",
        }

        self.assertIsNone(
            InitializeRepositoryAPI().make_request(repository_id, repository_files)
        )
        
        mock_post.assert_called_once()


if __name__ == "__main__":
    unittest.main()
