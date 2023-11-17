from pathlib import Path
from unittest.mock import patch

import os
import sys
import unittest

NUM_PARENT_DIRECTORIES_TO_PROJECT_ROOT = 2
project_root_path = (
    Path(__file__).resolve().parents[NUM_PARENT_DIRECTORIES_TO_PROJECT_ROOT]
)

sys.path.append(str(project_root_path))

from src.config.env_vars import (
    load_environment_variables,
    NoEnvironmentMatchError,
    NoEnvironmentVariablesLoadedError,
)


class TestEnvVars(unittest.TestCase):
    @patch("src.config.env_vars.load_dotenv")
    def test_load_environment_variables(self, mock_load_dotenv) -> None:
        env = "prod"
        path = os.path.abspath(f"../../src/config/.env.{env}")
        mock_load_dotenv.return_value = True
        load_environment_variables(env)
        mock_load_dotenv.assert_called_with(path)

        env = "staging"
        mock_load_dotenv.return_value = False
        with self.assertRaises(NoEnvironmentMatchError) as context:
            load_environment_variables(env)
            self.assertEqual(
                context.exception, f"{env} does not match any of the valid environments"
            )

        env = "dev"
        path = os.path.abspath(f"../../src/config/.env.{env}")
        mock_load_dotenv.return_value = False
        with self.assertRaises(NoEnvironmentVariablesLoadedError) as context:
            load_environment_variables(env)
            self.assertEqual(
                context.exception, f"No environment variables loaded from {path}"
            )
        mock_load_dotenv.assert_called_with(path)


if __name__ == "__main__":
    unittest.main()
