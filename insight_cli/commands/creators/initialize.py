from pathlib import Path

from insight_cli.commands.classes import Command
from insight_cli.core import dot_insight_dir, repository
from insight_cli.utils.color import Color


def create_initialize_command() -> Command:
    return Command(
        flags=["-i", "--initialize"],
        description="initializes the current directory as an insight repository",
        handler={
            "params": [],
            "function": handle_initialize_command,
        },
    )


def handle_initialize_command() -> None:
    repository_dir_path = Path.cwd()

    dot_insight_dir_path: Path = repository_dir_path / dot_insight_dir.get_dir_name()

    if dot_insight_dir.is_valid(dot_insight_dir_path):
        print(
            Color.yellow(
                "The current directory is already an insight repository. This insight repository will be reinitialized."
            )
        )

        repository.reinitialize(repository_dir_path)

        print(Color.green("The current insight repository has been reinitialized."))

        return

    repository.initialize(repository_dir_path)

    print(
        Color.green(
            "The current directory has been initialized as an insight repository."
        )
    )
