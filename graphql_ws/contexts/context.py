from graphql_ws.protocols import ProtocolEnum


class BaseConnectionContext(object):

    def __init__(
        self,
        websocket,
        request_context=None,
        protocol: ProtocolEnum = ProtocolEnum.GRAPHQL_WS,
    ):
        self.protocol = protocol
        self.websocket = websocket
        self.request_context = request_context
        self.id_: str | None = None

    @property
    def id(self):
        return self.id_

    @id.setter
    def id(self, value: str):
        if not isinstance(value, str):
            raise TypeError("ID must be a string")
        self.id_ = value

    def receive(self):
        raise NotImplementedError("receive method not implemented")

    def send(self, data):
        raise NotImplementedError("send method not implemented")

    @property
    def closed(self):
        raise NotImplementedError("closed property not implemented")

    def close(self, code):
        raise NotImplementedError("close method not implemented")
