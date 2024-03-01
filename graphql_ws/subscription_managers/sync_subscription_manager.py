import abc
from abc import abstractmethod

from graphql import FormattedExecutionResult

from graphql_ws.contexts import SyncConnectionContext
from graphql_ws.subscription_managers import BaseSubscriptionManager
from graphql_ws.subscription_managers.exceptions import (
    SubscriberAlreadyExistException,
    TopicNotFoundException,
)


class SyncSubscriptionManager(BaseSubscriptionManager):

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
        self.subscribers: list[str] = subscribers
        self.connection_contexts: list[dict] = connection_contexts
        super().__init__(self.topics, self.subscribers, self.connection_contexts)

    @abstractmethod
    def subscribe(
        self, id_: str, topic: str, connection_context: SyncConnectionContext
    ):
        if topic not in self.topics:
            raise TopicNotFoundException()
        if id_ in self.subcribers:
            raise SubscriberAlreadyExistException()
        self.subcribers.append(id_)
        connection_context_ = next(
            context for context in self.connection_contexts if context["topic"] == topic
        )
        connection_context_["subcribers"].append(
            {"id": id_, "connection_context": connection_context}
        )

    @abstractmethod
    def create_topic(self, name: str):
        if name not in self.topics:
            self.topics.append(name)
        return name

    @abstractmethod
    def publish(self, topic: str, payload: FormattedExecutionResult):
        topic = self.create_topic(topic)
        connection_context = next(
            context for context in self.connection_contexts if context["topic"] == topic
        )
        for subcriber in connection_context.get("subcribers"):
            subcriber.get("connection_context")

    @abstractmethod
    def unsubscribe(self, id_: str):
        self.subcribers.pop(id_)
