


from infra.messaging.builder import MessageringBuilder
from infra.messaging.registry import MessageringRegistry
from infra.messaging.rabbit.connect import RabbitMQ
from infra.messaging.types import BuildSchema


class MessageringBootstrap:
    def __init__(self, url: str, schema: BuildSchema) -> None:
        self._url = url
        self._schema = schema
        self._messagering : RabbitMQ | None = None
    
    async def close(self) -> None:
        await self._messagering.close()

    async def start(self) -> MessageringRegistry:
        self._messagering = RabbitMQ(self._url)
        registry = MessageringRegistry(self._messagering)
        builder = MessageringBuilder(self._schema, self._messagering)

        await builder.build()

        consumers = builder.create_consumer()
        publishers = builder.create_publisher()

        for key, consumer in consumers.items():
            await consumer.consume()
            registry.set_consumer(key, consumer)

        for key, publisher in publishers.items():
            registry.set_publisher(key, publisher)

        return registry
