from dotenv import load_dotenv
import os


class NoEnvironmentMathError(Exception):
    def __init__(self, env: str):
        self.message = f"{env} does not match any of the valid environments"
        super().__init__(self.message)


class NoEnvironmentVariablesLoadedError(Exception):
    def __init__(self, path):
        self.message = f"No environment variables loaded from {path}"
        super().__init__(self.message)


def load_environment_variables(env: str) -> None:
    config_dir_absolute_path = os.path.dirname(os.path.abspath(__file__))

    env_files = {"dev": ".env.dev", "prod": ".env.prod"}

    if env not in env_files:
        raise NoEnvironmentMathError(env)

    env_file_absolute_path = os.path.join(config_dir_absolute_path, env_files[env])

    if not load_dotenv(env_file_absolute_path):
        raise NoEnvironmentVariablesLoadedError(env_file_absolute_path)

    print(f"ENV = {env}")
