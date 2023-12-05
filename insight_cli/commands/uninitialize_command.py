from pathlib import Path

from insight_cli.repository import Repository
from insight_cli.utils import Color
from .base.command import Command


class UninitializeCommand(Command):
    def __init__(self):
        super().__init__(
            flags=["-u", "--uninitialize"],
            description="uninitializes the current directory as an insight repository",
        )

    def execute(self) -> None:
        repository = Repository(Path.cwd())

        if not repository.is_valid:
            print(Color.red("The current directory is not an insight repository."))
            return

        repository.uninitialize()
        print(Color.green("The current insight repository has been uninitialized."))

