from abc import abstractmethod


class BiDirectionalMessage:

    @property
    @abstractmethod
    def data(self) -> dict:
        pass
