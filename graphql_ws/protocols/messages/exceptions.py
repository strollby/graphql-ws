class ClientToServerMessageInvalid(Exception):
    pass


class ServerToClientMessageInvalid(Exception):
    pass


class BiDirectionalMessageInvalid(Exception):
    pass


class ClientToServerOrBiDirectionalRequired(Exception):
    pass
