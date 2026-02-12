from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, Response, Request
from src.utils.auth import methods as auth_methods
from src.backend.schemas.auth import TokenData
from src.utils.auth.permissions import RightsChecker

router = APIRouter(prefix='/testing', tags=['Тестирование', 'Testing'])


@router.post("/auth", description="Ручка для тестирования входа/выхода из аккаунта")
async def login(response: Response, auth_form=Depends(OAuth2PasswordRequestForm)):
    tokens = await auth_methods.verify_user(auth_form.username, auth_form.password)
    response.set_cookie("refresh_token", tokens.get("refresh_token"),
                        httponly=True,
                        max_age=4320 * 60)
    return tokens


@router.get("/parseToken", description="Ручка для проверки payload токена", )
async def _(user: TokenData = Depends(RightsChecker("testing.parseToken"))):
    return user


@router.get("/getCookie", description="Ручка для проверки содержимого куков", )
async def _(request: Request, user: TokenData = Depends(RightsChecker("testing.readCookies"))):
    return request.cookies
