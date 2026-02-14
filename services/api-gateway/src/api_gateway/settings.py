
from core.config.settings import Settings

from pydantic import BaseModel


class DBConfig(BaseModel):
    host: str
    port: str
    user: str
    password: str
    dbname: str


class MessageringConfig(BaseModel):
    url: str


class RedisConfig(BaseModel):
    host: str
    port: str

class ApiGatewaySettings(Settings):

    DB_ENV: DBConfig
    CACHE_ENV: RedisConfig
    MESSAGERING_ENV: MessageringConfig