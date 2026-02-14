
from contextlib import asynccontextmanager

from fastapi import FastAPI

from api_gateway.container import AppContainer

from infra.messaging.registry import MessageringRegistry

@asynccontextmanager
async def lifespan(app: FastAPI):
    messaging_registry = MessageringRegistry()
    container = AppContainer(messaging_registry)

    app.state.container = container
    
    print("API Gateway is starting...")
    
    yield

    print("API Gateway is shutting down...")

    