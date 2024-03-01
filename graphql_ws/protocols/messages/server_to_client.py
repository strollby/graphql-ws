import abc
from abc import abstractmethod


class ServerToClientMessage(abc.ABC):

    @property
    @abstractmethod
    def data(self) -> dict:
        pass
