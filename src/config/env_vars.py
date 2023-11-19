import os

from dotenv import load_dotenv


class NoEnvironmentMatchError(Exception):
    def __init__(self, env: str):
        self.message = f"{env} does not match any of the valid environments"
        super().__init__(self.message)


class NoEnvironmentVariablesLoadedError(Exception):
    def __init__(self, path):
        self.message = f"No environment variables loaded from {path}"
        super().__init__(self.message)


def _get_dotenv_file_name(env: str) -> str:
    env_to_dotenv_file_name = {
        "dev": ".env.dev",
        "prod": ".env.prod",
    }

    if env not in env_to_dotenv_file_name:
        raise NoEnvironmentMatchError(env)

    return env_to_dotenv_file_name[env]


def load_environment_variables(env: str) -> None:
    config_dir_absolute_path: str = os.path.dirname(os.path.abspath(__file__))

    dotenv_file_name: str = _get_dotenv_file_name(env)

    dotenv_file_absolute_path: str = os.path.join(
        config_dir_absolute_path, dotenv_file_name
    )

    loaded_at_least_one_env_var = load_dotenv(dotenv_file_absolute_path)

    if not loaded_at_least_one_env_var:
        raise NoEnvironmentVariablesLoadedError(dotenv_file_absolute_path)

    print(f"ENV = {env}")
