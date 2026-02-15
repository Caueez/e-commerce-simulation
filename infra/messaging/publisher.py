
from dataclasses import asdict
from infra.messaging.interface.messagering import MessageringInterface


class Publisher:
    def __init__(self, menssagering: MessageringInterface, exchange_name: str, routing_key: str) -> None:
        self._menssagering = menssagering
        self._exchange_name = exchange_name
        self._routing_key = routing_key


    @property
    def exchange_name(self) -> str:
        return self._exchange_name

    @property
    def routing_key(self) -> str:
        return self._routing_key


    async def publish(self, message: dict) -> None:
        await self._menssagering.publish(self.exchange_name, self.routing_key, asdict(message))
    