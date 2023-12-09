from pathlib import Path
from unittest.mock import patch, PropertyMock
import contextlib, io, unittest

from insight_cli.commands import InitializeCommand
from insight_cli.repository import InvalidRepositoryError
from insight_cli.utils import Color


class TestInitializeCommand(unittest.TestCase):
    @patch("builtins.print")
    @patch("insight_cli.repository.Repository.initialize")
    @patch(
        "insight_cli.repository.Repository.is_valid",
        new_callable=PropertyMock,
        return_value=False,
    )
    def test_execute_with_invalid_repository(
        self, mock_repository_is_valid, mock_initialize, mock_print
    ) -> None:
        initialize_command = InitializeCommand()

        initialize_command.execute()

        mock_repository_is_valid.assert_called_once()
        mock_initialize.assert_called_once()
        mock_print.assert_called_once_with(
            Color.green(f"Initialized insight repository in {Path.cwd()}")
        )

    @patch("insight_cli.repository.Repository.reinitialize")
    @patch(
        "insight_cli.repository.Repository.is_valid",
        new_callable=PropertyMock,
        return_value=True,
    )
    def test_execute_with_valid_repository(
        self, mock_repository_is_valid, mock_reinitialize
    ) -> None:
        initialize_command = InitializeCommand()

        with io.StringIO() as buffer, contextlib.redirect_stdout(buffer):
            initialize_command.execute()
            output = buffer.getvalue().strip().split("\n")

        mock_repository_is_valid.assert_called_once()
        mock_reinitialize.assert_called_once()
        self.assertEqual(
            output,
            [
                Color.green(
                    f"Reinitialized existing insight repository in {Path.cwd().resolved()}"
                )
            ],
        )

    @patch("insight_cli.repository.Repository.initialize")
    @patch(
        "insight_cli.repository.Repository.is_valid",
        new_callable=PropertyMock,
        return_value=False,
    )
    def test_execute_with_non_invalid_repository_exception(
        self, mock_repository_is_valid, mock_initialize
    ) -> None:
        initialize_command = InitializeCommand()
        mock_initialize.side_effect = TypeError("error message")

        with self.assertRaises(TypeError) as context_manager:
            initialize_command.execute()
            self.assertEqual(str(context_manager.exception), "error message")

        mock_repository_is_valid.assert_called_once()
        mock_initialize.assert_called_once()

    @patch("builtins.print")
    @patch("insight_cli.repository.Repository.initialize")
    @patch(
        "insight_cli.repository.Repository.is_valid",
        new_callable=PropertyMock,
        return_value=False,
    )
    def test_execute_with_invalid_repository_exception(
        self, mock_repository_is_valid, mock_initialize, mock_print
    ) -> None:
        path = Path()
        mock_initialize.side_effect = InvalidRepositoryError(path)
        initialize_command = InitializeCommand()

        initialize_command.execute()

        mock_repository_is_valid.assert_called_once()
        mock_print.assert_called_once_with(
            Color.red(f"{path.resolve()} is not an insight repository")
        )


if __name__ == "__main__":
    unittest.main()
