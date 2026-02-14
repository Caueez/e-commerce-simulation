
from infra.messaging.interface.messagering import MessageringInterface
from infra.messaging.types import BuildSchema, ExchangeType, QueueType


class MessageringBuilder:
    def __init__(self, schema: BuildSchema, messagering: MessageringInterface) -> None:
        self.messagering = messagering
        self.schema = schema

    async def _create_connetion(self):  
        await self.messagering.connect()
        await self.messagering.create_channel()
    
    async def _create_exchange(self, schema: ExchangeType) -> None:
        await self.messagering.create_exchange(schema.exchange_name, schema.exchange_type, schema.durable)

    async def _create_queue(self, schema: QueueType) -> None:
        await self.messagering.create_queue(schema.queue_name, schema.exchange_name, schema.routing_key, durable=schema.durable)
    
    async def build(self):        
        await self._create_connetion()
        
        for exchange in self.schema.exchanges:
            await self._create_exchange(exchange)
        
        for queue in self.schema.queues:
            await self._create_queue(queue)