from graphql_ws.protocols.messages import ServerToClientMessage


class ConnectionAckGraphQLWSMessage(ServerToClientMessage):
    """
    Direction: Server -> Client
    Expected response to the ConnectionInit message from the client acknowledging a
    successful connection with the server. The server can use the optional payload field to transfer additional
    details about the connection.
    """

    type: str = "connection_ack"

    def __init__(self, payload: dict | None = None):
        self.payload: dict = payload

    @property
    def data(self) -> dict:
        return {"type": self.type, "payload": self.payload}
