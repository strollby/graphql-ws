import asyncio
import random
from typing import AsyncGenerator

import graphene
from graphene import ClientIDMutation
from graphql import GraphQLResolveInfo


class UserCreatePayload(graphene.ObjectType):
    client_mutation_id = graphene.String()
    name = graphene.String(required=True)


class UserObjectType(graphene.ObjectType):
    name = graphene.String(required=True)


class UserCreateMutation(ClientIDMutation):
    class Input:
        name = graphene.String(required=True)

    Output = UserCreatePayload

    # noinspection PyMethodMayBeStatic
    async def mutate_and_get_payload(
        self, info: GraphQLResolveInfo, name: str, client_mutation_id: str | None = None
    ):
        await info.context.subscription_manager.publish(
            topic="user_created", payload=UserObjectType(name=name)
        )
        # noinspection PyArgumentList
        return UserCreatePayload(client_mutation_id=client_mutation_id, name=name)


class Query(graphene.ObjectType):
    base = graphene.String()


class Mutation(graphene.ObjectType):
    user_create_mutation = UserCreateMutation.Field()


class RandomType(graphene.ObjectType):
    seconds = graphene.Int()
    random_int = graphene.Int()


class Subscription(graphene.ObjectType):
    user_created = graphene.Field(UserObjectType, required=True)
    count_seconds = graphene.Int(up_to=graphene.Int())
    random_int = graphene.Field(RandomType)

    async def subscribe_count_seconds(
        self, info: GraphQLResolveInfo, up_to: int = 100
    ) -> AsyncGenerator[int, None]:
        for i in range(up_to):
            yield i
            await asyncio.sleep(0.5)

    async def subscribe_user_created(
        self, info: GraphQLResolveInfo
    ) -> AsyncGenerator[str, None]:
        return info.context.subscription_manager.subscribe(
            topic="user_created", connection_context=info.context.connection_context
        )

    async def subscribe_random_int(self, info):
        i = 0
        while True:
            yield RandomType(seconds=i, random_int=random.randint(0, 500))
            await asyncio.sleep(1.0)
            i += 1


schema = graphene.Schema(
    query=Query,
    mutation=Mutation,
    subscription=Subscription,
)
