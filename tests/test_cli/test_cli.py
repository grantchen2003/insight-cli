import argparse, unittest
from unittest.mock import patch

from insight_cli.cli import CLI
from insight_cli.commands import Command, QueryCommand, InitializeCommand


class TestCLI(unittest.TestCase):
    def test_parse_command_with_no_execute_params(self) -> None:
        initialize_command = InitializeCommand()

        parsed_command = CLI._parse_command(initialize_command)

        self.assertEqual(parsed_command["name"], "initialize")
        self.assertEqual(parsed_command["flag_strings"], ["-i", "--initialize"])
        self.assertEqual(
            parsed_command["options"],
            {
                "action": "store_const",
                "const": [],
                "help": initialize_command.description,
            },
        )

    def test_parse_command_with_execute_params(self) -> None:
        query_command = QueryCommand()

        parsed_command = CLI._parse_command(query_command)

        self.assertEqual(parsed_command["name"], "query")
        self.assertEqual(parsed_command["flag_strings"], ["-q", "--query"])
        self.assertEqual(
            parsed_command["options"],
            {
                "help": query_command.description,
                "metavar": tuple(
                    f"<{param_name}>"
                    for param_name in query_command.executor_param_names
                ),
                "nargs": query_command.num_executor_params,
            },
        )

    @patch("insight_cli.cli.CLI._raise_for_invalid_description")
    @patch("insight_cli.cli.CLI._raise_for_invalid_commands")
    def test_raise_for_invalid_args(
        self,
        mock_cli_raise_for_invalid_commands,
        mock_cli_raise_for_invalid_description,
    ) -> None:
        commands = []
        description = ""

        CLI._raise_for_invalid_args(commands, description)

        mock_cli_raise_for_invalid_commands.assert_called_with(commands)
        mock_cli_raise_for_invalid_description.assert_called_with(description)

    def test_raise_for_invalid_commands_with_non_list_commands(self) -> None:
        commands = "hi"

        with self.assertRaises(TypeError) as context_manager:
            CLI._raise_for_invalid_commands(commands)
        self.assertEqual(
            str(context_manager.exception), "[commands] must be of type list"
        )

    def test_raise_for_invalid_commands_with_empty_commands_list(self) -> None:
        commands = []

        with self.assertRaises(ValueError) as context_manager:
            CLI._raise_for_invalid_commands(commands)
        self.assertEqual(
            str(context_manager.exception), "[commands] must be a non-empty list"
        )

    def test_raise_for_invalid_commands_with_list_of_all_non_commands(self) -> None:
        commands = [1, "hello"]

        with self.assertRaises(TypeError) as context_manager:
            CLI._raise_for_invalid_commands(commands)
        self.assertEqual(
            str(context_manager.exception),
            "each command in [commands] must be of type Command",
        )

    def test_raise_for_invalid_commands_with_list_with_some_non_commands(self) -> None:
        commands = [QueryCommand(), "hello"]

        with self.assertRaises(TypeError) as context_manager:
            CLI._raise_for_invalid_commands(commands)
        self.assertEqual(
            str(context_manager.exception),
            "each command in [commands] must be of type Command",
        )

    def test_raise_for_invalid_commands_with_non_unique_flag_strings(self) -> None:
        class Command1(Command):
            def __init__(self):
                super().__init__(
                    flags=["-c", "--command1"],
                    description="command1",
                )

            def execute(self) -> None:
                print("command 1 executor")

        class Command2(Command):
            def __init__(self):
                super().__init__(
                    flags=["-c", "--command2"],
                    description="command2",
                )

            def execute(self) -> None:
                print("command 2 executor")

        commands = [Command1(), Command2()]

        with self.assertRaises(ValueError) as context_manager:
            CLI._raise_for_invalid_commands(commands)
        self.assertEqual(
            str(context_manager.exception),
            "all flag strings in [commands] must be unique",
        )

    def test_raise_for_invalid_commands_with_non_unique_flag_names(self) -> None:
        class Command1(Command):
            def __init__(self):
                super().__init__(
                    flags=["--c"],
                    description="command1",
                )

            def execute(self) -> None:
                print("command 1 executor")

        class Command2(Command):
            def __init__(self):
                super().__init__(
                    flags=["-c"],
                    description="command2",
                )

            def execute(self) -> None:
                print("command 2 executor")

        commands = [Command1(), Command2()]

        with self.assertRaises(ValueError) as context_manager:
            CLI._raise_for_invalid_commands(commands)
        self.assertEqual(
            str(context_manager.exception),
            "all flag names in [commands] must be unique",
        )

    def test_raise_for_invalid_commands_with_valid_commands(self) -> None:
        commands = [QueryCommand(), InitializeCommand()]
        CLI._raise_for_invalid_commands(commands)

    def test_raise_for_invalid_description_with_non_string(self) -> None:
        description = 44

        with self.assertRaises(TypeError) as context_manager:
            CLI._raise_for_invalid_description(description)
        self.assertEqual(
            str(context_manager.exception), "[description] must be of type str"
        )

    def test_raise_for_invalid_description_with_empty_description(self) -> None:
        description = ""
        CLI._raise_for_invalid_description(description)

    def test_raise_for_invalid_description_with_non_empty_description(self) -> None:
        description = "water"
        CLI._raise_for_invalid_description(description)

    def test_add_commands(self) -> None:
        query_command = QueryCommand()
        initialize_command = InitializeCommand()
        commands = [query_command, initialize_command]

        cli = CLI(commands=commands)

        self.assertEqual(
            [action.dest for action in cli._parser._actions],
            ["help", "initialize", "query"],
        )

        for command_name in cli._parsed_commands:
            del cli._parsed_commands[command_name]["get_executor_args"]

        self.assertEqual(
            cli._parsed_commands,
            {
                "initialize": {
                    "command": initialize_command,
                    "name": "initialize",
                    "flag_names": ["i", "initialize"],
                    "flag_strings": ["-i", "--initialize"],
                    "options": {
                        "action": "store_const",
                        "const": [],
                        "help": initialize_command.description,
                    },
                },
                "query": {
                    "command": query_command,
                    "name": "query",
                    "flag_names": ["q", "query"],
                    "flag_strings": ["-q", "--query"],
                    "options": {
                        "help": query_command.description,
                        "metavar": ("<query_string>",),
                        "nargs": 1,
                    },
                },
            },
        )

    @patch("sys.argv", [""])
    def test_parse_arguments_with_one_argument(self) -> None:
        cli = CLI(commands=[QueryCommand(), InitializeCommand()])

        cli.parse_arguments()

        self.assertEqual(
            cli._arguments, argparse.Namespace(initialize=None, query=None)
        )

    @patch("sys.argv", ["", "--query", "water"])
    def test_parse_arguments_with_one_argument(self) -> None:
        cli = CLI(commands=[QueryCommand(), InitializeCommand()])

        cli.parse_arguments()

        self.assertEqual(
            cli._arguments, argparse.Namespace(initialize=None, query=["water"])
        )

    @patch("sys.argv", ["", "--query", "water", "-i"])
    def test_parse_arguments_with_two_arguments(self) -> None:
        cli = CLI(commands=[QueryCommand(), InitializeCommand()])

        cli.parse_arguments()

        self.assertEqual(
            cli._arguments, argparse.Namespace(initialize=[], query=["water"])
        )

    @patch("builtins.print")
    @patch("sys.argv", ["", "--c"])
    def test_execute_invoked_commands_with_one_argument(self, mock_print) -> None:
        class Command1(Command):
            def __init__(self):
                super().__init__(
                    flags=["--c"],
                    description="command1",
                )

            def execute(self) -> None:
                print("command 1 executor")

        cli = CLI(commands=[Command1()])

        cli.parse_arguments()

        cli.execute_invoked_commands()

        mock_print.assert_called_with("command 1 executor")


if __name__ == "__main__":
    unittest.main()
