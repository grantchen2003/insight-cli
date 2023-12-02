from abc import ABC, abstractmethod


class CLIArgumentValidatorInterface(ABC):
    @staticmethod
    @abstractmethod
    def raise_for_invalid_args(self, *args, **kwargs) -> None:
        pass
