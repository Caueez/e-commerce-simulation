
from rabbit.consumer import Consumer
from rabbit.publisher import Publisher
from rabbit.connect import RabbitMQ


class Handler:
    @staticmethod
    async def handle(message: dict) -> None:
        print("Received message :", message.get("id"))

class MessageringBuilder:
    def __init__(self) -> None:
        self.messagering = RabbitMQ("ampq://admin:admin@localhost:5672/")

    async def _create_connetion(self):  
        await self.messagering.connect()
        await self.messagering.create_channel()
    
    async def _create_exchange(self, exchange_name: str, exchange_type: str, durable: bool = True) -> None:
        await self.messagering.create_exchange(exchange_name, exchange_type, durable)

    async def _create_queue(self, exchange_name: str, routing_key: str, queue_name: str) -> None:
        await self.messagering.create_queue(queue_name, exchange_name, routing_key, durable=True)

    async def _create_consumer(self, queue_name: str, callback: callable) -> Consumer:
        return Consumer(self.messagering, queue_name, callback)
    
    async def _create_publisher(self, exchange_name: str, routing_key: str) -> Publisher:
        return Publisher(self.messagering, exchange_name, routing_key)
    
    async def build(self):
        await self._create_connetion()
        await self._create_exchange('exchange', 'direct', True)
        await self._create_queue('exchange', 'routing_key', 'queue')

        consumer = await self._create_consumer('queue', Handler.handle)
        await consumer.consume()
    
        publisher = await self._create_publisher('exchange', 'routing_key')
        await publisher.publish({'id': 1})


if __name__ == "__main__":
    import asyncio

    builder = MessageringBuilder()
    asyncio.run(builder.build())