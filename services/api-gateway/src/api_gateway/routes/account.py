import asyncio

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
async def create_account(
    request: CreateAccountResquest,
    container: AppContainer = Depends(get_container)
    ):

    response = await container.create_account_use_case.execute(request.name, request.email, request.password)

    return JSONResponse(content=response, status_code=status.HTTP_202_ACCEPTED)

@router.get("/accounts/{account_id}")
async def get_accounts(
    account_id: str, 
    container: AppContainer = Depends(get_container)
    ):
    
    try:
        response = await container.get_account_use_case.execute(account_id)
    except asyncio.TimeoutError:
        return JSONResponse(
            content={"message": "Timeout waiting for account response"},
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
        )

    return JSONResponse(content=response, status_code=status.HTTP_200_OK)
