

from infra.cache.redis.redis_impl import RedisCache
from infra.database.postgres.postgres import PostgresDatabase
from infra.messaging.registry import MessageringRegistry
from core.config import Settings


class AppContainer:
    def __init__(self) -> None:
        self.settings = Settings()
        self.msg_registry = MessageringRegistry()
        self.redis = RedisCache("localhost", 6379)
        self.repo = PostgresDatabase(host="localhost", port=5432, user="admin", password="admin", dbname="db")

    async def bootstrap(self):
        await self.msg_registry.build()
        await self.redis.build()
        await self.repo.connect()