
import asyncio
from dataclasses import asdict

from api_gateway.settings import ApiGatewaySettings

from infra.cache.redis.redis_impl import RedisCache

from infra.database.postgres.postgres import PostgresDatabase

from infra.messaging.bootstrap import MessageringBootstrap
from infra.messaging.types import BuildSchema, ExchangeType, QueueType

from api_gateway.contracts.account import AccountRespondedEvent, AccountResponsePayload
from api_gateway.use_cases.create_account import CreateAccountUseCase
from api_gateway.use_cases.get_account import GetAccountUseCase


schema = BuildSchema(
    exchanges=[
        ExchangeType(
            exchange_name="exchange",
            exchange_type="direct",
            durable=True
        )
    ],
    queues=[
        QueueType(
            queue_name="account",
            exchange_name="exchange",
            bindings=[
                "account.request", 
                "account.response", 
                "account.created", 
                "account.updated", 
                "account.deleted"
                ],
            durable=True
        ),
    ])


class Handler:
    def __init__(self, container: "AppContainer") -> None:
        self.container = container

    async def handle_account_created(self, payload: dict):
        print(payload)

    async def handle_account_request(self, payload: dict):
        request_payload = payload.get("payload", {})
        correlation_id = payload.get("correlation_id")

        if not correlation_id:
            return

        # Consumer local para demonstrar RPC sem alterar outros serviços.
        response = AccountRespondedEvent(
            correlation_id=correlation_id,
            payload=AccountResponsePayload(
                id=request_payload.get("id", ""),
                name="Mock Account",
                email="mock-account@email.com",
            ),
        )

        await self.container.bus.publish(asdict(response))

    async def handle_account_response(self, payload: dict):
        correlation_id = payload.get("correlation_id")

        if not correlation_id:
            return

        future = self.container.pending_requests.get(correlation_id)
        if not future or future.done():
            return

        future.set_result(payload)

class AppContainer:
    def __init__(self) -> None:
        self.settings = ApiGatewaySettings()

        self.msg_bootstrap = MessageringBootstrap(self.settings.MESSAGERING_ENV.url, schema)

        self.cache = RedisCache(
            self.settings.CACHE_ENV.host, 
            self.settings.CACHE_ENV.port
            )
        
        self.repo = PostgresDatabase(
            self.settings.DB_ENV.host, 
            self.settings.DB_ENV.port, 
            self.settings.DB_ENV.user, 
            self.settings.DB_ENV.password, 
            self.settings.DB_ENV.dbname
        )
        self.pending_requests: dict[str, asyncio.Future] = {}
        self._handler = Handler(self)

    async def bootstrap(self):
        self.bus = await self.msg_bootstrap.start()
        await self.cache.build()
        await self.repo.connect()

        handlers = {
            "account.created": self._handler.handle_account_created,
            "account.request": self._handler.handle_account_request,
            "account.response": self._handler.handle_account_response,
        }
        await self.bus.consume("account", handlers) 

        self.create_account_use_case = CreateAccountUseCase(self.bus)
        self.get_account_use_case = GetAccountUseCase(self.bus, self.pending_requests)
    
    async def shutdown(self):
        await self.repo.close()
        await self.msg_bootstrap.close()
