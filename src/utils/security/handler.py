from pwdlib import PasswordHash
from pwdlib.exceptions import UnknownHashError, HasherNotAvailable
from src.utils.log import logger
from fastapi import HTTPException

pwd = PasswordHash.recommended()


def hash_password(password: str) -> str:
    try:
        return pwd.hash(password)
    except HasherNotAvailable as e:
        logger.error(f"Ошибка с хешером: {e}")
        raise HTTPException(status_code=500, detail="Произошла ошибка при регистрации аккаунта, попробуйте позже")


def verify_password(password: str, hashed_password: str) -> bool:
    try:
        return pwd.verify(password, hashed_password)
    except UnknownHashError as e:
        logger.error(f"Неверный хеш в базе: {hashed_password}, лог ошибки: {e}")
        raise HTTPException(status_code=500, detail="Произошла ошибка при попытке входа в аккаунт, попробуйте позже")
