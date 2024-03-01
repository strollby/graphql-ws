class ClientToServerMessage:
    def __init__(self, type: str, payload: dict | None = None, id_: str | None = None):
        self.id = id_
        self.type = type
        self.payload = payload
