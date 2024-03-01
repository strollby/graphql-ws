class SubscriberAlreadyExistException(Exception):
    def __init__(self, unique_operation_id: str):
        self.code = 4409
        self.message = f"Subscriber for {unique_operation_id} already exists"


class TopicNotFoundException(Exception):
    pass
