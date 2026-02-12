import asyncio
import aio_pika

from aio_pika import RobustConnection, RobustChannel

class RabbitMQ:
    def __init__(self) -> None:
        self._url : str | None = None
        self._connection : RobustConnection | None = None

    async def connect(self, url: str) -> None:
        while True:
            try:
                if self._connection is not None:
                    print("Connection already open, closing connection...")
                    await self._connection.close()

                self._connection = await aio_pika.connect_robust(url)
            except Exception as e:
                print(e)
                await asyncio.sleep(5)
    
    async def close(self) -> None:
        await self._connection.close()

    async def channel(self) -> RobustChannel:
        if self._connection is None:
            raise Exception("Connection is not open")
        
        return await self._connection.channel()


