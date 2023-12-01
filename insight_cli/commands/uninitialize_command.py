from pathlib import Path

from insight_cli.commands.base.command import Command
from insight_cli.core import dot_insight_dir, repository
from insight_cli.utils.color import Color


class UninitializeCommand(Command):
    def __init__(self):
        super().__init__(
            flags=["-u", "--uninitialize"],
            description="uninitializes the current directory as an insight repository",
        )

    def execute(self) -> None:
        repository_dir_path = Path.cwd()

        dot_insight_dir_path: Path = repository_dir_path / dot_insight_dir.get_dir_name()

        if not dot_insight_dir.is_valid(dot_insight_dir_path):
            print(Color.red("The current directory is not an insight repository."))
            return

        repository.uninitialize(repository_dir_path)

        print(Color.green("The current insight repository has been uninitialized."))

