from graphql_ws.protocols.messages import BiDirectionalMessage


class PingGraphQLTransportWSMessage(BiDirectionalMessage):
    """
    Direction: bidirectional

    Useful for detecting failed connections, displaying latency metrics or other types of network probing.

    A Pong must be sent in response from the receiving party as soon as possible.

    The Ping message can be sent at any time within the established socket.

    The optional payload field can be used to transfer additional details about the ping.
    """

    type: str = "ping"

    @property
    def data(self) -> dict:
        return {"type": self.type}

    def __init__(self):
        pass
