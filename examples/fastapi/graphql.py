from fastapi import APIRouter
from starlette.requests import Request
from starlette.websockets import WebSocket

from graphql_ws.integrations.fastapi.server import FastAPISubscriptionServer
from graphql_ws.protocols import ProtocolEnum
from graphql_ws.subscription_managers import AsyncSubscriptionManager
from .schema import schema

router = APIRouter(tags=["GraphQL Server"])

subscription_manager = AsyncSubscriptionManager()
subscription_server = FastAPISubscriptionServer(
    schema, subscription_manager=subscription_manager
)


class Context:
    def __init__(
        self,
        request: Request | WebSocket,
        subscription_manager_: AsyncSubscriptionManager,
    ) -> None:
        self.subscription_manager = subscription_manager_


@router.post("", name="Endpoint")
async def graphql_post(request: Request):  # noqa
    """Graphql post request endpoint"""
    request_json = await request.json()
    result = await schema.execute_async(
        request_json.get("query"),
        operation_name=request_json.get("operationName"),
        variables=request_json.get("variables"),
        context=Context(request=request, subscription_manager_=subscription_manager),
    )
    return result.formatted


@router.websocket("", name="Subscription Endpoint")
async def websocket_endpoint(websocket: WebSocket):
    await subscription_server.handle(
        websocket,
        request_context=Context(
            request=websocket, subscription_manager_=subscription_manager
        ),
        protocol=ProtocolEnum.GRAPHQL_TRANSPORT_WS
    )
    return websocket
