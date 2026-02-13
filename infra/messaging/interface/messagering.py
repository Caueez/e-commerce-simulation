from abc import ABC, abstractmethod

class MessageringInterface(ABC):

    @abstractmethod
    async def connect(self) -> None: ...

    @abstractmethod
    async def close(self) -> None: ...

    @abstractmethod
    async def publish(self, exchange_name: str, routing_key: str, message: dict) -> None: ...

    @abstractmethod
    async def consume(self, queue_name: str, callback: callable) -> None: ...

    @abstractmethod
    async def create_queue(self, queue_name: str, exchange_name: str, routing_key: str, durable: bool = True) -> None: ...

    @abstractmethod
    async def create_exchange(self, exchange_name: str, exchange_type: str, durable: bool = True) -> None: ...

    @abstractmethod
    async def create_channel(self, qos: int = 10) -> None: ...