import unittest

from insight_cli.commands.base.flag import Flag


class TestFlag(unittest.TestCase):
    def test_raise_for_invalid_args_with_non_string(self) -> None:
        invalid_flag_string = 3

        with self.assertRaises(TypeError) as context_manager:
            Flag._raise_for_invalid_args(invalid_flag_string)

        self.assertEqual(
            str(context_manager.exception),
            f"{invalid_flag_string} must be of type str"
        )

    def test_raise_for_invalid_args_with_string_containing_whitespaces(self) -> None:
        invalid_flag_string = "-- lol"

        with self.assertRaises(ValueError) as context_manager:
            Flag._raise_for_invalid_args(invalid_flag_string)

        self.assertEqual(
            str(context_manager.exception),
            f"{invalid_flag_string} cannot contain any whitespaces"
        )

    def test_raise_for_invalid_args_with_too_short_string_length(self) -> None:
        invalid_flag_string = "-"

        with self.assertRaises(ValueError) as context_manager:
            Flag._raise_for_invalid_args(invalid_flag_string)

        self.assertEqual(
            str(context_manager.exception),
            f"{invalid_flag_string} must have length of at least {Flag._MIN_PREFIX_LENGTH + Flag._MIN_NAME_LENGTH}"
        )

    def test_raise_for_invalid_args_with_invalid_prefix(self) -> None:
        invalid_flag_string = "klol"

        with self.assertRaises(ValueError) as context_manager:
            Flag._raise_for_invalid_args(invalid_flag_string)

        self.assertEqual(
            str(context_manager.exception),
            f"the first {Flag._MIN_PREFIX_LENGTH} characters of {invalid_flag_string} must all be '{Flag._PREFIX_CHAR}'"
        )

    def test_raise_for_invalid_args_with_invalid_name(self) -> None:
        invalid_flag_string = "--"

        with self.assertRaises(ValueError) as context_manager:
            Flag._raise_for_invalid_args(invalid_flag_string)

        self.assertEqual(
            str(context_manager.exception),
            f"{invalid_flag_string} must have a name of at least length {Flag._MIN_NAME_LENGTH}"
        )

    def test_raise_for_invalid_args_with_valid_flag(self) -> None:
        valid_flag_string = "--i"

        Flag._raise_for_invalid_args(valid_flag_string)

    def test_str(self) -> None:
        flag = Flag("--i")
        self.assertEqual(str(flag), "--i")

    def test_name(self) -> None:
        flag = Flag("--i")
        self.assertEqual(flag.name, "i")

    def test_prefix(self) -> None:
        flag = Flag("--i")
        self.assertEqual(flag.prefix, "--")


if __name__ == "__main__":
    unittest.main()
