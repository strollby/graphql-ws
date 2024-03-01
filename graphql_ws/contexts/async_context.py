from abc import abstractmethod
from typing import Any

from .context import BaseConnectionContext
from ..protocols import ProtocolEnum


# noinspection DuplicatedCode
class AsyncConnectionContext(BaseConnectionContext):

    def __init__(
        self,
        websocket: Any,
        request_context=None,
        protocol: ProtocolEnum = ProtocolEnum.GRAPHQL_WS,
    ):
        self.websocket = websocket
        super().__init__(websocket, request_context=request_context, protocol=protocol)

    @abstractmethod
    async def receive(self):
        raise NotImplementedError("receive method not implemented")

    @abstractmethod
    async def send(self, data: dict):
        raise NotImplementedError("receive method not implemented")

    @property
    @abstractmethod
    def closed(self):
        raise NotImplementedError("receive method not implemented")

    @abstractmethod
    async def close(self, code):
        raise NotImplementedError("receive method not implemented")
