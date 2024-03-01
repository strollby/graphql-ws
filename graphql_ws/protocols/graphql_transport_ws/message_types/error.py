from graphql import GraphQLError

from graphql_ws.protocols.messages import ServerToClientMessage


class ErrorGraphQLTransportWSMessage(ServerToClientMessage):
    """
    Direction: Server -> Client

    Operation execution error(s) in response to the Subscribe message. This can occur before execution starts,
    usually due to validation errors, or during the execution of the request. This message terminates the operation and
    no further messages will be sent.
    """

    def __init__(self, id_: str, payload: list[GraphQLError]):
        self.id = id_
        self.type: str = "error"
        self.payload: list[GraphQLError] = payload
