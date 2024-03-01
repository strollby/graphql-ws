from graphql import ExecutionResult

from graphql_ws.protocols.messages import ServerToClientMessage


class NextGraphQLTransportWSMessage(ServerToClientMessage):
    """
    Direction: Server -> Client

    Operation execution result(s) from the source stream created by the binding Subscribe message. After all results have
    been emitted, the Complete message will follow indicating stream completion.
    """

    type: str = "next"

    def __init__(self, id_: str, payload: ExecutionResult | None = None):
        self.id = id_
        self.type: str = "next"
        self.payload: ExecutionResult = payload

    @property
    def data(self) -> dict:
        return {"id": self.id, "type": self.type, "payload": self.payload}
