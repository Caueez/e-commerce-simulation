
from redis.asyncio import Redis

from infra.cache.interface.cache import CacheInterface


class RedisCache(CacheInterface):
    def __init__(
            self, 
            host: str, 
            port: int, 
            db: int = 0, 
            decode_responses: bool = True, 
            client_name: str = "redis"
        ) -> None:

        self._cache = None
        self._host = host
        self._port = port
        self._db = db
        self._decode_responses = decode_responses
        self._client_name = client_name
    
    async def build(self):
        self._cache = Redis(
            host=self._host, 
            port=self._port, 
            db=self._db, 
            decode_responses=self._decode_responses, 
            client_name=self._client_name)

    async def get(self, key: str):
        return await self._cache.get(key)
    
    async def set(self, key: str, value: str, ex: int = 60):
        return await self._cache.set(key, value, ex=ex)
    
    async def delete(self, key: str):
        return await self._cache.delete(key)