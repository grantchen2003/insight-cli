from unittest.mock import patch, PropertyMock
import contextlib, io, unittest

from insight_cli.commands import InitializeCommand
from insight_cli.utils import Color


class TestInitializeCommand(unittest.TestCase):
    @patch("builtins.print")
    @patch("insight_cli.repository.Repository.initialize")
    @patch("insight_cli.repository.Repository.is_valid", new_callable=PropertyMock, return_value=False)
    def test_execute_with_invalid_repository(self, mock_repository_is_valid, mock_initialize, mock_print) -> None:
        initialize_command = InitializeCommand()

        initialize_command.execute()

        mock_repository_is_valid.assert_called_once()
        mock_initialize.assert_called_once()
        mock_print.assert_called_once_with(
            Color.green("The current directory has been initialized as an insight repository.")
        )

    @patch("insight_cli.repository.Repository.reinitialize")
    @patch("insight_cli.repository.Repository.is_valid", new_callable=PropertyMock, return_value=True)
    def test_execute_with_valid_repository(self, mock_repository_is_valid, mock_reinitialize) -> None:
        initialize_command = InitializeCommand()

        with io.StringIO() as buffer, contextlib.redirect_stdout(buffer):
            initialize_command.execute()
            output = buffer.getvalue().strip().split("\n")

        mock_repository_is_valid.assert_called_once()
        mock_reinitialize.assert_called_once()
        self.assertEqual(output, [
            Color.yellow(
                "The current directory is already an insight repository. This insight repository will be reinitialized."
            ),
            Color.green("The current insight repository has been reinitialized.")
        ])

    @patch("builtins.print")
    @patch("insight_cli.repository.Repository.initialize")
    @patch("insight_cli.repository.Repository.is_valid", new_callable=PropertyMock, return_value=False)
    def test_execute_with_invalid_repository_and_exception(self, mock_repository_is_valid, mock_reinitialize, mock_print) -> None:
        initialize_command = InitializeCommand()
        mock_reinitialize.side_effect = Exception("error message")

        initialize_command.execute()

        mock_repository_is_valid.assert_called_once()
        mock_reinitialize.assert_called_once()
        mock_print.assert_called_once_with(Color.red("error message"))


if __name__ == "__main__":
    unittest.main()
