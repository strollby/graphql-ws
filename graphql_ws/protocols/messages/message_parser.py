import json

from graphql_ws.protocols.exceptions import UnSupportedProtocolException
from graphql_ws.protocols.graphql_transport_ws.message_types import ConnectionInitGraphQLTransportWSMessage, \
    SubscribeGraphQLTransportWSMessage, PingGraphQLTransportWSMessage, PongGraphQLTransportWSMessage, \
    CompleteGraphQLTransportWSMessage
from graphql_ws.protocols.graphql_ws.message_types import (
    ConnectionInitGraphQLWSMessage,
    StartGraphQLWSMessage,
    ConnectionTerminateGraphQLWSMessage,
)
from graphql_ws.protocols.messages import ClientToServerMessage, BiDirectionalMessage
from graphql_ws.protocols.messages.exceptions import ClientToServerMessageInvalid
from graphql_ws.protocols.protocol import ProtocolEnum


class MessageParser(object):
    def __init__(self, protocol: ProtocolEnum):
        self.protocol = protocol

    def parse_client_message(self, message: str) -> ClientToServerMessage | BiDirectionalMessage:
        message = json.loads(message)
        if self.protocol == ProtocolEnum.GRAPHQL_WS:
            match message.get("type"):
                case ConnectionInitGraphQLWSMessage.type:
                    return ConnectionInitGraphQLWSMessage(
                        payload=message.get("payload")
                    )
                case StartGraphQLWSMessage.type:
                    return StartGraphQLWSMessage(
                        id_=message.get("id"), payload=message.get("payload")
                    )
                case ConnectionTerminateGraphQLWSMessage.type:
                    return ConnectionTerminateGraphQLWSMessage()
                case _:
                    raise ClientToServerMessageInvalid()
        elif self.protocol == ProtocolEnum.GRAPHQL_TRANSPORT_WS:
            match message.get("type"):
                case ConnectionInitGraphQLTransportWSMessage.type:
                    return ConnectionInitGraphQLTransportWSMessage(
                        payload=message.get("payload")
                    )
                case SubscribeGraphQLTransportWSMessage.type:
                    return SubscribeGraphQLTransportWSMessage(
                        id_=message.get("id"), payload=message.get("payload")
                    )
                case PingGraphQLTransportWSMessage.type:
                    return PingGraphQLTransportWSMessage()
                case PongGraphQLTransportWSMessage.type:
                    return PongGraphQLTransportWSMessage()
                case CompleteGraphQLTransportWSMessage.type:
                    return CompleteGraphQLTransportWSMessage(id_=message.get("id"))
                case _:
                    raise ClientToServerMessageInvalid()
        else:
            raise UnSupportedProtocolException()
