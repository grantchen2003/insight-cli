from unittest.mock import patch
import unittest

from insight_cli.config import config
from insight_cli.commands import VersionCommand


class TestVersionCommand(unittest.TestCase):
    @patch("builtins.print")
    def test_execute(self, mock_print) -> None:
        version_command = VersionCommand()

        version_command.execute()

        mock_print.assert_called_with(f"insight-cli v{config.INSIGHT_VERSION}")


if __name__ == "__main__":
    unittest.main()
