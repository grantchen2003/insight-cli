import colorama, sys


class Color:
    _RED = colorama.Fore.RED
    _GREEN = colorama.Fore.GREEN
    _YELLOW = colorama.Fore.YELLOW
    _RESET = colorama.Style.RESET_ALL

    @classmethod
    def init(cls):
        is_run_in_terminal = sys.stdout.isatty()
        if is_run_in_terminal:
            colorama.init()

    @classmethod
    def _colorize(cls, color: str, text: str) -> str:
        Color.init()
        return f"{color}{text}{cls._RESET}"

    @classmethod
    def red(cls, text: str) -> str:
        return cls._colorize(cls._RED, text)

    @classmethod
    def green(cls, text: str) -> str:
        return cls._colorize(cls._GREEN, text)

    @classmethod
    def yellow(cls, text: str) -> str:
        return cls._colorize(cls._YELLOW, text)
