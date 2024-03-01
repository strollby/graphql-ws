import abc
from abc import abstractmethod

from graphql_ws.contexts import BaseConnectionContext
from graphql_ws.protocols import ProtocolEnum
from graphql_ws.protocols.graphql_transport_ws.message_types import (
    SubscribeGraphQLTransportWSMessage,
)
from graphql_ws.protocols.graphql_ws.message_types import (
    StartGraphQLWSMessage,
    CompleteGraphQLWSMessage,
    ConnectionInitGraphQLWSMessage,
    ConnectionTerminateGraphQLWSMessage,
    StopGraphQLWSMessage,
)
from graphql_ws.protocols.messages import (
    ClientToServerMessage,
    BiDirectionalMessage,
    ServerToClientMessage,
)
from graphql_ws.subscription_managers import BaseSubscriptionManager


class BaseSubscriptionServer(abc.ABC):
    def __init__(
        self,
        schema,
        subscription_manager: BaseSubscriptionManager | None = None,
        keep_alive=True,
    ):
        self.schema = schema
        self.keep_alive = keep_alive
        self.subscription_manager = subscription_manager

    @abstractmethod
    def send_error(
        self, connection_context: BaseConnectionContext, exception: Exception
    ):
        pass

    @abstractmethod
    def on_message(
        self,
        protocol: ProtocolEnum,
        connection_context: BaseConnectionContext,
        message: ClientToServerMessage | BiDirectionalMessage,
    ):
        pass

    @staticmethod
    def get_graphql_params(
        connection_context: BaseConnectionContext, payload: dict
    ) -> dict:
        context = payload.get("context", connection_context.request_context)
        return {
            "request_string": payload.get("query"),
            "variable_values": payload.get("variables"),
            "operation_name": payload.get("operationName"),
            "context_value": context,
        }

    @abstractmethod
    def process_message(
        self,
        protocol: ProtocolEnum,
        connection_context: BaseConnectionContext,
        message: ClientToServerMessage | BiDirectionalMessage,
    ):
        pass

    @abstractmethod
    def on_connect(self, connection_context, payload):
        pass

    @abstractmethod
    def on_complete(
        self,
        connection_context: BaseConnectionContext,
        message: CompleteGraphQLWSMessage,
    ):
        pass

    @abstractmethod
    def on_terminate(
        self,
        connection_context: BaseConnectionContext,
        message: ConnectionTerminateGraphQLWSMessage | StopGraphQLWSMessage,
    ):
        pass

    @abstractmethod
    def on_stop(
        self, connection_context: BaseConnectionContext, message: StopGraphQLWSMessage
    ):
        pass

    @abstractmethod
    def on_connection_init(
        self,
        connection_context: BaseConnectionContext,
        message: ConnectionInitGraphQLWSMessage,
    ):
        pass

    @abstractmethod
    def send_message(
        self,
        connection_context: BaseConnectionContext,
        message: ServerToClientMessage | BiDirectionalMessage,
    ):
        pass

    @abstractmethod
    def on_start(
        self,
        connection_context: BaseConnectionContext,
        message: StartGraphQLWSMessage | SubscribeGraphQLTransportWSMessage,
    ):
        pass
