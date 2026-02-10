from pydantic import BaseModel, Field
from typing import Annotated


class UserAuthModel(BaseModel):
    login: str = Field(..., description="Логин пользователя")
    password: str = Field(..., description="Пароль пользователя")


class TokenResponse(BaseModel):
    access_token: str = Field(..., description="Основной токен (access)")
    refresh_token: str = Field(..., description="Для обновления access-токена'а")
