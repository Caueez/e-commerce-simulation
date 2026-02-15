
from infra.messaging.interface.messagering import MessageringInterface

class Consumer:
    def __init__(self, menssagering: MessageringInterface, queue_name: str, callbacks: dict[str, callable]) -> None:
        self._menssagering = menssagering
        self._queue_name = queue_name
        self._callbacks = callbacks
    

    @property
    def queue_name(self) -> str:
        return self._queue_name
    
    @property
    def callback(self, routing_key: str) -> callable:
        return self._callbacks[routing_key]


    async def consume(self) -> None:
        await self._menssagering.consume(self.queue_name, self._callbacks)

    
    