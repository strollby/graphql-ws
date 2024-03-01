import json
import os

from google import pubsub_v1
from graphql import FormattedExecutionResult

from graphql_ws.subscription_managers import AsyncSubscriptionManager


class AsyncGooglePubSubAsyncManager(AsyncSubscriptionManager):

    def __init__(self):
        super().__init__()
        self.publisher = pubsub_v1.PublisherClient()

    @staticmethod
    def topic_name(topic: str):
        return "projects/{project_id}/topics/{topic}".format(
            project_id=os.getenv("GOOGLE_CLOUD_PROJECT"), topic=topic
        )

    async def subscribe(self):
        pass

    def create_topic(self, name: str):
        self.publisher.create_topic(name=self.topic_name(name))

    async def publish(self, topic: str, payload: FormattedExecutionResult):
        topic = self.topic_name(topic=topic)
        if topic not in self.topics:
            self.create_topic(name=topic)
        # noinspection PyArgumentList
        await self.publisher.publish(
            topic=topic, payload=json.dumps(payload).encode("utf-8")
        )

    def unsubscribe(self):
        pass
