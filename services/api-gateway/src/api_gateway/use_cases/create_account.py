

import json
import uuid

from infra.database.repository import DatabaseRepository
from infra.messaging.registry import MessageringRegistry

import hashlib
# hashlib.scrypt(password.encode("utf-8"), salt=password.encode("utf-8"), n=2**14, r=8, p=1, dklen=32).hex()

from dataclasses import dataclass


@dataclass
class AccountCreatedPayload:
    name: str
    email: str
    password: str

@dataclass
class AccountCreatedEvent:
    idempotency_key: str
    payload: AccountCreatedPayload



class CreateAccountUseCase:
    def __init__(self, repo, msg_registry) -> None:
        self.repo : DatabaseRepository = repo
        self.msg_registry : MessageringRegistry = msg_registry

    
    async def execute(self, name: str, email: str, password: str):

        event = AccountCreatedEvent(
            idempotency_key=str(uuid.uuid4()),
            payload=AccountCreatedPayload(name, email, password)
            )


        await self.msg_registry.get_publisher("routing_key").publish(
            event
            )
        
        return {"message": "Account created"}