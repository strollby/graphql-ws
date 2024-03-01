from graphql_ws.protocols.messages import BiDirectionalMessage


class PongGraphQLTransportWSMessage(BiDirectionalMessage):
    """
    Direction: bidirectional

    The response to the Ping message. Must be sent as soon as the Ping message is received.

    The Pong message can be sent at any time within the established socket. Furthermore, the Pong message may even be sent unsolicited as an unidirectional heartbeat.

    The optional payload field can be used to transfer additional details about the pong.
    """

    type: str = "pong"

    @property
    def data(self) -> dict:
        return {"type": self.type}

    def __init__(self):
        pass
