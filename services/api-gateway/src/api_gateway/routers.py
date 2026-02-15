from fastapi import APIRouter


from api_gateway.routes.account import router as ping_router


router = APIRouter(prefix="/api/v1")

router.include_router(ping_router)