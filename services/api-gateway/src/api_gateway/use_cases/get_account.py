
import asyncio
from dataclasses import asdict
import hashlib
from typing import Any
import uuid

from api_gateway.contracts.account import AccountRequestedCommand, AccountRequestedPayload

from infra.messaging.interface.messagering import MessageringInterface



class GetAccountUseCase:
    def __init__(self, bus, pending_requests: dict[str, asyncio.Future]) -> None:
        self.bus: MessageringInterface = bus
        self.pending_requests = pending_requests

    async def execute(self, id: str) -> dict[str, Any]:
        correlation_id = str(uuid.uuid4())
        future = asyncio.get_running_loop().create_future()
        self.pending_requests[correlation_id] = future

        event = AccountRequestedCommand(
            idempotency_key=hashlib.sha256(id.encode()).hexdigest(),
            payload=AccountRequestedPayload(id=id),
            correlation_id=correlation_id,
        )

        await self.bus.publish(asdict(event))

        try:
            return await asyncio.wait_for(future, timeout=1)
        finally:
            self.pending_requests.pop(correlation_id, None)
