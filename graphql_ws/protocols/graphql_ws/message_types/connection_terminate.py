from graphql_ws.protocols.messages import ClientToServerMessage


class ConnectionTerminateGraphQLWSMessage(ClientToServerMessage):
    """
    Direction: Client -> Server

    Client sends this message to terminate the connection."""

    type: str = "connection_terminate"

    def __init__(self):
        super().__init__(id_=None, type=self.type, payload=None)
