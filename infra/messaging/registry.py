
from infra.messaging.interface.messagering import MessageringInterface
from infra.messaging.publisher import Publisher
from infra.messaging.consumer import Consumer


class MessageringRegistry:
    def __init__(self, messagering: MessageringInterface) -> None:
        self._messagering = messagering
        self._consumers : dict[str, Consumer] = {}
        self._publishers : dict[str, Publisher] = {}
    
    @property
    def messagering(self) -> MessageringInterface:
        return self._messagering

    def set_publisher(self, routing_key: str, publisher: Publisher) -> None:
        self._publishers[routing_key] = publisher

    def set_consumer(self, queue_name: str, consumer: Consumer) -> None:
        self._consumers[queue_name] = consumer
    
    def get_publisher(self, routing_key: str) -> Publisher:
        if routing_key not in self._publishers.keys():
            raise Exception("Routing_key not found")
        
        return self._publishers[routing_key]

    def get_consumer(self, queue_name: str) -> Consumer:
        if queue_name not in self._consumers.keys():
            raise Exception("Queue not found")
        
        return self._consumers[queue_name]
