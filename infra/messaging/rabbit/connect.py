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

    async def create_queue(self, queue_name: str, exchange_name: str, bindings: list[str], durable: bool = True) -> None:
        if not self._channel:
            raise Exception("Channel is not open")
        exchange = self._exchange.get(exchange_name)
        if exchange is None:
            raise Exception("Exchange is not open")
        
        self._queue[queue_name] = await self._channel.declare_queue(queue_name, durable=durable)
        
        for routing_key in bindings:
            await self._queue[queue_name].bind(exchange, routing_key=routing_key)
    
    async def consume(self, queue_name: str, callbacks: dict[str, callable]) -> None:
        if not self._channel:
            raise Exception("Channel is not open")

        queue = self._queue.get(queue_name)
        if queue is None:
            raise Exception("Queue is not open")

        async def _on_message(message: IncomingMessage, callbacks: dict[str, callable]) -> None:
            async with message.process():
                callback = callbacks.get(message.routing_key)
                if callback is None:
                    return
                await callback(json.loads(message.body))

        await queue.consume(lambda message: _on_message(message, callbacks))

    async def publish(self, event: dict) -> None:
        if not self._channel:
            raise Exception("Channel is not open")

        exchange = self._exchange.get(event.get("exchange_name"))
        if exchange is None:
            raise Exception("Exchange is not open")
        
        message = Message(
            json.dumps(event).encode("utf-8"),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT
        )
        
        await exchange.publish(message=message, routing_key=event.get("routing_key"))

