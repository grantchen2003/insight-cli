from pathlib import Path

from insight_cli.commands.classes import Command
from insight_cli.core import dot_insight_dir, repository
from insight_cli.utils.color import Color


def create_uninitialize_command() -> Command:
    return Command(
        flags=["-u", "--uninitialize"],
        description="uninitializes the current directory as an insight repository",
        handler={
            "params": [],
            "function": handle_uninitialize_command,
        },
    )


def handle_uninitialize_command() -> None:
    repository_dir_path = Path.cwd()

    dot_insight_dir_path: Path = repository_dir_path / dot_insight_dir.get_dir_name()

    if not dot_insight_dir.is_valid(dot_insight_dir_path):
        print(Color.red("The current directory is not an insight repository."))
        return

    repository.uninitialize(repository_dir_path)

    print(Color.green("The current insight repository has been uninitialized."))
