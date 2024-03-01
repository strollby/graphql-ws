from graphql_ws.contexts.exceptions import ConnectionClosedException
from graphql_ws.integrations.fastapi.context import FastAPIConnectionContext
from graphql_ws.protocols.messages import MessageParser, ClientToServerMessage
from fastapi import WebSocket

from graphql_ws.servers import AsyncSubscriptionServer
from graphql_ws.subscription_managers import AsyncSubscriptionManager
from graphql_ws.protocols.protocol import ProtocolEnum


class FastAPISubscriptionServer(AsyncSubscriptionServer):

    def __init__(
        self, schema, subscription_manager: AsyncSubscriptionManager | None = None
    ):
        super().__init__(schema, subscription_manager)

    @staticmethod
    async def on_open(connection_context):
        await connection_context.open()

    async def handle(
        self,
        websocket: WebSocket,
        request_context=None,
        protocol: ProtocolEnum = ProtocolEnum.GRAPHQL_WS,
    ):

        connection_context = FastAPIConnectionContext(
            websocket=websocket, request_context=request_context, protocol=protocol
        )
        request_context.connection_context = connection_context
        if protocol != ProtocolEnum(websocket.headers.get("sec-websocket-protocol")):
            await connection_context.close(1000)
            return
        await self.on_open(connection_context)
        try:
            while not connection_context.closed:
                message: ClientToServerMessage = MessageParser(
                    protocol=protocol
                ).parse_client_message(await connection_context.receive())
                await self.on_message(
                    protocol=protocol,
                    connection_context=connection_context,
                    message=message,
                )
        except ConnectionClosedException:
            pass
        else:
            await connection_context.close(1000)
