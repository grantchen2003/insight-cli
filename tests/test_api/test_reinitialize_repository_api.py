from unittest.mock import patch
import base64, unittest

from insight_cli.api import ReinitializeRepositoryAPI
from insight_cli.config import config


class TestReinitializeRepositoryAPI(unittest.TestCase):
    def test_batch_repository_file_changes(self) -> None:
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
            ReinitializeRepositoryAPI._add_metadata_to_batches(
                ReinitializeRepositoryAPI._batch_repository_file_changes(
                    repository_file_changes
                ),
                repository_id,
            ),
            [
                {
                    "files": {
                        "file1": {
                            "content": base64.b64encode(
                                repository_file_changes["add"][0][1][: 10 * 1024**2]
                            ).decode("utf-8"),
                            "size_bytes": 10 * 1024**2,
                            "chunk_index": 0,
                            "num_total_chunks": 2,
                        }
                    },
                    "changes": {
                        "file1": "add",
                    },
                    "repository_id": repository_id,
                    "batch_index": 0,
                    "num_total_batches": 3,
                },
                {
                    "files": {
                        "file1": {
                            "content": base64.b64encode(
                                repository_file_changes["add"][0][1][10 * 1024**2 :]
                            ).decode("utf-8"),
                            "size_bytes": 1 * 1024**2,
                            "chunk_index": 1,
                            "num_total_chunks": 2,
                        },
                        "file2": {
                            "content": base64.b64encode(
                                repository_file_changes["add"][1][1][: 9 * 1024**2]
                            ).decode("utf-8"),
                            "size_bytes": 9 * 1024**2,
                            "chunk_index": 0,
                            "num_total_chunks": 2,
                        },
                    },
                    "changes": {
                        "file1": "add",
                        "file2": "add",
                    },
                    "repository_id": repository_id,
                    "batch_index": 1,
                    "num_total_batches": 3,
                },
                {
                    "files": {
                        "file2": {
                            "content": base64.b64encode(
                                repository_file_changes["add"][1][1][9 * 1024**2 :]
                            ).decode("utf-8"),
                            "size_bytes": 1 * 1024**2,
                            "chunk_index": 1,
                            "num_total_chunks": 2,
                        },
                        "file3": {
                            "content": base64.b64encode(
                                repository_file_changes["update"][0][1]
                            ).decode("utf-8"),
                            "size_bytes": 5 * 1024**2,
                            "chunk_index": 0,
                            "num_total_chunks": 1,
                        },
                        "file4": {
                            "content": base64.b64encode(
                                repository_file_changes["update"][1][1]
                            ).decode("utf-8"),
                            "size_bytes": 2 * 1024**2,
                            "chunk_index": 0,
                            "num_total_chunks": 1,
                        },
                    },
                    "changes": {
                        "file2": "add",
                        "file3": "update",
                        "file4": "update",
                        "file5": "delete",
                        "file6": "delete",
                    },
                    "repository_id": repository_id,
                    "batch_index": 2,
                    "num_total_batches": 3,
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
            "batch_index": 1,
            "num_total_batches": 1,
        }

        ReinitializeRepositoryAPI._make_batch_request(payload)

        mock_request_put.assert_called_once_with(
            url=f"{config.INSIGHT_API_BASE_URL}/reinitialize_repository",
            json={
                "repository_id": payload["repository_id"],
                "files": payload["files"],
                "changes": payload["changes"],
                "batch_index": payload["batch_index"],
                "num_total_batches": payload["num_total_batches"],
            },
            timeout=None
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

        self.assertEqual(mock_put.call_count, 3)


if __name__ == "__main__":
    unittest.main()
