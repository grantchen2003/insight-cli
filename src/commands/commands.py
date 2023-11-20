from pathlib import Path
from argparse import ArgumentParser

from src.core import dot_insight_dir, repository


def add_initialize_command(parser: ArgumentParser) -> None:
    parser.add_argument(
        "-i",
        "--initialize",
        action="store_true",
        help="initializes the current directory as an insight repository",
    )


def add_query_command(parser: ArgumentParser) -> None:
    parser.add_argument(
        "-q",
        "--query",
        type=str,
        help="shows files in the current insight repository that satisfy the given natural language query",
    )


def add_uninitialize_command(parser: ArgumentParser) -> None:
    parser.add_argument(
        "-u",
        "--uninitialize",
        action="store_true",
        help="uninitializes the current directory as an insight repository",
    )


def add_version_command(parser: ArgumentParser) -> None:
    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        help="shows the current version of insight",
    )


def initialize() -> None:
    repository_dir_path = Path.cwd()

    dot_insight_dir_path: Path = repository_dir_path / dot_insight_dir.get_dir_name()

    if dot_insight_dir.is_valid(dot_insight_dir_path):
        print(
            "The current directory is already an insight repository. This insight repository will be reinitialized."
        )

        repository.reinitialize(repository_dir_path)

        print("The current insight repository has been reinitialized.")

        return

    repository.initialize(repository_dir_path)

    print("The current directory has been initialized as an insight repository.")


def uninitialize() -> None:
    repository_dir_path = Path.cwd()

    dot_insight_dir_path: Path = repository_dir_path / dot_insight_dir.get_dir_name()

    if not dot_insight_dir.is_valid(dot_insight_dir_path):
        print("The current directory is not an insight repository.")
        return

    repository.uninitialize(repository_dir_path)

    print("The current insight repository has been uninitialized.")


def query(query_string: str) -> None:
    print(f"query_string: {query_string}")


def version() -> None:
    print("insight 0.0.0")
