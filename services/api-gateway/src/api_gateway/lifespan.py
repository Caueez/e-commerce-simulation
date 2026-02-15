
from contextlib import asynccontextmanager

from fastapi import FastAPI

from api_gateway.container import AppContainer

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("API Gateway is starting...")

    container = AppContainer()
    await container.bootstrap()    

    app.state.container = container
    
    yield
    print("API Gateway is shutting down...")

    await container.shutdown()

    