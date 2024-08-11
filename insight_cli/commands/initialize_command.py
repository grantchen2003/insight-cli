from pathlib import Path

from .base.command import Command
from insight_cli.repository import (
    Repository,
    FileSizeExceededError,
    InvalidRepositoryError,
)
from insight_cli.utils import Color


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
                terminal_output = f"Reinitialized existing insight repository in {repository.path.resolve()}"

            else:
                repository.initialize()
                terminal_output = (
                    f"Initialized insight repository in {repository.path.resolve()}"
                )

            print(Color.green(terminal_output))

        except FileSizeExceededError as e:
            print(Color.red(e))

        except InvalidRepositoryError as e:
            print(Color.red(e))
