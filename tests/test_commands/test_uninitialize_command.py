import unittest
from unittest.mock import patch, PropertyMock, MagicMock

from insight_cli.commands import UninitializeCommand
from insight_cli.repository import Repository
from insight_cli.utils import Color


class TestUninitializeCommand(unittest.TestCase):
    @patch("builtins.print")
    @patch.object(Repository, "is_valid", new_callable=PropertyMock, return_value=False)
    def test_execute_valid_repository_with_invalid_repository(
        self, mock_is_valid, mock_print
    ):
        uninitialize_command = UninitializeCommand()

        uninitialize_command.execute()

        self.assertTrue(mock_is_valid.called)
        mock_print.assert_called_once_with(
            Color.red("The current directory is not an insight repository.")
        )

    @patch("builtins.print")
    @patch("insight_cli.repository.Repository.uninitialize")
    @patch.object(Repository, "is_valid", new_callable=PropertyMock, return_value=True)
    def test_execute_invalid_repository_with_valid_repository(
        self, mock_is_valid, mock_uninitialize, mock_print
    ):
        uninitialize_command = UninitializeCommand()

        uninitialize_command.execute()

        self.assertTrue(mock_is_valid.called)
        mock_uninitialize.assert_called_once()
        mock_print.assert_called_once_with(
            Color.green("The current insight repository has been uninitialized.")
        )


if __name__ == "__main__":
    unittest.main()
