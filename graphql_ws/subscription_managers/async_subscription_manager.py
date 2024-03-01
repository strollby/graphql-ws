import asyncio

from . import BaseSubscriptionManager
from .exceptions import SubscriberAlreadyExistException
from ..contexts import AsyncConnectionContext


class AsyncSubscriptionManager(BaseSubscriptionManager):

    def __init__(self):
        self.topics: list[str] = []
        self.subscribers: list[str] = []
        self.connection_contexts: list[dict] = []
        super().__init__(self.topics, self.subscribers, self.connection_contexts)

    async def subscribe(self, topic: str, connection_context: AsyncConnectionContext):
        queue = asyncio.Queue()
        if topic not in self.topics:
            self.topics.append(topic)
        # if connection_context.id in self.subcribers:
        #     raise SubscriberAlreadyExistException(unique_operation_id=connection_context.id)
        if connection_context.id not in self.subcribers:
            self.subcribers.append(connection_context.id)
        connection_context_ = next(
            (
                context
                for context in self.connection_contexts
                if context["topic"] == topic
            ),
            None,
        )
        if not connection_context_:
            connection_context_ = {"topic": topic, "subscribers": []}
            self.connection_contexts.append(connection_context_)
        connection_context_["subscribers"].append(
            {
                "id": connection_context.id,
                "connection_context": connection_context,
                "queue": queue,
            }
        )
        while True:
            item = await queue.get()
            yield item

    async def create_topic(self, name: str):
        if name not in self.topics:
            self.topics.append(name)
        return name

    async def publish(self, topic: str, payload: dict):
        topic = await self.create_topic(topic)
        connection_context_ = next(
            (
                context
                for context in self.connection_contexts
                if context["topic"] == topic
            ),
            None,
        )
        if not connection_context_:
            connection_context_ = {"topic": topic, "subscribers": []}
            self.connection_contexts.append(connection_context_)
        # noinspection PyUnresolvedReferences,PyTypeChecker
        tasks = [
            asyncio.create_task(subscriber["queue"].put(payload))
            for subscriber in connection_context_["subscribers"]
        ]
        await asyncio.gather(*tasks)

    async def unsubscribe(self, connection_context: AsyncConnectionContext):
        if connection_context.id and connection_context.id in self.subcribers:
            self.subcribers.remove(connection_context.id)
