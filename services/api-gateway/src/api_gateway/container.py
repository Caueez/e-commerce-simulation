
from api_gateway.settings import ApiGatewaySettings

from infra.cache.redis.redis_impl import RedisCache

from infra.database.postgres.postgres import PostgresDatabase

from infra.messaging.registry import MessageringRegistry
from infra.messaging.bootstrap import MessageringBootstrap
from infra.messaging.types import BuildSchema, ConsumerType, ExchangeType, PublisherType, QueueType

from api_gateway.use_cases.create_account import CreateAccountUseCase


class Handler:
    @staticmethod
    async def handle(message: dict) -> None:
        print("Handler 1 :", message)
    
    @staticmethod
    async def handle_2(message: dict) -> None:
        print("Handler 2 :", message)


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
            queue_name="queue",
            exchange_name="exchange",
            bindings=["routing_key", "routing_key_2"],
            durable=True
        ),
    ],
    consumers=[
        ConsumerType(
            queue_name="queue",
            callbacks={
                "routing_key": Handler.handle,
                "routing_key_2": Handler.handle_2
            }
        )
    ],
    publishers=[
        PublisherType(
            exchange_name="exchange",
            routing_key="routing_key"
        ),
        PublisherType(
            exchange_name="exchange",
            routing_key="routing_key_2"
        ),
    ])

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

    async def bootstrap(self):
        self.msg_registry = await self.msg_bootstrap.start()
        await self.cache.build()
        await self.repo.connect()

        self.create_account_use_case = CreateAccountUseCase(self.repo, self.msg_registry)
    
    async def shutdown(self):
        await self.repo.close()
        await self.msg_bootstrap.close()