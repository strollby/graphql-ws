from fastapi import FastAPI

from .apollo_sandbox import router as apollo_sandbox_router
from .graphql import router as graphql_router

app = FastAPI()

app.include_router(apollo_sandbox_router, prefix="")
app.include_router(graphql_router, prefix="/graphql")
