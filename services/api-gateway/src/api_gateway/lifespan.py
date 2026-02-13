
from contextlib import asynccontextmanager

from fastapi import FastAPI



@asynccontextmanager
async def lifespan(app: FastAPI):
    
    print("API Gateway is starting...")
    
    yield

    print("API Gateway is shutting down...")

    