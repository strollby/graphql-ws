import abc

from graphql import FormattedExecutionResult

from graphql_ws.contexts import BaseConnectionContext


class BaseSubscriptionManager(abc.ABC):

    def __init__(
        self,
        topics: list[str] | None = None,
        subscribers: list[str] | None = None,
        connection_contexts: list[dict] | None = None,
    ):
        if topics is None:
            topics = []
        if subscribers is None:
            subscribers = []
        if connection_contexts is None:
            connection_contexts = []
        self.topics: list[str] = topics
        self.subcribers: list[str] = subscribers
        self.connection_contexts: list[dict] = connection_contexts

    @abc.abstractmethod
    def subscribe(self, topic: str, connection_context: BaseConnectionContext):
        pass

    @abc.abstractmethod
    def create_topic(self, name: str):
        pass

    @abc.abstractmethod
    def publish(self, topic: str, payload: FormattedExecutionResult):
        pass

    @abc.abstractmethod
    def unsubscribe(self, connection_context: BaseConnectionContext):
        pass
