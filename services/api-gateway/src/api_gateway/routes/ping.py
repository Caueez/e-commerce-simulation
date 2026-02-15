from fastapi import APIRouter, Request


router = APIRouter(prefix="/ping", tags=["Ping"])


@router.get("/pub1")
async def ping(request: Request):

    publisher = request.app.state.container.msg_registry.get_publisher("routing_key")

    await publisher.publish({"message": "pub1"})

    return {"ping": "pong"}

@router.get("/pub2")
async def ping(request: Request):

    publisher = request.app.state.container.msg_registry.get_publisher("routing_key_2")

    await publisher.publish({"message": "pub2"})

    return {"ping": "pong"}