from dotenv import load_dotenv


class NoEnvironmentMathError(Exception):
    def __init__(self, env: str):
        self.message = f"{env} does not match any of the valid environments"
        super().__init__(self.message)


def load_environment_variables(env: str) -> None:
    env_file_paths = {
        "dev": ".env.dev",
        "prod": ".env.prod",
    }
    if env not in env_file_paths:
        raise NoEnvironmentMathError(env)

    load_dotenv(env_file_paths[env])
    print(f"ENV = {env}")
