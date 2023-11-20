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


def handle_initialize_command() -> None:
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
