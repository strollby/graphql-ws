import json

from starlette.websockets import WebSocketDisconnect, WebSocketState

from fastapi import WebSocket

from graphql_ws.contexts import AsyncConnectionContext
from graphql_ws.contexts.exceptions import ConnectionClosedException
from graphql_ws.protocols import ProtocolEnum


class FastAPIConnectionContext(AsyncConnectionContext):

    def __init__(
        self,
        websocket: WebSocket,
        request_context=None,
        protocol: ProtocolEnum = ProtocolEnum.GRAPHQL_WS,
    ):
        self.websocket = websocket
        self.protocol = protocol
        super().__init__(websocket, request_context=request_context, protocol=protocol)

    async def receive(self):
        if self.closed:
            raise ConnectionClosedException()
        try:
            message = await self.websocket.receive_text()
            return message
        except (WebSocketDisconnect, RuntimeError):
            raise ConnectionClosedException()

    async def send(self, data):
        if self.closed:
            return
        try:
            await self.websocket.send_text(json.dumps(data))
        except (WebSocketDisconnect, RuntimeError):
            raise ConnectionClosedException()

    @property
    def closed(self):
        return self.websocket.client_state == WebSocketState.DISCONNECTED

    async def close(self, code):
        await self.websocket.close(code)

    async def open(self):
        # for protocol in self.protocols:
        await self.websocket.accept(self.protocol.value)
