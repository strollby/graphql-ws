from graphql_ws.protocols.messages import ClientToServerMessage


class SubscribeGraphQLTransportWSMessage(ClientToServerMessage):
    """
    Direction: Client -> Server

    Requests an operation specified in the message payload. This message provides a unique ID field to connect
    published messages to the operation requested by this message.

    If there is already an active subscriber for an operation matching the provided ID, regardless of the operation
    type, the server must close the socket immediately with the event 4409: Subscriber for <unique-operation-id>
    already exists.

    The server needs only keep track of IDs for as long as the subscription is active. Once a client completes an
    operation, it is free to re-use that ID.

    Executing operations is allowed only after the server has acknowledged the connection through the ConnectionAck
    message, if the connection is not acknowledged, the socket will be closed immediately with the event 4401:
    Unauthorized.

    """

    type: str = "subscribe"

    def __init__(self, id_: str, payload: dict):
        super().__init__(self.type, payload, id_)
        self.id = id_
        self.payload: dict = payload
