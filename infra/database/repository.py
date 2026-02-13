
from infra.database.interface.database import DatabaseInterface


class DatabaseRepository:
    def __init__(self, database: DatabaseInterface) -> None:
        self._database = database

    async def connect(self) -> None:
        await self._database.connect()

    async def execute(self, query: str, *args) -> str:
        return await self._database.execute(query, *args)
    
    async def fetch_one(self, query: str, *args):
        return await self._database.fetch_one(query, *args)
    
    async def fetch_all(self, query: str, *args):
        return await self._database.fetch_all(query, *args)
    
    async def close(self):
        await self._database.close()