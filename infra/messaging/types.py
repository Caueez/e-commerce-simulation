from dataclasses import dataclass


@dataclass(frozen=True)
class ExchangeType:
    exchange_name: str
    exchange_type: str
    durable: bool


@dataclass(frozen=True)
class QueueType:
    queue_name: str
    exchange_name: str
    bindings: list[str]
    durable: bool


@dataclass
class BuildSchema:
    exchanges: list[ExchangeType]
    queues: list[QueueType]