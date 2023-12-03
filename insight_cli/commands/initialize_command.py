from pathlib import Path

from insight_cli.repository import Repository
from insight_cli.utils import Color
from .base.command import Command


class InitializeCommand(Command):
    def __init__(self):
        super().__init__(
            flags=["-i", "--initialize"],
            description="initializes the current directory as an insight repository",
        )

    def execute(self):
        repository = Repository(Path.cwd())

        if repository.is_valid:
            print(
                Color.yellow(
                    "The current directory is already an insight repository. This insight repository will be reinitialized."
                )
            )

            repository.reinitialize()

            print(Color.green("The current insight repository has been reinitialized."))

            return

        repository.initialize()

        print(
            Color.green(
                "The current directory has been initialized as an insight repository."
            )
        )
