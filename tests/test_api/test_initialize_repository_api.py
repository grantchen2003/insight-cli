from unittest.mock import patch, MagicMock
import unittest

from insight_cli.api import InitializeRepositoryAPI
from insight_cli.config import config


class TestInitializeRepositoryAPI(unittest.TestCase):
    def test_get_batched_repository_files(self) -> None:
        repository_files = {
            "file1": bytes(10 * 1024**2),
            "file2": bytes(5 * 1024**2),
            "file3": bytes(5 * 1024**2),
            "file4": bytes(4 * 1024**2),
            "file5": bytes(4 * 1024**2),
            "file6": bytes(4 * 1024**2),
        }

        self.assertEqual(
            InitializeRepositoryAPI._get_batched_repository_files(repository_files),
            [
                {
                    "files": {
                        "file1": bytes(10 * 1024**2),
                    }
                },
                {
                    "files": {
                        "file2": bytes(5 * 1024**2),
                        "file3": bytes(5 * 1024**2),
                    }
                },
                {
                    "files": {
                        "file4": bytes(4 * 1024**2),
                        "file5": bytes(4 * 1024**2),
                    }
                },
                {
                    "files": {
                        "file6": bytes(4 * 1024**2),
                    }
                },
            ],
        )

    def test_add_batches_request_metadata(self) -> None:
        batches = InitializeRepositoryAPI._add_batches_request_metadata(
            [
                {
                    "files": {
                        "file1": bytes(10 * 1024**2),
                    }
                },
                {
                    "files": {
                        "file2": bytes(5 * 1024**2),
                        "file3": bytes(5 * 1024**2),
                    }
                },
            ]
        )

        for i, batch in enumerate(batches):
            self.assertEqual(batch["batch_number"], i + 1)
            self.assertEqual(batch["num_total_batches"], len(batches))

    @patch("requests.post")
    def test_make_batch_request(self, mock_request_post) -> None:
        expected_response = {"repository_id": "1234123"}
        mock_request_post.return_value = MagicMock(
            json=lambda: expected_response,
            raise_for_status=lambda: None,
        )

        payload = {
            "files": {
                "file2": bytes(5 * 1024**2),
                "file3": bytes(5 * 1024**2),
            },
            "session_id": "1234asdfdasfas",
            "batch_number": "2",
            "num_total_batches": "4",
        }

        result = InitializeRepositoryAPI._make_batch_request(payload)

        mock_request_post.assert_called_once_with(
            url=f"{config.INSIGHT_API_BASE_URL}/initialize_repository",
            cookies={"session_id": payload["session_id"]},
            files=payload["files"],
            data={
                "batch_num": payload["batch_number"],
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
