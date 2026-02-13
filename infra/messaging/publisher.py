
from messaging.interface.messagering import MessageringInterface


class Publisher:
    def __init__(self, menssagering: MessageringInterface, exchange_name: str, routing_key: str) -> None:
        self.menssagering = menssagering
        self.exchange_name = exchange_name
        self.routing_key = routing_key
    
    async def publish(self, message: dict) -> None:
        await self.menssagering.publish(self.exchange_name, self.routing_key, message)
    