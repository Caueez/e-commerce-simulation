from abc import ABC, abstractmethod


class CacheInterface(ABC):
    @abstractmethod
    async def build(self): ...

    @abstractmethod
    async def get(self, key: str): ...

    @abstractmethod
    async def set(self, key: str, value: str, ex: int = 60): ...

    @abstractmethod
    async def delete(self, key: str): ...
