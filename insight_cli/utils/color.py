class Color:
    _RED = "\033[91m"
    _GREEN = "\033[92m"
    _YELLOW = "\033[93m"
    _END = "\033[0m"

    @classmethod
    def red(cls, text: str) -> str:
        return f"{cls._RED}{text}{cls._END}"

    @classmethod
    def green(cls, text: str) -> str:
        return f"{cls._GREEN}{text}{cls._END}"

    @classmethod
    def yellow(cls, text: str) -> str:
        return f"{cls._YELLOW}{text}{cls._END}"
