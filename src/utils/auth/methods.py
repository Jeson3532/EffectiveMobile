import jwt
from jwt.exceptions import PyJWTError, DecodeError, ExpiredSignatureError
from src.utils.security import handler
from src.utils.log import logger
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv
from typing import Annotated
from fastapi import HTTPException
from src.utils.enums.tokens import TokenType
from src.database.pg.methods import AuthMethods, AccountMethods
from src.backend.enums.http import HTTPDetail
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from src.backend.schemas.auth import UserVerifyModel
from src.backend.schemas.auth import TokenData
from src.utils.security.generator import generate_jti
from src.database.redis.handler import check_blacklist
load_dotenv()

auth_scheme = OAuth2PasswordBearer(tokenUrl="testing/auth")

_algorithms = ['HS256']
_SECRET_KEY = os.getenv("SECRET_KEY")

EXP_TIME_MIN_REFRESH = 4320
EXP_TIME_MIN_ACCESS = 300


def get_datetime(tz=timezone.utc):
    return datetime.now(tz=tz)


def generate_jwt_token(sub, user_id, exp_time_min: int = 60, token_type: TokenType = 'access', role: str = "user"):
    try:
        now = get_datetime()
        payload = {
            "sub": sub,
            "user_id": user_id,
            "role": role,
            "jti": generate_jti(),
            "type": token_type.value,
            "exp": now + timedelta(minutes=exp_time_min),
            "iat": now
        }
        return jwt.encode(payload=payload, key=_SECRET_KEY, algorithm=_algorithms[0])
    except PyJWTError as e:
        logger.error(f"Общая ошибка при генерации JWT-токена: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при попытке выдачи токена")


def update_access_token(refresh_token: str) -> Annotated[dict, "Присылает новый access-токен, если действует refresh"]:
    try:
        payload = jwt.decode(refresh_token, key=_SECRET_KEY, algorithms=_algorithms)

        token_type = payload.get("type", None)
        if token_type != 'refresh':
            raise HTTPException(status_code=401, detail="Прислан невалидный тип токена")
        sub = payload.get("sub", None)
        exp = payload.get("exp", None)
        if not sub or not exp:
            logger.error(f"Прислан refresh-токен с неполным payload: {payload}")
            raise HTTPException(status_code=500, detail="Произошла ошибка при попытке обработать токен")
        access_token = generate_jwt_token(sub=sub, exp_time_min=300, token_type=TokenType.ACCESS)
        return {"access_token": access_token}
    except DecodeError as e:
        logger.error(f"Ошибка при декодировании access-токена: {e}")
        raise HTTPException(status_code=401, detail="Ошибка при декодировании токена")
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Срок действия токена истёк")
    except PyJWTError as e:
        logger.error(f"Общая ошибка при генерации JWT-токена: {e}")
        raise HTTPException(status_code=401, detail="Ошибка при обработке токена")


async def verify_user(email: str, password: str) -> Annotated[dict, "Возвращает токен при успешной аутентификации"]:
    user = await AuthMethods.get_user_by_email(email.lower().strip(), model=UserVerifyModel)
    is_active = user.is_active

    if not is_active:
        raise HTTPException(status_code=404, detail=HTTPDetail.DETAIL_404_NOT_FOUND_USER)

    hash_user_pass = user.password
    user_id = user.id
    verified = handler.verify_password(password, hash_user_pass)
    if verified:
        access_token = generate_jwt_token(email, user_id, EXP_TIME_MIN_ACCESS, token_type=TokenType.ACCESS,
                                          role=user.role)
        refresh_token = generate_jwt_token(email, user_id, EXP_TIME_MIN_REFRESH, token_type=TokenType.REFRESH,
                                           role=user.role)
        return {"access_token": access_token, "refresh_token": refresh_token}
    raise HTTPException(status_code=401, detail=HTTPDetail.DETAIL_401_UNAUTHORIZED)


async def get_user(access_token: str = Depends(auth_scheme)) -> TokenData:
    try:
        payload = jwt.decode(access_token, key=_SECRET_KEY, algorithms=_algorithms)

        jti = payload.get("jti")
        if await check_blacklist(jti):
            raise HTTPException(status_code=401, detail="Сессия не найдена")
        user_id = payload.get("user_id")
        token_type = payload.get("type")
        if token_type != TokenType.ACCESS.value:
            raise HTTPException(status_code=400, detail="Токен не распознан")
        if not await AccountMethods.account_is_active(user_id):
            raise HTTPException(status_code=404, detail=HTTPDetail.DETAIL_404_NOT_FOUND_USER)
        return TokenData(**payload)
    except DecodeError as e:
        logger.error(f"Ошибка при декодировании access-токена: {e}")
        raise HTTPException(status_code=401, detail="Ошибка при декодировании токена")
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Срок действия токена истёк")
