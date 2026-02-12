from pydantic import BaseModel, Field, EmailStr, ConfigDict, model_validator
from typing import Annotated


class UserAuthModel(BaseModel):
    email: EmailStr = Field(..., description="Логин пользователя (e-mail)")
    password: str = Field(..., description="Пароль пользователя")


class TokenResponse(BaseModel):
    access_token: str = Field(..., description="Основной токен (access)")
    refresh_token: str = Field(..., description="Для обновления access-токена'а")


class UserRegModel(BaseModel):
    username: str = Field(..., min_length=4)
    first_name: str = Field(...)
    last_name: str = Field(...)
    middle_name: str | None = Field(default=None)
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=8, max_length=48)
    repeat_password: str = Field(...)

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode='after')
    def check_password(self):
        if self.password != self.repeat_password:
            raise ValueError("Пароли не совпадают, проверьте правильность введеного пароля")
        return self


class UserRegResponse(BaseModel):
    username: str = Field(...)
    first_name: str = Field(...)
    last_name: str = Field(...)
    middle_name: str | None = Field(default=None)
    email: EmailStr = Field(...)


class UserVerifyModel(BaseModel):
    id: int = Field(...)
    username: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    role: str = Field()
    is_active: bool = Field(...)

    model_config = ConfigDict(from_attributes=True)


class TokenData(BaseModel):
    sub: str = Field(...)
    role: str = Field(...)
    type: str = Field(...)
    jti: str = Field(...)
    user_id: int = Field(...)
    exp: int = Field(...)
    iat: int = Field(...)

    model_config = ConfigDict(from_attributes=True)
