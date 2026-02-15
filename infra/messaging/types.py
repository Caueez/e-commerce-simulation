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


@dataclass(frozen=True)
class ConsumerType:
    queue_name: str
    callbacks: dict[str, callable]


@dataclass(frozen=True)
class PublisherType:
    exchange_name: str
    routing_key: str


@dataclass
class BuildSchema:
    exchanges: list[ExchangeType]
    queues: list[QueueType]
    consumers: list[ConsumerType]
    publishers: list[PublisherType]