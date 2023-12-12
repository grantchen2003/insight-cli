from pathlib import Path

from insight_cli.repository import Repository, InvalidRepositoryError
from insight_cli.utils import Color
from .base.command import Command


class UninitializeCommand(Command):
    def __init__(self):
        super().__init__(
            flags=["-u", "--uninitialize"],
            description="uninitializes the current directory as an insight repository",
        )

    def execute(self) -> None:
        try:
            repository = Repository(Path(""))
            repository.uninitialize()
            print(
                Color.green(
                    f"Uninitialized insight repository in {repository.path.resolve()}"
                )
            )

        except InvalidRepositoryError as e:
            print(Color.red(e))
