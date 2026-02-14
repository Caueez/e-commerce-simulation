
from infra.messaging.interface.messagering import MessageringInterface

class Consumer:
    def __init__(self, menssagering: MessageringInterface, queue_name: str, callback: callable) -> None:
        self.menssagering = menssagering
        self.queue_name = queue_name
        self.callback = callback
    
    async def consume(self) -> None:
        await self.menssagering.consume(self.queue_name, self.callback)

    
    