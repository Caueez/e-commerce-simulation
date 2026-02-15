from abc import ABC, abstractmethod

class MessageringInterface(ABC):

    @abstractmethod
    async def connect(self) -> None: ...

    @abstractmethod
    async def close(self) -> None: ...

    @abstractmethod
    async def publish(self, event: dict) -> None: ...

    @abstractmethod
    async def consume(self, queue_name: str, callbacks: dict[str, callable]) -> None: ...

    @abstractmethod
    async def create_queue(self, queue_name: str, exchange_name: str, bindings: list[str], durable: bool = True) -> None: ...

    @abstractmethod
    async def create_exchange(self, exchange_name: str, exchange_type: str, durable: bool = True) -> None: ...

    @abstractmethod
    async def create_channel(self, qos: int = 10) -> None: ...
