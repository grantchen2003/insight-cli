import contextlib, io, unittest

from insight_cli.commands import QueryCommand
from insight_cli.utils import Color


class TestQueryCommand(unittest.TestCase):
    def test_print_matches_with_no_matches(self) -> None:
        matches = []

        with io.StringIO() as buffer, contextlib.redirect_stdout(buffer):
            QueryCommand._print_matches(matches)
            output = buffer.getvalue().strip().split("\n")

        self.assertEqual(output, [Color.yellow("0 matches found")])

    def test_print_matches_with_one_match(self) -> None:
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
                Color.yellow("1 match found in the following file:"),
                "/example_path",
                f"\tLine 3 - 4: {Color.green('const x = () => {...};')}",
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
                Color.yellow("2 matches found in the following files:"),
                "/server/insight_cli/config/database.js",
                f"\tLine 3 - 15: {Color.green('const connectToDatabase = async () => {...};')}",
                "",
                "/server/insight_cli/server.js",
                f"\tLine 25: {Color.green('await connectToDatabase(app);')}",
            ],
        )


if __name__ == "__main__":
    unittest.main()
