#  Copyright © 2020 - 2023 Strollby, Inc or it's affiliates. All Rights Reserved.
#  Project : Strollby Experiences
#  Filename : apollo_sandbox.py
#  Author : u58346
#  Current modification time : Tue, 11 Apr 2023 at 11:12 am India Standard Time
#  Last modified time : Thu, 6 Apr 2023 at 1:09 pm India Standard Time
from fastapi import APIRouter
from starlette.responses import HTMLResponse

router = APIRouter(tags=["GraphQL Server"])


@router.get("/", name="Apollo Sandbox")
async def apollo_sandbox() -> HTMLResponse:
    """Endpoint for ping-pong healthcheck"""
    return HTMLResponse(
        content="""
        <div id="sandbox" style="position:absolute;top:0;right:0;bottom:0;left:0"></div>
        <script
         src="https://embeddable-sandbox.cdn.apollographql.com/_latest/embeddable-sandbox.umd.production.min.js">
         </script>
        <script>
         new window.EmbeddedSandbox({
           target: "#sandbox",
           // Pass through your server href if you are embedding on an endpoint.
           // Otherwise, you can pass whatever endpoint you want Sandbox to start up with here.
           initialEndpoint: window.location.origin + "/graphql",
         });
         // advanced options: https://www.apollographql.com/docs/studio/explorer/sandbox#embedding-sandbox
        </script>
    """
    )
