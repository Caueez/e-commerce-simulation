import asyncio
import json
import aio_pika

from aio_pika import IncomingMessage, Message, RobustConnection, RobustChannel, RobustExchange, RobustQueue, AMQPException

from infra.messaging.interface.messagering import MessageringInterface


class RabbitMQ(MessageringInterface):
    def __init__(self, url: str) -> None:
        self._url = url
        self._connection : RobustConnection | None = None
        self._channel : RobustChannel | None = None
        self._queue : dict[str, RobustQueue] = {}
        self._exchange : dict[str, RobustExchange] = {}

    async def connect(self) -> None:
        while True:
            try:
                if self._connection:
                    print("Connection already open, skipping...")
                    break

                self._connection = await aio_pika.connect_robust(self._url)
                break
            except AMQPException as e:
                print(e)
                await asyncio.sleep(5)
    
    async def close(self) -> None:
        await self._connection.close()
        self._connection = None

    async def create_channel(self, qos: int = 10) -> None:
        if self._connection is None:
            raise Exception("Connection is not open")
        
        self._channel = await self._connection.channel()
        await self._channel.set_qos(prefetch_count=qos)
    
    async def create_exchange(self, name: str, type: str, durable: bool) -> None:
        if not self._channel:
            raise Exception("Channel is not open")
        
        self._exchange[name] = await self._channel.declare_exchange(name, type=type, durable=durable)

    async def create_queue(self, queue_name: str, exchange_name: str, routing_key: str, durable: bool = True) -> None:
        if not self._channel:
            raise Exception("Channel is not open")
        if self._exchange[exchange_name] is None:
            raise Exception("Exchange is not open")
        
        self._queue[queue_name] = await self._channel.declare_queue(queue_name, durable=durable)
        
        await self._queue[queue_name].bind(self._exchange[exchange_name], routing_key=routing_key)
    
    async def consume(self, queue_name: str, callback: callable) -> None:
        if not self._channel:
            raise Exception("Channel is not open")
        
        await self._queue[queue_name].consume(lambda message: _on_message(message, callback))
    
        async def _on_message(message: IncomingMessage, callback: callable) -> None:
            async with message.process():
                await callback(json.loads(message.body))

    async def publish(self, exchange_name: str, routing_key: str, message: dict) -> None:
        if not self._channel:
            raise Exception("Channel is not open")
        
        if self._exchange[exchange_name] is None:
            raise Exception("Exchange is not open")
        
        message = Message(
            json.dumps(message).encode("utf-8"),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT
        )
        
        await self._exchange[exchange_name].publish(message=message, routing_key=routing_key)


