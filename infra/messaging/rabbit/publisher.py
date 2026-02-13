
from rabbit.connect import RabbitMQ


class Publisher:
    def __init__(self, menssagering: RabbitMQ) -> None:
        self.menssagering = menssagering
    
    async def publish(self, exchange_name: str, routing_key: str, message: dict) -> None:
        await self.menssagering.publish(exchange_name, routing_key, message)
    