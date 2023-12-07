from unittest.mock import patch
import unittest

from insight_cli.commands import Command


class TestCommand(unittest.TestCase):
    @patch("insight_cli.commands.Command._raise_for_invalid_executor")
    @patch("insight_cli.commands.Command._raise_for_invalid_description")
    @patch("insight_cli.commands.Command._raise_for_invalid_flags")
    def test_raise_for_invalid_args(
            self,
            mock_raise_for_invalid_flags,
            mock_raise_for_invalid_description,
            mock_raise_for_invalid_executor
    ) -> None:
        flags, description, executor = [], "", lambda x: 5

        Command._raise_for_invalid_args(flags, description, executor)

        mock_raise_for_invalid_flags.assert_called_once_with(flags)
        mock_raise_for_invalid_description.assert_called_once_with(description)
        mock_raise_for_invalid_executor.assert_called_once_with(executor)

    def test_raise_for_invalid_flags_with_non_list(self) -> None:
        invalid_flags = 3

        with self.assertRaises(TypeError) as context_manager:
            Command._raise_for_invalid_flags(invalid_flags)

        self.assertEqual(
            str(context_manager.exception),
            f"{invalid_flags} must be a list"
        )

    def test_raise_for_invalid_flags_with_too_few_flags(self) -> None:
        invalid_flags = []

        with self.assertRaises(ValueError) as context_manager:
            Command._raise_for_invalid_flags(invalid_flags)

        self.assertEqual(
            str(context_manager.exception),
            f"at least {Command._MIN_NUM_REQUIRED_FLAGS} flag(s) required"
        )

    def test_raise_for_invalid_flags_with_list_containing_non_flags(self) -> None:
        invalid_flags = [3]

        with self.assertRaises(TypeError) as context_manager:
            Command._raise_for_invalid_flags(invalid_flags)

        self.assertEqual(
            str(context_manager.exception),
            f"every flag in {invalid_flags} must be of type str"
        )

    def test_raise_for_invalid_flags_with_non_unique_flags(self) -> None:
        invalid_flags = ["--i", "--i"]

        with self.assertRaises(ValueError) as context_manager:
            Command._raise_for_invalid_flags(invalid_flags)

        self.assertEqual(
            str(context_manager.exception),
            f"every flag in {invalid_flags} must be unique"
        )

    def test_raise_for_invalid_flags_with_valid_flags(self) -> None:
        valid_flags = ["--i"]

        Command._raise_for_invalid_flags(valid_flags)

    def test_raise_for_invalid_description_with_non_string(self) -> None:
        invalid_description = 3

        with self.assertRaises(TypeError) as context_manager:
            Command._raise_for_invalid_description(invalid_description)

        self.assertEqual(
            str(context_manager.exception),
            f"{invalid_description} must be of type str"
        )

    def test_raise_for_invalid_description_with_whitespace_string(self) -> None:
        invalid_description = "     "

        with self.assertRaises(ValueError) as context_manager:
            Command._raise_for_invalid_description(invalid_description)

        self.assertEqual(
            str(context_manager.exception),
            f"{invalid_description} must not be a whitespace string"
        )

    def test_raise_for_invalid_executor_with_invalid_executor_types(self) -> None:
        def executor(color: str, age) -> str:
            return f"{color} {age}"

        with self.assertRaises(ValueError) as context_manager:
            Command._raise_for_invalid_executor(executor)

        self.assertEqual(
            str(context_manager.exception),
            f"the {executor} parameter 'age' does not have a type"
        )

    def test_execute_abstract_method_raises_error_on_execute(self) -> None:
        with self.assertRaises(TypeError):
            Command(["--i"], "example description")

    def test_description(self) -> None:
        class TestConcreteCommand(Command):
            def execute(self) -> int:
                return 4

        command = TestConcreteCommand(["--i"], "descr")
        self.assertEqual(command.description, "descr")

    def test_flags(self) -> None:
        class TestConcreteCommand(Command):
            def execute(self) -> int:
                return 4

        flags = ["--test", "-t"]
        command = TestConcreteCommand(flags, "descr")

        self.assertEqual(len(command.flags), len(flags))

        for flag_string, flag in zip(flags, command.flags):
            self.assertEqual(flag_string, str(flag))

    def test_has_executor_params_with_no_executor_params(self) -> None:
        class TestConcreteCommand(Command):
            def execute(self) -> int:
                return 4

        command = TestConcreteCommand(["--test", "-t"], "descr")
        self.assertEqual(command.has_executor_params, False)

    def test_has_executor_params_with_executor_params(self) -> None:
        class TestConcreteCommand(Command):
            def execute(self, num: int) -> int:
                return num

        command = TestConcreteCommand(["--test", "-t"], "descr")
        self.assertEqual(command.has_executor_params, True)

    def test_num_executor_params_with_no_executor_params(self) -> None:
        class TestConcreteCommand(Command):
            def execute(self) -> int:
                return 5

        command = TestConcreteCommand(["--test", "-t"], "descr")
        self.assertEqual(command.num_executor_params, 0)

    def test_num_executor_params_with_executor_params(self) -> None:
        class TestConcreteCommand(Command):
            def execute(self, num: int) -> int:
                return num

        command = TestConcreteCommand(["--test", "-t"], "descr")
        self.assertEqual(command.num_executor_params, 1)

    def test_executor_params_with_no_executor_params(self) -> None:
        class TestConcreteCommand(Command):
            def execute(self) -> int:
                return 5

        command = TestConcreteCommand(["--test", "-t"], "descr")
        self.assertEqual(command.executor_params, [])

    def test_executor_params_with_executor_params(self) -> None:
        class TestConcreteCommand(Command):
            def execute(self, num: int) -> int:
                return num

        command = TestConcreteCommand(["--test", "-t"], "descr")
        self.assertEqual(command.executor_params, [{"name": "num", "type": int}])

    def test_executor_param_names_with_no_executor_params(self) -> None:
        class TestConcreteCommand(Command):
            def execute(self) -> int:
                return 5

        command = TestConcreteCommand(["--test", "-t"], "descr")
        self.assertEqual(command.executor_param_names, [])

    def test_executor_param_names_with_executor_params(self) -> None:
        class TestConcreteCommand(Command):
            def execute(self, num: int) -> int:
                return num

        command = TestConcreteCommand(["--test", "-t"], "descr")
        self.assertEqual(command.executor_param_names, ["num"])

    def test_executor_param_types_with_no_executor_params(self) -> None:
        class TestConcreteCommand(Command):
            def execute(self) -> int:
                return 5

        command = TestConcreteCommand(["--test", "-t"], "descr")
        self.assertEqual(command.executor_param_types, [])

    def test_executor_param_types_with_executor_params(self) -> None:
        class TestConcreteCommand(Command):
            def execute(self, num: int) -> int:
                return num

        command = TestConcreteCommand(["--test", "-t"], "descr")
        self.assertEqual(command.executor_param_types, [int])


if __name__ == "__main__":
    unittest.main()
