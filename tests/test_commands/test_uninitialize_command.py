from pathlib import Path
from unittest.mock import patch
import unittest

from insight_cli.commands import UninitializeCommand
from insight_cli.repository import InvalidRepositoryError
from insight_cli.utils import Color


class TestUninitializeCommand(unittest.TestCase):
    @patch("builtins.print")
    @patch("insight_cli.repository.Repository.uninitialize")
    @patch("insight_cli.api.ValidateRepositoryIdAPI.make_request")
    def test_execute_valid_repository_with_invalid_repository(
        self,
        mock_validate_repository_id_api_make_request,
        mock_uninitialize,
        mock_print,
    ):
        mock_uninitialize.side_effect = InvalidRepositoryError(Path.cwd())
        uninitialize_command = UninitializeCommand()

        mock_validate_repository_id_api_make_request.return_value = {
            "repository_id_is_valid": True
        }

        uninitialize_command.execute()

        mock_validate_repository_id_api_make_request.assert_called_once()
        mock_print.assert_called_once_with(
            Color.red(f"{Path.cwd()} is not an insight repository")
        )

    @patch("builtins.print")
    @patch("insight_cli.repository.Repository.uninitialize")
    @patch("insight_cli.api.ValidateRepositoryIdAPI.make_request")
    def test_execute_invalid_repository_with_valid_repository(
        self,
        mock_validate_repository_id_api_make_request,
        mock_uninitialize,
        mock_print,
    ):
        uninitialize_command = UninitializeCommand()

        mock_validate_repository_id_api_make_request.return_value = {
            "repository_id_is_valid": True
        }

        uninitialize_command.execute()

        mock_validate_repository_id_api_make_request.assert_called_once()
        mock_uninitialize.assert_called_once()
        mock_print.assert_called_once_with(
            Color.green(f"Uninitialized insight repository in {Path.cwd().resolve()}")
        )


if __name__ == "__main__":
    unittest.main()
