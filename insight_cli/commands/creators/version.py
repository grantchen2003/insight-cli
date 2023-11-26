from insight_cli.commands.classes import Command
from insight_cli.utils.color import Color
import insight_cli


def create_version_command() -> Command:
    return Command(
        flags=["-v", "--version"],
        description="shows the current version of insight",
        handler={
            "params": [],
            "function": handle_version_command,
        },
    )


def handle_version_command() -> None:
    print(Color.green(f"insight-cli v{insight_cli.__version__}"))
