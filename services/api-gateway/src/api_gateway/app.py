from fastapi import FastAPI

from api_gateway.lifespan import lifespan

from api_gateway.routers import router



def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan, title="API Gateway", description="API Gateway from FastAPI", version="0.0.1")
    app.include_router(router)
    return app


app = create_app()
    