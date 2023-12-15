from pathlib import Path

from insight_cli.repository import Repository, InvalidRepositoryError
from insight_cli.utils import Color
from .base.command import Command


class InitializeCommand(Command):
    def __init__(self):
        super().__init__(
            flags=["-i", "--initialize"],
            description="initializes the current directory as an insight repository",
        )

    def execute(self):
        try:
            repository = Repository(Path(""))

            if repository.is_valid:
                repository.reinitialize()
                print(
                    Color.green(
                        f"Reinitialized existing insight repository in {repository.path.resolve()}"
                    )
                )

            else:
                repository.initialize()
                print(
                    Color.green(
                        f"Initialized insight repository in {repository.path.resolve()}"
                    )
                )

        except InvalidRepositoryError as e:
            print(Color.red(e))
