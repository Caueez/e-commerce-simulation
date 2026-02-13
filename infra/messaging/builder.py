import asyncio
from rabbit.consumer import Consumer
from rabbit.publisher import Publisher
from rabbit.connect import RabbitMQ



class MessageringBuilder:
    def __init__(self):
        self.messagering = RabbitMQ("amqp://admin:admin@localhost:5672")

    async def build(self):  
        await self.messagering.connect()
        await self.messagering.create_channel()
        await self.messagering.create_exchange("account", "direct", True)
        await self.messagering.create_queue("account", "account", "account", durable=True)
    
    async def create_consumer(self) -> Consumer:
        return Consumer(self.messagering)
    
    async def create_publisher(self) -> Publisher:
        return Publisher(self.messagering)

if __name__ == "__main__":
    try:
        builder = MessageringBuilder()
        asyncio.run(builder.build())

    except KeyboardInterrupt:
        print("Connection closed")
