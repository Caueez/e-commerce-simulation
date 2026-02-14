from typing import Optional
import asyncpg

from infra.database.interface.database import DatabaseInterface


class PostgresDatabase(DatabaseInterface):
    def __init__(self, host: str, port: str, user: str, password: str, dbname: str) -> None:
        self._dsn = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
        self._pool : Optional[asyncpg.Pool] = None

    async def connect(self) -> None:
        try:
            self._pool = await asyncpg.create_pool(
                dsn=self._dsn,
                max_size=10,
                min_size=1
            )
        except asyncpg.ConnectionFailureError as e:
            print(e)
    
    async def close(self) -> None:
        await self._pool.close()
    
    async def fetch_one(self, query: str, *args) -> Optional[asyncpg.Record]:
        async with self._pool.acquire() as conn:
            if isinstance(conn, asyncpg.Connection):
                return await conn.fetchrow(query, *args)

    async def fetch_all(self, query: str, *args) -> list[asyncpg.Record]:
        async with self._pool.acquire() as conn:
            if isinstance(conn, asyncpg.Connection):
                return await conn.fetch(query, *args)

    async def execute(self, query: str, *args) -> str:
        async with self._pool.acquire() as conn:
            if isinstance(conn, asyncpg.Connection):
                return await conn.execute(query, *args)