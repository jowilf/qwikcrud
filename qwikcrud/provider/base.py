from abc import abstractmethod

from qwikcrud.schemas import App


class AIProvider:
    def __init__(self) -> None:
        pass

    @abstractmethod
    def get_name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def query(self, prompt: str) -> App:
        raise NotImplementedError
