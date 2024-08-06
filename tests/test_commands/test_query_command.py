from pathlib import Path
from unittest.mock import patch
import contextlib, io, unittest

from insight_cli.repository import InvalidRepositoryError
from insight_cli.commands import QueryCommand
from insight_cli.utils import Color


class TestQueryCommand(unittest.TestCase):
    def test_print_matches_with_one_match(self) -> None:
        Color.init()
        matches = [
            {
                "path": "/example_path",
                "start_line": 3,
                "end_line": 4,
                "content": "const x = () => {...};",
            }
        ]

        with io.StringIO() as buffer, contextlib.redirect_stdout(buffer):
            QueryCommand._print_matches(matches)
            output = buffer.getvalue().strip().split("\n")

        self.assertEqual(
            output,
            [
                str(Path("").resolve() / "/example_path"),
                "Line 3 - 4:",
                Color.green('const x = () => {...};'),
            ],
        )

    def test_print_matches_with_two_matches(self) -> None:
        matches = [
            {
                "path": "/server/insight_cli/config/database.js",
                "start_line": 3,
                "end_line": 15,
                "content": "const connectToDatabase = async () => {...};",
            },
            {
                "path": "/server/insight_cli/server.js",
                "start_line": 25,
                "end_line": 25,
                "content": "await connectToDatabase(app);",
            },
        ]

        with io.StringIO() as buffer, contextlib.redirect_stdout(buffer):
            QueryCommand._print_matches(matches)
            output = buffer.getvalue().strip().split("\n")

        self.assertEqual(
            output,
            [
                str(Path("").resolve() / "/server/insight_cli/config/database.js"),
                "Line 3 - 15:",
                Color.green('const connectToDatabase = async () => {...};'),
                "",
                str(Path("").resolve() / "/server/insight_cli/server.js"),
                "Line 25:",
                Color.green('await connectToDatabase(app);'),
            ],
        )

    @patch("insight_cli.commands.QueryCommand._print_matches")
    @patch("insight_cli.repository.Repository.query")
    def test_execute_with_valid_repository(
        self, mock_repository_query, mock_print_matches
    ) -> None:
        query_command = QueryCommand()
        query_string = "sample_query_string"
        limit = 1

        mock_repository_query.return_value = []

        query_command.execute(query_string, limit)

        mock_repository_query.assert_called_once_with(query_string, limit)
        mock_print_matches.assert_called_once()

    @patch("builtins.print")
    @patch("insight_cli.repository.Repository.query")
    def test_execute_with_invalid_repository(
        self, mock_repository_query, mock_print
    ) -> None:
        Color.init()
        query_command = QueryCommand()
        query_string = "sample_query_string"
        limit = 1

        mock_repository_query.side_effect = InvalidRepositoryError(Path.cwd())

        query_command.execute(query_string, limit)

        mock_repository_query.assert_called_once_with(query_string, limit)
        mock_print.assert_called_once_with(
            Color.red(f"{Path.cwd()} is not an insight repository")
        )

    @patch("insight_cli.repository.Repository.query")
    def test_execute_with_connection_error(self, mock_repository_query) -> None:
        Color.init()
        query_command = QueryCommand()
        query_string = "sample_query_string"
        limit = 1

        mock_repository_query.side_effect = ConnectionError("error message")

        with self.assertRaises(ConnectionError):
            query_command.execute(query_string, limit)

        mock_repository_query.assert_called_once_with(query_string, limit)

    @patch("builtins.print")
    def test_execute_with_invalid_limit(self, mock_print) -> None:
        Color.init()
        query_command = QueryCommand()
        query_string = "sample_query_string"
        limit = 0
        
        query_command.execute(query_string, limit)

        mock_print.assert_called_once_with(
            Color.red("Limit must be a positive integer")
        )


if __name__ == "__main__":
    unittest.main()
