

from infra.cache.redis.redis_impl import RedisCache
from infra.database.postgres.postgres import PostgresDatabase
from infra.messaging.rabbit.connect import RabbitMQ
from infra.messaging.registry import MessageringRegistry
from api_gateway.settings import ApiGatewaySettings


class AppContainer:
    def __init__(self) -> None:
        self.settings = ApiGatewaySettings()

        self.messagering = RabbitMQ(self.settings.MESSAGERING_ENV.url)
        self.msg_registry = MessageringRegistry(self.messagering)

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
        await self.msg_registry.build()
        await self.cache.build()
        await self.repo.connect()
    
    async def shutdown(self):
        await self.repo.close()
        await self.messagering.close()