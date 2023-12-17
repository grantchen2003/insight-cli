from unittest.mock import patch, MagicMock
import unittest

from insight_cli.api import ReinitializeRepositoryAPI
from insight_cli.config import config


class TestReinitializeRepositoryAPI(unittest.TestCase):
    def test_get_batched_repository_file_changes(self) -> None:
        repository_id = "123"
        repository_file_changes = {
            "add": [
                ("file1", bytes(11 * 1024**2)),
                ("file2", bytes(10 * 1024**2)),
            ],
            "update": [
                ("file3", bytes(5 * 1024**2)),
                ("file4", bytes(2 * 1024**2)),
            ],
            "delete": [
                ("file5", bytes(0)),
                ("file6", bytes(0)),
            ],
        }

        self.assertEqual(
            ReinitializeRepositoryAPI._get_batched_repository_file_changes(
                repository_id, repository_file_changes
            ),
            [
                {
                    "files": {"file1": bytes(11 * 1024**2)},
                    "changes": {
                        "file1": "add",
                    },
                    "repository_id": repository_id,
                },
                {
                    "files": {"file2": bytes(10 * 1024**2)},
                    "changes": {
                        "file2": "add",
                    },
                    "repository_id": repository_id,
                },
                {
                    "files": {
                        "file3": bytes(5 * 1024**2),
                        "file4": bytes(2 * 1024**2),
                        "file5": bytes(0),
                        "file6": bytes(0),
                    },
                    "changes": {
                        "file3": "update",
                        "file4": "update",
                        "file5": "delete",
                        "file6": "delete",
                    },
                    "repository_id": repository_id,
                },
            ],
        )

    @patch("requests.put")
    def test_make_batch_request(self, mock_request_put) -> None:
        payload = {
            "files": {
                "file3": bytes(5 * 1024**2),
                "file4": bytes(2 * 1024**2),
                "file5": bytes(0),
                "file6": bytes(0),
            },
            "changes": {
                "file3": "update",
                "file4": "update",
                "file5": "delete",
                "file6": "delete",
            },
            "repository_id": "12312",
        }

        ReinitializeRepositoryAPI._make_batch_request(payload)

        mock_request_put.assert_called_once_with(
            url=f"{config.INSIGHT_API_BASE_URL}/reinitialize_repository",
            files=payload["files"],
            data={
                "repository_id": payload["repository_id"],
                "changes": payload["changes"],
            },
        )

    @patch("requests.put")
    def test_make_request(self, mock_put):
        repository_id = "123"
        repository_file_changes = {
            "add": [
                ("file1", bytes(11 * 1024**2)),
                ("file2", bytes(10 * 1024**2)),
            ],
            "update": [
                ("file3", bytes(5 * 1024**2)),
                ("file4", bytes(2 * 1024**2)),
            ],
            "delete": [
                ("file5", bytes(0)),
                ("file6", bytes(0)),
            ],
        }

        ReinitializeRepositoryAPI().make_request(repository_id, repository_file_changes)

        self.assertTrue(mock_put.call_count == 3)


if __name__ == "__main__":
    unittest.main()
