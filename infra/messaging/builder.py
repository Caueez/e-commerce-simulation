
from infra.messaging.types import BuildSchema

from infra.messaging.interface.messagering import MessageringInterface
from infra.messaging.publisher import Publisher
from infra.messaging.consumer import Consumer


class MessageringBuilder:
    def __init__(self, schema: BuildSchema, messagering: MessageringInterface) -> None:
        self.messagering = messagering
        self.schema = schema
    
    async def build(self) -> None:
        await self._create_connetion()
        await self._create_exchange()
        await self._create_queue()

    async def _create_connetion(self):  
        await self.messagering.connect()
        await self.messagering.create_channel()
    
    async def _create_exchange(self) -> None:
        for exchange in self.schema.exchanges:
            await self.messagering.create_exchange(exchange.exchange_name, exchange.exchange_type, exchange.durable)

    async def _create_queue(self) -> None:
        for queue in self.schema.queues:
            await self.messagering.create_queue(queue.queue_name, queue.exchange_name, queue.bindings, durable=queue.durable)
    
    def create_publisher(self) -> dict[str, Publisher]:
        return {
            pub.routing_key:
            Publisher(self.messagering, pub.exchange_name, pub.routing_key) 
            for pub in self.schema.publishers
        }
    
    def create_consumer(self) -> dict[str, Consumer]:
        return {
            con.queue_name:
            Consumer(self.messagering, con.queue_name, con.callbacks) 
            for con in self.schema.consumers 
        }