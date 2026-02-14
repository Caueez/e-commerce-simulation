


from infra.messaging.consumer import Consumer
from infra.messaging.interface.messagering import MessageringInterface
from infra.messaging.publisher import Publisher
from infra.messaging.types import BuildSchema


class MessageringFactory:
    def __init__(self, schema: BuildSchema, messagering: MessageringInterface) -> None:
        self.messagering = messagering
        self.schema = schema

    def create_consumer(self) -> list[Consumer]:
        return [
            Consumer(self.messagering, con.queue_name, con.callback) 
            for con in self.schema.consumers 
            ]
    
    def create_publisher(self) -> list[Publisher]:
        return [
            Publisher(self.messagering, pub.exchange_name, pub.routing_key) 
            for pub in self.schema.publishers 
            ] 
        
        
