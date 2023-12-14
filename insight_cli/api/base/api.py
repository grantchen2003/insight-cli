from abc import ABC, abstractmethod
from typing import Any


class API(ABC):
    @abstractmethod
    def make_request(self, *args, **kwargs) -> Any:
        pass
