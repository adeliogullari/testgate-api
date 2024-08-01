from typing import Any, AsyncGenerator
from config import Settings
from redis.asyncio.client import Redis, ConnectionPool

settings = Settings()

host = settings.testgate_redis_host
port = settings.testgate_redis_port
username = settings.testgate_redis_username
password = settings.testgate_redis_password

connection_pool = ConnectionPool(
    host=host, port=port, username=username, password=password
)


async def get_redis_client() -> AsyncGenerator[Redis, Any]:
    async with Redis(connection_pool=connection_pool) as client:
        yield client
