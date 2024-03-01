from graphql_ws.protocols.messages import BiDirectionalMessage


class CompleteGraphQLTransportWSMessage(BiDirectionalMessage):
    """
    Direction: bidirectional

    Server -> Client indicates that the requested operation execution has completed. If the server dispatched the Error
    message relative to the original Subscribe message, no Complete message will be emitted.

    Client -> Server indicates that the client has stopped listening and wants to complete the subscription. No further
    events, relevant to the original subscription, should be sent through. Even if the client sent a Complete message for
    a single-result-operation before it resolved, the result should not be sent through once it does.

    Note: The asynchronous nature of the full-duplex connection means that a client can send a Complete message to the
    server even when messages are in-flight to the client, or when the server has itself completed the operation (via a
    Error or Complete message). Both client and server must therefore be prepared to receive (and ignore) messages for
    operations that they consider already completed.

    """

    type: str = "complete"

    @property
    def data(self) -> dict:
        return {
            "id": self.id,
            "type": self.type
        }

    def __init__(self, id_: str):
        self.id = id_
