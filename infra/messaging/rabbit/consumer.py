
from rabbit.connect import RabbitMQ


class Consumer:
    def __init__(self, menssagering: RabbitMQ) -> None:
        self.menssagering = menssagering
    
    async def consume(self, queue_name: str, callback: callable) -> None:
        await self.menssagering.consume(queue_name, callback)
    