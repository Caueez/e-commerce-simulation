
from infra.messaging.registry import MessageringRegistry
import os

from infra.messaging.publisher import Publisher
import asyncio



class ManualTest:
    def __init__(self):
        self.registry = MessageringRegistry()
    
    async def _build(self):
        await self.registry.build()

    async def main_sync(self):
        await self._build()

        for consumer in self.registry.consumers:
            await consumer.consume()

        while True:
            for i, publisher in enumerate(self.registry.publishers):
                await publisher.publish({"id": i + 1})

            await asyncio.sleep(0.1)


    async def main_async(self):
        await self._build()

        async def test_async_publisher(publisher: Publisher, i: int):
            while True:
                try:
                    await publisher.publish({"id": i + 1})
                except Exception as e:
                    print(e)
                await asyncio.sleep(0.1)

        tasks = []

        for consumer in self.registry.consumers:
            await consumer.consume()

        for i, publisher in enumerate(self.registry.publishers):
            tasks.append(test_async_publisher(publisher, i))
        
        await asyncio.gather(*tasks)

        await self.registry.messagering.close()
