from fastapi import APIRouter, Depends, Request, status

from fastapi.responses import JSONResponse

from api_gateway.container import AppContainer


router = APIRouter(tags=["Accounts"])

from pydantic import BaseModel


class CreateAccountResquest(BaseModel):
    name: str
    email: str
    password: str


def get_container(request: Request) -> AppContainer:
    return request.app.state.container


@router.post("/accounts")
async def ping(
    request: CreateAccountResquest,
    container: AppContainer = Depends(get_container)
    ):

    response = await container.create_account_use_case.execute(request.name, request.email, request.password)

    return JSONResponse(content=response, status_code=status.HTTP_202_ACCEPTED)