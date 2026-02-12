from redis.asyncio import Redis, ConnectionPool
import platform
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = "localhost" if platform.system() == "Windows" else os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")

pool = ConnectionPool(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=0,
    decode_responses=True
)


def get_redis_client() -> Redis:
    return Redis(connection_pool=pool)
