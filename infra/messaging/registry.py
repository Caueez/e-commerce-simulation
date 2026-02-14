
from infra.messaging.builder import MessageringBuilder
from infra.messaging.consumer import Consumer
from infra.messaging.factory import MessageringFactory
from infra.messaging.interface.messagering import MessageringInterface
from infra.messaging.publisher import Publisher

from infra.messaging.rabbit.connect import RabbitMQ

from infra.messaging.types import BuildSchema, ConsumerType, ExchangeType, PublisherType, QueueType


class Handler:
    @staticmethod
    async def handle(message: dict) -> None:
        print("Received message :", message.get("message"))


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
            routing_key="routing_key",
            durable=True
        ),
        QueueType(
            queue_name="queue_2",
            exchange_name="exchange",
            routing_key="routing_key_2",
            durable=True
        )
    ],
    consumers=[
        ConsumerType(
            queue_name="queue",
            callback=Handler.handle
        ),
        ConsumerType(
            queue_name="queue_2",
            callback=Handler.handle
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

class MessageringRegistry:
    def __init__(self, messagering: MessageringInterface) -> None:
        self.messagering = messagering
        self._builder : MessageringBuilder = None
        self._factory : MessageringFactory = None
        self.consumers : dict[str, Consumer] = []
        self.publishers : dict[str, Publisher] = []

    async def build(self) -> None:
        self._builder = MessageringBuilder(schema, self.messagering)
        await self._builder.build()

        self._factory = MessageringFactory(schema, self.messagering)

        self.consumers = self._factory.create_consumer()
        self.publishers = self._factory.create_publisher()

        for con in self.consumers.values(): 
            await con.consume()
    
    async def publisher(self, routing_key: str) -> Publisher:
        if routing_key not in self.publishers.keys():
            raise Exception("Routing_key not found")
        
        return self.publishers[routing_key]

    async def consumer(self, queue_name: str) -> Consumer:
        if queue_name not in self.consumers.keys():
            raise Exception("Queue not found")
        
        return self.consumers[queue_name]
    