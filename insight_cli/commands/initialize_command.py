from pathlib import Path

from insight_cli.commands.base.command import Command
from insight_cli.core import dot_insight_dir, repository
from insight_cli.utils.color import Color


class InitializeCommand(Command):
    def __init__(self):
        super().__init__(
            flags=["-i", "--initialize"],
            description="initializes the current directory as an insight repository",
        )

    def execute(self):
        repository_dir_path = Path.cwd()

        dot_insight_dir_path: Path = (
            repository_dir_path / dot_insight_dir.get_dir_name()
        )

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
