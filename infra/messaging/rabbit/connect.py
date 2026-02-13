import asyncio
import json
import aio_pika

from aio_pika import Message, RobustConnection, RobustChannel, RobustExchange, RobustQueue, AMQPException

class RabbitMQ:
    def __init__(self, url: str) -> None:
        self._url = url
        self._connection : RobustConnection | None = None
        self._channel : RobustChannel | None = None
        self._queue : dict[str, RobustQueue] = {}
        self._exchange : dict[str, RobustExchange] = {}

    async def connect(self) -> None:
        while True:
            try:
                if self._connection is not None:
                    print("Connection already open, closing connection...")
                    await self._connection.close()

                self._connection = await aio_pika.connect_robust(self._url)
                break
            except AMQPException as e:
                print(e)
                await asyncio.sleep(5)
    
    async def close(self) -> None:
        await self._connection.close()

    async def create_channel(self, qos: int = 10) -> RobustChannel:
        if self._connection is None:
            raise Exception("Connection is not open")
        
        self._channel = await self._connection.channel()
        await self._channel.set_qos(prefetch_count=qos)
    
    async def create_exchange(self, name: str, type: str, durable: bool) -> RobustExchange:
        if not self._channel:
            raise Exception("Channel is not open")
        
        self._exchange[name] = await self._channel.declare_exchange(name, type=type, durable=durable)

    async def create_queue(self, name: str, exchange_name: str, routing_key: str, durable: bool = True) -> RobustQueue:
        if not self._channel:
            raise Exception("Channel is not open")
        
        queue = await self._channel.declare_queue(name, durable=durable)

        if self._exchange[exchange_name] is None:
            raise Exception("Exchange is not open")
        
        await queue.bind(self._exchange[exchange_name], routing_key=routing_key)

        self._queue[name] = queue
    
    async def consume(self, queue_name: str, callback: callable) -> None:
        if not self._channel:
            raise Exception("Channel is not open")
        
        await self._queue[queue_name].consume(callback)

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


