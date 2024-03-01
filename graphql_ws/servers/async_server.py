from graphql.pyutils import is_awaitable

from .server import BaseSubscriptionServer
from ..contexts import AsyncConnectionContext, BaseConnectionContext
from ..protocols import ProtocolEnum
from ..protocols.graphql_transport_ws.message_types import (
    SubscribeGraphQLTransportWSMessage, ConnectionInitGraphQLTransportWSMessage, ConnectionAckGraphQLTransportWSMessage,
    NextGraphQLTransportWSMessage, PingGraphQLTransportWSMessage, PongGraphQLTransportWSMessage,
    CompleteGraphQLTransportWSMessage,
)
from ..protocols.graphql_ws.message_types import (
    ConnectionInitGraphQLWSMessage,
    ConnectionAckGraphQLWSMessage,
    StartGraphQLWSMessage,
    DataGraphQLWSMessage,
    CompleteGraphQLWSMessage,
    ConnectionTerminateGraphQLWSMessage,
    StopGraphQLWSMessage,
)
from ..protocols.messages import (
    ClientToServerMessage,
    BiDirectionalMessage,
    ServerToClientMessage,
)
from ..protocols.messages.exceptions import ClientToServerOrBiDirectionalRequired
from ..subscription_managers import AsyncSubscriptionManager
from ..subscription_managers.exceptions import SubscriberAlreadyExistException


class AsyncSubscriptionServer(BaseSubscriptionServer):

    def __init__(self, schema, subscription_manager: AsyncSubscriptionManager):
        self.subscription_manager = subscription_manager
        super().__init__(schema, subscription_manager=subscription_manager)

    async def execute(self, params):
        try:
            return await self.schema.subscribe(
                query=params.get("request_string"),
                operation_name=params.get("operation_name"),
                variable_values=params.get("variable_values"),
                context_value=params.get("context_value"),
            )
        except Exception as error:
            a = 1

    async def on_message(
        self,
        protocol: ProtocolEnum,
        connection_context: AsyncConnectionContext,
        message: ClientToServerMessage | BiDirectionalMessage,
    ):
        try:
            if issubclass(type(message), ClientToServerMessage) or issubclass(
                type(message), BiDirectionalMessage
            ):
                await self.process_message(protocol, connection_context, message)
            else:
                raise ClientToServerOrBiDirectionalRequired()
        except ClientToServerOrBiDirectionalRequired:
            return self.send_error(connection_context, None, e)

    async def process_message(
        self,
        protocol: ProtocolEnum,
        connection_context: AsyncConnectionContext,
        message: ClientToServerMessage | BiDirectionalMessage,
    ):
        if protocol == protocol.GRAPHQL_WS:
            if isinstance(message, ConnectionInitGraphQLWSMessage):
                await self.on_connection_init(connection_context, message)
            elif isinstance(message, StartGraphQLWSMessage):
                connection_context.id = message.id
                await self.on_start(connection_context, message)
            elif isinstance(message, ConnectionTerminateGraphQLWSMessage):
                await self.on_terminate(connection_context, message)
            elif isinstance(message, StopGraphQLWSMessage):
                await self.subscription_manager.unsubscribe(
                    connection_context=connection_context
                )
                await self.on_terminate(connection_context, message)
        elif protocol == protocol.GRAPHQL_TRANSPORT_WS:
            if isinstance(message, ConnectionInitGraphQLTransportWSMessage):
                await self.on_connection_init(connection_context, message)
            elif isinstance(message, PingGraphQLTransportWSMessage):
                await self.send_message(connection_context, PongGraphQLTransportWSMessage())
            elif isinstance(message, PongGraphQLTransportWSMessage):
                await self.send_message(connection_context, PingGraphQLTransportWSMessage())
            elif isinstance(message, SubscribeGraphQLTransportWSMessage):
                connection_context.id = message.id
                await self.on_start(connection_context, message)
            elif isinstance(message, CompleteGraphQLTransportWSMessage):
                await self.subscription_manager.unsubscribe(
                    connection_context=connection_context
                )
        else:
            pass

    async def on_start(
        self,
        connection_context: AsyncConnectionContext,
        message: StartGraphQLWSMessage | SubscribeGraphQLTransportWSMessage,
    ):
        params = self.get_graphql_params(connection_context, message.payload)
        execution_result = await self.schema.subscribe(
            query=params.get("request_string"),
            operation_name=params.get("operation_name"),
            variable_values=params.get("variable_values"),
            context_value=params.get("context_value"),
        )
        try:
            if hasattr(execution_result, "__aiter__"):
                iterator = execution_result.__aiter__()
                async for result in iterator:
                    if isinstance(message, StartGraphQLWSMessage):
                        await self.send_message(
                            connection_context,
                            message=DataGraphQLWSMessage(
                                id_=message.id, payload=result.formatted
                            ),
                        )
                    elif isinstance(message, SubscribeGraphQLTransportWSMessage):
                        await self.send_message(
                            connection_context,
                            message=NextGraphQLTransportWSMessage(
                                id_=message.id, payload=result.formatted
                            ),
                        )
            else:
                if is_awaitable(execution_result):
                    execution_result = await execution_result
                if isinstance(message, StartGraphQLWSMessage):
                    await self.send_message(
                        connection_context,
                        message=DataGraphQLWSMessage(
                            id_=message.id, payload=execution_result.formatted
                        ),
                    )
                elif isinstance(message, SubscribeGraphQLTransportWSMessage):
                    await self.send_message(
                        connection_context,
                        message=NextGraphQLTransportWSMessage(
                            id_=message.id, payload=execution_result.formatted
                        ),
                    )
        except SubscriberAlreadyExistException as error:
            pass
            # await self.send_error(connection_context, error)
        else:
            if isinstance(message, StartGraphQLWSMessage):
                await self.on_complete(
                    connection_context=connection_context,
                    message=CompleteGraphQLWSMessage(id_=message.id),
                )
            elif isinstance(message, SubscribeGraphQLTransportWSMessage):
                await self.on_complete(
                    connection_context=connection_context,
                    message=CompleteGraphQLTransportWSMessage(id_=message.id),
                )

    async def on_complete(
        self,
        connection_context: AsyncConnectionContext,
        message: CompleteGraphQLWSMessage | CompleteGraphQLTransportWSMessage,
    ):
        await self.send_message(connection_context, message=message)
        await self.subscription_manager.unsubscribe(
            connection_context=connection_context
        )
        await connection_context.close(1000)

    async def on_terminate(
        self,
        connection_context: AsyncConnectionContext,
        message: ConnectionTerminateGraphQLWSMessage | StopGraphQLWSMessage,
    ):
        await self.subscription_manager.unsubscribe(
            connection_context=connection_context
        )
        await connection_context.close(1000)

    async def on_stop(
        self, connection_context: AsyncConnectionContext, message: StopGraphQLWSMessage
    ):
        await self.subscription_manager.unsubscribe(
            connection_context=connection_context
        )
        await connection_context.close(1000)

    async def on_connect(
        self, connection_context, message: ConnectionInitGraphQLWSMessage
    ):
        pass

    async def send_error(
        self,
        connection_context: AsyncConnectionContext,
        exception: SubscriberAlreadyExistException,
    ):
        if not connection_context.closed:
            await connection_context.close(exception.code)

    async def on_connection_init(
        self,
        connection_context: AsyncConnectionContext,
        message: ConnectionInitGraphQLWSMessage | ConnectionInitGraphQLTransportWSMessage,
    ):
        await self.on_connect(connection_context, message)
        if isinstance(message, ConnectionInitGraphQLWSMessage):
            await self.send_message(
                connection_context,
                message=ConnectionAckGraphQLWSMessage(payload=message.payload),
            )
        elif isinstance(message, ConnectionInitGraphQLTransportWSMessage):
            await self.send_message(
                connection_context,
                message=ConnectionAckGraphQLTransportWSMessage(payload=message.payload))

    async def send_message(
        self,
        connection_context: AsyncConnectionContext,
        message: ServerToClientMessage | BiDirectionalMessage,
    ):
        await connection_context.send(data=message.data)
