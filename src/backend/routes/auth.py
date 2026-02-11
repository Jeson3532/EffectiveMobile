from fastapi import APIRouter, Body, HTTPException, Response
from src.backend.schemas import auth as auth_schema
from src.utils.auth import methods as auth_methods
from src.database.pg.methods import AuthMethods

router = APIRouter(prefix="/auth", tags=['Аутентификация', 'Authentication'])


@router.post("/register", response_model=auth_schema.UserRegResponse, description="Регистрация нового аккаунта в системе")
async def register(reg_form: auth_schema.UserRegModel = Body(...)):
    user = await AuthMethods.register_user(reg_form)
    return user


@router.post("", response_model=auth_schema.TokenResponse, description="Вход в аккаунт")
async def login(response: Response, auth_form: auth_schema.UserAuthModel = Body(...)):
    tokens = await auth_methods.verify_user(auth_form.email, auth_form.password)
    response.set_cookie("refresh_token", tokens.get("refresh_token"),
                        httponly=True,
                        max_age=4320 * 60)
    return tokens

