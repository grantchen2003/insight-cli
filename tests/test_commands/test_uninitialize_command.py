from pathlib import Path
from unittest.mock import patch
import unittest

from insight_cli.commands import UninitializeCommand
from insight_cli.repository import InvalidRepositoryError
from insight_cli.utils import Color


class TestUninitializeCommand(unittest.TestCase):
    @patch("builtins.print")
    @patch("insight_cli.repository.Repository.uninitialize")
    def test_execute_valid_repository_with_invalid_repository(
        self, mock_uninitialize, mock_print
    ):
        mock_uninitialize.side_effect = InvalidRepositoryError(Path.cwd())
        uninitialize_command = UninitializeCommand()

        uninitialize_command.execute()

        mock_print.assert_called_once_with(
            Color.red(f"{Path.cwd()} is an invalid insight repository.")
        )

    @patch("builtins.print")
    @patch("insight_cli.repository.Repository.uninitialize")
    def test_execute_invalid_repository_with_valid_repository(
        self, mock_uninitialize, mock_print
    ):
        uninitialize_command = UninitializeCommand()

        uninitialize_command.execute()

        mock_uninitialize.assert_called_once()
        mock_print.assert_called_once_with(
            Color.green("The current insight repository has been uninitialized.")
        )


if __name__ == "__main__":
    unittest.main()
