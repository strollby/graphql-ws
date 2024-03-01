from graphql import FormattedExecutionResult

from graphql_ws.protocols.messages import ServerToClientMessage


class DataGraphQLWSMessage(ServerToClientMessage):
    """
    Direction: Server -> Client
    Expected response to the ConnectionInit message from the client acknowledging a
    successful connection with the server. The server can use the optional payload field to transfer additional
    details about the connection.
    """

    type: str = "data"

    def __init__(self, id_: str, payload: FormattedExecutionResult):
        self.id = id_
        self.payload: dict = payload

    @property
    def data(self) -> dict:
        return {"id": self.id, "type": self.type, "payload": self.payload}
