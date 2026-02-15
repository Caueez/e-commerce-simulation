from dataclasses import dataclass, field
import uuid

# ----------------------------------------------------------------------------
@dataclass
class Event:
    routing_key: str
    exchange_name: str
    idempotency_key: str

@dataclass
class Command:
    routing_key: str
    exchange_name: str
    idempotency_key: str
    correlation_id: str
# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
@dataclass
class AccountCreatedPayload:
    name: str
    email: str
    password: str

@dataclass
class AccountCreatedEvent:
    idempotency_key: str
    payload: AccountCreatedPayload
    routing_key: str = "account.created"
    exchange_name: str = "exchange"
# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------

@dataclass
class AccountRequestedPayload:
    id: str

@dataclass
class AccountRequestedCommand:
    idempotency_key: str
    payload: AccountRequestedPayload
    routing_key: str = "account.request"
    exchange_name: str = "exchange"
    correlation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    reply_to: str = "account.response"


@dataclass
class AccountResponsePayload:
    id: str
    name: str
    email: str


@dataclass
class AccountRespondedEvent:
    correlation_id: str
    payload: AccountResponsePayload
    routing_key: str = "account.response"
    exchange_name: str = "exchange"
# ----------------------------------------------------------------------------
