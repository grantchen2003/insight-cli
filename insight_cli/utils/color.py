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
    def red(cls, text: str) -> str:
        Color.init()
        return f"{cls._RED}{text}{cls._RESET}"

    @classmethod
    def green(cls, text: str) -> str:
        Color.init()
        return f"{cls._GREEN}{text}{cls._RESET}"

    @classmethod
    def yellow(cls, text: str) -> str:
        Color.init()
        return f"{cls._YELLOW}{text}{cls._RESET}"
