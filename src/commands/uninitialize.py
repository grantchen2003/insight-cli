from pathlib import Path
from argparse import ArgumentParser

from src.core import dot_insight_dir, repository


def add_uninitialize_command(parser: ArgumentParser) -> None:
    parser.add_argument(
        "-u",
        "--uninitialize",
        action="store_true",
        help="uninitializes the current directory as an insight repository",
    )


def handle_uninitialize_command() -> None:
    repository_dir_path = Path.cwd()

    dot_insight_dir_path: Path = repository_dir_path / dot_insight_dir.get_dir_name()

    if not dot_insight_dir.is_valid(dot_insight_dir_path):
        print("The current directory is not an insight repository.")
        return

    repository.uninitialize(repository_dir_path)

    print("The current insight repository has been uninitialized.")
