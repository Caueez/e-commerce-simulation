
from dataclasses import asdict

from infra.messaging.interface.messagering import MessageringInterface

import hashlib
# hashlib.scrypt(password.encode("utf-8"), salt=password.encode("utf-8"), n=2**14, r=8, p=1, dklen=32).hex()

from api_gateway.contracts.account import AccountCreatedEvent, AccountCreatedPayload

class CreateAccountUseCase:
    def __init__(self, bus) -> None:
        self.bus : MessageringInterface = bus

    async def execute(self, name: str, email: str, password: str):

        event = AccountCreatedEvent(
            idempotency_key=hashlib.sha256(email.encode()).hexdigest(),
            payload=AccountCreatedPayload(
                name=name, 
                email=email, 
                password=password
                )
            )

        await self.bus.publish(asdict(event))
        
        return {"message": "Account created"}