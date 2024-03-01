from graphql_ws.protocols.messages import ClientToServerMessage


class ConnectionInitGraphQLTransportWSMessage(ClientToServerMessage):
    """
    Direction: Client -> Server

    Indicates that the client wants to establish a connection within the existing socket. This connection is not the
    actual WebSocket communication channel, but is rather a frame within it asking the server to allow future
    operation requests.

    The server must receive the connection initialisation message within the allowed waiting time specified in the
    connectionInitWaitTimeout parameter during the server setup. If the client does not request a connection within
    the allowed timeout, the server will close the socket with the event: 4408: Connection initialisation timeout.

    If the server receives more than one ConnectionInit message at any given time, the server will close the socket
    with the event 4429: Too many initialisation requests.

    If the server wishes to reject the connection, for example during authentication, it is recommended to close the
    socket with 4403: Forbidden."""

    type: str = "connection_init"

    def __init__(self, payload: dict | None = None):
        super().__init__(self.type, payload)
        self.payload: dict = payload
