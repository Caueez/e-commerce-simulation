


from infra.messaging.builder import MessageringBuilder
from infra.messaging.interface.messagering import MessageringInterface
from infra.messaging.rabbit.connect import RabbitMQ
from infra.messaging.types import BuildSchema


class MessageringBootstrap:
    def __init__(self, url: str, schema: BuildSchema) -> None:
        self._url = url
        self._schema = schema
        self._messagering : RabbitMQ | None = None
    
    async def close(self) -> None:
        await self._messagering.close()

    async def start(self) -> MessageringInterface:
        self._messagering = RabbitMQ(self._url)
        builder = MessageringBuilder(self._schema, self._messagering)

        await builder.build()

        return self._messagering
