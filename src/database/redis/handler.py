from src.database.redis.client import get_redis_client
from typing import Annotated, Any, Union
from redis.exceptions import RedisError
from datetime import timedelta, datetime, timezone
import logging
from src.utils.log import logger
from fastapi import HTTPException


async def add_token_in_blacklist(jti: str, exp: int):
    try:
        now = datetime.now(timezone.utc).timestamp()
        ttl = int(exp - now)

        if ttl <= 0:
            return True

        async with get_redis_client() as client:
            await client.setex(f"bl:{jti}",
                               timedelta(minutes=ttl), "true")
    except RedisError as e:
        logger.error(f"Ошибка с Redis: {e}")
        raise HTTPException(status_code=500,
                            detail="Произошла непредвиденная ошибка, попробуйте выполнить операцию позже")


async def check_blacklist(jti: str):
    try:
        async with get_redis_client() as client:
            return await client.exists(f"bl:{jti}")
    except RedisError as e:
        logger.error(f"Ошибка с Redis: {e}")
        raise HTTPException(status_code=500,
                            detail="Произошла непредвиденная ошибка, попробуйте выполнить операцию позже")
