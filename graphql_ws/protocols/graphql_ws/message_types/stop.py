from graphql_ws.protocols.messages import ClientToServerMessage


class StopGraphQLWSMessage(ClientToServerMessage):
    """
    Direction: Client -> Server

    Client sends this message to terminate the connection."""

    type: str = "stop"

    def __init__(self, id_: str):
        super().__init__(id_=id_, type=self.type, payload=None)
        self.id_ = id_
