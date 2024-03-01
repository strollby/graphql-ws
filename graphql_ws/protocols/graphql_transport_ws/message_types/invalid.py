from graphql_ws.protocols.messages import BiDirectionalMessage


class InvalidGraphQLTransportWSMessage(BiDirectionalMessage):
    """
    Direction: bidirectional

    Receiving a message of a type or format which is not specified in this document will result in an immediate socket
    closure with the event 4400: <error-message>. The <error-message> can be vaguely descriptive on why the received
    message is invalid.

    Receiving a message (other than Subscribe) with an ID that belongs to an operation that has been previously completed
    does not constitute an error. It is permissable to simply ignore all unknown IDs without closing the connection.
    """

    def __init__(
        self,
    ):
        pass
