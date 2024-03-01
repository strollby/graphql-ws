from graphql_ws.protocols.messages import ServerToClientMessage


class CompleteGraphQLWSMessage(ServerToClientMessage):
    """
    Direction: Server -> Client Server sends this message to indicate that a GraphQL operation is done, and no more
    data will arrive for the specific operation.
    """

    type: str = "complete"

    def __init__(self, id_: str):
        self.id: str = id_

    @property
    def data(self) -> dict:
        return {"type": self.type, "id": self.id}
